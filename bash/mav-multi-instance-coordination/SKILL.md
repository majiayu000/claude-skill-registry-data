---
name: mav-multi-instance-coordination
description: Claim, lease, heartbeat, and release protocols for when multiple Claude Code instances may act on the same issue or epic concurrently. GitHub labels and marker comments are the coordination surface; local state is a cache.
user-invocable: false
disable-model-invocation: true
---

# Multi-Instance Coordination

Several Claude Code instances, on different machines, may be asked to act on
the same issue or epic at the same time. This skill defines how they
coordinate so that:

- Two instances never silently step on the same story.
- A machine dying without notice is detected within ~10 minutes.
- No committed work is lost on takeover.

All coordination state is **on GitHub**. The local filesystem is a cache.

## Entry check — before any work

Every workflow entry point must run the entry check before touching an
issue. The CLI helper `uv run maverick coord read <repo> <issue>` returns
a JSON snapshot; parse it and decide:

```dot
digraph entry {
    "Read claim state" [shape=box];
    "blocked-by:#N label?" [shape=diamond];
    "Abort — report block to user" [shape=box];
    "claude-in-progress label?" [shape=diamond];
    "lease live?" [shape=diamond];
    "Abort — report holder + expiry" [shape=box];
    "Stale lease — takeover or defer" [shape=diamond];
    "Claim scope" [shape=box];
    "Claim" [shape=box];

    "Read claim state" -> "blocked-by:#N label?";
    "blocked-by:#N label?" -> "Abort — report block to user" [label="yes"];
    "blocked-by:#N label?" -> "claude-in-progress label?" [label="no"];
    "claude-in-progress label?" -> "lease live?" [label="yes"];
    "claude-in-progress label?" -> "Claim scope" [label="no"];
    "lease live?" -> "Abort — report holder + expiry" [label="yes"];
    "lease live?" -> "Stale lease — takeover or defer" [label="no"];
    "Stale lease — takeover or defer" -> "Claim" [label="take over"];
    "Claim scope" -> "Claim";
}
```

### The four exit points

| Exit | When | Action |
| --- | --- | --- |
| Blocked | `blocked-by:#N` label present | Report to user; do not claim, do not modify issue |
| Claimed with live lease | Another instance is active | Report holder id and expiry; do not modify issue |
| Claimed with stale lease | Holder likely crashed | Decide: take over now, or defer |
| Free | No claim or stale/absent lease | Claim and proceed |

## Claim scope

Decide the breadth of the claim before calling `coord claim`:

- **Whole epic** — one instance owns the epic and every child story. Use
  when you intend to run `do-epic` end-to-end.
- **Group of stories** — typically one wave from the epic DAG. Use when a
  separate instance is already working on a different wave.
- **Single story** — use when coming in from `do-issue-solo` for ad-hoc
  single-issue work.

The chosen scope is recorded in the `maverick-claim` payload so other
instances reading the marker can see exactly what you own.

## Atomic claim

Run `uv run maverick coord claim <repo> <issue>`. The behavioural
contract is all you need: **exit 0 means you own the claim; non-zero
means you do not — abort cleanly without modifying the issue.** Race
detection, tie-breaking, and label/marker/lease mechanics live inside the
CLI (see `docs/conventions/github-markers.md` for internals); never
re-implement or second-guess them.

## Heartbeat

Once claimed, refresh the lease every ~2 minutes:

```bash
uv run maverick coord heartbeat <repo> <issue>
```

The refresh pushes `expires_at` forward by 10 minutes. If two consecutive
heartbeats fail (network flake, transient GitHub error), do **not** keep
working on the assumption you still own the claim — abort and release.

Heartbeat may also raise `ClaimLost` if:

- The `claude-in-progress` label has been removed (another instance took
  over, or a human resolved the claim manually).
- The `maverick-claim` marker now names a different instance.

On `ClaimLost`: stop work immediately, do not push, do not comment
further. Clean up local worktree state and report to the user.

## Release

On completion, eject, or any clean exit:

```bash
uv run maverick coord release <repo> <issue> --reason merged
uv run maverick coord release <repo> <issue> --reason ejected
uv run maverick coord release <repo> <issue> --reason abort
```

This removes the label, writes a lease-released marker, and unassigns the
GitHub App. Always release on every exit path. If an instance dies before
release, the lease expires in ~10 minutes and another instance can take
over.

## Takeover

If you find a claim with a stale lease (holder's last heartbeat > TTL ago),
decide before acting:

- **Take over now** when the work is high priority and the holder's
  crash is obvious (lease expired hours ago, host unresponsive to ping).
- **Defer** when the work can wait — avoids stepping on a holder that's
  merely suspended (laptop asleep, debugging under breakpoint).

To take over:

```bash
uv run maverick coord takeover <repo> <issue>
```

This posts a takeover comment naming the prior instance and then runs
claim with takeover permission. The prior instance's heartbeat will fail
on its next attempt with `ClaimLost`.

## Release on exit

Releases happen at three layers; entry-point skills rely on them instead
of inventing exit handlers:

1. **Explicit** — the skill runs `coord release --reason <merged|ejected|…>`
   at its own workflow boundaries. This is the normal path and produces
   the audit-trail reason.
2. **SessionEnd hook** — the plugin runs `coord release-all` when the
   session ends for any reason (done, user interrupt, crash-caught),
   releasing every claim this instance recorded locally.
3. **Lease expiry** — the 10-minute TTL is the designed crash path for
   machine death; another instance takes over cleanly via `coord takeover`.

Do **not** attempt trap-on-exit wrappers: each Bash tool call is a fresh
shell, so a trap can never survive to session end — the pattern only
produces false confidence.

## Rules

- **Never skip the entry check.** Even if you "know" the issue is free,
  the GitHub state may have changed since you last looked.
- **Never extend a lease past TTL silently.** If two heartbeats fail,
  treat the claim as lost — do not assume you still hold it.
- **Never release another instance's claim.** If you're not the holder,
  you cannot remove the label or write a release marker for them.
  (Takeover is the exception, and it posts its own takeover marker.)
- **Lower instance-id wins ties.** Document this in every race-detection
  branch so two instances produce the same decision independently.
- **Always scope claims to the smallest sensible unit.** Claiming an
  entire epic when you only intend to work on one wave blocks other
  instances unnecessarily.

<!-- maverick-plugin-version: 4.0.2-dev -->
