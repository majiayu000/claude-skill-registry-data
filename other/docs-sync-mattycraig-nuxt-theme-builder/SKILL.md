---
name: docs-sync
description: Audit the project's documentation (CLAUDE.md, .claude/rules, skills, README, CONTRIBUTING, SECURITY, .env.example, app/data/*.md, learn articles) against the actual code and config, and fix drift. Use after refactors, dependency or workflow changes, or on a schedule.
argument-hint: "[--report-only]"
context: fork
agent: general-purpose
---

# Docs ↔ code drift audit

Verify every factual claim against the source. Anything unverifiable or wrong gets fixed, or listed if `--report-only` was passed ($ARGUMENTS).

## Checks

1. **Commands**: every `pnpm <script>` mentioned in README.md, CONTRIBUTING.md, CLAUDE.md, `.claude/**`, and `.github/**` exists in `package.json` `scripts`.
2. **Files and paths**: every path mentioned in docs exists (`ls`/`Glob`). Pay special attention to the architecture trees in README.md and CLAUDE.md.
3. **CI/workflows**: descriptions of `.github/workflows/*.yml` (triggers, jobs, what runs) match the YAML.
4. **Env vars**: `.env.example` lists exactly the variables read by `nuxt.config.ts`, `server/`, `playwright.config.ts`, and workflows, each with an accurate description.
5. **Product facts**: palette, font, shade, and radius lists in `app/data/*.md`, `content/learn/**`, and `server/utils/aiSystemPrompt.ts` match `shared/constants/theme.ts`. AI model lists in docs match `app/types/ai.ts`.
6. **Dependencies**: libraries named in docs (e.g. SECURITY.md's "DOMPurify", "Renovate") are actually installed or configured and used.
7. **Claude setup**: skills and agents named in CLAUDE.md and `.claude/README.md` exist; `.claude/rules/*` `paths:` globs match real files; hooks referenced in `.claude/settings.json` exist.
8. **Config hygiene**: `.prettierignore`, `.gitignore`, `knip.json`, `eslint.config.mjs`, `.github/labeler.yml`, and `.github/CODEOWNERS` don't reference paths that no longer exist.

## Output

A table of `file:line | claim | reality | action`. Fix what you can (docs only; if the _code_ is wrong, report it rather than change behavior), run `pnpm format`, and summarize the fixes and open questions.
