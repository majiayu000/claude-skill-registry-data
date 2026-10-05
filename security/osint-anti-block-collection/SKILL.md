---
name: osint-anti-block-collection
description: 反拦截情报搜集 — 五层防拦截采集体系（出口轮换/指纹伪装/行为节流/多源降级/OPSEC 被动优先）。使用当爬取或情报采集被 WAF/反爬/平台风控/GFW 拦截时，或需要隐蔽被动侦察。含 curl_cffi 伪装、Tor/代理轮换、指数退避、Wayback 降级链脚本。调用前必须先经 router 选择。
version: 1.0.0
domain: security
subdomain: osint
license: MIT (user-owned)
tags:
- osint
- anti-block
- stealth
- reconnaissance
- intelligence-gathering
- curl-cffi
- evasion
---

# 反拦截情报搜集 (osint-anti-block-collection)

## 何时使用（触发信号）

- 爬取/采集时被 **WAF 或反爬**拦截：403/429、验证码挑战、返回假数据、IP 被封
- **平台风控**：社媒/接口频控、账号限流、需登录墙
- **GFW / 网络层封锁**：情报源（Telegram 频道、paste 站、论坛）访问不通
- **隐蔽性**：不想在目标侧留痕，需要纯被动视角采集
- 与 `security:acs-security-library` 的 OSINT 技能互补：**它们管"查什么"，本技能管"怎么查不被拦"**

**不用于**：主动攻击/扫描（走 kali-pentest / acs 技能）；未授权目标（见下方边界）。

## 边界（用户授权框架）

- 仅限**授权范围**内的情报采集（用户声明的目标/环境即可，与 AGENTS.md 授权框架一致）
- 本技能是采集工程层，不做漏洞利用；采集到的数据仅用于授权目的
- 节流与降级是默认行为——不主动对抗验证码、不暴力绕过登录墙

## 五层架构（拦截在哪一层发生，就在哪层解决）

| 层 | 拦截威胁 | 对策 | 实现 |
|---|---|---|---|
| 1 出口层 | GFW / 目标按 IP 封禁 | 出口轮换 | Shadowrocket 隧道（本机常开）→ Tor 电路 → 代理列表轮换 |
| 2 指纹层 | WAF 识别 TLS/HTTP2 指纹 | 伪装真实浏览器 | `curl_cffi` impersonate（chrome/firefox/safari 系列） |
| 3 行为层 | 平台风控（频控/限流） | 节流+退避+随机化 | `scripts/stealth_fetch.py` 内置策略 |
| 4 源层 | 主源被拦/假数据 | 多源降级链 | `scripts/fallback_chain.py` + `references/sources.md` |
| 5 OPSEC 层 | 目标侧留痕 | 被动优先 | 流程纪律（见下） |

## 快速开始

```bash
VENV=~/.hermes/venvs/osint   # 已建好，含 curl_cffi
$VENV/bin/python scripts/stealth_fetch.py -u "https://example.com" -i chrome131
# 指纹伪装抓取，自动节流+重试+指数退避

$VENV/bin/python scripts/fallback_chain.py -t example.com
# 多源降级链：主源 → 备用 → Wayback → 搜索缓存
```

## Step 1 — 出口层：选出口

按隐蔽性递增排列（默认从 Shadowrocket 开始，够用不折腾）：

1. **Shadowrocket 隧道（默认）**：本机常开，全流量走隧道、出口北美。直接可用，无需配置。
   - 注意：共享出口 IP 易被 Cloudflare 类标记 → 配合指纹层（curl_cffi）补短板
2. **Tor（需要时安装）**：`brew install tor`，启动后 `socks5://127.0.0.1:9050`
   - 电路轮换：`echo -e "AUTHENTICATE\r\nSIGNAL NEWNYM\r\nQUIT" | nc 127.0.0.1 9051`
   - 每次请求前轮换电路（`stealth_fetch.py --tor --newnym`）
3. **代理列表轮换**：文本文件每行一个 `socks5://host:port` 或 `http://user:pass@host:port`，`--proxy-file proxies.txt --rotate` 每次请求换一个
   - 商业代理池（Bright Data 类）按需配置，key 存环境变量不写死

## Step 2 — 指纹层：curl_cffi 伪装

`curl_cffi` 模拟真实浏览器的 **TLS 指纹 + HTTP2 指纹 + 请求头**，WAF 无法从握手层区分。

```python
from curl_cffi import requests
r = requests.get(url, impersonate="chrome131", timeout=20, proxies=...)  # 或 firefox133/safari18_0
```

- 可用指纹：`chrome99..chrome131`、`firefox109..firefox133`、`safari17_0/18_0`、`edge101`
- **403/400 时换指纹重试**：Cloudflare 常只放行特定版本
- 需要 JS 渲染（SPA/挑战页）→ 换用 `patchright`（playwright 反检测分支，按需安装）

## Step 3 — 行为层：节流与退避（内置在脚本）

- 默认：请求间隔 1.5–4.5s 随机抖动；429/503 指数退避（1s→2s→4s→8s，上限 30s）
- 单目标并发 ≤ 2；批量任务总时长预估后分片跑
- 请求头随机化：UA 从指纹对应列表选、Accept-Language 轮换、Sec-CH-UA 顺带
- **账号类操作（登录/发帖）绝不自动重试**——高频重试是封号第一诱因

## Step 4 — 源层：多源降级链

主源被拦 → 自动降级，不中断采集。链定义在 `references/sources.md`，脚本读取执行：

```
主源（直连/指纹伪装）→ 备用镜像 → Wayback Machine → 搜索引擎缓存 → 第三方索引（Shodan/crt.sh/OTX）
```

`fallback_chain.py -t <target>` 对每个情报项按链依次尝试，返回第一个成功源 + 标注来源。

## Step 5 — OPSEC 层：被动优先纪律

1. **先被动后主动**：优先用第三方视角（Shodan 索引、证书透明日志、Wayback、DNS 历史）看目标，不直连
2. **必须直连时**：用一次性出口（Tor 新电路 / 未复用代理）
3. **不留痕**：不提交表单、不触发交互、单请求单目标
4. **数据纪律**：降级链返回的每个结果带来源标注，交叉验证 2 源以上再采信

## 脚本

| 脚本 | 用途 | 示例 |
|---|---|---|
| `scripts/stealth_fetch.py` | 指纹伪装单次/批量抓取（节流+退避+代理/Tor） | `-u URL -i chrome131 --tor` / `-f urls.txt -o out/` |
| `scripts/fallback_chain.py` | 多源降级链采集 | `-t example.com` |
| `references/sources.md` | 情报源清单 + 降级链定义 | 编辑后 fallback_chain 自动读取 |

## 验证

- 指纹伪装生效：`stealth_fetch.py -u "https://tls.peet.ws/api/all" -i chrome131` 返回的 TLS 指纹应显示为真实 Chrome 特征（非 curl/python）
- 降级链生效：断网主源或用 `--fail-first` 模拟主源失败，观察自动切到 Wayback
- 节流生效：批量抓 10 个 URL，时间戳间隔应 ≥ 1.5s

## 联动

- 方法论层（查什么）：`security:acs-security-library` → conducting-external-reconnaissance-with-osint / performing-osint-with-spiderfoot 等 7 个 OSINT 技能
- 浏览器自动化（需要 JS/交互）：`tools:browser`
- MCP 封装：`osint-collector` MCP（同一套逻辑，agent 直接调）
