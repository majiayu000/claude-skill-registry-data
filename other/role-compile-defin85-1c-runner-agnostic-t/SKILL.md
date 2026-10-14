---
name: role-compile
description: "Создание роли 1С из описания прав. Используй когда нужно создать новую…"
metadata:
  short-description: "Создание роли 1С из описания прав. Используй когда нужно создать новую…"
---

<!-- GENERATED: sync-imported-skills -->

# Agent Skill: role-compile

Repo script: `./scripts/skills/run-imported-skill.sh role-compile`
Windows launcher: `./scripts/skills/run-imported-skill.ps1 role-compile`

## Use When

- Создание роли 1С из описания прав. Используй когда нужно создать новую роль с набором прав на объекты
- Нужно использовать template-managed импортированный workflow без копирования inline логики из upstream `SKILL.md`.

## Usage

```bash
./scripts/skills/run-imported-skill.sh role-compile --help
./scripts/skills/run-imported-skill.sh role-compile ...
```

```powershell
./scripts/skills/run-imported-skill.ps1 role-compile --help
./scripts/skills/run-imported-skill.ps1 role-compile ...
```

## Adaptation

- Vendored upstream source: `automation/vendor/cc-1c-skills/skills/role-compile/SKILL.md`
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
