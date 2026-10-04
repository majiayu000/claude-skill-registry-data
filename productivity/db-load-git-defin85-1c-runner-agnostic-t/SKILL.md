---
name: db-load-git
description: "Prefer native 1c-load-diff-src, 1c-load-task-src. Загрузка изменений из…"
metadata:
  short-description: "Prefer native 1c-load-diff-src, 1c-load-task-src. Загрузка изменений из…"
---

<!-- GENERATED: sync-imported-skills -->

# Agent Skill: db-load-git

Repo script: `./scripts/skills/run-imported-skill.sh db-load-git`
Windows launcher: `./scripts/skills/run-imported-skill.ps1 db-load-git`

## Use When

- Загрузка изменений из Git в базу 1С. Используй когда пользователь просит загрузить изменения из гита, обновить базу из репозитория, partial load из коммита
- Нужно использовать template-managed импортированный workflow без копирования inline логики из upstream `SKILL.md`.

## Usage

```bash
./scripts/skills/run-imported-skill.sh db-load-git --help
./scripts/skills/run-imported-skill.sh db-load-git ...
```

```powershell
./scripts/skills/run-imported-skill.ps1 db-load-git --help
./scripts/skills/run-imported-skill.ps1 db-load-git ...
```

## Adaptation

- Vendored upstream source: `automation/vendor/cc-1c-skills/skills/db-load-git/SKILL.md`
- Runtime kind: `python`
- Readiness target: `make imported-skills-readiness`
- Direct readiness command: `./scripts/skills/run-imported-skill.sh --readiness`
- Windows readiness command: `./scripts/skills/run-imported-skill.ps1 --readiness`
- Исполнение идёт через repo-owned dispatcher, который вызывает vendored Python helper.
- Для native runner-agnostic workflow предпочитайте: `1c-load-diff-src`, `1c-load-task-src`.

## Rules

- Публичный contract для этого skill находится в repo-owned dispatcher, а не в vendored markdown.
- Если нужны детали параметров, сначала читайте vendored upstream `SKILL.md`, затем helper-скрипты из `automation/vendor/cc-1c-skills/`.
- Если dispatcher сообщает о missing dependencies, сначала используйте canonical readiness path, а не helper traceback.
- Не переносите upstream PowerShell snippets в новый automation contract шаблона.
