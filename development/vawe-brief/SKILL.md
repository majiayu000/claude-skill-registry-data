---
name: vawe-brief
description: "Plan an HTML to video film (motion graphics as code). Turn a film request into films/<name>/brief.md: ask the person for the details that make a good film (subject, message, what to show, look), then write the brief in the measured anatomy and name the first draft command. Load when a person asks for a film and no brief.md exists yet."
effort: medium
license: Apache-2.0
---

# vawe-brief: the interview, then the brief

When you talk to the person, use plain words: describe what the viewer sees, not the harness terms (map: harness/lib/plain-words.mjs).
Run this skill inside a vawe checkout: `AGENTS.md`, `taste/` and `bin/vawe` live there. With no checkout, get one: `git clone https://github.com/vawe-hq/vawe.git && cd vawe && npm install && bin/vawe-dev doctor`.

A better film comes from a better prompt, and a better prompt comes from asking the person for the
details a thin request leaves out. This skill runs that interview once, at the start, and writes the
brief. Ask only for missing details while you write it. Once the Board is filled, show the plan and end with "If you like it, type /vawe-approve".

## 0. Ask for the details

```bash
bin/vawe new <name> --request "<the ask>" --questions-json
```

This writes nothing. It prints the open details as `calls`, each call at most 4 questions in the shape of
the AskUserQuestion tool (required details first). The list is `DETAILS` in
`harness/lib/measured-brief.mjs`; do not keep a copy. Call AskUserQuestion once per call, in order, with
that call's `questions` as given. Map each answer (the chosen label without "(Recommended)", or the
"Other" text) to a `key: value` line in an answers file, the key being the header in lower case. Then run
the `answer_with` command:

```bash
bin/vawe new <name> --request "<the ask>" --answers <file>
```

If the person answers "you decide", or no person is there (hill-climb, CI), run `bin/vawe new` with
`--defaults` instead: it guesses each open detail and names which.

When the request is thin, add one more call before the answers file: offer 2 or 3 ideas for the key beat as one AskUserQuestion question (each idea is an option with its device and a one-line description, the least typical one marked Recommended). Make the ideas with `guides/IDEATE.md`; the pick goes in the film's `film` row of the brief's `## Ideas` table.

## 1. Pick the template

`guides/ROUTING.md` maps the request to a film type and a `prompts/<t>.md`. Two
rules of thumb: a real product from a URL is `brand-launch-from-url`; a song that exists is
`music-video-beat-synced`; a reference mp4 is `reference-rebuild`; no brief at all is
`showreel-one-liner`. Under 15 s most types are one continuous action.

## 2. Start the film

```bash
bin/vawe new <name> --from prompts/<t>.md --answers <file>
```

It prints the template's question bank (five questions, each with its default and its reason, in
the order they change the film) and writes `films/<name>/brief.md` with every default filled in and
marked `[unanswered: default taken]`, and the measured-brief sections with guesses marked `(guess: change me)`.

Before you fill the directions, read `taste/build/DIGEST.md`: one thread, three materials, a hero that is not an attractor.
Show the three to the person with `bin/vawe frame <page> --directions` (one board, the same lines per direction), then write `picked:`.

## 3. Template questions

The template's bank is for what step 0 did not cover. Do not ask it again: take each default. Replace each marker with the answer or keep the default and
delete the marker. Never reopen a question; a wrong default is fixed at the critique.

## 4. Write the brief

`brief.md` already has the measured brief's shape (`prompts/ANATOMY.md`): task, directions, look, spec,
acceptance, gates, pitfalls, deliver. Every field the request did not answer holds a guess marked
`(guess: change me)`. Replace each guess with a number:

- **look**: hex for ground, ink and accent, typeface and weight, cap height as a percent of frame height.
- **spec**: the Shots, Words and Objects tables (times in seconds, positions as a percent of the frame).
  Start a 20 to 30 s film from a RECIPES.md chain, and turn its `invent` row into the film's own moment.
- **acceptance**: pre-filled; keep the rows, fill the measured value after each draft.

A director's brief (a music video, a story) may leave the tables to the first draft; it keeps task,
acceptance and gates (`prompts/ANATOMY.md`, "When a director's brief wins").

## 5. Name the first draft

End the interview turn with the one next command:

```bash
bin/vawe dev films/<name>/page.html
```

Then load `vawe-page` to write the page, and `vawe-critique` in a fresh session to look at it.

## Gotchas

- A default is a real value, never "ask again". If a template default does not fit, say the value
  you took and why, in the brief.
- Ask each unanswered detail once, in one message. The next step is the draft, not a second round.
- A brief with no anchor in its direction reads as a template; name the genre or the reference.
- `films/<name>/brief.md` is a per-film artefact, not doctrine.
