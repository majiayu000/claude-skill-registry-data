---
name: research
description: Investigate a question against high-trust primary sources and capture the cited findings as a Kairos document attached to the initiating item. Use when the user wants a topic researched, docs or API facts gathered, or reading legwork delegated to a background agent.
---

Spin up a **background agent** to do the research, so you keep working while it reads.

Its job:

1. Investigate the question against **primary sources** — official docs, source code, specs, first-party APIs — not a secondary write-up of them. Follow every claim back to the source that owns it.
2. Write the findings as markdown, citing each claim's source.
3. Save them to Kairos, not as repo markdown: `create_item` with `item_type: document`, the findings as `content`, `board` set to the team board (SessionStart context) — the owner board of the document, which `create_item` requires for a document — and `parent` set to the item that prompted the research — the task or the initiative that the answer serves. That parent is what makes the findings discoverable later. If no initiating item exists, the findings are about the repository as a whole: send `board` and no `parent`. Ask the user when no board is known.
4. When the findings are about a repository, say so: `link_items` with `source` the new document, `target` the slug of the repository, and `relationship: impacts`. `get_repository` then lists the findings for each agent that works in that repository.

Spawn the agent with Kairos tool access: it performs the `create_item` save itself and reports back the created document's short code. Done when that short code exists under the initiating item, or with the team board as its owner, and has been surfaced to the user.
