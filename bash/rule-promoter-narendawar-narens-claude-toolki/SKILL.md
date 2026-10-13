---
name: rule-promoter
description: "Use when the user wants rules in CLAUDE.md enforced with hooks, says Claude keeps ignoring a CLAUDE.md rule, or asks to turn CLAUDE.md rules into hooks (for example 'promote my CLAUDE.md rules to hooks' or 'make Claude stop editing migrations')."
---

# Rule Promoter

## Overview

CLAUDE.md rules are advice: Claude can rationalize past them. A hook is enforcement. This skill reads the project's CLAUDE.md, picks out the rules a hook can actually enforce, writes them into a rules file enforced by a small tested engine, proves each rule blocks a violation, and installs the hooks after the user confirms. It runs only when the user asks. Hooks are guardrails, not a security boundary: a determined workaround (a helper script, `sh -c`) can get past a pattern. Say so.

## Files (in this skill's base directory, shown when the skill loads)

- `scripts/rule_hook.py`: the engine. Copy it to `.claude/hooks/rule_hook.py` in the project. `python rule_hook.py selftest` proves every rule; `check` is the hook entry point.
- `scripts/settings_merge.py`: `launcher` picks a Python command that works; `plan` shows the settings diff; `apply` writes it.

Run both with a Python 3 command that works on this machine (try `python3`, `python`, `py -3`). Quote paths.

## Process

1. **Read.** Find `CLAUDE.md`, `.claude/CLAUDE.md` and `CLAUDE.local.md` in the project. List every rule with its file and line. If there is none, say so and stop.
2. **Classify** each rule into exactly one of:
   - an engine type (below) with concrete parameters;
   - `taste`, with a one-line reason;
   - `needs input`, with the specific question to ask (for example "which command runs your tests?").

   A rule is enforceable only if it names concrete tools, paths, commands or text patterns, and a violation is detectable from one tool call or from an end-of-turn command's exit status. When unsure, mark it `needs input` and ask; never guess a pattern for a vague rule. Never invent a rule type.
3. **Review.** Show a table: rule, type, pattern or command, a sample violation, a sample pass, and the false-positive risk. Show every `stop_check` command verbatim. Ask the user to drop or adjust rows. Write nothing yet.
4. **Prove.** After approval, create `.claude/hooks/` and copy `scripts/rule_hook.py` there, write `.claude/rules.json`, then run `python .claude/hooks/rule_hook.py selftest` from the project root. Show the output. A rule whose proof fails is not installed: fix its pattern or drop it, and say which one.
5. **Install.** Run `settings_merge.py launcher --script .claude/hooks/rule_hook.py`, then `settings_merge.py plan --settings .claude/settings.json --launcher "<launcher>" [--pretool] [--stop]` (`--pretool` if any path, command or content rules exist; `--stop` if any stop_check rules exist). Show the diff and ask for a yes. Only after a yes, run the same command with `apply`. If it reports invalid settings JSON or a duplicate key, stop and tell the user; do not edit the file by hand. The helper removes only its own `rule_hook.py` entries and leaves every other hook alone. If the end-to-end check below shows the hook did not fire although `selftest` passes and `disableAllHooks` is not set, some Claude Code versions lack exec-form `args`: re-run `plan` and `apply` with `--shell-form`.
6. **Verify end to end.** If you can run `claude -p` in the project, test with a `protected_path` or `banned_content` rule against a throwaway file (for example ask it to edit `tmp-rule-check.txt` under a protected glob), never with a `blocked_command` or `stop_check` that would really run something, and undo any change afterwards. Check `disableAllHooks` in the project, local and user settings before concluding anything. Confirm the output shows the `Rule <id>:` block message, and show it. If you cannot run a nested session, say so and say the install is verified only by `selftest`.
7. **Report.** List the promoted rules, the skipped rules with reasons, and one limitation: Claude can still edit `.claude/rules.json`, `.claude/hooks/` and `.claude/settings.json`. Offer to add a `protected_path` rule for them, and say it also blocks re-running this skill until the rule is disabled. Then say how to turn things off: set `"enabled": false` on a rule in `.claude/rules.json`, or delete the `rule_hook.py` entries from `.claude/settings.json`.

Never write `rules.json`, hook files or `settings.json` before the user has reviewed the table. Never write `settings.json` before showing the diff and getting a yes.

If the user adds a rule or changes a pattern after the table, or you have to change a pattern because it is invalid or its proof fails, show that new or changed row (pattern, sample violation, sample pass, risk) and wait for a yes before writing anything. An approval given earlier does not cover a different pattern, and never substitute a pattern the user did not see.

## Rule types

Every rule has `id` (kebab-case), `source` (`CLAUDE.md:14`), `text` (the original rule), `message` (shown to Claude when blocked), `type`, the fields below, and a `proof` with a `violation` and a `pass` payload.

**protected_path**: no edits to matching files. Globs match the whole project-relative path; use `**/name` for any depth.

```json
{"id": "no-migration-edits", "source": "CLAUDE.md:3", "text": "Never edit anything under migrations/",
 "type": "protected_path", "globs": ["**/migrations/**"], "allow_globs": [],
 "message": "Migrations are generated. Create a new migration instead.",
 "proof": {"violation": {"hook_event_name": "PreToolUse", "tool_name": "Edit", "tool_input": {"file_path": "app/migrations/0001_initial.py", "old_string": "a", "new_string": "b"}},
           "pass": {"hook_event_name": "PreToolUse", "tool_name": "Edit", "tool_input": {"file_path": "app/models.py", "old_string": "a", "new_string": "b"}}}}
```

**blocked_command**: Bash commands matching a regular expression, tested against each segment of a compound command. Use `except_patterns` for safe variants; an exception exempts the whole segment, so make it specific.

```json
{"id": "no-force-push", "source": "CLAUDE.md:4", "text": "Never run git push --force",
 "type": "blocked_command", "patterns": ["\\bgit\\s+push\\b.*(?:--force\\b|\\s-[A-Za-z]*f[A-Za-z]*\\b|\\s\\+\\w)"], "except_patterns": ["--force-with-lease"],
 "message": "Force pushes are not allowed.",
 "proof": {"violation": {"hook_event_name": "PreToolUse", "tool_name": "Bash", "tool_input": {"command": "git push --force origin main"}},
           "pass": {"hook_event_name": "PreToolUse", "tool_name": "Bash", "tool_input": {"command": "git push origin feature"}}}}
```

**banned_content**: regular expressions that must not appear in the new text being written (Edit, Write, MultiEdit, NotebookEdit), optionally limited by file `globs`. Old text is never inspected.

```json
{"id": "no-console-log", "source": "CLAUDE.md:5", "text": "No console.log( in src/",
 "type": "banned_content", "patterns": ["console\\.log\\("], "globs": ["src/**"],
 "message": "Use the logger, not console.log.",
 "proof": {"violation": {"hook_event_name": "PreToolUse", "tool_name": "Write", "tool_input": {"file_path": "src/a.js", "content": "console.log(1)"}},
           "pass": {"hook_event_name": "PreToolUse", "tool_name": "Write", "tool_input": {"file_path": "src/a.js", "content": "logger.info(1)"}}}}
```

**stop_check**: a command that must succeed before Claude may stop. It blocks the stop when the command exits non-zero. `when_changed_globs` limits it to turns that changed matching files (uncommitted changes only: omit it if Claude tends to commit before stopping). The proof uses `simulate_exit` (selftest does not run the real command).

```json
{"id": "tests-pass", "source": "CLAUDE.md:6", "text": "Run npm test before you finish",
 "type": "stop_check", "command": "npm test", "timeout_seconds": 240, "when_changed_globs": ["src/**", "tests/**"],
 "message": "The tests must pass before you stop.",
 "proof": {"violation": {"hook_event_name": "Stop", "simulate_exit": 1}, "pass": {"hook_event_name": "Stop", "simulate_exit": 0}}}
```

The file is `{"version": 1, "rules": [ ... ]}`. Tool payloads: Bash uses `tool_input.command`; Edit uses `file_path`, `old_string`, `new_string`; Write uses `file_path`, `content`.

## What is enforceable (classification guide)

- Enforceable: "never edit X/", "don't touch .env", "never run Y", "don't use Z in files under W", "run T before finishing".
- Taste: "prefer small functions", "write clear commit messages", "keep the UI accessible", "favor clarity". No pattern can decide these.
- Needs input: "be careful with the database", "make sure tests pass" (which command?), "avoid legacy code" (which paths?). Ask; do not guess.
- Globs support only `*`, `**` and `?`, relative to the project (no `[ab]`, `{a,b}`, leading `./` or `/`); the engine refuses anything else. `timeout_seconds` is at most 280, and `enabled` must be `true` or `false`.
- Prefer narrow patterns. State the false-positive risk for each rule (for example a `main` pattern also matches a branch named `main-menu`) and add `allow_globs` or `except_patterns` when that matters.

## Tone

Brief and factual. This is setup work, not a lecture about rules.

## Common Mistakes

- Writing any file, or settings, before the user has reviewed the table.
- Writing `settings.json` without showing the diff and getting a yes.
- Installing a rule the user has not seen as a table row, or quietly replacing the pattern the user asked for.
- Installing a rule whose proof did not pass.
- Promoting a taste rule, or guessing a pattern for a vague rule.
- Inventing a rule type the engine does not have.
- Leaving out the false-positive risk, or the "guardrail, not a security boundary" caveat.
- Editing an invalid `settings.json` by hand instead of stopping.
- Claiming an end-to-end block you did not actually observe.
