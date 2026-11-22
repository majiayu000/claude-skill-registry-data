---
name: cart
description: Create, design, compose, preview and manage Lexsis cart profiles. Edit promotion drafts, inspect readiness, and publish exact approved versions. Supports custom module state, commands and conditional visibility.
---

# Configure a Cart

Cart profiles are managed separately from page section HTML.

Use `lexsis_cart.get`, `lexsis_cart.capabilities`,
`lexsis_cart.promotions`, and `lexsis_cart.preview`. When requested, use
`lexsis_drafts.cart_set`, `cart_edit`, and `cart_promotions_edit`. Profile lifecycle
actions are listed below. Resolve unfamiliar
argument schemas with exact router/action discovery. An empty discovery result
is not a cart outage; the actual cart call determines availability. Do not
infer the effective cart profile from page HTML.

Resolve the target store from a page binding, an explicit saved choice, or the
unambiguous default in `work/storefront/setup/setup.json`. If it is not saved,
stop and ask the user to run `/setup`; never invoke setup automatically.

## References

- `references/cart-composition.md`: ownership, placement, IDs and patch semantics
- `references/module-authoring.md`: lifecycle, commands and a complete upsell
- `references/styling-hooks.md`: shell/island parts and inline-style exceptions
- `references/cart-profile-management.md`: lifecycle, promotions and previews

Natural-language discovery returns at most 10 ranked matches by default, with
schemas for the top 3. Use `include_schema:true` for all returned schemas,
`limit`/`offset` to page, or exact router/action for one schema.
`lexsis_cart.promotions` accepts `cart_profile_id` alone; the store is inferred.
Transient upstream failures return `UPSTREAM_UNAVAILABLE` with top-level
`retryable:true` and `retry_after_s`. Before retrying a write, re-read its version
and history because a lost response does not prove the write failed.

## Rules

- A page enables the cart through its supported page configuration; do not add
  DrawerShell or cart-line markup to page sections.
- Effective profile order is page assignment, campaign assignment, store
  default, then legacy fallback.
- Draft edits are not live until the exact version is explicitly approved and
  published through `lexsis_live_ops.cart_publish` or the app.
- Do not invent products, prices, currencies, offers, or selling plans.
- Promotion, offer, threshold, coupon, payment and rule edits use
  `lexsis_drafts.cart_promotions_edit`. Shopify writes happen only at publish.
- Defaults, campaign/page assignment and archive with reassignment change live
  resolution. Obtain explicit approval and use publish access for these writes.
- Rollback restores a forward draft; it does not publish.
- Custom modules use the same Lexsis source format as normal pages: HTML,
  `<style>`, section `<script>`, managed motion, and registered `<lx-island>`
  components. Cart lines, order summary, checkout, and DrawerShell remain
  renderer-owned.

## Workflow

1. Call `lexsis_cart.get`.
   - Use `page_id` to inspect the effective profile and resolution source.
   - Use `cart_profile_id` to inspect an editable profile.
   - Use `store_id` to list profiles.
2. Call `lexsis_cart.capabilities` before the first design or composition edit
   in a task. Resolve island props through `lexsis_design.island_schema`.
3. Before adding or changing milestone rewards, pick exactly one reward mode
   with "Choosing a reward mode" in `references/cart-profile-management.md`:
   third-party checkout or an app that already gives the gift -> `external`;
   Shopify checkout on the public Lexsis app needing replacing tiers ->
   `whole_cart` Function (never on enterprise/custom apps: no Function ships);
   otherwise native codes. Make any custom milestone copy match that mode, keep
   one progress bar, and for `external` confirm the real checkout gives the
   same gift before publishing.
   For discounts or offers, call `lexsis_cart.promotions` and report the
   configured profile values, active Shopify discounts, and readiness or
   conflict diagnostics. Apply requested changes with `cart_promotions_edit`,
   using the latest `expected_version`, then review the returned readiness.
4. When requested, assign a published profile with
   `lexsis_drafts` action `cart_set`. Passing a null profile removes the page
   assignment.
5. Edit a draft with `lexsis_drafts` action `cart_edit` and a partial patch.
   Supported areas are cart mode, typed design settings, responsive
   presentation, scoped custom CSS, and composition operations.
   - `upsert` adds or replaces one custom module from one source section.
     Omit source to change `visible_when` on an existing custom or optional
     built-in module; pass `visible_when: null` to clear the rule.
   - `move` reorders a module within its header, body, or footer region.
   - `set_enabled` toggles custom or optional modules.
   - `remove` deletes only custom modules.
   - Use `before_module_id: "checkout"` and `region: "footer"` for a block
     immediately above checkout.
6. Responses default to compact summaries. Re-read needed fields with
   `lexsis_cart.get` using `fields:["version","design_spec","layout_schema"]`,
   or `response:"full"` for all source. Use `dry_run:true` on `cart_edit` to
   compile before saving: no version or audit write, and a signed preview URL.
7. Call `lexsis_cart.preview` with `page_id`, `cart_profile_id` and
   `fixture:"all_unlocked"` (or another named state). Omit `page_id` for an
   isolated preview. The URL expires after 15 minutes. For all six URLs,
   snapshots, visibility and static checks, call `lexsis_cart.preview_states`.
   Lexsis starts no browser; open returned URLs in your own browser and inspect
   mobile/desktop. Sample carts are in memory, block checkout and never touch
   `lx_cartId`. Computed estimates do not prove Shopify discount readiness.

Use real catalog and review data in custom modules. For example, a rotating
review strip above checkout should use `ReviewCarousel` with an active review
collection or merchant-confirmed reviews; never fabricate quotes or ratings.
Cart triggers dispatch `cart:open`; they do not need a profile ID.

`design_patch` is JSON Merge Patch: omitted fields remain, null removes an
override and arrays replace arrays. A source-bearing `upsert` replaces the
whole module source, including its CSS and script. `data-module` is the layout
ID; `data-module-type` is the layout type (for example `product_offer`).

Custom CSS must remain scoped to the cart. External imports, remote URLs,
script escapes, and unbalanced rules are not allowed.

## Cheap edit examples

All arguments below belong inside the router's `args`.

Compile a title before saving with `lexsis_drafts.cart_edit`:

```json
{
  "cart_profile_id": "PROFILE_UUID", "expected_version": 12,
  "page_id": "PAGE_UUID", "dry_run": true,
  "patch": {"design_patch": {"shell": {"title": "Your cart"}}}
}
```

Inspect `module_tree`, `compile_errors`, `warnings` and the temporary
`preview_url`. Repeat with `dry_run:false` to save the reviewed patch. A stale
version still fails. Default writes return version, changed fields, bounded
warnings, URL and readiness summary; `response:"full"` opts into full source.
If `preview_error` says the draft saved, retry preview only.

Edit one named CSS block:

```json
{
  "cart_profile_id": "PROFILE_UUID", "expected_version": 12,
  "patch": {"css_ops": [
    {"op": "upsert", "id": "checkout", "css": "[data-part=\"checkout\"] { font-weight: 700; }"}
  ]}
}
```

`custom_css` replaces **all** CSS and named blocks; null clears them. Never
resend it for a one-block change. `css_ops` retains insertion order, imports
old CSS as `legacy` on first use, and supports remove by existing ID. Do not
combine the two mechanisms.

Preview a saved state with `lexsis_cart.preview`:

```json
{
  "page_id": "PAGE_UUID", "cart_profile_id": "PROFILE_UUID",
  "fixture": "all_unlocked"
}
```

Named states are empty, below_first_reward, between_rewards, all_unlocked,
gift_chosen and code_applied. Explicit fixtures use
`{lines:[{variantId,quantity,sellingPlanId?}],codes?:[]}` with verified catalogue
GIDs, up to 12 lines and 10 codes. Source is currently `computed`; warn on
unavailable tiers/catalogue scopes. Unready rewards may be simulated for design
review but remain flagged and cannot authorize publication.

Request all states with `lexsis_cart.preview_states` and
`{page_id:"PAGE_UUID",cart_profile_id:"PROFILE_UUID"}`. Static reports cover
configured color contrast, ineffective settings, shown unready rewards,
compile errors and checkout links. They contain no screenshots or DOM/layout
measurements. Open the URLs in your existing browser for visual proof. A
missing sample badge plus `fixture_invalid` means normal cart fallback; mint
a new URL before interacting with the cart.

Request a small schema with `lexsis_design.island_schema` and
`{name:"CartRewardProgress",fields:["rewards","visuals"],verbose:false}`.
Defaults return a compact overview; `expand:true` marks omitted nested detail.
Repeated icons use `$defs.iconName`. Use `verbose:true` for styling and examples.

## Lifecycle example

Read `references/cart-profile-management.md` for exact schemas and failure handling.
A complete cycle uses these router actions (parameters shown inside `args`):

1. `lexsis_drafts.cart_create` with `{store_id, name, from_preset:"default"}`.
   Alternatively use `from_profile_id`, or `lexsis_drafts.cart_duplicate` with `{cart_profile_id,name}`.
2. `cart_edit` for design, with the returned `expected_version`.
3. `cart_promotions_edit` for a partial, ID-addressed draft patch:

```json
{
  "cart_profile_id": "PROFILE_UUID",
  "expected_version": 2,
  "patch": {
    "rewards": [{
      "id": "shipping", "type": "free_shipping", "title": "Free shipping",
      "threshold": 150000, "discount_source": "managed", "enabled": true
    }],
    "payment_settings": {"placement": "below_checkout", "providers": ["visa", "mastercard"]}
  }
}
```

Use the store's real minor currency units: 150000 is ₹1,500 in INR. Gift products,
variants and qualifying products/collections must use verified catalog IDs.
Omitted rows remain; remove one with `{id,operation:"remove"}`. Empty patch arrays
do not clear a collection. Coupons/providers replace their nested ordered lists.

4. Re-read and call `lexsis_cart.preview`; inspect mobile/desktop and applicable
   empty, populated and reward states.
5. Obtain explicit approval of the exact draft, then call
   `lexsis_live_ops.cart_publish` with `{cart_profile_id,expected_version,allow_partial:false,skip_reward_ids:[]}`.
   `CART_NOT_READY` returns issues; `VERSION_CONFLICT` requires re-reading and
   approving the current draft. With partial approval, list the exact rewards
   to disable in `skip_reward_ids`; unskipped/global issues still block publication.
6. To restore, call `lexsis_live_ops.cart_rollback` with `{cart_profile_id,target_version}`.
   Preview and separately approve publication of the new forward draft.

Default: `lexsis_live_ops.cart_set_default` with `{store_id,cart_profile_id}`.
Campaign: `lexsis_drafts.cart_assign_campaign` with `{campaign_id,cart_profile_id}`;
null clears the override. These change live resolution even though campaign
assignment is grouped under drafts.

Archive: `lexsis_drafts.cart_archive` with `{cart_profile_id}`. If default or assigned,
provide an explicitly approved published `reassign_to` in the same store.
History: `lexsis_cart.get` with `{cart_profile_id,include_history:true}` returns
actor, MCP client and changed-field summaries.

Shopify failure leaves the previous published pointer live and triggers
compensation. `CART_PUBLISH_RECOVERY_REQUIRED` means cleanup could not be verified:
report its recovery details and resolve them before retrying. Never claim a
failed or uncertain publish succeeded.

## Custom module examples

Read `capabilities.snapshot_schema`, `commands`, and `conditions` first.
Money has decimal `amount`, `currencyCode`, and integer `minor`. Never supply
a fallback currency. Snapshot amounts share CartSummary's confirmed selectors.
`lifecycle.cart` is deeply frozen. Use `onCart` during initialization: it waits
for currency/prices and settlement, calls at most once per frame, and cleans up
on unmount. The getter reports pending status with confirmed merchandise values
while a mutation runs.

### Read live gift remaining

Use this single section as `composition_ops[].source`. Its reward comes from
the existing profile, not a hardcoded threshold or invented gift.

```html
<!-- section: gift-remaining -->
<section>
  <p data-gift-message hidden>Only <strong data-remaining></strong> to go for your gift.</p>
  <script>
    lifecycle.onCart((cart, previous) => {
      const next = cart.rewards.next;
      lifecycle.query('[data-gift-message]').hidden = !next;
      lifecycle.query('[data-remaining]').textContent = next
        ? new Intl.NumberFormat(cart.context.locale || undefined, {
            style: 'currency', currency: next.remaining.currencyCode
          }).format(Number(next.remaining.amount))
        : '';
    });
  </script>
</section>
```

### Send a managed command

Every command uses a unique request ID and bubbles from `section`; responses
return to this module. Replaying the identical request returns its terminal
response without another write. The eight additional commands are
`update-line`, `remove-line`, `apply-code`, `remove-code`, `set-attributes`,
`set-note`, `choose-gift`, and `swap-variant`, all prefixed `lx:cart:`.
Read their exact limits and payloads in capabilities.

```html
<!-- section: cart-note -->
<section>
  <label>Order note <textarea data-note maxlength="5000"></textarea></label>
  <button type="button" data-lx-control="save-note">Save note</button>
  <span data-result role="status"></span>
  <script>
    let sequence = 0;
    lifecycle.on(lifecycle.query('[data-lx-control="save-note"]'), 'click', () => {
      section.dispatchEvent(new CustomEvent('lx:cart:set-note', {
        bubbles: true,
        detail: {
          requestId: 'note-' + Date.now() + '-' + (++sequence),
          note: lifecycle.query('[data-note]').value
        }
      }));
    });
    lifecycle.on(section, 'lx:cart:set-note:success', () => {
      lifecycle.query('[data-result]').textContent = 'Note saved';
    });
    lifecycle.on(section, 'lx:cart:set-note:error', (event) => {
      lifecycle.query('[data-result]').textContent = event.detail.message;
    });
  </script>
</section>
```

Success waits for settlement; pending/accepted/confirmed are intermediate
phases. Shopper code application and gift selection do not change promotion
configuration. Gift IDs and variants must come from the configured profile.
An AJAX variant swap can return `partial_swap` if only the replacement add
succeeded; show the error and current cart, never blindly replay a new add.

### Hide a module on an empty cart

Use the actual module ID from `cart.get`. This example updates an existing
payment module without replacing its renderer-owned source:

```json
{
  "operation": "upsert",
  "module_id": "payment-options",
  "visible_when": {
    "op": "AND",
    "clauses": [{"field": "cart.item_count", "op": "gt", "value": 0}]
  }
}
```

The same `visible_when` works on custom modules and offers. To hide an upsell
after its variant is added, use `cart.has_variant_id`, `op: "neq"`, and the
real ProductVariant GID as `value`. Hidden content leaves the accessibility
tree; it updates without a reload. Required cart modules cannot be hidden.
Money conditions use minor units. Customer flags default false without a host
session provider; tags/collections depend on available Shopify metadata.

### Bind simple content without JavaScript

```html
<!-- section: gift-binding -->
<section>
  <p data-lx-if="rewards.next.remaining.minor &gt; 0">
    Only <strong data-lx-text="rewards.next.remaining"></strong> to go.
  </p>
</section>
```

Conditions also accept comparisons, `!`, `&&`, `||`, parentheses and predicates
such as `!reward.unlocked('REAL_REWARD_ID')`. Unknown paths/functions are rejected
by the compiler. Money text uses the real snapshot currency. No `window` or
`document` access is needed.

## Return

Report the effective profile, resolution source, composition and design
changes, promotion diagnostics, preview URL/evidence, page assignment, and
which actions still require review or publication in Lexsis.
