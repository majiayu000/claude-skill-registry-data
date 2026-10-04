---
name: db-load-xml
description: "Загрузка конфигурации 1С из XML-файлов. Используй когда пользователь пр…"
metadata:
  short-description: "Загрузка конфигурации 1С из XML-файлов. Используй когда пользователь пр…"
---

<!-- GENERATED: sync-imported-skills -->

# Agent Skill: db-load-xml

Repo script: `./scripts/skills/run-imported-skill.sh db-load-xml`
Windows launcher: `./scripts/skills/run-imported-skill.ps1 db-load-xml`

## Use When

- Загрузка конфигурации 1С из XML-файлов. Используй когда пользователь просит загрузить конфигурацию из файлов, XML, исходников, LoadConfigFromFiles
- Нужно использовать template-managed импортированный workflow без копирования inline логики из upstream `SKILL.md`.

## Usage

```bash
./scripts/skills/run-imported-skill.sh db-load-xml --help
./scripts/skills/run-imported-skill.sh db-load-xml ...
```

```powershell
./scripts/skills/run-imported-skill.ps1 db-load-xml --help
./scripts/skills/run-imported-skill.ps1 db-load-xml ...
```

## Adaptation

- Vendored upstream source: `automation/vendor/cc-1c-skills/skills/db-load-xml/SKILL.md`
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
