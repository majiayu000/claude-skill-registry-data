---
name: skill
description: "Use when creating or editing a skill, agent, or command inside the ni plugin, when a skill does not trigger or triggers too often, when moving content between skills or into a reference file, or when the user asks how ni skills are structured, linked, tested, or installed."
---
# Skill

## When to use
- User asks to create, rename, split, merge, or rewrite a ni skill, agent, or command
- A skill does not trigger, or triggers on unrelated prompts
- A SKILL.md grows past 300 lines or carries content another skill also needs
- User asks how ni is laid out, linked, validated, or installed

## Overview

A skill is a reference guide for a proven technique, not a story about one task. It
loads only when its description matches the prompt, so the description decides
whether the body is ever read. Write the smallest body that changes behaviour.

Every ni skill fits one plugin. Same voice, same sections, same linking. A new skill
that reads like its neighbours costs the reader nothing to learn.

Template: [template.md](template.md). Copy it, then delete the sections you do not need.

## Layout

```
natural-intelligence/
  .claude-plugin/plugin.json   manifest
  agents/<name>.md             subagents, spawned as ni:<name>
  commands/<name>.md           slash commands, run as /ni:<name>
  skills/<name>/SKILL.md       one skill per folder, name = folder
  skills/<name>/<topic>.md     reference file, linked from SKILL.md
  README.md                    skill, agent, and command tables
```

Names are short nouns or noun pairs, lowercase, hyphens: `plan`, `tdd`, `code-review`.
Folder name equals frontmatter `name`. Claude exposes it as `ni:<name>`.

## Frontmatter

```yaml
---
name: <folder-name>
description: "Use when <triggers>. Also use when <more triggers>."
---
```

Description rules:

1. Triggers first. Say when to load. One short clause on what the skill is may precede
   it. Never summarise the workflow: a description that summarises the steps gets followed
   instead of the body.
2. Start with "Use when". Third person. Double quotes. Name under 64 characters.
3. List concrete symptoms, phrasings, file types, and tool names a prompt would contain.
4. Under 500 characters when possible, 1024 at most.

Not: `description: "Prevents hallucinations by requiring evidence for all claims."`
Yes: `description: "Use when analysing code, explaining behaviour, reviewing a change, or making any claim about how the code works."`

## Body

Sections in this order. Drop any that has nothing to say.

| Section | Holds |
|---|---|
| `# Title` | Skill name in words |
| `## When to use` | Bullets, one trigger each, mirrors the description |
| `## Overview` | Two to four sentences: what it is, core principle, links to related skills |
| `## Rules` or `## Workflow` | Numbered when order matters, bullets otherwise |
| `## <Topic>` | One heading per technique or table |
| `## Boundaries` | What the skill never does, what it hands to another skill |

Voice: short plain prose. Full sentences under 20 words,
active, imperative for instructions, one term per concept. No filler, no emoji, no
decorative tables. Tables carry data or comparisons only.

Length: under 300 lines. Under 150 when the skill loads often. Move heavy reference
(commands, API detail, long examples) to a sibling file and link it.

Examples: one "Not" line and one "Yes" line beat a paragraph. Code blocks for commands.

Snippets: ni runs on Linux, macOS, and Windows with or without WSL. Every command in a
skill, agent, or command file follows the shell rules in
[onboarding.md](../software-engineer/onboarding.md#shell-rules): one command per line,
no shell syntax, each shell's form on its own line where the invocation differs. No
hooks, no script that needs one particular shell.

## Linking

Link sibling skills with relative markdown links: [`tdd`](../tdd/SKILL.md). Reference
files link back to their skill: [`code-review`](SKILL.md). Mark hard dependencies:

- `**REQUIRED BACKGROUND:** the [`x`](../x/SKILL.md) skill defines ...`
- `**REQUIRED SUB-SKILL:** use [`tdd`](../tdd/SKILL.md) for the failing test`

Never repeat a rule that lives in another skill. Link it. One owner per rule.

Reference files sit next to SKILL.md and link from it directly, one level deep. No
reference file links another reference file.

Agents are referenced by their spawn name in backticks: `ni:investigator`.

## Agents

File `agents/<name>.md`. Frontmatter: `name`, `description` (when to spawn, what comes
back), optional `model` (`haiku` for locate and review jobs), `tools` as a comma list.
Body: role in one line, job, output contract as a code block, refusals as terminal
first lines, auto-clarity note. Output contracts are the point: rows, not prose.

## Commands

File `commands/<name>.md`. Frontmatter: `description`, optional `argument-hint`. Body
is the prompt Claude receives. The placeholder `ARGUMENTS` with a dollar prefix carries the
arguments (written out here because skills expand it too). Keep commands thin:
point at a skill, do not restate rules. A command that needs a shell call prompts for
approval, so prefer commands that only read and reason.

## Verify and install

1. `claude plugin validate . --strict` from the repo root
2. `bash .github/scripts/docs.test.sh`: enforces the shell rules, links, and shipped tree
3. `claude --plugin-dir . -p "..."` to load from the working tree
4. Add the skill, agent, or command to the README table
5. Bump `version` in `.claude-plugin/plugin.json`: users only get updates on a version change
6. `/reload-plugins` in a running session, or start a new one
7. Commit with the [`git-conventions`](../git-conventions/SKILL.md) skill

Optional trigger test: run a prompt that should load the skill with `--model haiku -p`
and ask which skills it used. Run one that should not. Adjust the description on a miss.

## Boundaries

This skill covers ni only. Project skills under `.claude/skills/` follow their project.
Never write a skill for a one-off task or a project convention: those go in `CLAUDE.md`.
Never duplicate a rule an existing skill owns.
