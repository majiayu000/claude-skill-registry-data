---
name: why-review
version: 1.7.0
description: '[Code Quality] Use when a workflow step or the user asks for rationale review: why needed/chosen, trade-offs, good idea or best practice. Only explicit rationale asks; not generic reviews or how-it-works. --fix-loop fixes/re-reviews.'
---

> **[GOAL REMINDER — MUST ATTENTION CRITICAL]**
>
> Ensure every review target is reasonable, correct, proof-backed, and best-practice aligned.
> **ALWAYS ASK THE 3 TRADE-OFF QUESTIONS (every decision AND every recommendation you make):** (1) **is there any trade-off?** — name what it sacrifices; "none" is an unfinished analysis, not an answer; (2) **is it worth it?** — gain vs cost, who pays, when → WORTH IT / NOT WORTH IT / UNCLEAR; (3) **is the trade-off material enough to confirm with the user?** — irreversible, cost shifted to someone else, one quality attribute traded for another, boundary crossed, high-consequence path, or UNCLEAR → STOP and confirm via `AskUserQuestion` BEFORE the verdict. NEVER resolve a material trade-off silently. — why: naming a benefit without its price is an endorsement, not a review, and a one-way door is the user's call to walk through, never yours.
> **MANDATORY SECOND PASS (full mode):** whenever Round 1 produces ANY finding, you MUST call `/why-review --validate-findings` a SECOND time on those findings to confirm each is correct and reasonable BEFORE handoff. NEVER skip it; NEVER suppress, demote, or under-report findings to dodge it. The self-recursive review loop bound as the first full-mode action — the **protocol loop primarily** (host-independent), plus a `/goal` Stop-hook gate WHEN available — BLOCKS stopping until findings are validated. — why: an unvalidated finding is an unproven claim, and a second self-review catches the misreads and inflation Round 1 rationalized.

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
- **STEP 1 — DETECT MODE FIRST** (recursion control): `--validate-findings` is TERMINAL — NEVER re-invokes `/why-review`, NEVER runs the gate, NEVER spawns a sub-agent; full mode may call itself ONCE in validate-findings mode. Non-negotiable guard. — why: any of these from terminal mode loops infinitely.
- **STEP 2 — FULL-MODE FIRST ACTION** → read `references/full-mode.md` in full (BLOCKING; see **Mode References**), then bind the self-recursive review loop: the **protocol loop is the primary, host-independent binding** (you self-drive review → validate → reconcile → full re-review until the findings report validates CLEAN; retained target findings are returned by handoff to the fixing caller; at most 2 re-dos for report defects, for 3 full review cycles total, then escalate), and a `/goal` gate is an **optional accelerator invoked WHEN available** (its absence never weakens the loop) — NEVER bind it in terminal mode; "self-fix" = reconcile this review's OWN findings set, not code. THEN Task Bootstrap: create phase tasks + the MANDATORY Findings Validation Gate closing task.
- **STEP 3 — RESOLVE TARGET TYPE** before any review (commit/PR/diff → code-change; PBI/spec/doc → artifact; "no active plan" ONLY for an unresolved plan-rationale request — NEVER silently convert), read the active Goal Contract, then route by concern (code-reviewer / security-auditor / performance-optimizer / general-purpose). **Integration tests in the target → apply the Integration-Test-Review Linkage** (read `/integration-test --mode=review`'s 8 gates, or delegate in standalone full mode) — SKIPPED under its 4-row recursion guard.
- **STEP 4 — REVIEW as SKEPTIC** → complete ALL 7 Anti-Bias Gate boxes (steel-man rejected alt · unseen alternative · args against · stressed assumptions · pre-mortem · pros/cons symmetry · **Trade-Off Interrogation Gate**) + Validation Checklist (presence AND quality depth) + Round 2 re-review; triangulate spec↔tests↔code — any disagreeing face is a finding, presence is NEVER a pass.
- **TRADE-OFF GATE — ALWAYS ASK, on every decision AND every recommendation YOU make:** (1) **is there any trade-off?** name the sacrifice — "none" is an unfinished analysis, so state the dimensions checked; (2) **is it worth it?** gain vs cost, who pays, when → WORTH IT / NOT WORTH IT / UNCLEAR; (3) **is it material enough to confirm with the user?** irreversible · cost shifted elsewhere · quality attribute traded · boundary crossed · high-consequence path · UNCLEAR → **STOP and confirm via `AskUserQuestion` BEFORE the verdict**. Emit the `Trade-Off Assessment` table; a material trade-off unconfirmed = NEVER PASS.
- **STEP 5 — FINDINGS VALIDATION GATE** on your OWN findings (any severity): re-invoke terminal `--validate-findings`, reconcile, and RE-DO the full review only when validation finds report defects or missed findings (at most 2 re-dos; 3 full review cycles total); CLEAN validates the report, not the target, then ask next step via `AskUserQuestion` (+ conditional `/llm-council`). Dual-feedback: a behavior-changing finding needs BOTH a spec-drift verdict (CODE-WRONG / SPEC-STALE / AMBIGUOUS / SPEC-SILENT / in-sync) AND a test-feedback action; SPEC-SILENT requires enriching the configured canonical owner with its profile-declared requirement/invariant and scenario/case, plus a guarding test mapped to the actual executor and assertion. Only the strict default profile uses the §4 BR/§3 AC + §8 TC representation. A missing axis is HAS-ISSUES, never clean.
- **STEP 6 — CLOSE WITH USER OWNERSHIP:** **MUST ATTENTION** ask the required next-step question in full mode only after validation/re-review; apply the workflow-suppression and frontmatter gates before any optional `/llm-council` follow-up, and keep `validate-findings` terminal. **NEVER** auto-proceed past a material trade-off or unresolved blocking finding.
<!-- FIX-LOOP-MODE:START -->
- **OPTIONAL `--fix-loop` MODE (opt-in; absent flag = everything above unchanged)** — pairs this review with `/fix` in a bounded outer loop: resolve target + Goal Contract → bind the convergence loop (protocol-first, `/goal` optional) → per round { run the DEFAULT full-mode review pass INLINE (never with the flag, never as a sub-agent) → Trade-Off Gate on each validated blocking fix → `/fix` at the owning layer → log } → converge on a fresh full re-review of the changed target at the round bar (round 1: zero open findings; from round 2: LOW-only deferred) → recap. Round cap 3, hard maximum 3, failing tests uncapped, non-shrinking/increasing blockers escalate. Read-only callers (any sub-agent or nested report-only run) NEVER pass it. Full protocol: `references/fix-loop.md` — read it FIRST when the flag is present (BLOCKING).
<!-- FIX-LOOP-MODE:END -->

**Workflow:** Detect mode/target → (full mode only) read `references/full-mode.md`, then bind the self-recursive review loop (protocol-primary; optional `/goal` accelerator when available) → route path/docs/sub-agent focus (optional graph hint) → review dimensions/adversarial gates/Easy-to-Change → validate findings via terminal `--validate-findings` → reconcile + holistic full re-review when validation identifies report defects or missed findings (at most 2 re-dos; 3 full review cycles total); otherwise hand off retained target findings → ask next step in full mode.

**Key Rules:** MUST ATTENTION resolve target type BEFORE review. MUST ATTENTION every finding needs `file:line`, severity, confidence, best-practice rationale. MUST ATTENTION ask the 3 trade-off questions on every decision AND every recommendation (trade-off? worth it? material → confirm with user); NEVER accept "no trade-off" unexamined, NEVER decide a material trade-off silently. NEVER say "No active plan" except unresolved plan-rationale request. NEVER call `/why-review` from `validate-findings`. MUST ATTENTION judge by Easy-to-Change: lower future change cost or reject.

## Your Mission

<task>
$ARGUMENTS
</task>

## Review Mode (DETECT FIRST — recursion control)

Detect mode from `$ARGUMENTS` BEFORE any review work:

| Mode                   | Trigger in `$ARGUMENTS`                                                                          | What it runs                                                                                                                                                                                                              | Recursion                                                                                          |
| ---------------------- | ----------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------- |
| **full** (default)     | no `validate-findings` or `--fix-loop` token                                                     | Full design-rationale review (Validation Checklist + Adversarial Rounds in `references/full-mode.md`), THEN the **Findings Validation Gate** closing task — which re-invokes THIS skill in `validate-findings` mode on its own findings. | May call itself **ONCE** in `validate-findings` mode (same session).                               |
| **validate-findings**  | `$ARGUMENTS` contains `--validate-findings` / `mode=validate-findings` / `validate findings in` | ONLY the **Findings Validation Routine** against the supplied findings/report — verify each finding is correct, proof-backed, reasonable, best-practice; surface missed enhancements; emit a CLEAN / HAS-ISSUES verdict.   | **TERMINAL — NEVER calls `/why-review`, NEVER runs the gate, NEVER spawns a sub-agent.** Stops recursion. |
| **fix-loop** (opt-in)  | `$ARGUMENTS` contains `--fix-loop` AND no `validate-findings` token                              | The **Fix-Loop Mode** in `references/fix-loop.md`: an outer review → fix → fresh full re-review loop whose every review pass is THIS skill's **full** (default) mode, run inline without the flag. Main session only. | Round passes NEVER carry `--fix-loop` (no nested outer loop); each pass keeps its own single validate-findings call. |

> **Recursion guard (NON-NEGOTIABLE):** `validate-findings` terminates. MUST NOT invoke `/why-review` or validation gate — prevents infinite recursion. Re-do loop lives in CALLER, at most 2 re-dos for 3 full review cycles total, SAME main-agent session, NEVER spawned sub-agent. **Flag precedence:** `validate-findings` beats `--fix-loop` — terminal mode ignores the flag. `--fix-loop` never nests: its round passes run full mode WITHOUT the flag.

> **In `validate-findings` mode:** skip full Validation Checklist, Adversarial Rounds, Task Bootstrap, Next-Steps council gate, and never read `references/full-mode.md` or `references/fix-loop.md`. Jump straight to **Findings Validation Routine**, emit verdict, return to caller.

> **Full-mode sub-agent callers (parallel, report-only):** these rules bind ANY caller that runs this skill in full mode as a sub-agent or as a nested report-only step — you are in this context when you were spawned as a sub-agent, or your brief names you a parallel/barrier member or a report-only occurrence. Examples: a review skill's parallel rationale dimension beside its dimensional reviewers, or a workflow's whole-target review occurrence dispatched beside another reviewer. In these runs: never edit the target, never bind the `/goal` gate — record `/goal accelerator unavailable — sub-agent context`, return material Trade-Off / owner-judgment questions UNANSWERED for the caller to ask (never call `AskUserQuestion`), skip Next Steps and the `/llm-council` follow-up, and never invoke the caller. Findings validation of the caller's merged report is a separate, sequential `/why-review --validate-findings` invocation the caller owns. **These callers NEVER pass `--fix-loop`** — they are read-only and a sub-agent cannot own an outer fix loop. If `--fix-loop` ever reaches a sub-agent run, refuse it, record `--fix-loop refused — sub-agent context; ran report-only full mode`, and return retained findings for the caller to fix.

## Mode References (read at point of use — BLOCKING)

Mode-only text lives in this skill's `references/` folder and loads only when its mode runs. `validate-findings` mode reads neither file: its whole body is the **Findings Validation Routine** below. The protocol bodies both files cite (the `SYNC:*` blocks) stay in this file.

- **Full mode (default):** your FIRST action after mode detection is to read `references/full-mode.md` in full (BLOCKING) — before Task Bootstrap and before any review work. Its first section, **Bind the Self-Recursive Review Loop**, is the first action after that read. It also holds Task Bootstrap, the adversarial mindset and the Anti-Bias and Trade-Off gates, Target Resolution, the Validation Checklist, the Output Format, Round 2, the Report Closure Contract and the Findings Validation Gate. A full-mode run that skips the read has not run the review.
- **`--fix-loop` (opt-in):** read `references/fix-loop.md` first (BLOCKING); each round's full-mode pass then follows the full-mode rule above.

## First Principle — Easy to Change · Easy to Scale · Easy to Maintain

> The full gate is `SYNC:core-engineering-principles`, inlined with this skill's protocol blocks below; its closing digest ends this file.

---

## Findings Validation Routine (validate-findings mode body — TERMINAL)

> Executed ONLY in `validate-findings` mode. **TERMINAL: do NOT call `/why-review`, do NOT run gate, do NOT spawn sub-agent, do NOT create closing task.** Validate, emit verdict, return.

Read supplied findings/report (path from `$ARGUMENTS`). For EACH finding, weakness, missing item, adversarial argument, assumption, verify ALL of these checks:

- **Correct** — re-trace cited plan text / `file:line`; finding actually holds (not a misread or stale reference), and names a reachable trigger path — a caller, input or state that reaches the defect in a supported configuration. An unreachable concern is dropped as an observation; unsettled reachability becomes `NOT VERIFIABLE` when the concern would be MEDIUM or higher, an observation otherwise (`SYNC:severity-rubric`).
- **Proof-backed** — concrete `file:line` or quoted plan/report section present; reject "probably / should be / I think".
- **Reasonable** — severity/weight proportionate, not inflated; steel-man of opposing view does not dissolve it.
- **Best-practice** — recommendation reflects project conventions and Easy-to-Change metric (lowers future change cost), not preference or speculative generality.
- **Trade-off priced** — the finding's recommendation names what it SACRIFICES, carries a WORTH IT / NOT WORTH IT / UNCLEAR verdict, and has its materiality decided (per the `SYNC:trade-off-interrogation-gate` block in this file). A recommendation presented as a pure win, or with `Trade-off: none` and no dimensions-checked justification, is a validation FAIL — flag HAS-ISSUES naming the unpriced recommendation. A **material** trade-off left unconfirmed with the user is HAS-ISSUES: name it so the CALLER escalates (terminal mode assesses, never asks). NOT WORTH IT → the finding is dropped or its recommendation replaced, never kept as-is. — why: a fix that costs more than the bug it removes is a finding the review should have withdrawn.
- **Dual-feedback (behavior-changing findings only)** — if ANY finding changes observable behavior, confirm both axes: (1) a spec-drift verdict — CODE-WRONG / SPEC-STALE / AMBIGUOUS / SPEC-SILENT / in-sync (per `SYNC:spec-drift-adjudication`) — AND (2) a test-feedback action mapped through the project's configured profile to an executing assertion/result. For SPEC-SILENT, enrich the configured canonical owner with the missing requirement/invariant and canonical scenario/case, then ensure the actual guarding test is mapped at the declared cardinality. The strict default profile represents this as §4 BR/§3 AC plus a §8 TC via `/spec [update]` + `/spec [mode=tests]`; a configured native profile uses its declared owner, IDs, carrier and mapping. A missing axis is HAS-ISSUES, never clean.
- **Confidence bar (distinct from the >80% act-gate)** — a finding survives ONLY if its own stated confidence that it is a real issue is **≥85%**. This is a HIGHER bar than the generic >80% act-gate, and a DIFFERENT question: the act-gate asks "may I act on this evidence?"; this bar asks "is this reported finding strong enough to KEEP?". A finding at 80-84% is demoted or dropped, not kept. The ≥85% must rest on the Proof-backed check above (a cited `file:line` + a traced failure path); confidence resting on inference alone caps below the bar.
- **Premise-neutral (`SYNC:judgement-integrity`)** — when the reviewed report or drafted answer responds to a leading request (a gap/issue hunt, the user's own theory, "is this right?"), each finding or verdict must survive the reverse question: would it still be reported had the requester asked the opposite? A finding that exists only because the request presumed one is dropped; a verdict that simply echoes the requester's premise without the opposite having been tested is HAS-ISSUES, and so is a verdict on external facts (library/tool behavior, versions, standards, best practice) that cites no current source — it stays `Unverified` until web research confirms it. "No material issues found" with the checked scope named is a valid, CLEAN outcome — never pad the list to avoid it, and never invent disagreement to look independent.

Then **sweep for misses** — apply the adversarial techniques once more (steel-man the opposing view, why-NOT, assumption stress test, pre-mortem, pros/cons symmetry, contrarian pass): unexamined alternative, hidden assumption, enhancement opportunity?

**Emit a verdict** to `tmp/reports/why-review-validate-{date}.md`:

- **CLEAN** — every finding passes every check above AND nothing new surfaced.
- **HAS ISSUES** — list each finding to drop/demote/fix (reason + `file:line`) and each newly surfaced finding/enhancement (`file:line`).

Return verdict path + status. **Caller owns reconciliation and bounded re-do; routine does NOT modify caller report and does NOT loop.**


---

## Next Steps

> **EXEMPT in `validate-findings` mode:** terminal mode returns verdict; skip `## Next Steps`, `AskUserQuestion`, council gate.

**MANDATORY — FULL MODE:** after review, use `AskUserQuestion`; user owns next step.

> **[BLOCKING] Material trade-off confirmation comes FIRST.** Any trade-off the Trade-Off Interrogation Gate marked MATERIAL (irreversible · shifts cost to someone else · trades one quality attribute for another · crosses a boundary · high-consequence path · worth-it verdict UNCLEAR) MUST be confirmed with the user via its OWN `AskUserQuestion` — stating the trade-off, both options, what each sacrifices, and your recommendation — BEFORE the next-step question and BEFORE any PASS verdict. Multiple material trade-offs → ask the highest-consequence ones first (cap 3 questions per call), never bundle them into one vague "proceed?". — why: a one-way door walked through silently cannot be un-walked, and the user is the only one who owns that call.

- **"/feature-implement (Recommended)"** — Begin implementation after design rationale is validated
- **"/plan --mode=execute"** — If implementing a simpler change
- **"Skip, continue manually"** — user decides

### Additionally — conditional /llm-council escalation

After first next-step question, evaluate gate:

1. **Workflow suppression first:** resolve the current `workflowId` from host-injected workflow context; when it is not already present, read the host's documented state owner — `.claude/hooks/lib/workflow-state.cjs` owns `CK_TMP_DIR/workflow/{sessionId}.json` in this repository, while a host may use a legacy `.workflow-state.json` at the plans root (default `plans/`; relocated by `docsRoots.plans.path` in `docs/project-config.json`) only when that file is actually present. Never assume the legacy file exists. If no state is available, record `workflowId = unavailable` and continue to the frontmatter gate without fabricating a workflow. Suppress council for `workflow-refactor`, `workflow-bugfix`, and `test-*`. Rationale: council costs 11 LLM calls; these workflows are routine/reversible/test-only enough for `/why-review`. Matches `.claude/skills/llm-council/SKILL.md` "Workflow Integration".
2. **Frontmatter gate:** read active `plan.md` or PBI frontmatter. Gate fires when ANY true: `cross_service_impact != NONE`; `breaking_changes`; `complexity in {high, critical}` or `story_points >= 13`; `new_framework`; `irreversible`; `security_critical`; `performance_critical`; `cost_high`.
3. **Override/defaults:** absent fields default no-fire; `council_suppress: true` skips prompt and logs reason.

If suppressed or no-fire, do NOT mention `/llm-council`. If gate fires, ask a **SECOND** separate follow-up question:

- **"Escalate to /llm-council (Recommended)"** — Gate fired (high-stakes signal detected). Run 11 sub-agent council (5 advisors + 5 reviewers + chairman). Use when `/why-review` alone is insufficient. Cheaper alternatives already exhausted at this point: `/plan --mode=validate` is the prior rung.
- **"Skip — proceed without council"** — Acknowledge the gate; proceed with current decision anyway.

> **[BLOCKING — full mode only]** MUST ATTENTION ask at least one user question before completing. `validate-findings` asks nothing because it only returns verdict.
> **[IMPORTANT]** Use `TaskCreate` before work, including file-read tasks; simple tasks need documented skip decision.
> **Critical Purpose:** Ensure quality: no flaws, bugs, missing updates, or stale content. Verify code AND documentation.
> **External Memory:** Long reviews write intermediate + final results to `tmp/reports/`.
> **Evidence Gate:** MANDATORY every claim/finding/recommendation requires `file:line` proof or trace with confidence (>80% act, <80% verify).
> **OOP & DRY Enforcement:** MANDATORY flag 3+ duplicated patterns for extraction; same-group/suffix classes (`*Entity`, `*Dto`, `*Service`) should share a base when it lowers future change cost.

<!-- SYNC:core-engineering-principles -->

> **Core Engineering Principles — Easy to Change · Easy to Scale · Easy to Maintain** — The success metric of every plan, implementation and review is _future change cost_: the next change must be cheap, safe and provable. DRY, reuse, abstraction, interfaces, wrappers, patterns, layering, tests and the harness exist only to serve that goal. Apply this gate BEFORE any narrower design rule or checklist; when a narrower design rule would raise change cost, this principle wins — it never waives a required gate (tests, review, security, user confirmation). It is evidence-gated: judge fit against the project's config, accepted decisions and local patterns, and never impose a technique the project does not use.
>
> 1. **Easy to change.** Keep one owner per piece of knowledge — DRY the rule, not look-alike text. Reuse an existing helper, component or module before writing a new one (search 3+ siblings and cite them). Put purpose-named interfaces or ports at volatile boundaries: wrap a third-party SDK or infrastructure dependency in an adapter when it is volatile, likely to be swapped, or needs a test seam, so a swap touches one place — a stable dependency used directly is fine, and a pass-through wrapper that lowers no change cost is a defect. Keep units small and cohesive with explicit dependencies; no hidden state, boolean traps or leaked implementation detail. Extract an abstraction for a real second consumer or an evidenced change axis, never for speculation; prefer the reversible decision and defer an irreversible one until evidence forces it. Depth → `SYNC:design-patterns-quality`, `SYNC:complexity-prevention`.
> 2. **Easy to scale.** Growth in features, modules, team, data or load must not multiply edit sites or cost. Add a variant by extension (a new handler, registration or config entry), not by editing every switch over the same discriminator. Keep module boundaries and dependency direction explicit. Bound every loop, query, result set, queue and concurrency on the paths that matter, so work grows with the request, not with total data. Scale only what the project's profile warrants — no speculative distribution or infrastructure. Depth → `SYNC:scale-technique-gate`, `SYNC:engineering-foundation-gate` (F5, F6).
> 3. **Easy to maintain.** Protect every changed behavior with tests that name the business intent or invariant and FAIL when it breaks — happy, error, edge, boundary and regression paths, not only the changed line. Tests are repeatable and isolated. The mechanical harness (format, lint, types, build, test — the same command locally and in CI) runs and passes. Names and structure state intent, and docs or specs that embed the behavior stay in sync. Depth → `SYNC:engineering-foundation-gate` (F3, F4, F7), `SYNC:harness-setup`.
>
> **By phase:**
>
> - **Plan** — each phase names what it reuses (`file:line`), the seam or abstraction it adds or why none is needed, the next plausible change and its edit-site count, the growth bound, and the test that proves each invariant — or `N/A` with a reason where an item cannot apply (a docs-only phase has no growth bound).
> - **Implement** — search for reuse before writing; after writing, recount the edit sites of the next plausible change, confirm each new test fails when its intent breaks, and run the harness.
> - **Review** — judge each pillar `PASS` / `FAIL` / `N/A` with `file:line` evidence and name the real enemy: coupling, duplicated knowledge, hidden state, unbounded growth, untested intent, unclear intent or an irreversible decision exposed too early. A finding names its consequence for the next change; absence of a pattern is not a defect.
>
> **Self-check before claiming done:** (1) What is the next plausible change, and how many files would it touch? (2) What breaks at 10× features, data or load? (3) Which named test goes red if this behavior breaks, and does the harness run it?

<!-- /SYNC:core-engineering-principles -->

<!-- SYNC:end-to-start-debugger-trace -->

> **End-to-Start Debugger Trace** — For non-trivial bugs, failed verification, regression fixes, behavior-changing code, or unclear code flow, start from the observed final state and walk backward before proposing a fix.
>
> 1. **Frame 0: observed end state** — Name the exact user-visible output, failing assertion, log line, persisted value, API response, rendered UI, or aggregate bucket. Record the reader/query/renderer that produced it with `file:line` evidence.
> 2. **Walk backward one hop at a time** — Trace final reader -> projection/cache/storage -> writer -> consumer/handler/job -> producer/caller -> original trigger. At every hop record: input, transformation, output, owner, and evidence.
> 3. **Enumerate all feeder paths** — Find every upstream producer/caller/event/job that can write into the final path, including retry, async, cache, background, and alternate UI/API paths. Mark each path verified, ruled out, or still unknown.
> 4. **Build the hypothesis matrix** — For each plausible cause, list evidence for, evidence against, how to reproduce/verify, blast radius, and status (`primary`, `contributing`, `ruled out`, `latent`). Do not fix until competing causes are explicitly resolved or bounded.
> 5. **Choose the owning fix layer** — Identify the invariant owner and select the authoritative correction and enforcement points from traced contracts and the project's architecture. Keep validation at untrusted boundaries. Choose a shared point only when evidence shows it owns the invariant for those consumers. A fix at the symptom site is rejected unless the symptom site owns the invariant.
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


<!-- SYNC:cross-stack-impact-trace -->

> **Cross-Stack Impact Trace** — FIRST review action: comprehend change holistically, THEN judge files. Every reviewed diff: note change context, trace full pipeline of main affected area end-to-end across client↔server seam, so a change on one tier can never silently break the other. (Distinct from `SYNC:cross-service-check`, which owns service-to-service / event boundary — this owns client↔server tier seam inside one app; pair both for full-pipeline coverage.)
>
> 1. **Comprehend context FIRST** — before file-by-file review, write short **Change Context** note: what changed, intent (why), originating tier (frontend / backend / shared / infra), main affected feature/flow. Do before flagging anything.
> 2. **Identify cross-stack seam(s)** — for main affected area, locate contract seam(s) between client and server: API route/endpoint + verb, request/response DTO or payload shape, shared type/schema, event/message contract, query/route params. Infer tier layout from `docs/project-config.json` and project conventions.
> 3. **Trace full pipeline end-to-end, in change's direction:**
>     - **Backend change → trace FORWARD to every frontend consumer:** handler/controller → response DTO/serializer → API client/service → store/state → component/template rendering or submitting it.
>     - **Frontend change → trace BACKWARD to backend contract:** component/form → API client call → route/endpoint → request DTO/validation → handler/domain.
>     - Grep route path, DTO/type name, each field name across BOTH tiers. Optional: when `.code-graph/graph.db` exists, `/graph-code --mode=connect-api` or `python .claude/scripts/code_graph trace <file> --direction both --json` can add hints about the connection (may be stale — verify by reading).
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
> 3. For plan/review work, create `tmp/reports/{skill}-{YYMMDD}-{HHmm}-{slug}.md` before first finding.
> 4. Append findings after each file/section/decision and synthesize from the report file at the end.
> 5. Final output cites `Full report: tmp/reports/{filename}`.
>
> **Blocked until:** task breakdown exists, report path declared for plan/review work, first finding persisted before the next finding.

<!-- /SYNC:task-tracking-external-report -->

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
> **Stop conditions:** confidence <60% on any critical decision → stop and escalate via AskUserQuestion (60-80% → verify first) · ≥3 revisions on same thought → re-frame the problem · branch count >3 → split into sub-task.
>
> **Implicit mode:** apply methodology internally without visible markers when adding markers would clutter the response (routine work where reasoning aids accuracy).

<!-- /SYNC:sequential-thinking-protocol -->

<!-- SYNC:evidence-based-reasoning -->

> **Evidence-Based Reasoning** — Do not present inference as fact; ground material claims in evidence appropriate to the task.
>
> 1. Cite `file:line` for repository claims, configuration or reference paths for project rules, and URLs or artifact locations for external or observed claims.
> 2. State confidence when a conclusion is uncertain; verify material assumptions before acting and withhold recommendations when evidence is insufficient.
> 3. Trace the consumers, boundaries, or dependencies that exist in the affected path; do not assume services, modules, or architectural styles that the project does not use.
> 4. "I don't have enough evidence" is valid and expected output.
>
> **BLOCKED until:** material claims have traceable evidence, relevant searches are complete, and uncertainties are stated. Search comparable patterns when the task has existing implementations; record when none are available.
>
> **Forbidden without proof:** "obviously", "I think", "should be", "probably", "this is because"
> **If incomplete →** output: `"Insufficient evidence. Verified: [...]. Not verified: [...]."`

<!-- /SYNC:evidence-based-reasoning -->


<!-- SYNC:review-protocol-injection -->

> **Review Protocol Injection** — Fresh reviewer prompts MUST embed 11 protocol blocks VERBATIM, copied WHOLESALE; these are review-tier renderings. When canonical `SYNC:` protocols change, update their renderings here in the same edit. Copy this template into the Agent `prompt`; replace only `{placeholders}` in Task / Round / Reference Docs / Target Files / Output. Never alter embedded sections at dispatch.
>
> **Why inline expansion:** Fresh reviewers need every rule immediately; file pointers/placeholders depend on reads or hooks that may not fire. The hybrid policy (`SYNC:shared-protocol-duplication-policy`) therefore retains all 11 full bodies in this template, copied wholesale.

### Subagent Type Selection

- `code-reviewer` — for code reviews (reviewing source files, git diffs, implementation)
- `general-purpose` — for plan / doc / artifact reviews (reviewing markdown plans, docs, specs)

### Canonical Agent Call Template (Copy Verbatim)

```
Agent({
  description: "Fresh Round {N} review",
  subagent_type: "code-reviewer",
  prompt: `
## Task
{review-specific task — e.g., "Review all uncommitted changes for code quality" | "Review plan files under {plan-dir}" | "Review integration tests in {path}"}

## Round
Round {N}; ZERO prior-round memory. Re-read every target with your own tools. Trust no main-agent information beyond this prompt.

## Protocols (follow VERBATIM — these are non-negotiable)

### Spec ↔ Tests ↔ Code Triangulation
FIRST review the WHOLE PACKAGE. Read `docs/project-config.json`: valid `specArtifacts` profiles select configured `intent/contracts/evidence` roles, identifiers, ownership and test-carrier dialects; only absent profiles use strict-default §3 ACs / §4 BRs / §5 invariants / §8 TCs. Malformed/unsupported declarations are `BLOCKED`, never absent/fallback. Load governing artifact, tests, and changed code TOGETHER; judge mutual consistency before isolated checks.
1. Locate canonical owner sections, guarding tests, and implementing code. Native profiles: preserve owner path + case/scenario ID + optional variant; resolve configured carriers to actual tests. Missing faces are findings (SPEC-GAP / TEST-GAP / DEAD-SPEC).
2. Triangulate pairwise; log every disagreement and classify its wrong face:
   - code vs spec: behavior absent from configured `intent/contracts` (or strict-default §3/§4/§5/§8) → CODE-EXTRA or SPEC-STALE; a hard contract/invariant with no enforcing path → CODE-WRONG.
   - tests vs spec: native case without executing assertions, or assertions absent from native rules/cases → TEST-GAP or SPEC-SILENT. Without `specArtifacts`, check strict-default §8 TCs.
   - tests vs code: uncovered changed path → TEST-GAP; test passing a deliberately broken invariant → WEAK-TEST (apply the mutation thinking in Bug Detection).
3. Hidden-rule capture: enforced but unstated invariants (SPEC-SILENT) MUST become findings, additions to configured `intent`/`contracts`, and `evidence` links to native cases with inspected executing assertions. Without profiles, use strict-default §3/§4/§5/§8 and TC. Enrich; never silently pass.
4. Proceed only after agreement or all disagreements are logged; re-review enriched spec/test packages.
NEVER PASS unlogged spec/test/code disagreements. Diff = entry point; package = judgment unit.

### Evidence-Based Reasoning
Speculation FORBIDDEN; prove every claim.
1. Every claim: cite file:line, grep results, or framework docs
2. Confidence: >80% act freely; 60-80% verify first; <60% DO NOT recommend
3. Cross-service validation required for architectural changes
4. Insufficient evidence is valid/expected output
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
Admit a finding only with a reachable trigger path (the caller, input or state that reaches the defect) and a consequence; a concern no supported path reaches is an observation, and unsettled reachability is `NOT VERIFIABLE` only when the concern would be MEDIUM or higher.
Classify every finding by consequence (never by effort): CRITICAL = immediate material security/safety/data-loss risk or failed binary gate → block; HIGH = material correctness, contract, privacy, or authority risk → must fix; MEDIUM = bounded consequential edge/resilience/maintainability gap → must clear the current round, or escalate with an explicit residual-risk follow-up that does not create a clean pass; LOW = non-blocking polish with no credible present impact → record/defer from round 2; `NOT VERIFIABLE` is unresolved evidence, not LOW.

### Design Patterns Quality
Every code change:
1. Consistency/reuse: follow documented patterns; justify extraction cost by repetition or real consumer need. Similar names alone never require shared bases.
2. Responsibility: follow config/references/accepted decisions/code; place behavior with its owner. Assume no entity/service/controller hierarchy or forbidden layer without evidence.
3. Apply cohesion/coupling/dependency principles where paradigm assumptions fit; SOLID suits OO boundaries, not every language/codebase.
4. After extraction/move/rename: Grep ENTIRE scope for dangling references. Zero tolerance.
5. YAGNI: repetition prompts evaluation, never numeric extraction thresholds. Extract when shared change reasons, real consumers, or evidenced ownership/substitution lower total change cost; no hypothetical-use patterns.
6. Purpose naming: public/cross-layer abstractions name consumer capability/domain/contract, not provider/SDK/framework/database/transport. `IStorage`/`Storage` → `AzureBlobStorage`; use `IAzureStorage` only when Azure-specific semantics are intentionally part of the contract.
7. Contract-fit: read callers/all implementations; narrow over-broad abstractions (`IObjectStore`, `DocumentStore`), never reward misleading generic names.
8. Naming signals: `Manager`, `Helper`, `Utils`, `Data`, `Thing`, `Service`, `Interface`, type decorations/unexplained abbreviations are defects only when hiding purpose/scope/responsibility.
9. Concrete names: provider/strategy/transport/test-double names may distinguish real behavior (`AzureBlobStorage`, `InMemoryStorage`, `RetryingStorage`); exclude from caller contracts unless promised.
10. Preserve local interface syntax/naming: `.NET` `I` prefixes and Google TypeScript unmarked interfaces are both valid.
Anti-patterns to flag: God Object, Copy-Paste inheritance, Circular Dependency, Leaky Abstraction.

### Logic & Intention Review
Verify behavior matches change intent.
1. Every changed file MUST serve stated purpose; flag unrelated scope creep.
2. Trace one complete success scenario through changed code.
3. Trace one failure/edge scenario through changed code.
4. With plan context, map every acceptance criterion to code.
5. Test/spec changes: tests name protected business rule/invariant and fail when it breaks.
6. Migration exclusion: no migration-code tests; schema/data migrations are one-time paths, not core application logic.
NEVER PASS without both happy/error traces.

### Test Spec Verification
Map changed code to test specs.
1. Discover test/spec format in docs, test cases, BDD features, or spec folders.
2. Every changed path MUST map to a test case/spec or be flagged "needs test case".
3. New functions/endpoints/handlers → test-spec creation flag.
4. Exclude migrations from test/spec creation: one-time execution, not core application logic.
5. Verify existing spec evidence resolves actual code (file:line); flag stale references.
6. Meaningful cases name business intent/invariants; flag implementation-mirroring behavior-only cases.
7. Auth/data changes → verify corresponding authorization and data-state test cases exist.
8. Missing changed-path specs → log gap, recommend project test-spec workflow.
NEVER skip test mapping; uncovered paths risk production bugs.

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
Trace execution/data flow; fix the violated contract's owner, never assume the crash site.
MANDATORY before ANY fix:
1. Trace actual origin, transformations, boundaries, failure; invent no absent layers.
2. Identify invalid-state/behavior contract owner from architecture/code evidence.
3. Fix authoritative owner; retain untrusted-boundary validation. Justify multi-file fixes by owned contracts, not file-count thresholds.
4. Inspect relevant existing bypass entries: constructors/adapters/parsers/caches/persistence.
BLOCKED until: The affected path is traced; the owner is supported by file:line evidence; relevant consumers and bypass paths are checked; and the correction point fits the project's architecture.
Anti-patterns (REJECT): assuming the symptom site is the owner; scattering workarounds without tracing the contract; assuming the lowest technical layer is always authoritative; removing validation from a real trust boundary to force a single correction point.

### Rationalization Prevention
AI skips steps via these evasions. Recognize and reject:
- "Too simple for a plan" → Simple + wrong assumptions = wasted time. Plan anyway.
- "I'll test after" → RED before GREEN. Write/verify test first.
- "Already searched" → Show grep evidence with file:line. No proof = no search.
- "Just do it" → Still need TaskCreate. Skip depth, never skip tracking.
- "Just a small fix" → Small fix in wrong location cascades. Verify file:line first.
- "Code is self-explanatory" → Future readers need evidence trail. Document anyway.
- "Combine steps to save time" → Combined steps dilute focus. Each step has distinct purpose.

### Graph-Assisted Investigation (optional advice)
Optional: for high-risk blast radius (shared contract/many callers/cross-module/cross-service/public API), .code-graph/graph.db suggests callers/dependents/impacted tests. Treat it as a hint, NOT proof: stale/incomplete graphs lag uncommitted edits/unindexed paths. Verify important results by files/grep; skip low-risk/local changes. An absent or stale graph is never a finding.
Pattern: grep/read → optional graph suggestions → grep/read verification.
- High-risk investigation: trace --direction both on 2-3 entry files
- Fix/debug with wide reach: callers_of on buggy function + tests_for
- Feature touching a shared contract: connections on files to be modified
- Review of a high-risk change: tests_for on changed functions
- Blast radius: trace --direction downstream
CLI: python .claude/scripts/code_graph {command} --json. Use --node-mode file first (10-30x less noise), then --node-mode function for detail.

### Understand Code First
HARD-GATE: Do NOT write, plan, or fix until you READ existing code.
1. Search 3+ similar patterns (grep/glob) — cite file:line evidence.
2. Read existing files in target area — understand structure, base classes, conventions.
3. Optional high-risk hints: python .claude/scripts/code_graph trace <file> --direction both --json if .code-graph/graph.db exists; verify stale-capable caller/dependent hints by files.
4. Map dependents by grep/read callers; optional graph connections/callers_of adds hints.
5. Write investigation to tmp/analysis/ for non-trivial tasks (3+ files).
6. Re-read analysis file before implementing — never work from memory alone.
7. NEVER invent new patterns when existing ones work — match exactly or document deviation.
BLOCKED until: Read target files; Grep 3+ patterns; Assumptions verified with evidence. (The code graph is optional advice, never a gate.)

## Reference Docs (READ before reviewing)
Read only lane-resolved docs; do not re-resolve the whole set.
- `code-review-rules.md`, inside the reference-docs root (default `docs/project-reference`; a `docsRoots.projectReference.path` entry in `docs/project-config.json` overrides the path)
- {lane-specific docs the orchestrator resolved — e.g., the pattern doc for the files under review, integration-test-reference.md for a test lane, the governing spec for a spec-compliance lane}

## Target Files
{explicit file list OR "run git diff to see uncommitted changes" OR "read all files under {plan-dir}"}

## Output
Write a structured report to tmp/reports/{review-type}-round{N}-{date}.md with sections:
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
- DO choose `code-reviewer` subagent_type for code reviews and `general-purpose` for plan / doc / artifact reviews
- DO NOT paraphrase, summarize, or skip any protocol section
- DO NOT pass file contents inline — the sub-agent reads via its own tool calls so it has a fresh context
- DO NOT reference protocols by file path or tag name — the bodies are already embedded above
- DO NOT introduce placeholder markers for the protocols — they must stay literally expanded

<!-- /SYNC:review-protocol-injection -->

<!-- SYNC:graph-impact-analysis -->

> **Graph Impact Analysis (optional advice)** — Optional: for high-risk changes (shared contract, many callers, cross-module/cross-service flow, public API), an existing `.code-graph/graph.db` can suggest affected files via `blast-radius --json` (7 edge types: CALLS, MESSAGE_BUS, API_ENDPOINT, TRIGGERS_EVENT, PRODUCES_EVENT, TRIGGERS_COMMAND_EVENT, INHERITS). Outside-changeset files are read candidates, not proof of staleness; `<5` / `5-20` / `>20` files roughly hint low/medium/high impact. Use `trace --direction downstream` for deep chains. The graph can be stale or incomplete (uncommitted edits/unindexed paths); verify by reading files. An absent graph is never a finding; skip low-risk/local changes.

<!-- /SYNC:graph-impact-analysis -->

<!-- SYNC:severity-rubric -->

> **Severity Rubric** — Classify every finding by consequence, not by effort, reviewer preference, or how annoying the fix is. One scale applies to every review, skill, agent, workflow, and host so a tier means the same everywhere. Choose the highest credible consequence supported by evidence; do not lower a tier to make a round pass.
>
> **Finding vs observation (required):** An observation becomes a finding only when it names the affected user/system/data/contract, the shipped consequence, the evidence location, and the normalized tier. `INFO`, advice, preference, duplicate wording, or an unsubstantiated concern is not a finding and must not reopen a loop. If the concern might affect a required behavior or gate but evidence is incomplete, emit `NOT VERIFIABLE` with the missing evidence and keep it unresolved; never silently convert uncertainty into LOW.
>
> **Reachable trigger path (required):** a finding also names HOW a supported configuration reaches the defect — the caller, input, state or event sequence that drives execution or data there. A concern on a path nothing reaches (dead code, a branch its guard excludes, an impossible state) is an observation: record it as advice, never as a LOW to fix. Also never a finding: what a compiler, type checker, linter or test run for this change already reports in the review evidence; a behavior change the stated intent asks for; an issue silenced by a suppression that predates this change and states its reason (a suppression the change adds is itself reviewed); a pre-existing issue on a line the change neither touched nor made reachable. When reachability cannot be settled and the concern would be MEDIUM or higher, emit `NOT VERIFIABLE` naming what would settle it; a polish-level concern with unsettled reachability is an observation. — why: a speculative LOW admitted as a finding becomes build work in round 1.
>
> | Severity | Action | Definition and examples |
> | --- | --- | --- |
> | CRITICAL | Block immediately; escalate | Immediate material risk if shipped: authentication/authorization or safety bypass; secrets/PII exposure; irreversible destructive action; data loss/corruption; a silent failure on a critical path. A failed binary gate is carried by the executable policy as a separate synthetic blocker, not an ordinary severity judgment. |
> | HIGH | Must fix before PASS/merge | Material correctness or contract risk: wrong behavior on a supported path; violated business/data invariant; meaningful privacy or authority gap; breaking API/schema/compatibility change; likely harm to users/downstream systems; a missing proof for a behavior-changing fix. |
> | MEDIUM | Must clear the current round; escalate if the fix needs an owner decision | Bounded but consequential risk: an edge case, resilience/observability/testability/maintainability gap, credible future defect, or local architectural drift — real impact, not immediate material loss. A recorded follow-up does not make an open MEDIUM a clean pass. |
> | LOW | Record and defer; never opens another fix/re-review round from round 2 onward, never raises the round budget | Non-blocking polish with no credible present correctness, security, privacy, authority, availability, or data-integrity impact: wording/formatting, minor documentation or convention drift, optional defensive cleanup, cosmetic refinement. |
>
> **Consequence decision tree (apply in order):** (1) A failed binary gate stays a separate hard blocker (synthetic CRITICAL in the executable helper) — never hide it behind an ordinary label. Otherwise, would shipping permit immediate material security/safety/authority harm, irreversible destruction, data loss/corruption, or a critical-path silent failure? → **CRITICAL**. (2) Does a supported path, invariant, public contract, privacy/authority boundary, compatibility promise, or behavior-changing proof fail with material impact? → **HIGH**. (3) A bounded but consequential edge, resilience, observability, testability, maintainability, or architectural gap with credible impact? → **MEDIUM**. (4) Evidence shows only non-blocking polish? → **LOW**. (5) Evidence to choose among 1–4 missing → **NOT VERIFIABLE**, not LOW. When several tiers fit, select the highest credible consequence; effort, cost, reviewer discomfort, frequency alone, proximity to the round cap, and obtaining another round never decide the tier.
>
> **Boundary examples:** auth bypass, exposed secret/PII, destructive command without an authority gate, or failed required test/generation/parity gate → **CRITICAL**; wrong supported response, broken invariant/API/schema, meaningful privacy/authority defect, or unproven behavior-changing fix → **HIGH**; bounded retry/timeout/alert/testability gap or credible maintainability drift → **MEDIUM**; typo, formatting, optional cleanup, or cosmetic suggestion proven not to affect behavior → **LOW**. A missing fact about any boundary is **NOT VERIFIABLE** until evidence or a documented residual-risk decision exists.
>
> **Classification procedure (every finding):** (1) state the affected user, system, data, contract, or gate; (2) assess consequence if it ships; (3) assess exposure/likelihood and reversibility/detectability; (4) select the highest justified tier; (5) cite `file:line` or equivalent evidence and a confidence percentage. `NOT VERIFIABLE` is a pending evidence state, not a fifth tier and never a LOW escape hatch: if the claim could affect required behavior, security, privacy, authority, availability, data integrity, or a binary gate, it stays an open evidence blocker until resolved or explicitly owner-accepted with documented residual risk. Classify LOW only when evidence supports the absence of credible present material impact.
>
> **Hard-gate rule:** Binary gates (tests, required artifacts, security must-fix checks, generated parity, policy compliance) are not severity-rated findings. The executable helper records a failed gate as a synthetic CRITICAL blocker so one predicate can carry it; the report still names the gate and failure evidence. A failed gate blocks at every round, even when all ordinary findings are LOW. A failed non-test gate is bounded by the three-round review cap; a failing test gate is outside the round budget and loops until the tests pass.
>
> **Score-based skills** map their numeric scale onto these tiers — no parallel vocabulary:
>
> - **0-2 criterion scoring** (e.g. production-readiness-review): `0` = CRITICAL/HIGH (unmet, blocks readiness), `1` = MEDIUM (partial, consequential gap), `2` = pass. A polish-only criterion is LOW, not a forced `0`.
> - **Two-axis scoring** (e.g. performance-review, impact × likelihood): high impact + high exposure → CRITICAL/HIGH; material impact, bounded exposure → HIGH/MEDIUM; low impact and exposure → LOW. Record the axes and why the tier is the highest credible consequence.
> - **Scorecards / `/20` grades** (e.g. `architecture --mode=scalability`): the aggregate score and verdict band are separate from finding severity. A sub-80 area is evidence to investigate, not an automatic tier; classify each underlying gap by the decision tree and keep advisory score deductions apart from blocking findings.
>
> **Domain-vocabulary normalization (mandatory):** a skill may keep a local reporting vocabulary, but it MUST feed this same four-tier round predicate — never a second severity system:
>
> - `BLOCKED`, `HARD FAIL`, or `FAIL` is a blocking local verdict, not an automatic CRITICAL: CRITICAL for an immediate material risk or failed binary gate, otherwise HIGH or MEDIUM with evidence, while the local block holds until the owning gate is satisfied.
> - `WARN` is not permission to ignore: MEDIUM when consequential, LOW only when evidence shows no credible present material impact, HIGH/CRITICAL when the consequence warrants. `PASS`/compliant is not a finding.
> - UI `P0`/`P1`/`P2`/`P3`/`P4` start as CRITICAL/HIGH/MEDIUM/LOW/LOW; override upward only on evidence of a higher shipped consequence. A P0/P1 accessibility or task-completion floor stays a blocking gate even when called a priority.
> - Numeric SRE/readiness or impact/likelihood scores are evidence inputs, not tiers: emit the score, the consequence, and the normalized tier together. `INFO`/advisory observations are not findings unless evidence shows a material consequence.
>
> A tier drives the gate: CRITICAL/HIGH/MEDIUM stay actionable and blocking under the round policy; all review blockers may use up to three rounds, then escalate; LOW may be tracked as a follow-up and, from round 2, never justifies another fix/re-review by itself. An owner decision may explain or schedule an open MEDIUM but never makes it a clean pass; owner acceptance never makes a failed binary gate pass and must record scope, rationale, and residual risk.

<!-- /SYNC:severity-rubric -->


<!-- SYNC:goal-contract-satisfaction-loop -->

> **Goal Contract Satisfaction Loop** — Persist the user goal in an external file, execute against it, and loop review/fix until every saved required criterion passes or a blocker escalates. Bounded closed loop — NEVER open-ended autonomous exploration.
>
> 1. **Resolve the active goal** (in order): active plan `goal.md` → `<plans root>/goals/{YYMMDD-HHmm}-{slug}/goal.md` (plans root default `plans`; a `docsRoots.plans.path` entry in `docs/project-config.json` overrides the path) → create a new Goal Contract from the current user request (template: `.claude/templates/goal-contract-template.md`).
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
> **MATERIAL → STOP and confirm via `AskUserQuestion` BEFORE the verdict stands** — state the trade-off, both options, what each sacrifices, and your recommendation. **NOT material →** record it inline with a one-line justification and proceed.
>
> **Non-asking execution contexts — ESCALATE BY HANDOFF, never by silence.** `AskUserQuestion` reaches only the main interactive agent: a sub-agent cannot ask the user, and a terminal/verdict-only mode asks nothing by design. When you are running in such a context, the obligation is **redirected, never waived** — do ALL of: (a) complete questions 1 and 2 normally; (b) decide materiality and record it in the Trade-Off Assessment row with `confirmed? = NO — cannot ask from this context`; (c) **name the unconfirmed MATERIAL trade-off explicitly in your returned summary/verdict so the CALLER (or parent orchestrator) escalates it via `AskUserQuestion` on your behalf** — a material trade-off mentioned only inside a report file on disk is NOT a handoff; (d) do not emit an unqualified PASS — mark the verdict as carrying an unconfirmed material trade-off, so the caller's gate stays closed until the user answers. The caller inherits the escalation duty the moment it reads your return.
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
- **MANDATORY** Persist plan/review findings to `tmp/reports/` incrementally and synthesize from disk.

<!-- /SYNC:task-tracking-external-report:reminder -->

<!-- SYNC:cross-stack-impact-trace:reminder -->

**MUST ATTENTION** FIRST review action — note change context + holistically trace full pipeline of main affected area across client↔server seam (BE→FE forward, FE→BE backward). Verify both tiers still agree on route/DTO/field/type/nullability/auth; any mismatch = BREAKING finding. Skip only for single-tier / docs-only changes (state so).

<!-- /SYNC:cross-stack-impact-trace:reminder -->

<!-- SYNC:cross-service-check:reminder -->

**IMPORTANT MUST ATTENTION** microservices/event-driven: scan producers, consumers, sagas, contracts in task scope. Per touchpoint: owner · message · consumers · risk (NONE/ADDITIVE/BREAKING). Missing consumer = silent regression.

<!-- /SYNC:cross-service-check:reminder -->

<!-- SYNC:end-to-start-debugger-trace:reminder -->

**IMPORTANT MUST ATTENTION** debugger trace gate: for non-trivial bug/fix/investigation/review work, start at the observed final output and trace backward through reader -> storage/projection -> writer -> consumer/job -> producer/trigger. Enumerate all feeder paths and hypotheses before fixing; select the authoritative invariant owner from project architecture and retain validation at untrusted boundaries. **BLOCKED until** trace, hypothesis matrix, owning fix layer, and forward convergence proof exist.

<!-- /SYNC:end-to-start-debugger-trace:reminder -->


<!-- SYNC:goal-contract-satisfaction-loop:reminder -->

- **MANDATORY** Resolve the active Goal Contract BEFORE work (active plan `goal.md` → `<plans root>/goals/{YYMMDD-HHmm}-{slug}/goal.md`, plans root default `plans` and overridable via a `docsRoots.plans.path` entry in `docs/project-config.json` → create from current request) and read saved success criteria before editing.
- **MANDATORY** Append iteration evidence after execution; emit a Goal Satisfaction matrix (PASS/FAIL/BLOCKED) before reporting PASS; loop on validated FAIL; escalate repeated no-progress or blockers. NEVER store secrets in goal files.

<!-- /SYNC:goal-contract-satisfaction-loop:reminder -->

<!-- SYNC:severity-rubric:reminder -->

- **MANDATORY** Classify every finding Critical/High/Medium/Low by consequence using the affected asset, shipped impact, exposure, reversibility, evidence location, and confidence; Critical/High/MEDIUM remain actionable under the round bar, while LOW is recorded/deferred from round 2 onward.
- **MANDATORY** A finding names a reachable trigger path (caller, input, state or event that reaches the defect) and a consequence; an unreachable concern is an observation, and unsettled reachability is `NOT VERIFIABLE` only when the concern would be MEDIUM or higher (an observation otherwise) — never a speculative LOW.
- **MANDATORY** Keep binary gates separate from severity: a failed test, security must-fix, required artifact, or parity check blocks at every round and is never relabeled LOW.
- **MANDATORY** Score-based skills (sre 0-2, perf two-axis) map onto the same four tiers — no parallel severity vocabulary.

<!-- /SYNC:severity-rubric:reminder -->


<!-- PROMPT-ENHANCE:STEP-TASK-CLOSING:START -->

## Prompt-Enhance Closing Anchors

- **IMPORTANT MUST ATTENTION** follow declared step order for this skill; NEVER skip, reorder, or merge steps without explicit user approval
- **IMPORTANT MUST ATTENTION** for every step/sub-skill call: set `in_progress` before execution, set `completed` after execution
- **IMPORTANT MUST ATTENTION** every skipped step MUST include explicit reason; every completed step MUST include concise evidence
- **IMPORTANT MUST ATTENTION** if Task tools unavailable, maintain an equivalent step-by-step plan tracker with synchronized statuses

<!-- PROMPT-ENHANCE:STEP-TASK-CLOSING:END -->


<!-- SYNC:trade-off-interrogation-gate:reminder -->

- **MANDATORY MUST ATTENTION ALWAYS ASK THE 3 TRADE-OFF QUESTIONS** — on the thing under review AND on every recommendation you make: (1) **what does it SACRIFICE?** name the dimensions checked (change cost · complexity · perf · coupling · reversibility · migration · ops load · blast radius · security · testability · delivery time · UX) — "none"/"pure win" is an unfinished analysis; (2) **is it worth it?** gain (with a metric) vs cost, WHO pays, WHEN → emit **WORTH IT / NOT WORTH IT / UNCLEAR**; NOT WORTH IT → withdraw or replace it; (3) **is it MATERIAL enough to confirm with the user?** irreversible/one-way door · cost shifted onto another team/ops/maintainer/user · one quality attribute traded for another · a tier/service/event/library boundary crossed · auth/money/data-integrity/breaking-change/High-or-Medium-risk path · verdict UNCLEAR → **STOP and confirm via `AskUserQuestion` BEFORE the verdict**.
- **MANDATORY** A MATERIAL trade-off with no user confirmation can NEVER be PASS; never bury one as a Low-severity note, never decide it silently, and never let delivery or convergence pressure authorize a one-way door — an un-walked-back one-way door is the user's call, not the reviewer's.
- **MANDATORY — a context that cannot ask escalates BY HANDOFF, never by silence.** `AskUserQuestion` reaches only the main interactive agent, so a sub-agent or a terminal/verdict-only mode cannot ask. There the duty is REDIRECTED, not waived: still name the trade-off, still decide materiality, record `confirmed? = NO — cannot ask from this context`, and **state the unconfirmed MATERIAL trade-off in your RETURNED verdict so the CALLER escalates it** (a note only in an on-disk report is not a handoff); never emit an unqualified PASS. If you CAN ask, you MUST ask.

<!-- /SYNC:trade-off-interrogation-gate:reminder -->


<!-- SYNC:review-principle-awareness -->

> **Review Applicability / Current-Principles Awareness** — Every review must first classify the change context (greenfield foundation, brownfield feature/refactor, test/docs/config/UI/infra, or actor-facing/machine surface) and take notice of the applicable current principles below. This is an evidence-gated applicability check, not a mandate to flag or build every item.
>
> **Detailed protocol routing — read/apply only when warranted:**
> - `SYNC:scale-ready-foundation` — greenfield foundation is blocking; big-feature brownfield fit/adapt/defer; architecture review is advisory when auditing. Detailed carriers: `workflow-greenfield-init`, `workflow-big-feature`.
> - `SYNC:test-architecture-execution-contract` — assertion-bearing tests use the project's configured/native format, name the guarded intent/technical contract, and assert an owned outcome; GWT is one valid format. Detailed carriers: `integration-test`, `workflow-greenfield-init`, and the test-architecture review path.
> - `SYNC:ai-agent-as-user-access` — when an AI/machine actor or future contract is evidenced, inspect identity/delegation, capability boundaries, selected API/CLI/MCP/WebMCP/event/SDK surface, safety/consent, audit/observability, and native-format contract tests. Detailed carriers: `workflow-greenfield-init`, `workflow-big-feature`, `architecture --mode=review`.
> - `SYNC:design-system-check` — when UI changes, inspect the design-system and component-contract obligations; route visual/UX depth to the owning UI review.
>
> **Review behavior:** Check only principles applicable to the reviewed scope; record `APPLY-NOW`, `ADAPT-IN-SLICE`, `DEFER-AS-OPPORTUNITY`, `NOT-APPLICABLE`, `BLOCKED`, or `UNVERIFIED` with `file:line`/config/CI evidence, status/severity, owner/route, and next step/revisit trigger. Do not invent findings from a generic checklist, flag unrelated pre-existing gaps as regressions, silently expand the requested scope, or mutate a parent gate merely because advice exists.
>
> **Ownership:** `changes-review` coordinates the applicability pass and routes depth to the owning specialist (`architecture --mode=review`, `integration-test --mode=review`, `security-audit`, `performance-review`, `ui-design --mode=review`, `production-readiness-review`, or another matching review). A specialist reports its own lens and does not duplicate or override another review's verdict; existing brownfield gaps stay advisory unless new, safety-relevant, or explicitly in scope.
>
> **Required review note:** `context/scope | principle/protocol checked | evidence | status/verdict | severity | owner/route | next step/revisit trigger`.
>
> **BLOCKED when:** an applicable principle is required for safety/correctness but missing, unowned, or untestable. Otherwise record an evidence-backed `NOT-APPLICABLE`, advisory, `DEFER-AS-OPPORTUNITY`, or `UNVERIFIED` result according to the lifecycle and change context; creating a greenfield foundation remains subject to its own blocking protocol.

<!-- /SYNC:review-principle-awareness -->

<!-- SYNC:review-principle-awareness:reminder -->

**IMPORTANT MUST ATTENTION** Every review first checks the change context and routes only applicable principles to their detailed protocols: scale-ready foundation, test intent in the project's native format (GWT is one option), AI-agent-as-user access, and UI/component design when relevant. Record evidence-backed apply/adapt/defer/N/A/block/unverified status with owner and next step; do not invent unrelated findings or expand scope.

<!-- /SYNC:review-principle-awareness:reminder -->

## Closing Reminders

**IMPORTANT MUST ATTENTION Goal:** Resolve the requested review target and apply the matching adversarial review path (plan/PBI rationale, code changes, docs/spec/report, findings, or explicit artifact) so decisions, findings, and plans survive adversarial rationale review before downstream work proceeds.

**IMPORTANT MUST ATTENTION Main steps (full mode) — execute in order, the skill AI keeps forgetting:** (1) DETECT MODE — `--validate-findings` is TERMINAL; (2) read `references/full-mode.md` in full (BLOCKING), then bind the self-recursive review loop — protocol loop primary (host-independent), optional `/goal` gate WHEN available — + Task Bootstrap (phase tasks + closing Findings Validation Gate task); (3) RESOLVE TARGET TYPE + read active Goal Contract + route by concern; (4) REVIEW as SKEPTIC — 7 Anti-Bias boxes (incl. the **Trade-Off Interrogation Gate**: trade-off? worth it? material → confirm with user) + Validation Checklist (presence AND quality depth) + Round 2 re-review + spec↔tests↔code triangulation; (5) FINDINGS VALIDATION GATE — re-invoke terminal `--validate-findings`, reconcile, then re-DO the full review only for report defects or missed findings identified by validation (at most 2 re-dos; 3 full review cycles total); hand off retained target findings without claiming target PASS, then ask next step via `AskUserQuestion`. NEVER skip, reorder, or merge a step without explicit user approval. — why: the steps ARE the review's integrity; dropping one ships an unproven verdict.

**Protocols in force (concise digest of the SYNC/shared blocks this skill carries):** these are signposts — the canonical bodies above are binding; MUST ATTENTION honor each, NEVER treat a digest line as the full rule.

- **End-To-Start Debugger Trace:** for non-trivial bugs, trace observed final state backward to trigger.
- **Behavioral Delta Matrix:** bugfix verdict needs ≥3-row pre/post delta table, one outside report.
- **Nested Task Creation:** workflow rows still expand child phase tasks; link parent when nested.
- **Task Tracking & External Report:** bootstrap tasks; persist long-review findings to `tmp/reports/` incrementally.
- **Sequential Thinking:** multi-step Thought N/M with REVISION/BRANCH/HYPOTHESIS markers and confidence closer.
- **Evidence-Based Reasoning:** cite `file:line`/grep/docs for every claim; no proof, no recommendation.
- **Double Round-Trip Review:** report-only here: review → validate → reconcile report defects → holistic re-review when reconciliation changes the report → validated handoff. The fixing caller owns target fixes, severity eligibility and failed binary gates.
- **Fresh Context Review:** after a fix cycle restart full review with fresh zero-memory sub-agents.
- **Review Protocol Injection:** embed all 11 protocol bodies VERBATIM into each fresh sub-agent prompt.
- **Graph Impact Analysis (optional):** `blast-radius` can suggest impacted files as a stale-able hint; never required.
- **Severity Rubric:** classify findings Critical/High/Medium/Low by consequence; round 1 blocks on every open validated finding (Round-1 LOW closure), round 2 blocks only CRITICAL/HIGH/MEDIUM, and LOW is recorded/deferred. Failed binary gates always block regardless of tier.
- **Trade-Off Interrogation Gate:** always ask — trade-off? worth it? material → confirm with the user before any PASS.
- **Parallel Sub-Agent Dispatch:** Tag tasks PAR/SEQ, group PAR into disjoint-write-set waves, spawn each wave in ONE message, barrier before advancing.

**IMPORTANT MUST ATTENTION** default stance SKEPTIC, NOT validator — before ANY verdict complete all 7 Anti-Bias Gate boxes: steel-man ≥1 rejected alternative, name ≥1 unseen alternative, list 2-3 arguments AGAINST chosen approach, stress-test 2-3 hidden assumptions, run a pre-mortem, check pros/cons symmetry, run the Trade-Off Interrogation Gate. — why: section presence is never a pass, and a reviewer who already endorsed the reasoning needs a forced reset to find what's wrong.

**IMPORTANT MUST ATTENTION ALWAYS ASK THE 3 TRADE-OFF QUESTIONS** — on the decision under review AND on EVERY recommendation you yourself make: (1) **Is there any trade-off?** name what it SACRIFICES across future change cost · complexity · performance · coupling · reversibility · migration · ops load · blast radius · security · testability · team skill · delivery time · UX — "no trade-off" / "pure win" is an unfinished analysis, so state the dimensions checked and why each is unaffected; (2) **Is it worth it?** weigh gain vs sacrifice explicitly — what is gained (with a metric), what it costs, WHO pays, WHEN it comes due → emit **WORTH IT / NOT WORTH IT / UNCLEAR**; NOT WORTH IT → withdraw or replace the recommendation, never keep it; (3) **Is the trade-off material enough to confirm with the user?** MATERIAL when irreversible (one-way door) · cost shifted onto another team/ops/maintainer/user · one quality attribute traded for another · a tier/service/event/library boundary crossed · an auth/money/data-integrity/breaking-change/High-or-Medium-risk path · or the worth-it verdict is UNCLEAR → **STOP and confirm via its OWN `AskUserQuestion` BEFORE the next-step question and BEFORE any PASS verdict**, stating the trade-off, both options, what each sacrifices, and your recommendation. Emit the `Trade-Off Assessment` table every review; a MATERIAL trade-off with no user confirmation can NEVER be PASS, and NEVER bury one as a Low-severity note. In `validate-findings` terminal mode: assess and record, do NOT ask — flag it so the caller escalates. — why: a benefit named without its price is an endorsement rather than a review, unpriced fixes cost more than the bugs they remove, and a one-way door is the user's call to walk through, never the reviewer's.
**IMPORTANT MUST ATTENTION** resolve target type BEFORE reviewing: plan/PBI rationale, code changes, docs/spec/report, findings, or another artifact. Commit/PR/diff input defaults to code-change review; say "no active plan" ONLY for unresolved plan-rationale requests, NEVER silently convert target types. — why: wrong target type reviews the wrong artifact against the wrong checklist.
**IMPORTANT MUST ATTENTION** recursion guard is non-negotiable: full mode may call `/why-review --validate-findings` at most ONCE; validate-findings mode is TERMINAL — NEVER re-invokes why-review, NEVER runs the gate, NEVER spawns a sub-agent. — why: any of these from terminal mode causes infinite recursion.

**IMPORTANT MUST ATTENTION** cite `file:line` evidence + severity + confidence for EVERY finding (>80% act, <60% do NOT recommend); reject "probably / should be / I think" — why: an unproven finding is speculation, not a review result.
**IMPORTANT MUST ATTENTION** judge by Easy-to-Change — every finding, test, refactor, abstraction must lower future change cost; name the real enemies (coupling, hidden state, duplicated knowledge, unclear intent, premature irreversible decisions) or reject the recommendation. — why: this metric overrides any downstream "best practice" that raises change cost.
**IMPORTANT MUST ATTENTION** search 3+ existing patterns and read target files BEFORE judging conventions; evaluate fit before flagging a nearby pattern as "wrong" (closest example ≠ matching preconditions). — why: local conventions override generic framework defaults; pattern-matching without context manufactures false findings.
**IMPORTANT MUST ATTENTION** break work into small todo tasks via `TaskCreate` BEFORE starting; in full mode create the **Findings Validation Gate** closing task at skill START (Task Bootstrap) and run it whenever findings exist — re-invoke `/why-review --validate-findings` (TERMINAL, SAME session) to confirm every finding is correct, proof-backed, reasonable, best-practice; RE-DO ONLY on surfaced finding issues/enhancements (at most 2 re-dos; 3 full review cycles total, then escalate via `AskUserQuestion`). — why: the gate catches inflated, misread, or unproven findings before handoff.
**IMPORTANT MUST ATTENTION** execute the review loop: review → validate findings → reconcile report defects → full re-review when reconciliation changes the report; validation CLEAN ends this report review and hands off all retained target findings. NEVER implement target fixes here or retain an unvalidated finding; NEVER reuse a sub-agent across rounds (spawn NEW `Agent` calls); main agent reads sub-agent reports but does NOT filter or override. — why: every re-review invalidates the prior verdict, and orchestrator confirmation bias hides regressions a fresh zero-memory reviewer catches.
**IMPORTANT MUST ATTENTION** judge the WHOLE PACKAGE, not the diff alone — resolve the configured canonical spec owner and profile, then load its declared requirements/scenarios, mapped executing tests and assertions, and the changed code together; a missing or disagreeing face is itself a finding (CODE-WRONG / SPEC-STALE / TEST-GAP / SPEC-SILENT). Use §3 AC / §4 BR / §8 TC only when the strict default profile applies. NEVER mark PASS while any face disagrees without a logged finding. — why: the diff is the entry point, the package is the unit of judgment.
**IMPORTANT MUST ATTENTION** when the target holds integration/E2E tests — or changes behavior that HAS covering integration tests — apply the **Integration-Test-Review Linkage**: `/integration-test --mode=review` owns the 8 test-quality gates, so read its protocol (Mode A default) or delegate to it (Mode B, standalone full mode only) rather than judging assertion quality by eye. SKIP under any of the 4 guard rows (validate-findings mode · invoked by `/integration-test --mode=review` finding validation · by `changes-review` in ANY phase — 0.8, 6, or 7.5 — or `/workflow-review-changes` · by `/investigate --mode=debug`'s root-cause gate) and record the deferral line. — why: this skill's `Test/spec/doc sync` dimension claims to prove tests protect the invariant, but only those gates can answer it; and an unguarded call closes a `why-review → integration-test --mode=review → why-review` cycle.
**IMPORTANT MUST ATTENTION** every behavior-changing finding carries BOTH a spec-drift verdict (CODE-WRONG / SPEC-STALE / AMBIGUOUS / SPEC-SILENT / in-sync) AND profile-mapped test feedback; a SPEC-SILENT verdict additionally requires enriching the configured canonical owner with its missing requirement/invariant and scenario/case, plus an actual guarding assertion mapped to the declared executor cardinality. The strict default profile uses §4 BR/§3 AC + §8 TC. A missing axis is HAS-ISSUES, never a clean finding. — why: code-only fixes silently drop the invariant from the spec and leave it unguarded.
**IMPORTANT MUST ATTENTION** for bugfix / regression / behavior-changing reviews, walk the End-to-Start debugger trace (observed final state → backward → feeder paths → hypothesis matrix → owning layer → forward convergence proof) and produce the Behavioral Delta Matrix (≥3 rows, ≥1 row outside the bug report) BEFORE the verdict; any REGRESSION delta → FAIL until a preservation test covers it. — why: narrative claims hide regressions and symptom-first fixes the matrix and trace force into view.
**IMPORTANT MUST ATTENTION** require fixes at the owning layer — the lowest layer that owns the invariant — NEVER at the symptom/crash site; a fix touching 3+ files with defensive checks signals the wrong layer, go lower. — why: symptom-site patches leave every other consumer exposed.
**IMPORTANT MUST ATTENTION** High/Medium residual risk must be fixed, reduced, or explicitly accepted by the user/owner before PASS; AI-extracted spec or test-case artifacts are not accepted evidence unless the configured canonical owner/review gate accepted them. — why: unowned residual risk is a deferred failure, not a pass.
**IMPORTANT MUST ATTENTION** flag 3+ duplicated patterns for extraction and same-suffix classes (`*Entity`/`*Dto`/`*Service`) for a shared base when it lowers future change cost; NEVER recommend a pattern with fewer than 3 occurrences (YAGNI). — why: both over- and under-abstraction raise future change cost.
**IMPORTANT MUST ATTENTION** read reference docs chosen by Project Reference Docs Gate (always include `lessons.md` from the project-reference docs root — default `docs/project-reference/`; path from `docsRoots.projectReference.path` in `docs/project-config.json`); persist long-review findings to `tmp/reports/` incrementally; validate the next step with the user via `AskUserQuestion` in full mode — NEVER auto-proceed. — why: project docs override generic assumptions, external memory survives compaction, and the review gate is user-owned.
**IMPORTANT MUST ATTENTION** add a final review todo task to verify work quality.
<!-- FIX-LOOP-MODE:START -->

**IMPORTANT MUST ATTENTION `--fix-loop` mode (OPTIONAL — only when the flag is present):** pair the full-mode review pass + `/fix` in a recursive loop over a fixed target — review to find validated blocking findings → `/fix` to resolve them → fresh full re-review of the CHANGED target — until a complete full-mode pass clears the current round's exit bar (round 1: zero open findings; round 2: zero CRITICAL/HIGH/MEDIUM, LOW deferred). Steps: (FL-0) target + Goal Contract + loop task plan → (FL-0b) bind the convergence loop (protocol loop primary, optional `/goal`) → (FL-1) full-mode pass INLINE → Trade-Off Gate → `/fix` VALIDATED blocking findings at owning layer → Iteration Log → (FL-2) converge / escalate → (FL-3) recap + deferred next-step question.
**IMPORTANT MUST ATTENTION** in `--fix-loop`, NEVER self-invoke with the flag (each round is plain full mode), NEVER run the pass or the mode as a sub-agent, and NEVER let a read-only caller pass the flag; a sub-agent receiving `--fix-loop` refuses it and runs report-only.
**IMPORTANT MUST ATTENTION** in `--fix-loop`, ALWAYS ask the 3 trade-off questions BEFORE every fix lands — NOT WORTH IT → do not apply, count still-open; MATERIAL → PAUSE the loop and confirm via `AskUserQuestion` before the edit; convergence pressure NEVER authorizes a one-way door.
**IMPORTANT MUST ATTENTION** in `--fix-loop`, convergence = a **fresh full** review pass over the **post-fix** target with zero open findings in round 1 (Round-1 LOW closure), or zero CRITICAL/HIGH/MEDIUM from round 2 onward (remaining LOWs listed as deferred); apply ONLY validated findings (≥85% survival bar); never rely on a stale clean verdict predating the last fix.
**IMPORTANT MUST ATTENTION** enforce the **round cap (default 3, hard maximum 3)**; review blockers not shrinking across 2 rounds or increasing, or the budget spent with findings still open → **STOP & escalate** via `AskUserQuestion`. NEVER loop past round 3 on review blockers, or open-ended — only failing test gates continue, until green.
**IMPORTANT MUST ATTENTION** `--fix-loop` does NOT commit or push unless the user explicitly asks.

<!-- FIX-LOOP-MODE:END -->
<!-- SYNC:sequential-thinking-protocol:reminder -->

**MUST ATTENTION** use structured reasoning for complex or ambiguous work, implicitly when visible markers would clutter. Verify hypotheses, revise assumptions, and close with confidence, assumptions, open questions and a concrete next action.

<!-- /SYNC:sequential-thinking-protocol:reminder -->

> **[IMPORTANT]** Analyze how big the task is and break it into many small todo tasks systematically before starting — this is very important.

> **[GOAL REMINDER — MUST ATTENTION CRITICAL]**
>
> Ensure every review target is reasonable, correct, proof-backed, and best-practice aligned.
> **ALWAYS ASK THE 3 TRADE-OFF QUESTIONS (every decision AND every recommendation you make):** (1) **is there any trade-off?** — name what it sacrifices; "none" is an unfinished analysis, not an answer; (2) **is it worth it?** — gain vs cost, who pays, when → WORTH IT / NOT WORTH IT / UNCLEAR; (3) **is the trade-off material enough to confirm with the user?** — irreversible, cost shifted to someone else, one quality attribute traded for another, boundary crossed, high-consequence path, or UNCLEAR → STOP and confirm via `AskUserQuestion` BEFORE the verdict. NEVER resolve a material trade-off silently. — why: naming a benefit without its price is an endorsement, not a review, and a one-way door is the user's call to walk through, never yours.
> **MANDATORY SECOND PASS (full mode):** whenever Round 1 produces ANY finding, you MUST call `/why-review --validate-findings` a SECOND time on those findings to confirm each is correct and reasonable BEFORE handoff. NEVER skip it; NEVER suppress, demote, or under-report findings to dodge it. The self-recursive review loop — the **protocol loop primarily** (host-independent), plus a `/goal` Stop-hook gate WHEN available — BLOCKS stopping until findings are validated. — why: an unvalidated finding is an unproven claim, and a second self-review catches the misreads and inflation Round 1 rationalized.

**Anti-Rationalization:**

| Evasion                 | Rebuttal                                                                                |
| ----------------------- | --------------------------------------------------------------------------------------- |
| "No active plan"        | Valid only for unresolved plan-rationale requests; commits/diffs/PBIs/docs are targets. |
| "Just code review"      | Still resolve target, read docs, map tests/specs/docs.                       |
| "Findings look obvious" | Validate every finding via terminal `--validate-findings`.                              |
| "Round 1 is enough"     | Full mode with ANY finding MUST run the SECOND `--validate-findings` pass; the protocol review loop (and the `/goal` Stop hook when available) blocks stopping until it does. |
| "Report zero findings, skip the gate" | Suppressing/demoting findings to dodge validation is the exact bias the SKEPTIC stance forbids; surface them, THEN validate. |
| "Validate inline, don't re-invoke" | The second pass is a real terminal `/why-review --validate-findings` call on the written report — not a mental once-over. |
| "All dimensions at once" | One focused pass per dimension; split attention catches misses.                        |
| "Ask later"             | Full mode asks user next step before completion.                                        |
| "Looks good / faces agree" | Default SKEPTIC; complete all 7 Anti-Bias boxes; triangulate spec↔tests↔code — any disagreeing face is a finding. |
| "No trade-off here / pure win" | Unexamined ≠ absent. Name the dimensions checked (change cost, complexity, perf, coupling, reversibility, ops, security, delivery) and why each is unaffected. |
| "Trade-off is obvious, it's fine" | Emit the explicit WORTH IT / NOT WORTH IT / UNCLEAR verdict with gain, cost, who pays, when. "Obvious" is not a verdict. |
| "I'll note the trade-off in the report instead of asking" | A MATERIAL trade-off needs its OWN `AskUserQuestion` before any PASS — a buried note is not a confirmation. |
| "Just a review, not my decision to escalate" | Surfacing a material trade-off for the user's call IS the review's job; silence hands the decision to no one. |
| "Behavior change, no spec impact" | Emit a spec-drift verdict + profile-mapped test action; SPEC-SILENT requires requirement/invariant and scenario/case enrichment at the configured owner plus a guarding test. Strict default only: §4 BR/§3 AC + §8 TC. |
| "Fix where it crashes"  | Fix at the owning layer (lowest invariant owner); the crash site is the symptom, not the cause.       |
| "High risk, but ship"   | High/Medium residual risk must be fixed, reduced, or owner-accepted before PASS.        |

<!-- SYNC:core-engineering-principles:reminder -->

**MUST ATTENTION** Core Engineering Principles — every plan, implementation and review must be **Easy to change** (reuse first, one owner per rule, interfaces/adapters at volatile boundaries, no speculative abstraction) · **Easy to scale** (extend by addition, bounded growth, explicit boundaries, sized to the project's real profile) · **Easy to maintain** (intent-named tests that fail when the rule breaks across happy/error/edge paths; harness green locally and in CI). Before done: next change → how many edit sites? 10× → what breaks? which test goes red?

<!-- /SYNC:core-engineering-principles:reminder -->
