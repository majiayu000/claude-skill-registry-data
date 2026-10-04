---
name: epf-dump
description: "Разобрать EPF-файл обработки 1С (EPF/ERF) в XML-исходники. Используй ко…"
metadata:
  short-description: "Разобрать EPF-файл обработки 1С (EPF/ERF) в XML-исходники. Используй ко…"
---

<!-- GENERATED: sync-imported-skills -->

# Agent Skill: epf-dump

Repo script: `./scripts/skills/run-imported-skill.sh epf-dump`
Windows launcher: `./scripts/skills/run-imported-skill.ps1 epf-dump`

## Use When

- Разобрать EPF-файл обработки 1С (EPF/ERF) в XML-исходники. Используй когда пользователь просит разобрать, декомпилировать обработку, получить исходники из EPF/ERF файла
- Нужно использовать template-managed импортированный workflow без копирования inline логики из upstream `SKILL.md`.

## Usage

```bash
./scripts/skills/run-imported-skill.sh epf-dump --help
./scripts/skills/run-imported-skill.sh epf-dump ...
```

```powershell
./scripts/skills/run-imported-skill.ps1 epf-dump --help
./scripts/skills/run-imported-skill.ps1 epf-dump ...
```

## Adaptation

- Vendored upstream source: `automation/vendor/cc-1c-skills/skills/epf-dump/SKILL.md`
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
