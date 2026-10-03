---
name: repo-launch
description: Audit and polish a GitHub-ready repository. Use when Codex needs to classify a rough project, choose the right README shape, and add only the minimum launch essentials needed for a clean shareable repo.
---

# Repo Launch

Use this skill when a project needs to go from loose files or a rough prototype to a clean, public-facing repository.

## Quick Start

1. Run `python3 scripts/repo_launch_audit.py --repo-dir .` before editing so the repo shape, app-to-skill overlap, runner command coverage, and launch gaps are explicit.
2. Choose a repository mode first: app repo, skill catalog, library, template, or multi-project collection.
3. Create only the minimum repo essentials the project actually needs.
4. Prefer a short, scannable `README.md` with one clear install or usage path.
5. Add a `LICENSE` when the user wants the repo to be shareable.
6. Keep names, commands, and folder structure simple enough for first-time visitors.

## Workflow

### Repo Audit

- Use the audit helper to classify the repo before changing files.
- Read the overlap map before editing so exact app pairs, near-equivalent skill names, and shared runner command families are obvious.
- If the repo is a skill catalog or multi-project collection, keep the top-level README compact and avoid repeating shared setup across subprojects.
- If the repo is a single app, make the install or run path obvious on the first screen.

### Repository Basics

- Start with the smallest useful set of files: `README.md`, `.gitignore`, `LICENSE`, and project-specific entrypoints.
- Match the repository structure to the project type instead of forcing a template.
- If there is already a strong project layout, improve it rather than replacing it.
- If the repo has more than one top-level product, create a compact index and avoid repeating setup instructions in multiple places.

### Launch Readiness

- Make the repo understandable from the first screen on GitHub.
- Prefer one copy-paste install or run command over long setup prose.
- Surface the main value of the project in one sentence near the top.
- If the repo contains multiple packages or apps, add a compact index instead of long documentation.
- Always leave the user with a visible "start here" path: one command, one folder, or one primary entrypoint.

### Required Deliverables

- A classified repo mode, gap list, and overlap map from `python3 scripts/repo_launch_audit.py --repo-dir .`.
- A top-level `README.md` that answers:
  - what this is
  - how to run or install it
  - where the main folders are
- A matching `.gitignore` for the project stack.
- A license file when the repo is intended to be shared.
- A small amount of launch polish if needed: badges, examples, or a table index.

### Decision Rules

- If the project is a single app, optimize the README for first-run success.
- If the project is a catalog, optimize the README for browsing and installation by name.
- If the project is a starter or template, make setup steps explicit and short.
- If there is no stable install flow yet, say so clearly instead of faking one.

### Editing Guidance

- Keep generated copy plain and concrete, not hypey.
- Use action-oriented names for scripts, folders, and commands.
- Avoid adding extra docs unless they remove real confusion for contributors or users.
- Do not bury the main install command below long narrative text.
- Avoid skeleton files that look official but add no actual value.

## Resources

- `scripts/repo_launch_audit.py`: deterministic repo-shape audit helper with app/skill overlap and runner command inventory for rough projects, skill catalogs, and multi-project collections.
- `agents/openai.yaml`: UI metadata and default invocation prompt.
- `assets/`: branded icons for repo listings and skill chips.
- `references/repo-patterns.md`: lightweight patterns for app repos, catalog repos, multi-project collections, templates, and libraries.
