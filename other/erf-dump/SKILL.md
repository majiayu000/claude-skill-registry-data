---
name: erf-dump
description: "Разобрать ERF-файл отчёта 1С в XML-исходники. Используй когда пользоват…"
metadata:
  short-description: "Разобрать ERF-файл отчёта 1С в XML-исходники. Используй когда пользоват…"
---

<!-- GENERATED: sync-imported-skills -->

# Agent Skill: erf-dump

Repo script: `./scripts/skills/run-imported-skill.sh erf-dump`
Windows launcher: `./scripts/skills/run-imported-skill.ps1 erf-dump`

## Use When

- Разобрать ERF-файл отчёта 1С в XML-исходники. Используй когда пользователь просит разобрать, декомпилировать отчёт, получить исходники из ERF файла
- Нужно использовать template-managed импортированный workflow без копирования inline логики из upstream `SKILL.md`.

## Usage

```bash
./scripts/skills/run-imported-skill.sh erf-dump --help
./scripts/skills/run-imported-skill.sh erf-dump ...
```

```powershell
./scripts/skills/run-imported-skill.ps1 erf-dump --help
./scripts/skills/run-imported-skill.ps1 erf-dump ...
```

## Adaptation

- Vendored upstream source: `automation/vendor/cc-1c-skills/skills/erf-dump/SKILL.md`
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
