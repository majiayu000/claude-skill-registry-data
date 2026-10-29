---
name: memory-recall
description: Use when an agent needs to look up what it already knows
  before doing new work, or when an operator wants the facts behind a
  past decision. Covers query patterns (keyword choice, kind filters,
  tag and agent filters), how the memory-store relevance ranking works,
  interpreting confidence and staleness, and recalling procedural
  knowledge mid-task. Use when starting any scan, investigation, or
  incident, when verifying a claim, or when drafting a report that
  depends on earlier findings.
version: 1.0.0
domain: memory
lifecycle: stable
last_verified: "2026-10-23"
requires: []
extends: []
relates: [memory-capture, memory-consolidation]
tools:
  - name: memory-store
    version: 1.0.0
  - name: SQLite
    version: 3.45.1
  - name: Python
    version: "3.12"
---

Recall is the habit of asking the store before doing new work. It saves
re-running scans, prevents contradicting established facts, and surfaces
procedural knowledge exactly when a task needs it. This skill covers
query patterns, relevance ranking, and how to read a result set with a
critical eye. Schemas live in memory/MEMORY_SCHEMA.md; recall timing in
memory/LIFECYCLE.md.

## Quick Workflow

1. State the question in 2 to 4 keywords before querying.
2. Recall broadly first (no kind filter), then narrow with kind, tag,
   or agent filters.
3. Read results top-down: higher relevance first, but check confidence
   and date on each entry.
4. Treat low-confidence or stale entries as leads to verify, not facts.
5. If the query returns nothing useful, note the gap: store what you
   learn so the next recall hits.

## 1. Basic query patterns

Start broad, then filter. The default limit of 10 is usually right for
interactive use; raise it for audits.

```bash
# Broad search across all kinds
memory-store.py recall --query "login brute force" --limit 10

# Durable facts only
memory-store.py recall --query "token expiry" --kind semantic

# How-to knowledge for the current task
memory-store.py recall --query "nmap rate limit" --kind procedural

# What happened on one host
memory-store.py recall --query "10.0.1.5" --kind episodic --limit 20
```

Keyword choice matters more than sentence structure. Use the nouns the
entry would contain: `staging api token`, not "what do we know about
how long staging tokens last". Try synonyms on a miss: `auth` vs
`login`, `scan` vs `sweep`.

## 2. Filtering with tags and agents

When the store is large, filters beat longer queries:

```bash
# Entries from one agent about one topic
memory-store.py recall --query "scan" --tags nmap --agent hunter-01

# Everything procedural an operator recorded
memory-store.py recall --query "" --kind procedural --agent operator-izaz --limit 50
```

Combine kind plus tags for the common case: "procedural knowledge about
sqlmap" becomes `--kind procedural --tags sqlmap` with a short query.
Agent filters are useful for audits ("what did this agent claim?") and
for finding the operator's own notes.

## 3. How relevance ranking works

memory-store ranks results in four passes, and knowing the order helps
you write better queries:

1. Kind, tag, and agent filters apply first; filtered-out entries
   never score.
2. Query token overlap with the payload scores the entry. More distinct
   query tokens matched means a higher rank.
3. Ties break on confidence (higher first), then recency (newer first).
4. Expired entries never appear in recall results.

Practical consequences: a query with one rare keyword (`token`) beats a
query with three common ones (`the api is`); filters are the only way
to guarantee a kind shows up; and a stale-but-confident entry can
outrank fresh evidence, so always read the `created` timestamp.

## 4. Reading results critically

Every result shows id, kind, agent, confidence, date, tags, and text:

```bash
memory-store.py recall --query "port 22 10.0.1.5" --limit 5
```

Interpretation rules:

- Confidence 0.9+ from a direct observation: trust, but confirm the
  date is recent for fast-changing facts (open ports, running
  services).
- Confidence 0.4 to 0.6: a lead, not a fact. Verify with a fresh
  command before acting on it.
- Two entries disagree: read both timestamps and agents. Newer direct
  observation wins; if both are recent and credible, tag the topic
  `disputed` and re-check live (see memory-hygiene).
- `merged_from` entries carry merged confidence from duplicates; the
  confidence is stronger than the text age suggests.

After recall, act: use the knowledge, then record the outcome with
memory-capture so the store learns whether the recalled fact held up.

## Edge cases

- Query returns nothing. The knowledge may be tagged differently, or
  it was never captured. Try synonyms, drop filters, then accept the
  gap and store the new finding when you learn it.
- Query returns hundreds of rows. Narrow with `--kind` and `--tags`
  before raising `--limit`. Reading 50 rows is an audit; reading 500
  is a script job (dump with a small Python snippet against the
  SQLite file directly).
- Expired knowledge is needed anyway. Expired entries are hidden from
  recall by design. If you truly need them (forensics on old events),
  query the SQLite file directly with a raw SELECT before the next
  `forget --expired` run, and export what you need.
- Recall during an active incident. Query with the host or indicator
  first, then the technique: `recall --query 10.0.2.41` before
  `recall --query lateral movement`. Specifics beat abstractions
  under time pressure.

## Escalation

- Contradictory entries on a fact you must act on now: trust the
  newest direct observation, record your decision as episodic, and
  mark the topic `disputed` for later hygiene.
- A critical procedural entry looks outdated (names an old tool
  version): verify the procedure against the current version before
  following it, then update or supersede the entry.
- Recall is slow on a large store: the ranking is token-overlap over
  full rows; for stores past ~50k rows, add tag filters to every
  query and shorten the episodic TTL (see memory-hygiene size
  budgets).
- The store file is corrupt: stop, copy the file aside, and restore
  from the latest backup. Never run write commands against a
  suspect database.

## Detection and defender view

Misuse of recall looks like bulk extraction: one agent dumping the
whole store (`--limit` huge, empty queries) to exfiltrate operational
knowledge, or fishing queries for secrets that should never have been
stored. Detect it by watching for abnormal query volume from one agent
and by auditing recalled content for secret-like patterns. The
mitigation is twofold: never store secrets (memory-capture redaction
rules), and treat the memory database as sensitive data at rest, with
the same access controls as any credential-adjacent file.

## Key references

- CWE-200 (Exposure of Sensitive Information to an Unauthorized
  Actor): why the store is sensitive data at rest.
- SQLite documentation: https://sqlite.org/docs.html
- Python sqlite3 module: https://docs.python.org/3/library/sqlite3.html
- memory/MEMORY_SCHEMA.md and memory/LIFECYCLE.md in this repo.
