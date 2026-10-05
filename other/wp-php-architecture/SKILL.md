---
name: wp-php-architecture
description: WordPress PHP architecture patterns — repository, service layer, DDD, SOLID, plugin/theme structure, CPT design, and anti-patterns. The definitive reference for professional WordPress PHP development.
tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - Bash
---

# WordPress PHP Architecture Patterns

This skill encodes battle-tested architecture patterns for WordPress PHP development. Every pattern is adapted to WordPress realities: global state, hook-driven execution, no native DI container, and the functions.php bootstrap model. Use these patterns to write WordPress code that is testable, maintainable, and scalable.

---

## 1. Repository Pattern for WordPress

Wrap all data access behind repository classes. Never scatter `$wpdb` calls or raw `WP_Query` usage across business logic.

### Base Repository Interface

```php
interface PostRepositoryInterface {
    public function find_by_id( int $id ): ?object;
    public function find_all( array $criteria = [] ): array;
    public function save( object $entity ): int;
    public function delete( int $id ): bool;
}
```

### WP_Query Repository Implementation

```php
class ProductRepository implements PostRepositoryInterface {
    private string $post_type = 'product';

    public function find_by_id( int $id ): ?Product {
        $post = get_post( $id );
        if ( ! $post || $post->post_type !== $this->post_type ) {
            return null;
        }
        return $this->hydrate( $post );
    }

    public function find_all( array $criteria = [] ): array {
        $defaults = [
            'post_type'      => $this->post_type,
            'posts_per_page' => 20,
            'post_status'    => 'publish',
        ];
        $query = new WP_Query( array_merge( $defaults, $criteria ) );
        return array_map( [ $this, 'hydrate' ], $query->posts );
    }

    public function save( object $entity ): int {
        $args = [
            'post_type'    => $this->post_type,
            'post_title'   => $entity->get_name(),
            'post_content' => $entity->get_description(),
            'post_status'  => 'publish',
        ];
        if ( $entity->get_id() ) {
            $args['ID'] = $entity->get_id();
            wp_update_post( $args );
            $id = $entity->get_id();
        } else {
            $id = wp_insert_post( $args );
        }
        update_post_meta( $id, '_product_price', $entity->get_price()->amount() );
        update_post_meta( $id, '_product_sku', $entity->get_sku() );
        return $id;
    }

    public function delete( int $id ): bool {
        return (bool) wp_delete_post( $id, true );
    }

    private function hydrate( WP_Post $post ): Product {
        return new Product(
            id:          $post->ID,
            name:        $post->post_title,
            description: $post->post_content,
            price:       new Money( (float) get_post_meta( $post->ID, '_product_price', true ) ),
            sku:         (string) get_post_meta( $post->ID, '_product_sku', true ),
        );
    }
}
```

### Direct $wpdb Repository (for custom tables)

```php
class OrderRepository {
    private wpdb $db;
    private string $table;

    public function __construct() {
        global $wpdb;
        $this->db    = $wpdb;
        $this->table = $wpdb->prefix . 'custom_orders';
    }

    public function find_by_id( int $id ): ?Order {
        $row = $this->db->get_row(
            $this->db->prepare( "SELECT * FROM {$this->table} WHERE id = %d", $id )
        );
        return $row ? Order::from_row( $row ) : null;
    }

    public function find_by_customer( int $customer_id, int $limit = 50 ): array {
        $rows = $this->db->get_results(
            $this->db->prepare(
                "SELECT * FROM {$this->table} WHERE customer_id = %d ORDER BY created_at DESC LIMIT %d",
                $customer_id,
                $limit
            )
        );
        return array_map( [ Order::class, 'from_row' ], $rows );
    }
}
```

**Key rule:** Business logic calls `$repository->find_by_id()`, never `get_post()` directly. This makes the code testable (swap the repository) and decouples domain logic from WordPress data layer.

---

## 2. Service Layer Pattern

Services contain business logic. They depend on repositories (not on WordPress globals) and are registered via hooks at bootstrap time.

### Service Class

```php
class OrderService {
    private OrderRepository $orders;
    private ProductRepository $products;
    private NotificationService $notifications;

    public function __construct(
        OrderRepository $orders,
        ProductRepository $products,
        NotificationService $notifications
    ) {
        $this->orders        = $orders;
        $this->products      = $products;
        $this->notifications = $notifications;
    }

    public function place_order( int $customer_id, array $items ): Order {
        $line_items = [];
        foreach ( $items as $item ) {
            $product = $this->products->find_by_id( $item['product_id'] );
            if ( ! $product ) {
                throw new InvalidProductException( $item['product_id'] );
            }
            $line_items[] = new LineItem( $product, $item['quantity'] );
        }

        $order = Order::create( $customer_id, $line_items );
        $this->orders->save( $order );

        // Domain event via WordPress hook system
        do_action( 'myshop_order_placed', $order );

        $this->notifications->send_order_confirmation( $order );
        return $order;
    }
}
```

### Service Registration (Simple Factory at Bootstrap)

WordPress has no DI container. Use a static factory or a lightweight service locator in the main plugin file.

```php
class MyShopPlugin {
    private static ?self $instance = null;
    private array $services = [];

    public static function instance(): self {
        if ( null === self::$instance ) {
            self::$instance = new self();
        }
        return self::$instance;
    }

    private function __construct() {
        $this->register_services();
        $this->register_hooks();
    }

    private function register_services(): void {
        $products      = new ProductRepository();
        $orders        = new OrderRepository();
        $notifications = new NotificationService();

        $this->services['order_service'] = new OrderService( $orders, $products, $notifications );
        $this->services['product_repo']  = $products;
    }

    public function get( string $key ): object {
        if ( ! isset( $this->services[ $key ] ) ) {
            throw new RuntimeException( "Service '{$key}' not registered." );
        }
        return $this->services[ $key ];
    }

    private function register_hooks(): void {
        add_action( 'rest_api_init', [ $this, 'register_rest_routes' ] );
        add_action( 'init', [ $this, 'register_post_types' ] );
    }
}

// Bootstrap in main plugin file:
add_action( 'plugins_loaded', [ MyShopPlugin::class, 'instance' ] );
```

**Key rule:** Services never call `add_action` or `add_filter` themselves. The plugin bootstrap wires hooks to service methods. Services stay framework-agnostic and testable.

---

## 3. Domain-Driven Design Adapted for WordPress

### Value Objects

Value objects are immutable, compared by value, and encapsulate validation.

```php
final class Money {
    private float $amount;
    private string $currency;

    public function __construct( float $amount, string $currency = 'USD' ) {
        if ( $amount < 0 ) {
            throw new InvalidArgumentException( 'Amount cannot be negative.' );
        }
        $this->amount   = round( $amount, 2 );
        $this->currency = strtoupper( $currency );
    }

    public function amount(): float { return $this->amount; }
    public function currency(): string { return $this->currency; }

    public function add( Money $other ): self {
        if ( $this->currency !== $other->currency ) {
            throw new CurrencyMismatchException();
        }
        return new self( $this->amount + $other->amount, $this->currency );
    }

    public function equals( Money $other ): bool {
        return $this->amount === $other->amount && $this->currency === $other->currency;
    }
}

final class EmailAddress {
    private string $value;

    public function __construct( string $email ) {
        if ( ! is_email( $email ) ) { // Uses WP's is_email() validator
            throw new InvalidArgumentException( "Invalid email: {$email}" );
        }
        $this->value = sanitize_email( $email );
    }

    public function value(): string { return $this->value; }
}
```

### Entities as CPTs

A Custom Post Type IS a WordPress entity. Map domain entities to CPTs, but keep the domain model clean by using the repository to hydrate and persist.

```php
class Product {
    private ?int $id;
    private string $name;
    private string $description;
    private Money $price;
    private string $sku;

    public function __construct( ?int $id, string $name, string $description, Money $price, string $sku ) {
        $this->id          = $id;
        $this->name        = $name;
        $this->description = $description;
        $this->price       = $price;
        $this->sku         = $sku;
    }

    public function get_id(): ?int { return $this->id; }
    public function get_name(): string { return $this->name; }
    public function get_description(): string { return $this->description; }
    public function get_price(): Money { return $this->price; }
    public function get_sku(): string { return $this->sku; }

    public function apply_discount( float $percent ): void {
        $discounted = $this->price->amount() * ( 1 - $percent / 100 );
        $this->price = new Money( $discounted );
    }
}
```

### Domain Events via WordPress Hooks

`do_action` IS the domain event dispatcher. `add_action` IS the event subscriber.

```php
// Dispatching a domain event (in service layer):
do_action( 'myshop_order_placed', $order );
do_action( 'myshop_product_price_changed', $product, $old_price, $new_price );

// Subscribing to domain events (at bootstrap):
add_action( 'myshop_order_placed', [ $inventory_service, 'decrement_stock' ] );
add_action( 'myshop_order_placed', [ $analytics_service, 'track_purchase' ] );
add_action( 'myshop_product_price_changed', [ $cache_service, 'invalidate_product_cache' ] );
```

### Bounded Contexts as Plugins

Each bounded context (catalog, ordering, shipping, analytics) maps to a separate plugin. Cross-context communication uses `do_action` / `apply_filters` only. Never import classes across plugin boundaries. Define shared interfaces in a common package if needed.

---

## 4. SOLID Principles in WordPress

### Single Responsibility Principle (SRP)

One hook callback does one thing. If a callback grows beyond 15 lines, extract a service method.

```php
// BAD: callback does validation, processing, notification, and logging
add_action( 'save_post', 'do_everything_on_save' );

// GOOD: one callback, one responsibility
add_action( 'save_post_product', [ $product_service, 'sync_inventory_on_save' ], 10, 2 );
add_action( 'save_post_product', [ $cache_service, 'invalidate_on_save' ], 20, 2 );
add_action( 'save_post_product', [ $audit_service, 'log_product_change' ], 30, 2 );
```

### Open/Closed Principle (OCP)

Use `apply_filters` to make behavior extensible without modifying source code.

```php
class PricingEngine {
    public function calculate( Product $product, int $quantity ): Money {
        $unit_price = $product->get_price();
        $total      = new Money( $unit_price->amount() * $quantity );

        // Extensible via filters - other plugins can modify pricing
        $total = apply_filters( 'myshop_calculated_price', $total, $product, $quantity );
        return $total;
    }
}

// A separate plugin adds a bulk discount without touching PricingEngine:
add_filter( 'myshop_calculated_price', function( Money $total, Product $product, int $qty ): Money {
    if ( $qty >= 10 ) {
        return new Money( $total->amount() * 0.9 );
    }
    return $total;
}, 10, 3 );
```

### Liskov Substitution Principle (LSP)

Abstract base classes for CPT handlers ensure all subtypes are interchangeable.

```php
abstract class PostTypeHandler {
    abstract protected function get_post_type(): string;
    abstract protected function get_labels(): array;
    abstract protected function get_args(): array;

    public function register(): void {
        register_post_type( $this->get_post_type(), array_merge(
            $this->get_args(),
            [ 'labels' => $this->get_labels() ]
        ) );
    }
}
```

### Interface Segregation Principle (ISP)

Small, targeted interfaces rather than one monolithic plugin API.

```php
interface Renderable {
    public function render(): string;
}

interface Cacheable {
    public function cache_key(): string;
    public function cache_ttl(): int;
}

interface RestExposable {
    public function to_rest_response(): array;
    public function get_rest_schema(): array;
}

// A class implements only what it needs:
class ProductCard implements Renderable, Cacheable {
    public function render(): string { /* ... */ }
    public function cache_key(): string { return "product_card_{$this->id}"; }
    public function cache_ttl(): int { return HOUR_IN_SECONDS; }
}
```

### Dependency Inversion Principle (DIP)

Depend on interfaces, not WordPress globals.

```php
// BAD: tight coupling to WordPress global
class ReportGenerator {
    public function get_data(): array {
        global $wpdb;
        return $wpdb->get_results( "SELECT ..." );
    }
}

// GOOD: depend on an abstraction
class ReportGenerator {
    private ReportDataSourceInterface $source;

    public function __construct( ReportDataSourceInterface $source ) {
        $this->source = $source;
    }

    public function get_data(): array {
        return $this->source->fetch_report_data();
    }
}
```

---

## 5. Plugin Architecture Patterns

### Main Plugin File Structure

```php
<?php
/**
 * Plugin Name: My Shop
 */

defined( 'ABSPATH' ) || exit;

define( 'MYSHOP_VERSION', '1.0.0' );
define( 'MYSHOP_PATH', plugin_dir_path( __FILE__ ) );
define( 'MYSHOP_URL', plugin_dir_url( __FILE__ ) );

// Composer autoloader
require_once MYSHOP_PATH . 'vendor/autoload.php';

// Bootstrap
add_action( 'plugins_loaded', [ MyShop\Plugin::class, 'instance' ] );

// Activation/deactivation
register_activation_hook( __FILE__, [ MyShop\Installer::class, 'activate' ] );
register_deactivation_hook( __FILE__, [ MyShop\Installer::class, 'deactivate' ] );
```

### Directory Layout

```
my-shop/
  my-shop.php              # Bootstrap only
  composer.json             # Autoloading, dependencies
  src/
    Plugin.php             # Singleton service locator
    Installer.php          # Activation, DB table creation
    Domain/
      Product.php          # Entity
      Order.php            # Aggregate root
      Money.php            # Value object
    Repository/
      ProductRepository.php
      OrderRepository.php
    Service/
      OrderService.php
      PricingEngine.php
    Admin/
      ProductAdminPage.php
      OrderListTable.php
    Rest/
      ProductController.php
  templates/
    admin/
      product-edit.php
    frontend/
      product-card.php
  tests/
    Unit/
    Integration/
```

### Strategy Pattern for Rendering

```php
interface RenderStrategy {
    public function render( array $data ): string;
}

class GridRenderStrategy implements RenderStrategy {
    public function render( array $data ): string {
        ob_start();
        include MYSHOP_PATH . 'templates/frontend/product-grid.php';
        return ob_get_clean();
    }
}

class ListRenderStrategy implements RenderStrategy {
    public function render( array $data ): string {
        ob_start();
        include MYSHOP_PATH . 'templates/frontend/product-list.php';
        return ob_get_clean();
    }
}

class ProductDisplay {
    private RenderStrategy $strategy;

    public function __construct( RenderStrategy $strategy ) {
        $this->strategy = $strategy;
    }

    public function output( array $products ): string {
        return $this->strategy->render( [ 'products' => $products ] );
    }
}
```

### Template Method for Admin Pages

```php
abstract class AdminPage {
    abstract protected function get_page_title(): string;
    abstract protected function get_menu_slug(): string;
    abstract protected function get_capability(): string;
    abstract protected function render_content(): void;

    public function register(): void {
        add_menu_page(
            $this->get_page_title(),
            $this->get_page_title(),
            $this->get_capability(),
            $this->get_menu_slug(),
            [ $this, 'render' ]
        );
    }

    public function render(): void {
        if ( ! current_user_can( $this->get_capability() ) ) {
            wp_die( 'Unauthorized.' );
        }
        echo '<div class="wrap">';
        echo '<h1>' . esc_html( $this->get_page_title() ) . '</h1>';
        $this->render_content();
        echo '</div>';
    }
}
```

---

## 6. Theme Architecture

### Child Theme Directory Structure

```
oshin_child/
  style.css                 # Theme header + minimal styles
  functions.php             # Bootstrap ONLY - no logic here
  inc/
    setup.php              # Theme supports, menus, sidebars
    enqueue.php            # Script and style registration
    hooks.php              # Custom action/filter callbacks
    template-functions.php # Helper functions for templates
    customizer.php         # Customizer settings
  template-parts/
    content/
      content-product.php
      content-page.php
    components/
      hero-banner.php
      cta-block.php
  assets/
    css/
    js/
    images/
```

### functions.php as Pure Bootstrap

```php
<?php
// functions.php - BOOTSTRAP ONLY. No logic. No HTML. No queries.
defined( 'ABSPATH' ) || exit;

define( 'CHILD_THEME_VERSION', '1.0.0' );
define( 'CHILD_THEME_DIR', get_stylesheet_directory() );
define( 'CHILD_THEME_URI', get_stylesheet_directory_uri() );

// Load organized includes
require_once CHILD_THEME_DIR . '/inc/setup.php';
require_once CHILD_THEME_DIR . '/inc/enqueue.php';
require_once CHILD_THEME_DIR . '/inc/hooks.php';
require_once CHILD_THEME_DIR . '/inc/template-functions.php';
```

### Template Hierarchy Mastery

Always use the most specific template file. WordPress resolves templates in order of specificity. Use `get_template_part()` for reusable sections.

```php
// In archive-product.php
get_header();

if ( have_posts() ) :
    while ( have_posts() ) : the_post();
        // Loads template-parts/content/content-product.php
        get_template_part( 'template-parts/content/content', get_post_type() );
    endwhile;
    the_posts_pagination();
endif;

get_footer();
```

---

## 7. Custom Post Type Architecture

### Registration Pattern

```php
class ProductPostType extends PostTypeHandler {
    protected function get_post_type(): string {
        return 'product';
    }

    protected function get_labels(): array {
        return [
            'name'          => 'Products',
            'singular_name' => 'Product',
            'add_new_item'  => 'Add New Product',
            'edit_item'     => 'Edit Product',
        ];
    }

    protected function get_args(): array {
        return [
            'public'       => true,
            'has_archive'  => true,
            'rewrite'      => [ 'slug' => 'products' ],
            'supports'     => [ 'title', 'editor', 'thumbnail', 'excerpt' ],
            'show_in_rest' => true,
            'menu_icon'    => 'dashicons-cart',
        ];
    }
}
```

### Meta Box Architecture

```php
class ProductMetaBox {
    private string $post_type = 'product';
    private string $nonce_action = 'product_meta_save';
    private string $nonce_name = '_product_meta_nonce';

    public function register(): void {
        add_action( 'add_meta_boxes', [ $this, 'add_meta_boxes' ] );
        add_action( "save_post_{$this->post_type}", [ $this, 'save' ], 10, 2 );
    }

    public function add_meta_boxes(): void {
        add_meta_box( 'product-details', 'Product Details', [ $this, 'render' ], $this->post_type );
    }

    public function render( WP_Post $post ): void {
        wp_nonce_field( $this->nonce_action, $this->nonce_name );
        $price = get_post_meta( $post->ID, '_product_price', true );
        $sku   = get_post_meta( $post->ID, '_product_sku', true );
        include MYSHOP_PATH . 'templates/admin/product-meta-box.php';
    }

    public function save( int $post_id, WP_Post $post ): void {
        if ( ! isset( $_POST[ $this->nonce_name ] ) ) return;
        if ( ! wp_verify_nonce( $_POST[ $this->nonce_name ], $this->nonce_action ) ) return;
        if ( defined( 'DOING_AUTOSAVE' ) && DOING_AUTOSAVE ) return;
        if ( ! current_user_can( 'edit_post', $post_id ) ) return;

        if ( isset( $_POST['product_price'] ) ) {
            update_post_meta( $post_id, '_product_price', sanitize_text_field( $_POST['product_price'] ) );
        }
        if ( isset( $_POST['product_sku'] ) ) {
            update_post_meta( $post_id, '_product_sku', sanitize_text_field( $_POST['product_sku'] ) );
        }
    }
}
```

### Query Optimization for CPTs

```php
// Pre-fetch all needed meta in one query instead of N+1
function myshop_prefetch_product_meta( array $post_ids ): void {
    if ( empty( $post_ids ) ) return;
    update_meta_cache( 'post', $post_ids );
}

// Use pre_get_posts to modify the main query, not a new WP_Query
add_action( 'pre_get_posts', function( WP_Query $query ): void {
    if ( $query->is_main_query() && $query->is_post_type_archive( 'product' ) ) {
        $query->set( 'posts_per_page', 24 );
        $query->set( 'orderby', 'meta_value_num' );
        $query->set( 'meta_key', '_product_price' );
    }
} );
```

---

## 8. Anti-Patterns to Avoid

### God functions.php

Never put business logic, HTML templates, database queries, or AJAX handlers directly in `functions.php`. It is a bootstrap file, not a dumping ground.

### Direct $wpdb in Templates

```php
// NEVER do this in a template file:
global $wpdb;
$results = $wpdb->get_results( "SELECT * FROM ..." );

// ALWAYS use a repository or helper, called from the template:
$products = MyShopPlugin::instance()->get( 'product_repo' )->find_all();
```

### Mixing Concerns in Hook Callbacks

```php
// BAD: one callback validates, saves, sends email, logs, and redirects
add_action( 'save_post', function( $id ) {
    // 80 lines of mixed concerns
});

// GOOD: discrete, testable operations
add_action( 'save_post_product', [ $validator, 'validate' ], 5 );
add_action( 'save_post_product', [ $repo, 'sync' ], 10 );
add_action( 'save_post_product', [ $notifier, 'notify' ], 20 );
```

### Ignoring Transients for Expensive Queries

```php
// ALWAYS cache expensive queries:
function myshop_get_featured_products(): array {
    $cached = get_transient( 'myshop_featured_products' );
    if ( false !== $cached ) {
        return $cached;
    }
    $repo     = MyShopPlugin::instance()->get( 'product_repo' );
    $products = $repo->find_all( [ 'meta_key' => '_featured', 'meta_value' => '1' ] );
    set_transient( 'myshop_featured_products', $products, HOUR_IN_SECONDS );
    return $products;
}

// Invalidate on change:
add_action( 'save_post_product', function(): void {
    delete_transient( 'myshop_featured_products' );
} );
```

### Hardcoded Queries and Magic Numbers

```php
// BAD:
$wpdb->get_results( "SELECT * FROM wp_posts WHERE post_type = 'product' LIMIT 10" );

// GOOD: use $wpdb->prefix and named constants
$wpdb->get_results( $wpdb->prepare(
    "SELECT * FROM {$wpdb->posts} WHERE post_type = %s LIMIT %d",
    'product',
    self::DEFAULT_LIMIT
) );
```

### Summary of Rules

1. **Repositories** wrap all data access. Templates and services never touch `$wpdb` or `WP_Query` directly.
2. **Services** contain business logic, receive dependencies via constructor, and never call `add_action` themselves.
3. **Value Objects** enforce domain rules at construction time. Use them for prices, emails, slugs, any constrained type.
4. **Hooks are domain events.** Use `do_action` to dispatch, `add_action` to subscribe. Wire them at bootstrap only.
5. **Plugins are bounded contexts.** Cross-plugin communication happens only through hooks and shared interfaces.
6. **functions.php is a bootloader.** It requires files. It defines constants. It does nothing else.
7. **Cache everything expensive.** Transients for queries, object cache for session data, `update_meta_cache` to prevent N+1.
8. **Prepare all SQL.** Every `$wpdb` call uses `$wpdb->prepare()`. No exceptions. No string concatenation in queries.
