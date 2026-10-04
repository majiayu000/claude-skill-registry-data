---
name: quick-wrap
description: "Short session close: commit, loose ends, stop. Not workstream-complete."
version: 1.0.0
allowed-tools: ["Read", "Edit", "Bash", "Grep", "Glob", "Skill"]
argument-hint: "[optional context]"
---

# Quick Wrap — the Light End-of-Work Close

<!-- Purpose: names and discharges "commit-and-stop". -->
<!-- Negative-spec: NOT a cheaper workstream-complete. Writes no completion entry, reconciles no
     plan, opens no review trail, terminates no handoff chain with ancestors. A lesson does NOT
     disqualify. -->

The short checklist for a session whose work is finished, small, and unremarkable. The entry test
is a positive gate: fail one of the four and this is not the room — route to the named remedy, no
negotiating. Every computable condition names a single field read
— never a procedure the EM runs and interprets.

---

## Entry test — ALL four must hold

| # | Condition | Read | If it fails |
|---|---|---|---|
| 1 | **No governing plan** drove this session's work † | `close_gate.governing_plan` — `quick-wrap-assemble brief` | `/workstream-complete` |
| 2 | **Diff under the review brightline** — <500 novel LOC, <5 commits, <4 surfaces | `close_gate.diff` (session-scoped, carve-outs pre-applied) — `quick-wrap-assemble brief` | **Scoped review, then wrap** (below), not `/workstream-complete` |
| 3 | **What this session claimed has no ancestors** ‡ | `artifact.chain.ancestor_count == 0` — `pickup-assemble brief <path>` for the artifact this session claimed; nothing claimed means nothing to read, test passes | `/workstream-complete` — a chain that accumulated history owes a coverage gate |
| 4 | **Work is finished** — nothing in-flight for a successor | judgment | `/handoff`, only if context pressure genuinely forces the stop |

**† `spec-dispatch`.** `close_gate.governing_plan.scope_mode == "spec-dispatch"` passes test 1 as a
deferred obligation, conditional on step 2's reconciliation micro-step running and step 4 reporting
it. `dispatch`-routed sessions carry `governing_plan.present: false` and pass as before.

**‡ A pickup is not itself the disqualifier — ancestry is.** A chain-root baton (`predecessor:`
`none`/null, no `additional_predecessors`, no `forked_from`) carries no prior session's scope to
account for, so claiming one and finishing it leaves no coverage gate owed. Until
`artifact.ancestry` lands, read those three frontmatter fields off the same brief. It closes here:
step 2 stamps its terminal disposition.

`close_gate.diff` already excludes relocated-without-modification lines and doc-only lines —
engine-applied, not an EM procedure. Report gross and novel counts in step 4 when the carve-out is
what drops the session under the line.

### The named routes past test 2

Test 2 failing means a review is owed, not that this ceremony is wrong. Two routes exist; the
first is the default and the second requires a named class member.

**1. Scoped review, then wrap (the default).** (1) register the reviewed file list with
`review-findings-ledger targets --add`, then dispatch a reviewer scoped to the risk surface —
`Skill(coordinator:review-code)` diff-shaped, or a direct `coordinator:code-reviewer` when scope
is narrow; (2) the reviewer applies and verifies its own ledger, applied never ratified back as a
list; (3) run the checklist below, verdict in step 4.

> **Do not ask whether to dispatch** — invoking this skill IS the request for the dispatch this
> step names; it dissolves no gate this skill's own body names.

**2. Successor-runs-review handoff — only when the owed review is genuinely un-runnable in this
session.** The class member that fires must be named per `coordinator/skills/handoff/SKILL.md`
§ Step 0 trigger 4; that trigger's own discharge (name the blocker and the event that clears it
in the successor's remit) governs, not a local restatement here. This route terminates in
`/handoff`, never in `/execute-plan`'s Phase-5 halt (`coordinator/skills/execute-plan/SKILL.md`
§ Phase 5 — that halt is native to that skill, evidence-gated to scope-explosion, and does not
itself terminate). Route 1 stays the default: reach for route 2 only when a named class member
actually fires, never as a lighter-weight substitute for dispatching a reviewer.

**Unlocks nothing else** — test 1, 3, or 4 failing still routes to its named sibling regardless
of review outcome.

**A lesson is not a disqualifier** — capture through the `lesson` CLI, then wrap.

- **Branch ready to ship** → `/merging-to-main`. Quick-wrap ends a session, never a branch.
- **End of the working day** → `/workday-complete`, which supersedes this; never run both.

**Mutual exclusion.** `/quick-wrap`, `/workstream-complete`, and `/handoff` are exclusive — one
session, one closing ceremony. Two genuinely different workstreams close separately, named which.

---

## The checklist

Four steps. Longer than a few minutes means the entry test was wrong.

**1. Commit.** Run the safe-commit mechanism — it computes this session's safe pathspec from its
touch-list (minus anything a live peer also claims) and commits — publishing is the separate
cadence checkpoint below, not part of this call:

<!-- VERBATIM -->
On a PowerShell host, invoke the `coordinator-invoke.exe` door by absolute path through the call
operator (Shape W, `${CLAUDE_PLUGIN_ROOT}/snippets/resolve-coordinator-bin.md` § The door):

`& "$env:COORDINATOR_SETTINGS_HOME\bin\coordinator-invoke.exe" session.safe_commit_offer '{"cwd":"<repo-root>","session_id":"<this session's id>"}'`

POSIX-host form (Shape A/B) dials the same op through the bare `coordinator-invoke` door.

**Pass `session_id` explicitly — the op refuses without it.** Scope is "none", so identity is
never taken from the environment, and `cwd` does not supply it either: `cwd` selects which tree is
scanned, nothing more. With no explicit `params.session_id` and no carried identity on the wire the
op returns `caller identity could not be established`, rather than falling back to the environment
of whoever spawned the warm server and committing one session's paths under another's claim. Both
params are required in practice: `cwd` for the tree, `session_id` for the identity.

**Payload is one positional JSON string, not `k=v`** — `cwd=<repo> message="<subject>"` does not
parse. **Never pass `--repo`**: this op is scope "none" and refuses it (`-32603`). Add `"dry_run": true` to preview; omit it to commit.

**Do not ask whether to commit** — being asked was itself the defect, by explicit PM ruling. Run
it, report what the op's `rendered` field says landed. `"message": "<subject>"` for one group, the
`groups` param (inline list of `{"paths": [...], "message": "..."}` objects) for several — mutually
exclusive with `message`. A path outside the computed safe pathspec is silently dropped, never
caller-widened.

**2. Close loose ends.** The judgment step — sweep what this session actually touched:

- A **queue entry** resolved this session: closure is a move, never in-place — `git mv state/<queue>/<slug>.yaml archive/<queue>/<YYYY-MM>/<slug>.yaml`, set
  `status: closed`, `closed_at:`, `closed_by:`.
- An **inbound cross-repo memo** actioned this session → resolve it.
- **A residual surfaced but not closed**, recorded only in prose: file via
  `coordinator-queue-append --schema bug-backlog|debt-backlog|improvement-queue` — naming it
  in step 4 alone is dumping it.
- A `scope_mode: spec-dispatch` plan authored/executed this session: tick ACs, set `plan-tasks`
  dispositions; a met terminal judge stamps `status: implemented` inside `terminal_commit`
  ([terminal-judge](../../docs/wiki/reviewer-pipeline/terminal-judge.md)); verify, never restamp. Where it did not stamp, the `d-stamp-plan-implemented` directive owns it.
  `A-PLAN-SELF-COMPLETES-ONLY-ON-A-MET-TERMINAL-JUDGE`.
  `[[the-deliverable-cascade-has-never-written-a-terminal-status]]`
- A plan this session executed whose `exit_criterion_met` is absent blocks the close — no
  directive can compute this. `asserted: false` is a legitimate, first-class outcome and does not
  block; it routes to `/handoff` or a Phase-5 halt instead (`coordinator/skills/execute-plan/SKILL.md`
  § Phase 5).
- **The chain-root baton this session claimed and finished** (the only kind test 3 admits): stamp
  `deployment_state: shipped` + `shipped_in: <this session's commit>`; `status` stays `claimed`
  (the schema enum admits only `open`/`claimed`). Same first-hand-observer ground as the
  `dispatch`-routed sizing below — the session that did the work observes its own completion.
  Leaving it unstamped strands a claim no successor will ever release, and
  `sweep-terminal-handoffs` never archives it — it classifies an unstamped record `not-terminal`
  and walks past. Nothing downstream catches this: there is no boot-time sweep behind it. Both
  keys, or the baton sits in `state/handoffs/` indefinitely and every roadmap that counts it reads
  behind its real state. The stamp makes it archivable; the drain below is what files it.
- **A `dispatch`-routed sizing that routed this session**, work done: write `status: shipped`
  directly — no plan means this is its only write path.
- **Every terminal sizing-object** (`shipped`/`declined`/`superseded`), cited or not:
  `close_gate.terminal_sizings`
  archive with `coordinator-invoke fleet.archive_terminal_sizings '{"dry_run":false}'` — it moves
  each to `archive/sizings/<YYYY-MM>/` unmodified and commits the move itself, so a sizing this
  session did not author still lands (a hand `git mv` is refused by `safe_commit_offer` as
  unattributable). No `closed_at`/`closed_by` (schema disallows both). A record still at `sized`, `routed`, or `draft` is untouched no matter how
  finished it looks — only what a prior step already marked terminal moves.
  **A citation does NOT pin a record in place, and archiving a cited one does not dangle.**
  `plan.schema.json` does constrain `sizing_object` to `^state/sizings/.+\.yaml$` and the plan is
  never repointed — but the FK is archive-agnostic by design:
  `coordinator_core/ops/_sizing_citation.py::resolve_sizing_citation` resolves live-then-archive,
  probing `archive/sizings/**` by basename, and both consumers call it
  (`assert_plan_sizing_citation`, `dispatch_emit/emit.py`). A value resolving only under `archive/`
  is correct, not broken — the sizings sibling of the existing handoff FK fallback. So archive
  every terminal record; `close_gate.terminal_sizings` filters on status alone, which is correct as
  built rather than a producer gap.
- `coordinator-fold-execution-record` sidecars this session produced — a diverged sidecar's prose
  is already in the envelope (judgment point `j-diverged-sidecars`; a failed scan surfaces as
  `j-diverged-sidecars-degraded`), so settle that point, then delete. Never open sidecars to read.

**Then drain — MANDATORY, and the last act of this step.** Run `sweep-terminal-handoffs` once,
after every stamp above is written. A record stamped archivable and left in `state/handoffs/` is an
unfinished close, not a tidy-up for the next ceremony: until it moves, every surface that counts open
batons reads it as *unstarted*, and the `/workday-complete` backstop may be weeks out. **The close
condition is checkable and you check it: `state/handoffs/` holds no record carrying a terminal
`deployment_state` when you report.** The drain is idempotent and a sub-second no-op when there is
nothing to move, so nothing justifies skipping it; it drains other sessions' terminal residue in the
same pass, which is the point, not overreach.
`[[terminal-batons-are-swept-at-close-not-left-to-the-next-ceremony]]`

Nothing to close is an ordinary outcome — say so and move on. **The drain is not covered by that
sentence:** it runs whether or not this session had anything of its own to close.

**3. Refresh.** `regenerate-orientation-cache --invoker quick-wrap` — batch into the same shell call as step 1's
`session.safe_commit_offer` dial when step 2 needed no separate CLI invocation of its own (no
dirty-tree/queue CLI ran between them); keep it a separate call only when step 2 actually ran one.

**4. Report.** Three lines: what landed (commit SHA), what you closed, what's deliberately open.
Five for `scope_mode: spec-dispatch`: add the `code-reviewer` verdict + ledger verified + one
commit, and that the plan-reconciliation micro-step ran. Then stop.

---

## Anti-scope

- **Never deletes, force-pushes, or rewrites history.** No `reset --hard`, `checkout --` over
  another's hunk, branch deletion, rebase. Authorized: a scoped forward commit, a `git mv` of a
  queue entry or terminal sizing-object into archive, this session's own terminal-status write —
  on a sizing-object, or on the chain-root baton it claimed itself. **Never on a baton with
  ancestors** — that chain's termination belongs to `/workstream-complete`.
- **Writes no continuity artifact** — no handoff, spinoff, completion entry; the entry test
  already routed you elsewhere if one was owed.
- **Captures no lesson itself** — via the `lesson` CLI, then wrap.
- **Runs no test suite.** `Skill(coordinator:validate)` is deliberately gone from step 1 — the
  "fast" tier is neither fast nor cheap, and paying for it at every light close was the defect. Do
  not re-add it or hand-roll `pytest`. Report evidence already produced as-is; a suite already
  known red fails the entry test.
- **Opens no review trail of its own.** Above the test-2 brightline, the scoped-review route runs
  *before* this checklist and never substitutes for the partitioned review a plan-driven or
  predecessor-consuming session owes — except `scope_mode: spec-dispatch`, discharged upstream.
- **Never closes a queue entry this session didn't resolve** — closing on a hunch is worse than
  leaving it open.
- **Does not supersede the PM's closure authority.** Closing a *workstream* is the PM's call; this
  closes a *session* — never emits a "Session Complete" header.

## Discovery, test surface, see also

Surfaced at `/workday-start`; named in `/handoff`'s Step 0 NO-tests as the "shipped, not
handed-off" destination. No runtime test for the body — prose doctrine, not code; checks are
skill-body lint and frontmatter validation. The entry test is a table so drift stays greppable.

- `skills/workstream-complete/SKILL.md` — the heavy close, for a test 1/3/4 failure.
- `skills/handoff/SKILL.md` — its Step 0 redirects here.
- `commands/workday-complete.md` — supersedes this one.
