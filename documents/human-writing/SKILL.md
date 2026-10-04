---
name: human-writing
description: >-
  Write documents in a plain, human voice and remove phrasing that reads as machine-generated.
  Use this skill EVERY time you produce a written artifact meant to be read by a person:
  READMEs, official documentation, design or planning docs, summaries, reports, proposals,
  release notes, changelogs, commit messages, GitHub issues, pull request descriptions,
  letters, emails, blog posts, and similar deliverables.
  Trigger it whenever the task is "write/draft/generate a doc" rather than answering a question in chat.
  Do NOT trigger it for direct conversational replies, inline explanations, or code.
  Run it in two passes: write the document, then re-read the finished draft
  and rewrite anything that signals a machine wrote it, presenting only the corrected version.
---

# Human Writing

When generating a document a person will read, write in a plain voice and strip out phrasing that reads as machine-generated.
Rely on your own judgment of what sounds artificial.
The examples below calibrate that judgment; they do not bound it.

Scope: apply this whenever the text will live outside this conversation and be read later.
Skip it for direct chat answers, inline explanations, and code.

## Pass 1 — Write

Draft plain and direct on the first attempt: short words over long ones, concrete nouns, claims backed by specifics, and no filler whose only purpose is to sound thoughtful.
Do not emit a default draft with the intent to clean it afterward.

## Pass 2 — Audit and rewrite (always run)

Re-read the finished draft and rewrite every construction that signals a machine.
Common tells, for calibration:

- Em dash as a dramatic pause. Replace with a period, comma, parentheses, or "and".
- Semicolon used as a soft period. Replace with a period or "and".
- Negation flip ("it's not just X, it's Y"). State the claim directly.
- Filler openers: "it's worth noting", "in today's fast-paced world", "when it comes to", "at the end of the day", "in conclusion". Cut them.
- Overused vocabulary: delve, leverage, robust, seamless, myriad, foster, harness, unlock, ecosystem, and similar. Use the plain equivalent.
- Fake-inclusive or fake-range openers: "whether you're X or Y", "from X to Y". Address the specific case instead.
- Compulsive three-item lists, decorative bold, and unrequested emoji. Remove.

Apply judgment beyond this list.

## Output

Present only the corrected artifact. Do not show the pre-audit draft, do not show both versions, and do not narrate the edits.
