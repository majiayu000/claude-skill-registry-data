---
name: lower-my-bill
description: "Negotiate a recurring bill down — internet, phone, insurance, cable, gym — with a ready-to-read script, the competitor leverage that actually moves the price, and exactly what to say when they say no. Use when asked to lower my bill, negotiate my internet/phone bill, my provider raised my price, or how do I get a discount on [service]."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# lower-my-bill

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

Produces a call-or-chat script in your words, the specific leverage for your situation, a fallback ladder (discount → downgrade → cancel lever), and a note of what to write down so the promised deal actually sticks.
