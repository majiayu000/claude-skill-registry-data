---
name: ai-short-drama-delivery-baseline
description: 用于 AI 短剧的确定交接版本、依赖和包内文件清单。交付交付版本与清单的专项结果；综合阶段任务使用 ai-short-drama-handoff，不自动执行其他子步骤。
---

# G5 交接-1 交付版本与清单

## 输入与范围

指定剧本、设定台账、审核报告、交付范围。

先读[共同约定](../ai-short-drama-writing/references/common.md)，再按需读[交接协议](../ai-short-drama-writing/references/handoff.md)与模板第7节。入口：[标准](../ai-short-drama-writing/references/standards.md)、[流程](../ai-short-drama-writing/references/workflow.md)、[模板](../ai-short-drama-writing/assets/templates.md)。

## 执行

1. 确定唯一正文基线及准确路径/版本，发现混用先列冲突。
2. 记录draft/reviewed/locked及真实依据，草稿按用户请求可预交接但标未审核。
3. 列应有文件、现有文件、缺失项及影响；后续提取完再核对清单，不假填接收状态。

## 产物与写入边界

handoff/<集>-<版本>.md 的清单：文件、来源版本、用途、状态、缺失影响、锁定依据。

默认在已有项目文件的对应章节维护；无文件时可先交付同结构文本。只修改上述产物及用户明确要求的必要关联内容，其他问题列影响与返工建议。每次标明输入版本、输出版本、覆盖范围和未决项。

## 验收与返工

包内来源可追踪，未锁定仅供预制作；清单不等于所有内容已完成。

多个基线冲突无法消解时不拼接正文，等待必要选择。

本步骤完成后停止，除非用户已要求后续步骤。可通过[阶段入口](../ai-short-drama-handoff/SKILL.md)衔接；直接调用无需先执行阶段入口。共享资料与父入口需要保留相邻目录。

## 可核对交付

需要逐句机器核对时读取[结构化记录](../ai-short-drama-writing/references/structured-records.md)，按[操作手册](../ai-short-drama-writing/references/operations.md)执行 parity/bundle。MATCH 仅表示列明字段一致；接收、配音实测与语义审查分别保留真实依据，缺少时标未验证。
