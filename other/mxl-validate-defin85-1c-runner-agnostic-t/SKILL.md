---
name: mxl-validate
description: "Валидация макета табличного документа (MXL). Используй после создания и…"
metadata:
  short-description: "Валидация макета табличного документа (MXL). Используй после создания и…"
---

<!-- GENERATED: sync-imported-skills -->

# Agent Skill: mxl-validate

Repo script: `./scripts/skills/run-imported-skill.sh mxl-validate`
Windows launcher: `./scripts/skills/run-imported-skill.ps1 mxl-validate`

## Use When

- Валидация макета табличного документа (MXL). Используй после создания или модификации макета для проверки корректности
- Нужно использовать template-managed импортированный workflow без копирования inline логики из upstream `SKILL.md`.

## Usage

```bash
./scripts/skills/run-imported-skill.sh mxl-validate --help
./scripts/skills/run-imported-skill.sh mxl-validate ...
```

```powershell
./scripts/skills/run-imported-skill.ps1 mxl-validate --help
./scripts/skills/run-imported-skill.ps1 mxl-validate ...
```

## Adaptation

- Vendored upstream source: `automation/vendor/cc-1c-skills/skills/mxl-validate/SKILL.md`
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
