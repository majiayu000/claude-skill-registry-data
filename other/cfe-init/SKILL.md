---
name: cfe-init
description: "Создать расширение конфигурации 1С (CFE) — scaffold XML-исходников. Исп…"
metadata:
  short-description: "Создать расширение конфигурации 1С (CFE) — scaffold XML-исходников. Исп…"
---

<!-- GENERATED: sync-imported-skills -->

# Agent Skill: cfe-init

Repo script: `./scripts/skills/run-imported-skill.sh cfe-init`
Windows launcher: `./scripts/skills/run-imported-skill.ps1 cfe-init`

## Use When

- Создать расширение конфигурации 1С (CFE) — scaffold XML-исходников. Используй когда нужно создать новое расширение для исправления, доработки или дополнения конфигурации
- Нужно использовать template-managed импортированный workflow без копирования inline логики из upstream `SKILL.md`.

## Usage

```bash
./scripts/skills/run-imported-skill.sh cfe-init --help
./scripts/skills/run-imported-skill.sh cfe-init ...
```

```powershell
./scripts/skills/run-imported-skill.ps1 cfe-init --help
./scripts/skills/run-imported-skill.ps1 cfe-init ...
```

## Adaptation

- Vendored upstream source: `automation/vendor/cc-1c-skills/skills/cfe-init/SKILL.md`
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
