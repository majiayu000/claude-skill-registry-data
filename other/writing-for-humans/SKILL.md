---
name: writing-for-humans
description: Write or rewrite prose that people will read (replies, docs, READMEs, commit and PR text, messages, reports) so it is clear, specific, and free of AI tells while keeping the writer's voice. Apply by default to final replies unless told to skip. Routes to Strunk for structure, the seven anti-slop rules for register, and voice and genre checks for fit.
---

# Writing for Humans

Use this skill for prose people will read: replies, docs, READMEs, PRs, commits,
issues, email, Slack, and reports. Leave code, config, data, quoted text, front
matter, and structured output unchanged. Keep a format the user requested.

This skill routes to three references. Read them as files rather than invoking
them through the Skill tool. Strunk and the anti-slop rules sit beside this
skill in the core plugin:

- [`../writing-clearly-and-concisely/`](../writing-clearly-and-concisely/):
  Strunk's *Elements of Style*, for sentence and paragraph structure. Its full
  text is about 12,000 tokens.
- [`../write-for-humans/`](../write-for-humans/): the seven anti-slop rules,
  voice preservation, a pattern catalog in `REFERENCE.md`, and a
  `prose-humanizer` subagent for long rewrites.

Better Writing provides audience and genre fit, voice dials, genre tells and
exemptions, an anti-slop audit, and a delivery preflight. It comes from a separate
plugin. Resolve `better-writing` through the client's current skill catalog and
read its `SKILL.md`; resolve its reference files relative to that skill. Do not
assume its cache directory or plugin namespace. If it is unavailable, complete
the structure and register passes; identify the missing fit pass when it matters
to the requested edit.

Relative paths beginning with `../` start at this file. A bare filename in a
step is relative to the sibling skill that step names.

## Short pass: ordinary replies

Edit from memory. Do not load references for a normal reply. Keep the author's
meaning and voice; then return the edited text without a preamble.

1. Lead with the answer. Remove openers, closers, throat-clearing, and sentences
   that announce what the next sentence will say.
2. State the positive claim directly. Remove negative parallelism such as
   “not X, it's Y” and “not just X but Y.”
3. Replace inflated words (such as *pivotal*, *crucial*, *robust*, *seamless*,
   *testament*, and *landscape*) with a fact or remove them.
4. Prefer plain verbs: use “is,” “has,” or “does,” or turn a noun back into its
   active verb.
5. End sentences at the fact. Remove editorializing “-ing” endings.
6. Earn adjectives and em dashes. Use no more than two em dashes per page; omit
   bold-label bullets, decorative Unicode, and emoji unless the medium expects
   them.
7. Vary sentence rhythm. Use at most one tricolon in a short piece; break
   repeated openings and ornamental variation.

Before returning, check that the first sentence makes a claim, the ending adds
no recap, and no edit changes meaning or voice. Remove any remaining inflated
word, negative parallel, or editorializing ending.

## Full pass: drafts for editing or publication

Use this sequence for documents, rewrites, and anything the user will edit or
publish. Finish each pass before moving to the next.

1. **Structure.** Read `../writing-clearly-and-concisely/SKILL.md` for its rule
   list. Load `elements-of-style.md` only for a long document or when a
   structural problem needs the source. Prefer active voice, one topic per
   paragraph, the topic first, needless-word cuts, and emphatic endings.
2. **Register.** Read `../write-for-humans/SKILL.md` and apply its seven rules
   in order. For heavy slop or a long draft, read `REFERENCE.md` for the full
   catalog, or dispatch `../write-for-humans/agents/prose-humanizer.md` with
   the draft when context is tight.
3. **Fit.** When audience, channel, or genre matters, or the user asks to
   “humanize,” “de-AI,” or make text sound less like a bot, read
   Better Writing's `SKILL.md` at the location found in the client catalog. Set
   the read (genre, audience, tone, outcome) with its
   `references/voice-and-context.md`; check genre exemptions in
   `references/genre-tells.md`; finish with `references/preflight.md`.

For rewrite mode, read the whole draft, judge whether the slop is light or
heavy, cut first, then rewrite. Compare the result with the original and revert
edits that change meaning or flatten the writer's voice.

## Voice and accuracy

- Simplify and subtract. Do not add facts, quotes, names, numbers, next steps,
  or opinions absent from the source.
- Keep the author's rhythm, contractions, first person, swearing, rough edges,
  and lowercase style.
- Editing is not fact-checking. Flag a doubtful fact in a note; do not silently
  correct it.
- Preserve code identifiers, API and product names, regulatory terms, and
  exact UI labels.
- When two edits work equally well, choose the shorter one.

## Tables in narrow displays

For terminal output, TUIs, chat transcripts, and narrow panes, keep tables
readable: shorten columns, split wide tables, or use a list when a table wraps.
Rendered Markdown files can use ordinary tables with short column names.
