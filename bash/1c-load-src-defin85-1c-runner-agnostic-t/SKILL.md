---
name: 1c-load-src
description: Используйте, когда нужно загрузить исходники в информационную базу через канонический runtime contract проекта.
metadata:
  short-description: Загрузка исходников в ИБ.
---

# Agent Skill: 1c-load-src

Repo script: `./scripts/platform/load-src.sh`
Windows launcher: `./scripts/platform/load-src.ps1`

## Use When

- Нужно загрузить исходники конфигурации или расширения в ИБ.
- Нужен adapter-aware load с machine-readable артефактами.

## Usage

```bash
./scripts/platform/load-src.sh --profile env/local.json
./scripts/platform/load-src.sh --profile env/ci.json --run-root /tmp/load-src-run
./scripts/platform/load-src.sh --profile env/local.json --dry-run
```

## Rules

- Не переносите shell/1C CLI в skill как inline logic.
- После выполнения сначала читайте `summary.json`.
