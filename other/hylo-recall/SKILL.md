---
name: hylo-recall
description: "Gets things back out of the user's notes and knowledge base: finds resources, topics, views and every note touching something (old and forgotten ones included), digs up ideas and material, reviews a past week or month or a random slice of history, and maps their knowledge as a whole. Use for 'find my notes on X', 'what do I know/think about X', 'what relates to this', 'give me material for X', 'inspire me', 'weekly review', 'show me something I've forgotten', 'what's in my knowledge base', '找一下关于 X 的笔记', '我对 X 怎么看', '找点素材/灵感', '周回顾', '随便翻翻', '我的知识库都有什么'."
---

# Hylo Recall

Gets things back out of the user's notes. Everything here is said in the conversation; nothing is saved unless they pick that afterwards.

Tools named here are Hylo's MCP tools (server `hylo`, maybe shown as `mcp__hylo__read`). If they aren't in your tool list, search your deferred tools for "hylo"; if still missing, say Hylo's tools are unavailable and stop.

## Pick the mode

| Mode | The user wants | Read |
| --- | --- | --- |
| **Find** | a resource, a topic, a view, every note touching something, or what relates to a piece of content | `find.md` |
| **Inspire** | ideas and material for something they're thinking about or about to write | `inspire.md` |
| **Review** | a look back over the past week or month, or at random through their history | `review.md` |
| **Explore** | the whole picture: what their knowledge covers, where it comes from, what's growing or quiet | `explore.md` |

Read the matching file and follow it. If you can't tell which they mean, ask with `choices`.

## Rules for every mode

- Find things in the order your instructions give, and link every unit or note you lean on.
- Keep the user's own views apart from what they read (`perspective`): an `external` view is "you read that…", with its source, never theirs.
- Date what you show by its source's original date.
- If their notes have nothing on it, say so in one line. Don't fill the gap with your own knowledge as if it were theirs.
