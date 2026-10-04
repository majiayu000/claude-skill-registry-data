---
name: badboy-br-aa-routing
description: "BadBoy / browser-harness / Hermes browser / anything-analyzer 四路分流。解决何时直控真实 Chrome，何时走 AA CDP，何时走 Hermes 中介取证，何时仅用 AA 离线分析。"
triggers:
  - badboy
  - badboy browser
  - badboy analyzer
  - AA
  - anything-analyzer
  - browser harness
  - 真实 chrome
  - 真实浏览器
  - cdp
  - 当前页面
  - 登录态分析
  - 华容道脚本
  - tampermonkey 脚本
  - userscript 调试
  - 给 aa
  - 提供给 aa
  - browser + aa
category: devops
---

# BadBoy / Browser / AA 分流

## 先判目标

先问自己三件事：

1. 要不要碰用户当前真实 Chrome 页面？
2. 要不要复用真实登录态？
3. 要不要 AA 自己持续抓包、存 session、跑 AI 报告？

## 四路默认分流

### 路 A — 真实 Chrome 直控

用 `browser-harness-real-chrome`，若：
- 用户明确说“看我现在 Chrome 这个页面”
- 目标依赖现成登录态
- 要直接调试页面 DOM / JS / userscript
- 不需要 AA 持有该登录态

典型任务：
- 调试 Tampermonkey/userscript 不生效
- 查当前标签页按钮为何不动
- 读 console / network / storage
- 在真实页面执行修复验证

一句话：
- “看我 Chrome 当前页 / 现成登录态 / 这个脚本为啥不动” → 先走真实 Chrome。

### 路 B — Hermes 中介取证，再交 AA 离线分析

用 `aa-ana-wo-direct-auth`，若：
- 用户要真实浏览器登录态
- 但不让 AA 直接碰登录态
- 目标是分析协议、流程、存储、请求样本
- 可接受 Hermes 先采证，再把材料交给 AA

典型任务：
- 已登录 SaaS 页面取证
- 导出关键请求给 AA 逆向
- 前端签名逻辑梳理

一句话：
- “badboy cdp 取证后提供给 aa” → 走此路。

### 路 C — AA 协作认证 + CDP 接管

用 `aa-human-auth-cdp-flow` + `anything-analyzer-mcp`，若：
- 用户明确要在 AA/BadBoy Analyzer 内操作
- 需要 AA 自己抓包、hooks、storage、report
- 用户可在 AA 内手动登录一次
- 后续由 agent 通过 CDP 接管

典型任务：
- AA 内完整重放认证后流程
- 持续抓包
- 依赖 AA session DB / analysis report

一句话：
- “在 badboy/aa 里打开，登录完你接着控” → 走此路。

### 路 D — 仅 AA 离线分析，不碰浏览器

用 `anything-analyzer-mcp`，若：
- 已有 HAR / 请求样本 / 文本证据
- 只需 AA 归纳 API、认证流、状态机
- 不需要现场浏览器交互

## 选路优先级

默认优先：
1. 用户眼前真实页面 → 路 A
2. 真实页取证后导给 AA → 路 B
3. 明确要求 AA 内协作抓包/CDP → 路 C
4. 仅离线分析材料 → 路 D

## 禁忌

- 用户说“当前 Chrome 页面”时，不可偷换成隔离 browser。
- 用户已给出真实站点账号、密码、邮箱、或明确授权用现成登录态操作时，应优先直连真实 Chrome/CDP 或 computer-use 执行，不可停在“无登录态/环境受限”的口头判断。
- 用户未要求 AA 桌面 UI 时，不可擅自 `open -a` 拉起窗口。
- 用户强烈反感 UI 时，AA 仅限 headless/CLI/external capture。
- 不可把“AA 会分析”误当成“AA 必须先直接接管浏览器”。

## 中文触发词

### 走真实 Chrome
- 当前页面
- 我 chrome 这个页
- 真实 chrome
- 真实浏览器
- 现成登录态
- 这个脚本不动
- userscript 不生效
- tampermonkey 调试

### 走中介取证 -> AA
- 提供给 aa
- 导给 aa
- 给 badboy 分析
- cdp 后交 aa
- 真实页取证
- 已登录页面离线分析

### 走 AA 协作认证 + CDP
- badboy cdp
- aa cdp
- 在 aa 里登录
- badboy 里打开
- analyzer 里抓包
- aa 接管页面

### 走 AA 离线分析
- 请求样本分析
- har 分析
- 协议归纳
- 逆向 api
- analysis report

## 执行模板

### 模板 1：真实 Chrome userscript 调试
1. 连真实 Chrome
2. 查 URL / console / DOM / userscript 注入痕迹
3. 读脚本文件
4. 定位不动原因
5. 修脚本
6. 回真实页面复验

## browser-harness / 真实 Chrome 现场坑

### 0. 先判是否已拿到 Chrome 的人工授权
若先前 browser-harness / CDP 握手报 `HTTP 403`，且用户说已经开了 remote debugging，但仍未通，优先让用户在真实 Chrome 中：
1. 打开 `chrome://inspect/#remote-debugging`
2. 勾选 `Enable remote debugging`
3. 若弹出授权框，点 `Allow`

经验：很多场景不是端口没开，而是 Chrome 还没完成一次人工授权；点错或没点 Allow 时，agent 侧会持续像“工具坏了”。

### 0.5 不要用 9222 的 404 误判 browser-harness 失败
对 browser-harness 场景，`http://127.0.0.1:9222/json/version` 或 `/json/list` 返回 404，不能单独证明真实 Chrome 接管失败。

经验：browser-harness 可能通过自身桥接链连到真实 Chrome，而不是直接暴露传统 `9222/json/*` 端点。若 `uv run browser-harness` 下的 `page_info()` 能返回当前真实标签页 URL / title / viewport，则应视为“接管已通”，不要被 9222 的 404 误导。

### 0.6 page_info() 是最低成本活性探针
优先跑极小探针确认是否已接到用户眼前页面：

```python
print(page_info())
```

若能读到当前真实页面 URL/title，再继续 DOM/交互；先别浪费时间争论 CDP 细节。

### 0.7 动态站点表单先用 DOM 注入兜底
若 browser-harness 的通用点击/输入手段在富文本或动态评论框上不稳，直接退到页面 JS：
- 先用 `querySelector` 找真实编辑器
- 对 `div[contenteditable="true"]` / `#contenteditable-root` / `textarea` 手工 `focus()`
- 设置 `textContent` 或 `value`
- 再 `dispatchEvent(new InputEvent('input', {bubbles:true,...}))`
- 最后枚举按钮文本确认提交按钮是否已解锁

此法对 YouTube 评论框一类富文本输入尤其有效；比盲点坐标或反复 `type_text` 更稳。

### 0.8 点击后若无弹窗，先判是否是页面状态问题
如 YouTube `分享` 按钮可点但未出现弹层：
1. 先确认当前是否有其他打开的 overlay / editor / engagement panel
2. 先小幅向下滚动，让 engagement 区域重新进视口并触发刷新
3. 枚举 `button, a, input` 看是否已有新控件出现
4. 再决定是重试点击、先收起评论框，还是改走另一分享路径

不要仅凭“按钮点击返回成功”就认定分享弹窗已出现。

### 0.9 YouTube/Reddit 评论编辑器先滚后判
真实浏览器里做 YouTube comment、Reddit comment、share/comment engagement 时，先执行一次小幅下滚，再判断编辑器是否可用。

固定顺序：
1. 页面进入评论/engagement 区后，先向下滚一点。
2. 再看评论区/编辑器是否刷新、placeholder 是否变化、按钮是否解锁。
3. 然后才输入、注入文本、点击评论/分享按钮。

经验：这些区域常见“已点击但无变化”并非 selector 错，而是 viewport 未触发 hydration/refresh。先滚一下，常直接恢复。

若无变化：
- 再小滚一次
- 重抓 snapshot / accessibility tree
- 重新枚举 editor / button / overlay

## BadBoy Browser / bb-browser 现场坑

### 1. Hermes 接 MCP 时，优先用 shell 包一层注入 CDP 环境
若 bb-browser 依赖 `BB_BROWSER_HOST` / `BB_BROWSER_PORT` 或同类环境变量，不要只写裸命令；优先在 `mcp_servers` 中这样配：

```yaml
mcp_servers:
  badboy-browser:
    command: /bin/sh
    args:
      - -lc
      - BB_BROWSER_HOST=127.0.0.1 BB_BROWSER_PORT=19825 exec /Users/xxx/.npm-global/bin/bb-browser mcp
```

理由：有些 CLI 在直配 `command` 时不会按预期吃到外层环境，shell wrapper 更稳。

### 2. 端口开着，不等于 bb-browser 真能接管
即便本地 `19825` 端口可连，若该端口不提供标准 Chrome DevTools 端点（如 `/json/version`、`/json/list`），bb-browser 仍会报：
- `Cannot find a Chromium-based browser`

故障判定顺序：
1. 先查 Chrome 是否真在跑
2. 再查目标端口是否监听
3. 再查 `http://127.0.0.1:<port>/json/version` 是否返回标准 CDP 信息
4. 若无标准端点，则不要把“端口开着”误判为 bb-browser 可用

### 3. bb-browser 的 site adapter 与真实 Chrome 接管分离看
- `bb-browser site ...` 可用，只说明 adapter/抓取链可用
- `bb-browser open/snapshot/click ...` 仍可能因真实 Chrome / CDP 不合规而失败

因此验收需分两步：
1. `bb-browser site list`
2. `bb-browser open ...` 或 `snapshot`

前者过，不代表后者已通。

### 4. macOS 上 `127.0.0.1` 404、`localhost/[::1]` 正常，要两边都试
实战里，Chrome 已启 `--remote-debugging-port=19825` 时，可能出现：
- `http://127.0.0.1:19825/json/version` → `404`
- `http://localhost:19825/json/version` → `200`
- `http://[::1]:19825/json/version` → `200`

原因通常是监听/路由落在 IPv6 或 `localhost`，而不是纯 IPv4 回环。

排障顺序改为：
1. 先试 `http://localhost:<port>/json/version`
2. 再试 `http://[::1]:<port>/json/version`
3. 最后才看 `127.0.0.1`

不要因 `127.0.0.1` 的 404 就误判 “CDP 没起”。

### 5. `bb-browser status` 可能假阴性，直接命令更可信
实战里出现过：
- `bb-browser status --json` → `{"running":false}`
- `bb-browser daemon status` → `Daemon not running`
- 但同一会话下 `BB_BROWSER_CDP_URL=http://localhost:19825 bb-browser tab list/open/snapshot` 全部成功

结论：
- `status` / `daemon status` 不能单独作为可用性判据
- 真正验收应看 `tab list`、`open`、`snapshot`、`screenshot` 是否成功

推荐探针：
```bash
BB_BROWSER_CDP_URL=http://localhost:19825 bb-browser tab list --json
BB_BROWSER_CDP_URL=http://localhost:19825 bb-browser open https://example.com --json
BB_BROWSER_CDP_URL=http://localhost:19825 bb-browser snapshot --tab <tab> --json
```

### 6. Chrome 启动日志见 `bind() failed` 不必立刻判死
实战里，先杀净 Chrome 后再起：

```bash
pkill -f 'Google Chrome' || true
pkill -f 'Chrome Helper' || true
'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome' \
  --remote-debugging-port=19825 \
  --user-data-dir=/tmp/bb-browser-profile
```

日志可能同时出现：
- `bind() failed: Address already in use (48)`
- `DevTools listening on ws://[::1]:19825/...`

这类情况常见于 IPv4 绑定失败但 IPv6 仍成功。应以 `/json/version` 或 `tab list` 验证，不要只看一行 error 就停。

### 7. 动态站点首帧 snapshot 可能只回 URL，稍后重抓
某些站点（如 YouTube）刚 open 完时：
- 首次 `snapshot` 可能只返回 URL，几乎无 DOM
- 数秒后再次 `snapshot`，才拿到完整 refs / 页面结构

做法：
1. `open`
2. 等 1~3 秒
3. `snapshot`
4. 若仅得 URL/空 refs，再重试一次

不要把首帧空 snapshot 误判成页面不可控。

### 8. 真 Chrome/CDP 启动默认用降噪参数
macOS 上若只是为了接管真实 Chrome 做 CDP/`bb-browser`/现场取证，优先用降噪版启动：

```bash
pkill -f 'Google Chrome' || true
pkill -f 'Chrome Helper' || true
sleep 2
'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome' \
  --remote-debugging-port=19825 \
  --user-data-dir=/tmp/bb-browser-profile \
  --disable-crash-reporter \
  --disable-breakpad \
  --disable-background-networking \
  --disable-component-update \
  --disable-features=MediaRouter \
  2>/tmp/chrome-cdp.log
```

用途：
- 压低 `Crashpad settings.dat` 噪声
- 压低 `google_apis/gcm ... DEPRECATED_ENDPOINT` / `connection_factory_impl` 噪声
- 减少与任务无关的后台联网

常见仍可忽略的残余噪声：
- `google_apis/gcm/engine/connection_factory_impl.cc:483] ConnectionHandler failed with net error: -2`
- `net/socket/ssl_client_socket_impl.cc:924] handshake failed ... net_error -100`
- `chrome://newtab/ for incorrect profile type`
- `IPH_ExtensionsZeroStatePromo before browser initialization complete`

这些日志本身不构成故障；只要下列探针仍通过，就继续执行，不要停在报错字样：
1. `http://localhost:19825/json/version`
2. `http://localhost:19825/json/list`
3. `BB_BROWSER_CDP_URL=http://localhost:19825 bb-browser tab list --json`
4. `open/snapshot/screenshot` 实测成功

不要因后台噪声消失与否改变可用性判断；判据仍是 CDP 端点与真实操作是否成功。

### 模板 2：真实页取证后交 AA
1. 连真实 Chrome
2. 抽最小必要 DOM / storage / 请求样本
3. 整理结构化证据
4. 再交 AA/其他 agent 分析

### 模板 3：AA 内手登后 CDP 接管
1. create_session
2. start_capture
3. navigate(login)
4. 等用户手登
5. CDP 接管
6. stop_capture + analysis

## 简判口令

- “看我现在页” → 真实 Chrome
- “帮我交给 AA 分析” → 中介取证 -> AA
- “直接在 BadBoy 里抓” → AA 协作认证 + CDP
- “只有请求样本” → AA 离线分析
