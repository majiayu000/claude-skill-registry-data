---
name: mxl-compile
description: "Компиляция табличного документа (MXL) из JSON-определения. Используй ко…"
metadata:
  short-description: "Компиляция табличного документа (MXL) из JSON-определения. Используй ко…"
---

<!-- GENERATED: sync-imported-skills -->

# Agent Skill: mxl-compile

Repo script: `./scripts/skills/run-imported-skill.sh mxl-compile`
Windows launcher: `./scripts/skills/run-imported-skill.ps1 mxl-compile`

## Use When

- Компиляция табличного документа (MXL) из JSON-определения. Используй когда нужно создать макет печатной формы
- Нужно использовать template-managed импортированный workflow без копирования inline логики из upstream `SKILL.md`.

## Usage

```bash
./scripts/skills/run-imported-skill.sh mxl-compile --help
./scripts/skills/run-imported-skill.sh mxl-compile ...
```

```powershell
./scripts/skills/run-imported-skill.ps1 mxl-compile --help
./scripts/skills/run-imported-skill.ps1 mxl-compile ...
```

## Adaptation

- Vendored upstream source: `automation/vendor/cc-1c-skills/skills/mxl-compile/SKILL.md`
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
