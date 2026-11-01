---
name: spec-review
description: "This skill should be used when the user shares a project specification — full spec book, individual CSI MasterFormat sections, or specs paired with drawings — and wants it audited for division completeness, drawing-spec coordination, prescriptive vs performance balance, basis-of-design products, reference-standard currency, AHJ amendments, section-internal completeness, and OPR alignment. Trigger on 'spec review', 'spec audit', 'CSI review', 'check this spec section', 'are the specs and drawings coordinated', 'reference standards', 'basis of design', 'or equal language', or pasted spec content with completeness intent. Generates a structured review markdown in `docs/spec-reviews/` and appends to the project spec-review index."
license: MIT
metadata:
  title: "Spec Review"
  summary: "Audit a spec book for gaps and drawing coordination"
  discipline: "construction-admin"
  tags: "Design"
---

# Spec Review


## Overview


Audit a project specification against eight axes — division completeness, drawing-spec coordination, prescriptive vs performance, basis-of-design products, reference-standard currency, AHJ-specific references, section-internal completeness (Part 1/2/3), and OPR alignment — and produce a written review that lives in `docs/spec-reviews/`.


Aligned with NA practice: CSI MasterFormat 2020, CSI SectionFormat / PageFormat, AIA MasterSpec or ARCAT-derived specs, the ConsensusDOCS spec norms in design-build, and the typical owner-architect agreement (AIA B101 §3.4.5) that defines the architect's specification responsibility.


This skill is the paired counterpart to `brief-review` (front-end) and `submittal-review` (back-end). It runs in late DD / early CD when the spec book is starting to firm up, and again at 95% CD before issue-for-permit.


## Scope and limits — read first


**What this does.** Audits the specification you supply against eight axes and
writes findings to `docs/spec-reviews/`, each naming the section, the part, and
the paragraph it lives in. A coordination finding names both ends, the sheet and
the section, so one pass closes both.

**What this does not do.**

- **It does not know which edition of a standard your code adopts.** It flags a
  reference cited without a year, and the year that belongs there comes from the
  code edition in force on your project.
  `references/csi_masterformat_2020_index.md` carries division and section
  titles only, and CSI's own publication governs where the two disagree.
- **It does not write or rewrite the spec.** It reports defects; the spec writer
  fixes them.
- It does not open the drawings. Coordination is checked against the references
  you supply, and confirming that sheet A-501 detail 3 exists is your pass.
- It does not judge whether a specified product is the right product. It checks
  that the section says what a section has to say.
- It does not review submittals, bids, or the drawing set. Those are
  `submittal-review`, `bid-review`, and `drawing-checklist`.

**What you need before starting.** The sections as text or files, the phase they
are at, the master they came from, the jurisdiction and code edition, and the
drawings or schedules you want them coordinated against.

## When to use


Trigger on:

- Pasted spec sections (typed from the spec book or pulled from Word / InDesign / Acrobat).
- Project file paths to a spec book or section folder.
- Explicit asks: "spec review", "spec audit", "are the specs coordinated", "is this spec complete", "check Section 07 27 26 for completeness", "are the reference standards current".
- Hand-off from `brief-review` when the OPR sets performance criteria that need to land in the spec.

Do NOT trigger for:

- Drawing-set review without specs (use `drawing-checklist`).
- Brief / OPR review (use `brief-review`).
- Submittal review against an issued spec (use `submittal-review`).
- Bid review of contractor pricing against the spec (use `bid-review`).

## Workflow


### Step 1 — Bootstrap if needed


Check that `docs/spec-reviews/index.md` exists. If not:


```bash
python scripts/init_spec_review_workspace.py
```


### Step 2 — Anchor the spec basis


Spec review is meaningless without the contract basis. Pin these before applying axes.

- Read `docs/project.md` if it exists for project number, delivery method, jurisdiction (drives AHJ-required references), code edition (drives reference-standard year), and OPR / brief.
- Identify the spec system: AIA MasterSpec / SpecLink / ARCAT-derived / office-master / ConsensusDOCS / agency-master (e.g., GSA P-100, USACE UFGS, CA OSHPD/HCAI, NYC SCA). Different systems have different default reference editions and AHJ language.
- Note the spec phase: DD outline spec, 50% CD spec, 95% CD spec, issue-for-permit. Findings differ by phase — division gaps are normal at DD, fatal at 95%.
- Pull MasterFormat division titles from `references/csi_masterformat_2020_index.md` for completeness checking.

### Step 3 — Apply eight-axis review


Load `references/spec_axes.md` for the full framework with sub-criteria. Quick reference:

1. **Division completeness** — Required Divisions present for the project's scope? Common gaps: Division 02 (Existing Conditions) on renovations, Division 13 (Special Construction) on labs/medical, Division 25 (Integrated Automation) on smart buildings, Division 31-33 (Earthwork / Exterior Improvements / Utilities) on ground-up. Section-numbering conventions follow MasterFormat 2020.
2. **Drawing-spec coordination** — Cross-references in both directions match: spec section refs on drawings (e.g., "see 08 41 13") resolve to actual sections, and sheet/detail refs in specs resolve to actual drawings. Material call-outs on plans match products in spec basis-of-design. Schedules (door, window, finish, hardware) resolve to specs.
3. **Prescriptive vs performance balance** — Each section uses prescriptive (named product / dimension / installation method) where the owner has a defined preference, and performance (test result / criterion / industry standard) where multiple products may comply. Mixed within a section is fine; contradictory within a section is a defect ("provide GIb gypsum board, ½" thick, by USG; or any equal product with X performance" — the "or equal" defeats the named product).
4. **Basis-of-design & "or equal"** — Named manufacturers list 2-3 acceptable equals or a clear "approved equal" mechanism per Section 01 25 00 (or Section 01 60 00 in some masters). "Sole-source" specifications justified per the AHJ's procurement law (typically a memo on file for public projects).
5. **Reference-standard currency** — ASTM, ANSI, UL, NFPA, ASHRAE, AISC, ACI, ASCE, ICC standards cited with edition year (e.g., "ASTM C1396-17"), and the user confirms the cited edition is the one their code adopts. Generic "ASTM C1396" without year is a defect — different editions of the same standard test differently.
6. **AHJ-specific references** — Local amendments cited (e.g., "per CBC 2022 §1505 and CRC §R902 for fire-rated roof assemblies in WUI areas"), AHJ-required certifications named (NYC DOB MEA, FDNY COA, CA OSHPD/HCAI OSP, USACE UFGS section overlays). Federal projects (GSA, USACE, VA, DoD) have their own master spec systems that override commercial defaults — flag if commercial language is left in.
7. **Section-internal completeness (Part 1/2/3)** — Per CSI SectionFormat: Part 1 (General — references, submittals, quality assurance, delivery/storage, warranty), Part 2 (Products — manufacturers, materials, fabrication, finishes, mixes, source quality control), Part 3 (Execution — examination, preparation, installation, field quality control, cleaning, protection). Each section has all three Parts populated for actual scope; placeholder language ("TBD", "to be determined") flagged.
8. **OPR alignment** — Performance criteria from the OPR (energy target, certification, acoustic, IAQ, embodied carbon) actually land in the appropriate spec sections? Common gap: OPR commits to LEED Gold but Division 01 quality assurance section says nothing about LEED documentation, commissioning, or LEED-specific submittals.

Focus on the 3-5 axes with real signal. A 50% CD review reads heavily on axes 1, 2, 8. A 95% CD review reads heavily on 3, 4, 5, 7. A federal project review reads heavily on 6 first.


### Step 4 — Write the review


Read `assets/spec-review-template.md`, fill placeholders. Filename:


`docs/spec-reviews/<YYYY-MM-DD>-<slug>.md`


Slug rule: lowercase, `[^a-z0-9-]` removed, max 40 chars, derived from project + spec phase or division focus (`acme-hq-95cd`, `school-div-08-fenestration`). If a review with the same date+slug already exists, suffix `-<n>`.


### Step 5 — Update the spec-review index


```bash
python scripts/append_to_index.py \
  --date 2026-05-09 \
  --slug acme-hq-95cd \
  --spec-phase "95% CD" \
  --primary-axes "drawing-coordination,reference-standards,opr-alignment" \
  --findings-high 4
```


The script appends a row to `docs/spec-reviews/index.md`. Do NOT edit the index manually with the Edit tool.


### Step 6 — Report


Tell the user:

- Path to the review file.
- The 2-3 highest-severity findings and the spec sections they live in.
- Drawing-spec coordination defects that need both a spec edit and a drawing edit (these are the change-order-prone ones).
- Whether a follow-up `bid-review` should pre-load for the divisions where prescriptive language drives bid risk.

## Rules

- Every finding names the spec section number and the specific Part / paragraph / line where the issue lives ("Section 09 51 13, Part 2.2.A.3 cites 'ASTM C635' without edition year"). "Specs are unclear" is not a finding.
- Reference-standard year cited explicitly in every finding that touches a standard. Standards revise on 5- to 10-year cycles; "ASTM E84" is not specific.
- Drawing-spec coordination findings cite both the drawing reference (sheet number, detail number) and the spec section, so the design team can fix both ends in one edit.
- Distinguish defects of completeness (missing) from defects of coordination (present but contradicts something) from defects of currency (present and consistent but using outdated standard). Different fixes.
- Federal / agency projects: name the controlling spec system (UFGS for USACE, P-100 for GSA, OSP for CA HCAI, SCA spec for NYC SCA). Defaults from commercial masters that conflict with the agency master are findings.
- "Or equal" language: every named product needs an "or equal" clause unless the spec is sole-source and justified. Public-sector procurement law typically requires the equal mechanism.

## Anti-patterns

- Generic findings ("specs need coordination", "reference standards out of date") without section / paragraph / standard year. Useless to the spec writer.
- Reviewing every Division when the project doesn't include 03, 04, 13, or 25. Adjust completeness scope to actual project.
- Confusing CSI SectionFormat with MasterFormat. SectionFormat is Part 1 / 2 / 3 within a section; MasterFormat is the section-numbering taxonomy across the spec book.
- Over-applying federal / agency master language on commercial projects. UFGS clauses in a private spec are a defect, not a feature.
- Treating an outline spec at DD as a final spec at 95% CD. Phase-appropriate findings.
- Editing `index.md` manually instead of using `append_to_index.py`.

## Resources

- `scripts/init_spec_review_workspace.py` — bootstrap `docs/spec-reviews/` and the spec-review index
- `scripts/append_to_index.py` — append a row to `docs/spec-reviews/index.md`
- `references/spec_axes.md` — eight-axis framework with sub-criteria, common failure modes, example findings tied to typical NA spec sections (concrete, fenestration, finishes, MEP, Division 01)
- `references/csi_masterformat_2020_index.md` — Division and major-section titles per MasterFormat 2020, for completeness checking
- `assets/spec-review-template.md` — review markdown template with finding-by-section block
