---
name: analyze-interaction-performance
description: 诊断交互卡顿/响应性问题——打字慢、quick open 卡、切 tab 掉帧、大文件滚动卡、某文件夹里操作明显慢。当任务需要采集交互性能报告（Event Timing + LoAF 归因）、在指定真实工作区文件夹上复现卡顿、或区分 JS 瓶颈 vs 渲染管线/环境噪音时使用。
disable-model-invocation: true
---

# 分析交互性能（响应性卡顿）

本仓库有一套常驻的运行时响应性监控：`IInteractionPerfService`（`apps/editor/src/renderer/services/performance/InteractionPerfService.ts`）用 **Event Timing + LoAF 双 observer** 采集所有 ≥16ms 的交互，慢交互（≥ `performance.responsiveness.warnThresholdMs`，默认 **200ms**，即 INP good 线）带完整归因。两个 @perf e2e spec 把「典型编辑手势巡演」跑一遍并产出 JSON + Markdown 报告，直接喂给 agent 定位卡顿。

> ⚠️ 第一原则：**先采集、再定性（JS 瓶颈 vs 渲染管线 vs 环境噪音）、最后才改代码**。交互计时在自动化窗口下系统性失真（见「读报告心智」），对着 present 数字优化产品代码是本流程最常见错误。

## 采集机制（必须先理解，否则会读错报告）

- **Event Timing observer**：每个交互（keydown/pointerdown/input…）记录三段分解——`inputDelayMs`（事件排队等主线程）/ `processingMs`（事件处理 JS）/ `presentationDelayMs`（处理完到像素呈现）。**只有 processing 是产品代码可直接优化的部分**。
- **LoAF（long-animation-frame）observer**：长帧归因，`blockingDuration` 是主线程 JS 时间，`scripts[]` 给出函数级归因（invoker + sourceUrl + 函数名）。渲染线程/合成器耗时**不进** scripts。
- **`recordPerfPhase(name, fn)`**（`services/performance/perfPhases.ts`）：给热路径包相位归因，自动进报告（如 `fileEditor.setModel`）。新优化点的标准动作是先包相位再测。
- **阈值语义**：spec 是 observe-only 不设预算断言；「达标」= 慢交互数 0 @ 默认 200ms。降阈值采集（如 50ms）是**放大归因**的手段，不是目标。
- **slowest 上限 20 条**（`MAX_SLOWEST_ENTRIES`），按时长降序；**`e2e/test-results/` 每次运行被清空**——要对比就备份到目录外。
- 报告产物：慢交互按场景窗口归桶（同一 `performance.now()` 时间轴），含三段分解 + 相位 + LoAF + target/editor 上下文。探针：`window.__E2E__.getInteractionPerfSummary()`。

## 采集流程

### 1. 基线（seeded 临时工作区，确定性 tour）

```bash
pnpm --filter @universe-editor/editor e2eg "drives an editing tour"
# 报告：apps/editor/e2e/test-results/interaction-perf-report.{json,md}
```

固定内容的工作区（4 个小 ts + 5000 行 large.ts + notes.md），用于回归对比：同代码两次跑的 byType max 应稳定。

### 2. 真实文件夹采集（用户指定目录）

`smoke.interactionPerfCollect.spec.ts`（@perf）把同一套 tour 跑在**用户指定的真实文件夹**上（watcher/文件索引/搜索宽度都是真实负载）：

```bash
# Windows bash / POSIX 通用（pnpm script 内已 cross-env）
UNIVERSE_PERF_WORKSPACE='D:\path\to\folder' pnpm --filter @universe-editor/editor e2eg "drives the editing tour against a user-picked folder"
# 深采（放大归因，top-20 慢交互带完整相位/LoAF）：
UNIVERSE_PERF_WORKSPACE='D:\path\to\folder' UNIVERSE_PERF_THRESHOLD_MS=50 pnpm --filter @universe-editor/editor e2eg "drives the editing tour against a user-picked folder"
# 报告：apps/editor/e2e/test-results/interaction-perf-collect.{json,md}
```

- `UNIVERSE_PERF_WORKSPACE`（必填，未设则 skip）：绝对路径，作为位置参数启动（与 workspaceSeeder 同走 `openWindowForFolder`，扩展宿主保持单代）。
- `UNIVERSE_PERF_THRESHOLD_MS`（可选）：慢交互阈值覆盖（Memory target 运行时生效，不写用户配置）。
- **真实文件夹保护**：写操作（打字/撤销/保存）只落在工作区根目录的两个探针文件 `.universe-perf-probe{,-large}.ts`（spec 自创建、finally 删除）；真实文件只读（quick open 打开 / 搜索）。搜索用探针文件里的独特 token（`perfProbeFn1`）保证结果集确定；想测真实搜索负载就改 spec 里的 token。
- 与 seeded 版的已知差异：真实文件夹可能有**仅大小写不同的同名文件**，quick open（大小写不敏感匹配）打开的那个未必是断言的那个——断言一律大小写不敏感（spec 已处理，改 tour 时保持）。

### 3. JS 热点复核（CDP Profiler）

报告只给 LoAF 函数归因（常为 `<no script attribution>`），要确认 processing 的构成用 CDP Profiler：

```ts
const session = await page.context().newCDPSession(page)
await session.send('Profiler.enable')
await session.send('Profiler.setSamplingInterval', { interval: 100 })
await session.send('Profiler.start')
// …驱动可疑手势…
const { profile } = await session.send('Profiler.stop')   // 写盘后离线分析
```

分析：按 `samples`/`timeDeltas` 聚合 self time；对嫌疑交互找 `dispatchDiscreteEvent`（React 合成事件派发，含同步 render+commit）/ `performSyncWorkOnRoot` 的调用树 total time。产物 bundle 是压缩的，靠调用链上的语义函数名（`handleKey`/`onAccept`/`_open` 等）定位。

## 读报告心智（定性三分法）

| 信号 | 定性 | 动作 |
|---|---|---|
| `processingMs` 大（≥30ms），LoAF scripts 有业务函数归因 | **真 JS 瓶颈** | 优化该函数/渲染路径 |
| `present` 占大头（≥80%），`blocking≈0`，`<no script attribution>` | **渲染管线耗时**（style/layout/paint/合成，自动化非前台窗口下被系统性放大） | 默认不改产品代码；确认真实机器可复现才动 CSS/DOM 结构 |
| `inputDelayMs` 大，同帧 loaf blocking 也小 | **排队等前一帧渲染** | 同上，非 JS 问题 |

判别环境噪音的铁律：

1. **同代码连跑两次**。自动化窗口（非前台）的 present 延迟可差 2 倍；`pnpm build` 后紧接着跑会因缓存冷全面膨胀 present。**判定回归前必须系统空闲时复跑**。
2. processing 在慢环境下依然小 = 优化没退化，present 膨胀是环境。
3. `dispatchDiscreteEvent` 出现在 loaf scripts 里且 >30ms = React 同步渲染真耗时；其中的子树（render/commit/passive effects）无单一热点时，优先查**整树重复渲染**（memo 缺失、deferred 误用、context 广播）而非单函数。

## 已修案例（优化方向速查）

- **QuickPickPanel 双重渲染**（2026-08，commit `6d1a7729`）：`useDeferredValue(filterText)` 对 `filterExternally` picker（quick open / workspace symbol / 全局搜索）是纯浪费——deferred 值不进 `filtered` 计算，却每击键多调度一次整树 transition 渲染。修法 = `useDeferredValue(filtersLocally ? filterText : '')`（入参恒定即不调度）。效果：quick-open 首字符 processing 51ms→0，正式阈值下 keydown max 168→136ms。教训：**deferred/transition 类 API 的收益只在消费方真的用 deferred 值时存在**。
- **FileQuickAccessProvider 每击键全量扫描**（2026-08）：百万级文件工作区（清单封顶 10 万条）上，quick open 每击键在 `onDidChangeValue`（React onChange 派发内）同步对全清单跑 `scoreFileMatch` + 排序，input processing 108~145ms，LoAF 归因 `dispatchDiscreteEvent (BODY.oninput)`；对照小工作区仅 1~5ms（定性=随规模放大的真 JS 瓶颈）。修法 = 自适应：候选池 ≤5000 保持同步（小库零延迟、单测同步断言不破）；大池分块扫描（8ms 时间片 `yieldToMain` + 复用 `seq`/token 过期丢弃 + 行压实控住终排序），且每次**完整**扫描的命中集作为下一次「追加字符」击键的候选池（子序列匹配保证追加只会收缩命中集；新清单落地必须重置收窄池）。效果：50ms 阈值下 loaf 133→13、keydown p95 100→50ms、场景窗口内高 processing 条目清零。教训：**type-to-filter 面的同步扫描要按最大工作区设防——要么限池，要么切片让出**。
- 相位归因样板：`fileEditor.setModel`/`applyOptions`/`restoreViewState`/`registerAndFocus`（`workbench/editor/FileEditor.tsx`）、`dirtyDiff.compute`、`mergeConflict.scan`、`quickOpen.filterFiles`（`services/quickInput/providers/FileQuickAccessProvider.ts`）——热路径照此包 `recordPerfPhase`。

## 收尾验证（分级）

1. `pnpm check`（lint/typecheck/相关测试）
2. 交互逻辑改动：`pnpm --filter @universe-editor/editor e2e:smoke`（@p0 冒烟）
3. 正式 spec 复跑对比 max/slow（**机器空闲时**，连续两次取好的那次对齐基线）

## 参考文件

- `apps/editor/e2e/specs/smoke.interactionPerfReport.spec.ts` — seeded 基线 tour
- `apps/editor/e2e/specs/smoke.interactionPerfCollect.spec.ts` — 真实文件夹采集（env 驱动）
- `apps/editor/src/renderer/services/performance/InteractionPerfService.ts` — 采集层（阈值/slowest 上限/归因组装）
- `apps/editor/src/renderer/services/performance/perfPhases.ts` — `recordPerfPhase`
- `apps/editor/src/renderer/e2e/probe.ts` — `getInteractionPerfSummary` / `updateConfigValue` 探针
- `docs/development/testing.md` — @perf tag 分流与 CI 工件
