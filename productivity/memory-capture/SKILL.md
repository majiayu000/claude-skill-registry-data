---
name: memory-capture
description: Use when an agent needs to record what it learned so future
  runs can reuse it, or when an operator wants durable notes from a task
  that took real effort. Covers choosing the right memory kind (episodic
  events, semantic facts, procedural how-to), writing one-idea entries
  with honest confidence scores, tagging for later recall, and capturing
  with the memory-store CLI. Use when a scan finishes, a host behaves
  unexpectedly, a lesson is learned the hard way, or a session ends and
  the knowledge must survive it.
version: 1.0.0
domain: memory
lifecycle: stable
last_verified: "2026-10-23"
requires: []
extends: []
relates: [memory-recall, memory-hygiene, incident-response]
tools:
  - name: memory-store
    version: 1.0.0
  - name: SQLite
    version: 3.45.1
  - name: Python
    version: "3.12"
---

Agent memory is what survives between runs: observations, durable facts,
and procedures that make the next run smarter. This skill covers capture,
the first stage of the memory lifecycle: deciding what is worth
recording, picking the right kind, writing entries with honest
confidence, and storing them with the memory-store CLI. Schemas and field
definitions live in memory/MEMORY_SCHEMA.md; capture timing rules live
in memory/LIFECYCLE.md.

## Quick Workflow

1. Decide if the knowledge is worth storing: will a future agent or
   operator make a better decision because of it?
2. Recall first: check whether an equivalent entry already exists.
3. Pick the kind: just happened (episodic), durable fact (semantic),
   or how-to (procedural).
4. Write one idea per entry, plain text, with a confidence that matches
   the evidence.
5. Store with memory-store, tagging for recall and setting TTL only
   when the default is wrong.
6. Redact secrets before storing, never after.

## 1. Recall before you store

Never record blind. A duplicate entry wastes space and splits confidence
across two rows.

```bash
# Check for an equivalent entry before writing
memory-store.py recall --query "staging api token" --kind semantic --limit 5
```

If an equivalent entry exists, do not store a second one. The new
observation corroborates the old one: note that in your notes, and if
the store supports it, let consolidation raise the confidence later. If
the old entry is wrong, record a new entry that supersedes it by id
(see memory-consolidation) instead of silently duplicating.

## 2. Pick the right kind

Ask two questions: "will this be true next month?" and "did this just
happen?" True next month means semantic. Just happened means episodic.
"Does this tell me how to do something better?" means procedural.

```bash
# Episodic: an event with a timestamp and an actor
memory-store.py store --kind episodic --agent hunter-01 \
  --text "Finished nmap sweep of 192.168.11.0/24: 14 hosts up, 3 with port 22 open." \
  --confidence 0.8 --tags "nmap,subnet,scan"

# Semantic: a fact that stays true
memory-store.py store --kind semantic --agent analyst-02 \
  --text "The staging API rejects tokens older than 15 minutes." \
  --confidence 0.9 --tags "api,staging,auth"

# Procedural: hard-won how-to
memory-store.py store --kind procedural --agent operator-izaz \
  --text "Run sqlmap with --batch and --threads=2 on fragile targets to avoid interactive prompts and overload." \
  --confidence 0.95 --tags "sqlmap,web"
```

Misfiled kinds are cheap to fix later (recall by topic, delete, re-store
correctly), but getting it right at capture keeps recall clean. When
unsure, default to episodic with modest confidence; promotion to
semantic happens in consolidation.

## 3. Write entries with honest confidence

Confidence reflects evidence, not hope. Use these anchors:

- 0.9+: corroborated by a second independent observation, or recorded
  by the operator who set the fact.
- 0.7 to 0.8: single direct observation (you ran the command, you saw
  the output).
- 0.4 to 0.6: inferred from indirect evidence, or copied from someone
  else's report.
- Below 0.4: a guess. Usually not worth storing at all.

```bash
# Direct observation, solid confidence
memory-store.py store --kind episodic --agent hunter-01 \
  --text "Port 445 is open on 10.0.1.5 and responds to SMB negotiation." \
  --confidence 0.8 --tags "smb,scan"

# Second-hand report, lower confidence
memory-store.py store --kind episodic --agent analyst-02 \
  --text "Helpdesk reports the file server was slow all morning, possibly under load." \
  --confidence 0.5 --tags "helpdesk,report"
```

Never round confidence up to make an entry look more certain. A recall
query that surfaces a 0.5 entry tells the reader to verify; a fake 0.9
tells them not to, and that is how bad memory causes bad decisions.

## 4. Tag for recall

Tags are the index. Use lowercase, specific nouns, no spaces:

```bash
memory-store.py store --kind procedural --agent operator-izaz \
  --text "Scan internal subnets with --max-rate 200 to avoid IDS alerts." \
  --confidence 0.9 --tags "nmap,ids,rate-limit"
```

Good tags: `nmap`, `smb`, `staging`, `ids`, `sqlmap`. Bad tags:
`stuff`, `important`, `networking` (too broad). Two to four tags per
entry is enough; more tags usually means the entry contains two ideas
and should be split.

## 5. Redact secrets at capture time

Secrets never enter the store. Redact before calling store, not after.

```bash
# WRONG: raw token in the entry
memory-store.py store --kind episodic --agent hunter-01 \
  --text "Used token ghp_x1y2z3 to query the API"

# RIGHT: describe the event, redact the secret
memory-store.py store --kind episodic --agent hunter-01 \
  --text "Queried the API with a personal access token (redacted); it returned 200 for all 40 requests."
```

If you catch a secret after storing, rotate the secret on the real
system first, then delete the entry with `memory-store.py forget --id`.
Deleting does not un-leak a live key.

## Edge cases

- Capturing from a long transcript. Do not store the whole transcript.
  Store the conclusion and the path to the artifact, e.g. "Full scan
  output at /tmp/scans/net-2026-10-23.xml; conclusion: 14 hosts up."
- The agent is unsure the observation is correct. Store it anyway with
  low confidence (0.4 to 0.5) and tag it `unverified`. Low-confidence
  memory is a flag to verify, not a lie.
- Two agents capture the same event seconds apart. Both entries are
  legitimate; consolidation will merge them later. Do not delete one
  manually unless you wrote it yourself.
- Capture during an incident. Record timestamps obsessively; timeline
  reconstruction depends on `created_at`. See incident-response for
  the full incident workflow.
- The database file is missing or locked. memory-store creates the
  file on first use; a lock usually means another process is writing.
  Wait a few seconds and retry rather than writing to a second file.

## Escalation

- Equivalent entry exists but contradicts the new observation: do not
  overwrite. Store the new observation as episodic with both ids
  mentioned in the text, then resolve per memory/HYGIENE.md
  contradiction rules.
- Entry must be stored but the payload is over 2,000 characters:
  write the full content to a file, store the conclusion plus the
  path.
- Secret already stored and still live: rotate the secret on the real
  system first, delete the entry second, note the deletion in the
  audit log.
- Capture fails repeatedly with database errors: check disk space and
  file permissions on MEMORY_STORE_DB, and fall back to a dated notes
  file until the store is healthy.

## Detection and defender view

For memory, the "defender" is the future operator reviewing the store.
Misuse looks like this: entries stuffed with secrets (exposure), fake
high-confidence entries that poison decisions (integrity), entries
written about systems outside the authorized scope (overreach), and
poisoned procedural entries that would make an agent run harmful
commands. Detect these by auditing `stats` output for odd agents, by
scanning recalls for secret-like patterns, and by requiring procedural
entries to name the safe context they apply to. Any memory entry that
tells an agent to do something destructive gets the same review as a
change to production code.

## Key references

- CWE-312 (Cleartext Storage of Sensitive Information): why secrets
  never enter the store.
- CWE-200 (Exposure of Sensitive Information to an Unauthorized
  Actor): the cost of a leaked memory database.
- SQLite documentation: https://sqlite.org/docs.html
- Python sqlite3 module: https://docs.python.org/3/library/sqlite3.html
- memory/MEMORY_SCHEMA.md and memory/LIFECYCLE.md in this repo.
