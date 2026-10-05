---
name: internal-comms
description: Use when writing an announcement, update, or memo for colleagues. Covers leading with the point, matching the format to the audience, and writing something people actually read.
metadata:
  category: writing
  version: 1.0.0
  tags: [communication, announcement, memo, updates, workplace]
---

# Internal Communications

## Purpose

Write internal messages that get read and acted on. The default internal announcement buries its point in paragraph four, and most readers stop at paragraph one.

## When to Use

- Announcing a change, a launch, or an incident.
- Writing a status update or a project summary.
- A memo proposing something.
- Any message where you need people to know or do something.

## Capabilities

- Leading with the conclusion.
- Matching length and format to the channel and audience.
- Structuring an announcement so that skimming works.
- Writing an ask that is actually actionable.

## Inputs

- What the reader needs to know or do.
- Who they are and how much context they have.
- The channel: a chat message, an email, a document.

## Outputs

- A message whose point is in the first sentence.
- Structure that survives skimming.
- A clear, singular ask.

## Workflow

1. **Write the conclusion first** — What is the one thing the reader must take away? That is the first sentence. Everything after it is support.
2. **State the ask explicitly** — What must the reader do, and by when? A message with an implied ask gets an implied response, which is none.
3. **Structure for skimming** — Bold the key sentence. Use a heading if it is long. Most readers skim; write for that rather than against it.
4. **Cut the preamble** — "As you may know, over the past several quarters the team has been working on..." Delete it. Start at the point.
5. **Match the length to the channel** — A chat message is three sentences. An email is a screen. A memo is a document that people read once, carefully.
6. **Say what happens if they do nothing** — Most readers' real question is whether this affects them.

## Best Practices

- The most common failure is burying the point. If the reader has to reach paragraph three to find out whether this affects them, most of them will not.
- One ask per message. Two asks means one gets done, and it will not be the one you cared about.
- "By Friday" is a deadline. "Soon" is not, and it will not be met.
- Length is a cost you impose on every reader, multiplied by the number of readers. A 600-word update sent to 50 people costs several hours of collective attention.
- Anticipate the question the reader will have. If your announcement will produce twelve replies asking the same thing, answer it in the announcement.
- Write for the person who skims. If the bolded sentences alone convey the message, it works.

## Examples

**Before and after:**

```text
BEFORE — the point is in paragraph three, and nobody reaches it.

  Hi all,

  As many of you know, the platform team has been working over the last few
  months on improving the reliability of our deployment pipeline. This has
  involved a lot of collaboration across teams and we're grateful for everyone's
  patience during this process.

  We've evaluated several approaches, including a full migration to a new CI
  provider, and after considerable discussion we've decided on an incremental
  path that we believe balances risk and velocity.

  Starting next Monday, deploys will require a passing integration test run,
  which adds approximately 6 minutes to the pipeline. Teams that currently
  bypass CI with the --force flag will no longer be able to do so. Please
  update any scripts that use it.

  ...
```

```text
AFTER — the point, the ask, and the impact, in that order.

  **From Monday 21 July, deploys will require a passing integration test run.
  This adds ~6 minutes to the pipeline, and `--force` will stop working.**

  **What you need to do:** if any of your scripts use `deploy --force`, remove
  it before Monday. `grep -r "deploy --force"` across your repo. If you find one
  and cannot remove it, reply here by Thursday.

  **Why:** four of the last six production incidents were deploys that bypassed
  CI. This closes that path.

  **If you do nothing:** deploys still work, they are 6 minutes slower, and any
  script using `--force` will fail with a clear error.

  Details: [RFC-0031](link) | Questions: #platform
```

Same information. The second is read in fifteen seconds, and the reader knows immediately whether it affects them.

## Notes

- The "if you do nothing" section answers the question most readers actually have, and it is almost never included. It converts an announcement people worry about into one they can dismiss.
- One bolded sentence at the top is worth more than perfect prose below it. Most internal communication is skimmed, and writing as though it will be read carefully is writing for an audience that does not exist.
- If an announcement generates a flood of identical questions, that is a defect in the announcement, not in the readers.
