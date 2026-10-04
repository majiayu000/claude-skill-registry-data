---
name: web-publish
description: "Prefer native 1c-publish-http. Публикация информационной базы 1С через…"
metadata:
  short-description: "Prefer native 1c-publish-http. Публикация информационной базы 1С через…"
---

<!-- GENERATED: sync-imported-skills -->

# Agent Skill: web-publish

Repo script: `./scripts/skills/run-imported-skill.sh web-publish`
Windows launcher: `./scripts/skills/run-imported-skill.ps1 web-publish`

## Use When

- Публикация информационной базы 1С через Apache. Используй когда пользователь просит опубликовать базу, сервисы, настроить веб-доступ, веб-клиент, открыть в браузере
- Нужно использовать template-managed импортированный workflow без копирования inline логики из upstream `SKILL.md`.

## Usage

```bash
./scripts/skills/run-imported-skill.sh web-publish --help
./scripts/skills/run-imported-skill.sh web-publish ...
```

```powershell
./scripts/skills/run-imported-skill.ps1 web-publish --help
./scripts/skills/run-imported-skill.ps1 web-publish ...
```

## Adaptation

- Vendored upstream source: `automation/vendor/cc-1c-skills/skills/web-publish/SKILL.md`
- Runtime kind: `native-alias`
- Readiness target: `make imported-skills-readiness`
- Direct readiness command: `./scripts/skills/run-imported-skill.sh --readiness`
- Windows readiness command: `./scripts/skills/run-imported-skill.ps1 --readiness`
- Это compatibility alias: dispatcher проксирует вызов в native runner-agnostic capability шаблона.
- Для native runner-agnostic workflow предпочитайте: `1c-publish-http`.

## Rules

- Публичный contract для этого skill находится в repo-owned dispatcher, а не в vendored markdown.
- Если нужны детали параметров, сначала читайте vendored upstream `SKILL.md`, затем helper-скрипты из `automation/vendor/cc-1c-skills/`.
- Если dispatcher сообщает о missing dependencies, сначала используйте canonical readiness path, а не helper traceback.
- Не переносите upstream PowerShell snippets в новый automation contract шаблона.
