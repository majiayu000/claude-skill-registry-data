---
name: meta-edit
description: "Точечное редактирование объекта метаданных 1С. Используй когда нужно до…"
metadata:
  short-description: "Точечное редактирование объекта метаданных 1С. Используй когда нужно до…"
---

<!-- GENERATED: sync-imported-skills -->

# Agent Skill: meta-edit

Repo script: `./scripts/skills/run-imported-skill.sh meta-edit`
Windows launcher: `./scripts/skills/run-imported-skill.ps1 meta-edit`

## Use When

- Точечное редактирование объекта метаданных 1С. Используй когда нужно добавить, удалить или изменить реквизиты, табличные части, измерения, ресурсы или свойства существующего объекта конфигурации
- Нужно использовать template-managed импортированный workflow без копирования inline логики из upstream `SKILL.md`.

## Usage

```bash
./scripts/skills/run-imported-skill.sh meta-edit --help
./scripts/skills/run-imported-skill.sh meta-edit ...
```

```powershell
./scripts/skills/run-imported-skill.ps1 meta-edit --help
./scripts/skills/run-imported-skill.ps1 meta-edit ...
```

## Adaptation

- Vendored upstream source: `automation/vendor/cc-1c-skills/skills/meta-edit/SKILL.md`
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
