---
name: reviewer-base
description: Code reviewer shared rules — context, SonarQube, commit style.
---

## Foundational Rule

1. Load `skills/shared/project-context/SKILL.md` — covers README, CLAUDE.md, AGENTS.md, project.md, session-summary, code-standards, architecture, and recent git log.

2. Additionally for review sessions:
   - Read linter configs (`.eslintrc*`, `pyproject.toml`, `.rubocop.yml`, `phpcs.xml`, `golangci.yml`) — source of truth for style
   - Run `git diff main...HEAD --stat` first to see the size and shape of the change. Under ~15 files / ~800 lines, follow with a single `git diff main...HEAD` for full content. Above that, do not pull the whole diff into context in one call — review file-by-file with targeted `git diff main...HEAD -- <path>` calls (or batches of a few related files), so one oversized diff never inflates a single turn enough to risk a context/prompt-size failure. Either way, focus all findings on what changed, not pre-existing code
   - Load `skills/shared/comments-policy/SKILL.md`
   - Load `skills/shared/conventional-commits/SKILL.md`
   - Load `skills/shared/scoped-test-execution/SKILL.md` **before running any test command** — a review that verifies behaviour runs the tests covering the diff, never the project's full suite. Reviewing is not one of the signals that authorize a full run
   - Detect SonarQube using the `## Detection Signals` table in `skills/devops/sonarqube/SKILL.md` — if **any** signal in that table matches, load the skill. That table is the single source of truth; do not maintain or infer a signal list here, and do not treat the config files as the only trigger (a CI scanner step or a `sonarqube` service in `docker-compose.yml` counts too).

Apply `skills/shared/token-efficiency/SKILL.md` — prefer `grep`/`head` over full-file reads; use `git diff` output directly rather than re-reading changed files.

After loading this skill, apply `skills/shared/reviewer-mindset/SKILL.md` for the review mindset questions.
