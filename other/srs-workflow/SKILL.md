---
name: srs-workflow
description: >
  Full SRS workflow: Brainstorm → Spec → Plan (per-section files) → User Review
  → SRS Generation → Validation → Improvement Report → Context Save.
  Use when user provides a project topic and wants a complete requirements pipeline.
---

# srs-workflow — Full SRS Workflow

```
Phase 0  Topic Intake
Phase 1  Deep Brainstorm      ← multi-round, categorized, options-driven
Phase 2  Spec Writing         ← no word limit
Phase 3  Options Gate         ← user chooses next action
Phase 4  Plan Writing         ← 1 .md file per SRS section
Phase 5  User Review          ← iterate until approved
Phase 6  SRS Generation       ← 1 .md file per section, full detail
Phase 7  Auto-Validate        ← .codex/scripts/srs_validator.py
Phase 8  Improvement Report
Phase 9  Context Save
```

**Output directory:** `projects/{slug}/`

---

## Phase 0 — Topic Intake

Receive the user's topic (1 sentence to 1 paragraph). Do NOT ask questions yet.

Identify:
- Domain (e-commerce, healthcare, fintech, internal tool, SaaS, etc.)
- Scale signals (startup, enterprise, MVP, etc.)
- Any constraints mentioned

Echo back a 3-line summary:
```
Topic:      {topic}
Domain:     {detected domain}
Scale:      {detected scale or "unknown"}
```

Then state: "Starting deep brainstorm. I will ask questions by category before writing anything."
Proceed to Phase 1.

---

## Phase 1 — Deep Brainstorm

**Hard rule: AI must not proceed to Phase 2 until it can confidently answer ALL of:**
- Who are ALL actors (primary + secondary + external systems)?
- What are ALL core features (not just mentioned ones — infer and confirm)?
- What are the explicit system boundaries (in scope / out of scope)?
- What are the technical constraints?
- What are the business rules and compliance requirements?

Load `.codex/skills/srs-workflow/references/brainstorm-guide.md` for domain-specific question sets.

### Round structure

Each round: ask ONE category of questions.
Maximum 5 questions per round. Present concrete options wherever possible — never ask
open-ended questions when a multiple-choice with "Other" covers the space.

**Mandatory rounds (in order):**

**Round 1 — Actors & Users**
Ask about: primary users, secondary users, admin roles, external systems/APIs.
For each actor type: present role options with descriptions. Wait for answers.

**Round 2 — Core Features**
Present a feature checklist derived from the domain + topic.
For each feature cluster: show sub-options (e.g., authentication: email/password | OAuth | SSO | all).
Mark user selections as [CONFIRMED]. Infer likely features not mentioned — ask to confirm or reject.
Wait for answers.

**Round 3 — Scope Boundary**
Present a two-column table: proposed IN scope vs. proposed OUT scope.
Ask user to move items or add new ones. Hard-block on scope: NEVER proceed without explicit
in/out boundary.
Wait for answers.

**Round 4 — Technical Constraints**
Ask about: tech stack, hosting, existing systems to integrate, security/compliance standards,
performance targets (give numeric examples), timeline/budget signals.
Wait for answers.

**Round 5 — Business Rules & Edge Cases**
Ask about: data ownership, roles/permissions model, pricing/billing logic (if applicable),
regulatory requirements, key failure scenarios the system must handle gracefully.
Wait for answers.

**After Round 5:** Run completeness check:
- Any actor still undefined? → ask NOW before proceeding.
- Any feature with unclear scope? → ask NOW.
- Missing NFR baseline? → ask NOW.

**[GATE]** Only proceed to Phase 2 when completeness check passes with zero open items.
State: "Brainstorm complete. I now have enough information to write the spec. Proceeding."

---

## Phase 2 — Spec Writing

Write `projects/{slug}/spec.md` using the spec template structure.

**No word limit.** Write every section fully — do not summarize or truncate.
- Every actor: full description, access rights, experience level
- Every feature: stated in user's words + AI-expanded detail
- Every constraint: verbatim + implication
- In/Out scope table: exhaustive
- Business rules: numbered, precise
- NFR targets: numeric where confirmed, [TBD with context] where not

After writing, output:
```
Spec written: projects/{slug}/spec.md
Sections: §1 ... §N
Word count: ~{N}
```

Proceed to Phase 3.

---

## Phase 3 — Options Gate

Present the following menu:

```
Spec is ready. What would you like to do next?

A) Write plan          → break SRS into per-section plan files, then review
B) Re-read spec        → show full spec.md content for review/editing
C) Adjust brainstorm   → return to Phase 1 to add/change requirements
D) Jump to SRS         → skip planning, generate SRS directly (not recommended)
```

Wait for user choice. Route accordingly.
B → display spec.md, then return to Phase 3.
C → return to Phase 1 Round that covers the gap.
D → skip to Phase 6.
A → proceed to Phase 4.

---

## Phase 4 — Plan Writing

Load `.codex/skills/srs-workflow/references/plan-structure-guide.md`.

Create one plan file per SRS section under `projects/{slug}/plan/`:

```
plan/
  00-overview.md
  01-introduction.md
  02-overall-description.md
  03-01-external-interfaces.md
  03-02-functional-requirements.md
  03-03-performance.md
  03-04-database.md
  03-05-design-constraints.md
  03-06-system-attributes.md
  03-07-other-requirements.md
  appendix-a-glossary.md
  appendix-b-open-issues.md
```

**For each file:**
- Write the full planned content for that SRS section
- Include: what will be written, every sub-item, FR list with "shall" stubs, NFR targets
- No word limit — plan files are the blueprint, they must be unambiguous
- Tag any item still needing user input: `[NEEDS USER INPUT: {what}]`

After all plan files are written, output a summary table:
```
| File | Section | FRs planned | NFRs planned | Open items |
|------|---------|------------|--------------|------------|
```

Proceed to Phase 5.

---

## Phase 5 — User Review

Present summary table from Phase 4. Then ask:

```
Plan is ready for review. What would you like to do?

A) Approve plan → proceed to SRS generation
B) Modify section → specify which section(s) to change
C) Add features → return to Phase 1 Round 2
D) Show full plan file → specify which file to display
```

If user modifies: update the relevant plan file(s) and return to this gate.
**[GATE]** Only proceed to Phase 6 on explicit "Approve plan" (option A).

When approved, state: "Plan approved. Beginning SRS generation."

---

## Phase 6 — SRS Generation

Generate SRS section by section, each as its own file under `projects/{slug}/srs/`:

```
srs/
  01-introduction.md
  02-overall-description.md
  03-01-external-interfaces.md
  03-02-functional-requirements.md
  03-03-performance.md
  03-04-database.md
  03-05-design-constraints.md
  03-06-system-attributes.md
  03-07-other-requirements.md
  appendix-a-glossary.md
  appendix-b-open-issues.md
```

Load and follow `.codex/skills/srs-generator/references/srs-template.md` for each section's format.

**FR format (mandatory):**
```
FR-NN [Essential|Conditional|Optional]
Requirement:  The system shall {verb} {object} when {condition}.
Actor / Precondition / Given / When / Then / Source
```

**NFR format:** ISO/IEC 25023 Quality Attribute Scenario — numeric Response Measure only.

**No word limit.** Each file must be complete. A full SRS across all files may reach 300+ pages — this is normal and expected.

Also generate `projects/{slug}/srs/00-master-index.md` linking all section files with word counts.

Proceed to Phase 7.

---

## Phase 7 — Auto-Validate

Run the validator across the whole SRS directory at once:

```bash
python .codex/scripts/srs_validator.py --dir projects/{slug}/srs/
```

Output the full validation table. Then summarize:

```
## Validation Results
Overall: COMPLIANT | PARTIALLY COMPLIANT | NON-COMPLIANT
Errors:   N   (must fix before proceeding)
Warnings: N   (captured in Phase 8 report)
```

For each ERROR: fix the affected SRS section file immediately, then re-run the validator.
Do not leave any ERROR unresolved. WARN items do not block — capture in Phase 8.

Proceed to Phase 8.

---

## Phase 8 — Improvement Report

Write `projects/{slug}/improvement-report.md`:

- **Deferred features** — items marked out-of-scope but flagged as likely future needs
- **Technical risks** — NFRs with [TBD] targets, integration unknowns, compliance gaps
- **Refinement suggestions** — FRs that could be split further, NFRs needing real load-test data
- **Next version candidates** — features users mentioned but explicitly deferred
- **Validation warnings** — WARN items from Phase 7 that should be resolved before dev

No word limit. Be specific — reference exact FR/NFR IDs, section numbers, and user quotes from brainstorm.

Proceed to Phase 9.

---

## Phase 9 — Context Save

Write `projects/{slug}/_context/`:

```
_context/
  vision.md           ← project goals, problem statement, success metrics
  features.md         ← confirmed in/out scope feature list
  tech_stack.md       ← confirmed tech constraints
  glossary.md         ← all terms defined in Appendix A
  quality_standards.md← confirmed NFR numeric targets
  session-notes.md    ← key decisions made, open questions, next steps
```

Then output final summary:
```
Workflow complete.

Project:    {name}
Location:   projects/{slug}/
SRS files:  {N} section files
FRs:        {total FR count}
NFRs:       {total NFR count}
Verdict:    {COMPLIANT | PARTIALLY COMPLIANT}
Open items: {count} (see appendix-b-open-issues.md)

Next step: share projects/{slug}/srs/ with your dev team.
```
