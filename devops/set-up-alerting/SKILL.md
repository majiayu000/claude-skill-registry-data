---
name: set-up-alerting
description: Use when a service needs alerts — symptoms users feel, severity P0–P3 with routing, per-environment thresholds, a runbook and owner on every rule; SigNoz is the default (Grafana, Azure Monitor, CloudWatch tracks) and alerts are code promoted with the service through the same pipeline.
---

# Set Up Alerting

An alert rule is code: one rule set per environment, applied by the pipeline that applies the
service, promoted by the promotion that promotes the service. Signals, resource attributes, SLO
burn-rate: [observability](../../core/_shared/observability.md); log fields:
[logging-contract](../../core/_shared/logging-contract.md); telemetry path:
[deploy-otel-collector](../../infra/deploy-otel-collector/SKILL.md); the why:
[alerting-patterns.md](./alerting-patterns.md).

## 1. Audit current state (change nothing)

```bash
cat .claude/stack-profile.md 2>/dev/null   # observability.backend, observability.otel, iac, ci
ls alerts/ 2>/dev/null; ls terraform/alerts.tf 2>/dev/null
grep -rn --include='*.tf' -iE 'signoz|grafana|monitor_metric_alert|monitor_scheduled_query|cloudwatch_metric_alarm' . | head
grep -rn --include='*.tfvars' -iE 'alert|threshold' terraform/envs/ 2>/dev/null
gh workflow list 2>/dev/null               # an observability workflow beside the infra pipeline?
```

Then list the rules in the backend itself (read-only API or UI): name, query, threshold, window,
route, runbook, owner. Rules that exist only in the UI are unmanaged drift; record them for step 2.

## 2. Decide what to do

- No rules in code or backend → full setup (steps 3 to 7).
- Rules only in the backend UI → codify: write the catalogue from what the API returns, import the
  rules into state or recreate them — one of the two, never both.
- Rules in code, but a separate observability workflow applies them only from `main` → move them
  into the same per-environment pipeline (step 6).
- Catalogue, code, per-env pipeline and read-back all present → "already in place"; run step 7 only.

## 3. Detect the track

| `observability.backend` | Rules | As code |
|---|---|---|
| `signoz` (default) | alert rules, notification channels | Terraform provider `SigNoz/signoz` — *unverified*: source address and current version must be re-verified on registry.terraform.io — or the SigNoz REST API |
| `grafana` | rule groups, contact points | `grafana` provider (`grafana_rule`, `grafana_contact_point`) — *unverified*, same registry check |
| Azure Monitor | metric alerts, log alerts | `azurerm` provider: `azurerm_monitor_metric_alert`, `azurerm_monitor_scheduled_query_rules_alert` |
| CloudWatch | metric alarms, composite alarms | `aws` provider: `aws_cloudwatch_metric_alarm`; log-based alerts via metric filters |

The backend is an exporter setting ([observability](../../core/_shared/observability.md)); if the
profile names none, ask. Queries below use SigNoz/OTel names; other tracks translate.

## 4. Install only what is missing

- The Terraform toolchain is already there ([set-up-opentofu](../../infra/set-up-opentofu/SKILL.md));
  the alerts root adds one provider, pinned and locked like the others.
- One SigNoz API key per environment, as a CI environment secret
  ([manage-secrets](../../infra/manage-secrets/SKILL.md)); never in tfvars.
- Notification channels (Slack, Teams, email, webhook) need webhook URLs. A provider-managed channel
  writes the URL into state: one dedicated, revocable webhook per channel, rotated — or channels by
  hand, referenced by id.

## 5. Generate

**The alert catalogue first** — `alerts/catalogue.md` in the target repo, or the same table as
Terraform locals: the single source the rules are generated from, the artifact the monthly noise
review reads. Name format `[P<n>][<env>] <service> — <symptom>`:

| Name | Query | Threshold (dev/stg/prd) | Window | Route | Runbook | Owner |
|---|---|---|---|---|---|---|
| `[P0][<env>] <service> — fatal log lines` | `level = 'fatal'` on the service's logs | any / any / any | 5 m | page | `<runbook-url>` | `<owner>` |
| `[P1][<env>] <service> — error rate` | 5xx ratio from `http.server.request.duration` | 5% / 1% / 0.5% | 10 m | chat channel | `<runbook-url>` | `<owner>` |
| `[P1][<env>] <service> — latency burn` | SLO burn rate, two windows ([observability](../../core/_shared/observability.md)) | 14.4× over 1 h, 6× over 6 h | 1 h + 6 h | chat channel | `<runbook-url>` | `<owner>` |
| `[P2][<env>] <service> — job failed` | `event = 'job.failed'` | ≥ 1 / ≥ 1 / ≥ 1 | 15 m | ticket | `<runbook-url>` | `<owner>` |
| `[P2][<env>] <service> — queue age` | oldest message age | 10 m / 5 m / 2 m | 5 m | ticket | `<runbook-url>` | `<owner>` |
| `[P1][<env>] <service> — heartbeat missing` | count of `event = 'job.completed'` | < 1 in 25 h | 25 h | chat channel | `<runbook-url>` | `<owner>` |

**Per-environment thresholds via tfvars** — one `number` variable per threshold, one value per
environment file:

```dotenv
# terraform/envs/dev.tfvars
alert_error_rate_threshold = 0.05   # stg 0.01, prd 0.005 — one file per env
```

**The rules.** Every HCL snippet below is *unverified* — written from the provider's documented
shape, never run; confirm source, version and attribute names on registry.terraform.io first.

```hcl
# terraform/alerts.tf — provider block once per root (*unverified*)
terraform {
  required_providers {
    signoz = { # *unverified* — re-verify source address and version on registry.terraform.io
      source = "SigNoz/signoz", version = "0.x.y" # placeholder — pin the current registry version
    }
  }
}

provider "signoz" {
  api_url = "https://<signoz-host>" # self-hosted host, or the SigNoz Cloud URL of <org>
  api_key = var.signoz_api_key      # CI environment secret for this env
}

locals {
  # the value the exporter writes — a query that spells it differently never matches
  env_attr = { dev = "development", stg = "staging", prd = "production" }[var.env]
}
```

Log-based alert:

```hcl
resource "signoz_alert" "fatal_log" { # *unverified* resource and attribute names
  name        = "[P0][${var.env}] ${var.service} — fatal log lines"
  description = "Any fatal line in the service logs. Runbook <runbook-url>, owner <owner>."
  rule_type   = "log"
  query       = "level = 'fatal' AND service.name = '${var.service}' AND deployment.environment.name = '${local.env_attr}'"
  labels      = { severity = "P0", service = var.service, env = var.env }
}
```

Metric / error-rate alert:

```hcl
resource "signoz_alert" "error_rate" { # *unverified*
  name        = "[P1][${var.env}] ${var.service} — error rate"
  description = "Failed-request ratio above the env threshold. Runbook <runbook-url>, owner <owner>."
  rule_type   = "metric"
  query       = "sum(rate(http_server_request_duration_count{status_code=~'5..'}[10m])) / sum(rate(http_server_request_duration_count[10m]))" # shape only — *unverified*
  threshold   = var.alert_error_rate_threshold
  labels      = { severity = "P1", service = var.service, env = var.env }
}
```

Heartbeat / absence alert (cron jobs, pipelines):

```hcl
resource "signoz_alert" "heartbeat" { # *unverified*
  name        = "[P1][${var.env}] <service> — heartbeat missing"
  description = "No job.completed event in 25 h. Runbook <runbook-url>, owner <owner>."
  rule_type   = "log"
  query       = "event = 'job.completed' AND service.name = '${var.service}' AND deployment.environment.name = '${local.env_attr}'"
  threshold   = 1 # fires when the count in the window is below this
  window      = "25h" # job period plus slack
  labels      = { severity = "P1", service = var.service, env = var.env }
}
```

Notification channel:

```hcl
resource "signoz_notification_channel" "oncall_chat" { # *unverified*
  name = "<team>-oncall-chat"
  type = "slack" # slack | msteams | email | webhook
  # endpoint or recipients per the provider docs; webhook URL handling per step 4
}
```

## 6. Wire

- **Same pipeline, same promotion.** The alert resources live in the same Terraform root per
  environment as everything else: every rule reaches `dev` with its PR, `stg` only after
  `promote-stg`, `prd` only after `promote-prd`
  ([set-up-terraform-pipeline](../../infra/set-up-terraform-pipeline/SKILL.md),
  [branch-promotion](../../core/_shared/branch-promotion.md)). An observability workflow that
  applies only from `main` never reaches stg — the failure mode this wiring prevents.
- **Post-apply read-back.** After every apply, list the rules through the API and assert each
  catalogue name exists exactly once and every channel reference resolves (commands in step 7).

## 7. Verify

```bash
# read-back — *unverified* endpoint; confirm the path in the SigNoz API docs
curl -fsS -H "Authorization: Bearer $SIGNOZ_API_KEY" "https://<signoz-host>/api/v1/rules" > rules.json
jq -r '.data[].name' rules.json | sort | uniq -d          # expect: no output — nothing exists twice
jq -r '.data[].name' rules.json | grep -cxF '[P0][dev] <service> — fatal log lines'   # expect: 1
```

- **Test-fire every new alert in dev** before it promotes further: trigger one real matching event
  (a request that returns 500, one forced `fatal` log line, skip one heartbeat emission), then check
  the route: **one card, once, on the right channel** — not zero (query or route broken), not two
  (duplicate routes). Resolve it and confirm it clears; an alert that cannot be cleared in dev
  cannot be cleared in prd at 03:00.

## References

- [alerting-patterns.md](./alerting-patterns.md): symptom choice, severity routing, per-env thresholds,
  the stuck-gauge and negative-filter traps, heartbeats, CI/CD health, noise review.
- Signals, SLOs, burn-rate windows: [observability](../../core/_shared/observability.md); log fields:
  [logging-contract](../../core/_shared/logging-contract.md); telemetry path:
  [deploy-otel-collector](../../infra/deploy-otel-collector/SKILL.md).
- The pipeline alerts ride on: [set-up-terraform-pipeline](../../infra/set-up-terraform-pipeline/SKILL.md),
  [branch-promotion](../../core/_shared/branch-promotion.md).
