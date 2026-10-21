---
name: alert-as-code
category: observability
description: Use when the repository keeps its alerting in code, or a person asks for alerts outside TaskTrooper - PrometheusRule YAML, a Cloud Monitoring alert policy in Terraform, a Datadog monitor, each routed to TaskTrooper's alert ingest URL so it opens an incident here
source: prometheus-operator/prometheus-operator, hashicorp/terraform-provider-google, DataDog/terraform-provider-datadog docs (Apache-2.0/MPL-2.0), adapted
---

# Alerts as code

TaskTrooper's own alert rules (`propose_alert_rule`) need nothing in the repository. Use this skill only when the team's alerting lives in code already, or the signal is only readable by the monitoring system itself. The alert must land here as an incident: every rule below notifies TaskTrooper's alert ingest URL, `POST <server>/v1/alerts/ingest/<token>`, which accepts Alertmanager, Sentry, Google Cloud Monitoring and a generic `{title, severity, env, detail, fingerprint, resolved}` JSON. A person creates the token under the repository's alert tokens; it is a secret — it goes in the monitoring system's secret store, never in the repository.

## Prometheus (prometheus-operator)

```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: checkout-api
spec:
  groups:
    - name: checkout-api.golden
      rules:
        - alert: CheckoutApiHighErrorRatio
          expr: |
            sum(rate(http_server_request_duration_seconds_count{service_name="checkout-api",http_response_status_code=~"5.."}[5m]))
              / sum(rate(http_server_request_duration_seconds_count{service_name="checkout-api"}[5m])) > 0.02
          for: 5m
          labels: { severity: high }
          annotations:
            summary: checkout-api error ratio above 2%
```

Alertmanager routes it with a `webhook_configs` receiver whose `url` is the ingest URL (from a secret file: `url_file`), `send_resolved: true` so recovery resolves the incident.

## Google Cloud Monitoring (Terraform)

A `google_monitoring_notification_channel` of `type = "webhook_tokenauth"` with `labels = { url = var.tasktrooper_ingest_url }`, and a `google_monitoring_alert_policy` whose `conditions.condition_threshold` filters the service's metric (`resource.type = "cloud_run_revision" AND resource.labels.service_name = "checkout-api"`), with `duration = "300s"` and `notification_channels` naming that channel. Cloud Monitoring's incident payload is understood as is, opened and closed.

## Datadog

A `datadog_monitor` (`type = "query alert"`, e.g. `query = "sum(last_5m):sum:trace.http.request.errors{service:checkout-api}.as_count() / sum:trace.http.request.hits{service:checkout-api}.as_count() > 0.02"`). Datadog has no payload TaskTrooper parses natively, so use the generic shape through two webhooks (`datadog_webhook`): `tasktrooper` with the payload `{"title": "$EVENT_TITLE", "severity": "high", "env": "prod", "detail": "$EVENT_MSG", "fingerprint": "datadog-$ALERT_ID"}`, and `tasktrooper-resolved` with the same payload plus `"status": "resolved"`. The monitor's message routes each transition: `{{#is_alert}}@webhook-tasktrooper{{/is_alert}}{{#is_recovery}}@webhook-tasktrooper-resolved{{/is_recovery}}`. The shared `fingerprint` is what lets the recovery close the incident the alert opened.

## In the task

One rule per golden signal, thresholds from what the metric reads today (never a copied number), `for` long enough that one bad scrape does not page, and a recovery notification so incidents close themselves. Acceptance criterion: "Given the rule's condition holds in staging (forced with a test), then an incident opens in TaskTrooper for this repository, and it resolves when the condition clears."
