---
name: brd-generation
description: Generate an SBSI Business Requirements Document (BRD) from the company's standard BRD template (sbsi-template-router/templates/brd/BRD_Template.docx), given a user's requirements. Use when asked to write, draft, or create a BRD, or to fill in the BRD template for a product/feature.
---

# Generating a BRD from SBSI's Standard Template

This is the BRD-specific companion to the `office-file-generation` skill —
read that skill first for the general docx mechanics (docxtemplater vs the
`docx` package, install commands). This skill documents the actual
template's structure so content gets placed correctly and nothing gets
invented.

The canonical template lives at
`../sbsi-template-router/templates/brd/BRD_Template.docx` — a copy of SBSI
Product Development's (PTSP) standard BRD, Vietnamese-language, owned by
PTSP as input to CNTT's (IT/BA) SRS. It lives alongside every other SBSI
document type's template under `sbsi-template-router/templates/` (not in
this skill's own folder) so the whole template set has one predictable
location as new document types get registered — see that skill's
`template_registry.json` and "Adding a new template type" procedure.

## Relationship to sbsi-template-router / sbsi-docx-format-core

BRD is registered as the `brd` document type in `sbsi-template-router`'s
`template_registry.json`, pointing at
`templates/brd/BRD_Template.docx` (+ `templates/brd/template_manifest.json`)
— template *path* resolution for BRD goes through the same router as every
other SBSI document type. This does **not** change who owns BRD's content
workflow: this skill still owns BRD end to end (the direct-XML-DOM-edit
fill technique, the 13-section structure, and the OBJ/BR/RULE/UC/ACT/AC
traceability ID scheme below) — `sbsi-template-router` never touches BRD
content, it only hands back the template path + manifest.

**Format enforcement uses the SAME shared `sbsi-docx-format-core` engine as
every other SBSI document type — BRD is not skipped or special-cased in the
scripts.** What differs is data, not code: BRD's own verified typography
(Times New Roman **12pt** — `docDefaults`/`Normal` resolve to `sz=24`, not
the 13pt governance-document default) and its lack of real Word
heading/outline-level styles (BRD's 13 section titles are large/bold
`Normal`-based text, a PTSP template design choice — this skill's step 4
already says to preserve the template's exact original branding
pixel-for-pixel) are declared explicitly in
`templates/brd/template_manifest.json`'s `typography_profile` and
`requires_real_headings: false` fields. **Always pass
`--manifest ../sbsi-template-router/templates/brd/template_manifest.json`**
when running `validate_sbsi_docx.py` or `normalize_ordinary_text.py`
against BRD output — without it, both scripts fall back to the 13pt
governance default and will (correctly, for a template that doesn't
declare otherwise) report BRD as non-compliant. Chương/Điều
heading-vocabulary and Khoản/Điểm numbering rules don't apply to BRD's
plain numbered sections either way, and never did.

**A real pre-existing typography inconsistency inside `BRD_Template.docx`
itself was found and fixed (2026-08-17):** many ordinary-body runs were
directly overridden to 11pt (`sz=22`) or a bracketed
`[BẮT BUỘC]`/`[KHUYẾN NGHỊ]` tag at 10pt (`sz=20`) instead of the
style-declared 12pt, and a few sub-labels sat exactly at 13pt (`sz=26`) —
real drift inside the live template file (most likely from past copy/paste
edits), not a validator false positive. Fixed by running
`normalize_ordinary_text.py` against the canonical template itself with its
own manifest, verified beforehand (byte-identical text content across all
82 paragraphs, same 20 zip parts, TOC field intact) and verified after
(`validate_sbsi_docx.py` now PASS, 0 warnings). **Not verified**: rendered
appearance in real Word — this environment has no LibreOffice for a
render/visual QA pass, only the structural checks above ran. If a future
edit to this template reintroduces size drift, don't silently loosen the
validator or re-normalize without telling the user first — that's exactly
the shortcut this fix avoided taking.

## Important: this template has no merge tags

`BRD_Template.docx` uses plain red-italic `‹fill-in›` placeholder
text (e.g. `‹điền›`, `‹Tên sản phẩm / tính năng›`), meant for a human to
type over in Word — **not** `docxtemplater`-style `{tags}`. Verified by
extracting `word/document.xml` directly; don't assume otherwise.

Three ways to generate from it — pick based on what the task needs:

1. **Copy the template and edit its XML directly, no tagging** (default —
   validated end-to-end 2026-07-26, see
   `office-file-generation` skill's "Word — filling an existing template
   without pre-tagging (direct XML DOM edit)" section for the full
   technique). Preserves the exact original branding (navy `#1F3864`
   header shading, Times New Roman, borders, `tblGrid`) pixel-for-pixel,
   with no manual Word-UI step and no risk of ever touching the real
   template file. This is now the default choice unless the task
   specifically wants a reusable `{tag}`-based master (option 2).
2. **Tag it once, then template-fill with `docxtemplater`** (worth it only
   if the team wants a permanently reusable tagged master for repeated
   future BRDs edited by hand in Word). Requires a one-time pass replacing
   each `‹placeholder›` with a `{tag}` and wrapping each variable-length
   table's data row with docxtemplater row-loop syntax (`{#objectives}` in
   the first cell of the loop row, `{/objectives}` in the last cell of the
   same row).
3. **Rebuild from scratch with the `docx` package** (last resort — only if
   the copy/edit-XML approach genuinely doesn't fit). Mirror this skill's
   section list/order/table columns below; you won't get the exact
   original table shading/borders unless you replicate them explicitly in
   the `docx` builder API, and you must set `columnWidths` explicitly (see
   the column-collapse pitfall in `office-file-generation`) or tables can
   render broken.

Default to option 1. Only ask the user which path they want if they
specifically mention wanting a reusable tagged master (option 2) or if
option 1 hits something this skill doesn't anticipate.

## Document structure (verbatim from the template)

### Cover page

- Company/department header: "CÔNG TY CỔ PHẦN CHỨNG KHOÁN STANLEY
  BROTHERS (SBSI)" / "Phòng Phát triển Sản phẩm & Dịch vụ Số"
- Title: "TÀI LIỆU YÊU CẦU NGHIỆP VỤ / BUSINESS REQUIREMENTS DOCUMENT (BRD)"
- Product/feature name, doc code `BRD.‹Mã SP›.‹YYNN›`, version, status
  (Dự thảo / Đang review / Đã duyệt), Hà Nội + month/year.

### Document control tables

- **Thông tin chung** (general info): Tên sản phẩm/tính năng, Mã tài liệu,
  Chủ sở hữu (Owner), Người soạn (Author), Người phê duyệt (Approver),
  Trạng thái.
- **Lịch sử phiên bản** (version history): Phiên bản | Ngày | Người thực
  hiện | Mô tả thay đổi.
- **Phê duyệt** (approval/sign-off): Vai trò | Họ tên | Chức danh | Ngày
  duyệt — fixed rows: Người soạn (PO – PTSP), Người phê duyệt (Giám đốc
  PTSP), Bên tiếp nhận (Đại diện CNTT/BA).

### Body — 13 numbered sections

Each section is marked **[BẮT BUỘC]** (mandatory) or **[KHUYẾN NGHỊ]**
(recommended) in the template itself. A section that doesn't apply to a
given BRD must say **"Không áp dụng"** with a reason — never delete the
section heading (this is the template's own stated rule, not a convention
I'm inventing).

1. **Giới thiệu & bối cảnh** (Introduction & context) — [BẮT BUỘC]
   - 1.1 Bài toán kinh doanh [BẮT BUỘC] — free text: the business
     problem/need, current pain point, impact scale, why now (answers
     "Why").
   - 1.2 Mục tiêu & giá trị kinh doanh [BẮT BUỘC] — table `Mã | Mục tiêu |
     Chỉ số đo lường (KPI)`, IDs `OBJ-01, OBJ-02, …`. Goals must be SMART.
   - 1.3 Đối tượng đọc tài liệu — free text, audience (default template
     text: leadership, Business, Product, Compliance, Operations, IT
     BA/QA/Architecture — adjust per project).
2. **Phạm vi (Scope)** — [BẮT BUỘC]
   - 2.1 Trong phạm vi (in scope) — free text.
   - 2.2 Ngoài phạm vi (out of scope) — free text. Template stresses this
     is as important as in-scope, to avoid scope creep.
   - 2.3 Đối tượng/hệ thống liên quan — related systems; for packaged/
     Hybrid CORE rollouts, note partner systems, config-vs-customization
     boundary, expected Gap Analysis points.
3. **Đối tượng tham gia (Actors)** — [BẮT BUỘC] — table `Mã | Đối tượng/
   vai trò | Mô tả trách nhiệm | Quyền hạn nghiệp vụ chính`, IDs `ACT-01,
   ACT-02, …`.
4. **Quy trình nghiệp vụ (Business Process)** — [BẮT BUỘC]
   - 4.1 Quy trình hiện tại (As-Is) — free text/diagram, current process,
     bottlenecks.
   - 4.2 Quy trình mục tiêu (To-Be) — table `Bước | Hoạt động | Mô tả/xử
     lý | Vai trò thực hiện`, numbered steps with input–process–output and
     the actor performing each step.
5. **Yêu cầu nghiệp vụ (Business Requirements)** — [BẮT BUỘC] — table `Mã
   | Mô tả yêu cầu nghiệp vụ | Ưu tiên | Tham chiếu mục tiêu`, IDs `BR-01,
   BR-02, …`. Priority is **MoSCoW** (Must/Should/Could/Won't). One
   requirement per row, business-level ("What"), not technical spec
   ("How"). Each row should reference an `OBJ-xx`.
6. **Quy tắc nghiệp vụ (Business Rules)** — [BẮT BUỘC] — table `Mã | Nội
   dung quy tắc | Nguồn/căn cứ`, IDs `RULE-01, RULE-02, …`. Constraints,
   conditions, formulas, thresholds, compliance logic — business-level,
   clear enough for BA to turn into system logic.
7. **Trường hợp sử dụng (Use Cases)** — [KHUYẾN NGHỊ] — repeat this block
   per use case: `Mã Use Case (UC-01) | Tên | Đối tượng/Actor (ACT-0x) |
   Mục tiêu | Luồng chính | Luồng thay thế | Tham chiếu yêu cầu (BR-0x,
   RULE-0x)`.
8. **Điều kiện đầu vào/đầu ra** — [KHUYẾN NGHỊ] — table `Điều kiện đầu vào
   (Pre-conditions) | Điều kiện đầu ra (Post-conditions)`.
9. **Trường hợp ngoại lệ nghiệp vụ** — [KHUYẾN NGHỊ] — table `Mã | Tình
   huống ngoại lệ | Cách xử lý nghiệp vụ kỳ vọng`, IDs `EX-01, EX-02, …`.
10. **Tiêu chí nghiệm thu nghiệp vụ** — [BẮT BUỘC] — table `Mã | Tiêu chí
    nghiệm thu (đo lường được) | Tham chiếu (BR/OBJ)`, IDs `AC-01, AC-02,
    …`. This is PTSP's basis for accepting the product (business-level
    UAT) — criteria must be measurable and reference a `BR-xx`/`OBJ-xx`.
11. **Yêu cầu phi chức năng (mức mục tiêu)** — table `Nhóm | Mục tiêu định
    hướng`, fixed rows: Hiệu năng (Performance), Bảo mật & tuân thủ
    (Security & compliance), Tính sẵn sàng (Availability), Khả năng mở
    rộng (Scalability), Audit/Logging. BRD states directional targets
    only — IT quantifies precisely in the SRS.
12. **Giả định, ràng buộc & phụ thuộc**
    - 12.1 Giả định (Assumptions).
    - 12.2 Ràng buộc (Constraints) — e.g. packaged-CORE system limits,
      budget, timeline, legal/regulatory constraints.
    - 12.3 Phụ thuộc (Dependencies) — systems/units/partners the product
      depends on.
13. **Phụ lục – Thuật ngữ & viết tắt** (glossary) — table `Thuật ngữ/viết
    tắt | Diễn giải`. Template pre-fills `BRD` and `SRS`; append
    project-specific terms, don't remove the pre-filled rows.

### Traceability ID scheme (don't break this — it's the template's whole point)

`OBJ-xx` (objectives) ← referenced by `BR-xx` (business requirements) →
referenced by `UC-xx` (use cases) and `RULE-xx` (business rules) →
referenced by `AC-xx` (acceptance criteria). `ACT-xx` (actors) is
referenced by the Actors table and by each use case's Actor field. Keep
IDs sequential and never reuse/renumber an ID once other sections
reference it.

## Generation workflow

1. Read the template (`mammoth` or the raw XML) if you need to confirm
   current structure — this SKILL.md should already match it, but the
   template file is the source of truth if they ever diverge.
2. Gather actual content from the user for every **[BẮT BUỘC]** section at
   minimum — business problem, objectives/KPIs, scope in/out, actors,
   business process, requirements, rules, and acceptance criteria. Never
   invent business content (a fabricated KPI or acceptance criterion is
   worse than an empty one) — if the user hasn't given you something,
   leave the section as "Không áp dụng — <ask user>" rather than guessing,
   and flag it back to them.
3. Assign IDs sequentially per the coding scheme above as content is
   filled in, keeping cross-references (`Tham chiếu mục tiêu`, `Tham chiếu
   yêu cầu`, `Tham chiếu (BR/OBJ)`) consistent.
4. Copy `../sbsi-template-router/templates/brd/BRD_Template.docx` to a
   scratch working file first — never open/edit the template path itself.
5. Generate via the chosen path — default is the direct XML DOM edit on
   the copy (option 1 above); see `office-file-generation` skill's
   "Word — filling an existing template without pre-tagging" section for
   the full technique (helper functions, guidance-paragraph deletion,
   row/block cloning, the header-row off-by-one gotcha, validation steps).
6. Write output to a new file, never overwrite `BRD_Template.docx` or the
   scratch copy in place — e.g. `<product-code>-brd.docx` in the location
   the user specifies.
7. Run `sbsi-docx-format-core`'s validator with BRD's own manifest before
   handing off — `python3 validate_sbsi_docx.py --doc <output.docx>
   --template ../sbsi-template-router/templates/brd/BRD_Template.docx
   --manifest ../sbsi-template-router/templates/brd/template_manifest.json`
   — any new `ERROR:` beyond the known pre-existing typography drift noted
   above is your content edit's own regression, fix it before delivering.
8. Also validate before handing off: `unzip -t` for zip integrity, then dump
   the **full** document text with `mammoth` and read it end to end,
   checking every table's rows land under the right headers/labels (the
   header-row skip is easy to get wrong and silently shifts a whole
   table by one row). Grep for any remaining `‹...›` placeholders and
   report genuinely-unresolved ones back to the user rather than
   inventing values.
9. Note to the user: the template's "Mục lục" (table of contents) is a
   Word TOC field — remind them to update fields (Word: right-click → Update
   Field, or Update Table) after opening the generated file, since
   generated page numbers/section listing won't be live until Word
   recalculates it.

## Load this skill when

- Asked to write, draft, generate, or fill in a BRD for SBSI.
- Asked what sections/fields a BRD needs.

## Skip when

- The task is about a different document type (SRS, PRD, etc.) — this
  skill only covers the SBSI BRD template specifically.
