---
name: goal
description: Autonomous goal loop — give it ONE goal plus how to verify it, the agent runs check→fix→check itself and comes back only with the finished result (code with audit, research with fact-check, content with critique, audit/backtest). Self-verification instead of constant supervision, with hard safety guards. Vary the loop with a verification rubric designed before it runs. Triggers — "work autonomously to the result", "don't come back until it's done", "run the loop yourself", "drive it to done".
---

# /goal — autonomous goal loop

You prompt yourself a proactive executor: state a GOAL plus how to verify it, and the agent runs check→fix→check on its own, returning ONLY with the finished result. Frees you from sitting at the monitor nudging every step.

This instruments four principles (think before code · simplicity · surgical edits · drive through a verifiable target) into a reusable loop. Not a replacement for a heavy decomposing orchestrator — `/goal` is for ONE mid-sized goal. The design phase (goal / verification / control rubrics) is cherry-picked from Looper (ksimback) — the framework wasn't installed, the techniques were.

## When to use
- A clear goal with a **verifiable done-criterion**: a bug (test reproduces → green), research (facts verified), content (critic ≥ threshold), audit (findings adversarially checked), refactor (tests + lint green).
- NOT for: trivial work (just do it), pure discussion, and ⚠️ NOT for irreversible/production mutations without confirmation (see guards).

## Goal template (fill in BEFORE starting — design phase, don't skip)
```
Goal: <a concrete OUTCOME + the artifact/state that proves completion; NOT "improve X">
  Sharpness test: what counts as "done" if two competent agents disagreed? Subjective → measurable proxy.
Scope: included <…> / excluded <…> / max depth <…>
Context: <path to project/data, symptoms, logs — what to READ, not assume>
Checks (typed, programmatic FIRST — see "Verification"):
  - [programmatic] <test / compile / run script / grep an invariant / critic ≥ N>
  - [judge] <rubric for semantics — judged by a SEPARATE pass, not the author>
  - [human] <user sign-off: taste / business / money / legal risk>
Done-criterion: <all programmatic green AND judge=pass AND human (if any)>
Budget (whichever hits first = STOP): cycles N=3-5 · time <if relevant> · tokens <if relevant>
```

## Verification — types (programmatic → judge → human)
- **programmatic** (preferred WHENEVER possible): a command returns pass/fail — test/build/lint/schema/grep/script. Deterministic goes FIRST.
- **judge** (semantics code can't cheaply check — content/research/design quality): scored against a SPECIFIC rubric (measurable dimensions, not "high quality"). ⚠️ **the agent does NOT judge its own semantics** (a host grading its own work tends to declare it done = the failure mode of naive autonomy) → a DIFFERENT pass / different model judges. Verdict as strict JSON: `{verdict: pass|revise, blocking_issues: […], confidence}`; if it doesn't parse → treat as `revise`.
- **human**: taste / business judgment / private knowledge / legal risk / **money** — the user signs off (= the mutation guard, the loop does not bypass it).
- Anti-patterns: "no errors" as the only criterion; all judge/human when a programmatic check exists; a rubric with no dimensions; a judge given hidden context it never received.

## Loop rules
1. **Reproduce/understand BEFORE editing** — find root cause, don't patch blindly (blind patching burns context).
2. **Minimal surgical edit** — only what moves toward the goal.
3. **Run REAL checks** — commands/script/run, not "looks right".
4. **Failed → read logs, fix, retry.** Don't stop after the first failure.
5. **Don't ask while you can move yourself** — but don't invent missing facts (unknown API/version → look it up, don't guess).
6. **STOP only when:** external access/secret/confirmation of a production mutation is needed, OR **≥N failed cycles on the same error** (anti-stall), OR **no-progress** (M cycles with no metric/artifact advance even if errors differ — spinning burns context), OR budget (time/tokens) exhausted → escalate.

## ⚠️ Guards (the difference from "just autonomous" when real money/irreversible actions are in play)
- **Production/irreversible mutation = ALWAYS confirm; the loop does not bypass it**: process restart, order, deploy, rm, git push, kill — the loop reaches the mutation point and STOPS for confirmation. Read-only/code/backtest/content cycle freely.
- **Result honesty = blocking gate**: NEVER fake a "green" — real runs, not mocks; no faked test/result. Can't reach it → STOP + escalate, NOT fake.
- **Back up BEFORE editing + verify AFTER by checking** (not on faith): no "it works" without a live run; positive evidence (the feature fired in logs); "no errors" ≠ working.
- **Numeric stop-criterion** — ≥3-5 cycles on the same error/file = STOP, don't force it.
- **Durable trail for a long loop** — `run-log.md` (each step/decision/check result/blocker) + `state.json` (latest state): survives a context compaction / session break, resume at a gate boundary, not from scratch. Optional for short loops.
- **Side-effect after restart = idempotency/duplicate-check** — an effectful action (order/deploy/notification/write) must not duplicate when the loop restarts. Before repeating an action, check whether it already happened.

## Final report (only when the goal is reached OR on STOP)
- **Root cause** briefly (what was actually wrong, not the symptom).
- **Diff summary** — what changed and why (each edit ← from the goal).
- **The real check commands and their RESULT** (the output, not "passed").
- If STOP — what blocks it + what's already done + what's needed from the user.

## Anti-actions
- ❌ Don't bypass confirmation of a production mutation "because it's autonomous mode".
- ❌ Don't fake check results to exit the loop.
- ❌ Don't patch blindly without root cause (≥3 blind = STOP).
- ❌ Don't grind >N cycles on the same error — it burns context, escalate.
- ❌ Don't return "seems done" without checks actually run.
