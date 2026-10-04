---
name: epf-build
description: "Собрать внешнюю обработку 1С (EPF/ERF) из XML-исходников. Используй ког…"
metadata:
  short-description: "Собрать внешнюю обработку 1С (EPF/ERF) из XML-исходников. Используй ког…"
---

<!-- GENERATED: sync-imported-skills -->

# Agent Skill: epf-build

Repo script: `./scripts/skills/run-imported-skill.sh epf-build`
Windows launcher: `./scripts/skills/run-imported-skill.ps1 epf-build`

## Use When

- Собрать внешнюю обработку 1С (EPF/ERF) из XML-исходников. Используй когда пользователь просит собрать, скомпилировать обработку или получить EPF/ERF файл из исходников
- Нужно использовать template-managed импортированный workflow без копирования inline логики из upstream `SKILL.md`.

## Usage

```bash
./scripts/skills/run-imported-skill.sh epf-build --help
./scripts/skills/run-imported-skill.sh epf-build ...
```

```powershell
./scripts/skills/run-imported-skill.ps1 epf-build --help
./scripts/skills/run-imported-skill.ps1 epf-build ...
```

## Adaptation

- Vendored upstream source: `automation/vendor/cc-1c-skills/skills/epf-build/SKILL.md`
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
