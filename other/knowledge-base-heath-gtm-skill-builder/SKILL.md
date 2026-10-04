---
name: knowledge-base
description: Build the operator knowledge base future-you and any AI can actually search. Capture facts, playbooks, stakeholders, and how-tos as plain greppable markdown, organized so the answer is a search away instead of a memory or a Slack scroll. Trigger on "start a knowledge base", "write this down somewhere findable", "document how we do this", "who owns what again", "capture this for later", or any fact you have now looked up more than once.
---

# Knowledge Base

## What this does
Turns the facts you keep re-deriving into a knowledge base you and your tools can search. It captures four things: facts (the stable truths), playbooks (how a repeated thing gets done), stakeholders (who owns what), and how-tos (the specific steps). It writes them as plain markdown, organized and cross-referenced, so the next time you or an AI needs the answer, it is one search away. A thing you have looked up twice belongs here.

## What you'll need
You do not need to connect anything to get value today. Paste what you know and the skill structures it. Connect the tools below and it maintains the base as a living, greppable store.

- Works today with: whatever you can dump, notes, a thread, a list of who-does-what. It sorts it into the four types and structures each entry.
- More powerful connected to a repo: the base lives as markdown files you can grep, diff, and review.
- Sharper with a notes or wiki tool: entries land where your team already looks.
- Sharper with a decision log or context pack: they cross-link, so a fact points to the decision that set it.

## How this runs at your connection level
This skill is never reliant on a connector. It structures what you give it and gets more durable as you connect somewhere to keep it. It never writes or overwrites an entry without approval.

- **Bring your data**: paste the raw material. The skill sorts, structures, and cross-links it today. No connection required.
- **Connect your tools**: it writes the entries as files, keeps the index current, and flags duplicates, once you approve each change.
- **Just exploring**: nothing to capture yet? Get the four entry templates and a worked example, so the structure is ready when you are.

Every run ends with the one entry most worth adding next, usually the fact you just looked up again.

## Customize this for yourself
This was built for an operator tired of re-finding the same answer. Set these to your world:

| Set this | What it is | Default / Example |
|---|---|---|
| KB_HOME | where the base lives | a git repo, /kb; a notes/wiki tool |
| ENTRY_TYPES | the categories you keep | facts, playbooks, stakeholders, how-tos |
| NAMING | how files are named | type-slug.md, lower-kebab-case |
| INDEX | the front door | a README that lists and links everything |
| REVIEW_CADENCE | when entries get re-checked | quarterly, or on change |
| OWNER_FIELD | who is accountable for an entry | you, by default |

The four types cover most of what an operator forgets. Add or rename to fit. The rule that it stays plain and searchable does not change.

## The method

### Sort by type
Every capture is one of four things. A fact is a stable truth ("the trial is 14 days"). A playbook is how a repeated process runs. A stakeholder entry is who owns what and how to reach them. A how-to is the steps for a specific task. Mixing them is why old wikis rot; keeping them separate is why this one stays usable.

### Greppable structure
Plain markdown. Consistent headings. A predictable filename. So a search for a term lands on the entry, not near it. No entry hides inside a screenshot or a table nobody can grep.

### The index is the front door
One README lists every entry, grouped by type, each a link. If it is not in the index, it does not exist. The index is maintained on every add, not once a year.

### Cross-links over duplication
A fact that a playbook depends on is linked, not copied. One source of truth per fact. When it changes, it changes in one place. The skill flags a would-be duplicate instead of writing it.

### Freshness, not just capture
Every entry carries a last-checked date and an owner. Stale knowledge is worse than none, because it is trusted. The base surfaces what is overdue for a look.

## Quality gates
- Nothing is written or overwritten without your explicit approval, per entry. The skill drafts; you place it.
- No duplicate facts. A would-be duplicate is flagged and linked to the existing source, not written again.
- Every entry has a type, an owner, and a last-checked date. An undated fact is a trap.
- The index is updated whenever an entry is added. An orphan entry nobody can find is not knowledge.

## Output (example)
```
KNOWLEDGE BASE · proposed additions · 3 entries

FACT  ·  trial-length.md
  The standard trial is 14 days. Owner: you. Last checked: today.
  Linked from: onboarding-playbook.md

PLAYBOOK  ·  new-signup-routing.md
  How a signup gets routed to an owner (5 steps). Owner: you.
  Depends on fact: company-size-bands.md (linked, not copied)

STAKEHOLDER  ·  eu-signups-owner.md
  UNRESOLVED. No named owner for EU signups yet. Flagged, not invented.

INDEX UPDATE
  + 3 entries added to README under Facts / Playbooks / Stakeholders

(all drafts. approve to write; the EU owner stays blank until you name one)
```

## Where the inputs come from
ENTRY_TYPES and REVIEW_CADENCE are defaults, not laws. Some operators add a "glossary" type or a "vendors" type; some review monthly, some on change only. The four types are the starting set because they are what an operator forgets most. Reshape the categories. Keep it plain and greppable.

## Example chat
Here is the skill running on a real capture, start to finish.

**You:** Start a knowledge base from this thread. We keep re-explaining how EU signups get routed.

**Claude:** Sorted into three entries, one flagged unresolved.
```
FACT · trial-length.md
  The standard trial is 14 days. Owner: you. Last checked: today.

PLAYBOOK · new-signup-routing.md
  How a signup gets routed to an owner (5 steps).

STAKEHOLDER · eu-signups-owner.md
  UNRESOLVED. No named owner for EU signups yet. Flagged, not invented.
```
The catch worth naming: I didn't invent an owner for EU signups just to fill the slot. That's the entry most likely to rot into a wrong answer if I'd guessed, so it stays blank until you name someone. One sharpener: connect a repo so these live as files you can grep and diff, instead of living in this one chat.

## Go further
The capture is step one. Here is where an operator takes it once the manual version proves out.

- **Catch facts the second time you look them up.** Wire a scheduled Claude task to scan your Slack search history weekly for repeated questions, and draft a KB entry for anything asked twice.
- **Keep the index honest.** Run a monthly freshness check against the last-checked date on every entry, and post the overdue list to Slack for the named owner.
- **Make it queryable by the whole team.** Sync the base into Notion or a wiki tool so any AI agent your team runs (a support bot, a sales assistant) reads from the same source of truth instead of guessing.

You built the base once, now it stays the place people actually check first.


## Make it yours
Fork it. Add types, change the naming, wire the freshness check to a reminder. Cut what your work never needs. The point is that the second time you look something up, you find it instead of re-deriving it. Built by an operator. Customize it, break it, make it better.
