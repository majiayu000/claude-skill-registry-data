---
name: 1c-update-db
description: Используйте, когда нужно применить изменения основной конфигурации к конфигурации базы данных.
metadata:
  short-description: Update DB contour.
---

# Agent Skill: 1c-update-db

Repo script: `./scripts/platform/update-db.sh`
Windows launcher: `./scripts/platform/update-db.ps1`

## Use When

- Нужно выполнить `UpdateDBCfg` через канонический script contract.
- Нужно применить изменения после загрузки исходников.

## Usage

```bash
./scripts/platform/update-db.sh --profile env/local.json
./scripts/platform/update-db.sh --profile env/ci.json --run-root /tmp/update-db-run
./scripts/platform/update-db.sh --profile env/local.json --dry-run
./scripts/platform/update-db.sh --profile env/local.json --vendor-cf ./build/vendor.cf --run-root /tmp/update-db-run
```

- `--vendor-cf <file.cf>` обновляет конфигурацию на поддержке из CF поставщика: Designer `/UpdateCfg`, затем
  `/UpdateDBCfg`. ibcmd так не умеет, поэтому флаг работает только с адаптерами `direct-platform` и
  `remote-windows` и требует `--run-root`: туда пишется `designer-out.log`.

## Rules

- Skill не должен становиться отдельным runtime implementation.
- Если нужен новый adapter behavior, меняйте repo script.
