---
name: memory-hygiene
description: "Use when the memory store needs a health check: removing duplicates safely, resolving contradictory entries, decaying stale confidence, redacting secrets that slipped in, keeping an audit trail, or enforcing size budgets. Covers the full hygiene pass (dedupe, contradiction procedure, confidence decay, PII redaction, audit, budgets) with memory-store commands. Use when running the weekly maintenance pass, when recall returns conflicting facts, when stats show the store growing too fast, or after any incident that may have polluted the store."
version: 1.0.0
domain: memory
lifecycle: stable
last_verified: "2026-10-23"
requires: []
extends: []
relates: [memory-capture, memory-consolidation, agent-state]
tools:
  - name: memory-store
    version: 1.0.0
  - name: SQLite
    version: 3.45.1
  - name: Python
    version: "3.12"
---
Hygiene keeps memory trustworthy: no unresolved contradictions, no
rotting confidence, no secrets, a visible audit trail, and a bounded
size. This skill is the maintenance counterpart to memory-capture and
memory-consolidation: run it on a schedule (weekly for busy agents,
monthly otherwise) and after any event that may have polluted the
store. Full policy detail is in memory/HYGIENE.md.

## Quick Workflow

1. Run `stats` to see total entries, per-kind shares, and expired
   count.
2. Dry-run consolidation; merge duplicates that agree.
3. Hunt contradictions with targeted recalls and resolve each one.
4. Scan for secrets and PII that slipped past capture-time redaction.
5. Expire old entries with `forget --expired`.
6. Check size budgets; shorten TTLs if the store is growing too fast.
7. Log the pass: date, merges, deletions, contradictions resolved.

## 1. Measure first

```bash
# Baseline: totals, per-kind shares, expired, top agents
memory-store.py stats
```

Warning signs: episodic above 80 percent of rows, total entries past
50,000, expired count high (TTL cleanup not running), or one agent
producing far more entries than the others (possible write loop).

## 2. Deduplicate safely

```bash
# Review candidates, merge only entries that agree
memory-store.py consolidate --dry-run
memory-store.py consolidate
```

The rule from memory-consolidation applies here too: similar wording
about the same fact merges; entries that disagree go to the
contradiction procedure below, never into a merge.

## 3. Resolve contradictions

Two entries that both cannot be true (port open vs port closed on the
same host) need a decision, not a merge:

```bash
# Pull both entries
memory-store.py recall --query "10.0.1.5 port 22" --limit 10
```

Resolution order:

1. Newer direct observation beats older ones; systems change.
2. Direct observation beats second-hand reports.
3. Record a new entry stating the resolution with both ids cited,
   e.g. "Re-scanned 10.0.1.5 on 2026-10-23: port 22 closed. Entry
   871 (open) is superseded." Then `forget --id 871`.
4. If neither wins, keep both, tag both `disputed`, lower neither
   confidence, and schedule a live re-check.

```bash
# Delete the superseded entry after recording the resolution
memory-store.py forget --id 871
```

Never edit another agent's entry in place. Add your own entry and
link by id, so the audit trail shows who decided what.

## 4. Decay stale confidence and redact secrets

Confidence rots. On each pass, find old semantic entries nobody has
confirmed and mark them stale; scan for secret-like patterns that
escaped capture-time redaction:

```bash
# Entries about a topic, oldest first, to spot stale facts
memory-store.py recall --query "staging api" --kind semantic --limit 30

# Hunt for secrets that slipped in
memory-store.py recall --query "key token secret password private" --limit 50
```

For a found secret: rotate the secret on the real system first, then
`forget --id` the entry, then note the deletion in the audit log
without copying the secret into the log. For stale semantic entries:
drop confidence to 0.5 and tag `stale`, then re-confirm live or
delete.

## 5. Expire and budget

```bash
# Remove TTL-expired entries
memory-store.py forget --expired

# Confirm the store is back inside budget
memory-store.py stats
```

Budgets: under 50,000 total entries, episodic under 80 percent of
rows, single payload under 2,000 characters. If the store keeps
outgrowing the budget, the fix is structural: lower the episodic TTL,
consolidate weekly, promote repeated observations sooner. Deleting
healthy entries to hit a number is a last resort, not a policy.

## Edge cases

- Contradiction where both entries are old and the host is gone.
  Neither can be re-verified. Keep the newer, delete the older, and
  note in the surviving entry that the loser was removed
  unresolvable.
- Secret found but already rotated. Delete the entry anyway; a dead
  key in the store is still clutter and a bad example.
- An agent disputes your resolution. Both entries stay, both get the
  `disputed` tag, and the disagreement itself becomes an episodic
  entry so the next hygiene pass sees it.
- `forget --expired` deletes entries someone still references. TTLs
  are the contract: if an entry mattered past its TTL, it should
  have been promoted. Restore from backup only for genuine mistakes,
  and fix the TTL or promote immediately after.

## Escalation

- Contradictions keep appearing on the same topic. The underlying
  system is flapping or two agents measure differently. Investigate
  the measurement (different scan flags, different vantage points)
  before writing more entries.
- Secret exposure is large (whole table of tokens). Rotate
  everything, delete the entries, audit who had store access, and
  treat it as a security incident per incident-response.
- Store growth is exponential and consolidation cannot keep up.
  Find the write loop or the agent capturing raw output, stop it,
  delete the noise, and require one-idea entries going forward.
- The database file is corrupt or locked during the pass. Stop, back
  up the file, restore from the last good copy, and re-run the pass.

## Detection and defender view

Hygiene failures are how memory attacks succeed: an attacker who can
write to the store plants high-confidence false facts, and without
regular passes those lies calcify into "knowledge". Detect tampering
by watching `stats` for odd agents or sudden confidence inflation, by
auditing `merged_from` trails for evidence destruction, and by
treating any entry that instructs destructive action as a change to
production. The hygiene pass is the immune system; skipping it is how
a poisoned store stays poisoned.

## Key references

- CWE-312 (Cleartext Storage of Sensitive Information): secrets do
  not belong in memory.
- CWE-200 (Exposure of Sensitive Information to an Unauthorized
  Actor): the store is sensitive data at rest.
- CWE-922 (Insecure Storage of Sensitive Information): file-level
  access controls for the SQLite database.
- SQLite documentation: https://sqlite.org/docs.html
- memory/HYGIENE.md and memory/LIFECYCLE.md in this repo.
