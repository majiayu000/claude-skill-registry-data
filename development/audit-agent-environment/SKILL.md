---
name: audit-agent-environment
description: Audit a Claude Code and Codex setup (CLAUDE.md, AGENTS.md, skills, plugins, config) for token usage, workflow friction, and tool vs. script vs. skill fit, then recommend and apply fixes. Use when sessions feel slow or costly, before adding skills, or as periodic cleanup.
---

# Audit Agent Environment

Measure what every session pays for before it does any work, find the waste and the friction, and move each workflow to the lightest mechanism that does it well.

## Reasoning Framework

Every session starts by loading the instruction files plus a description of every skill it can see, in both Claude Code and Codex, whether or not the task needs them. That cost repeats for every session in every repo the files apply to. The fix is structural:

- Always-loaded files hold only the rules every session needs.
- Procedures live in skills, which load only when used.
- Deterministic work lives in scripts, which cost zero context and can be tested.

Measure first: `scripts/token_audit.py` produces the numbers, and this skill supplies the judgment.

## Output Contract

| Artifact | Format | Handed to |
|----------|--------|-----------|
| Baseline | `scripts/token_audit.py` report (plus the measured Codex prompt) | User |
| Audit report | Markdown: findings ranked by impact and effort, each with evidence and a fix | User |
| Applied changes | Repo edits on a branch, with before/after numbers | User, for review |

## When to Use

- Sessions feel slow, expensive, or forgetful of rules
- Before adding a batch of skills or plugins
- Setting up a repo so Claude Code and Codex both work well in it
- Quarterly hygiene

## When NOT to Use

- Debugging one misbehaving skill's content: edit that skill (or use `skill-creator`)
- Measuring a single live session's context: run `/context` in Claude Code

## Inputs

1. **Repos to audit**: default is the current repo.
2. **Include user-level config?** `~/.claude` and `~/.codex`, read-only.
3. **Harness usage**: what each harness does in each repo (same work, or different roles).
4. **Permission to apply**: repo edits are made on a branch. Global config changes need explicit approval, one change at a time.

## Steps

1. **Measure (script)**, from the pm-skills repo:
   ```bash
   python3 scripts/token_audit.py --repo <path> --global --codex
   ```
   `--codex` renders Codex's real startup prompt with `codex debug prompt-input`, which makes no model call. For Claude Code, ask the user to paste `/context` from a session if you need the harness's own prompt, tool, and MCP overhead, which the script cannot see.
2. **Triage the instruction files.** Put every section of CLAUDE.md and AGENTS.md in one of four buckets: needed every session, needed for some tasks, reference, or stale or contradictory. Move "some tasks" into a skill or a doc linked by plain path. Don't use an `@` import, because imports load at launch. Delete what is stale, and check git history for sections that came back by accident.
3. **Find duplication:**
   - Skill catalogs pasted into instruction files. The harness already lists every skill.
   - The same rules in CLAUDE.md and AGENTS.md. When both harnesses do the same work, symlink `AGENTS.md` → `CLAUDE.md` (Codex follows it). When their roles differ, keep two files and share nothing by copy.
   - The same skill listed twice, for example a plugin and a synced copy.
4. **Classify workflows** with the decision rules below. Look for deterministic steps written as skill prose (parsing, counting, scoring, math, validation), repeated multi-command sequences, scripts without tests, and subagents spawned for single lookups.
5. **Check skill hygiene:**
   - Placeholder skills. Their descriptions load every session, so finish or delete them.
   - Descriptions that never say when to use the skill.
   - Overlapping skills with no "When NOT to use" section.
   - Descriptions over about 400 characters without eval evidence that the length helps.
   - SKILL.md files over 500 lines. Split reference material into `references/`.
6. **Check cross-harness parity:**
   - Codex scans `.agents/skills`, plus the legacy `.codex/skills`, and not `.claude/skills`. Link `.agents/skills` → `../.claude/skills` for parity.
   - Codex recurses into nested folders, while Claude Code only looks one level deep. Move nested skill libraries out of the skills tree first.
   - Codex drops AGENTS.md content past 32 KiB (`project_doc_max_bytes`).
   - Project-specific skills installed at user level leak into every repo.
   - Folders without a SKILL.md in skill roots are orphans.
7. **Review defaults.** Compare model and reasoning effort per harness with the task mix, for example 1M-context models for small doc edits, or config that contradicts what the docs claim. Recommend changes; don't make them.
8. **Report** using the template. Put a token or reliability impact on every finding.
9. **Apply** with approval: repo changes on a branch; `bash scripts/check.sh` must pass. Rerun step 1 and report before and after.

## Decision Rules: Tool, Script, Skill, or Subagent

| Mechanism | Use for | Signals |
|---|---|---|
| **Tool** (direct command) | One-off reads, searches, git or gh queries, a single edit | Fewer than about 3 commands, no reuse expected |
| **Script** (`scripts/`, tested) | Anything deterministic: parse, merge, count, score, compute, validate, format | Same input gives the same output; run a third time; arithmetic or counting involved |
| **Skill** (`.claude/skills/`) | Judgment-heavy procedures that repeat: synthesis, writing, analysis, reviews | Needs context, taste, or trade-offs; the same steps every time |
| **Subagent** | Independent, parallel, sizable work with clear ownership | Worth the hand-off cost; no file overlap; you only need the conclusion |

Graduation rule: a one-off check stays a command. Run it a third time and it becomes a script. A script plus recurring judgment becomes a skill that calls the script. Never create a skill for a deterministic task.

## Report Template

```markdown
# Agent Environment Audit: [repo(s)], [date]

## Baseline (before)
| Harness | Always loaded (≈ tokens) | Skills listed | Notes |

## Findings
| # | Finding | Evidence | Impact | Fix | Effort |
|---|---|---|---|---|---|
| 1 | [..] | [measured number or file:line] | [tokens/session or reliability] | [..] | S/M/L |

## Recommended changes
Repo (applied on a branch): ..
Global (needs your approval): ..

## After
| Harness | Always loaded (≈ tokens) | Skills listed | Change |
```

## Examples

- "Audit this repo for token usage." Measure, find a 259-line CLAUDE.md with a duplicated skill catalog and 9 placeholder skills, move reference sections to docs, finish or delete the placeholders, and report the before/after.
- "Codex feels slow in my app repo." Run with `--codex` and find a 27 KB AGENTS.md at 83% of the 32 KiB cap. Recommend moving procedures into skills or a playbook.

## Guardrails

- Measure, don't guess. Label every estimate (characters ÷ 4) as an estimate.
- Never print secrets. The script reads only model and effort keys from config files. Don't `cat` auth or config files into the conversation.
- Don't delete skills, plugins, or memories, or edit `~/.claude` or `~/.codex`, without explicit approval of that specific change.
- Keep changes reversible and one concern per commit.
- Don't copy private repo details into public repos. Generalize the lesson instead.

## Related Skills

- `skill-creator` (plugin): improve an individual skill's description with trigger evals
- `engineering-foundations`: habits behind scripts-first and tested tooling
