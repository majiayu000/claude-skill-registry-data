---
name: editing
description: Use when editing prose for clarity and force. Covers cutting, structural editing, the specific constructions that weaken writing, and editing someone else's work without destroying their voice.
metadata:
  category: writing
  version: 1.0.0
  tags: [editing, clarity, concision, prose, revision]
---

# Editing

## Purpose

Make writing shorter and stronger without making it yours. Most editing is cutting; most weak prose is not badly constructed but merely padded.

## When to Use

- Editing your own draft.
- Editing someone else's writing.
- Prose that is technically correct and somehow limp.
- Cutting a piece to a length.

## Capabilities

- Structural editing: order, emphasis, what to cut entirely.
- Line editing: sentence-level force and clarity.
- Identifying the specific constructions that weaken prose.
- Preserving another author's voice.

## Inputs

- The draft, and what it is meant to do.
- The audience.
- The constraint: a length, a level, a tone.

## Outputs

- A shorter, clearer version.
- Structural notes distinguished from line edits.
- The author's voice intact.

## Workflow

1. **Structure before sentences** — There is no point polishing a paragraph you are about to cut. Read for the argument first: does each section earn its place, and are they in the right order?
2. **Cut the throat-clearing** — Most drafts genuinely begin in the second or third paragraph. Find where the piece actually starts and delete everything above it.
3. **Then edit the lines** — Cut hedges, filter phrases, and nominalizations. Prefer the active voice unless the passive is doing real work.
4. **Read it aloud** — Every sentence you stumble over is a sentence that needs rewriting. This is the single most reliable line-editing tool there is.
5. **When editing someone else's work, separate suggestion from correction** — A grammatical error is a correction. A different word choice is a suggestion, and it is theirs to decline.

## Best Practices

- The first draft is 30% too long. This is nearly universal and the cut nearly always improves it.
- Hedging destroys force: "it could be argued that", "in some sense", "arguably", "perhaps", "somewhat". Assert or do not.
- Filter phrases put distance between the reader and the point: "it is important to note that", "there is a growing body of evidence suggesting that". Delete the filter and state the thing.
- Nominalizations bury the verb: "made a decision" is "decided"; "performed an analysis of" is "analyzed"; "is indicative of" is "indicates".
- The passive voice is not a sin, but it is usually evasion: "mistakes were made" exists to avoid saying who made them.
- Never rewrite another author's voice into your own. Fix what is broken; leave what is merely different.

## Examples

**A line edit, showing the specific constructions:**

```text
BEFORE (61 words):

  It is important to note that there is a growing body of evidence which
  suggests that the implementation of comprehensive code review processes
  may potentially lead to a reduction in the number of defects that are
  introduced into production systems, although it should be acknowledged
  that the effectiveness of such processes can vary considerably depending
  on a number of different factors.

AFTER (24 words):

  Code review reduces production defects — though how much depends heavily
  on how it is done. Reviews that rubber-stamp large diffs catch almost nothing.

What was cut, and why:
  "It is important to note that"          filter phrase — delete, never replace
  "there is a growing body of evidence
   which suggests that"                    filter phrase — say the thing
  "the implementation of ... processes"    nominalization — "code review"
  "may potentially"                        double hedge — one of these, at most
  "lead to a reduction in the number of"   nominalization — "reduces"
  "that are introduced into"               passive padding
  "although it should be acknowledged
   that"                                   filter phrase
  "can vary considerably depending on a
   number of different factors"            says nothing — replaced with a
                                           specific, useful claim
```

The second version is not merely shorter. It is more informative, because the space freed by cutting the padding was spent on an actual claim.

**Editing someone else's work — the distinction that matters:**

```markdown
## Structural
- Sections 3 and 4 argue the same point with different examples. Merge them;
  the piece loses nothing and gains 400 words of pace.
- The strongest argument is in section 5. It should be section 2 — the reader
  currently has to earn it.

## Corrections (these are errors)
- "the data shows" — "data" takes a plural verb in this publication's style guide.
- Para 6: the 40% figure contradicts the 34% in the chart. One of them is wrong.

## Suggestions (yours to take or leave)
- "utilise" -> "use" throughout. Not wrong; just heavier than your usual register.
- The opening quote is doing less work than the sentence after it. Consider
  cutting it — but it is your voice, and if you like it, keep it.
```

## Notes

- Reading aloud finds every awkward sentence, and it finds them faster than any amount of silent rereading. The stumble is the signal.
- The most valuable single edit in most drafts is deleting the first two paragraphs. Writers warm up in public; readers should not have to watch.
- When editing another person's work, the temptation is to make it sound like you would have written it. Resist it. Your job is to make their version better, not to replace it.
