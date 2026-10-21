---
name: draft-knowledge-page
description: Draft one knowledge page for a topic a drive found missing from memory — something no screen shows and research can answer (a speed bar for a kind of product, the rules that apply to a kind of record, the usual roles in a kind of team) — researched with its sources, and raise it through the memory tool as a memory update a person approves (ADR 035). One page answers every question of its topic. Marks the page for the project's memory when it is a fact about the product or its team, not about one drive. Used by the knowledge-builder agent in /build-knowledge.
user-invocable: false
model: opus
allowed-tools: Read, Write, Bash, WebSearch, WebFetch
---

# draft-knowledge-page

Some questions no prototype could answer, because they are not about screens: how fast a
review page must respond, whether GDPR applies to review records, who in a software team may
approve what. Asking the person each one is slow and asks them to be an expert. Instead, this
skill drafts the knowledge once, with its sources, for the person to approve.

## Input

| Field | Required | Meaning |
|-------|----------|---------|
| `topic` | yes | The topic (e.g. "speed bar for a review tool's pages") and the questions it must answer |
| `context` | yes | What the drive knows of the product — its intents, its domain — from the build's working files |
| `issue` | yes | The drive's issue; the memory update lands in its short-term memory |
| `memory_tool` | yes | `.garura/core/tools/memory/memory.py` |

## Process

1. List what the page must let an agent answer — every question in the topic.
2. Research: standards, common practice, the law, well-known references. Keep each source's
   link and what it says. Prefer one clear source to many weak ones.
3. Write the page in plain words, as knowledge an agent can use on any later drive for this
   product: the facts, the usual values, the choices and when each applies. Mark what is a
   choice the person must make (a target they set), not a fact.
4. Raise it through the memory tool, never by writing memory yourself:

   ```bash
   python3 <memory_tool> propose --request '{"issue": <issue>,
     "missing": "<the topic, in one line>", "target_tier": "short-term",
     "target_path": "<issue>/context/answers/kb/<topic-slug>.md", "draft": "<the page>",
     "draft_source": "web", "sources": [<each link>], "requested_by": "knowledge-builder (/build-knowledge)"}'
   ```

5. Say whether the page belongs in the **project's memory** (`for_project_memory: true`): a
   fact about this product or its team that every later drive needs. Moving it there is a
   person's promotion, later (`/promote-memory`).

## Output

The memory update's id, and `for_project_memory`.

## Rules

- Never decide, apply or promote an update; a person decides (ADR 035, ADR 039).
- Every fact on the page has a source; a value the person must choose is marked as a choice.
