---
name: gtm-web-container-and-datalayer
description: Design and implement the client-side Google Tag Manager web container and the dataLayer contract that feeds every downstream tag. Use when the user asks about installing GTM, the GTM container snippet, dataLayer, dataLayer.push, dataLayer init order, an ecommerce dataLayer, the ecommerce items array, built-in variables, Data Layer variables vs custom JS, event names, gtm.js/gtm.dom/gtm.load, or why a tag reads empty or stale dataLayer values.
---

# GTM web container and dataLayer

Stand up the client-side Google Tag Manager web container and define the dataLayer contract that every tag on the page reads from. The dataLayer is the single structured handoff between the site and GTM: the developers write to it, and tags, triggers, and variables read from it. Get this contract right and every downstream tag (GA4, Google Ads, Floodlight) reads clean, consistent values. Get it wrong and every tag inherits the same missing, mistyped, or stale data.

This skill assumes you know what a tag, trigger, and variable are and what a CPM or conversion is. For KPI math see the `programmatic-foundations` skill.

## When to use this skill

- "How do I install GTM / where does the container snippet go?"
- "Design our dataLayer" / "What should the dataLayer look like?"
- "Build the ecommerce dataLayer" / "purchase / add_to_cart / view_item events."
- "dataLayer.push isn't working" / "my variable reads undefined or the old value."
- "Should this be a Data Layer variable, a custom JavaScript variable, or a built-in variable?"
- "What is gtm.js / gtm.dom / gtm.load / gtm.uniqueEventId?"
- "Enable built-in variables" / "Client ID / Session ID as a variable."

Boundaries with sibling skills:
- Building the actual GA4, Google Ads, and Floodlight tags, triggers, and variables on top of this dataLayer: `gtm-tags-triggers-variables`.
- Consent Mode v2 signals, default/update ordering, and modeling eligibility: `gtm-consent-mode-v2`.
- Moving collection to a tagging server on Cloud Run, clients, and the transport URL: `gtm-server-side-tagging`.
- The GA4 event data model and marking key events: `ga4-events-and-key-events`.
- Where GA4 sits and its data streams: `ga4-property-and-data-stream-setup`.

This skill owns the web container install and the dataLayer schema. Everything that reads from the dataLayer belongs to a sibling.

## Quick reference

| Question | Answer | Why |
| --- | --- | --- |
| Where does the container snippet go? | `<head>` snippet as high as possible; `<noscript>` iframe right after `<body>` | GTM must load before the tags it fires depend on |
| Init the dataLayer before or after the snippet? | Before, in a script above the container snippet | Values pushed after the snippet arrive too late for page-load tags |
| Push data or set a variable? | Always `dataLayer.push({...})`, never assign to `dataLayer` directly | Direct assignment overwrites the array and drops earlier state |
| One-time page context vs an interaction | Static context above the snippet; interactions via `push` with an `event` key | The `event` key is what fires triggers |
| Ecommerce shape | `ecommerce` object with an `items` array, GA4 event names | GA4 and the ecommerce built-in variables expect this exact shape |
| Read a dataLayer value in GTM | Data Layer Variable with the exact dot-path key | It reads the merged dataLayer state at trigger time |
| Client ID / Session ID as a variable | Built-in Utilities variables (added Dec 2025) | Officially supported, no custom JS needed |

## Core process

1. Initialize the dataLayer before the container snippet, so page-context values exist when GTM loads. Put `window.dataLayer = window.dataLayer || [];` and the initial `dataLayer.push({...})` of static page context in a script that runs above the GTM snippet in the `<head>`. Pushing after the snippet means load-time tags fire before the data lands.
2. Install the container snippet. The `<script>` part goes as high in the `<head>` as possible; the `<noscript>` iframe goes immediately after the opening `<body>` tag. Use one container per site unless you have a hard reason to split. The container ID looks like `GTM-XXXXXXX`.
3. Define the dataLayer schema as a contract, not ad hoc pushes. Name every key once, fix its type (string, number, array), and document it. Downstream Data Layer Variables reference these keys by exact dot-path, so a rename or a type flip silently breaks every tag that reads it. The field map lives in `references/datalayer-init-and-push-model.md`.
4. Push interactions with an `event` key. `dataLayer.push({ 'event': 'add_to_cart', ... })` is what fires a Custom Event trigger. Static context (page type, logged-in state) does not need an `event`; behavioral interactions do. Keep event names in a controlled vocabulary so triggers stay predictable.
5. Model ecommerce with the GA4 shape. Use the recommended event names (`view_item`, `add_to_cart`, `begin_checkout`, `purchase`) and an `ecommerce` object containing an `items` array. Clear stale ecommerce state with a `dataLayer.push({ ecommerce: null })` before each new ecommerce push so items do not leak between events. Full schema in `references/ecommerce-datalayer-schema.md`.
6. Enable the built-in variables you need and prefer them over custom JavaScript. Built-in variables (Page, Click, Form, Scroll, and the Dec 2025 Utilities additions Client ID, Session ID, Session Number) are maintained by Google and cheaper than hand-rolled JS. Reference in `references/2025-builtin-variables.md`.
7. Validate in Preview before publishing. Preview mode shows, per event, which tags fired and what every variable resolved to. Confirm the dataLayer holds the expected keys and types on each event, then publish. Never publish a container change straight to production without a Preview pass. Publishing is a live-config change: treat it as a human-gated step.

## Decision rules and thresholds

### dataLayer init ordering (the rule that breaks the most setups)

- Static page context (page_type, user_id, content_group) must be pushed above the container snippet. If it is pushed later, load-time tags read `undefined`.
- Never assign `dataLayer = [...]` or `dataLayer = {...}`. Always `dataLayer.push(...)`. Direct assignment replaces the array object GTM is holding a reference to and orphans all prior state and listeners.
- The dataLayer is a running merge. A `push` merges shallowly over prior state, so once you push `user_id`, it stays set for later events unless you overwrite it. This is why ecommerce needs an explicit `ecommerce: null` reset.

### Push vs set vs get

- `dataLayer.push({key: value})` is the normal write. Use it for both static context and events.
- `dataLayer.push(function() { this.set('k', v); })` sets a value via the abstract data layer API. `this.get('k')` reads current merged state, `this.reset()` clears it. Reserve these for rare cases; plain object pushes cover almost everything.
- The `event` key triggers Custom Event triggers. Reserve it for actual interactions so you do not fire triggers on static pushes.

### Reserved names to not collide with

- Keys under `gtm` (for example `gtm.uniqueEventId`, `gtm.start`) are written by GTM. Do not push your own values into `gtm.*`.
- The auto-fired events `gtm.js` (container loaded), `gtm.dom` (DOM ready), and `gtm.load` (window load) drive the built-in Page View, DOM Ready, and Window Loaded triggers. Do not push these event names yourself.
- `gtm.uniqueEventId` increments per push and is how GTM keeps each event distinct. Custom JS that reads dataLayer state should account for it.

### Variable type: which one to reach for

- Reading a key the developers push: Data Layer Variable with the exact key path.
- A property of the page GTM already knows (URL, referrer, click element, form): a built-in variable.
- A computed value not in the dataLayer and not a page property: Custom JavaScript variable, last resort, because it runs on every evaluation and is yours to maintain.
- Client ID, Session ID, Session Number: the Dec 2025 built-in Utilities variables, not custom JS.

### Data Layer Variable version and defaults

- Data Layer Variables read the merged state at evaluation time. Set a Default Value so a missing key resolves predictably instead of `undefined`, which downstream tags may send as a literal string.
- For nested keys use dot notation in the variable name, for example `ecommerce.items.0.item_id`.

### Container and API limits worth knowing

- The Tag Manager API v2 quota is 10,000 requests per project per day and 0.25 queries per second per project (25 requests per 100 seconds), enforced on a 100 second sliding window. Programmatic container edits must throttle to this. Details in `references/2025-builtin-variables.md`.
- Prefer one web container per site. Multiple containers on a page multiply load cost and make debugging harder.

## Reference material

- `references/datalayer-init-and-push-model.md`: the init-before-snippet pattern, the push vs set/get/reset model, reserved `gtm.*` keys, the gtm.js/gtm.dom/gtm.load lifecycle, a recommended core-context field map (page_type, user_id, content_group, consent snapshot), and Data Layer Variable resolution rules. Read this when defining the dataLayer contract or debugging a variable that reads empty or stale.
- `references/ecommerce-datalayer-schema.md`: the full GA4 ecommerce dataLayer, every recommended event (`view_item`, `select_item`, `add_to_cart`, `begin_checkout`, `add_payment_info`, `purchase`, `refund`), the `items` array field map, the `ecommerce: null` reset pattern, and worked pushes with real values. Read this when building or auditing ecommerce tracking.
- `references/2025-builtin-variables.md`: the built-in variable catalog by category (Pages, Utilities, Errors, Clicks, Forms, History, Scroll, Video, Visibility, Consent), the Dec 2025 Utilities additions (Client ID, Session ID, Session Number), enablement steps, and the API v2 quota table for programmatic edits. Read this when choosing a variable type or automating container changes.

## Templates and examples

Init block, above the container snippet, static page context first:

```html
<script>
  window.dataLayer = window.dataLayer || [];
  window.dataLayer.push({
    'page_type': 'product',
    'user_id': 'u_84213',
    'logged_in': true,
    'content_group': 'apparel/mens/jackets'
  });
</script>
<!-- Google Tag Manager container snippet goes below this block -->
```

Interaction push with an `event` key:

```javascript
dataLayer.push({
  'event': 'add_to_cart',
  'ecommerce': {
    'currency': 'USD',
    'value': 129.00,
    'items': [{
      'item_id': 'SKU_9931',
      'item_name': 'Waxed Field Jacket',
      'item_brand': 'Northbound',
      'item_category': 'apparel/mens/jackets',
      'price': 129.00,
      'quantity': 1
    }]
  }
});
```

Ecommerce reset before a new ecommerce event, so items do not leak:

```javascript
dataLayer.push({ ecommerce: null });
dataLayer.push({
  'event': 'purchase',
  'ecommerce': {
    'transaction_id': 'T_20260319_00417',
    'currency': 'USD',
    'value': 258.00,
    'tax': 21.30,
    'shipping': 9.95,
    'items': [ /* ... */ ]
  }
});
```

Data Layer Variable to read the value: variable name `ecommerce.value`, type Data Layer Variable, Default Value `0`.

## Common pitfalls

- Context pushed after the snippet. Load-time tags fire before the data lands, so GA4 page_view and the like read `undefined`. Push static context above the snippet.
- Assigning to dataLayer directly. `dataLayer = [{...}]` replaces the array and orphans all prior state and GTM's listeners. Always `push`.
- Stale ecommerce leaking between events. The dataLayer is a running merge, so a prior `items` array survives into the next event. Push `ecommerce: null` before each ecommerce event.
- Renaming or retyping a key. Every Data Layer Variable references the key by exact path and type, so a silent rename or a number-to-string flip breaks every reading tag. Treat the schema as a versioned contract.
- Custom JS where a built-in exists. Client ID and Session ID as hand-rolled JS were fragile; use the Dec 2025 built-in Utilities variables instead.
- Publishing without Preview. A container change is a live-config change. Confirm in Preview which tags fired and what each variable resolved to, then publish. Do not push straight to production.
- Missing Default Value. A Data Layer Variable with no default resolves `undefined`, which some tags send as the literal string "undefined". Set a sensible default.

## Sources

- [Data layer, Tag Platform developer guide](https://developers.google.com/tag-platform/tag-manager/datalayer) (as of July 2026)
- [Google Tag Manager release notes and built-in variables](https://support.google.com/tagmanager/answer/4620708?hl=en) (as of July 2026)
- [Tag Manager API v2 limits and quotas](https://developers.google.com/tag-platform/tag-manager/api/v2/limits-quotas) (as of July 2026)
- [Consent overview, Tag Platform](https://developers.google.com/tag-platform/security/guides/consent) (as of July 2026)
- [Send data to a server container](https://developers.google.com/tag-platform/tag-manager/server-side/send-data) (as of July 2026)
- [Google tag gateway for advertisers](https://developers.google.com/tag-platform/tag-manager/gateway) (as of July 2026)
- [Tag Manager API v2 overview](https://developers.google.com/tag-platform/tag-manager/api/v2) (as of July 2026)
