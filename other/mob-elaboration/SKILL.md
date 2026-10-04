---
name: mob-elaboration
description: >
  Use when defining a project before writing code. Phase 1 (Mob Elaboration)
  turns a business idea into validated requirements (vision, scope, stories,
  constraints) via structured questioning. Phase 2 (Mob Construction) produces
  architecture (domain model, layers, integrations, ADRs). Use at kickoff, new
  service, or major feature when requirements/architecture are not yet agreed.
  Outputs: docs only (no scaffolded code). References: phase1-elaboration-guide.md,
  phase2-construction-guide.md.
---

# Mob Elaboration

To establish a project foundation before writing code via two sequential phases. Each phase produces focused documents (one concern per file) to keep context minimal.

## References

| Phase   | Read before starting | File |
| ------- | -------------------- | ---- |
| Phase 1 | Before Mob Elaboration | `references/phase1-elaboration-guide.md` |
| Phase 2 | Before Mob Construction | `references/phase2-construction-guide.md` |

## When to Activate

- Starting a new project, service, or product from a business idea
- Starting a major feature that crosses multiple layers or teams
- Requirements are ambiguous or not yet agreed upon
- Team wants alignment before the first commit

Do NOT activate if all `docs/requirements/` and `docs/architecture/` files are already filled.

---

## Decision Tree

```
SITUATION?
│
├─ Have a business idea, no requirements yet
│  └─ START Phase 1 → read references/phase1-elaboration-guide.md
│
├─ Phase 1 files complete, need architecture
│  └─ START Phase 2 → read references/phase2-construction-guide.md
│
├─ Requirements exist but architecture missing
│  └─ SKIP Phase 1 → START Phase 2 → read references/phase2-construction-guide.md
│
└─ All files complete
   └─ Skill done — proceed to implementation
```

---

## Phase 1 — Mob Elaboration

**Goal:** Transform a business idea into 4 validated requirement files.

**Entry condition:** User provides a seed — an idea, problem statement, feature request, or ticket.

**Workflow:**

1. Read `references/phase1-elaboration-guide.md` before starting
2. Run 4 structured question rounds (domain → scope → stories → acceptance criteria)
3. Ask 3–5 questions per round; wait for mob answers before proceeding
4. After each round is confirmed, write only that round's file — do not batch
5. Get explicit mob confirmation on all 4 files before advancing to Phase 2

**Outputs (one file per round):**

- Round 1 → `docs/requirements/01-vision.md`
- Round 2 → `docs/requirements/02-scope.md`
- Round 3+4 → `docs/requirements/03-user-stories.md`
- Final → `docs/requirements/04-constraints.md`

---

## Phase 2 — Mob Construction

**Goal:** Translate validated requirements into 3 architecture files + individual ADRs.

**Entry condition:** Phase 1 files complete and mob-confirmed (or user skips Phase 1).

**Workflow:**

1. Read `references/phase2-construction-guide.md` before starting
2. Read all `docs/requirements/` files before proposing anything
3. Run 4 structured steps (domain model → layers → integrations → ADRs)
4. After each step is confirmed, write only that step's file
5. Each ADR is a separate file; copy `docs/architecture/adr/ADR-000-template.md`
6. Get explicit mob confirmation on all files before closing Phase 2

**Outputs (one file per step):**

- Step 1 → `docs/architecture/01-domain-model.md`
- Step 2 → `docs/architecture/02-layers.md`
- Step 3 → `docs/architecture/03-integrations.md`
- Step 4 → `docs/architecture/adr/ADR-NNN-[kebab-title].md` (one per decision)

---

## Document Output Protocol

To produce each output file:

1. Read the corresponding template in `docs/`
2. Fill every `[FILL: ...]` placeholder — leave none empty
3. Present the filled content to the mob
4. Ask: "Does this capture everything? What is missing or wrong?"
5. Incorporate corrections
6. Only write the file to disk after mob confirms it
7. Do not write the next file until the current one is confirmed

---

## Core Principles

- **Questions before proposals** — never propose until the relevant round is complete
- **Mob validation is mandatory** — never write a file without explicit confirmation
- **One file at a time** — confirm each file before starting the next
- **Tech-agnostic in Phase 1** — requirements describe business needs, not implementations
- **Record all assumptions** — when mob cannot answer, state the assumption and write it in `04-constraints.md`

---

## Output Structure

```
docs/
├── requirements/
│   ├── 01-vision.md
│   ├── 02-scope.md
│   ├── 03-user-stories.md
│   └── 04-constraints.md
└── architecture/
    ├── 01-domain-model.md
    ├── 02-layers.md
    ├── 03-integrations.md
    └── adr/
        ├── ADR-000-template.md   ← do not edit, copy per decision
        └── ADR-NNN-[title].md    ← one file per ADR
```

**Reference files:** See References table at top. Read the corresponding guide before starting each phase.
