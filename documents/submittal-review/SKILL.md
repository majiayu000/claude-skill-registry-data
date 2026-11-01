---
name: submittal-review
description: "This skill should be used during construction administration when the user shares a contractor submittal — shop drawings, product data, samples, or mockup documentation — and wants it reviewed for conformance with the contract documents. Trigger on 'review this submittal', 'shop drawing review', 'check this product data', 'submittal log', 'is this approved', 'spec compliance check', 'AIA G712', or pasted submittal content paired with CA-phase context. Generates a structured submittal-review markdown in `docs/submittals/` and appends to the project submittal log."
license: MIT
metadata:
  title: "Submittal Review"
  summary: "Review a shop drawing or product data against the documents"
  discipline: "construction-admin"
  tags: "Construction"
---

# Submittal Review


## Overview


Review contractor submittals (shop drawings, product data, samples, mockups, schedules) against the contract documents in the construction administration phase, and produce a written review that lives in `docs/submittals/`. The output mirrors the AIA G712 submittal log and assigns one of the standard CA-phase action stamps.


Aligned with NA practice: AIA A201-2017 §3.12 (Submittals), AIA G712 (Shop Drawing & Sample Record), CSI MasterFormat 2020 / SectionFormat / PageFormat, and the typical owner-architect agreement (B101 §3.6.4) defining the architect's review responsibility.


This skill is for the architect / EOR / owner's rep position. The review documents what changed between the contract documents and the contractor-proposed product or fabrication, flags deviations, and recommends an action stamp.


## Scope and limits — read first


**What this does.** Compares one submittal against the contract documents you
supply, across eight axes, and writes a review to `docs/submittals/` with a
recommended action stamp and the reasons behind it. Every deviation names where
the documents require one thing and where the submittal shows another.

**What this does not do.**

- **It does not stamp anything.** The stamp is a recommendation. The architect
  or engineer of record signs, and that signature is what carries the
  responsibility under the agreement.
- **It does not know what your specification requires.** The section, the
  basis-of-design product, the substitution clause, and the list of required
  submittals all come from your documents. Without them there is nothing to
  review against, and the run says so instead of reviewing against a typical
  section.
- It does not verify that a test report, listing, or certification is genuine or
  still current. It checks that one is present and records its date for you to
  confirm.
- It does not verify field dimensions. Those sit with the contractor under the
  general conditions, and a submittal deferring a dimension critical to adjacent
  work is flagged rather than accepted.
- It does not select products, review the original spec, or review the drawings.
  Those are `spec-review` and `drawing-checklist`.

**What you need before starting.** The submittal, the spec section it answers
to, the drawing details it touches, and the prior review if this is a
resubmittal. A resubmittal read without the previous comments is how a C-stamp
quietly turns into a B.

## When to use


Trigger on:

- Pasted submittal cover sheet, product data, or shop drawing details with a request to review.
- Project file paths to a submittal package.
- Explicit asks: "review this submittal", "shop drawing review", "check this product data", "is this approved", "what's the status code on this".
- A submittal log entry needing analysis before stamp.

Do NOT trigger for:

- Original contract drawing review (use `drawing-checklist`).
- Original spec section review (use `spec-review`).
- Bid-stage product evaluation (use `bid-review`).
- Generic product research (this skill reviews against an existing contract — it does not pick products from scratch).

## Workflow


### Step 1 — Bootstrap if needed


Check that `docs/submittals/index.md` exists. If not:


```bash
python scripts/init_submittals_workspace.py
```


### Step 2 — Anchor the contract basis


A submittal is meaningless without the contract document it is being reviewed against. Pin these before applying axes.

- Read `docs/project.md` if it exists for project number, current spec edition, and CA-phase status.
- Identify the spec section number (CSI MasterFormat, e.g., 08 41 13 — Aluminum-Framed Entrances and Storefronts) and the relevant drawing details.
- Note the basis-of-design product named in the spec, the "or equal" language, and any owner-prior-approval list.
- Note prior submittals on the same section: is this the original (Rev 0), a resubmittal after C-stamp (Rev 1+), or an as-built record submittal post-installation?
- For shop drawings, confirm the field-verified dimensions are noted as such — the contractor is responsible for them per A201 §3.12.7.

### Step 3 — Apply eight-axis review


Load `references/submittal_axes.md` for the full framework with sub-criteria. Quick reference:

1. **Contract-document conformance** — Does the submitted product/fabrication match what is shown and specified? Flag every deviation, even apparently minor ones.
2. **Completeness against spec submittal article** — Most spec sections (Part 1.04 or 1.05) list required submittals: shop drawings, product data, samples, certifications, warranties, mock-up requirements. Confirm each item is present or note what is missing.
3. **Dimensions & coordination** — Field-verified dimensions stated? Clearances to adjacent work (structural, MEP, FF&E) shown? Connections to backing / blocking / structure detailed?
4. **Performance & product data** — Stated performance (U-factor, STC, fire rating, slip resistance, color fastness) matches the spec basis-of-design or exceeds it? Test reports referenced (ASTM, ANSI, NFPA, UL) with current dates?
5. **Fabrication feasibility & lead time** — Lead time stated and compatible with construction schedule? Fabrication tolerance vs. the contract document tolerance? Long-lead components called out?
6. **Code & certification compliance** — UL listings, ICC-ES evaluation reports, NFPA test reports, IECC envelope criteria, ADA / ANSI A117.1 dimensions, AHJ-required certifications attached and in-date?
7. **Deviations, substitutions & "or equal" claims** — Substitutions explicitly flagged with side-by-side comparison vs. basis-of-design? Per A201 §3.4.2, the contractor warrants equivalent products only when so represented. Hidden substitutions are a frequent source of disputes.
8. **Owner-furnished, contractor-installed (OFCI) coordination** — Items the owner is furnishing (FF&E, AV, signage, art, lab/medical equipment) coordinated with this submittal? Power/data/structural backing accommodated?

Focus on the 3-5 axes with real signal for this submittal. A storefront submittal triggers axes 1, 3, 4, 6 hard; a paint product data sheet triggers 2, 4, 6 lightly. Do not pretend to find issues that aren't there.


### Step 4 — Recommend an action stamp


AIA G712-style action stamps (terminology may vary by office; document the office convention if different):

- **A — No exceptions taken / Approved** — Submittal conforms; work may proceed.
- **B — Make corrections noted / Approved as noted** — Conforms with minor markups; work may proceed if corrections are incorporated. No resubmittal required.
- **C — Revise & resubmit** — Substantial nonconformance; resubmit before fabrication.
- **D — Rejected** — Does not comply or is fundamentally wrong scope; resubmit a different product / fabrication.
- **E — Reviewed for record only** — Information-only submittal (e.g., maintenance manual at closeout). No action stamp drives fabrication.

The recommended stamp is informed by axes 1 (conformance), 7 (deviations), and any axis where a "below code" finding appears.


### Step 5 — Write the review


Read `assets/submittal-review-template.md`, fill placeholders. Filename:


`docs/submittals/<YYYY-MM-DD>-<spec-section>-<slug>.md`


Slug rule: lowercase, `[^a-z0-9-]` removed, max 40 chars, derived from product type + revision (`storefront-rev0`, `roof-membrane-rev1`). Spec section uses dot-stripped MasterFormat (`08-41-13`). If a review with the same date+section+slug already exists, suffix `-<n>`.


### Step 6 — Update the submittal log


```bash
python scripts/append_to_index.py \
  --date 2026-05-09 \
  --spec-section "08 41 13" \
  --slug storefront-rev0 \
  --revision 0 \
  --action-stamp B \
  --primary-axes "conformance,performance,deviations"
```


The script appends a row to `docs/submittals/index.md`. Do NOT edit the index manually with the Edit tool.


### Step 7 — Report


Tell the user:

- Path to the review file.
- The recommended action stamp and the 1-2 most-load-bearing reasons.
- Any follow-up RFI questions the submittal raises.
- If the submittal hides a substitution, flag it explicitly and recommend the contractor refile per A201 §3.4.2.

## Rules

- Every deviation cites WHERE the contract requires X and WHY the submittal is showing Y. "This doesn't match the drawings" without a sheet/detail reference is not a finding.
- Distinguish minor markup (B-stamp) from substantive nonconformance (C-stamp). The threshold is whether fabrication can proceed safely with the markup.
- Substitutions: if the submittal lists a product different from the basis-of-design without a substitution form, this is a hidden substitution. Flag it and route through the formal substitution process — never quietly approve.
- For samples and mockups, the review is qualitative (color, finish, joinery) — but the standard for approval is what the spec set as the standard, not personal taste.
- "Or equal" claims are the contractor's warranty, not the architect's. Per A201 §3.4.2, the contractor warrants equivalence; the architect reviews for general conformance.
- Field-verified dimensions: never accept "TBD" or "to be field verified at fab" for dimensions critical to adjacent work. Push back via RFI.

## Anti-patterns

- Stamping A on a submittal that contains a substitution. Substitutions need their own process — A on the wrong document signs away the spec.
- Letting B-stamp markup quietly accumulate substantive changes ("approved as noted" on 47 redlined items is a C-stamp masquerading as a B-stamp).
- Assuming the contractor's lead-time claim. Verify against the construction schedule baseline.
- Reviewing a resubmittal without referencing the prior review's comments — if Rev 1 ignored Rev 0 comments, the C-stamp persists.
- "Reviewed for general conformance" without naming the conformance axis. The phrase covers the architect's contract risk only when the review actually documents what was checked.
- Editing `index.md` manually instead of using `append_to_index.py`.

## Resources

- `scripts/init_submittals_workspace.py` — bootstrap `docs/submittals/` and the submittal log
- `scripts/append_to_index.py` — append a row to `docs/submittals/index.md`
- `references/submittal_axes.md` — eight-axis framework with sub-criteria, common failure modes, example findings tied to typical NA spec sections (storefronts, roofing, MEP, finishes)
- `assets/submittal-review-template.md` — review markdown template with action-stamp block
