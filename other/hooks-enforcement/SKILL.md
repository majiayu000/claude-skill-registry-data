---
name: hooks-enforcement
description: Optional Claude Code hook config that mechanically assists AI-01–AI-03, and separately hard-gates git commit on the pre-commit skill. Trigger when installing into a Claude Code project using ai-standards.md and/or pre-commit.
compat: claude-code-only
---

# Hooks Enforcement — Claude Code Only

**This is Claude Code-only: it needs Claude Code's hook system (`SessionStart`, `PreToolUse` events in `.claude/settings.json`) — no other tool this kit targets has an equivalent.**

`ai-standards.md`'s context-integrity rules (AI-01–AI-03) work by prompt compliance — the model polices itself, which degrades exactly when context pressure is highest. Claude Code hooks can inject deterministic reminders and block tool calls; they cannot verify prose output. This skill automates the *reminder*, not the *verification* — say so plainly rather than overselling it.

`ai-standards.md` remains the authoritative, tool-agnostic contract regardless of whether this is installed — never make any rule depend on this skill being present.

## Self-improvement (do this first and last)
1. **At start:** read `learnings.md` in this skill's folder if it exists. Apply relevant lessons.
2. **At end of every use:** append one dated bullet — a case this caught, a false block, or a hook exit-code behavior that didn't match what's documented here. Merge instead of duplicating; delete disproven bullets.

## Non-goal
This cannot confirm `[CX]` is honest — only that a proxy artifact exists. Residual reliance on prompt compliance is inherent and stays. Do not describe this as "enforcing" AI-01–AI-03 in project docs; describe it as assisting.

## `handover/` guard (hard rule)
**Hooks configured by this skill must never read, write, or gate on any path under `handover/`.** Lane coordination in `role-session` stays exclusively inside the model-driven claim protocol — a hook racing `locks.md` outside the dev's visibility corrupts claims silently.

## Sample config
`SessionStart` hook — injects the AI-02 declaration reminder into every new session's context, since a model under context pressure is the one most likely to skip it unprompted:
```json
{
  "hooks": {
    "SessionStart": [
      { "hooks": [{ "type": "command", "command": "echo 'Reminder: state loaded standards (AI-02) before any work, and write .claude/.standards-declared once done.'" }] }
    ]
  }
}
```
`PreToolUse` hook (matcher `Edit|Write`) — blocks the first edit until the model has completed its own AI-02 declaration:
```json
{
  "hooks": {
    "PreToolUse": [
      { "matcher": "Edit|Write", "hooks": [{ "type": "command", "command": "test -f .claude/.standards-declared || { echo 'Standards not declared yet (AI-02) — state loaded standards, then create .claude/.standards-declared, before editing.' >&2; exit 2; }" }] }
    ]
  }
}
```
The marker file is written by the **model**, as the last step of its AI-02 declaration — never by the hook itself, which only checks for it.

Merge this into the target's `.claude/settings.json` — never overwrite an existing one.

## Pre-commit gate (separate from AI-01–AI-03, same hook mechanism)

Skill triggers that depend on the model noticing a moment in conversation ("this is the done-moment", "this is a bug worth investigating") cannot be hooked — there's no tool-call event to match on. `git commit` is different: it's an actual Bash call, so it's mechanically detectable. This gate hard-blocks it until `pre-commit`'s checklist has actually run.

`PreToolUse` hook (matcher `Bash`) — blocks any Bash call containing `git commit` until the marker file exists:
```json
{
  "hooks": {
    "PreToolUse": [
      { "matcher": "Bash", "hooks": [{ "type": "command", "command": "bash .claude/hooks/pre-commit-gate.sh" }] }
    ]
  }
}
```
`PostToolUse` hook (matcher `Bash`) — clears the marker after any `git commit` call, so the next commit needs a fresh declaration:
```json
{
  "hooks": {
    "PostToolUse": [
      { "matcher": "Bash", "hooks": [{ "type": "command", "command": "bash .claude/hooks/pre-commit-clear.sh" }] }
    ]
  }
}
```
Both scripts live in `.claude/hooks/` (companion files of this skill, install alongside it) and parse the hook's stdin JSON for `tool_input.command`, matching the substring `git commit`. **Known limitation:** substring matching means a Bash command whose *text* merely mentions "git commit" (e.g. `echo "run git commit next"`) also blocks — a false positive, not a false negative. Acceptable trade-off since the failure mode leans safe (over-blocks rather than under-blocks), but don't oversell this as precise command parsing.

The marker (`.claude/.pre-commit-declared`) is written by the **model**, as the last step of actually running `pre-commit`'s checklist — never by the hook itself.

### What the gate checks, beyond the marker

Once the marker exists, the gate script also runs two mechanical checks the `pre-commit` skill would otherwise re-derive by reasoning over `git diff` output every time — moving pure pattern-matching out of the model loop:

1. **Debug leftovers in the staged diff** — greps added lines (`git diff --cached -U0`, excluding `.claude/**`) for `console.log(`, `console.debug(`, `debugger;`, `FIXME`. Blocks with the offending `file:line`s on match. Deliberately excludes bare `TODO` (too common as legitimate deferred work) and doesn't attempt `print(`/language-specific probes — extend the pattern in the script per project if needed.
2. **Commit message format** — extracts the `-m "..."` argument and checks it against Conventional Commits (git-standards RULE G-06/G-07: `type: summary` with type in `feat|fix|patch|style|refactor|chore|docs|test|remove`) and the 50-char header limit (RULE G-08). This assumes the project's `git-standards.md` is still the kit default — if a project overrides commit format, either edit the regex in the script or drop this block.

**Known regex-engine trap (fixed once, documented so it isn't reintroduced):** the diff-header exclusion line originally used plain `grep -v '^\+\+\+'` (BRE). GNU BRE treats `\+` as a quantifier, not a literal `+`, so `\+\+\+` parsed as a degenerate quantifier chain and matched *every* line starting with `+` — silently swallowing all staged additions, not just the `+++ b/file` diff header, and making the debug-leftover check permanently pass with no findings. Fixed by using `grep -vE '^\+\+\+'` (ERE, where `+` needs no escaping as a literal within `\+` under `-E` semantics is unambiguous). Verified via manual stdin-JSON test invocations of the script (bypassing the live PreToolUse gate itself, which intercepts any Bash call whose *text* contains "git commit" — including test payloads — per the substring-matching limitation above).

## Reminder-only assist for non-hookable triggers

`SessionStart` hook — for skills with no tool-call event to gate on (e.g. `debug-protocol`'s "two failed fixes" or "hunting a bug" trigger), inject a plain-text reminder instead of attempting to block anything:
```json
{
  "hooks": {
    "SessionStart": [
      { "hooks": [{ "type": "command", "command": "echo 'Reminder: debug-protocol applies when hunting a bug/regression, or after two failed fixes — invoke it explicitly instead of continuing ad hoc edits.'" }] }
    ]
  }
}
```
This is a nudge, not enforcement — nothing stops the model from ignoring it, same limitation as the base AI-02 reminder above.

## Staleness guard
Hook exit-code semantics (0 = allow, 2 = block with stderr shown to the model) and event names can change between Claude Code CLI versions. Confirm current behavior against the live Claude Code docs before relying on this in a production project — treat the block above as a starting point, not a guarantee.

## Failure mode this prevents
A session drifting past its context window silently drops the AI-02 declaration and nothing catches it until a later response is discarded for missing `[CX]` — by then the drift has already cost a turn. A hook-level check surfaces the same gap before any edit happens, at zero model-token cost.
