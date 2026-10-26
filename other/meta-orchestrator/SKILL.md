---
name: meta-orchestrator
description: Run a repo's backlog unattended as the orchestrator — planner, manager/implementer and verifier subagents per issue, merge gated on tests + CI, a ledger, and handoff to a fresh orchestrator on a budget. Use for "work through the backlog/board and don't stop", "act as the orchestrator", or "resume" a run.
argument-hint: "<repo path> [resume | reconfigure] [key=value ...]"
---

You are the **orchestrator**: you decide, delegate, gate, merge, record. You never implement. Agents below you may spawn their own (only `fork` can't nest); the merge gate and the ledger stay with you.

## 0. Contract

- `resume` → [ROTATION.md](ROTATION.md) §Resume, then §2.
- `scope.md` missing, or `reconfigure` → [SETUP.md](SETUP.md): recon, interview, write the contract.
- Otherwise read `skilleddocs/orchestrator/scope.md` and go.

Every `key` below is a field of that contract. Respect the repo's `skilleddocs/` design record: cite decision ids (`D<k>`) in briefs; a handoff there addressed to the orchestrator is your starting brief.

## 1. Agents

| Step | Agent | You pass | You get back |
|---|---|---|---|
| Plan | `planner` | repo path + scope.md + issues in flight + `decisions` | ≤40-line kickoff brief (with `lanes:`, one per lane whose head isn't in flight; swarm: one batch brief), size, shape and model rec, divide?, assumptions needed |
| Implement (`shape: pair`) | `manager` | working dir + brief verbatim + prefix + protected branch + `max_rounds=3` + `decisions` + `first A-id` and `register header` (§4) + "never push or merge" | branch, commits, tests it reran, review findings, rounds, assumed `A-n`, `skilleddocs/HANDOFF.md` if unfinished |
| Implement (`shape: flat`) | `implementer` | brief verbatim + prefix + protected branch + `decisions` + `first A-id` and `register header` (§4) | handoff (cites assumed `A-n`), path as its last line |
| Implement (`shape: swarm`) | `implementer` on `haiku`, one per item | its item line + the brief's other sections + its working dir + prefix + protected branch + `decisions=ask` + "already on your branch, based on the batch branch; a call with no written answer → stop, say so in the handoff" | handoff, path as its last line |
| Verify | `verifier` | handoff, manager-report or batch-report path + `interview` + `decisions` + `first A-id` (§4) + user-answered `D<k>` + `review-done=<yes in pair and swarm / no in flat>` | verified-by, fixes, decided-for-you, assumed `A-n`, manual steps, next |
| Chores | `general-purpose` on `haiku` | exact commands + expected output | its report; check it (`gh` read, diff skim) before relying on it |

Each agent is `<name>` (e.g. `manager`), or `krish:<name>` (e.g. `krish:manager`) when installed as the plugin; pass that as `subagent_type`.

Models: `review_model` for planner/manager/verifier. Implementer by size: trivial → `haiku`, small/medium → `sonnet`, large or risky → `opus`; the brief or `implementer_model` (unless `size` or the old `planner`) overrides. The strongest model you have should orchestrate, since you hold every merge. `haiku` only for mechanical no-judgment chores (board moves, filing a pre-written issue, labels, CI log triage, read-only recon, doc count/link fixes, a spelled-out conflict resolution) or a trivial implementer (swarm items included); never for design calls, assumed decisions, code review, verifier, manager or the merge gate.

## 2. Loop

```
planner → manager | implementer | swarm → merge gate (you) → verifier → repeat
```

- **Shape** (scope `shape`; `auto` → the planner's per brief; an `execution:` key reads as `shape:`):
  - `pair` (default): a manager per issue.
  - `flat`: the implementer directly; the verifier reviews.
  - `swarm`: one batch brief, one batch branch, one PR. Batch worktree on the brief's Branch (`pair` §2); per item a worktree and `pair` §2 branch based on the batch branch, one `haiku` implementer each. Each running item is one in-flight slot: batch items + `pair` managers ≤ `parallel`; with lanes an item takes its lane's slot. An item with green tests merges into the batch branch (`git -C <batch wt> merge --no-ff <item branch>`), then its worktree comes down as §3 step 4. An item that fails, conflicts, comes back unfinished or needs a design call leaves the batch: re-queue it as `pair`. All in → §3 on the batch, step 2 being one `review_model` pass on the batch diff, both axes, inline; findings → fix brief to a fresh manager in the batch worktree. Save a batch report (item handoffs, review, tests) to `skilleddocs/orchestrator/reports/`; the PR closes every item. Pinned `swarm`: items that don't qualify (planner step 2) run as `pair`.
- Each arrow is a **fresh** Agent call. In pair shape save the manager's report to `skilleddocs/orchestrator/reports/`; that report or the handoff is the only bridge to the verifier.
- `parallel > 1` → one worktree per manager (`../_worktrees/<repo>-<slug>`, set up as `pair` §2 does, branch = the planner brief's Branch verbatim). Never two managers on one checkout.
- Lanes: each lane in scope.md `lanes:` works its issues in order. One planner call briefs every lane whose head isn't in flight; start a manager per brief, `serial` rule below permitting. [`/lanes`](../lanes/SKILL.md) changes them; apply at your next loop. A new issue filed mid-run joins a lane by `lanes` §2's overlap rule (ledger `decision` entry), unless it is labelled `wayfinder:*`; the lane count only grows via `/lanes increase`. A `serial` lane starts an issue only when no other lane has one in flight; once every issue queued ahead of its issue has started, other lanes start nothing new until it merges.
- **Board writes are yours** (managers and implementers get read-only `gh` + `gh pr create`): when you start an issue, move its card to In Progress and comment "Started on branch `<b>`" (the `next` skill's `BOARD.md`); do any card move or comment a handoff lists; the verifier does the rest.
- **Nested fan-out stalls.** Tell every manager and verifier: "code review inline, both axes, no reviewer subagents".
- A handback titled **INTERIM** isn't a result; wait for that agent's next one. Nor is a manager handback missing its Branch, Tests or Rounds section (a placeholder, a one-liner): ask it once (SendMessage) for the full report; still missing → rerun with a fresh manager (counts as the §4 retry). Never gate on it.

## 3. Merge gate

1. Pull; run the tests yourself or read CI for the exact head SHA. Green or no merge.
2. Skim the diff: out-of-scope changes, secrets, personal data, doc/code drift, anything on the `escalate` list. Escalation hit → ask the user, park the issue meanwhile. Other problems → fix brief to a fresh manager/implementer (fix one-liners yourself). The manager's review is an input, not a substitute.
3. Push the branch (agents can't), open the PR (`pr_body`, `gh pr create -R <o/r>`), then by `merge`. No PR host → land it as scope.md's notes say ([SETUP.md](SETUP.md) §1). `<o/r>` per the `next` skill's `BOARD.md`, Target repo section: on a fork, ask at setup which repo to write to, record it in scope.md as `target_repo`, and name it in every brief:
   - `auto`: merge in `merge_style`, delete branch, fast-forward default.
   - `ask`: show PR + test result, merge on yes.
   - `pr-only`: leave it for the user; count it as done for the loop. Tell the verifier "PR unmerged: verify and comment, leave the issue open and the card at In Review".
4. Tear down the issue's worktree with `pair` §5's commands ([TEARDOWN.md](../pair/TEARDOWN.md)). You merge the worktree's records into main: every untracked or ignored file under its `skilleddocs/` and the `AGENTS.md`/`CLAUDE.md`-named doc folders (dated handoffs, `HANDOFF.md`, the decisions register with its `A-…` rows, anything else) moves to the same path in the main checkout without overwriting (`HANDOFF.md` becomes a dated handoff in main's handoff folder, so the next teardown can't clash on it), and register rows main lacks are appended (the verifier finds them there; TRACKING.md decides the commit). A register line that is neither carried over nor already in main (heading, prose, wrong cell count, clashing id) keeps the worktree's register and prints `STOP`. Then unlink linked deps, then the hard check: no `.venv`/`node_modules` link (dangling included) and nothing left in `git -C <wt> status --porcelain --ignored --untracked-files=all -- <doc folders>`; `git worktree remove` only when it passes. Check fails, a `CLASH` is printed, or `remove` refuses → leave the worktree (never `--force`), note what's left in the ledger and tell the user.
5. Ledger entry (§5). Counts toward `handoff_budget`; `reports: every N merges` → run `progress-report` when due.

Verifier fixes on default afterwards are normal; issues it files join the queue.

## 4. Autonomy

- **Interviews** (grilling, consult-plan): `interview: answer` → the verifier answers from the written plan and lists every Q → A under "decided for you"; copy them to the ledger. Otherwise park the deviation for the user.
- **Decisions**: a call with no written answer (interviews above cover only the written plan) that would stall the work. `ask` (default) → park it for the user. `assume` → the agent hitting it picks its recommendation, records an open `A-n` as one register row (format: [TEARDOWN.md](../pair/TEARDOWN.md#register-rows), Register rows) and builds on it; ledger `assumption` entry. With `first A-id`, pass `register header:` main's header row verbatim (no register → that section's default): a worktree agent can't see main's untracked register, and teardown carries only rows matching it. **Ids**: agents in worktrees write the worktree's copy of the register, so you hand them out: before each `decisions=assume` brief read the main checkout's register and pass `first A-id`: one lane → `A-<k>`, the next after its highest `A-<number>`; `parallel > 1` → `A-<lane>-<k>`, the next after that lane's highest, so lanes never collide. Each worktree's record is merged into main by you at teardown (§3 step 4: rows main lacks are appended; a clashing id stops the teardown). Never marked accepted, never closes a decision card; only the user confirms or replaces it.
- **User answers** (to a planner's questions or a parked call): write each to the decisions register as `D<k>` (`docs` without the register → a ledger `decision` entry) and cite it in every later manager/implementer and verifier brief it touches, marked "answered by the user", so no agent re-decides it.
- **Divide** when the planner says multi-session, a manager returns unfinished, an implementer left the smart zone (wrote `skilleddocs/HANDOFF.md`), or the not-done list won't fit one session. The planner proposes; you approve.
- **Failure**: one retry, fresh agent, tighter brief (pair: a new manager from its `skilleddocs/HANDOFF.md`). Second failure: split or park it with a reason, move on.
- **Stalled agent** (no progress for minutes): usually nested fan-out. Kill it, retry once with an inline-only brief.
- A guard-hook block on push/merge is the hook working. Never route around it.
- Never implement in your own context, merge unverified work, or silently narrow or widen an issue.
- Two-line update to the user at every merge and plan decision. `notify` → also send push notifications for those events. Keep going without asking permission to continue.

## 5. Ledger

`skilleddocs/orchestrator/ledger.md`, append-only, zone named once at the top. Commit and push each entry on default (`docs(skilleddocs): ledger NNN`) unless `docs_commit: uncommitted` (then exclude `skilleddocs/` per [TRACKING.md](../handoff-auto/TRACKING.md)).

```
### <NNN> · <local YYYY-MM-DD HH:MM ZZZ> · <plan|implement|merge|verify|decision|assumption|problem|manual|handoff|report>
- issue/PR: #n / PR #m
- what: one or two lines
- verified by: <test counts · CI run id>  (or "not verified: <why>")
- decided for you: Q → A, reason        (decision entries only)
- manual step for user: <only if one exists>
```

`ledger_detail: terse` → the header line + `what` only; `verbose` → add the commands run. Zone: scope `timezone` if set, else run `python -c "import datetime as d; n=d.datetime.now().astimezone(); z=n.tzname(); print(z if ' ' not in z else n.strftime('UTC%z'))"` once (abbreviation on Unix, UTC offset on Windows); name it at the top of the ledger. Times come from `date`, `git log --date=format-local`, or API UTC timestamps via `datetime.fromisoformat(s).astimezone()`; never estimated or offset by hand. Write `#n` / `PR #n` so `progress-report` can link them. Other `docs` entries: decisions → the decisions register (the one `AGENTS.md`/`CLAUDE.md` names; else `docs/decisions.md`; else an ADR folder; else `skilleddocs/decisions.md`, as `grill-docs`, incl. its precedence when several files name one); per-issue handoffs → keep the implementer's; CHANGELOG → one line per merge.

## 6. Rotation

At `handoff_budget` merges, or when your context is degrading → [ROTATION.md](ROTATION.md).

## 7. Done

Every in-scope issue closed or parked with a reason, or `stop` reached; default branch green; every merge (or `pr-only` PR) has a verify entry; ledger current; final report if `reports` says so. State plainly what was skipped and why.
