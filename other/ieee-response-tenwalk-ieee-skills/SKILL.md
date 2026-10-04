---
name: ieee-response
description: >-
  Draft the two letters an IEEE submission needs — the point-by-point response to reviewers and
  the cover letter to the editor — so every comment is answered, every change is traceable to the
  revised manuscript, and the tone stays cooperative without conceding more than the evidence
  requires. Use this whenever the user is replying to a review or submitting a manuscript:
  "respond to reviewers", "rebuttal letter", "reviewer 2 says...", "write a cover letter",
  "我要回复审稿意见", "审稿回复", "投稿信", "怎么回复 reviewer". For changing the manuscript text the response
  promises, hand to ieee-writing/ieee-polishing; for new simulations a reviewer demands, hand to
  ieee-experiments.
---

# IEEE Reviewer Response and Cover Letter

Use this skill to turn a set of reviews into a disciplined response letter, and to write the cover
letter that frames a submission for the editor. The response letter is a contract: each reply
states what changed and where to find it.

## Core stance

- **Answer every comment, in order.** No reviewer point is skipped, merged away, or silently
  ignored — even the ones you disagree with.
- **Every "we changed X" must be locatable.** Quote the revised text or cite the section/line; a
  promise with no anchor reads as evasion.
- **Cooperative, not submissive.** Thank, then engage on the merits. You may disagree — back it
  with evidence, not insistence — but concede readily when the reviewer is right.
- **No fabrication.** Do not claim experiments you did not run, results you did not get, or
  citations you did not add. If a request needs work not yet done, mark it `[AUTHOR INPUT NEEDED]`
  and list it — never paper over it.
- **The letter and the manuscript agree.** Anything the response says you did must actually exist
  in the revised PDF.

## When to open extra files

| File | Open when |
|---|---|
| [references/response-structure.md](references/response-structure.md) | Building the point-by-point letter: comment IDs, the triage/action model, reply templates, agree/disagree/defer patterns, traceability, tone |
| [references/cover-letter.md](references/cover-letter.md) | Writing the cover letter for a new or revised submission: structure, contribution framing, editor-facing claims, required statements |

## The triage model (classify every comment first)

```
ACCEPT_TEXT       reviewer is right → make the change, quote it in the reply
SOFTEN_CLAIM      reviewer found an overclaim → narrow the wording, point to the new sentence
ADD_EVIDENCE      needs an experiment/analysis → run it (ieee-experiments) or mark AUTHOR INPUT NEEDED
CLARIFY           a misunderstanding → fix the text that misled, then explain (the fault is usually the writing)
DISAGREE          reviewer is mistaken → rebut with evidence, respectfully, and still add a clarifying line
DEFER             out of scope / future work → acknowledge, justify briefly, note in limitations
```

Disagreement is legitimate but expensive: every DISAGREE should still produce a small text change
so the reviewer sees they were heard.

## Workflow

1. **Extract and number every comment.** Split each reviewer's text into atomic points
   (R1.1, R1.2, ...). One concern per ID, even if buried mid-paragraph.
2. **Triage each** with the model above; decide the action before drafting a word.
3. **Do the work first, write the reply second.** Text edits via ieee-writing/ieee-polishing, new
   results via ieee-experiments. The reply describes work that exists.
4. **Draft each reply** as: thank/restate → what we did → where it is (quote or location). Keep
   the reviewer's words quoted above your response.
5. **Open with a summary** of the main changes and a thank-you to the editor and reviewers.
6. **Check coverage:** every comment ID has a reply; every "changed" has an anchor; no fabricated
   claim; tone consistent.
7. **Write the cover letter** separately (see cover-letter.md) — it addresses the editor, not the
   reviewers, and frames fit and contribution.
8. **Return** the response letter, the cover letter, and a coverage checklist.

## Output format

1. `Response letter:` per-reviewer, numbered, quoted comment + reply (thank → change → location).
2. `Cover letter:` editor-facing, framing contribution and fit (and, for revisions, the headline
   changes).
3. `Coverage check:` table of `Comment ID → action → anchor in manuscript → status`.
4. `Open items:` anything marked `[AUTHOR INPUT NEEDED]` the user must still supply.
