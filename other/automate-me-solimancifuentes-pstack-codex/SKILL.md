---
name: automate-me
description: "Use for \"automate me\", \"create/update/refresh my -mode skill\", \"turn/capture my preferences or working style into a skill\", or wanting agents to follow how the user works. Drafts or revises a personal -mode skill via skill-creator + unslop, optionally pulling fresh evidence from recent transcripts."
---

# Automate me

A guided flow for turning the user's working conventions into a skill agents will follow. The output is one `-mode` skill tailored to them (e.g. `jay-mode`, `priya-mode`).

This skill orchestrates three others: an inline mining pass (see step 1), the available `skill-creator` (authoring), and the **unslop** skill (prose discipline). It sequences them. It doesn't replace them.

## Flow

### 0. Check for an existing skill

Inspect the current host's supported, in-scope skill locations for a mode matching the user's handle. On Codex these can include `.agents/skills/**/*-mode/SKILL.md` and `~/.codex/skills/*-mode/SKILL.md`. A Dot cloud environment may not contain the local computer's skills. Do not search unrelated plugin caches or invent a shared global path. Mode skills can live in a personal category directory (`.agents/skills/<handle>/`), not only at the top level. If one exists, confirm intent with an available user-input tool or concise chat question (unless they already said "update my skill" or similar):

- Update the existing skill (default for repeat runs)
- Start fresh (rare, ask why before doing it)

Update mode changes the rest of the flow:
- Step 1 mines only history since the skill was last edited (`git log -1 --format=%cI <path>`).
- Step 2 asks what's changed or missing, not what to capture from zero.
- Step 4 edits the existing file in place. Preserve sections the user hasn't contradicted. Revise ones with new evidence. Add new sections only for genuinely new rules.

### 1. Mine their history

Use the current conversation and explicitly scoped history evidence, following the selected host adapter in [CODEX.md](../../CODEX.md). Identify the project, topic, and date range before any history search. Desktop chat APIs are optional; supplied transcripts and logs work in CLI, while Dots may provide native task history. Do not inspect unrelated projects. If raw transcripts are unavailable, mine the available messages or summaries and label that evidence limit.

Survey recent agent conversations within that scope for recurring patterns. Run multiple parallel subagents across slices of history (e.g. last 2-4 weeks, split into 3 slices so each has enough material). Follow the actual model and delegation policy in CODEX.md. Each slice mining subagent reads only the scoped chat artifacts the parent provides, looks for the signals below, and returns a short structured list of patterns it saw with evidence pointers. Default signals worth hunting:

- Response preferences (length, tone, format, "dumb it down" corrections)
- Delegation habits (subagents, models, specialized workflows, parallelism)
- Verification posture (what "done" means, unit tests vs live repro, reviewers)
- Code and prose discipline (style, principles cited, lint/format tools)
- Process conventions (worktrees, commits, PRs, review/merge tooling)
- Meta preferences (fixing skills mid-task, proposing new ones)

Cross-check across slices before elevating a signal. Patterns seen in 2+ slices are high-confidence. Lone signals are weak and usually get dropped.

### 2. Ask the user directly

Mining misses intent that hasn't come up yet. Use an available user-input tool within its real schema, or ask a concise chat question when useful. Do not require the user to restate preferences already supported by the session.

Use the current input tool's real schema and question limits when one is available. Otherwise ask a concise question in chat. Start with the most consequential unknown and follow up only when the answer changes the draft. Existing session preferences are evidence, so do not make the user repeat them.

Don't dump 20 questions.

### 3. Cluster findings

Group the combined signals into sections. Common ones (use only what applies):

- **Response style**: length, tone, format.
- **Autonomy**: how much to do without asking, MCP tool use.
- **Understand first**: which skills to reach for when scoping or investigating a change.
- **Subagents**: default, parallelism, model-to-task, specialized workflows.
- **Prose / code discipline**: principles, lint tools, style guides.
- **Review and verify**: repro posture, verification skills, live-testing tools.
- **Process**: git worktrees, commits, PRs, review/merge tooling.
- **Skills**: skill-authoring habits, fix-the-skill-first, proposing new skills.

The **poteto-mode** skill shows the shape. Read it for granularity. Don't copy its content. The user's rules are not the same as poteto-mode's.

### 4. Draft the skill

Use the available `skill-creator` skill to author the skill. Placement:

- Path: preserve an existing mode skill's category. For a new mode, use `.agents/skills/<handle>/<handle>-mode/SKILL.md` when the repo has an established personal category for that handle. Otherwise default to `.agents/skills/<handle>-mode/SKILL.md` in the project (or `~/.codex/skills/<handle>-mode/` if the user prefers a personal skill).
- Handle: the user's first name or chosen identifier.
- Frontmatter `description`: trigger on their name + `/<handle>-mode` + "work in their style", not on generic keywords like "write code" or "review PR".
- Frontmatter formatting: follow `skill-creator`'s YAML rules. Keep `description` as one YAML scalar. Quote it or use `description: >-` with indented continuation lines when punctuation or wrapping requires it.
- Preserve invocation intent. For a personal mode the user wants explicit-only, set `policy.allow_implicit_invocation: false` in `agents/openai.yaml`. Use the target host's supported metadata rather than Cursor frontmatter controls. The `agents/openai.yaml` example applies to the Codex plugin format; verify target-format support before assuming a Dots installation reads it. A workflow profile does not register a persistent Custom Mode.

### 5. Iterate on prose

Apply the **unslop** skill and `skill-creator`'s writing guidelines to every line.

Show the draft to the user and take feedback. Expect multiple iterations. Cut ruthlessly. A mode skill is not a manual.

### 6. Land it

For a project skill, use an isolated worktree and a draft PR when that delivery is within the requested scope. For a personal skill, show the concrete installation changes and honor the user's installation approval preference before writing the global location. Keep the completed draft available for review. Do not create a repository or PR solely because this source workflow assumed one.

## Guardrails

- **Don't overfit to one conversation.** A preference stated once and contradicted another time is noise. Require multiple instances before codifying it.
- **Don't be clever.** Restating other skills' contents, inventing metaphors, or writing "poetic" prose for an agent reader is cost without benefit. Keep it operational.
- **Reference, don't inline.** Other skills the user relies on should appear as path references, not pasted excerpts. Same for any principle docs they maintain elsewhere.
- **Keep sections minimal.** Only add a section if the user has a specific, non-default rule there. "Communicate clearly" is not a section. "Short paragraphs. Tables when comparing options. Bullets only when items are genuinely parallel." is.
- **Name conventions generic.** Use "the user" or "the human" in imperatives, not the author's first name.
- **Don't force symmetry.** If a user has no process rules worth writing down, skip the Process section entirely.

## Evaluation

A `-mode` skill is subjective output. A `skill-creator`-style test/iterate benchmark loop isn't useful here. Vibe-check with the user: does it read like them? Did it miss anything? Then ship.

Run a description-optimization loop only if the skill's trigger accuracy turns out to be a problem in practice.

## When not to use

- User wants a task-specific skill (not working conventions): `skill-creator` alone, no mining required.
- User wants to capture one narrow workflow (e.g. "how I write commit messages"). That's a regular skill, not a mode skill.

