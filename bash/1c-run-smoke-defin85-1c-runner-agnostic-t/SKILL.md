---
name: 1c-run-smoke
description: Используйте, когда нужно запустить smoke contour через канонический test entrypoint проекта.
metadata:
  short-description: Smoke contour.
---

# Agent Skill: 1c-run-smoke

Repo script: `./scripts/test/run-smoke.sh`
Windows launcher: `./scripts/test/run-smoke.ps1`

## Use When

- Нужно быстро проверить минимальный рабочий contour.
- Нужен единый smoke entrypoint с machine-readable итогом.

## Usage

```bash
./scripts/test/run-smoke.sh --profile env/local.json
./scripts/test/run-smoke.sh --profile env/ci.json --run-root /tmp/run-smoke
./scripts/test/run-smoke.sh --profile env/local.json --dry-run
```

## Rules

- Не переносите smoke runtime logic в skill.
- Используйте `summary.json` как первичный verdict.
