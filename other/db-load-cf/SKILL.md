---
name: db-load-cf
description: "Загрузка конфигурации 1С из CF-файла. Используй когда пользователь прос…"
metadata:
  short-description: "Загрузка конфигурации 1С из CF-файла. Используй когда пользователь прос…"
---

<!-- GENERATED: sync-imported-skills -->

# Agent Skill: db-load-cf

Repo script: `./scripts/skills/run-imported-skill.sh db-load-cf`
Windows launcher: `./scripts/skills/run-imported-skill.ps1 db-load-cf`

## Use When

- Загрузка конфигурации 1С из CF-файла. Используй когда пользователь просит загрузить конфигурацию из CF, восстановить из бэкапа CF
- Нужно использовать template-managed импортированный workflow без копирования inline логики из upstream `SKILL.md`.

## Usage

```bash
./scripts/skills/run-imported-skill.sh db-load-cf --help
./scripts/skills/run-imported-skill.sh db-load-cf ...
```

```powershell
./scripts/skills/run-imported-skill.ps1 db-load-cf --help
./scripts/skills/run-imported-skill.ps1 db-load-cf ...
```

## Adaptation

- Vendored upstream source: `automation/vendor/cc-1c-skills/skills/db-load-cf/SKILL.md`
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
