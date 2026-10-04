---
name: WordPress Theme Development
description: Expert knowledge in building custom WordPress themes, template hierarchy, hooks, filters, and WordPress.com compatibility. Triggers on keywords like "wordpress theme", "template", "wp_", "get_template_part", "theme.json", "block theme", "functions.php".
version: 1.0.0
---

# WordPress Theme Development

Build modern, performant WordPress themes with proper structure, hooks, and WordPress.com compatibility for SkyyRose.

## When to Use This Skill

Activate when working on:
- Custom WordPress theme development
- Template hierarchy and structure
- functions.php and theme setup
- WordPress hooks and filters
- Custom post types and taxonomies
- Theme customization API
- WordPress.com specific requirements
- Block themes (Full Site Editing)

## Theme Structure

### Modern WordPress Theme

```
skyyrose-2025/
├── style.css                    # Theme header (required)
├── functions.php                # Theme setup
├── index.php                    # Fallback template
├── screenshot.png               # Theme preview (1200x900px)
│
├── header.php                   # Site header
├── footer.php                   # Site footer
├── sidebar.php                  # Sidebar
│
├── template-parts/              # Reusable template parts
│   ├── content.php
│   ├── content-single.php
│   └── navigation.php
│
├── templates/                   # Page templates
│   ├── template-collection.php  # Immersive collections
│   └── template-home.php
│
├── inc/                         # Theme includes
│   ├── setup.php               # Theme setup and registration
│   ├── enqueue.php             # Scripts and styles
│   ├── custom-post-types.php   # CPT registration
│   ├── customizer.php          # Customizer options
│   └── security-hardening.php  # Security headers
│
├── assets/                      # Theme assets
│   ├── css/
│   ├── js/
│   └── images/
│
├── elementor-widgets/           # Custom Elementor widgets
│   ├── product-3d-viewer.php
│   └── collection-grid.php
│
├── woocommerce/                 # WooCommerce template overrides
│   ├── archive-product.php
│   └── single-product.php
│
└── languages/                   # Translation files
    └── skyyrose.pot
```

### style.css Header (Required)

```css
/*
Theme Name: SkyyRose 2025
Theme URI: https://skyyrose.co
Author: SkyyRose LLC
Author URI: https://skyyrose.co
Description: Luxury fashion e-commerce theme with immersive 3D experiences
Version: 1.0.0
Requires at least: 6.0
Tested up to: 6.4
Requires PHP: 8.0
License: Proprietary
License URI: https://skyyrose.co/license
Text Domain: skyyrose
Tags: e-commerce, luxury, fashion, jewelry, woocommerce, elementor, 3d
*/
```

## functions.php Setup

### Theme Setup

```php
<?php
/**
 * SkyyRose 2025 Theme Functions
 *
 * @package SkyyRose_2025
 */

// Prevent direct access
if (!defined('ABSPATH')) {
    exit;
}

// Theme constants
define('SKYYROSE_VERSION', '1.0.0');
define('SKYYROSE_THEME_DIR', get_template_directory());
define('SKYYROSE_THEME_URI', get_template_directory_uri());

// Load theme files
require_once SKYYROSE_THEME_DIR . '/inc/setup.php';
require_once SKYYROSE_THEME_DIR . '/inc/enqueue.php';
require_once SKYYROSE_THEME_DIR . '/inc/customizer.php';
require_once SKYYROSE_THEME_DIR . '/inc/security-hardening.php';

// WooCommerce support
if (class_exists('WooCommerce')) {
    require_once SKYYROSE_THEME_DIR . '/inc/woocommerce.php';
}

// Elementor support
if (did_action('elementor/loaded')) {
    require_once SKYYROSE_THEME_DIR . '/inc/elementor.php';
}
```

### inc/setup.php

```php
<?php
/**
 * Theme setup and registration
 */

add_action('after_setup_theme', 'skyyrose_theme_setup');

function skyyrose_theme_setup() {
    // Translation support
    load_theme_textdomain('skyyrose', SKYYROSE_THEME_DIR . '/languages');

    // Add theme support
    add_theme_support('title-tag');
    add_theme_support('post-thumbnails');
    add_theme_support('automatic-feed-links');
    add_theme_support('html5', [
        'search-form',
        'comment-form',
        'comment-list',
        'gallery',
        'caption',
        'style',
        'script'
    ]);

    // Custom logo
    add_theme_support('custom-logo', [
        'height'      => 100,
        'width'       => 400,
        'flex-height' => true,
        'flex-width'  => true,
    ]);

    // WooCommerce support
    add_theme_support('woocommerce');
    add_theme_support('wc-product-gallery-zoom');
    add_theme_support('wc-product-gallery-lightbox');
    add_theme_support('wc-product-gallery-slider');

    // Custom image sizes
    add_image_size('skyyrose-hero', 1920, 1080, true);
    add_image_size('skyyrose-product', 800, 800, true);
    add_image_size('skyyrose-thumbnail', 400, 400, true);

    // Register navigation menus
    register_nav_menus([
        'primary' => esc_html__('Primary Menu', 'skyyrose'),
        'footer'  => esc_html__('Footer Menu', 'skyyrose'),
    ]);

    // Add editor styles
    add_editor_style('assets/css/editor-style.css');

    // Enable Block Editor features
    add_theme_support('align-wide');
    add_theme_support('responsive-embeds');
    add_theme_support('editor-styles');
}

// Register widget areas
add_action('widgets_init', 'skyyrose_widgets_init');

function skyyrose_widgets_init() {
    register_sidebar([
        'name'          => esc_html__('Shop Sidebar', 'skyyrose'),
        'id'            => 'shop-sidebar',
        'description'   => esc_html__('Appears on shop pages', 'skyyrose'),
        'before_widget' => '<section id="%1$s" class="widget %2$s">',
        'after_widget'  => '</section>',
        'before_title'  => '<h3 class="widget-title">',
        'after_title'   => '</h3>',
    ]);

    register_sidebar([
        'name'          => esc_html__('Footer Area', 'skyyrose'),
        'id'            => 'footer-sidebar',
        'description'   => esc_html__('Appears in the footer', 'skyyrose'),
        'before_widget' => '<div class="footer-widget">',
        'after_widget'  => '</div>',
        'before_title'  => '<h4>',
        'after_title'   => '</h4>',
    ]);
}
```

### inc/enqueue.php

```php
<?php
/**
 * Enqueue scripts and styles
 */

add_action('wp_enqueue_scripts', 'skyyrose_enqueue_assets');

function skyyrose_enqueue_assets() {
    // Main stylesheet
    wp_enqueue_style(
        'skyyrose-style',
        SKYYROSE_THEME_URI . '/style.css',
        [],
        SKYYROSE_VERSION
    );

    // Custom styles
    wp_enqueue_style(
        'skyyrose-custom',
        SKYYROSE_THEME_URI . '/assets/css/custom.css',
        ['skyyrose-style'],
        SKYYROSE_VERSION
    );

    // Fonts — self-hosted woff2, zero CDN (declared in theme.json Font Library + assets/css/fonts.css)
    wp_enqueue_style(
        'skyyrose-fonts',
        SKYYROSE_THEME_URI . '/assets/css/fonts.css',
        [],
        SKYYROSE_VERSION
    );

    // Main JavaScript
    wp_enqueue_script(
        'skyyrose-main',
        SKYYROSE_THEME_URI . '/assets/js/main.js',
        ['jquery'],
        SKYYROSE_VERSION,
        true
    );

    // Localize script
    wp_localize_script('skyyrose-main', 'skyyrose', [
        'ajaxurl' => admin_url('admin-ajax.php'),
        'nonce'   => wp_create_nonce('skyyrose-nonce'),
        'siteUrl' => get_site_url(),
        'brand'   => [
            'primaryColor' => '#B76E79',
            'tagline'      => __('Where Love Meets Luxury', 'skyyrose'),
        ],
    ]);

    // Three.js for 3D viewers (only on product pages)
    if (is_product()) {
        wp_enqueue_script(
            'threejs',
            'https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.min.js',
            [],
            '0.160.0',
            true
        );

        wp_enqueue_script(
            'skyyrose-3d-viewer',
            SKYYROSE_THEME_URI . '/assets/js/3d-viewer.js',
            ['threejs'],
            SKYYROSE_VERSION,
            true
        );
    }

    // Comments
    if (is_singular() && comments_open() && get_option('thread_comments')) {
        wp_enqueue_script('comment-reply');
    }
}
```

## Template Hierarchy

### homepage (index.php fallback)

```php
<?php
/**
 * The main template file
 */

get_header(); ?>

<main id="main" class="site-main" role="main">

    <?php if (have_posts()) : ?>

        <div class="posts-grid">
            <?php while (have_posts()) : the_post(); ?>
                <?php get_template_part('template-parts/content', get_post_type()); ?>
            <?php endwhile; ?>
        </div>

        <?php the_posts_navigation(); ?>

    <?php else : ?>

        <?php get_template_part('template-parts/content', 'none'); ?>

    <?php endif; ?>

</main>

<?php
get_sidebar();
get_footer();
```

### Custom Page Template

```php
<?php
/**
 * Template Name: Immersive Collection
 *
 * @package SkyyRose_2025
 */

get_header(); ?>

<div class="immersive-collection" data-collection="<?php echo esc_attr(get_field('collection_name')); ?>">

    <!-- 3D Canvas -->
    <canvas id="collection-3d-scene"></canvas>

    <!-- Collection Navigation -->
    <nav class="collection-nav">
        <button class="nav-prev" aria-label="Previous room">←</button>
        <button class="nav-next" aria-label="Next room">→</button>
    </nav>

    <!-- Product Hotspots -->
    <div class="product-hotspots">
        <?php
        $products = get_field('featured_products');
        if ($products) :
            foreach ($products as $product) :
                ?>
                <div class="hotspot" data-product-id="<?php echo esc_attr($product->ID); ?>">
                    <button class="hotspot-trigger">
                        <span class="pulse"></span>
                        <span class="sr-only"><?php echo esc_html($product->post_title); ?></span>
                    </button>
                </div>
            <?php
            endforeach;
        endif;
        ?>
    </div>

    <!-- Product Quick View Modal -->
    <div id="product-quick-view" class="modal" aria-hidden="true">
        <div class="modal-content">
            <!-- Populated via AJAX -->
        </div>
    </div>

</div>

<script>
// Initialize 3D scene
document.addEventListener('DOMContentLoaded', () => {
    const collection = document.querySelector('.immersive-collection').dataset.collection;
    initCollectionScene(collection);
});
</script>

<?php get_footer(); ?>
```

## WordPress Hooks

### Common Action Hooks

```php
// Header hooks
add_action('wp_head', 'skyyrose_custom_head', 10);
add_action('wp_enqueue_scripts', 'skyyrose_enqueue_assets', 10);

// Content hooks
add_action('before_post', 'skyyrose_before_post', 10);
add_action('after_post', 'skyyrose_after_post', 10);

// Footer hooks
add_action('wp_footer', 'skyyrose_custom_footer', 10);

// WooCommerce hooks
add_action('woocommerce_before_main_content', 'skyyrose_woo_wrapper_start', 10);
add_action('woocommerce_after_main_content', 'skyyrose_woo_wrapper_end', 10);
add_action('woocommerce_before_shop_loop_item_title', 'skyyrose_product_badge', 15);
```

### Common Filter Hooks

```php
// Excerpt length
add_filter('excerpt_length', 'skyyrose_excerpt_length', 10);

function skyyrose_excerpt_length($length) {
    return 30;
}

// Excerpt more
add_filter('excerpt_more', 'skyyrose_excerpt_more', 10);

function skyyrose_excerpt_more($more) {
    return '...';
}

// Body class
add_filter('body_class', 'skyyrose_body_classes', 10);

function skyyrose_body_classes($classes) {
    if (is_shop() || is_product()) {
        $classes[] = 'woocommerce-page';
    }

    if (has_post_thumbnail()) {
        $classes[] = 'has-featured-image';
    }

    return $classes;
}

// WooCommerce product class
add_filter('woocommerce_post_class', 'skyyrose_product_class', 10, 2);

function skyyrose_product_class($classes, $product) {
    $collection = get_post_meta($product->get_id(), '_skyyrose_collection', true);

    if ($collection) {
        $classes[] = 'collection-' . sanitize_html_class($collection);
    }

    return $classes;
}
```

## WordPress.com Compatibility

### Critical Differences

```php
/**
 * WordPress.com specific adjustments
 */

// Check if running on WordPress.com
function skyyrose_is_wpcom() {
    return defined('IS_WPCOM') && IS_WPCOM;
}

// Adjust REST API endpoints
function skyyrose_rest_url($endpoint) {
    if (skyyrose_is_wpcom()) {
        // WordPress.com uses index.php?rest_route=
        return home_url('/index.php?rest_route=' . $endpoint);
    }

    return rest_url($endpoint);
}

// WordPress.com Content Security Policy
if (skyyrose_is_wpcom()) {
    // Use platform-level CSP
    // Don't try to override headers (won't work)
    // Ensure all resources in whitelist are HTTPS
}

// No FTP/SSH access on WordPress.com
// All deployments via admin UI
// Use WordPress.com Batcache (5-10 min TTL)
```

### WordPress.com REST API

```javascript
// WordPress.com REST API pattern
const wpcomRestUrl = 'https://skyyrose.co/index.php?rest_route=/wp/v2/posts';

// NOT: https://skyyrose.co/wp-json/wp/v2/posts
```

## Custom Post Types

```php
/**
 * Register Collections CPT
 */
add_action('init', 'skyyrose_register_collections_cpt');

function skyyrose_register_collections_cpt() {
    $labels = [
        'name'               => _x('Collections', 'post type general name', 'skyyrose'),
        'singular_name'      => _x('Collection', 'post type singular name', 'skyyrose'),
        'menu_name'          => _x('Collections', 'admin menu', 'skyyrose'),
        'add_new'            => _x('Add New', 'collection', 'skyyrose'),
        'add_new_item'       => __('Add New Collection', 'skyyrose'),
        'edit_item'          => __('Edit Collection', 'skyyrose'),
        'new_item'           => __('New Collection', 'skyyrose'),
        'view_item'          => __('View Collection', 'skyyrose'),
        'search_items'       => __('Search Collections', 'skyyrose'),
        'not_found'          => __('No collections found.', 'skyyrose'),
        'not_found_in_trash' => __('No collections found in Trash.', 'skyyrose'),
    ];

    $args = [
        'labels'             => $labels,
        'public'             => true,
        'publicly_queryable' => true,
        'show_ui'            => true,
        'show_in_menu'       => true,
        'query_var'          => true,
        'rewrite'            => ['slug' => 'collection'],
        'capability_type'    => 'post',
        'has_archive'        => true,
        'hierarchical'       => false,
        'menu_position'      => 5,
        'menu_icon'          => 'dashicons-portfolio',
        'supports'           => ['title', 'editor', 'thumbnail', 'excerpt', 'custom-fields'],
        'show_in_rest'       => true, // Block Editor support
    ];

    register_post_type('collection', $args);
}
```

## Theme Customizer

```php
/**
 * Customizer settings
 */
add_action('customize_register', 'skyyrose_customize_register');

function skyyrose_customize_register($wp_customize) {
    // Brand section
    $wp_customize->add_section('skyyrose_brand', [
        'title'    => __('SkyyRose Branding', 'skyyrose'),
        'priority' => 30,
    ]);

    // Primary color
    $wp_customize->add_setting('skyyrose_primary_color', [
        'default'           => '#B76E79',
        'sanitize_callback' => 'sanitize_hex_color',
        'transport'         => 'postMessage',
    ]);

    $wp_customize->add_control(new WP_Customize_Color_Control($wp_customize, 'skyyrose_primary_color', [
        'label'    => __('Primary Color', 'skyyrose'),
        'section'  => 'skyyrose_brand',
        'settings' => 'skyyrose_primary_color',
    ]));

    // Tagline
    $wp_customize->add_setting('skyyrose_tagline', [
        'default'           => 'Where Love Meets Luxury',
        'sanitize_callback' => 'sanitize_text_field',
    ]);

    $wp_customize->add_control('skyyrose_tagline', [
        'label'    => __('Brand Tagline', 'skyyrose'),
        'section'  => 'skyyrose_brand',
        'type'     => 'text',
    ]);

    // Enable 3D viewers
    $wp_customize->add_setting('skyyrose_enable_3d', [
        'default'           => true,
        'sanitize_callback' => 'rest_sanitize_boolean',
    ]);

    $wp_customize->add_control('skyyrose_enable_3d', [
        'label'    => __('Enable 3D Product Viewers', 'skyyrose'),
        'section'  => 'skyyrose_brand',
        'type'     => 'checkbox',
    ]);
}
```

## Security Best Practices

```php
/**
 * Security hardening
 */

// Escape output
echo esc_html($text);
echo esc_attr($attribute);
echo esc_url($url);
echo wp_kses_post($html);

// Sanitize input
$clean = sanitize_text_field($_POST['field']);
$clean_html = wp_kses_post($_POST['content']);
$clean_url = esc_url_raw($_POST['url']);

// Verify nonces
if (!wp_verify_nonce($_POST['nonce'], 'skyyrose-action')) {
    wp_die('Security check failed');
}

// Check capabilities
if (!current_user_can('edit_posts')) {
    wp_die('Insufficient permissions');
}

// Prepare SQL
$wpdb->prepare(
    "SELECT * FROM {$wpdb->posts} WHERE post_title = %s",
    $title
);
```

## References

See `references/` for:
- `template-hierarchy-guide.md` - Complete template hierarchy
- `hooks-filters-reference.md` - Common hooks and filters
- `wpcom-compatibility.md` - WordPress.com specific requirements
- `security-checklist.md` - Theme security best practices

## Examples

See `examples/` for:
- `custom-post-type.php` - CPT registration
- `customizer-settings.php` - Customizer implementation
- `page-template-immersive.php` - Immersive page template
- `woocommerce-overrides/` - WooCommerce template overrides
