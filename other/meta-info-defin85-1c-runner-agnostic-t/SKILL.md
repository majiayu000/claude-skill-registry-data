---
name: meta-info
description: "Анализ структуры объекта метаданных 1С из XML-выгрузки — реквизиты, таб…"
metadata:
  short-description: "Анализ структуры объекта метаданных 1С из XML-выгрузки — реквизиты, таб…"
---

<!-- GENERATED: sync-imported-skills -->

# Agent Skill: meta-info

Repo script: `./scripts/skills/run-imported-skill.sh meta-info`
Windows launcher: `./scripts/skills/run-imported-skill.ps1 meta-info`

## Use When

- Анализ структуры объекта метаданных 1С из XML-выгрузки — реквизиты, табличные части, формы, движения, типы. Используй для изучения структуры объектов (вместо чтения XML-файлов напрямую) и как подготовительный шаг при написании запросов и кода, работающего с объектами
- Нужно использовать template-managed импортированный workflow без копирования inline логики из upstream `SKILL.md`.

## Usage

```bash
./scripts/skills/run-imported-skill.sh meta-info --help
./scripts/skills/run-imported-skill.sh meta-info ...
```

```powershell
./scripts/skills/run-imported-skill.ps1 meta-info --help
./scripts/skills/run-imported-skill.ps1 meta-info ...
```

## Adaptation

- Vendored upstream source: `automation/vendor/cc-1c-skills/skills/meta-info/SKILL.md`
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
