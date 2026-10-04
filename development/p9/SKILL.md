---
name: p9
tier: D
primitive: P9
category: orchestration
description: |
  Something is running and you are stuck waiting on it — CI checks on a PR you
  just pushed, a deploy going out, a container image build, a slow migration or
  a long reindex. This skill puts a watcher on the wait and spends the wait on
  the next piece of work, instead of watching a spinner or calling `sleep`. Also
  use it for a wait already in flight: "is the watcher running?", "did it
  notify?", "if I close my laptop does the wait just evaporate?", "I want my
  phone to buzz when it finishes or when it dies".
  Invoke it on the wait alone. You do NOT need the PR number, the URL, the
  branch, or the polling command first — locating the target is the skill's own
  first step, not a precondition for loading it. Asking the user which PR /
  which command / which watcher instead of invoking is the known failure mode
  here, and it is never the right move.
  Not for a wait nobody is waiting on any more — checks already landed, run
  already finished, PR already merged, a red result handed to you cold to
  debug. A failure your own watcher reported is NOT that; it is still this
  skill. And not for general advice about waiting — answer that directly.
when_to_use: |
  Triggers on "watch the checks", "watch the deploy", "waiting on CI", "while
  that runs", "let me know when it finishes", "notify me when", "buzz my
  phone", "is the watcher running", "did it notify", "don't make me watch a
  spinner", "productive wait", "p9" — and automatically after any `git push`
  that opens or updates a PR.
---

# P9 — Productive Wait (Wait-Optimizer Skill)

## Cardinal rule

> **Never `sleep` on a blocking wait.** Whether you're waiting on PR CI,
> a push-triggered deploy, a long build, or an index sync — convert the
> wait into productive work on the next priority. For PR CI, `p9 watch <pr>`
> spawns the observer in the background and the agent pulls work from the
> wait-queue. For non-PR waits, `p9 wait-for <name> --cmd '<predicate>'`
> gives the wait the same lifecycle (state row, heartbeat, termination
> report, re-arm). Sleep is a footgun — it burns clock time the agent could
> be using to validate definitions, refresh the knowledge graph, or draft
> the next slice.

## When to invoke

| Trigger | Action |
|---|---|
| `git push` opens or updates a PR | `p9 watch <pr> --background` immediately |
| `run_in_background` task notification fires for the watcher | `p9 status --pr <n>` to read terminal state |
| `gh pr checks` returned non-zero | `p9 heal <pr> --classify` to inspect failure |
| Push triggers a deploy / long non-PR operation | `p9 wait-for <name> --cmd '<predicate>' --detach` (or `--preset railway\|vercel`) |
| Fresh session picking up after a kill/crash/reboot | `p9 report` to read state + next action; `p9 rearm` to re-arm dead watchers |
| A watcher/wait looks wedged | `p9 stuck-scan` — structured dump + notification |
| About to `sleep` | **Don't.** Pull from `p9 wait-queue pop` instead |

## Parallel agent sessions (BRO-1529, BRO-2373)

P9 state lives in one shared dir (`~/.config/broomva/p9/`). Concurrent agents
stay collision-free by **scoping every record to a session id**.

**Isolation is on by default — no export required** (BRO-2373). `p9` resolves
its scope in this order:

| # | Source | When it applies |
|---|---|---|
| 1 | `BROOMVA_P9_SESSION` | explicit override, for a harness that knows its own scope better than p9 can infer it (`bstack wave` plans, tests) |
| 2 | a **composite over every harness marker present** — `CLAUDE_CODE_MESSAGING_SOCKET`, `ORCA_WORKTREE_ID`, `AGENT_SESSION_ID` — recomputed each call, **not** latched | automatic; the id is `<prefix>-<hash16>`, so `cc-…` / `orca-…` in `p9 status` names which harness answered first |
| 3 | persisted `session-default.id` | nothing derivable — one shared scope, the pre-BRO-2373 behavior |

Adding a harness is one row in `SESSION_MARKERS` (`p9.py`); a row that does not
actually isolate fails `test_every_declared_marker_isolates`.

> **Why this changed.** BRO-1529 built the scoping and required rung 1. A
> workspace-wide grep found `BROOMVA_P9_SESSION` set in *tests and nowhere
> else*, so every real agent landed on rung 3: **1364 of 3508** recorded
> events carried one shared id. The per-session ceiling was a global one, and
> two agents in one repo starved each other at `max_concurrent_prs: 1` on
> different PRs. The guarantee this section used to promise had never held.

### Why a composite, and why nothing is latched

**Composite, not first-present.** A marker *shared* by two agents would
otherwise mask a lower-priority marker that distinguishes them: two agents
under one Claude process but in different Orca worktrees both resolved to the
same `cc-*` id and starved each other. Composing is never *less*
discriminating — an identical marker set gives an identical id, and any
difference in any marker gives a different payload — hence a different id, up
to the 64-bit bound noted below.

**Identity is not latched, and that is deliberate.** A latch was built and
removed. Adopting an existing identity when the marker *set* changes is
non-transitive, so a subset latch bridges two sets that explicitly conflict:

```
A {cc:S, orca:W1}  -> latches id C
A {cc:S}           -> adopts C, records a SUBSET latch {cc:S}
B {cc:S, orca:W2}  -> rejects A's full latch (orca conflicts)
                      ...then adopts the SUBSET latch -> merges into A
```

The two requirements are irreconcilable, not merely hard: stability across a
changing marker set *requires* adopting on partial overlap, and distinctness
*requires* never adopting on partial overlap — a shared marker is exactly what
two concurrent agents have in common. Only an identifier present on **every**
invocation satisfies both, and p9 cannot mint one; the harness must issue it.
That is rung 1.

So the accepted failure mode is **fragmentation rather than merging** — barring
a 64-bit hash collision, and barring two agents whose marker sets are genuinely
identical, which no derivation can separate. An agent
whose environment is sanitized mid-session (`env -i` strips these markers)
changes identity and loses its queued work. That costs a ceiling slot and some
orphaned queue items; merging would cost isolation itself. Between an edge case
that over-isolates and one that under-isolates, only the first is safe.

**A harness that wants stability across a sanitized environment should set
`BROOMVA_P9_SESSION`** — rung 1 exists precisely for the case derivation
cannot serve.

**The git worktree is not itself a marker.** An agent that `cd`s between repos
— routine in this monorepo — would otherwise change identity mid-session.
`ORCA_WORKTREE_ID` already carries worktree identity where a harness exposes it.

**Marker values are never normalized.** Whitespace decides *presence*, never
*identity*: an earlier revision stripped values "to be forgiving" and merged
`'x'`, `' x '`, `'  x'` and `'x  '` into one scope. The composite is
length-prefixed per field, so a crafted value cannot forge a field boundary,
and values are encoded with `surrogateescape` so an undecodable POSIX byte
does not raise.

Known and **not** solved: two agents in one worktree under one process expose
an identical marker set and therefore share a scope. Derivation cannot separate
them — only rung 1 can. A recycled pid can likewise reproduce a prior session's
marker. The 64-bit id is a birthday bound, not an impossibility claim.

What the session id buys you:

| Dimension | Behavior |
|---|---|
| **Concurrency ceiling** | `max_concurrent_prs` is counted **per session**, and over the scope `ci_watch.max_concurrent_prs_scope` names (`repo`, the default, or `global`). A session's *own* second watch in the same scope still blocks. |
| **PR identity** | Keyed by `(repo, pr)` — the same PR number in two repos never collides, in the state table *and* in the ceiling count. |
| **Wait-queue** | `pop`/`list`/`clear` default to the **current session's** view (its items + legacy-unowned). `--all` crosses sessions. This is what "context-scoped" finally means in code. |
| **Watcher de-dup** | A second `p9 watch` on a PR that already has a **live** watcher is refused (`--force` to supersede). A **dead** watcher is superseded automatically once aged, or now via `--adopt`. |

### Repo identity (BRO-1988)

Every lifecycle command (`watch`, `merge-ready`, `merge-status`, `auto-merge`,
`abandon`) resolves the repo **once, before it reads state**, and uses that one
answer for both the read key and the write key. Resolution order:

1. `--repo OWNER/REPO`
2. `BROOMVA_P9_REPO` — the deterministic hook for tests and for harnesses that
   already know the target. `-` pins "no repo"; an **empty value means unset**
   (shell convention), so `export BROOMVA_P9_REPO=$(cmd_that_failed)` degrades
   to normal detection instead of silently dropping into repo-less state. A
   value that does not reduce to `OWNER/REPO` gets a stderr notice.
3. `gh repo view` → `git remote get-url origin` from cwd (memoized per process).
   The `git` fallback matters wherever `gh` is absent or unauthenticated (CI).

Any spelling normalizes to `owner/name` — `https://host/o/r.git`,
`git@host:o/r.git`, `ssh://git@host/o/r.git`, trailing slashes — and comparison
is case-insensitive, so one logical repo never splits into two keys. Host
parsing is generic, not a github.com allowlist: an allowlist made every repo on
a GHE/GitLab host collapse to a single key. The host is stripped rather than
keyed on, matching `gh --repo` (which takes a bare `OWNER/REPO` and gets its
host from `GH_HOST`).

**Ceiling scope** — `ci_watch.max_concurrent_prs_scope: repo | global`
(default `repo`). `repo` counts in-flight PRs per `(session, repo)`; `global`
is the pre-BRO-1988 cross-repo count — one bounded merge train across every
repo, which is what the design spec describes. `repo` is the default because a
global count let an in-flight PR in one repo refuse `p9 watch` in an unrelated
one, and since `watch` is the only transition into GREEN that made the whole
lifecycle unreachable there. The tradeoff is real and is why the knob exists:
at `max_concurrent_prs: 1` across N repos a session holds N watchers, and the
defer-into-wait-queue discipline stops firing cross-repo. Spec reconciliation
is tracked separately. With no resolvable repo the count falls back to global —
an ambiguous identity must not silently disable the ceiling.

**Rows with no recorded repo.** Rows written before repo stamping carry
`repo: ""`, and p9 does **not** migrate them.
It keeps that key: `""` is the row's true identity and a perfectly good one —
it collides with no real repo, so it can neither shadow one nor (under a
repo-scoped ceiling) hold its slot. `current_pr_state(pr, "")` still reaches
such a row, and `reap` / `rearm` still drain it. Nothing is discarded; p9
simply declines to invent the one thing it does not know.

Attributing them to the ambient repo was tried and reverted, because:

- it put a `gh repo view` call on every state read;
- it let `p9 rearm` re-watch the PR against the ambient repo — and omitting
  `--repo` from the child argv does **not** help, because the child calls
  `resolve_repo(None)` itself and, sharing cwd and env, resolves the same
  value. The observed chain ended in `gh pr merge` on a PR nobody targeted;
- and when the ambient repo genuinely had a PR of the same number, the guess
  *shadowed* the real row — recreating the exact defect BRO-1988 fixes.

So a row with no recorded repo is **folded and not re-armed**. There is no
correct repo to re-arm against; that is the whole content of "no repo
recorded". Folding frees the concurrency slot, and recovery is an explicit
`p9 watch <pr> --repo <owner/name> --adopt` — a human naming the repo p9
could not.

### Lifecycle / self-healing

- **`p9 reap`** — reconcile dead-watcher rows (pid gone) to `ABANDONED`,
  freeing the concurrency slot a crashed/closed session would otherwise hold
  forever. `--now` ignores the grace window; `--no-reconcile` skips the gh
  enrichment query. `watch` and `status` run a liveness-only reap as a cheap
  preflight, so the ceiling self-heals without manual `cleanup`.
- **`p9 watch <pr> --adopt`** — re-watch a PR whose prior watcher pid is gone
  (orphan recovery after a session ends mid-watch).
- **Queue TTL** — items are pruned once their PR reaches a terminal state, or
  after `BROOMVA_P9_QUEUE_TTL_DAYS` (default 14).
- **`p9 heal <pr> --apply`** — run the classified `heal_command` under
  `heal.lock` (serialized workspace-wide, so a heal in a parallel session can't
  race on shared codegen/cache). Auto-classifiable failures only; `--dry-run`
  prints the command. `--classify` stays read-only.

## Wait-time work selection (priority order)

When the watcher is running, drain work from these sources in priority order
(higher = pulled first):

1. **session** — TODOs already on the agent's TaskList tagged `wait_ok=true`.
2. **memory** — items from `~/.claude/.../memory/MEMORY.md` flagged "needs
   follow-up" within the last 24h.
3. **graph** — knowledge-graph entities adjacent to files-touched-in-PR
   (BFS depth 1 via `bookkeeping.py query`).
4. **docs** — cross-refs from the current PR's diff (mentioned files not
   yet updated).
5. **linear** — tickets in the current cycle, label-matched to PR's Linear ID.

### Isolation tier (per spec §5.5)

Each pop returns the inferred isolation tier:

| Work type | Tier | Where it happens |
|---|---|---|
| research, docs, knowledge-graph mutations, Linear updates | `none` | current worktree, no separate branch |
| code that's independent of the in-flight PR | `worktree` | new P5 worktree off main |
| code that depends on the in-flight PR | `stacked_branch` | branch off `feat/X+1` from `feat/X` HEAD |
| anything touching `CLAUDE.md` / `AGENTS.md` / `.control/` | `blocked` | **not** auto-handled; surface to user |

## Wakeup protocol

When the bg task notification fires:

```text
1. p9 status --pr <n> --json
2. parse `to_state`:
   - GREEN          → p9 merge-ready <n>; defer to control metalayer
   - RED_CLASSIFIED → p9 heal <n> --classify; if classified+evaluator-positive,
                      apply heal_command (in PR scope only); push amend; loop
   - RED_UNCLASSIFIED, ESCALATED → notify user via Linear ticket; stop healing,
                                    keep watcher alive in case human pushes a fix
   - ABANDONED      → surface failure to user; remove watcher; skip cleanup
```

### The watcher exit code is necessary-not-sufficient (BRO-1489)

`GREEN` only means `gh pr checks --watch` exited 0 — which it does on a *subset*
of checks (required-only) and *before* async bot reviews (CodeRabbit) settle.
Observed three times on bstack PR #78: exit 0 while the PR was `UNSTABLE` / had a
pending review.

`p9 merge-ready` therefore **verifies the real merge predicate** before marking
`MERGE_READY`: it queries `gh pr view --json mergeable,mergeStateStatus,reviewDecision`
plus a best-effort `gh api graphql` unresolved-thread count, and is ready iff
`mergeStateStatus ∈ {CLEAN, UNSTABLE}` with no `CHANGES_REQUESTED` and zero
unresolved review threads. `BLOCKED`/`DIRTY`/`BEHIND`/`DRAFT`/`UNKNOWN`, an open
thread, or any gh error → refused (fail-safe). Pass `--no-verify` to skip
(test/offline only).

Query it directly without transitioning state:

```text
p9 merge-status <n> [--json]   # exit 0 iff merge-ready; prints the verdict + reason
```

### Gated auto-merge: the gates decide, not the branch name (BRO-2591)

`p9 auto-merge <n>` merges a `MERGE_READY` PR under `.control/policy.yaml`
`auto_merge`. With a `gates:` block, **any branch** merges iff every gate passes.
Without one, the legacy prefix rules apply. Every gate is re-read from GitHub at
merge time, because the `MERGE_READY` row is history and `merge-ready
--no-verify` can write it. In legacy mode the merge predicate is re-read too.

**What the gates read.** The file listing is the paginated REST one. It
includes pre-rename paths: renaming `AGENTS.md` away keeps the PR governance-class.
Its row count must equal `changedFiles`, or the command refuses rather than judge
part of a diff. The listing, the gates and the merge must all describe one head,
or the run blocks. The merge is pinned with `--match-head-commit` to that head.
The base is pinned to one commit: the policy is read AT that commit, the
`up_to_date` gate compares against it, and it is re-read just before merging. A
moved base blocks, and so does a PR retargeted to another base in between.

| Gate | Passes iff | Unknown |
|---|---|---|
| `classifiable` | head/base read; file list not truncated | FAIL |
| `open` | `OPEN` and not draft | FAIL |
| `mergeable` | `MERGEABLE`, `mergeStateStatus ∈ {CLEAN, UNSTABLE, HAS_HOOKS}` | FAIL |
| `required_checks` | every required check `pass` (every run with that name), and at least one that is not a review bot | FAIL |
| `up_to_date` | 0 commits behind base, at a recorded base tip | FAIL |
| `no_changes_requested` | no reviewer's latest *opinionated* review is `CHANGES_REQUESTED`. A later COMMENTED review does not withdraw it; a later APPROVED or DISMISSED one does. (gh preloads every page of reviews and comments.) | FAIL |
| `threads_resolved` | 0 unresolved review threads (more than 100 threads block) | FAIL |
| `p20` | if over the P20 threshold, the latest verdict is a PASS ≥ `pass_score`, bound to the reviewed commit. Under the threshold no verdict is required, but once one is recorded it binds: the gate judges it as over the threshold, so a non-pass blocks and a PASS must cover the head. The threshold: >200 LOC, >1 file, an always-review path, a binary change (any row with 0 changed lines, including a rename: a pure rename cannot be told from a renamed binary without fetching both blobs), or governance-class. | FAIL |
| `independent_check` | a check that is neither a bot nor an aggregate (`Merge Gate`, which passes vacuously when nothing else ran) ran and passed, **or** a P20 pass covers the PR | FAIL |
| `governance_strata` | governance-class: the verdict lists strata A, B and C | FAIL |
| `governance_checks` | governance-class: every run of each required check (default `stability-check`) passed; skipped or absent fails | FAIL |
| `l3_rate` | governance-class: no governance change LANDED on base inside the τ_a₃ window (≥ 1 day). Each commit that reached base in the window (a merge, squash or rebase is dated when it landed) is diffed against its first parent, so an old-dated governance commit merged by a human still counts. | FAIL |

**Always-review paths.** These always need a P20 pass, whatever the change's
size: `.github/workflows/**`, `.githooks/**`, `.claude/**` (settings, local
settings, agents, commands, hooks), `.mcp.json` and `.control/preauth.yaml`. A `pull_request` run executes the PR's own workflow
files, so a one-line edit to the aggregate check would otherwise pass itself. A
policy's `p20.public_api_paths` adds to this list and cannot remove from it.

**Review bots never vouch.** A rate-limited CodeRabbit reports SUCCESS without
reviewing anything. A check or review from a `review_bots` login (or any
`*[bot]`) never counts as a required check and cannot record a verdict.
Configured bots, like configured aggregates, *extend* the built-in list.

**The P20 marker.** Record it with the helper, passing the commit the reviewers
**read**, not the head at record time. A nit fix pushed after the review is
unreviewed code:

```text
p9 p20-record <n> --sha <reviewed commit> --score 8 --strata B,C \
    [--verdict PASS|FAIL|STOP] [--note "..."]
# comment line 1:  P20-VERDICT: PASS score=8 strata=B,C sha=<reviewed commit>
```

Rules for reading markers:

- **First line only.** Only the first line of a comment is a marker, and `--note`
  may not contain `P20-VERDICT`, so a quoted ledger can never be read as the
  verdict.
- **Trusted authors only.** Only comments from `OWNER`/`MEMBER`/`COLLABORATOR`
  accounts that are not bots count.
- **The latest verdict wins.** A later FAIL cancels an earlier PASS. A trusted
  comment that names `P20-VERDICT` but whose first line does not parse (bold, a
  typo, prose) is a MALFORMED verdict and blocks. It does not leave the earlier
  PASS standing.
- **Carry-forward.** A verdict on an older commit still covers the head only
  when that commit is an ancestor of head and nothing since has touched a
  reviewed file or a current PR file. That is the case after updating the branch
  from base.
- **A recorded verdict binds at every size.** Under the P20 threshold no
  verdict is required, but once a PR carries a trusted, non-bot marker the gate
  judges it exactly as over the threshold. A latest FAIL, STOP, MALFORMED, or
  PASS below `pass_score` blocks, and later commits never clear it (a merge
  from base brings in files the PR never changed, so the file list cannot prove
  the reviewed code changed). A PASS clears it only if it covers the head, at
  head or by the carry-forward rule above, so a PASS recorded for another
  commit does not clear a FAIL on this one, and a stale PASS stops vouching once
  its reviewed code changes. Remedies: record a PASS ≥ `pass_score` for the
  head (`p9 p20-record`); a STOP goes to a person; a comment that only mentions
  `P20-VERDICT` (and so reads as MALFORMED) can be edited. Limit: markers are
  per PR, so a replacement PR from the same branch starts with none. Without
  this, a small PR whose review failed was one `gate-check` away from merging.

**Governance-class paths get a stricter gate, not a human click.** The
governance paths are `CLAUDE.md`, `AGENTS.md`, `METALAYER.md`,
`.control/policy.yaml` and `.control/rcs-parameters.toml`, repo-root and
case-folded. They carry L3, the level with the narrowest stability margin, so
the tier requires all three strata including a cross-vendor review, a
`stability-check` that actually ran, and the L3 rate budget, which CI only
reports. A governance change that cannot get a cross-vendor verdict (Codex
down) waits for one.

**The base branch's policy judges the PR.** p9 reads `.control/policy.yaml`
from the PR's base ref (URL-encoded), not from the checkout. Reading the
checkout let a PR be judged by its own policy edit. The fallbacks:

- **No policy file on base:** the local one applies, unless the PR is the one
  introducing it.
- **Base ref missing** (`No commit found for the ref`) or **an unreadable
  policy:** blocks.

The checkout's own `auto_merge.enabled` is a fail-closed pre-check. A checkout
that disables auto-merge, or cannot parse, refuses before the base is read, so
it can stop a merge but never enable one.

**No YAML can weaken a gate.** The parser rejects:

- an unknown key in the `auto_merge`, `gates`, `p20` or `governance` blocks, since a
  typo would otherwise run on the default;
- a flag that is not a real boolean, here and in `ci_watch`/`ci_heal`
  (`enabled: "false"` would otherwise read as true). A quoted value is a string
  in both YAML loaders, so both reject it. Unquoted spellings differ (PyYAML
  reads `yes`/`on` as true, the minimal loader reads `tRUE` as true), but each
  loader rejects what it does not read as a boolean, so neither weakens a gate.
  CI runs the minimal one;
- `pass_score < 7`, `max_loc > 200` or `max_files > 1`;
- governance `paths` or `required_checks` that drop an L3 path or
  `stability-check`;
- `required_strata` other than A, B and C;
- an L3 budget looser than one commit per day;
- `default_action: auto` alongside `gates`, because a p9 that predates gates
  reads only `default_action` and would merge everything ungated;
- `action: auto` rules alongside `gates`, where rules may only block. A path rule
  is a SUBSTRING match, not a glob (a `*` in it matches only a literal `*`);
  blocking path rules match case-folded, `auto` ones exactly.

`gates:` with no value means gated with the defaults, under both YAML loaders.

**What the gates do not do (named, not hidden).**

- **The marker is self-attested.** It records that a review passed and cannot
  prove the review ran. Replacing a human click with recorded reviews, a real
  stability check and the L3 budget was a deliberate decision (BRO-2591). The
  gate still fails on a PR with no pass, a low pass, or a pass on different code.
- **p9 binds the autonomous flow, not an adversarial caller.** Whoever controls
  the environment can set `BROOMVA_P9_POLICY` (an operator/test pin, honored
  as-is) or run `gh pr merge` directly. The server-side ruleset is the boundary
  against that. Pinning its aggregate check to the GitHub Actions app is the
  repo-side hardening for check-name spoofing.
- **A repo with no policy on base** (e.g. broomva/skills) is judged by the
  local walk-up policy, meaning the operator's workspace checkout.
- **Merge skew.** Between the base re-check and GitHub's merge there is a
  sub-second window. A base that moves inside it merges an untested
  combination, the same as a human click on a ruleset without "require up to
  date".
- **The L3 counter is check-then-merge.** Two governance merges in the same
  second could both see zero. It counts landings made through GitHub (merge,
  squash, rebase); a commit pushed straight to base with an old committer date
  is not listed (the workspace ruleset rejects direct pushes to main).
- **Check identity is by name**, as in GitHub's own required-check model. A
  different app posting a check under a real check's name counts as that
  check. Pinning required checks to an app in the ruleset is the repo-side fix.

```text
p9 gate-check <n> [--json]   # read-only: every gate PASS/FAIL + reason; exit 0 iff the decision is
                             # auto now (all gates pass AND no blocking rule matches);
                             # auto-merge also needs the PR in MERGE_READY
```

## Termination conditions

The agent exits the heal loop when **any** of:

- `to_state ∈ {MERGED, ESCALATED, ABANDONED}` (terminal)
- `attempt ≥ ci_heal.max_attempts` (default 5)
- evaluator returned `stalled=true` for two consecutive cycles
- user interrupt (Ctrl-C in terminal, or chat message)
- session ends (the `Stop` hook leaves watchers running for next session pickup)

## Examples

### Example 1 — Green on first try (happy path)

```bash
$ git push origin feat/my-change
$ gh pr create ... ; PR=42
$ p9 watch $PR --background
watcher_id=ab12cd34ef56 pid=78901 pr=42 repo=broomva/workspace

# Run watcher in foreground/background; meanwhile drain queue
$ p9 wait-queue pop
{"id": "...", "source": "graph", "item": "verify entities adjacent to ...", "isolation_tier": "none"}

# ... agent does the work ...

# bg task notification fires; check terminal state
$ p9 status --pr 42 --json
{"open_prs": [{"pr": 42, "to_state": "GREEN", ...}]}

$ p9 merge-ready 42
PR #42 marked MERGE_READY (control metalayer authorizes merge)

# the policy's gates authorize; p9 re-verifies them and merges
$ p9 auto-merge 42
```

### Example 2 — Lint-failure self-heal

```bash
$ p9 status --pr 42 --json
{"open_prs": [{"pr": 42, "to_state": "RED_CLASSIFIED", "attempt": 0}]}

$ p9 heal 42 --classify
{"failure_type": "lint", "classified": true, "confidence": 0.8, "heal_command": "bun run lint:fix", "rationale": "matched lint at confidence 0.80"}

# agent runs heal_command, scoped to PR diff files
$ bun run lint:fix
$ git commit -am "fix(lint): heal CI"
$ git push --force-with-lease   # only if existing P6 policy permits
$ p9 watch 42 --background       # new WATCHING cycle; attempt=1
```

### Example 3 — Unclassified-failure escalation

```bash
$ p9 heal 42 --classify
{"failure_type": "unclassified", "classified": false, "confidence": 0.0, "heal_command": null, "rationale": "no rubric pattern matched"}

# Agent does NOT attempt to heal. Creates a Linear ticket via MCP:
#   title: "[P9 ESCALATION] PR #42: feat/my-change"
#   body:  failure signature + log excerpt
#   label: ci-heal-escalation
# Watcher stays running — if a human pushes a fix, watcher resumes and
# the next green check transitions to MERGE_READY.
```

## Background-work visibility (BRO-1701)

### Termination invariant (hard rule)

> **On watcher termination — success, failure, OR kill — P9 always reports
> state + next action.** Killed watchers must not die silently.

Every exit path of `p9 watch` and `p9 wait-for` (green, red, timeout,
SIGTERM/SIGINT/SIGHUP, unexpected exception) folds a state event, prints a
`P9-TERMINATION-REPORT {json}` line to **stderr** (stdout stays
machine-parseable), and pushes through the notify channels. The report
carries `state`, `cause`, and a concrete `next_action` (e.g. ABANDONED →
"re-arm: p9 watch <pr> --adopt"). SIGKILL and machine death can't be
trapped — that path is covered by `p9 reap` (emits the same report shape
when it reconciles a dead row) and `p9 rearm`.

Read-side: `p9 report [--pr <n>] [--json]` renders the latest report for
every tracked watcher/wait — this is what a fresh session (or the Tier-1 #1
post-notification reconcile rule) consumes to learn what happened and what
to do next. Report fields are additive-only.

`gh pr checks --watch` output now lands in `$P9_HOME/logs/watch-<id>.log`
(not the void): the log's mtime is a progress signal for `stuck-scan` and
its tail rides along in reports — full details to understand *why*, not
just *that*, something died.

### Notify channels (push-to-phone)

`p9 notify <title> [--body ...]` and every termination/stuck event fan out
to channels in `$P9_HOME/notify.json`:

```json
{"channels": [
  {"type": "ntfy",    "topic": "broomva-p9", "url": "https://ntfy.sh"},
  {"type": "webhook", "url": "https://example.com/hook"},
  {"type": "command", "cmd": "scripts/p9-escalate-notify.sh"}
]}
```

- **ntfy** — reaches a phone with zero infra (install the ntfy app,
  subscribe to the topic). Quick-config without a file:
  `export BROOMVA_P9_NTFY_TOPIC=<topic>`.
- **webhook** — generic JSON POST (`{title, body, payload}`).
- **command** — JSON on stdin to any hook script; this is the seam for
  Omnara, Telegram, Discord, or claude-remote-sessions relays.
- Escalation-class events (`termination:escalated`, `stuck`, and any kind
  containing `escalat`) additionally fire the policy's
  `ci_heal.escalation_channel.notify_hook` (previously dead config — now
  invoked).

Delivery is best-effort and per-channel isolated: a failing channel is
recorded and skipped, never raised — a notification must never take down
the watcher it reports on. Every attempt (even with zero channels) appends
an audit row to `$P9_HOME/notify.jsonl`; that audit floor is what makes the
termination invariant verifiable after the fact.

**In-session protocol (PushNotification/Omnara):** when an agent session
receives a termination report or stuck dump while the user is off-terminal,
it MUST surface it through the harness `PushNotification` tool (or the
Omnara session surface) — the file-level channels cover the no-session
case; the harness tool covers the live-session case.

### Non-PR waits — `p9 wait-for`

```bash
p9 wait-for railway-deploy --preset railway --interval 30 --timeout 1800 --detach
p9 wait-for vercel-deploy  --preset vercel --target <deployment-url> --detach
p9 wait-for extraction     --cmd 'test -f /tmp/extract.done' --interval 60 --timeout 7200 --detach
```

Polls the predicate command until exit 0 (`SUCCEEDED`), deadline
(`TIMED_OUT`), first-poll exit 126/127 (`FAILED` fast), or signal
(`KILLED`) — each terminal state folds + reports + notifies exactly like a
PR watch. State lives in `$P9_HOME/waits.jsonl` (its own stream — PR-state
consumers never see wait states); every poll touches a heartbeat file that
`stuck-scan` reads. Presets are convenience templates over `--cmd` —
deploy-CLI output shapes drift, so verify against your installed CLI and
fall back to an explicit `--cmd` when they do.

### Re-arm after kill — `p9 rearm`

`p9 rearm [--dry-run] [--now]` scans for dead-but-unfinished work: PR rows
whose watcher pid is gone re-enter via a detached `p9 watch --adopt`; dead
waits are folded ABANDONED and re-spawned from their recorded argv (with
`rearmed_from` lineage). This closes the loop the July-1 leverage audit
flagged: watchers killed before their notification fires now leave a
report AND come back.

### Stuck-detector — `p9 stuck-scan`

`p9 stuck-scan [--threshold-min N] [--json]` flags **live** watchers/waits
with no progress (state event / watch-log mtime / heartbeat) inside the
threshold (default 45 min, env `BROOMVA_P9_STUCK_MIN`): structured failure
dump (pid, ages, log tail, next action) + notification, deduped to one per
stall episode (`--renotify` overrides; a new episode starts when progress
moves). Dead pids are reap/rearm territory, not stuck. Exit code 1 when
anything is stuck — wire it into cron/governor loops as a cheap probe.

## Cardinal invariant (hard rule)

> **P9 never silently drops state.** Every failure produces (a) a
> `state.jsonl` event, (b) a Linear ticket, or (c) both. If P9 cannot
> write to `state.jsonl` AND cannot reach Linear, it crashes loudly
> (exit 99) — degraded silent operation is forbidden.

## See also

- Spec: `docs/superpowers/specs/2026-05-04-p9-ci-watcher-design.md`
- Rubric: `references/scoring-rubric.md`
- CLI: `scripts/p9.py` (run `python3 scripts/p9.py --help`)
- Related primitives: P1 (Conversation Bridge), P2 (Control Gate),
  P3 (Linear Tickets), P4 (PR Pipeline), P5 (Parallel Agents),
  P6 (Knowledge Bookkeeping), P8 (Branch + Worktree Janitor),
  P10 (Worktree Hygiene Discipline), P11 (Empirical Feedback Loop).
