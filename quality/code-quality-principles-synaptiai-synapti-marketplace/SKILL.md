---
name: code-quality-principles
description: "Enforce code quality through the Boy Scout Rule (leave code better than found), secret-free commits, production-ready code (no TODOs, console.log, mocks, or commented code), and self-review against an atomic-commits checklist. Use when writing, modifying, or reviewing code. This skill MUST be consulted because production code without these standards causes quality regressions and operational incidents."
allowed-tools: Bash, Read, Grep, Glob
---

# Code Quality Principles

## Iron Law

**EVERY CHANGE MUST BE INTENTIONAL. If you can't explain why a line changed, revert it.**

## Before You Write Code

Answer first, or return to EXPLORE: which task/criterion this code serves; which files change and why each; which existing project patterns apply; what could go wrong (error cases, edge cases, security); how you will verify it.

## Boy Scout Rule

Leave every file you touch better than you found it. Touching a file means owning its known issues.

**The proximity test is NOT a deferral mechanism for P1/P2 findings.** It decides *how* a cleanup is committed (alongside the feature fix vs. a separate `improve:` commit), not *whether* it gets fixed. A P1 or P2 in a file the PR modifies is fixed in this PR.

**A cleanup is a standalone `improve:` commit when ALL true:**
1. The file is already being modified for the current task
2. The fix is self-evidently correct (lint, format, typo, obvious bug, missing error handling)
3. The fix is small (under ~10 lines)
4. It does not change public API signatures or behavior semantics
5. It needs no explanation beyond "Boy Scout cleanup"

**A finding requires expanded scope (still fixed; may need a design note or tests) when ANY true:**
1. Requires modifying files NOT already touched by the task
2. Changes architecture, module boundaries, or public APIs
3. Requires new tests to validate
4. Would benefit from its own issue to explain motivation
5. Is a subjective style preference (P3 at most, not a fix-blocker)

P1/P2 in the expanded-scope bucket: fix in-PR with an appropriate commit message. Finding triage is NEVER a valid escalation trigger — do NOT file a six-field escalation to ask whether to fix a finding (see `skills/llm-operator-principles/SKILL.md` and `references/escalation-format.md`). "Disagree to fix" and "ask the user whether to fix" are not options.

**Default mode:** cosmetic P3 in truly untouched files is fixed if bounded (<10 lines) or documented inline in the PR body. Do NOT create follow-up issues for them.

**Minimal-scope mode (`settings.json` → `minimalScope: true`):** the follow-up issue workflow for cosmetic P3 in untouched files is restored.

## No Secrets in Code

Never commit secrets, credentials, or sensitive values. Use environment variables and gitignored `.env` files; reference secrets by name. A hardcoded secret is P1 immediately.

## Production Code Standards

No `TODO` comments in committed code (track in issues); no `console.log` / `puts` / `print` debugging; no mocked or stubbed "implement later" code; no commented-out code blocks; no placeholder error messages.

## Quality Command Execution

Run independent quality commands (lint, test, typecheck) as parallel Bash calls, never chained with `&&`. After checks: P1 fix immediately, P2 before PR, P3 in-PR by default.

## Anti-Patterns

Do NOT: modify imports/formatting in files you aren't changing for the task; commit generated files without verifying them; copy-paste instead of extracting a shared function; catch exceptions silently (`catch {}` / `rescue nil`).

## First-Touch Awareness

A file with 0 prior commits on the branch and large additions is "first touch": flag it in change classification, give it extra review attention, and ensure it follows project conventions.

## Atomic Commits

Commit only when you can describe the change without "WIP" or "partial", it leaves the codebase working, and reverting it cleanly undoes one logical change.

## Self-Review Checklist

Before marking any task complete: `git diff` shows only intended changes; no debug code or temporary files; new code follows existing project patterns; edge cases considered (null, empty, boundary); error messages helpful and specific. Tests passing is necessary, not sufficient.
