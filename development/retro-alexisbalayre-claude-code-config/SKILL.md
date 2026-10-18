---
name: retro
description: "Conduct a retrospective on a coding session."
disable-model-invocation: true
---

The user has asked for a **retrospective**. You are suggesting improvements to the coding agent's **environment** to improve future runs. (The CI review pipeline has its own retrospective over its run records: `/review-retro`.)

## Steps

1. Call the Skill tool with `writing-for-agents` for the writing style guide.

2. Read the primary sources for the session the user specifies. Claude Code keeps each session's transcript at `~/.claude/projects/<project path with every character but letters and digits replaced by "-">/<session id>.jsonl`. If the user doesn't specify a session, default to the current one.

3. Look for candidates for improvement in these categories.

- **Navigation**: how easy was it for the agent to find the right files? Are there hidden dependencies between files? Would a **navigation pointer** make it easier? _Use when_ the session took a long time to find a piece of information.
- **Automated checks**: are there automated checks that could catch errors the agent made? Linting, typing, tests, filesystem linters? Read the repo's own checks first (`LINT_CMD`, `TYPECHECK_CMD` and `TEST_CMD` in `.claude/project.env`, which `scripts/pre-commit` runs, and the `Stop` hook too, tests aside, and the workflows under `.github/workflows/`), so a check that already exists but sits unwired or silently broken is the finding, not a reinvention. A repo with no **guardrail** (those keys empty, and no CI job running lint/typecheck/test) is itself a finding: an un-linted repo is a standing missed opportunity, not a neutral default. _Use when_ the agent made a mistake an automated check could have caught, or the repo has no guardrail at all.
- **Coding standards**: should the **reviewer agents** (`review-conventions` under `/pr-ci-review`, `convention-checker` before a commit) be given a new rule to enforce? Should an existing rule be removed or clarified? Classify the violation first: a **mechanical** one (a fixed syntactic pattern, a banned API, an import shape, a file-location rule) gets a deterministic check, full stop: a rule in the repo's own linter, a row in `.claude/spot-checks.tsv`, a hook under `.claude/hooks/`, a `scripts/pre-commit` step, or a CI job, whichever the repo's language and existing guardrail make cheapest. Default to building the check over writing the rule. Reserve `docs/conventions/<area>.md` for genuine **judgement calls** (cross-file consistency, "matches the surrounding style," anything no guardrail could ever substitute for). _Use when_ a reviewer agent failed to catch a mistake.
- **Global AGENTS.md**: are there any steering instructions in `AGENTS.md` or `CLAUDE.md` that should be moved to `docs/conventions/` (or automated checks) instead? _Use when_ those files are particularly large - in the repo OR the user's global scope (`~/.claude/CLAUDE.md`).
- **Tool economy**: did the agent make expensive tool calls that could be streamlined? Is there any custom tooling (CLI's, MCP's) that is particularly token-inefficient? _Use when_ the agent made an expensive tool call.
- **No-ops**: look for instructions in steering files that don't modify the agent's behavior. _Use when_ the steering files are large and unwieldy.
- **Information access**: look for opportunities to increase the agent's access to information. Teeing dev server logs, readonly access to third-party services. _Use when_ a crucial piece of information was not available to the agent.

4. Present these candidates to the user, in order of severity.

## Reference

### Implementation vs Review

Remember that all work goes through two stages: implementation and review. The implementation agent has the most **context pressure**. They are responsible for exploration, writing code, and debugging failures.

The review agent has the least context pressure - it receives a diff, so no exploration needed. It often does not need to write code or debug.

This means that the review agents should be responsible for imposing coding standards, not the implementation agent.

### Files

You have access to several files in the repo:

- `CLAUDE.md`/`AGENTS.md`: these files are pushed to the context window of any agent working in this repo. They should be used incredibly sparingly, usually only for **navigation pointers** to other files.
- `docs/conventions/<area>.md`: the coding standards. `.claude/rules/` loads one only when an agent touches its area, and the reviewer agents enforce them on the diff. Point a doc at other `docs/` pages rather than growing it past 1,000 lines.
- Docs: `docs/` (indexed by `docs/README.md`) holds reference files, pointed to by other files. Look for existing docs before writing new ones.
- Skills: use skills for docs (since their description goes into the agent's context window), or for user-invoked commands. Follow the advice in the `writing-for-agents` skill.
