---
name: setup-pstack
description: Set pstack up for this user and this computer. Generates the `select-model` skill, which records the agent products and models found here and the user's preferences, so the model running a task can decide which model to use and how. Use for /setup-pstack, "configure pstack models", "pstack budget", or changing pstack's model choices.
---

# Setup pstack

pstack does not ship a model table. It generates `select-model`, a skill under `~/.agents/skills/select-model/` that holds this user's preferences and this computer's agents and models. Every harness with an adapter reads it by that path at the start of a task. Nothing loads it for them. The generator can also link it into the skill folders of the harnesses that list skills from their own folder (`locate` gives each), as the `skills` CLI does, and asks first.

## Steps

### 1. Check what exists

If `~/.agents/skills/select-model/SKILL.md` exists, this is an update. Otherwise it is a new setup. Tell the user which in one sentence.

### 2. Generate or update `select-model`

Run the **create-model-selection-skill** skill by reading its `SKILL.md` next to this one, and follow it to the end. It surveys this computer, asks five questions, writes the skill, and starts one read-only job per agent product to prove it.

### 3. Confirm

Repeat the generator's hand-over in two sentences: where the skill is, and that the next task reads it. Say how to change it: edit a sentence under `## Preferences` in that file, or run `/setup-pstack` again.

When a product on this computer cannot run from this session, say which environment starts it. The Launching harnesses section of each environment adapter says which products it starts. Without an environment, a session starts another product only through that product's own CLI, as its adapter's Start me from outside section says.

When an environment adapter's Launching harnesses says the environment refuses a product's model or effort flags, say so, and say which file sets the model that product runs there and that the user changes it in that file.

### 4. Offer a verification skill (optional)

Check whether the project has a way to drive the real app for proof (a `verify-*` skill, or an existing harness). If not, offer once: "want a project-local verification skill, so agents can drive the app the way a user does and prove changes work? I can generate one with /create-verification-skill." On yes, run the **create-verification-skill** skill by reading its `SKILL.md` next to this one. On no, move on without pushing.

### 5. Offer a formal verification skill (optional)

Check whether the project already has a formal verification skill (a project skill that runs a model checker, a proof, or another verifier against the code). If not, offer once: "want a formal verification skill, so agents can prove a key property of your code holds in every case in scope, not only the cases tests reach? I can generate one with /create-formal-verification-skill." On yes, run the **create-formal-verification-skill** skill by reading its `SKILL.md` next to this one. On no, move on without pushing.
