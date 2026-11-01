---
name: closeout-check
description: "Builds and tracks the closeout deliverables list in docs/construction/closeout.md: O&M manuals, warranties, test and inspection reports, record documents, spare parts and attic stock, training, each with the spec section that requires it. Trigger on \"closeout\", \"closeout checklist\", \"O&M manuals\", \"warranties\", \"attic stock\", \"record drawings\", \"as-builts\", \"turnover package\", \"handover\", \"closeout-check\", or the end of construction approaching. The list is built by reading the closeout requirements out of your spec book or typed by you; the skill never invents a deliverable a spec did not require. Received items are recorded with dates; the report leads with what is outstanding, by division. Whether the contract's closeout conditions are met is the architect's certification, not this skill's."
license: MIT
metadata:
  title: "Closeout Check"
  summary: "Track closeout deliverables from the spec book to handover"
  discipline: "construction-admin"
  tags: "Construction Admin"
---

# Closeout Check

The end of a project is a list of paper: manuals, warranties, reports,
record documents, keys, spare tiles. Every item was promised somewhere in
the spec book months ago, and the owner's move-in depends on nobody
forgetting which ones are still missing. This builds that list from the spec
and tracks it to zero.

## Scope and limits — read first

**What this does.** Builds `docs/construction/closeout.md` by collecting
closeout requirements: from spec sections you paste or point it at, or typed
directly. One row per deliverable with the spec section that requires it,
the type (O&M, warranty, test report, record document, spare parts,
training), and who owes it. Records receipt as you report it, and reports
what is outstanding by division, which is the list the next OAC meeting
needs.

**What this does not do.**

- **It does not invent deliverables.** Every row cites the spec section or
  the person who required it. No generic closeout checklist is bundled here,
  because a list that is not your spec's list is wrong in both directions:
  it demands what was never specified and misses what was.
- **It does not review the content of what arrives.** Whether a warranty's
  terms are right or an O&M manual is complete is a review against the spec
  section, and `submittal-review` is the shape of that job.
- It does not certify substantial or final completion, does not release
  retainage, and does not process the final payment application
  (`draft-payment-application` drafts those). It tracks paper; the contract
  acts are the architect's and owner's.
- It does not track the punch list. `punch-list` does; the two lists close
  out in parallel and neither substitutes for the other.
- It does not store the documents. It records that they arrived, when, and
  where you filed them.

**What you need before starting.** The spec book, or at least its Division
01 closeout sections and the sections' individual closeout paragraphs, in
any pasteable form. After that, news of what arrives.

## Workflow

### Step 1. Bootstrap if needed

Check whether `docs/construction/closeout.md` exists. If not, copy
`assets/closeout-template.md` there. If the project has no `docs/` folder at
all, confirm before creating one.

### Step 2. Build the list from the spec

Work division by division. For each spec section you paste or name:

1. Read its closeout paragraphs: submittals at closeout, warranties, extra
   materials, demonstration and training.
2. One row per deliverable, quoting the requirement and citing the section
   and paragraph.
3. A section with no closeout requirements is recorded as checked, so a
   silent gap and an unread section never look the same.

Requirements you dictate without a spec source are logged with you as the
source. If a `submittal-log-builder` log exists, offer to cross-check:
closeout submittals it lists should each have a row here.

### Step 3. Record what arrives

On receipt: the date, who delivered it, where it was filed. Partial
deliveries stay `partial` with what remains noted; `received` is reserved
for complete. If you report that an item was reviewed and rejected, it
returns to `outstanding` with the dated note.

### Step 4. Report

Outstanding first, grouped by division, each row with its spec citation and
who owes it. Then partials. Then the received count. Offer the outstanding
list formatted for the meeting minutes or the transmittal
(`create-transmittal` writes the cover).

### Step 5. Reach zero

When every row reads `received`, say so, with the count and the file's
location. Whether that satisfies the contract's closeout conditions is the
architect's call under the contract, and the report says that too.

## Rules

- **Every row cites its source**: a spec section and paragraph, or the
  person who required it.
- **Checked sections are recorded**, so coverage is visible and a section
  never reads as clean just because nobody opened it.
- **Partial is not received.**
- **Outstanding leads every report.** The received pile is not the news.
- **Never delete a row.** A requirement waived gets `waived`, by whom, dated.

## Anti-patterns

- Padding the list with customary closeout items no section requires.
- Marking `received` on the contractor's word that it is in the truck.
- Letting a rejected O&M manual sit in `received` because it arrived once.
- Reporting percent complete without naming what is missing.
- Treating a finished list as completion itself; the certification is a
  contract act this file only supports.

## Resources

- `assets/closeout-template.md` — the file this creates, empty.

No reference files. The requirements come from your spec book, not from
here.
