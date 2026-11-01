---
name: bid-review
description: "This skill should be used during the bid phase when the user shares contractor bids, sub-bids, or proposal packages and wants them reviewed for completeness, scope alignment, qualifications, exclusions, alternates, and contract terms before owner award. Trigger on 'review these bids', 'bid review', 'check this proposal', 'compare bids', 'are these bids complete', 'bid leveling', 'bid analysis', 'qualifications and exclusions', or pasted bid content with award-decision intent. Generates a structured bid-review markdown in `docs/bids/` and appends to the project bid index."
license: MIT
metadata:
  title: "Bid Review"
  summary: "Review contractor bids for scope, exclusions, and terms before award"
  discipline: "construction-admin"
  tags: "Construction"
---

# Bid Review


## Overview


Review contractor bids — GC base-bid proposals, sub-bids, design-build proposals, or alternate bid packages — against eight axes and produce a written review that lives in `docs/bids/`. The output is a working document for the owner / owner's rep / architect: bid leveling, qualification flags, exclusion rollup, and a recommended-award rationale.


Aligned with NA practice: AIA A101-2017 / A102-2017 / A103-2017 owner-contractor forms, AIA A201-2017 General Conditions, AIA A305 Contractor's Qualification Statement, EJCDC C-410 Bid Form, and standard ITB / Division 00 / Division 01 conventions.


This skill is for the owner-side perspective. It produces a leveling and recommendation memo, not a binding award. Public-sector projects with sealed-bid procurement have additional process constraints — the skill flags them, the user's procurement counsel handles them.


## Scope and limits — read first


**What this does.** Reads the bids you supply, runs each one against eight axes,
levels them to a common scope so the prices can be compared, and writes a review
to `docs/bids/` with a recommended award and the reasons behind it. Every
exclusion and every defect is quoted with the bidder and the page it came from.

**What this does not do.**

- **It does not price anything.** No $/sf, no unit prices, no independent
  estimate. `references/bid_benchmarks.md` names the publishers to pull current
  figures from and holds no figures of its own, so a benchmark in a review is
  one you quoted with its source and edition.
- It does not award the contract. The memo is a recommendation to the owner, and
  on a public sealed bid the leveling is advisory rather than determinative.
- It does not clear a responsiveness defect. It flags what looks fatal on the
  bid form; procurement counsel decides whether it is.
- It does not verify a bidder's bonding capacity, insurance, or licence. It says
  what to ask for and who to ask.
- It does not check the bid against code, buildability, or the specification.
  Those are `code-compliance-review`, `constructability-review`, and `spec-review`.

**What you need before starting.** The bids themselves, the ITB with its
Division 00 and 01 requirements, the delivery method and procurement type, and,
for a leveled comparison, which alternates the owner intends to select.

## When to use


Trigger on:

- Pasted bid forms, bid tabs, sub-bid sheets, qualification statements, schedules of values.
- Project file paths to a bid package.
- Explicit asks: "bid review", "level these bids", "compare these proposals", "is this bid complete", "what are they excluding".
- Hand-off from `brief-review` when the brief flags procurement risk.

Do NOT trigger for:

- Construction-phase submittal review (use `submittal-review`).
- Spec-section review (use `spec-review`).
- Cost estimating from scratch (this skill reviews bids against an issued ITB — it does not generate independent estimates).
- RFP brief/owner-requirements review (use `brief-review`).

## Workflow


### Step 1 — Bootstrap if needed


Check that `docs/bids/index.md` exists. If not:


```bash
python scripts/init_bids_workspace.py
```


### Step 2 — Anchor the procurement basis

- Read `docs/project.md` if it exists for delivery method (DBB, CMAR, DB, IPD), procurement type (public sealed, private negotiated, RFP-based), bid form template (AIA A305 / EJCDC / agency-specific), and Division 00/01 contents.
- Identify the bid package scope — full GC base bid, single trade sub-bid (NY filed-sub style), CM at-risk GMP, design-build proposal, or alternates-only.
- Note the bid form requirements: bid bond %, listing of subcontractors, MWBE / DBE participation, prevailing-wage acknowledgment, addenda acknowledgments, bid form signatures.
- Pull comparable cost benchmarks from `references/bid_benchmarks.md` (typical $/sf for the project type and region) for sanity-checking against the engineer's estimate.

### Step 3 — Apply eight-axis review


Load `references/bid_axes.md` for the full framework with sub-criteria. Quick reference:

1. **Base-bid scope completeness** — All scopes in the ITB / drawings / specs reflected in the bid? Missing trades or "by others" tags inconsistent with the contract scope?
2. **Qualifications & exclusions** — Bidder's clarifications (assumptions about hazardous materials, unsuitable soils, owner-furnished items) reasonable? Exclusions itemized or buried?
3. **Alternates** — Add/deduct alternates priced individually? Pricing internally consistent (Alt 1 deduct vs Alt 2 add for the same area shouldn't double-count)? Alternate selection sensitivity for award.
4. **Unit prices & allowances** — Where the bid form specifies unit prices (rock excavation, structural steel adjustment, finish upgrade) or allowances (signage, landscape, art), are they defensible against `references/bid_benchmarks.md`?
5. **Schedule & milestones** — Substantial completion date acknowledged? Liquidated-damages rate accepted? Weather-day allowance? Phased turnover dates? Long-lead procurement commitments?
6. **Contractor qualifications** — AIA A305 or equivalent submitted? Bonding capacity ≥ contract value × applicable multiple? Insurance limits per A201 / Division 01? Similar-project experience (size, type, region, recency)? Key personnel committed? Subcontractor list with each sub's pre-qual status?
7. **Bid form completeness & responsiveness** — All addenda acknowledged? Bid bond / cashier's check attached at correct percentage? Required signatures and notarization? MWBE / DBE goal met or good-faith documented? Non-collusion affidavit? On public projects, anything that makes the bid non-responsive is fatal.
8. **Contract-terms alignment** — Bidder accepting the AIA A101 / A102 / A103 / agency form as-is, or proposing exceptions (insurance limits, indemnification, retainage %, payment terms, dispute resolution)? Each exception is a negotiation point with cost.

Focus on the 3-5 axes with real signal. A leveling memo on three GC base bids reads heavily on axes 1, 2, 3, 7. A single-bidder GMP review reads heavily on 4, 5, 8.


### Step 4 — Level the bids


For multi-bidder reviews, build a leveling table that adjusts each bid to a common scope:

- Start with bid base price.
- Add value of each bidder's exclusions back in (using the highest-bidder's price for that scope as a proxy when the exclusion is unpriced elsewhere).
- Subtract or add for unit-price differences on assumed quantities.
- Adjust for alternates if the owner has signaled which alternates will be selected.
- Display the **leveled** bid alongside the **submitted** bid, with the delta itemized.

This is documented in the review file's "Leveled Bid Comparison" section. The leveled bid, not the submitted bid, is the basis for award recommendation on private projects. Public sealed-bid awards must follow procurement law — leveling is advisory, not determinative.


### Step 5 — Write the review


Read `assets/bid-review-template.md`, fill placeholders. Filename:


`docs/bids/<YYYY-MM-DD>-<bid-package>-<scope>.md`


Slug rule: lowercase, `[^a-z0-9-]` removed, max 40 chars (`acme-hq-gc-base`, `school-finish-pkg-alt2`). If a review with the same date+slug already exists, suffix `-<n>`.


### Step 6 — Update the bid index


```bash
python scripts/append_to_index.py \
  --date 2026-05-09 \
  --slug acme-hq-gc-base \
  --bid-type "gc-base" \
  --bidder-count 4 \
  --recommended "ABC Construction" \
  --primary-axes "scope,qualifications,alternates"
```


The script appends a row to `docs/bids/index.md`. Do NOT edit the index manually with the Edit tool.


### Step 7 — Report


Tell the user:

- Path to the review file.
- The leveled-bid spread and the recommended award (with the 2-3 reasons that drive it).
- Any responsiveness defects on the apparent low bidder that, on a public project, would force a second-low award.
- Open clarifications to issue before contract award (typically 2-5 items per bidder).
- Whether `submittal-review` should be queued for the long-lead items the bidder identified.

## Rules

- Every flagged exclusion cites the bidder + the bid sheet location ("ABC, Page 4, Item 7: 'Excludes hazardous materials abatement'") plus an estimated dollar impact.
- Distinguish "responsive" from "responsible" — responsiveness is whether the bid form was submitted correctly (fatal if not, on public projects); responsibility is whether the bidder can actually perform (negotiable).
- Bonding capacity verified independently when possible. A bidder claiming $50M capacity on a $30M project should still produce a current bonding letter; capacity claims age fast.
- Schedule analysis cites named milestones from the bid form, not generic durations. "120 calendar days from NTP to substantial completion" is reviewable; "approximately 4 months" is not.
- Recommend negotiations only on the low or apparent-low bidder; multi-bidder negotiation rounds are common in private DBB but inappropriate in public sealed-bid procurement.
- Bid bond percentage: standard NA practice is 5% on public, 10% on some private. Confirm the percentage required by the ITB before flagging an under-percentage as defective.

## Anti-patterns

- Awarding on submitted price without leveling for exclusions. The cheap bid is often cheap because it excluded scope.
- Treating qualifications as boilerplate. A "qualification" that the bidder assumes the existing slab is sound shifts $300K of risk back to the owner.
- Ignoring schedule fit on a fast-track project. Lowest price + 30-day longer schedule may net negative when liquidated damages and financing carry are included.
- "Or equal" submitted at bid time. A201 §3.4.2 substitution process applies post-award; bid-time substitutions need to have been allowed by the ITB.
- Editing `index.md` manually instead of using `append_to_index.py`.
- Recommending award on a public sealed-bid project before procurement counsel has cleared responsiveness defects.

## Resources

- `scripts/init_bids_workspace.py` — bootstrap `docs/bids/` and the bid index
- `scripts/append_to_index.py` — append a row to `docs/bids/index.md`
- `references/bid_axes.md` — eight-axis framework with sub-criteria, common failure modes, example findings tied to NA delivery methods (DBB, CMAR, DB, IPD)
- `references/bid_benchmarks.md` — typical $/sf and unit-price ranges for major NA building types and regions (RSMeans-anchored, current to 2026 Q2)
- `assets/bid-review-template.md` — review markdown template with leveled-bid comparison block
