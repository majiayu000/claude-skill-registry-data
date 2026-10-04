---
name: skd-edit
description: "Точечное редактирование схемы компоновки данных 1С (СКД). Используй ког…"
metadata:
  short-description: "Точечное редактирование схемы компоновки данных 1С (СКД). Используй ког…"
---

<!-- GENERATED: sync-imported-skills -->

# Agent Skill: skd-edit

Repo script: `./scripts/skills/run-imported-skill.sh skd-edit`
Windows launcher: `./scripts/skills/run-imported-skill.ps1 skd-edit`

## Use When

- Точечное редактирование схемы компоновки данных 1С (СКД). Используй когда нужно модифицировать существующую СКД — добавить поля, итоги, фильтры, параметры, изменить текст запроса
- Нужно использовать template-managed импортированный workflow без копирования inline логики из upstream `SKILL.md`.

## Usage

```bash
./scripts/skills/run-imported-skill.sh skd-edit --help
./scripts/skills/run-imported-skill.sh skd-edit ...
```

```powershell
./scripts/skills/run-imported-skill.ps1 skd-edit --help
./scripts/skills/run-imported-skill.ps1 skd-edit ...
```

## Adaptation

- Vendored upstream source: `automation/vendor/cc-1c-skills/skills/skd-edit/SKILL.md`
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
