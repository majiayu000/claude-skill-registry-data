---
model_tier: inherit
name: ai-council
description: "Use when polling external AIs (OpenAI, Anthropic) outside the host session for a neutral second opinion on a roadmap, diff, prompt, or file set — or 'cross-check with another model'."
domain: process
meta_skill: true
parallelizable: independent
workspaces:
  - agent-config-maintainer
packs:
  - meta
---

> **Experimental.** AI Council is not yet validated by external users. API costs apply per consultation.

<!-- cloud_safe: degrade -->

# ai-council

## Council-first — try the council BEFORE the user, on these classes

```
A DESIGN DECISION THE AGENT CANNOT SETTLE FROM THE TREE GOES TO THE COUNCIL
FIRST, NOT TO THE USER FIRST. THE USER IS THE ESCALATION, NOT THE DEFAULT.
NEVER PRESENT A COUNCIL VERDICT THAT WAS NOT REACHED. AN INCONCLUSIVE RUN
IS REPORTED AS INCONCLUSIVE, AND WHATEVER YOU DECIDE INSTEAD IS LABELLED
OWN ANALYSIS.
```

Interrupting the user is the expensive path: it costs a round trip and their
attention, and on a question two models could have settled it buys nothing they
wanted to be asked. So the ordering is **tree → council → user**, and the
council leg is the one that gets skipped.

**Classes that go to the council first** — each is a judgement with a real
trade-off and no answer in the tree:

| Class | Example |
|---|---|
| Competing implementations of one feature | two sessions shipped the same phase; discard, overwrite, or merge |
| Which of N designs, all defensible | four declared types with a derived fifth, or five declared |
| Reopening a recorded decision | an ADR or honest-null blocks a change that now looks net-positive |
| Scope re-cut inside an authorized task | this phase splits into two, or absorbs the next |
| Is the evidence sufficient to conclude | n=1 measurement, a proxy metric, an unreplicated finding |

**Classes that still go straight to the user, and the council never substitutes
for them:** anything behind the Hard Floor
([`non-destructive-by-default`](../../rules/non-destructive-by-default.md)) ·
spend · a scope EXPANSION beyond what was authorized · a decision whose inputs
only the user holds (a preference, a deadline, a business constraint) · the
`high_impact` and `user_required` classes, which
[`ask-when-uncertain`](../../rules/ask-when-uncertain.md) routes to the user by
Iron Law. A council cannot consent on the user's behalf, and asking it to is not
autonomy, it is laundering.

### When the council cannot answer

Measured 2026-08-17: a run returned **0 of 2 seats**, both `cli_quota_exhausted`,
with the counters at 72/50 and 99/50. The CLI reported it correctly as
`INCONCLUSIVE — DEGRADED` and did not print a quorum it had not reached. Three
things follow, and the first is the one under pressure:

1. **Never dress your own verdict as the council's.** A fan-out, a solo read, or
   your own judgement is a legitimate substitute **only when named as such** —
   the boundary [`council-availability`](../../rules/council-availability.md)
   states.
2. **Do not bounce to the user just because the council failed.** An
   unreachable council does not upgrade a decidable question into a
   user-required one. Decide it, label it own analysis, state the reason the
   council was unavailable, and name what would change the answer.
3. **Escalate only if it is genuinely undecidable without them** — the two
   options are close AND the cost of being wrong is high AND nothing in the tree
   separates them. Then say the council was attempted and why it failed, so the
   user is not asked to arbitrate something they will assume was already tried.

`agent-config council:status` is free and answers availability; `council_cli
estimate <file>` is free and answers parse-and-cost. Run both before concluding
the council is not an option — and note the question goes in a **file**, since
prose passed as an argument overflows the argument limit.

## When to use

* The host agent has drafted a roadmap, plan, or design and wants an
  **external** critique that is not biased by its own framing.
* The user asks "what would Claude / GPT say about this?" or invokes
  `/council`.
* A PR diff or commit range needs a second-opinion review beyond the
  internal four-judge pass.
* A free-form proposal benefits from being challenged by an outside
  reviewer before it calcifies into work.

Do NOT use when:

* The decision is internal-only and budget matters more than diversity
  of opinion → use `subagent-orchestration` (in-session, no network,
  no money).
* The task is **iterated build → review → fix with full repo access by a
  single strong model** (the reviewer needs to see the working diff and
  return actionable fixes) → that is **team mode** (`/team`), the depth
  complement to the council's breadth. The council is artefact-only and
  never grants the external model repo access or the host's framing; team
  mode deliberately does the opposite. Neither replaces the other.
* The artefact contains secrets that cannot be redacted with the
  bundler's pattern set → ask the user before sending.
* The user has not configured any council member → state that and stop;
  do not silently fall back to anything. **But "not configured" is
  decided by the CLI, never by the project tree** — see the rule below.

## Configuration is ALWAYS user-global

```
THE COUNCIL CONFIG IS ALWAYS USER-GLOBAL. NEVER SEARCH THE PROJECT FOR IT.
THE ABSENCE OF A COUNCIL FILE IN A PROJECT SAYS NOTHING ABOUT WHETHER
THE COUNCIL IS CONFIGURED. ONLY THE CLI / RESOLVER DECIDES THAT.
```

The council config lives at one place only:
`~/.event4u/agent-config/settings/.ai-council.yml` (per
[ADR-104](../../../docs/decisions/ADR-104-ai-council-config-global-only.md),
superseding ADR-093). It is configured **once per developer** and works
in **every** project, worktree, and CWD — including consumer repos that
carry none of this package's internals.

Before claiming the council is unavailable, you MUST run the CLI
(`council:estimate`) and read its exit code + message. **Never** conclude
"council not configured in this project" from missing project files:
`scripts/ai_council` (a package-internal directory, absent from every
consumer repo), `.agent-settings.yml` (the legacy block was removed in
ADR-093), or a project-local `.ai-council.yml` (never read — ADR-104).
Eyeballing the project for any of these and then deciding solo — instead
of running the resolver — is the canonical failure ADR-104 exists to stop.

The only escape from the user-global location is `$AI_COUNCIL_CONFIG`, an
explicit absolute path for tests / power users — still not a project search.

## When NOT to invoke — necessity self-check

The Phase 6 necessity classifier (see
[`ai-council-config § Necessity classifier`](../../../docs/contracts/ai-council-config.md))
runs as a pre-flight gate inside the CLI and skips the council when
the prompt looks like routine work. Route around it BEFORE the gate
fires so the user never pays the classifier-pause cost on a request
that obviously did not need a council in the first place.

Skip the council and stay in-session for:

* **Bugfix shape** — stack trace, error, crash, failing test, "broken",
  regression. Use `systematic-debugging` or `bug-investigate`.
* **Syntax / format / lint** — `typo`, `formatting`, `lint`, `indent`,
  `import order`, simple rename. Use the language skill directly
  (`php-coder`, `eloquent`, `nextjs-patterns`, etc).
* **Single-file implementation** — "this function", "this method",
  "this file", "one-liner", "small change", "add a getter". Use the
  language skill directly.
* **Documentation lookup** — "what is X", "how does Y work", "example
  of Z", "syntax of W". Use `codebase-retrieval` or the docs skill,
  never the council.

Invoke the council when:

* **Architectural / structural** — system boundaries, coupling,
  refactor strategy, migration plan, rewrite vs redesign.
* **Multi-axis trade-off** — stakeholders disagree; competing
  alternatives need weighing; "pros and cons" is the actual ask.
* **Strategic / direction** — "should we …", "shall we …", roadmap
  shape, long-term technical direction.
* **Explicit ambiguity** — the user wrote "unsure / uncertain /
  ambiguous / second opinion / sanity check".

Agent orchestration MUST call `council_cli` with
`--invocation agent` so the gate can skip silently on routine
requests. User-typed `/council` keeps the default
(`--invocation user_explicit`); the user gets the educational message
+ `--proceed-anyway` override path. Mode `block` ignores
`--proceed-anyway` by design — cost-strict opt-in.

## Goal

Bring in **independent** external models to critique a project
artefact. Independent means: the council members never see the host
agent's reasoning, internal state, or framing language — only the
artefact (roadmap, diff, prompt, file set) plus a neutral system
prompt that asks them to think on their own merits.

## Neutrality guidelines (Iron Law)

```
THE COUNCIL NEVER SEES THE HOST AGENT'S ANALYSIS, REASONING, OR FRAMING.
ROUND 1 SEES THE ARTEFACT + THE NEUTRAL SYSTEM PROMPT. NOTHING ELSE.
ROUND 2+ MAY SEE PRIOR PEER REPLIES — ANONYMISED ONLY, NEVER ATTRIBUTED, NEVER THE HOST'S.
THE HOST AGENT IS THE CONVENER, NEVER A REVIEWER.
```

If you find yourself wanting to "frame" the artefact for the council,
stop. Framing is exactly what kills the second-opinion value. Use the
unbiased system prompts in `scripts/ai_council/prompts.ts`; do not
roll your own.

The host runs the council and synthesises convergence — it is the
convener, not a reviewer. The reviewer-ban is structural: the host
wrote (or framed) the artefact and cannot critique it independently.
Anonymising the host as "Reviewer C" is worse than excluding it — the
user is told they got an outside vote when they did not. Externals
down → surface and skip; never substitute the host as a reviewer.

## Modes

This skill is a router head. Everything above is true in every mode and stays
here: which decision classes reach the council at all, what to do when it cannot
answer, the user-global configuration fact, the necessity self-check, and the
neutrality Iron Law. So does the output format below — it is an ordered MUST that
a pointer cannot carry. The operational manuals live in `references/`; load the
one the task calls for, not the set.

| Task | Mode body | Covers |
|---|---|---|
| Pick an execution mode, or handle a degraded one | [`references/execution-modes.md`](references/execution-modes.md) | Manual-mode and CLI-mode UX, the cost-gate bypass for non-billable members, degradation modes |
| Run a session end to end | [`references/procedure.md`](references/procedure.md) | The neutrality context-handoff, the numbered procedure, the convener-skeptic stance, why a mechanism claim needs a probe rather than a second opinion, what this is NOT |
| Place the artefact, or render the synthesis | [`references/output-and-synthesis.md`](references/output-and-synthesis.md) | Output path convention with its forbidden and exempt sets, lens-aware synthesis templates, the `--prose-synthesis` escape hatch, renderer lens resolution |
| Estimate or gate the spend, or check what is redacted | [`references/cost-and-redaction.md`](references/cost-and-redaction.md) | Redaction expectations, cost awareness, the pre-call estimate format, the stale price-table gate, the mid-flow overrun callback |
| Multi-round debate, deep tier, advisors, replay, low-impact fast-path | [`references/advanced-modes.md`](references/advanced-modes.md) | `rounds:N` debate, the deep-reasoning tier and its manual-mode parity, `/council debate`, Karpathy peer-review, thinking-style advisors, the decision-replay artefact, the Lightweight-QA fast-path with its own Iron Law and output markers |

Two of those bodies carry obligations a pointer cannot summarise: the
output-path convention is enforced by CI, and the Lightweight-QA fast-path
markers are required verbatim by
[`fast-path-marker-visibility`](../../rules/fast-path-marker-visibility.md).
Load the body before acting in either mode rather than working from memory of it.

## Procedure

1. **Inspect first.** Run the necessity self-check above and read the artefact
   you are about to hand over. It is cheaper to not convene than to convene and
   discard.
2. **Confirm availability** — `agent-config council:status`, never an inference
   from the project tree (see § Configuration is ALWAYS user-global).
3. **Pick the execution mode** from
   [`references/execution-modes.md`](references/execution-modes.md).
4. **Run the session** per the numbered procedure in
   [`references/procedure.md`](references/procedure.md), under the neutrality
   Iron Law above — the preamble is not optional and the question is never
   authored toward a conclusion.
5. **Estimate the spend before the call** per
   [`references/cost-and-redaction.md`](references/cost-and-redaction.md).
6. **Write the artefact** in the output format below, at the path
   [`references/output-and-synthesis.md`](references/output-and-synthesis.md)
   fixes, then apply the convener-skeptic verdict yourself — convergence is not
   correctness.

## Output format

Every council reply MUST contain, in this order:

1. **Header line** with mode, member count, and total token cost.
2. **One section per member**, titled `### <provider> · <model>`,
   containing the member's verbatim output.
3. **Convergence / Divergence summary** — bullet list, every claim
   attributed by provider name. **When the convergence settles a
   question as "don't relitigate" / locked / a durable disposition**,
   the summary MUST record two additional lines, per
   [`decision-revisit-gate`](../../rules/decision-revisit-gate.md):
   `scope:` (exactly which mechanism or question is settled — narrow
   enough that a superficially similar but different proposal is not
   silently covered) and `revisit-if:` (at least one concrete condition
   that reopens it — new evidence class, model-generation or tooling
   change, an N-th blocked encounter, or an age threshold). A lock
   recorded without both lines is an authoring error. Also state
   whether the disposition is **settled-by-evidence** (an eval ran) or
   **settled-by-decision** (a maintainer call) — the latter is cheaper
   to reopen and should say so.
4. **Host verdict per finding** — one row per finding with `accept`
   / `accept-with-modification` / `reject` / `needs-input` plus a
   one-line reason citing host evidence (file:line, ADR, contract).
   See *Critical evaluation* above.
5. **User-facing options — CONDITIONAL, on ownership.** A conclusive
   **technical** verdict emits **no** options block: it is a resolution,
   and handing it over as options routes a technical decision to a person
   because it was hard (ADR-268 § 10). The block is owed when the verdict
   is owner-owned (`product-owned`, `business-owned`, `destructive-owned`)
   or when the council did not converge — then it is a numbered block per
   `user-interaction`, carrying the host verdict in each option, with
   "discard council input" always present. Convergence is read from the
   record, never inferred: a record that does not say whether its members
   converged is itself the finding. Checkable in both directions with
   `./scripts-run src/scripts/council_record_shape <record.md>`.

The host agent NEVER ships council output as its own reasoning, and
NEVER ships the host verdict as council output. Provider attribution
stays visible in the per-member sections; host verdicts stay
attributed to the host.

> **Tally-vs-reasoned boundary.** Option-level decisions (which design /
> approach to take) use the council **stance tally** — the Convergence /
> Divergence summary aggregates member stances across the option set.
> Finding-level review (is this specific bug/line real) uses the
> **reasoned validation** in [`code-review`](../code-review/SKILL.md)
> (each finding stands on its own traced reason, never a vote count). The
> two never cross-apply — no resolving a design option by
> reasoned-validating one member's take, no resolving a bug finding by
> counting council votes. Mirrored in `code-review` so the boundary is
> grep-checkable from both sides.


## Do NOT

- Do NOT paraphrase council output into the host agent's voice — strip
  attribution and you've stripped the value.
- Do NOT surface council findings to the user without a host verdict
  — convergence ≠ correctness, and the user deserves the agent's
  reasoned filter, not a raw forward.
- Do NOT pre-warm the council with the host agent's analysis or
  identity — that primes the reviewer and collapses diversity.
- Do NOT silently truncate a too-large bundle — surface the size and
  ask for narrower scope.
- Do NOT spend against an unbounded budget without asking — a billable
  member with neither `max_total_usd` nor `daily_limit_usd` set has no
  ceiling, and autonomy is not a ceiling.
- Do NOT reuse SDK clients across invocations — re-load keys via
  `load_*_key()` each call.

## Gotchas

Real failure modes seen in the wild:

- **Bias-by-framing:** agent pastes "I think X is the right answer,
  what do you think?" → council rubber-stamps. Symptom: 100%
  convergence, zero unique insight. Fix: send artefact only, neutral
  preamble, no host reasoning.
- **Silent budget overrun:** `cost_budget_exceeded` mid-fan-out, agent
  retries one member to "complete" the council. Result: skewed sample,
  hidden spend. Fix: surface partial result, stop, ask user.
- **Identity leak:** roadmap text contains "the agent decided…" —
  reviewer infers host model and mirrors it. Fix: redact host-agent
  identity strings before bundling.

| Anti-pattern | Why it's wrong | Correct approach |
|---|---|---|
| "Pre-warm" the council with the agent's own analysis. | Bias attack — collapses the reviewer to a yes-man. | Send the artefact text only. |
| Paste the host-agent identity ("I am Augment / Claude Code…") | Identity primes the reviewer's model. | Neutrality preamble in `prompts.ts` already handles this. |
| Silently truncate a too-large bundle. | Misleads the reviewer into thinking they saw the whole thing. | Bundler raises `BundleTooLarge`; surface and ask for narrower scope. |
| Reuse the same SDK client across calls without re-loading the key. | Leaks the key in long-lived process state. | Each invocation builds fresh clients from `load_*_key()`. |
| Spend against a billable member with no configured ceiling because "the council is standing-authorized". | Standing authorization is a *bound* the user set once, not a blank cheque. No ceiling = nothing was authorized. | Surface the estimate and ask, exactly in that one case (Procedure § 3). |
| Re-ask per invocation once a ceiling exists. | The ceiling already carried the decision; re-asking is the approval burden this default removed. | Fan out; let `on_overrun` ask on breach. |
| Forward council convergence to the user as numbered options without a host verdict. | Convergence ≠ correctness; the council never saw the codebase. | Apply the *Critical evaluation* lens; tag every finding `accept` / `accept-with-modification` / `reject` / `needs-input` with one-line reason. |
| Reject a finding on preference, not evidence. | "I don't like this" is not a verdict. | Cite the file, line, ADR, or contract that justifies the rejection — or surface as `needs-input`. |
| Paraphrase council output into the host's own analysis to defend a verdict. | Strips attribution, breaches `direct-answers` no-invented-facts. | Verdict cites host evidence (file:line); council output stays attributed in the per-member sections. |

## Redaction and cost

Both moved verbatim to
[`references/cost-and-redaction.md`](references/cost-and-redaction.md): what the
bundler's redaction pass strips, the cost-awareness rules, the pre-call estimate
format, the stale price-table gate, and the mid-flow overrun callback. A breach
without `on_overrun` short-circuits the remaining members — surface the partial
result and ask, never retry silently.

## Advanced modes

Multi-round debate, the deep-reasoning tier, Karpathy peer-review, thinking-style
advisors, the decision-replay artefact and the Lightweight-QA fast-path moved
verbatim to [`references/advanced-modes.md`](references/advanced-modes.md). Each
is opt-in and each prices higher than a single round; none is a default.

## See also

- `/council` command — the user-facing entry point.
- `subagent-orchestration` skill — internal multi-agent variant (no
  network, no spend, but no diversity of weights either).
- `/team` command — collaborative cross-model review WITH repo access
  (depth); council is breadth on an artefact, team is one strong model in
  the repo. Different mechanism, not a competitor.
- `scripts/ai_council/prompts.ts` — neutrality preamble + per-mode
  system prompts.
- `scripts/ai_council/advisors.ts` — replace-mode planning + persona
  resolution.
- `scripts/ai_council/bundler.ts` — redaction pattern set + size
  guard.
- `docs/customization.md` § `ai_council.*` — settings reference.
- `docs/contracts/ai-council-config.md` § advisors — schema + precedence
  contract.
- `docs/contracts/ai-council-config.md` § Decision-replay artefact —
  Phase 9 audit trail contract + redaction modes.
- `scripts/ai_council/replay.ts` — pure projection renderer (no model
  calls).
