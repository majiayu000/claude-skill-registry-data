---
name: checkout_service_runbook
description: Use when checkout-api health, checkout failures, or a checkout deployment must be diagnosed.
---

# Checkout service runbook

For `checkout-api`, begin with the current error rate and health state. Confirm
which deployment is active, compare the error increase with its deployment
time, and inspect logs for the failing request path and error category. Check
whether failures are broad or limited to a dependency, region, or request type.

The last-known-good version is useful evidence, but its existence does not prove
that rollback is authorized, required, or already complete. Diagnosis should
precede production mutation. Do not tell customers to retry or say checkout is
restored while recovery remains unconfirmed.

A concise checkout triage note should make the present impact clear, avoid an
unsupported root-cause claim, and name the health, deployment, and log evidence
needed for the next decision.
