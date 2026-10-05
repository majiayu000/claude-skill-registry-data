---
name: context-compression
description: Compress long task context into a verified handoff that preserves goals, authority, constraints, decisions, evidence, artifacts, failures, and next steps.
license: MIT
---

# Context Compression

## Preserve

- user goal, acceptance criteria, scope, and explicit authority;
- user corrections and preferences;
- verified facts with source paths/links and freshness;
- decisions, rationale, rejected alternatives, and invariants;
- files/state changed, backups, commands, test results, and failures;
- active task graph, dependencies, risks, blockers, and next actions.

Remove repeated prose, superseded speculation, raw logs already stored in artifacts, completed low-value narration, and source text that can be reopened by pointer.

## Method

1. Inventory current instructions, conversation, files, tool outputs, and external state.
2. Separate verified fact, inference, proposal, and unresolved question.
3. Write a compact handoff with exact paths, counts, commands, hashes/timestamps where relevant.
4. Check every critical claim against its source. Mark stale/external facts that need refresh.
5. Include negative knowledge: failed approaches and why they failed.
6. State the next dependency-ready step and its completion test.
7. After transfer/compaction, reopen the handoff and current artifacts; verify mutable state before acting.

## Handoff template

```markdown
Goal and done definition:
Scope / authority / do-not-do:
Verified current state:
Decisions and rationale:
Artifacts and backups:
Validation run and results:
Failures/attempts not to repeat:
Open risks/blockers:
Next actions in dependency order:
```

Do not claim a host-specific compact/rewind/clear command exists. Use the active host's actual mechanism when available.
