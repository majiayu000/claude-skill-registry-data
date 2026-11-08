---
name: write-a-skill
description: Creating a new skill — one with no law above it — a showcase, a generator, a third-party service, a working technique of this tree. Load when asked to create, write or rewrite a skill. The shape of a rule and a pattern is not here — that is pattern spec-driven-rule.
---
<!-- rt-kit v0.34.0 · skills/write-a-skill.md · d47ecf64004b · правится надстройкой, не здесь -->

# How a skill is created

A skill is what the agent loads before work and reads in full. Everything else follows: it is
short, it declares when to load it, and it does not retell what is already written in the
neighbouring one.

## When to use

- A skill with no law above it is being created: a showcase, a generator, work with a
  third-party service, a technique adopted in this tree.
- A skill has grown, and it is time to split it.
- The skill exists, but nobody loads it — the declaration needs fixing.

**A rule and a pattern do not go here.** A rule stands under a law, a pattern next to a rule,
and the shape of both is held by the pattern `spec-driven-rule`. A skill without a law is the
third case, and only it is here.

## Order

1. **Ask what is missing.** What work the skill covers, where people stumbled without it,
   whether ready-made commands are needed or an order of actions is enough. A skill written
   without this retells the tool's documentation — and the agent knows that anyway.
2. **Write a draft.** One file. Additional ones — only when the first stops being readable in
   full.
3. **Show the owner.** A skill acts on all future sessions, and creating it silently is not
   allowed.

## When the owner hands over the text

A text the owner wrote is carried, not rewritten. Before the first split it lands whole in the
task folder: a request cut with `[…]` leaves nothing to compare against. Headings keep their case
and wording, sentences their words, code samples stay whole. What the shape of a skill forces —
the declaration, "When to use", a link in place of "above" — goes into a list of deviations, one
line each. Before the first commit a script compares every heading and paragraph of the source
with the skill files and prints what is missing or changed. A size limit the text does not fit
splits the text into files, never shortens it.

## What is in the file

```
<skill-name>/
├── SKILL.md          # mandatory, and usually the only one
├── <SOMETHING>.md    # a separate file — when SKILL.md stopped being readable in full
└── scripts/          # ready-made scripts, if the operation is deterministic
```

The preamble between `---` is `name` and `description`, then the title and the sections. The
first section is "When to use": the agent decides by it, not by the title.

## The declaration decides everything

`description` is **the only thing the agent sees** when it decides whether to load the skill or
not. It stands in the system prompt next to the descriptions of all the others, and the choice
goes by them.

It answers two questions: what the skill gives and when to load it. Write in the third person,
up to three hundred characters: the first sentence — what it does, the second — "Load when…", the
third — what is not in it and where to look for that. Where the tree has the descriptions check
laid out, it refuses a longer declaration.

```
✓ Creating a new skill — one with no law above it. Load when asked to create, write or
  rewrite a skill. The shape of a rule and a pattern is not here — that is pattern
  spec-driven-rule.

✗ Helps with skills.
```

The second declaration gives the agent no way to tell this skill from the neighbouring one —
and it loads neither.

The line "what is not here" is not decoration: there are dozens of skills in the tree, and half
of the wrong choices are the neighbour taken instead. Name it by name.

## Ready-made commands instead of a description

A script is put next to the skill when the operation is deterministic — a check, bringing to a
form, parsing output. Such a thing is cheaper to call than to generate anew, and an error in it
is seen once, not in every generation.

An order of actions that depends on what was found does not become a script: it stays text.

## When to split

Split when:

- the file stopped being readable in full — by experience, that is around a hundred lines;
- it holds two different subjects, and the second is needed once a month;
- ready-made code took more room than the explanation of what it is for.

Do not split for beauty: two files instead of one cost one extra hop at every reading, and a
link deeper than one level is not followed at all.

## How a skill does harm

- **Retelling the tool's documentation.** The agent reads the skill at every piece of work; a
  line it knows anyway pushes out the one it does not.
- **Duplicating a neighbour.** Two skills about one thing start to contradict each other, and
  the first to notice is whoever has carried out both.
- **What goes stale together with the code.** A skill naming a version, a number or a file name
  that is edited more often than once a quarter lies silently.
- **Length.** A skill of three screens stops being read in full and is read up to the first
  familiar section.

## Before handing it over

- [ ] the declaration has "Load when…" and names the neighbour not to load;
- [ ] the first section is "When to use";
- [ ] the file is readable in full in one sitting;
- [ ] not one line repeats the neighbouring skill;
- [ ] nothing that goes stale by itself: versions, numbers, dates;
- [ ] at least one ready-made sample, not only an explanation;
- [ ] links go one level deep, no deeper;
- [ ] where the tree has the descriptions check laid out, it is green before the first commit,
      not only before the push.

## So that the skill gets loaded

Writing it is not enough: a skill nobody opens does not act. A new skill is either named in the
gate map of this tree, or called by name by another skill or a role. A skill named nowhere stays
a decoration.
