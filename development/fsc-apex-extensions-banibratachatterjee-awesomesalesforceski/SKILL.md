---
name: fsc-apex-extensions
description: "Use this skill when extending Financial Services Cloud (FSC) behavior through Apex: customizing financial rollup recalculation, disabling built-in FSC triggers to write custom trigger logic, implementing Compliant Data Sharing (CDS) participant/role integrations, or building custom FSC action handlers. NOT for standard Apex unrelated to the FSC managed package, standard Salesforce sharing rules, or configuring FSC rollups through the Admin UI — use the admin/financial-account-setup skill for declarative rollup setup."
category: apex
salesforce-version: "Spring '25+"
well-architected-pillars:
  - Security
  - Reliability
  - Performance
tags:
  - fsc
  - financial-services-cloud
  - apex
  - rollup-customization
  - compliant-data-sharing
  - trigger-management
  - finserv-namespace
inputs:
  - FSC managed package version installed in the org (check via Setup > Installed Packages)
  - Whether the org uses FinServ__ namespace or the newer platform-native FSC data model
  - Confirmation of which FSC trigger settings are currently enabled (FinServ__TriggerSettings__c)
  - Rollup recalculation batch schedule and whether bulk data loads are involved
  - Compliant Data Sharing configuration — participant types, role assignments, sharing set definitions
outputs:
  - Apex trigger class that coexists safely with FSC built-in triggers
  - Rollup recalculation invocation code for post-bulk-load scenarios
  - CDS-aware sharing logic that respects the participant/role model
  - FinServ__TriggerSettings__c management code for enabling/disabling FSC triggers per-transaction
triggers:
  - "FSC rollup not recalculating after bulk data load"
  - "custom Apex trigger conflicts with FSC built-in trigger logic"
  - "compliant data sharing participant record not granting access"
  - "FinServ__TriggerSettings__c needs to be disabled for integration user"
  - "calling FSC managed package Apex from custom code causes type errors"
dependencies: []
version: 1.0.0
author: Pranav Nagrecha
updated: 2026-04-11
---

# FSC Apex Extensions

Use this skill when you need to write Apex that extends or integrates with Financial Services Cloud managed-package behavior: custom triggers that coexist with FSC's built-in trigger framework, post-bulk-load rollup recalculation invocations, or Compliant Data Sharing integrations that must use the CDS participant/role model rather than standard Apex sharing.

---

## Before Starting

Gather this context before working on anything in this domain:

- Confirm the FSC package namespace in use: `FinServ__` (managed-package) or the newer platform-native FSC objects. Nearly all production orgs installed before Winter '23 use the managed-package model and you must use the `FinServ__` prefix for all sObjects and fields.
- Check which FSC triggers are currently active by querying `FinServ__TriggerSettings__c`. Each FSC trigger domain (FinancialAccount, AccountAccountRelation, Lead, etc.) has a separate custom setting record; disabling the wrong one causes silent data integrity failures.
- Understand whether the deployment involves bulk data loads. FSC rollups do **not** auto-fire on DML inserts at bulk scale — the `FinServ.RollupRecalculationBatchable` class must be invoked explicitly after loads.
- If Compliant Data Sharing is enabled, map the participant types and sharing roles before writing any Apex. Manual `AccountShare` or `FinancialAccountShare` records inserted outside the CDS participant model will be silently reverted on the next CDS recalculation pass.
- Verify the FSC managed package API version. Managed package classes are frozen at their own API version; calling them from max-version Apex can cause type incompatibilities with newer platform types.

---

## Core Concepts

### FSC Trigger Management via FinServ__TriggerSettings__c

FSC ships with its own Apex trigger framework. Every FSC-owned trigger checks the `FinServ__TriggerSettings__c` hierarchy custom setting before executing. If your custom trigger and the FSC trigger both fire on the same object/event, both execute — which causes duplicate processing (e.g., double rollup increments, double notification events).

The correct pattern is to disable the specific FSC trigger for the duration of your custom logic. To disable Account-level FSC triggers:

```apex
FinServ__TriggerSettings__c ts = FinServ__TriggerSettings__c.getInstance();
ts.FinServ__AccountTrigger__c = false;
upsert ts;
// ... your DML
ts.FinServ__AccountTrigger__c = true;
upsert ts;
```

This pattern must be wrapped in a try/finally block to prevent the setting remaining false if an exception occurs. Because the custom setting is org-wide hierarchy type, test classes must also set it up explicitly — do not rely on default values in tests.

### Rollup Recalculation is Not Event-Driven at Bulk Scale

FSC financial rollups aggregate values across household members, joint owners, and group relationships. The rollup engine is designed to fire from transactional DML inside Apex triggers. At bulk scale — Data Loader, Bulk API, or any batch that bypasses the standard trigger invocation threshold — FSC rollups do not self-correct. After any bulk insert or update of `FinServ__FinancialAccount__c`, `FinServ__FinancialAccountTransaction__c`, or related objects, you must invoke:

```apex
Database.executeBatch(new FinServ.RollupRecalculationBatchable(), 200);
```

This batchable recalculates all pending rollup summaries. The batch size of 200 is the Salesforce-recommended value for avoiding CPU limit violations on complex household graphs. Scheduling this batch immediately after any bulk load is a production requirement, not an optional optimization.

### Compliant Data Sharing Cannot Be Overridden with Standard Apex Sharing

When FSC Compliant Data Sharing (CDS) is enabled on an object, the CDS engine owns the share records. Any `AccountShare`, `FinancialAccountShare`, or related share object records you insert manually in Apex — including those inserted by standard Apex managed sharing — will be silently removed the next time the CDS recalculation job runs.

To share a record under CDS, you must insert a `FinServ__ShareParticipant__c` record (or the equivalent native object) that registers the participant relationship. CDS then generates the share records automatically based on the participant's assigned sharing role. The `RowCause` on CDS-generated shares is `CompliantDataSharing` — do not attempt to create records with this RowCause manually; the system sets it.

### Managed Package API Version Lock

The FSC managed package compiles its Apex at the API version current at the time of the package's release. When the org's Apex version moves ahead of the package's compiled version, type resolution for platform-provided types (custom metadata types, new sObject subtypes, newer Apex system classes) can diverge. The practical impact: if your custom Apex calls FSC managed package classes and passes newly introduced types, you may receive runtime `TypeException` or method-not-found errors that do not appear in sandbox at the same version. Always test FSC Apex extensions in a full-copy sandbox that mirrors the production FSC package version before deploying.

---

## Common Patterns

### Pattern: Safe Trigger Co-Existence with FSC Built-Ins

**When to use:** You need to add custom business logic to the same object event already handled by an FSC trigger (e.g., before-update on `FinServ__FinancialAccount__c`).

**How it works:**
1. Create a custom trigger that fires on the target object/event.
2. At the start of the trigger handler, read `FinServ__TriggerSettings__c` and selectively disable the relevant FSC trigger flag.
3. Execute your logic.
4. In a `finally` block, re-enable the FSC trigger flag.
5. Allow FSC rollup recalculation to run post-transaction (it will fire naturally for transactional DML, or batch for bulk DML).

**Why not the alternative:** Simply adding a trigger without disabling the FSC built-in causes both triggers to run for the same records. On Financial Account updates, this results in double rollup increments, which produces incorrect household balance totals that are difficult to detect without dedicated rollup validation tests.

### Pattern: Post-Bulk-Load Rollup Reset

**When to use:** A migration, integration, or scheduled batch performs large-volume DML on FSC financial objects outside the normal transactional trigger path.

**How it works:**
1. Complete the bulk DML (Data Loader, Bulk API, or custom batch).
2. In a separate Apex job (Queueable or scheduled Batch), invoke `Database.executeBatch(new FinServ.RollupRecalculationBatchable(), 200)`.
3. Optionally chain a validation query to spot-check household totals post-recalculation.

**Why not the alternative:** Relying on the scheduled nightly rollup batch leaves household totals stale for hours. Financial advisors querying household net worth immediately after a migration will see incorrect values, which in regulated environments constitutes a compliance risk.

---

## Decision Guidance

| Situation | Recommended Approach | Reason |
|---|---|---|
| Custom logic on the same object/event as an FSC trigger | Disable FSC trigger via `FinServ__TriggerSettings__c`, run custom logic, re-enable in finally | Prevents double processing without removing FSC trigger permanently |
| Sharing a Financial Account with a new participant | Insert `FinServ__ShareParticipant__c` record via CDS model | Direct share record inserts are silently reverted by CDS recalculation |
| Bulk data load of FinancialAccount or related objects | Invoke `FinServ.RollupRecalculationBatchable` after load | FSC rollups do not auto-fire reliably at bulk scale |
| Calling FSC managed Apex from org Apex at newer API version | Test in full-copy sandbox; avoid passing newer platform types to managed methods | Managed package is locked to an older API version; type mismatches cause runtime errors |
| Rollup recalculation taking too long post-load | Reduce batch size below 200, or use FSC Admin UI batch trigger for selective recalculation | Complex household graphs approach CPU limits at 200 batch size in some orgs |

---

## Recommended Workflow

Step-by-step instructions for an AI agent or practitioner working on this task:

1. **Assess trigger landscape** — Query `FinServ__TriggerSettings__c` and list which FSC trigger flags are currently enabled. Cross-reference with the objects your custom Apex will touch to identify all overlap points.
2. **Draft trigger handler with FSC trigger guard** — Write the custom Apex trigger handler. Add a try/finally block that disables the relevant `FinServ__TriggerSettings__c` flags before DML and re-enables them in the finally clause. Never leave FSC triggers permanently disabled.
3. **Add rollup recalculation hook** — If the trigger handles bulk DML paths (context `isBulk` or batch size > 50), enqueue a `FinServ.RollupRecalculationBatchable` call after DML rather than relying on transactional rollup firing.
4. **Handle CDS participation** — If the feature requires sharing records with non-owner users, insert `FinServ__ShareParticipant__c` records using the correct `FinServ__ShareRole__c` value. Never insert share records directly on CDS-governed objects.
5. **Write test classes with FSC setting setup** — Test classes must explicitly configure `FinServ__TriggerSettings__c` for the running user context. Do not assume org defaults persist in test execution. Use `@TestSetup` to initialize the custom setting.
6. **Validate in full-copy sandbox** — Deploy to a sandbox whose FSC package version matches production. Run the `check_fsc_apex_extensions.py` script against the deployed metadata to check for common misconfigurations.
7. **Confirm rollup totals post-deployment** — After go-live of any bulk-load-adjacent feature, manually verify household total fields on a sample of affected accounts to confirm rollup recalculation completed correctly.

---

## Review Checklist

Run through these before marking work in this area complete:

- [ ] `FinServ__TriggerSettings__c` disabled/re-enabled in a try/finally block — no permanent disablement
- [ ] `FinServ.RollupRecalculationBatchable` invoked after any bulk-path DML on FSC financial objects
- [ ] All sharing logic uses `FinServ__ShareParticipant__c` inserts — no direct share record DML on CDS-governed objects
- [ ] Test classes set up `FinServ__TriggerSettings__c` explicitly; not relying on org defaults in test context
- [ ] Code tested in a sandbox whose FSC package version matches production (not a Developer Edition with a different version)
- [ ] No usage of FSC managed package methods that receive newer platform types introduced after the package's compiled API version

---

## Salesforce-Specific Gotchas

Non-obvious platform behaviors that cause real production problems:

1. **FSC Rollups Silent on Bulk Insert** — FSC rollup recalculation does not fire reliably when records are inserted via Bulk API or Data Loader at batch sizes beyond what triggers can handle. Household totals remain stale until `FinServ.RollupRecalculationBatchable` is run. The failure is silent — no error is thrown, rollup fields simply do not update.
2. **CDS Silently Reverts Manual Share Records** — Any share record (AccountShare, FinancialAccountShare) inserted manually through Apex on a CDS-governed object will be deleted the next time the CDS recalculation job runs. There is no error; the record simply disappears. The only durable sharing mechanism is the `FinServ__ShareParticipant__c` participant model.
3. **Managed Package API Version Lock Causes Runtime TypeException** — The FSC managed package Apex compiles against the API version active at the time of that package version's release. If org Apex at a newer API version passes a type introduced after that API version to a managed package method, a `System.TypeException` is thrown at runtime that does not surface during compilation or deploy-time validation.

---

## Output Artifacts

| Artifact | Description |
|---|---|
| FSC-safe Apex trigger | Custom trigger handler with `FinServ__TriggerSettings__c` guard pattern |
| Rollup recalculation invocation | Apex code to explicitly invoke `FinServ.RollupRecalculationBatchable` after bulk loads |
| CDS participant insertion snippet | Apex code to register sharing via `FinServ__ShareParticipant__c` |

---

## Related Skills

- admin/financial-account-setup — declarative setup of FSC rollup configuration, without Apex; use when rollup behavior needs to be changed through admin settings rather than code
- admin/household-model-configuration — FSC household and group model setup; relevant context when Apex extensions touch household aggregation logic
