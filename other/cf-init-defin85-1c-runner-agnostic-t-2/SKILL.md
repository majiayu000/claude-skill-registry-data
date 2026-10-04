---
name: cf-init
description: "Создать пустую конфигурацию 1С (scaffold XML-исходников). Используй ког…"
metadata:
  short-description: "Создать пустую конфигурацию 1С (scaffold XML-исходников). Используй ког…"
---

<!-- GENERATED: sync-imported-skills -->

# Agent Skill: cf-init

Repo script: `./scripts/skills/run-imported-skill.sh cf-init`
Windows launcher: `./scripts/skills/run-imported-skill.ps1 cf-init`

## Use When

- Создать пустую конфигурацию 1С (scaffold XML-исходников). Используй когда нужно начать новую конфигурацию с нуля
- Нужно использовать template-managed импортированный workflow без копирования inline логики из upstream `SKILL.md`.

## Usage

```bash
./scripts/skills/run-imported-skill.sh cf-init --help
./scripts/skills/run-imported-skill.sh cf-init ...
```

```powershell
./scripts/skills/run-imported-skill.ps1 cf-init --help
./scripts/skills/run-imported-skill.ps1 cf-init ...
```

## Adaptation

- Vendored upstream source: `automation/vendor/cc-1c-skills/skills/cf-init/SKILL.md`
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
