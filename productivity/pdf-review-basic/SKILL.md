---
name: pdf-review-basic
description: "Perform a lightweight, read-only, text-only PDF check only when the user explicitly limits the task to extractable text, headings, obvious textual issues, and a short issue list without OCR, rendering, scanned-content recognition, tables, images, complex layout, or source-file changes. Do not use for an unqualified PDF review; use pdf-review for generic requests, page or visual verification, OCR, scanned pages, tables, images, layout, or completeness. PDF modification or regeneration is outside both review Skills and requires a separately authorized editing workflow. 仅在用户明确把任务限定为基础、轻量、只读、纯文本检查时，检查 PDF 的可提取文字、标题和明显文本问题并给出简短清单，不做 OCR、页面渲染、扫描内容识别、表格、图片、复杂版式或源文件修改。不得用于未限定范围的通用 PDF 审查；通用请求、页码或视觉核验、OCR、扫描页、表格、图片、版式或完整性应使用 pdf-review。PDF 修改或重新生成不属于这两个审查 Skill，需要另行授权的编辑流程。"
---

# English

# Basic PDF Review

Perform only an explicitly requested lightweight, read-only check of extractable PDF text.

## Safety Boundary

- Do not provide legal conclusions.
- Do not provide financial or investment advice.
- Do not infer missing content without marking it as an assumption.
- Do not modify or regenerate the PDF.
- Do not perform OCR, rendering, scanned-page recognition, table or image review, complex-layout review, or missing-page verification.
- Cite an extracted section or page marker only when the extraction result supplies it; never infer one.

## Routing Boundary

- Use this Skill only when the user explicitly requests basic, lightweight, text-only review without OCR or rendering.
- Route an unqualified request such as “Review this PDF” to `pdf-review`.
- Route page-level, visual, scanned, OCR, table, image, layout, or completeness requests to `pdf-review`.
- PDF modification or regeneration is outside both review Skills; do not treat an editing request as review or claim that either Skill changed the file.
- Tool unavailability does not make a generic PDF request basic. If an explicitly basic request has no extractable text, state the limitation and stop rather than expanding the scope.

## Workflow

1. Confirm that the user explicitly wants a basic, text-only, read-only check.
2. Confirm that extractable text is available and record any extraction limits.
3. Check headings, obvious grammar or terminology problems, unresolved placeholders, and clear contradictions within the extracted text.
4. Cite extracted text locations when available and list items that require manual confirmation.
5. Return a concise text-issue list and explicitly name the advanced checks that were not performed.

# Output Format

1. Text-only scope and extraction limits
2. Extracted heading and text overview
3. Text findings with supplied section or page markers when available
4. Obvious textual consistency issues
5. Manual confirmation items
6. Excluded OCR, visual, layout, table, image, and scanned-content checks

# 简体中文

# PDF 基础审查

仅执行用户明确要求的轻量、只读 PDF 可提取文字检查。

## 安全边界

- 不给出法律结论。
- 不提供财务或投资建议。
- 不把缺失内容当作事实；需要标记为推断。
- 不修改或重新生成 PDF。
- 不执行 OCR、页面渲染、扫描页识别、表格或图片审查、复杂版式审查或缺页核验。
- 只有提取结果明确提供时才引用章节或页码标记，绝不推断位置。

## 路由边界

- 仅在用户明确要求基础、轻量、纯文本且不做 OCR 或渲染时使用本 Skill。
- “审查这个 PDF”等未限定范围的请求应交给 `pdf-review`。
- 页码级、视觉、扫描件、OCR、表格、图片、版式或完整性请求应交给 `pdf-review`。
- PDF 修改或重新生成不属于这两个审查 Skill；不得把编辑请求当作审查，也不得声称任一 Skill 已修改文件。
- 工具不可用不会把通用 PDF 请求变成 basic；明确 basic 的请求如果没有可提取文字，应说明限制并停止，不得自行扩大范围。

## 工作流程

1. 确认用户明确要求基础、纯文本、只读检查。
2. 确认可提取文字可用，并记录提取限制。
3. 检查标题、明显语法或术语问题、未解决占位符和提取文字中的清晰矛盾。
4. 在可用时引用提取文字位置，并列出需要人工确认的事项。
5. 输出精简文字问题清单，并明确未执行的高级检查。

# 输出格式

1. 纯文本范围与提取限制
2. 提取到的标题和文字概览
3. 含已有章节或页码标记的文字问题
4. 明显文本一致性问题
5. 人工确认项
6. 未执行的 OCR、视觉、版式、表格、图片和扫描内容检查
