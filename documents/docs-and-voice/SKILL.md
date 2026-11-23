---
name: docs-and-voice
description: Where documentation lives (README, docs/RUN.md, the Lean Mean Clean Apps docs site) and the house voice - professional with a dry sense of humour, Australian spelling, humour in prose but never in steps, commands or tables. Use when writing a README, docs page, release note, issue reply or pull request description.
metadata:
  scope: repository
---

# Docs and voice

## The rule

| What | Where |
| --- | --- |
| A short introduction, install, the options table and links | `README.md` and `NUGET.md` (the package page) |
| Running the app, environments, database and tests | `docs/RUN.md`, which also ships in every generated solution |
| Full guides | The docs site, <https://leanmeanclean.dev>, in the `leanmeancleanapps.github.io` repository, with a home page per template |
| How to contribute | `CONTRIBUTING.md` |
| How agents work here | `AGENTS.md` and `.agents/` |

The voice is a small team that knows its stuff and doesn't take itself too seriously: the Lean Mean Clean Apps team, which is Stephen Walsh for now and open to more. Professional first, with the odd dry line.

| Kind of writing | Humour |
| --- | --- |
| Home pages, introductions, explanations, contributing guides | Yes, lightly, one line at a time |
| Guides and reference pages, troubleshooting included | Yes, one dry line in an introduction or a section's prose |
| Steps, commands, tables, error messages, skills | None |

The templates are always listed in the same order: Minimal API, MCP, GraphQL, Web API, Lambda Function.

## Steps

1. Lead with the point. Short sentences, plain words, Australian spelling (behaviour, colour, initialise).
2. Show the command or the code instead of describing it.
3. Change the docs in the same pull request as the behaviour they describe.
4. Guides go to the docs site repository, not into this repository.
5. Release notes come from pull request titles, so write titles as plain sentences about the change.
6. In an options table, put an option's long and short form on separate lines, `--name`<br>`-n`, never `--name`, `-n` on one line where it can wrap in the middle. `NUGET.md` gives the short form its own column instead, because NuGet doesn't render HTML.

### Accessibility

Everything we write aims for WCAG 2.2 AA, the same as the [accessibility statement](https://leanmeanclean.dev/accessibility/).

| What | Rule |
| --- | --- |
| Images | Alt text that says what the image tells you. A decorative image gets `alt=""` |
| Links | Text that makes sense on its own, never "here" or "this link" |
| Headings | One `#` per page, then in order, without skipping a level |
| Colour | Never the only way to say something. Pair it with a word, a label or an icon |
| Tables | A header row, and no empty first cell |
| Demo videos | A text description of what the video shows next to it, and captions if it has narration |
| Messages the code returns | Say what went wrong and what to do next, in plain words |

## Don't

- Use marketing words ("blazing fast", "revolutionary", "seamless").
- Put jokes in steps, commands, tables or error messages, or let one bend a fact.
- Duplicate a guide from the docs site in the README.
- Write in the first person singular; it's "we" and "the team".
- Use "click here", "see below" or a colour on its own to point at something.

## Check

- Read it out loud. If a sentence needs a second breath, split it.
- Every image has alt text, every link makes sense out of context, and the headings go in order.
