---
name: aeo
description: Answer Engine Optimization (AEO) skill — optimize content to be cited
  by AI language models (ChatGPT, Perplexity, Claude, Gemini, Mistral) as authoritative
  sources. Distinct from SEO — AEO optimizes for citation in LLM-generated responses,
  not search rankings. Use when planning content for AI-first search audiences, auditing
  existing content for E-E-A-T signals, tracking which pages get cited by which LLMs,
  or building a citation-friendly content strategy. Triggers — 'AEO audit', 'optimize
  for ChatGPT', 'get cited by Perplexity', 'LLM citation strategy', 'answer engine
  optimization', 'content for AI search', 'E-E-A-T audit'. Output is a markdown audit
  report (default) or JSON for pipeline integration. Stdlib-only Python tools.
metadata:
  source-package: claude-skills-main
  adapted-for: Codex
---

# aeo

## Работа в Codex

Прочитай [предметную процедуру](WORKFLOW.md), затем только нужные разделы ресурсов;
пути разрешай от содержащего их файла. Соблюдай AGENTS.md, цель, стек и полномочия
пользователя. Навык не разрешает создание агентов, hooks или фоновые действия.
Инструменты Claude — обозначения исходной платформы: используй реальные API Codex,
не подменяй CLI механически. Недоступные зависимости укажи; MCP подключай штатно.
До запуска скрипта проверь его код, зависимости, пути и побочные эффекты.
Примеры не подтверждают факты; актуальные API и тарифы проверяй по официальным
источникам. Уточняй существенное, обратимые действия в рамках задачи выполняй сам.

