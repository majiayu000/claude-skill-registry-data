---
name: diagnose-renderer-oom
description: 诊断 renderer OOM（内存耗尽崩溃）。当用户交来 renderer OOM 诊断包（zip 或 logs 目录）、报告编辑器窗口变黑/自动关闭、或提到 renderer OOM / Automatic resume is paused / oom-lo-space-size / 切 tab 后内存冲到数 GB 时使用。
---

# 诊断 renderer OOM（内存耗尽崩溃）

renderer OOM 是「堆在被压垮之前没有观测」的那类事故：renderer 自己来不及上报，所以证据全在 **main 侧落盘的文件**里。诊断包由命令 `workbench.action.exportDiagnostics` 导出（组成见 `docs/development/error-diagnostics.md`）。核心套路：**先用三件套判定「这是不是 OOM、哪一类增长」，再按族去查元凶，最后核对结论能否被计数器解释**。

> ⚠️ 第一原则：**诊断包里的三件套先读全，再谈元凶**。历史上三次 OOM（claude 回放、codex 回放、会话改动 tracker）在只看单份日志时都被误判过；三件套齐读能把「崩没崩、崩在哪、崩的时候还有谁在跑」一次锁死。机制/阈值/releaser 表的单一真相是 `docs/development/memory-pressure.md`，本 skill 只讲**读法**。

## 诊断三件套（先读这三份）

1. **`processMetrics.log` 的 renderer 内存曲线**。两条线分开读：main 每 30s（有进程超 2GB 时 10s）写 `pid=… type=Tab mem=…MB cpu=…%`（`app.getAppMetrics()` 的 OS 工作集，看不到 V8 堆膨胀）+ renderer 自报的 `renderer-heap window=… used=…MB limit=…MB usedPct=… level=… holders=…`（`apps/editor/src/renderer/services/memory/rendererHeapReporter.ts`）。判据优先于数值：`used` 涨而 `holders` 不涨 = **元凶不在已知持有者里**（`unexplained=` 就是那个差值）；`level=critical` 在线上方停了多久 = releaser 是否有效。诊断包里 `memory.txt` 另存曲线尾部 32 条——日志尾部有 512KiB 截断，会恰好丢掉慢速爬升最早的那几条。
2. **`acpSessionRestore.log` 的 `skipping auto-restore of session <id>: recent OOM crash in this window`**（`apps/editor/src/renderer/services/acp/session/acpSessionRestoreCoordinator.ts:250`，通道 id `acpSessionRestore` 在同文件 `:151`）。这行是**判决书**：出现即本窗口刚发生过被判定为 OOM 的崩溃，且自动恢复已被保护性跳过——别把「重启后会话没回来」再当独立 bug 查。
3. **`processes.txt` 里同一 session 的多个 `--resume` 命令行**（如 3 个 `claude.exe --resume=<同一 session>`）。renderer 崩溃后旧 agent 进程无人回收，crash reload 又 spawn 一个新的：这些孤儿还在后台读扫，放大下一轮压力。修法（`AcpHostMainService`/`ExtensionHostMainService` 的 `stopAllForWindow`）与计数器口径见 `docs/development/memory-pressure.md`「崩溃恢复链路」。

**旁证**：`sessionWatchedChanges.log`（通道 id `sessionWatchedChanges`，`apps/editor/src/renderer/contributions/SessionWatchedChangesContribution.ts:105`）的 watched-change storm = 大规模工具活动正在发生，用于解释「为什么这个会话在长」；它本身不是死因。

## 交叉还原（三件套之外还能看什么）

- **`acpProtocol.log` 只留尾部 512KB**（各日志统一，`apps/editor/src/main/services/diagnostics/diagnosticsMainService.ts` 的 `LOG_TAIL_BYTES`），崩溃前原文常已滚出窗口 → 改用三份交叉还原：`processMetrics` 的曲线形状 + `tabSwitchPerf.log` 里 `ipc.decode` 相位的**连发**（形如 `ipc.decode (response fileSearch.findFiles #42, 18.4MB)`，见 `docs/development/memory-pressure.md` §一）+ `sessionWatchedChanges.log` 的 storm。
- **`ipc-frames.txt`**：main 侧的帧 ring 记录。renderer 自己那份在 OOM 时来不及落盘，所以「同一份内容被反复读回来」这一维度**只有 main 侧这份是权威答案**。
- **`memory.txt` / `sysinfo.md`**：main 堆 + 系统提交内存 + 托管进程树内存 + `[memory] …` 水位行。

## 判定流程

1. **确认是 OOM 而不是别的**：`acpSessionRestore` 的 `skipping` 行或 `errors.jsonl` 的 `renderProcessGone`（`source=renderer:<id>`）命中即 OOM 家族；`oom-lo-space-size=<n>MB` 字样直接给出崩溃时的堆量级。都没有则先查 `error-diagnostics.md` 的异常退出取证。
2. **看曲线形状定「族」**（决定后面查哪里）：分钟级暴涨（回放期）/ 数小时慢爬（某条常驻路径没有预算）/ 受压线上方长期滞留（释放无效或削的是无关内容）/ 周期性尖峰（另有未修项，见 `memory-pressure.md`「已知取舍与后续项」）。
3. **按族对照预算清单**：回放期 → 回放预算窗口与源头 cap（`apps/editor/src/renderer/services/acp/session/cases-memory-budget.md`）；live 期 → `LIVE_INGESTION_BUDGET` 与 children 递归修剪（同文件）；慢爬 → 「每条常驻路径是否都被某个度量覆盖」，重点怀疑 `_observables` / 缓存类常驻结构。
4. **核对结论**：结论必须能对上 `holders=`/`counts=`/`unexplained=` 与 `flow=`/`gauge=` 两组读数（`memory-pressure.md` 第五、六类缺口）。**零修剪告警却在爬升 = 增长完全在记账之外**，这才是要报的结论。
5. **沉淀**：新形态追加到 `references/cases.md`（信号行必填），并在下方「案例索引」补一行。

## 案例索引（按三件套信号速查）

- `skipping auto-restore` 出现 + 0.5GB→5.5GB / 40s + 会话含子 agent 大量 Read/Grep → 案例 1（回放绕过预算窗口）
- 同一 session 多个 `--resume` 孤儿 + 三个独立缺口叠加（live / 回放 / 孤儿） → 案例 2
- 切 tab 后 20s 内冲 4.4GB、`acpProtocol.log` 尾部窗口不足以还原 → 案例 3（codex 回放无源头 cap）
- 0.7GB 慢爬到 5.4GB、`holders` 与 `used` 缺口巨大且修剪告警零命中 → 案例 4（observable 双份全文）

## 关键参考路径

- `docs/development/memory-pressure.md` —— 机制/阈值/releaser 表/诊断包文件/已知取舍（**先读它**）
- `docs/development/error-diagnostics.md` —— 诊断包组成、errors.jsonl、崩溃闭环、脱敏
- `apps/editor/src/renderer/services/memory/` —— `memoryPressureService.ts`（分级与释放）、`rendererHeapReporter.ts`（曲线出站）、`boundedCache.ts`
- `apps/editor/src/renderer/services/acp/session/cases-memory-budget.md` —— 会话/持久化预算族（含 tracker 活行）
- `apps/editor/src/main/services/diagnostics/` —— zip 组装、`LOG_TAIL_BYTES`、受控堆快照
- `apps/editor/cases-interaction-perf.md` + skill `analyze-interaction-performance` —— 渲染节奏 / 切 tab 面

## 其它

- 后续用本 skill，发现新经验按「判定流程」第 5 步同步更新 `references/cases.md` 与上面的索引。
- 本 skill 只做**读法与定性**；修完之后的验证走 `pnpm check` 与对应 e2e（如 `smoke.memoryPressure.spec.ts`）。
