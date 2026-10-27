---
name: document-review
description: "Default to this Skill for an unqualified document or Word review and for holistic checks of structure, logic, completeness, terminology, factual support, figures, citations, grammar, formatting, tables, links, comments, tracked changes, or authorized revisions. When DOCX or rendering tools are unavailable, degrade within this Skill and state the limitation. Use content-consistency-check for cross-document reconciliation, and do not use when the user explicitly requests word-document-review-basic or a lightweight, read-only, text-and-headings-only Word check without complex formatting or revisions. 未限定范围的通用文档或 Word 审查，以及结构、逻辑、完整性、术语、事实依据、数字、引用、语法、格式、表格、链接、批注、修订痕迹或获授权修订等整体检查，默认使用本 Skill。DOCX 或渲染工具不可用时仍在本 Skill 内降级并说明限制。跨文档核对应使用 content-consistency-check；用户明确指定 word-document-review-basic，或明确要求轻量、只读、只检查文字和标题且不处理复杂格式或修订时不使用本 Skill。"
---

# English

# Document Review

Read `references/productivity-evidence-and-file-safety.md` and `references/document-review-checklist.md`.

Treat an unqualified request such as “Review this document” or “Review this Word document” as this Skill's default. Use `word-document-review-basic` only when the user explicitly requests a basic, lightweight, read-only check limited to accessible text and headings without editing, tracked changes, comments, complex tables, images, or formatting preservation. Capability gaps do not transfer a generic request to the basic Skill; continue here with a clearly stated reduced scope.

1. Confirm the audience, purpose, review depth, source of truth, allowed fact-checking, and whether the user wants findings only or an edited copy.
2. Verify the available reader and, for DOCX edits, the ability to preserve structure and render the result. If unavailable, review only accessible text and state formatting limits.
3. Review the document as a whole before line edits: structure, argument, missing sections, contradictions, unsupported claims, figures, citations, terminology, grammar, links, tables, captions, and formatting consistency.
4. Report issues with location, evidence, impact, and a concrete suggestion. Classify them as required, recommended, or optional. Do not rewrite the whole document by default.
5. If edits are explicitly requested, preserve meaning, headings, tables, links, terminology, and traceability; write a new file unless overwrite is explicit.
6. Reopen and render the edited artifact when tools support it. Report which textual, structural, link, and visual checks passed or remained unavailable.

Use `content-consistency-check` when the primary task is reconciling values across multiple artifacts.

# Output Contract

1. Scope, audience, and capability status
2. Required changes
3. Recommended changes
4. Optional polish
5. Edited-file location when authorized
6. Validation results and limitations

# 简体中文

# 文档审查

读取 `references/productivity-evidence-and-file-safety.md` 和 `references/document-review-checklist.md`。

“审查这份文档”或“审查这个 Word 文档”等未限定范围的请求默认由本 Skill 处理。只有用户明确要求基础、轻量、只读、仅检查可访问文字和标题，且不编辑、不处理修订痕迹、批注、复杂表格、图片或格式保留时，才使用 `word-document-review-basic`。能力工具不足不会把通用请求转给 basic；应继续在本 Skill 内明确降级范围。

1. 确认读者、目的、审查深度、权威依据、是否允许事实核验，以及用户只要问题清单还是编辑后副本。
2. 确认平台具备文档读取能力；编辑 DOCX 时还需具备结构保留和渲染能力。工具不可用时只审查可访问文本，并声明格式限制。
3. 先整体后局部检查结构、论证、缺失内容、矛盾、无依据主张、数字、引用、术语、语法、链接、表格、图注和格式一致性。
4. 每个问题给出位置、证据、影响和具体建议，并分为必须修改、建议修改和可选润色；默认不整篇重写。
5. 用户明确要求编辑时，保留原意、标题、表格、链接、术语和追踪性；除非明确覆盖，否则写入新文件。
6. 工具支持时重新打开并渲染编辑结果，报告文本、结构、链接和视觉检查的通过项与不可用项。

主要任务是核对多个材料间的值时使用 `content-consistency-check`。

# 输出契约

1. 范围、读者和能力状态
2. 必须修改
3. 建议修改
4. 可选润色
5. 获授权时的编辑文件位置
6. 验证结果与限制
