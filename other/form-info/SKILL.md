---
name: form-info
description: "Анализ структуры управляемой формы 1С (Form.xml) — элементы, реквизиты,…"
metadata:
  short-description: "Анализ структуры управляемой формы 1С (Form.xml) — элементы, реквизиты,…"
---

<!-- GENERATED: sync-imported-skills -->

# Agent Skill: form-info

Repo script: `./scripts/skills/run-imported-skill.sh form-info`
Windows launcher: `./scripts/skills/run-imported-skill.ps1 form-info`

## Use When

- Анализ структуры управляемой формы 1С (Form.xml) — элементы, реквизиты, команды, события. Используй для понимания формы — при написании модуля формы, анализе обработчиков и элементов
- Нужно использовать template-managed импортированный workflow без копирования inline логики из upstream `SKILL.md`.

## Usage

```bash
./scripts/skills/run-imported-skill.sh form-info --help
./scripts/skills/run-imported-skill.sh form-info ...
```

```powershell
./scripts/skills/run-imported-skill.ps1 form-info --help
./scripts/skills/run-imported-skill.ps1 form-info ...
```

## Adaptation

- Vendored upstream source: `automation/vendor/cc-1c-skills/skills/form-info/SKILL.md`
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
