---
name: pdf-review
description: "Default to this Skill for an unqualified PDF review and for checks involving searchable text, structure, tables, page-located claims, numeric consistency, citations, scanned pages, OCR, rendering, completeness, or visual layout. Detect available capabilities and degrade within this Skill when tools are unavailable; do not modify the source PDF or claim unsupported verification. Do not use when the user explicitly requests pdf-review-basic or a lightweight, text-only check without OCR, rendering, or complex layout review. 未限定范围的通用 PDF 审查，以及涉及可搜索文字、结构、表格、页码定位、数字一致性、引用、扫描页、OCR、渲染、完整性或视觉版式的检查，默认使用本 Skill。检测可用能力，工具不可用时仍在本 Skill 内降级；不得修改原 PDF 或声称完成不受支持的验证。用户明确指定 pdf-review-basic，或明确要求不做 OCR、渲染和复杂版式检查的轻量纯文本任务时不使用本 Skill。"
---

# PDF Review（PDF 审查）

Use the section matching the user's language. 使用与用户输入语言一致的章节。

# PDF Review

Read `references/productivity-evidence-and-file-safety.md` and `references/pdf-capability-matrix.md`.

Treat an unqualified request such as “Review this PDF” as this Skill's default. Use `pdf-review-basic` only when the user explicitly asks for a basic, lightweight, text-only check without OCR, rendering, scanned-content, table, image, or complex-layout review. Capability gaps do not transfer a generic request to the basic Skill; continue here with a clearly stated reduced scope.

1. Confirm the review objective: content, figures, citations, completeness, tables, page layout, or all applicable dimensions.
2. Detect available capabilities separately for metadata, text extraction, page mapping, table extraction, rendering, and OCR. State the document mode and which checks are possible before drawing conclusions.
3. Preserve page locations from the tool output. Never infer a page number from text order when page mapping is unavailable.
4. Review structure, table of contents, missing or duplicate pages when verifiable, extraction corruption, tables, figures, numeric contradictions, references, headers/footers, and cross-references.
5. Render representative and issue-related pages for visual review when possible. Treat OCR as uncertain evidence and quote it only with an OCR label and confidence warning.
6. Report each finding with page or location status, evidence, impact, severity, confidence, and recommendation. Separate content findings from extraction/OCR and layout findings.

Keep the original PDF read-only. If rendering or OCR is unavailable, explicitly exclude visual or scanned-content conclusions.

# Output Contract

1. Scope, PDF mode, and capability matrix
2. Document and page-structure summary
3. Findings with page/location status, severity, evidence, impact, and confidence
4. Content, table, citation, extraction/OCR, and visual findings
5. Unreviewed pages or capabilities and limitations

---

# PDF 审查

读取 `references/productivity-evidence-and-file-safety.md` 和 `references/pdf-capability-matrix.md`。

“审查这个 PDF”等未限定范围的请求默认由本 Skill 处理。只有用户明确要求基础、轻量、纯文本，且不做 OCR、渲染、扫描内容、表格、图片或复杂版式审查时，才使用 `pdf-review-basic`。能力工具不足不会把通用请求转给 basic；应继续在本 Skill 内明确降级范围。

1. 确认审查目标：内容、数字、引用、完整性、表格、页面版式或其中适用组合。
2. 分别检测元数据、文本提取、页码映射、表格提取、渲染和 OCR 能力；在得出结论前声明文档模式和可执行检查。
3. 保留工具返回的页面位置；无法映射页面时，绝不根据文本顺序猜页码。
4. 在可验证范围内检查结构、目录、缺页或重页、提取乱码、表格、图形、数字矛盾、引用、页眉页脚和交叉引用。
5. 工具允许时渲染代表页和问题页进行视觉检查；OCR 只作为不确定证据，引用时标记 OCR 和置信度风险。
6. 每个发现给出页码或位置状态、证据、影响、严重度、置信度和建议，并区分内容、提取/OCR 和版式问题。

原 PDF 保持只读。无法渲染或 OCR 时必须排除视觉或扫描内容结论。

# 输出契约

1. 范围、PDF 模式与能力矩阵
2. 文档和页面结构摘要
3. 含页码/位置状态、严重度、证据、影响和置信度的发现
4. 内容、表格、引用、提取/OCR 和视觉发现
5. 未审页面或能力及限制
