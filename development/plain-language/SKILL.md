---
name: plain-language
description: >
  Craft text that is easy to understand and engaging for non-technical readers —
  ticket titles/descriptions, QA test steps, release notes, status updates, UI copy,
  and any business communication. Use whenever you are writing for a non-engineer
  audience (QA testers, product, stakeholders, end users), whenever a draft needs a
  "make this less technical" / "say this plainly" / "rewrite this for QA" pass, or when
  another skill asks for plain-language copy (project-manager ticket prose, daily
  tracker comments). Not for scholarly prose — grants/manuscripts want a scholarly
  voice instead. For how a document is structured — who it is for, what it
  argues, and what order the sections run in — pair with information-architecture;
  this skill owns the wording inside those sections.
  Turns engineering detail into clear, friendly, jargon-free prose without losing
  accuracy. Learns the user's voice over time.
---

# Plain language — clear, engaging writing for non-technical readers

Goal: take something true-but-technical and say it so a smart non-engineer (a QA
tester, a product manager, a customer) understands it instantly and stays engaged —
without dumbing it down or making it inaccurate.

## Who you're writing for

Assume the reader is **intelligent but not technical**. They don't know the codebase,
the framework, the API, or the internal jargon. They know the *product* and what users
are trying to do with it. Write to that person.

## Core principles

1. **Lead with the point.** First sentence says what this is and why it matters to the
   reader. No throat-clearing, no "this PR refactors…". Reader should never have to dig
   for the takeaway.
2. **Plain words over jargon.** Replace engineering terms with what the user *sees* or
   *does*. Translate, don't transliterate:
   - "endpoint / API returns 403" → "the page shows a 'not allowed' error"
   - "null state / empty array" → "when there's nothing to show yet"
   - "auth / RBAC / token" → "who's allowed to do this / signing in"
   - "persisted to the DB" → "saved"
   - "the modal renders" → "a pop-up window opens"
   - "VIN-routed update" → name the actual user action instead
   When a technical term is genuinely needed, define it in one short aside.
3. **Concrete, not abstract.** Name the screen, the button, the field, the user role.
   "Click **Save** on the Business Profile page," not "submit the form."
4. **Short sentences, active voice.** One idea per sentence. "You'll see a green
   banner," not "a green banner will be displayed to the user."
5. **Structure for scanning.** Short paragraphs, headings, numbered steps for anything
   sequential, bullets for lists. A wall of text loses people.
6. **Engaging, not stiff.** Warm and direct, like a helpful colleague. A little
   personality is good; corporate filler ("in order to facilitate") is not. Never
   sacrifice clarity for cleverness.
7. **Accurate above all.** Plain ≠ vague. Don't round off the meaning to make it
   simpler. If a detail matters for the reader to act correctly, keep it — just say it
   plainly. When simplifying would mislead, keep the precise version.
8. **Respect the reader's time.** Cut every word that doesn't earn its place. If a
   sentence can go without losing meaning, cut it.

## A quick method

When asked to write or rewrite copy:
0. **Read `LEARNINGS.md` beside this skill, when your copy keeps one, first** — the
   user's voice preferences, approved before→after rewrites, and the jargon→plain
   glossary live there; copy that ignores them gets corrected.

1. Identify the **reader** and what they need to *do* or *decide* after reading.
2. State the **one main point** in a single plain sentence — that's your opener/title.
3. Add only the supporting detail that reader needs, in scannable structure.
4. **De-jargon pass:** reread as if you'd never seen the code. Swap each technical term
   for what the reader observes. Flag anything you couldn't translate.
5. **Tighten pass:** cut filler, split long sentences, switch passive→active.
6. **Engagement check:** would a busy non-engineer keep reading? Is the opener
   compelling? Is the tone friendly, not robotic?

## Titles specifically

A good title is a plain-language headline: specific, action/outcome oriented, readable
at a glance, no internal codenames or file paths. Prefer the user-facing outcome.

- Weak: "Refactor the vehicle service to route through the new backend"
- Better: "Saving a vehicle's details now works for non-VIN updates"
- Weak: "Add validation decorators to the checkout endpoints"
- Better: "Checkout now tells you which field needs fixing"

(This install's original examples: `LOCAL.md` beside this skill, when your copy keeps
one — *Title examples*.)

## Output discipline

- Match the requested **format and length**. A ticket title is one line; a description
  has sections; a status update is a few sentences. Don't over-produce.
- When you simplified something where the precise technical detail still matters for an
  engineer, you may add a short **"Technical notes"** aside at the end — kept separate
  from the reader-facing copy, so the plain part stays plain.
- If you can't translate a term without losing necessary meaning, say so and ask,
  rather than guessing.

## Common failure modes — if you're about to do one of these, stop

- **Shipping untranslated jargon** ("endpoint", "modal", "403", "persisted", a file
  path, a function name) in reader-facing copy — check the glossary in LEARNINGS.md;
  if a term has no plain equivalent, say so and ask rather than guessing.
- **Rounding off the meaning to sound simpler.** Plain ≠ vague; if the simplification
  would make the reader act incorrectly, keep the precise version and say it plainly.
- **Burying engineer detail in the reader-facing body.** It belongs in a separate
  "Technical notes" aside so the plain part stays plain.
- **Describing third-party services by function** ("our payment processor") — reference
  them by brand name (Stripe, Lyft); brand names are clearer to non-technical readers.
- **Over-producing.** A title is one line; a status update is a few sentences. Match
  the requested format and length — extra prose costs the reader time.

## Before you call this done

- [ ] LEARNINGS.md was read first; the copy matches the recorded voice and glossary.
- [ ] De-jargon pass done: reread as a non-engineer; every technical term translated
      or explicitly flagged.
- [ ] The first sentence states the point; sequential content is numbered; the whole
      thing scans.
- [ ] Nothing was made inaccurate by simplification.
- [ ] Engineer-only detail sits in a "Technical notes" aside, not the body.
- [ ] Format and length match what was asked for.

## Related skills

- [project-manager](../project-manager/SKILL.md): ticket titles, descriptions and QA steps are written in this voice.
- [status-update](../status-update/SKILL.md): a status report is a dashboard plus a short TLDR; this skill owns the TLDR's wording.
- [frontend](../frontend/SKILL.md): UI copy (labels, empty, loading and error states) is written here and placed there.

## Capturing the user's voice (session-handoff protocol)

Record voice/tone preferences, approved phrasings, and term→plain-language
translations the user liked in `LEARNINGS.md` beside this skill, when your copy keeps
one. On "update skills" / after a writing task where the user corrected tone or
wording: add the example (before → after), dedupe, and note the context. Read it before writing so future copy matches the
user's established voice. Keep a running **jargon → plain** glossary there for your
product's domain (this install's: `LOCAL.md` beside this skill, when your copy keeps
one — *Glossary domain*).
