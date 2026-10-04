---
name: meta-remove
description: "Удалить объект метаданных из конфигурации 1С. Используй когда пользоват…"
metadata:
  short-description: "Удалить объект метаданных из конфигурации 1С. Используй когда пользоват…"
---

<!-- GENERATED: sync-imported-skills -->

# Agent Skill: meta-remove

Repo script: `./scripts/skills/run-imported-skill.sh meta-remove`
Windows launcher: `./scripts/skills/run-imported-skill.ps1 meta-remove`

## Use When

- Удалить объект метаданных из конфигурации 1С. Используй когда пользователь просит удалить, убрать объект из конфигурации
- Нужно использовать template-managed импортированный workflow без копирования inline логики из upstream `SKILL.md`.

## Usage

```bash
./scripts/skills/run-imported-skill.sh meta-remove --help
./scripts/skills/run-imported-skill.sh meta-remove ...
```

```powershell
./scripts/skills/run-imported-skill.ps1 meta-remove --help
./scripts/skills/run-imported-skill.ps1 meta-remove ...
```

## Adaptation

- Vendored upstream source: `automation/vendor/cc-1c-skills/skills/meta-remove/SKILL.md`
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
