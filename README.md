# Clash Rules Lite（Mihomo / Karing 精简零风险版）

自用轻量级 Clash / Mihomo / Karing 规则托管仓库：
- 仅维护**纯 `domain` 规则源文件（`rules/*.yaml`）**，通过 GitHub Actions 自动编译为 Mihomo `.mrs` 二进制规则集与通用 `.yaml` 规则集，发布到 `release` 分支并自动刷新 jsDelivr CDN。
- 搭配社区预编译基础库（`appshubcc/bett-rules`、`MetaCubeX/meta-rules-dat`），彻底替代冗长的手工 `KEYWORD` 与 GFWList 规则，显著降低本地 CPU 与内存占用。

---

## 一、在线规则集直链（`@release` 分支）

| 规则集 | 用途 | Mihomo (`.mrs`) | Karing / 通用 (`.yaml`) |
| :--- | :--- | :--- | :--- |
| `direct-cn-extra` | 国内银行/支付/政务补充、Oracle、LAN `.home` 等直连扩展 | `https://fastly.jsdelivr.net/gh/yzy19950807/clash-rules-lite@release/direct-cn-extra.mrs` | `https://fastly.jsdelivr.net/gh/yzy19950807/clash-rules-lite@release/direct-cn-extra.yaml` |
| `bank-pay-extra` | 跨境 B2B 支付与外贸收款补充（Airwallex / Payoneer / PingPong / WorldFirst / Mercury / SafePal） | `https://fastly.jsdelivr.net/gh/yzy19950807/clash-rules-lite@release/bank-pay-extra.mrs` | `https://fastly.jsdelivr.net/gh/yzy19950807/clash-rules-lite@release/bank-pay-extra.yaml` |
| `web3-extra` | 链上钱包与浏览器补充（TokenPocket / imToken / TronLink / Phantom / Ledger） | `https://fastly.jsdelivr.net/gh/yzy19950807/clash-rules-lite@release/web3-extra.mrs` | `https://fastly.jsdelivr.net/gh/yzy19950807/clash-rules-lite@release/web3-extra.yaml` |
| `google-cn-fix` | Google CN CDN 修复（`googleapis.cn`、`xn--ngstr-lra8j.com`） | `https://fastly.jsdelivr.net/gh/yzy19950807/clash-rules-lite@release/google-cn-fix.mrs` | `https://fastly.jsdelivr.net/gh/yzy19950807/clash-rules-lite@release/google-cn-fix.yaml` |
| `reject-extra` | 运营商追踪域名拦截 | `https://fastly.jsdelivr.net/gh/yzy19950807/clash-rules-lite@release/reject-extra.mrs` | `https://fastly.jsdelivr.net/gh/yzy19950807/clash-rules-lite@release/reject-extra.yaml` |

---

## 二、完全脱敏配置模板

- [`templates/clash-verge-mihomo.yaml`](./templates/clash-verge-mihomo.yaml)：**Clash Verge Rev（Mihomo 内核）推荐版**（22 个全手动 `select` 策略组、全量 `.mrs`、零泄露 Fake-IP DNS）。
- [`templates/karing-universal.yaml`](./templates/karing-universal.yaml)：**Karing（sing-box）& Clash Verge Rev 通用版**（标准 `.yaml` 规则集）。

### 使用方式
1. 下载或复制对应模板到本地；
2. 将 `proxies:` 中的示例占位节点替换为你的真实自建/链式节点；
3. 将 `proxy-providers:` 中的占位 URL 替换为你的真实机场订阅链接；
4. 日后只需在 GitHub 上编辑 `rules/*.yaml` 并提交，Actions 会自动重新编译 `.mrs` 并刷新 CDN，各设备客户端刷新 `rule-providers` 即可同步生效。
