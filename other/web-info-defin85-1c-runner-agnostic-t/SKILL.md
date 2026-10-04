---
name: web-info
description: "Статус Apache и веб-публикаций 1С — запущен ли сервер, какие базы опубл…"
metadata:
  short-description: "Статус Apache и веб-публикаций 1С — запущен ли сервер, какие базы опубл…"
---

<!-- GENERATED: sync-imported-skills -->

# Agent Skill: web-info

Repo script: `./scripts/skills/run-imported-skill.sh web-info`
Windows launcher: `./scripts/skills/run-imported-skill.ps1 web-info`

## Use When

- Статус Apache и веб-публикаций 1С — запущен ли сервер, какие базы опубликованы, ошибки. Используй когда пользователь спрашивает про статус веб-сервера, опубликованные базы, работает ли Apache
- Нужно использовать template-managed импортированный workflow без копирования inline логики из upstream `SKILL.md`.

## Usage

```bash
./scripts/skills/run-imported-skill.sh web-info --help
./scripts/skills/run-imported-skill.sh web-info ...
```

```powershell
./scripts/skills/run-imported-skill.ps1 web-info --help
./scripts/skills/run-imported-skill.ps1 web-info ...
```

## Adaptation

- Vendored upstream source: `automation/vendor/cc-1c-skills/skills/web-info/SKILL.md`
- Runtime kind: `python`
- Readiness target: `make imported-skills-readiness`
- Direct readiness command: `./scripts/skills/run-imported-skill.sh --readiness`
- Windows readiness command: `./scripts/skills/run-imported-skill.ps1 --readiness`
- Исполнение идёт через repo-owned dispatcher, который вызывает vendored Python helper.

## Rules

- Публичный contract для этого skill находится в repo-owned dispatcher, а не в vendored markdown.
- Если нужны детали параметров, сначала читайте vendored upstream `SKILL.md`, затем helper-скрипты из `automation/vendor/cc-1c-skills/`.
- Если dispatcher сообщает о missing dependencies, сначала используйте canonical readiness path, а не helper traceback.
- Не переносите upstream PowerShell snippets в новый automation contract шаблона.
