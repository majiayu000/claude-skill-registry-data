---
name: add-json-schema-association
description: 为特定 JSON 文件（按文件名/glob 匹配）接 schema 智能提示（补全/校验/hover）。当用户说打开某类 JSON 给专属提示、像 settings.json 那样为 *.xxx.json 配 schema、给配置 JSON 加校验和补全，或要新增一种 JSON 文件类型的 schema 关联时使用。
---

# 为特定 JSON 文件接上 schema 智能提示

本仓库的 JSON schema 智能提示（补全/校验/hover）底层管道**已就绪且通用**：所有来源最终都注册到平台的 `JSONContributionRegistry`，由 `JsonSchemaBridgeContribution` 自动推给 Monaco 的 JSON 语言服务。**新增一种 JSON 文件类型的提示 = 往三条来源路径之一「声明一条」，而不是写新管道。** 核心套路：**判定该用哪条来源路径 → 把 schema 内联成对象 → 注册到 `JSONContributionRegistry`（或走能汇入它的声明点）→ 加测试 → 验证**。

> ⚠️ 第一原则：**先选对来源路径**。三条路径的声明者、schema 来源、读文件位置完全不同（见下表），选错会写在错误的进程/层里。绝大多数「为某类文件配 schema」的需求走**路径 A（扩展 jsonValidation）**。

> ⚠️ 硬约束：Monaco 设了 `schemaRequest: 'ignore'`（`MonacoLoader.ts` 的 `BASE_JSON_DIAGNOSTICS`），**JSON worker 不会自己去 fetch/读取 schema 文件**。所以任何指向文件的 schema 都必须**先读出内容、`JSON.parse` 成对象**再注册——只有内联对象能生效。这条决定了「在哪一端读文件」。

## 核心机制：统一出口 + 自动桥接（必须先理解）

```
来源 A 扩展 contributes.jsonValidation ─┐
来源 B 用户 settings.json 的 json.schemas ─┼─► JSONContributionRegistry.registerSchema({uri, fileMatch, schema})
来源 C 内置声明表（核心代码） ───────────┘         │ onDidChangeContributions
                                                  ▼
                                   JsonSchemaBridgeContribution._pushSchemasToMonaco()
                                                  ▼
                                   MonacoLoader.setJsonSchemas()
                                                  ▼
                                   monaco.json.jsonDefaults.setDiagnosticsOptions({schemas})
```

关键事实：
- **唯一出口是 `JSONContributionRegistry.registerSchema(contribution): IDisposable`**（`packages/platform/src/configuration/jsonSchemaRegistry.ts`）。`contribution = { uri: string; fileMatch: string[]; schema: IJSONSchema }`。同 `uri` 再注册会替换；dispose 句柄即移除。
- **注册即生效**：Bridge 监听 `onDidChangeContributions`，自动重新推 Monaco。**不要碰 `MonacoLoader` / `JsonSchemaBridgeContribution` 的推送逻辑**——它们已经消费所有注册项。
- **`fileMatch` 是 Monaco 的 glob**：Monaco 把每条 `fileMatch` 包成 `**/<pattern>` 去匹配规范化后的 model URI。常用 glob：`**/*.entity.json`。
- **精确单文件匹配**：若要只匹配「我们自己的某个绝对路径文件」（不误伤用户打开的同名外部文件，如 `~/.claude/settings.json`），用 `schemaFileMatchForUri(uri)`（`apps/editor/src/renderer/services/preferences/schemaFileMatch.ts`）把绝对路径转成精确 fileMatch。settings/keybindings/aiSettings 都用它；按 glob 匹配的新文件类型一般**不需要**。
- **校验呈现为 warning**：`schemaValidation: 'warning'`，未知 key / 不符 schema 是黄色波浪线而非红错（JSONC 注释静默）。

## 三条来源路径 → 选哪条

| 路径 | 声明者 | schema 来源 | 读文件位置 | 何时用 |
|---|---|---|---|---|
| **A. 扩展 `contributes.jsonValidation`** | 扩展开发者 | 扩展目录内 `.json` | **host 扫描时读并内联进 DTO** | **首选**：随某扩展分发的文件类型；可独立打包；对标 VSCode 主路径 |
| **B. 用户 `json.schemas` 设置** | 终端用户 | 内联对象 / 本地文件路径 | renderer 走 `IFileService` 读 | 用户自助把任意文件关联到任意 schema |
| **C. 内置声明表** | 核心代码 | 内联对象 | 无需读文件 | schema 必须活在核心而非扩展里（少见） |

判定：**随扩展走 → A**；**给用户开放自助配置 → B（已实现，通常无需改代码，只是用法）**；**核心内置且不属于任何扩展 → C**。多数新增"游戏内容 JSON"用 **A**。

## 路径 A：扩展 jsonValidation（首选，端到端示范见 `extensions/claude-helper`）

最省事的形态——**一个 declaration-only 扩展 = 一个 package.json**（schema 走本地文件或远程 http），无需 `main`、无需编译：

1. **建扩展目录** `extensions/<name>/`：
   - `package.json`：`name`（建议 `@universe-editor/<name>`）、`version`、`engines.universe`、本地 schema 时加 `files: ["schemas"]`（staging 靠它带入 schema 目录；纯远程 schema 无需）、
     ```json
     "contributes": {
       "jsonValidation": [
         { "fileMatch": ["**/*.entity.json"], "url": "./schemas/entity.json" }
       ]
     }
     ```
   - `schemas/<x>.json`：标准 JSON Schema（draft-07）。`fileMatch` 可为 string 或 string[]；`url` 为**相对扩展根的本地路径**或 **http(s) 远程地址**（见下「远程 http schema」）。
2. **完事**。打包/dev 自动发现（`extensionScanner.ts` 扫 `extensions/*`，`runtime-resources.mjs` 的 `discoverBuiltinExtensions` 按 `files` 带入），无需改 electron-builder.yml。

> 端到端实例 `extensions/claude-helper`：declaration-only + 远程 http schema，把 `**/.claude/settings.json` / `**/.claude/settings.local.json` 关联到官方 `https://json.schemastore.org/claude-code-settings.json`。无 `main`、无 `files`、无 build。

> 机制链路（已实现，**给已支持的扩展加 jsonValidation 条目无需动**；只有要扩展该贡献点本身的字段时才碰）：
> - 类型：`packages/extension-manifest/src/manifest.ts`（`IJsonValidationContribution` manifest 形态 / `IResolvedJsonValidation` host 已解析形态：本地→`schema` 内联、http→`url` 透传 / `IExtensionContributionsDto`）
> - zod 校验：`packages/extension-host/src/manifest.ts`（`jsonValidationSchema`）
> - host 解析：`packages/extension-host/src/extensionScanner.ts`（`resolveJsonValidation`：本地 url `path.resolve` → `readFile` → `JSON.parse` 内联成 `{fileMatch, schema}`，单条失败跳过并记日志；**http(s) url 透传成 `{fileMatch, url}` 不读盘**）+ `extensionService.ts` 的 `getContributions()` 注入 DTO
> - renderer 翻译进注册表：`apps/editor/src/renderer/services/extensions/ExtensionPointTranslator.ts` 的 `_registerJsonValidation()`（`uri: extension://<extId>/jsonvalidation/<index>`）；本地 `schema` 同步注册，http `url` 经注入的 `resolveRemoteSchema` 异步下载后注册（含 dispose 守卫）。`ExtensionsContribution.ts` 注入服务并构造 `resolveRemoteSchema`。

## 路径 B：用户 json.schemas 设置（已实现，多为用法）

用户在 settings.json 写：
```json
"json.schemas": [
  { "fileMatch": ["**/*.bar.json"], "schema": { "type": "object", ... } },
  { "fileMatch": ["**/*.baz.json"], "url": "/abs/path/to/schema.json" }
]
```
- 每条二选一：内联 `schema` 对象，或 `url`（本地绝对路径 / http(s) 远程地址，见下「远程 http schema」）。
- 变更即时重算（dispose 上轮句柄重注册）。
- 实现：`apps/editor/src/renderer/contributions/JsonSchemaAssociationsContribution.ts`（同时承载路径 C）；设置项 schema 也在此用 `ConfigurationRegistry.registerConfiguration` 自注册（`id: 'json'`）。

## 远程 http(s) schema（路径 A 与 B 通用）

Monaco 不抓网络，所以远程 schema 必须**先下载成文本、`JSON.parse` 成对象**再注册。下载在 **main 进程**完成（带缓存/离线回退），renderer 做信任策略后调用——对标 VSCode 的 client/server 分工。

- **main 下载器**：`apps/editor/src/main/services/remoteSchema/remoteSchemaMainService.ts`（`IRemoteSchemaService.fetchSchema(url) → {ok, content} | {ok:false, error}`）。纯下载器**无策略**：`<userData>/json-schema-cache/` 缓存、ETag 重验证、TTL（12h）内不联网、网络失败回退陈旧缓存。跨进程接线见 `shared/ipc/remoteSchemaService.ts` + 套路 C 六处。
- **renderer 策略 + 解析**：`apps/editor/src/renderer/services/preferences/schemaUrlResolver.ts` 的 `resolveSchemaFromUrl(url, deps, label)`——本地路径走 `IFileService`；http(s) 先查 `json.schemaDownload.enable`（默认 true）+ `json.schemaDownload.trustedDomains`（白名单前缀，默认含 schemastore / json-schema.org），过了才调 `remoteSchema.fetchSchema`。路径 A（`ExtensionsContribution` 构造 `resolveRemoteSchema`）与路径 B（`JsonSchemaAssociationsContribution._resolveSchema`）**复用同一解析器**。
- **安全**：远程下载是联网行为，默认仅限白名单域名；非白名单 url 被跳过并 warn。要放行新域名，往 `json.schemaDownload.trustedDomains` 加 `"https://<prefix>/": true`。

## 路径 C：内置声明表（核心内置，少见）

往 `apps/editor/src/renderer/services/preferences/builtinJsonSchemas.ts` 的 `BUILTIN_JSON_SCHEMAS` 加一条：
```ts
{ key: 'level', fileMatch: ['**/*.level.json'], schema: { type: 'object', ... } }
```
`JsonSchemaAssociationsContribution` 构造时遍历注册（`uri: builtin://schemas/<key>`）。**优先考虑路径 A**——除非该 schema 确实属于核心而非任何扩展。

## 直接代码注册（动态/依赖运行时数据的 schema）

若 schema 内容要**从运行时数据动态生成**（如随可用 AI 模型刷新 enum、随配置项注册刷新 settings schema），照 `AiConfigurationContribution.ts` / `JsonSchemaBridgeContribution.ts` 的范式**写一个 Contribution 类**：注入数据源服务 → 监听其变更事件 → `_refresh()` 里重建 schema 并 `JSONContributionRegistry.registerSchema(...)`（用 `MutableDisposable` 或句柄字段管理 dispose）→ 在 `contributions/index.ts` 以 `WorkbenchPhase.BlockStartup` 注册。这是「声明式三条路径」之外、给**动态 schema** 的逃生舱。

## 加测试

- **扩展 jsonValidation（路径 A 机制）**：`packages/extension-host/src/__tests__/extensionScanner.test.ts`（本地 url 读取内联、fileMatch 归一为数组、坏文件跳过仍保留扩展、**http url 透传不读盘**）；`manifest.test.ts`（zod 接受合法、拒绝缺 url）；`ExtensionTranslation.test.ts`（本地 schema 同步注册、**http url 经注入的 `resolveRemoteSchema` 异步注册**、dispose 移除）。
- **路径 B/C（contribution）**：`apps/editor/src/renderer/contributions/__tests__/JsonSchemaAssociationsContribution.test.ts`——用真实 `ConfigurationService` + fake `IFileService` + fake `IRemoteSchemaService`，断言内联/本地 url/可信 http url 正确注册、坏 url 跳过、download 关闭或非白名单 http 跳过、`json.schemas` 变更后清旧注册新。该测试 await 两个 microtask 让异步 refresh 落定。属 **renderer-node** project。
- **远程下载器/解析器**：`apps/editor/src/main/services/remoteSchema/__tests__/remoteSchemaMainService.test.ts`（stub `fetch` + tmp 缓存目录：200 写缓存、TTL 内不联网、304 返回缓存、网络失败回退陈旧缓存、坏 JSON 报错）；`apps/editor/src/renderer/services/preferences/__tests__/schemaUrlResolver.test.ts`（`isTrustedSchemaUrl` 前缀匹配、本地读、可信 http 下载、非白名单/禁用/下载失败/坏 JSON 返回 undefined）。

## 验证

```bash
# 改了 platform / extensions-common / extension-host：先重建 dist，apps 才看得到
pnpm --filter @universe-editor/platform build
pnpm --filter @universe-editor/extensions-common --filter @universe-editor/extension-host build
pnpm ext:build                 # 改了 extensions/* 后重建（declaration-only 扩展会被 turbo 跳过 build，无妨）

pnpm check                     # lint + typecheck + test，仅看错误输出（错误路径测试的 stderr 噪音非失败）
```
手动端到端（`pnpm dev`）：新建一个匹配 `fileMatch` 的文件（如 `foo.entity.json`）→ 打开 → 应有补全、未知 key 黄色波浪线、hover 显示字段 description。

> e2e：本仓库本地 Windows 跑 e2e 会因 Playwright electron.launch 失败，交给 CI；纯 schema 关联不涉及交互流程，一般不需要 e2e。

## 易踩坑速记

1. **Monaco 不读文件**（`schemaRequest: 'ignore'`）——指向文件的 schema 必须先读成对象再注册。路径 A 在 host 读，路径 B 在 renderer 读，路径 C 本就是对象。
2. **改了 platform/extensions-common 没重建 dist**——apps 用的是 `dist/`，`pnpm dev` 下 watcher 自动重建，否则手动 build，否则看不到新类型/新逻辑。
3. **空 enum 让所有值报错**——动态 enum（如模型 id）为空时应**省略 enum**而非给 `[]`（见 `AiConfigurationContribution` 的 `buildSchema` 注释）。
4. **精确 vs 宽泛 fileMatch**——只想匹配自己的某个绝对路径文件用 `schemaFileMatchForUri`（避免误伤外部同名文件，commit `da68a6f1` 的教训）；按文件类型铺开则用 glob。
5. **远程 url 走下载器**——路径 A/B 的 http(s) url 由 main `IRemoteSchemaService` 下载（缓存/离线回退）、renderer 经 `json.schemaDownload.enable` + `trustedDomains` 白名单校验后注册；非白名单域名被跳过。要本地 path/内联则各按原样。
6. **declaration-only 扩展无需 main/build**——只有 `package.json` + schema 文件即可；记得 `files: ["schemas"]` 否则打包不带入 schema。
7. **strict 模式**（`additionalProperties: false`）让未知 key 报 warning——给会动态扩字段的文件类型慎用，或在数据源变更时重建 schema（见 settings.json 的做法）。

## 关键参考路径

- `packages/platform/src/configuration/jsonSchemaRegistry.ts` —— 唯一出口 `JSONContributionRegistry` + `ISchemaContribution` / `IJSONSchema` 类型
- `apps/editor/src/renderer/contributions/JsonSchemaBridgeContribution.ts` —— 注册表 → Monaco 的自动桥接（**勿改推送逻辑**）；动态 schema 范式
- `apps/editor/src/renderer/contributions/AiConfigurationContribution.ts` —— 动态 schema（随模型刷新 enum）范式
- `apps/editor/src/renderer/contributions/JsonSchemaAssociationsContribution.ts` —— 路径 B（用户 json.schemas）+ 路径 C（内置表）实现
- `apps/editor/src/renderer/services/preferences/builtinJsonSchemas.ts` —— 路径 C 声明表
- `apps/editor/src/renderer/services/preferences/schemaFileMatch.ts` —— 绝对路径 → 精确 fileMatch
- `apps/editor/src/renderer/services/extensions/ExtensionPointTranslator.ts` —— 路径 A 的 `_registerJsonValidation`（本地 schema 同步 / http url 异步解析）
- `apps/editor/src/renderer/contributions/ExtensionsContribution.ts` —— 注入服务、构造 `resolveRemoteSchema` 传给 translator
- `packages/extension-host/src/extensionScanner.ts` —— 路径 A 的 host 端解析（`resolveJsonValidation`：本地内联 / http 透传）
- `packages/extension-manifest/src/manifest.ts` —— jsonValidation 贡献点类型（manifest / resolved / DTO）
- `apps/editor/src/main/services/remoteSchema/remoteSchemaMainService.ts` —— 远程 schema 下载器（缓存 / ETag / 离线回退）
- `apps/editor/src/renderer/services/preferences/schemaUrlResolver.ts` —— 本地/远程 url 统一解析 + 信任策略（路径 A/B 复用）
- `extensions/claude-helper/` —— 路径 A 端到端示范（declaration-only + 远程 http schema）
- `apps/editor/src/renderer/workbench/editor/monaco/MonacoLoader.ts` —— `setJsonSchemas` + `BASE_JSON_DIAGNOSTICS`（`schemaRequest: 'ignore'` 的根因）
- `apps/editor/CLAUDE.md` —— 套路 C（跨进程服务）、套路 D（Contribution）、套路 I（AI 配置，动态 schema 参照）

## 其它

- 后续用本 skill，发现新经验，需同步更新本文件
