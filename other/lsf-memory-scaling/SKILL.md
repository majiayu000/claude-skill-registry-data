---
name: lsf-memory-scaling
description: LSF 作业内存不足时的调整技能。当作业因内存不够被挂起(SSUSP)或终止(EXIT/MEMLIMIT)时，通过调整 bsub -n 的节点（核数/slot）数量来扩大可用内存——可用运行内存 ≈ 5GB × 申请节点数。当用户说内存不足、作业被杀、OOM、需要更大内存，或排查 EXIT/SSUSP 作业时，配合 lsf-ncpgr skill 一起使用。
tags: [lsf, memory, oom, memlimit, bsub, bmod, 内存, 内存不足]
triggers: ["内存不足", "内存不够", "OOM", "out of memory", "MEMLIMIT", "SSUSP", "作业被杀", "加大内存", "调整内存"]
used_with: [lsf-ncpgr]
solves: ["LSF作业内存不足", "作业因内存被终止", "SSUSP挂起", "调整作业运行内存"]
---

# LSF 作业内存调整（5GB × 节点数）

## 核心规则

**本集群作业可用运行内存 = 5GB × 申请节点数（`#BSUB -n` 的 slot 数）。**

内存不够时不要加 `-M` / `rusage[mem=...]`（违反 lsf-ncpgr 编写规范，队列已自动管理内存），
而是**增加 `-n` 的数值**：每多申请 1 个 slot，作业多获得约 5GB 可用内存。

| 需要内存 | 计算 | 申请 |
|---------|------|------|
| 10 GB | 10 ÷ 5 | `#BSUB -n 2` |
| 20 GB | 20 ÷ 5 | `#BSUB -n 4` |
| 40 GB | 40 ÷ 5 | `#BSUB -n 8` |
| 80 GB | 80 ÷ 5 | `#BSUB -n 16` |
| 100 GB | 100 ÷ 5（向上取整） | `#BSUB -n 20` |

公式：**`slots = ceil(需要的GB数 / 5)`**，宁多勿少。

## 什么时候触发本技能（内存不足的信号）

满足以下任意一条，即按"内存不足"处理：

- `bjobs` 显示作业状态为 **SSUSP**（节点内存不足被系统挂起）
- 作业 **EXIT**，且 `.err` / `bjobs -l <jobid>` 输出中出现：
  - `TERM_MEMLIMIT`、`Exceeded job memory limit`
  - `Out of memory`、`Cannot allocate memory`、`std::bad_alloc`
  - `Killed` / exit code **137**（OOM killer）
- 程序日志提示内存分配失败（如 samtools/bwa 的 allocation 报错）
- 用户直接说"内存不够/加大内存/OOM"

## 处理流程（必须按顺序执行）

1. **确认是内存问题**：`bjobs -l <jobid>` 或查看 `<jobid>.err`，找到上面的信号之一。不要凭空猜测。
2. **估算所需内存**：询问用户该任务大概需要多少内存；用户不清楚时，按上次申请量翻倍估算。
3. **换算节点数**：`slots = ceil(所需GB / 5)`。
4. **先征得用户同意再操作**（用 ask_user，把换算结果做成选项）：
   > "该作业因内存不足失败。按 5GB×节点数 计算，需要 N 个 slot（约 5N GB）。是否改为 -n N 重新提交？"
   > 候选选项示例：`改为 -n N 重新提交`、`改为 -n 2N 保险一点`、`换 smp/high 大内存队列`、`先不处理`
5. **执行调整**（二选一）：
   - 作业还在排队（PEND）：`bmod -n <slots> <jobid>`
   - 作业已结束（EXIT/DONE）：修改 `.lsf` 脚本中的 `#BSUB -n <slots>`，重新 `bsub < job.lsf`
6. **汇报**：说明 原配置 → 新配置（slots 数与约等于的内存量）、作业 ID。

## 注意事项

- **不要**在脚本中设置 `#BSUB -M` 或 `#BSUB -R "rusage[mem=...]"`——本集群队列已配置自动内存限制，遵循 lsf-ncpgr 的极简编写规范。
- 软件实际使用的线程数应继续用 `$LSB_DJOB_NUMPROC` 引用，改 `-n` 后无需改命令行。
- 单 slot 内存上限受队列约束：normal 约 6-10GB/slot，smp 约 12-20GB/slot，high 约 11-15GB/slot。
  若用户需要的是**单节点超大内存**（如 >100GB 且核数不多），建议换 `smp` 或 `high` 队列，而不是无限堆 slot。
- 增加 slot 会延长排队时间；内存够用时不要多申请（参考 lsf-ncpgr 的资源规划规则）。
- 调整后若仍因内存失败：按新估算值继续上调（每次至少翻倍），并提醒用户检查程序是否存在内存泄漏或输入数据异常。
