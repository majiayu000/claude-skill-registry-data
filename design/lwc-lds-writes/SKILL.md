---
name: lwc-lds-writes
description: "Use when an LWC must create, update, or delete records via Lightning Data Service (`lightning/uiRecordApi` — `createRecord`, `updateRecord`, `deleteRecord`) or via `lightning-record-edit-form` / `lightning-record-form`. Triggers: 'updateRecord cache not refreshing', 'createRecord returns DUPLICATES_DETECTED', 'updateRecord input shape with field references', 'lightning-record-edit-form submit not committing', 'should I use LDS write or imperative Apex DML'. NOT for read-only wires (use lwc/wire-service-patterns), NOT for refreshing wired data after a write (use lwc/lwc-wire-refresh-patterns), and NOT for Apex DML from LWC (use apex/apex-dml-patterns)."
category: lwc
salesforce-version: "Spring '25+"
well-architected-pillars:
  - Security
  - Reliability
  - User Experience
triggers:
  - "lwc updateRecord not committing or cache stays stale after write"
  - "createRecord throws DUPLICATES_DETECTED or FIELD_INTEGRITY_EXCEPTION on a working sObject"
  - "should the component use LDS createRecord or call Apex DML for this write"
  - "lightning-record-edit-form submit fires but record doesn't update in the database"
  - "deleteRecord succeeds but related @wire still shows the deleted record"
  - "uiRecordApi recordInput shape with FieldId schema imports vs string field names"
tags:
  - lds-writes
  - uiRecordApi
  - createRecord
  - updateRecord
  - deleteRecord
  - lightning-record-edit-form
  - cache-invalidation
inputs:
  - "the operation (create / update / delete) and the sObject"
  - "whether the component already wires the same record via getRecord"
  - "whether sharing/CRUD/FLS enforcement matters or whether the user lacks access"
  - "whether the write is part of a multi-record transaction or a single user-initiated action"
outputs:
  - "an LDS write call (or a justified imperative Apex fallback) with correct recordInput shape"
  - "post-write refresh strategy for any wired reads of the same record"
  - "error handling for FIELD_VALIDATION_EXCEPTION, DUPLICATES_DETECTED, and INSUFFICIENT_ACCESS"
dependencies: []
version: 1.0.0
author: Pranav Nagrecha
updated: 2026-05-05
---

# LWC Lightning Data Service Writes

Activate when an LWC needs to **mutate** record data — create, update, or delete — and the right answer is the Lightning Data Service write API (`lightning/uiRecordApi` or the form base components) rather than imperative Apex. The skill produces a correctly shaped `recordInput`, an explicit cache-refresh strategy, and error handling for the four UI API error shapes that surface to the user. It complements `lwc/wire-service-patterns` (read path) and `lwc/lwc-wire-refresh-patterns` (refresh path); writes are deliberately separated because the input format, error shape, and cache semantics differ from reads.

---

## Before Starting

Gather this context before writing any LDS write code:

- **Operation type and cardinality** — single record from a user gesture (LDS is the right fit), or a batch/transaction (likely Apex DML). LDS writes are one record per call.
- **Record-edit form vs imperative call** — `lightning-record-edit-form` and `lightning-record-form` are LDS in disguise; they cover 80% of single-record edit UX without writing a JS handler. Imperative `updateRecord` is for when the form layout is wrong for the use case (multi-step wizard, conditional fields, custom save button labelling).
- **Whether the same component reads the record via wired `getRecord`** — if yes, LDS will refresh that wire automatically after a write to the same `recordId`. If a *different* component reads it, you may need `notifyRecordUpdateAvailable`.
- **Sharing / CRUD / FLS posture** — UI API enforces sharing, CRUD, FLS, and validation rules in the running user's context; Apex `without sharing` does not. Choosing LDS is also choosing the user's full access stack.

---

## Core Concepts

### `lightning/uiRecordApi` is the JS write surface

`createRecord({ apiName, fields })`, `updateRecord({ fields: { Id, ... } })`, and `deleteRecord(recordId)` are imported from `lightning/uiRecordApi` and return Promises. They call the Salesforce UI API (`/services/data/vXX.X/ui-api/records/...`), which enforces sharing, CRUD, FLS, validation rules, duplicate rules, and triggers exactly as if the user clicked Save in standard UI.

### The `fields` object shape uses API names, not FieldId imports

For writes, `fields` is a plain object whose keys are **string field API names** (not `@salesforce/schema/Account.Name` imports). The exception is `apiName`, which can come from a schema import:

```javascript
import ACCOUNT_OBJECT from '@salesforce/schema/Account';
import NAME_FIELD from '@salesforce/schema/Account.Name';
import { createRecord } from 'lightning/uiRecordApi';

const recordInput = {
    apiName: ACCOUNT_OBJECT.objectApiName,   // schema import → ".objectApiName"
    fields: {
        [NAME_FIELD.fieldApiName]: 'Acme',   // schema import → ".fieldApiName"
        Industry: 'Technology'                 // or just a string literal
    }
};
const account = await createRecord(recordInput);
```

For `updateRecord`, the `fields` object **must include `Id`** at the top level inside `fields`:

```javascript
await updateRecord({ fields: { Id: this.recordId, Industry: 'Manufacturing' } });
```

`recordInput` for create vs update is shaped differently (`apiName` only on create), and getting this wrong throws `INVALID_FIELD_FOR_INSERT_UPDATE`.

### LDS auto-refreshes wired `getRecord` for the same recordId in the same component

After a successful `updateRecord` or `createRecord`, any `@wire(getRecord, { recordId: '$recordId', fields: [...] })` in the *same* component instance is re-evaluated automatically. You do not call `refreshApex` — that is for Apex-backed wires. Cross-component refresh requires `notifyRecordUpdateAvailable([{ recordId }])` to tell LDS that records changed outside its visibility (after Apex DML, for example).

### UI API errors come back as a structured object, not a thrown string

The Promise rejects with `{ body: { output: { errors: [...], fieldErrors: {...} } }, statusText, status }`. Field-level errors are keyed by field API name. Catch the rejection and surface field errors next to the right input, surface object-level errors as a toast, and treat `INSUFFICIENT_ACCESS_OR_READONLY` differently from `FIELD_VALIDATION_EXCEPTION`.

---

## Common Patterns

### Pattern: `lightning-record-edit-form` for the standard single-record edit

**When to use:** a single record, the layout you need is close to a page layout, and you want LDS sharing/CRUD/FLS enforcement plus inline field-level errors for free.

**How it works:** Wrap `lightning-input-field` elements inside `<lightning-record-edit-form record-id={recordId} object-api-name="Account" onsuccess={handleSuccess} onerror={handleError}>`. Submit with `<lightning-button type="submit">` or programmatically via `this.template.querySelector('lightning-record-edit-form').submit()`. No JS write call needed.

**Why not the alternative:** Reaching for `updateRecord` when a form would do means you also rebuild field rendering, validation, and CRUD/FLS toggling.

### Pattern: imperative `updateRecord` for a custom save button or conditional field set

**When to use:** the save UX is non-standard (multi-step, computed fields, conditional save validation that the form can't express), but the write is still a single record.

**How it works:**

```javascript
import { updateRecord } from 'lightning/uiRecordApi';
import { ShowToastEvent } from 'lightning/platformShowToastEvent';

async handleSave() {
    try {
        await updateRecord({ fields: { Id: this.recordId, ...this.dirtyFields } });
        this.dispatchEvent(new ShowToastEvent({ title: 'Saved', variant: 'success' }));
    } catch (err) {
        const fieldErrs = err?.body?.output?.fieldErrors ?? {};
        this.fieldErrors = fieldErrs;
        const objectErrs = err?.body?.output?.errors?.map(e => e.message).join('; ');
        if (objectErrs) {
            this.dispatchEvent(new ShowToastEvent({ title: 'Save failed', message: objectErrs, variant: 'error' }));
        }
    }
}
```

**Why not the alternative:** Calling Apex DML loses sharing/FLS enforcement unless the controller does it manually, and bypasses validation rules' UI behavior (record-page error placement).

### Pattern: cross-component refresh with `notifyRecordUpdateAvailable`

**When to use:** a write happens via Apex DML (or in another component) and a different LWC on the same page wires the same record via `getRecord`.

**How it works:** After the Apex call resolves, call `notifyRecordUpdateAvailable([{ recordId }])`. LDS re-fetches the record on its next provisioning cycle, and any `@wire(getRecord)` for that recordId across the page receives the new value.

**Why not the alternative:** Without it, the wired component holds the cached pre-write copy until the user navigates away.

### Pattern: `deleteRecord` with optimistic UI removal

**When to use:** a list view component where the user clicks "Remove" on a row.

**How it works:** Optimistically splice the row out of the rendered array, call `await deleteRecord(rowId)`, and on rejection re-insert the row plus toast. If the list itself is wired, call `refreshApex` on that wire after success.

---

## Decision Guidance

| Situation | Recommended Approach | Reason |
|---|---|---|
| Single-record edit, standard layout | `lightning-record-edit-form` | Free CRUD/FLS, validation rendering, no JS write |
| Single-record edit, custom UX | imperative `updateRecord` | Keeps LDS enforcement and cache benefits |
| Multi-record transaction (atomic) | Apex DML via `@AuraEnabled` | LDS writes are per-record; no transaction boundary |
| Mutation must run as `without sharing` (admin tool) | Apex DML | LDS always runs in user context |
| Need to suppress validation rules / triggers | Not possible from LDS | Use a different architecture; no LDS bypass exists |
| Update from another component, must refresh this one | `notifyRecordUpdateAvailable` after the write | LDS auto-refresh only inside the same component instance |
| Bulk insert (e.g., 50 contacts at once) | Apex DML | LDS writes are one record per call; 50 calls is a CPU/UX problem |

For "should this be Flow / Apex / LDS at all?", read `standards/decision-trees/automation-selection.md` first.

---

## Recommended Workflow

1. Confirm the use case is single-record and user-initiated. Multi-record or system writes belong in Apex.
2. Decide form vs imperative: if a `lightning-record-edit-form` covers the layout, default to it.
3. For imperative writes, build `recordInput` with `apiName` (only on create) plus a `fields` object. For updates, `Id` goes inside `fields`, not at the top level.
4. Wire the post-write UX: success toast/navigation, field error mapping, object-error fallback. Map `err.body.output.fieldErrors` to your input components.
5. Decide refresh strategy: same-component wires refresh automatically; cross-component wires need `notifyRecordUpdateAvailable`; Apex-backed wires need `refreshApex`.
6. Verify CRUD/FLS in a non-admin profile sandbox before shipping — UI API rejects writes the user lacks access to, but with a non-obvious `INSUFFICIENT_ACCESS_OR_READONLY` error rather than silent no-op.
7. Add Jest tests that mock `createRecord`/`updateRecord`/`deleteRecord` from `lightning/uiRecordApi` and assert the `recordInput` shape your code produces.

---

## Review Checklist

- [ ] `apiName` only present on `createRecord` calls, never on `updateRecord`
- [ ] `Id` for updates is inside `fields`, not at the top level of `recordInput`
- [ ] `fields` keys are string API names (or `.fieldApiName` from a schema import)
- [ ] Error handler reads `err.body.output.fieldErrors` and `err.body.output.errors`
- [ ] Cross-component refresh uses `notifyRecordUpdateAvailable`, not a custom event
- [ ] Apex-backed wired data refreshed via `refreshApex`, not LDS APIs
- [ ] Jest test mocks `lightning/uiRecordApi` and asserts the call shape
- [ ] Confirmed in a non-admin profile that CRUD/FLS denial surfaces a meaningful error to the user

---

## Salesforce-Specific Gotchas

1. **`Id` placement differs from REST API** — `updateRecord({ fields: { Id, ... } })`. Putting `Id` at the top level of `recordInput` (mirroring REST `PATCH /sobjects/Account/<id>`) throws `INVALID_FIELD_FOR_INSERT_UPDATE`.
2. **Schema imports for fields use `.fieldApiName` for writes** — `import NAME from '@salesforce/schema/Account.Name'` exposes `NAME.fieldApiName` (a string). Using the import object itself as a key emits `[object Object]` and fails at the server.
3. **LDS writes do not bulk** — there is no array form. Looping `await updateRecord(...)` for 200 records will trigger 200 UI API calls and a multi-second UX.
4. **Validation rule errors are returned at field-level when possible** — but rules with `null` `errorDisplayField` come back as object-level errors only. Code defensively for both shapes.
5. **`INSUFFICIENT_ACCESS_OR_READONLY` covers FLS denial, CRUD denial, sharing denial, and recordtype denial** — the error shape doesn't distinguish them. Don't claim "you don't own this record" in the toast unless you've separately verified.
6. **Same-record auto-refresh only happens for `getRecord` wires in the same component** — it does NOT cascade to `getRecords` (note the plural), GraphQL wires, or Apex-backed wires. Each needs its own refresh path.
7. **`deleteRecord` returns `undefined` on success, not the deleted record** — code that destructures the return throws `TypeError`.
8. **A read-only field included in `fields` causes the entire write to fail** — even if you're not changing it, including `LastModifiedDate` or a formula field in `fields` produces `INVALID_FIELD_FOR_INSERT_UPDATE`. Filter dirty-only.

---

## Output Artifacts

| Artifact | Description |
|---|---|
| LWC write handler | JS handler with shaped `recordInput`, structured error mapping, and refresh call |
| Field-error binding | Mapping from `err.body.output.fieldErrors` keys to `lightning-input-field` / form inputs |
| Cross-component refresh wiring | `notifyRecordUpdateAvailable` call site (often after an Apex DML resolves) |
| Jest spec | Mocks `lightning/uiRecordApi`; asserts `recordInput` shape and error-path UX |

---

## Related Skills

- `lwc/wire-service-patterns` — for the read path and reactive parameters; LDS writes complement, not replace, this skill
- `lwc/lwc-wire-refresh-patterns` — for the post-write refresh path (`refreshApex`, `RefreshView`, `getRecordNotifyChange`/`notifyRecordUpdateAvailable`)
- `lwc/lwc-base-component-recipes` — for `lightning-record-edit-form` and `lightning-record-form` configuration patterns
- `apex/apex-dml-patterns` — for the Apex DML alternative when LDS writes are not the right fit (multi-record, system context, transaction boundary)
- `standards/decision-trees/automation-selection.md` — for the "Flow vs LWC vs Apex" decision before reaching for any of the above
