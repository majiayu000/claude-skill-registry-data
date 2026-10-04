---
name: orbit-uat-woo
description: UAT template + Playwright spec scaffolds for WooCommerce extensions — product creation, cart flows, checkout (incl. Block Checkout), order lifecycle, refund / partial refund, HPOS-aware queries, REST + Store API. Use when the user says "WooCommerce UAT", "test my Woo plugin", "checkout flow test", "Block Checkout".
---

# 🪐 orbit-uat-woo — WooCommerce extension UAT

WC has more moving parts than any WP plugin you'll integrate with. UAT must cover the actual flows users hit — not just "does the settings page load."

---

## Quick start

```bash
PLUGIN_SLUG=my-woo-extension npx playwright test --project=uat-woo
```

Requires WooCommerce active in the test site (auto-installed by `create-test-site.sh --woo`).

---

## What the UAT covers

### 1. Product CRUD
```js
test('Create simple product', async ({ page }) => {
  await page.goto('/wp-admin/post-new.php?post_type=product');
  await page.fill('#title', 'Test Product');
  await page.fill('#_regular_price', '29.99');
  await page.click('Publish');
  await expect(page.getByText('Product published')).toBeVisible();
});
```

### 2. Add to cart + checkout
Cover BOTH classic checkout AND Block Checkout (WC 8.0+ default):
```js
test('Block Checkout completes', async ({ page }) => {
  await page.goto('/?p=' + productId);
  await page.click('button[name="add-to-cart"]');
  await page.goto('/checkout/');
  // Block Checkout has different DOM than classic
  await expect(page.locator('.wp-block-woocommerce-checkout')).toBeVisible();
  // Fill billing fields, submit, verify order page
});
```

### 3. Order lifecycle
- Order create → email sent
- Status change (Processing → Completed)
- Refund issuance
- Partial refund
- Custom order status (if your plugin adds one)

### 4. HPOS compatibility
**Whitepaper intent:** WC 8.x defaults to HPOS (High-Performance Order Storage). Plugins reading orders directly from `wp_posts` break. Your UAT must run BOTH HPOS-on and HPOS-off configurations.

```js
// Explicitly set HPOS in WC settings
await page.goto('/wp-admin/admin.php?page=wc-settings&tab=advanced&section=features');
await page.check('text=Use the High-Performance Order Storage');
```

Plugin header must declare:
```php
// Plugin Name: My Woo Extension
// WC requires at least: 8.0
// WC tested up to: 9.x
//
// (And in code:)
add_action( 'before_woocommerce_init', function() {
  if ( class_exists( '\Automattic\WooCommerce\Utilities\FeaturesUtil' ) ) {
    \Automattic\WooCommerce\Utilities\FeaturesUtil::declare_compatibility( 'custom_order_tables', __FILE__, true );
  }
} );
```

### 5. REST API + Store API
- REST: `/wp-json/wc/v3/products` with API keys
- Store API (frontend, no auth): `/wp-json/wc/store/v1/cart`

### 6. Tax + shipping calculations
Trigger zone-based tax + flat-rate shipping; verify totals match expected.

### 7. Subscriptions (if extending WC Subscriptions)
- Renewal order generation
- Subscription pause / cancel / reactivate

### 8. Multilingual (if WPML or Polylang active)
Product title/description translatable, cart works in second language.

---

## Output

```markdown
# WooCommerce UAT — my-woo-extension

## 42 tests, 38 passed, 4 failed

❌ "Block Checkout — custom field renders" — field missing in block context
   → Plugin extends classic checkout via woocommerce_checkout_fields, not Block Checkout's API
   → Migrate to extensions API (woocommerce_blocks_loaded hook)

❌ "HPOS — order count" — get_posts() returns 0 with HPOS on
   → Replace get_posts() with wc_get_orders()

✓ Refund flow — passes
✓ REST API — products endpoint works
```

---

## Pair with

- `/orbit-wp-database` — wc_get_orders vs $wpdb queries
- `/orbit-pay-stripe` / `/orbit-pay-paypal` — payment integration tests
- `/orbit-conflict-matrix` — WC + competitor plugins together

---

## Sources & Evergreen References

### Canonical docs
- [WooCommerce Developer Resources](https://developer.woocommerce.com/) — root
- [HPOS Migration Guide](https://github.com/woocommerce/woocommerce/wiki/High-Performance-Order-Storage-Upgrade-Recipe-Book) — wiki
- [Block Checkout extensions](https://github.com/woocommerce/woocommerce-blocks/blob/trunk/docs/third-party-developers/extensibility/checkout-block/README.md) — extensibility
- [WC REST API](https://woocommerce.github.io/woocommerce-rest-api-docs/) — REST reference
- [WC Store API](https://github.com/woocommerce/woocommerce-blocks/blob/trunk/docs/third-party-developers/extensibility/rest-api/README.md) — frontend REST

### Rule lineage
- HPOS — WC 7.x optional, WC 8.0 default
- Block Checkout — WC 8.3 default for new stores, WC 9.x default for all
- declare_compatibility — required since WC 7.1

### Last reviewed
- 2026-04-29 — re-review on every WC minor (active changes)
