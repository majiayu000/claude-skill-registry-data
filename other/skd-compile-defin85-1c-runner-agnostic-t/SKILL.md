---
name: skd-compile
description: "Компиляция схемы компоновки данных 1С (СКД) из компактного JSON-определ…"
metadata:
  short-description: "Компиляция схемы компоновки данных 1С (СКД) из компактного JSON-определ…"
---

<!-- GENERATED: sync-imported-skills -->

# Agent Skill: skd-compile

Repo script: `./scripts/skills/run-imported-skill.sh skd-compile`
Windows launcher: `./scripts/skills/run-imported-skill.ps1 skd-compile`

## Use When

- Компиляция схемы компоновки данных 1С (СКД) из компактного JSON-определения. Используй когда нужно создать СКД с нуля
- Нужно использовать template-managed импортированный workflow без копирования inline логики из upstream `SKILL.md`.

## Usage

```bash
./scripts/skills/run-imported-skill.sh skd-compile --help
./scripts/skills/run-imported-skill.sh skd-compile ...
```

```powershell
./scripts/skills/run-imported-skill.ps1 skd-compile --help
./scripts/skills/run-imported-skill.ps1 skd-compile ...
```

## Adaptation

- Vendored upstream source: `automation/vendor/cc-1c-skills/skills/skd-compile/SKILL.md`
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
