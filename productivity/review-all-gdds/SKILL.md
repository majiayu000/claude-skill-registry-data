---
name: review-all-gdds
description: "Use this skill when all MVP module CDDs need a cross-document review for dependency, ownership, formula, scenario, and design coherence before architecture begins."
argument-hint: "[focus: full | consistency | design-theory | since-last-review]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Bash, AskUserQuestion, Task
model: opus
---

## Scope, evidence and effects

Read `standards/evidence-lifecycle.md` and `standards/notes-adr-sync.md` from the
project root. Reuse explicit existing authorization for its named paths, effects
and limits across roles and retries. Present unresolved material choices or new
effects for approval; a document/batch/synchronization authorization does not
require another question for each covered section or file. Content agreement,
write authority, independent review, ADR acceptance and workflow completion
remain separate.

Analysis defaults to read-only: no write entrypoint, input edits, status/index/
session/Memory Bank updates. Report-only may write one new assigned report with
authority; report approval does not authorize indexes or rolling logs. Other
writes need the named path/effect in existing authority or a concrete draft and
changeset approval. Unknown paths are findings, not permission to create them.
No Memory Bank means use the established report/conversation fallback. Next
steps are recommendations; execute only effects already authorized or explicitly
selected by the user. Tool availability determines the question interface.

Bind claims to a declared scope and minimum direct/indirect evidence closure:
record original paths, full SHA-256, byte sizes, source commit plus exact diff
and uncommitted/ignored/external identities, exclusions and recoverable originals.
Do not read sensitive local settings or secrets merely to complete discovery.
Read required inputs back from their actual paths, verify closure and report
missing inputs as incomplete affected checks. Keywords, timestamps, counts,
equal hashes at two collections and static checks do not certify semantic review,
continuous unchanged history, runtime behavior or independent approval.

Classify meaningful choices with the shared disposition record (`cdd-layer`,
`no-adr`, `covered`, `documentation-update`, `adr-required`, `conflict`). Significant
trust, public contract, durable format or state ownership changes require an
Accepted ADR/valid scoped exception before affected implementation continues.
Keep As-Is observations and their evidence separate from Target promises and
gaps; implemented behavior cannot lower a governing Target. Continue independent
work while blocking only affected dependants.

## User Guide

- When to use: Holistic cross-CDD consistency and design review. Reads all module CDDs simultaneously and checks for contradictions between them, stale references, ownership conflicts, and design theory issues. Supports both game and general product domains. Run after all MVP CDDs are written, before architecture begins.
- Inputs: Command arguments: `/review-all-gdds [focus: full | consistency | design-theory | since-last-review]`; project artifacts referenced below; user decisions and approvals before writes.
- Outputs: Primary artifacts, reports, or conversation guidance described below; write files only after user approval.
- Memory-bank writes: Only with initialized Memory Bank and separately authorized review-index effect; none in read-only/report-only.
- Next steps: Follow the workflow hand-off or next-step guidance below; recommendations do not auto-run and require explicit user command/approval.

# Review All CDDs

This skill reads every system CDD simultaneously and performs two complementary
reviews that cannot be done per-CDD in isolation:

1. **Cross-CDD Consistency** — contradictions, stale references, and ownership
   conflicts between documents
2. **Design Holism** — issues that only emerge when you see all systems
   together: dominant strategies or paths, economy or data-flow imbalances,
   cognitive overload, principle drift, and competing progression or value loops

**This is distinct from `/design-review`**, which reviews one CDD for internal
completeness. This skill reviews the *relationships* between all CDDs.

**When to run:**
- After all MVP-tier CDDs are individually approved
- After any CDD is significantly revised mid-production
- Before `/create-architecture` begins (architecture built on inconsistent CDDs
  inherits those inconsistencies)

**Argument modes:**

**Focus:** `$ARGUMENTS[0]` (absent = `full`)

Validate before spawn/write/verdict: only `full`, `consistency`,
`design-theory` and `since-last-review` are legal focus values. Reject unknown
focus, additional selectors and unknown explicit flags with a corrective error
and usage `/review-all-gdds [full|consistency|design-theory|since-last-review]`.
Do not silently default an invalid supplied argument.

- **No argument / `full`**: Both consistency and design theory passes
- **`consistency`**: Cross-CDD consistency checks only (faster)
- **`design-theory`**: Domain-appropriate design holism checks only
- **`since-last-review`**: Incremental review from an exact prior bound baseline,
  including changed required dependencies; it is not a new Full review.

---

## Phase 1: Load Everything

### Phase 1a — L0: Summary Scan (fast, low tokens)

Before reading any full document, use Grep to extract `## Summary` sections
from all CDD files:

```
Grep pattern="## Summary" glob="design/cdd/*.md" output_mode="content" -A 5
```

Display a manifest to the user:
```
Found [N] CDDs. Summaries:
  • combat.md — [summary text]
  • inventory.md — [summary text]
  ...
```

For `since-last-review`, compare the prior review's exact input manifest and
retained bytes with current commit+diff, staged/unstaged, untracked/ignored and
external inputs. Include changed direct/indirect dependencies and affected
relationships, not only CDD filenames. Mtime/report creation date/git log cannot
be the baseline. If the baseline is unavailable, offer a new Full review or
explicitly narrower current-scope review; never claim no changes from missing
history.

Declare the exact set, exclusions and reading coverage before L1. Full reads
every module CDD and required closure for the declared project/module scope.
`consistency`/`design-theory` are focused claims even when every scoped file is
read. Incremental findings bind old/new identities and say which prior checks
were reused. Same-byte continuation resumes an interrupted review only when the
exact input/rule/dependency scope matches; it is neither incremental review of
changes nor proof of a completed new Full review. Historical review reports
retain their original scope and actors.


### Phase 1b — Registry Pre-Load (fast baseline)

Before full-reading any CDD, check for the entity registry:

```
Read path="design/registry/entities.yaml"
```

If the registry exists and has entries, use it as a **pre-built conflict**
baseline**: known entities, items, formulas, and constants with their**
authoritative values and source CDDs. In Phase 2, grep CDDs for registered
names first — this is faster than reading all CDDs in full before knowing
what to look for.

If the registry is empty or absent: proceed without it. Note in the report:
"Entity registry is empty — consistency checks rely on full CDD reads only.
Registry additions can be proposed through /design-system with authority;
/consistency-check does not populate it as a review side effect."

### Phase 1c — L1/L2: Full Document Load

Full-read the in-scope documents:

1. `design/cdd/game-concept.md` or `design/cdd/product-concept.md` — project vision, core loop/journey, MVP definition
2. `design/cdd/game-pillars.md` or `design/cdd/principles.md` if either exists — design pillars/principles and anti-pillars
3. `design/cdd/module-index.md` — authoritative system list, layers, dependencies, status
4. **Every in-scope system CDD in `design/cdd/`** — read completely (skip
   game-concept.md, product-concept.md, and module-index.md — those are read above)

Report actual full-reading closure, semantic eight-role coverage for module
CDDs under `design/INSTRUCTIONS.md`, concept context under its actual template
owner, inaccessible dependencies and specialist completion.
Summaries/grep/counts discover inputs; they do not qualify Full semantic review.
Report: "Loaded [N] system CDDs covering [M] systems. Pillars: [list]. Anti-pillars: [list]."

If fewer than 2 system CDDs exist, stop:
> "Cross-CDD review requires at least 2 system CDDs. Write more CDDs first,
> then re-run `/review-all-gdds`."

---

### Parallel Execution

Phase 2 (Consistency) and Phase 3 (Design Theory) are independent — they read
the same CDD inputs but produce separate reports. Spawn both as parallel Task
agents simultaneously rather than waiting for Phase 2 to complete before
starting Phase 3. Collect both results before writing the combined report.

---

**Domain detection.** The module set reveals the domain. [Game] game modules; [Product] product modules.

## Phase 2: Cross-CDD Consistency

Work through every pair and group of CDDs to find contradictions and gaps.

### 2a: Dependency Bidirectionality

For every CDD's Dependencies section, check that every listed dependency is
reciprocal:
- If CDD-A lists "depends on CDD-B", check that CDD-B lists CDD-A as a dependent
- If CDD-A lists "depended on by CDD-C", check that CDD-C lists CDD-A as a dependency
- Flag any one-directional dependency as a consistency issue

```
⚠️  Dependency Asymmetry
[system-a].md lists: Depends On → [system-b].md
[system-b].md does NOT list [system-a].md as a dependent
→ One of these documents has a stale dependency section
```

### 2b: Rule Contradictions

For each game rule, mechanic, or constraint defined in any CDD, check whether
any other CDD defines a contradicting rule for the same situation:

Categories to scan:
- **Floor/ceiling rules**: Does any CDD define a minimum value for an output? Does any other say a different system can bypass that floor? These contradict.
- **Resource ownership**: If two CDDs both define how a shared resource accumulates or depletes, do they agree?
- **State transitions**: If CDD-A describes what happens when a character dies,
  does CDD-B's description of the same event agree?
- **Timing**: If CDD-A says "X happens on the same frame", does CDD-B assume
  it happens asynchronously?
- **Stacking rules**: If CDD-A says status effects stack, does CDD-B assume
  they don't?

```
🔴 Rule Contradiction
[system-a].md: "Minimum [output] after reduction is [floor_value]"
[system-b].md: "[mechanic] bypasses [system-a]'s rules and can reduce [output] to 0"
→ These rules directly contradict. Which CDD is authoritative?
```

### 2c: Stale References

For every cross-document reference (CDD-A mentions a mechanic, value, or
system name from CDD-B), verify the referenced element still exists in CDD-B
with the same name and behaviour:

- If CDD-A says "combo multiplier from the combat system feeds into score", check
  that the combat CDD actually defines a combo multiplier that outputs to score
- If CDD-A references "the progression curve defined in [system].md", check that
  [system].md actually has that curve, not a different progression model
- If CDD-A was written before CDD-B and assumed a mechanic that CDD-B later
  designed differently, flag CDD-A as containing a stale reference

```
⚠️  Stale Reference
inventory.md (written first): "Item weight uses the encumbrance formula
  from movement.md"
movement.md (written later): Defines no encumbrance formula — uses a flat
  carry limit instead
→ inventory.md references a formula that doesn't exist
```

### 2d: Data and Tuning Knob Ownership Conflicts

Two CDDs should not both claim to own the same data or tuning knob. Scan all
Tuning Knobs sections across all CDDs and flag duplicates:

```
⚠️  Ownership Conflict
[system-a].md Tuning Knobs: "[multiplier_name] — controls [output] scaling"
[system-b].md Tuning Knobs: "[multiplier_name] — scales [output] with [factor]"
→ Two CDDs define multipliers on the same output. Which owns the final value?
  This will produce either a double-application bug or a design conflict.
```

### 2e: Formula Compatibility

For CDDs whose formulas are connected (output of one feeds input of another),
check that the output range of the upstream formula is within the expected
input range of the downstream formula:

- If [system-a].md outputs values between [min]–[max], and [system-b].md is
  designed to receive values between [min2]–[max2], is the mismatch intentional?
- If an economy CDD expects resource acquisition in range X, and the
  progression CDD generates it at range Y, the economy will be trivial or
  inaccessible — is that intended?

Flag incompatibilities as CONCERNS (design judgment needed, not necessarily wrong):

```
⚠️  Formula Range Mismatch
[system-a].md: Max [output] = [value_a] (at max [condition])
[system-b].md: Base [input] = [value_b], max [input] = [value_c]
→ Late-[stage] [scenario] can resolve in a single [event].
  Is this intentional? If not, either [system-a]'s ceiling or [system-b]'s ceiling needs adjustment.
```

### 2f: Acceptance Criteria Cross-Check

Scan Acceptance Criteria sections across all CDDs for contradictions:

- CDD-A criteria: "Player cannot die from a single hit"
- CDD-B criteria: "Boss attack deals 150% of player max health"
These acceptance criteria cannot both pass simultaneously.

---

## Phase 3: Design Holism

Read [design holism checks](references/design-holism.md) before assessing the combined module set. Apply every subsection relevant to the detected domain and record non-applicable checks explicitly rather than silently dropping them.

## Phase 4: Cross-Module Scenario Walkthrough

Walk through the project from the user's perspective.

Walk through the project from the user's perspective to find problems that only
appear at the interaction boundary between multiple modules — things static
analysis of individual CDDs cannot surface.

### 4a: Identify Key Multi-Module Moments

Scan all CDDs and identify the 3–5 most important moments where
multiple modules activate simultaneously.

**[游戏专用]** Look specifically for:
- **Combat + Economy overlap**: killing enemies that drop resources, spending
  resources during combat, death/respawn interacting with economy state
- **Progression + Difficulty overlap**: level-up triggering mid-fight, ability
  unlocks changing combat viability, difficulty scaling at progression milestones
- **Narrative + Gameplay overlap**: dialogue choices locking/unlocking mechanics,
  story beats interrupting resource loops, quest completion triggering system
  state changes
- **3+ system chains**: any player action that triggers System A, which feeds
  into System B, which triggers System C (these are highest-risk interaction paths)

**[通用产品]** Look specifically for:
- **API + Auth overlap**: request hitting auth middleware, token refresh mid-request, rate limiting per-user vs per-IP, permission check cascading across microservices
- **Frontend + Backend overlap**: SSR vs CSR data freshness, optimistic updates vs server state, error boundary cascade, form validation on both client and server
- **Data pipeline + Storage overlap**: ETL failure mid-write, schema migration during active ingestion, stale reads after write, cache invalidation during bulk updates
- **3+ module chains**: any user action that triggers Module A, which feeds into Module B, which triggers Module C (these are highest-risk interaction paths)

List each identified scenario with a one-line description before proceeding.

### 4b: Walk Through Each Scenario

For each scenario, step through the sequence explicitly:

1. **Trigger** — what user action or event starts this?
2. **Activation order** — which modules activate, in what sequence?
3. **Data flow** — what does each module output, and is that output a valid
   input for the next module in the chain?
4. **User experience** — **[游戏专用]** what does the player see, hear, or feel at each step? **[通用产品]** what does the user see in the UI, what API response do they get, what latency do they experience?
5. **Failure modes** — are there any of the following?
   - **Race conditions**: two modules trying to modify the same state simultaneously
   - **Feedback loops**: Module A amplifies Module B which re-amplifies Module A
     with no cap or dampener
   - **Broken state transitions**: a module assumes a state that a previous
     module may have changed (e.g., "user is authenticated" assumption after an auth
     step that could have caused a session expiry)
   - **Contradictory messaging**: **[游戏专用]** player receives conflicting feedback from two systems (e.g., "success" sound + "failure" UI). **[通用产品]** user receives conflicting signals (e.g., HTTP 200 OK body with error message, success toast over a failed form submission)
   - **Compounding load spikes**: **[游戏专用]** two systems both scaling up at the same progression point. **[通用产品]** two features both triggering heavy queries at the same workflow point, multiplying the intended load
   - **Double-processing**: two modules both reacting to the same trigger with
     side effects that together exceed the intended behavior (e.g., duplicate event processing, double-send of notifications)
   - **Undefined behavior**: the CDDs don't specify what happens in this combined
     state (neither module's rules cover it)

**[游戏专用]** Example walkthrough:
```
Scenario: Player kills elite enemy at level-up threshold during active quest

Trigger: Player lands killing blow on elite enemy
→ combat.md: awards kill XP (100 pts)
→ progression.md: XP total crosses level threshold → triggers level-up
  Output: new level, stat increases, ability unlock popup
→ quest.md: kill-count criterion met → triggers quest completion event
  Output: quest reward XP (500 pts), completion fanfare
→ progression.md (again): quest XP added → triggers SECOND level-up in same frame
  ⚠️  Data flow issue: quest.md awards XP without checking if a level-up
  is already in progress. progression.md has no guard against concurrent
  level-up events. Undefined behavior: does the player level up once or twice?
  Does the ability popup fire twice? Does the second level use the updated or
  pre-update stat baseline?
```

**[通用产品]** Example walkthrough:
```
Scenario: User submits order during auth token refresh with payment processing

Trigger: User clicks "Place Order" while a background token refresh is in flight
→ auth.md: token refresh in progress (async, ~200ms remaining)
→ order.md: receives order submission, reads current (stale) auth token
→ payment.md: receives payment request with stale token
  Output: payment gateway returns 401 — token expired during processing
→ order.md: order state is "payment_pending" but payment failed
  ⚠️  Data flow issue: order.md doesn't verify auth token freshness before
  calling payment. auth.md doesn't expose a "refresh in progress" signal.
  Undefined behavior: is the order in "payment_pending" or "payment_failed"?
  Does the user see a success confirmation or an error? Can they retry?
```

### 4c: Flag Scenario Issues

For each problem found during the walkthrough, categorize severity:

- **BLOCKER**: undefined behavior, broken state transition, or contradictory
  user messaging — the experience is broken or incoherent in this scenario
- **WARNING**: compounding spikes, feedback loops without caps, double-processing —
  the experience works but produces unintended outcomes
- **INFO**: minor ordering ambiguity or messaging overlap — worth noting but
  unlikely to cause user-visible problems

Add all findings to the output report under **"Cross-Module Scenario Issues"**.
Each finding must cite: the scenario name, the specific modules involved, the
step where the issue occurs, and the nature of the failure mode.

---

## Phase 5: Output the Review Report

```
## Cross-CDD Review Report
Date: [date]
CDDs Reviewed: [N]
Systems Covered: [list]

---

### Consistency Issues

#### Blocking (must resolve before architecture begins)
🔴 [Issue title]
[What CDDs are involved, what the contradiction is, what needs to change]

#### Warnings (should resolve, but won't block)
⚠️  [Issue title]
[What CDDs are involved, what the concern is]

---

### Design Holism Issues

#### Blocking
🔴 [Issue title]
[What the problem is, which CDDs are involved, design recommendation]

#### Warnings
⚠️  [Issue title]
[What the concern is, which CDDs are affected, recommendation]

---

### Cross-System Scenario Issues

Scenarios walked: [N]
[List scenario names]

#### Blockers
🔴 [Scenario name] — [Systems involved]
[Step where failure occurs, nature of the failure mode, what must be resolved]

#### Warnings
⚠️  [Scenario name] — [Systems involved]
[What the unintended outcome is, recommendation]

#### Info
ℹ️  [Scenario name] — [Systems involved]
[Minor ordering ambiguity or note]

---

### CDDs Flagged for Revision

| CDD | Reason | Type | Priority |
|-----|--------|------|----------|
| [system-a].md | Rule contradiction with [system-b].md | Consistency | Blocking |
| [system-c].md | Stale reference to nonexistent mechanic | Consistency | Blocking |
| [system-d].md | No pillar alignment | Design Theory | Warning |

---

### Verdict: [PASS / CONCERNS / FAIL]

PASS: No blocking issues. Warnings present but don't prevent architecture.
CONCERNS: Warnings present that should be resolved but are not blocking.
FAIL: Required issues block named affected architecture/dependants; continue
independent work. Missing required review/input is incomplete, not fabricated PASS.

### If FAIL — required actions before re-running:
[Specific list of what must change in which CDD]
```

---

## Phase 6: Write Report and Flag CDDs

Reuse existing authority for the new assigned report. If absent, show findings
and use `AskUserQuestion` (when available) for its exact path/effect:
- Prompt: "May I write this review to `design/cdd/cross-review-[date].md`?"
- Options: `[A] Yes — write the report` / `[B] No — skip`

When `memory_bank/` exists, update
`memory_bank/t3_archive/reviews/review-index.md` only if its separate path/effect
is authorized. A report-only run never updates this index.

Update the Memory Bank index only when this run enters its separately named, authorized effect after saving the actual report. Initialized Memory Bank alone is insufficient; read-only and report-only scopes exclude indexing. If the intended effect or initialization is unresolved, retain Unknown. Before indexing, read the saved immutable report and exact input/evidence identities; a proposed output or INFO is insufficient. This effect does not initialize Memory Bank.

- Review Type: `cross-cdd-review`
- Source Artifact: `design/cdd/cross-review-[date].md`
- Use `Source Artifact` as the dedupe key.
- If the same source artifact already exists, update Date, Verdict, and
  Follow-up Owner instead of adding a duplicate row.
- If `memory_bank/` does not exist, do not create it from `/review-all-gdds`;
  use the authorized report/conversation fallback and disclose the absent
  optional index; initialization is not a review side effect.

If flagged CDD status updates are authorized, apply the concrete named changes.
Otherwise optionally request this separate effect with `AskUserQuestion`:
- Prompt: "Should I update the module index to mark these CDDs as needing revision? ([list of flagged CDDs])"
- Options: `[A] Yes — update module index` / `[B] No — leave as-is`
- If yes: update each flagged CDD's Status field in module-index.md to "Needs Revision".
  (Do NOT append parentheticals to the status value — other skills match "Needs Revision"
  as an exact string and parentheticals break that match.)

### Session State Update

Only if separately authorized (never in report-only), append the following
progress to `production/session-state/active.md`:

    ## Session Extract — /review-all-gdds [date]
    - Verdict: [PASS / CONCERNS / FAIL]
    - CDDs reviewed: [N]
    - Flagged for revision: [comma-separated list, or "None"]
    - Blocking issues: [N — brief one-line descriptions, or "None"]
    - Recommended next: [the Phase 7 handoff action, condensed to one line]
    - Report: design/cdd/cross-review-[date].md

Create `active.md` only if creation is authorized. Otherwise keep progress in
conversation. Confirm only actual effects.

---

## Phase 7: Handoff

After actual authorized effects, recommend applicable next steps. Use a closing
question when a new action/choice is needed; no next workflow auto-runs.

Before building options, check project state:
- Are there any Warning-level items that are simple edits (flagged with "30-second edit", "brief addition", or similar)? → offer inline quick-fix option
- Are any CDDs in the "Flagged for Revision" table? → offer /design-review option for each
- Read module-index.md for the next system with Status: Not Started → offer /design-system option
- Is the verdict PASS or CONCERNS? → offer /gate-check or /create-architecture

Build the option list dynamically — only include options that apply:

**Option pool:**
- `[_] Apply quick fix: [W-XX description] in [cdd-name].md — [effort estimate]` (one option per simple-edit warning; only for Warning-level, not Blocking)
- `[_] Run /design-review [flagged-cdd-path] — address flagged warnings` (one per flagged CDD, if any)
- `[_] Run /design-system [next-system] — next in design order` (include only if an actual undesigned system remains)
- `[_] Run /create-architecture — begin architecture (verdict is PASS/CONCERNS)` (include if verdict is not FAIL)
- `[_] Run /gate-check — validate Systems Design phase gate` (include if verdict is PASS)
- `[_] Stop here`

Assign letters A, B, C… only to included options. Mark the most pipeline-advancing option as `(recommended)`.

Never end the skill with plain text. Always close with this widget.

---

## Error Recovery Protocol

If any spawned agent returns BLOCKED, errors, or fails to complete:

1. **Surface immediately**: Report "[AgentName]: BLOCKED — [reason]" before continuing
2. **Assess dependencies**: If the blocked agent's output is required by a later phase, do not proceed past that phase without user input
3. **Offer options** via AskUserQuestion with three choices:
   - Skip this agent and note the gap in the final report
   - Retry with narrower scope (fewer CDDs, single-system focus)
   - Stop here and resolve the blocker first
4. **Always produce a partial report** — output whatever was completed so work is not lost

---

## Collaborative Protocol

1. **Read silently** — load all CDDs before presenting anything
2. **Show everything** — present the full consistency and design theory analysis
   before asking for any action
3. **Distinguish blocking from advisory** — not every issue needs to block
   architecture; be clear about which do
4. **Don't make design decisions** — flag contradictions and options, but never
   unilaterally decide which CDD is "right"
5. **Ask before writing** — confirm before writing the report or updating the
   module index
6. **Be specific** — every issue must cite the exact CDD, section, and text
   involved; no vague warnings
