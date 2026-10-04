---
name: lwc-custom-lookup
description: "Custom lookup component in LWC — typeahead/autocomplete that searches records via Apex SOSL/SOQL, shows pills, supports keyboard navigation, and manages open/close state. Use when lightning-input-field or lightning-record-picker won't work (cross-org search, computed filters, custom result rendering). NOT for the base lightning-record-picker — use lwc/lwc-record-picker. NOT for in-form lookups inside lightning-record-edit-form."
category: lwc
salesforce-version: "Spring '25+"
well-architected-pillars:
  - Performance
  - Security
triggers:
  - "lwc custom typeahead lookup component"
  - "lightning-record-picker not flexible enough"
  - "lwc autocomplete record search apex"
  - "search records lwc soql lookup pill"
  - "lwc lookup keyboard navigation arrow keys"
  - "debounce lookup search lwc apex callout"
  - "lookup with multiple object types lwc"
tags:
  - lookup
  - typeahead
  - search
  - sosl
  - keyboard-accessibility
inputs:
  - "Object(s) to search and which fields to show in results"
  - "Debounce window (ms) for search-as-you-type"
  - "Whether selection is single or multi-select"
outputs:
  - "LWC component template + JS controller with debounced search"
  - "Cacheable Apex method using SOSL or SOQL with WITH USER_MODE"
  - "Pill/chip rendering pattern for selected record(s)"
dependencies: []
version: 1.0.0
author: Pranav Nagrecha
updated: 2026-05-05
---

# LWC Custom Lookup

The standard `lightning-input-field` (inside an LDS form) or
`lightning-record-picker` (Spring '24+, free-standing) is the
correct choice for ~90% of lookup use cases. Reach for a custom
lookup only when those don't fit:

- **Cross-org / external search** — picking from a system other
  than Salesforce (the Salesforce-side lookup needs a custom Apex
  method that talks to the external).
- **Computed filters that change per-row** — filter set depends
  on other field values that the running user just changed; the
  declarative lookup filter cannot model.
- **Multi-object search** — one input that matches Accounts and
  Contacts and Opportunities together (SOSL territory).
- **Custom result rendering** — second line, badges, conditional
  icons; the standard picker shows one line.

The hard parts of a hand-rolled lookup are not the SOQL: they are
debounce, keyboard accessibility, the open/close state machine,
the pill UI, and not making the user search for the same thing
they already selected. Skip any of those and the component feels
broken even when it works.

## Recommended Workflow

1. **Confirm `lightning-record-picker` is not enough.** Spring '24
   added the standalone picker with `display-info`, `matching-info`,
   and `filter`. It supports cross-object search via the
   `objectApiName` array. Read its docs first.
2. **Design the Apex search.** Use SOSL for multi-object,
   short-string queries (`FIND :term IN ALL FIELDS RETURNING ...`).
   Use SOQL with `LIKE` only for single-object, indexed-field
   matches. Both with `WITH USER_MODE` and
   `@AuraEnabled(cacheable=true)`. `WITH USER_MODE` is GA from API
   57.0; the clause it replaces, `WITH SECURITY_ENFORCED`, no
   longer compiles at 67.0+ (Summer '26).
3. **Debounce the search by 250-300ms.** Use `setTimeout` /
   `clearTimeout` in the input's `oninput` handler. Without
   debounce, every keystroke fires a callout — exhausting Apex CPU
   and pinning the org.
4. **Build the open/close state machine.** Three states: closed,
   open-with-search-loading, open-with-results. Open on focus,
   close on blur (with a 200ms delay so result clicks land
   first), close on escape, close on selection.
5. **Implement keyboard navigation.** Arrow up/down move
   `activeIndex`, Enter selects, Escape closes. Render
   `aria-activedescendant` on the input pointing at the result li
   so screen readers track focus.
6. **Render the selected state as a pill.** Once chosen, swap the
   input for an SLDS pill (`<lightning-pill>`) with a remove
   action. Re-clicking the remove returns to search mode.
7. **Cache the SObject icon.** `getObjectInfo` gives the icon URL;
   prepend it to results once per render rather than per result.

## What This Skill Does Not Cover

- **Lookups inside `lightning-record-edit-form`** — use
  `lightning-input-field` and configure lookup filters in metadata.
- **`lightning-record-picker` (standalone, Spring '24+)** — see
  `lwc/lwc-record-picker`.
- **Lookup filters at the field-metadata level** — see
  `admin/lookup-filter-design`.
- **Type-ahead against external systems** — see
  `integration/external-search-via-named-credential`.
