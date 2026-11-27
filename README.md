# Clash Rules Lite（Mihomo / Karing 全量聚合零冲突版）

自用轻量级 Clash / Mihomo / Karing 规则聚合与编译仓库：
- **云端全量聚合与去重**：通过 [`bundles.yaml`](./bundles.yaml) + [`scripts/build_bundles.py`](./scripts/build_bundles.py)，每天定时及每次推送自动拉取 `MetaCubeX/meta-rules-dat` 上游源码，与 [`rules/*.yaml`](./rules) 中的个人增量规则合并、去重并**自动剔除跨组冲突**（例如从系统服务中自动减除 `github` 与 `@cn` 子集、从金融集合中自动剔除 `.cn` 与 Web3 交集）。
- **双格式统一托管**：由 GitHub Actions 自动编译为 Mihomo `.mrs` 二进制规则集与 Karing/通用 `.yaml` 规则集，推送至 `release` 分支并刷新 jsDelivr CDN，本地配置不再零散引用任何第三方规则源。

---

## 一、在线聚合规则集直链（`@release` 分支）

| 规则集 | 行为 | 用途与包含内容 | Mihomo (`.mrs`) | Karing / 通用 (`.yaml`) |
| :--- | :---: | :--- | :--- | :--- |
| `reject-all` | domain | 运营商追踪拦截（个人拦截源码） | `https://fastly.jsdelivr.net/gh/yzy19950807/clash-rules-lite@release/reject-all.mrs` | `https://fastly.jsdelivr.net/gh/yzy19950807/clash-rules-lite@release/reject-all.yaml` |
| `private-domain` | domain | 局域网与保留域名（`private`） | `https://fastly.jsdelivr.net/gh/yzy19950807/clash-rules-lite@release/private-domain.mrs` | `https://fastly.jsdelivr.net/gh/yzy19950807/clash-rules-lite@release/private-domain.yaml` |
| `google-cn-fix` | domain | Google CN CDN 修复（`googleapis.cn`、`xn--ngstr-lra8j.com`） | `https://fastly.jsdelivr.net/gh/yzy19950807/clash-rules-lite@release/google-cn-fix.mrs` | `https://fastly.jsdelivr.net/gh/yzy19950807/clash-rules-lite@release/google-cn-fix.yaml` |
| `direct-cn-all` | domain | `cn` + `geolocation-cn` + `@cn` CDN + 国内银行/B站 + 个人直连（已剔除 `google-cn-fix`） | `https://fastly.jsdelivr.net/gh/yzy19950807/clash-rules-lite@release/direct-cn-all.mrs` | `https://fastly.jsdelivr.net/gh/yzy19950807/clash-rules-lite@release/direct-cn-all.yaml` |
| `pay-all` | domain | PayPal / Stripe / Wise / RedotPay / SafePal / Visa / Mastercard / HSBC / 渣打 / 国际金融（已剔除 `.cn` 与 Web3） | `https://fastly.jsdelivr.net/gh/yzy19950807/clash-rules-lite@release/pay-all.mrs` | `https://fastly.jsdelivr.net/gh/yzy19950807/clash-rules-lite@release/pay-all.yaml` |
| `web3-all` | domain | `category-cryptocurrency` + 链上钱包扩展 | `https://fastly.jsdelivr.net/gh/yzy19950807/clash-rules-lite@release/web3-all.mrs` | `https://fastly.jsdelivr.net/gh/yzy19950807/clash-rules-lite@release/web3-all.yaml` |
| `media-all` | domain | YouTube / Netflix / Disney+ / Twitch / Spotify / Prime Video / HBO | `https://fastly.jsdelivr.net/gh/yzy19950807/clash-rules-lite@release/media-all.mrs` | `https://fastly.jsdelivr.net/gh/yzy19950807/clash-rules-lite@release/media-all.yaml` |
| `googlefcm` | domain | Google FCM 推送 | `https://fastly.jsdelivr.net/gh/yzy19950807/clash-rules-lite@release/googlefcm.mrs` | `https://fastly.jsdelivr.net/gh/yzy19950807/clash-rules-lite@release/googlefcm.yaml` |
| `google-meta-all` | domain | Meta（含去重后的 WhatsApp / Instagram）+ Google（已剔除 `media-all` 与 `googlefcm`） | `https://fastly.jsdelivr.net/gh/yzy19950807/clash-rules-lite@release/google-meta-all.mrs` | `https://fastly.jsdelivr.net/gh/yzy19950807/clash-rules-lite@release/google-meta-all.yaml` |
| `tiktok` | domain | TikTok 独立运营域名 | `https://fastly.jsdelivr.net/gh/yzy19950807/clash-rules-lite@release/tiktok.mrs` | `https://fastly.jsdelivr.net/gh/yzy19950807/clash-rules-lite@release/tiktok.yaml` |
| `social-all` | domain | LinkedIn / X(Twitter) / Telegram / Discord / Reddit / Pinterest | `https://fastly.jsdelivr.net/gh/yzy19950807/clash-rules-lite@release/social-all.mrs` | `https://fastly.jsdelivr.net/gh/yzy19950807/clash-rules-lite@release/social-all.yaml` |
| `ai-all` | domain | `category-ai-!cn` + Notion（已剔除金融/Web3/Google-Meta 交集） | `https://fastly.jsdelivr.net/gh/yzy19950807/clash-rules-lite@release/ai-all.mrs` | `https://fastly.jsdelivr.net/gh/yzy19950807/clash-rules-lite@release/ai-all.yaml` |
| `github` | domain | GitHub 独立域名（已剔除 AI 交集，独立走日常代理） | `https://fastly.jsdelivr.net/gh/yzy19950807/clash-rules-lite@release/github.mrs` | `https://fastly.jsdelivr.net/gh/yzy19950807/clash-rules-lite@release/github.yaml` |
| `system-all` | domain | Apple / Microsoft / Samsung 非 CN 流量（已剔除 `direct-cn-all`、`github`、`ai-all`） | `https://fastly.jsdelivr.net/gh/yzy19950807/clash-rules-lite@release/system-all.mrs` | `https://fastly.jsdelivr.net/gh/yzy19950807/clash-rules-lite@release/system-all.yaml` |
| `noncn-all` | domain | 其余已知海外域名（`geolocation-!cn` 减去上述所有专属业务集） | `https://fastly.jsdelivr.net/gh/yzy19950807/clash-rules-lite@release/noncn-all.mrs` | `https://fastly.jsdelivr.net/gh/yzy19950807/clash-rules-lite@release/noncn-all.yaml` |
| `private-ip` | ipcidr | 局域网与保留 IP 段 | `https://fastly.jsdelivr.net/gh/yzy19950807/clash-rules-lite@release/private-ip.mrs` | `https://fastly.jsdelivr.net/gh/yzy19950807/clash-rules-lite@release/private-ip.yaml` |
| `meta-ip` | ipcidr | Meta / WhatsApp / IG AS IP 段（防 App 直连 IP 漏网） | `https://fastly.jsdelivr.net/gh/yzy19950807/clash-rules-lite@release/meta-ip.mrs` | `https://fastly.jsdelivr.net/gh/yzy19950807/clash-rules-lite@release/meta-ip.yaml` |
| `media-ip` | ipcidr | Netflix AS IP 段（防 App 直连 IP 漏网） | `https://fastly.jsdelivr.net/gh/yzy19950807/clash-rules-lite@release/media-ip.mrs` | `https://fastly.jsdelivr.net/gh/yzy19950807/clash-rules-lite@release/media-ip.yaml` |
| `social-ip` | ipcidr | Telegram + X(Twitter) 专用 IP 段 | `https://fastly.jsdelivr.net/gh/yzy19950807/clash-rules-lite@release/social-ip.mrs` | `https://fastly.jsdelivr.net/gh/yzy19950807/clash-rules-lite@release/social-ip.yaml` |
| `cn-ip` | ipcidr | 中国大陆全量 IPv4/IPv6 段 | `https://fastly.jsdelivr.net/gh/yzy19950807/clash-rules-lite@release/cn-ip.mrs` | `https://fastly.jsdelivr.net/gh/yzy19950807/clash-rules-lite@release/cn-ip.yaml` |
| `fakeip-filter` | domain | Mihomo Fake-IP 排除清单（CI 自动镜像） | `https://fastly.jsdelivr.net/gh/yzy19950807/clash-rules-lite@release/fakeip-filter.mrs` | — |

---

## 二、完全脱敏配置模板

- [`templates/clash-verge-mihomo.yaml`](./templates/clash-verge-mihomo.yaml)：**Clash Verge Rev（Mihomo 内核）推荐版**（22 个全手动 `select` 策略组、21 个自托管 `.mrs`、23 条极简规则、零泄露 Fake-IP DNS）。
- [`templates/karing-universal.yaml`](./templates/karing-universal.yaml)：**Karing（sing-box）& Clash Verge Rev 通用版**（20 个自托管 `.yaml` 规则集、23 条极简规则）。

### 使用方式
1. 下载或复制对应模板到本地；
2. 将 `proxies:` 中的示例占位节点（`🇺🇸 US-Node-01`、`🔗 Relay-Node-01` 等）替换为你的真实节点或链式节点，并同步调整策略组中的引用；
3. 将 `proxy-providers:` 中的占位 URL 替换为你的真实订阅链接；
4. 日后只需在 GitHub 上编辑 `rules/*.yaml` 或 `bundles.yaml` 并提交，Actions 会自动重新聚合去重、编译 `.mrs` 并刷新 CDN，各设备客户端刷新 `rule-providers` 即可同步生效。
