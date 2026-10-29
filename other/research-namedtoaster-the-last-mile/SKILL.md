---
name: research
description: Answer a question by searching the project's own docs and code first, then official sources, and file the dated, sourced answer where it will be read again. Adds to an existing doc before creating a new one, marks anything unverified, and keeps a one line summary with the headline finding in the rules file's Docs index. Gives a short answer in chat first. Use when the user asks to research, look into, compare options for, or find out how something works before deciding or building.
---

# Research

Answer the question, then file the answer where someone will find it next time.

Most research docs are written once and never opened again. In one shipped app,
108 of 134 research docs were never touched after the day they were written. What
got read was the one line summary in the rules file's Docs index, because the rules
file is loaded every session. So the index line matters more than the doc. Write
both, and write the index line as if it is the only thing anyone will read.

Do not write app code during research. If the answer says to change something, say
so and let the user decide.

## 1. Pin down the question

Restate the question in one sentence, and the decision it should inform. If the
question is too vague to answer (for example "look into payments"), ask one short
question to narrow it. Otherwise start.

## 2. Look at what the project already knows

Before searching the web:

1. Read the **Docs** section of the rules file (`CLAUDE.md` or `AGENTS.md`).
2. Search the docs folder and the root docs for the topic and its synonyms:
   `grep -ril "<term>" docs/ *.md`. Try two or three words, not one.
3. Search the code for the feature or library involved.

If an existing doc already answers the question and its date is recent enough for
the topic, answer from it, cite it, and stop. Say how old it is. Store rules, prices
and library versions go stale in months; product reasoning lasts longer.

## 3. Research

Sources, in this order of trust:

1. **Official docs** for the thing in question (the store, the platform, the
   library's own docs and changelog, the vendor's pricing page).
2. **Primary sources**: the library's source code or issue tracker, a release note,
   a test you run yourself.
3. **Secondary sources**: blog posts, forum answers, videos, other people's skills
   and repos. Treat these as leads to check, not as answers.

Rules:

- Cite every claim that matters with a link and the date you read it.
- If a claim comes only from a secondary source, or from memory, mark it
  **(unverified)** and say what would confirm it.
- Prefer concrete numbers: limits, prices, sizes, timings, version numbers.
- When sources disagree, say so and say which one you trust and why.
- Prefer depth on the two or three real options over a long shallow list.
- For store rules or console steps, read the current official page now. Never
  state them from memory.

## 4. Decide where it goes

File into an existing doc whenever one fits. Create a new doc only when nothing
does. Check in this order:

1. **An existing doc on the same topic** found in step 2. Add a dated section, or
   update the old one and note what changed and when. Do not leave two answers
   that disagree.
2. **A doc the answer naturally belongs in**: the backlog item it informs (add
   research notes to that item), the algorithms doc for logic, the rules file's
   **Standing decisions** if the user makes a decision from it, the rules file's
   **Gotchas** if it explains a surprise that cost time.
3. **A new doc**, only if nothing above fits. Use `templates/research-doc.md` from
   this skill's folder. Put it in `docs/research/` with a plain topic name, for
   example `docs/research/push-notification-providers.md`.

Never create an archive folder. Git keeps history.

## 5. Write the entry

Whether it is a new doc or a section in an old one, every entry has:

- **A date** (`YYYY-MM-DD`) on the entry itself, not just the file.
- **The question**, in one sentence.
- **The answer first**: the finding and the recommendation, in two or three lines.
- **The detail**: options, numbers, trade offs, rough effort (small, medium,
  large).
- **Sources**, official first, each with a link and the date read.
- **Unverified**: anything not confirmed, listed plainly with what would confirm it.
- **Open questions**: what is still unknown and who could answer it.

Keep it as short as the answer allows. A long doc nobody reads helps nobody.

## 6. Update the Docs index

In the rules file's **Docs** section, add or update one line for the doc:

```
- `docs/research/push-notification-providers.md`: Provider A is cheapest under 10k
  users and has an Expo plugin; Provider B only wins on rich media (2026-10-11)
```

The line must carry the **headline finding**, not just the topic. "Research on push
providers" is useless; the reader still has to open the file. Include the key
number or the recommendation and the date. If the doc already has a line, rewrite
it so it matches the newest finding.

If the entry went into a doc that is already indexed (the backlog, the algorithms
doc), update that doc's line only if its headline changed.

If the rules file has no **Docs** section, add one at the end with the heading
`## Docs` and the sentence "One line per doc, with its headline number, so the
summary is enough most of the time."

## 7. Answer in chat

Lead with the answer:

1. The short answer and recommendation, in two to four lines.
2. Anything unverified, in one line.
3. Where it was filed: the doc path, and that the Docs index line was added or
   updated.

Do not paste the whole write up into chat. If the user wants the detail, it is in
the doc.

## Do not

- Do not create a new doc when an existing one covers the topic.
- Do not leave an entry without a date or without sources.
- Do not present a blog post, a forum answer or memory as confirmed.
- Do not leave the Docs index line as a bare title.
- Do not commit. The session end skill, or the user, does that.
