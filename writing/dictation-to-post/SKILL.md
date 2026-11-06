---
description: Turn an agreed dictation into a post — the same argument as written text, following the recording but free to supply a link the speaker left unsaid. Writes writing/<project>/drafts/<slug>.md with the copy-exact text and a table of every place the draft departs from the recording. Invoke as `/dictation-to-post <dictation file>`. Use when the operator says "сделай из этого пост", "напиши текст по диктовке", or asks for the written version of something already transcribed.
---

End state of this skill: `writing/<project>/drafts/<slug>.md` holds the post as
copy-exact text, plus a table naming every place it departs from the recording,
so the operator can put any of them back.

**It runs on an agreed dictation**, never on the raw response and never on a
transcript the operator has not been through. What this skill may change is
bounded by the recording, so a recording that is still wrong makes a post that
is wrong in the same places without showing it.

## What the post is bound to, and what it is not

The video is bound to the recording word for word: the words on screen are the
words spoken, which is what `@.claude/skills/dictation/SKILL.md` verbatim mode
protects. **A post is not bound that way.** It goes by the text — same order,
same argument, the speaker's own phrasing wherever it survives on paper — and it
may supply a sentence that was not said where the argument genuinely needs one.

"Genuinely" is the whole bar, and it has a shape. A licensed addition restores a
link the recording assumes and skips: a step the speaker plainly reasoned
through and did not voice, usually because in speech the next image carried it.
An unlicensed one is your opinion arriving as theirs, however good. The test is
whether the speaker, reading the sentence, recognises it rather than considers
it.

The other direction is narrower. **Speech repeats on purpose and writing does
not**, so a phrase said three times for rhythm can stand twice on a page — but
cutting a digression, merging two paragraphs or tightening a loose sentence is
not this skill's licence. A post that reads better than the recording has
stopped being the same piece.

## The draft file

- **A header line** — which dictation, which channel, status: yours
- **The post**, in a `text` fence — the deliverable
- **`## Швы`** — the departures, one row each: yours, and the reason this skill
  can be trusted
- **`## Открытые вопросы`** — anything the draft could not settle: yours, and
  only where a real question is open

**The post text is copy-exact**, per `@writing/CLAUDE.md` § "A draft's post text
is copy-exact": one unwrapped line per paragraph inside a `text` fence, because
a hard wrap in the source becomes a line break in the feed.

**The seams table is the point.** One row per departure: where it is, and what
was done — added, cut, or repeated less. A draft that quietly reads well gives
the operator nothing to push back on, which is the failure this table exists to
prevent, exactly as the dictation's own table of guesses does. It is transient
in the same way: a row they have ruled on comes out, and when the last goes, so
does the heading.

## The conclusion is not yours to add

Where the recording stops at the question, the post stops at the question. This
is the one place where supplying the missing link is forbidden, because it is
not missing: a link the speaker reasoned through and left unvoiced is theirs to
restore, and the conclusion they did not reach is yours, arriving in their
voice. It is also the one departure the seams table cannot make good — a row
saying "the moral is the agent's" leaves a post whose position nobody holds.

## Do NOT

- Write from the recording's audio or the recognizer's output. The agreed
  dictation file is the source.
- Add a conclusion, a moral, or a closing summary the speaker did not reach.
- Improve a sentence that is merely loose. That voice is the thing being kept.
- Leave a departure out of the seams table. An unlisted one is a silent rewrite.
