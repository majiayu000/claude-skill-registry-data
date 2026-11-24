---
name: ai-short-drama-structured-export
description: 将 AI 短剧交接信息导出为 JSON 或校对交付包。交付结构化导出与交付核对的专项结果；综合阶段任务使用 ai-short-drama-handoff，不自动执行其他子步骤。
---

# G5 交接-5 结构化导出与交付核对

## 输入与范围

同版本正文、交接表、协议、下游格式要求。

先读[共同约定](../ai-short-drama-writing/references/common.md)，再按需读交接协议与模板第7节。入口：[标准](../ai-short-drama-writing/references/standards.md)、[流程](../ai-short-drama-writing/references/workflow.md)、[模板](../ai-short-drama-writing/assets/templates.md)。
导出前必须读[交接协议](../ai-short-drama-writing/references/handoff.md)。

## 执行

1. 只有需要机器读取才按协议导出JSON；否则核对可读包。明确协议版本，不宣称平台API兼容。
2. 检查字段类型、枚举、ID唯一、引用存在、时间相加与目标范围；逐句和正文核对。
3. 对照交付清单核查缺失与失效版本，保留未决项和审核状态，不代填接收记录。

## 产物与写入边界

可选同版本JSON及交付核对结果：覆盖文件、格式/引用/时长/逐句检查结果、缺失、状态。

默认在已有项目文件的对应章节维护；无文件时可先交付同结构文本。只修改上述产物及用户明确要求的必要关联内容，其他问题列影响与返工建议。每次标明输入版本、输出版本、覆盖范围和未决项。

## 验收与返工

可解析与内容一致分别验证；无测试不得声称已通过，格式通过不等于剧情或制作通过。

提取错误在本层修；剧情矛盾回审核；目标超时不能在导出时暗改数值。

本步骤完成后停止，除非用户已要求后续步骤。可通过[阶段入口](../ai-short-drama-handoff/SKILL.md)衔接；直接调用无需先执行阶段入口。共享资料与父入口需要保留相邻目录。

## 可核对交付

需要逐句机器核对时读取[结构化记录](../ai-short-drama-writing/references/structured-records.md)，按[操作手册](../ai-short-drama-writing/references/operations.md)执行 parity/bundle。MATCH 仅表示列明字段一致；接收、配音实测与语义审查分别保留真实依据，缺少时标未验证。
