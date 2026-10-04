---
name: cf-edit
description: "Точечное редактирование конфигурации 1С. Используй когда нужно изменить…"
metadata:
  short-description: "Точечное редактирование конфигурации 1С. Используй когда нужно изменить…"
---

<!-- GENERATED: sync-imported-skills -->

# Agent Skill: cf-edit

Repo script: `./scripts/skills/run-imported-skill.sh cf-edit`
Windows launcher: `./scripts/skills/run-imported-skill.ps1 cf-edit`

## Use When

- Точечное редактирование конфигурации 1С. Используй когда нужно изменить свойства конфигурации, добавить или удалить объект из состава, настроить роли по умолчанию
- Нужно использовать template-managed импортированный workflow без копирования inline логики из upstream `SKILL.md`.

## Usage

```bash
./scripts/skills/run-imported-skill.sh cf-edit --help
./scripts/skills/run-imported-skill.sh cf-edit ...
```

```powershell
./scripts/skills/run-imported-skill.ps1 cf-edit --help
./scripts/skills/run-imported-skill.ps1 cf-edit ...
```

## Adaptation

- Vendored upstream source: `automation/vendor/cc-1c-skills/skills/cf-edit/SKILL.md`
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
