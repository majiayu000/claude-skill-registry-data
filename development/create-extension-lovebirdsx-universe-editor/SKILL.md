---
name: create-extension
description: 从零创建一个新插件（extension）时使用。当任务是新建内置插件、照 numbered-bookmarks/ai/git 的样子起新扩展、加 commands/menus/keybindings/configuration 贡献点、activate 里注册命令/状态栏/装饰/SCM、插件不激活/被扫描器跳过、或 manifest 文案本地化（package.nls）时使用。
---

# 从零创建一个新插件（extension）

> 本 skill 面向**仓库内内置扩展**（`extensions/<name>/`，in-workspace）。**仓库外第三方作者**走 npm 脚手架 `npm create @universe-editor/extension`（`packages/create-extension`），不要照本 skill 的外部目录套路手工搭建。

本仓库的扩展模型完整对标 VSCode：一个插件是 `extensions/<name>/` 下的一个目录，由 **manifest（`package.json`）声明贡献点 + 激活时机**，可选地带 **运行时代码（`src/extension.ts`）** 在激活时通过 `@universe-editor/extension-api` 门面注册命令/菜单/键位/配置/provider。放进 `extensions/` 目录即被扫描器自动发现，**无需在主程序手动注册**。

> ⚠️ 第一原则：**先判断你要的是"纯声明"还是"有代码"**。很多需求（给某 JSON 配 schema、给已有命令加键位、挂个菜单项）只需一个 `package.json`，**不写一行 TS、不需要构建**（见 `claude-helper`）。只有当激活时要跑逻辑（注册命令处理器、装饰、状态栏、SCM、provider）才需要 `src/extension.ts` + esbuild。别默认从代码起步。
>
> ⚠️ 第二原则：**`engines.universe` 必须能满足当前 host API 版本**。host API 版本 = `packages/extension-api/src/index.ts` 的 `version` 常量（现为 `0.12.0`）。范围写不对，扫描器会**静默跳过整个插件**（只在扩展输出通道 `console.error` 一行），表现为"插件完全不生效"。**统一写 `">=0.1.0 <1.0.0"`**，别用 `^0.1.0`（0.x 下 caret 锁 minor，`0.12.0` 会被挡下）。原因见文末"engines 兼容红线"。

## 两种形态 → 选哪种

| 你的需求 | 形态 | 需要的文件 | 范例 |
|---|---|---|---|
| 只贡献静态声明：jsonValidation、给已有命令配键位、挂菜单项 | **纯声明** | 仅 `package.json` | `extensions/claude-helper/` |
| 激活时要跑代码：注册命令处理器 / 状态栏 / 装饰 / SCM / provider | **有代码** | manifest + esbuild + `src/extension.ts` + 测试 | `extensions/ai/`（最简）、`numbered-bookmarks/`（完整）、`git/`（全贡献点） |

> 若要做的是**语言能力 provider**（definition/hover/completion/诊断…）→ 用 skill `extend-language-plugin`；**webview/自定义编辑器预览** → 见 `apps/editor/src/renderer/workbench/webview/CLAUDE.md`（新预览扩展范例照抄 `extensions-external/pdf/CLAUDE.md`）；**只接 JSON schema** → 用 skill `add-json-schema-association`。这些是本套路的特化场景，已有专门文档。

## 纯声明型：只需一个 package.json

照抄 `extensions/claude-helper/package.json`。**没有 `main`、没有 `activationEvents`、没有 scripts/devDependencies**——扫描器 `mainPath` 为 undefined 即视为 declaration-only。

```json
{
  "name": "@universe-editor/<name>",
  "version": "0.0.1",
  "private": true,
  "type": "module",
  "displayName": "Human Readable Name",
  "description": "...",
  "engines": { "universe": ">=0.1.0 <1.0.0" },
  "contributes": {
    "jsonValidation": [
      { "fileMatch": ["**/foo.config.json"], "url": "https://.../schema.json" }
    ]
  }
}
```

## 有代码型：起骨架（照抄 `extensions/ai`，最简代码插件）

```
extensions/<name>/
  package.json         manifest + main:"dist/extension.js" + activationEvents + files:["dist"] + scripts + devDependencies
  esbuild.config.mjs   从 ai/numbered-bookmarks 逐字复制，仅改日志 label（bundle→dist/extension.js，注入 createRequire banner）
  tsconfig.json        extends "@universe-editor/config-ts/node"，noEmit，types:["node"]，include:["src","esbuild.config.mjs"]
  vitest.config.ts     defineConfig({})（空，默认 node 环境）
  src/extension.ts     export activate(context) + deactivate()
  src/*.ts             （可选）把可测逻辑抽成纯模块
  src/__tests__/*.test.ts  （可选）vi.mock extension-api + 动态 import 被测模块
```

`package.json` 相比纯声明型多出的字段（**scripts / devDependencies 六件套逐字复制 `ai` 的**）：
```json
"main": "dist/extension.js",
"files": ["dist"],
"activationEvents": ["onCommand:<name>.someCommand"],
"scripts": {
  "build": "node esbuild.config.mjs",
  "dev": "node esbuild.config.mjs --watch",
  "typecheck": "tsc --noEmit",
  "test": "vitest run",
  "lint": "eslint src",
  "clean": "node -e \"require('node:fs').rmSync('dist',{recursive:true,force:true})\""
},
"devDependencies": {
  "@universe-editor/config-ts": "workspace:*",
  "@universe-editor/extension-api": "workspace:*",
  "@types/node": "catalog:", "esbuild": "catalog:", "eslint": "catalog:",
  "typescript": "catalog:", "vitest": "catalog:"
}
```

## src/extension.ts：activate / deactivate / context

```ts
import { commands, type ExtensionContext } from '@universe-editor/extension-api' // 门面 namespace
import { doThing } from './thing.js' // 相对 import 必带 .js 后缀（ESM/NodeNext）

export function activate(context: ExtensionContext): void { // 可同步，也可 async 返回 Promise
  context.subscriptions.push( // 一切注册结果都 push 到 subscriptions，host 在停用时统一 dispose
    commands.registerCommand('<name>.someCommand', (arg) => doThing(arg)),
  )
}
export function deactivate(): void {} // 通常空实现——subscriptions 已托管
```

- **`ExtensionContext`**：`subscriptions: Disposable[]`、`extensionPath: string`、`globalState: Memento`（跨工作区 KV）、`workspaceState: Memento`（工作区级 KV）。`Memento` = `get<T>(key, default?)` / `update(key, value): Promise<void>`。**持久化状态用 `workspaceState`，绝不往工作区写 json 文件**（见 numbered-bookmarks）。
- **日志走 `console.error`**——stdout 是 host↔renderer 的 RPC 通道，普通日志只能走 stderr（约定加 `[<name>] ...` 前缀）。
- **`activate` 只接线**：把有逻辑的部分抽成纯模块（`commitMessage.ts` / `bookmarks.ts` …）再单测，入口本身一般不测。

## extension-api 门面（`packages/extension-api/src/index.ts` 末尾的 namespace 常量）

| namespace | 能力 | 备注 |
|---|---|---|
| `commands` | `registerCommand` / `executeCommand<T>` | |
| `window` | 消息框 / `showQuickPick` / `showInputBox` / `createStatusBarItem` / `createOutputChannel` / `getActiveTextEditor` / `onDidChangeActiveTextEditor` / `createTextEditorDecorationType` / `registerCustomEditorProvider` | |
| `workspace` | `rootPath` / `fs`（受控 FS 网关）/ `textDocuments` / `onDidOpen·Change·CloseTextDocument` / `getConfiguration(section)` | 配置读 `getConfiguration('<name>').get(key, default)` |
| `languages` | 14 类 provider 注册 + `createDiagnosticCollection` | 语言特性走 skill `extend-language-plugin` |
| `scm` | `createSourceControl(id, label, rootUri?)` | |
| `ai` | `getModels` / `sendRequest` / `computeTokenLength` … | **仅 trusted（内置）插件可用**；restricted（用户装的）拿不到此 proxy |

门面被 esbuild **内联进每个插件**，运行时委托给 host 装在 `globalThis` 的 bridge 越进程 RPC。所以 `@universe-editor/extension-api` 只需列 devDependency。

## contributes 贡献点写法（全量 schema 见 `packages/extension-manifest/src/manifest-schema.ts`）

- **commands**：`{ command, title, category?, icon? }`（`icon` 用 codicon 名如 `"bookmark"`）
- **keybindings**：`{ command, key: "ctrl+shift+0", mac?, when?: "editorTextFocus" }`
- **configuration**：`{ title, properties: { "<name>.foo": { type, default, description, minimum?, enum?, items? } } }`（`type` ∈ string/number/boolean/array/object/null）
- **menus**：`{ "<内置菜单位或自定义submenu id>": [ { command | submenu, group?: "navigation@1", when?, icon? } ] }`（`command`/`submenu` 二选一必填）。内置菜单位如 `scm/title`、`scm/inputBox`、`scm/resourceState/context`、`editor/title` —— 完整样板见 `git`
- **submenus**：`{ id: "<name>.someMenu", label, icon? }`（配合 menus 里 `{submenu: "<name>.someMenu"}`）
- **jsonValidation** / **customEditors**：见各自专门 skill
- 未知贡献点 / 未知字段被 zod `.passthrough()` 容忍（前向兼容）；但 `activationEvents`、`engines`、命令/菜单结构是**强校验**，不合法整插件被跳过

**activationEvents** 合法值（`extension-manifest/src/activation.ts`）：`"*"`（eager，慎用）、`"onStartupFinished"`、`"onCommand:<id>"`、`"onLanguage:<id>"`、`"onView:<id>"`、`"onCustomEditor:<viewType>"`。懒激活优先（如命令型插件用 `onCommand:`），全局常驻才用 `onStartupFinished`。

## NLS 本地化 manifest 文案（可选，机制见 `packages/extension-host/src/nls.ts`）

1. manifest 里所有用户可见字符串写 `%key%` 占位（command title / submenu label / config description）
2. 插件根旁放 `package.nls.json`（英文默认，必须）+ `package.nls.<locale>.json`（如 `package.nls.zh-cn.json`）
3. **NLS 文件必须列进 `package.json` 的 `files` 数组**，否则打包丢失（见 `git` 的 `files:["dist","package.nls.json","package.nls.zh-cn.json"]`）
4. locale bundle 合并覆盖默认（缺 key 回退英文，再缺保留字面 `%key%` 让缺翻译可见）；locale 经 `env.UNIVERSE_DISPLAY_LOCALE` 传入
5. **运行时代码内**的消息本地化是另一套（不走 manifest NLS）：仿 `git/src/nls.ts` 内嵌 locale 表 + `localize(key, defaultMsg, vars?)`，支持 `{0}` 插值。两者互不相关

## 加载链路（放进 extensions/ 就被自动发现，无需手动注册）

- **`extensions/*` 在 pnpm workspace 内**（`pnpm-workspace.yaml` globs 含 `'extensions/*'`）。
- 扫描目录 `apps/editor/src/main/services/extensionHost/extensionHostMainService.ts`：dev/e2e = repo `extensions/`（`resolveFromRepo`），packaged = `resources/extensions/`。目录经 env `UNIVERSE_BUILTIN_EXTENSIONS_DIR` 传给 host。
- host bootstrap `packages/extension-host/src/bootstrap.ts`：`import { version as HOST_API_VERSION } from '@universe-editor/extension-api'` → `scanExtensions(dir, HOST_API_VERSION, locale)`。
- 扫描器 `packages/extension-host/src/extensionScanner.ts` 的 `scanOne` 顺序：读 package.json → 加载 NLS → 翻译 `%key%` → zod 校验 → **`satisfies(hostApiVersion, engines.universe)` 版本检查**（`:88`）→ 解析 jsonValidation → 组装。任一步抛错则 `console.error` 跳过该插件、不阻塞其余。

## engines 兼容红线（本 skill 的头号坑，务必看）

`satisfies` 是**自研极简 semver**（`packages/extension-manifest/src/semver.ts`），**不是 npm 的 semver**：

- 支持：exact / `*` / `x` / partial(`1`,`1.2`) / `^` / `~` / 比较符 / **空格连接的 AND**（`>=0.1.0 <1.0.0`）。
- **不支持**：`||`（OR）、hyphen range（`1.0.0 - 2.0.0`）——一律 **fail-closed 直接拒绝加载**。
- pre-1.0 的 `^` 按 npm 语义**锁 minor**：`^0.1.0` = `>=0.1.0 <0.2.0`，`0.12.0` 不满足 → 插件被跳过。

**规则**：内置插件统一写 `">=0.1.0 <1.0.0"`（接受整个 0.x）。若插件依赖某次 minor 引入的新 API，把下界抬到那次 minor（如 Tree View 需要 `">=0.12.0 <1.0.0"`）。

**当 `packages/extension-api` 的 `version` bump 时**（走 `COMPATIBILITY.md` 的破坏性变更流程），必须**同步检查全部内置插件的 `engines.universe`**——这一步漏了会导致所有插件被静默拒载（历史事故：0.1.0→0.2.0 时内置插件仍写 `^0.1.0`，全崩）。

## 加测试（node 环境，`src/__tests__/*.test.ts`）

mock extension-api 的标准套路（见 `extensions/ai/src/__tests__/commitMessage.test.ts`）：

```ts
import { describe, it, expect, vi } from 'vitest'
const executeCommand = vi.fn()
vi.mock('@universe-editor/extension-api', () => ({
  AiMessageRole: { System: 0, User: 1, Assistant: 2 }, // value 枚举要手动补
  commands: { executeCommand: (...a) => executeCommand(...a) },
  workspace: { getConfiguration: () => ({ get: (k, d) => d }) },
}))
const { generateCommitMessage } = await import('../commitMessage.js') // mock 提升，之后再动态 import 被测模块
```

只 stub 用到的 namespace 成员；枚举等 value 手动提供；逻辑抽到纯模块单测，入口 `extension.ts` 一般不测。

## 验证

```bash
# 改了 platform/extension-manifest/extensions-common/extension-host 后先重建 dist，apps/host 才看得到（pnpm dev 下 watcher 自动重建）
pnpm --filter @universe-editor/extension-manifest --filter @universe-editor/extensions-common --filter @universe-editor/extension-host build

pnpm ext:build   # 重建 extensions/*（turbo，declaration-only 插件无 build 会被跳过，无妨）
pnpm check       # lint + typecheck + test，仅看错误输出（被测错误路径的 stderr 噪音非失败）
```

- 手动端到端（`pnpm dev`）：触发插件的激活事件（命令面板跑命令 / 打开匹配文件），确认贡献点生效。
- **插件"完全不生效"排查**：多半是 scanner 跳过了它——去应用的扩展输出通道找 `[ext-host] skipping <name>: ...`。最常见原因是 `engines.universe` 不满足（见红线）或 manifest zod 校验失败。诊断时可临时在 e2e/dev 把 host stderr echo 出来（host stderr 默认只进扩展输出通道，不进日志文件）。
- 涉及交互流程用 `pnpm e2e`（本地 Windows 跑 e2e 有 Playwright launch flake，交给 CI）。

## 关键参考路径

- `extensions/claude-helper/` —— 纯声明型范例（仅 package.json）
- `extensions/ai/` —— 最简代码插件（单命令 + menus + configuration + 测试 mock 范式）
- `extensions/numbered-bookmarks/` —— 完整代码插件（commands/keybindings/configuration + workspaceState 持久化 + 装饰 + 多测试文件）
- `extensions/git/` —— 全贡献点样板（submenus / 嵌套 menus / when 上下文键 / manifest NLS + 运行时 NLS）
- `packages/extension-api/src/index.ts` —— 门面 namespace + `version` 常量（= host API 版本）+ `ExtensionContext`/`Memento` 类型
- `packages/extension-api/COMPATIBILITY.md` —— API 版本承诺 + 破坏性变更流程（bump version 必同步内置插件 engines）
- `packages/extension-manifest/src/manifest-schema.ts` —— contributes 全量 zod schema
- `packages/extension-manifest/src/activation.ts` —— 合法 activationEvents + 构造器
- `packages/extension-manifest/src/semver.ts` —— 自研 `satisfies`（engines 检查用；不支持 `||`/hyphen）
- `packages/extension-host/src/extensionScanner.ts` —— scanOne 校验顺序 + engines satisfies 检查（`:88`）
- `packages/extension-host/src/bootstrap.ts` —— HOST_API_VERSION 来源 + scanExtensions 调用
- `packages/extension-host/src/nls.ts` —— manifest `%key%` 本地化实现
- `apps/editor/src/main/services/extensionHost/extensionHostMainService.ts` —— 扫描目录解析（dev vs packaged）+ env 传参
- `apps/editor/CLAUDE.md` —— 套路 A（命令/键位 Action2）、套路 D（Contribution）；`docs/user/zh-CN/customization/extensions.md` —— 用户视角说明
- memory：`extension-system-progress` / `extension-manifest-nls` / `typescript-builtin-plugin`

## 其它

- 涉及**用户可见文案/命令名/键位**改动时，检查 `docs/user/zh-CN/customization/extensions.md` 是否需同步。
- 新建 skill 后跑 `pnpm skills:policy` 生成 `agents/openai.yaml`（codex 侧 manual-only 策略），CI 会用 `pnpm skills:policy:check` 校验。
- 后续用本 skill 发现新经验，同步更新本文件。
