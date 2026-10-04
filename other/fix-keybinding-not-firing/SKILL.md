---
name: fix-keybinding-not-firing
description: 排查「快捷键不生效」：按键后命令没执行，或日志报 NO MATCH / no binding registered。当用户说快捷键按了没反应、keybindings.json 配的键不工作、改键仍触发旧的、when 子句满足却不执行时使用。区别于 register-monaco-command（那个是把命令接进来，本 skill 是键已配但不触发的诊断）。
---

# 排查快捷键不生效（NO MATCH / 按了没反应 / 改键无效）

本仓库的快捷键最终都汇入同一个 `KeybindingsRegistry`，运行期由 `useGlobalKeybindingHandler` 解析并执行。一个键「不生效」可能断在**注册期**（绑定根本没进 registry，或进了但被同 command 的另一条覆盖），也可能断在**运行期**（进了 registry 但被分发层的某道 guard 拦下）。核心套路：**开键盘调试日志读诊断行 → 用 `same-key` 判别是「没注册」还是「when/运行期问题」→ 沿决策树定位到具体一层 → 先写最小复现（优先单测，端到端守护再补 e2e）再修 → 验证不双触发/不覆盖**。

> ⚠️ 第一原则：**先用诊断行判别断在哪一层，别凭症状猜**。「没反应」可能是没注册、也可能 when 不满足、也可能被可编辑目标 guard 吃掉——三者修法完全不同，判错会改错地方。

## 第 0 步：开诊断、读那一行

命令面板 → `Developer: Toggle Keyboard Shortcuts Troubleshooting`（`workbench.action.toggleKeybindingsLog`，`actions/developerActions.ts`），会打开 Output 面板的键盘调试 channel。按下目标键，每次按键输出一条 `traceKeystroke`；**当结果是 `no-match` 时**额外打一行 `diag`（`useGlobalKeybindingHandler.ts:296-313`）：

```
diag: registry=<N> bindings | same-key(ignoring when)=<M> | monaco bridged=<bool>
    | cmds total=<..> editor.action.*=<..> hasCopyLinesDown=<bool>
    | vscode-keybindings: parsed=<P> registered=<R> path=<...>
```

逐字段含义：
- **`same-key(ignoring when)=M`** —— 忽略 when，registry 里有多少条候选键等于你按的键。**这是最关键的判别位**。
- **`monaco bridged`** —— `bridgeAllMonacoActions()` 是否已把 Monaco EditorAction 镜像进 `CommandsRegistry`（即编辑器是否已加载过）。
- **`cmds total / editor.action.* / hasCopyLinesDown`** —— 目标命令是否存在于项目 `CommandsRegistry`（`hasCopyLinesDown` 是 Monaco 懒注册的探针样本）。
- **`vscode-keybindings: parsed / registered`** —— 只读 VSCode 兼容层这次 reload 解析出几条、实际注册了几条（差值 = 被命令存在性过滤跳过的条数）。`path` 是该层指向的真实文件。

## 判别与决策树

### 分叉 0（先判这个）：主键那一下 keydown 在日志里**整行消失** —— 键根本没到达 document 监听器
按下 `no-match` 才会打 `diag` 行——前提是**键到达了 document 监听器**。`runResolution` 对任何到达的非修饰主键都必打一行 `traceKeystroke`（哪怕 `no-match`）。所以先数日志行：组合键按下应有「每个修饰键各一行 + 主键一行」。**若主键那一行压根没出现**（例：按 `ctrl+alt+up`，只看到 `Control`、`Alt` 两行 `modifier key alone`，`ArrowUp` 一行都没有），说明主键在到达 document 监听器前就被吞了——**不属于注册期/运行期任何一层，别去查 registry/when/guard**。这正是键盘调试工具自己声明的盲区（`keyboardDebugFormat.ts:88-92`：Monaco/浏览器/OS 在到达 app 前拦截）。
- **头号嫌疑：编辑器聚焦时被 Monaco 内部 dispatch 吃掉**。本应用 `editorFocus===true` 时 capture handler 直接 return、把优先权让给 Monaco（`useGlobalKeybindingHandler.ts:355-365`）；Monaco 若有该键的内置默认绑定，会在编辑器容器内执行并 `stopPropagation`，document 的 bubble 监听器永远收不到 → 主键整行消失。判别：**点到编辑器外**（如侧栏/资源管理器）再按同一个键；若此时主键出现在日志、编辑器内才消失，几乎可以坐实是 Monaco 吃的。`ctrl+alt+up = editor.action.insertCursorAbove` 是经典例子（与你想绑的 `editor.gotoPreviousFold` 冲突）。
- **次要嫌疑：OS/显卡驱动全局热键**。`Ctrl+Alt+方向键` 在 Windows 上还可能是 Intel/AMD 显卡的屏幕旋转热键，OS 层就吞掉；这种情况**编辑器内外都收不到**主键。用「编辑器外也消失」与上一条区分。
- **修法（Monaco 吃键）**：keybindings.json 里的 `-monacoCommand`（disable）现在会**真正同步去 Monaco 解绑**，原样配 VSCode 那两条即可——见 **案例 4**。
- **修法（OS 吃键）**：非产品 bug，关掉显卡驱动/系统的该全局热键，或改绑到未被 OS 占用的键位。

### 分叉 A：`same-key == 0` —— 绑定根本没进 registry
按的键在 registry 里一条候选都没有。往「为什么没注册」走：

1. **目标命令存在吗？**（看 `hasCopyLinesDown` / 自己确认 `CommandsRegistry.getCommand(id)`）
   - **命令不存在** → 多半是**懒注册命令 + VSCode 兼容层的命令存在性过滤**。只读 VSCode 层（`UserKeybindingsService._reloadVSCodeFile`，`UserKeybindingsService.ts:263-278`）在启动期就读完，遇到当时不存在的命令会 `if (!CommandsRegistry.getCommand) continue` 跳过：
     - **Monaco 命令**（`editor.action.*`）：只在 Monaco 加载、`bridgeAllMonacoActions()` 后才存在。需要「桥接完成后再 reload 一次」补上——见 **案例 2**（`MonacoKeybindingSyncContribution`）。诊断特征：`monaco bridged=false`（没开过编辑器）或 bridged 后仍 0（reload 触发缺失）。
     - **扩展贡献命令**：扩展宿主异步注册，`ExtensionsContribution` 在宿主起来后调 `reload()` 补上（`ExtensionsContribution.ts`）。
     - **命令 id 拼错 / 与 VSCode 不一致**：对标 VSCode 的功能 id 必须一致（apps/editor/CLAUDE.md 末条）。
   - **命令存在但键仍缺** → 看 `vscode-keybindings: parsed=P registered=R`：
     - **`R < P`** 且差的就是你这条 → 注册阶段把它丢了。**头号嫌疑：同一 command 多条 VSCode 条目互相覆盖**——见 **案例 1**（曾按 command id 去重，后一条 dispose 掉前一条）。
     - 也可能是 **key 字符串规范化不匹配**：`KeybindingsRegistry.normalizeKey`（`keybindingRegistry.ts`）把修饰键按**字母序**排序（alt < ctrl < meta < shift），`shift+alt+down` 实际存成 `alt+shift+down`。注册侧会规范化，但**探针/断言侧若原样比较**就会“查不到”——见 **案例 3**（这是测试假象，不是产品 bug，但同样表现为“同一个键查不到”）。

2. 应用自己的 `keybindings.json`（`_reloadFromFile`，`UserKeybindingsService.ts:288-303`）**没有**命令存在性过滤——所以同一条绑定放这里能生效、放 VSCode 兼容层不行，正是「VSCode 的 key settings 不工作」的典型分界。

### 分叉 B：`same-key > 0` 但仍 `no-match` —— when 子句没过
有候选键，但 when 表达式在当前上下文求值为 false。看 `traceKeystroke` 里每条候选的 when 求值：
- **ContextKey 没 seed / 值不对** → 表达式里的 key 必须已在 `ContextKeyContribution` seed，否则恒 false。
- **当前确实不该触发** → 如 `when: editorTextFocus` 要求焦点在编辑器内；日志里 `target=DIV editable=false` 说明编辑器没聚焦，属预期，先点进编辑器再验。
- **表达式写错** → `contextKeyParser.parse()` 对非法输入返回 `undefined`（**不抛异常**），该条绑定被静默忽略；核对表达式语法。

### 分叉 C：`result.kind === 'execute'` 但命令没跑 —— 运行期被 guard 拦
registry 解析出来了，但 `useGlobalKeybindingHandler` 的某道闸把它挡了（日志会打 `formatGuardStop` 说明原因）：
- **可编辑目标保留可打印键**：单字符键 + 无 ctrl/alt/meta + 焦点在 input/textarea/contentEditable → 让位文本输入（`isPrintableTyping`，`useGlobalKeybindingHandler.ts:321-333`）。
- **Quick Input 打开**：只放行 Escape，其余键归 Quick Input（`useGlobalKeybindingHandler.ts:213-247`）。
- **模态对话框内**：dialog 自己处理键，整体不拦截（`isInsideRendererDialog`）。
- **命令未注册兜底**：解析到 execute 但 `CommandsRegistry.getCommand(result.command)` 为空 → 静默 return（`useGlobalKeybindingHandler.ts:335-342`）。
- **editorFocus 决定 capture/bubble**：编辑器聚焦时走 bubble 且 `e.defaultPrevented` 的键已被 Monaco 吃掉（Monaco 先 `stopPropagation`）；编辑器未聚焦走 capture。若“编辑器内不触发、编辑器外触发”或反之，多半是这层焦点门——本应用故意把编辑器聚焦时的优先权让给 Monaco（`useGlobalKeybindingHandler.ts:353-365`）。
- **chord 未完成**：两段式（如 `ctrl+k ctrl+s`）第二段没在超时内按或不匹配 → chord 取消。

## 修复纪律：先复现再修

定位到分叉后，**先写最小复现测试，红了再改**（用户的标准要求：“先构造用例复现，再尝试解决”）。

- **单测优先**（确定性、快）：`UserKeybindingsService.test.ts` 用 `FakeUserData` 往 `UserDataFile.VSCodeKeybindings` 注入条目，`initialize()` / `reload()` 后断言 `KeybindingsRegistry.resolveKeystroke(key)` 等于 `{kind:'execute', command}`。注册期的 bug（分叉 A）几乎都能在这里确定性复现+判别。
- **e2e 端到端守护**（补，不替代单测）：`smoke.vscodeKeybindings.spec.ts` 用 `UNIVERSE_VSCODE_KEYBINDINGS_PATH` 把只读层指到 tmp 文件，开真编辑器、等扩展宿主与 monaco 桥接就绪，再用 `window.__E2E__.getKeybindingCommandsForKey(key)` 断言绑定落到 registry。**注意 e2e 跑 `out/` 产物**，且受启动期时序影响（monaco 桥接常抢先于 ext-reload），它守护“整条链跑通”，**不适合隔离单条修复路径**——隔离判别交给单测。
- **断言用规范化后的键**：e2e 探针 `getKeybindingCommandsForKey` 原样字符串比较，断言里写规范序（修饰键字母序，如 `alt+shift+down` 而非 `shift+alt+down`），否则会假阴性。
- 手动验证：开键盘调试日志，复刻用户场景（注意 when 要求的焦点），确认从 `NO MATCH` 变 `EXECUTE <command>`，且**不双触发**。

## 案例库

> 每条：症状/诊断特征 → 断在哪层 → 根因 → 修法 → 文件锚点。新经验往下追加。

### 案例 1：同一 command 配多条键，只有一条生效（注册期覆盖）
- **症状/诊断**：用户给 `editor.action.copyLinesDownAction` 同时配了 `ctrl+shift+d` 和 `shift+alt+down`，按下其中一个 `NO MATCH`；`same-key=0`、命令存在（`hasCopyLinesDown=true`）、`monaco bridged=true`、`vscode-keybindings registered < parsed`。
- **断在**：分叉 A——命令存在但键缺。
- **根因**：`_applyEntryToStore` 按 `entry.command` 在 disposables map 里去重，后一条同 command 的注册会 `dispose` 掉前一条 → 用户自定义键被“同命令的另一条绑定”悄悄顶掉。
- **修法**：VSCode 只读层**逐条注册不去重**——抽出 `_registerEntry`（纯注册，无 command 级去重），`_reloadVSCodeFile` 直接对每条调它（store 每次整体 clear，无泄漏）；`_applyEntryToStore` 仅给用户层保留“一命令一绑定”的去重。
- **锚点**：`apps/editor/src/renderer/services/keybindings/UserKeybindingsService.ts`（`_reloadVSCodeFile` / `_registerEntry` / `_applyEntryToStore`）、其单测 `keeps every VSCode binding when one command has multiple entries`、`e2e/specs/smoke.vscodeKeybindings.spec.ts` 的多条目守护用例。

### 案例 2：VSCode 层绑定到「懒注册 Monaco 命令」永远缺失（注册期时序）
- **症状/诊断**：VSCode keybindings.json 里 `ctrl+shift+d → editor.action.copyLinesDownAction` 完全不触发；`same-key=0`，且命令在启动期不存在（开编辑器前 `monaco bridged=false`）。
- **断在**：分叉 A——命令不存在（懒注册）+ VSCode 层命令存在性过滤。
- **根因**：只读 VSCode 层启动期就读完并过滤掉当时不存在的命令；Monaco EditorAction 要到首个编辑器打开、`bridgeAllMonacoActions()` 才进 `CommandsRegistry`，而**没有任何东西触发桥接后重新注册** → 永久缺失。对照扩展命令有 `ExtensionsContribution` 的 reload，Monaco 侧原本缺这个等价触发。
- **修法**：`MonacoLoader` 暴露 `actionsBridged` 标志 + `onDidBridgeActions` 事件（桥接 promise resolve 后 fire）；新增 `MonacoKeybindingSyncContribution`（`WorkbenchPhase.AfterRestore`），桥接完成后调 `userKeybindings.reload()`；`reload()` 用 `_reloadChain` promise 串行化，防它与 `ExtensionsContribution` 并发交错 clear/register。
- **锚点**：`workbench/editor/monaco/MonacoLoader.ts`（`actionsBridged` / `onDidBridgeActions`）、`contributions/MonacoKeybindingSyncContribution.ts`、`contributions/index.ts`（注册）、`UserKeybindingsService.ts`（`reload` 串行化）、参考范式 `contributions/ExtensionsContribution.ts`。

### 案例 3：键“查不到”其实是修饰键顺序（测试假象，非产品 bug）
- **症状**：单测/e2e 里写 `shift+alt+down` 断言查不到，但产品里该键正常工作。
- **根因**：`KeybindingsRegistry.normalizeKey` 把修饰键按字母序排序存储（alt < ctrl < meta < shift），`shift+alt+down` 规范化成 `alt+shift+down`；原样比较的探针/断言匹配不上。
- **修法**：断言写规范序键。记住规范形是字母序，不是“ctrl→alt→shift→meta”的直觉序。
- **锚点**：`packages/platform/src/command/keybindingRegistry.ts`（`normalizeKey`）、`e2e/specs/smoke.vscodeKeybindings.spec.ts` 的 `SECOND_KEY` 注释。

### 案例 4：`ctrl+alt+up` 没反应，主键 keydown 整行不出现（Monaco 内置默认键在编辑器内吃掉 + `-command` 同步解绑）
- **症状/诊断**：用户给 `editor.gotoPreviousFold` 配 `ctrl+alt+up`，并配 `-editor.action.insertCursorAbove` 想腾出键，按下没反应。键盘调试日志**只有两行**——`Control` 与 `Alt` 的 `modifier key alone (no stroke)`，**`ArrowUp` 那一下 keydown 一行都没有**（连 `traceKeystroke`/`diag` 都没打）。
- **断在**：分叉 0——主键没到达 document 监听器。注意：**一开始极易误判为 OS/显卡热键**；实测「点到编辑器外按同键，主键正常出现；编辑器内才消失」→ 坐实是 Monaco 吃的，不是 OS。
- **根因**：Monaco 内部默认 `ctrl+alt+up = editor.action.insertCursorAbove`。编辑器聚焦时 capture handler 让位 Monaco（`useGlobalKeybindingHandler.ts:355-365`），Monaco 在编辑器容器内执行该 action 并 `stopPropagation` → document bubble 监听器收不到。**而 keybindings.json 的 `-insertCursorAbove`（disable）原本只作用于项目 `KeybindingsRegistry`**，触达不到 Monaco 内部 dispatch——Monaco 默认键不在该 registry（`monacoActionsBridge` 只存进 side-table，故意把默认键留给 Monaco 自己 dispatch，见该文件头注释），所以那条 `-` 去 negate 时 `toNegate.length===0`，什么也没做，键照样被吃。
- **修法（方案 B，已落地）**：让 `-monacoCommand` 真正同步去 Monaco 解绑。
  1. `UserKeybindingsService` 暴露 `disabledCommands`（合并 VSCode 层 + user 层所有 `key===null` 的 command，去重；在 `_reloadVSCodeFile` 收集 VSCode 层，user 层从 `_userEntries` 派生）。
  2. 新增 `MonacoDefaultKeybindingOverrideContribution`（`AfterRestore`）：对 `disabledCommands` 中 `getMonacoDefaultKeybinding(id)!==undefined` 的命令，调 `monaco.editor.addKeybindingRule({keybinding:0, command:'-${id}'})`（与 `MonacoLoader` drop `quickOutline`、导航命令同一机制）在 Monaco 侧解绑，持有返回的 `IDisposable`；用 diff 处理增删（撤销 disable → `dispose()` 还原 Monaco 默认键）。触发：`MonacoLoader.actionsBridged`/`onDidBridgeActions`（不 force-load，`peek()` 取 monaco，未加载则跳过——此时 Monaco dispatch 不存在不吃键）+ `userKeybindings.onDidChange`（热改 keybindings.json）。diff 抽纯函数 `diffMonacoDisabled` 单测。
  3. 用户侧 keybindings.json 原样两条即生效：`{key:'ctrl+alt+up', command:'editor.gotoPreviousFold'}` + `{key:'ctrl+alt+up', command:'-editor.action.insertCursorAbove', when:'editorTextFocus'}`。
- **验证**：编辑器聚焦按 `ctrl+alt+up`，从「ArrowUp 整行消失」变 `EXECUTE editor.gotoPreviousFold` 且不再插入上方光标。
- **锚点**：`UserKeybindingsService.ts`（`disabledCommands` / `_reloadVSCodeFile` 收集）、`contributions/MonacoDefaultKeybindingOverrideContribution.ts`（`diffMonacoDisabled` + `_sync`）、`contributions/index.ts`（`workbench.contrib.monacoDefaultKeybindingOverride`，AfterRestore）、`workbench/editor/monaco/MonacoLoader.ts:205-212`（`addKeybindingRule` 范式）、`monacoActionsBridge.ts`（头注释解释为何默认键不进 registry、`getMonacoDefaultKeybinding`）。

### 案例 5：Action2 的 `keybinding.primary` 写 VSCode 风格空格 chord 字符串静默失效（注册期解析缺失）
- **症状/诊断**：`SelectColorThemeAction` 声明 `keybinding: { primary: 'ctrl+k ctrl+t' }`，按 `ctrl+k ctrl+t` 不弹主题选择框；`same-key(ignoring when)=0`（`ctrl+k` 一条候选都没有），但命令存在、f1 也能从命令面板搜到。
- **断在**：分叉 A——绑定“注册了但永远匹配不上”。
- **根因**：`registerAction2` 对字符串 `primary` 原样当**单键**注册（`{ key: 'ctrl+k ctrl+t' }`），registry 规范化后存成一条 chords 长度为 1、键值为 `'ctrl+k ctrl+t'` 的记录；运行期每次按键产生的规范化键（`'ctrl+k'`、`'ctrl+t'`）永远不等于它 → chord 状态机永远进不去。而仓库里其它层（`UserKeybindingsService`、`ExtensionPointTranslator`、`monacoKeybindingDecoder`）都会 `trim().split(/\s+/)` 把空格分隔字符串拆成两段 chord——**只有 Action2 这层不拆**，静默失败不报错。全仓库其它 chord 都写元组形式 `['ctrl+k','ctrl+t']`，唯独这一处照 VSCode 习惯写了单字符串。
- **修法（已落地）**：`registerAction2` 内新增 `toKeyOrChords`——字符串 `primary` 先 `trim().split(/\s+/)`，两段则注册为 `chords` 元组，否则按单键（与 `UserKeybindingsService.keyToKeybindingItem` 行为一致）。`IAction2Keybinding.primary` docstring 补上空格 chord 为合法输入。
- **验证**：`action.test.ts` 新增用例（字符串 chord → `resolveKeystroke('ctrl+k')` 返回 `enter-chord` → 第二段返回 `execute`）；e2e `smoke.themes.spec.ts` 新增「ctrl+k ctrl+t chord opens the theme picker」真键盘整链守护。注意 Playwright `--grep` 是正则，标题含 `+` 需转义或换不含 `+` 的 grep 词，否则报 `No tests found`。
- **锚点**：`packages/platform/src/command/action.ts`（`toKeyOrChords`）、`packages/platform/src/__tests__/command/action.test.ts`（SpaceChordAction 用例）、`apps/editor/src/renderer/actions/preferencesActions.ts`（`SelectColorThemeAction`，事发点）、对照已支持的各层：`UserKeybindingsService.ts:100`、`ExtensionPointTranslator.ts:293`、`monacoKeybindingDecoder.ts:249`。

## 易踩坑速记
0. **先数日志行**：组合键应有「每修饰键一行 + 主键一行」。**主键那一行整个消失** = 键没到达 document 监听器（分叉 0、案例 4）。**头号嫌疑是编辑器聚焦时 Monaco 内置默认键 `stopPropagation`**（用「点到编辑器外按同键是否出现」区分；OS/显卡热键则编辑器内外都消失）。Monaco 吃键现在可用 keybindings.json 的 `-monacoCommand` 同步解绑（案例 4）。
1. **`no-match` 先看 `same-key`**（前提：主键已到达、有 `traceKeystroke`）：`0` = 没注册（分叉 A）；`>0` = when/运行期问题（分叉 B/C）。别一上来就改 when。
2. **只有 VSCode 兼容层有命令存在性过滤**，应用自己的 keybindings.json 没有——“VSCode 配的不灵、放本应用配置灵”就是这条分界。
3. **Monaco 命令是懒注册**，启动期不存在；缺“桥接后 reload”就永久丢绑定（案例 2）。
4. **同 command 多条键别按 command 去重**（案例 1）；用户层一命令一绑定、VSCode 层逐条注册，两套语义不同。
5. **Action2 的 chord 两种写法都合法**：元组 `['ctrl+k','ctrl+t']` 或 VSCode 风格空格字符串 `'ctrl+k ctrl+t'`（`toKeyOrChords` 拆分，案例 5）；但**直接调 `KeybindingsRegistry.registerKeybinding` 时 `key` 只认单键**，chord 必须用 `chords` 元组——绕过 Action2 的底层调用没有空格拆分。
5. **修饰键规范化是字母序**（alt/ctrl/meta/shift），断言/探针比较要用规范形（案例 3）。
6. **`contextKeyParser.parse()` 不抛异常**，非法 when 返回 `undefined` 被静默忽略——表达式写错不会报错，只会“这条不生效”。
7. **运行期 guard 会吞键**：可编辑目标保留可打印键、Quick Input 只放 Escape、dialog 自管、editorFocus 切 capture/bubble 把优先权让给 Monaco——`formatGuardStop` 会写明原因。
8. **先复现再修**：注册期 bug 用 `UserKeybindingsService` 单测确定性复现；e2e 是整链守护、不隔离单条路径；e2e 跑 `out/` 产物。

## 关键参考路径
- `apps/editor/src/renderer/services/keybindings/UserKeybindingsService.ts` —— 三层汇入点：`_reloadVSCodeFile`（VSCode 只读层，有命令过滤、逐条注册）/ `_reloadFromFile`（应用层，无过滤）/ `_registerEntry` / `reload` 串行化 / `diagnostics`
- `apps/editor/src/renderer/workbench/useGlobalKeybindingHandler.ts` —— 运行期分发 + 全部 guard + `no-match` 时的 `diag` 行（分叉 C 全在这）
- `apps/editor/src/renderer/services/keybinding/keyboardDebugService.ts` / `keyboardDebugFormat.ts` —— 键盘调试日志（`traceKeystroke` / `formatGuardStop` / `formatKeystrokeTrace`）
- `apps/editor/src/renderer/actions/developerActions.ts` —— `Developer: Toggle Keyboard Shortcuts Troubleshooting`（开诊断）
- `packages/platform/src/command/keybindingRegistry.ts` —— `KeybindingsRegistry`：`normalizeKey`（字母序）/ `resolveKeystroke` / `traceKeystroke` / `registerKeybinding`
- `packages/platform/src/command/contextKeyParser.ts` —— when 表达式解析（非法返回 `undefined` 不抛）
- `apps/editor/src/renderer/contributions/MonacoKeybindingSyncContribution.ts` + `ExtensionsContribution.ts` —— 懒注册命令的“桥接/宿主就绪后 reload”范式
- `apps/editor/src/renderer/contributions/MonacoDefaultKeybindingOverrideContribution.ts` —— `-monacoCommand` 同步去 Monaco 解绑内置默认键（案例 4，分叉 0 的 Monaco 吃键修法）
- `apps/editor/src/renderer/workbench/editor/monaco/MonacoLoader.ts` / `monacoActionsBridge.ts` —— Monaco 桥接、`actionsBridged` / `onDidBridgeActions`、默认键侧表
- `apps/editor/src/renderer/services/keybindings/__tests__/UserKeybindingsService.test.ts` —— 注册期复现/判别单测范式
- `apps/editor/e2e/specs/smoke.vscodeKeybindings.spec.ts` —— 端到端守护范式（`UNIVERSE_VSCODE_KEYBINDINGS_PATH` + `getKeybindingCommandsForKey`）
- 姊妹 skill `register-monaco-command` —— 当结论是“命令压根没接进来”（命令面板都搜不到）时转去那个

## 其它
- 后续用本 skill，发现新经验，需同步更新本文件
