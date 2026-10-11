---
name: lwc-imperative-apex
description: "Call Apex methods imperatively from LWC — on button click, lifecycle hooks, or conditional logic. Covers import syntax, cacheable vs non-cacheable, async/await patterns, error handling, loading states, and Promise.all. NOT for wire service (use wire-service-patterns) and NOT for testing Apex mocks (use lwc-testing)."
category: lwc
salesforce-version: "Spring '25+"
well-architected-pillars:
  - Security
  - Performance
  - Reliability
triggers:
  - "how do I call an Apex method from LWC on button click without using wire"
  - "my LWC imperative Apex call is not refreshing data after a save operation"
  - "how do I handle errors from an imperative Apex call in a Lightning web component"
  - "how do I show a loading spinner while an Apex call is in progress in LWC"
  - "how do I run multiple Apex methods in parallel from a Lightning web component"
tags:
  - lwc
  - apex
  - imperative
  - auraenabled
  - promise
  - async-await
inputs:
  - Apex class and method name to call
  - Whether the call is cacheable (read) or non-cacheable (DML/write)
  - LWC component that triggers the call
outputs:
  - Working imperative Apex call with error handling and loading state
  - Correct @AuraEnabled annotation guidance
  - Error extraction utility
dependencies: []
version: 1.0.0
author: Pranav Nagrecha
updated: 2026-04-04
---

# LWC Imperative Apex

This skill activates when a Lightning Web Component needs to call an Apex method on demand — in response to a button click, a lifecycle hook, or explicit conditional logic — rather than reactively through the wire service. It covers the full pattern from import syntax through error handling and parallel calls.

---

## Before Starting

Gather this context before working on anything in this domain:

- Identify whether the Apex method performs DML or is read-only. This determines whether `@AuraEnabled(cacheable=true)` is valid.
- Confirm the Apex class has `@AuraEnabled` on the method and that the class is accessible from the component namespace.
- Understand whether the caller needs to refresh data after a write. Refreshing imperative calls requires re-calling the method — `refreshApex()` does not work with imperative calls.
- Note the governor limits in play: each imperative call is a synchronous Apex execution subject to per-transaction limits (100 SOQL queries, 150 DML statements, heap, CPU).

---

## Core Concepts

### Mode 1 — Import and Call With Promise Chain

The fundamental imperative pattern imports the Apex method as a module and calls it as a function that returns a Promise.

```js
import getContacts from '@salesforce/apex/ContactController.getContacts';

// In a handler or lifecycle hook:
getContacts({ accountId: this.recordId })
    .then(result => {
        this.contacts = result;
        this.error = undefined;
    })
    .catch(error => {
        this.error = error;
        this.contacts = undefined;
    });
```

The import path always follows `@salesforce/apex/<ClassName>.<methodName>`. The Apex method must be `static` and annotated `@AuraEnabled`. Parameters are passed as a plain object where keys match the Apex parameter names exactly (case-sensitive).

### Mode 2 — Async/Await With Loading State

The async/await form is more readable when the handler has sequential operations or multiple calls. Wrap it in a try/catch block and manage an `isLoading` boolean for UI feedback.

```js
async handleSave() {
    this.isLoading = true;
    try {
        const result = await saveRecord({ recordData: this.draftValues });
        this.dispatchEvent(new ShowToastEvent({ title: 'Saved', variant: 'success', message: result }));
        this.draftValues = [];
    } catch (error) {
        this.error = error;
    } finally {
        this.isLoading = false;
    }
}
```

The `finally` block guarantees `isLoading` is cleared even if the Apex throws. This avoids a spinner that never stops — one of the most common UX bugs in LWC Apex integration.

### Mode 3 — Parallel Calls With Promise.all

When the component needs two or more independent Apex results simultaneously (for example, loading related data sets for a detail view), run them in parallel rather than sequentially:

```js
async connectedCallback() {
    this.isLoading = true;
    try {
        const [accounts, contacts] = await Promise.all([
            getAccounts(),
            getContacts({ accountId: this.recordId })
        ]);
        this.accounts = accounts;
        this.contacts = contacts;
    } catch (error) {
        this.error = error;
    } finally {
        this.isLoading = false;
    }
}
```

Sequential `await` calls add latency because each waits for the prior round-trip. `Promise.all` fires both calls concurrently and resolves when both complete. If any call rejects, the catch fires and the entire batch is treated as failed — design accordingly.

---

## Common Patterns

### Cacheable Read — Data Displayed on Load

**When to use:** The component loads record data, picklist values, or lookup results that do not change until the user explicitly refreshes the page.

**How it works:**
1. Annotate the Apex method `@AuraEnabled(cacheable=true)`.
2. Import and call in `connectedCallback` (or a handler triggered by input changes).
3. Store the result in a reactive property so the template re-renders automatically.

```js
import getAccountSummary from '@salesforce/apex/AccountController.getAccountSummary';

async connectedCallback() {
    try {
        this.summary = await getAccountSummary({ accountId: this.recordId });
    } catch (error) {
        this.error = getErrorMessage(error);
    }
}
```

**Why not wire:** Wire is appropriate when the data should reactively refresh whenever reactive properties change. For one-shot load on mount, imperative is simpler and avoids the wire provisioning lifecycle.

### Non-Cacheable Write — DML on User Action

**When to use:** A button or form submission should create, update, or delete records. Cacheable methods cannot perform DML; attempting it throws a runtime error.

**How it works:**
1. Annotate the Apex method `@AuraEnabled` (no `cacheable=true`).
2. Call it in the click handler.
3. After a successful write, re-call any read methods that need fresh data — `refreshApex()` does not apply here.

```js
import upsertContact from '@salesforce/apex/ContactController.upsertContact';

async handleSubmit() {
    this.isLoading = true;
    try {
        await upsertContact({ contact: this.draftContact });
        // Re-fetch to get the latest state
        this.contacts = await getContacts({ accountId: this.recordId });
    } catch (error) {
        this.error = getErrorMessage(error);
    } finally {
        this.isLoading = false;
    }
}
```

### Error Message Extraction

The error object from a rejected Apex call is an object with a `body` property. Extract a readable string before displaying it:

```js
function getErrorMessage(error) {
    if (Array.isArray(error.body)) {
        return error.body.map(e => e.message).join(', ');
    }
    if (typeof error.body?.message === 'string') {
        return error.body.message;
    }
    return error.message ?? 'Unknown error';
}
```

Using `error.message` directly without checking `body` fails silently — the user sees "undefined" in the UI.

---

## Decision Guidance

| Situation | Recommended Approach | Reason |
|---|---|---|
| Data loads once on component mount | Imperative call in `connectedCallback` | Simpler than wire for non-reactive scenarios |
| Data must refresh when a property changes | `@wire` adapter | Wire re-runs automatically on reactive property change; imperative requires manual re-call |
| Button triggers a DML operation | Non-cacheable imperative call | Cacheable methods cannot perform DML |
| Two independent data sets needed on load | `Promise.all` with imperative calls | Parallel calls are faster than sequential awaits |
| Need to refresh after a write | Re-call the read method imperatively | `refreshApex()` only works with wire results |
| Reading standard objects with field-level security | Wire LDS adapters (`getRecord`) | LDS handles FLS automatically; custom Apex must enforce it explicitly |

---


## Recommended Workflow

Step-by-step instructions for an AI agent or practitioner activating this skill:

1. Gather context — confirm the org edition, relevant objects, and current configuration state
2. Review official sources — check the references in this skill's well-architected.md before making changes
3. Implement or advise — apply the patterns from Core Concepts and Common Patterns sections above
4. Validate — run the skill's checker script and verify against the Review Checklist below
5. Document — record any deviations from standard patterns and update the template if needed

---

## Review Checklist

Run through these before marking work in this area complete:

- [ ] The Apex method is `static`, `@AuraEnabled`, and (if read-only) `cacheable=true`.
- [ ] The Apex class enforces sharing (`with sharing` or explicit CRUD/FLS checks) — never `without sharing` unless justified.
- [ ] `isLoading` is set before the call and cleared in a `finally` block.
- [ ] Error handling checks `error.body.message` (or the array form) rather than `error.message`.
- [ ] Any data refresh after a write re-calls the read method imperatively — no `refreshApex()` on imperative results.
- [ ] Parallel reads use `Promise.all` rather than sequential `await`.
- [ ] Jest tests mock the Apex import at the module level, not as a wire adapter.

---

## Salesforce-Specific Gotchas

Non-obvious platform behaviors that cause real production problems:

1. **refreshApex() silently does nothing on imperative results** — `refreshApex()` is a wire-only utility. Calling it on a variable populated by an imperative call neither throws nor refreshes; data simply stays stale. Re-call the method explicitly to get fresh data.
2. **cacheable=true blocks all DML, including `Database.insert` inside helper methods** — If a `cacheable=true` method calls any helper that performs DML (even via a private method chain), Salesforce throws a runtime error: `System.QueryException: Callout not allowed after DML`. Mark the method non-cacheable if any part of the call stack writes to the database.
3. **Parameter names are case-sensitive and must match Apex exactly** — Passing `{ AccountId: id }` when the Apex parameter is `accountId` results in a `null` value in Apex with no error thrown. Debug by adding a null check in Apex or verifying the parameter name case.

---

## Output Artifacts

| Artifact | Description |
|---|---|
| Imperative Apex call pattern | JS snippet with import, async handler, `isLoading`, and error extraction ready to paste into a component |
| Error extraction utility | Reusable `getErrorMessage(error)` function that handles both single-message and array-form body shapes |
| Parallel load pattern | `Promise.all` snippet for loading multiple independent data sets in connectedCallback |

---

## Related Skills

- wire-service-patterns — Use when data should reactively update when component properties change; covers `@wire` decorator, reactive parameters, and `refreshApex()`
- lwc-testing — Use to write Jest tests for components that call Apex imperatively; covers `jest.mock` for Apex imports and promise resolution helpers
- apex-security — Use to verify the Apex class enforces sharing, CRUD, and FLS correctly before exposing it to LWC
