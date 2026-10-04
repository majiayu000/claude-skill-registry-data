---
name: db-update
description: "Prefer native 1c-update-db. Обновление конфигурации базы данных 1С. Исп…"
metadata:
  short-description: "Prefer native 1c-update-db. Обновление конфигурации базы данных 1С. Исп…"
---

<!-- GENERATED: sync-imported-skills -->

# Agent Skill: db-update

Repo script: `./scripts/skills/run-imported-skill.sh db-update`
Windows launcher: `./scripts/skills/run-imported-skill.ps1 db-update`

## Use When

- Обновление конфигурации базы данных 1С. Используй когда пользователь просит обновить БД, применить конфигурацию, UpdateDBCfg
- Нужно использовать template-managed импортированный workflow без копирования inline логики из upstream `SKILL.md`.

## Usage

```bash
./scripts/skills/run-imported-skill.sh db-update --help
./scripts/skills/run-imported-skill.sh db-update ...
```

```powershell
./scripts/skills/run-imported-skill.ps1 db-update --help
./scripts/skills/run-imported-skill.ps1 db-update ...
```

## Adaptation

- Vendored upstream source: `automation/vendor/cc-1c-skills/skills/db-update/SKILL.md`
- Runtime kind: `native-alias`
- Readiness target: `make imported-skills-readiness`
- Direct readiness command: `./scripts/skills/run-imported-skill.sh --readiness`
- Windows readiness command: `./scripts/skills/run-imported-skill.ps1 --readiness`
- Это compatibility alias: dispatcher проксирует вызов в native runner-agnostic capability шаблона.
- Для native runner-agnostic workflow предпочитайте: `1c-update-db`.

## Rules

- Публичный contract для этого skill находится в repo-owned dispatcher, а не в vendored markdown.
- Если нужны детали параметров, сначала читайте vendored upstream `SKILL.md`, затем helper-скрипты из `automation/vendor/cc-1c-skills/`.
- Если dispatcher сообщает о missing dependencies, сначала используйте canonical readiness path, а не helper traceback.
- Не переносите upstream PowerShell snippets в новый automation contract шаблона.
