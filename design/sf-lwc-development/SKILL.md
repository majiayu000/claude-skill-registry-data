---
name: sf-lwc-development
description: Covers building Lightning Web Components on the Salesforce platform - bundle anatomy and js-meta.xml targets/targetConfigs, the reactivity model, @api/@wire/@track decorators, Lightning Data Service and imperative Apex, CustomEvent and Lightning Message Service communication, lifecycle hooks, template directives (lwc:if, for:each, iterator, lwc:ref, lwc:dom="manual", slots), SLDS styling hooks, shadow vs light DOM, NavigationMixin, toasts, labels and i18n, static resources and third-party JS, Lightning Web Security constraints, and performance/accessibility rules. Use this skill whenever work touches force-app/**/lwc/**, a *.js-meta.xml file, a wire adapter such as getRecord or graphql, an @AuraEnabled(cacheable=true) method consumed from JavaScript, refreshApex, a LightningMessageChannel, or when a component must be exposed to a Lightning App Page, Record Page, Flow screen, quick action, or Experience Cloud site.
---

# Lightning Web Components Development

## When to use

| Situation | Use this skill |
| --- | --- |
| Creating or editing anything under `force-app/main/default/lwc/` | Yes |
| Choosing between `@wire`, imperative Apex, and Lightning Data Service | Yes |
| Component must appear in Lightning App Builder, Flow Builder, or Experience Builder | Yes |
| Writing the Apex controller behind the component | Skill `sf-apex-development` (this skill covers only the JS side of the contract) |
| Writing Jest tests for the component | Skill `sf-lwc-jest-testing` |
| Previewing the component without deploying | Skill `sf-local-development` |
| ESLint/PMD/Code Analyzer findings on LWC JS | Skill `sf-code-analyzer-quality` |
| Generating a component, spec or migration with Salesforce DX MCP tools or Agentforce Vibes LWC skills | Yes - [`references/mcp-and-skills.md`](references/mcp-and-skills.md), then the same gates apply |

LWC is the owner slice of `sf-lwc-engineer` in wave 1: `lwc/` and `aura/` only. Apex signatures the
component consumes are fixed in wave 0 and recorded in `.vibeforce/state/contract.md`.

## Decision table

| Need | Mechanism | Cacheable | Refresh path |
| --- | --- | --- | --- |
| Read one record, fields known at build time | `@wire(getRecord, {recordId, fields})` | Yes (LDS) | Automatic; `notifyRecordUpdateAvailable()` after out-of-band writes |
| Read several related objects in one round trip | `@wire(graphql, {query, variables})` | Yes (LDS) | `refreshGraphQL` / re-evaluate variables |
| Read object metadata or picklists | `getObjectInfo`, `getPicklistValues` | Yes (LDS) | Automatic |
| Read a query/aggregate LDS cannot express | `@wire(apexMethod)` with `@AuraEnabled(cacheable=true)` | Yes (client cache) | `refreshApex(this.wiredResult)` |
| Write one record, standard fields | `createRecord` / `updateRecord` / `deleteRecord` (`lightning/uiRecordApi`) | n/a | LDS updates wires automatically |
| Write with server-side business logic | imperative Apex (`@AuraEnabled`, never `cacheable=true`) | No | `await notifyRecordUpdateAvailable([{recordId}])` |
| Form UI with zero JS | `lightning-record-form` / `lightning-record-edit-form` | n/a | `onsuccess` event |
| Fire-and-forget action on user click | imperative Apex in an `async` handler | No | n/a |

Rule: a method annotated `@AuraEnabled(cacheable=true)` **cannot perform DML**; it is the only shape
`@wire` accepts. Any DML path must be a separate non-cacheable `@AuraEnabled` method.

## Core patterns

### 1. Bundle anatomy and configuration

```
force-app/main/default/lwc/accountCard/
  accountCard.js          default-exported class extending LightningElement
  accountCard.html        template (optional only for service components)
  accountCard.css         scoped styles (optional)
  accountCard.js-meta.xml required; controls exposure and builder configuration
  __tests__/accountCard.test.js   Jest suite (gate: vf-check jest)
```

```xml
<?xml version="1.0" encoding="UTF-8"?>
<LightningComponentBundle xmlns="http://soap.sforce.com/2006/04/metadata">
    <apiVersion>67.0</apiVersion>
    <isExposed>true</isExposed>
    <masterLabel>Account Card</masterLabel>
    <description>Shows key account fields with an escalate action.</description>
    <targets>
        <target>lightning__RecordPage</target>
        <target>lightning__AppPage</target>
        <target>lightningCommunity__Default</target>
    </targets>
    <targetConfigs>
        <targetConfig targets="lightning__RecordPage">
            <property name="showEscalate" type="Boolean" label="Show Escalate Button" default="true"/>
            <objects>
                <object>Account</object>
            </objects>
        </targetConfig>
        <targetConfig targets="lightningCommunity__Default">
            <property name="recordId" type="String" label="Record Id"/>
        </targetConfig>
    </targetConfigs>
</LightningComponentBundle>
```

`apiVersion` comes from `config/vibe-force.defaults.json` (`67.0`). Beginning in Spring '25 every
component must carry an `apiVersion` tag to be saved back to Salesforce. `isExposed=false` hides the
component from all builders; exposure additionally requires at least one `<target>`. Full target list:
`references/component-reference.md`.

### 2. Reactivity: fields, not state objects

```javascript
import { LightningElement, track } from 'lwc';

export default class ReactivityExample extends LightningElement {
    // Reactive by default: reassignment of a field re-renders if the field is used in the template
    count = 0;
    filters = { status: 'Open' };
    @track rows = [];          // @track only for mutation-in-place of objects/arrays

    get label() {              // getters are the supported way to compute template values
        return `${this.count} open`;
    }

    mutate() {
        this.count = 1;                               // rerender
        this.filters.status = 'Closed';               // NO rerender: field not reassigned
        this.filters = { ...this.filters, status: 'Closed' }; // rerender
        this.rows.push({ id: '1' });                  // rerenders only because of @track
    }
}
```

Reassigning a field to an `===`-equal primitive is not a mutation and does not rerender. Prefer
immutable replacement (`{...obj}`, `[...arr]`) over `@track`; reserve `@track` for deep mutation you
genuinely cannot avoid. `@track` and `@api` on the same property is a compile error (LWC1093).

### 3. Public API: `@api` properties and methods

```javascript
import { LightningElement, api } from 'lwc';

export default class Badge extends LightningElement {
    @api recordId;            // set by the record page container
    @api variant = 'neutral';

    _rows = [];
    @api
    get rows() { return this._rows; }
    set rows(value) { this._rows = Array.isArray(value) ? [...value] : []; } // normalize on the way in

    @api focusFirst() {       // public method, called by parent via querySelector
        this.refs.firstInput?.focus();
    }
}
```

Never mutate an `@api` property from inside the component; the owner owns the value. Public property
setters run before `connectedCallback()` on initial render and again on every reassignment by the
owner.

### 4. Wire service and refresh

```javascript
import { LightningElement, api, wire } from 'lwc';
import { getRecord, getFieldValue } from 'lightning/uiRecordApi';
import NAME_FIELD from '@salesforce/schema/Account.Name';
import RATING_FIELD from '@salesforce/schema/Account.Rating';
import getOpenCases from '@salesforce/apex/AccountCaseController.getOpenCases';
import { refreshApex } from '@salesforce/apex';

export default class AccountCard extends LightningElement {
    @api recordId;
    wiredCases;
    error;

    @wire(getRecord, { recordId: '$recordId', fields: [NAME_FIELD, RATING_FIELD] })
    account;

    @wire(getOpenCases, { accountId: '$recordId' })
    handleCases(result) {
        this.wiredCases = result;            // keep the whole result for refreshApex
        const { data, error } = result;
        this.error = error ? this.reduce(error) : undefined;
    }

    get accountName() {
        return getFieldValue(this.account.data, NAME_FIELD);
    }

    async refresh() {
        await refreshApex(this.wiredCases);
    }

    reduce(error) {
        return error?.body?.message ?? error?.body?.pageErrors?.[0]?.message ?? 'Unknown error';
    }
}
```

`$recordId` makes the configuration dynamic: when `recordId` changes, the adapter re-provisions.
`refreshApex` takes the value provisioned by an Apex `@wire` (the whole result object, not
`result.data`). Never mutate a wire configuration property inside `renderedCallback()`; that is an
infinite-loop generator.

### 5. Imperative Apex and error shape

```javascript
import escalate from '@salesforce/apex/CaseEscalationService.escalate';
import { notifyRecordUpdateAvailable } from 'lightning/uiRecordApi';
import { ShowToastEvent } from 'lightning/platformShowToastEvent';

async handleEscalate() {
    this.busy = true;
    try {
        await escalate({ caseId: this.recordId, reason: this.reason });
        await notifyRecordUpdateAvailable([{ recordId: this.recordId }]);
        this.dispatchEvent(new ShowToastEvent({
            title: 'Escalated', message: 'Case escalated to tier 2.', variant: 'success'
        }));
    } catch (error) {
        this.dispatchEvent(new ShowToastEvent({
            title: 'Escalation failed', message: this.reduce(error), variant: 'error', mode: 'sticky'
        }));
    } finally {
        this.busy = false;
    }
}
```

Apex errors reach JavaScript as `{ body: { message } }` for `AuraHandledException`, and as
`{ body: { pageErrors: [], fieldErrors: {}, output: {...} } }` for DML/record errors from LDS. Always
reduce defensively - see `references/data-access-patterns.md` for a complete `reduceErrors` helper.

### 6. Events: child to parent, and cross-tree

```javascript
// child: selector.js
handleSelect(event) {
    this.dispatchEvent(new CustomEvent('rowselect', {
        detail: { recordId: event.currentTarget.dataset.id }   // primitives only
    }));
}
```

```html
<!-- parent -->
<c-selector onrowselect={handleRowSelect}></c-selector>
```

Defaults are `bubbles: false, composed: false`: the event stops at the component boundary, which is
what you want for parent/child. Use `{ bubbles: true, composed: true }` only for genuinely
application-level events, and never put mutable objects in `detail`. For sibling or cross-DOM
communication use Lightning Message Service, not a home-grown pubsub module:

```javascript
import { LightningElement, wire } from 'lwc';
import { publish, subscribe, unsubscribe, MessageContext, APPLICATION_SCOPE } from 'lightning/messageService';
import RECORD_SELECTED from '@salesforce/messageChannel/Record_Selected__c';

export default class ListPanel extends LightningElement {
    @wire(MessageContext) messageContext;
    subscription;

    connectedCallback() {
        this.subscription = subscribe(this.messageContext, RECORD_SELECTED,
            (message) => { this.selectedId = message.recordId; },
            { scope: APPLICATION_SCOPE });
    }
    disconnectedCallback() { unsubscribe(this.subscription); this.subscription = null; }
    select(id) { publish(this.messageContext, RECORD_SELECTED, { recordId: id }); }
}
```

### 7. Lifecycle hooks

| Hook | Fires | Safe to do | Never do |
| --- | --- | --- | --- |
| `constructor()` | Once, before insertion | Call `super()` first, set non-DOM defaults | Touch `this.template`, read `@api` values |
| `connectedCallback()` | On DOM insertion, parent to child | Subscribe (LMS, message bus), read `@api` props, kick off imperative calls | Assume children rendered |
| `render()` | Before each render | Return an imported template for multi-template components | Side effects |
| `renderedCallback()` | After every render, child to parent | One-time third-party init guarded by a boolean, imperative DOM reads | Mutate `@api`/wire-config props (infinite loop) |
| `disconnectedCallback()` | On DOM removal | `unsubscribe`, `clearInterval`, abort fetches | Assume it runs on tab close |
| `errorCallback(error, stack)` | Child throws in lifecycle/render | Render a fallback, log | Swallow silently |

### 8. Templates

```html
<template>
    <template lwc:if={hasRows}>
        <ul>
            <template for:each={rows} for:item="row" for:index="i">
                <li key={row.id} data-id={row.id} onclick={handleSelect}>{row.name}</li>
            </template>
        </ul>
    </template>
    <template lwc:elseif={loading}><lightning-spinner alternative-text="Loading"></lightning-spinner></template>
    <template lwc:else><p>No results.</p></template>

    <ul>
        <template iterator:it={rows}>
            <li key={it.value.id} class={it.first}>{it.value.name}</li>
        </template>
    </ul>

    <input lwc:ref="firstInput" type="text" />
    <div lwc:dom="manual" class="chart"></div>
    <slot name="footer"></slot>
</template>
```

`lwc:if`/`lwc:elseif`/`lwc:else` supersede `if:true`/`if:false`; they cannot be combined on the same
element, and `lwc:elseif`/`lwc:else` must immediately follow their sibling. Expressions support only
simple dot notation - anything else goes in a getter. `key` is required on the first element inside
`for:each`/`iterator:` and must be a stable business id, never the index. Access refs with
`this.refs.firstInput` (do not use `lwc:ref` inside `for:each`).

### 9. Styling, shadow DOM, and light DOM

```css
:host {
    --slds-c-card-color-background: var(--slds-g-color-surface-1);
    display: block;
}
:host(.compact) .row { padding: 0; }
lightning-input { --slds-c-input-color-border: var(--slds-g-color-border-accent-1); }
```

Style with SLDS utility classes and SLDS styling hooks (CSS custom properties); do not reach across
the shadow boundary with descendant selectors - it does not work and will not be supported. Opt into
light DOM only when a third-party library or global stylesheet must see your markup:

```javascript
export default class LightPanel extends LightningElement {
    static renderMode = 'light';   // template must declare <template lwc:render-mode="light">
    renderedCallback() { this.querySelector('.chart'); } // light DOM: no shadowRoot
}
```

Light DOM gives up style scoping and event retargeting - state the reason in a code comment.

### 10. Navigation, toasts, labels, static resources

```javascript
import { NavigationMixin } from 'lightning/navigation';
import { loadScript, loadStyle } from 'lightning/platformResourceLoader';
import CHARTJS from '@salesforce/resourceUrl/chartjs';
import LABEL_ESCALATE from '@salesforce/label/c.Escalate_Case';
import LANG from '@salesforce/i18n/lang';

export default class Panel extends NavigationMixin(LightningElement) {
    label = { escalate: LABEL_ESCALATE };
    lang = LANG;
    chartInitialized = false;

    goToRecord(recordId) {
        this[NavigationMixin.Navigate]({
            type: 'standard__recordPage',
            attributes: { recordId, objectApiName: 'Case', actionName: 'view' }
        });
    }

    async renderedCallback() {
        if (this.chartInitialized) return;
        this.chartInitialized = true;
        await loadStyle(this, `${CHARTJS}/chart.css`);
        await loadScript(this, `${CHARTJS}/chart.umd.js`);
        this.renderChart();
    }
}
```

Never hardcode user-facing strings: import custom labels via `@salesforce/label/c.Name` and locale
data via `@salesforce/i18n/*`. Third-party JS must live in a static resource and load through
`lightning/platformResourceLoader`; CDN script tags are blocked by CSP.

## Anti-patterns

| Anti-pattern | Why it fails | Fix |
| --- | --- | --- |
| `this.filters.status = 'x'` on an untracked object and expecting a rerender | Field was not reassigned; no mutation detected | `this.filters = { ...this.filters, status: 'x' }` |
| `@track` on every field | Deep proxying cost with no benefit; fields are already reactive | Remove; use `@track` only for in-place mutation |
| Setting a wired config property inside `renderedCallback()` | Re-provision triggers rerender triggers hook: infinite loop | Set it in `connectedCallback()` or a handler |
| `@AuraEnabled(cacheable=true)` on a method that performs DML | Runtime error; cacheable methods cannot write | Split into a cacheable read and a non-cacheable write |
| Calling an imperative Apex writer and expecting `@wire(getRecord)` to update | LDS does not know the record changed | `await notifyRecordUpdateAvailable([{recordId}])` |
| `new CustomEvent('select', { bubbles: true, composed: true })` for a parent handler | Leaks the event to the whole page; breaks encapsulation | Default (`bubbles: false`) and handle on the child tag |
| Custom `pubsub.js` module for sibling communication | Not supported across DOM trees or Aura/Visualforce; leaks subscriptions | Lightning Message Service with `MessageContext` and `unsubscribe` |
| `element.shadowRoot.querySelector` from a parent component | Breaks encapsulation; blocked/locked at runtime | `@api` method or event |
| `key={index}` in `for:each` | Diffing reuses the wrong nodes on reorder | `key={row.id}` |
| `console.log` left in shipped components | Leaks data to the browser console in production | Remove; `vf-check lint` flags `no-console` |
| Building a form with 12 `lightning-input` fields plus manual DML | Reimplements field-level security, layouts, and validation | `lightning-record-edit-form` or `lightning-record-form` |
| CDN `<script src>` or inline `<script>` | Blocked by CSP and Lightning Web Security | Static resource + `loadScript` |

## Verification

```bash
# LWC unit tests and coverage (no org needed)
node "${CLAUDE_PLUGIN_ROOT}/scripts/checks/vf-check.mjs" jest --changed

# Full local gate: prettier + eslint + Code Analyzer + jest
node "${CLAUDE_PLUGIN_ROOT}/scripts/checks/vf-check.mjs" local --changed

# Live preview of the component against a scratch org (no deploy)
sf lightning dev component --name accountCard --target-org vf-dev

# Validate the bundle compiles server-side before deploying
sf project deploy start --source-dir force-app/main/default/lwc/accountCard \
  --dry-run --target-org vf-dev

# Deploy, then verify in the org
sf project deploy start --source-dir force-app/main/default/lwc/accountCard --target-org vf-dev
sf org open --path lightning/n/Account_Console --target-org vf-dev
```

Gates that apply to LWC work: `requireJestForLwc` (every bundle needs `__tests__`), `jestCoverageMin`
80, and `analyzerFailSeverity` 3. See skills `sf-lwc-jest-testing`, `sf-code-analyzer-quality`, and
`sf-post-deploy-verification`.

## References

- [`references/component-reference.md`](references/component-reference.md) - decorators, lifecycle hooks, every template directive, `js-meta.xml` targets, `@salesforce/*` module table.
- [`references/data-access-patterns.md`](references/data-access-patterns.md) - wire vs imperative vs LDS matrix, GraphQL wire adapter, `reduceErrors`, record-form components.
- [`references/events-and-messaging.md`](references/events-and-messaging.md) - CustomEvent propagation matrix, LMS setup, parent/child patterns, Aura/Visualforce interop.
- [`references/mcp-and-skills.md`](references/mcp-and-skills.md) - `lwc-experts`, `aura-experts` and `experts-validation` toolsets, per-tool GA status, the LWC skills that superseded them, and the checklist for accepting generated code.
- [`references/lwc-recipes-catalog.md`](references/lwc-recipes-catalog.md) - curated runnable patterns mapped to `trailheadapps/lwc-recipes`.
- Official: [Lightning Web Components Developer Guide](https://developer.salesforce.com/docs/platform/lwc/guide/introduction.html), [Lifecycle Hooks](https://developer.salesforce.com/docs/platform/lwc/guide/create-lifecycle-hooks.html), [renderedCallback()](https://developer.salesforce.com/docs/platform/lwc/guide/create-lifecycle-hooks-rendered.html), [XML Configuration File Elements](https://developer.salesforce.com/docs/platform/lwc/guide/reference-configuration-tags.html), [notifyRecordUpdateAvailable](https://developer.salesforce.com/docs/platform/lwc/guide/reference-notify-record-update.html), [Lightning Message Service](https://developer.salesforce.com/docs/platform/lightning-component-reference/guide/lightning-message-service.html), [Lightning Web Security](https://developer.salesforce.com/docs/platform/lightning-components-security/guide/lws-intro.html).
