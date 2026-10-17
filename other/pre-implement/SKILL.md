---
name: pre-implement
description: 在计划或讨论结束、开始实际交付多步骤任务时调用：新建并维护 implementation notes，逐步记录实现决策；偏离 plan、spec 时记录 Deviations。
---

新建并维护当前任务的 `.agents/notes/<task-slug>-implementation-notes.md`（若目录不存在则自动创建）。已有 notes 属于其他任务时，另起文件。

Implementation notes 属于记录“因果”（为何做此决策、舍弃了什么、踩了什么坑）的演进记录，专供下一次尝试或后续 Agent 学习，不得随意放入面向确定“事实”的 `docs/` 目录中。

文件在任务完成的过程中逐渐生长，不同于一次性生成在执行之前的 spec。在每一步执行后，记录实现过程中做出的决策，供下一次尝试学习。遇到 edge case 迫使你偏离计划时：选保守的那个选项，记录在 Deviations 下（偏离了什么、为什么、选了什么），然后继续实现。

文件顶部维护简短状态区，覆盖本次交付范围内的所有 work unit，包括尚未开始的。每项一行：单元与交付目标、状态（未开始／进行中／待验收／blocked／done）、实际产物路径与验收证据、下一步或阻塞。每次状态变化先更新状态区，再对外汇报；汇报以状态区为依据。

状态由维护本文件的 agent 更新；派发 worker 时，worker 回报证据，派发方验收后更新。仅当该单元约定的交付物存在且有通过验收的证据时标 done；验收标准引用对应 ticket/spec，缺失时先补齐。拆分或调整计划时标明被替代的单元。规划与核查单元的 done 不得外推为整体交付完成——整体 done 须覆盖全部必需交付物。

用户没有给输入 implement 所需要的相关 artifact 时，派一个子代理先调研：spec 文件、prototype、grilling 结论等。
