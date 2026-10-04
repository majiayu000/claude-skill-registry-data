---
name: 1c-diff-src
description: Используйте, когда нужно сравнить source tree или выполнить adapter-aware diff через repo-owned entrypoint.
metadata:
  short-description: Diff исходников через repo script.
---

# Agent Skill: 1c-diff-src

Repo script: `./scripts/platform/diff-src.sh`
Windows launcher: `./scripts/platform/diff-src.ps1`

## Use When

- Нужно посмотреть diff исходников.
- Нужен единый machine-readable результат прогона.

## Usage

```bash
./scripts/platform/diff-src.sh --profile env/local.json
./scripts/platform/diff-src.sh --profile env/ci.json --run-root /tmp/diff-src-run
./scripts/platform/diff-src.sh --profile env/local.json --dry-run
```

## Rules

- Не копируйте diff logic в `SKILL.md`.
- Интерпретацию результата начинайте с `summary.json`.
