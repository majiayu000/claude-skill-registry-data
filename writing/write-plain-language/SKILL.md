---
name: write-plain-language
description: >-
  Load this skill when writing words a user reads inside the product: labels, empty states,
  onboarding copy, tooltips, confirmation dialogs, CLI help. Trigger on "make this clearer", "plain
  English", "reword this label". Not for error text (use ceh-usability-audit:audit-error-messages).
disable-model-invocation: false
user-invocable: false
license: Apache-2.0
---

# Write in plain language

Clear copy comes from a **floor you can check a word against**, and a list of the things you must
not simplify. The work is done when every harvested string has a row in the rewrite table and the
one-name check has passed.

The failure is rarely that the writer chose a hard word on purpose. It is that the implementation's
vocabulary is the vocabulary they have been living in for weeks, and it reads as ordinary to them.

## Procedure

1. **Harvest the strings.** UI labels and copy from the component/template files, CLI text from
   `--help` and the argument parser, plus any user-facing constants file. Errors are out of scope
   here — route those to `audit-error-messages`.
2. **Run the floor over every string**, then the sentence rules. Most rewrites fall out mechanically.
3. **Check one-name consistency.** The same concept must have exactly one word across UI, CLI, API,
   docs, and errors. Two good names for one thing is still a defect — list every alias and pick one.
4. **Produce a rewrite table**, current → proposed, one row per string. Do not rewrite in place
   without showing the table first; copy changes are cheap to make and expensive to review buried in
   a diff.
5. **Read the result aloud.** It is the only reliable check, and it catches every rule below at once.

## Rules

### The vocabulary floor

**Every word must be one a twelve-year-old reads without pausing.** That is the whole rule. When a
word fails it, swap it — and there is nearly always a shorter word that is also more precise.

| Don't              | Do              |     | Don't                  | Do              |
| ------------------ | --------------- | --- | ---------------------- | --------------- |
| utilize, leverage  | use             |     | authenticate           | sign in         |
| initiate, commence | start           |     | provision, instantiate | create, set up  |
| terminate          | stop, end       |     | configure              | set up          |
| execute            | run             |     | populate               | fill in         |
| modify             | change          |     | validate               | check           |
| prior to           | before          |     | in order to            | to              |
| subsequent to      | after           |     | in the event that      | if              |
| facilitate         | help            |     | is able to             | can             |
| additional         | more            |     | attempt to             | try             |
| require            | need            |     | sufficient             | enough          |
| currently          | now (or cut it) |     | at this time           | now (or cut it) |

Product-specific nouns are worse than verbs, because a swap table cannot fix them. `instance`,
`payload`, `entity`, `resource`, `workspace`, `tenant`, `sync`, `token`, `cache`, `hook`, `job`,
`pipeline` — each is either a thing the user recognizes under a different name, or a concept they do
not have. Name it what the user calls it, and if the user has no word for it, the concept probably
should not be on the surface.

### Sentence rules

1. **One idea per sentence.** Two ideas joined by "and" or a semicolon are two sentences.
2. **Twenty words maximum.** Read it aloud; if you take a breath mid-sentence, split it.
3. **Active voice, user as the subject.** "You'll get an email" — not "An email will be sent".
4. **Present tense.** "This deletes your files", not "This will delete your files".
5. **Second person.** "your project", not "the user's project".
6. **Front-load the point.** The consequence goes first, the qualification second: "Your files stay
   for 30 days, then they're deleted" — not the other way round.
7. **Cut the throat-clearing.** "Please note that", "It is important to understand that", "Simply",
   "Just" — all deletable, and "simply"/"just" additionally tell someone who is stuck that their
   difficulty is unreasonable.

### Define on first use, in the interface

Any domain term that survives the floor — because it genuinely is the user's word, or because there
is no shorter one — **gets defined where it first appears, not in a glossary**. Someone confused by
a word will not go looking for a page that explains it.

```
Bad:   Webhook URL
Good:  Webhook URL
       Where we send updates when something changes. Your server needs to accept POST requests here.
```

One sentence beneath the label. If it needs a paragraph, the concept is too big for this screen.

### Labels, buttons, and numbers

- **Button labels are verbs naming the outcome:** "Save changes", "Delete 3 files", "Send invite".
  Never "OK", "Submit", "Yes", "Confirm". Someone reading only the button must know what happens.
- **A confirmation dialog's buttons must not be "Yes" and "No"** — they must be "Delete forever" and
  "Keep it". The dialog text can be skipped; the buttons cannot.
- **Placeholder text is not a label.** It disappears exactly when the user needs it, and greyed
  text reads as disabled. Always a real, visible label.
- **A checkbox says what happens when it is checked**, phrased positively. `Don't disable
notifications` is unreadable in both states.
- **Give numbers, not adjectives.** "About 2 minutes" beats "Processing". "3 of 7" beats a spinner.
  "Up to 25 MB" beats "large files not supported".
- **Time is relative first, absolute on hover or beside:** "3 hours ago" over `2026-08-01T09:14Z`.
  A reader judges recency at a glance but has to work out a timestamp.
- **Empty states carry the first action as a control**, not as a sentence. "No projects yet" plus a
  **Create your first project** button — not "You can create a project from the menu above."

### Never simplify these

Simplification that removes precision is a regression, not an improvement. These stay exact even
when they read badly:

| Keep exact                                     | Why                                                                                |
| ---------------------------------------------- | ---------------------------------------------------------------------------------- |
| Legal, consent, licensing, and privacy wording | Meaning is the obligation; paraphrase changes what was agreed                      |
| Safety and destructive-action consequences     | "This can't be undone" is the whole message. Softening it costs data               |
| Security wording, and auth failure detail      | Vagueness on auth is deliberate — never say _which_ of email or password was wrong |
| Exact identifiers, versions, paths, commands   | A friendlier rendering of a value the user must copy is a broken value             |
| Exact numbers, limits, and units               | "A few" is not a limit anyone can plan against                                     |
| The actual failing value in an error           | See `audit-error-messages` — the quoted value is the message                       |

Ambiguity is the cost of over-simplifying, and it is a usability failure in its own right. **Say
less, not vaguer.**

## Output

A rewrite table, shown before any string is changed in place:

| Location               | Current                   | Proposed                         | Rule          |
| ---------------------- | ------------------------- | -------------------------------- | ------------- |
| `SettingsPanel.tsx:42` | `Configure sync interval` | `How often to check for updates` | floor, jargon |

## Stop conditions

- **The term is the user's own word.** Accountants say "reconcile"; doctors say "triage".
  Simplifying to a general-audience word makes it _less_ clear for the actual audience → establish
  who the reader is before running the floor.
- **The string is a public contract** — a CLI flag name, an API field, a documented setting key.
  Renaming it is a breaking change, not a copy edit → flag it and route to
  `ceh-python-library:publish-python-library`.
- **The copy is fine and the interface is the problem.** Better words for a step that should not
  exist is the wrong fix → route to `audit-interface`.

## Hands off to

- The string is an error message: `ceh-usability-audit:audit-error-messages`.
- The wording is a symptom of a confusing flow: `ceh-usability-audit:audit-interface`.
- Does a newcomer get far enough to read this at all? `ceh-usability-audit:simulate-newcomer-first-run`.
- It's a docs page, not in-product copy: `ceh-documentation:write-guides-and-runbooks` for a guide
  or runbook, `ceh-documentation:write-concept-docs` for an explanation.
- It's the README first screen or a package description: `ceh-seo:write-project-listing-text`.
- The label is unreadable to a screen reader or has no accessible name:
  `ceh-web-frontend:make-ui-accessible`.
