---
name: register-monaco-command
description: 把 Monaco 编辑器命令接进命令面板 + Keyboard Shortcuts 编辑器 + 可配快捷键。当用户说某 Monaco 命令在命令面板搜不到 / 快捷键编辑器列不出 / 右键能用但配不了键 / 想给它配快捷键，或要新增包装 Monaco 内置命令的 Action2 时使用。
---

# 把 Monaco 命令接进项目命令面板 + 可配快捷键

本仓库的命令面板（`ShowCommandsAction`）和 Keyboard Shortcuts 编辑器只认**项目自己的** `CommandsRegistry` / `KeybindingsRegistry` 里的命令。Monaco 内置命令默认大多不在其中，能否接进来、怎么触发，取决于该命令在 Monaco 侧用哪种机制注册。核心套路：**先判定命令属于 Monaco 的哪套注册机制 → 按结果选集成路径（多数 EditorAction 已自动桥接，无需新增代码）→ 若要项目级默认键则包装成 Action2 并拆掉 Monaco 自身默认键防双触发 → 注册 → 加测试 → 验证**。

> ⚠️ 第一原则：**先判定类型，别凭命令名猜**。两套机制的可见性、`editor.getAction()` 行为、触发方式完全不同，判错会写出永远不生效（或双触发）的代码。

## 核心机制：Monaco 的两套命令注册（必须先理解）

Monaco 用两种互不相通的机制注册编辑器命令：

| | `registerEditorAction` | `registerAction2` |
|---|---|---|
| 典型命令 | find / replace / format / rename / quickOutline | goto/peek 全系列（Definition、Type Definition、Implementations、References，`goToCommands.js`） |
| 注册去向 | `EditorExtensionsRegistry` | Monaco **内部 platform** 的 CommandsRegistry + MenuRegistry(右键 EditorContext) + standalone KeybindingService（F12 等默认键） |
| `editor.getAction(id)` | **非 null**，可 `.run()` | **返回 `null`** |
| `getSupportedActions()` | 可见 | 不可见 |

关键事实：`codeEditorWidget` 只从 `EditorExtensionsRegistry` 填充内部 `_actions`。所以：

- **EditorAction 型**能被项目的自动桥接（`monacoActionsBridge`）和命令面板的枚举抓到。
- **action2 型**两者都抓不到——它从未进入项目的 CommandsRegistry / KeybindingsRegistry，这正是 goto/peek「右键能用、F12 能跳，但命令面板搜不到、改不了键」的根因。

## 判定流程

### 1. 判定命令属于哪套机制
- **运行期最快**：打开一个文件，`FileEditorRegistry.get(input)?.getAction('<id>')`——返回非 null → **EditorAction**；返回 `null` → **action2 或 core 命令**。
- **源码确认**：在 `node_modules/monaco-editor` 里 grep 该 id，看注册调用是 `registerEditorAction(...)` 还是 `registerAction2(...)` / 直接 `MenuRegistry.appendMenuItem`。
- **存疑就当 action2 处理**（走路径 2 的 `trigger` 分发，对两类都安全；而 `getAction().run()` 只对 EditorAction 有效）。

### 2. 选集成路径

**路径 0 — EditorAction 已自动桥接，通常无需新增代码**
所有 EditorAction（+ undo/redo/selectAll 等手列 core 命令）在 `MonacoLoader` 启动时由 `bridgeAllMonacoActions()`（`monacoActionsBridge.ts`）自动镜像进项目 `CommandsRegistry`，其默认键存进侧表（`getMonacoDefaultKeybinding(id)`）而**不进** `KeybindingsRegistry`——把默认键的上下文相关分发留给 Monaco（如 find widget 里的 ESC、IntelliSense 的 ESC）。因此这些命令本就出现在 Keyboard Shortcuts 编辑器、可被用户改键。
→ **先确认目标命令是不是已经在这条路里**（打开快捷键编辑器搜一下）。是 → 大概率无需写任何代码。只有当你要给它一个**项目级显式默认快捷键**、或自定义标题/分组/precondition 时，才走路径 1。

**路径 1 — EditorAction 型的显式 Action2 包装**
dispatch 用 `editor.getAction(actionId)?.run()`。模板见 `searchActions.ts` 的 `runActiveMonacoAction`：

```ts
function runActiveMonacoAction(accessor: ServicesAccessor, actionId: string): void {
  const groups = accessor.get(IEditorGroupsService)
  const active = groups.activeGroup.activeEditor
  if (!(active instanceof FileEditorInput)) return
  const editor = FileEditorRegistry.get(active)
  const action = editor?.getAction(actionId)
  if (action) void action.run()
}
```

**路径 2 — action2 型的显式 Action2 包装**
`getAction(id)` 对它返回 null，必须用 `editor.trigger(source, id, payload)`——统一入口，未命中 `_actions` 时落到 standalone commandService 执行 action2。**触发前必须先 `editor.focus()`**：action2 内部用 `getFocusedCodeEditor() || getActiveCodeEditor()` 解析目标编辑器，而从命令面板触发时编辑器已失焦。模板见 `gotoLocationActions.ts` 的 `runMonacoNavAction` + 表驱动工厂：

```ts
function runMonacoNavAction(accessor: ServicesAccessor, actionId: string): void {
  const groups = accessor.get(IEditorGroupsService)
  const active = groups.activeGroup.activeEditor
  if (!(active instanceof FileEditorInput)) return
  const editor = FileEditorRegistry.get(active)
  if (!editor) return
  editor.focus() // ← 关键：action2 靠 focused/active editor 解析目标
  editor.trigger('universe', actionId, {})
}
```

命令集稳定且小时，用**一张声明表 + 工厂**生成 Action2 子类（见 `gotoLocationActions.ts` 的 `NAVIGATION_COMMANDS` + `createNavAction`），比逐个手写类好维护。

**路径 3 — 内核从没配过键的命令：只补键，不新增命令**
内核里有一类 EditorAction 自带实现却**没有任何默认键**（如 `editor.action.sortLinesAscending` / `sortLinesDescending`——Monaco 的 `linesOperations.js` 就没给 `_kbOpts`）。这类命令已被路径 0 镜像，只缺一键，于是把键填进 `monacoExtraKeybindings.ts` 的数据表即可（与 compat 表同一注册机制，理由不同：那张表是「原生键被占后补备选键」）。

```ts
const WHEN = `${EDITOR_TEXT_FOCUS} && !editorReadonly`
export const MONACO_EXTRA_KEYBINDINGS: readonly IMonacoCommandKeybinding[] = [
  { id: 'editor.action.sortLinesAscending', key: 'f9', when: WHEN },
]
```

**别为它走路径 1**：同名 id 会在项目 `CommandsRegistry` 里叠出第二个 handler，命令面板也多一条重复条目——而你并没有新命令要注册，只有键要补。

### 3. 处理默认键双触发（给 action2 配了项目默认键时必看）
现象：你在项目 Action2 上声明了默认键（如 `f12`），而 Monaco 自身的同名默认键还在 → 一次按键被触发两次。
解法：在 `MonacoLoader`（`loadMonaco()` 内 Monaco 就绪后）对**有默认键**的 id 批量拆掉 Monaco 默认键：

```ts
for (const id of monacoNavDefaultKeybindingCommandIds) {
  monacoMod.editor.addKeybindingRule({ keybinding: 0, command: `-${id}` })
}
```

`keybinding: 0` + `command: '-<id>'` 表示移除该命令的默认键绑定；命令本身仍注册、仍可 `trigger`。用一个**导出的「带默认键 id 列表」**做两端单一事实源（见 `gotoLocationActions.ts` 的 `monacoNavDefaultKeybindingCommandIds`，由声明表过滤生成），避免 MonacoLoader 与 Action 表脱节。先例：quickOutline（`'-editor.action.quickOutline'`）。
> 无默认键的命令无需此步。路径 0/1 的 EditorAction 默认键走侧表、由 Monaco 自身分发，也无需此步。

### 4. 注册 + 对齐 VSCode
- 在 `actions/index.ts` 对应分组里 `registerAction2(MyAction)`；若是 Action2 列表则 `for (const a of actions) registerAction2(a)`。
- **id 与默认键对齐 VSCode 原生**（apps/editor/CLAUDE.md 末条：对标 vscode 的功能，command id 和默认键须一致）。项目 `CommandsRegistry` 与 Monaco 内部 `CommandsRegistry` 是不同实例，复用同名 id **不冲突**（项目侧命中项目命令，`run()` 里再 `trigger` 同名 id 走 Monaco service）。
- Action2 的 `precondition` 用项目已 seed 的 ContextKey（如 `'hasActiveEditor'`，字符串会在 Action2 内部 `ContextKeyExpr.deserialize`；确保 key 已在 `ContextKeyContribution` seed）。`f1: true` 让它进命令面板，`category` 用 `localize(...)` 归类。

### 5. 加测试
参考 `gotoLocationActions.test.ts`（renderer 项目，happy-dom）。mock `FileEditorRegistry.register(input, { trigger: triggerSpy, focus: focusSpy } as never)`，断言：
1. `registerAction2` 后命令进 `CommandsRegistry`，且 `MenuRegistry.getMenuItems(MenuId.CommandPalette)` 含该 id（`f1` 生效）。
2. 默认键经 `KeybindingsRegistry.resolveKeybinding('<key>')` 命中正确 id。
3. `run()`（取 `CommandsRegistry.getCommand(id).handler` 在 `inst.invokeFunction` 里调）——路径 2 断言**先 focus 后 trigger** 正确 id（`expect(triggerSpy).toHaveBeenCalledWith('universe', '<id>', {})`）；路径 1 断言调了 `getAction(id).run()`。
4. 无 active editor 时 `run()` no-op（trigger 不被调用）。
afterEach 记得 `FileEditorRegistry._resetForTests()` / `MonacoModelRegistry._resetForTests()`。

### 6. 验证
```bash
pnpm check                # lint + typecheck + test，仅看错误输出
pnpm e2e                  # 必要时跑 commandPalette / keyboardShortcut 冒烟
```
命令面板（`ShowCommandsAction` 枚举 `CommandsRegistry.getCommands()`）与 Keyboard Shortcuts 编辑器（枚举有 metadata 的命令）会**自动收录**新 Action2，无需改动它们。手动验证：打开文件 → 命令面板搜命令能执行 → 快捷键编辑器能看到并改键 → 按默认键行为正常且**不双触发**。

### 7. 沉淀经验
遇到新命令/新坑（如某 action2 还依赖额外 context key、某命令 payload 非空、某命令需要 declaration provider 才生效），追加到下面**案例库**。

## 案例库

> 每条：命令/场景 → 属哪套机制 → 怎么接 → 文件锚点。新经验往下追加。

### 案例 1：Go to / Peek 导航全系列（action2 型）
- **命令**：`editor.action.revealDefinition`（Go to Definition, f12）、`peekDefinition`(alt+f12)、`goToTypeDefinition`、`peekTypeDefinition`、`goToImplementation`(ctrl+f12)、`peekImplementation`(ctrl+shift+f12)、`goToReferences`(shift+f12)、`referenceSearch.trigger`（Peek References）。
- **机制**：全部 `registerAction2`（`goToCommands.js`），`editor.getAction()` 返回 null，故命令面板/快捷键编辑器原本都抓不到。
- **怎么接**：走**路径 2**——表驱动工厂生成 8 个项目 Action2（`category: 'Go'`、`f1: true`、`precondition: 'hasActiveEditor'`、声明默认键），`run()` 里 `focus()` + `trigger('universe', id, {})`；在 `MonacoLoader` 对有默认键的 5 个 id 做 `addKeybindingRule({keybinding:0, command:'-<id>'})` 防双触发；`actions/index.ts` 用 `for...of registerAction2`。id 与默认键全对齐 VSCode。
- **取舍**：未走「自动镜像 Monaco 内部 platform registry」的路（需 import 不稳定内部模块、各命令 precondition/键差异大、脆弱）。命令集稳定且小 → 显式声明表最清晰。Declaration 系列因项目未注册 declarationProvider，本次未含。
- **锚点**：`apps/editor/src/renderer/actions/gotoLocationActions.ts`（模板）、`actions/index.ts`（“Go — location navigation” 分组）、`workbench/editor/monaco/MonacoLoader.ts`（拆默认键，紧挨 quickOutline 那段）、`actions/__tests__/gotoLocationActions.test.ts`。
- **教训**：goto/peek 这种「右键能用、F12 能跳，但命令面板搜不到」的命令，必是 action2 型——别试 `getAction().run()`（恒为 null），直接走 focus + trigger。

### 案例 2：Find / Replace / Find Next/Prev（EditorAction 型）
- **机制**：`registerEditorAction`，`editor.getAction('actions.find')` 等非 null。
- **怎么接**：这些命令本已被 `bridgeAllMonacoActions` 自动桥接进命令面板/快捷键编辑器（路径 0）。项目额外给它们配了**项目级显式默认键**（ctrl+f / ctrl+h / f3 / shift+f3）所以走**路径 1**：Action2 包装 + `getAction(id)?.run()`。
- **锚点**：`apps/editor/src/renderer/actions/searchActions.ts`（`runActiveMonacoAction` + `FindInFileAction` 等）。

### 案例 3：排序选中行（内核有实现、无键、也不进右键菜单）
- **命令**：`editor.action.sortLinesAscending` / `sortLinesDescending`（内核 `linesOperations.js`；VSCode 同样只给命令、不给键）。
- **机制**：`registerEditorAction` → 路径 0 **已自动镜像**（命令面板里叫「按升序排列行」，Monaco NLS patch 提供中文名），`precondition: writable` 使只读文件里静默 no-op。**缺口只有键和菜单**。
- **怎么接**：走**路径 3**——新 `monacoExtraKeybindings.ts` 表（f9 / shift+f9，`when` = `editorTextFocus && !isInMergeEditor && !editorReadonly`）；`monacoActionsBridge` 第 4 参由「compat 表」升格为**表列表** `[MONACO_COMPAT_KEYBINDINGS, MONACO_EXTRA_KEYBINDINGS]`，共用 `registerMonacoCommandKeybindings`（`monacoCommandKeybindings.ts`，权重 `WorkbenchContrib` 必须 > `MonacoDefault`，命令不存在则跳过）。右键菜单两项加在 `EditorContextMenuContribution.ts`，`when: 'editorHasSelection && !editorReadonly'`（走 per-group scoped ctx）。**不新增命令、不自研排序**。
- **内核语义**（照抄，别自创）：按**整行**排；只选中一行内一段 → 静默 no-op；已有序 → no-op 且不产生 undo 条目（**e2e 必须从已知乱序体断言具体排列**，否则「没反应」也能蒙混过关）；多光标各自排序、全有或全无；**单光标无选区时排整篇**（键/菜单行为不对称，文档写明）。
- **锚点**：`workbench/editor/monaco/monacoExtraKeybindings.ts`、`monacoCommandKeybindings.ts`、`monacoActionsBridge.ts`（表列表参数）、`contributions/EditorContextMenuContribution.ts`、`e2e/specs/smoke.editorTextShortcuts.spec.ts`（真按键重排缓冲区）。
- **教训**：给「内核已有实现」的功能加一键，**先确认它是不是已经被镜像**——是的话只补键；一旦包装成 Action2，就凭空多出一个同 id handler 和一条重复的命令面板条目。

## 易踩坑速记
1. **`editor.getAction(id)` 对 action2 恒返回 null**——goto/peek 用它必失败，改用 `editor.trigger(source, id, {})`。
2. **action2 触发前必须 `editor.focus()`**——否则从命令面板（编辑器已失焦）触发时解析不到目标编辑器，静默不执行。
3. **双触发**：给 action2 配了项目默认键，务必在 `MonacoLoader` 用 `addKeybindingRule({keybinding:0, command:'-<id>'})` 拆掉 Monaco 自身默认键；用导出的 id 列表做两端单一事实源。
4. **EditorAction 多半已自动桥接**——别重复包装；只有要项目级显式默认键/自定义标题时才包装（路径 1）。
5. **id / 默认键对齐 VSCode**（apps/editor/CLAUDE.md 末条）。项目与 Monaco 是不同 CommandsRegistry 实例，同名 id 不冲突。
6. **Monaco 是 dynamic import**——单测里 mock `FileEditorRegistry`，用 `_resetForTests()` 清状态，别真加载 worker。
7. `precondition` 字符串里的 ContextKey 必须已在 `ContextKeyContribution` seed，否则表达式恒 false。
8. 存疑命令属哪套时，按 action2 处理（trigger 对两类都安全；getAction().run() 只对 EditorAction 有效）。

## 关键参考路径
- `apps/editor/src/renderer/actions/gotoLocationActions.ts` —— **action2 型**表驱动 Action2 模板（focus + trigger）
- `apps/editor/src/renderer/actions/searchActions.ts` —— **EditorAction 型** Action2 模板（getAction().run()）
- `apps/editor/src/renderer/workbench/editor/monaco/monacoActionsBridge.ts` —— EditorAction + core 命令的**自动桥接**（路径 0）+ 默认键侧表
- `apps/editor/src/renderer/workbench/editor/monaco/monacoExtraKeybindings.ts` / `monacoCommandKeybindings.ts` —— **路径 3**：给内核无键的命令补项目默认键（数据表 + 注册机制）
- `apps/editor/src/renderer/workbench/editor/monaco/monacoCompatKeybindings.ts` —— 「原生键被占用后补备选键」的表（同一注册机制，不同理由）
- `apps/editor/src/renderer/workbench/editor/monaco/MonacoLoader.ts` —— Monaco 加载、拆默认键（`addKeybindingRule`）、触发 `bridgeAllMonacoActions`
- `apps/editor/src/renderer/actions/index.ts` —— Action2 注册入口（按业务域分组）
- `apps/editor/src/renderer/actions/__tests__/gotoLocationActions.test.ts` —— 测试范式
- `apps/editor/src/renderer/services/editor/FileEditorRegistry.ts` / `FileEditorInput.ts` —— URI→editor 实例解析
- `apps/editor/CLAUDE.md` —— 套路 A（加 Action2）、套路 H（语言特性 provider 一键点亮 Outline + F12 跳转）、末条（对齐 VSCode id/键）

## 其它
- 后续用 skill，发现新经验，可自动更新本文件
