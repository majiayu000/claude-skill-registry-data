---
name: writing-bible
description: "World bibles, series bibles, and story canon: build and maintain the canonical source of truth for a fiction project — people, places, systems, timeline, who-knows-what — with a consistency ledger and retcon log. Use when the user mentions a world bible, series bible, story bible, lore, canon, worldbuilding, character sheets, or tracking continuity across books, chapters, or episodes; or when writing and a fact about the world must be checked or recorded."
---

# Bible

The bible is the project's **canon**: one fact, one home. Its job is that chapter
nine never contradicts chapter two — and that you never re-derive the world from
a stale summary.

Three disciplines make it work:

- **Canon discipline.** Each fact lives in exactly one entry. Established,
  planned, and disputed facts carry different status tags; only _established_
  is binding on prose.
- **Entries on demand.** Write the entry when the story needs it, not to
  "complete the world". A bible that grows from scenes stays load-bearing; a
  bible generated wholesale becomes decoration nobody reads.
- **The iceberg.** The bible may hold ten times what surfaces in prose, and
  should — depth is what makes prose feel lived-in. But background that never
  serves a scene, an arc, or a theme gets tagged `background`, so it never
  forces its way into the prose as an info-dump.

## Workflow

1. **Pick the frame.**
   - _Canon ledger_ — a lean, growing file of established facts only. Right for
     a short story or a WIP with no world doc yet. Start here for most projects.
   - _World bible_ — full scaffolding: geography, cultures, systems, history.
     Right when the setting itself carries the story (SFF, epic, mystery with
     red herrings that must be fair).
   - _Series bible_ — people-first: leads' arcs, voice, running threads,
     episode/book summaries, the promise ledger. Right for sequels and serials.
     Grow up as the project grows; migrating a ledger into a bible is cheap, a
     wholesale regeneration is how canon gets silently rewritten.
2. **Scaffold the file** from the templates in
   [references/entry-templates.md](references/entry-templates.md). Every entry
   carries: status (`established` / `planned` / `disputed`), first appearance,
   and a one-line job ("what story work this does").
3. **Capture canon as it happens.** Any fact committed in prose or agreed in
   planning goes in during that session, not later. An entry written "when there
   is time" is an entry that gets contradicted first.
4. **Check before you commit.** New fact lands → search the bible for collisions
   with established entries. Collision: surface it, propose which side yields,
   and log the decision in the retcon log. The bible is allowed to change; it is
   not allowed to change silently.
5. **Keep the ledgers current** (next section). They are the bible's active
   parts; the entries are its memory.

## The ledgers

**Open questions** — what the project has promised but not answered, each with
where it was raised and the intended payoff point. Promises without a row here
get dropped; that is how mystery boxes rot.

**Who-knows-what** — per character (and the reader), the facts they hold, with
the chapter each was learned. Dramatic irony, mysteries, and any reveal live on
this ledger; a plot turn that requires someone to know something they haven't
learned is the classic outline bug this catches.

**Retcon log** — what changed, when, and the blast radius: every place the old
fact appeared and still needs a fix. A retcon without a blast-radius list will
be re-broken by the next draft.

**Timeline** — events with in-world dates or era anchors, so relative mentions
("two winters after the flood") stay checkable.

## What goes in an entry

Template skeletons live in
[references/entry-templates.md](references/entry-templates.md); the principle:

- **People**: want, need, the lie they believe, voice (speech tells), key
  relationships, and the arc's shape — plus what changed for them in each
  appearance. Voice entries are what keep a six-book narrator from drifting.
- **Places**: what it does to the people in it (mood, light, cost of living),
  who runs it, what it costs to enter or leave.
- **Systems** (magic, tech, politics): what it _cannot_ do, what it costs, who
  knows it exists. Limits are the story engine — power without cost solves
  plots instead of creating them.
- **Cultures**: values, taboos, texture of daily life (food, money, weather,
  work). This is where prose texture comes from.
- **Events**: what happened, who remembers, what it set in motion.

## Working with the other skills

- `writing-outline` feeds promises and character data in; the bible's open
  questions and who-knows-what feed structure back.
- `writing-draft` consults the bible before writing into an established area and
  files every newly established fact back to it in the same session.
- The bible never edits prose. Canon disputes between a draft and the bible are
  surfaced, not silently resolved: name the collision, recommend a winner, let
  the user rule.
