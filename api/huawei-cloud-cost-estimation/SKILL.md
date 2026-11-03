---
name: huawei-cloud-cost-estimation
description: >-
  Estimate Huawei Cloud pre-order costs, provision allowlisted resources through
  hcloud, and guide unsubscribe requests through the console. Use for Huawei Cloud
  pricing, budgets, resource creation, unsubscribe guidance, or hcloud readiness checks.
compatibility:
  hcloud KooCLI 7.2+, matching IAM permissions, and outbound network; the agent does not install
  dependencies
metadata:
  language: en
  translation_of: huawei-cloud-cost-estimation-cn
  author: concept-git
  version: "3.3.0"
  openclaw:
    requires:
      bins: [hcloud]
    primaryEnv: HUAWEICLOUD_SDK_AK
    homepage: https://github.com/concept-git/cloud-concept-skills/tree/main/skills/en/huawei-cloud-cost-estimation
    envVars:
      - { name: HUAWEICLOUD_SDK_AK, required: false }
      - { name: HUAWEICLOUD_SDK_SK, required: false }
      - { name: HUAWEICLOUD_SDK_REGION, required: false }
---

# Huawei Cloud Quotes and Provisioning

Community-maintained, not an official Huawei Cloud skill. Use current API evidence and command help.

## Read by task

Before deciding or calling hcloud, read the matching categories in `references/gotchas.md`. Paths below are relative to `references/`; read relevant sections and reuse prior reads.

| Task | Read | Gotchas |
| --- | --- | --- |
| Check hcloud | `cli-installation.md` | A |
| Quote/compare | `pricing/commands.md` | A, B |
| Check compatibility | `lifecycle/concepts.md`: relevant checks | A, C |
| Check existing orders/errors | Current help for the relevant read-only API | A, D |
| Prepare login | `lifecycle/concepts.md`: login selection | E |
| Prepare provisioning | `lifecycle/concepts.md`; selected operation, dependencies and payment fields in `lifecycle/commands.md` | A–D; add E for credentials |
| Unsubscribe/stop | `lifecycle/concepts.md`: unsubscribe section, console guidance only | — |

For provisioning, read pricing files only for unresolved or changed quotes. Route bills/balances to the read-only billing skill or Cost Center; other clouds and non-allowlisted writes to their consoles.

## Quote

1. Establish service, region, configuration, quantity, billing mode and period/usage. Ask missing decision-relevant inputs together. When delegated, choose for the user's budget and purpose. Disclose Linux/empty-AZ/NA assumptions for quotes; obtain billing mode and duration from the user.
2. Resolve the candidate and product billing mapping using the pricing contract. Submit only lines eligible under G03–G06; retain their configuration, source, exact request and matched response.
3. Itemize verified prices and missing items, reconcile totals/currency and state the query date. Reuse the same evidence and line states in exported quotes; this is not a final bill.

## Provision

1. Find the operation in the allowlist and read its current help. Verify dependencies through read-only calls; classify each as supported, incompatible, or unresolved with evidence.
2. Quote the complete configuration and associated costs. For an unverified cost, disclose that charges may apply and obtain separate consent; known incompatibility remains blocking.
3. Build the final request with explicit payment, renewal and login choices. Inspect conditional fields and run global `--dryrun`, following G09/G12. Keep the checked request revision with its evidence.
4. Show the configuration, cost and execution order; associate confirmation with that request. Execute it separately with only global `--dryrun` removed. Follow G09–G11 for edits or failures.
5. Query order/payment and resource outcomes. Report verified results and unresolved items, retaining their IDs with the checked request and confirmation.

## Communication and lookup

Match the user's language; give the conclusion, evidence and next step plainly. Complete clear read-only work without repeated permission requests. Ask only for missing decisions and purchase confirmation; report progress on long tasks.

- Permission failure: `references/iam-policies.md`.
- Field relationships unclear: `references/pricing/rfq-models/rfq-core.yml` and only the relevant billing-mode model.
