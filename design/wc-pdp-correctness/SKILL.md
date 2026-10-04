---
name: wc-pdp-correctness
description: WooCommerce product-detail-page and add-to-cart correctness for the skyyrose-flagship theme — AJAX contract, variation forms, stock states, cart fragments. Use when building, changing, or reviewing single-product templates, product cards, or any add-to-cart surface under wordpress-theme/skyyrose-flagship/. Do NOT use for WooCommerce core contributions (that is woocommerce-backend-dev) or for REST-API automation against the live store (that is wordpress-woocommerce-automation).
---

# WooCommerce PDP Correctness

Core-contribution style guides don't cover this. This checklist is for THEME add-to-cart surfaces —
where a broken button means zero revenue and no error log. Nothing fatals; the button just does
nothing.

## When to use

Fires on an observable event:

- You edited or are reviewing anything under
  `wordpress-theme/skyyrose-flagship/woocommerce/` (`single-product.php`, `content-product.php`,
  `archive-product.php`, `cart/`, `checkout/`).
- You edited a product card that renders an add-to-cart control —
  e.g. `template-parts/product-card-v7-lookbook.php`.
- You changed cart-related enqueues in `inc/enqueue.php`, or any JS that listens for
  `added_to_cart` / `wc_fragments_refreshed`.
- A report arrives that "add to cart does nothing", the cart badge is stale, or a variation picker
  is dead.

**Not for:** WooCommerce plugin/core PHP (use `woocommerce-backend-dev`), webhook receivers
(`woocommerce-webhooks`), bulk product writes over REST (`wordpress-woocommerce-automation`), or
pure CSS/visual polish (`theme-min-build` + `design-qc`).

## Inputs

Required before you start. If any is absent, **stop and get it — do not proceed on assumption**:

| Input | How to confirm | If absent |
|---|---|---|
| Theme working tree | `ls wordpress-theme/skyyrose-flagship/woocommerce/` | STOP — you are in the wrong checkout |
| Theme composer tooling | `ls wordpress-theme/skyyrose-flagship/vendor/bin/phpcs` | STOP — run `composer install` in the theme dir; do not skip phpcs |
| The specific template(s) you changed | `git diff --stat -- wordpress-theme/skyyrose-flagship` | STOP — an unscoped "PDP review" cannot be verified |
| A product to test against | catalog CSV `data/skyyrose-catalog.csv` (SOT) | STOP — never invent a SKU or product id |
| Browser access, for the interactive battery | Playwright / Chrome DevTools available | Do NOT mark those steps passed. They become a **SKIP with a named owner** (the caller runs them) |

Kids Capsule renders 0 cards **by design** (launch mode). That is not an input failure and is not a
bug to fix.

## Procedure

1. Read the current template before editing it. Quote `file:line` for anything you claim about it.
2. **Simple-product AJAX contract.** The button needs BOTH the class `ajax_add_to_cart` AND
   `data-product_id="<id>"` — `wc-add-to-cart.js` binds on the class and reads the data attribute.
   Missing either is a silent no-op. Also required: `data-quantity`, `rel="nofollow"` on anchors,
   and an `aria-label` naming the product.
3. **Never emit a bare `?add-to-cart=` GET href as the primary control.** Crawlers follow it and
   edge caches poison it. The href stays the permalink; the data attributes drive the add.
4. **Enqueues.** Depend on the registered `wc-add-to-cart` handle rather than re-implementing it —
   `WC_Frontend_Scripts::register_scripts()` registers it and `wc_add_to_cart_params` is
   auto-localized by `localize_printed_scripts()`.
5. **Fragments.** Custom mini-cart or count badges must listen for `added_to_cart` AND
   `wc_fragments_refreshed`, or counts go stale after the first add.
6. **Variable products.** They cannot use the simple-product AJAX path: the form posts
   `variation_id` plus every attribute field. A themed quick-add must open the variation form, or
   pass ALL required attributes — a partial attribute set produces a WC error notice, not an add.
   Keep `data-product_variations` JSON and the `woocommerce_variation_add_to_cart` hooks intact when
   restyling; stripping them kills the picker silently.
7. **Out-of-stock variations.** The form still renders; the button must disable on
   `found_variation` / `hide_variation`. Test one OOS combination explicitly.
8. **Purchasability and quantity.** Respect `$product->is_purchasable()` and `is_in_stock()`;
   pre-order and launch-mode products are non-purchasable on purpose. Take min/max/step from
   `woocommerce_quantity_input_args` — a custom stepper that ignores `max` oversells.
9. **Button states.** Style all of `default → .loading → .added → View cart` link. WooCommerce
   toggles those classes; if custom CSS styles only the default state, the button looks dead for the
   whole round-trip.
10. Run the Verification block below. Any CSS/JS you touched also needs `npm run build` in
    `wordpress-theme/` — production serves `.min`, so a source-only edit ships nothing.
11. Record anything surprising in `.wolf/buglog.json` with a fresh id from
    `python scripts/wolf_bug_id.py`.

## Verification

Run every CLI check. Each states its command, its pass condition, and the evidence tag it earns.

```bash
cd /Users/theceo/DevSkyy/.claude/worktrees/glimmering-crafting-shannon/wordpress-theme/skyyrose-flagship
php -l woocommerce/single-product.php   ### PASS: "No syntax errors detected"            [repro]
vendor/bin/phpcs --standard=.phpcs.xml woocommerce/single-product.php   ### PASS: exit 0, "1 / 1 (100%)", 0 errors   [repro]
grep -n 'ajax_add_to_cart' template-parts/product-card-v7-lookbook.php | grep -c 'data-product_id'   ### PASS: prints 1 (N == number of add buttons)   [repo]
cd .. && npm run verify:theme -- --only wc-support   ### PASS: aspect OK, exit 0          [test]
npm run build && npm run verify:theme -- --only min-sync   ### PASS: no stale .min, exit 0   [test]
curl -sI "https://skyyrose.co/?cb=$(date +%s)" | head -1   ### PASS: HTTP/2 200           [live]
```

What each one buys you: `php -l` — a fatal in a PDP template takes the whole page down.
`phpcs` — catches unescaped output on data attributes. The `grep` pair — the add-to-cart contract
asserted on the markup itself; class and `data-product_id` must sit on the SAME element.
`wc-support` — gallery zoom/lightbox/slider plus declared theme support. `min-sync` — shipped bytes
match source, because production serves `.min`. The `curl` — cache-busted, because Batcache serves
stale and WebFetch strips `<script>`.

Browser battery — these cannot run headless from this skill. **A SKIP is not a PASS**: report each
as SKIP and name the caller as owner, or run them under Playwright/Chrome DevTools yourself:

1. Simple product: click add → network shows `?wc-ajax=add_to_cart` 200 → cart count increments with
   no page reload. `[live]`
2. Variable product: choose a full attribute set → add → cart line shows the correct variation meta.
3. An OOS variation combination → button disabled, no add possible.
4. Quantity > 1 is respected on the cart line.
5. Logged-out clean incognito session — the first-ever add works (nonce/session edge).
6. Fragments refresh: badge updates on add AND after browser-back.

**Prove the check can fail before you trust it** (rule 3): delete `data-product_id` from the button,
re-run check 3, confirm it prints `0`, then restore. A gate you have never seen go red is a guess
with a citation. **A gate that dies is not a gate that passed** (rule 1) — if `verify:theme` errors
or times out, its silence is an artifact; re-run it by hand.

**Attribution** (rule 4): before claiming a phpcs/phpstan finding is caused by your change, run the
same gate on a pristine tree —
`git archive HEAD wordpress-theme/skyyrose-flagship | tar -x -C "$SCRATCH"` — and diff the check's
*contents*, not its pass/fail state. Never `git stash`; the stash stack is shared across worktrees.

## Worked example

Reviewing the lookbook card's quick-add control, 2026-07-29, in this worktree.

```bash
$ sed -n '148,153p' wordpress-theme/skyyrose-flagship/template-parts/product-card-v7-lookbook.php
			printf(
				'<a href="%s" data-quantity="1" data-product_id="%d" data-magnetic class="v7card__quickadd button add_to_cart_button ajax_add_to_cart" rel="nofollow">%s</a>',
				esc_url( $v7_permalink ),
				absint( $v7_product->get_id() ),
				esc_html__( 'Quick Add', 'skyyrose' )
			);
```

Contract satisfied on one element: class `ajax_add_to_cart`, `data-product_id` (via `absint()`),
`data-quantity="1"`, `rel="nofollow"`, `esc_url()` on the href. The comment immediately above at
`:140-142` states the rule this template follows — the href is the permalink, never a
`?add-to-cart=` GET, because crawlers would fire cart-adds and poison the cache. `[repo]`

Gates run the same session:

```
$ php -l woocommerce/single-product.php
No syntax errors detected in woocommerce/single-product.php

$ vendor/bin/phpcs --standard=.phpcs.xml woocommerce/single-product.php
. 1 / 1 (100%)
Time: 679ms; Memory: 14MB
$ echo $?
0

$ curl -sI "https://skyyrose.co/?cb=$(date +%s)" | head -1
HTTP/2 200
```

`[repro]` for the two local gates, `[live]` for the storefront probe. The live theme asset version
observed the same session was `ver=1.12.9`, matching `functions.php:21`
(`define( 'SKYYROSE_VERSION', '1.12.9' );`) — the deployed build is current, not stale.

## Failure modes

| Symptom | Cause | Evidence needed |
|---|---|---|
| Button click navigates instead of adding | class present, `data-product_id` missing (or vice-versa) | grep check 3 above `[repo]`, then a network trace `[live]` |
| Cart badge stale after first add | custom JS listens for `added_to_cart` only, not `wc_fragments_refreshed` | console + network on a real add `[live]` |
| Variation picker dead, no console error | template stripped `data-product_variations` or the `woocommerce_variation_add_to_cart` hooks | diff the template against `git archive HEAD` `[repo]` |
| "Add" succeeds but wrong/no variation meta | partial attribute set submitted | inspect the POST body `[live]` |
| Oversell past stock | custom stepper ignores `max` from `woocommerce_quantity_input_args` | order record vs stock `[live]` |
| Add-to-cart 403 in production | plugin interference corrupting CommerceKit nonces — fixed by the MU-plugin `option_active_plugins` guard. Check plugin interference **before** blaming the theme | prod network trace `[live]` — **bug-096-adjacent; the recorded incident is the homepage plugin guard, PR #596** |
| CSS change looks right locally, unchanged live | `.min` not rebuilt; production serves `.min` | `verify:theme --only min-sync` `[test]` |
| Kids Capsule shows 0 cards | launch mode, **by design** | do not "fix" it |
| REST probe returns 401 on `/wp-json/` | WP.com Atomic — use `?rest_route=` form | `[live]` |

Two standing traps, both recorded as recurring:

- **Fail-open gates (bug-230, ×6).** A verification step whose input is missing must block, never
  pass. If `verify:theme` cannot find the theme, that is a FAIL, not a skip.
- **Scope-jumping severity (bug-287, ×2).** A finding read from the working tree is `[repo]`. Calling
  it a "production bug" requires a `[live]` probe of skyyrose.co in the same session. State scope
  before severity.
