---
name: vibe-spec-review
description: >
  Spec quality gate — audits planning documents before any code is written.
  Automatically triggered by vibe-brainstorm (after BRIEF.md), vibe-agent
  (after AGENT_ARCH.md), vibe-architect (after ARCHITECTURE.md), vibe-new-app
  and vibe-init (after vibe/ folder), and vibe-add-feature (after FEATURE_SPEC.md).
  Audits all documents that exist: BRIEF.md, AGENT_ARCH.md, SPEC.md,
  ARCHITECTURE.md, FEATURE_SPEC.md.
  P0 findings are critical gaps that will cause build failures if not fixed.
  P1/P2 findings are warnings — user decides whether to fix or continue.
  Shows findings clearly, waits for user decision, never blocks silently.
  Triggers on "spec-review:" prefix, "review the spec", "check the brief",
  "audit the spec", "is the spec ready", "review before we build".
  Always use when planning documents exist and build is about to begin.
---

# Vibe Spec Review Skill

Audits every planning document before a line of code is written.
Finds gaps, contradictions, untestable criteria, and missing boundaries
that would cause failures, confusion, or rework during the build.

> **Autonomous / headless mode.** At startup resolve the settings with
> `python3 ~/.claude/skills/vibe-mode/scripts/vibe_state.py mode`. If `vibe_mode` is
> `autonomous`, every "wait", "ask", "confirm" and approval step in this skill follows
> vibe-mode's `references/HEADLESS.md` §2 instead: take the recommended option, accept your
> own draft after one self-check, log each choice to `vibe/DECISIONS.md`, never ask the
> user, and stop — writing `vibe/.run_state.json` — only when a person is genuinely required.

A bad spec is the most expensive bug in software.
This skill finds it before it costs anything.

**Never edits the documents it reviews unless the user says "fix [finding]".** It always
writes its own report to `vibe/spec-reviews/` and a summary to `vibe/DECISIONS.md`.

---

## The principle

The O'Reilly northstar is clear: "Most agent files fail because they're too vague."
Vague specs produce vague code. Untestable criteria produce unverifiable builds.
Missing boundaries produce agents that go off-script at the worst moment.

This skill is the last checkpoint before execution begins.
It asks: if an agent read only these documents, would it build the right thing?
If the answer is "maybe" — that's a finding.

---

## Trigger points — how this skill is invoked

This skill is **primarily** handed off from other skills at exactly the right moment
(Triggers 1–4 below) — that is the common path. It can **also** be run on demand by
the user typing `spec-review:` (Trigger 5), e.g. to re-check documents before a build.
Both are valid entry points.

### Trigger 1 — After `vibe-brainstorm`
Invoked by: the final step of `vibe-brainstorm` after BRIEF.md is written.
Announcement: *"BRIEF.md written. Running spec-review to check quality before architect:..."*
Scope: BRIEF.md only.
Purpose: catch vague goals, untestable success criteria, missing user definition,
and undefined constraints before they propagate into ARCHITECTURE.md and SPEC.md.

### Trigger 2 — After `vibe-agent`
Invoked by: the final step of `vibe-agent` after AGENT_ARCH.md is written.
Announcement: *"AGENT_ARCH.md written. Running spec-review to validate agent design..."*
Scope: AGENT_ARCH.md + BRIEF.md if exists.
Purpose: catch missing VerifierAgents, undefined HITL gates, hallucinated tools,
agents with multiple responsibilities, and state ownership conflicts.

### Trigger 2.5 — After `vibe-architect`
Invoked by: the final step of `vibe-architect` after ARCHITECTURE.md is written
(before the user runs `new:`).
Announcement: *"Architecture drafted. Running spec-review before you scaffold..."*
Scope: ARCHITECTURE.md + BRIEF.md if exists.
Purpose: catch missing patterns/conventions, empty boundary (Always/Ask/Never)
sections, a missing "never commit secrets" rule, and stack drift from BRIEF.md —
so drift is caught at authoring time, not indirectly when `new:` runs.

### Trigger 3 — After `vibe-new-app` or `vibe-init`
Invoked by: the final step of `vibe-new-app` / `vibe-init` after vibe/ folder is created.
Announcement: *"vibe/ folder created. Running spec-review before first task..."*
Scope: SPEC.md + ARCHITECTURE.md + BRIEF.md + AGENT_ARCH.md (all that exist).
Purpose: catch spec-architecture contradictions, missing acceptance criteria,
undefined tech stack, empty boundary sections, and provisional SPEC.md warnings.

### Trigger 4 — After `vibe-add-feature`
Invoked by: the final step of `vibe-add-feature` after FEATURE_SPEC.md is written.
Announcement: *"FEATURE_SPEC.md written. Running spec-review before feature build..."*
Scope: FEATURE_SPEC.md + SPEC.md (for contradiction check).
Purpose: catch untestable feature criteria, missing scope boundaries,
tasks without file assignments, and contradictions with existing SPEC.md.

### Trigger 5 — On demand
Triggered by: `spec-review:` prefix in the user's message.
Scope: all documents that exist in the project.
No announcement needed — user explicitly requested it.

---

## Step 0 — Detect what exists

```bash
ls BRIEF.md AGENT_ARCH.md SPEC.md ARCHITECTURE.md \
   vibe/SPEC.md vibe/ARCHITECTURE.md \
   vibe/features/*/FEATURE_SPEC.md 2>/dev/null
```

Build the audit list from what's found. Skip documents that don't exist.
Never fail because a document is missing — just audit what's there.

If nothing exists:
> "No planning documents found. Run `brainstorm:` to start."
Stop.

---

## Step 1 — Audit BRIEF.md

**Skip if BRIEF.md does not exist.**

Read the full BRIEF.md. Check against `references/BRIEF_RUBRIC.md`.

### 1A — Problem definition
- [ ] Is the core problem stated in one clear sentence? (vague = P1)
- [ ] Is the problem grounded in a real user pain? (generic = P1)
- [ ] Does it say who has the problem specifically? (missing = P0)

### 1B — User definition
- [ ] Is at least one primary user type defined? (missing = P0)
- [ ] Is the user described with enough specificity to make design decisions?
      ("small business owners" = too vague = P1 / "marketing managers at B2B SaaS companies with 10-50 employees" = good)

### 1C — Success criteria
- [ ] Are success criteria present? (missing = P0)
- [ ] Are they measurable? ("users are happy" = P0 / "user completes onboarding in <5 minutes" = good)
- [ ] Could a developer write a test for each criterion? (untestable = P1)
- [ ] Is there at least one quantitative metric? (none = P1)

### 1D — Constraints and non-goals
- [ ] Are technical constraints stated? (missing = P1)
- [ ] Are non-goals stated? (missing = P1 — without non-goals, scope creep is guaranteed)
- [ ] Is the v1 scope explicitly bounded? (unbounded = P1)

### 1E — Risks
- [ ] Are known risks or open questions listed? (missing = P2)
- [ ] Are dependencies on external systems noted? (missing = P1 if applicable)

---

## Step 2 — Audit AGENT_ARCH.md

**Skip if AGENT_ARCH.md does not exist.**

Read the full AGENT_ARCH.md. Check against `references/AGENT_ARCH_RUBRIC.md`.

### 2A — Pattern and framework
- [ ] Is a pattern selected with reasoning? (missing = P1)
- [ ] Is pattern selection appropriate for the stated complexity?
      (Orchestrator+Subagents for a 2-step pipeline = P1 over-engineering)
- [ ] Is a framework selected? (missing = P1)
- [ ] Does the framework match the stated stack? (mismatch = P0)

### 2B — Agent roles
- [ ] Does every agent have exactly one stated responsibility? (multiple = P1)
- [ ] Are agent names descriptive of their function? (Agent1, Agent2 = P2)
- [ ] Is there an orchestrator defined if the pattern requires one? (missing = P0)
- [ ] Does any agent's responsibility overlap with another's? (overlap = P1)

### 2C — VerifierAgent coverage
- [ ] Does every sub-agent have a corresponding VerifierAgent? (missing = P0)
- [ ] Does each verifier have a defined rubric (not just "checks quality")? (vague = P1)
- [ ] Is retry logic defined? (retry once → HITL = required, missing = P1)
- [ ] Does each verifier have a PASS/FAIL verdict format? (missing = P1)

### 2D — HITL checkpoints
- [ ] Are HITL checkpoints defined for irreversible actions? (missing = P0 if applicable)
- [ ] Does each checkpoint define what the human sees? (vague = P1)
- [ ] Does each checkpoint define available actions? (missing = P1)
- [ ] Is timeout behaviour defined for each checkpoint? (missing = P2)

### 2E — Tool mapping
- [ ] Does every tool have an assigned owner agent? (unassigned = P1)
- [ ] Are write tools flagged for risk? (unflagged write tool = P1)
- [ ] Are external API dependencies noted? (missing = P1)
- [ ] Do any write tools lack a HITL gate? (missing HITL before irreversible write = P0)

### 2F — State design
- [ ] Is state ownership defined per key? (missing = P1)
- [ ] Are there any multi-writer state keys? (multi-writer = P0 — race condition risk)
- [ ] Is cross-run memory need addressed? (yes/no required, missing = P2)

### 2G — Implementation plan
- [ ] Is an implementation order defined? (missing = P1)
- [ ] Does implementation order respect dependencies? (misordered = P0)

---

## Step 3 — Audit SPEC.md / vibe/SPEC.md

**Skip if neither exists.**

Read the full SPEC.md. Check against `references/SPEC_RUBRIC.md`.

### 3A — O'Reilly six core areas check
Per the O'Reilly northstar, a complete spec covers six areas.
Score each as present (✅) / partial (⚠️) / missing (❌):

- [ ] **Commands** — build, test, lint, run commands with exact flags (missing = P1)
- [ ] **Testing** — framework, file locations, coverage expectations (missing = P1)
- [ ] **Project structure** — where source, tests, docs live (missing = P1)
- [ ] **Code style** — naming conventions, formatting, real code example (missing = P2)
- [ ] **Git workflow** — branch naming, commit format, PR process (missing = P2)
- [ ] **Boundaries** — three-tier system: always / ask first / never (missing = P1)

Any missing area with P1 severity is a collective finding:
> "Spec is missing [N] of the 6 O'Reilly core areas: [list]. These will cause agent confusion during build."

### 3B — Acceptance criteria quality
For each feature / requirement in SPEC.md:
- [ ] Does it have acceptance criteria? (missing = P0 on any item)
- [ ] Is each criterion testable by a developer? (untestable = P1)
- [ ] Is each criterion specific enough to write a single test for? (vague = P1)
- [ ] Are edge cases and error states covered? (missing on critical paths = P1)

**Testability test:** Can you write `expect([something]).toBe([specific value])`
from this criterion? If no — it's untestable.

Examples:
- "Users should have a good experience" → P0 untestable
- "Users can log in" → P1 incomplete (no error state, no timeout)
- "User submits valid email + password → redirected to /dashboard within 2s" → ✅

### 3C — Scope and non-goals
- [ ] Is v1 scope explicitly defined? (missing = P1)
- [ ] Are non-goals listed? (missing = P1)
- [ ] Does scope align with BRIEF.md? (contradiction = P0)
- [ ] Are deferred features documented? (missing = P2)

### 3D — Tech stack completeness
- [ ] Is the primary language and framework stated with version? (missing = P1)
- [ ] Is the database stated? (missing = P1 if applicable)
- [ ] Are key dependencies listed? (missing = P2)
- [ ] Does the stack match what ARCHITECTURE.md prescribes? (mismatch = P0)

### 3E — Provisional flag check
If SPEC.md contains `⚠️ PROVISIONAL` (set by vibe-init):
> "⚠️ P1: SPEC.md is marked PROVISIONAL — generated from code, not from original requirements. Human must verify it reflects actual intent before this review is considered complete."

---

## Step 4 — Audit ARCHITECTURE.md / vibe/ARCHITECTURE.md

**Skip if neither exists.**

Read the full ARCHITECTURE.md. Check against the `# ARCHITECTURE_RUBRIC.md` section inside `references/SPEC_RUBRIC.md`.

### 4A — Pattern documentation
- [ ] Is the primary architectural pattern stated? (missing = P1)
- [ ] Is the folder structure defined? (missing = P1)
- [ ] Is state management approach defined? (missing = P1 for frontend projects)
- [ ] Is the API design pattern defined (REST/GraphQL/tRPC)? (missing = P1 if applicable)

### 4B — Convention completeness
- [ ] Are naming conventions defined? (missing = P1)
- [ ] Is TypeScript strictness level stated? (missing = P1 for TS projects)
- [ ] Is error handling pattern defined? (missing = P1)
- [ ] Are testing conventions defined? (missing = P1)

### 4C — Boundary definition (three-tier)
- [ ] Is an Always section present? (missing = P1)
- [ ] Is an Ask First section present? (missing = P1)
- [ ] Is a Never section present? (missing = P1)
- [ ] Does Never include "never commit secrets"? (missing = P0)
- [ ] Are the three tiers specific enough to act on?
      ("write good code" in Always = P1 too vague)

### 4D — SPEC.md alignment
- [ ] Does the tech stack match SPEC.md? (mismatch = P0)
- [ ] Do architectural patterns support the spec's requirements? (gap = P1)
- [ ] Are there requirements in SPEC.md that have no architectural pattern? (gap = P1)

### 4E — Performance and security
- [ ] Are performance expectations defined? (missing = P2)
- [ ] Are security requirements stated? (missing = P1 for any user-facing system)
- [ ] Are authentication/authorisation patterns defined? (missing = P0 if auth required)

---

## Step 5 — Audit FEATURE_SPEC.md

**Skip if no FEATURE_SPEC.md exists.**

Read the FEATURE_SPEC.md for the current feature.
Check against the `# FEATURE_SPEC_RUBRIC.md` section inside `references/SPEC_RUBRIC.md`.

### 5A — Acceptance criteria
- [ ] Every task has acceptance criteria (missing = P0)
- [ ] Every criterion is testable (untestable = P1)
- [ ] Error states are covered on every user-facing task (missing = P1)
- [ ] Edge cases are covered on critical paths (missing = P1)

### 5B — Scope boundary
- [ ] Does FEATURE_SPEC.md define what is explicitly OUT of scope? (missing = P1)
- [ ] Does it contradict anything in SPEC.md? (contradiction = P0)
- [ ] Does it introduce a new pattern not in ARCHITECTURE.md? (undocumented pattern = P1)

### 5C — Task quality
- [ ] Every task has a Touches field listing specific files (missing = P1)
- [ ] Every task has a Dependencies field (missing = P1)
- [ ] Every task is scoped to a single file or concern (multi-file sprawl = P1)
- [ ] Task sizes are estimated (S/M/L) (missing = P2)

---

## Step 6 — Cross-document consistency check

Check for contradictions across all documents that exist.

**BRIEF.md ↔ SPEC.md:**
- Does SPEC.md scope match BRIEF.md's v1 definition? (mismatch = P0)
- Do SPEC.md success criteria satisfy BRIEF.md's success criteria? (gap = P1)

**SPEC.md ↔ ARCHITECTURE.md:**
- Does the tech stack match? (mismatch = P0)
- Do architectural constraints allow the spec's requirements? (conflict = P0)

**AGENT_ARCH.md ↔ SPEC.md:**
- Does every agent's output map to a SPEC.md requirement? (orphaned agent = P1)
- Does every SPEC.md requirement that needs an agent have one? (missing agent = P0)

**AGENT_ARCH.md ↔ ARCHITECTURE.md:**
- Does the agent framework match the stated stack? (mismatch = P0)
- Do agent patterns conflict with architectural conventions? (conflict = P1)

---

## Step 7 — Score and present findings

Read `references/SPEC_REVIEW_REPORT.md` for the output format.

**Severity definitions:**
- **P0 — Critical:** Will cause build failure, agent confusion, or unverifiable output.
  The agent literally cannot build the right thing without this information.
- **P1 — Warning:** Will likely cause rework, drift, or quality issues.
  Important to fix, but build can proceed with user's explicit acknowledgment.
- **P2 — Note:** Minor gap. Low risk. Fix when convenient.

**Present findings clearly:**

```
SPEC REVIEW — [Project Name] — [trigger source]
══════════════════════════════════════════════

Documents audited: [list]
Documents missing: [list or "none"]

FINDINGS

P0 — Critical ([N] found)
────────────────────────
[If none: "None — no critical gaps found ✅"]

  P0-001 · [Document] · [Section]
  ──────────────────────────────
  Issue:   [Exactly what is wrong — specific, not vague]
  Why:     [What will go wrong in the build if this isn't fixed]
  Fix:     [Specific action — what to add/change/remove]
  Example: [If helpful — show what good looks like]

  [Repeat per P0]

P1 — Warnings ([N] found)
─────────────────────────
[If none: "None ✅"]

  P1-001 · [Document] · [Section]
  Issue:   [What is weak or missing]
  Fix:     [Specific action]

  [Repeat per P1 — grouped by document]

P2 — Notes ([N] found)
──────────────────────
  [Inline list — one line each]
  · [Document] — [issue] — [quick fix]

O'REILLY SIX CORE AREAS
────────────────────────
  Commands:         [✅ / ⚠️ partial / ❌ missing]
  Testing:          [✅ / ⚠️ / ❌]
  Project structure:[✅ / ⚠️ / ❌]
  Code style:       [✅ / ⚠️ / ❌]
  Git workflow:     [✅ / ⚠️ / ❌]
  Boundaries:       [✅ / ⚠️ / ❌]

CROSS-DOCUMENT CONSISTENCY
───────────────────────────
  [✅ No contradictions found]
  [or list each contradiction as P0/P1]

VERDICT
───────
  [✅ SPEC READY — 0 P0 findings. Proceed to [next step].]
  [⚠️  SPEC HAS WARNINGS — 0 P0, [N] P1 findings above.]
  [🔴 SPEC HAS CRITICAL GAPS — [N] P0 findings. See above.]

[If P0 or P1 found:]
  Fix issues above, or say "continue anyway" to proceed
  with findings logged to vibe/spec-reviews/[date].md.
  Say "fix [P0-001]" to fix a specific finding now.
```

**Wait for user response** — except in autonomous mode (below).

### Autonomous mode — fix, re-review, then decide

When `vibe_state.py mode` reports `vibe_mode: autonomous`, don't wait:

1. Apply fixes for **every P0 and P1** finding to the source documents — the smallest
   change that resolves each one, following the finding's intent (the "fix all" path
   below, without per-fix confirmation).
2. Re-run this review from Step 2 over the same scope and write a fresh report.
3. Repeat at most **2 fix rounds**.
4. Then: **0 P0** → log the remaining P1/P2 as usual and return to the calling skill.
   **P0s still open** → write
   `python3 ~/.claude/skills/vibe-mode/scripts/vibe_state.py run-state set --status needs_human --reason "spec review: [N] P0 still open after 2 fix rounds" --next "see vibe/spec-reviews/[report]"`
   and stop — a spec with critical gaps must not be built.

Record the rounds in the DECISIONS.md entry (`Action: fixed autonomously — [N] rounds`).
Spec-review never sets the spec **gate** itself — the calling skill (vibe-new-app Step
10S) records the sign-off once the plan is final.

---

## Step 8 — Handle user response

### "continue anyway" or "proceed"
Log all findings to `vibe/spec-reviews/[YYYY-MM-DD]-[trigger].md`.
Update `vibe/TASKS.md` with a note:
```
⚠️ Spec review findings logged — [N] P0, [N] P1 unresolved
   See: vibe/spec-reviews/[date]-[trigger].md
```
Return control to the calling skill.
Do not block. Do not repeat findings.

### "fix [finding ID]" or "fix all P0s"
For each named finding — apply the fix from the Fix field.
Modifies the relevant document (BRIEF.md / AGENT_ARCH.md / SPEC.md / ARCHITECTURE.md).
After fixing: re-run only the affected check. Show updated result.
If all P0s resolved: announce "P0 findings resolved — spec is ready."

### "fix all"
Work through every P0 and P1 fix in order.
Show each fix before applying it. Apply after confirmation.
Re-run full review at the end.

### No response / just proceeds
Return control to calling skill with findings summary in one line:
```
[spec-review: N P0, N P1 found — logged to vibe/spec-reviews/]
```

---

## Step 9 — Write the review file

Save findings to `vibe/spec-reviews/[YYYY-MM-DD]-[trigger-source].md`
regardless of whether fixes were applied.

Format: full report from Step 7.

Update `vibe/DECISIONS.md`:
```
---
## [date] — Spec review: [trigger source]
> P0: [N] · P1: [N] · P2: [N]
> Action: [fixed / continued with warnings / fully resolved]
> Report: vibe/spec-reviews/[date]-[trigger].md
---
```

---

## Absolute rules

**Never modifies the reviewed documents unless the user explicitly says "fix [finding]".**
Its own report and DECISIONS.md entry are always written.
The default action is always to report and wait. Never silently modify a spec.

**Every finding must be specific.**
"The spec is vague" is not a finding.
"SPEC.md line 14: 'users should have a good experience' — untestable, no measurable criterion" is a finding.

**P0 severity is reserved for build-breaking gaps only.**
Do not inflate findings. A missing code style section is P1, not P0.
Reserve P0 for: missing users, untestable success criteria, stack mismatch,
missing VerifierAgents, multi-writer state, missing auth pattern on auth system.

**Never repeat findings the user has acknowledged.**
Once the user says "continue anyway", the findings are logged and closed.
Do not surface them again in the same session.

**Cross-document consistency always runs.**
Even if individual document checks are clean, contradictions between documents
are where the most dangerous gaps hide. Never skip Step 6.
