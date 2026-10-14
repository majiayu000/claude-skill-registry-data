---
name: prove-fix
description: '[Code Quality] Use when you need to prove fix correctness with adversarial code proof traces — a skeptic tries to DISPROVE the fix and trace all related paths first, with confidence scoring and stack-trace-style evidence chains, so confidence is earned by surviving attack, not by confirming it works.'
---

> Codex compatibility note:
>
> - Invoke repository skills with `$skill-name` in Codex; this mirrored copy rewrites legacy Claude `/skill-name` references.
> - Task tracker mandate: BEFORE executing any workflow or skill step, create/update task tracking for all steps and keep it synchronized as progress changes.
> - User-question prompts mean to ask the user directly in Codex.
> - Ignore Claude-specific mode-switch instructions when they appear.
> - Strict execution contract: when a user explicitly invokes a skill, execute that skill protocol as written.
> - Subagent authorization: when a skill is user-invoked or AI-detected and its protocol requires subagents, that skill activation authorizes use of the required `spawn_agent` subagent(s) for that task.
> - Do not skip, reorder, or merge protocol steps unless the user explicitly approves the deviation first.
> - For workflow skills, execute each listed child-skill step explicitly and report step-by-step evidence.
> - If a required step/tool cannot run in this environment, stop and ask the user before adapting.

<!-- CODEX:PROJECT-REFERENCE-LOADING:START -->

## Codex Project-Reference Loading (No Hooks)

Codex uses static project-reference loading instead of runtime-injected project docs.
When coding, planning, debugging, testing, or reviewing, open project docs explicitly using this routing.

**Always read:**

- `docs/project-config.json` (project-specific paths, commands, modules, and workflow/test settings)
- `docs/project-reference/docs-index-reference.md` (routes to the full `docs/project-reference/*` catalog)
- `docs/project-reference/lessons.md` (always-on guardrails and anti-patterns)

**Missing/stale context route:** If `docs/project-config.json`, the docs index, `lessons.md`, `CLAUDE.md`, `AGENTS.md`, or any task-required reference doc is missing or stale, auto-run `$project-init` or the narrow setup route (`$project-config`, `$docs-init`, `$scan-all`, `$scan --target=<key>`, `$claude-md-init`) before ordinary project-specific work. If Codex mirrors or `AGENTS.md` are missing/stale, ask the user to run `$sync-codex`; do not auto-run it.

**Situation-based docs:**

- Project structure/architecture/tech-stack/deployment/setup (any layer — backend, frontend, or infra): `project-structure-reference.md`
- Backend/CQRS/API/domain/entity changes: `backend-patterns-reference.md`, `domain-entities-reference.md`
- Frontend/UI/styling/design-system: `frontend-patterns-reference.md`, `scss-styling-guide.md`, `design-system/README.md`
- Spec authoring, `docs/specs/` pathing, or TC format: `feature-spec-reference.md`, `spec-system-reference.md`, `spec-principles.md`
- Behavior/public-contract changes or spec-test-code sync: `workflow-spec-test-code-cycle-reference.md` plus the spec docs above
- Derived spec indexes/ERDs/reimplementation guides: `spec-system-reference.md` and source Feature Specs under `docs/specs/`
- Integration test implementation/review: `integration-test-reference.md`
- E2E test implementation/review: `e2e-test-reference.md`
- Code review/audit work: `code-review-rules.md` plus domain docs above based on changed files

Do not read all docs blindly. Start from `docs-index-reference.md`, then open only relevant files for the task.

<!-- CODEX:PROJECT-REFERENCE-LOADING:END -->

<!-- PROMPT-ENHANCE:STEP-TASK-ANCHOR:START -->

> **[BLOCKING]** Execute skill steps in declared order. NEVER skip, reorder, or merge steps without explicit user approval.
> **[BLOCKING]** Before each step or sub-skill call, update task tracking: set `in_progress` when step starts, set `completed` when step ends.
> **[BLOCKING]** Every completed/skipped step MUST include brief evidence or explicit skip reason.
> **[BLOCKING]** If Task tools are unavailable, create and maintain an equivalent step-by-step plan tracker with the same status transitions.

<!-- PROMPT-ENHANCE:STEP-TASK-ANCHOR:END -->

## Quick Summary

**Goal:** Block shipping an unproven fix — adopt a SKEPTIC's stance and try to DISPROVE the fix first, then build a code proof trace (like a debugger stack trace) for each change with confidence percentages, so every code change carries a `file:line` evidence chain that survived a genuine refutation attempt and a fix ships only when its correctness is proven (≥80%), never assumed.

**Summary:**

- **Purpose / default stance is SKEPTIC, not validator** — find why the fix is WRONG or INCOMPLETE, never confirm it works. Skill name ("prove-fix") + post-`$fix` context + points rubric all bias toward confirmation; the Adversarial Verification Mindset forces a reset so confidence is _earned by surviving attack_, not awarded for coherence.
- **The 5 main steps (run in order, NEVER skip):** (1) **Change Inventory** — list EVERY change (file:line, before/after, type: root-cause/secondary/defensive/cleanup); (2) **Proof Trace per change** — stack-trace chain symptom → trigger path → root cause → fix mechanism → why-correct → **refutation attempt** → related paths → edge cases → side effects, every arrow `file:line`; (3) **Confidence Scoring** — points rubric + SKEPTIC caps; (4) **Cross-Verification** — Anti-Bias Gate FIRST, then interaction/completeness/regression/dependency/performance (paging+index DB protocol); (5) **Final Verdict** + Goal Satisfaction update.
- Runs AFTER `$fix` (NEVER before) — the non-negotiable verification gate between `$fix` and `$code-simplifier`; ≥80% ship · 60-79% flag · <60% BLOCK (route back to `$debug-investigate` or `$fix`).
- For EACH change, run a **Refutation Pass** FIRST (strongest case the fix is wrong/incomplete: counter-cases, unclosed feeder paths, wrong layer, regression risk, "test passes for the wrong reason") before scoring — an un-attacked change cannot exceed 79%.
- **Trace ALL related things** — every caller, consumer, sibling/alternate path, feeder path, downstream dependent, shared-state writer the change touches; an un-enumerated related path is an unproven path and caps confidence below 80%. — why: the reproduction exercises one path; the bug survives through paths you never traced.
- Score with the points rubric (root cause +25, fix mechanism +20, pattern precedent +15, framework +10, edge cases +5 each, side effects +10, no regressions +5); pattern precedent (1+ working example), edge cases (error/null/concurrent), survived refutation, and spec-loop evidence (property TC + mutation-kill + Dual-Feedback) are REQUIRED, not optional.
- Map every fix part to a primary/contributing/latent root cause from the hypothesis matrix and prove ALL feeder paths closed; finish with the **Anti-Bias Gate** + cross-change checks + final verdict, then resolve the active Goal Contract (map each proof trace to its success criterion, emit the PASS/FAIL/BLOCKED matrix) — a SHIP verdict does NOT close work while any required criterion remains FAIL.

**Workflow:**

1. **Inventory** — List every code change made by the fix (file:line, before/after)
2. **Trace + Refute** — For each change, build a proof chain (symptom → root cause → fix) AND run a refutation pass that tries to break it before believing it
3. **Score** — Assign confidence percentage per change with evidence; confidence is earned by surviving refutation, not awarded for coherence
4. **Verify** — Anti-Bias Gate + cross-check fix against edge cases, side effects, and ALL related paths
5. **Verdict** — Overall fix confidence and any remaining risks

**Key Rules:**

- **Default stance is SKEPTIC, not validator** — actively try to DISPROVE each change before scoring it; "looks correct" is the bias this gate exists to break
- Every claim MUST ATTENTION have `file:line` evidence — no exceptions
- Each change gets its OWN proof trace, refutation pass, and confidence score
- A change that has not been genuinely attacked (refutation pass) cannot exceed 79%
- If ANY change scores below 80%, flag it and recommend additional investigation
- Always run this proof-trace step after `$fix` — **non-negotiable**, never skip it

### Frontend/UI Context (if applicable)

> When this task involves frontend or UI changes,

- Component patterns: `docs/project-reference/frontend-patterns-reference.md`
- Styling/BEM guide: `docs/project-reference/scss-styling-guide.md`
- Design system tokens: `docs/project-reference/design-system/README.md`

**Be skeptical. Apply critical thinking, sequential thinking. Every claim needs traced proof, confidence percentages (Idea should be more than 80%).**

# Prove Fix

Post-fix verification skill building evidence-based proof chains for every code change. A code debugger's stack trace, but for proving WHY a fix is correct.

---

## When to Use

- **After `$fix`** in bugfix, hotfix, or any fix workflow
- After applying code changes that fix a reported bug
- Verify fix correctness before review/commit

## When NOT to Use

- Before fix applied (use `$debug-investigate` instead)
- New feature verification (use `$test` instead)
- Code quality review (use `$code-review` instead)

---

## Adversarial Verification Mindset (NON-NEGOTIABLE)

**Default stance: SKEPTIC, not validator. Your job is to prove the fix is WRONG or INCOMPLETE — and only conclude it is correct when every attack fails.**

> **Confirmation-bias trap (acute for THIS skill):** The skill is literally named "prove-fix", you arrive immediately after `$fix` (you may have written the fix yourself), and the scoring rubric _awards points for verified items_ — three forces that all pull toward confirming the fix works. A reviewer who already endorsed the fix cannot also be its skeptic without a forced reset. This section is that reset. — why: "build a proof FOR X" silently becomes "find reasons X is right"; real verification is "try to break X and report what survived".

**Reframe the goal:** Do NOT set out to demonstrate the fix is correct. Set out to demonstrate it is BROKEN. Confidence is whatever is left standing _after_ a genuine attempt to break it — never a tally of agreements.

### Refutation Techniques (apply ALL per change before scoring)

| Technique                    | Think (try to make the fix FAIL)                                                                                                                                                   |
| ---------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Counter-case hunt            | Find ONE input/state/timing where the "fixed" code still produces the symptom. If you cannot, prove the input domain is exhausted — don't assume it.                               |
| Test-passes-for-wrong-reason | Does the regression test pass because the fix is correct, or because the test is weak (asserts the example, not the invariant; mocks away the bug; never executes the fixed line)? |
| Unclosed feeder path         | Name every OTHER producer/caller/event/job/cache that can write the observed final state. Did the fix close ALL of them, or just the one you reproduced?                           |
| Wrong-layer challenge        | Argue the fix patches a symptom site, not the invariant owner. Would the bug recur through a sibling path that bypasses this fix?                                                  |
| Regression injection         | Assume the fix introduced a NEW bug. Where would it be? (changed scope, broadened catch, altered ordering, new query without paging/index.)                                        |
| Steel-man "no fix"           | Argue the original code was actually correct and the real bug is elsewhere. If that argument has any legs, the root cause is unproven.                                             |
| Contrarian verdict           | Before writing the score, argue in 2 sentences that this change should be BLOCKED. Then choose the stronger of ship-vs-block.                                                      |

### Forbidden Patterns

| Forbidden                           | Required correction                                                           |
| ----------------------------------- | ----------------------------------------------------------------------------- |
| "Fix is obviously correct"          | Obviousness is the illusion this gate breaks. Run the refutation pass anyway. |
| "Reproduction test passes → proven" | A passing example ≠ a closed invariant. Attack the test before trusting it.   |
| Award points for coherence          | Points require _survived attack_, not a plausible-sounding chain.             |
| "I wrote the fix, I know it works"  | Author ≠ reviewer. Reset to skeptic; attack your own change hardest.          |
| Stop at the path you reproduced     | Enumerate ALL feeder/related paths; an un-attacked path is an unproven path.  |

### Anti-Bias Gate (MANDATORY before any SHIP/SHIP-WITH-CAVEATS verdict)

Complete ALL of these — per change — before writing the final verdict (MUST ATTENTION):

- [ ] Ran the Refutation Pass (≥1 genuine counter-case attempt, recorded with `file:line` evidence of why it fails to reproduce)
- [ ] Attacked the regression test itself — confirmed it fails on the _un-fixed_ code and asserts the invariant, not the example
- [ ] Enumerated ALL related/feeder paths and proved each is closed or explicitly listed as unverified
- [ ] Stated the strongest argument the fix is at the WRONG layer, and rebutted it with evidence
- [ ] Named ≥1 plausible NEW regression the change could introduce, and ruled it out with evidence
- [ ] Wrote the contrarian (BLOCK) argument and explained why ship still wins

Any box unchecked → verification is NOT complete; confidence is capped at 79% (flag, do not ship). NEVER round an un-refuted change up to 80%.

---

## Step 1: Change Inventory

List ALL changes made by the fix. For each change, document:

```
CHANGE #N: [short description]
  File: [path/to/file.ext]
  Lines: [start-end]
  Before: [code snippet — the broken version]
  After:  [code snippet — the fixed version]
  Type:   [root-cause-fix | secondary-fix | defensive-fix | cleanup]
```

**Change types:**

- **root-cause-fix** — Directly addresses the root cause of the bug
- **secondary-fix** — Fixes a related issue discovered during investigation
- **defensive-fix** — Prevents the same class of bug from recurring
- **cleanup** — Removed dead code or simplified logic (no behavior change)

---

## Step 2: Proof Trace (per change)

For EACH change, build a **stack-trace-style proof chain** — the core of the skill.

### Proof Trace Format

```
PROOF TRACE — Change #N: [description]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SYMPTOM (what the user sees):
  → [Observable behavior, e.g., "UI doesn't refresh after assigning PIC"]

TRIGGER PATH (how the symptom occurs):
  1. [file:line] User action → [method/event]
  2. [file:line] → calls [method]
  3. [file:line] → dispatches [action/event]
  4. [file:line] → handler/effect [name]
  5. [file:line] ← BUG HERE: [exact broken behavior]

ROOT CAUSE (proven):
  → [One sentence: what exactly is wrong and why]
  → Evidence: [file:line] shows [specific code proving the bug]
  → Hypothesis matrix mapping: RC-[N] status [primary/contributing/latent] from [report path/section]
  → Feeder paths closed: [path names or "single path verified"]; unresolved paths: [none/list]

FIX MECHANISM (how the change fixes it):
  → [One sentence: what the fix does differently]
  → Before: [broken code path with file:line]
  → After:  [fixed code path with file:line]
  → Owning fix layer: [layer/component] — why this is the lowest shared owner

WHY THIS FIX IS CORRECT:
  → [Reasoning backed by code evidence]
  → Pattern precedent: [file:line] shows same pattern working elsewhere
  → Framework behavior: [file:line or doc reference] confirms expected behavior
  → Forward convergence: [origin/trigger] -> [corrected transformations] -> [observed final output no longer stale/wrong]

RELATED PATHS TRACED (all related things — none left un-attacked):
  → Callers/consumers of changed symbol: [file:line list] — [each unaffected/updated, with evidence]
  → Other feeder paths that write the final state: [file:line list] — [each closed / explicitly unverified]
  → Sibling/alternate paths (retry, async, cache, background, alternate UI/API): [file:line] — [status]
  → Downstream dependents (graph trace --direction downstream when graph.db exists): [evidence]

REFUTATION ATTEMPT (try to break it — REQUIRED before scoring):
  → Strongest counter-case attempted: [input/state/timing] → [why it does NOT reproduce, with file:line]
  → Test attacked: [does the regression test fail on un-fixed code? assert invariant or just the example?] — [file:line]
  → Wrong-layer challenge: [strongest argument this is a symptom patch] → [rebuttal with file:line, or CONCEDED]
  → New-regression hunt: [most plausible bug the change could introduce] → [ruled out with file:line, or OPEN]
  → Contrarian verdict (2 sentences arguing BLOCK): [...] → [why ship still wins, or why it does not]
  → Survived attack? [YES — all attacks failed / NO — finding(s): ...]

EDGE CASES CHECKED:
  → [edge case 1]: [verified/not-verified] — [evidence]
  → [edge case 2]: [verified/not-verified] — [evidence]

SIDE EFFECTS:
  → [None / List of potential side effects with evidence]

CONFIDENCE: [X%]  (earned by surviving the refutation pass, NOT by tallying agreements)
  Survived attacks: [list of attacks attempted that failed to break the fix]
  Verified: [list of verified items]
  Not verified / un-attacked: [list of unverified items — each caps confidence below 80%]
```

### Proof Trace Rules

1. **Every arrow (→) MUST ATTENTION have a `file:line` reference** — no exceptions
2. **TRIGGER PATH must be traceable** — someone should be able to follow it step-by-step in the code
3. **REFUTATION ATTEMPT is REQUIRED and must be GENUINE** — you MUST try to break the fix (counter-case, weak-test, wrong-layer, new-regression, contrarian) before scoring. A trace with an empty or token refutation pass is INCOMPLETE and caps confidence at 79%. Default to "broken until proven otherwise", not "correct until disproven".
4. **RELATED PATHS must be fully traced ("all related things")** — enumerate every caller, consumer, sibling/alternate path, feeder path, downstream dependent, and shared-state writer the change touches; an un-enumerated related path is an unproven path and caps confidence below 80%.
5. **Hypothesis matrix mapping is REQUIRED for bugfixes** — every fix part maps to a primary/contributing/latent root cause or is flagged as unrelated scope
6. **Feeder paths must be accounted for** — prove the fix closes every path that can write the final observed state, or explicitly list remaining unverified paths
7. **Pattern precedent is REQUIRED** — find at least 1 working example of the same pattern elsewhere in the codebase
8. **Edge cases MUST ATTENTION be enumerated** — at minimum: error path, null/empty input, concurrent access
9. **Side effects MUST ATTENTION be assessed** — what else could this change affect?
10. **The regression test MUST be attacked, not trusted** — confirm it FAILS on the un-fixed code and asserts the protected invariant (not just the reproduction example, not a mock that hides the bug, and the fixed line actually executes). A test you did not try to break is not evidence.
11. **Spec-loop evidence is REQUIRED for a complete proof** (canonical: `SYNC:spec-loop-discipline`) — the proof MUST carry, with `file:line`: (a) the **regression property TC** guarding the fixed invariant — a universally-quantified property ("for ALL inputs in {domain}, {invariant} holds") + boundary counter-case, not just the reproduction example; (b) **mutation-kill evidence** for the fixed core-logic line — show a surviving mutant on that line is now killed (MUTATION-SCORE bar, not line-coverage %); (c) a **Dual-Feedback entry** — the spec rule restored/added AND the guarding test that feeds it back. A proof trace missing any of (a)/(b)/(c) is INCOMPLETE — cap its confidence below the 80% ship threshold until the spec-loop evidence is supplied.

---

## Step 3: Confidence Scoring

Each change gets an individual confidence score:

| Score       | Meaning                                                                     | Action Required                                    |
| ----------- | --------------------------------------------------------------------------- | -------------------------------------------------- |
| **95-100%** | Full proof trace complete, all edge cases verified, pattern precedent found | Ship it                                            |
| **80-94%**  | Main proof trace complete, some edge cases unverified                       | Ship with caveats noted                            |
| **60-79%**  | Proof trace partial, some links unverified                                  | Flag to user — recommend additional investigation  |
| **<60%**    | Insufficient evidence                                                       | **BLOCK** — do not proceed until evidence gathered |

### Scoring Criteria

Award points for each verified item:

| Criterion                                 | Points  | Evidence Required             |
| ----------------------------------------- | ------- | ----------------------------- |
| Root cause identified with file:line      | +25     | Code reference                |
| Fix mechanism explained with before/after | +20     | Code diff                     |
| Pattern precedent found in codebase       | +15     | Working example at file:line  |
| Framework behavior confirmed              | +10     | Framework source or docs      |
| Edge cases checked (per case)             | +5 each | Verification result           |
| Side effects assessed                     | +10     | Impact analysis               |
| No regressions identified                 | +5      | Test results or code analysis |

**Total possible: 100+** (normalize to percentage)

> **[SKEPTIC GATE — applied AFTER the additive score]** The rubric measures evidence _gathered_; it does not measure whether the fix _survived attack_. Apply these caps regardless of the additive total — a high tally never overrides a failed/missing attack:
>
> - Refutation Pass not genuinely attempted, or any related/feeder path left un-enumerated → **cap at 79%** (flag, do not ship).
> - Any refutation attack succeeded (counter-case reproduces, test is weak, wrong layer, open regression) → that is a **finding**: score reflects the unresolved defect (typically <60%, BLOCK) until the finding is closed.
> - Contrarian (BLOCK) argument is stronger than the ship argument → **BLOCK**, route back to `$debug-investigate` or `$fix`.
>
> Confidence is what remains _after_ the attack — never the additive tally alone.

---

## Step 4: Cross-Verification

After individual proof traces, perform cross-change verification:

0. **Anti-Bias Gate (MANDATORY first)** — Complete every box of the Anti-Bias Gate (from the Adversarial Verification Mindset section) for the change set as a whole before any SHIP verdict. An unchecked box means verification is incomplete — go back, do not ship.
1. **Interaction check** — Do the changes interact with each other? Could one change break another?
2. **Completeness check** — Does the combined fix address ALL reported symptoms? Steel-man "the bug is still present somewhere" — what would prove it?
3. **Regression check** — Could the combined changes introduce new bugs? Assume they did; where?
4. **Dependency check** — Are there other code paths that depend on the changed behavior?
5. **Performance regression check** — Does the fix introduce performance issues?

> **[IMPORTANT] Database Performance Protocol (MANDATORY):**
>
> 1. **Paging Required** — ALL list/collection queries MUST ATTENTION use pagination. NEVER load all records into memory. Verify: no unbounded `GetAll()`, `ToList()`, or `Find()` without `Skip/Take` or cursor-based paging.
> 2. **Index Required** — ALL query filter fields, foreign keys, and sort columns MUST ATTENTION have database indexes configured. Verify: entity expressions match index field order, database collections have index management methods, migrations include indexes for WHERE/JOIN/ORDER BY columns.

---

## Step 5: Final Verdict

Produce a summary verdict:

```
FIX VERIFICATION VERDICT
━━━━━━━━━━━━━━━━━━━━━━━

Overall Confidence: [X%]

Anti-Bias Gate: [ALL boxes checked? YES/NO — if NO, verdict CANNOT be SHIP]

Changes Summary:
  #1: [description] — [X%] ✅/⚠️/❌ — refutation: [survived / finding: ...]
  #2: [description] — [X%] ✅/⚠️/❌ — refutation: [survived / finding: ...]
  #N: [description] — [X%] ✅/⚠️/❌ — refutation: [survived / finding: ...]

Symbols: ✅ ≥80% (ship) | ⚠️ 60-79% (flag) | ❌ <60% (block)

Attacks that FAILED to break the fix (these earn the confidence):
  - [attack]: [why it could not reproduce — file:line]

Attacks that SUCCEEDED (open findings — block until closed):
  - [attack]: [the defect it exposed — file:line] (or "none")

Remaining Risks:
  - [risk 1]: [likelihood] × [impact] — [mitigation]
  - [risk 2]: [likelihood] × [impact] — [mitigation]

Verification Method:
  - [Manual testing required? Which scenarios?]
  - [Automated tests cover this? Which tests?]
  - [Additional monitoring needed post-deploy?]

Recommendation: [SHIP / SHIP WITH CAVEATS / INVESTIGATE FURTHER / BLOCK]
```

**Goal Satisfaction update (MANDATORY after verdict):** resolve the active Goal Contract per `SYNC:goal-contract-satisfaction-loop` and map each proof trace to the saved success criterion it satisfies. Append proof evidence and remaining gaps to the goal file's Iteration Log and update its Goal Satisfaction matrix (PASS/FAIL/BLOCKED per criterion). A SHIP recommendation does NOT close the work while any required goal criterion remains FAIL — route the validated gap into another bounded fix loop or escalate a blocker.

---

## Example: Proof Trace for NgRx Effect Fix

```
PROOF TRACE — Change #1: Move catchError inside switchMap
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SYMPTOM:
  → UI doesn't refresh after assigning PIC, Job Opening, or changing stage

TRIGGER PATH:
  1. candidate-quick-card-v2.component.ts:445 — User clicks "Assign PIC"
  2. candidate-card.container.component.ts:892 — onPersonInChargeChange($event)
  3. candidate-card.effect.ts:275 — SavePersonInCharge effect
  4. candidate-card.effect.ts:284 — dispatches LoadCandidateDetailsAction
  5. candidate-card.effect.ts:48 ← EFFECT IS DEAD — never processes the action

ROOT CAUSE:
  → catchError at outer pipe level (effect.ts:64) causes effect completion on ANY error
  → Evidence: effect.ts:43-69 shows catchError OUTSIDE switchMap
  → Evidence: ngrx-effects.js:156-165 confirms defaultEffectsErrorHandler
     only catches errors, not completions

FIX MECHANISM:
  → Move catchError INSIDE switchMap so errors are caught per-request
  → Before: effect.ts:64 — catchError at outer pipe → effect COMPLETES → DEAD
  → After:  effect.ts:52 — catchError inside switchMap → inner obs completes → outer SURVIVES

WHY THIS FIX IS CORRECT:
  → RxJS: catchError inside switchMap catches per-emission, outer stream continues
  → Pattern precedent: effect.ts:120 (moveApplicationToNextState) uses same inner pattern
  → Framework: NgRx effects auto-resubscribe on ERROR but NOT on COMPLETION

RELATED PATHS TRACED:
  → Callers of SavePersonInCharge effect: container:892 only — verified no other dispatcher
  → Other effects sharing the dead-stream bug: grep catchError outside switchMap →
     effect.ts:300 (SaveJobOpening), effect.ts:355 (ChangeStage) have SAME bug —
     ⚠ NOT fixed by this change; listed as unverified/out-of-scope feeder paths
  → Downstream consumers of LoadCandidateDetailsAction: reducer.ts:88 — unaffected (no contract change)

REFUTATION ATTEMPT:
  → Counter-case: a SECOND error after the fix → inner catchError re-catches; outer survives (verified effect.ts:52)
  → Test attacked: spec fails on un-fixed code (effect completes, no SetCandidateDetails emitted) AND asserts
     the effect still emits on the 2nd call — invariant, not just the one example (effect.spec.ts:140-176)
  → Wrong-layer challenge: could fix at component? NO — effect owns the stream lifetime invariant; component patch
     would leave SaveJobOpening/ChangeStage broken. Layer confirmed correct.
  → New-regression hunt: broadened catch could swallow a real error → ruled out, same error branch returns
     same action, only scope moved (effect.ts:52 vs :64)
  → Contrarian: "BLOCK — two sibling effects still carry the bug." → Ship THIS change (correct + tested) but
     the sibling paths are a SEPARATE finding to route back to $fix, not a reason to block this one.
  → Survived attack? YES for this change — but surfaced 2 un-fixed sibling feeder paths as findings.

EDGE CASES:
  → 403 Forbidden: verified — returns SetCandidateDetails with isAllowDisplayed=false
  → Network timeout: verified — returns EMPTY, effect survives
  → Multiple rapid requests: verified — switchMap cancels previous (unchanged)

SIDE EFFECTS:
  → None for this effect — same error handling logic, only scope changed

CONFIDENCE: 90% (this change), with a BLOCKING completeness finding
  Survived attacks: counter-case, weak-test, wrong-layer, new-regression all failed to break it
  Verified: root cause, fix mechanism, pattern precedent, framework source, all edge cases
  Not verified / open finding: SaveJobOpening (effect.ts:300) and ChangeStage (effect.ts:355) share the
     identical bug and are NOT fixed — the original symptom ("UI doesn't refresh after ... changing stage")
     is only PARTIALLY resolved. Completeness check FAILS until those are fixed too.
```

> **What the skeptic stance bought here:** a confirmation-biased pass would have scored this 95% ("root cause found, test passes, ship it") and shipped a fix that leaves two-thirds of the reported symptom alive. The refutation pass + "trace all related things" caught the sibling feeder paths the reproduction never exercised.

---

> Run `python .claude/scripts/code_graph trace <file> --direction downstream --json` to prove fix doesn't break downstream.

## Graph Intelligence (RECOMMENDED if graph.db exists)

If `.code-graph/graph.db` exists, enhance analysis with structural queries:

- **Verify test coverage:** `python .claude/scripts/code_graph query tests_for <function> --json`
- **Trace affected code paths:** `python .claude/scripts/code_graph query callers_of <function> --json`
- **Batch analysis:** `python .claude/scripts/code_graph batch-query file1 file2 --json`

### Graph-Trace for Fix Verification

When graph DB is available, use `trace` to PROVE the fix doesn't break downstream consumers:

- `python .claude/scripts/code_graph trace <fixed-file> --direction downstream --json` — verify all downstream consumers, event handlers, and bus message listeners are unaffected
- `python .claude/scripts/code_graph trace <fixed-file> --direction both --json` — full context: what triggered the bug (upstream) + what the fix affects (downstream)
- Include trace results as evidence in the proof chain

## Integration with Other Skills

This skill is the **mandatory verification gate** between `$fix` and `$code-simplifier` in fix workflows.

**Workflow position:**

```
... → $fix → $prove-fix → $code-simplifier → $changes-review → ...
```

**If proof trace reveals issues:**

- Score ≥80%: proceed to next step
- Score 60-79%: ask user whether to proceed or investigate further
- Score <60%: BLOCK — return to `$debug-investigate` or `$fix` step

---

<prove-context>$ARGUMENTS</prove-context>

---

## Workflow Recommendation

> **MANDATORY IMPORTANT MUST ATTENTION — NO EXCEPTIONS:** If you are NOT already in a workflow, you MUST ATTENTION use ask the user directly to ask the user. Do NOT judge task complexity or decide this is "simple enough to skip" — the user decides whether to use a workflow, not you:
>
> 1. **Activate `workflow-bugfix` workflow** (Recommended) — scout → investigate → debug → plan → fix → prove-fix → review → test
> 2. **Execute `$prove-fix` directly** — run this skill standalone

---

## Next Steps

**MANDATORY IMPORTANT MUST ATTENTION — NO EXCEPTIONS** after completing this skill, you MUST ATTENTION use ask the user directly to present these options. Do NOT skip because the task seems "simple" or "obvious" — the user decides:

- **"$code-simplifier (Recommended)"** — Clean up fix implementation
- **"$integration-test"** — Generate/update regression integration tests
- **"$workflow-review-changes"** — Review all changes before commit
- **"Skip, continue manually"** — user decides

> **[IMPORTANT]** Use task tracking to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI MUST ATTENTION ask user whether to skip.

**Prerequisites:** **MUST ATTENTION READ** before executing:

- `docs/project-reference/domain-entities-reference.md` — Domain entity catalog, relationships, cross-service sync (read when task involves business entities/models)

> **External Memory:** For complex or lengthy work (research, analysis, scan, review), write intermediate findings and final results to a report file in `plans/reports/` — prevents context loss and serves as deliverable.

> **Evidence Gate:** MANDATORY IMPORTANT MUST ATTENTION — every claim, finding, and recommendation requires `file:line` proof or traced evidence with confidence percentage (>80% to act, <80% must verify first).

<!-- SYNC:end-to-start-debugger-trace -->

> **End-to-Start Debugger Trace** — For non-trivial bugs, failed verification, regression fixes, behavior-changing code, or unclear code flow, start from the observed final state and walk backward before proposing a fix.
>
> 1. **Frame 0: observed end state** — Name the exact user-visible output, failing assertion, log line, persisted value, API response, rendered UI, or aggregate bucket. Record the reader/query/renderer that produced it with `file:line` evidence.
> 2. **Walk backward one hop at a time** — Trace final reader -> projection/cache/storage -> writer -> consumer/handler/job -> producer/caller -> original trigger. At every hop record: input, transformation, output, owner, and evidence.
> 3. **Enumerate all feeder paths** — Find every upstream producer/caller/event/job that can write into the final path, including retry, async, cache, background, and alternate UI/API paths. Mark each path verified, ruled out, or still unknown.
> 4. **Build the hypothesis matrix** — For each plausible cause, list evidence for, evidence against, how to reproduce/verify, blast radius, and status (`primary`, `contributing`, `ruled out`, `latent`). Do not fix until competing causes are explicitly resolved or bounded.
> 5. **Choose the owning fix layer** — Identify the invariant owner and the lowest shared point that protects all downstream consumers. A fix at the symptom site is rejected unless the symptom site owns the invariant.
> 6. **Prove convergence forward** — After choosing the fix, walk start -> end again and show how the corrected state reaches the observed final output. Map each root cause to a fix part and each fix part to a test/proof.
>
> **BLOCKED until:** final state named · backward trace written · all feeder paths enumerated · hypothesis matrix completed · owning fix layer justified · forward convergence proof mapped to tests.
>
> **NEVER:** Start at the first suspicious code path. Collapse multiple producers into one "flow". Treat duplicate symptoms as duplicate records without proving the read model. Skip ruled-out hypotheses.

<!-- /SYNC:end-to-start-debugger-trace -->

<!-- SYNC:ui-system-context -->

> **UI System Context** — For ANY task touching `.ts`, `.html`, `.scss`, or `.css` files:
>
> **MUST ATTENTION READ before implementing:**
>
> 1. `docs/project-reference/frontend-patterns-reference.md` — component base classes, stores, forms
> 2. `docs/project-reference/scss-styling-guide.md` — BEM methodology, SCSS variables, mixins, responsive
> 3. `docs/project-reference/design-system/README.md` — design tokens, component inventory, icons
>
> Reference `docs/project-config.json` for project-specific paths.

<!-- /SYNC:ui-system-context -->

<!-- SYNC:graph-assisted-investigation -->

> **Graph-Assisted Investigation** — MANDATORY when `.code-graph/graph.db` exists.
>
> **HARD-GATE:** MUST ATTENTION run at least ONE graph command on key files before concluding any investigation.
>
> **Pattern:** Grep finds files → `trace --direction both` reveals full system flow → Grep verifies details
>
> | Task                | Minimum Graph Action                         |
> | ------------------- | -------------------------------------------- |
> | Investigation/Scout | `trace --direction both` on 2-3 entry files  |
> | Fix/Debug           | `callers_of` on buggy function + `tests_for` |
> | Feature/Enhancement | `connections` on files to be modified        |
> | Code Review         | `tests_for` on changed functions             |
> | Blast Radius        | `trace --direction downstream`               |
>
> **CLI:** `python .claude/scripts/code_graph {command} --json`. Use `--node-mode file` first (10-30x less noise), then `--node-mode function` for detail.

<!-- /SYNC:graph-assisted-investigation -->

<!-- SYNC:critical-thinking-mindset -->

> **Critical Thinking Mindset** — Apply critical thinking, sequential thinking. Every claim needs traced proof, confidence >80% to act.
> **Anti-hallucination:** Never present guess as fact — cite sources for every claim, admit uncertainty freely, self-check output for errors, cross-reference independently, stay skeptical of own confidence — certainty without evidence root of all hallucination.

<!-- /SYNC:critical-thinking-mindset -->

<!-- SYNC:understand-code-first -->

> **Understand Code First** — HARD-GATE: Do NOT write, plan, or fix until you READ existing code.
>
> 1. Search 3+ similar patterns (`grep`/`glob`) — cite `file:line` evidence
> 2. Read existing files in target area — understand structure, base classes, conventions
> 3. Run `python .claude/scripts/code_graph trace <file> --direction both --json` when `.code-graph/graph.db` exists
> 4. Map dependencies via `connections` or `callers_of` — know what depends on your target
> 5. Write investigation to `.ai/workspace/analysis/` for non-trivial tasks (3+ files)
> 6. Re-read analysis file before implementing — never work from memory alone. — why: long context drifts from the file; the file is ground truth
> 7. NEVER invent new patterns when existing ones work — match exactly or document deviation. — why: divergent patterns fragment the codebase and slow every future reader
>
> **BLOCKED until:** `- [ ]` Read target files `- [ ]` Grep 3+ patterns `- [ ]` Graph trace (if graph.db exists) `- [ ]` Assumptions verified with evidence

<!-- /SYNC:understand-code-first -->

<!-- SYNC:fix-layer-accountability -->

> **Fix-Layer Accountability** — NEVER fix at the crash site. Trace the full flow, fix at the owning layer.
>
> AI default behavior: see error at Place A → fix Place A. This is WRONG. The crash site is a SYMPTOM, not the cause.
>
> **MANDATORY before ANY fix:**
>
> 1. **Trace full data flow** — Map the complete path from data origin to crash site across ALL layers (storage → backend → API → frontend → UI). Identify where the bad state ENTERS, not where it CRASHES.
> 2. **Identify the invariant owner** — Which layer's contract guarantees this value is valid? That layer is responsible. Fix at the LOWEST layer that owns the invariant — not the highest layer that consumes it.
> 3. **One fix, maximum protection** — Ask: "If I fix here, does it protect ALL downstream consumers with ONE change?" If fix requires touching 3+ files with defensive checks, you are at the wrong layer — go lower.
> 4. **Verify no bypass paths** — Confirm all data flows through the fix point. Check for: direct construction skipping factories, clone/spread without re-validation, raw data not wrapped in domain models, mutations outside the model layer.
>
> **BLOCKED until:** `- [ ]` Full data flow traced (origin → crash) `- [ ]` Invariant owner identified with `file:line` evidence `- [ ]` All access sites audited (grep count) `- [ ]` Fix layer justified (lowest layer that protects most consumers)
>
> **Anti-patterns (REJECT these):**
>
> - "Fix it where it crashes" — Crash site ≠ cause site. Trace upstream.
> - "Add defensive checks at every consumer" — Scattered defense = wrong layer. One authoritative fix > many scattered guards.
> - "Both fix is safer" — Pick ONE authoritative layer. Redundant checks across layers send mixed signals about who owns the invariant.

<!-- /SYNC:fix-layer-accountability -->

<!-- SYNC:source-test-drift-check -->

> **Source/test drift check.** For coding, fix, debug, investigation, test, or review work: when source behavior changes, inspect affected unit/integration/E2E tests and decide from evidence whether tests should change to match intended behavior or the source change is an unintended bug to fix. Do not write tests for migration code; schema/data migrations are one-time execution paths, not core application logic.

<!-- /SYNC:source-test-drift-check -->

<!-- SYNC:test-failure-fault-adjudication -->

> **Test-Failure Fault Adjudication** — When a test fails (or you are debugging or fixing a failure), the job is to determine _who is at fault — the source code or the test code_. Getting that verdict right matters more than turning the suite green. Binds every debug / fix / test skill identically.
>
> 1. **Provisional verdict before touching either side.** Classify the observed evidence as SOURCE-WRONG, TEST-WRONG, TEST-NOT-OPTIMAL, ENVIRONMENT-BLOCKED, or AMBIGUOUS; then `$debug-investigate` and trace end-to-start before editing. A green-again suite is NOT the goal.
> 2. **Triangulate against the spec AND the source.** If a governing Feature Spec covers the behavior (e.g. `docs/specs/**` — §3 ACs / §4 BRs / §5 invariants / §8 TCs), it is the tiebreaker for _intended_ behavior — compare BOTH the production source and the failing test against it. With no spec, the documented intent / acceptance criteria / caller contract is the reference. Decide from this evidence whether the SOURCE is wrong or the TEST is wrong.
> 3. **Classify who is at fault, then fix the wrong side at its root:**
>     - **SOURCE-WRONG** — production code violates the spec's intended behavior or a clear invariant → fix the source at the owning layer; keep or strengthen the test that caught it.
>     - **TEST-WRONG** — the test encodes a stale or incorrect assertion, setup, or expectation that contradicts intended behavior → fix the test at its root. NEVER weaken an assertion, add a skip, or relax a timeout to force green.
>     - **TEST-NOT-OPTIMAL** — intended behavior is valid but the test seam, timing, or assertion signal is fragile → improve the test without weakening the invariant.
>     - **ENVIRONMENT-BLOCKED** — infrastructure or external state prevents a source/test verdict → preserve diagnostics and stop mutation until the environment is healthy.
>     - **AMBIGUOUS** — evidence or intended behavior does not safely select an owner → ask the user or canonical owner before editing.
>     - NEVER change a test to match broken source, and NEVER change source to satisfy a broken test. (Migration code excluded — schema/data migrations are one-time execution paths, not core application logic.)
> 4. **Ask the user when intended behavior is unclear.** If no spec covers the behavior, the spec is silent, or the spec is ambiguous about which side is correct, STOP and ask the user directly (or consult the canonical spec owner) before editing either side — never silently pick source or test just to make the suite pass.
>
> Reconcile to intended behavior, never to whichever side currently passes — green can encode the very bug.

<!-- /SYNC:test-failure-fault-adjudication -->

<!-- SYNC:ai-mistake-prevention -->

> **AI Mistake Prevention** — Failure modes to avoid on every task:
>
> **Re-read files after context changes.** Context compaction, resume, or long-running work can make memory stale; verify current files before acting.
> **Verify generated content against source evidence.** AI hallucinates APIs, names, claims, and document facts. Check the relevant source before documenting or referencing.
> **Check downstream references before deleting or renaming.** Removing an artifact can stale docs, generated mirrors, configs, and callers; map references first.
> **Trace the full impact chain after edits.** Changing a definition can miss derived outputs and consumers. Follow the affected chain before declaring done.
> **Verify ALL affected outputs, not just the first.** One green check is not all green checks; validate every output surface the change can affect.
> **Assume existing values are intentional — ask WHY before changing OR flagging one as a defect.** Before changing or reporting a constant, limit, flag, cutoff, wording, or pattern, read nearby context and history, the CALLER's ordering, and 2+ sibling call sites of the same convention. A doc stating WHAT without WHY is missing rationale, not proof of a missing guard.
> **Surface ambiguity before acting — don't pick silently.** Multiple valid interpretations require an explicit question or stated assumption with risk.
> **Assert the outcome your system owns, not the intermediate state your infrastructure owns.** When verifying async work, assert the final business state — never the delivery/retry bookkeeping held in shared infrastructure that any co-running process can write. Such a check passes when run alone and flakes the moment anything else shares that infrastructure.
> **Keep shared guidance role-relevant.** Universal guidance must help every receiving skill or agent; code-specific obligations belong only in code-specific protocols.

<!-- /SYNC:ai-mistake-prevention -->

<!-- SYNC:understand-code-first:reminder -->

**IMPORTANT MUST ATTENTION** search 3+ existing patterns and read code BEFORE any modification. Run graph trace when graph.db exists.

<!-- /SYNC:understand-code-first:reminder -->

<!-- SYNC:evidence-based-reasoning:reminder -->

- **MANDATORY IMPORTANT MUST ATTENTION** cite `file:line` evidence for every claim. Confidence >80% to act, <60% = do NOT recommend.
  <!-- /SYNC:evidence-based-reasoning:reminder -->

<!-- SYNC:ui-system-context:reminder -->

**IMPORTANT MUST ATTENTION** read frontend-patterns-reference, scss-styling-guide, design-system/README before any UI change.

<!-- /SYNC:ui-system-context:reminder -->

<!-- SYNC:graph-assisted-investigation:reminder -->

**IMPORTANT MUST ATTENTION** run at least ONE graph command on key files when graph.db exists. Pattern: grep → graph trace → grep verify.

<!-- /SYNC:graph-assisted-investigation:reminder -->

<!-- SYNC:fix-layer-accountability:reminder -->

**IMPORTANT MUST ATTENTION** trace full data flow and fix at the owning layer, not the crash site. Audit all access sites before adding `?.`.

<!-- /SYNC:fix-layer-accountability:reminder -->

<!-- SYNC:critical-thinking-mindset:reminder -->

**MUST ATTENTION** apply critical + sequential thinking — every claim needs appropriate traced evidence (`file:line` for repo/code claims; source URL or artifact section for research, product, content, and docs claims); confidence >80% to act, <60% DO NOT recommend. Anti-hallucination: never present guess as fact, admit uncertainty freely, cross-reference independently, stay skeptical of own confidence.

<!-- /SYNC:critical-thinking-mindset:reminder -->

<!-- SYNC:ai-mistake-prevention:reminder -->

**MUST ATTENTION** apply AI mistake prevention — verify generated content against evidence, trace downstream references before deleting or renaming, verify all affected outputs, re-read files after context loss, and surface ambiguity before acting.

<!-- /SYNC:ai-mistake-prevention:reminder -->

<!-- SYNC:end-to-start-debugger-trace:reminder -->

**IMPORTANT MUST ATTENTION** debugger trace gate: for non-trivial bug/fix/investigation/review work, start at the observed final output and trace backward through reader -> storage/projection -> writer -> consumer/job -> producer/trigger. Enumerate all feeder paths and hypotheses before fixing. **BLOCKED until** trace, hypothesis matrix, owning fix layer, and forward convergence proof exist.

<!-- /SYNC:end-to-start-debugger-trace:reminder -->

<!-- SYNC:goal-contract-satisfaction-loop:reminder -->

- **MANDATORY** Resolve the active Goal Contract BEFORE work (active plan `goal.md` → `plans/goals/{YYMMDD-HHmm}-{slug}/goal.md` → create from current request) and read saved success criteria before editing.
- **MANDATORY** Append iteration evidence after execution; emit a Goal Satisfaction matrix (PASS/FAIL/BLOCKED) before reporting PASS; loop on validated FAIL; escalate repeated no-progress or blockers. NEVER store secrets in goal files.

<!-- /SYNC:goal-contract-satisfaction-loop:reminder -->

<!-- PROMPT-ENHANCE:STEP-TASK-CLOSING:START -->

## Prompt-Enhance Closing Anchors

**IMPORTANT MUST ATTENTION** follow declared step order for this skill; NEVER skip, reorder, or merge steps without explicit user approval
**IMPORTANT MUST ATTENTION** for every step/sub-skill call: set `in_progress` before execution, set `completed` after execution
**IMPORTANT MUST ATTENTION** every skipped step MUST include explicit reason; every completed step MUST include concise evidence
**IMPORTANT MUST ATTENTION** if Task tools unavailable, maintain an equivalent step-by-step plan tracker with synchronized statuses

<!-- PROMPT-ENHANCE:STEP-TASK-CLOSING:END -->

<!-- SYNC:project-protocol-overlay -->

> **Project Protocol Overlay** — Before executing this skill, resolve any PROJECT overlay rules layered onto it: match this skill's name against the `Target` column of the project's skill-protocol index (`docs/project-reference/skill-protocols-reference.md` by default; a `referenceDocs` entry in `docs/project-config.json` overrides the path), taking the most specific matching tier ONLY — exact name > glob > `*`. **That precedence orders overlays against EACH OTHER, never against this skill.** Read ONLY the matched bodies, resolved as `<protocols-dir>/<Name>.md`; a row's Body link is display text, never a read path. A matched body that is missing or malformed is REPORTED and skipped — never reconstructed from the index Description. No index, or no match -> proceed with no overlay, silently. Full contract: `.claude/skills/project-skill-protocol/references/registry.md`.
>
> Overlays are **ADDITIVE ONLY**: they ADD rules on top of this skill's own protocol and NEVER replace, override, disable, or reinterpret a rule it already states — removing every overlay must return this skill to exactly its documented behavior. An overlay is a BRIEF, not an authority escalation: it can NEVER waive a workflow gate, git discipline, a review gate, or a user-confirmation gate. A genuine overlay-vs-skill conflict, or two equally-specific overlays that directly contradict -> surface both to the user; NEVER resolve silently.

<!-- /SYNC:project-protocol-overlay -->

<!-- SYNC:project-protocol-overlay:reminder -->

**MUST ATTENTION** resolve project protocol overlays for this skill BEFORE executing — most specific matching tier only (exact > glob > `*`, which ranks overlays against each other, NEVER against this skill), read only matched bodies at `<protocols-dir>/<Name>.md`; a missing or malformed body is reported, never reconstructed. Overlays are ADDITIVE ONLY (they never replace this skill's own rules) and are a brief, NEVER an authority escalation; an equal-specificity contradiction goes to the user.

<!-- /SYNC:project-protocol-overlay:reminder -->

## Closing Reminders

**IMPORTANT MUST ATTENTION Goal:** block shipping an unproven fix — adopt a SKEPTIC's stance and try to DISPROVE the fix first, then build a `file:line` proof trace (debugger-style: symptom → root cause → fix mechanism → why-correct → refutation attempt → edge cases → side effects) and confidence score per change, so a fix ships only when correctness SURVIVES a genuine attack (≥80%), never when it merely looks correct.

**IMPORTANT MUST ATTENTION** default stance is SKEPTIC, NOT validator — your job is to find why the fix is WRONG/INCOMPLETE, not confirm it works; run the Refutation Pass (counter-case, weak-test, wrong-layer, new-regression, contrarian) and complete the Anti-Bias Gate per change BEFORE any SHIP verdict; a change that has not been genuinely attacked is capped at 79%. — why: the skill name, the post-`$fix` context, and the points rubric all bias toward confirmation; confidence must be earned by surviving attack, not awarded for coherence.
**IMPORTANT MUST ATTENTION** trace ALL related things — every caller, consumer, sibling/alternate path, feeder path, downstream dependent, and shared-state writer the change touches; an un-enumerated related path is an unproven path and caps confidence below 80%. — why: the reproduction exercises one path; the bug often survives through the paths you never traced.
**IMPORTANT MUST ATTENTION** execute the 5 steps in order, NEVER skip or merge: (1) **Change Inventory** — every change with file:line, before/after, type → (2) **Proof Trace per change** — symptom → trigger path → root cause → fix mechanism → why-correct → refutation attempt → related paths → edge cases → side effects (every arrow `file:line`) → (3) **Confidence Scoring** — points rubric + SKEPTIC caps → (4) **Cross-Verification** — Anti-Bias Gate FIRST, then interaction/completeness/regression/dependency/DB-performance → (5) **Final Verdict** + Goal Satisfaction update. — why: AI forgets the skill's own steps and ad-libs a partial verification that ships an unproven fix.

**Protocols in force (concise digest of the SYNC/shared blocks this skill carries):**

- **End-to-Start Trace:** start at observed output, trace backward, hypothesis matrix before fixing.
- **UI System Context:** read frontend-patterns, scss-styling, design-system before any UI change.
- **Graph Investigation:** run ≥1 graph command on key files when graph.db exists.
- **Critical Thinking:** traced `file:line` proof per claim; confidence >80% to act.
- **Understand Code First:** grep 3+ patterns and read code before any modification.
- **Fix-Layer Accountability:** trace full data flow, fix at owning layer not crash site.
- **Source/Test Drift:** when source behavior changes, reconcile affected unit/integration/E2E tests from evidence.
- **AI Mistake Prevention:** verify generated content against evidence, trace downstream references, verify all affected outputs, re-read after context loss, surface ambiguity.

**IMPORTANT MUST ATTENTION** every arrow (→) in every proof trace MUST ATTENTION carry a `file:line` reference — no exceptions; a claim without traced evidence is speculation and BLOCKS the ship. — why: a proof chain with an unproven link proves nothing.
**IMPORTANT MUST ATTENTION** score each change with the points rubric (root cause +25, fix mechanism +20, pattern precedent +15, framework +10, edge cases +5 each, side effects +10, no regressions +5) → ≥80% ship · 60-79% flag to user · <60% BLOCK; NEVER ship a <80% change — route it back to `$debug-investigate` or `$fix`. — why: the threshold is the gate; bypassing it defeats the skill.
**IMPORTANT MUST ATTENTION** run AFTER `$fix`, never before — this is the non-negotiable verification gate between `$fix` and `$code-simplifier`; NEVER skip it because the fix "looks obviously right". — why: obviousness is the exact illusion this gate exists to break.

**Domain protocols this proof MUST NOT skip:**

**IMPORTANT MUST ATTENTION** pattern precedent is REQUIRED, not optional — cite at least 1 working example of the same pattern at `file:line` elsewhere in the codebase; "no precedent found" caps confidence below 80%. — why: a fix with no precedent is an unproven invention.
**IMPORTANT MUST ATTENTION** edge cases are REQUIRED — enumerate at minimum error path, null/empty input, concurrent access, each verified with evidence; assess side effects (what else this change touches). — why: the happy path passing is not the change being correct.
**IMPORTANT MUST ATTENTION** spec-loop evidence is REQUIRED for a complete proof (`SYNC:spec-loop-discipline`) — (a) a regression PROPERTY TC (∀ inputs in {domain}, invariant holds) + boundary counter-case, (b) mutation-kill evidence on the fixed line (MUTATION-SCORE, not line-coverage %), (c) a Dual-Feedback entry (spec rule restored + guarding test); missing any one caps confidence below 80%. — why: line coverage and a single reproduction example let the original defect class survive.
**IMPORTANT MUST ATTENTION** map every fix part to a primary/contributing/latent root cause from the hypothesis matrix and prove ALL feeder paths are closed; fix at the LOWEST shared owning layer, NEVER patch the crash/symptom site. — why: a symptom-site patch leaves the real cause writing bad state through other paths.
**IMPORTANT MUST ATTENTION** for non-trivial bug/fix work, start at the observed final output and trace BACKWARD (reader → storage/projection → writer → consumer/job → producer/trigger) before proposing a fix; build the hypothesis matrix first. — why: starting at the first suspicious line fixes a symptom, not the cause.
**IMPORTANT MUST ATTENTION** run the Database Performance Protocol in cross-verification — ALL list/collection queries paginated (no unbounded `GetAll/ToList/Find`), ALL filter/FK/sort columns indexed. — why: a correct fix that degrades query performance ships a new regression.
**IMPORTANT MUST ATTENTION** when `.code-graph/graph.db` exists, run a `trace --direction downstream` on the fixed file to prove no downstream consumer breaks; include trace output as proof evidence. — why: a green local change can silently break a distant caller.
**IMPORTANT MUST ATTENTION** resolve the active Goal Contract AFTER the verdict (`SYNC:goal-contract-satisfaction-loop`) — map each proof trace to its success criterion, emit the PASS/FAIL/BLOCKED matrix; a SHIP verdict does NOT close work while any required criterion remains FAIL. — why: a verified change is not a satisfied goal.
**MANDATORY IMPORTANT MUST ATTENTION** break work into small task tracking todos BEFORE starting (one task per change/proof), keep exactly one `in_progress`, add a final review todo; on context loss the current task list first — resume, never duplicate.

**Anti-Rationalization:**

| Evasion                                        | Rebuttal                                                                                         |
| ---------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| "Fix is obviously correct, skip the proof"     | Obviousness is the illusion this gate breaks. Build the trace anyway — every arrow `file:line`.  |
| "No precedent, but it's clearly right"         | No precedent caps confidence <80%. Find a working example or mark the change unproven.           |
| "Reproduction test passes, that's enough"      | A single example ≠ a property. Add the universally-quantified regression TC + boundary case.     |
| "Line coverage is green"                       | Coverage ≠ kill. Show the surviving mutant on the fixed line is now killed (mutation score).     |
| "I'll just patch where it crashes"             | Crash site ≠ cause site. Trace backward, fix the lowest invariant owner that protects all paths. |
| "Score is 75%, close enough to ship"           | <80% BLOCKS. Flag to user or return to `$debug-investigate` — never round a confidence up.       |
| "I'm building the proof FOR the fix"           | That's confirmation bias. Build the proof AGAINST it — attack first, score what survives.        |
| "I wrote this fix, I know it's right"          | Author ≠ reviewer. Reset to skeptic and attack your own change hardest of all.                   |
| "Didn't really try to break it, but it's fine" | No genuine refutation pass → capped at 79%. An un-attacked fix is unproven, not proven.          |
| "Only traced the path I reproduced"            | Trace ALL related/feeder/sibling paths. The bug usually survives where you never looked.         |

**IMPORTANT MUST ATTENTION** be a SKEPTIC — try to DISPROVE the fix and trace ALL related paths; run AFTER `$fix` only; every arrow carries `file:line`; confidence is what survives the attack (≥80% to ship, <60% BLOCK) — these are the gate. (primacy-recency echo of the top three)

**[TASK-PLANNING]** Before acting, analyze task scope and break it into small task tracking todos systematically before starting — this is very important.

<!-- CODEX:SYNC-PROMPT-PROTOCOLS:START -->

## Hookless Prompt Protocol Mirror (Auto-Synced)

Source: `.claude/.ck.json` + `.claude/skills/shared/sync-inline-versions.md` (`:full` blocks) + `.claude/scripts/lib/hookless-prompt-protocol.cjs`

## [WORKFLOW-EXECUTION-PROTOCOL] [BLOCKING] Workflow Execution Protocol — MANDATORY IMPORTANT MUST CRITICAL. Do not skip for any reason.

**Generic portability boundary:** Reusable skills and protocol text stay project-neutral; project-specific conventions are discovered from docs/project-config.json and docs/project-reference/. Apply shared AI-SDD from `shared/sdd-artifact-contract.md`. Read `docs/project-config.json` and `docs/project-reference/docs-index-reference.md`, then open the project reference docs named there. For spec, test-case, behavior-change, public-contract, or `docs/specs/` work, route through the local spec docs named by the docs index: `feature-spec-reference.md`, `spec-system-reference.md`, `spec-principles.md`, and `workflow-spec-test-code-cycle-reference.md` when specs/tests/code must stay synchronized. If either file or a required reference doc is missing or stale, auto-run `$project-init` (or the narrow lower-level route such as `$project-config`, `$docs-init`, `$scan-all`, or `$scan --target=<key>`) before ordinary project-specific work. Any supported AI tool may execute when this shared context and local docs are available.

1. **DETECT:** If the prompt starts with an explicit slash skill/workflow command, execute it directly. Otherwise match the prompt against the workflow catalog and skill list.
2. **ANALYZE:** Choose the best option: execute directly, invoke a skill, activate a standard workflow, or compose a custom step combination.
3. **AUTO-SELECT:** Pick the best option yourself. Do not ask the user to choose between direct execution, skill, standard workflow, or custom workflow.
4. **ACTIVATE:** For a selected workflow, call `$start-workflow <workflowId>`; for a selected skill, invoke that skill; for a custom workflow, sequence custom steps directly; for direct execution, proceed with the task.
5. **CREATE TASKS:** task tracking for ALL workflow/skill/custom steps before execution when the selected path has multiple steps.
6. **PARALLELIZE:** Before executing the task list, tag each task `PAR` (independent inputs + write set disjoint from every other `PAR` task) or `SEQ` (name the blocking dependency), group `PAR` tasks into waves, declare the wave plan, and spawn each wave's sub-agents in ONE message — all-return barrier per wave, fan-out one level deep unless a sub-agent's own definition authorizes further fan-out. Sequential-by-default is a defect when tasks are independent; do not parallelize shared write targets, output-consuming tasks, trivial single-file work, ordering a skill or workflow explicitly fixes, or user-approval gates.
7. **EXECUTE:** Advance per the **Workflow Step Advancement & Parallel Phases** rule in your context instructions — model-driven; a sub-agent completion advances a step identically to an inline call; a parallel-phase group is an all-return barrier (advance only after ALL members return, never serialize it)

## Shared AI-SDD Protocol Markers

Source: `.claude/skills/shared/sync-inline-versions.md`

## SYNC:ai-sdd-artifact-contract

> **AI-SDD Artifact Contract** — Shared spec-driven development rules stay portable and source-owned.
>
> 1. Keep reusable AI-SDD principles in `.claude`; put repository-specific paths, commands, owners, products, and formats in project config/reference docs.
> 2. Preserve cycle: `spec -> plan -> tasks -> implement -> verify -> update spec/docs`.
> 3. Trace every requirement or invariant through decision, task, TC/test, source evidence, and docs/spec update.
> 4. Treat code-to-spec extraction as reference-only until accepted by the canonical spec owner.
> 5. Any supported AI tool may plan, implement, review, or verify with synced context; using multiple tools is optional.
> 6. Update `.claude` source first, then sync generated mirrors; do not manually edit `.agents`, `.codex`, or `AGENTS.md`. — why: mirrors are generated artifacts; hand-edits are overwritten on the next sync
> 7. If `docs/project-config.json`, root instruction files, or a required project-reference doc is missing or stale, auto-run `$project-init` or the narrow lower-level route before ordinary project-specific work.
>
> **Active reference:** `shared/sdd-artifact-contract.md` in the active skills root.

---

## SYNC:ai-sdd-artifact-contract:reminder

- **MANDATORY** Apply `shared/sdd-artifact-contract.md`; keep reusable AI-SDD in `.claude` and local rules in project docs.
- **MANDATORY** Code-to-spec extraction is reference-only until canonical acceptance; any supported AI tool may execute with synced context.
- **MANDATORY** Update `.claude` source before syncing generated mirrors; do not manually edit `.agents`, `.codex`, or `AGENTS.md`.
- **MANDATORY** Missing or stale project config, root instruction files, or required reference docs route project-specific work through `$project-init` or the narrow setup route automatically.
  **[TASK-PLANNING] [MANDATORY]** BEFORE executing any workflow or skill step, create/update task tracking for all planned steps, then keep it synchronized as each step starts/completes.

## [LESSON-LEARNED-REMINDER] [BLOCKING] Task Planning & Continuous Improvement — MANDATORY. Do not skip.

Break work into small tasks (task tracking) before starting. Add final task: "Analyze AI mistakes & lessons learned".

**Extract lessons — ROOT CAUSE ONLY, not symptom fixes:**

1. Name the FAILURE MODE (reasoning/assumption failure), not symptom — "assumed API existed without reading source" not "used wrong enum value".
2. Generality test: does this failure mode apply to ≥3 contexts/codebases? If not, abstract one level up.
3. Write as a universal rule — strip project-specific names/paths/classes. Useful on any codebase.
4. Consolidate: multiple mistakes sharing one failure mode → ONE lesson.
5. **Recurrence gate:** "Would this recur in future session WITHOUT this reminder?" — No → skip `$learn`.
6. **Auto-fix gate:** "Could `$code-review`/`$code-simplifier`/`$security-review`/`$lint` catch this?" — Yes → improve review skill instead.
7. BOTH gates pass → ask user to run `$learn`.
   **[CRITICAL-THINKING-MINDSET]** Apply critical thinking, sequential thinking. Every claim needs traced proof, confidence >80% to act.
   **Anti-hallucination principle:** Never present guess as fact — cite sources for every claim, admit uncertainty freely, self-check output for errors, cross-reference independently, stay skeptical of own confidence — certainty without evidence root of all hallucination.
   **AI Attention principle (Primacy-Recency):** Put the 3 most critical rules at both top and bottom of long prompts/protocols so instruction adherence survives long context windows.
   **Goal-driven execution:** Define success criteria first, loop until verified, and stop only when observable checks pass.
   **Tests verify intent:** Tests must protect business rules/invariants and fail when the protected intent breaks, not only mirror current behavior.

## Common AI Mistake Prevention (System Lessons)

- **Re-read files after context compaction.** Edit requires prior Read in same context; compaction wipes read state. Re-read before editing.
- **Grep for old terms after bulk replacements.** AI over-trusts find/replace completeness. Grep full repo after bulk edits for missed refs in docs/configs/catalogs.
- **Check downstream references before deleting.** Deletions cascade doc/code staleness. Map referencing files before removal.
- **After memory loss, check existing state before creating new.** Compaction wipes prior-work memory. Query current state to resume — never blindly duplicate.
- **Verify AI-generated content against actual code.** AI hallucinates APIs, class names, method signatures. Grep to confirm existence before documenting/referencing.
- **Trace full dependency chain after edits.** Changing a definition misses downstream consumers. Trace the full chain.
- **When renaming, grep ALL consumer file types.** Some file types silently ignore missing refs (no compile error). Search code, templates, configs, generated files.
- **Trace ALL code paths when verifying correctness.** Code existing ≠ code executing. Trace early exits, error branches, conditional skips — not just happy path.
- **Update docs that embed canonical data when source changes.** Docs inlining derived data (workflows, schemas, configs) go stale silently. Update all embedding docs alongside source.
- **Verify sub-agent results after context recovery.** Background agents may finish while parent compacted — grep-verify output, don't trust assumed completion.
- **Cross-check full target list against sub-agent assignments.** Parallel sub-agents by category miss boundary items. Reconcile union of assignments against target list before proceeding.
- **Sub-agents inherit knowledge only from their agent .md definition — use custom agent types, not built-in Explore.** Tool adoption = permission + knowledge + enforcement (numbered workflow step).
- **Persist sub-agent findings incrementally, not as a final batch.** Long sub-agents hit cutoffs before final write — findings lost. Instruct append-per-section to report file.
- **When debugging, ask "whose responsibility?" before fixing.** Trace caller (wrong data) vs callee (wrong handling). Fix at responsible layer — never patch symptom site.
- **Test failure → record a provisional verdict before trace/edit, then investigate.** Use the full five-way taxonomy: SOURCE-WRONG (production violates intent), TEST-WRONG (assertion/setup is stale), TEST-NOT-OPTIMAL (valid but fragile or low-signal test), ENVIRONMENT-BLOCKED (external state prevents a verdict), or AMBIGUOUS (intent/evidence cannot choose safely). Then trace root cause and triangulate against the governing spec (`docs/specs/**` if one exists) AND source. NEVER weaken an assertion, add a skip, relax a timeout, or change source merely to force green.
- **Grep ALL removed names after extraction/refactoring.** Primary file "done" ≠ secondary files clean. Grep entire scope for every removed symbol before declaring complete.
- **Assume existing values are intentional — ask WHY before changing OR flagging one as a defect.** Pattern-matching as "wrong" skips context. Before changing or reporting any constant/limit/flag/cutoff: read comments, git blame, the CALLER's ordering (the guarantee that makes the value correct usually lives in code running immediately BEFORE the cited line), and 2+ sibling call sites of the same convention. A doc stating WHAT without WHY is missing rationale, not proof of a missing guard — and in a validation pass, an accurate `file:line` citation proves the transcription, never the defect.
- **Verify ALL affected outputs, not just the first.** One build green ≠ all green. Multi-stack changes (backend/frontend/tests/docs) require verifying EVERY output.
- **Evaluate fit before copying a nearby pattern.** Closest example ≠ matching preconditions — verify the new context shares the same constraints, base classes, scope, lifetime.
- **Holistic-first debugging — resist nearest-attention trap.** Don't dive into first plausible cause. List EVERY precondition (config, env vars, paths, DB, endpoints, creds, versions, DI, data). Verify each against evidence (grep/query — not reasoning). Ask "what would falsify this?" — if nothing, it's not a hypothesis. Most expensive failure: going deeper in "obvious" layer while bug sits in layer never questioned.
- **Surgical changes — apply the diff test (context-aware).** Two modes: (1) Bug fix → every line traces to the bug; no restyling; orphan cleanup only for imports YOUR changes made unused. (2) Review/enhancement → implement improvements AND announce as "Enhancement beyond main request: [what]". Never silently scope-creep. Diff test: "Would this line exist if I wasn't asked to do X?" — if no, delete or announce.
- **Surface ambiguity before coding — don't pick silently.** Multiple valid interpretations → present each with effort: "[Request] could mean (1) [N h], (2) [N h]. Which matters?" List scope/format/volume/constraints assumptions first. If simpler path exists, say so. Never silently pick.
- **[MANDATORY FIRST ACTION] ALWAYS activate a suitable skill or workflow BEFORE responding.** Match task against workflow catalog + skill list; invoke via skill invocation or `$start-workflow <workflowId>`. NEVER answer or write code before checking. Skip = protocol violation.
- **Why-Review adversarial mindset — apply when reviewing any plan, decision, or design.** Default SKEPTIC not VALIDATOR: steel-man a rejected alternative, invert each stated reason ("what does it sacrifice?"), stress-test top 2-3 assumptions, run pre-mortem ("ships, fails in 3 months — what breaks?"), surface 1-2 alternatives author missed. Section presence ≠ quality; quality = causal reasoning + concrete mitigations + evidence, not "it's better" or "monitor closely".
- **Front-load report-write in sub-agent prompts for large reviews.** Many-file sub-agents hit budget before final write — findings lost. Design prompts so: (1) report-write is first explicit deliverable, (2) append per-file/section (not batched), (3) scope bounded so reads don't exhaust budget. Truncated mid-sentence with no report file → spawn narrower scope, don't retry same prompt.
- **After context compaction, re-verify all prior phase outcomes before continuing.** Summaries describe intent, not environment state (git index, filesystem, processes). On resume, FIRST audit: git status, re-read modified files, verify filesystem. Every "completed" claim is an untested hypothesis until evidence confirms.
- **OOM/memory: check row count before row size.** Triage: (1) Unbounded query — no DB filter for trigger? Push filter to DB; eliminates OOM. (2) Large rows? Projection reduces proportionally. Row reduction > projection in ROI.
- **Assert the outcome your system OWNS, never the intermediate state your INFRASTRUCTURE owns.** When testing anything asynchronous (queue/broker delivery, retries, background jobs, caches, replication), assert the final business/entity state. NEVER assert the delivery bookkeeping — consume/send status, attempt counts, last-error, row existence or counts in a broker, scheduler, or outbox/inbox table. That bookkeeping lives in shared infrastructure that ANY co-running process (a peer worker, a second replica, a leftover local container) can write, usually under a deterministic shared key, so the assertion silently tests the developer's environment instead of the system: green when run alone, flaky the instant anything else shares that broker + database. Gate question for every assertion: "would this hold no matter WHICH process did the work?" — if no, assert the converged data state instead. Corollary: process-local fault injection and in-process telemetry cannot gate work any process may perform — use them as stress amplifiers (arm → bounded window → disarm → assert convergence), never as preconditions.
- **Keep domain concepts out of generic/shared/infrastructure layers.** Reusable layer (shared library, framework, infra module) must reference NO consumer-specific domain concept — tenant/customer/product IDs, business entities, feature rules. Leak compiles + runs → passes review silently while coupling the "reusable" layer to one consumer. Keep shared type domain-free; push domain fields/logic down into the consumer via subclass/composition. — why: a layer coupled to one consumer's domain is no longer reusable.

<!-- CODEX:SYNC-PROMPT-PROTOCOLS:END -->
