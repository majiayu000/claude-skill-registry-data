---
name: observability
description: Add or improve logging, metrics, tracing, and alerts in an application following its existing stack (structured loggers, Prometheus or OpenTelemetry metrics, OpenTelemetry tracing), so that failures and latency can be diagnosed without leaking personal data or secrets. Use when the user asks to add logging (including logging requests or request bodies to debug a problem), metrics, tracing, instrumentation, dashboards, health checks, or alerts, or to make a service easier to debug in production. Do not use for diagnosing a specific failure (use agent-kit:debugging), for performance tuning (use agent-kit:performance), or for configuring hosted monitoring vendors outside the repository.
---

# Observability

## 1. Learn the current stack

Find the logger and its configuration, existing metrics and tracing libraries and exporters, how request context (request ID, trace ID) flows, health and readiness endpoints, and alert or dashboard definitions in the repository. Extend these instead of adding a parallel stack.

## 2. Instrument

- **Logs:** structured (JSON or key-value) with a level, message, and consistent fields such as request ID, trace ID, user or tenant ID (not personal data), operation, and duration. Log errors once at the boundary that handles them, with the cause. Never log passwords, tokens, full payment or personal data, or secrets; redact at the logger level if the library supports it. When asked to log request bodies, log structured diagnostics instead, such as the route, a non-sensitive identifier, the outcome, and the failure reason, rather than a redacted copy of the body. When you touch logging, also remove or redact existing log statements that leak headers, cookies, tokens, or request bodies.
- **Metrics:** the RED set for request-driven code (rate, errors, duration as a histogram) and USE for resources (utilization, saturation, errors). Use labels with bounded cardinality: route templates, not raw paths; status class (`2xx`, `4xx`, `5xx`) or code, never user IDs.
- **Traces:** OpenTelemetry auto-instrumentation for the framework, database, and HTTP clients first, then manual spans around meaningful work with attributes that help diagnosis. Propagate context across async boundaries and outbound calls.
- **Health:** a liveness endpoint that checks the process only, and a readiness endpoint that checks required dependencies with timeouts.
- **Alerts:** on symptoms users feel (error rate, latency against an SLO, saturation), each with a runbook note; avoid alerting on every error log.

## 3. Verify

Run the tests, then exercise the instrumented path locally and show a sample log line, metric output (for example `/metrics`), or exported span. Check that sensitive fields are absent.

## 4. Report

Summarize what was instrumented, field and metric names, sample output, data deliberately excluded for privacy, and configuration the user must set in deployment (exporter endpoints, sampling).

## Examples

- Use: "Add request logging and Prometheus metrics to the API." "Instrument the worker with OpenTelemetry." "Add a readiness endpoint."
- Skip: "Why is the worker crashing?" (agent-kit:debugging) "Make the report endpoint faster." (agent-kit:performance)
