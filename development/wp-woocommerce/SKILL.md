---
name: wp-woocommerce
description: "Use when building, extending, or debugging a WooCommerce plugin — custom product types, payment gateways (WC_Payment_Gateway, process_payment(), process_refund()), shipping methods (WC_Shipping_Method, calculate_shipping()), CRUD via WC_Product / WC_Order / WC_Customer (wc_get_product, wc_create_order, wc_get_orders, get_meta, update_meta_data), HPOS compatibility (FeaturesUtil::declare_compatibility, wc_get_orders instead of WP_Query on posts), REST API extensions (woocommerce_rest_prepare, woocommerce_rest_pre_insert, Store API woocommerce_store_api_register_endpoint_data), cart/checkout blocks (registerCheckoutFilters, extensionCartUpdate, SlotFills), key hooks (woocommerce_cart_calculate_fees, woocommerce_checkout_fields, woocommerce_order_status_changed, woocommerce_payment_gateways), or WooCommerce subscription/coupon/webhook logic. Triggers: \"WooCommerce extension\", \"custom product type\", \"payment gateway\", \"hook into WooCommerce checkout\", \"WC_Order\", \"wc_create_order()\", \"wc_get_product()\", \"add a shipping method\", \"WooCommerce REST API\", \"HPOS compatible\", \"FeaturesUtil::declare_compatibility\", \"cart block\", \"checkout block filter\", \"woocommerce_payment_gateways\", \"WC_Product CRUD\", \"Store API endpoint\", \"extend WooCommerce\", \"woocommerce_cart_calculate_fees\", \"woocommerce_checkout_fields\", \"process_payment()\", \"process_refund()\", \"woocommerce_rest_prepare_product\", \"registerCheckoutFilters\", \"WC webhook HMAC\", \"WC coupon CRUD\", \"wc_get_orders HPOS\". Not for: Freemius monetisation — use `wp-freemius`; plain WordPress post/taxonomy work without WooCommerce."
---

# WooCommerce Extension Development

> **Model note:** Complex — payment gateways, HPOS compatibility, and block cart/checkout require multi-file reasoning. Use `sonnet` or `opus`. `haiku` for isolated CRUD or hook lookups only.

Guide for building WooCommerce extensions: custom product types, payment gateways, hooks, CRUD, REST, and admin UI. Assumes the host plugin passes the `wp-plugin-audit` baseline and the official `wp-plugin-development` security conventions.

## When to use

- "Add a custom product type", "create a payment gateway", "add a shipping method".
- "Extend the WooCommerce REST API", "add fields to WC orders/products".
- "Build a WooCommerce admin tab", "add product meta", "custom checkout field".
- "Hook into WC cart/checkout", "add a fee", "apply a discount programmatically".
- "Debug WooCommerce order status flow", "fix a WC hook not firing".

**Not for:** General WordPress plugin architecture — use `wp-plugin-development`. PHPStan types for WC — use `wp-phpstan-stubs` to scaffold WC stubs.

## Method

### 1. Identify extension point category

Determine which WC subsystem applies before writing code:

| Goal | Subsystem |
|---|---|
| Custom product type | `WC_Product` subclass + `product_type_query` filter |
| Payment gateway | `WC_Payment_Gateway` subclass + `woocommerce_payment_gateways` filter |
| Shipping method | `WC_Shipping_Method` subclass + `woocommerce_shipping_methods` filter |
| Custom order status | `wc_register_order_status` + `wc_order_statuses` filter |
| Cart/checkout field | `woocommerce_checkout_fields` filter or block integration API |
| Admin product tab | `woocommerce_product_data_tabs` + `woocommerce_product_data_panels` |
| Order list column | `manage_edit-shop_order_columns` + `manage_shop_order_posts_custom_column` |
| REST API extension | `woocommerce_rest_*` hooks or custom endpoint on `WC_REST_Controller` |

### 2. CRUD — use WC classes, not direct `$wpdb`

Always use WC CRUD methods; they fire the correct hooks and invalidate caches.

```php
// Orders
$order = wc_create_order( [ 'status' => 'pending', 'customer_id' => $user_id ] );
$order->add_product( wc_get_product( $product_id ), 1 );
$order->calculate_totals();
$order->save();

// Products
$product = new WC_Product_Simple();
$product->set_name( 'My Product' );
$product->set_regular_price( '19.99' );
$product->set_status( 'publish' );
$product->save();

// Reading
$order   = wc_get_order( $order_id );       // returns WC_Order or false
$product = wc_get_product( $product_id );   // returns WC_Product subclass or false
```

For meta, use `$order->get_meta()` / `$order->update_meta_data()` + `$order->save()` — never `update_post_meta()` on orders (breaks HPOS).

### 3. HPOS compatibility

WooCommerce 8.2+ ships **High-Performance Order Storage** (HPOS). Extensions must declare compatibility or they're disabled in HPOS stores.

```php
add_action( 'before_woocommerce_init', function() {
    if ( class_exists( \Automattic\WooCommerce\Utilities\FeaturesUtil::class ) ) {
        \Automattic\WooCommerce\Utilities\FeaturesUtil::declare_compatibility(
            'custom_order_tables', __FILE__, true
        );
    }
} );
```

Rules under HPOS:
- Never read/write orders via `get_post_meta()` / `update_post_meta()` — use `WC_Order` getters/setters.
- Never query orders via `WP_Query` with `post_type=shop_order` — use `wc_get_orders()`.
- Avoid `$wpdb` queries directly on `{prefix}posts` for order data.

### 4. Payment gateway skeleton

```php
class My_Payment_Gateway extends WC_Payment_Gateway {
    public function __construct() {
        $this->id                 = 'my_gateway';
        $this->method_title       = __( 'My Gateway', 'my-plugin' );
        $this->method_description = __( 'Pay via My Gateway.', 'my-plugin' );
        $this->supports           = [ 'products', 'refunds' ];
        $this->init_form_fields();
        $this->init_settings();
        $this->title   = $this->get_option( 'title' );
        $this->enabled = $this->get_option( 'enabled' );
        add_action( 'woocommerce_update_options_payment_gateways_' . $this->id,
            [ $this, 'process_settings' ] );
    }

    public function process_payment( $order_id ) {
        $order = wc_get_order( $order_id );
        // ... call payment API ...
        $order->payment_complete( $transaction_id );
        return [ 'result' => 'success', 'redirect' => $this->get_return_url( $order ) ];
    }

    public function process_refund( $order_id, $amount = null, $reason = '' ) {
        // return true on success, WP_Error on failure
    }
}
add_filter( 'woocommerce_payment_gateways', fn( $gateways ) => [ ...$gateways, My_Payment_Gateway::class ] );
```

### 5. REST API extension

Extend existing WC REST endpoints via `woocommerce_rest_prepare_*` hooks, or register a custom controller:

```php
// Add field to products REST response
add_filter( 'woocommerce_rest_prepare_product_object', function( $response, $product, $request ) {
    $response->data['my_custom_field'] = $product->get_meta( '_my_field' );
    return $response;
}, 10, 3 );

// Accept field on write
add_filter( 'woocommerce_rest_pre_insert_product_object', function( $product, $request ) {
    if ( isset( $request['my_custom_field'] ) ) {
        $product->update_meta_data( '_my_field', sanitize_text_field( $request['my_custom_field'] ) );
    }
    return $product;
}, 10, 2 );
```

### 6. Key hooks reference

```php
// Cart
add_action( 'woocommerce_cart_calculate_fees', [ $this, 'add_fee' ] );
add_filter( 'woocommerce_cart_item_price',     [ $this, 'modify_price' ], 10, 3 );

// Checkout
add_filter( 'woocommerce_checkout_fields',     [ $this, 'add_field' ] );
add_action( 'woocommerce_checkout_update_order_meta', [ $this, 'save_field' ] );

// Orders
add_action( 'woocommerce_order_status_changed', [ $this, 'on_status_change' ], 10, 4 );
add_filter( 'wc_order_statuses',               [ $this, 'register_status' ] );

// Products
add_filter( 'woocommerce_product_data_tabs',   [ $this, 'add_tab' ] );
add_action( 'woocommerce_product_data_panels', [ $this, 'render_panel' ] );
add_action( 'woocommerce_process_product_meta', [ $this, 'save_meta' ] );
```

**Where you register these matters.** Product-data hooks are admin-only, but order
lifecycle hooks are not. `woocommerce_order_status_changed`, subscription renewal
hooks, and anything a payment gateway triggers all fire from cron, the Action
Scheduler queue, and webhook requests — contexts where `is_admin()` is `false`.
Registering them in an admin-only bootstrap makes them work when a human clicks
through the admin and silently do nothing for automatic transitions:

```php
// Always loaded — admin, front-end, cron, CLI, gateway webhooks
new My_Plugin\Common\Order_Controller();      // order status, renewals, gateway callbacks

if ( is_admin() ) {
    new My_Plugin\Admin\Product_Controller();  // product data tabs, meta boxes
}
```

Make the side effect idempotent too — a renewal or gateway callback can arrive more
than once (retries, or a manual and an automatic path both completing):

```php
add_action( 'woocommerce_subscription_renewal_payment_complete', function ( $subscription, $order ) {
    if ( $order->get_meta( '_my_plugin_processed' ) ) {
        return; // already handled this renewal
    }
    my_plugin_handle_renewal( $subscription, $order );
    $order->update_meta_data( '_my_plugin_processed', 1 );
    $order->save();
}, 10, 2 );
```

Context table, detection steps and verification commands → `wp-background-processing` §7.

### 7. Blocks (cart/checkout) compatibility

Classic shortcode hooks (`woocommerce_checkout_fields`) do **not** fire for the block-based checkout. Use the Store API extension registry:

```php
add_action( 'woocommerce_blocks_loaded', function() {
    if ( ! function_exists( 'woocommerce_store_api_register_endpoint_data' ) ) return;
    woocommerce_store_api_register_endpoint_data( [
        'endpoint'        => Automattic\WooCommerce\StoreApi\Schemas\V1\CartSchema::IDENTIFIER,
        'namespace'       => 'my-plugin',
        'schema_callback' => fn() => [ 'my_field' => [ 'type' => 'string' ] ],
        'data_callback'   => fn() => [ 'my_field' => get_user_meta( get_current_user_id(), '_my_field', true ) ],
    ] );
} );
```

Declare blocks compatibility alongside HPOS:
```php
\Automattic\WooCommerce\Utilities\FeaturesUtil::declare_compatibility( 'cart_checkout_blocks', __FILE__, true );
```

## Notes

- Always check `class_exists( 'WooCommerce' )` before any WC code; gate with `woocommerce_loaded` action.
- Order lifecycle and gateway hooks must be registered outside `is_admin()` — see §6. Symptom: works when an admin changes the status by hand, never fires for an automatic transition.
- Minimum WC version requirements: HPOS stable in 8.2, blocks checkout stable in 8.3.
- Use `wc_get_logger()` for debug logging — writes to **WooCommerce → Status → Logs**, not the WP debug log.
- For testing: WC ships test helpers in `woocommerce/tests/legacy/includes/` — use `WC_Helper_Product::create_simple_product()` etc. in PHPUnit tests.

## References

- `references/wc-hooks.md` — categorised hook list (cart, checkout, orders, products, admin) with signatures and since versions.
- `references/hpos-migration.md` — HPOS compatibility checklist and query migration patterns.
- `references/product-crud.md` — WC_Product factory, meta CRUD, product type registration, variation patterns.
- `references/rest-api.md` — WC REST API auth, endpoints, batch operations, extending product/order responses via filters.
- `references/block-cart-checkout.md` — SlotFills, registerCheckoutFilters, extensionCartUpdate, woocommerce_store_api_register_update_callback, enqueue pattern.
- `references/payment-methods.md` — registerPaymentMethod(), registerExpressPaymentMethod(), AbstractPaymentMethodType PHP class, block payment registration.
- `references/payment-gateway.md` — WC_Payment_Gateway scaffold, process_payment(), process_refund(), webhook handler, settings fields.
- `references/shipping.md` — WC_Shipping_Method scaffold, calculate_shipping(), woocommerce_package_rates filter, zone handling, split packages.
- `references/orders.md` — wc_get_orders(), getter list, line item iteration, status hooks, custom status registration, wc_create_refund(), HPOS admin columns.
- `references/coupons-tax-webhooks.md` — WC_Coupon CRUD, wc_order_statuses filter, WC_Tax::calc_tax(), WC_Webhook programmatic creation, HMAC-SHA256 verification.
