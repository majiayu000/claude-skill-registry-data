---
name: extend-language-plugin
description: 在内置语言插件（extensions/typescript 这类插件内自 spawn LSP server 的形态）里开发语言特性时使用。当任务是加/改 provider（code action / inlay hint / formatting / folding / semantic tokens 等）、调 LSP 客户端 / initialize 参数 / spawn 方式、诊断补全 hover 不生效、或照 typescript 的样子迁一个新语言成内置插件时使用。
---

# 在内置语言插件体系里开发语言特性

TypeScript 已是**内置插件** `extensions/typescript`（VSCode 原汁原味的「选项 B」形态）：插件进程内自 spawn `typescript-language-server`、持有 LSP 客户端，通过 `languages.register*Provider` / `createDiagnosticCollection` / `workspace.onDid*TextDocument` 接入编辑器。语言特性**不再**是 renderer core 硬编码。在这套体系里加/改能力，核心是搞清**一个 provider 调用要穿四个进程边界**，按数据流对号入座改对应环节。

> ⚠️ 第一原则：**先定位你的改动落在四条数据流的哪一条**，再动手。改错环节（比如想加 provider 却只动了插件没动 wire 协议）会编译过但运行时 provider 永远不被调用。

## 三进程拓扑（必须先建立）

```
renderer (Monaco UI)  ──MainThread* / extHost* RPC──  main (字节管道)  ──  extension host (trusted, 无沙箱 Node)
                                                                              └─ spawn typescript-language-server (LSP over stdio)
```
- `extHost*` 通道 = renderer → host（如 `extHostLanguages.$provideXxx`）。
- `mainThread*` 通道 = host → renderer（如 `mainThreadLanguages.$registerProvider` / `$publishDiagnostics`）。
- 通道定义全在 `packages/extensions-common/src/protocol/rpc.ts`（`ExtHostChannels` + `IExtHostLanguages` / `IExtHostDocuments` / `IMainThreadLanguages` 接口）。
- 语言插件**只能跑 trusted host**（要 spawn 子进程）；restricted host 不能 spawn。

## 四条数据流（改之前先认领你属于哪条）

### A. provider 调用（F12 / hover / 补全 …）
```
Monaco 调 provider → renderer LanguageProviderProxy.provideXxx(model,pos)
  → [extHostLanguages.$provideXxx(handle, uri, lspPos, ctx)] renderer→host
  → host extensionService 按 handle 查 provider → provider.provideXxx(doc,pos)
  → 插件 client.provideXxx → 本地 tsserver
  → LSP 结果原路返回 → renderer xxxToMonaco → Monaco 渲染
```
- renderer 壳：`apps/editor/src/renderer/services/languageFeatures/languageProviderProxy.ts`（一组 `createXxxProxy(handle, extHost)` 工厂，每个 = `monacoPositionToLsp` → `$provideXxx` → `xxxToMonaco`）。
- 转换层：`apps/editor/src/renderer/services/languageFeatures/typescript/lspMonacoConvert.ts`（LSP 0-based ↔ Monaco 1-based、enum 重映射、completion/workspace-edit 整形）。**所有 LSP↔Monaco 转换只在这里**。

### B. 文档同步（model open/change/close）
```
Monaco model 变化 → renderer DocumentSyncContribution（debounce 200ms + 全文）
  → activateByEvent('onLanguage:<lang>') 去重激活
  → [extHostDocuments.$acceptDocument{Open,Change,Close}] renderer→host
  → host ExtHostDocuments：更新 TextDocument 镜像 + fire onDidOpen/Change/Close
  → 插件 workspace.onDid* → client.didOpen/didChange/didClose → 本地 tsserver
```
- renderer：`apps/editor/src/renderer/contributions/DocumentSyncContribution.ts`（通用，广播**所有文本 model**；markdown 那条独立 LSP 同步并存、不要动它）。

### C. 诊断（server PUSH）
```
本地 tsserver publishDiagnostics → 插件 client.onDiagnostics → diagnosticCollection.set(uri, diags)
  → [mainThreadLanguages.$publishDiagnostics(owner, uri, diags)] host→renderer
  → renderer MainThreadLanguages → diagnosticToMarker → setModelMarkers(model, owner=name, …)
```
- `owner` = `createDiagnosticCollection(name)` 的 name（TS 用 `'typescript'`）。

### D. provider 注册（句柄路由，仿 SCM）
```
插件 activate → languages.registerXxxProvider(selector, provider)
  → host 分配 handle、存 _providers Map、[mainThreadLanguages.$registerProvider(handle,type,selector)] host→renderer
  → renderer MainThreadLanguages 按 type 调 createXxxProxy 造 Monaco provider → 注册 ILanguageFeaturesService → 存 handle→IDisposable
  → dispose → $unregisterProvider(handle)
```
- host：`packages/extension-host/src/extensionService.ts`（`_providers: Map<number, {type, provider}>` + `_nextHandle`，每个 `registerXxxProvider` 分配 handle 调 `$registerProvider`）。
- renderer：`apps/editor/src/renderer/services/extensions/MainThreadLanguages.ts`（`$registerProvider` 按 `LanguageProviderType` 选工厂；`$publishDiagnostics` 落 marker）。
- `LanguageProviderType` 枚举（10 种）：`definition | references | implementation | typeDefinition | hover | completion | signatureHelp | documentSymbol | rename | workspaceSymbol`（`rpc.ts:199`）。

## 关键约定

### wire 类型：直接复用 `vscode-languageserver-types`，不写中立 DTO
LSP 类型是 plain-JSON，跨 `ProxyChannel` verbatim，两端共享单一定义，零转换直返。uri 跨进程用 `UriComponents`（插件内 `vscode-uri` 的 `URI.parse/from` 在 string ↔ components 间转）。position LSP 0-based、Monaco 1-based，转换只在 `lspMonacoConvert.ts`。catalog 已 pin `vscode-languageserver-types`，三处 type-only 依赖即可（esbuild type-only 不进 bundle）。

### KEEP IN SYNC：bridge 接口三处必须一致（漏一处 typecheck 报错）
1. `packages/extension-api/src/index.ts` 的 `IExtensionHostBridge`（+ 对外 `languages` / `workspace` namespace 与 provider 类型）。
2. `packages/extension-host/src/apiFactory.ts` 的 `IExtensionHostBridge`。
3. `packages/extension-host/src/extensionService.ts` 的实现类。
加任何新 bridge 方法（如新 provider 注册、新 workspace 事件），**三处同步加**。

### LSP 路径：唯一 Electron 耦合留在主进程
- `apps/editor/src/main/services/extensionHost/tsServerPaths.ts` 的 `resolveTsServerPaths()`（dev 从 `app.getAppPath()` walk-up、packaged 从 `process.resourcesPath`）算 `{cli, tsserver}`。
- `extensionHostMainService.ts` 启动 trusted host 时注入 `env.UNIVERSE_TSLS_CLI` / `UNIVERSE_TSLS_TSSERVER`（`:180` 附近，可选构造参 `_resolveTsServerPaths` 便于单测）。
- 插件 `lspClient.ts` 从 `process.env` 读，spawn `process.execPath [cli,'--stdio']`（`ELECTRON_RUN_AS_NODE=1` + `ENV_DENYLIST` sanitize），initialize 时 `initializationOptions.tsserver.path = tsserver`。插件**不碰任何 Electron API**。

## 常见任务 → 改哪里

### 任务 1：给 TS 加一类**新 provider**（如 code action / formatting / inlay hint / folding / document highlight / semantic tokens）
这是最大的一类，要穿全部环节。按数据流 A + D，对号改：
1. **rpc 协议**（`rpc.ts`）：`IExtHostLanguages` 加 `$provideXxx(handle, …)`；`LanguageProviderType` 枚举加新成员（若该特性走句柄 provider 路由）。
2. **extension-api**（`index.ts`）：加 provider 类型（方法吃 `TextDocument`+`Position`/参数、返回 LSP 类型）+ `languages.registerXxxProvider` + `IExtensionHostBridge` 加方法。
3. **apiFactory.ts**：`IExtensionHostBridge` 同步加（KEEP IN SYNC）。
4. **extensionService.ts**：`registerXxxProvider` 分配 handle 调 `$registerProvider`；RPC `provideXxx(handle,…)` 查 `_providers` 调 provider（KEEP IN SYNC 实现）。
5. **renderer proxy**（`languageProviderProxy.ts`）：加 `createXxxProxy(handle, extHost)` 工厂；转换函数加进 `lspMonacoConvert.ts`（+ 单测）。
6. **renderer MainThreadLanguages**：`_register` 的 type→工厂 switch 加分支。
7. **插件**（`extension.ts` + `lspClient.ts`）：`lspClient` 加 `provideXxx`（`sendRequest('textDocument/xxx', …)`）；`extension.ts` 的 `registerProviders` 加一行 `languages.registerXxxProvider(TS_JS_LANGUAGES, {...})`。
> 若新特性 Monaco 没有「provider」概念（如纯命令），评估是否该走 Action2（见 `register-monaco-command` skill）而非 provider 路由。

### 任务 2：**扩展已有 provider 的入参/返回**（如补全带更多 context、hover 富信息）
通常只需：`lspClient.ts` 改 `sendRequest` 参数 → `extension.ts` 透传 → `lspMonacoConvert.ts` 改转换（+ 单测）。若改了跨进程方法签名，记得 rpc + KEEP IN SYNC 三处跟上。

### 任务 3：改 **LSP 客户端**（spawn 方式 / initialize 参数 / 崩溃重启 / 触发字符）
只在 `extensions/typescript/src/lspClient.ts`。崩溃重启后要重推所有 open doc（`_resyncAll` 思路已在）。改 spawn/env 注意 `ENV_DENYLIST` + `ELECTRON_RUN_AS_NODE`。触发字符在 `extension.ts`（`COMPLETION_TRIGGER_CHARACTERS` / `SIGNATURE_TRIGGER_CHARACTERS`）。

### 任务 4：诊断不出/要调
查 C 链路：`lspClient` 的 `onDiagnostics` → `extension.ts` 的 `diagnostics.set` → `mainThreadLanguages.$publishDiagnostics` → `MainThreadLanguages._setMarkers`（`diagnosticToMarker` + `setModelMarkers`，owner 必须等于 collection name）。注意：MonacoLoader 里关掉了 ts-worker 自带 diagnostics 防双注册（`disableLanguageDiagnostics`）。

### 任务 5：迁一个**新语言**成内置插件（仿 extensions/typescript）
1. `extensions/<lang>/`：仿 `extensions/typescript/` 结构（`package.json` activationEvents `onLanguage:*` + esbuild bundle `vscode-jsonrpc`/`vscode-languageserver-types` + `tsconfig.json` + `src/{extension,lspClient}.ts`）。
2. 若用独立 LSP server：主进程加路径解析 + env 注入（仿 `tsServerPaths.ts`），或插件自带二进制；`scripts/release/runtime-resources.mjs` 确认 server node_modules 进 `.runtime-resources`。
3. provider 全复用现成句柄路由（renderer proxy/MainThreadLanguages 不用改，除非要新 provider 类型）。文档同步复用通用 `DocumentSyncContribution`（已广播所有语言）。
> markdown 目前仍是旧的独立 LSP 同步路径（`services/languageFeatures/markdown/`），未迁入插件——若要迁，它就是下一个样板对象。

### 任务 6：tsserver 路径找不到 / dev vs 打包不一致
`tsServerPaths.ts`：dev walk-up 容忍 `electron .`（appPath=apps/editor）和 e2e `electron out/main/index.js` 两种布局；packaged 走 `process.resourcesPath`。`typescript-language-server` 的 node_modules 由 `vendor/` + `scripts/release/runtime-resources.mjs` 带入打包产物。插件激活时若 env 缺失会把原因写进「TypeScript」输出通道并直接不激活——排查第一站（也可用命令 `typescript.openTsServerLog` 打开）。

## 验证
```bash
pnpm check        # lint + typecheck + test，仅看错误输出
pnpm e2e          # 改了交互链路时跑冒烟，仅截错误
```
- 逐包 typecheck 顺序：`extensions-common` → `extension-api` → `extension-host` → `editor` → `pnpm ext:build`（出 `extensions/typescript/dist/extension.js`）。
- 加了转换函数务必补 `lspMonacoConvert.test.ts` 单测（renderer 项目，happy-dom）。
- **手测**（无法自动化）：`pnpm dev` → Output 面板「TypeScript」通道打印插件 + tsserver 启动（插件日志的归属地；「Extension Host」只剩 host 框架日志）→ 打开 .ts → F12/Shift+F12/hover/补全/签名/重命名/Outline 全可用 → 改代码出红波浪线（诊断）。

## 易踩坑速记
1. **加 provider 编译过但运行时不触发** → 多半漏了某环节：检查数据流 A+D 七步是否齐（尤其 rpc 枚举 + MainThreadLanguages 的 type→工厂分支）。
2. **KEEP IN SYNC 三处**（extension-api ↔ apiFactory ↔ extensionService）漏一处 → typecheck 报错；改 bridge 必三处同步。
3. **uri 跨进程是 `UriComponents` 不是 `URI`** → 插件内 `URI.parse/from` 转 string 喂 LSP；renderer 内 `URI.revive`。
4. **position 差一** → LSP 0-based、Monaco 1-based，只在 `lspMonacoConvert.ts` 转，别在别处自己 ±1。
5. **诊断 owner 不匹配** → `setModelMarkers` 的 owner 必须等于 `createDiagnosticCollection(name)` 的 name，否则清不掉/串色。
6. **双注册** → Monaco 自带 ts-worker 的 diagnostics/completion/hover… 已在 `MonacoLoader.disableLanguageDiagnostics` 关掉；新增插件 provider 时确认对应 ts-worker 特性也关了，否则一个位置两份结果。
7. **插件碰 Electron API** → 不行。host 是纯 Node，所有 Electron 相关（路径解析）必须留主进程经 env 注入。
8. **`.tsx` languageId** → 给 tsserver 必须是 `typescriptreact`/`javascriptreact`（`TS_JS_LANGUAGES` 四个），别用 `typescript`。
9. **激活时序**：插件激活晚于文档打开 → `activate` 时遍历 `workspace.textDocuments` 补 didOpen（已实现，新语言插件照抄）。
10. **崩溃恢复**：lspClient 重启后必须重推所有 open doc，否则补全/诊断全空。
11. **虚拟 scheme 文档会打到 LSP（diff/peek 视图）**：Monaco 语言请求**不区分 model scheme**，而 `DocumentSelector` 只有 languageId 无 scheme 过滤；diff 视图的 `diff-original:`/`diff-modified:` 模型（`diffModelUri.ts`，只换 scheme、languageId 仍是 typescript）的 hover/补全/语义 tokens 会一路到 LSP——host 的 `ExtHostDocuments.getOrSynthesize` 对未同步 URI 还合成空文档兜底，请求必发。tsgo 对无 project 的 URI 报 `no project found for URI <uri>`（该字符串在 tsgo.exe 里，tsls/tsserver 源码搜不到），沿 RPC 回传成 renderer error 日志。**修法**（新语言插件照抄）：插件内统一谓词 `isServerBackedDocument`（languageId ∈ 支持集合 && `uri.scheme === 'file'`，对齐 VSCode TS 插件 selector 的 `scheme: 'file'`），门控 ①documentSync 的 open/change/close ②每个 provider 回调（`forServerDocs` 高阶包装，非 file 返回 null）。参考 `extensions/typescript/src/extension.ts` + 复现测试 `src/__tests__/documentScope.test.ts`。
12. **插件诊断日志走专属输出通道，禁止 console.error**：console.* 全混进共享的「Extension Host」通道，排查时要在噪音里捞针。TS 插件的样板：`src/logger.ts`（off/error/info/verbose 分级的**内部级别**，`OutputChannelLogger` 写「TypeScript」通道；用户设置 `js/ts.tsserver.log` 走 VSCode 值域 off/terse/normal/verbose/requestTime，经 `loggerLevelForSetting` 映射到内部级别、经 `logVerbosityForSetting` 映射到 tsserver 文件日志详细度——**一个键管两件事**；级别 = `UNIVERSE_TS_LOG_LEVEL` env（内部级别）> 该设置，verbose 记 server stderr + 每请求耗时）+ 调试命令 `typescript.openTsServerLog` / `typescript.restartTsServer`（onCommand 激活 + contributes.commands 走 nls）。新语言插件照抄这套。

13. **异步请求的 range 属于发起时的文档版本**：发送前 flush 只能保证入口一致；TSLS codeAction 等诊断后仍会拿旧 range 请求重构。须在服务端 await 后检查文档版本、对象身份及取消状态，不用 clamp 或隐藏错误兜底。持久补丁见 `vendor/typescript-language-server/patch.mjs`（npm postinstall、缓存命中和远程部署均须覆盖），回归见 `tsCodeActionStaleRange.spec.ts`。取证同时看通知、输出通道及 tsserver 请求日志，单看 console 可能假绿。

## 关键参考路径
- `extensions/typescript/src/extension.ts` —— 插件入口：activate + 10 类 provider 注册 + 文档同步（**新语言插件模板**）
- `extensions/typescript/src/lspClient.ts` —— 插件内 LSP 客户端：spawn / initialize / sendRequest / 诊断 / 崩溃重启
- `packages/extensions-common/src/protocol/rpc.ts` —— 三向通道契约 + `LanguageProviderType` 枚举（加 provider 第一站）
- `packages/extension-api/src/index.ts` —— `languages`/`workspace` 对外 API + `IExtensionHostBridge`（KEEP IN SYNC 之一）
- `packages/extension-host/src/apiFactory.ts` —— `IExtensionHostBridge`（KEEP IN SYNC 之二）
- `packages/extension-host/src/extensionService.ts` —— provider 句柄路由 + diagnostics collection 实现（KEEP IN SYNC 之三）
- `apps/editor/src/renderer/services/extensions/MainThreadLanguages.ts` —— host→renderer：句柄→Monaco provider、诊断落 marker
- `apps/editor/src/renderer/services/languageFeatures/languageProviderProxy.ts` —— 通用 `createXxxProxy` 工厂
- `apps/editor/src/renderer/services/languageFeatures/typescript/lspMonacoConvert.ts` —— **唯一** LSP↔Monaco 转换层（+ 同目录 `__tests__`）
- `apps/editor/src/renderer/contributions/DocumentSyncContribution.ts` —— 通用文档广播
- `apps/editor/src/main/services/extensionHost/tsServerPaths.ts` —— 唯一 Electron 耦合的路径解析
- `apps/editor/src/main/services/extensionHost/extensionHostMainService.ts` —— trusted host 启动 + env 注入（`:180` 附近）
- `extensions/git/` —— 另一个内置插件样板（commands/scm，不含 provider）
- 相关 skill：`register-monaco-command`（命令/键位走 Action2，不走 provider 路由时看它）

## 其它
- 对标 VSCode 的特性：command id / 默认键 / 触发字符与 VSCode 原生保持一致。
- 后续用本 skill，发现新经验，需同步更新本文件
