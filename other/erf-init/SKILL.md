---
name: erf-init
description: "Создать пустой внешний отчёт 1С (scaffold XML-исходников)"
metadata:
  short-description: "Создать пустой внешний отчёт 1С (scaffold XML-исходников)"
---

<!-- GENERATED: sync-imported-skills -->

# Agent Skill: erf-init

Repo script: `./scripts/skills/run-imported-skill.sh erf-init`
Windows launcher: `./scripts/skills/run-imported-skill.ps1 erf-init`

## Use When

- Создать пустой внешний отчёт 1С (scaffold XML-исходников)
- Нужно использовать template-managed импортированный workflow без копирования inline логики из upstream `SKILL.md`.

## Usage

```bash
./scripts/skills/run-imported-skill.sh erf-init --help
./scripts/skills/run-imported-skill.sh erf-init ...
```

```powershell
./scripts/skills/run-imported-skill.ps1 erf-init --help
./scripts/skills/run-imported-skill.ps1 erf-init ...
```

## Adaptation

- Vendored upstream source: `automation/vendor/cc-1c-skills/skills/erf-init/SKILL.md`
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
