---
name: db-dump-cf
description: "Выгрузка конфигурации 1С в CF-файл. Используй когда пользователь просит…"
metadata:
  short-description: "Выгрузка конфигурации 1С в CF-файл. Используй когда пользователь просит…"
---

<!-- GENERATED: sync-imported-skills -->

# Agent Skill: db-dump-cf

Repo script: `./scripts/skills/run-imported-skill.sh db-dump-cf`
Windows launcher: `./scripts/skills/run-imported-skill.ps1 db-dump-cf`

## Use When

- Выгрузка конфигурации 1С в CF-файл. Используй когда пользователь просит выгрузить конфигурацию в CF, сохранить конфигурацию, сделать бэкап CF
- Нужно использовать template-managed импортированный workflow без копирования inline логики из upstream `SKILL.md`.

## Usage

```bash
./scripts/skills/run-imported-skill.sh db-dump-cf --help
./scripts/skills/run-imported-skill.sh db-dump-cf ...
```

```powershell
./scripts/skills/run-imported-skill.ps1 db-dump-cf --help
./scripts/skills/run-imported-skill.ps1 db-dump-cf ...
```

## Adaptation

- Vendored upstream source: `automation/vendor/cc-1c-skills/skills/db-dump-cf/SKILL.md`
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
