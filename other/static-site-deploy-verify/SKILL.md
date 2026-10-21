---
name: static-site-deploy-verify
description: 静态站（GitHub Pages / Cloudflare Pages / 任意 CDN）推完之后做一次到位校验，专门抓"缓存名 bump 了但文件内容还是旧的"这类版本撕裂。适用于用户说"我更新了但线上还是老样子""帮我确认线上是不是最新的""推完再验一遍"。
version: 1.0.0
---

# 静态站部署后校验

## 何时用
- 用户反馈「我改了但线上没变」「还是上个版本」
- 刚刚推送完静态站，用户要求确认线上是最新的
- Service Worker / PWA 项目，怀疑缓存没失效

## 核心洞察：版本撕裂
只 bump 缓存名而不推齐文件 = **缓存名是新的、内容还是旧的**，用户端会长期命中旧缓存，表现为"我改了没效果"。

修复必须**两步一起做**：
1. 把所有不一致的文件推齐
2. 把 `sw.js` 里的 `const CACHE` 再 bump 一次（不 bump 的话用户端仍命中旧缓存）

## 铁律：判断线上版本用 GitHub API 查文件，不信本地 git log
MCP `push_files` 之类的推送**不产生本地 commit**，所以 `git log` 会停在旧版本，误判成"线上版本不明"。
要确认线上是什么版本，直接查远端文件：

```bash
curl -s "https://api.github.com/repos/<owner>/<repo>/contents/<path>?ref=main"
```

## 标准流程

### 1. 先跑一遍五类检查
| # | 检查项 | 做什么 |
|---|---|---|
| 1 | **漏推** | 本地有的文件远端没有 |
| 2 | **内容不一致** | 同名文件本地/远端 size 或 sha 不同（这是版本撕裂的根因） |
| 3 | **SW 缓存清单** | `sw.js` 里列出的文件是否与实际部署的文件对齐 |
| 4 | **HTML 引用** | `index.html` 引用的 css/js/img 是否全部存在（防 404） |
| 5 | **PWA 三件套** | manifest.json / sw.js / icon 是否齐全且互相引用一致 |

### 2. 具体做法
```bash
# 拿远端文件清单 + size/sha
curl -s "https://api.github.com/repos/<owner>/<repo>/git/trees/main?recursive=1"

# 逐个比对本地 size
# 注意：>1MB 的文件 contents API 不返回 base64（encoding: none）
#       要改用 GET /repos/<owner>/<repo>/git/blobs/<sha>
```

### 3. 修复后必须强刷验证
改完让用户 **Ctrl+Shift+R**（不是 F5，F5 可能仍走内存缓存）再看。
⚠️ 这一步**必须由人在浏览器里做**，AI 无法代验——本机网络能否访问目标域名跟线上是否可用是两回事。

### 4. 判断"到底是网络问题还是站点挂了"
```bash
nslookup <domain>
```
- 解析到 **185.199.x** → GitHub Pages 真实 IP，正常
- 解析到 **31.13.x / 2a03:2880:** → 这是 **Meta/Facebook 的 IP 段**，说明 DNS 被劫持/污染，**不代表站点故障**
- 全部超时 → 换手机流量或非公司网再验一次再说

## Example

> 用户：「我更新了 TalkCal 的 css，但线上还是老样子。」

1. API 查远端 `css/style.css` 的 size，对比本地 → 发现本地 20987 B / 远端 18035 B，**内容不一致**
2. 同时查 `js/calendar.js` → 同样不一致
3. 检查 `sw.js` 的 `const CACHE` → 已经是 `talkcal-v2.6.1`（说明之前只 bump 了缓存名没推内容）
4. 修复：推齐两个文件 **+** CACHE bump 到 `talkcal-v2.6.2`
5. 等 CDN 自动重新部署，跑一遍第 1 步的五类检查确认全部对齐
6. 让用户 Ctrl+Shift+R 验收

## 坑位清单
- `curl` 在公司网络下可能需要 `--noproxy '*'`，否则拿到假的连接失败
- 本机测不到的域名**不代表线上挂了**（`*.workers.dev` / `*.supabase.co` 常被公司 DNS 拦）
- 改 `sw.js` 缓存名但忘记推文件内容 = 白改；推了内容但忘记 bump = 用户端还是旧的
- 本地 git 历史与线上 API commit 分叉（如 `ahead 1`）时，先确认内容一致再决定是否 `git reset --hard origin/main`，**不要擅自 reset**

## 隐私与边界
只读远端公开文件 + 本地文件比对。不读取、不输出任何 token 明文；PAT 走本机凭据管理器。
