---
name: db-run
description: "Запуск 1С:Предприятие. Используй когда пользователь просит запустить 1С…"
metadata:
  short-description: "Запуск 1С:Предприятие. Используй когда пользователь просит запустить 1С…"
---

<!-- GENERATED: sync-imported-skills -->

# Agent Skill: db-run

Repo script: `./scripts/skills/run-imported-skill.sh db-run`
Windows launcher: `./scripts/skills/run-imported-skill.ps1 db-run`

## Use When

- Запуск 1С:Предприятие. Используй когда пользователь просит запустить 1С, открыть базу, запустить предприятие
- Нужно использовать template-managed импортированный workflow без копирования inline логики из upstream `SKILL.md`.

## Usage

```bash
./scripts/skills/run-imported-skill.sh db-run --help
./scripts/skills/run-imported-skill.sh db-run ...
```

```powershell
./scripts/skills/run-imported-skill.ps1 db-run --help
./scripts/skills/run-imported-skill.ps1 db-run ...
```

## Adaptation

- Vendored upstream source: `automation/vendor/cc-1c-skills/skills/db-run/SKILL.md`
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
