---
name: hardware-prd
description: "Write a PRD for a physical hardware product — target cost (BOM and landed), industrial design constraints, regulatory certifications, reliability targets, serviceability, packaging, and forecast assumptions. Use when asked to write a hardware PRD, spec a new device, define requirements for a physical product, or kick off an NPI program."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# hardware-prd

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

Produces a complete hardware PRD with a cost stack, cert matrix, reliability spec, and EVT/DVT/PVT milestone targets.
