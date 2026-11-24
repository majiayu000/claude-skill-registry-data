---
name: ai-short-drama-audio-handoff
description: 用于 AI 短剧的提取配音台词、旁白、音效和声音要求。交付对白与声音交接的专项结果；综合阶段任务使用 ai-short-drama-handoff，不自动执行其他子步骤。
---

# G5 交接-3 对白与声音交接

## 输入与范围

基线正文、人物口吻及声线设定。

先读[共同约定](../ai-short-drama-writing/references/common.md)，再按需读[交接协议](../ai-short-drama-writing/references/handoff.md)与模板第7节。入口：[标准](../ai-short-drama-writing/references/standards.md)、[流程](../ai-short-drama-writing/references/workflow.md)、[模板](../ai-short-drama-writing/assets/templates.md)。

## 执行

1. 逐句提取对白ID、场ID、角色、方式与原文，保留否定词和必要停顿。
2. 整理读音、语气、同时说话/画外等关系；分离对白、环境声、音效和屏幕文字。
3. 逐句回查，不为配音顺口自行改词；未有录音不填实测时长。

## 产物与写入边界

交接单的对白/声音表：对白ID、场ID、说话者、方式、原文、读法、必要表演；音效位置与作用。

默认在已有项目文件的对应章节维护；无文件时可先交付同结构文本。只修改上述产物及用户明确要求的必要关联内容，其他问题列影响与返工建议。每次标明输入版本、输出版本、覆盖范围和未决项。

## 验收与返工

对白不漏句、不改义、说话者存在，声音需求可定位。

改词需要回正文修订；提取稿不能成为不同版本的第二份剧本。

本步骤完成后停止，除非用户已要求后续步骤。可通过[阶段入口](../ai-short-drama-handoff/SKILL.md)衔接；直接调用无需先执行阶段入口。共享资料与父入口需要保留相邻目录。

## 可核对交付

需要逐句机器核对时读取[结构化记录](../ai-short-drama-writing/references/structured-records.md)，按[操作手册](../ai-short-drama-writing/references/operations.md)执行 parity/bundle。MATCH 仅表示列明字段一致；接收、配音实测与语义审查分别保留真实依据，缺少时标未验证。
