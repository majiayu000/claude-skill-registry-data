---
name: construct-skill
description: 'Drafts a new skill for a plugin in a marketplace repo, to its guidelines. Use when the user wants a skill written or a workflow made into one ("write a skill", "create a SKILL.md", "add a skill to the plugin"). Not for .claude/skills project skills.'
argument-hint: <skill name or intent>
allowed-tools: Read, Write, Edit, AskUserQuestion, Bash(claude plugin validate:*)
---

# Construct Skill

## Overview

Walks the user through writing one new skill for a plugin in this marketplace repo, so that it meets the repo's skill guidelines at first review. The loop is test-first. RED collects the failures an agent shows when the task runs without the skill. GREEN writes the skill around those failures. REFACTOR re-reads the draft as a skeptic and runs the pre-publish checklist. The user approves the finished draft before the run ends.

## When to Use

One new skill under `plugins/<plugin>/skills/<name>/` in a marketplace checkout, from its frontmatter to its phase and reference files.

- Reviewing skill changes on a branch or PR: use `review-branch` or `github-review-pr`.
- Editing one phase file of an existing skill: edit it directly.
- A project skill under `.claude/skills/`, or a repo with no `plugins/` tree: out of scope, because the checks here assume the plugin layout.
- Writing an agent, a rule file or a plan: this skill covers skills only, and agents follow AGENTS_GUIDELINES.md.

## Constants

- **SKILL_DIR**: `${CLAUDE_SKILL_DIR}`
- **PROJECT_ROOT**: the path printed in Phase 0 by `echo "${MZ_MEMORY_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}"`. It holds `.mz/` and nothing else.
- **REPO_ROOT**: the path printed in Phase 0 by `git rev-parse --show-toplevel`, the checkout the user is authoring in. The plugin tree lives here. `MZ_MEMORY_ROOT` can point `.mz/` at another checkout, so it never decides where the skill is written.
- **TARGET_DIR**: `<REPO_ROOT>/plugins/<plugin>/skills/<SkillName>/`, the new skill's directory
- **DESCRIPTION_MAX_CHARS**: 250, the repo cap on `description` plus `when_to_use`. It protects the skill-listing budget that every installed skill shares.
- **MAX_REFACTOR_ATTEMPTS**: 2. An item that still fails after two rework passes needs the user's call, not a third guess.

The phase file writes `<SKILL_DIR>`, `<PROJECT_ROOT>`, `<REPO_ROOT>` and `<TARGET_DIR>`, because a file opened with Read gets no variable substitution and shell variables don't persist between Bash calls. Expand each to its absolute path before reading a file or running a command.

## Core Process

### Phase Overview

| Phase | Goal                                                | Details               | Loop           |
| ----- | --------------------------------------------------- | --------------------- | -------------- |
| 0     | Setup                                               | Inline below          |                |
| 1     | Author (RED, GREEN, REFACTOR) and approve the draft | `phases/authoring.md` | until approved |

### Phase 0: Setup

1. **Resolve the roots.** Run the `PROJECT_ROOT` and `REPO_ROOT` commands once, before any `cd`, and keep the printed paths. Check that `<REPO_ROOT>` holds `.claude-plugin/marketplace.json` and a `plugins/` directory.
1. **Parse the input.** `$ARGUMENTS` is the skill name or a short intent. If it is empty, ask in prose what the skill should do and which plugin it belongs to.
1. **Settle the skill name.** If `$ARGUMENTS` is already a kebab-case name, use it. Otherwise propose a short kebab-case name from the intent (lowercase letters, digits and single hyphens) and ask in prose whether to keep it or replace it.
1. **Note the skill's role**: discipline, collaboration or reference, as `${CLAUDE_SKILL_DIR}/references/persuasion-principles.md`, "Register by role", defines them. The role sets the voice of the body.
1. **Name the task** `<YYYY_MM_DD>_construct-skill_<slug>`: today's date with underscores, then a snake_case summary of the skill name of at most 20 characters. On a same-day collision, append `_v2`, `_v3`. Write `state.md` with `SkillName` and `SkillRole`.
1. **Pick the target plugin** under `<REPO_ROOT>/plugins/`. If several fit, ask with AskUserQuestion, header "Plugin", offering the likeliest ones (up to four) as options; the user can type any other name. Check that `TARGET_DIR` doesn't exist yet, then add `TargetDir` to `state.md`.

Then read `<SKILL_DIR>/phases/authoring.md` and run Phase 1. After compaction, re-read `<PROJECT_ROOT>/.mz/task/<task_name>/state.md`, then the phase file, before continuing.

## Red Flags

- The draft's description summarizes the workflow, or opens with a prefix every skill shares instead of a capability clause and "Use when…".
- A draft section reads `N/A` or is a pointer line such as "delegated to phase files". Leave the heading out instead.
- The rationalization table holds excuses nobody saw an agent make, excuses from the user, or rebuttals with invented figures.
- The draft's body uses all-caps emphasis, which current models over-apply, or flattery and pleasantries, which push models toward agreeing with the user.
- The gate message shows a path, a line count or a summary where the draft belongs verbatim.
- A mechanical checklist item is marked PASS with no command output behind it.

## Verification

The run is done when two things are on screen: the pre-publish checklist from Phase 1, each item marked PASS, n/a or open with its evidence (the command and its output for mechanical items), and the user's explicit Approve at the draft gate.

## References

- `${CLAUDE_SKILL_DIR}/references/canonical-skill-anatomy.md`: the SKILL.md section layout, a skeleton to copy, path rules, the state blocks, the gate skeleton and the supporting rules for reports, waves, tooling, input and escalation. Read it in full at the start of GREEN.
- `${CLAUDE_SKILL_DIR}/references/anti-rationalization-library.md`: seed rows, grouped by the rule they guard. Search it for the matching area heading during RED rather than reading all of it.
- `${CLAUDE_SKILL_DIR}/references/persuasion-principles.md`: how to word a skill body for its role. Read it before the wording pass in GREEN.

## Error Handling

- **Not a marketplace checkout** (`git rev-parse --show-toplevel` fails, or `<REPO_ROOT>` lacks `.claude-plugin/marketplace.json` or `plugins/`): stop and say that this skill writes plugin skills in a marketplace repo only.
- **Empty arguments**: ask in prose what the skill should do and which plugin it belongs to. Don't invent either.
- **Target plugin missing**: stop and ask. Don't create a plugin directory as a side effect.
- **`TARGET_DIR` already exists**: ask whether to pick another name or stop. This skill writes new skills only and doesn't overwrite one.
- **Description can't fit `DESCRIPTION_MAX_CHARS` without dropping a trigger or the counter-trigger**: show the conflict and let the user choose what to drop. Don't cut triggers silently.
- **`claude plugin validate` or PyYAML unavailable**: mark that checklist item open, run the other checks, and say so in the final report.
- **A checklist item still fails after `MAX_REFACTOR_ATTEMPTS` passes**: ask with AskUserQuestion, header "Checklist", naming the item, with the options **Accept** (keep the exception with a written reason), **Rework** and **Abort**.
- **Nobody can answer** (AskUserQuestion is denied or unavailable, or the skill runs inside a subagent): finish the work that doesn't need the answer, write the question and its options to `state.md`, set `Status: blocked`, and stop. Inside a subagent, return `STATUS: BLOCKED` with the question and its options.

## State Management

State persists to `.mz/task/<task_name>/state.md` under the project root, `${MZ_MEMORY_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}`, resolved once at the start of the run. Schema is **v2**: line 1 is `schema_version: 2`; line 2 is `Status:` with one of `pending`, `running`, `blocked`, `complete`, `aborted_by_user` or `failed`, lowercase and unquoted; then `Phase`, `Started`, `phase_complete` (boolean) and `what_remains` (YAML list of strings), with skill-specific keys below them. Milestones go in `Phase`; the reason for `blocked` or `failed` goes in `what_remains`. Set `phase_complete: false` on phase entry and `true` once the phase's artifacts are written and its gates pass. Refresh `what_remains` on every phase transition; it is `[]` when `Status` is `complete`. Write the file after every phase and before every gate, and re-read it after compaction. Record decisions worth recalling under a heading that reads exactly `## Decisions`, placed before `## Notes`; mz-memory harvests them only once `Status` is `complete`. Under a heading that reads exactly `## Lessons`, add one line whenever a review finding is accepted and fixed, a step fails, gate feedback corrects a mistake, or an approved approach is reversed, in the form `- (review|failure|correction|change) WHEN <situation> → <what to do> — WHY <cause>`, concrete and under about 40 words; mz-memory harvests lessons whatever the `Status`. Treat a legacy `completed` as `complete`. On reading a `schema_version: 1` or unversioned file, put `schema_version: 2` on line 1 and `Status` on line 2, add the missing keys, and log the upgrade. Leave a file with a higher `schema_version` untouched: ask whether to Restart (archive it), start New (`_v2`) or Abort, and stop if nobody can answer.

This skill also keeps the optional schema key `FilesWritten`, next to the other schema keys: every file the run creates, appended as it is written, relative to `PROJECT_ROOT` or absolute outside it. Its skill-specific keys are `SkillName` and `SkillRole` (from Phase 0) and `TargetDir` (the absolute `TARGET_DIR`). `Phase` records the authoring step: `1_red`, `1_green`, `1_refactor` or `1_approval`.
