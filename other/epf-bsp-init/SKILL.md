---
name: epf-bsp-init
description: "Добавить функцию регистрации БСП (СведенияОВнешнейОбработке) в модуль о…"
metadata:
  short-description: "Добавить функцию регистрации БСП (СведенияОВнешнейОбработке) в модуль о…"
---

<!-- GENERATED: sync-imported-skills -->

# Agent Skill: epf-bsp-init

Repo script: `./scripts/skills/run-imported-skill.sh epf-bsp-init`
Windows launcher: `./scripts/skills/run-imported-skill.ps1 epf-bsp-init`

## Use When

- Добавить функцию регистрации БСП (СведенияОВнешнейОбработке) в модуль объекта обработки
- Нужно использовать template-managed импортированный workflow без копирования inline логики из upstream `SKILL.md`.

## Usage

```bash
./scripts/skills/run-imported-skill.sh epf-bsp-init --help
./scripts/skills/run-imported-skill.sh epf-bsp-init ...
```

```powershell
./scripts/skills/run-imported-skill.ps1 epf-bsp-init --help
./scripts/skills/run-imported-skill.ps1 epf-bsp-init ...
```

## Adaptation

- Vendored upstream source: `automation/vendor/cc-1c-skills/skills/epf-bsp-init/SKILL.md`
- Runtime kind: `reference`
- Readiness target: `make imported-skills-readiness`
- Direct readiness command: `./scripts/skills/run-imported-skill.sh --readiness`
- Windows readiness command: `./scripts/skills/run-imported-skill.ps1 --readiness`
- Это reference-only импорт: repo script печатает адаптированную сводку и указывает на vendored upstream материалы.

## Rules

- Публичный contract для этого skill находится в repo-owned dispatcher, а не в vendored markdown.
- Если нужны детали параметров, сначала читайте vendored upstream `SKILL.md`, затем helper-скрипты из `automation/vendor/cc-1c-skills/`.
- Если dispatcher сообщает о missing dependencies, сначала используйте canonical readiness path, а не helper traceback.
- Не переносите upstream PowerShell snippets в новый automation contract шаблона.
