---
name: gz-obpi-lock
persona: main-session
description: Use to claim, release or list OBPI work locks.
category: obpi-pipeline
lifecycle_state: active
owner: gzkit-governance
last_reviewed: 2026-10-17
metadata:
  skill-version: "6.4.1"
model: haiku
---

# gz-obpi-lock

Claim or release OBPI-level work locks for multi-agent coordination.

### Common Rationalizations

These thoughts mean STOP — you are about to bypass coordination:

| Thought | Reality |
|---------|---------|
| "No one else is working on this, I don't need to lock" | You do not know what other agents are doing. The lock is coordination, not permission. |
| "I'll just do a quick fix, no need for a lock" | Quick fixes that conflict with another agent's work create merge conflicts. Lock first, always. |
| "The lock expired, so I'll just re-claim it" | An expired lock may mean another agent started work. Check status before re-claiming. |
| "I'll release the lock manually later" | `gz obpi complete` surrenders it at Stage 5. Manual release outside the pipeline risks orphaned work. |
| "Lock conflicts slow me down" | Merge conflict resolution after concurrent edits is far slower than waiting for a lock. |

### Red Flags

- Multiple agents editing the same ADR's files without lock coordination
- Lock file exists but agent proceeds without checking it
- Pipeline completes but lock is never released (orphaned lock)
- Agent force-releases another agent's lock without investigating
- Work begins on an OBPI without any `gz obpi lock claim` in the session

---

## Three subjects (operator ruling, verbatim canon)

Keep three subjects distinct: transit is ecosystem movement through the airlock (ADR-0.33.0); exchange is one block’s occupancy (ADR-0.0.41); handoff is session memory (ADR-0.0.65). Classify by the citing event type, never a shared field name or path. Token blocks implement features through the airlock’s Build door. The airlock provides awareness and synthetic memory, controls project movement, keeps the agent focused and watches for contamination, and monitors results/disturbance; it is not a verification gate. ADR-0.33.0 incompletely captures those purposes; silence does not revoke them. Transit supplies current ecosystem orientation and handoff carries the prior session model; they cooperate, and neither alone supplies a resident project model.

> Carried verbatim from root `AGENTS.md` § Operator Doctrine on 2026-09-17 (GHI #921), and into this surface on 2026-09-24 (GHI #1091, sweep findings S07/S08), where transit, exchange and lock work happens. The corpus `.gzkit/corpus/AGENTS.md.jsonl` keeps the ruling's history.

## When to Use

- Before starting work on an OBPI (claim it)
- After completing or abandoning OBPI work (release it)
- To check which OBPIs are currently claimed by agents

---

## Invocation

```text
/gz-obpi-lock claim OBPI-0.0.25-03
/gz-obpi-lock release OBPI-0.0.25-03
/gz-obpi-lock status                    # show all locks
/gz-obpi-lock status ADR-0.0.25        # show locks for one ADR
```

---

## Lock Mechanism

**File-based locks** in `.gzkit/locks/` (gitignored — local coordination only).

### Lock File Format

Path: `.gzkit/locks/obpi/{OBPI-ID}.lock.json`

```json
{
  "obpi_id": "OBPI-0.0.25-03",
  "agent": "claude-code",
  "pid": 12345,
  "session_id": "abc123",
  "claimed_at": "2026-02-14T12:00:00Z",
  "branch": "master",
  "ttl_minutes": 120
}
```

### Lock Rules

1. **Claim succeeds** if no lock file exists or existing lock is expired (past TTL)
2. **Claim fails** if lock exists and is not expired — show who holds it
3. **Release** deletes the lock file once the surrender is accounted for: an exchange record that postdates the claim, or an `--abandon` category
4. **Stale lock detection** — locks older than TTL are automatically released on next claim attempt
5. **Same-agent re-claim** — if the claiming agent already holds the lock, refresh the timestamp
6. **Concurrent locks** — Multiple OBPIs from the same ADR can be locked concurrently by different agents when their allowed paths are non-overlapping. One lock per OBPI at a time; each OBPI's human attestation is independent (universal per ADR-0.0.36).

---

## Procedure

### Claim

```bash
uv run gz obpi lock claim OBPI-X.Y.Z-NN
uv run gz obpi lock claim OBPI-X.Y.Z-NN --ttl 240
uv run gz obpi lock claim OBPI-X.Y.Z-NN --json
```

Exit code 0 = claimed, 1 = conflict (another agent holds it).

### Release

```bash
uv run gz obpi lock release OBPI-X.Y.Z-NN
uv run gz obpi lock release OBPI-X.Y.Z-NN --json
uv run gz obpi lock release OBPI-X.Y.Z-NN --abandon <category>:<reason>   # abort — surrender with a recorded category
uv run gz obpi lock release OBPI-X.Y.Z-NN --force   # waives the ownership check only
```

Exit code 0 = released (or no lock found), 1 = ownership error (without `--force`) or an invalid `--abandon` spec, 3 = refused: no exchange record postdates the claim and no `--abandon` was given.

A held lock is released only against a register entry (`.gzkit/rules/token-block-discipline.md` § Sub-Invariant 5). `gz obpi complete` writes that entry and surrenders the lock itself. Before completion the route is `--abandon`, whose categories are a closed enum listed in `docs/user/manpages/obpi-lock-release.md`. `--force` does not bypass the register entry, and a session handoff is not one (GHI #1167).

### Check (single OBPI)

```bash
uv run gz obpi lock check OBPI-X.Y.Z-NN
uv run gz obpi lock check OBPI-X.Y.Z-NN --json
```

Exit code 0 = held (prints holder info), 1 = free.

### List (all locks)

```bash
uv run gz obpi lock list
uv run gz obpi lock list --adr ADR-X.Y.Z
uv run gz obpi lock list --json
```

---

## Agent Identity

Agents identify themselves by environment:

| Signal | Agent |
|--------|-------|
| `CLAUDE_CODE` env var or Claude Code runtime | `claude-code` |
| `CODEX_SANDBOX` env var | `codex` |
| VS Code Copilot context | `copilot` |
| Fallback | `unknown-{PID}` |

---

## Integration with Pipeline

The pipeline calls `uv run gz obpi lock claim` at Stage 1 (Load Context). At Stage 5 `uv run gz obpi complete` writes the completion exchange record and surrenders the lock; no separate release runs. On an abort the pipeline surrenders with `uv run gz obpi lock release {OBPI-SLUG} --abandon <category>:<reason>`; when no category describes the abort the lock stays held, is named in the handoff, and is reaped at its TTL.

---

## Conflict Detection

### Shared File Registry

Files known to cause multi-agent conflicts:

| File Pattern | Conflict Type | Mitigation |
|-------------|---------------|------------|
| `docs/governance/GovZero/adr-status.md` | Derived ADR status index | Never hand-edit; regenerate via `uv run gz register-adrs` |
| `**/logs/obpi-audit.jsonl` | Append-only ledger | JSONL merge driver (see below) |
| `docs/design/adr/**/*.md` (status field) | Brief status | Lock prevents concurrent edits |
| `.gzkit/insights/agent-insights.jsonl` | Append-only log | JSONL merge driver |

### JSONL Merge Strategy

For append-only JSONL files, conflicts are resolvable by union merge:

1. Parse both sides as line arrays
2. Union (deduplicate by timestamp + content hash)
3. Sort by timestamp ascending
4. Write merged result

Add to `.gitattributes`:

```gitattributes
*.jsonl merge=union
```

The `merge=union` strategy keeps lines from both sides, which is correct for append-only ledgers.

### Pre-Push Conflict Check

Before pushing, agents should verify no divergence on shared files:

```bash
# Check if shared governance files have diverged from remote
git fetch origin
git diff --name-only origin/main..HEAD | grep -E '(adr_status|obpi-audit\.jsonl|agent-insights\.jsonl)'
```

If shared files appear in the diff, the agent should:
1. Pull and rebase
2. Regenerate computed files (`/gz-adr-sync`, `/gz-obpi-sync`)
3. Re-push

---

## Worktree Isolation (Advanced)

For heavy parallel workloads, a subagent may work in an ephemeral local git
worktree that is never pushed. Its result lands on main through the single
writer, never by merging a branch (`AGENTS.md` § Operator Doctrine):

```bash
# Detached worktree at HEAD; no branch is created
git worktree add --detach ../gzkit-claude-code HEAD

# In the worktree: stage the work and write it out as a patch
git -C ../gzkit-claude-code add -A
git -C ../gzkit-claude-code diff --cached --binary HEAD > ../gzkit-claude-code.patch

# On main, the single writer applies the patch and commits through the hooks
git apply ../gzkit-claude-code.patch
git worktree remove --force ../gzkit-claude-code
```

**When to use worktrees:**
- 2+ agents working on the same ADR simultaneously
- OBPIs with overlapping file paths
- Long-running implementation sessions (>2 hours)

**When NOT to use worktrees:**
- Single agent sessions (unnecessary overhead)
- Quick fixes or single-OBPI work
- OBPIs with non-overlapping paths

---

## Related

- Pipeline integration: `gz obpi lock claim` (Stage 1), `gz obpi complete` (Stage 5 surrender)
- Session handoff: `/gz-session-handoff` (session memory; it names a held lock and never releases one)
