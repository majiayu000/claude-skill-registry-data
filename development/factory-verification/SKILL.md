---
name: factory-verification
description: How we know the software the factory produces is correct, and how we know the kit's own conventions are followed. Defines the four-tier eval spectrum (CLI rule / test / agent / human gate), the rule that evals graduate downward to their cheapest home, the banded coverage score with severity-aware disclosure, and the delta-gated GitHub Action that guards the PR boundary without disrupting the inner loop. The recipe locks to `factory-kit-check` + GitHub Actions; the principles are stack-agnostic. Read at project kickoff, when wiring the conformance gate, and whenever asking "how do we know the agent did this right?"
---

# Factory verification

Each section leads with **Principle** (one sentence, stack-agnostic), then **Why** (constraint → option → tradeoff), then **Recipe** (the `factory-kit-check` + GitHub Actions shape we use), and **Failure mode** when there's one to name.

This skill answers a question the others assume: when an agent produces code, how do we know it's right — and how do we know the kit's own conventions were actually followed, not just documented? Scope is two layers: **L1**, verifying the software the factory ships; **L3**, verifying the factory's own conformance. Evaluating *shipped LLM features* (golden datasets, LLM-as-judge) is **L2** — a distinct problem, deferred; see the forward-pointer at the end.

## Verification is manufactured rigor

**Principle.** When you unbundle production from comprehension — an agent produces, a human directs — you must deliberately re-add the verification that hand-writing every line used to bundle in for free. Code you didn't type is guilty until verified.

**Why.** Hand-coding made comprehension a precondition of output: you could not ship what you did not understand, because understanding was the only way to produce the text. Agent-assisted building breaks that coupling — code can ship that no human has reasoned about. The constraint is the same as it ever was (don't ship what you can't stand behind); the option that vanished is "the work forces understanding on you." So the rigor must be manufactured on purpose. The trade-off accepted: verification is now explicit cost — gates, reviews, a score — where it used to be a free side effect of typing. That cost is the price of the leverage; refusing to pay it is not a saving, it's a deferral with interest.

## The four-tier eval spectrum

**Principle.** A verification is an eval. Every eval lives at the cheapest tier that can run it reliably; the factory's job is to keep pushing each eval down to that tier.

**Why.** "How do we know the agent performed well?" has no single answer because correctness is decided in different ways: some by static inspection, some only by running the code, some only by judgment. Conflating them is the trap — people reach for a human review when a regex would do, or trust a green test suite for a question only a human can answer. Naming the tiers lets you put each check where it's cheapest and run it as often as it's cheap.

**Recipe.** Four tiers, by what's needed to decide the question:

| Tier | Decides by | Home | Runs |
|---|---|---|---|
| **CLI rule** | static inspection of the repo | `check/rules/*.ts` (`factory-kit-check`) | the GitHub Action, per PR |
| **Test** | executing code against fixtures | `__tests__/` (Vitest/Playwright) | pre-push + CI |
| **Agent** | semantic judgment, no human | `agents/*.md` (`code-reviewer`, `verification-engineer`, `claude-code-action`) | per PR |
| **Human gate** | comprehension, taste, irreversibility | the person | before merge / before a destructive prod write |

The cheapest tier that *can* decide a question is the right home for it. A missing `.where()` is decidable by inspection → CLI rule. "Does this RAG node return the right chunks" needs fixtures → test. "Is this the right abstraction" needs judgment → agent. "Do I understand this well enough to own it at 2am" is irreducibly human. `factory-db-migration.md`'s preflight/mutate/verify/rollback is this spectrum applied to the highest-blast-radius case: all four tiers, human gate last.

## Evals graduate downward

**Principle.** An eval is born as a human catch, hardens into an agent check, and graduates into a CLI rule — where it runs forever, for free. The promotion path *defect → Failure-mode block → deterministic rule* is that downward migration.

**Why.** A verification caught only by a human runs once, when that human is paying attention. The same verification encoded as a rule runs on every PR, for everyone, with no attention budget. So the highest-leverage move in the whole system is converting expensive judgment into cheap inspection — every pitfall that graduates from "a senior noticed it" to "a rule blocks it" is a verification that can never lapse again. The constraint: not every eval is graduatable — some genuinely need judgment and stay at the agent or human tier. The tradeoff accepted: maintaining the rule set is ongoing work, but it's work that compounds, where re-catching the same defect by hand does not.

**Recipe.** The promotion pipeline, concretely:

1. A defect is caught (in review, in prod, by `verification-engineer`).
2. It's written as a **Failure mode** block in the skill whose principle it violates (or a process pitfall in `factory-pitfalls.md`).
3. When it's decidable by static inspection, a rule lands in `check/rules/` citing that section; its entry is **removed** from the `UNCOVERED` backlog in `check/rules/index.ts`.

The gap between named pitfalls (~40 in `factory-pitfalls.md`) and encoded rules is the **eval backlog**; `UNCOVERED` is its live, severity-tagged list. The shrinking of that list over time *is* the factory's measurable progress. When you add a Failure mode to a skill, either add its rule or add it to `UNCOVERED` — a pitfall that appears in neither is invisible to the score.

## Score the codebase, disclose the instrument

**Principle.** Report a banded verdict (pass / warn / fail), severity-gated; and always alongside it, the coverage that says how much to trust the verdict. The precision of the score must match the precision of the instrument.

**Why.** A wall of findings is not guidance — a developer needs a verdict in one glance. But a precise-looking number (87.3/100) over a regex-heuristic instrument is a lie about confidence: it implies a measurement the tool can't make. A *band* tells the truth — the tool can reliably say "a critical is present" but not "this repo is 87% good." And a verdict without coverage is the more dangerous lie: a green grade from a checker blind to half the critical-class pitfalls reads as "all clear" when it means "clear of the things we happen to check." Disclosing coverage is what keeps the score honest. The tradeoff accepted: a band carries less apparent information than a number; that's correct, because the extra precision was never real.

**Recipe.** The model lives in `check/score.ts`, pure and tested:

- **Conformance band.** `fail` if any **critical** finding (one is disqualifying — a data-loss bug cannot be averaged away by clean cosmetics); `warn` if any **high**; else `pass`. Medium/low inform the counts, never the gate — no tunable "N mediums = warn" knob, because the instrument isn't precise enough to defend the threshold.
- **Coverage.** `activeRules / (activeRules + UNCOVERED)`, reported as a percentage, **plus the severity-aware caveat**: the count and names of critical-class pitfalls with no rule. This is the load-bearing honesty line — `coverageFor()` surfaces `criticalUncovered` precisely so a passing band can't impersonate "nothing critical is wrong."
- **Output.** Terminal report leads with the band; `--json` and `--md` (the scorecard) carry it to the GitHub Action.

## Gate the delta, contextualize the absolute

**Principle.** The PR check fails only when the change introduces a *new* critical; the absolute score is shown for context, never as the gate. Pre-existing debt does not block a PR.

**Why.** A gate on the absolute score punishes whoever happens to touch a messy repo next — which teaches people to avoid touching messy repos, the opposite of what you want. A gate on the *delta* asks the only fair question: did this change make it worse at the severity that matters? That lets a clean PR land in a debt-laden repo (encouraging incremental cleanup) while still stopping the one PR that introduces an auth bypass. The constraint: you need both base and head findings to compute a delta. The tradeoff accepted: the gate ignores standing debt, so a repo can stay red for a long time — but standing debt is a backlog decision, not a per-PR veto, and conflating the two is how gates become things people route around.

**Recipe.** `delta(baseFindings, headFindings)` keys findings by `(ruleId, file, line)`; `deltaBlocks()` returns true on `newCritical > 0` (or `newHigh > 0` when `.factory-check.json` sets `"gateOnHigh": true`). The runner computes base findings by materialising the base ref in a throwaway git worktree (`check/git.ts`) — read-only to the target working tree. With `--base`, the CLI exit code follows the delta gate; without it, the legacy whole-repo `hasBlocking` (critical/high) still applies. This mirrors Codecov's split: project score is context, patch/delta is the gate.

## Guardrails at the boundary, never the inner loop

**Principle.** The score surfaces at the PR boundary as a GitHub Action — a sticky comment plus a check — and never in the developer's edit-run-commit loop.

**Why.** The fastest way to get a guardrail ignored is to make it interrupt flow. A pre-commit hook that blocks a `git commit` to lecture about a pre-existing medium-severity finding trains the developer to `--no-verify`, and now the guardrail is off everywhere. The PR boundary is where review already happens — the score is *there when you look at the PR*, in the same context as human review, costing the inner loop nothing. The constraint: CI feedback is slower than local feedback. The tradeoff accepted: you learn the score minutes after pushing rather than instantly — but for a guardrail (as opposed to a fast typo-catcher like typecheck), arriving at the review boundary is exactly on time, and it's the price of never being the thing that interrupts a developer mid-thought.

**Recipe.** `templates/factory-conformance.yml`, installed into a repo with `npx @nonlinear-labs/factory-kit add-ci`. On `pull_request`: checkout with `fetch-depth: 0` (so the base ref resolves), run `factory-kit-check . --base origin/$BASE_REF --md`, post the markdown as a **sticky** comment (matched by the `<!-- factory-kit-check:scorecard -->` marker, updated in place — one comment, not one per push), and fail the job only on a new critical. Make `Factory conformance` a required check in branch protection (see `factory-ci.md`) to make the new-critical gate load-bearing; the comment itself stays advisory. Composes with `anthropics/claude-code-action@v1` (the agent tier) — the deterministic rules and the agent's judgment fold into the same review surface.

**Failure mode — verification theater.** The gates run as ceremony: the suite is green, the band is checked, the human approval is clicked — but no one read the output. The rung that fails silently is the human comprehension gate: a diff gets approved that the approver could not have written and cannot explain, because "the checks passed." The checks passing is necessary, never sufficient — they verify the absence of *known* failures, not the presence of understanding. Right move: treat the human gate as load-bearing, not decorative. If you can't say *why this code is this way and not another way*, you haven't verified it, you've witnessed it. The day "Claude probably got it right" replaces reading the diff, you've stopped architecting and started hoping — and the score can't catch that, because it's a check on the code, not on your comprehension.

**Failure mode — silent verification gap.** A pitfall is named in a skill but has no rule and no test — it is *documented* but not *enforced*. The skill reads as covered; the score's denominator quietly omits it; a contributor greps the docs, sees the convention, and assumes something checks it. Documentation is not verification. Right move: every Failure mode block lands in exactly one enforced place — a CLI rule, a test, or the `UNCOVERED` backlog (which at least makes the gap *count against coverage*). A convention enforced by nothing is a convention that holds only while the person who wrote it is in the room.

## Layer 2 — evaluating shipped LLM features (deferred)

Verifying an LLM *feature you ship to a client* — does the RAG return the right chunks, does the agent take the right trajectory, has a prompt change regressed — is a different problem from everything above. It needs golden datasets, LLM-as-judge and code evaluators, and regression runs; the machinery exists (the LangSmith dataset/evaluator/trace skills) but is not yet wired into the kit's conventions. It is out of scope here, named so the gap is visible rather than silently missing. When it's built, it slots in as the L2 companion to this skill, and `factory-llm-workflows.md` points at it.

## Source patterns

This skill is **new** in the factory — it synthesizes the verification discipline that was previously scattered across `factory-testing.md` (tests), `factory-ci.md` (the merge gate), `factory-security.md` (AI-code read-only-by-default), and `factory-db-migration.md` (the verify stage), and adds the eval spectrum, the score model, and the delta-gated conformance Action. The score and Action grow the pre-existing `factory-kit-check` skeleton (the `hasBlocking` "GitHub Action contract" stub and the `UNCOVERED` honesty count were already there).

## Related

- `factory-pitfalls.md` — the eval backlog; the labeled dataset the score's denominator is drawn from
- `factory-ci.md` — the merge gate this Action joins; branch protection makes the new-critical gate load-bearing
- `factory-testing.md` — the test tier (rungs 2–3 of the spectrum)
- `factory-security.md` — "AI-generated code is read-only by default" is the same guilty-until-verified principle at the security boundary
- `factory-db-migration.md` — the full spectrum applied to destructive prod writes (preflight/mutate/verify/rollback)
- `factory-llm-workflows.md` — where the deferred L2 (LLM-feature eval) companion will be pointed at
