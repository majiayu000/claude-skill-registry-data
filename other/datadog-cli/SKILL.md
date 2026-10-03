---
name: datadog-cli
description: |
  Datadog CLI for searching logs, querying metrics, and tracing requests.
  Use when user mentions "Datadog", "DD logs", "production debugging",
  "check metrics", "trace request", or needs to investigate production incidents.
  Triggers on "datadog", "DD", "로그 검색", "메트릭 조회", "장애 조사".
---

# Datadog CLI

A CLI tool for AI agents to debug and triage using Datadog logs and metrics.

## Required Reading

**You MUST read the relevant reference docs before using any command:**
- [Log Commands](references/logs-commands.md)
- [Metrics](references/metrics.md)
- [Query Syntax](references/query-syntax.md)
- [Workflows](references/workflows.md)
- [Dashboards](references/dashboards.md)

## Setup (최초 1회)

이 스킬은 `config.json`에 설정이 필요합니다.

1. `config.json`을 읽는다 (`skills/datadog-cli/config.json` 또는 현재 CLI의 글로벌 스킬 경로)
2. 빈 필드가 있으면 현재 CLI의 질문 방식으로 사용자에게 질문한다
3. 답변을 `config.json`에 저장한다
4. 이후 실행 시에는 `config.json`에서 자동으로 읽는다

| 항목 | 설명 | 예시 |
|------|------|------|
| `dd_site` | Datadog 사이트 도메인 | `datadoghq.com` / `datadoghq.eu` |
| `default_service` | 기본 서비스명 (쿼리 자동완성에 사용) | `api-server` |
| `default_env` | 기본 환경 | `production` / `staging` |
| `log_index` | 기본 로그 인덱스 | `main` |

**Setup 로직:**

```
config.json 읽기
  ├─ dd_site가 기본값(datadoghq.com)이면 → "Datadog 사이트를 확인해주세요 (EU 사용자: datadoghq.eu, 맞으면 Enter)"
  ├─ default_service 비어있음? → "주로 조회할 서비스명을 입력해주세요 (예: api-server, 건너뛰려면 Enter)"
  ├─ default_env 비어있음? → "기본 환경을 입력해주세요 (예: production, staging)"
  └─ 답변 수집 후 config.json에 저장 → 이후 자동 사용
```

> **모든 필드가 채워져 있으면 이 단계를 건너뜁니다.**
> `config.json`의 `dd_site` 값은 `--site` 플래그로 자동 주입됩니다.

---

## Setup

### Environment Variables (Required)

```bash
export DD_API_KEY="your-api-key"
export DD_APP_KEY="your-app-key"
```

Get keys from: https://app.datadoghq.com/organization-settings/api-keys

### Running the CLI

```bash
npx @leoflores/datadog-cli <command>
```

For non-US Datadog sites, use `--site` flag:
```bash
npx @leoflores/datadog-cli logs search --query "*" --site datadoghq.eu
```

## Commands Overview

| Command | Description |
|---------|-------------|
| `logs search` | Search logs with filters |
| `logs tail` | Stream logs in real-time |
| `logs trace` | Find logs for a distributed trace |
| `logs context` | Get logs before/after a timestamp |
| `logs patterns` | Group similar log messages |
| `logs compare` | Compare log counts between periods |
| `logs multi` | Run multiple queries in parallel |
| `logs agg` | Aggregate logs by facet |
| `metrics query` | Query timeseries metrics |
| `errors` | Quick error summary by service/type |
| `services` | List services with log activity |
| `dashboards` | Manage dashboards (CRUD) |
| `dashboard-lists` | Manage dashboard lists |


## Quick Examples

### Search Errors
```bash
npx @leoflores/datadog-cli logs search --query "status:error" --from 1h --pretty
```

### Tail Logs (Real-time)
```bash
npx @leoflores/datadog-cli logs tail --query "service:api status:error" --pretty
```

### Error Summary
```bash
npx @leoflores/datadog-cli errors --from 1h --pretty
```

### Trace Correlation
```bash
npx @leoflores/datadog-cli logs trace --id "abc123def456" --pretty
```

### Query Metrics
```bash
npx @leoflores/datadog-cli metrics query --query "avg:system.cpu.user{*}" --from 1h --pretty
```

### Compare Periods
```bash
npx @leoflores/datadog-cli logs compare --query "status:error" --period 1h --pretty
```

## Global Flags

| Flag | Description |
|------|-------------|
| `--pretty` | Human-readable output with colors |
| `--output <file>` | Export results to JSON file |
| `--site <site>` | Datadog site (e.g., `datadoghq.eu`) |

## Time Formats

- **Relative**: `30m`, `1h`, `6h`, `24h`, `7d`
- **ISO 8601**: `2024-01-15T10:30:00Z`

## Incident Triage Workflow

```bash
# 1. Quick error overview
npx @leoflores/datadog-cli errors --from 1h --pretty

# 2. Is this new? Compare to previous period
npx @leoflores/datadog-cli logs compare --query "status:error" --period 1h --pretty

# 3. Find error patterns
npx @leoflores/datadog-cli logs patterns --query "status:error" --from 1h --pretty

# 4. Narrow down by service
npx @leoflores/datadog-cli logs search --query "status:error service:api" --from 1h --pretty

# 5. Get context around a timestamp
npx @leoflores/datadog-cli logs context --timestamp "2024-01-15T10:30:00Z" --service api --pretty

# 6. Follow the distributed trace
npx @leoflores/datadog-cli logs trace --id "TRACE_ID" --pretty
```

See [workflows.md](references/workflows.md) for more debugging workflows.
