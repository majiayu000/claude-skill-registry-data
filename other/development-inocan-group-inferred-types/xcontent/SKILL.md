---
name: XContent
description: X (Twitter) content creation system. USE WHEN create post, write tweet, create thread, build in public, reply tweet, x content, twitter visual.
---

# XContent

X (Twitter) content creation system for @TheSoloWolfEng - targeting 10k high-signal technical founders through build-in-public content.

## Workflow Routing

| Workflow | Trigger | File |
|----------|---------|------|
| **CreatePost** | "create x post", "write tweet" | `Workflows/CreatePost.md` |
| **CreateThread** | "create thread", "twitter thread" | `Workflows/CreateThread.md` |
| **CreateReply** | "reply to tweet", "engage" | `Workflows/CreateReply.md` |
| **CreateVisual** | "create visual", "twitter image" | `Workflows/CreateVisual.md` |

## Context Files

| File | Purpose |
|------|---------|
| `Voice.md` | X content voice and tone guidelines |
| `Examples.md` | High-performing post examples |

## Examples

**Example 1: Build in public post**
```
User: "Create a post about shipping the real-time interview assistant"
→ Invokes CreatePost workflow
→ Uses build-in-public voice
→ Generates engaging post with hook
```

**Example 2: Technical thread**
```
User: "Create a thread explaining my SaaS tech stack"
→ Invokes CreateThread workflow
→ Structures 5-7 tweet thread
→ Includes code snippets and insights
```

**Example 3: Engagement reply**
```
User: "Reply to this tweet about AI coding assistants"
→ Invokes CreateReply workflow
→ Adds value to conversation
→ Shows expertise without being salesy
```
