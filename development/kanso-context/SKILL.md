---
name: kanso-context
description: Use when the user asks to update, prune, audit, or create AGENTS.md, CLAUDE.md, or other agent context files. Also use when the user says their AI agents keep making the same mistakes and they want to fix it at the context level.
argument-hint: "[optional: prune|audit|init|sync]"
disable-model-invocation: true
allowed-tools: Bash(git *) Bash(rg *) Bash(find *) Bash(wc *)
---

# kanso-context

Curates agent context files to improve AI-agent reliability on this codebase. Primary target is `AGENTS.md` (cross-tool standard). CLAUDE.md is only updated when guidance is genuinely Claude-specific.

The principles from `kanso-principles` apply. This skill is biased toward deletion.

## The governing evidence

This skill's design is pinned to the empirical record as of 2026:

- **Vercel benchmark:** a lean ~8KB AGENTS.md with a compressed docs index hit 100% on agent evaluations. Skills-only context hit 53%. Skills with explicit invocation instructions hit 79%.
- **ETH Zurich AGENTbench:** LLM-generated context files *reduced* success rates by 0.5-2% and inflated cost by over 20%. Developer-written context files added 4%.
- **Real-world prevalence study (2,303 files):** only 14.5% of context files include security or performance guidance. This is the largest systematic gap.
- **Median effective length:** ~485 words for Claude Code, ~150 lines ceiling for AGENTS.md. Longer files degrade agent performance.

Three practical implications:

1. **This skill does not generate context from scratch.** It prunes, curates, flags gaps, and asks the user to fill them. Generation without the user's input is the failure mode the research warns against.
2. **Less is more.** The default action on any file over 150 lines is to propose deletions.
3. **Security and performance guidance is the universal gap.** Flag it if missing and relevant.

## Modes

`$ARGUMENTS` selects the mode:

- **`audit`** (default) — review existing context files, produce a findings report. No edits.
- **`prune`** — act on audit findings to remove stale, redundant, or noisy content. Edits with approval.
- **`init`** — bootstrap a minimal AGENTS.md for a repo that doesn't have one. Interactive; asks the user for inputs.
- **`sync`** — compare context files against recent PRs (last 20-30 merged) to find drift: instructions that no longer match how the code actually works.

If no argument is given, default to `audit`.

## What belongs in AGENTS.md

Based on the Vercel + empirical studies, ordered by impact:

### Tier 1 — almost always worth including

1. **Exact build/test/lint/run commands.** Never make the agent guess. Not "run the dev server" but `pnpm dev:firefox`. The agent needs these to verify its own output.
2. **Architectural boundaries.** Which modules own which domains. Which directories have which roles. Who owns the database layer, who owns the API layer.
3. **Active conventions.** Naming patterns, error-handling style, forbidden dependencies, deprecated patterns to avoid. Write explicit rules. "Always use named exports" beats "follow best practices".
4. **Explicit "do not" boundaries.** What the agent should never touch. Migration files, production config, generated code. This is the highest-leverage section for preventing costly mistakes.

### Tier 2 — worth including if relevant

5. **Development process.** Branch strategy, commit format, PR requirements. Short: a few lines.
6. **Project overview.** One paragraph. What is this, what's its stack, where does it deploy. Not a marketing blurb.
7. **Security requirements.** Underrepresented in 85.5% of files. If the project has auth, data handling, or compliance constraints, write them down.
8. **Performance requirements.** Same gap. If there's an SLA, a p99 target, or a memory ceiling, the agent should know.

### Tier 3 — usually skip

9. Directory enumerations. Doesn't help the agent find files any faster.
10. Summaries of the README. If it's in the README, link; don't duplicate.
11. Explanations of standard-library patterns or common frameworks. The model already knows.
12. Anything a linter enforces. Let the linter enforce it.

## What to remove

When pruning:

- **Stale instructions.** Rules about a pattern the codebase no longer uses.
- **Redundant content.** Anything duplicated from the README, CONTRIBUTING, or linter config.
- **Vague guidance.** "Follow best practices", "Write clean code", "Be careful". Remove or replace with specifics.
- **Instructions for things the model already knows.** "Use semicolons in JavaScript", "Python uses indentation". Model knows.
- **Codebase overviews.** The research is clear these don't help.
- **AI-generated filler.** Sections written by an agent to pad the file. Usually recognisable by their generic voice.

## The three-level hierarchy (Claude Code specific)

For Claude-specific guidance only:

- `~/.claude/CLAUDE.md` — user-level, personal, all projects. Treat as a dotfile.
- `CLAUDE.md` at repo root — team-level, committed.
- `.local/CLAUDE.md` — local overrides, gitignored.

More specific scopes take precedence. The `@filepath` import syntax lets CLAUDE.md stay lean while linking to heavier docs on demand.

If AGENTS.md covers the need, don't duplicate it in CLAUDE.md. Recommend a symlink or a one-line `CLAUDE.md` that references AGENTS.md.

## Mode: audit

Produce a findings report without editing:

1. **Locate context files.** AGENTS.md, CLAUDE.md, `.cursor/rules/*.mdc`, `.github/copilot-instructions.md`.
2. **Measure.** Line count, word count, Flesch reading ease if possible. Flag anything over 150 lines as a candidate for trimming.
3. **Categorise content.** Map each section to the Tier 1/2/3 categories above.
4. **Flag gaps.** Missing build commands, missing do-not boundaries, missing security/performance guidance if the project has a clear need.
5. **Flag drift.** Compare against recent PRs (last 20-30 merged) for instructions that no longer match reality.
6. **Flag redundancy.** Anything duplicated in README, CONTRIBUTING, or linter configs.

Output format:

```markdown
# AGENTS.md audit

**Files reviewed:** AGENTS.md (187 lines), CLAUDE.md (42 lines)

## Summary

AGENTS.md is 37 lines over the recommended ceiling. ~40% of content
is Tier 3 (skippable). Security and performance sections are absent.

## Deletion candidates

- Lines 34-52: codebase overview. Doesn't help agent navigation (ETH
  Zurich research). Remove.
- Lines 78-91: duplicates README "Getting started" section. Remove.
- Lines 145-167: explains JavaScript import syntax. Model knows. Remove.
- Lines 180-187: "Be careful with concurrency". Vague. Replace with
  a specific rule or remove.

## Gaps to fill

- No security section. This project handles user auth — worth adding
  a few lines on session handling rules.
- No "do not modify" section. You mentioned migrations are manually
  managed — that belongs here.
- Build commands present but test commands missing.

## Drift detected

- Line 23 says "use Jest for testing". Recent PRs show Vitest is now
  used. Update.
- Line 67 references `src/legacy/` — deleted in PR #412. Remove.

## Recommended next action

Run `/kanso-context prune` to act on the deletion candidates, then
I'll walk you through filling the gaps.
```

## Mode: prune

Acts on a prior audit. Shows each proposed deletion with line references, waits for approval (bulk or per-item), then removes. Never silently edits.

After pruning, show the new line count. Target is under 150 lines for AGENTS.md, under 300 for CLAUDE.md.

## Mode: init

Interactive. Bootstraps a minimal AGENTS.md (target: ~80 lines).

1. **Detect automatically:** package manager, test runner, framework, build command, lint command. Ask the user to confirm or correct.
2. **Ask for architectural boundaries.** "What are the main directories and what do they own?"
3. **Ask for do-not rules.** "What should the agent never modify?"
4. **Ask about security/performance constraints.** "Any auth rules, data handling rules, or performance targets worth writing down?"
5. **Draft the file.** Show it to the user. Offer to commit.

The starting skeleton:

```markdown
# AGENTS.md

## Project overview

<One paragraph — what this is, primary tech, deployment context.>

## Build, test, run

- Install: `<exact command>`
- Dev: `<exact command>`
- Test: `<exact command>`
- Lint: `<exact command>`
- Type check: `<exact command>`

## Architecture

<Module-by-module. Keep it to one line each.>

## Conventions

<Naming, error handling, forbidden deps, deprecated patterns.
Bullet list. Specific.>

## Do not

<What the agent should never modify or do. Specific.>

## Development process

<Branching, commit format, PR requirements. Short.>

## References

<Links to deeper docs. Use @filepath imports in Claude Code.>

## Standing rules

<Only when skill libraries are installed. Point, don't copy:
"Before writing code, read and follow `.agents/skills/kanso-principles/SKILL.md`
(or `~/.agents/skills/...` for user-level installs)." Claude Code auto-loads
principles skills; other Agent Skills tools load skills on demand, so this
pointer is what puts the standing rules in front of them.>
```

## Mode: sync

Compare AGENTS.md against recent merged PRs:

1. `!git log main --merges -n 30 --format="%H %s"` to find recent merges.
2. For each merge, look at file changes and infer whether the pattern in AGENTS.md still matches reality.
3. Flag mismatches: "AGENTS.md says use Jest, but the last 12 PRs used Vitest."
4. Flag emerging patterns: "Three recent PRs introduced `src/domains/` subfolders. Is this a new convention worth documenting?"
5. Never auto-write new rules based on emerging patterns. Ask the user.

## The self-updating context loop

Context files decay. The cheapest way to keep one alive is to let the agent itself propose updates the moment a mistake recurs — but only on the user's command, never silently. Two halves: the in-file footer, and the workflow the user runs when an agent slips up.

### The footer (added on init / prune)

Append this to AGENTS.md:

```markdown
## Maintenance

When you (the agent) learn a durable project-specific fact during a
session — a gotcha, a convention, a "do not" — propose an update to
this file. Do not edit without the user's approval.
```

This invites the agent to participate in maintenance. The user still holds the pen.

### The user-side prompt (paste-ready)

When the agent makes a mistake that would be cheaper to prevent than to keep correcting, the user can fix it at the context layer in one move. Surface this prompt to the user in audit output and in the init / prune wrap-up — verbatim, so they can paste it:

```
Update AGENTS.md so you do not repeat this. Add the rule in the
correct section, keep it specific (not "be careful"), and show me
the diff before saving.
```

The result is a context file that learns from its own failures. The user gates every change; the agent does the drafting.

Same instruction works for `CLAUDE.md` when the mistake is genuinely Claude-specific (tool use, slash command behaviour, IDE quirks). Default target is AGENTS.md.

## Framing

- Read the file before suggesting edits. Vague recommendations are worse than none.
- Every deletion proposal includes the line number and the reason.
- Don't modernise. If the file uses a style that works, match it.
- Don't introduce cross-tool context (AGENTS.md) if the repo is clearly single-tool. A Claude-only shop doesn't need AGENTS.md.
- Respect the user's voice. Context files take on the personality of their author — don't generic-ify them.

## What this skill never does

- Auto-generate sections from scratch without the user's input. The research is definitive on this.
- Edit files silently. Every change needs approval.
- Suggest content that duplicates the README.
- Pad short files. A 40-line AGENTS.md is fine if it does the job.
- Copy rules from other repos. Borrowed rules introduce contradictions.
- Add sections just because a template has them.

## Failure modes to avoid

- Treating length as a proxy for quality. Shorter is almost always better.
- Recommending deletion of a rule that's obscure but load-bearing. Read carefully.
- Assuming the repo wants cross-tool AGENTS.md. Ask.
- Syncing against PRs that are themselves slop. Drift detection only works if recent history is clean.
- Generating the "security" section without actually understanding the project's threat model. Ask.
