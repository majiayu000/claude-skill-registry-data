---
name: logging-telemetry
description: Configure structured logging and telemetry for the .NET 8 WPF widget host app using Serilog, ETW, and Application Insights. Use when wiring logging sinks, correlation IDs, PII redaction, error reporting, and diagnostics exports.
---

# Logging Telemetry

## Overview

Set up structured logs and telemetry that are safe, correlated, and useful for diagnosing widget issues.

## Constraints

- .NET 8
- Serilog for structured logging
- ETW for local diagnostics
- Application Insights for telemetry

## Definition of done (DoD)

- Serilog configured with file sink (rolling, 7-day retention)
- Correlation IDs present on user-initiated actions
- No PII or secrets in logs (verify before merge)
- Structured properties used instead of string interpolation
- Application Insights wired when connection string available
- Log levels appropriate (Debug for verbose, Warning+ for production noise)

## Workflow

1. Define log levels and categories (UI, sync, data, widgets).
2. Configure Serilog sinks and enrichers.
3. Add correlation IDs per user action or sync cycle.
4. Redact or hash PII before logging.
5. Wire Application Insights for events, traces, and exceptions.

## Guidance

- Do not log secrets or full payloads.
- Prefer structured properties over string interpolation.
- Keep noisy logs at Debug.

## References

- `references/serilog.md` for sink and enricher setup.
- `references/appinsights.md` for telemetry wiring.
- `references/pii-handling.md` for redaction rules.
- `references/correlation.md` for correlation IDs and scopes.
