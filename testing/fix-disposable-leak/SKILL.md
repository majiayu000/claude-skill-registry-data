---
name: fix-disposable-leak
description: 诊断并修复 Disposable 内存泄漏。当用户提到内存泄漏 / memory leak / 未释放的 Disposable / Disposable leak(s) detected，或贴出带 trackDisposable / lifecycle.ts / computeLeakingDisposables 的泄漏堆栈时使用。
---

# 修复 Disposable 内存泄漏

本仓库用基于父子链的 `DisposableTracker` 检测泄漏。修复套路高度一致：**找到泄漏对象的创建点 → 确认它没被挂到正确的父节点 → 用 `_register` / `DisposableStore.add` / React cleanup 把它挂上 → 加回归测试 → 验证**。具体是哪个类、哪条业务路径泄漏，由你读代码当场判断。

## 检测机制（必须先理解，否则会误判）

源码：`packages/platform/src/base/lifecycle.ts`。

- **`Disposable` 基类构造时会创建一个内部 `_store: DisposableStore`**，并把 `_store` 设为自身的子节点。所以**一个泄漏的 Disposable 通常会报成两条**：一条是 `new DisposableStore`（在 `new Disposable` 里），一条是 `new Disposable` 本身，且两者 `idx` 连续。看到连续 idx 的这对，按**同一个对象**处理。
- **判定“未泄漏”的唯一条件**：该对象已被 `dispose()`，**或**它的根祖先被 `markAsSingleton` 标记。
- **父子链只由 `DisposableStore.add(o)` / `this._register(o)` 建立**（内部调 `setParentOfDisposable`）。⚠️ **闭包里引用一个 disposable 不会建立父链** —— 仅仅 `() => foo.dispose()` 持有引用，`foo` 的根仍是它自己，照样会被上报。要消除泄漏，**必须真正 `_register` / `add`**。
- 渲染进程 tracker 在 **DEV / E2E** 安装：`apps/editor/src/renderer/main.tsx`。所有根服务挂在单例 `workbenchStore = markAsSingleton(new DisposableStore())` 下，因此根服务即使不显式 dispose 也不会被报。
- 报告时机：`beforeunload` 里**先 `reactRoot.unmount()` 再 `computeLeakingDisposables()`**（main.tsx 的 `snapshotLeaks`）。意味着 React `useEffect` 的 cleanup 已经跑过——**正常关窗路径下 React 订阅不会是元凶**；元凶是没挂上父链、或挂错地方的对象。
- ⚠️ **但 reload 路径（Ctrl+Alt+R / `ReloadWindowAction`）历史上有第二条检测点**：它曾在弹"检测到 N 个泄漏"确认框前直接 `tracker.computeLeakingDisposables()`，**此时 React 还挂载着**，于是把所有活跃的 useEffect 订阅（OutlineView/AiStatusBarItem 的 `onDidChangeXxx` 等）全误报成泄漏。报告头 `[renderer:reload]`（来自 `printLeaks` 的 `source`）就是这条路径的指纹。**判据**：若同一批泄漏里 React useEffect 订阅扎堆、且报告来自 reload，先怀疑"检测时机错"（没先 unmount），而非订阅本身漏了——这类是假阳性。已修复为"reload 只 `markUnloadReason`，检测交给 beforeunload"。
- 主进程也有 tracker（`apps/editor/src/main/index.ts`，`process.on('exit')` 时报告）。

## 排查流程

### 1. 解析泄漏报告
- 每条泄漏有 `idx`（创建序号）和创建堆栈。**自底向上读堆栈**：最靠近业务的那一帧（`new XxxService` / `new XxxSession` / `someService.onDidChangeXxx`）就是拥有者/创建点。
- 连续 idx + 同一构造点 = 同一对象的 Disposable/`_store` 对，合并看。
- idx 相差很大 = 不同事件、可能是**互相独立**的泄漏，分别处理，不要强行归因到一起。
- **核对路径与版本**：堆栈里的绝对路径必须对得上当前工作目录。本仓库常有并行 checkout（如 `universe-editor` vs `universe-editorN`）；**路径** 指向哪份就改哪份。
  - ⚠️ **行号陷阱**：dev 下 vite 会把 `.ts/.tsx` transform（剥离 `interface`/`type`/JSDoc）后再发给浏览器，所以栈里 `lifecycle.ts:42` 这种行号**通常比源文件（如 164）小一截，这是正常的，不代表旧代码**。不要因为"行号对不上源文件"就断定报告陈旧——先看**路径**对不对。只有路径都指向另一份 checkout 时才是版本问题。
- 堆栈被截断（结尾像 `(h`）无法定位时，**找用户要完整堆栈**，不要瞎猜。

### 2. 定位创建点（用 Explore / Grep 并行扫）
- 用堆栈帧里的类名/事件名，Grep 出**该构造函数或该事件的所有调用点**。
- **横向对比**：同一类对象往往有多条创建路径，其中一条正确 `_register` 了、另一条漏了——漏的那条就是 bug。（本次案例：`resumeSession()` 调了 `this._register(session)`，`createSession()` 漏了。）
- 确认拥有者本身是否挂在单例/被释放的父链上；如果拥有者没事，问题就在“拥有者→泄漏对象”这一环没建链。

### 3. 应用最小且一致的修复
按泄漏对象类型选手段：
- **某个 `Disposable` 子类实例**（service / view-model / session）→ 在其拥有者里 `this._register(theInstance)`，**对齐同文件里已正确的兄弟路径**。
- **事件订阅**（`xxx.onDidChangeYyy(listener)` 返回的 disposable）→ 用 `this._register(...)` 包住；若在 React 里则 `useEffect` 返回 `() => d.dispose()`。
- **`toDisposable(fn)` / 定时器 / 监听器** → 同样 `_register` / `add`。
- ⚠️ 再次强调：**别用闭包“假装”释放**。必须真正进父链或显式 `dispose()`。
- 本仓库处于开发期、无需向后兼容；优先“最小、与既有范式一致”的改法。若发现累积型隐患（如 close 后仍被 `_store` 持有直到服务销毁），可指出但默认不顺手大重构，除非用户要。

### 4. 加回归测试
测试位于 `src/**/__tests__/*.test.ts(x)`。两种写法：
- **直接断言级联释放**（推荐，确定性强）：构造拥有者 → 触发创建 → `owner.dispose()` → 断言子资源被释放（如底层连接 `disposed === true` / 状态变 `closed`）。本次即给 fake 连接加 `disposed` 标记，断言 `svc.dispose()` 后 `conn.disposed === true`。
- **用泄漏断言助手**：`packages/platform/src/__tests__/_helpers/leakAssert.ts` 的 `withLeakCheck(fn)` 或 `useLeakCheck()`，包住“创建→dispose”，自动断言无泄漏。注意它用全局 tracker，测试里 new 出来但没被拥有者接管的桩对象（history/storage 等）自身也会被算泄漏，必要时在用例内一并 dispose 或换用“级联释放”写法。
- 写完**先验证测试能抓住 bug**：移除修复行应当让新测试失败。

### 5. 验证
```bash
# 跑改动涉及的测试文件（按需替换路径）
pnpm --filter @universe-editor/editor exec vitest run --project renderer <test-file>
# 或平台包：pnpm --filter @universe-editor/platform test

pnpm --filter @universe-editor/editor typecheck
pnpm --filter @universe-editor/editor lint
# 提交前可跑全量：pnpm check
```
手动验证：`pnpm --filter @universe-editor/editor dev` 复现操作 → 关窗/Restart Editor → 看 dev console 不再打印对应 `Disposable leak(s) detected`。E2E 冒烟见 `apps/editor/e2e/specs/smoke.disposableLeak.spec.ts`。

## 关键参考路径
- `packages/platform/src/base/lifecycle.ts` —— `DisposableTracker` / `computeLeakingDisposables` / `Disposable` / `DisposableStore` / `toDisposable` / `markAsSingleton` / `setDisposableTracker`
- `apps/editor/src/renderer/main.tsx` —— tracker 安装（DEV/E2E）、`workbenchStore` 单例根、`beforeunload` 报告
- `apps/editor/src/main/index.ts` —— 主进程 tracker
- `packages/platform/src/__tests__/_helpers/leakAssert.ts` —— `withLeakCheck` / `useLeakCheck`
- `apps/editor/e2e/specs/smoke.disposableLeak.spec.ts` —— E2E 泄漏冒烟

## 易踩坑速记
1. 一个泄漏报两条（对象 + 其 `_store`），idx 连续，别当成两个 bug。
2. 闭包引用 ≠ 建立父链，消不掉泄漏。
3. React 订阅在**正常关窗**路径下不是元凶（报告前已 unmount）；但 **reload（`[renderer:reload]`）路径**可能在 unmount 前检测，把活跃订阅全误报——这类是假阳性，修检测时机而非订阅。
4. 根服务在单例下不被报——所以“没被报”不代表“被释放”。
5. 只用**路径**判断改哪份 checkout；dev 栈的**行号是 transform 后的**（比源文件小），不能据此判定报告陈旧。
6. 横向对比同类创建路径，漏 `_register` 的那条就是 bug。
7. 用 tracker 写回归测试时，`computeLeakingDisposables()` 无泄漏返回 **`undefined`（非 `null`）**；contribution 回退 `new NullLogger()` 等桩对象自身会被算泄漏，给个返回 `markAsSingleton` logger 的 loggerService 桩绕开。
8. **在飞请求的传输订阅（reload 时点）**：像 `AiModelClientService.sendRequest` 这类"每次调用创建一组事件订阅、只在流结束（`acceptEnd`）时 dispose"的代码，reload 时若请求仍在飞，订阅未挂父链必被报。修法：把 combined 挂到 owner 的 `_store`（根到单例即豁免），并让结束回调走 `this._store.delete(combined)`（移除+dispose，避免 store 累积已 dispose 对象）——例如 `reassembler.bindSubscriptions(toDisposable(() => this._store.delete(combined)))`。
9. **延迟释放挂在宏任务上（e2e 泄漏门禁时点）**：`expectNoLeaks` 是**同步快照**，`setTimeout(() => store.dispose(), 0)` 排的宏任务在快照时还没跑，整个 store 连同其成员被判泄漏——本地 dev 手动关窗看不到（人手速 >> 0ms），e2e 里约 50% 概率红。案例：`preferencesActions.ts` 的 `pickTheme` / `SelectColorThemeAction`，`pick.onDidHide` 里用 `setTimeout(…, 0)` 推迟「未 accept 则回滚主题 + dispose」，被 `smoke.iconThemes.spec.ts` 抓成 5 条泄漏。修法：需要「让同回合的 accept 先赢」时用 `queueMicrotask` 而非 `setTimeout`——微任务仍在当前回合内排空，既保住让位语义又不跨越快照点。判据：**任何 disposable 的释放若排在宏任务/定时器上，都必须假设门禁会在它之前快照**。
10. **释放时机只绑在异步事件上（主进程退出时点）**：主进程 tracker 在 `process.on('exit')` 报告，而子进程 `'exit'` 事件、流 `'close'`、**在飞 `fetch` 的 `finally`**（微任务，晚于 will-quit 的同步 dispose）在退出流程中**来不及跑**——只靠这类时机释放的 disposable 退出时必被报。修法：在同步可达的路径上补摘除（如 transport 的 `kill()` 里同步 dispose，`toDisposable` 幂等，事件回调里的再 dispose 兜底）。案例：`watcherUtilityTransport.ts`；AI 远端源 `remote/httpJson.ts` 的 `fetchJson`——同域已有正解 `providers/retry.ts` 的 `toAbortSignal(token, store)`（取消回调里**自己 `store.dispose()`**，与 cancel 同一 tick），新写的 fetch 路径漏用即复发，横向对比就能发现。

## 其它
- 后续用本 skill，发现新经验，需同步更新本文件
