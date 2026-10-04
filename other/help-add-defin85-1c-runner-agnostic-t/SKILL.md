---
name: help-add
description: "Добавить встроенную справку к объекту 1С (обработка, отчёт, справочник,…"
metadata:
  short-description: "Добавить встроенную справку к объекту 1С (обработка, отчёт, справочник,…"
---

<!-- GENERATED: sync-imported-skills -->

# Agent Skill: help-add

Repo script: `./scripts/skills/run-imported-skill.sh help-add`
Windows launcher: `./scripts/skills/run-imported-skill.ps1 help-add`

## Use When

- Добавить встроенную справку к объекту 1С (обработка, отчёт, справочник, документ и др.). Используй когда пользователь просит добавить справку, help, встроенную помощь к объекту
- Нужно использовать template-managed импортированный workflow без копирования inline логики из upstream `SKILL.md`.

## Usage

```bash
./scripts/skills/run-imported-skill.sh help-add --help
./scripts/skills/run-imported-skill.sh help-add ...
```

```powershell
./scripts/skills/run-imported-skill.ps1 help-add --help
./scripts/skills/run-imported-skill.ps1 help-add ...
```

## Adaptation

- Vendored upstream source: `automation/vendor/cc-1c-skills/skills/help-add/SKILL.md`
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
