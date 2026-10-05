---
name: thebrain-bird-address
description: "Use BIRD Book Deconstructor 2.2 to apply the formal BIRD 2.1 Knowledge Address protocol to complex manuscript text and TheBrain Thoughts. Use when splitting books into chapter/section/item knowledge nodes, assigning Book Address, structured Knowledge Index (Weight, Type, Keyword, Alias), Routes, verified Deep Links, and Semantic Roles; producing BIRD Excel workbooks, TheBrain scaffolds, Roam JSON, monochrome printable double nine-grid cards, or a routed handoff from iMandalArt to A4 eight-page booklets; or auditing and migrating existing BIRD/TheBrain indexes."
---

# BIRD Book Deconstructor 2.2

Convert complex structural text into addressable, searchable, cross-linked book nodes for TheBrain, Excel, Roam Research, Obsidian, and AI Agents.

Version 2.2 is the Skill integration release. Canonical interchange objects remain `BIRD-2.1` for backward compatibility.

## Three Kings 2.2 Integration

BIRD is the **address and route king** in the three-skill publishing chain:

`iMandalArt 2.2 eight angles -> BIRD 2.2 Book Address + Index + Route + Deep Link -> A4 Booklet 2.2`

- Receive the center, eight angles, source identities, and spatial order from iMandalArt.
- Turn reusable claims into stable Book Addresses and `W + T + K + A` Knowledge Indexes.
- Send seven ordered Routes, citations, pending Deep Links, and merge reasons to the booklet manifest.

## Formal Protocol

- `B = Book Address`: stable book/project hierarchy address; answer "where in the book?"
- `I = Knowledge Index`: structured index object `W + T + K + A`; answer "what knowledge object?"
- `R = Route`: ordered cross-node or cross-chapter paths; answer "where does it lead?"
- `D = Deep Link`: exact permanent application address; answer "how is it opened?"

Read [`references/bird-2.1-spec.md`](references/bird-2.1-spec.md) before assigning Index Weight, Index Type, or Semantic Role.

Do not use the old `B = Branch` or unstructured `I = title` interpretation. Mark legacy input as `BIRD 1.x` and map it into 2.1. Preserve valid BIRD 2.0 fields during migration; add `Role` only when evidence supports it.

## Distinguish Two Types

- `StructuralType`: book function, such as `部 / 章 / 節 / 項`.
- `IndexType`: knowledge kind inside `I`, using `C / M / P / B / T / O / E / L / S / A / X`.

Never put `章` into `IndexType`, or `Concept` into `StructuralType`.

## Choose the Mode

- **Single Node**: analyze one existing Thought and output one BIRD object.
- **Deconstruct Text**: split complex prose into chapter, section, and atomic item nodes.
- **Excel Workbook**: create a validated `.xlsx` with BIRD analysis, manuscript Notes, and code tables.
- **TheBrain Scaffold**: turn the validated Excel hierarchy into empty or selectively populated Thoughts with structural Types and workflow Tags.
- **Roam JSON Export**: convert canonical BIRD objects or flat `BIRD分析` rows into a Roam-importable page/block array.
- **Monochrome Double Nine-Grid**: compose one A4 landscape printable visual with the main table of contents and three Routes on the left, and the Knowledge Index on the right.
- **Audit/Migrate**: check or convert existing TheBrain or legacy Excel rows.

## Deconstruct Text

1. Identify book, part, chapter, section, existing numbering, central question, and argument order.
2. Preserve existing addresses. Use `待編` only when no reliable address exists; do not silently renumber.
3. Treat `章` and `節` as structural containers. Treat `項` as the normal manuscript unit: one claim, explanation, evidence/example, and transition.
4. Split when the claim, reader question, independent case, definition, or reusable reasoning step changes. Do not split mechanically by paragraphs.
5. Target 700-1000 Chinese characters per standard item Note; allow 300-600 for bridges/definitions and up to 1200 for an indivisible case.
6. Build one BIRD object per item:
   - assign one `B`;
   - assign one `I.W`, one `I.T`, one canonical `I.K`, and zero or more deduplicated `I.A`;
   - assign two to five meaningful `R` targets when supported;
   - preserve verified `D` byte-for-byte or leave it blank/pending for proposed nodes.
7. Preserve the author's stance, metaphors, examples, and evidence. Mark missing material `待補`; never fabricate support.
8. Return a structure tree, BIRD table, JSON objects, and item Note drafts unless the user requests only one format.

Read [`references/manuscript-structuring.md`](references/manuscript-structuring.md) for segmentation and output templates.

## Assign the Index

For every node, apply this order:

1. Choose `K`: one canonical retrieval term, 4-10 Chinese characters or 2-4 English words.
2. Choose `T`: one code from the controlled Index Type table.
3. Choose `W`: importance to this specific book, not general fame.
4. Add `A`: genuine synonyms, translations, abbreviations, or established alternate spellings. Exclude the canonical keyword itself.
5. Assign the optional BIRD 2.1 `Role` only when graph or hierarchy evidence supports it; otherwise leave blank.

Do not turn every noun into an Index. Create an index object only when the term supports retrieval, interpretation, or routing.

## Build Routes

- Use `B` for the table-of-contents location and `R` for meaningful cross-links.
- Prefer ordered routes such as `FIRE -> 語意索引 -> AI對話`.
- Store Route targets as existing Thought names, Book Addresses, or verified Deep Links.
- Exclude self-links, direct hierarchy repetitions, and nearby siblings without a semantic reason.
- Mark a proposed target `待建` rather than inventing its address.

## Preserve Deep Links

Copy each supplied `D` exactly from `brain://` through the final character. Never decode, encode, normalize, shorten, repair, rename, or regenerate its slug. For a proposed Thought, use a blank cell in Excel and `待建立 Thought 後貼入` in prose.

Before returning, compare every displayed `D` with its source string. Do not claim tool verification unless a tool returned that exact value in the current run.

## Create the Excel Workbook

Read [`references/excel-schema.md`](references/excel-schema.md). Create these sheets:

1. `BIRD分析`: one row per knowledge node with normalized BIRD fields.
2. `拆書正文`: one row per item with Note text and BIRD JSON.
3. `代碼表`: Weight, Index Type, Semantic Role, StructuralType, and Tag dictionaries.

Use a real spreadsheet library. Freeze headers, enable filters, wrap long text, set practical widths, and validate the workbook after saving. Preserve legacy columns only in a separate `舊表對照` sheet when migration is requested.

## Export Roam Research JSON

Read [`references/roam-json-import.md`](references/roam-json-import.md), then use the deterministic converter:

```bash
node scripts/bird_to_roam_json.mjs bird.json roam-import.json
```

- Accept one canonical BIRD object, an array, or an object containing `items`, `records`, or flat Excel `rows`.
- Emit an array of Roam pages using only supported page/block keys.
- Omit block `uid` by default; add UIDs only when preserving existing block references is explicitly required and collision risk has been audited.
- Stop on duplicate generated page titles. Roam merges matching titles, so silent duplicates can add content to the wrong page.
- Preserve `D_DeepLink` byte-for-byte inside the `D::` block.
- Validate the final JSON before delivery and recommend importing into a test graph first.

## Create a Monochrome Double Nine-Grid

Read [`references/black-white-double-nine-grid.md`](references/black-white-double-nine-grid.md) whenever the user asks for a double nine-grid, print card, printable image, or left-directory/right-keyword visual.

- Use one A4 landscape page with two aligned 3×3 grids.
- Put five main contents, three meaningful Routes, and the core BIRD object in the left grid.
- Put eight Knowledge Index objects around the core Index in the right grid.
- Use a pure white background and black text/lines only. Do not use cell fills, gray backgrounds, gradients, shadows, or decorative color.
- Deliver editable SVG plus a 3508×2480 PNG. Also deliver a verified one-page A4 landscape PDF when print output is requested.
- Keep every displayed BIRD field faithful to the canonical objects. Do not invent Book Addresses or Deep Links to fill the layout.

## Audit Rules

Report the smallest correction for:

- duplicate or missing Book Address;
- invalid Weight or Index Type code;
- empty canonical Keyword;
- Alias duplicating Keyword or another Alias;
- unsupported Semantic Role;
- Route self-link or hierarchy-only repetition;
- missing or transformed Deep Link;
- `StructuralType` and address-depth conflict;
- multiple primary workflow Tags.

Do not move, rename, merge, or delete live Thoughts without explicit authorization.

## Standard BIRD Output

```text
【BIRD 2.1】
B: 全系統/第三部/3.4/3.4.D/3.4.D.B
I:
  W: I3
  T: S | Skill
  K: 八領域週檢視
  A: Weekly Review to 8 Rocks | 八岩週檢視
R: 週檢視 -> 八領域週檢視 -> 週計劃
D: brain://... or 待建立 Thought 後貼入
StructuralType: 項
Tag: 草稿
Role:
```

For Agent interchange, also output:

```json
{
  "version": "BIRD-2.1",
  "bookAddress": "全系統/第三部/3.4/3.4.D/3.4.D.B",
  "index": {
    "weight": "I3",
    "typeCode": "S",
    "type": "Skill",
    "keyword": "八領域週檢視",
    "aliases": ["Weekly Review to 8 Rocks", "八岩週檢視"]
  },
  "route": ["週檢視", "週計劃"],
  "deepLink": "brain://...",
  "structuralType": "項",
  "tag": "草稿",
  "semanticRole": null
}
```

## TheBrain Instructions

- For one current Thought, return [`references/thebrain-instruction.md`](references/thebrain-instruction.md).
- For chapter/section text deconstruction, return [`references/thebrain-manuscript-instruction.md`](references/thebrain-manuscript-instruction.md).
- For bulk Excel-to-TheBrain scaffolds, read [`references/thebrain-scaffold-import.md`](references/thebrain-scaffold-import.md) before creating any Thought, Type, Tag, or Link.
