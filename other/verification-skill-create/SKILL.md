---
name: verification-skill-create
description: "Use when a project has no verifier for a focus (what is judged, through what) and an agent should from now on judge, alone, the product quality of what is delivered (done as specified, usable, finished): on request, or from the mandate questions of orchestrate-plan when the person says yes. Produces the project's `verify-<app>-<focus>` skill, proven by one quality pass. Not for a focus that has one (its verify skill adapts itself), running a pass (the project's verify skill), tests, code quality or review."
---

# Create a verification skill

**One thing is produced, and a later agent works from it alone**: the project's verifier for one focus, `verify-<app>-<focus>` (plain `verify-<app>` while the project has one only). A project keeps as many as it has focuses, whatever they are; for example: the app judged end to end in its browser, the API judged by its requests, whatever a project's workbench shows judged on it. The skill is short, as a proven project skill is: an agent arriving cold reads it in a minute and works.

**The skill opens on its role prompt and leaves the judging to the agent**: one paragraph that makes the agent the product's quality owner, seen through expert roles (a web product's UI/UX expert and art director among them). Written as `references/role-prompt.md` says, read before the first line, with the surface's roles from its harness reference.

**The verify skill validates the product, never the code.** It reaches and judges everything through the surface the consumer uses; reading the source is this skill's job, done once here, never the verify skill's.

## Before writing

**Four decisions are the person's, settled through the `interview` skill, one at a time, each proposed with its reason**: the focus, the inputs and their defaults, the experts, the feature to prove it on. The rest is established from the repository.

- **Understand the project, then settle the focus with the person**: what this verifier judges and through what. The project can be anything (an app, a service, a library, a pipeline); the candidates come from what it is: every surface it offers its consumers and every way the project already runs or judges a part of it, each proposed with what it would judge and why, one recommended. The examples above are examples, never the list. **Stop if a verifier with that focus exists**: it keeps itself true when run. Say so; never overwrite one. A first verifier named plain `verify-<app>` is renamed to its focus when a second is created, on the person's yes.
- **A project skill that already runs the app stays its own**, shared by every verifier: it is proven, and the next verifier needs it too. The verify skill names it in *Run the app* and restates none of it. None: the steps to run the app go in the verify skill, and a second verifier moves them into a skill of their own.
- **Establish from the repository, never by asking**: the consumer and what they come for, the interface they use, how the app starts and signals ready, the tool the agent acts through, where the specification lives (plans and their stories, decisions, reference prototypes, the `design-prototype` skill's design language), and **the inputs a pass of this focus depends on** (the widths and themes among them, where the focus has any), each with its default (`references/verify-skill-template.md`, *Scope and inputs*): a default follows the project's decisions first (its plans, its prototypes), its code second, and is the cheapest pass that answers the focus (the widths: the prototypes', not the code's breakpoints); the rest the scope sets. **The reference and its fidelity is an input of every focus with a prototype**: the experience, the layout, or a pixel match.
- **The harness reference** of the interface, read for the tool to act through and its observations, its expert roles an example to choose from (`references/role-prompt.md`): `references/web.md`, `api.md`, `service.md`, `cli.md` or `mcp.md`. A tool the agent operates is built as `references/tooling.md` says.

## The skill

**`verify-<app>-<focus>/SKILL.md`** in the project's local skill folder, written to the shape in `references/verify-skill-template.md`, read before the first line.

## Prove it

**Run one quality pass through the generated skill** on the feature to prove it on: the smallest delivered feature that exercises the focus, chosen only to prove the skill, never what the verifier covers. It is taken from the product as it stands now (the roadmap and the newest plans read first), with references that still describe it, never a feature since reworked, proposed to the person with what was established to run it (the start, the ready signal, how the agent's tool is opened), run on their yes or on the one they name instead, by a fresh agent on the plugin's `verifier` agent (`subagent_type: "swarmstorm:verifier"`), its brief the skill's name, the feature as its scope and the inputs that differ from the defaults: an agent arriving cold is what the skill is written for. The skill is proven when the pass is complete: every part of the scope reached, judged against its inputs, the verdict and its findings table in its report. A `not ready` verdict proves it as well as `ready`; what the pass finds on the app is reported, never fixed inside this skill. A part it could not reach fails on the skill: fix it and run again.

**Handoff**: the skill's path, its focus, the pass's report.

## Red flags

| Thought | Reality |
|---|---|
| "A list of what to check makes the skill thorough" | The agent checks that list and stops. The role prompt and the three counts are the protocol; the judgment is the agent's. |
| "The inputs are obvious" | The verifier guesses them and judges against the wrong reference. Each has a default in the skill or comes in the scope. |
| "The existing run skill could be written better" | It is proven. Wrap it; reword nothing that works. |
