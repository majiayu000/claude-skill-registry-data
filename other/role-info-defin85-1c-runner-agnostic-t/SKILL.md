---
name: role-info
description: "Компактная сводка прав роли 1С из Rights.xml — объекты, права, RLS, шаб…"
metadata:
  short-description: "Компактная сводка прав роли 1С из Rights.xml — объекты, права, RLS, шаб…"
---

<!-- GENERATED: sync-imported-skills -->

# Agent Skill: role-info

Repo script: `./scripts/skills/run-imported-skill.sh role-info`
Windows launcher: `./scripts/skills/run-imported-skill.ps1 role-info`

## Use When

- Компактная сводка прав роли 1С из Rights.xml — объекты, права, RLS, шаблоны ограничений. Используй для аудита прав — какие объекты и действия доступны, ограничения RLS
- Нужно использовать template-managed импортированный workflow без копирования inline логики из upstream `SKILL.md`.

## Usage

```bash
./scripts/skills/run-imported-skill.sh role-info --help
./scripts/skills/run-imported-skill.sh role-info ...
```

```powershell
./scripts/skills/run-imported-skill.ps1 role-info --help
./scripts/skills/run-imported-skill.ps1 role-info ...
```

## Adaptation

- Vendored upstream source: `automation/vendor/cc-1c-skills/skills/role-info/SKILL.md`
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
