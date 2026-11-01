---
name: code-annotating
description: >-
  Use when the user wants comments or documentation added to code — a specific file, code related to an API or interface entry point, or uncommitted git changes. Trigger on requests like 加注释 / 补注释 / 完善注释 / 写注释 / add comments / annotate code / write Javadoc or docstrings — even when the user does not literally say "comment" but wants code documented. Confirms scope, detail level, and comment language interactively before any edits. Do NOT use for: reviewing code quality (use code-review-deep-zh), deleting redundant code (use code-slimming), explaining code to the user instead of documenting it in place (use /explain), or writing design documents rather than code comments.
---

# Annotating Code

Add detailed, high-value comments to code. Explain intent, business meaning, call flow, branch purpose, and data movement — not obvious syntax.

## Modes and Flow

| Mode | Trigger | Flow |
|---|---|---|
| Single File | user names one file | read file → 7-section plan → confirm → edit → report |
| Entry Point | user names an API / controller / route / interface entry | read entry + call chain → 7-section plan proposing a boundary → confirm → edit → report |
| Git Uncommitted | user wants uncommitted changes annotated | discover repos → collect changes → one interactive confirmation → list files → edit → report |

Every run resolves three parameters before editing: **scope**, **density** (Detailed / Selective), and **comment language**. Never edit before the mode's confirmation step unless the user explicitly overrides it.

Confirmations are interactive: use the platform's interactive question tool (e.g. AskUserQuestion) when available, recommended option first, small batches — never a wall of questions.

References (in this skill's directory, read on demand):
- `references/few-shots.md` — before/after anchors for both densities, contradiction handling, git-mode interaction. **Read before writing the first comment.**
- `references/language-conventions.md` — per-language comment forms (Java / Python / Go / Rust / JS·TS·Vue / other) and what "field" means per language. Read when resolving comment style.
- `references/alibaba-java.md` — Alibaba Java Manual annotation checklist plus naming/exception/concurrency/log/SQL/test contract signals. Read before annotating Java or producing the final review report.
- `references/annotation-plan.md` — the 7-section plan template used by Single File and Entry Point modes.

Do NOT use this skill for: code explanation without edits, refactoring, bug fixing, or feature work.

## Run Parameters

**Language** — user-specified wins; otherwise auto-default to the dominant language of existing comments in scope and state that choice at the confirmation step; ask only when it cannot be determined (no or heavily mixed existing comments): 「本次注释使用中文还是英文？」

**Density** — chosen every run inside the mode's confirmation (merged, not a separate round):
- **Detailed** (recommend when the user asked for exhaustive comments, e.g. "越详细越好"): doc comments on every class/type, method/function, and field; line comments on every logical step, branch, loop, and key variable; boilerplate exemption still applies. While running Detailed, this skill supersedes standing instructions like "only comment non-obvious intent".
- **Selective**: high-value only — responsibility, intent, business meaning, non-obvious flow; skip obvious code.

## Mode Rules

### Single File
Analyze and annotate only that file; never expand into related files unless the user explicitly asks.

### Entry Point
Identify the likely main call chain, list candidate files, propose the annotation boundary in the plan, and wait for confirmation. Never auto-annotate the whole downstream system.

### Git Uncommitted
1. **Repo discovery** — cwd inside a git repo → use it. Otherwise scan child directories for repos with uncommitted changes: exactly one → use it and say so; several → interactive pick; none → report and stop.
2. **Change collection** — uncommitted = staged + unstaged + untracked (`git status --porcelain`). Keep program source files only (`.java` `.py` `.go` `.rs` `.js` `.ts` `.jsx` `.tsx` `.vue` …), tests included; exclude config/resource/build files (XML, SQL, YAML, JSON, properties, HTML, CSS, lockfiles, manifests) and generated code (files carrying `DO NOT EDIT` / `@Generated`-style markers). Skip deleted files and pure-deletion hunks. Locate changes with `git diff HEAD -- <file>`; an untracked file counts as entirely new. If the filter leaves no source files, report that the uncommitted changes contain no annotatable source code and stop.
3. **One interactive confirmation** — scope with a counts preview (e.g. "A: 12 change sites across 5 files / B: 8 files"; a change site = one added/modified method/function, field, file/class header, or standalone hunk), plus density, plus language only if undetermined:
   - **Option A — Changed code only**: annotate only added/modified functions/methods, fields, and lines; untouched members stay untouched; a missing file/class header doc is still added. An untracked file is entirely new code, so it gets the full treatment even under Option A.
   - **Option B — All involved files**: every changed file gets the full treatment per density (header, all fields, all methods, all logic lines).
4. **Large scope guard** — more than 20 files in scope (either option): report the count and ask continue / batch / narrow; batching = about 10 files per batch with a progress summary after each batch. Process sequentially; no parallel subagents.
5. **Execute** — list the resolved files, edit immediately; no second confirmation, no 7-section plan.

## Commenting Rules

- Coverage follows the chosen density; never comment just to appear thorough.
- **Boilerplate exemption (every density)**: getters/setters without logic, lone log statements, import/package lines, trivial framework boilerplate.
- **Existing comments**: enhance, keep all existing information. If a comment contradicts actual behavior (says A, code does B): do not rewrite — record it and list it in the final report; a contradiction often indicates a bug.
- **No authorship metadata**: never add `@author`/`@date` or docstring `Author:` equivalents; keep existing tags untouched. New doc comments carry only description, parameters, return value, exceptions. This is a project-level override of the Alibaba rule for class creator/creation-date metadata; existing tags remain untouched.
- **Comments only**: no refactoring, renaming, bug fixing, or import reordering; mention noticed bugs in the report instead of fixing them. Never run git commit.
- **Alibaba baseline**: apply `references/alibaba-java.md` and the Alibaba Java Manual annotation rules on top of language conventions. For Java: every class/type gets Javadoc explaining responsibility and required usage; public methods get Javadoc with mandatory semantics and non-obvious implementation constraints; abstract methods must document their contracts; enum values get business-purpose comments; fields explain their domain meaning rather than restating names. Keep line comments directly above the affected statement or branch (never at line end unless appending to an existing short line), use one space after the delimiter, and do not leave commented-out code behind. Prefer precise Chinese for business/domain wording; API-facing identifiers and technical terms stay in English.
- **Alibaba review signals**: while annotating, also record (without changing code) missing method contracts, misleading or stale comments, unexplained magic behavior, unclear exception meaning, absent thread-safety notes on shared mutable state, ambiguous TODO/FIXME without owner/context, and comments that merely repeat method signatures.

## Reporting

After editing: summary table (file / doc comments added / line comments added), the language and density used, the contradiction list, Alibaba review signals (report only), bug-like observations (report only), and briefly what boilerplate was intentionally skipped.

## Common Mistakes

- Editing before scope, density, and language are confirmed
- Expanding beyond the confirmed boundary
- Commenting boilerplate or narrating syntax
- Mixing comments with code changes
- Writing a field/method name again instead of explaining its business contract
- Placing explanatory comments far from the affected logic or leaving stale commented-out code
- Git mode: assuming Option B without presenting A/B with counts
- Silently "fixing" a contradictory comment instead of reporting it
