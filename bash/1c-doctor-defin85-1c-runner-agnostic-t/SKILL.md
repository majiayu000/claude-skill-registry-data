---
name: 1c-doctor
description: Используйте, когда нужно проверить readiness runtime profile, adapter config и базовые зависимости проекта.
metadata:
  short-description: Runtime readiness check.
---

# Agent Skill: 1c-doctor

Repo script: `./scripts/diag/doctor.sh`
Windows launcher: `./scripts/diag/doctor.ps1`

## Use When

- Нужно быстро проверить runtime environment перед запуском 1С контуров.
- Нужно увидеть missing tool/env dependency.

## Usage

```bash
./scripts/diag/doctor.sh --profile env/local.json
./scripts/diag/doctor.sh --profile env/ci.json --run-root /tmp/doctor-run
./scripts/diag/doctor.sh --profile env/local.json --dry-run
```

## Rules

- Этот skill проверяет readiness и не подменяет actual runtime capabilities.
- Вердикт и missing dependency берите из `summary.json`.
