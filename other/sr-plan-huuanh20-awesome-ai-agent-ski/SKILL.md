---
name: sr-plan
description: >
  Phase 4 of the SRS workflow. Reads spec.md and writes one detailed plan file
  per SRS section (§1–§3 + Appendices). Each file is a complete blueprint
  for the corresponding SRS section. No word limit.
---

# sr-plan

Goal: produce 12 plan files — one per SRS section — that serve as unambiguous blueprints
for SRS generation. No summarizing, no truncation.

---

## Step 0 — Identify Project

```
Ask the user: "Which project should I plan? (slug)"
```

Read `projects/{slug}/spec.md`. If missing, tell user to run `$sr-spec` first.
Load `.codex/skills/srs-workflow/references/plan-structure-guide.md`.

---

## Step 1 — Write Plan Files

Create all files under `projects/{slug}/plan/`. For each file, follow the detailed
spec in `plan-structure-guide.md` for what must be included.

Write in this order (each file before proceeding to next):

1. `00-overview.md`         — master map, FR/NFR count totals, actor table, assumptions
2. `01-introduction.md`     — §1.1 Purpose, §1.2 Scope (IN/OUT table), §1.3 Definitions, §1.4 References, §1.5 Overview
3. `02-overall-description.md` — §2.1 Perspective, §2.2 Functions, §2.3 User Characteristics, §2.4 Constraints, §2.5 Assumptions, §2.6 Apportioning
4. `03-01-external-interfaces.md` — UI screens, hardware, software APIs, communication protocols
5. `03-02-functional-requirements.md` — ALL FRs with "shall" stubs + GWT stubs + priority
6. `03-03-performance.md`   — ALL NFRs with numeric Response Measure or [TBD]
7. `03-04-database.md`      — entities, retention, volumes, PII fields
8. `03-05-design-constraints.md` — imposed tech stack, compliance-driven constraints
9. `03-06-system-attributes.md` — reliability, availability, security, maintainability, portability, usability
10. `03-07-other-requirements.md` — i18n, legal, operational, transition, training
11. `appendix-a-glossary.md`    — all domain terms needing precise definitions
12. `appendix-b-open-issues.md` — every [NEEDS USER INPUT] from all plan files, with owner + resolve-by

**FR numbering rules (enforced across all plan files):**
- Sequential: FR-01, FR-02, FR-03 … no resets between sections
- Format: `FR-NN [Essential|Conditional|Optional]`
- Every FR must have: Requirement (shall clause) + Given/When/Then stubs
- Tag unclear items: `[NEEDS USER INPUT: {specific question}]`

---

## Step 2 — Summary Table

After all 12 files are written, run:
```bash
python .codex/scripts/plan_validator.py --dir projects/{slug}/plan/ --stats
```
Use its counts (don't recount by hand — for large plans manual counting drifts).

Output:

```
| File | Section | FRs | NFRs | Open items |
|------|---------|-----|------|-----------|
| 00-overview.md | Master map | — | — | {n} |
| 03-02-functional-requirements.md | §3.2 FR | {n} | — | {n} |
...

Total: {FR count} FRs ({Essential}/{Conditional}/{Optional})
       {NFR count} NFRs ({confirmed} confirmed / {TBD} [TBD])
       {open} open items → see appendix-b-open-issues.md
```

---

## Step 3 — User Review Gate

```
Ask the user:
"Plan is ready. What would you like to do?
 A) Approve → proceed to $sr-generate
 B) Modify a section → which file(s)?
 C) Show a plan file → which one?
 D) Add features → run $sr-brainstorm again to extend"
```

If B: update the relevant file(s) and return to Step 3.
If C: display the file content, then return to Step 3.
If D: instruct user to run `$sr-brainstorm` and update spec, then restart from Step 0.
If A: proceed.

---

## Step 4 — Handoff

Output when plan is approved:
```
Plan approved.

Files: projects/{slug}/plan/ (12 files)
FRs planned: {total} ({Essential} Essential / {Conditional} Conditional / {Optional} Optional)
NFRs planned: {total}
Open items: {count}

Next: $sr-generate → generates full SRS from this plan (no word limit)
```
