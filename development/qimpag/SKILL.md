---
name: qimpag
description: ONLY on /qimpag. Questions-first impag — one questions round, then execute.
---

Questions-first variant of `impag`. It does **not** run a questions stage itself — it launches `impag` with a
directive to pause for one interactive questions round at the right moment: **after** `impag` has resolved the
target plan/stage (its steps 1–2), **before** it starts executing tasks (its step 3).

$ARGUMENTS — same as `impag`: plan file path (default: most recent in `docs/plans/`).

## Why this exists
`impag` is full-auto and never stops to ask. `qimpag` keeps `impag` fully in charge of plan/stage resolution
and the entire build — it only injects a single interactive checkpoint once `impag` knows *what* it's about to
build, so the questions are grounded in the actual resolved target rather than guessed up front.

## Process

This skill is a parameterized launch of `impag`. Do **not** load the plan, ask questions, or do any analysis
here — `impag` owns all of that.

1. **Invoke `impag`** at the main conversation level (via the Skill tool), passing the user's `$ARGUMENTS`
   **prepended with the directive below**. Then `impag` runs its normal flow; the directive tells it where to
   stop and ask.

   Directive to pass to `impag`:

   > Then follow `impag/SKILL.md` verbatim — qimpag adds ONLY the single interactive questions round after
   > the target plan/stage is resolved.
   >
   > Run ONE interactive round using `AskUserQuestion`, grouped as up to three short batches — **Goals**
   > (what success/done means, what's out of scope),
   > **Business logic** (domain rules, edge cases, thresholds the plan leaves implicit), and **Technical
   > approach** (architecture/library/seam choices, code location, migration vs. rewrite, test strategy; offer
   > concrete options, highest-maturity first). If `impag`'s plan-authoring pass already persisted a
   > **refactor-first `[USER DECISION]` block**, surface/confirm THAT (via the gated-stage rule below) rather
   > than re-asking migration-vs-rewrite freeform. Ask only what the plan and code don't already settle — skip any
   > batch that's already unambiguous and say why. Also surface the plan's own uncertainty markers (`[AUDIT]`,
   > `[likely cut]`, "not sure whether") as questions. Echo the contract as **four compact lines** —
   > `Goals:` / `Business rules:` / `Technical approach:` / `Out-of-scope:`, one line each, never paragraphs, nothing after them —
   > then **proceed directly**, do NOT ask a separate
   > go-ahead/confirmation question when the questions round already resolved every open decision (the answers
   > ARE the go-ahead; a redundant "shall I proceed?" wastes a turn). Re-prompt ONLY if echoing the contract
   > surfaces a genuinely NEW unresolved choice the questions didn't cover. If the answers reshape the work,
   > **write the agreed intent back into the plan file** (or a `docs/plans/`-tracked addendum) before
   > executing — task subagents re-read from disk, not chat (the plan is their durable contract). Settle the
   > contract first, then write it in one burst right before execution.

2. That's all this skill does. Everything past the questions round — staging, per-task execution (direct or subagent per impag's gate), verification,
   review, finish-branch, retro — is `impag`'s unchanged contract. Don't duplicate or second-guess it here.

## Rules
- The questions belong **inside** `impag`'s flow, after plan/stage resolution — never as a pre-stage in this
  skill. The whole point is that `impag` knows the concrete target before asking.
- **Ground the questions with a brief, not the subsystem.** Recon to ground the questions round (and any
  plan addendum they produce) runs via `Explore`(Haiku) → a condensed brief (line anchors + rule/function
  signatures + design conflicts) — do **NOT** inline-read the subsystem into the parent to "ask better
  questions." A brief grounds them; the byte-exact port is the **chained execution session's** job (fresh
  budget), and inline source re-bills as `cache_read` every turn after. This is `impag`'s delegation gate
  (d), and it holds **even when you intend to write the addendum yourself** — "the port is delicate" is an
  execution-phase concern, and execution is chained away.
- One interactive round **by default** — the upfront round after plan/stage resolution.
- **Never question the checkout, worktree or branch the user launched you in.** Which tree and which
  branch the work lands on is the user's standing choice, already made by where the session was started —
  it is never an `AskUserQuestion` option, not even when that tree is stale, behind `main`, or owes a merge.
  Note the consequence in one line if it matters ("merge to `main` owed before `make ship`") and execute.
- **Gated-stage rounds (standing user preference).** Plan stages the plan itself marks `[USER]` /
  `[USER DECISION]` (or an equivalent gate) are NOT skipped, auto-decided, or folded into the upfront
  round — surface each as its own `AskUserQuestion` round **when execution reaches it**, with the
  concrete evidence + options. For a genuine methodology/design decision (not a mere go/no-go confirm),
  **launch `/mybrain` FIRST** to help the user think it through (trade-offs, overfit/risk, what a
  trustworthy choice requires) — but its options **ship AS the
  `AskUserQuestion` round, in the same message**, never as prose that stops short of the ask.
  Writing "ready to put this to you as a round" IS the failure mode: emit the tool call instead.
  Never end a turn announcing a round you did not call. A **refactor-first `[USER DECISION]` block** `impag`'s plan-authoring pass
  persisted is exactly this
  kind of gated design decision — resolve it here, mybrain-first. Never pre-pick or code around a user-decision stage. A blocking ambiguity the plan
  did NOT pre-mark is still `impag`'s failure path (its **step 1** user-decision stop, plus step 7's
  un-armed chain).
  **Reached deep in a session, a gated stage is a stop — not a pause:** past `impag`'s step-4f zone, record the
  decision owed in project_state's "Next action", leave the chain un-armed (`impag` step 7), and open the round —
  mybrain-first — at the next session's small prefix (cost model → `impag` Rules: *a
  late human-input pause is a stop, not a wait*).
- If the resolved plan/stage is already unambiguous, `impag` skips the questions and proceeds —
  don't manufacture questions just to justify the wrapper.
- **An option's `description` is a factual claim — verify it before offering it.** Risk/cost/"these are
  equivalent" assertions in `AskUserQuestion` options steer the answer, so a wrong one buys a false-premise decision
  and a re-prompt round. When an option rests on a fact you haven't checked (are these two
  constants really mirrors? is this edit behavior-preserving?), re-derive / grep/read the anchor FIRST, or write the
  option so it states the uncertainty instead of resolving it. If a premise collapses after the user answered,
  say so plainly, show the evidence, and re-ask — never quietly execute the answer they'd have given differently.
  **This binds a MECHANISM you derived inline exactly as it binds a cited fact** — harder, since nothing about
  a *therefore* looks like a citation to check. When a description carries one, compute both sides on a toy
  input BEFORE the round (a throwaway sim, per the sim-before-ruling habit), or state the mechanism as
  untested. And verify the option is **ALLOWED**, not merely true: grep the path-gated rule governing the
  surface first — an option a project rule forbids is a false choice even when its description is accurate.
- **A banked literature search does NOT discharge the search obligation for a NEW fork.** A plan doc's
  prior §Search-evidence covers the questions it was run for. When the questions round opens a
  methodology/design fork that search did not ask (a different estimator, a different aggregation rule),
  **search FIRST, then offer options** — reusing the banked evidence silently presents unsearched options as
  if they were evidenced. Applies to the `/mybrain`-first gated round too: mybrain structures the
  trade-offs, it does not supply the sources.
- **A plan STEP'S premise is a claim too** — a "wire X" step may already be DONE by a sibling lever or rest on a
  MIS-MODELED flow; check the DERIVED set at RUNTIME + grep the CONSUMER before executing (LEGP Stage 1: legs
  convert via a LIVE `fetchSeries`, not the stored copy it assumed). Same for a queued **"go measure it"**
  option: the estimator may already be BUILT AND RUN under another name — grep the harness for the arm before
  authoring or offering its plan.
