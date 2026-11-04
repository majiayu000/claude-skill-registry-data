---
name: ai-harness
description: >-
  How this repo's Claude Code harness works and how to change it safely: .claude agents, skills, hooks,
  settings and commands; rules in tools/harness/hook-rules.mjs with tests; adding an agent or skill; hook
  design rules; the audit. Use when editing anything in .claude/, tools/harness, CLAUDE.md, or for "add an
  agent", "new skill", "the hook blocked me", "why was this denied?".
---

# AI harness

Owner: the `harness-engineer` agent. The harness steers every session, so a wrong rule here costs more than a
wrong line of app code.

## Layout

| Path                             | What                                                                                                                      |
| -------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| `CLAUDE.md`                      | rules, stack, layout, team table. Short and true; details go in skills                                                    |
| `AGENTS.md`                      | pointer for other agent tools                                                                                             |
| `.claude/settings.json`          | permission allow/deny lists, hook wiring                                                                                  |
| `.claude/agents/<name>.md`       | one specialist each: frontmatter (`name`, `description`, `tools`, `model`, optional `skills`, `hooks`, `memory`) + prompt |
| `.claude/skills/<name>/SKILL.md` | procedures and knowledge, loaded on demand                                                                                |
| `.claude/commands/<name>.md`     | slash commands (none yet)                                                                                                 |
| `.claude/hooks/*.mjs`            | thin I/O wrappers                                                                                                         |
| `tools/harness/hook-rules.mjs`   | **all rule logic**, pure functions                                                                                        |
| `tools/harness/git-context.mjs`  | branch / dirty facts for hooks                                                                                            |
| `tools/harness/frontmatter.mjs`  | tiny frontmatter reader for the audit                                                                                     |
| `tools/harness-audit.mjs`        | `pnpm run audit:harness`                                                                                                  |
| `tools/guardrails-audit.mjs`     | `pnpm run audit:guardrails`                                                                                               |
| `tools/__tests__/*.test.mjs`     | `pnpm run test:tools` (`node --test`)                                                                                     |

## Hooks

| Hook                 | Event / matcher                  | Effect                                                                                           |
| -------------------- | -------------------------------- | ------------------------------------------------------------------------------------------------ |
| `session-start.mjs`  | SessionStart                     | branch, dirty tree, days to deadline, the hard rules                                             |
| `pre-edit.mjs`       | PreToolUse Edit/Write/MultiEdit  | **deny**: protected files (lockfile, .env, build output), official-mark assets                   |
| `pre-bash.mjs`       | PreToolUse Bash                  | **deny**: npm/npx/yarn, no-verify, force-push, push to main; **ask**: `gh pr merge`, prod deploy |
| `post-edit.mjs`      | PostToolUse Edit/Write/MultiEdit | Prettier; **block** new hex in apps/ui; one-off reminders                                        |
| `read-only-bash.mjs` | agent frontmatter                | read-only Bash for reviewers and planners (`--allow` for scoped writers)                         |
| `edit-allowlist.mjs` | agent frontmatter                | per-agent edit scope (`--allow`, `--ask`)                                                        |

### Design rules

1. **Pure rules + thin I/O.** Logic in `hook-rules.mjs`, unit-tested. Hooks parse stdin, call a rule, and
   print the decision.
2. **Pick the right strength.** `deny` for what must never happen (Claude changes course). `ask` for what the
   user may want (they confirm). PostToolUse `block` for "fix before moving on". Plain context for reminders.
3. **Fast prefilter.** Bash hooks bail out early unless the command mentions a guarded tool.
4. **Never break on missing input.** No payload, no git, outside the repo: exit 0 silently.
5. **Explain the way out.** Every message says what to do instead and names the skill.
6. Rule sources (`tools/`, `.claude/`, `docs/`, `CLAUDE.md`) are exempt from the official-marks content check
   (`isRuleSource`), because they must name what they forbid.

### Known false positive

`pre-bash.mjs` scans the whole command text, including heredoc bodies. Writing a file that _mentions_ a
forbidden command through `cat <<EOF` gets denied. Write files with the Write tool instead. In tests, build
such strings from parts (see `hook-rules.test.mjs`).

## Adding or changing an agent

1. `.claude/agents/<name>.md`, where `name` equals the file name. The `description` says when to use it, with
   trigger phrases (the router reads only this).
2. Tools: least privilege. Reviewers and planners get the `read-only-bash.mjs` hook and no Edit/Write. Scoped
   writers get `edit-allowlist.mjs` with their paths.
3. Add its paths to the ownership map in the `add-feature` skill and the team table in `CLAUDE.md`.
4. Reference other agents and skills by exact name (the name in backticks followed by the word agent or
   skill). The audit checks them.
5. Body sections, as in the others: role, read first, how you work, what you own, before you report back,
   report format.

## Adding or changing a skill

1. `.claude/skills/<name>/SKILL.md`, where `name` equals the folder. The description covers what it is **and**
   when to trigger.
2. Concrete and repo-specific: paths, commands, tables. Push long references into sibling files in the skill
   folder.
3. Link it from the agents that follow it and from the ownership map.

## Changing a rule

1. Edit `tools/harness/hook-rules.mjs` and add or adjust a test in `tools/__tests__/hook-rules.test.mjs`
   first.
2. `pnpm run test:tools`, `pnpm run audit:harness`.
3. Try the hook by hand:
   `echo '{"tool_name":"Bash","tool_input":{"command":"git status"}}' | node .claude/hooks/pre-bash.mjs`.

## Verify

`pnpm run test:tools && pnpm run audit:harness && pnpm run audit:guardrails`, then start a new session (or
`/agents`) and confirm new agents and skills appear in the lists. A file that exists but doesn't load helps
nobody.
