---
name: wp-woocommerce
description: WooCommerce development patterns — custom product types, payment gateways, shipping methods, HPOS, REST API extensions, cart/checkout customization, email classes, block integration, and testing with WC helpers.
tools:
  - read
  - write
  - edit
  - bash
  - grep
  - glob
---

# WooCommerce Development

## 1. WooCommerce Architecture

WooCommerce is a singleton plugin built on WordPress. The `WC()` function returns the global instance. Key architectural layers:

- **WC_Data** — Abstract CRUD base class. All major entities (products, orders, coupons) extend this.
- **Data Stores** — Abstraction layer between CRUD classes and the database. Swappable via `woocommerce_data_stores` filter.
- **Session Handler** — `WC_Session_Handler` stores cart/session data. Uses a custom table (`wc_sessions`), not PHP sessions.
- **WC_Install** — Bootstrap class that runs on activation. Creates tables, sets default options, schedules cron events.

```php
// Access WooCommerce singleton
$wc = WC();
$cart = WC()->cart;
$session = WC()->session;

// Override a data store
add_filter( 'woocommerce_data_stores', function( $stores ) {
    $stores['product'] = 'My_Custom_Product_Data_Store';
    return $stores;
});
```

## 2. Custom Product Types

Extend `WC_Product` and register the type with WooCommerce admin.

```php
// Step 1: Define the product class
class WC_Product_Bundle extends WC_Product {
    public function get_type() {
        return 'bundle';
    }

    public function get_bundled_items() {
        return $this->get_meta( '_bundled_product_ids', true ) ?: [];
    }
}

// Step 2: Register the product type class
add_filter( 'woocommerce_product_class', function( $classname, $product_type ) {
    if ( $product_type === 'bundle' ) {
        return 'WC_Product_Bundle';
    }
    return $classname;
}, 10, 2 );

// Step 3: Add to product type selector in admin
add_filter( 'product_type_selector', function( $types ) {
    $types['bundle'] = __( 'Bundle Product', 'my-plugin' );
    return $types;
});

// Step 4: Add product data tab
add_filter( 'woocommerce_product_data_tabs', function( $tabs ) {
    $tabs['bundle_options'] = [
        'label'    => __( 'Bundle Items', 'my-plugin' ),
        'target'   => 'bundle_product_data',
        'class'    => [ 'show_if_bundle' ],
        'priority' => 25,
    ];
    return $tabs;
});

// Step 5: Render the tab panel
add_action( 'woocommerce_product_data_panels', function() {
    echo '<div id="bundle_product_data" class="panel woocommerce_options_panel">';
    woocommerce_wp_text_input([
        'id'          => '_bundled_product_ids',
        'label'       => __( 'Bundled Product IDs', 'my-plugin' ),
        'description' => __( 'Comma-separated product IDs', 'my-plugin' ),
        'desc_tip'    => true,
    ]);
    echo '</div>';
});

// Step 6: Save product data
add_action( 'woocommerce_process_product_meta_bundle', function( $post_id ) {
    $product = wc_get_product( $post_id );
    $ids = sanitize_text_field( $_POST['_bundled_product_ids'] ?? '' );
    $product->update_meta_data( '_bundled_product_ids', array_map( 'absint', explode( ',', $ids ) ) );
    $product->save();
});
```

## 3. Payment Gateway Development

Extend `WC_Payment_Gateway`. The `process_payment` method is the core contract.

```php
class WC_Gateway_Custom extends WC_Payment_Gateway {
    public function __construct() {
        $this->id                 = 'custom_gateway';
        $this->method_title       = __( 'Custom Gateway', 'my-plugin' );
        $this->method_description = __( 'Accept payments via Custom API.', 'my-plugin' );
        $this->has_fields         = true;
        $this->supports           = [ 'products', 'refunds', 'tokenization' ];

        $this->init_form_fields();
        $this->init_settings();
        $this->title   = $this->get_option( 'title' );
        $this->testmode = 'yes' === $this->get_option( 'testmode' );

        add_action( 'woocommerce_update_options_payment_gateways_' . $this->id, [ $this, 'process_admin_options' ] );
        add_action( 'woocommerce_api_' . strtolower( get_class( $this ) ), [ $this, 'handle_webhook' ] );
    }

    public function init_form_fields() {
        $this->form_fields = [
            'enabled'  => [ 'title' => 'Enable', 'type' => 'checkbox', 'default' => 'no' ],
            'title'    => [ 'title' => 'Title', 'type' => 'text', 'default' => 'Custom Pay' ],
            'testmode' => [ 'title' => 'Test Mode', 'type' => 'checkbox', 'default' => 'yes' ],
            'api_key'  => [ 'title' => 'API Key', 'type' => 'password' ],
        ];
    }

    public function process_payment( $order_id ) {
        $order = wc_get_order( $order_id );

        $response = wp_remote_post( $this->get_api_url() . '/charges', [
            'headers' => [ 'Authorization' => 'Bearer ' . $this->get_option( 'api_key' ) ],
            'body'    => wp_json_encode([
                'amount'   => $order->get_total() * 100,
                'currency' => $order->get_currency(),
                'metadata' => [ 'order_id' => $order_id ],
            ]),
        ]);

        $body = json_decode( wp_remote_retrieve_body( $response ), true );

        if ( ! empty( $body['id'] ) && $body['status'] === 'succeeded' ) {
            $order->payment_complete( $body['id'] );
            $order->add_order_note( sprintf( 'Payment completed. Transaction ID: %s', $body['id'] ) );
            WC()->cart->empty_cart();
            return [ 'result' => 'success', 'redirect' => $this->get_return_url( $order ) ];
        }

        wc_add_notice( $body['error']['message'] ?? 'Payment failed.', 'error' );
        return [ 'result' => 'failure' ];
    }

    public function process_refund( $order_id, $amount = null, $reason = '' ) {
        $order = wc_get_order( $order_id );
        $txn_id = $order->get_transaction_id();
        if ( ! $txn_id ) return new WP_Error( 'no_txn', 'No transaction ID found.' );

        $response = wp_remote_post( $this->get_api_url() . '/refunds', [
            'headers' => [ 'Authorization' => 'Bearer ' . $this->get_option( 'api_key' ) ],
            'body'    => wp_json_encode([ 'charge' => $txn_id, 'amount' => $amount * 100 ]),
        ]);

        $body = json_decode( wp_remote_retrieve_body( $response ), true );
        return ! empty( $body['id'] ) ? true : new WP_Error( 'refund_failed', 'Refund failed.' );
    }

    public function handle_webhook() {
        $payload = json_decode( file_get_contents( 'php://input' ), true );
        $order   = wc_get_order( $payload['metadata']['order_id'] ?? 0 );
        if ( $order && $payload['type'] === 'charge.refunded' ) {
            $order->update_status( 'refunded', 'Webhook: refund confirmed.' );
        }
        wp_die( 'OK', 200 );
    }

    private function get_api_url() {
        return $this->testmode ? 'https://api.sandbox.example.com' : 'https://api.example.com';
    }
}

add_filter( 'woocommerce_payment_gateways', function( $gateways ) {
    $gateways[] = 'WC_Gateway_Custom';
    return $gateways;
});
```

## 4. Shipping Method Development

```php
class WC_Shipping_Custom extends WC_Shipping_Method {
    public function __construct( $instance_id = 0 ) {
        $this->id                 = 'custom_shipping';
        $this->instance_id        = absint( $instance_id );
        $this->method_title       = __( 'Custom Shipping', 'my-plugin' );
        $this->method_description = __( 'Real-time rate calculation.', 'my-plugin' );
        $this->supports           = [ 'shipping-zones', 'instance-settings' ];

        $this->init();
    }

    public function init() {
        $this->instance_form_fields = [
            'base_cost' => [
                'title'   => __( 'Base Cost', 'my-plugin' ),
                'type'    => 'price',
                'default' => '5.00',
            ],
            'per_kg' => [
                'title'   => __( 'Cost per kg', 'my-plugin' ),
                'type'    => 'price',
                'default' => '1.50',
            ],
        ];
        $this->title = $this->get_option( 'title', $this->method_title );
    }

    public function calculate_shipping( $package = [] ) {
        $weight    = 0;
        $base_cost = (float) $this->get_option( 'base_cost', 5 );
        $per_kg    = (float) $this->get_option( 'per_kg', 1.5 );

        foreach ( $package['contents'] as $item ) {
            $product = $item['data'];
            $weight += (float) $product->get_weight() * $item['quantity'];
        }

        $cost = $base_cost + ( $weight * $per_kg );

        $this->add_rate([
            'id'    => $this->get_rate_id(),
            'label' => $this->title,
            'cost'  => $cost,
        ]);
    }
}

add_filter( 'woocommerce_shipping_methods', function( $methods ) {
    $methods['custom_shipping'] = 'WC_Shipping_Custom';
    return $methods;
});
```

## 5. WooCommerce Hooks Reference

### Critical Action Hooks

```php
// Validate checkout before processing
add_action( 'woocommerce_checkout_process', function() {
    if ( empty( $_POST['custom_field'] ) ) {
        wc_add_notice( __( 'Custom field is required.' ), 'error' );
    }
});

// After payment completes (order paid)
add_action( 'woocommerce_payment_complete', function( $order_id ) {
    $order = wc_get_order( $order_id );
    // Trigger fulfillment, send to ERP, etc.
}, 10, 1 );

// Order status transitions
add_action( 'woocommerce_order_status_changed', function( $order_id, $from, $to, $order ) {
    if ( $to === 'completed' ) {
        // Grant access, generate license keys, etc.
    }
}, 10, 4 );

// Item added to cart
add_action( 'woocommerce_add_to_cart', function( $cart_item_key, $product_id, $quantity, $variation_id, $variation, $cart_item_data ) {
    // Analytics tracking, cross-sell logic, etc.
}, 10, 6 );

// New order created (fires before payment)
add_action( 'woocommerce_new_order', function( $order_id, $order ) {
    // Reserve inventory, fraud check, etc.
}, 10, 2 );
```

### Critical Filter Hooks

```php
// Modify displayed cart item price
add_filter( 'woocommerce_cart_item_price', function( $price, $cart_item, $cart_item_key ) {
    return $price . ' <small>(per unit)</small>';
}, 10, 3 );

// Modify available shipping rates
add_filter( 'woocommerce_package_rates', function( $rates, $package ) {
    // Hide free shipping if other methods exist
    $dominated = [];
    foreach ( $rates as $rate_id => $rate ) {
        if ( 'free_shipping' === $rate->method_id && count( $rates ) > 1 ) {
            $dominated[] = $rate_id;
        }
    }
    return array_diff_key( $rates, array_flip( $dominated ) );
}, 10, 2 );

// Customize checkout fields
add_filter( 'woocommerce_checkout_fields', function( $fields ) {
    $fields['billing']['billing_vat'] = [
        'type'     => 'text',
        'label'    => __( 'VAT Number', 'my-plugin' ),
        'required' => false,
        'priority' => 120,
    ];
    unset( $fields['billing']['billing_company'] );
    return $fields;
});

// Control "add to cart" validation
add_filter( 'woocommerce_add_to_cart_validation', function( $passed, $product_id, $quantity ) {
    $product = wc_get_product( $product_id );
    if ( $product->get_meta( '_requires_approval' ) && ! current_user_can( 'approved_buyer' ) ) {
        wc_add_notice( __( 'This product requires buyer approval.' ), 'error' );
        return false;
    }
    return $passed;
}, 10, 3 );
```

## 6. REST API Extensions

```php
add_action( 'rest_api_init', function() {
    register_rest_route( 'my-plugin/v1', '/inventory/(?P<id>\d+)', [
        'methods'             => 'GET',
        'callback'            => 'mp_get_inventory',
        'permission_callback' => function( $request ) {
            return current_user_can( 'manage_woocommerce' );
        },
        'args' => [
            'id' => [ 'validate_callback' => 'is_numeric', 'required' => true ],
        ],
    ]);
});

function mp_get_inventory( WP_REST_Request $request ) {
    $product = wc_get_product( $request['id'] );
    if ( ! $product ) {
        return new WP_Error( 'not_found', 'Product not found', [ 'status' => 404 ] );
    }
    return rest_ensure_response([
        'product_id'    => $product->get_id(),
        'sku'           => $product->get_sku(),
        'stock_status'  => $product->get_stock_status(),
        'stock_quantity' => $product->get_stock_quantity(),
        'manage_stock'  => $product->get_manage_stock(),
    ]);
}
```

Extend the WC REST API namespace for deeper integration:

```php
// Register a custom batch endpoint compatible with WC API conventions
add_filter( 'woocommerce_rest_api_get_rest_namespaces', function( $controllers ) {
    $controllers['wc/v3']['custom-inventory'] = 'WC_REST_Custom_Inventory_Controller';
    return $controllers;
});
```

## 7. HPOS (High-Performance Order Storage)

WooCommerce 8.2+ uses custom order tables (`wc_orders`, `wc_order_addresses`, `wc_order_operational_data`) instead of `wp_posts` and `wp_postmeta`. Declare compatibility:

```php
add_action( 'before_woocommerce_init', function() {
    if ( class_exists( '\Automattic\WooCommerce\Utilities\FeaturesUtil' ) ) {
        \Automattic\WooCommerce\Utilities\FeaturesUtil::declare_compatibility(
            'custom_order_tables',
            __FILE__,
            true
        );
    }
});
```

Use `OrderUtil` for HPOS-safe queries:

```php
use Automattic\WooCommerce\Utilities\OrderUtil;

// Check if HPOS is active
if ( OrderUtil::custom_orders_table_usage_is_enabled() ) {
    // Use wc_get_orders() — works with both storage backends
    $orders = wc_get_orders([
        'status'     => 'processing',
        'limit'      => 50,
        'meta_query' => [
            [ 'key' => '_custom_flag', 'value' => '1' ],
        ],
    ]);
} else {
    // Legacy post-based query (fallback)
    $orders = wc_get_orders([
        'status' => 'processing',
        'limit'  => 50,
    ]);
}

// HPOS-safe order screen detection in admin
add_action( 'current_screen', function( $screen ) {
    if ( OrderUtil::is_order_list_table_screen() ) {
        // We are on the orders list screen
    }
    if ( OrderUtil::is_order_edit_screen() ) {
        // We are on the single order edit screen
    }
});

// Custom meta box that works with HPOS
add_action( 'add_meta_boxes', function() {
    $screen = OrderUtil::custom_orders_table_usage_is_enabled()
        ? wc_get_page_screen_id( 'shop-order' )
        : 'shop_order';

    add_meta_box( 'my_custom_box', 'Custom Data', 'render_my_custom_box', $screen, 'side' );
});
```

## 8. Cart and Checkout Customization

```php
// Add a custom checkout field, validate it, save it
add_action( 'woocommerce_after_order_notes', function( $checkout ) {
    woocommerce_form_field( 'delivery_date', [
        'type'     => 'date',
        'label'    => __( 'Preferred Delivery Date', 'my-plugin' ),
        'required' => true,
    ], $checkout->get_value( 'delivery_date' ) );
});

add_action( 'woocommerce_checkout_process', function() {
    if ( empty( $_POST['delivery_date'] ) ) {
        wc_add_notice( __( 'Please select a delivery date.' ), 'error' );
    }
    $date = sanitize_text_field( $_POST['delivery_date'] );
    if ( strtotime( $date ) < strtotime( '+2 days' ) ) {
        wc_add_notice( __( 'Delivery date must be at least 2 days from now.' ), 'error' );
    }
});

add_action( 'woocommerce_checkout_update_order_meta', function( $order_id ) {
    if ( ! empty( $_POST['delivery_date'] ) ) {
        $order = wc_get_order( $order_id );
        $order->update_meta_data( '_delivery_date', sanitize_text_field( $_POST['delivery_date'] ) );
        $order->save();
    }
});

// Add a dynamic cart fee
add_action( 'woocommerce_cart_calculate_fees', function( $cart ) {
    if ( is_admin() && ! defined( 'DOING_AJAX' ) ) return;

    $total = $cart->get_subtotal();
    if ( $total > 200 ) {
        $cart->add_fee( __( 'Insurance', 'my-plugin' ), 4.99, true );
    }
});
```

## 9. Custom Email Classes

```php
class WC_Email_Custom_Shipped extends WC_Email {
    public function __construct() {
        $this->id             = 'custom_shipped';
        $this->title          = __( 'Order Shipped', 'my-plugin' );
        $this->description    = __( 'Sent when an order is marked as shipped.', 'my-plugin' );
        $this->heading        = __( 'Your order has shipped!', 'my-plugin' );
        $this->subject        = __( 'Your {site_title} order #{order_number} has shipped', 'my-plugin' );
        $this->template_html  = 'emails/custom-shipped.php';
        $this->template_plain = 'emails/plain/custom-shipped.php';
        $this->template_base  = plugin_dir_path( __DIR__ ) . 'templates/';
        $this->customer_email = true;

        // Trigger on custom status transition
        add_action( 'woocommerce_order_status_processing_to_shipped_notification', [ $this, 'trigger' ], 10, 2 );

        parent::__construct();
    }

    public function trigger( $order_id, $order = false ) {
        if ( $order_id && ! is_a( $order, 'WC_Order' ) ) {
            $order = wc_get_order( $order_id );
        }
        if ( ! $order ) return;

        $this->object    = $order;
        $this->recipient = $order->get_billing_email();
        $this->placeholders['{order_number}'] = $order->get_order_number();
        $this->placeholders['{tracking_url}'] = $order->get_meta( '_tracking_url' );

        if ( $this->is_enabled() && $this->get_recipient() ) {
            $this->send( $this->get_recipient(), $this->get_subject(), $this->get_content(), $this->get_headers(), $this->get_attachments() );
        }
    }

    public function get_content_html() {
        return wc_get_template_html( $this->template_html, [
            'order'         => $this->object,
            'email_heading' => $this->get_heading(),
            'tracking_url'  => $this->object->get_meta( '_tracking_url' ),
            'sent_to_admin' => false,
            'plain_text'    => false,
            'email'         => $this,
        ], '', $this->template_base );
    }
}

add_filter( 'woocommerce_email_classes', function( $emails ) {
    $emails['WC_Email_Custom_Shipped'] = new WC_Email_Custom_Shipped();
    return $emails;
});
```

## 10. WooCommerce Blocks Integration

The block-based checkout uses the Store API. Extend it with custom data and blocks.

```php
// Register endpoint data for the Store API (checkout block)
use Automattic\WooCommerce\StoreApi\Schemas\V1\CheckoutSchema;
use Automattic\WooCommerce\StoreApi\StoreApi;

add_action( 'woocommerce_blocks_loaded', function() {
    woocommerce_store_api_register_endpoint_data([
        'endpoint'        => CheckoutSchema::IDENTIFIER,
        'namespace'       => 'my-plugin',
        'data_callback'   => function() {
            return [ 'delivery_date' => '' ];
        },
        'schema_callback' => function() {
            return [
                'delivery_date' => [
                    'description' => 'Preferred delivery date',
                    'type'        => 'string',
                    'context'     => [ 'view', 'edit' ],
                ],
            ];
        },
    ]);

    // Validate and save the block checkout extension data
    woocommerce_store_api_register_update_callback([
        'namespace' => 'my-plugin',
        'callback'  => function( $data ) {
            if ( empty( $data['delivery_date'] ) ) {
                throw new \Exception( 'Delivery date is required.' );
            }
        },
    ]);
});

// Save the extension data to order meta after checkout
add_action( 'woocommerce_store_api_checkout_update_order_from_request', function( $order, $request ) {
    $extensions = $request['extensions']['my-plugin'] ?? [];
    if ( ! empty( $extensions['delivery_date'] ) ) {
        $order->update_meta_data( '_delivery_date', sanitize_text_field( $extensions['delivery_date'] ) );
    }
}, 10, 2 );
```

Register the JS block:

```js
// checkout-block/index.js
import { registerCheckoutBlock } from '@woocommerce/blocks-checkout';
import { DeliveryDateBlock } from './delivery-date-block';

registerCheckoutBlock({
    metadata: {
        name: 'my-plugin/delivery-date',
        parent: [ 'woocommerce/checkout-shipping-methods-block' ],
    },
    component: DeliveryDateBlock,
});
```

## 11. Testing WooCommerce

Use `WC_Unit_Test_Case` as the base class. WooCommerce provides helper factories.

```php
class Test_Custom_Product extends WC_Unit_Test_Case {
    public function test_bundle_product_type() {
        $product = new WC_Product_Bundle();
        $this->assertEquals( 'bundle', $product->get_type() );
    }

    public function test_order_payment_complete_fires_hook() {
        $order = WC_Helper_Order::create_order();
        $order->set_payment_method( 'custom_gateway' );
        $order->save();

        $fired = false;
        add_action( 'woocommerce_payment_complete', function() use ( &$fired ) {
            $fired = true;
        });

        $order->payment_complete( 'txn_test_123' );

        $this->assertTrue( $fired );
        $this->assertEquals( 'completed', $order->get_status() );
        $this->assertEquals( 'txn_test_123', $order->get_transaction_id() );
    }

    public function test_shipping_rate_calculation() {
        $method  = new WC_Shipping_Custom();
        $product = WC_Helper_Product::create_simple_product( true, [ 'weight' => '2' ] );

        $package = [
            'contents' => [
                [ 'data' => $product, 'quantity' => 3 ],
            ],
            'destination' => [
                'country'  => 'US',
                'state'    => 'CA',
                'postcode' => '90210',
            ],
        ];

        $method->calculate_shipping( $package );
        $rates = $method->rates;

        $this->assertCount( 1, $rates );
        // base_cost (5) + weight (2 * 3 = 6) * per_kg (1.5) = 5 + 9 = 14
        $this->assertEquals( 14, $rates[ array_key_first( $rates ) ]->cost );
    }

    public function test_custom_checkout_field_validation() {
        // Simulate missing delivery_date
        $_POST['delivery_date'] = '';

        do_action( 'woocommerce_checkout_process' );

        $notices = wc_get_notices( 'error' );
        $this->assertNotEmpty( $notices );

        wc_clear_notices();
    }

    public function test_rest_api_inventory_endpoint() {
        $product = WC_Helper_Product::create_simple_product( true, [
            'sku'            => 'TEST-SKU-001',
            'stock_quantity' => 42,
            'manage_stock'   => true,
        ] );

        wp_set_current_user( $this->factory->user->create( [ 'role' => 'administrator' ] ) );

        $request  = new WP_REST_Request( 'GET', '/my-plugin/v1/inventory/' . $product->get_id() );
        $response = rest_do_request( $request );
        $data     = $response->get_data();

        $this->assertEquals( 200, $response->get_status() );
        $this->assertEquals( 'TEST-SKU-001', $data['sku'] );
        $this->assertEquals( 42, $data['stock_quantity'] );
    }

    public function test_hpos_compatibility_declared() {
        $this->assertTrue(
            class_exists( '\Automattic\WooCommerce\Utilities\FeaturesUtil' ),
            'FeaturesUtil class must exist for HPOS compatibility declaration.'
        );
    }
}
```

Run tests with wp-env:

```bash
# Start the WP test environment
wp-env start

# Run WooCommerce tests
wp-env run tests-cli ./vendor/bin/phpunit --filter=Test_Custom_Product

# Run E2E tests (Playwright)
cd wp-content/plugins/my-plugin && npx playwright test
```
