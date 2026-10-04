---
name: new-development
description: |
  Greenfield development path for products, tools, and systems that do
  not yet exist. G Stack validates the idea before anything is planned
  or built. Use when starting from zero: no existing codebase, no existing
  schema, no existing API that this extends.

  AUTO-FIRE immediately when the user says any of:
  - "new development", "/new-development [description]"
  - "I have an idea for [X]", "I want to build [X] from scratch"
  - "new product", "new tool", "new platform", "new application"
  - "build [X] — it doesn't exist yet", "start a new project"

  Do NOT use when an existing codebase already exists for the work —
  use /full-development for large brownfield work.
  If unsure: ask "Does any part of this already exist in code?" If yes → /full-development.

  This is the most token-intensive command. Use it when the investment
  is justified by the scope of what is being built.
---

# New Development

Read ~/.claude/skills/shared/context-guardian.md now and apply all rules
within it for the entire session before doing anything else.

---

## Entry check — greenfield confirmation

Before doing anything, confirm the build is truly greenfield.

Ask: "Does any part of this already exist as code — even partially?"

**If NO (nothing exists):** Proceed to Step 1.

**If YES (something exists):**
```
Part of this already exists as code.
/new-development is designed for greenfield builds only.
For changes to existing systems, use /full-development.

Shall I route to /full-development? YES / NO
```
If YES: instruct the user to run /full-development. Carry forward the
description. Stop this session.
If NO: ask what exactly exists and what is new. Determine the correct
command before proceeding.

---

## Step 1 — G Stack /office-hours (idea validation)

Invoke G Stack /office-hours.

This step validates whether the idea is worth building before any
planning or code begins. It uses six YC-style forcing questions.

Use Opus for this step.

The six forcing questions:
1. **Demand reality** — can you name a specific person, at a specific
   company, who needs this today?
2. **Status quo** — what are they doing right now to solve this problem?
   (If the answer is "nothing", that is a red flag, not an opportunity.)
3. **Desperate specificity** — how bad is the pain? Would they pay for
   a solution that is 30% better than the status quo?
4. **Narrowest wedge** — what is the single smallest version of this that
   delivers real value? What can be cut?
5. **Observation and surprise** — what have you seen in person that most
   people building in this space have not?
6. **Future fit** — will this still matter in 3 years, or will the
   underlying problem be solved by something else?

G Stack /office-hours asks these one at a time. It challenges every answer.
It does not move to planning until the user can answer all six with
specificity, or until the user explicitly decides to proceed despite gaps.

At completion, G Stack saves a design doc to `~/.gstack/projects/[name].md`.

```
/office-hours complete.
Design doc saved: ~/.gstack/projects/[name].md
Identified user: [specific person / company]
Core problem: [one sentence]
Narrowest wedge: [one sentence]
Proceeding to spec and PRD.
```

---

## Step 2 — G Stack /autoplan + Matt /to-prd

**G Stack /autoplan:** Chains CEO review and engineering review of the
design doc. Surfaces architectural concerns before planning begins.
Produces a scope-validated plan.

**Matt /to-prd:** Converts the validated plan into a PRD.
Files it as a GitHub issue in the current repository.

```
PRD filed: [GitHub issue URL]
This becomes the source of truth for the build.
GSD will use this PRD to create the phase plan.
```

Switch from Opus to Sonnet after /autoplan completes.

---

## Step 3 — GSD /gsd-new-project (always mandatory)

Invoke GSD /gsd-new-project.

GSD reads the PRD and the /office-hours design doc.
Runs the research synthesizer (parallel sub-agents) to:
- Investigate the technical domain
- Find existing libraries, APIs, or tools relevant to the build
- Identify risks the PRD did not surface
- Confirm that the narrowest wedge is actually buildable

GSD configuration for /new-development:
- Research before planning: YES
- Verify plan before execution: YES
- Verify work after each phase: YES
- Execution model: sequential
- Planning depth: standard (5–8 phases, 3–5 tasks each)

**Phase pre-validation (mandatory):**
Read the pre-validation rule in context-guardian.md.
Estimate token consumption per phase.
Split any phase estimated over 80k tokens.
Announce splits made.

Present the validated plan:
```
Phase plan ready ([N] phases):
  Phase 1: [name] — [N] tasks — estimated [Xk] tokens
  Phase 2: [name] — [N] tasks — estimated [Xk] tokens
  ...
  Total across sessions: ~[X]k tokens (midpoint)

Research findings:
  - [Key discovery 1]
  - [Key discovery 2]
  - [Risks flagged: list]

PRD coverage: [N of N PRD requirements mapped to phases]

Approve this plan? YES / REVISE
```

Wait for explicit YES or REVISE. Do not proceed without approval.

---

## Step 4 — Ralph Loop gate (always shown)

Read ~/.claude/skills/shared/ralph-loop-gate.md.

Always present the gate for /new-development.

Greenfield builds are lower risk for autonomous mode than brownfield —
there is no existing code to accidentally break. Note this difference
in the gate presentation.

Wait for explicit YES (autonomous) or NO (manual).

---

## Step 5 — Superpowers TDD execution

For every task in every phase, without exception:

1. **RED**: write the failing test first. Confirm it fails.
   For greenfield: the first test in a phase establishes the interface
   contract. Do not write implementation before this contract exists.
2. **GREEN**: write the minimal implementation. Make the test pass.
3. **REFACTOR**: clean up. Document public interfaces inline.
4. Commit after each task with a specific message.

Superpowers subagent-driven-development dispatches a fresh subagent
per task. Each subagent gets a clean 200k context window.
Context guardian 50% hard stop applies within each subagent session.

After all tasks in a phase:
- Superpowers /code-review runs
- Fix all critical and high issues before the next phase
- Phase completion summary presented before advancing

---

## Step 6 — Full delivery gate

Read ~/.claude/skills/shared/delivery-gate.md — Variant B (Full).

Run in sequence after all phases complete:
1. Superpowers /code-review
2. G Stack /review (security + completeness + architecture)
3. G Stack /qa — always run for /new-development (new product = new UI by default)
   Skip only if the build is a pure API or CLI with no user interface.

**G Stack /land-and-deploy:**
Run after the full delivery gate passes.
One-time setup detects the deployment platform, production URL, and
deploy commands. Sets up for all future deploys from this project.

```
[Delivery Gate] PASS
Deploying to production via G Stack /land-and-deploy.
```

---

## Post-build

**G Stack /retro:** Run after the first successful deploy.
Generates a sprint retrospective: lines changed, commits, patterns,
what went well, what to improve next time.

```
Build complete.
Production URL: [URL]
Retro saved to: retro-[YYYYMMDD].md
```

---

## Token budget

Expected: 220k+ tokens across all sessions.
/office-hours alone: ~15k tokens (Opus — higher per-token cost, justified).
GSD research synthesizer: ~30k tokens (Opus).
All execution: Sonnet (~50k per phase, midpoint).
Context guardian 50% hard stop applies in every session, including headless.

This is the most expensive command in the stack. Use it only for
genuine greenfield builds. For large extensions to existing code, use
/full-development — it skips /office-hours and /to-prd, saving ~45k tokens.
