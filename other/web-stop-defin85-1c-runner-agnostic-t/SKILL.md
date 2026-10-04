---
name: web-stop
description: "Остановка Apache HTTP Server. Используй когда пользователь просит остан…"
metadata:
  short-description: "Остановка Apache HTTP Server. Используй когда пользователь просит остан…"
---

<!-- GENERATED: sync-imported-skills -->

# Agent Skill: web-stop

Repo script: `./scripts/skills/run-imported-skill.sh web-stop`
Windows launcher: `./scripts/skills/run-imported-skill.ps1 web-stop`

## Use When

- Остановка Apache HTTP Server. Используй когда пользователь просит остановить веб-сервер, Apache, прекратить веб-публикацию
- Нужно использовать template-managed импортированный workflow без копирования inline логики из upstream `SKILL.md`.

## Usage

```bash
./scripts/skills/run-imported-skill.sh web-stop --help
./scripts/skills/run-imported-skill.sh web-stop ...
```

```powershell
./scripts/skills/run-imported-skill.ps1 web-stop --help
./scripts/skills/run-imported-skill.ps1 web-stop ...
```

## Adaptation

- Vendored upstream source: `automation/vendor/cc-1c-skills/skills/web-stop/SKILL.md`
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
