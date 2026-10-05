---
name: go
description: "Accept the recommendation from the most recent A/B/C option set and execute it without re-asking — for \"按你推荐的来\" / \"go with your pick\", when the user glanced at the options and wants the recommended branch executed immediately."
---

# Clade for Codex

This workflow runs **directly in Codex**. Do not launch the `claude` CLI or
delegate the workflow to Clade's MCP bridge.

Codex compatibility rules:

- Plugin skills are namespaced. Invoke this workflow explicitly as
  `$clade:go`; a bare `$name` does not select the installed Clade plugin.
- Read the nearest `AGENTS.md` files for repository instructions. If a project
  has only `CLAUDE.md`, treat it as legacy project guidance and read it too.
- Store new Clade working state under `.clade/` (or `~/.clade/` for personal
  state). Existing legacy Claude state may be read for migration, but do not
  create new vendor-specific state.
- A `/skill-name` reference means the corresponding Codex
  `$clade:skill-name` plugin skill, or the same workflow invoked naturally when
  explicit skill invocation is not available.
- Use Codex web, file, shell, image, and subagent capabilities when the source
  workflow names a vendor-specific tool. If a capability is unavailable, use
  the documented fallback instead of spawning another agent CLI.
- Paths such as `<plugin-root>/...` are relative to the installed Clade plugin
  containing this `SKILL.md`; resolve that root before invoking a helper.

## Canonical Clade workflow

<command-metadata>
name: go
trigger: user says "按推荐的来" / "go with your pick" after you offered enumerated options
completion-status: DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT
</command-metadata>

The user just saw a set of options you offered (numbered issues with A/B/C sub-options, or a recommendation block with alternatives). They don't want to re-read them — they want the one YOU recommended to be executed now.

## Execution

### Step 1: Locate the most recent options block

Scan the prior assistant messages in this conversation for the most recent message that:
- Enumerated 2+ options (A/B/C, 1/2/3, "Option 1/Option 2"), OR
- Presented a "Top pick" / "Recommended" / "Default" alongside alternatives

If multiple option sets exist in recent history, use the **most recent one that is still actionable** — ignore ones already resolved by subsequent messages.

### Step 2: Identify the recommendation

Look for an explicit recommendation marker:
- Words like "recommend", "推荐", "I'd go with", "Top pick", "Default:", "Suggest"
- A pick you marked with `★`, `▶`, bold, or placed first as "the one to pick"

### Step 3: Confirm and execute

**If the recommendation is unambiguous:**
- State in one line: `→ going with {option label}: {short description}`
- Execute immediately — no re-asking, no re-explaining tradeoffs
- Proceed to the full task the options were gating

**If options existed but no clear recommendation was flagged:**
- Surface the top 2 in a single line each with tradeoffs
- Ask: "No clear default in my last message — {A} or {B}?"
- Do NOT execute until the user picks

**If no recent options block exists (within the last ~5 assistant turns):**
- Respond: "Nothing pending to pick — what would you like me to go with?"
- Stop.

## Rules

- **One sentence of confirmation, then act.** This skill exists because the user wants speed.
- **Don't re-derive** the recommendation — trust what you already decided. If you said "I recommend A" 30 seconds ago, pick A now.
- **Don't expand scope.** `/go` executes the specific option; it doesn't also kick off related work you didn't offer.
- **If the recommended option has side effects that need confirmation** (file deletion, `git reset --hard`, force-push, migrations, `.env` edits): confirm once before executing. `/go` does not override the destructive-action rule in AGENTS.md.
- **Multiple numbered issues with their own A/B/C** (e.g. from Plan Mode): pick the recommended letter for each numbered issue and execute them in order. Mention the combined choice in one line (e.g. `→ going with 1A, 2B, 3A`).

## Completion Status

- ✅ **DONE**: Identified recommendation, executed it, produced the expected output.
- ⚠ **DONE_WITH_CONCERNS**: Executed but noticed the recommendation now looks weaker than when first given — flag that.
- ❌ **BLOCKED**: No clear recommendation or no recent options — asked user for clarification.
- ❓ **NEEDS_CONTEXT**: Recommendation requires a destructive action that needs explicit approval.

## Additional skill reference

# Go Skill

The user just saw a set of options you offered (numbered issues with A/B/C sub-options, or a recommendation block with alternatives). They don't want to re-read them — they want the one YOU recommended to be executed now.

## Execution

### Step 1: Locate the most recent options block

Scan the prior assistant messages in this conversation for the most recent message that:
- Enumerated 2+ options (A/B/C, 1/2/3, "Option 1/Option 2"), OR
- Presented a "Top pick" / "Recommended" / "Default" alongside alternatives

If multiple option sets exist in recent history, use the **most recent one that is still actionable** — ignore ones already resolved by subsequent messages.

### Step 2: Identify the recommendation

Look for an explicit recommendation marker:
- Words like "recommend", "推荐", "I'd go with", "Top pick", "Default:", "Suggest"
- A pick you marked with `★`, `▶`, bold, or placed first as "the one to pick"

### Step 3: Confirm and execute

**If the recommendation is unambiguous:**
- State in one line: `→ going with {option label}: {short description}`
- Execute immediately — no re-asking, no re-explaining tradeoffs
- Proceed to the full task the options were gating

**If options existed but no clear recommendation was flagged:**
- Surface the top 2 in a single line each with tradeoffs
- Ask: "No clear default in my last message — {A} or {B}?"
- Do NOT execute until the user picks

**If no recent options block exists (within the last ~5 assistant turns):**
- Respond: "Nothing pending to pick — what would you like me to go with?"
- Stop.

## Rules

- **One sentence of confirmation, then act.** This skill exists because the user wants speed.
- **Don't re-derive** the recommendation — trust what you already decided. If you said "I recommend A" 30 seconds ago, pick A now.
- **Don't expand scope.** `/go` executes the specific option; it doesn't also kick off related work you didn't offer.
- **If the recommended option has side effects that need confirmation** (file deletion, `git reset --hard`, force-push, migrations, `.env` edits): confirm once before executing. `/go` does not override the destructive-action rule in AGENTS.md.
- **Multiple numbered issues with their own A/B/C** (e.g. from Plan Mode): pick the recommended letter for each numbered issue and execute them in order. Mention the combined choice in one line (e.g. `→ going with 1A, 2B, 3A`).

## Completion Status

- ✅ **DONE**: Identified recommendation, executed it, produced the expected output.
- ⚠ **DONE_WITH_CONCERNS**: Executed but noticed the recommendation now looks weaker than when first given — flag that.
- ❌ **BLOCKED**: No clear recommendation or no recent options — asked user for clarification.
- ❓ **NEEDS_CONTEXT**: Recommendation requires a destructive action that needs explicit approval.

## Delivery completion

If this workflow changes files or external state:

- Inspect the real final state before responding, including `git status` for a
  repository task.
- Never report `DONE` while task-owned changes are uncommitted. Use or continue
  `$clade:delivery` and create a repository-compliant checkpoint or preserve
  the work when committing is unavailable.
- When the user request or trusted repository policy makes publication,
  deployment, or live verification part of the task, do not silently downgrade
  the result to local-only work.
- If a required delivery transition lacks authority, credentials, a destination,
  or reachable external state, report `BLOCKED` or `NEEDS_CONTEXT` rather than
  appending a "not committed/pushed/deployed" caveat after `DONE`.
