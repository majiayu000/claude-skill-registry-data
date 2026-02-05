---
name: code-sentinel
description: Use when tests/test_code_patterns.py fails - fixes recurring anti-patterns with documented root causes and verification
---

# Code Sentinel

Fix recurring anti-patterns detected by `tests/test_code_patterns.py`.

**You MUST use this skill when test_code_patterns.py fails.** Even if the fix looks obvious. The anti-pattern files document WHY patterns fail, not just HOW to fix them.

## Workflow

1. Run `pytest tests/test_code_patterns.py -v`
2. For each failing test, read the anti-pattern file (see index below)
3. Understand the root cause (not just the fix)
4. Apply the documented fix
5. Verify tests pass

## Anti-Pattern Index

### CI/Workflow Anti-Patterns

Issues that occur in GitHub Actions workflows and CI pipelines.

| Anti-Pattern | File | Automated Test |
|--------------|------|----------------|
| Heredocs fail inside YAML `run:` blocks | `ci-workflow/yaml-heredoc-indentation.md` | `test_no_heredocs_in_github_actions` |
| `grep -c \|\| echo "0"` creates duplicate output | `ci-workflow/grep-exit-code-echo-fallback.md` | `test_no_grep_exit_code_echo_pattern` |
| Git pull/rebase fails with dirty working tree | `ci-workflow/git-pull-without-autostash.md` | `test_git_operations_with_staging` |
| `gh workflow run` silently fails without permission | `ci-workflow/gh-workflow-run-permissions.md` | `test_workflow_dispatch_has_actions_permission` |
| Windows venv path used on Linux runner | `ci-workflow/windows-venv-path-on-linux.md` | `test_venv_activation_uses_linux_path` |

### Build/Packaging Anti-Patterns

Issues with PyInstaller bundling, version generation, and cross-platform builds.

| Anti-Pattern | File | Automated Test |
|--------------|------|----------------|
| Missing hidden imports after refactoring | `build-packaging/pyinstaller-missing-hidden-imports.md` | `test_pyinstaller_hidden_imports` |
| Import path case mismatch breaks bundling | `build-packaging/import-path-case-mismatch.md` | (manual) |
| Bare imports for sibling modules fail in bundle | `build-packaging/sibling-absolute-import-bundling.md` | `test_sibling_imports_use_relative_syntax` |
| Gitignored file committed before rule | `build-packaging/gitignored-file-still-tracked.md` | (manual) |
| Version hash embedded before commit | `build-packaging/version-hash-before-commit.md` | (design issue) |
| Windows backslash paths in .spec file | `build-packaging/windows-backslash-in-spec.md` | `test_spec_uses_forward_slashes` |

### Application/Runtime Anti-Patterns

Issues in application code that cause runtime failures or unexpected behavior.

| Anti-Pattern | File | Automated Test |
|--------------|------|----------------|
| Sort without secondary tiebreaker key | `application-runtime/sort-without-tiebreaker.md` | `test_deterministic_file_sorting` |
| Fixed window geometry cuts off content | `application-runtime/fixed-window-geometry.md` | `test_no_fixed_window_geometry` |
| Same constant defined in multiple modules | `application-runtime/duplicate-module-level-constants.md` | (manual) |
| Optional import fails silently | `application-runtime/silent-optional-import-failure.md` | (manual) |
| PIL ImageGrab black on secondary monitor | `application-runtime/pil-imagegrab-multimonitor.md` | (hardware-dependent) |
| PIL-saved ICO renders invisible | `application-runtime/pil-ico-save-invisible.md` | (Windows-dependent) |

## Quick Reference: Test-to-File Mapping

```
test_no_heredocs_in_github_actions       → ci-workflow/yaml-heredoc-indentation.md
test_no_grep_exit_code_echo_pattern      → ci-workflow/grep-exit-code-echo-fallback.md
test_git_operations_with_staging         → ci-workflow/git-pull-without-autostash.md
test_workflow_dispatch_has_actions_permission → ci-workflow/gh-workflow-run-permissions.md
test_venv_activation_uses_linux_path     → ci-workflow/windows-venv-path-on-linux.md
test_pyinstaller_hidden_imports          → build-packaging/pyinstaller-missing-hidden-imports.md
test_sibling_imports_use_relative_syntax → build-packaging/sibling-absolute-import-bundling.md
test_spec_uses_forward_slashes           → build-packaging/windows-backslash-in-spec.md
test_deterministic_file_sorting          → application-runtime/sort-without-tiebreaker.md
test_no_fixed_window_geometry            → application-runtime/fixed-window-geometry.md
```

## Common Mistakes

| Mistake | Why It's Wrong |
|---------|---------------|
| "Fix is obvious, skip the skill" | You miss the root cause. Next time you'll make the same mistake. |
| Fixing without reading anti-pattern doc | The doc explains WHY, not just WHAT. Understanding prevents recurrence. |
| Not verifying tests pass | The pattern might exist elsewhere in codebase. |

## Adding New Anti-Patterns

When you discover a new recurring issue:

1. **Identify the category**: CI/Workflow, Build/Packaging, or Application/Runtime
2. **Create the file** in the appropriate subfolder with a descriptive name
3. **Follow the template**:
   - Category
   - Issue (one-line summary)
   - Pattern to Avoid (code example)
   - Correct Approach (code example)
   - Why It Fails (root cause explanation)
   - Detection (how to find instances)
   - Test Reference (if automated test exists)
   - Related Commits (historical context)
4. **Update this index** with the new anti-pattern
5. **Add automated test** in `tests/test_code_patterns.py` if feasible

Anti-pattern files: `.claude/skills/code-sentinel/anti-patterns/`
