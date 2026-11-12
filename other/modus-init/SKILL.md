---
name: modus-init
description: 用户请求首次建立完整项目知识时，基于当前源码与材料初始化知识树；已有稳定 Domain/Module 身份时转入 modus-reinit 全量复核。
---

# modus-init

首次建立正文知识时使用。正文执行路线只有[六阶段入口](../using-modus/references/authoring/index.md)，质量与写入规则在其共享细则维护；本文件负责选择工作流。

## 先判断新任务或续作

开始 status、build 或调查前，先读取并执行[开始或恢复](../using-modus/references/authoring/index.md#开始或恢复)，完成续作、新任务、工作区和稳定身份的判断。只有新一轮普通项目且没有可恢复的 Domain/Module 身份时，才从下表 K1 开始；已有身份转 [modus-reinit](../modus-reinit/SKILL.md)，复用本轮盘点。

## 六个阶段入口

| 阶段 | 必须读取的入口 | 本工作流的动作 |
| --- | --- | --- |
| K1 | [范围建模](../using-modus/references/authoring/stages/k1-scope.md) | 本轮构建一次、scope-discovery、完整调查与一次范围确认 |
| K2 | [创作计划](../using-modus/references/authoring/stages/k2-plan.md) | 全局依赖与主定义先行，再安排当前域的目标与验收 |
| K3 | [证据闭环](../using-modus/references/authoring/stages/k3-evidence.md) | 逐 Module 精确取证、逐接口/字段/规则/场景核对 |
| K4 | [领域成稿](../using-modus/references/authoring/stages/k4-domain.md) | 完成六专题、模块与路由，逐篇回读和实际预览 |
| K5 | [项目约束](../using-modus/references/authoring/stages/k5-constraints.md) | 复用前序事实与机器线索，独立提炼并验收首次 Team Standard |
| K6 | [系统概览与发布](../using-modus/references/authoring/stages/k6-publish.md) | 消费 K4/K5 编写概览、补共享导航、全局回读、publication 与原卡清理 |

K1 后先做全局 K2，再按完整 Domain 循环 K2 → K3 ↔ K4，全部域完成后执行 K5/K6。进入阶段时确保已完整读取入口列出的适用细则，仍完整有效的内容按上下文合同复用，不只依据此表。未授权委派时由同一作者持续执行；只有用户明确授权且边界可拆分时才按[并行协议](../using-modus/references/authoring/parallel-domain-authoring.md)委派；范围确认不自动授权 subagent。

## 不变量

- 质量优先于一次写完的域数。遵守[初始化质量要求](../using-modus/references/authoring/framework/index.md#初始化质量要求)，全面覆盖已确认材料与正文，并完成相应案例、图形与实际预览。
- 每个可恢复单元按[执行策略](../using-modus/references/authoring/execution-strategy.md#在现有阶段内组织工作)保存后继续；恢复时先读原卡定位，仅补缺失输入，保持后续域深度。
- 一个 Domain 同时只有一个正文作者；根作者独占执行卡、共享事实与最终验收。跨域信息按[协作合同](../using-modus/references/authoring/cross-domain.md)持续传播，不等 K6 才拼接。
- 人工 constraint/business 默认保护；全部写入遵守读时哈希、锁、CAS 与原子替换，脚本不批量生成自然语言正文。
- publication clean 不替代内容与视觉验收；存在待验位置时保留原卡并如实说明。
