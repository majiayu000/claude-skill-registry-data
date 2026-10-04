---
name: cfe-borrow
description: "Заимствование объектов из конфигурации 1С в расширение (CFE). Используй…"
metadata:
  short-description: "Заимствование объектов из конфигурации 1С в расширение (CFE). Используй…"
---

<!-- GENERATED: sync-imported-skills -->

# Agent Skill: cfe-borrow

Repo script: `./scripts/skills/run-imported-skill.sh cfe-borrow`
Windows launcher: `./scripts/skills/run-imported-skill.ps1 cfe-borrow`

## Use When

- Заимствование объектов из конфигурации 1С в расширение (CFE). Используй когда нужно перехватить метод, изменить форму или добавить реквизит к существующему объекту конфигурации
- Нужно использовать template-managed импортированный workflow без копирования inline логики из upstream `SKILL.md`.

## Usage

```bash
./scripts/skills/run-imported-skill.sh cfe-borrow --help
./scripts/skills/run-imported-skill.sh cfe-borrow ...
```

```powershell
./scripts/skills/run-imported-skill.ps1 cfe-borrow --help
./scripts/skills/run-imported-skill.ps1 cfe-borrow ...
```

## Adaptation

- Vendored upstream source: `automation/vendor/cc-1c-skills/skills/cfe-borrow/SKILL.md`
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
