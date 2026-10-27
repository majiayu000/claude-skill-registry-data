---
name: word-document-review-basic
description: "Perform a lightweight, read-only, text-only Word check only when the user explicitly limits the task to wording, heading hierarchy, simple grammar, obvious consistency, and unresolved placeholders without editing the source, preserving complex formatting, or handling tracked changes, comments, complex tables, images, headers, footers, or visual layout. Do not use for an unqualified Word or document review; use document-review for holistic structure, logic, facts, revisions, formatting, tables, links, comments, or rendered DOCX verification. 仅在用户明确把任务限定为基础、轻量、只读、纯文本检查时，检查 Word 文档的文字、标题层级、简单语法、明显一致性和未解决占位符，不编辑源文件、不保留复杂格式，也不处理修订痕迹、批注、复杂表格、图片、页眉页脚或视觉版式。不得用于未限定范围的通用 Word 或文档审查；整体结构、逻辑、事实、修订、格式、表格、链接、批注或 DOCX 渲染验证应使用 document-review。"
---

# English

# Basic Word Document Review

Perform only an explicitly requested lightweight, read-only check of accessible Word text and headings.

## Safety Boundary

- Do not use company-internal templates.
- Do not provide legal conclusions.
- Do not edit, rewrite, overwrite, or create a revised document.
- Do not handle tracked changes, comments, complex tables, images, headers, footers, complex formatting, or visual layout.
- Cite accessible paragraph, heading, or section references when available.

## Routing Boundary

- Use this Skill only when the user explicitly requests basic, lightweight, text-only review without source edits or complex-format handling.
- Route an unqualified request such as “Review this Word document” or “document review” to `document-review`.
- Route holistic structure or logic review, fact checking, revisions, tracked changes, comments, tables, images, links, format preservation, or rendered DOCX verification to `document-review`.
- Tool unavailability does not make a generic Word request basic. If an explicitly basic request has no accessible text, state the limitation and stop rather than expanding the scope.

## Workflow

1. Confirm that the user explicitly wants a basic, text-only, read-only check.
2. Confirm that document text and heading structure are accessible and record any extraction limits.
3. Check wording, heading hierarchy, simple grammar, obvious terminology inconsistencies, and unresolved placeholders.
4. Cite accessible text locations for each finding.
5. Return a concise issue list, manual confirmation items, and the complex document features that were not reviewed.

# Output Format

1. Text-only scope and access limits
2. Heading and wording findings
3. Obvious textual consistency findings
4. Placeholder findings
5. Accessible text references
6. Manual confirmation items and excluded complex features

# 简体中文

# Word 文档基础审查

仅执行用户明确要求的轻量、只读 Word 可访问文字与标题检查。

## 安全边界

- 不使用公司内部模板。
- 不给出法律结论。
- 不编辑、改写、覆盖或创建修订后的文档。
- 不处理修订痕迹、批注、复杂表格、图片、页眉页脚、复杂格式或视觉版式。
- 可用时引用可访问的段落、标题或章节位置。

## 路由边界

- 仅在用户明确要求基础、轻量、纯文本且不修改源文件或处理复杂格式时使用本 Skill。
- “审查这个 Word 文档”或“文档审查”等未限定范围的请求应交给 `document-review`。
- 整体结构或逻辑审查、事实核验、修订、修订痕迹、批注、表格、图片、链接、格式保留或 DOCX 渲染验证应交给 `document-review`。
- 工具不可用不会把通用 Word 请求变成 basic；明确 basic 的请求如果没有可访问文字，应说明限制并停止，不得自行扩大范围。

## 工作流程

1. 确认用户明确要求基础、纯文本、只读检查。
2. 确认文档文字和标题结构可访问，并记录提取限制。
3. 检查措辞、标题层级、简单语法、明显术语不一致和未解决占位符。
4. 为每个发现引用可访问文字位置。
5. 输出精简问题清单、人工确认项和未审查的复杂文档特征。

# 输出格式

1. 纯文本范围与访问限制
2. 标题和措辞问题
3. 明显文本一致性问题
4. 占位符问题
5. 可访问文字位置
6. 人工确认项与未审查的复杂特征
