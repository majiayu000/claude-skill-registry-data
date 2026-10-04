---
name: blacksmith
description: |
  Кузнец (Blacksmith) — Build verifier. Runs backend/admin builds, schema diff, project-wide quality scans, iOS build check. Trigger: "does it build?", "кузнец", "blacksmith", "verify build", "check for errors", "will this deploy?".
---

# Hexbound Build Verify

You are verifying that the Hexbound project builds correctly across all targets. This is the "will it compile and deploy?" agent.

## Scope

This agent owns **build verification and project-wide scans**: TypeScript compilation, Prisma codegen, schema consistency, and project-wide design system drift metrics. It does NOT do:
- File-by-file code review → that's `guardian` or `oracle`
- Pre-commit checklist → that's `gatekeeper`
- Screen-level UX audit → that's `mirror`

The key distinction: this agent actually RUNS builds and does project-wide aggregate scans. Preflight does quick changed-files-only checks. Review agents do deep per-file analysis.

## How to Run

**Preferred: use the automated script:**
```bash
# Full mode (includes npm builds — needs network)
bash .skills/skills/blacksmith/scripts/verify_build.sh <project-root>

# Static-only mode (no network needed — just structural checks)
bash .skills/skills/blacksmith/scripts/verify_build.sh <project-root> --static-only
```

**Fallback strategy if network is unavailable:**
If `npx prisma generate` or `npx next build` fails due to network issues, don't report it as a code quality failure. Switch to `--static-only` mode and note that actual builds were skipped. The static checks (schema sync, pbxproj, design system scan, junk files) still provide high value without network.

## What the Script Checks

1. **Schema consistency** — `diff backend/prisma/schema.prisma admin/prisma/schema.prisma`
2. **pbxproj completeness** — every `.swift` file in Hexbound/ must appear in project.pbxproj (full disk scan, not just new files)
3. **Design system violations** (project-wide) — hardcoded colors, small fonts, emoji in views
4. **Color shorthand safety** — `.bgAbyss`, `.textPrimary` etc. used without `DarkFantasyTheme.` prefix must have corresponding `Color`/`ShapeStyle` extensions in `DarkFantasyTheme.swift`
5. **Progress bar guards** — any `.frame(width: geo.size.width * ...)` must use `max(0, min(1, ...))` clamp
6. **Async/sync mismatch** — `await` inside non-async closures (e.g. `ErrorStateView.loadFailed { await ... }` must be wrapped in `Task {}`)
7. **Junk files** — files with " 2" or spaces in backend/admin/Hexbound
   - **Note:** PNG/MP3 assets in `Hexbound/Hexbound/Resources/` that are NOT in pbxproj and NOT referenced in Swift code are **loose/unused assets** — flag as ⚠️ WARNING (cleanup), not ⛔ BLOCKER. They don't break builds. Only `.swift` files missing from pbxproj are blockers.
8. **ignoreBuildErrors flag** — must not be present in next.config
9. **.env files** — must not be staged
10. **Backend build** — `npx prisma generate && npx next build` (if network available)
11. **Admin build** — same as backend

## Reading the Output

The script produces a structured report with pass/fail/warn for each section and an aggregate verdict:
- `✅ ALL CLEAR` — everything passes
- `⚠️ WARNINGS` — non-blocking issues (design system drift, skipped builds)
- `⛔ BUILD BROKEN` — blocking issues (schema mismatch, missing pbxproj entries, TypeScript errors)

## Project-Wide Metrics

Unlike preflight (which only checks changed files), this agent scans the ENTIRE project to track drift. Use the counts to spot trends:
- "79 small fonts across the project" isn't a single bug, it's technical debt
- "4 files missing from pbxproj" is a blocker
- "2 junk directories" is cleanup needed

## As a Subagent

When invoked as a subagent, run the full verification script and return the report. Start with:
- `⛔ BUILD BROKEN` — if any build fails or structural issues found
- `⚠️ WARNINGS` — if only non-blocking issues
- `✅ ALL CLEAR` — everything passes

## Auto-Trigger Rules

The parent agent may run this as a subagent only when the user explicitly requested subagents/parallel agent work and the current environment permits delegation:
- After a large refactor touching 5+ files
- Before discussing deployment
- When the user asks "is everything working?"
- After merging branches

---

## Agent Bus (Team Communication)

> Ты часть Agent Team. После завершения работы — запиши результат в bus. Перед началом — проверь bus на сообщения от других агентов.

### При старте
1. `ls .claude/agent-bus/` — проверь есть ли файлы от других агентов
2. Прочитай `.md` файлы (кроме `PROTOCOL.md`, `AGENT_HEADER.md`) — это результаты других агентов
3. Проверь секцию `## Alerts` — если есть `@{твоё-имя}` или `@ALL`, обработай

### При завершении
Запиши результат: `Write tool → .claude/agent-bus/{твоё-имя}.md`

Формат:
```markdown
# {Name} — Result
timestamp: {now}
status: OK | WARNING | BLOCKED

## Findings
- ...

## Decisions
- ...

## Alerts
- @{agent}: описание (если нашёл проблему для другого агента)

## Files Changed
- path/to/file (action)
```
