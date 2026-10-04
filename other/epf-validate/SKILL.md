---
name: epf-validate
description: "Валидация внешней обработки 1С (EPF). Используй после создания или моди…"
metadata:
  short-description: "Валидация внешней обработки 1С (EPF). Используй после создания или моди…"
---

<!-- GENERATED: sync-imported-skills -->

# Agent Skill: epf-validate

Repo script: `./scripts/skills/run-imported-skill.sh epf-validate`
Windows launcher: `./scripts/skills/run-imported-skill.ps1 epf-validate`

## Use When

- Валидация внешней обработки 1С (EPF). Используй после создания или модификации обработки для проверки корректности
- Нужно использовать template-managed импортированный workflow без копирования inline логики из upstream `SKILL.md`.

## Usage

```bash
./scripts/skills/run-imported-skill.sh epf-validate --help
./scripts/skills/run-imported-skill.sh epf-validate ...
```

```powershell
./scripts/skills/run-imported-skill.ps1 epf-validate --help
./scripts/skills/run-imported-skill.ps1 epf-validate ...
```

## Adaptation

- Vendored upstream source: `automation/vendor/cc-1c-skills/skills/epf-validate/SKILL.md`
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
