---
name: why-review
description: '[Code Quality] Use when reviewing rationale and change quality for plans, PBIs, commits, diffs, docs, specs, reports, or explicit artifacts.'
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

> **[GOAL REMINDER — MUST ATTENTION CRITICAL]**
>
> Ensure every review target is reasonable, correct, proof-backed, and best-practice aligned.
> **ALWAYS ASK THE 3 TRADE-OFF QUESTIONS (every decision AND every recommendation you make):** (1) **is there any trade-off?** — name what it sacrifices; "none" is an unfinished analysis, not an answer; (2) **is it worth it?** — gain vs cost, who pays, when → WORTH IT / NOT WORTH IT / UNCLEAR; (3) **is the trade-off material enough to confirm with the user?** — irreversible, cost shifted to someone else, one quality attribute traded for another, boundary crossed, high-consequence path, or UNCLEAR → STOP and confirm by asking the user directly BEFORE the verdict. NEVER resolve a material trade-off silently. — why: naming a benefit without its price is an endorsement, not a review, and a one-way door is the user's call to walk through, never yours.
> **MANDATORY SECOND PASS (full mode):** whenever Round 1 produces ANY finding, you MUST call `$why-review --validate-findings` a SECOND time on those findings to confirm each is correct and reasonable BEFORE handoff. NEVER skip it; NEVER suppress, demote, or under-report findings to dodge it. The self-recursive review loop bound as the first full-mode action — the **protocol loop primarily** (host-independent), plus a `/goal` Stop-hook gate WHEN available — BLOCKS stopping until findings are validated. — why: an unvalidated finding is an unproven claim, and a second self-review catches the misreads and inflation Round 1 rationalized.

<!-- PROMPT-ENHANCE:STEP-TASK-ANCHOR:START -->

> **[BLOCKING]** Execute skill steps in declared order. NEVER skip, reorder, or merge steps without explicit user approval.
> **[BLOCKING]** Before each step or sub-skill call, update task tracking: set `in_progress` when step starts, set `completed` when step ends.
> **[BLOCKING]** Every completed/skipped step MUST include brief evidence or explicit skip reason.
> **[BLOCKING]** If Task tools are unavailable, create and maintain an equivalent step-by-step plan tracker with the same status transitions.

<!-- PROMPT-ENHANCE:STEP-TASK-ANCHOR:END -->

## Quick Summary

**Goal:** Resolve the requested review target and apply the matching adversarial review path (plan/PBI rationale, code changes, docs/spec/report, findings, or explicit artifact) so decisions, findings, and plans survive adversarial rationale review before downstream work proceeds.

**Summary:** (read-this-if-nothing-else digest — the skill's purpose + ALL main steps)

- **PURPOSE** — be the adversarial rationale reviewer: every plan/PBI/diff/doc/spec/report/finding survives a SKEPTIC pass before downstream work proceeds; success metric is Easy-to-Change (lower future change cost or reject). Gate EVERY finding on `file:line` + severity + confidence.
- **STEP 1 — DETECT MODE FIRST** (recursion control): `--validate-findings` is TERMINAL — NEVER re-invokes `$why-review`, NEVER runs the gate, NEVER spawns a sub-agent; full mode may call itself ONCE in validate-findings mode. Non-negotiable guard. — why: any of these from terminal mode loops infinitely.
- **STEP 2 — FULL-MODE FIRST ACTION** → bind the self-recursive review loop: the **protocol loop is the primary, host-independent binding** (you self-drive review → validate → reconcile → full re-review until CLEAN with no new findings; max 2 re-dos, then escalate), and a `/goal` gate is an **optional accelerator invoked WHEN available** (its absence never weakens the loop) — NEVER bind it in terminal mode; "self-fix" = reconcile this review's OWN findings set, not code. THEN Task Bootstrap: create phase tasks + the MANDATORY Findings Validation Gate closing task.
- **STEP 3 — RESOLVE TARGET TYPE** before any review (commit/PR/diff → code-change; PBI/spec/doc → artifact; "no active plan" ONLY for an unresolved plan-rationale request — NEVER silently convert), read the active Goal Contract, then route by concern (code-reviewer / security-auditor / performance-optimizer / general-purpose). **Integration tests in the target → apply the Integration-Test-Review Linkage** (read `$integration-test-review`'s 8 gates, or delegate in standalone full mode) — SKIPPED under its 4-row recursion guard.
- **STEP 4 — REVIEW as SKEPTIC** → complete ALL 7 Anti-Bias Gate boxes (steel-man rejected alt · unseen alternative · args against · stressed assumptions · pre-mortem · pros/cons symmetry · **Trade-Off Interrogation Gate**) + Validation Checklist (presence AND quality depth) + Round 2 re-review; triangulate spec↔tests↔code — any disagreeing face is a finding, presence is NEVER a pass.
- **TRADE-OFF GATE — ALWAYS ASK, on every decision AND every recommendation YOU make:** (1) **is there any trade-off?** name the sacrifice — "none" is an unfinished analysis, so state the dimensions checked; (2) **is it worth it?** gain vs cost, who pays, when → WORTH IT / NOT WORTH IT / UNCLEAR; (3) **is it material enough to confirm with the user?** irreversible · cost shifted elsewhere · quality attribute traded · boundary crossed · high-consequence path · UNCLEAR → **STOP and confirm by asking the user directly BEFORE the verdict**. Emit the `Trade-Off Assessment` table; a material trade-off unconfirmed = NEVER PASS.
- **STEP 5 — FINDINGS VALIDATION GATE** on your OWN findings (any severity): re-invoke terminal `--validate-findings`, reconcile, RE-DO the full review until CLEAN with no new findings (max 2), then ask next step by asking the user directly (+ conditional `$llm-council`). Dual-feedback: a behavior-changing finding needs BOTH a spec-drift verdict (CODE-WRONG / SPEC-STALE / AMBIGUOUS / SPEC-SILENT / in-sync) AND a test-feedback action; SPEC-SILENT also REQUIRES §4 BR/§3 AC + §8 TC enrichment — a missing axis is HAS-ISSUES, never clean.

**Workflow:** Detect mode/target → (full mode only) bind the self-recursive review loop (protocol-primary; optional `/goal` accelerator when available) → route path/docs/graph/sub-agent focus → review dimensions/adversarial gates/Easy-to-Change → validate findings via terminal `--validate-findings` → reconcile + holistic full re-review until CLEAN with no new findings (max 2 re-dos) → ask next step in full mode.

**Key Rules:** MUST ATTENTION resolve target type BEFORE review. MUST ATTENTION every finding needs `file:line`, severity, confidence, best-practice rationale. MUST ATTENTION ask the 3 trade-off questions on every decision AND every recommendation (trade-off? worth it? material → confirm with user); NEVER accept "no trade-off" unexamined, NEVER decide a material trade-off silently. NEVER say "No active plan" except unresolved plan-rationale request. NEVER call `$why-review` from `validate-findings`. MUST ATTENTION judge by Easy-to-Change: lower future change cost or reject.

## Your Mission

<task>
$ARGUMENTS
</task>

## Review Mode (DETECT FIRST — recursion control)

Detect mode from `$ARGUMENTS` BEFORE any review work:

| Mode                  | Trigger in `$ARGUMENTS`                                                                         | What it runs                                                                                                                                                                                                             | Recursion                                                                                                 |
| --------------------- | ----------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------- |
| **full** (default)    | no `validate-findings` token                                                                    | Full design-rationale review (Validation Checklist + Adversarial Rounds below), THEN the **Findings Validation Gate** closing task — which re-invokes THIS skill in `validate-findings` mode on its own findings.        | May call itself **ONCE** in `validate-findings` mode (same session).                                      |
| **validate-findings** | `$ARGUMENTS` contains `--validate-findings` / `mode=validate-findings` / `validate findings in` | ONLY the **Findings Validation Routine** against the supplied findings/report — verify each finding is correct, proof-backed, reasonable, best-practice; surface missed enhancements; emit a CLEAN / HAS-ISSUES verdict. | **TERMINAL — NEVER calls `$why-review`, NEVER runs the gate, NEVER spawns a sub-agent.** Stops recursion. |

> **Recursion guard (NON-NEGOTIABLE):** `validate-findings` terminates. MUST NOT invoke `$why-review` or validation gate — prevents infinite recursion. Re-do loop lives in CALLER, max 2 re-dos, SAME main-agent session, NEVER spawned sub-agent.

> **In `validate-findings` mode:** skip full Validation Checklist, Adversarial Rounds, Task Bootstrap, Next-Steps council gate. Jump straight to **Findings Validation Routine**, emit verdict, return to caller.

## Bind the Self-Recursive Review Loop (full mode — FIRST ACTION, after mode detection; protocol-first, `/goal` optional)

> **MUST ATTENTION:** In **full mode only**, the FIRST action after mode detection — before Task Bootstrap, before any review work — binds this skill's self-recursive review loop so you cannot stop until this review's own findings are all validated and a holistic re-review surfaces nothing new (or a bounded escalation fires). The loop is bound by TWO layers: the **protocol loop (primary, host-independent)** and an **optional `/goal` accelerator**. Correctness rides on the protocol loop — the project rule is that hooks/commands are accelerators only, so `/goal`'s absence NEVER weakens the loop.

**Entry gate:**

- **Run** in full mode (no `validate-findings` token).
- **SKIP** in `validate-findings` terminal mode — that mode only returns a verdict to its caller and MUST NOT bind a loop, install a goal, create a closing task, or loop (recursion guard). Record nothing.

**1. Protocol loop — ALWAYS binding (hook/command-independent).** You, the running agent, are personally responsible for not stopping until the loop converges or bounded-escalates. This binds Claude, Codex, and Copilot equally, whether or not `/goal` exists:

> Run the full adversarial review (Validation Checklist + both Adversarial Rounds) over the whole target → run `$why-review --validate-findings` on the findings → reconcile (drop unproven/inflated findings, fix proof gaps, ADD surfaced findings/enhancements) → re-run the FULL review over the WHOLE target combined with the reconciled findings (not just re-checking the changed findings) → loop until a complete pass yields zero new findings and validation returns CLEAN, or a bounded blocker escalates. Max 2 re-do rounds, then escalate by asking the user directly. Do not stop while a finding is unvalidated or a re-review would surface new findings.

Treat this as a standing obligation you re-read at the Findings Validation Gate — NOT a one-time note you can rationalize away after the first pass.

**2. `/goal` command — invoke as an accelerator WHEN AVAILABLE.** If a `/goal` command exists and you are permitted to run it in this environment, ALSO invoke it (a real command call, NOT a paraphrase, NOT a Goal Contract file substituted for it) with a condition encoding THIS skill's self-recursive loop, so a session Stop hook mechanically enforces it:

```
/goal why-review self-recursive loop: run the full adversarial review (Validation Checklist + both Adversarial Rounds) over the whole target → run $why-review --validate-findings on the findings → reconcile (drop unproven/inflated findings, fix proof gaps, ADD surfaced findings/enhancements) → re-run the FULL review over the WHOLE target combined with the reconciled findings (not just re-checking the changed findings) → loop until a complete pass yields zero new findings and validation returns CLEAN, or a bounded blocker escalates. Max 2 re-do rounds, then escalate by asking the user directly. Do not stop while a finding is unvalidated or a re-review would surface new findings.
```

The `/goal` Stop hook blocks stopping until the condition holds and auto-clears when met — do not tell the user to clear it.

**If `/goal` is unavailable, unregistered, or not permitted** (e.g. Codex/Copilot, or a Claude run without the command): DO NOT error, DO NOT block, and DO NOT invent a stand-in gate. Record ONE line where you track the review (the closing Findings Validation Gate task, or the active Goal Contract if one exists) — `/goal accelerator unavailable — review loop bound by protocol (above)` — and proceed. The protocol loop IS the gate, enforced by discipline instead of a hook.

> **why-review fixes its OWN findings set, not code.** "Self-fix" here = reconcile the findings report so every surviving finding is correct, proof-backed, reasonable, best-practice, and nothing is missed — the same loop the Findings Validation Gate runs, now made unabandonable by the goal gate. Code/spec/test fixes remain the caller's job; this skill is review-only.

## Task Bootstrap (full mode — do at skill START)

Before review work, task tracking phase tasks AND required closing task:

- [ ] `[Why-Review] Bind self-recursive review loop — protocol-primary; optional /goal accelerator when available (full mode only)` — in_progress **(MANDATORY FIRST TASK — skip in `validate-findings` mode)**
- [ ] `[Why-Review] Findings Validation Gate — if ANY findings exist, run $why-review --validate-findings on them; re-do until CLEAN (max 2)` — pending **(MANDATORY CLOSING TASK)**

> Create at START. Keep the closing task `pending` until findings exist; then execute before skill completes. In `validate-findings` mode, do NOT create either task.

## First Principle — Easy to Change

> **Success metric: future change cost.** DRY, SRP, abstraction, design patterns, naming, layering, tests exist to make next change cheaper.

When reviewing code/refactor/test/abstraction, ask: **does this make next change cheaper or more expensive?**

- Reject "best practices" raising change cost: premature abstraction, speculative generality, leaky indirection, ceremony without payoff.
- Name real enemies in findings: **coupling, hidden state, duplicated knowledge, unclear intent, irreversible decisions exposed too early**.
- Prefer simple design easy to change over sophisticated design hard to change.

Apply before any rule/checklist below; if downstream rule raises change cost, this principle wins.

---

## Adversarial Review Mindset (NON-NEGOTIABLE)

**Default stance: SKEPTIC, not validator. Your job is to find what's wrong, not confirm what's right.**

> **Confirmation bias trap:** After reading a coherent plan, AI naturally finds reasons to agree. Current context (post-plan, post-fix) amplifies this — you already saw the reasoning and rationalized it. This section breaks that loop. — why: a reviewer who already endorsed the reasoning cannot also be its skeptic without a forced reset.

### Adversarial Techniques (apply ALL before concluding)

| Technique               | Think                                                                                                                  |
| ----------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| Steel-Man               | Argue FOR rejected alternative. Would a 10-year domain senior choose it? If yes, dismissal needs stronger proof.       |
| Why NOT?                | For every "chose X because Y", ask what X sacrifices.                                                                  |
| Assumption Stress Test  | List top 3 assumptions; ask impact if wrong. Strong plan survives 2/3 false.                                           |
| Pre-Mortem              | Assume 3-month production failure; write one plausible scenario.                                                       |
| Unseen Alternatives     | Identify 1-2 approaches not mentioned; absence without exclusion reasoning = weak coverage.                            |
| Pros/Cons Symmetry      | Count chosen-approach pros/cons. Pros > cons by 2:1 means likely bias.                                                 |
| Contrarian Pass         | Before finding/verdict, argue opposite conclusion in 2 sentences; choose stronger argument.                            |
| Trade-Off Interrogation | Ask the 3 questions (below): is there a trade-off? · is it worth it? · is it material enough to confirm with the user? |

### Forbidden Patterns

| Forbidden pattern                   | Required correction                                                                              |
| ----------------------------------- | ------------------------------------------------------------------------------------------------ |
| "Looks good because..."             | Lead with challenges first.                                                                      |
| Presence = quality                  | Test quality depth; real alternatives, causal rationale.                                         |
| Vague rationale                     | Demand metric + cost: better at what cost?                                                       |
| Asymmetric trade-offs               | Treat 3 pros / 1 con as incomplete analysis.                                                     |
| "Looks fine"                        | Provide adversarial challenge evidence.                                                          |
| "No trade-off" / "pure win"         | Name the dimensions checked and why each is unaffected; unexamined ≠ absent.                     |
| Material trade-off decided silently | Escalate to the user by asking the user directly; a one-way door is never yours to walk through. |

### Anti-Bias Gate (MANDATORY before finalizing verdict)

Complete ALL 7 checks before writing the final verdict (MUST ATTENTION):

- steel-man at least one rejected alternative (argue FOR it)
- identify at least 1 alternative NOT in the plan
- list 2-3 arguments AGAINST the chosen approach
- surface 2-3 hidden assumptions with stress tests
- run the pre-mortem (one concrete failure scenario)
- check pros/cons symmetry
- run the **Trade-Off Interrogation Gate** below (trade-off named · worth-it verdict · materiality escalation decided)

Any check incomplete → adversarial review NOT complete. Go back.

## Trade-Off Interrogation Gate (MANDATORY — no verdict, no finding, no recommendation without it)

> **[BLOCKING]** Ask these THREE questions EVERY time — about the decision under review AND about every recommendation YOU make. — why: a review that names benefits without naming their price is an endorsement, not a review; and the biggest trade-offs are the ones nobody wrote down.

**1. Is there any trade-off?** Name what this decision/recommendation SACRIFICES. Every choice buys something with something. "None" is NOT an acceptable answer — it is an unfinished analysis. To claim no material trade-off, state which dimensions you checked and why each is unaffected:

> future change cost · complexity · performance/latency · memory/cost · coupling · reversibility · migration burden · operational/ops load · blast radius · security posture · testability · team skill/ramp · delivery time · UX.

**2. Is it worth it?** Weigh gain against sacrifice EXPLICITLY — **what is gained · what it costs · who pays · when it comes due** — then emit one verdict: **WORTH IT / NOT WORTH IT / UNCLEAR**. Anchor on Easy-to-Change: a trade-off raising future change cost needs a proportionate, named payoff, not a vague one. "Better" without a metric and a cost FAILS this question.

**3. Is the trade-off material enough to CONFIRM WITH THE USER?** A material trade-off is the user's call, never yours. MATERIAL when ANY row below holds:

| Material when the trade-off…                     | Examples                                                                            |
| ------------------------------------------------ | ----------------------------------------------------------------------------------- |
| Is irreversible — a one-way door                 | data migration, public API/contract shape, storage format, framework/vendor lock-in |
| Shifts cost onto someone else                    | another team, ops/on-call, the future maintainer, the end user                      |
| Trades one quality attribute for another         | correctness↔speed, security↔convenience, latency↔cost, simplicity↔flexibility       |
| Crosses a boundary                               | client↔server tier seam, service contract, event contract, shared library           |
| Sits on a high-consequence path                  | auth, money, data integrity, breaking change, High/Medium residual risk             |
| Cannot be evidenced (worth-it verdict = UNCLEAR) | gain or cost unquantifiable from available evidence                                 |

- **MATERIAL → STOP and confirm by asking the user directly** BEFORE the verdict stands: state the trade-off, both options, what each sacrifices, your recommendation. NEVER resolve a material trade-off silently on the user's behalf, and NEVER bury it as a Low-severity note.
- **NOT material → record it inline** in the Trade-Off Assessment table with a one-line justification and proceed; no escalation needed.
- In `validate-findings` terminal mode: **assess and record, do NOT escalate** — that mode asks nothing (see Next Steps exemption); flag the unescalated material trade-off in the verdict so the CALLER escalates it.

**Output:** every review emits the `Trade-Off Assessment` table (see Output Format) — one row per reviewed decision and per recommendation you make. An empty table with findings present is an incomplete review.

## Target Resolution (DO THIS BEFORE REVIEW)

Analyze user request, not only literal argument shape. Determine target, then choose matching path.

| User request / evidence                              | Review path                        | Required target work                                                                                                                  |
| ---------------------------------------------------- | ---------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| Explicit plan directory, `plan.md`, phase files      | Plan-rationale review              | Read `plan.md` and all `phase-*.md` files.                                                                                            |
| PBI/story/spec planning artifact, rationale request  | PBI/artifact rationale review      | Read the named artifact and related acceptance/design/risk sections; if it references plan files, read those too.                     |
| Commit SHA, `Commit: ...`, PR/merge commit, git diff | Code-change review                 | Establish the diff range, read changed files, run graph impact when available, and apply code-review/adversarial review protocols.    |
| Branch comparison or uncommitted changes             | Code-change review                 | Use the requested branch/diff or `git diff`; read changed files and tests/docs touched by the diff.                                   |
| Docs/spec/report/findings path                       | Artifact review                    | Read the target artifact and verify claims against source evidence; use rationale checklist only where the artifact is a plan/PBI.    |
| Ambiguous request                                    | Infer from evidence; ask if unsafe | Prefer a reasonable target from the request and repo evidence. Ask only when two plausible review paths would produce different work. |

**Important defaults:**

1. Commit hash / `Commit:` block => code-change review, not "no active plan."
2. PBI file => review that PBI/artifact; no `plans/**/plan.md` wrapper required.
3. "No active plan found. Run `$plan` first." valid ONLY for unresolved plan-rationale requests.
4. MUST ATTENTION record target type, evidence, confidence; NEVER silently convert target types.

**Active-goal read (BEFORE judging rationale):** Resolve active Goal Contract per goal-contract-satisfaction-loop protocol (active plan `goal.md` → `plans/goals/{YYMMDD-HHmm}-{slug}/goal.md`). When one exists, review artifact's rationale AGAINST saved Original Request, Purpose, Success Criteria — flag rationale justifying work the saved goal never asked for, and saved required criteria the artifact's reasoning never addresses. When none exists, record `No active goal — rationale reviewed against the current request only.` Full mode only; `--validate-findings` terminal mode skips this read.

### Review Focus Routing

| Detected concern                                                                                    | Primary focus / sub-agent route                                                                                                                                                                            |
| --------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Source code / diff                                                                                  | `code-reviewer` + embedded code-review protocols.                                                                                                                                                          |
| Integration/E2E tests in the target, OR a behavior change whose code has covering integration tests | Apply the **Integration-Test-Review Linkage** below — `$integration-test-review` owns the 8 test-quality gates; this skill reads its protocol (Mode A) or delegates to it (Mode B), never re-derives them. |
| Auth, secrets, permissions, data                                                                    | `security-auditor` if available; otherwise `code-reviewer` with explicit security pass.                                                                                                                    |
| Latency, scale, memory, queries                                                                     | `performance-optimizer` if available; otherwise `code-reviewer` with explicit performance pass.                                                                                                            |
| Plan / PBI / doc / spec                                                                             | `general-purpose` with rationale/artifact dimensions.                                                                                                                                                      |
| Mixed target                                                                                        | Split focused passes by concern; aggregate findings after all passes.                                                                                                                                      |

### Code-Change Review Path

When target is code changes:

1. Resolve the diff source:
    - Commit SHA: use `git show --name-status` and diff against its first parent.
    - Merge commit: default to first-parent diff unless the user specifies another parent/range.
    - Branch/range: use the user-supplied range.
    - Uncommitted changes: use `git diff` plus staged diff if relevant.
2. **Comprehend change context + trace full pipeline across BOTH boundaries (MANDATORY for code-change targets; N/A for pure plan/PBI/doc targets).** Before deep file judging, write a one-line Change Context (what · intent · originating tier · main affected flow), then apply BOTH inlined blocks below: `SYNC:cross-stack-impact-trace` for the client↔server tier seam (BE→FE forward, FE→BE backward) and `SYNC:cross-service-check` for the microservice / event / external / loosely-coupled boundary. Classify each seam/touchpoint NONE / ADDITIVE / BREAKING; a BREAKING seam whose other-side consumer is un-updated in the same diff is a HIGH-min finding. State `Single-tier / monolith — N/A` when no cross-boundary seam exists.
3. Read the changed files and any nearby tests/docs required to prove behavior.
4. **Integration-test detection (CONDITIONAL).** If the target contains integration/E2E test files, OR changes behavior-bearing code that has covering integration tests, run the **Integration-Test-Review Linkage** below before judging the `Test/spec/doc sync` dimension. State `No integration tests in target — linkage N/A` when neither holds.
5. Read project reference docs based on changed file types before judging patterns.
6. If `.code-graph/graph.db` exists, run graph blast-radius or trace on key changed files before concluding.
7. Apply embedded code-review protocols by serial focused pass: bug detection, design patterns quality, logic/intention, test/spec verification, graph investigation, Easy-to-Change.
8. Output findings first, with `file:line` evidence, severity, confidence, and tests/docs gaps.

### Integration-Test-Review Linkage (CONDITIONAL — advisory, guarded)

> **Purpose:** this skill's `Test/spec/doc sync` dimension asks _"does evidence prove tests/specs/docs protect the intended invariant?"_ — but the 8 gates answering it (assertion value · data state · repeatability · domain logic · spec traceability · three-way sync · change coverage · scenario fidelity) belong to `$integration-test-review`. Route to that owner; NEVER re-derive a weaker copy here. — why: a rationale review judging test quality by eye endorses assertions it never mutation-tested.

**Recursion guard — SKIP entirely when ANY row holds.** Record the deferral line, then proceed; NEVER invoke or read:

| Suppressing context                                                                                                                                      | Evidence                                                                                                                                                                                           | Deferral line to record                                                      |
| -------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| Mode is `validate-findings`                                                                                                                              | Terminal mode — no sub-skill calls at all                                                                                                                                                          | `Linkage N/A — validate-findings is terminal.`                               |
| Invoked by `$integration-test-review` Phase 9                                                                                                            | It calls this skill at `integration-test-review/SKILL.md:429-431` and guards the reverse edge at `:438`                                                                                            | `Linkage deferred — invoked by $integration-test-review Phase 9.`            |
| Invoked by `changes-review` in ANY phase — 0.8 parallel rationale dimension, 6 validate-findings, or 7.5 holistic — or inside `$workflow-review-changes` | `changes-review/SKILL.md:395` (Phase 0.8, which states this deferral as a binding sub-agent constraint), `:867` (Phase 6), `:938` (Phase 7.5); its Phase 3.7 (`:608-626`) already owns the gate    | `Linkage deferred to changes-review Phase 3.7 / parent workflow step.`       |
| Invoked by `$debug-investigate`'s Root Cause Validation gate                                                                                             | `debug-investigate/SKILL.md:151`; inside `integration-test-verify-loop` that gate fires in a round already running `$integration-test-review` (`integration-test-verify-loop/SKILL.md:98,110,495`) | `Linkage deferred — debug-investigate gate; the verify loop owns the audit.` |

> — why: unguarded, this edge closes a cycle (`why-review` → `integration-test-review` → Phase 9 → `why-review`) and re-creates the duplicate-ownership defect `integration-test-verify-loop/SKILL.md:31` removes.

**Mode A — READ the protocol (DEFAULT).** Read `.claude/skills/integration-test-review/SKILL.md` §"The 8 Quality Gates"; apply Gates 1-8 as review lenses over target tests. Cheap — no recursion, no sub-skill call. Findings enter this review's normal finding set with `file:line` evidence + severity.

**Mode B — DELEGATE to `$integration-test-review` (ESCALATION).** Invoke ONLY when ALL hold: no guard row fired · standalone full-mode review · target diff itself contains integration test files. Its GAP / SPEC-GAP verdicts become ordinary findings for this review's Findings Validation Gate.

**Advisory, NEVER blocking** — matches this skill's `Enforcement: Advisory` scope; mandatory coverage lives in `changes-review` Phase 3.7. — why: without this linkage a standalone rationale review silently skips test quality.

### Rationale / Artifact Review Dimensions

Run one focused pass per applicable dimension; do NOT scan all dimensions simultaneously.

| Dimension             | Think                                                                                                                                                                  |
| --------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Target fit            | Did we resolve what user asked, with evidence and confidence?                                                                                                          |
| Goal alignment        | Does the rationale serve the saved Goal Contract's purpose and success criteria — or drift past them?                                                                  |
| Rationale depth       | Are alternatives real, causal, symmetric, assumption-aware?                                                                                                            |
| Trade-off honesty     | What does this SACRIFICE, is it worth it, and is the trade-off material enough to confirm with the user? An unpriced benefit is a rationale gap.                       |
| Behavioral risk       | What breaks in happy, error, edge, and rollback paths?                                                                                                                 |
| Cross-boundary impact | Does a changed contract break a consumer on the other client↔server tier (BE↔FE), or a loosely-coupled/external service or event consumer? (tier seam + service/event) |
| Test/spec/doc sync    | Does evidence prove tests/specs/docs protect the intended invariant and avoid stale claims?                                                                            |
| Future change cost    | Does recommendation reduce coupling, hidden state, duplication, unclear intent?                                                                                        |

## Validation Checklist

For plan/PBI/artifact rationale reviews, read resolved target first. If plan directory, read `plan.md` and all `phase-*.md` files. Check **presence AND quality depth**.

For code-change reviews, use Code-Change Review Path instead of forcing plan checklist. Still include adversarial analysis, pre-mortem, assumptions, evidence, findings validation.

> **Rule:** Presence alone is NOT a pass. A section that exists but contains weak, asymmetric, or unverified reasoning FAILS quality depth.

### Required Sections (in plan.md or phase files)

| #   | Section                     | Presence Check                                    | Quality Depth Check (adversarial)                                                                                                                                                  |
| --- | --------------------------- | ------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | **Problem Statement**       | 2-3 sentences describing the problem              | Is the problem scoped correctly? Could it be framed differently to lead to a different solution? Are symptoms confused with root cause?                                            |
| 2   | **Alternatives Considered** | Minimum 2 alternatives listed with pros/cons      | Are alternatives real (not strawmen)? Would a domain expert seriously consider each? Are the cons of the CHOSEN approach listed, not just cons of the others?                      |
| 3   | **Design Rationale**        | Explicit reasoning linking decision to trade-offs | Is reasoning causal (X leads to Y) or just descriptive (X is better)? Are hidden assumptions surfaced? Does it address failure modes, not just success modes?                      |
| 4   | **Risk Assessment**         | At least 1 risk per phase                         | Are risks ranked by severity? Are mitigations concrete actions or vague intentions ("monitor closely")? Is there at least one risk about the approach itself (not just execution)? |
| 5   | **Ownership**               | Clear who maintains code post-merge               | Implicit OK (author owns), explicit better                                                                                                                                         |

## Residual Risk Gate

- Challenge over-broad scope, weak rejected alternatives, and any High/Medium residual risk.
- High/Medium risks must be fixed, reduced, or explicitly accepted by user/owner before PASS.
- AI-extracted specs/TCs are not accepted evidence unless the canonical owner/review gate accepted them.

### Optional (Flag if Missing, Don't Fail)

| #   | Section                  | When Required                           | Quality Depth Check                                                |
| --- | ------------------------ | --------------------------------------- | ------------------------------------------------------------------ |
| 6   | **Operational Impact**   | Service-layer or API changes            | Are rollback steps defined? What breaks if this is reverted?       |
| 7   | **Cross-Service Impact** | Changes touching multiple microservices | Are all downstream consumers identified? Who needs to be notified? |
| 8   | **Migration Strategy**   | Database schema or data changes         | Is there a rollback plan? Is it tested on a data sample?           |

## Output Format

```markdown
## Why-Review Results

**Plan:** {plan path}
**Target Type:** {plan/PBI/code changes/docs/spec/report/artifact}
**Target:** {path, commit, branch range, or artifact}
**Date:** {date}
**Verdict:** PASS / NEEDS WORK

### Checklist

| #   | Check                   | Presence  | Quality Depth | Notes                                                                |
| --- | ----------------------- | --------- | ------------- | -------------------------------------------------------------------- |
| 1   | Problem Statement       | ✅/❌     | ✅/⚠️/❌      | {what's strong / what's weak}                                        |
| 2   | Alternatives Considered | ✅/❌     | ✅/⚠️/❌      | {are they real or strawmen?}                                         |
| 3   | Design Rationale        | ✅/❌     | ✅/⚠️/❌      | {causal or just descriptive?}                                        |
| 4   | Risk Assessment         | ✅/❌     | ✅/⚠️/❌      | {concrete mitigations or vague?}                                     |
| 5   | Ownership               | ✅/❌     | ✅/⚠️/❌      | {details}                                                            |
| 6   | Bugfix Debugger Trace   | ✅/❌/N/A | ✅/⚠️/❌      | {final state, feeder paths, hypothesis matrix, owner, forward proof} |
| 7   | Trade-Off Gate          | ✅/❌     | ✅/⚠️/❌      | {trade-off named? worth-it verdict? material → user confirmed?}      |

> ✅ Strong ⚠️ Weak/Partial ❌ Missing

### Adversarial Analysis

**Strongest arguments AGAINST the chosen approach:**

1. {argument 1 — cite specific plan text that weakens under this pressure}
2. {argument 2}
3. {argument 3 if applicable}

**Unexamined alternatives** (not mentioned in the plan):

- {alternative A} — why it might be worth considering
- {alternative B if applicable}

**Weakest assumptions** (if wrong, the plan breaks):

1. {assumption} — impact if false: {consequence}
2. {assumption} — impact if false: {consequence}

**Bugfix trace challenge** (required for bugfix, failed verification, stale/incorrect final output, regression, or behavior-changing fix plans):

- Observed final state and final reader proven? {yes/no/N/A}
- All feeder paths enumerated or explicitly bounded? {yes/no/N/A}
- Hypothesis matrix includes ruled-out and latent causes, not only the chosen cause? {yes/no/N/A}
- Owning fix layer protects all downstream consumers? {yes/no/N/A}
- Forward convergence proof and tests/proof mapping make the symptom impossible or detect recurrence? {yes/no/N/A}

**Pre-mortem** (assume it ships and fails in 3 months):

> {One concrete, plausible failure scenario based on the plan's approach}

**Pros/Cons symmetry:** Pros listed: {N} | Cons listed: {N} | Bias: {balanced / leans toward pros / leans toward cons}

### Trade-Off Assessment (MANDATORY — one row per reviewed decision AND per recommendation you make)

| #   | Decision / recommendation       | Trade-off — what it sacrifices                       | Gain (metric)   | Who pays, when     | Worth it?                         | Material?                          | Confirmed with user?       |
| --- | ------------------------------- | ---------------------------------------------------- | --------------- | ------------------ | --------------------------------- | ---------------------------------- | -------------------------- |
| 1   | {decision or my recommendation} | {sacrifice — or dimensions checked + why unaffected} | {gain + metric} | {payer / when due} | WORTH IT / NOT WORTH IT / UNCLEAR | YES / NO ({which materiality row}) | asked / N/A (not material) |

> Material trade-off with `Confirmed with user? = no` → verdict CANNOT be PASS. Escalate by asking the user directly first.

**Cross-Boundary Impact:** (code-change targets) {per client↔server seam AND per service/event/external touchpoint: NONE / ADDITIVE / BREAKING with routed fix; or `Single-tier / monolith — N/A`}

### Missing Items (if any)

- {specific item to add before implementation}

### Recommendation

{Proceed to $feature-implement | Add missing sections first | Add adversarial analysis to plan/PBI | Fix code findings | Update docs/specs | Continue manually}
```

## Round 2: Adversarial Re-Review (MANDATORY)

> **Protocol:** Deep Multi-Round Review (inlined via SYNC:double-round-trip-review above)

After Round 1, execute **second full adversarial round**:

1. **Assume Round 1 was wrong** — start with: "Round 1 missed something. Find it."
2. **Challenge every PASS item** from Round 1 — generate at least 2 sentences arguing the opposite for each
3. **Complete the Anti-Bias Gate** (all 7 boxes from Adversarial Review Mindset section, including the Trade-Off Interrogation Gate)
4. **Populate Adversarial Analysis** — MANDATORY:
    - At least 2 arguments against the chosen approach
    - At least 1 unexamined alternative
    - At least 2 hidden assumptions with failure consequences
    - Pre-mortem scenario
    - Pros/Cons symmetry count
    - Trade-Off Assessment table — every decision AND every recommendation of yours: trade-off named, worth-it verdict, materiality decided; re-ask the 3 questions on any trade-off Round 1 called "none" — why: Round 1's most common miss is an unpriced benefit.
5. **Focus on Round-1 misses:**
    - Alternatives that are strawmen (too easy to dismiss)
    - Risks stated vaguely without concrete mitigations
    - Assumptions embedded in the problem statement itself
    - Scope creep disguised as "related improvements"
6. **Update verdict** if Round 2 found new issues
7. **Final verdict** incorporates BOTH rounds + Adversarial Analysis

## Scope

- **Applies to:** Features, refactors, architectural changes, commits/diffs/code changes, docs/spec/report reviews
- **Exempt from plan-rationale advisory only:** trivial config changes, tiny single-file tweaks when active workflow permits documented skip
- **Enforcement:** Advisory (soft warning) — does not block implementation

## Important Notes

- Review only — do NOT modify target files or implement changes
- Keep output concise — actionable in <2 minutes
- Simple plans still require Anti-Bias Gate; findings may be brief, but gate cannot be skipped

---

## Findings Validation Gate (full mode — MANDATORY CLOSING TASK when findings exist)

> **Purpose:** Before handoff, re-validate THIS review's OWN findings: **correct, proof-backed, reasonable, best-practice**. Catch finding issues and missed enhancements.

**Trigger:** Full mode with ANY finding, weakness, missing item, or NEEDS WORK verdict — of ANY severity (Critical, High, Medium, OR Low). A Medium or Low severity NEVER exempts a finding from validation; even one low-severity nit triggers the gate. Skip ONLY unconditional PASS with a literally empty finding set (zero findings/missing items of any severity); record skip reason. **NEVER run in `validate-findings` mode**. — why: "it's only Low" is itself a severity claim the validation pass must confirm, not a reason to skip it.

**Caller-side re-do loop (bounded — owned HERE, not by validate mode):**

1. Ensure findings written to a report (`plans/reports/why-review-{date}.md`).
2. **Invoke `$why-review --validate-findings plans/reports/why-review-{date}.md`** in SAME main-agent session, NOT sub-agent. Returns CLEAN / HAS-ISSUES. Each call terminal.
3. **CLEAN** → append `## Findings Validation` line to report ("All N findings re-validated; correct, proof-backed, reasonable, best-practice; no changes."), gate PASSES, exit loop.
4. **HAS ISSUES** → reconcile: drop/demote unproven or inflated findings (including any finding below the **≥85% finding-survival bar** — see the Findings Validation Routine's Confidence bar), fix proof gaps, add surfaced findings/enhancements, re-derive verdict, record `## Findings Validation Notes` citing what changed and why.
5. **RE-DO holistically** — because the reconciled findings changed the picture, re-run the FULL review (Validation Checklist + both Adversarial Rounds) over the WHOLE target combined with the reconciled findings — NOT just re-validate the changed findings in isolation — then re-invoke `$why-review --validate-findings` on the UPDATED report. Repeat until CLEAN with no new findings surfaced, or **max 2 re-do rounds**. Still not CLEAN → record unresolved state, mark the goal-gate blocker, and escalate by asking the user directly in `## Next Steps`.

## Findings Validation Routine (validate-findings mode body — TERMINAL)

> Executed ONLY in `validate-findings` mode. **TERMINAL: do NOT call `$why-review`, do NOT run gate, do NOT spawn sub-agent, do NOT create closing task.** Validate, emit verdict, return.

Read supplied findings/report (path from `$ARGUMENTS`). For EACH finding, weakness, missing item, adversarial argument, assumption, verify ALL four:

- **Correct** — re-trace cited plan text / `file:line`; finding actually holds (not a misread or stale reference).
- **Proof-backed** — concrete `file:line` or quoted plan/report section present; reject "probably / should be / I think".
- **Reasonable** — severity/weight proportionate, not inflated; steel-man of opposing view does not dissolve it.
- **Best-practice** — recommendation reflects project conventions and Easy-to-Change metric (lowers future change cost), not preference or speculative generality.
- **Trade-off priced** — the finding's recommendation names what it SACRIFICES, carries a WORTH IT / NOT WORTH IT / UNCLEAR verdict, and has its materiality decided (per the Trade-Off Interrogation Gate). A recommendation presented as a pure win, or with `Trade-off: none` and no dimensions-checked justification, is a validation FAIL — flag HAS-ISSUES naming the unpriced recommendation. A **material** trade-off left unconfirmed with the user is HAS-ISSUES: name it so the CALLER escalates (terminal mode assesses, never asks). NOT WORTH IT → the finding is dropped or its recommendation replaced, never kept as-is. — why: a fix that costs more than the bug it removes is a finding the review should have withdrawn.
- **Dual-feedback (behavior-changing findings only)** — if ANY finding changes observable behavior, confirm that BOTH halves of the feedback are present for it: (1) a spec-drift verdict — CODE-WRONG / SPEC-STALE / AMBIGUOUS / SPEC-SILENT / in-sync (per `SYNC:spec-drift-adjudication`) — AND (2) a concrete test-feedback action (regression/preservation TC via `$spec [mode=tests]`, or covering test via `$integration-test`). A behavior-changing finding missing EITHER half is a validation FAIL — flag it as HAS-ISSUES and name the missing axis (`spec verdict absent` or `test feedback absent`). A **SPEC-SILENT** verdict (code correctly enforces an invariant no spec artifact states) REQUIRES a spec-enrichment action on the spec axis — add the §4 BR/§3 AC + a §8 TC via `$spec [update]` + `$spec [mode=tests]`; a SPEC-SILENT finding with no spec-enrichment action is HAS-ISSUES, same as a blank dual-feedback axis. A code-only fix with no spec verdict and no owed TC is an incomplete finding, not a clean one.
- **Confidence bar (distinct from the >80% act-gate)** — a finding survives ONLY if its own stated confidence that it is a real issue is **≥85%**. This is a HIGHER bar than the generic >80% act-gate, and a DIFFERENT question: the act-gate asks "may I act on this evidence?"; this bar asks "is this reported finding strong enough to KEEP?". A finding at 80-84% is demoted or dropped, not kept. The ≥85% must rest on the Proof-backed check above (a cited `file:line` + a traced failure path); confidence resting on inference alone caps below the bar.

Then **sweep for misses** — apply Adversarial Techniques once more: unexamined alternative, hidden assumption, enhancement opportunity?

**Emit a verdict** to `plans/reports/why-review-validate-{date}.md`:

- **CLEAN** — every finding passes all four checks AND nothing new surfaced.
- **HAS ISSUES** — list each finding to drop/demote/fix (reason + `file:line`) and each newly surfaced finding/enhancement (`file:line`).

Return verdict path + status. **Caller owns reconciliation and bounded re-do; routine does NOT modify caller report and does NOT loop.**

---

## Next Steps

> **EXEMPT in `validate-findings` mode:** terminal mode returns verdict; skip `## Next Steps`, ask the user directly, council gate.

**MANDATORY — FULL MODE:** after review, use ask the user directly; user owns next step.

> **[BLOCKING] Material trade-off confirmation comes FIRST.** Any trade-off the Trade-Off Interrogation Gate marked MATERIAL (irreversible · shifts cost to someone else · trades one quality attribute for another · crosses a boundary · high-consequence path · worth-it verdict UNCLEAR) MUST be confirmed with the user via its OWN ask the user directly — stating the trade-off, both options, what each sacrifices, and your recommendation — BEFORE the next-step question and BEFORE any PASS verdict. Multiple material trade-offs → ask the highest-consequence ones first (cap 3 questions per call), never bundle them into one vague "proceed?". — why: a one-way door walked through silently cannot be un-walked, and the user is the only one who owns that call.

- **"$feature-implement (Recommended)"** — Begin implementation after design rationale is validated
- **"$plan-execute"** — If implementing a simpler change
- **"Skip, continue manually"** — user decides

### Additionally — conditional $llm-council escalation

After first next-step question, evaluate gate:

1. **Workflow suppression first:** read `plans/.workflow-state.json` or equivalent `workflowId`. Suppress council for `workflow-refactor`, `workflow-bugfix`, and `test-*`. Rationale: council costs 11 LLM calls; these workflows are routine/reversible/test-only enough for `$why-review`. Matches `.claude/skills/llm-council/SKILL.md` "Workflow Integration".
2. **Frontmatter gate:** read active `plan.md` or PBI frontmatter. Gate fires when ANY true: `cross_service_impact != NONE`; `breaking_changes`; `complexity in {high, critical}` or `story_points >= 13`; `new_framework`; `irreversible`; `security_critical`; `performance_critical`; `cost_high`.
3. **Override/defaults:** absent fields default no-fire; `council_suppress: true` skips prompt and logs reason.

If suppressed or no-fire, do NOT mention `$llm-council`. If gate fires, ask a **SECOND** separate follow-up question:

- **"Escalate to $llm-council (Recommended)"** — Gate fired (high-stakes signal detected). Run 11 sub-agent council (5 advisors + 5 reviewers + chairman). Use when `$why-review` alone is insufficient. Cheaper alternatives already exhausted at this point: `$plan-validate` is the prior rung.
- **"Skip — proceed without council"** — Acknowledge the gate; proceed with current decision anyway.

> **[BLOCKING — full mode only]** MUST ATTENTION ask at least one user question before completing. `validate-findings` asks nothing because it only returns verdict.
> **[IMPORTANT]** Use task tracking before work, including file-read tasks; simple tasks need documented skip decision.
> **Critical Purpose:** Ensure quality: no flaws, bugs, missing updates, or stale content. Verify code AND documentation.
> **External Memory:** Long reviews write intermediate + final results to `plans/reports/`.
> **Evidence Gate:** MANDATORY every claim/finding/recommendation requires `file:line` proof or trace with confidence (>80% act, <80% verify).
> **OOP & DRY Enforcement:** MANDATORY flag 3+ duplicated patterns for extraction; same-group/suffix classes (`*Entity`, `*Dto`, `*Service`) should share a base when it lowers future change cost.

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

<!-- SYNC:behavioral-delta-matrix -->

> **Behavioral Delta Matrix** — MANDATORY for bugfix reviews. Produce this table BEFORE PASS/FAIL verdict. Narrative descriptions don't substitute.
>
> | Input state | Pre-fix behavior   | Post-fix behavior | Delta                                |
> | ----------- | ------------------ | ----------------- | ------------------------------------ |
> | {condition} | {current behavior} | {fixed behavior}  | Preserved ✓ / Fixed ✓ / REGRESSION ✗ |
>
> **Rules:** ≥3 rows · ≥1 row the bug report did NOT mention · REGRESSION delta → FAIL until a preservation test covers it (`spec-tests-template.md#preservation-tests-mandatory-for-bugfix-specs`)
>
> **BLOCKED until:** ≥3 rows · ≥1 row outside bug report · no unmitigated REGRESSION

<!-- /SYNC:behavioral-delta-matrix -->

<!-- SYNC:nested-task-creation -->

> **Nested Task Expansion Contract** — For workflow-step invocation, the `[Workflow] ...` row is only a parent container; the child skill still creates visible phase tasks.
>
> 1. Call the current task list first. If a matching active parent workflow row exists, set `nested=true` and record `parentTaskId`; otherwise run standalone.
> 2. Create one task per declared phase before phase work. When nested, prefix subjects `[N.M] $skill-name — phase`.
> 3. When nested, link the parent with `TaskUpdate(parentTaskId, addBlockedBy: [childIds])`.
> 4. Orchestrators must pre-expand a child skill's phase list and link the workflow row before invoking that child skill or sub-agent.
> 5. Mark exactly one child `in_progress` before work and `completed` immediately after evidence is written.
> 6. Complete the parent only after all child tasks are completed or explicitly cancelled with reason.
>
> **Blocked until:** the current task list done, child phases created, parent linked when nested, first child marked `in_progress`.

<!-- /SYNC:nested-task-creation -->

<!-- SYNC:project-reference-docs-guide -->

> **Project Reference Docs Gate** — Run after task-tracking bootstrap and before target/source file reads, grep, edits, or analysis. Project docs override generic framework assumptions.
>
> 1. Identify scope: file types, domain area, and operation.
> 2. **Read `docs/project-config.json` first — the project's machine-readable map.** It is the single source of truth for THIS repo (modules/paths, framework + search keywords, test/E2E/integration run-commands, design system, architecture rules, workflow patterns); ground exact paths, run-commands, and conventions on it **before investigating, planning, or coding** — never assume framework defaults (`CLAUDE.md` + reference docs are derived from it). If it — or the docs index, `lessons.md`, `CLAUDE.md`, `AGENTS.md`, or any required reference doc — is missing or stale, auto-run `$project-init` or the narrow route (`$project-config`, `$docs-init`, `$scan-all`, `$scan --target=<key>`, `$claude-md-init`) first; if Codex mirrors or `AGENTS.md` are stale, ask the user to run `$sync-codex` (never auto-run it).
> 3. Required docs by trigger: always `docs/project-reference/lessons.md`; doc lookup `docs-index-reference.md`; review `code-review-rules.md`; backend/CQRS/API `backend-patterns-reference.md`; domain/entity `domain-entities-reference.md`; frontend/UI `frontend-patterns-reference.md`; styles/design `scss-styling-guide.md` + `design-system/design-system-canonical.md`; integration tests `integration-test-reference.md`; E2E `e2e-test-reference.md`; feature docs/specs `feature-spec-reference.md` + `spec-system-reference.md` + `spec-principles.md`; behavior/public-contract/spec-test-code sync `workflow-spec-test-code-cycle-reference.md`; derived spec index/ERD/reimplementation guides `spec-system-reference.md` + source Feature Specs under `docs/specs/`; architecture/new area `project-structure-reference.md`.
> 4. Read every required doc, then before target work state: `Reference docs read: ... | Not applicable: ...`.
>
> **Ready when:** scope evaluated, `docs/project-config.json` consulted, required docs checked/read or setup route completed, `lessons.md` confirmed, citation emitted.

<!-- /SYNC:project-reference-docs-guide -->

<!-- SYNC:cross-stack-impact-trace -->

> **Cross-Stack Impact Trace** — FIRST review action: comprehend change holistically, THEN judge files. Every reviewed diff: note change context, trace full pipeline of main affected area end-to-end across client↔server seam, so a change on one tier can never silently break the other. (Distinct from `SYNC:cross-service-check`, which owns service-to-service / event boundary — this owns client↔server tier seam inside one app; pair both for full-pipeline coverage.)
>
> 1. **Comprehend context FIRST** — before file-by-file review, write short **Change Context** note: what changed, intent (why), originating tier (frontend / backend / shared / infra), main affected feature/flow. Do before flagging anything.
> 2. **Identify cross-stack seam(s)** — for main affected area, locate contract seam(s) between client and server: API route/endpoint + verb, request/response DTO or payload shape, shared type/schema, event/message contract, query/route params. Infer tier layout from `docs/project-config.json` and project conventions.
> 3. **Trace full pipeline end-to-end, in change's direction:**
>     - **Backend change → trace FORWARD to every frontend consumer:** handler/controller → response DTO/serializer → API client/service → store/state → component/template rendering or submitting it.
>     - **Frontend change → trace BACKWARD to backend contract:** component/form → API client call → route/endpoint → request DTO/validation → handler/domain.
>     - When `.code-graph/graph.db` exists, use `$graph-connect-api` and `python .claude/scripts/code_graph trace <file> --direction both --json` to map connection; otherwise grep route path, DTO/type name, each field name across BOTH tiers.
> 4. **Verify BOTH sides still agree** — for every changed seam confirm other tier matches: route path & verb, field names & types, nullability/optionality, required vs optional params, enum values, auth/permission, error/status shape. Any mismatch = **BREAKING** finding (backend change breaks a frontend consumer, or frontend now sends what backend rejects).
> 5. **Classify each seam:** NONE (no contract change) / ADDITIVE (backward-compatible) / BREAKING (consumer on other tier must change too). BREAKING seam whose other-tier consumer NOT updated in same diff = HIGH severity minimum (CRITICAL for auth/money/data-integrity paths).
>
> **Skip ONLY** when change has no cross-tier seam — pure docs, pure styling with no data contract, or single-tier tooling. State explicitly: `Single-tier change — no cross-stack seam`. Backend-only or single-tier repo still traces internal consumers (`SYNC:cross-service-check` for service/event boundaries).
>
> **BLOCKED until:** Change Context noted · seam(s) identified or explicit N/A · full pipeline traced in change direction · every changed seam classified NONE / ADDITIVE / BREAKING.

<!-- /SYNC:cross-stack-impact-trace -->

<!-- SYNC:cross-service-check -->

> **Cross-Service Check** — Microservices/event-driven: MANDATORY before concluding investigation, plan, spec, or feature doc. Missing downstream consumer = silent regression.
>
> | Boundary            | Grep terms                                                                      |
> | ------------------- | ------------------------------------------------------------------------------- |
> | Event producers     | `Publish`, `Dispatch`, `Send`, `emit`, `EventBus`, `outbox`, `IntegrationEvent` |
> | Event consumers     | `Consumer`, `EventHandler`, `Subscribe`, `@EventListener`, `inbox`              |
> | Sagas/orchestration | `Saga`, `ProcessManager`, `Choreography`, `Workflow`, `Orchestrator`            |
> | Sync service calls  | HTTP/gRPC calls to/from other services                                          |
> | Shared contracts    | OpenAPI spec, proto, shared DTO — flag breaking changes                         |
> | Data ownership      | Other service reads/writes same table/collection → Shared-DB anti-pattern       |
>
> **Per touchpoint:** owner service · message name · consumers · risk (NONE / ADDITIVE / BREAKING).
>
> **BLOCKED until:** Producers scanned · Consumers scanned · Sagas checked · Contracts reviewed · Breaking-change risk flagged

<!-- /SYNC:cross-service-check -->

<!-- SYNC:task-tracking-external-report -->

> **Task Tracking & External Report Persistence** — Bootstrap this before execution; then run project-reference doc prefetch before target/source work.
>
> 1. Create a small task breakdown before target file reads, grep, edits, or analysis. On context loss, inspect the current task list first.
> 2. Mark one task `in_progress` before work and `completed` immediately after evidence; never batch transitions.
> 3. For plan/review work, create `plans/reports/{skill}-{YYMMDD}-{HHmm}-{slug}.md` before first finding.
> 4. Append findings after each file/section/decision and synthesize from the report file at the end.
> 5. Final output cites `Full report: plans/reports/{filename}`.
>
> **Blocked until:** task breakdown exists, report path declared for plan/review work, first finding persisted before the next finding.

<!-- /SYNC:task-tracking-external-report -->

<!-- SYNC:critical-thinking-mindset -->

> **Critical Thinking Mindset** — Apply critical thinking, sequential thinking. Every claim needs traced proof, confidence >80% to act.
> **Anti-hallucination:** Never present guess as fact — cite sources for every claim, admit uncertainty freely, self-check output for errors, cross-reference independently, stay skeptical of own confidence — certainty without evidence root of all hallucination.

<!-- /SYNC:critical-thinking-mindset -->

<!-- SYNC:sequential-thinking-protocol -->

> **Sequential Thinking Protocol** — Structured multi-step reasoning for complex/ambiguous work. Use when planning, reviewing, debugging, or refining ideas where one-shot reasoning is unsafe.
>
> **Trigger when:** complex problem decomposition · adaptive plans needing revision · analysis with course correction · unclear/emerging scope · multi-step solutions · hypothesis-driven debugging · cross-cutting trade-off evaluation.
>
> **Format (explicit mode — visible thought trail):**
>
> 1. `Thought N/M: [aspect]` — one aspect per thought, state assumptions/uncertainty
> 2. `Thought N/M [REVISION of Thought K]: ...` — when prior reasoning invalidated; state Original / Why revised / Impact
> 3. `Thought N/M [BRANCH A from Thought K]: ...` — explore alternative; converge with decision rationale
> 4. `Thought N/M [HYPOTHESIS]: ...` then `[VERIFICATION]: ...` — test before acting
> 5. `Thought N/N [FINAL]` — only when verified, all critical aspects addressed, confidence >80%
>
> **Mandatory closers:** Confidence % stated · Assumptions listed · Open questions surfaced · Next action concrete.
>
> **Stop conditions:** confidence <80% on any critical decision → escalate by asking the user directly · ≥3 revisions on same thought → re-frame the problem · branch count >3 → split into sub-task.
>
> **Implicit mode:** apply methodology internally without visible markers when adding markers would clutter the response (routine work where reasoning aids accuracy).
>
> **Deep-dive:** see `$sequential-thinking` skill (`.claude/skills/sequential-thinking/SKILL.md`) for worked examples (API design, debugging, architecture), advanced techniques (spiral refinement, hypothesis testing, convergence), and meta-strategies (uncertainty handling, revision cascades).

<!-- /SYNC:sequential-thinking-protocol -->

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

<!-- SYNC:evidence-based-reasoning -->

> **Evidence-Based Reasoning** — Speculation is FORBIDDEN. Every claim needs proof.
>
> 1. Cite `file:line`, grep results, or framework docs for EVERY claim
> 2. Declare confidence: >80% act freely, 60-80% verify first, <60% DO NOT recommend
> 3. Cross-service validation required for architectural changes
> 4. "I don't have enough evidence" is valid and expected output
>
> **BLOCKED until:** `- [ ]` Evidence file path (`file:line`) `- [ ]` Grep search performed `- [ ]` 3+ similar patterns found `- [ ]` Confidence level stated
>
> **Forbidden without proof:** "obviously", "I think", "should be", "probably", "this is because"
> **If incomplete →** output: `"Insufficient evidence. Verified: [...]. Not verified: [...]."`

<!-- /SYNC:evidence-based-reasoning -->

<!-- SYNC:double-round-trip-review -->

> **Validated-Finding Fix + Full Re-Review Loop** — Re-review is triggered by a validated finding fix cycle, not by a round number. Review purpose: `review → validate findings → fix validated findings → full re-review` until a complete review pass clears the round's exit bar (see **Severity floor** below). **A clean review ENDS the loop — no further rounds required.**
>
> _aka **Self-Review Convergence Loop**._ The name is historical — there is **NO 2-round cap**; "double-round-trip" only means a validated-finding fix cycle forces at least one fresh re-review. It runs until a clean pass, bounded by the **3-round ceiling** below.
>
> **Round cap — 3 rounds MAX (a ceiling, NEVER a target).** A clean pass ENDS the loop immediately at ANY round — round 1 included; the cap never obliges you to keep spinning. Hitting round 3 with blocking findings still open (severity floor applied) → **STOP and escalate by asking the user directly** with the still-open findings listed; NEVER emit a silent "good enough" PASS on cap exhaustion, and NEVER let the cap substitute for the clean-review requirement. The 2-repeated-no-progress blocker rule stays an EARLIER exit — escalate at whichever trips first.
>
> **Severity floor — from round 3, LOW stops blocking.** The exit bar tightens by round, so the loop converges on consequence instead of spinning on polish:

> Define one predicate everywhere: `blocking_findings(round, findings)` returns all validated findings in rounds 1–2 and only validated CRITICAL/HIGH/MEDIUM findings in round 3+. A binary gate (test-green, security must-fix, required artifact) is exempt only when its owning invariant explicitly says so.
>
> | Round | Exit bar — loop ENDS when the fresh full review has…                      | Must be fixed to continue      |
> | ----- | ------------------------------------------------------------------------- | ------------------------------ |
> | 1-2   | zero validated findings at ANY severity                                   | CRITICAL · HIGH · MEDIUM · LOW |
> | 3+    | zero validated CRITICAL / HIGH / MEDIUM findings — **LOW-only is a PASS** | CRITICAL · HIGH · MEDIUM only  |
>
> From round 3 onward LOW findings are **NOT required to be fixed**: a round whose validated findings are ALL LOW **ENDS the loop immediately** — do not open another round for them. Severity tiers are `SYNC:severity-rubric` (CRITICAL block-merge · HIGH must-fix · MEDIUM should-fix · LOW nice-to-fix); rounds 1-2 are unchanged, so an easy LOW still gets fixed early when it is cheap.
>
> **Severity-floor rules:**
>
> - **Never silently drop a deferred LOW.** Every unfixed LOW is listed in the final report under `## Deferred LOW Findings (severity floor, round ≥3)` with file, line, and description, so the owner can schedule it. Dropping it from the report is a protocol violation, not a clean pass.
> - **Never re-tier a finding to trigger the exit.** Downgrading a real CRITICAL/HIGH/MEDIUM to LOW so the loop can end is a FALSE PASS. Severity is set by consequence per `SYNC:severity-rubric` before the round bar is applied — never after, and never with the exit in view. — why: a floor that can be reached by relabeling is not a floor.
> - **The floor bounds the loop, not the standard.** It ends _iteration_; it never authorizes shipping a known CRITICAL/HIGH/MEDIUM, and it never lowers the finding-survival bar that admits a finding in the first place.
> - **The floor never applies to a hard gate.** Test-green gates (a suite must actually pass), security must-fix gates, and any gate whose criterion is binary rather than severity-rated are unaffected — a failing test is a failure, not a LOW finding.
>
> **Universal scope (any new output/judgment):** any newly produced output or judgment gets **≥1 self-review**; any **new judgment** gets **≥1 `$why-review --validate-findings` pass**; anything flagged to re-check is re-checked **≥1 time** — before that output is treated as final. This loop is the default convergence contract for ANY work-producing skill, not review skills only.
>
> **Routing invariant (author-facing):** a skill that validates findings MUST route them through `$why-review --validate-findings` (the terminal validator) — NEVER fork an inline finding-validation. Routing through why-review is what makes the finding-survival bar and this loop apply; the `verify-review-validate-coverage` sensor enforces this exact route mechanically.
>
> **Round 1:** Main-session review. Read target files, build understanding, note issues. Output findings + verdict (PASS / FAIL).
>
> **Decision after Round 1:**
>
> - **No issues found (PASS, zero findings)** → review ENDS. Do NOT spawn a fresh sub-agent for confirmation.
> - **`blocking_findings(round, findings)` is non-empty** → run the active review skill's findings-validation gate first; for review skills the default gate is `$why-review --validate-findings <report-path>`. Fix only validated findings, then restart the full review protocol from the beginning with a fresh task breakdown.
>
> **Fresh full re-review after every fix cycle:** Re-run the whole review protocol over the current full target. When sub-agents are part of that protocol, spawn NEW `spawn_agent` calls — never reuse prior agents. Reviewers re-read ALL files from scratch with ZERO memory of prior rounds. See `SYNC:fresh-context-review` for the spawn mechanism and `SYNC:review-protocol-injection` for the canonical Agent prompt template. Each fresh full review must catch:
>
> - Cross-cutting concerns missed in the prior round
> - Interaction bugs between changed files
> - Convention drift (new code vs existing patterns)
> - Missing pieces that should exist but don't
> - Subtle edge cases the prior round rationalized away
> - Regressions introduced by the fixes themselves
>
> **Loop termination:** After each full re-review, repeat the same decision against **that round's exit bar**: bar cleared → END; blocking findings remain → validate findings → fix → restart from the first review phase. Rounds 1-2 clear on zero findings at any severity; **from round 3 the bar is zero CRITICAL/HIGH/MEDIUM, so a LOW-only round ENDS the loop** (deferred LOWs go in the report). Capped at **3 rounds**. Escalate by asking the user directly at whichever comes first: the same validated finding repeats for 2 full invocations with no progress · a fix requires product/owner input · round 3 completes with CRITICAL/HIGH/MEDIUM still open. NEVER loop past 3 rounds, and NEVER convert cap exhaustion into a PASS.
>
> **Rules:**
>
> - A clean Round 1 ENDS the review — no mandatory Round 2
> - From round 3 on, a round whose validated findings are ALL LOW ENDS the loop — never open round N+1 to fix LOW alone; list those LOWs as deferred instead
> - NEVER re-tier a CRITICAL/HIGH/MEDIUM down to LOW to reach the round-3 exit — severity is assigned by consequence before the bar is applied
> - NEVER fix unvalidated findings; validate first using the caller's validation gate
> - Every surviving finding must additionally clear the **finding-survival bar** defined in why-review's Findings Validation Routine (a deliberately higher bar than the generic act-gate — "keep this finding?" is a stricter question than "act on this evidence?"); a finding below the bar is demoted or dropped, not kept
> - NEVER skip the full re-review after a fix cycle (every fix invalidates the prior verdict)
> - NEVER reuse a sub-agent across rounds — every iteration that uses sub-agents spawns NEW Agent calls
> - Main agent READS sub-agent reports but MUST NOT filter, reinterpret, or override findings
> - The 3-round cap NEVER replaces the clean-review requirement — it bounds runaway looping, it does not authorize shipping an un-clean review; a clean pass ends the loop early at any round, and cap exhaustion escalates rather than passes
> - Enforce the round cap of 3 alongside the 2 repeated-no-progress blocker rule; both are escalation triggers, neither is a completion criterion
> - Track recursive invocation count and repeated blockers in conversation context (session-scoped)
> - Final verdict must incorporate ALL rounds executed
>
> **Report must include `## Round N Findings (Fresh Sub-Agent)` for every round N≥2 that was executed, plus `## Deferred LOW Findings (severity floor, round ≥3)` whenever the loop ended on the round-3+ bar with LOWs still open.**

<!-- /SYNC:double-round-trip-review -->

<!-- SYNC:fresh-context-review -->

> **Fresh Context Re-Review** — Eliminate orchestrator confirmation bias after fixes by restarting the full review with isolated sub-agents where applicable.
>
> **Why:** The main agent knows what it (or `$feature-implement`) just fixed and rationalizes findings accordingly. A fresh sub-agent has ZERO memory, re-reads from scratch, and catches what the main agent dismissed. Sub-agent bias is mitigated by (1) fresh context, (2) verbatim protocol injection, (3) main agent not filtering the report.
>
> **When:** ONLY after a validated-finding fix cycle. A review round that finds zero issues ENDS the loop — do NOT spawn a confirmation sub-agent. A review round that finds issues triggers: validate findings → fix → full review restart from the first phase.
>
> **How:**
>
> 1. Start a NEW full review invocation/task breakdown; when that protocol calls for agents, spawn NEW `spawn_agent` tool calls — use `code-reviewer` agent_type for code reviews, `general-purpose` for plan/doc/artifact reviews
> 2. Inject ALL required review protocols VERBATIM into the prompt — see `SYNC:review-protocol-injection` for the full list and template. Never reference protocols by file path; AI compliance drops behind file-read indirection (see `SYNC:shared-protocol-duplication-policy`)
> 3. Sub-agent re-reads ALL target files from scratch via its own tool calls — never pass file contents inline in the prompt
> 4. Sub-agent writes structured report to `plans/reports/{review-type}-round{N}-{date}.md`
> 5. Main agent reads the report, integrates findings into its own report, DOES NOT override or filter
>
> **Rules:**
>
> - SKIP fresh sub-agent when the prior full review found zero issues (no fixes = nothing new to verify)
> - NEVER skip the full review restart after a fix cycle — every fix invalidates the prior verdict
> - NEVER reuse a sub-agent across rounds — every fresh round spawns a NEW `spawn_agent` call
> - Continue until a complete full review pass clears that round's exit bar per `SYNC:double-round-trip-review`: **rounds 1-2** → zero findings at any severity; **round 3+** → zero CRITICAL/HIGH/MEDIUM, so a round whose validated findings are ALL LOW ENDS the loop (list those LOWs as deferred instead of spawning another round). If the same blocker repeats 3 times with no progress, escalate by asking the user directly
> - Track iteration count and repeated blockers in conversation context (session-scoped, no persistent files)

<!-- /SYNC:fresh-context-review -->

<!-- SYNC:review-protocol-injection -->

> **Review Protocol Injection** — Every fresh sub-agent review prompt MUST embed 11 protocol blocks VERBATIM. The template below has ALL 11 bodies already expanded inline. Copy the template wholesale into the Agent call's `prompt` field at runtime, replacing only the `{placeholders}` in Task / Round / Reference Docs / Target Files / Output sections with context-specific values. Do NOT touch the embedded protocol sections.
>
> **Why inline expansion:** Placeholder markers would force file-read indirection at runtime. AI compliance drops significantly behind indirection (see `SYNC:shared-protocol-duplication-policy`). Therefore the template carries all 11 protocol bodies pre-embedded.

### Subagent Type Selection

- `code-reviewer` — for code reviews (reviewing source files, git diffs, implementation)
- `general-purpose` — for plan / doc / artifact reviews (reviewing markdown plans, docs, specs)

### Canonical Agent Call Template (Copy Verbatim)

```
spawn_agent({
  description: "Fresh Round {N} review",
  agent_type: "code-reviewer",
  prompt: `
## Task
{review-specific task — e.g., "Review all uncommitted changes for code quality" | "Review plan files under {plan-dir}" | "Review integration tests in {path}"}

## Round
Round {N}. You have ZERO memory of prior rounds. Re-read all target files from scratch via your own tool calls. Do NOT trust anything from the main agent beyond this prompt.

## Protocols (follow VERBATIM — these are non-negotiable)

### Spec ↔ Tests ↔ Code Triangulation
DO THIS FIRST — before any per-protocol check below. The review target is the WHOLE PACKAGE, not the diff alone: load the behavior's spec (§3 ACs / §4 BRs / §8 TCs), its tests, and the changed code TOGETHER, and reason about their mutual consistency BEFORE judging any one in isolation.
1. Locate all three faces: the Feature Spec section(s) governing the changed behavior, the tests that guard it, and the production code that implements it. A missing face is itself a finding (SPEC-GAP / TEST-GAP / DEAD-SPEC).
2. Triangulate pairwise — every disagreement is a finding; classify which face is wrong:
   - code vs spec: behavior the code does that no §3/§4/§8 rule describes → CODE-EXTRA or SPEC-STALE; a [HARD] §4 rule or §5 invariant with no enforcing code path → CODE-WRONG.
   - tests vs spec: a §8 TC with no test, or a test asserting behavior no TC/rule names → TEST-GAP or SPEC-SILENT.
   - tests vs code: a changed code path with no covering test → TEST-GAP; a test that still passes against a deliberately broken invariant → WEAK-TEST (apply the mutation thinking in Bug Detection).
3. Hidden-rule capture: any invariant the code enforces but the spec never states (SPEC-SILENT) MUST be surfaced as a finding to add into §3/§4/§8 AND guarded with a test — the enrichment loop, never a silent pass.
4. Only after the three faces agree — or every disagreement is logged as a finding — proceed to the per-protocol checks below; when enrichment adds spec/test content, re-review the package against the enriched spec.
NEVER mark review PASS while any spec/test/code face disagrees without a logged finding. The diff is the entry point; the package is the unit of judgment.

### Evidence-Based Reasoning
Speculation is FORBIDDEN. Every claim needs proof.
1. Cite file:line, grep results, or framework docs for EVERY claim
2. Declare confidence: >80% act freely, 60-80% verify first, <60% DO NOT recommend
3. Cross-service validation required for architectural changes
4. "I don't have enough evidence" is valid and expected output
BLOCKED until: Evidence file path (file:line) provided; Grep search performed; 3+ similar patterns found; Confidence level stated.
Forbidden without proof: "obviously", "I think", "should be", "probably", "this is because".
If incomplete → output: "Insufficient evidence. Verified: [...]. Not verified: [...]."

### Bug Detection
MUST check categories 1-4 for EVERY review. Never skip.
1. Null Safety: Can params/returns be null? Are they guarded? Optional chaining gaps? .find() returns checked?
2. Boundary Conditions: Off-by-one (< vs <=)? Empty collections handled? Zero/negative values? Max limits?
3. Error Handling: Try-catch scope correct? Silent swallowed exceptions? Error types specific? Cleanup in finally?
4. Resource Management: Connections/streams closed? Subscriptions unsubscribed on destroy? Timers cleared? Memory bounded?
5. Concurrency (if async): Missing await? Race conditions on shared state? Stale closures? Retry storms?
6. Stack-Specific: Check the configured language/runtime pitfalls and framework-specific failure modes discovered from local code.
Classify: CRITICAL (crash/corrupt) → FAIL | HIGH (incorrect behavior) → FAIL | MEDIUM (edge case) → WARN | LOW (defensive) → INFO.

### Design Patterns Quality
Priority checks for every code change:
1. DRY via OOP: Same-suffix classes (*Entity, *Dto, *Service) MUST share base class. 3+ similar patterns → extract to shared abstraction.
2. Right Responsibility: Logic in LOWEST layer (Entity > Domain Service > Application Service > Controller). Never business logic in controllers.
3. SOLID: Single responsibility (one reason to change). Open-closed (extend, don't modify). Liskov (subtypes substitutable). Interface segregation (small interfaces). Dependency inversion (depend on abstractions).
4. After extraction/move/rename: Grep ENTIRE scope for dangling references. Zero tolerance.
5. YAGNI gate: NEVER recommend patterns unless 3+ occurrences exist. Don't extract for hypothetical future use.
Anti-patterns to flag: God Object, Copy-Paste inheritance, Circular Dependency, Leaky Abstraction.

### Logic & Intention Review
Verify WHAT code does matches WHY it was changed.
1. Change Intention Check: Every changed file MUST serve the stated purpose. Flag unrelated changes as scope creep.
2. Happy Path Trace: Walk through one complete success scenario through changed code.
3. Error Path Trace: Walk through one failure/edge case scenario through changed code.
4. Acceptance Mapping: If plan context available, map every acceptance criterion to a code change.
5. Tests Verify Intent: For test/spec changes, verify tests name the protected business rule or invariant and would fail if that intent breaks.
6. Migration Test Exclusion: Do not write tests for migration code. Schema/data migrations are one-time execution paths, not core application logic.
NEVER mark review PASS without completing both traces (happy + error path).

### Test Spec Verification
Map changed code to test specifications.
1. Identify the project's test/spec format from existing docs, test-case files, BDD feature files, or spec folders.
2. Every changed code path MUST map to a corresponding test case/spec (or flag as "needs test case").
3. New functions/endpoints/handlers → flag for test spec creation.
4. Migration files are excluded from test/spec creation; schema/data migrations are one-time execution paths, not core application logic.
5. If spec evidence fields exist, verify they point to actual code (file:line, not stale references).
6. Verify each meaningful test case names the business intent/invariant; flag behavior-only cases that only mirror implementation details.
7. Auth/data changes → verify corresponding authorization and data-state test cases exist.
8. If no specs exist for a changed path → log the gap and recommend the project's test-spec workflow.
NEVER skip test mapping. Untested code paths are the #1 source of production bugs.

### Behavioral Delta Matrix
MANDATORY for any bugfix review. Produce input-state × pre-fix × post-fix × delta table BEFORE writing verdict.
- Minimum 3 rows; include at least one row OUTSIDE the original bug report.
- Any "REGRESSION" delta → review returns FAIL until a preservation test is added.
- Narrative descriptions do NOT substitute for the matrix.
Example rows (external-record sync fix):
| Input                 | Pre-fix | Post-fix                  | Delta      |
| --------------------- | ------- | ------------------------- | ---------- |
| Record exists (valid) | Reused  | Always recreated → orphan | REGRESSION |
| Record missing (404)  | Error   | Recreated                 | Fixed      |

### Fix-Layer Accountability
NEVER fix at the crash site. Trace the full flow, fix at the owning layer. The crash site is a SYMPTOM, not the cause.
MANDATORY before ANY fix:
1. Trace full data flow — Map the complete path from data origin to crash site across ALL layers (storage → backend → API → frontend → UI). Identify where bad state ENTERS, not where it CRASHES.
2. Identify the invariant owner — Which layer's contract guarantees this value is valid? Fix at the LOWEST layer that owns the invariant, not the highest layer that consumes it.
3. One fix, maximum protection — If fix requires touching 3+ files with defensive checks, you are at the wrong layer — go lower.
4. Verify no bypass paths — Confirm all data flows through the fix point. Check for direct construction skipping factories, clone/spread without re-validation, raw data not wrapped in domain models, mutations outside the model layer.
BLOCKED until: Full data flow traced (origin → crash); Invariant owner identified with file:line evidence; All access sites audited (grep count); Fix layer justified (lowest layer that protects most consumers).
Anti-patterns (REJECT): "Fix it where it crashes" (crash site ≠ cause site, trace upstream); "Add defensive checks at every consumer" (scattered defense = wrong layer); "Both fix is safer" (pick ONE authoritative layer).

### Rationalization Prevention
AI skips steps via these evasions. Recognize and reject:
- "Too simple for a plan" → Simple + wrong assumptions = wasted time. Plan anyway.
- "I'll test after" → RED before GREEN. Write/verify test first.
- "Already searched" → Show grep evidence with file:line. No proof = no search.
- "Just do it" → Still need task tracking. Skip depth, never skip tracking.
- "Just a small fix" → Small fix in wrong location cascades. Verify file:line first.
- "Code is self-explanatory" → Future readers need evidence trail. Document anyway.
- "Combine steps to save time" → Combined steps dilute focus. Each step has distinct purpose.

### Graph-Assisted Investigation
MANDATORY when .code-graph/graph.db exists.
HARD-GATE: MUST run at least ONE graph command on key files before concluding any investigation.
Pattern: Grep finds files → trace --direction both reveals full system flow → Grep verifies details.
- Investigation/Scout: trace --direction both on 2-3 entry files
- Fix/Debug: callers_of on buggy function + tests_for
- Feature/Enhancement: connections on files to be modified
- Code Review: tests_for on changed functions
- Blast Radius: trace --direction downstream
CLI: python .claude/scripts/code_graph {command} --json. Use --node-mode file first (10-30x less noise), then --node-mode function for detail.

### Understand Code First
HARD-GATE: Do NOT write, plan, or fix until you READ existing code.
1. Search 3+ similar patterns (grep/glob) — cite file:line evidence.
2. Read existing files in target area — understand structure, base classes, conventions.
3. Run python .claude/scripts/code_graph trace <file> --direction both --json when .code-graph/graph.db exists.
4. Map dependencies via connections or callers_of — know what depends on your target.
5. Write investigation to .ai/workspace/analysis/ for non-trivial tasks (3+ files).
6. Re-read analysis file before implementing — never work from memory alone.
7. NEVER invent new patterns when existing ones work — match exactly or document deviation.
BLOCKED until: Read target files; Grep 3+ patterns; Graph trace (if graph.db exists); Assumptions verified with evidence.

## Reference Docs (READ before reviewing)
- `.claude/docs/development-rules.md` — canonical development rules, code-quality guidelines, and pre-commit checklist
- docs/project-reference/code-review-rules.md
- {skill-specific reference docs — e.g., integration-test-reference.md for integration-test-review; backend-patterns-reference.md for backend reviews; frontend-patterns-reference.md for frontend reviews}

## Target Files
{explicit file list OR "run git diff to see uncommitted changes" OR "read all files under {plan-dir}"}

## Output
Write a structured report to plans/reports/{review-type}-round{N}-{date}.md with sections:
- Status: PASS | FAIL
- Issue Count: {number}
- Critical Issues (with file:line evidence)
- High Priority Issues (with file:line evidence)
- Medium / Low Issues
- Cross-cutting findings

Return the report path and status to the main agent.
Every finding MUST have file:line evidence. Speculation is forbidden.
`
})
```

### Rules

- DO copy the template wholesale — including all 11 embedded protocol sections
- DO replace only the `{placeholders}` in Task / Round / Reference Docs / Target Files / Output sections with context-specific content
- DO choose `code-reviewer` agent_type for code reviews and `general-purpose` for plan / doc / artifact reviews
- DO NOT paraphrase, summarize, or skip any protocol section
- DO NOT pass file contents inline — the sub-agent reads via its own tool calls so it has a fresh context
- DO NOT reference protocols by file path or tag name — the bodies are already embedded above
- DO NOT introduce placeholder markers for the protocols — they must stay literally expanded

<!-- /SYNC:review-protocol-injection -->

<!-- SYNC:graph-impact-analysis -->

> **Graph Impact Analysis** — When `.code-graph/graph.db` exists, run `blast-radius --json` to detect ALL files affected by changes (7 edge types: CALLS, MESSAGE_BUS, API_ENDPOINT, TRIGGERS_EVENT, PRODUCES_EVENT, TRIGGERS_COMMAND_EVENT, INHERITS). Compute gap: impacted_files - changed_files = potentially stale files. Risk: <5 Low, 5-20 Medium, >20 High. Use `trace --direction downstream` for deep chains on high-impact files.

<!-- /SYNC:graph-impact-analysis -->

<!-- SYNC:severity-rubric -->

> **Severity Rubric** — Classify every finding by consequence, not by how easy it is to fix. One scale across all reviews so a "High" means the same thing everywhere.
>
> | Severity | Action      | Definition                                                                |
> | -------- | ----------- | ------------------------------------------------------------------------- |
> | CRITICAL | Block merge | Silent runtime failure, data corruption, validation bypass, security hole |
> | HIGH     | Must fix    | Incorrect behavior, invariant gap, architectural violation                |
> | MEDIUM   | Should fix  | Design debt, maintainability, likely future bug                           |
> | LOW      | Nice to fix | Convention, documentation, minor clarity                                  |
>
> **Score-based skills** map their numeric scale onto these tiers — do not invent a parallel vocabulary:
>
> - **0-2 criterion scoring** (e.g. production-readiness-review): `0` = CRITICAL/HIGH (criterion unmet, blocks production readiness), `1` = MEDIUM (partial, should fix), `2` = pass (no finding).
> - **Two-axis scoring** (e.g. performance-review, impact × likelihood): map the resulting cell to the nearest tier — high-impact + high-likelihood → CRITICAL/HIGH; low-impact OR low-likelihood → MEDIUM/LOW.
>
> A finding's tier drives the gate: CRITICAL/HIGH must be resolved or explicitly accepted by the owner before PASS; MEDIUM/LOW may ship with a tracked follow-up.

<!-- /SYNC:severity-rubric -->

<!-- SYNC:goal-contract-satisfaction-loop -->

> **Goal Contract Satisfaction Loop** — Persist the user goal in an external file, execute against it, and loop review/fix until every saved required criterion passes or a blocker escalates. Bounded closed loop — NEVER open-ended autonomous exploration.
>
> 1. **Resolve the active goal** (in order): active plan `goal.md` → `plans/goals/{YYMMDD-HHmm}-{slug}/goal.md` → create a new Goal Contract from the current user request (template: `.claude/templates/goal-contract-template.md`).
> 2. **Required sections:** Original Request, Purpose, Success Criteria (checkboxes; mark required vs optional), Constraints, Evidence Required, Iteration Log, Goal Satisfaction matrix.
> 3. **Before work:** read the active goal and map planned work to saved success criteria — execution serves the saved criteria, never chat memory alone.
> 4. **After execution/verification:** append an Iteration Log entry — result, evidence references (`file:line`, command output, report path), remaining gaps.
> 5. **Review gate:** emit a Goal Satisfaction matrix — `| Success Criterion | Evidence | Status |` with PASS/FAIL/BLOCKED. Overall PASS requires every required criterion PASS.
> 6. **Loop rule (retry):** required criterion FAIL → validate the gap is real → fix → re-review only the affected criteria. Stop cleanly when all required criteria PASS.
> 7. **Escalation rule (stop):** two consecutive iterations with no criterion progressing, or a blocker needing user input → mark the criterion BLOCKED with a user-facing reason and escalate. NEVER loop indefinitely.
> 8. **Skip rule:** tiny conversational tasks may skip the goal file ONLY with a recorded one-line reason. User-accepted gate skips are recorded in the goal file with reason and scope.
> 9. **Security:** NEVER store secrets, tokens, credentials, or private customer data in goal files — store evidence references and redact sensitive values.
>
> **Blocked until:** active goal resolved (or skip reason recorded) · saved success criteria read before edits · iteration evidence appended after execution · Goal Satisfaction matrix emitted before any PASS verdict.

<!-- /SYNC:goal-contract-satisfaction-loop -->

<!-- SYNC:trade-off-interrogation-gate -->

> **Trade-Off Interrogation Gate** — ALWAYS ask these THREE questions before ANY verdict, score, finding, or recommendation — about the thing under review AND about every recommendation YOU make. — why: naming a benefit without its price is an endorsement, not a review; the costliest trade-offs are the ones nobody wrote down.
>
> 1. **Is there any trade-off?** Name what it SACRIFICES. "None" / "pure win" is an unfinished analysis, NOT an answer — to claim none, state which dimensions you checked and why each is unaffected: future change cost · complexity · performance/latency · memory/cost · coupling · reversibility · migration burden · operational load · blast radius · security posture · testability · team skill/ramp · delivery time · UX.
> 2. **Is it worth it?** Weigh gain against sacrifice EXPLICITLY — what is gained (with a metric) · what it costs · WHO pays · WHEN it comes due — then emit **WORTH IT / NOT WORTH IT / UNCLEAR**. "Better" with no metric and no cost FAILS this question. NOT WORTH IT → withdraw or replace the recommendation, never keep it as-is.
> 3. **Is the trade-off material enough to CONFIRM WITH THE USER?** A material trade-off is the user's call, never yours. **MATERIAL** when ANY holds: irreversible / one-way door (data migration, public contract, storage format, vendor lock-in) · cost shifted onto someone else (another team, ops/on-call, future maintainer, end user) · one quality attribute traded for another (correctness↔speed, security↔convenience, latency↔cost, simplicity↔flexibility) · a boundary crossed (client↔server tier, service contract, event contract, shared library) · a high-consequence path (auth, money, data integrity, breaking change, High/Medium residual risk) · the worth-it verdict is UNCLEAR.
>
> **MATERIAL → STOP and confirm by asking the user directly BEFORE the verdict stands** — state the trade-off, both options, what each sacrifices, and your recommendation. **NOT material →** record it inline with a one-line justification and proceed.
>
> **Non-asking execution contexts — ESCALATE BY HANDOFF, never by silence.** ask the user directly reaches only the main interactive agent: a sub-agent cannot ask the user, and a terminal/verdict-only mode asks nothing by design. When you are running in such a context, the obligation is **redirected, never waived** — do ALL of: (a) complete questions 1 and 2 normally; (b) decide materiality and record it in the Trade-Off Assessment row with `confirmed? = NO — cannot ask from this context`; (c) **name the unconfirmed MATERIAL trade-off explicitly in your returned summary/verdict so the CALLER (or parent orchestrator) escalates it by asking the user directly on your behalf** — a material trade-off mentioned only inside a report file on disk is NOT a handoff; (d) do not emit an unqualified PASS — mark the verdict as carrying an unconfirmed material trade-off, so the caller's gate stays closed until the user answers. The caller inherits the escalation duty the moment it reads your return.
>
> This carve-out is about **reachability, not convenience**: it applies ONLY where the tool genuinely cannot reach the user (spawned sub-agent, terminal validate/verdict-only mode, non-interactive/headless run). It is NEVER a licence to skip the question, to self-approve a one-way door, or to downgrade materiality because asking is inconvenient — if you CAN ask, you MUST ask.
>
> **Emit a Trade-Off Assessment row** per reviewed decision and per recommendation: `| decision | sacrifices | gain (metric) | who pays, when | WORTH IT/NOT/UNCLEAR | material? | confirmed? |`.
>
> **BLOCKED until:** trade-off named (or dimensions-checked justification given) · worth-it verdict emitted · materiality decided · every MATERIAL trade-off either confirmed with the user OR — in a non-asking context — handed off in the returned verdict for the caller to confirm. A MATERIAL trade-off that is neither confirmed nor handed off can NEVER be PASS, and NEVER gets buried as a Low-severity note.
>
> **NEVER** answer "no trade-off" without checking · decide a material trade-off silently on the user's behalf · let convergence/delivery pressure authorize walking through a one-way door · bundle several material trade-offs into one vague "proceed?".

<!-- /SYNC:trade-off-interrogation-gate -->

<!-- SYNC:task-tracking-external-report:reminder -->

- **MANDATORY** Bootstrap task tracking before target work; transition one task at a time.
- **MANDATORY** Persist plan/review findings to `plans/reports/` incrementally and synthesize from disk.

<!-- /SYNC:task-tracking-external-report:reminder -->

<!-- SYNC:project-reference-docs-guide:reminder -->

- **MANDATORY** Before investigating, planning, or coding, read `docs/project-config.json` (the project map: modules/paths, run-commands, conventions, architecture/workflow rules) + the required project-reference docs, and cite `Reference docs read: ...`.
- **MANDATORY** Always include `lessons.md`; project config + conventions override generic framework defaults.
- **MANDATORY** If project config, root instruction files, or any required reference doc is missing or stale, auto-run `$project-init` or the narrow lower-level route before ordinary project-specific work.

<!-- /SYNC:project-reference-docs-guide:reminder -->

<!-- SYNC:cross-stack-impact-trace:reminder -->

**MUST ATTENTION** FIRST review action — note change context + holistically trace full pipeline of main affected area across client↔server seam (BE→FE forward, FE→BE backward). Verify both tiers still agree on route/DTO/field/type/nullability/auth; any mismatch = BREAKING finding. Skip only for single-tier / docs-only changes (state so).

<!-- /SYNC:cross-stack-impact-trace:reminder -->

<!-- SYNC:cross-service-check:reminder -->

**IMPORTANT MUST ATTENTION** microservices/event-driven: scan producers, consumers, sagas, contracts in task scope. Per touchpoint: owner · message · consumers · risk (NONE/ADDITIVE/BREAKING). Missing consumer = silent regression.

<!-- /SYNC:cross-service-check:reminder -->

<!-- SYNC:end-to-start-debugger-trace:reminder -->

**IMPORTANT MUST ATTENTION** debugger trace gate: for non-trivial bug/fix/investigation/review work, start at the observed final output and trace backward through reader -> storage/projection -> writer -> consumer/job -> producer/trigger. Enumerate all feeder paths and hypotheses before fixing. **BLOCKED until** trace, hypothesis matrix, owning fix layer, and forward convergence proof exist.

<!-- /SYNC:end-to-start-debugger-trace:reminder -->

<!-- SYNC:nested-task-creation:reminder -->

- **MANDATORY** Parent workflow rows do not replace child phase tracking; expand phases and link the parent when nested.
- **MANDATORY** Orchestrators pre-expand child skill phases before invocation; use `[N.M] $skill-name — phase` prefixes and one-`in_progress` discipline.

<!-- /SYNC:nested-task-creation:reminder -->

<!-- SYNC:goal-contract-satisfaction-loop:reminder -->

- **MANDATORY** Resolve the active Goal Contract BEFORE work (active plan `goal.md` → `plans/goals/{YYMMDD-HHmm}-{slug}/goal.md` → create from current request) and read saved success criteria before editing.
- **MANDATORY** Append iteration evidence after execution; emit a Goal Satisfaction matrix (PASS/FAIL/BLOCKED) before reporting PASS; loop on validated FAIL; escalate repeated no-progress or blockers. NEVER store secrets in goal files.

<!-- /SYNC:goal-contract-satisfaction-loop:reminder -->

<!-- SYNC:severity-rubric:reminder -->

- **MANDATORY** Classify findings Critical/High/Medium/Low by consequence; Critical/High block PASS until fixed or owner-accepted.
- **MANDATORY** Score-based skills (sre 0-2, perf two-axis) map onto the same four tiers — no parallel severity vocabulary.

<!-- /SYNC:severity-rubric:reminder -->

<!-- PROMPT-ENHANCE:STEP-TASK-CLOSING:START -->

## Prompt-Enhance Closing Anchors

- **IMPORTANT MUST ATTENTION** follow declared step order for this skill; NEVER skip, reorder, or merge steps without explicit user approval
- **IMPORTANT MUST ATTENTION** for every step/sub-skill call: set `in_progress` before execution, set `completed` after execution
- **IMPORTANT MUST ATTENTION** every skipped step MUST include explicit reason; every completed step MUST include concise evidence
- **IMPORTANT MUST ATTENTION** if Task tools unavailable, maintain an equivalent step-by-step plan tracker with synchronized statuses

<!-- PROMPT-ENHANCE:STEP-TASK-CLOSING:END -->

<!-- SYNC:double-round-trip-review:reminder -->

- **MANDATORY IMPORTANT MUST ATTENTION** execute the review loop (aka **Self-Review Convergence Loop**): review → validate findings → fix validated findings → full re-review. A complete review pass with zero findings ENDS the review. Any newly produced output/judgment gets ≥1 self-review; any new judgment gets ≥1 `$why-review --validate-findings` pass before it is treated as final.
- **MANDATORY** apply the **severity floor**: rounds 1-2 exit on zero findings at any severity; **from round 3 the bar is zero CRITICAL/HIGH/MEDIUM — LOW findings are no longer required to be fixed, so a LOW-only round ENDS the loop.** List every deferred LOW in the report; NEVER re-tier a real CRITICAL/HIGH/MEDIUM down to LOW to reach the exit, and NEVER apply the floor to a binary gate (test-green, security must-fix).
- **MANDATORY** enforce the **round cap of 3 — a ceiling, NEVER a target**: a clean pass ends the loop immediately at any round (round 1 included), and round 3 completing with CRITICAL/HIGH/MEDIUM still open → **STOP & escalate by asking the user directly**, never a silent PASS. The 2-repeated-no-progress blocker rule is an earlier exit — escalate at whichever trips first. NEVER loop open-ended.

<!-- /SYNC:double-round-trip-review:reminder -->

<!-- SYNC:trade-off-interrogation-gate:reminder -->

- **MANDATORY MUST ATTENTION ALWAYS ASK THE 3 TRADE-OFF QUESTIONS** — on the thing under review AND on every recommendation you make: (1) **is there any trade-off?** name what it SACRIFICES (change cost · complexity · perf · coupling · reversibility · migration · ops load · blast radius · security · testability · delivery time · UX) — "none"/"pure win" is an unfinished analysis, so state the dimensions checked; (2) **is it worth it?** gain (with a metric) vs cost, WHO pays, WHEN → emit **WORTH IT / NOT WORTH IT / UNCLEAR**; NOT WORTH IT → withdraw or replace it; (3) **is it material enough to confirm with the user?** irreversible/one-way door · cost shifted onto another team/ops/maintainer/user · one quality attribute traded for another · a tier/service/event/library boundary crossed · auth/money/data-integrity/breaking-change/High-or-Medium-risk path · verdict UNCLEAR → **STOP and confirm by asking the user directly BEFORE the verdict**.
- **MANDATORY** A MATERIAL trade-off with no user confirmation can NEVER be PASS; NEVER bury one as a Low-severity note, NEVER decide it silently, and NEVER let delivery or convergence pressure authorize a one-way door. — why: an un-walked-back one-way door is the user's call to make, not the reviewer's.
- **MANDATORY — non-asking contexts escalate BY HANDOFF, never by silence.** ask the user directly reaches only the main interactive agent: a sub-agent cannot ask the user, and a terminal/verdict-only mode asks nothing by design. There the duty is REDIRECTED, not waived — still name the trade-off, still decide materiality, record `confirmed? = NO — cannot ask from this context`, **state the unconfirmed MATERIAL trade-off in your RETURNED verdict/summary so the CALLER escalates it** (a note only in an on-disk report is not a handoff), and never emit an unqualified PASS. Applies ONLY where the user is genuinely unreachable (spawned sub-agent, terminal validate mode, headless run) — if you CAN ask, you MUST ask.

<!-- /SYNC:trade-off-interrogation-gate:reminder -->

<!-- SYNC:parallel-subagent-dispatch -->

> **Parallel Sub-Agent Dispatch** — Plan parallelism the moment a task breakdown exists, BEFORE executing it — running provably independent tasks sequentially wastes wall-clock. Applies to every multi-step job: workflow steps, planning, batch updates, investigation, research, scans, reviews, doc sync. **Plan execution is metadata-gated, NEVER default-parallel** — fan-out follows ONLY what the plan declares (`PAR`/`SEQ` tags + per-phase write set); an untagged plan runs sequentially — why: a derived write set cannot see cascade or generated writes.
>
> 1. **Tag every task `PAR` or `SEQ`.** `PAR` = inputs exclude every pending task's output AND write set disjoint from every other `PAR`. Else `SEQ` — MUST ATTENTION name the dependency forcing it.
> 2. **Group `PAR` into waves.** No edge between members. Two writers of one file NEVER share a wave. Read-only work (search, investigation, review, research) parallelizes freely.
> 3. **Declare before dispatch:** `Parallel plan: wave 1 = [...] · wave 2 = [...] · SEQ = [...] (reason)`.
> 4. **Spawn each wave in ONE message** — every `spawn_agent` call in one response, NEVER dripped per turn. Route each task to its specialist (`.claude/skills/shared/sub-agent-selection-guide.md`); NEVER `code-reviewer` as catch-all.
> 5. **Brief each sub-agent self-contained:** goal · scope + owned files · reference docs · return contract (summary + `Full report:` path, per SYNC:subagent-return-contract) · incremental persistence to `plans/reports/` (per SYNC:incremental-persistence).
> 6. **Barrier per wave.** Advance ONLY after EVERY member returns (a skipped conditional counts as returned). Merge, mark each task completed/skipped, THEN dispatch the next wave. Mutating steps wait for the barrier.
> 7. **One level deep.** A dispatched sub-agent executes its own brief; further fan-out stays the orchestrator's job unless that agent's `.claude/agents/*.md` definition authorizes it.
>
> **NEVER parallelize:** tasks sharing a write target · a task consuming a pending task's output · trivial single-file work (dispatch overhead > gain) · an order a skill or workflow explicitly fixes · gates awaiting user approval.
>
> **Blocked until:** MUST ATTENTION every task tagged PAR/SEQ with a named reason per SEQ · waves declared + write-set disjointness checked · each wave spawned in ONE message · barrier honored before the next wave.

<!-- /SYNC:parallel-subagent-dispatch -->

<!-- SYNC:parallel-subagent-dispatch:reminder -->

- **MANDATORY** After planning tasks, tag each PAR/SEQ and spawn every PAR wave as parallel sub-agents in ONE message — default parallel for workflows, batch updates, investigation, research, reviews; plan execution fans out ONLY on what the plan declares.
- **MANDATORY** Disjoint write sets per wave · all-return barrier before the next wave · specialist routing · sub-agents NEVER fan out further unless their own agent definition authorizes it.

<!-- /SYNC:parallel-subagent-dispatch:reminder -->

<!-- SYNC:project-protocol-overlay -->

> **Project Protocol Overlay** — Before executing this skill, resolve any PROJECT overlay rules layered onto it: match this skill's name against the `Target` column of the project's skill-protocol index (`docs/project-reference/skill-protocols-reference.md` by default; a `referenceDocs` entry in `docs/project-config.json` overrides the path), taking the most specific matching tier ONLY — exact name > glob > `*`. **That precedence orders overlays against EACH OTHER, never against this skill.** Read ONLY the matched bodies, resolved as `<protocols-dir>/<Name>.md`; a row's Body link is display text, never a read path. A matched body that is missing or malformed is REPORTED and skipped — never reconstructed from the index Description. No index, or no match -> proceed with no overlay, silently. Full contract: `.claude/skills/project-skill-protocol/references/registry.md`.
>
> Overlays are **ADDITIVE ONLY**: they ADD rules on top of this skill's own protocol and NEVER replace, override, disable, or reinterpret a rule it already states — removing every overlay must return this skill to exactly its documented behavior. An overlay is a BRIEF, not an authority escalation: it can NEVER waive a workflow gate, git discipline, a review gate, or a user-confirmation gate. A genuine overlay-vs-skill conflict, or two equally-specific overlays that directly contradict -> surface both to the user; NEVER resolve silently.

<!-- /SYNC:project-protocol-overlay -->

<!-- SYNC:project-protocol-overlay:reminder -->

**MUST ATTENTION** resolve project protocol overlays for this skill BEFORE executing — most specific matching tier only (exact > glob > `*`, which ranks overlays against each other, NEVER against this skill), read only matched bodies at `<protocols-dir>/<Name>.md`; a missing or malformed body is reported, never reconstructed. Overlays are ADDITIVE ONLY (they never replace this skill's own rules) and are a brief, NEVER an authority escalation; an equal-specificity contradiction goes to the user.

<!-- /SYNC:project-protocol-overlay:reminder -->

## Closing Reminders

**IMPORTANT MUST ATTENTION Goal:** Resolve the requested review target and apply the matching adversarial review path (plan/PBI rationale, code changes, docs/spec/report, findings, or explicit artifact) so decisions, findings, and plans survive adversarial rationale review before downstream work proceeds.

**IMPORTANT MUST ATTENTION Main steps (full mode) — execute in order, the skill AI keeps forgetting:** (1) DETECT MODE — `--validate-findings` is TERMINAL; (2) bind the self-recursive review loop — protocol loop primary (host-independent), optional `/goal` gate WHEN available — + Task Bootstrap (phase tasks + closing Findings Validation Gate task); (3) RESOLVE TARGET TYPE + read active Goal Contract + route by concern; (4) REVIEW as SKEPTIC — 7 Anti-Bias boxes (incl. the **Trade-Off Interrogation Gate**: trade-off? worth it? material → confirm with user) + Validation Checklist (presence AND quality depth) + Round 2 re-review + spec↔tests↔code triangulation; (5) FINDINGS VALIDATION GATE — re-invoke terminal `--validate-findings`, reconcile, RE-DO the full re-review until CLEAN (max 2), then ask next step by asking the user directly. NEVER skip, reorder, or merge a step without explicit user approval. — why: the steps ARE the review's integrity; dropping one ships an unproven verdict.

**Protocols in force (concise digest of the SYNC/shared blocks this skill carries):** these are signposts — the canonical bodies above are binding; MUST ATTENTION honor each, NEVER treat a digest line as the full rule.

- **End-To-Start Debugger Trace:** for non-trivial bugs, trace observed final state backward to trigger.
- **Behavioral Delta Matrix:** bugfix verdict needs ≥3-row pre/post delta table, one outside report.
- **Nested Task Creation:** workflow rows still expand child phase tasks; link parent when nested.
- **Project Reference Docs:** read scoped project docs (always `lessons.md`) before judging conventions.
- **Task Tracking & External Report:** bootstrap tasks; persist long-review findings to `plans/reports/` incrementally.
- **Critical Thinking:** every claim traced + proof-backed; confidence >80% to act, stay self-skeptical.
- **Sequential Thinking:** multi-step Thought N/M with REVISION/BRANCH/HYPOTHESIS markers and confidence closer.
- **AI Mistake Prevention:** verify generated content against evidence, trace downstream references, verify all affected outputs, re-read after context loss, surface ambiguity.
- **Evidence-Based Reasoning:** cite `file:line`/grep/docs for every claim; no proof, no recommendation.
- **Double Round-Trip Review:** review → validate → fix validated → full re-review until clean ends loop.
- **Fresh Context Review:** after a fix cycle restart full review with fresh zero-memory sub-agents.
- **Review Protocol Injection:** embed all 11 protocol bodies VERBATIM into each fresh sub-agent prompt.
- **Graph Impact Analysis:** run blast-radius when graph.db exists; impacted minus changed = stale files.
- **Severity Rubric:** classify findings Critical/High/Medium/Low by consequence; Critical/High block PASS.
- **Trade-Off Interrogation Gate:** always ask — trade-off? worth it? material → confirm with the user before any PASS.
- **Parallel Sub-Agent Dispatch:** Tag tasks PAR/SEQ, group PAR into disjoint-write-set waves, spawn each wave in ONE message, barrier before advancing.

**IMPORTANT MUST ATTENTION** default stance SKEPTIC, NOT validator — before ANY verdict complete all 7 Anti-Bias Gate boxes: steel-man ≥1 rejected alternative, name ≥1 unseen alternative, list 2-3 arguments AGAINST chosen approach, stress-test 2-3 hidden assumptions, run a pre-mortem, check pros/cons symmetry, run the Trade-Off Interrogation Gate. — why: section presence is never a pass, and a reviewer who already endorsed the reasoning needs a forced reset to find what's wrong.

**IMPORTANT MUST ATTENTION ALWAYS ASK THE 3 TRADE-OFF QUESTIONS** — on the decision under review AND on EVERY recommendation you yourself make: (1) **Is there any trade-off?** name what it SACRIFICES across future change cost · complexity · performance · coupling · reversibility · migration · ops load · blast radius · security · testability · team skill · delivery time · UX — "no trade-off" / "pure win" is an unfinished analysis, so state the dimensions checked and why each is unaffected; (2) **Is it worth it?** weigh gain vs sacrifice explicitly — what is gained (with a metric), what it costs, WHO pays, WHEN it comes due → emit **WORTH IT / NOT WORTH IT / UNCLEAR**; NOT WORTH IT → withdraw or replace the recommendation, never keep it; (3) **Is the trade-off material enough to confirm with the user?** MATERIAL when irreversible (one-way door) · cost shifted onto another team/ops/maintainer/user · one quality attribute traded for another · a tier/service/event/library boundary crossed · an auth/money/data-integrity/breaking-change/High-or-Medium-risk path · or the worth-it verdict is UNCLEAR → **STOP and confirm via its OWN ask the user directly BEFORE the next-step question and BEFORE any PASS verdict**, stating the trade-off, both options, what each sacrifices, and your recommendation. Emit the `Trade-Off Assessment` table every review; a MATERIAL trade-off with no user confirmation can NEVER be PASS, and NEVER bury one as a Low-severity note. In `validate-findings` terminal mode: assess and record, do NOT ask — flag it so the caller escalates. — why: a benefit named without its price is an endorsement rather than a review, unpriced fixes cost more than the bugs they remove, and a one-way door is the user's call to walk through, never the reviewer's.
**IMPORTANT MUST ATTENTION** resolve target type BEFORE reviewing: plan/PBI rationale, code changes, docs/spec/report, findings, or another artifact. Commit/PR/diff input defaults to code-change review; say "no active plan" ONLY for unresolved plan-rationale requests, NEVER silently convert target types. — why: wrong target type reviews the wrong artifact against the wrong checklist.
**IMPORTANT MUST ATTENTION** recursion guard is non-negotiable: full mode may call `$why-review --validate-findings` at most ONCE; validate-findings mode is TERMINAL — NEVER re-invokes why-review, NEVER runs the gate, NEVER spawns a sub-agent. — why: any of these from terminal mode causes infinite recursion.

**IMPORTANT MUST ATTENTION** cite `file:line` evidence + severity + confidence for EVERY finding (>80% act, <60% do NOT recommend); reject "probably / should be / I think" — why: an unproven finding is speculation, not a review result.
**IMPORTANT MUST ATTENTION** judge by Easy-to-Change — every finding, test, refactor, abstraction must lower future change cost; name the real enemies (coupling, hidden state, duplicated knowledge, unclear intent, premature irreversible decisions) or reject the recommendation. — why: this metric overrides any downstream "best practice" that raises change cost.
**IMPORTANT MUST ATTENTION** search 3+ existing patterns and read target files BEFORE judging conventions; evaluate fit before flagging a nearby pattern as "wrong" (closest example ≠ matching preconditions). — why: local conventions override generic framework defaults; pattern-matching without context manufactures false findings.
**IMPORTANT MUST ATTENTION** break work into small todo tasks via task tracking BEFORE starting; in full mode create the **Findings Validation Gate** closing task at skill START (Task Bootstrap) and run it whenever findings exist — re-invoke `$why-review --validate-findings` (TERMINAL, SAME session) to confirm every finding is correct, proof-backed, reasonable, best-practice; RE-DO ONLY on surfaced finding issues/enhancements (max 2 re-dos, then escalate by asking the user directly). — why: the gate catches inflated, misread, or unproven findings before handoff.
**IMPORTANT MUST ATTENTION** execute the review loop: review → validate findings → fix validated findings → full re-review; a complete review pass with zero findings ENDS the review. NEVER fix unvalidated findings; NEVER reuse a sub-agent across rounds (spawn NEW `spawn_agent` calls); main agent reads sub-agent reports but does NOT filter or override. — why: every fix invalidates the prior verdict, and orchestrator confirmation bias hides regressions a fresh zero-memory reviewer catches.
**IMPORTANT MUST ATTENTION** judge the WHOLE PACKAGE, not the diff alone — load the behavior's spec (§3 AC / §4 BR / §8 TC), its tests, and the changed code together and triangulate; a missing or disagreeing face is itself a finding (CODE-WRONG / SPEC-STALE / TEST-GAP / SPEC-SILENT). NEVER mark PASS while any face disagrees without a logged finding. — why: the diff is the entry point, the package is the unit of judgment.
**IMPORTANT MUST ATTENTION** when the target holds integration/E2E tests — or changes behavior that HAS covering integration tests — apply the **Integration-Test-Review Linkage**: `$integration-test-review` owns the 8 test-quality gates, so read its protocol (Mode A default) or delegate to it (Mode B, standalone full mode only) rather than judging assertion quality by eye. SKIP under any of the 4 guard rows (validate-findings mode · invoked by `$integration-test-review` Phase 9 · by `changes-review` in ANY phase — 0.8, 6, or 7.5 — or `$workflow-review-changes` · by `$debug-investigate`'s root-cause gate) and record the deferral line. — why: this skill's `Test/spec/doc sync` dimension claims to prove tests protect the invariant, but only those gates can answer it; and an unguarded call closes a `why-review → integration-test-review → why-review` cycle.
**IMPORTANT MUST ATTENTION** every behavior-changing finding carries BOTH a spec-drift verdict (CODE-WRONG / SPEC-STALE / AMBIGUOUS / SPEC-SILENT / in-sync) AND a concrete test-feedback action; a SPEC-SILENT verdict additionally REQUIRES a spec-enrichment action (§4 BR/§3 AC + §8 TC). A missing axis is HAS-ISSUES, never a clean finding. — why: code-only fixes silently drop the invariant from the spec and leave it unguarded.
**IMPORTANT MUST ATTENTION** for bugfix / regression / behavior-changing reviews, walk the End-to-Start debugger trace (observed final state → backward → feeder paths → hypothesis matrix → owning layer → forward convergence proof) and produce the Behavioral Delta Matrix (≥3 rows, ≥1 row outside the bug report) BEFORE the verdict; any REGRESSION delta → FAIL until a preservation test covers it. — why: narrative claims hide regressions and symptom-first fixes the matrix and trace force into view.
**IMPORTANT MUST ATTENTION** require fixes at the owning layer — the lowest layer that owns the invariant — NEVER at the symptom/crash site; a fix touching 3+ files with defensive checks signals the wrong layer, go lower. — why: symptom-site patches leave every other consumer exposed.
**IMPORTANT MUST ATTENTION** High/Medium residual risk must be fixed, reduced, or explicitly accepted by the user/owner before PASS; AI-extracted specs/TCs are not accepted evidence unless the canonical owner/review gate accepted them. — why: unowned residual risk is a deferred failure, not a pass.
**IMPORTANT MUST ATTENTION** flag 3+ duplicated patterns for extraction and same-suffix classes (`*Entity`/`*Dto`/`*Service`) for a shared base when it lowers future change cost; NEVER recommend a pattern with fewer than 3 occurrences (YAGNI). — why: both over- and under-abstraction raise future change cost.
**IMPORTANT MUST ATTENTION** read reference docs chosen by Project Reference Docs Gate (always include `docs/project-reference/lessons.md`); persist long-review findings to `plans/reports/` incrementally; validate the next step with the user by asking the user directly in full mode — NEVER auto-proceed. — why: project docs override generic assumptions, external memory survives compaction, and the review gate is user-owned.
**IMPORTANT MUST ATTENTION** add a final review todo task to verify work quality.

<!-- SYNC:critical-thinking-mindset:reminder -->

**MUST ATTENTION** apply critical + sequential thinking — every claim needs appropriate traced evidence (`file:line` for repo/code claims; source URL or artifact section for research, product, content, and docs claims); confidence >80% to act, <60% DO NOT recommend. Anti-hallucination: never present guess as fact, admit uncertainty freely, cross-reference independently, stay skeptical of own confidence.

<!-- /SYNC:critical-thinking-mindset:reminder -->

<!-- SYNC:sequential-thinking-protocol:reminder -->

**MUST ATTENTION** apply sequential-thinking — multi-step Thought N/M, REVISION/BRANCH/HYPOTHESIS markers, confidence % closer; see `$sequential-thinking` skill.

<!-- /SYNC:sequential-thinking-protocol:reminder -->

<!-- SYNC:ai-mistake-prevention:reminder -->

**MUST ATTENTION** apply AI mistake prevention — verify generated content against evidence, trace downstream references before deleting or renaming, verify all affected outputs, re-read files after context loss, and surface ambiguity before acting.

<!-- /SYNC:ai-mistake-prevention:reminder -->

> **[IMPORTANT]** Analyze how big the task is and break it into many small todo tasks systematically before starting — this is very important.

> **[GOAL REMINDER — MUST ATTENTION CRITICAL]**
>
> Ensure every review target is reasonable, correct, proof-backed, and best-practice aligned.
> **ALWAYS ASK THE 3 TRADE-OFF QUESTIONS (every decision AND every recommendation you make):** (1) **is there any trade-off?** — name what it sacrifices; "none" is an unfinished analysis, not an answer; (2) **is it worth it?** — gain vs cost, who pays, when → WORTH IT / NOT WORTH IT / UNCLEAR; (3) **is the trade-off material enough to confirm with the user?** — irreversible, cost shifted to someone else, one quality attribute traded for another, boundary crossed, high-consequence path, or UNCLEAR → STOP and confirm by asking the user directly BEFORE the verdict. NEVER resolve a material trade-off silently. — why: naming a benefit without its price is an endorsement, not a review, and a one-way door is the user's call to walk through, never yours.
> **MANDATORY SECOND PASS (full mode):** whenever Round 1 produces ANY finding, you MUST call `$why-review --validate-findings` a SECOND time on those findings to confirm each is correct and reasonable BEFORE handoff. NEVER skip it; NEVER suppress, demote, or under-report findings to dodge it. The self-recursive review loop — the **protocol loop primarily** (host-independent), plus a `/goal` Stop-hook gate WHEN available — BLOCKS stopping until findings are validated. — why: an unvalidated finding is an unproven claim, and a second self-review catches the misreads and inflation Round 1 rationalized.

**Anti-Rationalization:**

| Evasion                                                   | Rebuttal                                                                                                                                                                      |
| --------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| "No active plan"                                          | Valid only for unresolved plan-rationale requests; commits/diffs/PBIs/docs are targets.                                                                                       |
| "Just code review"                                        | Still resolve target, read docs, run graph, map tests/specs/docs.                                                                                                             |
| "Findings look obvious"                                   | Validate every finding via terminal `--validate-findings`.                                                                                                                    |
| "Round 1 is enough"                                       | Full mode with ANY finding MUST run the SECOND `--validate-findings` pass; the protocol review loop (and the `/goal` Stop hook when available) blocks stopping until it does. |
| "Report zero findings, skip the gate"                     | Suppressing/demoting findings to dodge validation is the exact bias the SKEPTIC stance forbids; surface them, THEN validate.                                                  |
| "Validate inline, don't re-invoke"                        | The second pass is a real terminal `$why-review --validate-findings` call on the written report — not a mental once-over.                                                     |
| "All dimensions at once"                                  | One focused pass per dimension; split attention catches misses.                                                                                                               |
| "Ask later"                                               | Full mode asks user next step before completion.                                                                                                                              |
| "Looks good / faces agree"                                | Default SKEPTIC; complete all 7 Anti-Bias boxes; triangulate spec↔tests↔code — any disagreeing face is a finding.                                                             |
| "No trade-off here / pure win"                            | Unexamined ≠ absent. Name the dimensions checked (change cost, complexity, perf, coupling, reversibility, ops, security, delivery) and why each is unaffected.                |
| "Trade-off is obvious, it's fine"                         | Emit the explicit WORTH IT / NOT WORTH IT / UNCLEAR verdict with gain, cost, who pays, when. "Obvious" is not a verdict.                                                      |
| "I'll note the trade-off in the report instead of asking" | A MATERIAL trade-off needs its OWN ask the user directly before any PASS — a buried note is not a confirmation.                                                               |
| "Just a review, not my decision to escalate"              | Surfacing a material trade-off for the user's call IS the review's job; silence hands the decision to no one.                                                                 |
| "Behavior change, no spec impact"                         | Emit spec-drift verdict + test-feedback action; SPEC-SILENT requires §4 BR/§3 AC + §8 TC enrichment.                                                                          |
| "Fix where it crashes"                                    | Fix at the owning layer (lowest invariant owner); the crash site is the symptom, not the cause.                                                                               |
| "High risk, but ship"                                     | High/Medium residual risk must be fixed, reduced, or owner-accepted before PASS.                                                                                              |

---

> **Closing reminder — Easy to Change is the success metric.** Every finding,
> test, refactor, and abstraction must answer one question: _does this make
> the next change cheaper or more expensive?_ If it doesn't reduce future
> change cost, reject it. Coupling, hidden state, duplicated knowledge, and
> unclear intent are the real enemies — call them out by name.

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
