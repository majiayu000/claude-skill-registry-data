---
name: wiki-recall
description: Retrieve a small, relevant set of current Yarbrain notes, episodes, and approved procedures for an upcoming task. Use before substantial debugging, design, planning, or repeated work where prior knowledge can change the approach; remain read-only.
---

# Recall Wiki Knowledge

Load only knowledge that can materially help the current task.

## Workflow

1. Derive search terms from the repository or project, named components, error
   signatures, technologies, people, and task verbs.
2. Resolve ../../scripts/yarbrain.py relative to this SKILL.md and search the
   configured vault with a limit of five results.
3. Reject keyword-only matches whose scope or subject is unrelated.
4. Prefer current semantic notes. Prefer an approved procedure when the task
   matches its trigger. Read episodes only when the semantic note is incomplete
   or its provenance matters.
5. Read each selected item and check status, verified_at, volatility, scope,
   and disputed or superseded warnings before relying on it.
6. Return the relevant knowledge, why each item matters, its freshness, and any
   conflict or stale warning. Link or name the source item so deeper evidence
   can be read on demand.

Do not inject the whole vault, write recall summaries back into it, update access
timestamps, or let remembered guidance override current repository instructions
or authoritative source code.
