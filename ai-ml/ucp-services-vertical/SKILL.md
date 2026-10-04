---
name: ucp-services-vertical
description: >
  Designs draft UCP vendor-namespace extensions for service commerce, including
  service capability profiles, scope, pricing, deliverables, acceptance, and
  settlement lifecycle. Use when the user wants to model non-product services
  such as consulting, design, AI-agent labor, or SaaS on-demand transactions.
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
---

# UCP Services Vertical

Use this skill to keep services work separate from shopping onboarding.

## Output

Create a draft package under `store/clients/{client_name}/services-vertical/`:

- `service-profile.json`
- `service-catalog.json`
- `lifecycle.md`
- `vendor-namespace.md`

## Workflow

1. Define the vendor namespace, such as `com.example.services`.
2. Model service offerings with scope, deliverables, pricing, and acceptance.
3. Define lifecycle states: `booked`, `in_progress`, `delivered`, `verified`,
   `settled`, `canceled`.
4. Keep payment authorization separate from service acceptance.
5. Document what would need to graduate from vendor namespace to core UCP.

Read `references/services-model.md` for the draft object model.

## Hard Rules

- Do not mix service capabilities into `dev.ucp.shopping.*`.
- Do not promise official UCP support for services.
- Keep this as vendor-namespace design until the standard accepts a services
  vertical.
