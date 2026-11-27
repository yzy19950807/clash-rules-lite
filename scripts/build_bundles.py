#!/usr/bin/env python3
"""Fetch upstream MetaCubeX rulesets, merge with local rules, deduplicate, resolve conflicts, and write YAML bundles."""

import argparse
import os
import subprocess
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor

UPSTREAM_BASES = [
    "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo",
    "https://fastly.jsdelivr.net/gh/MetaCubeX/meta-rules-dat@meta/geo",
]


def parse_bundles_yaml(path):
    """Parse the constrained structure of bundles.yaml using only Python stdlib."""
    data = {"domain_bundles": {}, "ipcidr_bundles": {}}
    top = None
    bundle = None
    section = None

    with open(path, "r", encoding="utf-8") as f:
        for raw in f:
            line = raw.split("#", 1)[0].rstrip()
            if not line.strip():
                continue
            indent = len(line) - len(line.lstrip())
            stripped = line.strip()

            if indent == 0 and stripped.endswith(":"):
                top = stripped[:-1]
                data.setdefault(top, {})
                bundle = None
                section = None
            elif indent == 2 and stripped.endswith(":"):
                bundle = stripped[:-1]
                data[top][bundle] = {
                    "local": [],
                    "upstream": [],
                    "exclude_bundles": [],
                    "exclude_cn_tld": False,
                }
                section = None
            elif indent == 4 and ":" in stripped:
                key, val = [x.strip() for x in stripped.split(":", 1)]
                if val:
                    data[top][bundle][key] = val.lower() == "true"
                    section = None
                else:
                    section = key
            elif indent == 6 and stripped.startswith("- "):
                item = stripped[2:].strip().strip("'\"")
                data[top][bundle][section].append(item)
            else:
                raise ValueError(f"Unsupported line in {path}: {raw!r}")
    return data


def parse_payload_lines(text):
    """Extract payload items from a Mihomo domain/ipcidr YAML file."""
    items = []
    in_payload = False
    for raw in text.splitlines():
        s = raw.strip()
        if not s or s.startswith("#"):
            continue
        if s == "payload:":
            in_payload = True
            continue
        if in_payload and s.startswith("- "):
            val = s[2:].strip()
            if (val.startswith("'") and val.endswith("'")) or (val.startswith('"') and val.endswith('"')):
                val = val[1:-1]
            # Strip inline comments if unquoted
            if " #" in val:
                val = val.split(" #", 1)[0].strip()
            if val and "," not in val:
                items.append(val)
    return items


def fetch_upstream(key, cache):
    if key in cache:
        return cache[key]
    last_err = None
    for base in UPSTREAM_BASES:
        url = f"{base}/{key}.yaml"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "clash-rules-lite-builder/1.0"})
            with urllib.request.urlopen(req, timeout=20) as resp:
                txt = resp.read().decode("utf-8")
            items = parse_payload_lines(txt)
            if not items:
                raise ValueError(f"Empty payload from {url}")
            cache[key] = items
            return items
        except (urllib.error.URLError, ValueError, TimeoutError) as e:
            last_err = e
    raise RuntimeError(f"Failed to fetch upstream {key}: {last_err}")


def write_yaml_payload(out_path, items):
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("payload:\n")
        for item in sorted(items):
            f.write(f'  - "{item}"\n')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--out-dir", default="publish")
    parser.add_argument("--mihomo", default="")
    args = parser.parse_args()

    cfg = parse_bundles_yaml(os.path.join(args.repo_root, "bundles.yaml"))
    os.makedirs(args.out_dir, exist_ok=True)

    # Pre-fetch all upstream sources concurrently
    all_upstream = set()
    for group_type in ("domain_bundles", "ipcidr_bundles"):
        for spec in cfg[group_type].values():
            all_upstream.update(spec["upstream"])

    cache = {}
    with ThreadPoolExecutor(max_workers=8) as pool:
        futures = {k: pool.submit(fetch_upstream, k, {}) for k in sorted(all_upstream)}
        for k, fut in futures.items():
            cache[k] = fut.result()
    print(f"Fetched {len(cache)} upstream rulesets.")

    built_sets = {}

    for behavior, group_type in (("domain", "domain_bundles"), ("ipcidr", "ipcidr_bundles")):
        for name, spec in cfg[group_type].items():
            items = set()
            for rel in spec["local"]:
                p = os.path.join(args.repo_root, rel)
                with open(p, "r", encoding="utf-8") as f:
                    items.update(parse_payload_lines(f.read()))
            for uk in spec["upstream"]:
                items.update(cache[uk])

            if spec.get("exclude_cn_tld"):
                items = {x for x in items if not (x == "cn" or x.endswith(".cn"))}

            for ex in spec["exclude_bundles"]:
                if ex not in built_sets:
                    raise KeyError(f"Bundle {name} excludes {ex} which has not been built yet (check order in bundles.yaml)")
                items -= built_sets[ex]

            if not items:
                raise RuntimeError(f"Bundle {name} ended up empty!")

            built_sets[name] = items
            yaml_path = os.path.join(args.out_dir, f"{name}.yaml")
            write_yaml_payload(yaml_path, items)

            if args.mihomo:
                mrs_path = os.path.join(args.out_dir, f"{name}.mrs")
                subprocess.run(
                    [args.mihomo, "convert-ruleset", behavior, "yaml", yaml_path, mrs_path],
                    check=True,
                )
                if os.path.getsize(mrs_path) == 0:
                    raise RuntimeError(f"Compiled {mrs_path} is empty")
            print(f"[{behavior}] {name}: {len(items)} unique entries")


if __name__ == "__main__":
    main()
