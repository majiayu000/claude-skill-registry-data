---
description: "The cost-discipline constitution for multi-agent work: the **session's top model orchestrates; cheaper tiers execute**."
---

# /tiered-delegation

The cost-discipline constitution for multi-agent work: the **session's top model orchestrates; cheaper tiers execute**. Invoke it when a session is about to fan out subagents or workflows (audits, marathons, parallel implementation, large research) to load the delegation rules — who does what tier of work, how far down to push each task, and when a claim must be re-verified before it drives an action. It composes with the marathon machinery (`/prime-directive`, `/tackle-issues`, `/parallel-dev`) and with ad-hoc Workflow/Agent fan-outs alike.

The core invariant: **the model you are running as is the ceiling, not the default worker.** Orchestration, synthesis, and judgment stay at the ceiling; breadth, mechanics, and drafts go down-tier; nothing is ever delegated *up* past the session model, because a higher tier may simply not be available to the harness — a skill or prompt must never assume one.

## Arguments

- `$ARGUMENTS` — optional: a one-line description of the fan-out about to happen (e.g. `verification pass over 50 findings`, `implement 4 quick-win issues in parallel`). Used only to pick the matching scale row below; empty is fine.

## The tier ladder

Resolve the ladder from the active harness. Codex uses Astra for orchestration and Sol for workhorse tasks; Claude follows the installed fleet tier policy. Never assume an unavailable model.

Resolve the ladder **relative to the session model** at invocation time:

- **Ceiling** = the model this session runs as. It orchestrates. If the session runs a mid-tier model, that mid-tier IS the ceiling — the roles below all shift down one notch, and nothing tries to spawn a higher tier than the ceiling unless the harness explicitly lists one as available.
- **Workhorse** = one tier below the ceiling. Implementation, exploration breadth, per-area mapping, research fan-outs.
- **Mechanical** = the cheapest available tier, at low effort. Formatting, extraction, file shuffling, templated transforms.

When only one tier exists, everything runs at the ceiling and this skill's value reduces to the verification and role rules — that is fine; never invent a tier.

**Choosing the session ceiling is itself the biggest tier decision.** Routine orchestration belongs on **a mid-tier ceiling, not the top-most tier**: the orchestrator's main thread re-reads its full context at cache-read rates on every turn, and the top tier's cache-read rate is roughly double the tier below it — so a marathon orchestrated from the top tier pays double on the largest cost component for work a mid-tier ceiling handles fine (dispatching waves, running merge gates, writing briefs, triaging queues). Reserve the top-most tier (the highest listed orchestration tier) for the moments that actually need it: **convergence assessment** (is this run genuinely done?), **adjudicating ambiguous-blocked calls** (blocked-for-real vs blocked-by-timidity), and **gnarly decomposition** (carving an epic whose seams aren't obvious). Start those as fresh, narrow sessions or delegate them up only when the harness lists the tier as available — a standing marathon session at the top tier is an anti-pattern, not a safety margin.

## Role split (who does what)

| Role | Tier | Work |
|---|---|---|
| **Orchestrator** | ceiling | Decompose the task, write worker briefs, make scope/design decisions, synthesize results, write every user-facing conclusion. Never delegates synthesis or final judgment. |
| **Workers** | workhorse | Implementation (TDD in isolated worktrees when parallel), exploration/mapping breadth, research sweeps, drafting issue/PR bodies. |
| **Verifiers** | workhorse by default; ceiling-adjacent (or higher effort) for the riskiest claims | Independent, adversarial, **refute-first** re-checks of down-tier claims. A verifier never shares context with the producer of the claim it checks. |
| **Formatters** | mechanical, low effort | Entity cleanup, templated sections, batch file writes, index updates. |

## Non-negotiable rules

1. **Down-tier claims don't drive actions unverified.** Any load-bearing claim produced below the ceiling (a "this feature is absent" finding, a "tests pass" report, a dedup call) gets an independent adversarial verification before it triggers an irreversible or outward-facing action — filing issues, merging, publishing, deleting. Scale verifier strength to blast radius: surprising/security/destructive claims get the strongest affordable verifier; routine confirmations get the workhorse.
2. **The orchestrator stays the prime investigator.** Spot-check the load-bearing calls yourself; read the synthesis inputs yourself; never relay a subagent conclusion to the user that you haven't at least sanity-checked. Delegation conserves tokens, not accountability.
3. **No up-tier drift.** Worker briefs and skills must not hard-code a model name above the session ceiling. Specify roles ("workhorse", "mechanical") or omit the model so the harness inherits the session default — hard-code a specific tier only when certain it is at-or-below the ceiling.
4. **Don't duplicate delegated work.** Once a search/implementation is delegated, the orchestrator waits for the result instead of re-running it inline. Inline spot-checks are for *verifying*, not re-doing.
5. **Parallel writers get isolation.** Concurrent write-capable workers each get a worktree; read-only reviewers are explicitly forbidden to `checkout`/`switch`/`stash`. Re-verify worktree-built changes in the main checkout before merge (worktrees often lack `node_modules`/build state).
6. **Effort is a dial, not a default.** Mechanical stages run at low effort; implementation at default; only the hardest verify/judge stages get high effort. Raising effort is cheaper than raising tier — try it first.

## Scale table (match the fan-out to the task)

| Situation | Shape |
|---|---|
| Quick question / single-file fix | No delegation. Ceiling works solo; delegation overhead exceeds the work. |
| Standard task (one issue, one PR) | 1 workhorse implementer (worktree if anything else runs in parallel); orchestrator reviews + lands it. |
| Research / audit | Workhorse fan-out per area → **mandatory adversarial verify pass** over surviving claims → orchestrator synthesizes. Baseline/yardstick work can fan out in the same wave. |
| Marathon (multi-issue waves) | Waves of 2-4 parallel workhorse implementers in worktrees; orchestrator runs review/merge gates serially; formatters batch the paperwork; verify pass before anything irreversible. |

## Workflow mechanics

- Prefer the Workflow tool for deterministic fan-outs (per-agent `model:`/`effort:` overrides, `isolation: 'worktree'`, structured-output schemas); prefer single Agent calls for one-off background workers.
- Every worker brief is **self-contained**: repo context, exact scope, house style, what NOT to touch, the return format, and the project's exploration shortcut (targeted `rg` and exact reads; no repo-memory connector is wired here).
- Workers return raw findings/diffs; the orchestrator owns wording. Worker output that will reach the user verbatim (issue bodies, PR text) carries the same zero-attribution and honesty rules as the orchestrator's own writing.
- Record in the session log which tier produced and which tier verified each load-bearing result — on reload after compaction, unverified down-tier claims are re-verified, not trusted.

## Anti-patterns (each has burned a real session)

- Delegating the synthesis/report to a worker and pasting it to the user unread.
- A workhorse-produced "absent/missing" claim filed or acted on with no refute pass — explorers over-report absence; verifiers exist because of this.
- Spawning the ceiling tier for mechanical formatting because it was "already the default".
- Running a whole marathon with the top-most tier as the session model "for quality" — paying ~2x cache-read on every orchestration turn for work a mid-tier ceiling handles; the top tier earns its rate only at convergence/adjudication/decomposition moments.
- A skill hard-coding a top-tier model, breaking sessions that run below it.
- The orchestrator re-grepping what a delegated explorer is already searching, paying twice.
