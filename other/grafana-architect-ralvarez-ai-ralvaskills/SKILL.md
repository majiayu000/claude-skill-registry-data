---
name: grafana-architect
version: 1.0.0
description: Grafana dashboards + alerts — dashboards-as-code (Grizzly), per-service folders, one-question-per-panel, unified alerting with runbooks, low-cardinality discipline. Use when designing dashboards, writing alert rules, or auditing.
---

# Grafana Architecture — Signal Consumption

How an operator *uses* what [observability-architect](../observability-architect/SKILL.md) emits. Dashboards, alerts, data sources, exploration. **Dashboards-as-code via Grizzly** is the default; the Grafana UI is for exploration, not authoring. Layouts, panel reference, and alert YAML in [RECIPES.md](RECIPES.md).

## 1. Dashboards-as-code workflow

Dashboards live in the application repo (or a sibling `observability/` repo), versioned in git, applied via [Grizzly](https://grafana.github.io/grizzly/) (`grr`). Repo layout in [RECIPES § 1](RECIPES.md#1-observability-repo-layout).

- **Sync on merge to main** — staging on every push, prod on tagged releases. Dashboards drift only via reviewed PRs.
- **Never edit in the UI for production dashboards.** Grizzly refuses to apply on drift; resolve by pulling the change into JSON.
- **Exploration is different.** Build in the UI; once it earns a home, export and commit.

## 2. Folder organization — per service

One folder per service. Operators on call find dashboards by what they own, not by which team made them (teams reshuffle; services don't). Folder structure example in [RECIPES § 2](RECIPES.md#2-service-folder-layout).

- **Folder permissions match service ownership.**
- **General / platform dashboards** live in a top-level `Platform` folder owned by SRE.
- **No personal folders for production.**

## 3. Panel design — one question per panel

Every panel answers exactly one question. If the title is "stuff," redesign.

- **Panel title is a question or noun phrase:** `"Request rate (req/s)"`, `"p95 latency by route"`. Not `"Stats"`.
- **Y-axis unit is mandatory** — `seconds`, `bytes`, `req/s`, `percent`. Auto-formatting hides confusion.
- **Time range is consistent across the dashboard** unless the dashboard's purpose is the comparison.
- **Thresholds where they exist.** SLO at 99.9% gets a red line at 99.9%.
- **Legends are bounded.** Templatize the query (`sum by (route)`) to bound it. High natural cardinality → heatmap or top-N.

Panel-type reference (time series / stat / gauge / heatmap / bar / logs / traces / text) in [RECIPES § 3](RECIPES.md#3-panel-type-reference).

## 4. Variables and templating

Variables let one dashboard serve many slices.

- **Standard variables** on every service dashboard: `service`, `environment` (`prod`/`staging`), `region` if multi-region.
- **Variables come from label queries**, not hand-maintained lists: `label_values(up{job="$service"}, environment)`.
- **`All` is dangerous** on high-cardinality metrics — fans out into millions of series. Disable or restrict to a curated regex.
- **Don't split dashboards on a variable.** `Orders Prod` and `Orders Staging` are one dashboard with an `environment` variable.

## 5. Alerting — Grafana unified alerting

Alerts live alongside dashboards in Grizzly. A panel and its alert rule are version-controlled together. Full Grizzly YAML in [RECIPES § 4](RECIPES.md#4-grizzly-alert-rule).

### Alert hygiene

- **Every alert is actionable.** If the response is "I'll look in the morning," it's a dashboard, not an alert.
- **Two-tier severity:** `severity=page` (wakes someone) and `severity=ticket` (queues for next business day). No middle ground.
- **Multi-window, multi-burn-rate for SLOs:** `fast_burn = (2% in 1h)` AND `slow_burn = (5% in 6h)` together. Catches real issues without flapping.
- **`for:` is mandatory.** Minimum `2m` on noisy signals; `5m`+ for slow burns.
- **Annotations include a `runbook_url`.** First thing on-call clicks; if it doesn't exist, the alert is half-built.
- **Group related alerts** under labels (`team`, `service`) so silencing can target a service.

### Alerts NOT to write

- **CPU > 80%.** Useless without context. Use saturation (run queue, GC) or RED (latency/errors) instead.
- **"Disk full" without `for:`** — needs `for: 15m` so log rotation spikes don't page.
- **Per-instance alerts on horizontally scaled services.** Fleet-level signal; one bad pod isn't a page.
- **Static thresholds on metrics that grow with traffic.** Use rate-of-change or anomaly instead.

## 6. Data sources

- **Provisioned via Grizzly**, not the UI. Datasource `.yaml` lives next to dashboards.
- **One data source per signal type per environment:** `prometheus-prod`, `prometheus-staging`, `loki-prod`, `tempo-prod`.
- **Service account API keys**, not personal tokens. Rotate quarterly.
- **Read-only data sources for dashboards.** Write access (Alertmanager mute rules, etc.) goes through dedicated service accounts with audit logging.

## 7. Permissions

- **Editor at the folder level.** A service team gets `Editor` on `Orders/`; everyone else has `Viewer`.
- **Admin sparingly.** Two or three admins per Grafana instance.
- **`Anonymous` access off** in any environment with non-public data — including staging.
- **SSO (SAML/OIDC) for humans**, service accounts for automation. No shared passwords.

## 8. Common pitfalls

Sprawl, unactionable alerts, raw-label dashboards, unit mixups, static thresholds, UI drift, panel overload — full list with diagnostics + fixes in [RECIPES § 5](RECIPES.md#5-common-pitfalls).

## 9. SLO dashboards — the special case

Every service has exactly one **SLO dashboard** showing:

- **Current SLO compliance** — percentage over the rolling window (last 30 days).
- **Error budget remaining** — `(SLO_target - current_failure_rate) * total_requests` as a budget number.
- **Burn rate** — instantaneous burn rate, with fast/slow window thresholds visible as red lines.
- **Top contributors** — table of endpoints/operations driving the failure rate.

This dashboard is the single source of truth during an incident. Link to it from the runbook, the page, and the post-incident review.

## 10. Cross-skill ties

- [observability-architect](../observability-architect/SKILL.md) — produces what Grafana consumes. Naming and cardinality discipline established there must hold for queries here to work.
- [docker-architect §10](../docker-architect/SKILL.md#10-vulnerability-scanning--trivy) — Trivy scan results can be dashboards too (security metric over time).
- [rest-api-architect](../../protocols/rest-api-architect/SKILL.md) — SLO burn rate alerts reference REST status codes (`5xx` → error budget) and latency.
- [improve-codebase-architecture](../../refactoring/improve-codebase-architecture/SKILL.md) — friction visible in dashboards is input to architecture review.
- [grpc-architect §2](../../protocols/grpc-architect/SKILL.md) — gRPC status codes feed equivalent metrics; same SLO mechanics apply.
