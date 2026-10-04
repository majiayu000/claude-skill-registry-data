---
name: adclaw-host-ai-accounting
description: "Use for AdClaw Host AI quota accounting, hosted key provisioning, limit UX, and secret redaction reviews."
---

# AdClaw Host AI Accounting

## Purpose

Use this skill for AdClaw Host zero-setup onboarding work where paid
Starter/Pro/Business customers receive included Host AI messages and a hosted
Citedy Agent key without entering secrets manually.

The skill focuses on operational truth: quota math, D1 accounting, entitlement
gates, prompt/error UX, Citedy key handoff, and redaction. It does not replace
`cloudflare`, `workers-best-practices`, `stripe-best-practices`,
`architecture-patterns`, or `security-review`; use those together when touching
their domains.

## Trigger Examples

- "implement Host AI quota"
- "audit Workers AI cost model"
- "review included LLM messages per plan"
- "design Citedy auto key provisioning"
- "what happens on the 501st Starter message"
- "check prompt/accounting docs for AdClaw Host AI"
- "make sure LLM/Citedy keys are not leaked"

## Required Reading

Before changing code or docs, read the canonical project doc:

```text
/root/adclaw/CF/docs/goal/host-preactivated-llm-citedy-keys.md
```

When implementation touches Citedy key creation, also read:

```text
/root/saas-blog/docs/sub-project/adclaw/citedy-api-key-handoff.md
```

When implementation touches AdClaw provider/env storage, inspect current code
instead of assuming schema:

```text
/root/AdClaw/src/adclaw/providers/store.py
/root/AdClaw/src/adclaw/envs/store.py
/root/AdClaw/src/adclaw/app/routers/citedy.py
```

## Workflow

1. Establish current facts from repo docs and code.
2. Identify which boundary is being changed: Host Worker, D1 accounting,
   AdClaw sandbox bootstrap, Citedy key service, UI copy, or docs only.
3. Apply the accounting checks in `references/accounting-model.md`.
4. Apply the secret and abuse checks in `references/security-redaction.md`.
5. Apply the UX/prompt checks in `references/quota-ux.md`.
6. If reviewing implementation, use `references/review-checklist.md` as the
   findings checklist.
7. Validate with the smallest safe test. Do not run `saas-blog` Node workloads
   on this VPS unless the current user explicitly overrides the host ban.

## Core Decisions

- Workers AI access stays in the Host Worker through `env.AI`.
- The sandbox receives only a customer-scoped synthetic Host AI token.
- Never put Cloudflare account API tokens or Workers AI account credentials in
  a sandbox, backup, browser response, log, Sentry event, or analytics event.
- Citedy hosted auto-provisioning should create a securely random key for the
  deterministic `adclaw-host` agent record.
- Manual `Get Citedy key` remains fallback and rotation UX, not the normal paid
  hosted onboarding path.
- Host AI remains the managed default/fallback provider even when a customer
  adds their own provider key.
- Enforce both message limits and cost caps.
- Block before calling Workers AI when a quota or entitlement gate fails.
- R2 backups are secret-bearing if they contain `/workspace/working.secret`.

## Default Planning Quotas

Use these only as the current planning baseline. Re-check Cloudflare pricing
before changing production limits or customer-facing promises.

```text
Starter:  300 included Host AI messages, cost cap $1.00/month
Pro:    1,500 included Host AI messages, cost cap $4.50/month
Business: 5,000 included Host AI messages, cost cap $15.00/month
```

Initial model:

```text
@cf/google/gemma-4-26b-a4b-it
```

Pricing baseline:

```text
$0.10 per 1M input tokens
$0.30 per 1M output tokens
```

Formula:

```text
cost_usd = input_tokens / 1_000_000 * 0.10
         + output_tokens / 1_000_000 * 0.30
```

## Output Standard

When producing an audit or implementation plan, include:

- exact files or APIs affected;
- current fact source;
- quota/accounting impact;
- secret boundary impact;
- entitlement/refund/dispute behavior;
- customer-facing limit/error behavior;
- tests or smoke evidence required.

Avoid vague conclusions like "safe" without stating which boundary was checked.
