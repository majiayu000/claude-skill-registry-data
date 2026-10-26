---
name: facilitator-create
description: "Use when a project's leadership board opens and the project has no facilitator skill, or when a person asks for one or for the product's vision to be written down. Produces the project's `facilitator-<app>` skill (the vision, the principles and red lines the leadership board's facilitator rules by), drafted from the product as it is and settled through an interview. Not for running the board (the orchestrate skill's leadership board), the roadmap's slots (roadmap) or the project's code conventions (write-conventions)."
---

# Create the facilitator skill

**One thing is produced**: the project's `facilitator-<app>` skill, in its local skills folder, never the
plugin. The leadership board's facilitator session loads it, with the `orchestrate` skill's
`references/authority-roles/facilitator.md` for how it rules. **Stop if one exists**: update it on the
person's yes instead.

## Read the product as it is

- **What the product says it is**: the README, the roadmap and its iterations' outcomes, the
  foundation reference.
- **What it does**: the code's surfaces (screens, API, CLI), its boards and prototypes, its plans'
  stories.
- **What was already decided**: the leadership board's decision register, if any.
- **The conventions file, for context only**: the vision and principles never come from it. A rule
  there is how the code is kept, not what the product is for.

## Draft, then interview

**Draft the vision whole**, a recommendation in every place, each line citing what it came from:

- **for whom**, and the problem the product ends for them;
- **what it will never be**;
- **its bets** against the alternatives;
- **its principles**: what wins when two good ideas conflict;
- **its red lines**: what no ruling may cross.

**Then the `interview` skill on the draft**, one open point at a time; the person's words replace
the draft's. A line they do not confirm is left out.

## The skill

**`facilitator-<app>/SKILL.md`** written to `references/facilitator-skill-template.md`, read before the first line,
shown whole and written only on the person's yes. Link it from the roadmap's *Links* (the
`roadmap` skill).

**It grows**: a ruling the person upholds that sets a principle, or one they overturn that shows a
wrong one, is proposed into it at the board's close, on their yes.
