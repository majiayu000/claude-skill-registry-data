---
name: commitizen-aware
description: This skill should be used when working in the `commitizen-tools/commitizen` repository as a contributor (not as a downstream `[tool.commitizen]` user). It surfaces the conventions from the repo's own AGENTS.md — uv + poe tasks, conventional commits enforced by commitizen itself, ruff/mypy linting, pytest, and PR guidelines — so any task (review, quick-fix, refactor) in commitizen follows them.
---

<!-- mkdocs-include-start -->

# Commitizen-Aware

**Loaded by**: `repo-detect` hook (SessionStart) when `commitizen-tools/commitizen` is detected in git remote or file structure.
**Applies to**: Any skill execution within a commitizen-tools/commitizen contributor checkout — review, quick-fix, refactoring, or otherwise.

## When to apply

This is a **knowledge layer**, not a review checklist.
It is loaded automatically by the
[`repo_detect` hook](https://github.com/Lee-W/maigo/blob/main/hooks/repo_detect.py)
at session start when a commitizen repo is detected.
It mirrors and supplements the repo's own `AGENTS.md`, condensed for agent context.

It can also be triggered manually via a memory entry with `triggers: [commitizen-aware]`
(see [Memory-triggered skill loading](https://github.com/Lee-W/maigo/blob/main/docs/reference/skills.md)).

Once loaded, treat every convention as background — do not re-read each task.

## Read AGENTS.md first

The single source of truth for contributor conventions lives in the repo itself.

1. **First action**: read [`AGENTS.md`](https://github.com/commitizen-tools/commitizen/blob/main/AGENTS.md)
   (83 lines — short enough to read in full).
2. **Conflict resolution**: if anything in this skill contradicts `AGENTS.md`, the repo file wins.
   This skill is an onramp and supplement, not a competing authority.
3. **PR-specific guidance**: when working on a pull request, also read
   [`docs/contributing/pull_request.md`](https://github.com/commitizen-tools/commitizen/blob/main/docs/contributing/pull_request.md)
   and `.github/pull_request_template.md` (both explicitly named in AGENTS.md line 25).

## Contributor conventions

### 1. Defer to AGENTS.md

This skill is an onramp — a condensed version of `AGENTS.md` formatted for agent startup context.
It is not a replacement. Any time a convention here conflicts with what `AGENTS.md` says,
follow `AGENTS.md`. See the [Read AGENTS.md first](#read-agentsmd-first) section above.

### 2. Environment — uv + prek + poe

Bootstrap the dev environment:

```bash
uv sync --frozen --group base --group test --group linters
uv run poe setup-pre-commit   # installs git hooks (uses prek, a pre-commit runner)
```

**Do not call `pre-commit` directly** — commitizen uses [`prek`](https://github.com/j178/prek)
as its pre-commit runner (AGENTS.md line 51). `prek` is compatible with the same hooks.

Available poe tasks (AGENTS.md lines 40–44):

- `uv run poe format` — runs `ruff check --fix` then `ruff format`
- `uv run poe lint` — runs `ruff check` then `mypy`
- `uv run poe test` — runs `pytest -n auto`
- `uv run poe ci` — commit check + pre-commit hooks via prek + test with coverage
- `uv run poe all` — format + lint + check-commit + coverage

**Before pushing**: always run at least `uv run ruff check --fix . && uv run ruff format .`.
CI will fail if the formatter modifies any files (AGENTS.md line 46).

### 3. Cross-platform

Tests run on Linux, macOS, and Windows (Python 3.10–3.14 matrix). Avoid POSIX-only
assumptions in any new code:

- **Paths**: use `pathlib` — never string-concatenate with `"foo/bar"`.
- **Subprocesses**: be careful with shell-quoting differences across platforms.
- **Line endings**: do not assume `\n` only.

This is one of the most distinctive aspects of commitizen compared to many Python projects —
treat cross-platform correctness as a first-class constraint, not an afterthought.

### 4. Common CI failure patterns

From AGENTS.md lines 54–59:

- **"Format Python code...Failed"**: run `uv run poe format` and commit the result.
- **mypy `[arg-type]` on TypedDict**: dynamically-constructed dicts (e.g., from
  `pytest.mark.parametrize`) passed to TypedDict-typed params need `# type: ignore[arg-type]`.
- **"pathspec 'vX.Y.Z' did not match"**: `.pre-commit-config.yaml` pins a tag of this repo.
  Rebase onto `master` to pick up the tag.
- **`VersionProtocol` + `issubclass`**: this Protocol has non-method members (properties),
  so `issubclass()` raises `TypeError`. Use `hasattr` checks for runtime validation.

### 5. Commits, PRs, conventions

- **Commit messages** must follow [Conventional Commits](https://www.conventionalcommits.org/)
  — enforced by commitizen itself (AGENTS.md line 24).
- **Pull requests** must follow `docs/contributing/pull_request.md` and
  `.github/pull_request_template.md` (AGENTS.md line 25).
- **Preserve public behavior**: no breaking changes to CLI flags, exit codes, or public APIs
  unless explicitly requested (AGENTS.md line 22).
- **Behavior changes require tests or doc updates** (AGENTS.md line 23).

### 6. Coding rules

From AGENTS.md lines 75–78:

- **Types**: preserve or improve existing type hints.
- **Errors**: prefer error types from `commitizen/exceptions.py`; keep messages clear for CLI users.
- **Output**: use `commitizen/out.py`; do not add noisy logging.

### 7. When unsure

- Read tests and documentation first to understand expected behavior (AGENTS.md line 82).
- When behavior is ambiguous, assume backward compatibility with current tests and docs
  is required (AGENTS.md line 83).

### 8. What to read before changing

From AGENTS.md lines 62–72:

| Changing... | Read first |
|---|---|
| CLI flags/arguments | `commitizen/cli.py`, `docs/commands/<cmd>.md`, `tests/test_cli/` |
| Bump logic | `commitizen/bump.py`, `commitizen/commands/bump.py`, `docs/commands/bump.md` |
| Changelog generation | `commitizen/changelog.py`, `commitizen/changelog_formats/`, `docs/commands/changelog.md` |
| Version schemes | `commitizen/version_schemes.py`, `tests/test_version_schemes.py` |
| Version providers | `commitizen/providers/`, `tests/test_providers.py`, `docs/config/version_provider.md` |
| Config resolution | `commitizen/config/`, `tests/test_conf.py`, `docs/config/` |
| Tag handling | `commitizen/tags.py`, `tests/test_tags.py` |
| Pre-commit / CI | `.pre-commit-config.yaml`, `.github/workflows/`, `pyproject.toml` (poe tasks) |

## Composing with other skills

This skill pairs with
[`strict-review`](https://github.com/Lee-W/maigo/blob/main/skills/strict-review/SKILL.md).

**Review scenario** — run `strict-review`'s 9-item base checklist as usual, then apply
commitizen-aware conventions as project-specific supplements:

- Convention 5 (commits / PRs) reinforces base item 8 (commit hygiene).
- Convention 6 (coding rules) reinforces base items 5–6 (style / correctness).
- Convention 4 (CI failure patterns) translates findings into evidence-based fix suggestions.

**Quick-fix / refactor scenario** — use conventions 2, 3, 5, and 6 as background knowledge.
Flag violations you notice, but do not run the full `strict-review` checklist unless the
task calls for it.
