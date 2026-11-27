---
name: official-document-verification
description: >-
  Verify the exact wording of a bill, statute, audit report or regulator notice against the
  authoritative edition. When a disputed clause was added, removed or renumbered, pin the print,
  search section and subject, and separate publication status from text. Not for ghc-search.
metadata:
  revision: "6"
  areas: "work-management"
  targets: "runtime-agnostic"
  summary: "verify a claim against the exact print of the document, including artifacts a plain client cannot fetch"
  summary_zh: "用文档的确切版本核验结论，含只能用真浏览器取到的被封来源"
  kind: "entry"
---

# Official document verification

Use when a load-bearing claim rests on a bill, a statute, an audit report, a regulator's page, or any
artifact whose exact version and exact wording decide the conclusion. If a plain HTTP client cannot
reach it, use the access checks in section 3.

Companion skills: `evidence-backed-analytical-writing`
(claim hygiene and report structure), `hermes-ops-claim-verification` (cron results and "fixed" claims). This
skill covers what those do not: getting the right version, proving what it does and does not say, and
proposing a change instead of making one.

## 1. Pin the version before reading a single line

- Bills and statutes exist as several distinct prints: introduced → reported (RS) → engrossed (EH) →
  enrolled → public law. "The bill" is not a version. Every absence claim is scoped to the print actually
  fetched, so name it (chamber, print, size, line count) in the note that carries the claim.
- Keep status facts and text facts on separate records: the publisher's action history answers "has it
  moved", the fetched text answers "what does it say". A quiet action history does not constrain a future
  text, and text content does not establish procedural status.
- Report each finding per version. A provision present in the House print and absent from the Senate print
  is a single-chamber proposal — write that, not "proposed", which invites the reader to assume both.

## 2. Scan by number *and* by content

- Search section numbers and the citation of the older law, then open every hit and read its heading.
  Section numbers repeat across titles: a hit on `Sec. 904` may be an unrelated provision in another title
  while the section in question sits elsewhere. A number-only match publishes a false finding.
- Follow with a content scan for the named things — frozen capability lists, program elements, defined
  terms. Zero hits for those names across the whole text is the strongest negative available.
- State the negative as bounded: "in the fetched EH/RS text", never "in the bill", and never as a
  procedural forecast. "No renewal clause in either chamber's text" is a finding; "renewal can only come
  through conference" is a prediction the text does not contain.
- `scripts/scan_bill_text.py` performs this pass (section hits, citation windows, keyword counts) on a
  downloaded HTML or text file; run it before writing any absence claim.

## 3. Getting an artifact a plain client cannot fetch

- A 403 to `curl` is a statement about your client or the edge protection, not about the document. Load
  the URL in a real browser before concluding the source is gone, empty, or unpublishable.
- When the numbers live in a chart or an embedded image, read the rendered figure: screenshot the element
  and read it as an image, then record that you read a figure and not the report's table.
- **Check a chart reading by internal arithmetic.** Sum the component bars and compare with the total the
  figure prints. Disagreement means your transcription is wrong, not the source — re-read before quoting.
- Keep a per-figure status in the evidence note: figure readable / table unreadable = *partially blocked*.
  A legible chart never licenses citing the body text or the data table.
- When every path on a domain returns the same block page, that is an unresolved item. Split the question
  and record each part separately: listing/index state, access control on a gated list, availability of
  the original file elsewhere or in a mirror, and whether the document was submitted or is publishable.
  One unreachable index answers none of them, and "channel closed" is not a finding about a blocked page.

## 4. Caliber ladder for counts

`authorized` → `actual/staffed` → `filled/hired`; positions are not people, and neither is money. Name the
caliber in the same sentence as the number. When sources give different baselines, list them side by side
with their enumerators instead of reconciling: the disagreement is usually itself the finding, and a
single reconciled number launders it away.

## 5. Propose the change, do not make it

When a page has a reviewer or another writer, a draft edit is not a proposal — it is an unauthorized
landing. Prepare it outside the tree:

1. Copy the target into scratch; apply edits with an assertion that each anchor string occurs exactly once,
   so a silent no-op or a double replacement fails loudly instead of shipping.
2. Emit `diff -u --label a/<repo-path> --label b/<repo-path> <original> <candidate>` so the reviewer can
   apply it verbatim.
3. Validate before sending: frontmatter parses, headings and links intact, and `git status --porcelain`
   empty as proof the real tree was untouched.
4. In the covering note, say what each hunk **replaces** and what it **preserves**, so acceptance can
   happen at hunk granularity.

On a dated page, annotate rather than rewrite: keep the historical sentence and its date, attach a dated
correction marker, and state what the new evidence can and cannot compare with the old figure.

## Pitfalls

- Treating one print's silence as the measure's silence, then reporting it as "not in the bill".
- Matching a section number without reading its heading; the number repeats across titles.
- Escalating a bounded negative into a procedural conclusion about what later stages can or must do.
- Declaring a source unavailable because a plain fetch was blocked, when a browser renders it fine.
- Quoting a chart total without summing its components; the transcription error becomes a cited fact.
- Letting a readable figure stand in for the table or body text it does not contain.
- Reconciling two staffing or budget baselines into one number instead of naming both calibers.
- Editing a shared page to demonstrate a proposal, which converts review into an accident.
