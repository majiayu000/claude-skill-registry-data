---
name: graph-memory
description: "Push graph memory over a modelled corpus. Runs a SQLite walk before any model answers. Use when the user asks who signs something off, multi-hop policy/role/person questions, graph memory, or to compare graph recall against hybrid RAG. Do not use for ordinary vault search; that is fde-kb."
---

# Graph memory (push recall)

`<skill>` is the directory that contains this SKILL.md.

Typed facts in SQLite. One recursive walk. The launcher prints the facts. Whatever model you already have reads them and answers. The skill does not pick, pin, or call a model.

This is a sibling of `fde-kb`. fde-kb is pull search over notes. This skill is push recall over asserted triples. Do not fold one into the other.

## STOP

First action is exactly one launcher command. Show stdout. Then answer from the printed facts with the model you already have. Do not switch models. Do not grep the corpus when recall returned facts. If the output says `(no memory matches for this prompt)`, say so and stop. Do not guess.

Never write a new graph walker, embedder, or HTTP client. Never dump `corpus/` into context. Never require a named vendor model or a vendor hook.

## Launcher (always this)

- **macOS / Linux:** `<skill>/scripts/graph-memory`
- **Windows:** `<skill>/scripts/graph-memory.cmd`

```bash
<skill>/scripts/graph-memory recall "the user's question"
```

```bat
<skill>\scripts\graph-memory.cmd recall "the user's question"
```

## Setup (once)

```bash
<skill>/scripts/graph-memory build
```

Writes `graph.db` next to the skill (or `GRAPH_MEMORY_DB`). Do not commit that file.

## Commands

| User says | Run |
|-----------|-----|
| who signs this off / what does the graph say | `graph-memory recall "question"` |
| rebuild the graph | `graph-memory build` |
| prove pull vs push | `graph-memory compare` (optional question; default is the refund trap) |

`compare` needs sibling `skills/fde-kb`. It indexes unstructured `corpus-before` as a throwaway vault and prints JSON for both paths.

## How to answer

1. Run `recall` with the user's actual question.
2. Put the printed facts in context.
3. Answer from those facts. Cite the `source_doc` on each triple.
4. Conditions (amounts, dates) live under `where:`. Apply them. The walk does not filter by date.
5. If there are no matches, say the graph has nothing. Do not invent a person.

Optional submit hook: [hooks.json](hooks.json) + `src/recall_hook.py`. This skill works without it. Prefer the CLI.

## Demo questions (shipped corpus)

- `A customer wants an £800 refund in March. Who signs it off?` → Marcus Webb
- `Who approves supplier payments over £2,000?` → Alex Doyle
- `What is the onboarding process?` → Ops Manager, day-one checklist
- `What does Priya do?` → Support Lead
- `Who is in charge when the boss is away?` → no memory matches

## Red flags

- Calling fde-kb search instead of `recall` for a graph-memory question
- Switching to a "smarter" model to compensate for missing facts
- Treating empty recall as a cue to read `corpus-before/`
- Committing `graph.db`
