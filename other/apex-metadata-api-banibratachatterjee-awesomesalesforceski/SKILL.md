---
name: apex-metadata-api
description: "Use when Apex code must create or update metadata programmatically at runtime — custom fields, objects, picklist values, labels, or other supported types — using the Metadata namespace (Metadata.Operations, Metadata.DeployCallback). Triggers: 'Metadata.Operations', 'Metadata.CustomField from Apex', 'deploy metadata from Apex', 'enqueueDeployment', 'create a custom field programmatically', 'post-install script metadata setup'. NOT for Metadata API REST/SOAP (use metadata-api-and-package-xml) and NOT for reading Custom Metadata Type configuration rows in Apex (use custom-metadata-in-apex)."
category: apex
salesforce-version: "Spring '25+"
well-architected-pillars:
  - Operational Excellence
  - Scalability
triggers:
  - "create a custom field programmatically from Apex"
  - "deploy metadata changes from Apex code at runtime"
  - "use Metadata.Operations to add picklist values dynamically"
  - "how do I use enqueueDeployment in Apex to create a custom object"
  - "post-install script that adds a required field to a subscriber org"
  - "Apex callback after metadata deployment finishes"
  - "ISV managed package creates org customizations from Apex"
tags:
  - apex-metadata-api
  - metadata-namespace
  - enqueueDeployment
  - DeployCallback
  - isv
  - managed-package
  - programmatic-metadata
inputs:
  - "target metadata type to create or update (CustomField, CustomObject, CustomLabel, etc.)"
  - "the fullName and required attribute values for each metadata component"
  - "callback implementation class name for async result handling"
  - "managed package context if applicable (namespace, subscriber org expectations)"
outputs:
  - "Apex class implementing Metadata.DeployCallback to handle async deployment results"
  - "Apex code invoking Metadata.Operations.enqueueDeployment with correct component descriptors"
  - "review findings on supported types, concurrent deployment limits, and transaction boundaries"
dependencies: []
version: 1.0.0
author: Pranav Nagrecha
updated: 2026-04-04
---

# Apex Metadata API

Use this skill when Apex code must create or modify metadata components programmatically at runtime — not through a deployment pipeline, but through the `Metadata` namespace built into the Apex language. The central use case is ISV managed packages that add custom fields or objects to subscriber orgs during setup, or admin-tool applications that allow users to trigger schema changes via a UI action.

---

## Before Starting

Gather this context before working on anything in this domain:

- Confirm the metadata type being created or updated is in the supported Apex Metadata API type list. Not every metadata type is supported — the supported subset is documented in the Apex Reference Guide under `Metadata.Metadata` subclasses.
- Establish whether the deployment is happening inside a transaction that already contains DML. Apex Metadata API uses a separate asynchronous transaction, but the enqueue call itself cannot follow certain DML patterns without Queueable boundaries.
- Check concurrent deployment limits: an org can have at most 10 active Apex-initiated metadata deployments at once. Exceeding this throws a limit exception.

---

## Core Concepts

### The Metadata Namespace in Apex

Salesforce exposes a `Metadata` system namespace in Apex that provides classes representing a subset of metadata types. Key classes include `Metadata.CustomField`, `Metadata.CustomObject`, `Metadata.CustomTab`, `Metadata.Layout`, `Metadata.ListView`, `Metadata.CustomLabel`, `Metadata.WorkflowRule`, and others. These classes let you construct in-memory representations of metadata components and then deploy them to the org asynchronously. This is fundamentally different from both the SOAP Metadata API (which is a web service) and from standard Apex DML — it is a specialized async engine built into the platform.

The full list of supported Apex Metadata API types is in the Apex Reference Guide. Attempting to deploy an unsupported type causes a runtime error, not a compile-time error.

### Metadata.Operations and enqueueDeployment

`Metadata.Operations` is the class that performs the actual deployment. Its primary method is:

```apex
Metadata.DeployContainer mdContainer = new Metadata.DeployContainer();
mdContainer.addMetadata(/* a Metadata.Metadata subclass instance */);
Id jobId = Metadata.Operations.enqueueDeployment(mdContainer, callbackInstance);
```

`enqueueDeployment` is asynchronous. It submits the deployment to the platform's metadata deployment engine and returns a job ID immediately. The deployment runs in a separate transaction. There is no synchronous equivalent in the Apex Metadata API — the caller cannot block and wait for the result.

### The DeployCallback Interface

Because `enqueueDeployment` is async, results are delivered through a callback. Your Apex class must implement `Metadata.DeployCallback` and define the method:

```apex
public void handleResult(Metadata.DeployResult result, Metadata.DeployCallbackContext context) {
    if (result.isSuccess()) {
        // deployment succeeded — perform any post-setup logic
    } else {
        // examine result.details for failure messages
        List<Metadata.DeployMessage> errors = result.details.componentFailures;
    }
}
```

The `Metadata.DeployResult` object contains `isSuccess()`, `numberComponentErrors`, `numberComponentsDeployed`, and a `details` property with `componentFailures` — each failure has a `problem` and `problemType` field. The callback class must be a top-level class (not an inner class) in most contexts.

### Supported Metadata Types and Their Limits

The Apex Metadata API supports a controlled subset of the full Metadata API type catalog. As of Spring '25, supported types include: `CustomField`, `CustomObject`, `CustomTab`, `Layout`, `ListView`, `CustomLabel`, `WorkflowRule`, `WorkflowFieldUpdate`, `WorkflowAlert`, `WorkflowTask`, `WorkflowOutboundMessage`, `FlexiPage`, `CompactLayout`, `BusinessProcess`, `RecordType`, `WebLink`, `ValidationRule`, `SharingReason`, `FieldSet`. The list is subject to change — always verify against the official Apex Reference Guide before implementing.

Platform limits:
- Maximum 10 concurrent Apex-initiated metadata deployments per org.
- Counts as an asynchronous operation — subject to Apex async limits.
- Cannot combine Metadata.Operations.enqueueDeployment with standard Apex DML in certain transaction contexts without Queueable isolation.

---

## Common Patterns

### ISV Post-Install Field Creation

**When to use:** A managed package needs to create a custom field on a subscriber org object after installation (or after the admin triggers a setup flow). The field does not ship with the package — it must be added dynamically because it depends on subscriber-org conditions.

**How it works:** The post-install script or a Queueable job constructs a `Metadata.CustomField` instance, sets its `fullName` (e.g., `MyObject__c.NewField__c`), `label`, `type`, and any required attributes, adds it to a `Metadata.DeployContainer`, and calls `enqueueDeployment` with a callback class that logs or reacts to the result.

**Why not the alternative:** Packaging the field directly in the managed package forces the field to exist in every org from day one and removes per-subscriber control. Apex Metadata API allows conditional, deferred schema additions without a new package version.

### Admin Tool Triggered Schema Change

**When to use:** A custom Salesforce app (often a Visualforce or LWC-based admin UI) lets administrators add structured fields or labels to the org from a button click, avoiding the Salesforce Setup UI.

**How it works:** The button action calls an Apex controller that validates the user's inputs, constructs the appropriate `Metadata` namespace objects, enqueues the deployment, and stores the job ID for later status checking. The callback class updates a custom object record with success or failure details.

**Why not the alternative:** The SOAP Metadata API could do this, but it requires server-to-server callouts and OAuth token management. The Apex Metadata API runs entirely inside the platform, respects platform security, and does not require external callout configuration.

---

## Decision Guidance

| Situation | Recommended Approach | Reason |
|---|---|---|
| Create a custom field in a subscriber org from managed package setup | Apex Metadata API with Metadata.Operations.enqueueDeployment | In-platform, no external callouts, works within Apex transaction model |
| Standard CI/CD deployment of metadata across environments | SFDX / Metadata API (use metadata-api-and-package-xml skill) | Full type support, CLI-driven, not constrained to Apex Metadata API subset |
| Read Custom Metadata Type configuration records in Apex | Custom Metadata Type SOQL (use custom-metadata-in-apex skill) | Reading __mdt rows is SOQL, not Metadata.Operations |
| Create hundreds of metadata components in one run | Metadata API bulk deployment via CLI | Apex Metadata API is too slow and hits concurrent limits |
| Bulk-update picklist values for many fields | Metadata API deploy via CLI/pipeline | More reliable and supports full type catalog |

---

## Recommended Workflow

Step-by-step instructions for an AI agent or practitioner working on this task:

1. Confirm the target metadata type is in the supported Apex Metadata API type list (Apex Reference Guide, `Metadata.Metadata` subclasses). If it is not listed, stop and use the SOAP/REST Metadata API instead.
2. Verify the org and transaction context — determine whether the enqueue call happens in a trigger, a Queueable, a post-install script, or a controller. Use Queueable with `Database.AllowsCallouts` if DML precedes the enqueue call in the same transaction.
3. Construct the metadata component — create a `Metadata.CustomField` (or other supported type) instance, set `fullName`, `label`, `type`, and all required fields for that type. Missing required fields cause deployment failure that surfaces only in the callback.
4. Build the `Metadata.DeployContainer` and add the component — call `addMetadata()` for each component, then call `Metadata.Operations.enqueueDeployment(container, callbackInstance)`.
5. Implement `Metadata.DeployCallback` in a top-level class — handle both success and failure paths in `handleResult()`. Log errors; do not silently swallow failures.
6. Test the callback in a sandbox or scratch org — Apex Metadata API deployments do not run in unit test context with `@isTest`. Use integration testing in a real org or a post-install test flow.
7. Review concurrent deployment limits before shipping to production — monitor for `System.LimitException` if this pattern is triggered frequently.

---

## Review Checklist

Run through these before marking work in this area complete:

- [ ] Target metadata type is confirmed in the official Apex Metadata API supported type list.
- [ ] `Metadata.DeployCallback` is implemented in a named top-level class, not an anonymous or inner class where not supported.
- [ ] `handleResult()` covers both the success and failure branches and logs failure messages from `result.details.componentFailures`.
- [ ] Transaction boundary is verified — no unguarded DML immediately before `enqueueDeployment` in the same synchronous transaction.
- [ ] Concurrent deployment limit (10 per org) is accounted for in high-frequency scenarios.
- [ ] The job ID returned by `enqueueDeployment` is stored or logged for tracking.
- [ ] Integration test (not unit test) was performed in a sandbox or scratch org to verify the callback fires correctly.

---

## Salesforce-Specific Gotchas

Non-obvious platform behaviors that cause real production problems:

1. **enqueueDeployment is always asynchronous — there is no synchronous result** — code that inspects a return value expecting immediate success will never see it. The job ID returned is not a success indicator; it is a handle for the async job.
2. **Callback does not fire in unit tests** — `Metadata.Operations.enqueueDeployment()` is not executable in Apex test context. Unit tests that call this method throw an exception. Integration testing in a real org is mandatory.
3. **Not all Metadata API types are supported in Apex** — the Apex Metadata API covers a limited subset of the full Metadata API catalog. Trying to deploy an unsupported type (e.g., `Flow`, `ApexClass`) fails at runtime, not compile time.
4. **DML before enqueueDeployment in the same transaction can cause errors** — if a trigger or synchronous controller performs DML and then calls `enqueueDeployment`, the platform may reject it. Isolate the enqueue call in a Queueable job.
5. **10 concurrent deployment limit is per-org, not per-class** — if multiple users or automations trigger deployments simultaneously, you can hit this limit and get `System.LimitException` with no graceful recovery path unless you implement a queuing layer.

---

## Output Artifacts

| Artifact | Description |
|---|---|
| DeployCallback implementation | Apex class implementing Metadata.DeployCallback with result logging |
| enqueueDeployment invocation | Apex code that builds a DeployContainer and submits a deployment |
| Supported type verification | Checklist confirming target type is in the Apex Metadata API supported set |
| Integration test notes | Guidance on verifying callback behavior in a sandbox or scratch org |

---

## Related Skills

- `apex/metadata-api-and-package-xml` — use when deploying metadata via SOAP/REST Metadata API, CI/CD pipelines, or retrieving metadata from an org; covers the full type catalog without Apex runtime constraints.
- `apex/custom-metadata-in-apex` — use when reading or managing Custom Metadata Type configuration records in Apex via SOQL; not for schema creation at runtime.
- `devops/release-management` — use when the deployment question is about pipeline management, environment strategy, or promoting changes across orgs rather than programmatic runtime creation.
