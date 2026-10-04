---
name: cfe-diff
description: "Анализ расширения конфигурации 1С (CFE) — состав, заимствованные объект…"
metadata:
  short-description: "Анализ расширения конфигурации 1С (CFE) — состав, заимствованные объект…"
---

<!-- GENERATED: sync-imported-skills -->

# Agent Skill: cfe-diff

Repo script: `./scripts/skills/run-imported-skill.sh cfe-diff`
Windows launcher: `./scripts/skills/run-imported-skill.ps1 cfe-diff`

## Use When

- Анализ расширения конфигурации 1С (CFE) — состав, заимствованные объекты, перехватчики, проверка переноса. Используй когда нужно понять что содержит расширение или проверить перенесены ли вставки в конфигурацию
- Нужно использовать template-managed импортированный workflow без копирования inline логики из upstream `SKILL.md`.

## Usage

```bash
./scripts/skills/run-imported-skill.sh cfe-diff --help
./scripts/skills/run-imported-skill.sh cfe-diff ...
```

```powershell
./scripts/skills/run-imported-skill.ps1 cfe-diff --help
./scripts/skills/run-imported-skill.ps1 cfe-diff ...
```

## Adaptation

- Vendored upstream source: `automation/vendor/cc-1c-skills/skills/cfe-diff/SKILL.md`
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
