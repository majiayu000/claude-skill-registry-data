---
name: to-questionnaire
description: Turn a decision the user can't fully answer into a Markdown questionnaire for someone else to fill in, async or over a meeting.
disable-model-invocation: true
---

# To Questionnaire

Turn something the user can't answer alone into a **questionnaire**: a Markdown document they hand to one person to fill in async, or fill out together over a meeting. The recipient holds knowledge the user lacks; the questionnaire pulls it out of them.

**Grill the send, not the subject.** Interview the user only about the _send_, which they can always answer: who it goes to, and what they need back. The questions in the document then target the **gap** between what the recipient knows and what the user needs. Use the question shape from `grilling` for the setup questions, `AskUserQuestion` where available, otherwise chat.

The recipient has none of the user's context, so `grilling`'s **Frame the problem, then ask** and **Write it in Simplified Technical English** rules govern the whole document, not just the setup questions. A question the recipient must decode is a question they answer badly or skip.

1. **Who is it going to?** Ask, in one exchange, the recipient's role, expertise, and relationship to the user. This fixes the questionnaire's tone and how much context it must carry. Done when you know who the recipient is and what they know that the user doesn't.

2. **What do you need back?** Ask, in one exchange, the specific decisions or facts the user can't resolve alone and needs from this person. Done when you have a concrete list of what the user must walk away able to do or decide.

3. **Write the questionnaire.** Draft questions aimed at the gap from steps 1–2, following the Document structure below. Write it under the effort's `.scratch/` directory as `questionnaire-<slug>.md` (slug from the topic), alongside the map or spec it serves: never loose in the repo root. When it unblocks a `wayfinder` ticket, link it from that ticket through the tracker's Assets operation. The `.md` file stays the record. Where the harness can put it in front of the recipient to answer in place, also publish a private copy: a document connector where one is attached (Claude Docs, through its `docs` skill or `guide`), otherwise a page (the Artifact tool, after loading `artifact-design` and `artifact-capabilities`) whose answer boxes save each answer to its `db` collection `answers`, keyed by question; the recipient needs Contributor access to write. Add `**Answer online:** <link>` under the file's **From** line. Sharing the link is the user's call; without either, the user sends the Markdown file itself. Report the path and any link. Done when the file exists, is linked from any ticket it serves, and every item the user named in step 2 is covered by a question.

## Document structure

Frame the document as a **discovery questionnaire**: the user lacks context, the recipient holds it. Order questions most-important-first (async means you may only get one pass) and group them under `##` headings by theme once there are more than a handful. Write it using the template below.

<questionnaire-template>

# <Questionnaire title>

**Purpose:** why this questionnaire exists and the decision riding on it.

**From:** <the user> (**To:** <the recipient>) **How your answers will be used:** <where they go>

## Context

One paragraph orienting a recipient who wasn't in the user's head. Enough to answer well, not a page.

## How to answer

Deadline and rough effort. Partial answers and "I don't know" are useful: flag anything you're unsure of rather than skipping it.

## <Theme heading>

One `##` section per theme. Under each, its questions, most-important-first. Every question is one idea (never compound) with an answer stub directly beneath, and a one-line _why this matters_ only where the question could be misread or invite a throwaway answer.

<question-example>
### What load is the system expected to handle at launch?

_Why this matters: it decides whether we provision for burst traffic now or defer it._

>
</question-example>

## Anything else?

A closing catch-all: anything we didn't ask that we should know?

</questionnaire-template>

## When you're done

Print the end-of-session block using the frame in [`wayfinder/references/pipeline-end-block.md`](../wayfinder/references/pipeline-end-block.md).

```text
---
Pipeline: **decide** → spec → tickets → build   (a questionnaire unblocks a decision)
Done: <file path (and online link); who it's for; what it needs back>
Next:
  • <condition> → /<skill> <ref>
```

Stage-specific **Next** conditions (only those that apply, most likely first):

- **Questionnaire written, answers not back yet** → nothing to run; send it, then `/grill-me` on the blocked branch once answers land. Name the branch so the next session knows what was waiting.
- **Answers already in hand** → if they were given online, read them back first (Claude Docs `read`, or `ArtifactData` `list` on the page's `answers`) into the `.md` file's answer stubs; then `/grill-me` on the blocked branch, feeding the answers in
- **It unblocks a `wayfinder` ticket** → Release that ticket (clear its claim) and leave a `## Comments` note saying it waits on this questionnaire, so it stays visible on the frontier rather than stranded under a dead claim; `/wayfinder <map>` to re-claim and resolve it once the answers land
- **Part of the gap is a documented fact, not a person's knowledge** → `/research` on that part in parallel
- **Stopped before finishing** → say what the draft covers and which of the user's needs have no question yet
