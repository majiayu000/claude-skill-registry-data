---
name: invention-workshop
description: Sokka's invention workshop, where he studied how things really worked and built the machine that did it (war balloons, the submarine). Use for automate-me, /automate-me, "automate me", "create, update, or refresh my -mode skill", "turn my preferences or working style into a skill", or wanting agents to follow how the user works. Drafts or revises a personal -mode skill with new-scroll and tea-time, optionally mining fresh evidence from recent transcripts.
---

# Sokka's invention workshop

Sokka built the war balloons by taking apart what the Fire Nation flew, and the submarines by watching how the Mechanist's machines moved. He studied the real thing first, then built a machine that did it every time. Do the same for the way the user works. Watch the record, ask about what the record cannot show, and build one `-mode` skill that agents follow (for example `jay-mode` or `priya-mode`).

On Codex, read [avatar-mode/references/codex.md](../avatar-mode/references/codex.md) for tool equivalents.

This skill sequences three passes. An inline mining pass (step 1), `new-scroll` for authoring, and `tea-time` for prose discipline. It sequences them. It does not replace them.

## Flow

### 0. Check for an existing skill

Search recursively for a mode skill matching the user's handle.

- **Claude Code.** `.claude/skills/**/*-mode/SKILL.md` in the project and `~/.claude/skills/*-mode/SKILL.md`.
- **Codex.** `.agents/skills/**/*-mode/SKILL.md` in the project and `${CODEX_HOME:-~/.codex}/skills/*-mode/SKILL.md`.

Mode skills can live in a personal category directory (`.claude/skills/<handle>/`), not only at the top level. If one exists, confirm intent with `AskUserQuestion` unless the user already said "update my skill" or similar.

- Update the existing skill (the default for repeat runs).
- Start fresh (rare, so ask why before doing it).

Update mode changes the rest of the flow.

- Step 1 mines only history since the skill was last edited (`git log -1 --format=%cI <path>`).
- Step 2 asks what has changed or is missing, not what to capture from zero.
- Step 4 edits the existing file in place. Keep sections the user has not contradicted. Revise ones with new evidence. Add new sections only for truly new rules.

### 1. Mine their history

Locate the active workspace's transcripts before you fan out. Use only this workspace's path.

- **Claude Code.** `~/.claude/projects/<encoded-cwd>/*.jsonl`, where `<encoded-cwd>` is the workspace's working directory with `/` replaced by `-`.
- **Codex.** The rollout files under `${CODEX_HOME:-~/.codex}/sessions/` whose session metadata names this workspace as its `cwd`.

Never glob across every project. That crosses workspace boundaries and reads private chats from unrelated projects.

Survey recent agent conversations in that scope for recurring patterns. Split the history into slices (for example the last two to four weeks, in three slices, so each has enough material). Dispatch Toph (`subagent_type: "team-avatar:toph"`) on each slice in parallel, on Toph's model from the avatar-setup sheet. Pick each dispatch's reasoning effort for the job, as `avatar-mode` describes. Pass each the workspace-scoped path and its slice. Each returns a short structured list of the patterns it saw, with evidence pointers. When you are yourself a subagent, mine the slices yourself, one after another.

Default signals worth hunting:

- Response preferences (length, tone, format, "dumb it down" corrections).
- Delegation habits (subagents, models, specialized workflows, parallelism).
- Verification posture (what "done" means, unit tests against live repro, reviewers).
- Code and prose discipline (style, principles cited, lint and format tools).
- Process conventions (worktrees, commits, PRs, review and merge tooling).
- Meta preferences (fixing skills mid-task, proposing new ones).

Cross-check across slices before you elevate a signal. A pattern seen in two or more slices is high confidence. A lone signal is weak and usually gets dropped.

### 2. Ask the user directly

Mining misses intent that has not come up yet. Use the `AskUserQuestion` tool for structured multiple choice, rather than asking the user to type from scratch.

- One or two questions with four to six options each. Allow multiple answers for category questions.
- Start broad ("Which areas matter most?"), then follow up on the selected areas with specific options.
- After the structured rounds, ask one free-form question in chat to catch anything the options missed.

Do not dump twenty questions.

### 3. Cluster findings

Group the combined signals into sections. Common ones, used only where they apply:

- **Response style.** Length, tone, format.
- **Autonomy.** How much to do without asking, and MCP tool use.
- **Understand first.** Which skills to reach for when scoping or investigating a change.
- **Subagents.** The default, parallelism, model per task, specialized workflows.
- **Prose and code discipline.** Principles, lint tools, style guides.
- **Review and verify.** Repro posture, verification skills, live-testing tools.
- **Process.** Git worktrees, commits, PRs, review and merge tooling.
- **Skills.** Skill-authoring habits, fixing the skill first, proposing new skills.

`avatar-mode` shows the shape. Read it for granularity. Do not copy its content. The user's rules are not Team Avatar's rules.

### 4. Draft the skill

Author the skill with `new-scroll`. Placement:

- **Path.** Keep an existing mode skill's category. For a new mode, use `.claude/skills/<handle>/<handle>-mode/SKILL.md` when the repo has an established personal category for that handle. Otherwise default to `.claude/skills/<handle>-mode/SKILL.md` in the project, or `~/.claude/skills/<handle>-mode/` if the user prefers a personal skill. On Codex, use the matching `.agents/skills/` or `${CODEX_HOME:-~/.codex}/skills/` path.
- **Handle.** The user's first name or chosen identifier.
- **Description.** Trigger on their name, `/<handle>-mode`, and "work in their style". Never trigger on generic keywords like "write code" or "review PR".
- **Frontmatter format.** Follow the YAML rules in `new-scroll`. Keep `description` as one YAML scalar. Quote it, or use `description: >-` with indented continuation lines, when punctuation or wrapping requires it.
- **Invocation.** Set `disable-model-invocation: true` by default. Opt out only if the user explicitly wants their mode to apply on every turn.

### 5. Iterate on prose

Apply `tea-time` and the writing guidance in `new-scroll` to every line.

Show the draft to the user and take feedback. Expect several rounds. Cut ruthlessly. A mode skill is not a manual.

### 6. Land it

Work in a worktree off the default branch. Commit and open a PR with `yip-yip`. Never push to the default branch directly.

## Guardrails

- **Do not overfit to one conversation.** A preference stated once and contradicted another time is noise. Require several instances before you codify it.
- **Do not be clever.** Restating other skills, inventing metaphors, or writing poetic prose for an agent reader costs and gives nothing back. Keep it operational.
- **Reference, do not inline.** Other skills the user relies on appear as path references, not pasted excerpts. The same goes for principle docs they keep elsewhere.
- **Keep sections minimal.** Add a section only when the user has a specific, non-default rule there. "Communicate clearly" is not a section. "Short paragraphs. Tables when comparing options. Bullets only when items are truly parallel." is.
- **Keep names generic.** Write "the user" or "the human" in imperatives, not the author's first name.
- **Do not force symmetry.** If the user has no process rules worth writing down, skip the Process section.

## Evaluation

A `-mode` skill is subjective output, so a benchmark loop does not help here. Check the feel with the user. Does it read like them? Did it miss anything? Then ship.

Run a description-tuning loop only if the skill's trigger accuracy turns out to be a problem in practice.

## When not to use

- **A task-specific skill, not working conventions.** Use `new-scroll` alone. No mining is needed.
- **One narrow workflow** (for example "how I write commit messages"). That is a regular skill, not a mode skill.
