---
name: skd-info
description: "Анализ структуры схемы компоновки данных 1С (СКД) — наборы, поля, парам…"
metadata:
  short-description: "Анализ структуры схемы компоновки данных 1С (СКД) — наборы, поля, парам…"
---

<!-- GENERATED: sync-imported-skills -->

# Agent Skill: skd-info

Repo script: `./scripts/skills/run-imported-skill.sh skd-info`
Windows launcher: `./scripts/skills/run-imported-skill.ps1 skd-info`

## Use When

- Анализ структуры схемы компоновки данных 1С (СКД) — наборы, поля, параметры, варианты. Используй для понимания отчёта — источник данных (запрос), доступные поля, параметры
- Нужно использовать template-managed импортированный workflow без копирования inline логики из upstream `SKILL.md`.

## Usage

```bash
./scripts/skills/run-imported-skill.sh skd-info --help
./scripts/skills/run-imported-skill.sh skd-info ...
```

```powershell
./scripts/skills/run-imported-skill.ps1 skd-info --help
./scripts/skills/run-imported-skill.ps1 skd-info ...
```

## Adaptation

- Vendored upstream source: `automation/vendor/cc-1c-skills/skills/skd-info/SKILL.md`
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
