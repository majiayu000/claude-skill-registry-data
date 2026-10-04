---
name: edu-explainer
version: 1.0.0
description: Explain a hard concept at a target level using a concrete analogy and a check for understanding.
author: matrixx0070
tags: [education, explanation, analogy, comprehension, tutoring]
capabilities: []
---

## When to use

Use this to make one difficult concept click for a specific audience: pitch the explanation to their level, ground it in an analogy, then verify they actually got it. Great for jargon, abstract ideas, and "explain like I'm X" requests.

**Not for:** a full lesson with activities and timing (use edu-lesson-plan), a graded assessment (use edu-quiz-builder), or an extended back-and-forth dialogue (use edu-tutor-session).

## Method

1. Fix the target level. Confirm audience and prior knowledge (child, beginner adult, practitioner). Decision point: if unstated, default to "curious beginner, no jargon" and label it.
2. State the core idea in one plain sentence. Lead with the "what and why it matters" before any detail.
3. Choose an analogy from the learner's world. Pick something they already know; make the mapping explicit (X in the analogy = Y in the concept). Decision point: if the analogy breaks on an important point, say where it breaks so it doesn't create a misconception.
4. Layer detail. Add precision in one or two steps, replacing analogy with real terms as you go.
5. Give a concrete example. One worked, specific instance — no abstractions.
6. Check for understanding. End with a question or micro-task that reveals whether they got it (not "does that make sense?"). Provide the expected answer.

## Example

Concept: TCP handshake, for a beginner. Core: "Two computers agree they're both ready to talk before sending data." Analogy: a phone call — "Can you hear me?" / "Yes, can you hear me?" / "Yes." (SYN, SYN-ACK, ACK). Where it breaks: unlike a call, sequence numbers also sync so packets can be reordered. Example: your browser does this before loading a page. Check: "In the phone analogy, which step matches the server's SYN-ACK?" Expected: the "Yes, can you hear me?" reply.

## Pitfalls

- Pitching above the target level, drowning the idea in jargon the learner can't parse.
- Using an analogy that quietly breaks, planting a misconception you never flag.
- Ending with "make sense?" which invites a yes without evidence.
- Leading with edge cases and detail before the core one-sentence idea lands.

## Output format

```
Concept: <name> | Target level: <audience>

Core idea (1 sentence): <...>
Analogy: <familiar thing> → mapping: <X = Y>; breaks down at: <...>
Detail: <1-2 layers, real terms>
Concrete example: <specific instance>

Check for understanding: <question / micro-task>
Expected answer: <...>
```
