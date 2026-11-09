---
name: senior-qa
description: Generates unit tests, integration tests, and E2E tests for React/Next.js
  applications. Scans components to create Jest + React Testing Library test stubs,
  analyzes Istanbul/LCOV coverage reports to surface gaps, scaffolds Playwright test
  files from Next.js routes, mocks API calls with MSW, creates test fixtures, and
  configures test runners. Use when the user asks to "generate tests", "write unit
  tests", "analyze test coverage", "scaffold E2E tests", "set up Playwright", "configure
  Jest", "implement testing patterns", or "improve test quality".
metadata:
  source-package: claude-skills-main
  adapted-for: Codex
---

# senior-qa

## Работа в Codex

Прочитай [предметную процедуру](WORKFLOW.md), затем только нужные разделы ресурсов;
пути разрешай от содержащего их файла. Соблюдай AGENTS.md, цель, стек и полномочия
пользователя. Навык не разрешает создание агентов, hooks или фоновые действия.
Инструменты Claude — обозначения исходной платформы: используй реальные API Codex,
не подменяй CLI механически. Недоступные зависимости укажи; MCP подключай штатно.
До запуска скрипта проверь его код, зависимости, пути и побочные эффекты.
Примеры не подтверждают факты; актуальные API и тарифы проверяй по официальным
источникам. Уточняй существенное, обратимые действия в рамках задачи выполняй сам.

