---
name: claude-setup-tuneup
description: Audit and tune a Claude Code setup (CLAUDE.md files, rules, memory, settings, hooks, skills, session habits) against sourced best practices from Anthropic's docs and the Claude Code team, and design multi-step workflows with the Command → Agent → Skill pattern. Use when the user says "improve my claude setup", "audit my CLAUDE.md", "claude keeps ignoring my instructions", "best practices", "optimize claude code", "why is my context filling up", or asks how to structure a workflow out of commands, agents and skills.
---

# Claude setup tune-up

Built around github.com/shanraisshan/claude-code-best-practice (community repo, MIT, 66k★). The repo is a curated, **sourced** list of tips from Boris Cherny, Thariq, Cat Wu and others on the Claude Code team, plus the community. It is not a skill and not made by Boris. Its own README says to read it as a course. This skill turns it into an audit you can actually run.

## 1. Get the current tips

The repo changes almost daily, so read it fresh:

```bash
gh api repos/shanraisshan/claude-code-best-practice/readme -H "Accept: application/vnd.github.raw" > /tmp/ccbp.md
# no gh (cloud routine)? same file, no auth:
curl -sL https://raw.githubusercontent.com/shanraisshan/claude-code-best-practice/main/README.md > /tmp/ccbp.md
```

Read the `TIPS AND TRICKS` section. Every tip links its source. Weight them: Anthropic docs and Claude Code team > named community practitioners > everything else. Before recommending a tip that names a feature, flag or number, confirm it on code.claude.com/docs. Any docs page comes back as plain markdown if you add `.md` (`curl -sL https://code.claude.com/docs/en/memory.md`). Tips go stale when features change.

## 2. Audit

Read the user's real setup first: `~/.claude/CLAUDE.md`, any project `CLAUDE.md` / `.claude/rules/`, `~/.claude/settings.json`, the memory index `MEMORY.md`, and `ls ~/.claude/skills`. Then check these (verified against the official docs, 2026-09-25):

| Check | Why | Source |
|---|---|---|
| Each CLAUDE.md under 200 lines | Longer files cost context on every session and get followed less | code.claude.com/docs/en/memory |
| Instructions that only matter for some files live in `.claude/rules/*.md` with `paths:` frontmatter | They load only when Claude touches matching files | docs, memory → path-specific rules |
| Personal cross-project preferences live in `~/.claude/rules/` | Loads everywhere without bloating CLAUDE.md | docs, memory → user-level rules |
| `@imports` aren't a size fix | Imported files still load at launch (max 4 hops deep); only path-scoped rules actually defer context | docs, memory → imports |
| Memory index stays lean | Only the first 200 lines or 25KB of `MEMORY.md` load at start | docs, memory → auto memory |
| Anything that must *always* happen is a setting or hook, not prose | CLAUDE.md is context, not enforcement; use `settings.json` or a PreToolUse hook to block actions | docs, memory + hooks guide |
| Skill descriptions say what **and** when, with trigger phrases, key use case first | That's how skills get picked up; `description` + `when_to_use` is cut at 1,536 characters in the listing | code.claude.com/docs/en/skills |
| Skills meant to run from a scheduled task don't set `disable-model-invocation: true` | Since v2.1.196 that flag also stops the skill from running when a schedule fires with it as the prompt | skills docs → frontmatter |
| No overlapping skills doing the same job | Duplicates split triggering | judgement |

Session habits to suggest when relevant, all from the Claude Code team via the repo:
- New task, new session. Long sessions degrade well before the window is full.
- `/compact` with a focus hint beats waiting for autocompact.
- Rewind to before a failed attempt instead of stacking corrections on top of it.
- Send search-heavy work to a subagent; only its conclusion comes back.
- Plan first for big changes, and have a second Claude review the plan.

## 3. Report, then apply

Give the user a short prioritized list: the change, the file, why, and the source link. Apply edits only after a yes. Never paste the repo's tip list wholesale. Link it.

## 4. Designing a workflow: Command → Agent → Skill

Use this when building a multi-step automation:
- **Command**: the entry point. Takes input and talks to the user. Custom commands are merged into skills now, so build it as `.claude/skills/<name>/SKILL.md` with `disable-model-invocation: true` (only `/name` starts it). Old `.claude/commands/<name>.md` files still work (checked on code.claude.com/docs/en/skills, 2026-09-24).
- **Agent**: does the heavy lifting in its own context, with the skills it needs preloaded, and returns a compact result (`.claude/agents/<name>.md`).
- **Skill**: produces the output in a consistent format (`.claude/skills/<name>/SKILL.md`).

A working reference is in the repo: `.claude/commands/weather-orchestrator.md` → `.claude/agents/weather-agent.md` → its skills. Read it with `gh api repos/shanraisshan/claude-code-best-practice/contents/<path> -H "Accept: application/vnd.github.raw"`.
