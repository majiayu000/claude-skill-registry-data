---
name: 3380p-rule-maintainer
description: "维护 Chroma 3380P ATE 项目的编码规则、review checklist、notes 和本地 skills。用于用户提出新增/修改/废弃 3380P 写代码规则、评审规则、生成约束、checklist 条目、经验沉淀或来源链路同步时；尤其适用于把一次代码评审反馈转成长期规则。"
---

# 3380P 规则维护

## 工作流

1. 读取 `rules/3380P_project_style.md`，再按任务读取 `references/rule_update_targets.md` 中列出的目标文件。
2. 判断规则类型：代码生成约束、评审检查项、专题 note、clean/bad example 说明、skill 行为或 AGENTS 入口。
3. 在最小必要范围内同步规则。通用编码约束放入 `rules/3380P_project_style.md`；review 时必须检查的风险放入 `skills/3380p-code-review/references/review_checklist.md`；专题生成流程才同步到对应 `notes/`。
4. 新增条目必须保留来源链路。用户直接给出的规则可写“来源：用户规则反馈”，如有现有代码证据，再附具体文件路径。
5. 不删除旧规则，除非用户明确说明规则废弃；如果新规则修正旧表述，保留兼容上下文并收敛成更明确的检查方式。
6. 修改后用 `rg` 核对关键词是否只落在预期位置，并阅读变更片段确认中文、编号和 Markdown 结构正常。

## 落点原则

- 影响所有新生成 `.pln` / `.dec` / `.pat` 的规则，更新 `rules/3380P_project_style.md`。
- 用户要求“同步到 checklist”或规则可作为 review finding，更新 `skills/3380p-code-review/references/review_checklist.md`。
- 影响 test plan 转 PLN 的输入契约或验收 checklist，更新 `notes/test_plan_to_pln_generation_quick_reference.md`。
- 影响某一专题生成方法，例如 binary trim、supply sweep、register setup，只在对应 `notes/*.md` 中追加简短条目。
- 影响某个 skill 的使用流程，更新对应 `skills/*/SKILL.md`，必要时同步 `agents/openai.yaml` 描述。

## 写法要求

- 用短条目描述可执行检查点，避免复制大段代码。
- 对具体 statement、宏名和文件名使用反引号。
- 对新增 checklist item 写清风险和推荐检查方式，而不只写“注意某事”。
- 保持现有中文风格、章节层级和编号连续。
- 对 3380P tester 未验证的规则，不写成已上机验证事实；可写成项目编码约束或用户反馈规则。

