---
name: prototype
description: "Rapid prototyping workflow. Skips normal standards to quickly validate a game concept, mechanic, product feature, API contract, or technology choice. Produces throwaway code and a structured prototype report."
argument-hint: "[concept-description] [--review full|lean|solo]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Edit, Bash, Task
agent: prototyper
isolation: worktree
---

## User Guide

- When to use: Rapid prototyping workflow. Skips normal standards to quickly validate a game concept, mechanic, product feature, API contract, or technology choice. Produces throwaway code and a structured prototype report.
- Inputs: Command arguments: `/prototype [concept-description] [--review full|lean|solo]`; project artifacts referenced below; user decisions and approvals before writes.
- Outputs: Primary artifacts, reports, or conversation guidance described below; write files only after user approval.
- Memory-bank writes: `memory_bank/t3_archive/reviews/review-index.md`.
- Next steps: Follow the workflow hand-off or next-step guidance below; recommendations do not auto-run and require explicit user command/approval.

## Phase 0: Domain Detection

Read `standards/technical-preferences.md`, existing scoped domain decisions,
and the substantive bodies of any `design/cdd/game-concept.md` and
`design/cdd/product-concept.md` before selecting a branch. Filenames, placeholder
or copied concept text and shared extensions do not establish a domain. Read
actual configured values in `Product Stack` or the populated legacy
`Language & Framework`, `Platform & Deployment`, and `Agent Routing` /
`File Extension Routing`
sections in their owning domain context; missing new sections or a concept do
not erase configured legacy Product facts. A placeholder Game concept does not
override a configured Product.

Resolve Game from consistent substantive Game concept/decision or actual
configured engine/domain and Game behavior evidence; resolve Product from
consistent substantive Product concept/decision or actual Product configuration.
Two substantive concepts, conflicting concept/configuration values or mixed scope
leave the affected branch **Unknown** until a scoped decision resolves the conflict.
With no consistent substantive concept/scoped decision or sufficient actual
configuration evidence, the domain is also Unknown; a valid concept alone can
establish the domain before stack configuration.
Record the supporting sections and values. For Unknown, use an existing matching
scoped decision or clarify with the user/configured project lead before
domain-specific delegation or writes; resolved configured facts need no new vote.
Independent neutral reads may continue. Domain selection does not waive required
branch inputs: read their actual originals and leave missing inputs Incomplete.
Never silently default to Game.

Use `[Game]` or `[Product]` paths below only after that domain is resolved.

---

## Phase 1: Define the Question

Resolve the review mode (once, store for all gate spawns this run):
1. If `--review [full|lean|solo]` was passed → use that
2. Else read `production/review-mode.txt` → use that value
3. Else → default to `lean`

See `standards/director-gates.md` for the full check pattern.

Read the concept description from the argument. Identify the core question this prototype must answer. If the concept is vague, state the question explicitly before proceeding — a prototype without a clear question wastes time.

**[Game]** Focus: core mechanic feel, player experience, or technical feasibility of a gameplay system.
**[Product]** Focus: API contract viability, CLI workflow ergonomics, data pipeline behaviour, integration feasibility, or technology choice validation.

---

## Phase 2: Load Project Context

Read `CLAUDE.md` for project context and the current tech stack. Understand what engine, language, and frameworks are in use so the prototype is built with compatible tooling.

**[Game]** Read `design/cdd/game-concept.md` (if it exists) for game pillars and core fantasy.
**[Product]** Read `design/cdd/product-concept.md` (if it exists) for product principles and MVP scope.

---

## Phase 3: Select Prototype Type and Plan

**[Product]** Determine which prototype type fits the question:

| Type | Use When | Success Criteria |
|------|----------|-----------------|
| **API Spike** | Validating an API endpoint, contract, or protocol | Response shape is viable; latency is within budget; edge cases are understood |
| **CLI Spike** | Validating a CLI command interface or pipeline | Command ergonomics feel right; output is parseable; error messages are clear |
| **Data Pipeline Spike** | Validating a data transform, ETL step, or migration | Data fidelity is maintained; performance is acceptable; failure modes are known |
| **Workflow Prototype** | Validating a multi-step user workflow or integration | Each step is reachable; transitions are smooth; edge cases are handled |
| **Technology Spike** | Validating a library, framework, or infrastructure choice | API is usable for the intended purpose; performance/scale meets needs; no blocking limitations found |

**[Game]** the prototype type is implicitly the core mechanic or system being tested.

---

## Phase 4: Plan the Prototype

Define in 3-5 bullet points what the minimum viable prototype looks like:

- What is the core question?
- What is the absolute minimum code needed to answer it?
- What can be skipped (error handling, polish, architecture)?

**[Product]** Also define:
- What is the success threshold? (e.g., "API responds under 200ms p95", "CLI command completes in under 1s", "data transform preserves all 12 fields")
- What specific metrics will you collect?

Present this plan to the user before building. Ask for confirmation if scope seems unclear.

---

## Phase 5: Implement

Ask: "May I create the prototype directory at `prototypes/[concept-name]/` and begin implementation?"

If yes, create the directory. Every file must begin with:

```
// PROTOTYPE - NOT FOR PRODUCTION
// Question: [Core question being tested]
// Date: [Current date]
```

Standards are intentionally relaxed:

- Hardcode values freely
- **[Game]** Use placeholder assets
- Skip error handling
- Use the simplest approach that works
- Copy code rather than importing from production

Run the prototype. Observe behavior. Collect any measurable data.

**[Game]** Collect: frame times, interaction counts, feel assessments.
**[Product]** Collect: latency (p50/p95/p99), throughput, memory usage, error rates, iteration count.

---

## Phase 6: Generate Prototype Report

**[通用场景]** Draft the report using the template that matches the domain:

### [Game] Game Prototype Report Template

```markdown
## Prototype Report: [Concept Name]

### Hypothesis
[What we expected to be true -- the question we set out to answer]

### Approach
[What we built, how long it took, what shortcuts we took]

### Result
[What actually happened -- specific observations, not opinions]

### Metrics
[Any measurable data collected during testing]
- Frame time: [if relevant]
- Feel assessment: [subjective but specific -- "response felt sluggish at
  200ms delay" not "felt bad"]
- Player action counts: [if relevant]
- Iteration count: [how many attempts to get it working]

### Recommendation: [PROCEED / PIVOT / KILL]

[One paragraph explaining the recommendation with evidence]

### If Proceeding
[What needs to change for a production-quality implementation]
- Architecture requirements
- Performance targets
- Scope adjustments from the original design
- Estimated production effort

### If Pivoting
[What alternative direction the results suggest]

### If Killing
[Why this concept does not work and what we should do instead]

### Lessons Learned
[Discoveries that affect other systems or future work]
```

### [Product] Product Prototype Report Template

```markdown
## Prototype Report: [Concept Name]

### Hypothesis
[What we expected to be true -- the question we set out to answer]

### Method
[What we built — technology used, approach, time invested, shortcuts taken]

### Findings
[What actually happened — specific observations with evidence, not opinions]

### Metrics
[Any measurable data collected during testing]
- Latency (p50/p95/p99): [if API/CLI]
- Throughput: [if applicable]
- Memory usage: [if applicable]
- Error rate: [if applicable]
- Iteration count: [how many attempts to get it working]

### Success Threshold
- Threshold: [what qualified as success]
- Met? [YES / PARTIAL / NO]

### Recommendation: [PROCEED / PIVOT / KILL]

[One paragraph explaining the recommendation with evidence]

### If Proceeding
[What needs to change for a production-quality implementation]
- Architecture requirements
- Performance targets
- Scope adjustments from the original spec
- Estimated production effort

### If Pivoting
[What alternative direction the results suggest]

### If Killing
[Why this approach does not work and what we should do instead]

### Lessons Learned
[Discoveries that affect other systems or future work]
```

Ask: "May I write this report to `prototypes/[concept-name]/REPORT.md`?"

If yes, write the file.

If `memory_bank/` exists and the separately named index effect is authorized,
update `memory_bank/t3_archive/reviews/review-index.md` with the prototype decision
after saving the approved report.
Use `Source Artifact` as the dedupe key; if the same source artifact already
exists, update Date, Verdict, and Follow-up Owner instead of appending a
duplicate row.

Update the Memory Bank index only after the report is saved and only with authority
for that named index effect. Initialization alone, read-only scope and report-only
scope do not authorize it. If initialization or the intended effect is unresolved,
retain Unknown and leave the index unchanged. Before an authorized update, read
the saved immutable report revision and its exact input/evidence identities;
a proposed report or an INFO result is insufficient. This step does not initialize
Memory Bank.

Review index row:

- Review Type: `prototype-decision`
- Source Artifact: `prototypes/[concept-name]/REPORT.md`
- Verdict: `PROCEED`, `PIVOT`, or `KILL`
- Scope: prototype hypothesis or validated workflow
- Related Context: concept, CDD, or ADR path when available

Do not create `memory_bank/` from `/prototype`. If it does not exist, keep the
normal report behavior and tell the user to run `/constitute` to establish the
memory_bank governance control plane. T3 records decision evidence only;
prototype code stays isolated and is never promoted into production code.

---

## Phase 7: Review

**[Game] — Creative Director Review**

**Review mode check** — apply before spawning CD-PLAYTEST:
- `solo` → skip. Note: "CD-PLAYTEST skipped — Solo mode." Proceed to Phase 8 summary with the prototyper's recommendation as the final verdict.
- `lean` → skip (not a PHASE-GATE). Note: "CD-PLAYTEST skipped — Lean mode." Proceed to Phase 8 summary with the prototyper's recommendation as the final verdict.
- `full` → spawn as normal.

Spawn `creative-director` via Task using gate **CD-PLAYTEST** (`standards/director-gates.md`).

Pass: the full REPORT.md content, the original design question, game pillars and core fantasy from `design/cdd/game-concept.md` (if it exists).

The creative director evaluates the prototype result against the game's creative vision and pillars, then confirms, modifies, or overrides the prototyper's PROCEED / PIVOT / KILL recommendation. Their verdict is final. Update the REPORT.md `Recommendation` section if the creative director's verdict differs from the prototyper's.

**[Product] — Lead Programmer Review**

**Review mode check** — apply before spawning lead-programmer:
- `solo` → skip. Note: "Lead Programmer review skipped — Solo mode." Proceed to Phase 8 summary with the prototyper's recommendation as the final verdict.
- `lean` → skip. Note: "Lead Programmer review skipped — Lean mode." Proceed to Phase 8 summary with the prototyper's recommendation as the final verdict.
- `full` → spawn as normal.

Spawn `lead-programmer` via Task. Pass: the full REPORT.md content, the original design question, product principles from `design/cdd/product-concept.md` (if it exists), and technology stack from `standards/technical-preferences.md`.

The lead programmer evaluates the prototype result against the product's architecture and technology constraints, then confirms, modifies, or overrides the prototyper's PROCEED / PIVOT / KILL recommendation. Their verdict is final. Update the REPORT.md `Recommendation` section if the lead programmer's verdict differs from the prototyper's.

---

## Phase 8: Summary and Next Steps

Output a summary to the user: the core question, the result, the prototyper's initial recommendation, and the reviewer's final decision. Link to the full report at `prototypes/[concept-name]/REPORT.md`.

**[Game]** If **PROCEED**: run `/design-system` to begin the production CDD for this mechanic, or `/architecture-decision` to record key technical decisions before implementation.

**[Product]** If **PROCEED**: run `/architecture-decision` to record key technical decisions, then `/create-epics` to create an epic from the validated approach, then `/create-stories [epic-slug]` to break it into implementable stories.

If **PIVOT** or **KILL**: no further action needed — the prototype report is the deliverable.

Verdict: **COMPLETE** — prototype finished. Recommendation is PROCEED, PIVOT, or KILL based on findings above.

### Important Constraints

- Prototype code must NEVER import from production source files
- Production code must NEVER import from prototype directories
- If the recommendation is PROCEED, the production implementation must be written from scratch — prototype code is not refactored into production
- Total prototype effort should be timeboxed to 1-3 days equivalent of work
- If the prototype scope starts growing, stop and reassess whether the question can be simplified

---

## Recommended Next Steps

**[Game]**
- **If PROCEED**: Run `/design-system [mechanic]` to author the production CDD, or `/architecture-decision` to record key technical decisions before implementation
- **If PIVOT**: Run `/prototype [revised-concept]` to test the adjusted direction
- **If KILL**: No further action required — the prototype report is the deliverable
- Run `/playtest-report` to formally document any playtest sessions conducted during prototyping

**[Product]**
- **If PROCEED**: Run `/architecture-decision [title]` to record key technical decisions, then `/create-epics` to create an epic from the validated approach, then `/create-stories [epic-slug]` to break it into implementable stories
- **If PIVOT**: Run `/prototype [revised-concept]` to test the adjusted direction
- **If KILL**: No further action required — the prototype report is the deliverable
