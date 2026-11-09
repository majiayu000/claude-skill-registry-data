---
name: skill-vetting
description: "Vet an agent skill before installing it — read the SKILL.md and any scripts for the red-flag patterns (credential access, obfuscation, exfiltration, prompt injection), audit its blast radius, and produce a risk-tiered verdict. Use when asked is this skill safe to install, vet this SKILL.md, review this skill from a marketplace, or check what this skill can do to my machine."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# skill-vetting

## Работа в Codex

Прочитай [предметную процедуру](WORKFLOW.md), затем только нужные разделы ресурсов;
пути разрешай от содержащего их файла. Соблюдай AGENTS.md, цель, стек и полномочия
пользователя. Навык не разрешает создание агентов, hooks или фоновые действия.
Инструменты Claude — обозначения исходной платформы: используй реальные API Codex,
не подменяй CLI механически. Недоступные зависимости укажи; MCP подключай штатно.
До запуска скрипта проверь его код, зависимости, пути и побочные эффекты.
Примеры не подтверждают факты; актуальные API и тарифы проверяй по официальным
источникам. Уточняй существенное, обратимые действия в рамках задачи выполняй сам.

## Требования к результату

Produces the risk classification with quoted evidence, the permission-surface audit, the red-flag checklist results, and an install/sandbox/reject recommendation.
