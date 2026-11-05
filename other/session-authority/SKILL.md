---
name: session-authority
description: Use before starting real work in a git checkout this repo's Session Authority can't reach automatically (a cloud session, which never runs worktree-setup.ps1) — acquire a lease so a concurrent session can't silently collide with your uncommitted work, and release it cleanly when you finish. On a Windows bridge session, worktree-setup.ps1/worktree-teardown.ps1 already do this for you; this skill is the manual fallback for the one path nothing mechanically wires.
triggers: lease, acquire a lease, release the lease, cloud session, git checkout, concurrent session, uncommitted work, session authority, worktree-setup, collide, abandoned branch
---

# Session Authority

Built 2026-09-23 after an audit found 13 branches abandoned mid-task by
different sessions sharing this repo's checkouts — 8 of them piled onto
one branch (`statenour/hard-delete-guard-wiring`), 9 onto another
(`nickstire/dua-concept-engine`), with no technical guarantee that any
one session's uncommitted work wouldn't be stomped by another's
`git checkout`/reset on the same branch. `AGENTS.md` already warned about
this ("Concurrent sessions share this checkout... a sibling's work may be
in your tree") but only as a procedural rule, not an enforced one.

## What it actually is

A git-ref compare-and-swap, not a database or a service: a lease record
lives at `refs/leases/<branch>`, updated via `PATCH /git/refs/{ref}` with
`force:false` — GitHub rejects the update unless the new commit is a
fast-forward of the ref's current tip, which is what makes two racing
acquires resolve to exactly one winner. This is the one mechanism
reachable from both a Windows bridge session (shared local checkout) and
an ephemeral cloud container (fresh clone, no shared filesystem with
anything) — the reason it lives on GitHub, not on disk.

## When you need to run this yourself

`worktree-setup.ps1` and `worktree-teardown.ps1` already call
`agent-start.mjs`/`agent-finish.mjs` automatically — on a Windows bridge
session working through those scripts, you don't need this skill at all.

You need it when your session's checkout was **not** created by those
scripts — which today means every cloud session, since a cloud container
gets a fresh clone through a different mechanism entirely and never
touches the worktree scripts.

## Acquiring

```bash
node scripts/agent-os/agent-start.mjs --claimed-by "one-line task summary"
```

Branch and worktree default to the current checkout. Three outcomes:

- **Acquired** — exit 0, prints the lease's expiry (12h TTL, no renewal).
- **REFUSED, exit 1** — another session holds an active, unexpired lease
  on this exact branch. The message names who, since when, and for what.
  **Stop and confirm with the operator before proceeding** — this is
  exactly the collision the whole system exists to prevent.
- **Failed open, exit 0, loud warning** — the lease service itself was
  unreachable (no token, network, GitHub down). Proceed, but know the
  guarantee didn't actually apply this time.

## Releasing

```bash
node scripts/agent-os/agent-finish.mjs
```

Refuses (exit 1) if the worktree is dirty or has unpushed commits —
commit and push first. If you genuinely mean to abandon local work
(rare, and worth saying out loud to the operator first):

```bash
node scripts/agent-os/agent-finish.mjs --force-release-dirty "why"
```

The reason is written permanently into the release record.

Only the session that holds a live lease can release it. If the holder is
gone (its container was reclaimed, its lease is still live), confirm with the
operator, then:

```bash
node scripts/agent-os/agent-finish.mjs --force-release-foreign "why"
```

The reason and your session id are recorded permanently. This is also the
way out when `lease-check.mjs` blocks every call because this worktree holds
another session's live marker: that one command, run on its own (no `;`,
`&&`, pipe or subshell), is let through. An operator can instead set
`AGENT_OS_LEASE_OVERRIDE="why"` for the session, which turns the block into
a warning that repeats the reason.

## What this does NOT do

It does not know whether your local working tree is dirty from any
machine but the one you run it on — there is no cross-machine visibility
into file contents, only into who currently claims the branch. It is not
a security boundary; a session that skips `agent-start.mjs` entirely
just doesn't get the collision warning, the same trust model this
repo's `pretool.mjs` already uses for its own hooks.

## Related

`repo:status` (`scripts/agent-os/repo-status.mjs`) shows every local
worktree's lease state next to its dirty/unpushed/origin state in one
table. `repo:rescue` and `branch-sweep` build on the same evidence for
landing or classifying abandoned branches — see
`docs/agent-os/2026-09-23-branch-rescue-runbook.md` for the one-time
cleanup that motivated this build, and `docs/agent-os/BRANCH-SWEEP.md`
for the standing, weekly-refreshed ledger.
