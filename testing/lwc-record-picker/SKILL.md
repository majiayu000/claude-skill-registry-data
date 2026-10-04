---
name: lwc-record-picker
description: "lightning-record-picker base component (Winter '24 GA): object/record filter, displayInfo/matchingInfo, graph-ql filters, accessibility. Replaces ad-hoc lookup inputs. NOT for a fully custom typeahead lookup — use lwc/lwc-custom-lookup."
category: lwc
salesforce-version: "Spring '25+"
well-architected-pillars:
  - User Experience
  - Operational Excellence
tags:
  - lwc
  - record-picker
  - lookup
  - lightning-base-components
  - accessibility
triggers:
  - "lightning record picker component lwc replace custom lookup"
  - "record picker display info matching info config"
  - "record picker filter graphql criteria"
  - "how to preselect value in record picker"
  - "record picker accessibility keyboard"
  - "record picker vs lightning lookup aura"
inputs:
  - Target object API name
  - Fields to display / match
  - Filter criteria (graph-QL style)
  - Preselection value
outputs:
  - Configured lightning-record-picker usage
  - Migration plan from legacy custom lookup
  - Test coverage with jest
dependencies: []
version: 1.1.0
author: Pranav Nagrecha
updated: 2026-05-19
---

# LWC Record Picker

Activate when an LWC needs a user to search and select a single Salesforce record. `lightning-record-picker` (GA Winter '24) is the official base component; it replaces custom combobox+search implementations and hand-rolled `lightning-lookup` equivalents with one declarative tag.

## Before Starting

- **Use `lightning-record-picker`** rather than rolling a custom lookup.
- **Configure `display-info` and `matching-info`** — they drive what the user sees and what fields search hits.
- **Set a filter** for scoped choice lists (e.g., only active accounts).

## Core Concepts

### Minimum markup

```
<lightning-record-picker
    label="Account"
    placeholder="Search Accounts"
    object-api-name="Account"
    onchange={handleChange}>
</lightning-record-picker>
```

`event.detail.recordId` on change carries the selected record Id.

### display-info / matching-info

```
<lightning-record-picker
    object-api-name="Contact"
    display-info={displayInfo}
    matching-info={matchingInfo}>
</lightning-record-picker>
```

```
displayInfo = {
    primaryField: 'Name',
    additionalFields: ['Account.Name', 'Email']
};
matchingInfo = {
    primaryField: { fieldPath: 'Name' },
    additionalFields: [{ fieldPath: 'Email' }]
};
```

### Filter (graph-QL)

```
filter = {
    criteria: [
        { fieldPath: 'IsActive', operator: 'eq', value: true }
    ]
};
```

Limits search results.

### Preselection

Set `value={preselectedRecordId}`. The picker fetches display fields and shows the chip.

## Common Patterns

### Pattern: Filtered contact picker scoped to account

Filter on `AccountId = :this.accountId`; filter updates when the account context changes.

### Pattern: Multi-object picker via toggle

Two `<lightning-record-picker>` elements toggled by a dropdown that selects the object API name.

### Pattern: Reset on context change

Programmatically set `value = null` (or re-query) when context changes.

## Decision Guidance

| Need | Component |
|---|---|
| Standard single-record lookup | lightning-record-picker |
| Multi-record select | lightning-record-picker (not supported) → build custom |
| External object | lightning-record-picker does not support; custom |
| Enforce record-type filter | Use `filter` criteria on RecordTypeId |
| Filter by complex formula | Server-side Apex + custom combobox |

## Recommended Workflow

1. Confirm object is supported (standard + most custom). External objects unsupported.
2. Define `display-info` and `matching-info` — always set primaryField.
3. Build `filter` with graph-QL criteria for scope.
4. Wire `onchange` to capture selected Id and fetch additional record details.
5. Add accessibility attributes: label is required; leverage built-in keyboard nav.
6. Write jest test asserting `change` event dispatch.
7. Migrate any legacy custom lookup components to this one.

## Review Checklist

- [ ] `lightning-record-picker` used instead of custom combobox
- [ ] `object-api-name` supported by the base component
- [ ] `display-info` primaryField set
- [ ] `matching-info` matches display
- [ ] `filter` scopes results to valid options
- [ ] `onchange` handler captures `recordId`
- [ ] Label is descriptive and required attribute set where mandatory
- [ ] Jest test covers change event

## Salesforce-Specific Gotchas

1. **External Objects not supported.** The picker targets standard/custom only.
2. **Person Account nuance** — when Person Accounts are on, `Account` results include persons; filter if you want companies only.
3. **`matching-info` is required for custom search fields** — without it, only primary field matches.

## Output Artifacts

| Artifact | Description |
|---|---|
| Picker config template | displayInfo / matchingInfo / filter examples |
| Migration plan | Legacy custom lookup → record-picker |
| Jest test helper | Mock event dispatch |

## Related Skills

- `lwc/lwc-forms-patterns` — picker embedded in forms
- `lwc/lwc-lookup-custom-patterns` — when base picker is insufficient
- `admin/custom-field-creation` — lookup field design
