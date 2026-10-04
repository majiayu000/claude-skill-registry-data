---
name: session-memory
description: "Stores verified cross-session facts, decisions, preferences, and open questions without secrets, speculation, or monitoring."
---

# Session Memory

Use this skill when continuity between sessions matters: project conventions,
decisions, repeated user preferences, unresolved risks, or next-step state.

This is a conservative Codex adaptation of persistent-memory tools. It does not
install a background watcher, does not sync to external memory services, and
does not write secrets.

## Memory Contract

Only persist:

- verified project facts;
- explicit user preferences;
- architectural decisions;
- commands that passed or failed;
- unresolved questions;
- next steps with dates or commit references when useful.

Attach the source revision or file hash and evidence date to claims that can
become stale. A passed command records its actual exit code and raw artifact
pointer; a summary alone does not establish validation. A configured model is
not a verified route: retain requested and observed metadata separately under
the `subagent-result-merge` contract, with unknowns preserved.

Do not persist:

- credentials, tokens, private keys, `.env` values;
- personal data unrelated to the work;
- guesses presented as facts;
- transient thoughts that will confuse future sessions;
- large raw logs when a summary is enough.

## Where To Store

Prefer existing project docs:

- `docs/`
- `AGENTS.md` when the rule should affect future agents;
- a user-approved memory file if the repository already has one.

Only portable project decisions belong there. Keep machine configuration,
model mappings, capability snapshots, installation reports and raw validation
artifacts outside tracked files in private local state. Generated project-local
capabilities may live in ignored `.engineering-bible/`; derive them from actual
host discovery, not a package catalog.

Beads owns task status, session-memory owns verified durable decisions, and
QMD searches existing documents. Store each fact once in its owning system and
use references; do not replicate all records across these tools. Do not
initialize Beads or new memory stores across other projects automatically.

When a natural-language query misses relevant documents, the optional offline
`scripts/memory-retrieval.py` helper can plan a content-word variant and fuse the
ranked lists returned by the existing authorized search capability. Keep the
original results, per-query ranks, and source hashes. Verify the captured source
files before using the fused result as current evidence; without that check the
helper reports `SKIP`. It does not search, create another index, or authenticate
the search service. See `docs/memory-retrieval.md` for the input contract.

If there is no existing convention, output a proposed memory delta instead of
writing a new file automatically.

## Workflow

1. Read existing durable instructions or memory files.
2. Identify what changed in the current session.
3. Separate facts, decisions, preferences, and open questions.
4. Remove secrets and unverified claims.
5. Write only if the user asked for persistence or the repository already has
   an established memory/update rule.

## Memory Delta Format

```markdown
Memory delta:
- Fact:
- Decision:
- Preference:
- Open question:
- Validation:
```

## Output

Report:

- memory read;
- memory written or proposed;
- redactions made;
- facts that remain unconfirmed.
