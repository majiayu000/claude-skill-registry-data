---
name: claude-codex-upstream-update
description: "Use when researching Claude Code or Codex upstream releases, selecting adaptations, or preparing Harness upgrades. Local-only; not for distribution."
user-invocable: true
---

# Claude / Codex Upstream Update

A local-only skill for taking Claude Code and Codex upstream updates all the way through to Harness implementation diffs.
The goal is not to "introduce updates" but to "actually make Harness stronger."

## When to Use

- When you want to look at the Claude Code changelog and select updates to incorporate into Harness
- When you want to look at Codex releases and sort out the differences between using them from Claude vs. from Codex
- When you want to reflect changes not just in docs, but through to hooks / scripts / tests / Plans / CHANGELOG

## When Not to Use

- Simple release summaries intended for public distribution
- Just a changelog summary
- Promotional text not accompanied by implementation diffs

## Basic Rules

1. Check primary sources first
   - Claude: `https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md`
   - Codex: `https://github.com/openai/codex/releases`
2. Verify existing Harness implementation
   - `docs/CLAUDE-feature-table.md`
   - `.claude/skills/cc-update-review/SKILL.md`
   - `hooks/hooks.json`
   - `.claude-plugin/hooks.json`
   - `scripts/hook-handlers/`
   - `go/internal/guardrail/`
   - `tests/test-claude-upstream-integration.sh`
   - `tests/validate-plugin.sh`
3. Do not stop at just writing to the Feature Table
   - Follow the A/B/C classification in `.claude/skills/cc-update-review/SKILL.md`
   - `B = documentation only` is not acceptable. Proceed to an implementation proposal or the implementation itself
4. Prioritize Claude side decisions first
   - What to implement immediately this round
   - What to retain as a Codex comparison axis
   - What is covered by CC / Codex auto-inheritance

## Execution Flow

### 1. Break Down Official Updates

- Claude side: divide into "new features," "operational improvements," "fixes," and "auto-inherited"
- Codex side: divide into "items that become a comparison axis now" and "future tasks"
- What matters here is whether Harness can amplify it

Judgment criteria:

- Implementation target
  - Can be reduced to hook / script / skill / agent / validate
  - User experience improvement can be described in "before / after" terms
- Comparison axis
  - Not implementing this round, but high value in closing the gap between Claude and Codex
- Auto-inherited
  - Benefits from upstream fix alone

### 2. Fit into Existing Channels

Update candidates must always determine which surface they belong to.

- `hooks/` / `.claude-plugin/hooks.json`
- `scripts/hook-handlers/`
- `go/internal/guardrail/`
- `skills/` / `agents/`
- `tests/test-claude-upstream-integration.sh`
- `tests/validate-plugin.sh`
- `docs/CLAUDE-feature-table.md`
- `CHANGELOG.md`
- `Plans.md`

As a rule, do not make something an implementation target if it "doesn't fit anywhere."

### 3. Implement with Claude First

Prioritize one of the following.

- When Claude's new features are absorbed into Harness's existing channels, noise reduction, safety improvements, and automation strengthening occur
- Harness's existing features become even stronger with the upstream update

Example:

- Use the hooks conditional `if` field to narrow permission hooks to only the necessary Bash
- Fill in inconsistencies between existing guardrails like `MultiEdit` and hooks
- Connect new hook events to runtime tracking / recovery / Plans re-read reminders

### 4. Keep Codex as a Comparison Axis

Even if the Codex side is not the primary implementation target this round, keep it in the following form.

- `plugin-first workflow`
- `resume-aware effort continuity`
- readable agent addressing
- image-aware workflow

Do not try to do everything in one update cycle.
Complete the high-value items on the Claude side first, then cut out the Codex side into Plans.

### 5. Update Records

At minimum, update the following.

- `Plans.md`
- `docs/CLAUDE-feature-table.md`
- `CHANGELOG.md`
- `tests/test-claude-upstream-integration.sh`
- `tests/validate-plugin.sh` if needed

Writing standards:

- What increased upstream
- What Harness incorporated
- How the user experience changes

## Completion Criteria

- Primary source verification for Claude / Codex is complete
- On the Claude side, at least 1 implementation or verification reinforcement is complete
- The Feature Table and CHANGELOG read as "meaningful improvements"
- Future responses remain in Plans
- validate-plugin or relevant tests have been executed

## Non-Distribution Rule

- This skill is local-only
- Do not mirror
- Do not design with inclusion in public packages in mind
- If you want to distribute it, extract it as a separate skill with local-specific content removed

## Implementation Notes to Keep

### Auto-Completion and Input Normalization of AskUserQuestion Using `PreToolUse updatedInput`

In situations where `PreToolUse updatedInput` can be used stably on the Claude Code side, a design that "lightly tidies up" the `AskUserQuestion` input before the question is asked is effective.
Normalization here does not mean rewriting user intent, but completing options and aligning ambiguous expressions beforehand to reduce the number of question re-asks.

#### Purpose

- Reduce the number of times the same question is re-asked in different phrasings
- In interactive flows like `harness-plan create`, safely advance to the next question even from short answers
- Align known choices like `solo / team`, `patch / minor / major`, `scripted / exploratory` at an early stage

#### Suitable Surfaces

- `harness-plan create`
- `harness-release`
- Future interactive setup / review channels with something equivalent to `request_user_input`

#### Minimal Implementation Proposal

1. Detect `AskUserQuestion` calls in `PreToolUse`
2. Use `updatedInput` to adjust only the following:
   - Align known synonyms to canonical values
   - When blank, add safe default candidates as supplementary text
   - Values not in the choices are not forcibly converted; return them to the question as-is
3. When a change is made, briefly leave a trace of "what was completed"

#### What Is Acceptable to Normalize

- `solo`, `single`, `individual` → `solo`
- `team`, `issue`, `github issue` → `team`
- `browser exploratory`, `exploratory`, `check by touching` → `exploratory`
- `browser scripted`, `playwright`, `fixed steps` → `scripted`

#### What Must Not Be Normalized

- Proper nouns freely entered by the user
- Summaries that change the scope breadth
- Yes/no decisions related to security or permissions

#### Change Candidates for Next Implementation

- `.claude-plugin/hooks.json`
- `hooks/hooks.json`
- `PreToolUse` handler under `scripts/hook-handlers/`
- `skills/harness-plan/SKILL.md`
- `skills/harness-release/SKILL.md`
- `tests/test-claude-upstream-integration.sh`

#### Criteria for Done

- Both the value completed by `updatedInput` and the original input can be tracked
- Only acts on aligning known choices without rewriting intent
- The number of interactions decreases, while safely returning to the original input when a misconversion occurs
