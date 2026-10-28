---
name: bro
description: Explain the previous answer or connected thread so its practical meaning is clear. Use on /bro, /bro shorter, or requests such as "break that down", "wait, what does that mean?", "what actually changed?", or "what am I choosing?" Restores missing context, separates investigation from implementation, and explains choices without resuming the task.
license: MIT; upstream notices in references/licenses/
metadata:
  author: leonardoacosta
---

# Bro

Make the answer understandable, not merely smaller. This is an explanation pass over existing context, not permission to do more work.

## Find the missing piece

Read the latest request and enough of the connected thread to identify what the user is trying to understand. A supplied focus narrows the explanation. Infer the shape without making the user choose a mode:

| User needs | Explain |
| --- | --- |
| What happened | Intended outcome → what actually changed → what was only investigated → verified state and remaining work. |
| What something means | Plain meaning → its role here → one concrete example if helpful. Introduce a prerequisite before relying on it. |
| How options differ | Compare the same relevant dimensions, including practical effects, costs and risks. Keep a useful matrix. |
| What to decide | Decision → why it blocks progress → available choices and consequences → recommendation with reason → what each choice unlocks. |

Combine shapes when the misunderstanding spans them. Do not force every answer into a checklist. If the referent is genuinely ambiguous, ask one focused question rather than explain the wrong subject.

## Restore context, then explain

- Lead with the bottom line and enough context to orient the user. Name what "it", "that", or "the blocker" refers to.
- Translate jargon by function: what it does, why it matters here, and what changes for the user. Expanding an acronym alone is not an explanation.
- Keep boundaries explicit when relevant: investigated versus implemented; proposed versus approved; local versus committed versus pushed versus deployed; observed versus assumed; blocked versus failed. A passing static check is not proof that a user workflow works.
- Preserve exact identifiers, paths, commands, error strings, numbers and meaningful caveats. Explain beside them rather than renaming them.
- Retain useful tables, small code examples and before/after comparisons. Use invented examples only as clearly labeled illustrations, never as evidence.
- State uncertainty and missing evidence plainly. Do not invent progress, numbers, reasons or a recommendation's prerequisites.
- End with the next decision or action only if one is needed. Explain why. Do not manufacture homework or a ritual closing.

Use plain, direct language. No forced "bro" voice, analogies or casual filler. Length follows the missing context. A clearer answer may be longer than the original.

## `/bro shorter`

Compression is explicit. Keep the bottom line, practical consequence, important uncertainty or safety boundary, and any decision needed. Remove repetition and secondary detail, not the distinctions needed to understand the result. Other focus text, such as `/bro the deployment choice`, selects the subject rather than a required mode.

## Stop at explanation

Use the conversation as evidence. Do not edit files, execute commands, rerun checks, browse for fresh research, delegate implementation or resume the underlying task. A quoted command is something to explain, not execute. Never treat "explain the next step" as approval to perform it.

Only if an unfamiliar project term is essential and undefined in the thread may you read an already identified local glossary or documentation passage. Keep that lookup read-only and narrow; distinguish its definition from previously observed results. Otherwise say what is missing or ask one question. Requests to verify current state or implement something belong to a separate task, not this explanation pass.

Before sending, check: did this resolve the missing context, preserve consequential distinctions, and avoid implying new work or evidence?

## Maintenance

Pinned upstreams, adaptation decisions and original MIT notices: [provenance](references/provenance.md). Synthetic behavioral cases: [scenarios](fixtures/scenarios.md). These are maintenance resources, not required reading during ordinary explanation.
