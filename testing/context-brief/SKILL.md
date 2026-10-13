---
name: context-brief
description: >
  Maintain a `.claude/CONTEXT.md` project brief that lets a fresh Claude Code session
  pick up prior context — decisions, in-flight work, gotchas, entry points — without
  re-reading every CLAUDE.md and README from scratch.

  Trigger this skill when:
  - The user says "generate context brief", "update context", "backup context",
    "context handoff", "refresh CONTEXT.md", or invokes `/context-brief` /
    `/context-brief update` / `/context-brief read`.
  - On session start in a repo that has `.claude/CONTEXT.md`, silently ingest it
    (read only, don't regenerate unless asked).
  - When the user says "I'm switching machines" or "I need to hand this off" —
    proactively offer to refresh the brief before they leave.

  The skill writes exactly one file: `.claude/CONTEXT.md` at the repo root (or the
  current working directory if there is no `.git` here). It is designed to be
  committed to git. It never contains secrets.
---

## What this skill does

Produce and maintain a distilled, densely-informative Markdown brief at
`.claude/CONTEXT.md` inside the current repo (or the workspace root if the
user's `cwd` spans multiple repos).

The brief is intentionally:

- **Committable** — no secrets, no local paths that mention a specific user's
  home directory, no dev-machine-specific state. Uses repo-relative paths and
  `~/…` style refs only where necessary.
- **Short enough to load into context** — target 200–500 lines, hard cap 800.
- **Distilled** — collapses many CLAUDE.md/README/PLAN files into the operational
  bullets that matter for the next agent, keeping load-bearing warnings verbatim.
- **Auditable** — dates and repo SHAs are stamped in a footer so future readers
  can spot staleness.

## When invoked

### Mode 1 — `/context-brief update` (or "regenerate", "refresh")

1. Discover the target root: current `.git` toplevel if there is one, else `pwd`.
2. Ensure `.claude/` dir exists at that root.
3. Sweep the tree (skipping `node_modules`, `.venv`, `venv`, `dist`, `build`,
   `.next`, `.turbo`, `__pycache__`, `.pytest_cache`, `target`, `.terraform`,
   `coverage`, `playwright-report`, `test-results`, `.cache`).
4. Read (in this priority order):
   1. `CLAUDE.md` / `CLAUDE.MD` at repo root and any subprojects.
   2. `README.md` at repo root and subprojects.
   3. Files matching `*_PLAN.md`, `PROGRESS.md`, `ROADMAP.md`, `*_STATE.md`,
      `KIND1_*.md`, `E2E_*.md`, or any Markdown filed under a directory named
      `plans/`, `docs/`, `nocommit/` (report existence only for `nocommit/`,
      never dump contents).
   4. `.gitignore` — to understand what is deliberately excluded.
   5. `pyproject.toml`, `package.json`, `docker-compose.yml`, `Dockerfile`,
      `.tool-versions` — for stack/version info.
   6. `.github/workflows/*.yml` — for CI/CD shape (only names + triggers, not
      contents).
5. Read git state: `git log --oneline -20`, `git status -s`, `git branch --show-current`.
6. Write `.claude/CONTEXT.md` following the template at
   `templates/CONTEXT_TEMPLATE.md` in this skill dir.
7. Stamp the footer with an ISO date + repo SHA + skill version.
8. If there are already staged changes in the repo, do **not** stage the new
   `CONTEXT.md` automatically — mention it and ask.

### Mode 2 — `/context-brief read` (or "show me the brief", "what's the context")

1. Look for `.claude/CONTEXT.md` at repo root.
2. If present: read it and summarize the top 5 items the user should know
   before touching the code. Highlight anything stamped as in-flight.
3. If missing: offer to run `/context-brief update` to generate one.

### Mode 3 — Session start (auto)

If a `.claude/CONTEXT.md` exists, silently read it as part of your session
priming. Do not regenerate on session start; that only happens on explicit
user request or when the user says "handoff" / "switching machines".

## Content rules

- **Never** paste tokens, DB credentials, API keys, or contents of anything
  under `nocommit/` or `.env*`. Reference paths only.
- **Never** copy full file contents. Extract the operational: what a fresh
  Claude needs to run/build/deploy/test + the "don't do X" rules.
- **Preserve verbatim** any warnings in CLAUDE.md that are marked as
  "load-bearing", "will bite you", "never", or similar. Do not paraphrase
  safety-critical language.
- **Prefer** tables + bullets over prose.
- **Do not** invent state. If you can't tell whether something is done, say so.
- **Report** dirty repos + open branches near the top so a fresh reader knows
  work is in-flight.

## Repository-side integration

Each repo that uses this skill should include a one-liner in its `CLAUDE.md`:

```markdown
## Prior context (`.claude/CONTEXT.md`)

If `.claude/CONTEXT.md` exists in this repo, read it before touching any code.
It's a distilled brief of decisions, in-flight work, and gotchas maintained by
the `context-brief` skill (`nimbus-skills` repo). If it looks stale (>2 weeks),
say so — the user can run `/context-brief update` to refresh.
```

Copy this snippet into each repo's `CLAUDE.md` under the top-level guidance.

## Template

See `templates/CONTEXT_TEMPLATE.md` for the exact structure the generated
`.claude/CONTEXT.md` follows.

## Output validation

Before ending, self-check:
1. Every repo/subproject present in the "Repo inventory" section has a matching
   subsection later.
2. Every `CLAUDE.md` found was represented (grep excerpts back if unsure).
3. No secrets pasted.
4. File paths use repo-relative or `~/…` — no origin-machine home paths.
5. Total file size ≤ 200 KB (else compress further).
6. Footer stamped with ISO date + repo SHA.
