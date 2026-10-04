---
name: img-grid
description: "Наложить пронумерованную сетку на изображение для определения пропорций…"
metadata:
  short-description: "Наложить пронумерованную сетку на изображение для определения пропорций…"
---

<!-- GENERATED: sync-imported-skills -->

# Agent Skill: img-grid

Repo script: `./scripts/skills/run-imported-skill.sh img-grid`
Windows launcher: `./scripts/skills/run-imported-skill.ps1 img-grid`

## Use When

- Наложить пронумерованную сетку на изображение для определения пропорций колонок
- Нужно использовать template-managed импортированный workflow без копирования inline логики из upstream `SKILL.md`.

## Usage

```bash
./scripts/skills/run-imported-skill.sh img-grid --help
./scripts/skills/run-imported-skill.sh img-grid ...
```

```powershell
./scripts/skills/run-imported-skill.ps1 img-grid --help
./scripts/skills/run-imported-skill.ps1 img-grid ...
```

## Adaptation

- Vendored upstream source: `automation/vendor/cc-1c-skills/skills/img-grid/SKILL.md`
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
