---
name: mxl-info
description: "Анализ структуры макета табличного документа (MXL) — области, параметры…"
metadata:
  short-description: "Анализ структуры макета табличного документа (MXL) — области, параметры…"
---

<!-- GENERATED: sync-imported-skills -->

# Agent Skill: mxl-info

Repo script: `./scripts/skills/run-imported-skill.sh mxl-info`
Windows launcher: `./scripts/skills/run-imported-skill.ps1 mxl-info`

## Use When

- Анализ структуры макета табличного документа (MXL) — области, параметры, наборы колонок. Используй при разработке печати — получить области и заполняемые параметры макета
- Нужно использовать template-managed импортированный workflow без копирования inline логики из upstream `SKILL.md`.

## Usage

```bash
./scripts/skills/run-imported-skill.sh mxl-info --help
./scripts/skills/run-imported-skill.sh mxl-info ...
```

```powershell
./scripts/skills/run-imported-skill.ps1 mxl-info --help
./scripts/skills/run-imported-skill.ps1 mxl-info ...
```

## Adaptation

- Vendored upstream source: `automation/vendor/cc-1c-skills/skills/mxl-info/SKILL.md`
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
