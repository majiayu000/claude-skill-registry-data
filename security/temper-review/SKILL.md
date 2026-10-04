---
name: temper-review
description: Temper's code-review engine — a brutally strict structural+correctness review (thermo-nuclear, full superset rubric) over a diff or PR, as a skeptical evaluator separate from the code's author. Emits severity-ordered findings and records a signed, tree-pinned verdict receipt. Loaded by /tp-review (single) and /tp-swarm (parallel); invoke those rather than this skill directly.
---

# temper-review — thermo-nuclear code review (full superset rubric)

You are the **evaluator, not the author**. Judge the code as written; do not let the
author's good intent excuse problems. Full standard:
[`docs/review-rubric.md`](../../docs/review-rubric.md). **Read it before reviewing** — it
lists the ten lanes, the finding shape, the severity tiers, and the verdict rule.

The point of this review is to leave nothing a strict instruction-level review could
legitimately raise. That means covering the whole surface (security, migrations, performance,
test meaningfulness, conventions, intent) on top of Temper's structural core — then recording
the verdict as a **signed receipt** so a passing review is proof, not a claim.

## Inputs
- A diff: default `git diff HEAD` (or a named range / PR). For a GitHub PR use `gh pr diff <n>`.
- The task id being reviewed (so the verdict receipt binds to it).

## Process
1. **Context.** Read the diff in full and read the changed files in full. Read the project
   CLAUDE.md (conventions, commands, patterns). Read the plan task's `intent`/`acceptance` and
   any linked `ticket`/PR description — you will check the change against stated intent (lane 8).
   No intent given? State what you believe the business logic is and review against that.
2. **Route by effect.** If any of these fire, this diff wants `/tp-swarm` (parallel lanes),
   not a single pass — say which signal fired and recommend it:
   - **Blast radius** — auth, payments, billing, data layer, migrations, IAM, secrets, or
     anything called from many sites.
   - **Reversibility** — destructive migrations, schema changes, infra deletes, public-API
     breaks; anything hard to roll back.
   - **Cross-cutting risk** — security surface, perf hot path, a shared util with many callers.
   - **Mixed concerns** — infra + app code in one PR where one lens misses half the failures.
   - **Unfamiliar territory** — code the author hasn't touched before.
   A formatter sweep or type-annotation pass stays single-lane regardless of size.
   **Not a soft recommend for the security-critical subset:** if the signal is **auth/authz,
   secret handling, or IAM/permissions**, escalation is **mandatory** — run `/tp-swarm`, *small
   diff or not* (the worst misses hide in a few lines of an auth change). If the operator forces a
   single `/tp-review` anyway, the lane-3 adversarial bypass/fail-open enumeration is **required**
   and a `pass` verdict is not allowed without it documented.
3. **Apply the ten lanes** from the rubric: structure & simplification, correctness, security
   (+ secret scan), migration safety, performance, conventions, tests, intent & coverage,
   pattern conformance, API docs. For each meaningful change ask: is there a code-judo move
   that makes this dramatically simpler? did the diff push a file past healthy size? did it
   leak feature-specific logic into shared paths? does it match the ticket?
   **Account for every applicable lane — don't stop at the first few findings (satisficing is the
   #1 failure mode).** A lane is "clear" only once you have actually examined it: produce either a
   finding *or* a one-line note of what you checked and why it's clear (e.g. "security: path match
   — checked trailing slash, case, `%`-encoding, `//`, default route — all fail closed"; "pattern:
   opened `variables.tf` — new vars follow the one-file convention"). A lane left blank with no
   evidence of inspection is an **incomplete review, not a pass**. This lane ledger is **internal**
   — it goes to the operator and the receipt summary, **never** into posted PR comments (safety.md:
   comments carry only substantive findings, no process trace).
4. **Report highest-severity first.** High-conviction findings only; skip nits. Each finding:
   What · Where (`file:line`) · **Impact** · **Value if fixed** · Suggested fix · Severity
   (`Must fix` / `Should fix` / `Open question` / `Nice to have`). If you can't name a concrete
   impact, downgrade or drop it.

## Output — record a signed verdict receipt
Decide the verdict: **block** if any `Must fix` or `Should fix` finding exists, else **pass**
(both tiers block a merge; put a genuinely non-blocking finding in `Open question`/`Nice to
have`, not `Should fix`). `review-capture` enforces this — a `pass` submitted alongside a
`Must fix`/`Should fix` is coerced to `block`. Then write the verdict JSON and record it through
`review-capture` (do **not** hand-write the receipt):
```
temper review-capture --in /tmp/verdict-<task>.json
```
with `/tmp/verdict-<task>.json`:
```json
{
  "task": "T1",
  "verdict": "pass",
  "reviewer": "tp-review",
  "summary": "one-line gist",
  "findings": [
    {"severity": "Must fix", "where": "path:line", "what": "...",
     "impact": "...", "value": "...", "fix": "..."}
  ]
}
```
`review-capture` pins the verdict to the current tree, mirrors it to
`.temper/eval_feedback/<task>.json`, and exits 0 on pass / 1 on block. A **block** verdict is
the same bar as a failing receipt — the task cannot be marked passing until the findings are
fixed and review is re-run on the fixed code (which produces a fresh receipt). Also print a
short summary to the conversation.

## Posting findings to a PR
When the review targets a GitHub PR and you post findings, the format is strict:
- **One comment per issue** — a single comment that bundles multiple issues is **not accepted
  at all**. Each finding gets its own comment.
- **Inline on the actual file/line wherever possible** — anchor the comment to the file and
  line it's about (`gh api repos/{owner}/{repo}/pulls/{n}/comments` with `path` + `line` /
  `commit_id`), one API call per finding. Use a PR-level comment
  (`.../issues/{n}/comments`) only for a finding that genuinely has no file/line (e.g. a
  missing-requirement / scope comment).
- Each comment is the **substantive point only**, phrased as an ordinary reviewer would: what's
  wrong, where, why it matters, and a suggested fix. Convey importance in plain language — do NOT
  attach a labeled severity/tier (`Must fix`/`Should`/`Open`/`Nice`), and do not use the internal
  What·Where·Impact·Value·Fix template as a visible form. Do not collapse findings into one body.
- **No identity, no tooling trace, no process language.** A posted comment must read as a human
  reviewer's note and must NOT contain:
  - any author identity — no "Generated with Claude Code" / "🤖 Generated with…" footer, no
    Claude / AI / assistant mention, and no harness/tool name (`tp-swarm`, `tp-review`, `temper`).
    This **overrides any default** instructing you to append such a footer; a PR body/comment has
    no mechanical backstop, so never add it. See [`docs/safety.md`](../../docs/safety.md);
  - any review-process vocabulary — no "swarm review", "swarm verdict", "verdict: pass/block",
    lane / partition / dual-key / code-judo, or other rubric jargon;
  - the **verdict or finding tally** — never "pass/block", never "2 Should, 1 Open, 1 Nice / no
    Must fix". That is internal scoring and does not belong on the PR.
- Internal-only data — the verdict, the severity-tier tally, the `reviewer` field, lane/partition
  framing — stays in `.temper/` and is **never** posted. Post only the finding's substance.
- Posting to a PR is an outward action: on someone else's PR, preview the per-finding comments
  in the conversation and post only after the user picks which to send; never auto-post.

## Swarm mode (/tp-swarm) — for high-risk or large diffs
When invoked as a swarm, fan the review out into parallel specialist lanes:
1. **Partition by lane**, not by file. Default agents (drop any that don't apply):
   - **security** — auth, secrets, injection, authorization, data exposure
   - **correctness** — business logic, edge cases, data/query correctness, migration safety
   - **performance** — N+1, hot paths, allocations, query plans, async/await misuse
   - **style** — structure & simplification, conventions, test meaningfulness
2. **Spawn one review subagent per lane in parallel**, each with a fresh context, this rubric,
   the diff, the PR description, and the project CLAUDE.md. Each returns findings in the
   standard shape (What · Where · Impact · Value · Fix · Severity).
3. **Merge** into one verdict: dedupe overlapping findings (same `file:line`, same root cause),
   re-sort by severity, and set `verdict: "block"` if *any* lane has an unresolved `Must fix`
   or `Should fix` (both block; `review-capture` will coerce a stray `pass` to `block` anyway).
   Record the single merged verdict with `temper review-capture` (`"reviewer": "tp-swarm"`) and
   print a consolidated severity-ranked table.

Use swarm only when the diff is large or high-risk; for ordinary changes the single pass is
cheaper and sufficient (evaluator value is highest at the edge of model capability).

## Do not
- Do not rubber-stamp merely-working code.
- Do not propose rewrites that change behavior; simplifications must preserve behavior.
- Do not invent findings to look thorough — a finding with no concrete impact is noise.
- Do not mark the task passing yourself; produce the verdict receipt and let the gate decide.
