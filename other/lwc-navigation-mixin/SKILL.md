---
name: lwc-navigation-mixin
description: "Navigate between Lightning pages, records, and apps from LWC via NavigationMixin. Triggers: NavigationMixin, navigate, standard__recordPage. NOT for URL/deep-link strategy across apps — use lwc/navigation-and-routing. NOT for cross-tab state — use lwc/lwc-cross-tab-state-sync."
category: lwc
salesforce-version: "Spring '25+"
well-architected-pillars:
  - User Experience
  - Operational Excellence
tags:
  - lwc
  - navigation-mixin
  - pagereference
  - experience-cloud
  - deep-linking
triggers:
  - "navigationmixin.navigate recordpage pagereference"
  - "how to open record in new tab from lwc"
  - "generate url lwc and copy to clipboard"
  - "experience cloud navigation comm__namedpage"
  - "lwc navigate to related list with state"
  - "navigationmixin vs lightning-navigation"
  - "lwc navigation mixin page reference recordpage"
  - "lwc navigate to url state c__ prefix required"
inputs:
  - Target page type (record, list, custom, external)
  - Context (internal app, Experience Cloud, mobile)
  - URL params / state to pass
outputs:
  - PageReference configuration
  - navigate vs generateUrl usage
  - Experience Cloud variant
  - State-param pattern
dependencies: []
version: 1.1.0
author: Pranav Nagrecha
updated: 2026-05-15
---

# LWC NavigationMixin

Activate when an LWC needs to navigate — to a record, a list view, a named page, or an external URL. `NavigationMixin` is the canonical Salesforce API for navigation; raw `window.location` usage is forbidden on most surfaces and bypasses Salesforce's routing, tab, and mobile handling.

## Before Starting

- **Import the mixin correctly.** `import { NavigationMixin } from 'lightning/navigation';` and apply with `extends NavigationMixin(LightningElement)`.
- **Pick the right PageReference type.** Internal app vs Experience Cloud has different names (`standard__*` vs `comm__*`).
- **Distinguish `navigate()` vs `generateUrl()`.** Navigate triggers routing; generateUrl returns a URL promise for anchors, copy-to-clipboard, etc.

## Core Concepts

### PageReference shape

```
{
    type: 'standard__recordPage',
    attributes: { recordId: '001...', objectApiName: 'Account', actionName: 'view' },
    state: { c__tab: 'details' }
}
```

`attributes` are type-specific; `state` flows through URL params as `c__*`.

### Internal vs Experience Cloud

- Internal: `standard__recordPage`, `standard__objectPage`, `standard__namedPage`, `standard__webPage`
- Experience Cloud: `comm__namedPage`, `comm__loginPage` (prefer over `standard__`)

### navigate vs generateUrl

```
this[NavigationMixin.Navigate](pageRef);                     // route now
this[NavigationMixin.GenerateUrl](pageRef).then(url => ...); // URL string
```

`GenerateUrl` is async (returns a Promise).

### New tab

Wrap in an `<a target="_blank" href={url}>` using `generateUrl`. The mixin has no direct "open in new tab" option.

## Common Patterns

### Pattern: Navigate to record view

```
const ref = { type: 'standard__recordPage',
    attributes: { recordId: this.recordId, objectApiName: 'Account', actionName: 'view' } };
this[NavigationMixin.Navigate](ref);
```

### Pattern: Generate URL for copy-to-clipboard

```
const url = await this[NavigationMixin.GenerateUrl](ref);
navigator.clipboard.writeText(window.location.origin + url);
```

### Pattern: State params for tab selection

```
{ type: 'standard__recordPage', attributes: { ... },
  state: { c__selectedTab: 'history' } }
```

Receiving component reads `@wire(CurrentPageReference) pageRef` and `pageRef.state.c__selectedTab`.

## Decision Guidance

| Target | PageReference type |
|---|---|
| Record view / edit | standard__recordPage |
| Object list view | standard__objectPage + list actionName |
| Custom Lightning component | standard__component |
| External URL | standard__webPage |
| Experience Cloud named page | comm__namedPage |
| Relative URL in Experience Cloud | comm__namedPage with pageName |

## Recommended Workflow

1. Identify target context (internal, Experience, mobile).
2. Pick PageReference type matching target and context.
3. Populate `attributes` (recordId, objectApiName, etc.) per type spec.
4. Use `state` for transient params (tab, filter).
5. Choose `Navigate` (immediate) or `GenerateUrl` (async).
6. For mobile deep-links, test via Mobile Publisher.
7. Never fall back to `window.location.href =` — breaks routing.

## Review Checklist

- [ ] NavigationMixin applied via `extends NavigationMixin(LightningElement)`
- [ ] PageReference type matches the surface (standard vs comm)
- [ ] Attributes populated with required keys
- [ ] State params prefixed `c__` where custom
- [ ] GenerateUrl used for hrefs; Navigate for routing
- [ ] No `window.location` fallbacks
- [ ] Experience Cloud deep-links tested in the Experience context
- [ ] Mobile app deep-links tested

## Salesforce-Specific Gotchas

1. **`state` param names must start with `c__`** unless using a framework-defined key.
2. **`standard__namedPage` cannot be used in Experience Cloud**; use `comm__namedPage`.
3. **GenerateUrl is async.** Awaiting is required; returning the promise without awaiting leaves consumers with `undefined`.

## Output Artifacts

| Artifact | Description |
|---|---|
| PageReference catalog | Type × attributes × surface |
| URL helper module | Reusable generateUrl wrappers |
| Deep-link test matrix | Internal / Experience / Mobile coverage |

## Related Skills

- `lwc/lwc-url-params-and-state` — state-param handling
- `admin/app-and-tab-configuration` — tab and app setup
- `mobile/mobile-deep-linking` — mobile-specific nav
