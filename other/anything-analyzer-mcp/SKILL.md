---
name: anything-analyzer-mcp
description: |
  anything-analyzer 的 MCP/CLI/headless/MITM 使用心得总表。含抓包、逆向、启动、验活、路由边界。
  触发方式：Hermes 路由名 `devops/anything-analyzer-mcp`、通用 slash command `/skill devops/anything-analyzer-mcp`
triggers:
  - anything-analyzer
  - aa
  - aa mcp
  - aa headless
  - aa cli
  - 抓包分析
  - 协议分析
  - MCP 抓包
  - 流量分析
  - browser capture
  - cdp 抓包
  - reverse-api
  - 逆向抓包
  - 逆向接口
  - mitm
  - 代理抓包
  - streamablehttp
  - headless mcp
  - 外部抓包
---

# anything-analyzer MCP

## 何时用

命中下列意图，先载此 skill：
- 用户提 `anything-analyzer` / `aa`
- 需要抓包、逆向 API、看请求明细、跑 AI 分析
- 需要 AA 的 MCP、CLI、headless、MITM
- 需要“无 Electron/UI”地把 AA 当后端
- 需要让外部浏览器经 MITM 进 session

若任务是“当前真实 Chrome / 现成登录态 / 当前页面直控”，不要默认只靠 AA；先结合 `badboy-br-aa-routing` 分流。

## 总结论

AA 现有 3 条面：
1. MCP 面：`http://localhost:23816/mcp`
2. MITM 面：`127.0.0.1:8888`
3. browser-ui 面：仅在桌面 UI/backend 存在时可用

核心边界：
- `external` 模式：负责 MITM 抓包与后续分析；不负责页面内控制
- `browser-ui` 模式：才有 CDP / tabs / screenshot / hooks / storage 的完整页面内能力
- 用户明确禁止 Electron/UI 时，默认走 `headless + external`

## 起手检查

先判用户要哪类：
- 只要抓包/逆向/AI 分析，不要桌面窗口 → `headless + external`
- 要控制 AA 内嵌浏览器 / CDP / screenshot → `browser-ui`
- 要看用户真实 Chrome 当前页 → 先走 badboy/browser-harness/真实 Chrome 路线，AA 只做后端分析或外部抓包

## 启动方式

### 纯后端，禁 UI

```bash
cd ~/anything-analyzer
pnpm build:cli
AA_HEADLESS=1 AA_CONFIG_DIR="$HOME/Library/Application Support/anything-analyzer" node ./out/main/nodeHeadless.mjs
```

oneshot 验活：

```bash
cd ~/anything-analyzer
pnpm build:cli
AA_HEADLESS=1 AA_CONFIG_DIR="$HOME/Library/Application Support/anything-analyzer" node ./out/main/nodeHeadless.mjs --oneshot
```

成功判据：
- 有 `[MCP Server] Listening on http://localhost:23816/mcp`
- 有 `[MitmProxy] Listening on port 8888`
- JSON 含 `"mitmEnabled":true`

### 桌面 UI 路径

仅在用户明确要 AA 桌面界面时才可用。默认不要自动 `open -a`。

## MCP 信息

- URL: `http://localhost:23816/mcp`
- Transport: `StreamableHTTP`
- 必要请求头：
  - `Authorization: Bearer <authToken>`
  - `Accept: application/json, text/event-stream`
- 配置文件：
  - `~/Library/Application Support/anything-analyzer/mcp-server-config.json`
- 真实字段：
  - `enabled`
  - `port`
  - `authEnabled`
  - `authToken`

## MITM 信息

- 默认端口：`8888`
- 配置文件：
  - `~/Library/Application Support/anything-analyzer/mitm-proxy-config.json`
- MITM 成功不等于 CA 已装进系统信任；是否真可拦 HTTPS 仍取决于浏览器/系统是否信任该 CA

## 验活顺序

### 1. 先验构建产物不含 Electron/UI

```bash
cd ~/anything-analyzer
pnpm build:cli
node -e "const fs=require('fs'); const s=fs.readFileSync('out/main/nodeHeadless.mjs','utf8'); for (const x of ['electron','BrowserWindow','ipcMain','src/main/session/session-manager.ts','src/main/runtime/bootstrap.ts']) console.log(x+':', s.includes(x));"
```

期望全 `false`。

### 2. 再验 oneshot

```bash
AA_HEADLESS=1 AA_CONFIG_DIR="$HOME/Library/Application Support/anything-analyzer" node ./out/main/nodeHeadless.mjs --oneshot
```

### 3. 再验 MCP initialize

```bash
curl -i -X POST http://localhost:23816/mcp \
  -H 'Authorization: Bearer <authToken>' \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  --data '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"debug","version":"1.0"}}}'
```

成功判据：
- HTTP `200`
- 响应头有 `mcp-session-id`
- body 返回 `initialize` 结果

### 4. 若要确认 MITM 真起

看启动日志是否有：
- `[MitmProxy] Listening on port 8888`

oneshot JSON 应含：
- `"mitmEnabled":true`

## 常用工具面

### Session 管理
- `list_sessions`
- `create_session(name, targetUrl)`
- `start_capture(sessionId, mode?)`
- `pause_capture(sessionId)`
- `resume_capture(sessionId)`
- `stop_capture(sessionId)`
- `delete_session(sessionId)`

### 数据面
- `get_requests(sessionId)`
- `filter_requests(sessionId, filters)`
- `get_request_detail(requestId)`
- `get_hooks(sessionId)`
- `get_storage(sessionId)`

### AI 分析面
- `run_analysis(sessionId, purpose?, selectedSeqs?)`
- `get_reports(sessionId)`
- `chat_followup(sessionId, message)`

### browser-ui only
- `navigate(url)`
- `browser_back`
- `browser_forward`
- `browser_reload`
- `create_tab(url?)`
- `close_tab(tabId)`
- `list_tabs`
- `browser_screenshot`
- `cdp_send_command(method, params?)`

## 抓包工作流

### 外部浏览器抓包，禁 UI

适用：
- 用户真实 Chrome / BadBoyBrowser / 其它浏览器已开
- 只需抓请求、分析协议，不需 AA 自己开窗口

流程：
1. 起 AA headless
2. `create_session`
3. `start_capture(sessionId, mode="external")`
4. 让外部浏览器走 `127.0.0.1:8888`
5. 完成操作
6. `stop_capture(sessionId)`
7. `filter_requests` / `get_request_detail`
8. `run_analysis(purpose="reverse-api")`

要点：
- `external` 不依赖 AA tab
- `external` 不提供页面内控制
- 对某些 Hermes relay / browser-harness 页面，`external` 可能完全抓不到流量；即便系统代理已改到 `127.0.0.1:8888`、AA 8888/23816 监听正常、session 也成功 `start_capture`，抓到的仍可能只有 AA 自己的 MCP 请求而没有目标站点流量。若 `filter_requests` / `get_requests` 持续为空，不要继续假设 MITM 已接上该页面。
- 遇到上述情况，优先回退到页面内取证：在目标 userscript/页面里埋 `fetch`/`XMLHttpRequest` hook，仅记录目标 API（如 `/tile-api/*`）的 request/response 摘要，再由 Hermes/AA 做离线分析。
- 若用户要求“你替我接上 AA MITM”，可直接在宿主机把系统代理指向 `127.0.0.1:8888`，然后重载 AA headless 再复测抓包；在 macOS 上可用：
  - `networksetup -setwebproxy 'Wi-Fi' 127.0.0.1 8888`
  - `networksetup -setsecurewebproxy 'Wi-Fi' 127.0.0.1 8888`
  - `networksetup -setwebproxystate 'Wi-Fi' on`
  - `networksetup -setsecurewebproxystate 'Wi-Fi' on`
- 若 AA 通过 launchd 长驻，补充在 `~/Library/LaunchAgents/com.anything-analyzer.dev.plist` 写入 `http_proxy` / `https_proxy` / `HTTP_PROXY` / `HTTPS_PROXY` 到 `http://127.0.0.1:8888`，再执行：
  - `launchctl bootout gui/$(id -u) ~/Library/LaunchAgents/com.anything-analyzer.dev.plist 2>/dev/null || true`
  - `launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.anything-analyzer.dev.plist`
  - `launchctl kickstart -k gui/$(id -u)/com.anything-analyzer.dev`
- 适合“真实浏览器做人，AA收流量”

### browser-ui 抓包

适用：
- 需要 AA 内部页面控制
- 需要 CDP / screenshot / hooks / storage

流程：
1. `create_session`
2. `start_capture(sessionId, mode="browser-ui")`
3. `navigate`
4. 页面交互
5. `stop_capture`
6. 查询与分析

## 逆向 API 工作流

最短路径：
1. `create_session`
2. `start_capture`
3. 触发目标行为
4. `stop_capture`
5. `filter_requests(domain=..., contentType='json')`
6. `get_request_detail`
7. `run_analysis(purpose='reverse-api')`
8. `chat_followup('列认证链/签名算法/重放顺序')`

建议追问：
- 列所有认证相关请求
- 列请求依赖顺序
- 列 header/body 中签名字段
- 推测重放所需最小字段集
- 列可疑 crypto / nonce / timestamp 流程

## MCP 协议坑

### 必须带 Accept
若缺：
- `Accept: application/json, text/event-stream`

则常见为握手失败或客户端报 handshaking error。

### token 字段不是 token
真实字段名：
- `authToken`

不是：
- `token`

### initialize 成功不等于 tools/list 一定成功
已知坑：
- 某些版本 `tools/list` 会报 `_zod`

但：
- `initialize`
- `resources/list`
- `resources/read`

仍可能可用。

应对：
- 不要卡死在客户端“列工具失败”
- 直接看 `src/main/mcp/mcp-server.ts` 中注册了哪些 tool/resource
- 或直接手工 POST 调用已知方法

## Headless / CLI 心得

### `pnpm dev` 不是总有
CLI-only 打包态可能没有 `pnpm dev`。

若报：
- `ERR_PNPM_RECURSIVE_EXEC_FIRST_FAIL Command "dev" not found`

改走：
- `pnpm build:cli`
- `node ./out/main/nodeHeadless.mjs`

### launchd / LaunchAgent 常见双坑

若 `anything-analyzer (http)` 手动前台能起，后台 LaunchAgent 却失败，先查两项：

1. plist 还在跑旧命令 `pnpm dev`
2. launchd 用的是另一套 Node，致 `better-sqlite3` ABI 不匹配

现场判法：

```bash
launchctl list | grep -i anything-analyzer || true
launchctl print gui/$(id -u)/com.anything-analyzer.dev | sed -n '1,160p'
/usr/local/bin/node -p "process.execPath + ' ' + process.versions.modules + ' ' + process.version"
/opt/homebrew/bin/node -p "process.execPath + ' ' + process.versions.modules + ' ' + process.version"
cat /tmp/anything-analyzer-stdout.log 2>/dev/null || true
cat /tmp/anything-analyzer-stderr.log 2>/dev/null || true
```

典型现象：
- 前台 shell 用 `/opt/homebrew/bin/node`，如 Node 25，ABI `141`
- LaunchAgent PATH 先命中 `/usr/local/bin/node`，如 Node 22，ABI `127`
- 于是后台报：
  - `better_sqlite3.node was compiled against a different Node.js version`

修法：
- 先按当前目标 Node 重编：

```bash
cd ~/anything-analyzer
pnpm config set only-built-dependencies better-sqlite3
pnpm rebuild better-sqlite3
```

- 再把 `~/Library/LaunchAgents/com.anything-analyzer.dev.plist` 改到明确、单一路径：
  - PATH 以 `/opt/homebrew/bin` 开头
  - 不再跑 `pnpm dev`
  - 改跑 `pnpm build:cli && AA_HEADLESS=1 ... /opt/homebrew/bin/node ./out/main/nodeHeadless.mjs`
  - 环境变量显式写入 `AA_HEADLESS=1` 与 `AA_CONFIG_DIR`

- 最后重载：

```bash
launchctl bootout gui/$(id -u) ~/Library/LaunchAgents/com.anything-analyzer.dev.plist 2>/dev/null || true
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.anything-analyzer.dev.plist
launchctl kickstart -k gui/$(id -u)/com.anything-analyzer.dev
```

成功判据：
- `launchctl print ...` 显示 `state = running`
- stdout 日志出现：
  - `[MCP Server] Listening on http://localhost:23816/mcp`
  - `[MitmProxy] Listening on port 8888`
- `lsof -nP -iTCP:23816 -sTCP:LISTEN`
- `lsof -nP -iTCP:8888 -sTCP:LISTEN`

### 缺 headless 产物
若报：
- `Cannot find module ...nodeHeadless.js`
- `Cannot find module ...nodeHeadless.mjs`

先做：
- `pnpm build:cli`

### better-sqlite3 ABI 坑
若报：
- `NODE_MODULE_VERSION` 不匹配
- `ERR_DLOPEN_FAILED`
- `Could not locate the bindings file`

优先修：

```bash
cd ~/anything-analyzer
pnpm config set only-built-dependencies better-sqlite3
pnpm rebuild better-sqlite3
```

随后验：

```bash
node -e "const Database=require('better-sqlite3'); const db=new Database(':memory:'); console.log(db.prepare('select 1 x').get().x); db.close()"
```

### node-forge ESM 坑
真实踩坑：
- 当前 ESM 打包态下，`node-forge` 运行时常只暴露 `default`
- 若源码写 `import * as forge from 'node-forge'`，运行时可出现 `forge.pki` 空
- 继而 `privateKeyFromPem` 崩，MITM 起不来

稳妥写法：

```ts
import * as forgeNs from "node-forge";
const forge = (forgeNs as any).default ?? forgeNs;
```

修后验：

```bash
node -e "import * as forgeNs from 'node-forge'; const forge=(forgeNs.default??forgeNs); const keys=forge.pki.rsa.generateKeyPair({bits:512}); const pem=forge.pki.privateKeyToPem(keys.privateKey); const parsed=forge.pki.privateKeyFromPem(pem); console.log(!!parsed && !!parsed.n && !!parsed.e)"
```

### MITM 错误要降级
即便 MITM 失败，也不应阻断 MCP 本体启动。

验收须拆成两层：
- MCP 可用？
- MITM 可用？

不要把二者混为一谈。

### focused test 仍触发 Electron，多半是 runtime bootstrap 串错分支
真实踩坑：
- `tests/runtime-bootstrap-ipc-path.test.ts` 若报 `Electron failed to install correctly`
- 往往不是测试 mock 失效，而是 `src/main/runtime/bootstrap.ts` 仍静态拉进了 Electron 路径

优先查两点：
1. headless runtime 是否仍在用 `SessionManager`
   - 错：`../session/session-manager`
   - 对：`../node-session-manager`
2. bootstrap 是否在启动期注入了 IPC 路径提供者
   - 需调用：`setIpcPathProvider(options.pathProvider)`

推荐修法：
- `createRuntimeContext()` 中：
  - `setDatabasePathProvider(options.pathProvider)` 后立刻接 `setIpcPathProvider(options.pathProvider)`
  - `new SessionManager(...)` 改为 `new NodeSessionManager(...)`

修后先跑最小验证：

```bash
cd ~/anything-analyzer
pnpm exec vitest run tests/runtime-bootstrap-ipc-path.test.ts
```

再跑提交前 focused suite：

```bash
cd ~/anything-analyzer
pnpm build:cli
pnpm exec vitest run \
  tests/main/node-headless.test.ts \
  tests/runtime-bootstrap-ipc-path.test.ts \
  tests/runtime-headless-config.test.ts \
  tests/main/release-workflow.test.ts
```

## Electron/UI 禁令下的处置

用户若明确说：
- 不要 Electron
- 不要 UI
- 不要弹窗

则必须：
- 不自动 `open -a 'BadBoy Analyzer'`
- 不自动 `open -a 'Anything Analyzer'`
- 不用桌面窗口做“探测”

先止血：

```bash
pkill -f 'BadBoy Analyzer|Anything Analyzer|anything-analyzer.*Electron|electron.*anything-analyzer' || true
ps aux | grep -i 'BadBoy Analyzer\|Anything Analyzer\|electron.*anything-analyzer\|anything-analyzer.*electron' | grep -v grep || true
```

默认路径改为：
- `headless + external`

## 真实浏览器 / 当前页分流

若用户要：
- 当前页面
- 真实 Chrome
- 已登录态
- Tampermonkey 当前脚本

默认不要只靠 AA。

分流：
- 直控真实页面 → `badboy-browser` / `browser-harness-real-chrome` / computer-use
- AA 做后端抓包 → `start_capture(mode='external')`
- 需要离线分析 → `run_analysis` / `chat_followup`

一句话：
- 人在真实浏览器里操作
- AA 在后面收包、归档、分析

## 多平台配置格式

### Hermes
```yaml
anything-analyzer:
  transport: streamableHttp
  url: http://localhost:23816/mcp
  headers:
    Authorization: "Bearer <TOKEN>"
```

### Claude Code
```json
{
  "type": "url",
  "url": "http://localhost:23816/mcp",
  "headers": { "Authorization": "Bearer <TOKEN>" }
}
```

### Windsurf
```json
{
  "serverUrl": "http://localhost:23816/mcp",
  "headers": { "Authorization": "Bearer <TOKEN>" }
}
```

### Codex
```toml
[mcp_servers.anything-analyzer]
url = "http://localhost:23816/mcp"

[mcp_servers.anything-analyzer.headers]
Authorization = "Bearer <TOKEN>"
```

## 发布/打包经验

若目标是 agent-only：
- 默认发 CLI 产物，不默认发桌面安装包
- `pnpm build` 可 alias 到 `build:cli`
- `package.json main` 指向 headless entry
- 用 `files` 白名单裁 tarball

但：
- 裁发布包，不等于删除仓库 UI 源码
- 除非用户明确要求，不要直接删 `src/renderer/`、`electron-builder.yml`、`resources/`

## 推荐验证命令集

```bash
cd ~/anything-analyzer
pnpm build:cli
node -e "const fs=require('fs'); const s=fs.readFileSync('out/main/nodeHeadless.mjs','utf8'); for (const x of ['electron','BrowserWindow','ipcMain']) console.log(x+':', s.includes(x));"
node -e "const Database=require('better-sqlite3'); const db=new Database(':memory:'); console.log(db.prepare('select 1 x').get().x); db.close()"
AA_HEADLESS=1 AA_CONFIG_DIR="$HOME/Library/Application Support/anything-analyzer" node ./out/main/nodeHeadless.mjs --oneshot
```

## 路由短则

- 提 AA/MCP/抓包/逆向接口 → 先载此 skill
- 提 真实 Chrome/当前页面/现成登录态 → 先看 `badboy-br-aa-routing`
- 提 禁 UI/别弹窗 → 直接 `headless + external`
- 提 CDP/screenshot/tabs → 明示 `browser-ui only`
- 提 MITM 不通 → 先查 `node-forge`、CA、8888 监听、是否信任 CA
- 提 MCP 不通 → 先查 `authToken`、`Accept`、initialize、23816 监听
