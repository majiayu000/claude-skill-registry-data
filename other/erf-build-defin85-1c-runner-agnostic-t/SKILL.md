---
name: erf-build
description: "Собрать внешний отчёт 1С (ERF) из XML-исходников. Используй когда польз…"
metadata:
  short-description: "Собрать внешний отчёт 1С (ERF) из XML-исходников. Используй когда польз…"
---

<!-- GENERATED: sync-imported-skills -->

# Agent Skill: erf-build

Repo script: `./scripts/skills/run-imported-skill.sh erf-build`
Windows launcher: `./scripts/skills/run-imported-skill.ps1 erf-build`

## Use When

- Собрать внешний отчёт 1С (ERF) из XML-исходников. Используй когда пользователь просит собрать, скомпилировать отчёт или получить ERF файл из исходников
- Нужно использовать template-managed импортированный workflow без копирования inline логики из upstream `SKILL.md`.

## Usage

```bash
./scripts/skills/run-imported-skill.sh erf-build --help
./scripts/skills/run-imported-skill.sh erf-build ...
```

```powershell
./scripts/skills/run-imported-skill.ps1 erf-build --help
./scripts/skills/run-imported-skill.ps1 erf-build ...
```

## Adaptation

- Vendored upstream source: `automation/vendor/cc-1c-skills/skills/erf-build/SKILL.md`
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
