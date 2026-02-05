---
name: wordpress-development
description: "This skill provides comprehensive WordPress development expertise including self-hosted setup with Docker and Nginx, theme development (block and classic), plugin development with security best practices, performance optimization, and security hardening. Use this skill when setting up WordPress environments, developing themes or plugins, optimizing page load times, or implementing security measures. Triggers on requests involving WordPress, WP-CLI, WordPress hooks and filters, theme customization, plugin creation, or WordPress security and performance."
user-invocable: true
---

# WordPress Development Skill

Expert-level WordPress development guidance covering the full stack: infrastructure, themes, plugins, performance, and security.

## When to Use This Skill

- Setting up self-hosted WordPress (Docker, server configuration, WP-CLI)
- Developing WordPress themes (block themes, classic themes, child themes)
- Building WordPress plugins (hooks, REST API, custom post types, settings pages)
- Optimizing WordPress performance (caching, lazy loading, database, CDN)
- Implementing WordPress security (sanitization, nonces, capability checks, OWASP)

## Quick Reference

### Essential WP-CLI Commands

```bash
# Core management
wp core download --locale=en_US
wp core install --url="example.com" --title="Site" --admin_user="admin" --admin_password="password" --admin_email="admin@example.com"
wp core update
wp core verify-checksums

# Plugin management
wp plugin install <plugin-slug> --activate
wp plugin update --all
wp plugin deactivate <plugin-slug>

# Database
wp db export backup.sql
wp db import backup.sql
wp search-replace 'old-domain.com' 'new-domain.com' --dry-run

# Maintenance
wp cache flush
wp transient delete --all
wp cron event run --due-now
```

### Project Structure Standards

```
project/
├── docker/
│   ├── docker-compose.yml
│   ├── nginx/
│   │   └── default.conf
│   └── php/
│       └── uploads.ini
├── wp-content/
│   ├── themes/
│   │   └── theme-name/
│   ├── plugins/
│   │   └── plugin-name/
│   └── uploads/
└── .env
```

---

## 1. Self-Hosted WordPress Setup

### Docker + Nginx Setup

To set up a new WordPress environment, use the Docker Compose configuration in `assets/docker/`.

```bash
# Copy and customize
cp -r assets/docker/ ./docker
cp assets/docker/.env.example .env

# Edit environment variables
nano .env

# Start services
docker-compose up -d

# Install WordPress via WP-CLI
docker-compose exec wordpress wp core install \
  --url="localhost" \
  --title="My Site" \
  --admin_user="admin" \
  --admin_password="secure_password" \
  --admin_email="admin@example.com"
```

### Production Checklist

- [ ] Configure SSL/TLS with Let's Encrypt
- [ ] Set up automated backups (database + uploads)
- [ ] Configure proper file permissions (755 dirs, 644 files)
- [ ] Disable file editing in wp-config.php: `define('DISALLOW_FILE_EDIT', true);`
- [ ] Set proper memory limits: `define('WP_MEMORY_LIMIT', '256M');`
- [ ] Configure Redis/Memcached for object caching
- [ ] Set up log rotation

### wp-config.php Security Settings

```php
// Disable file editing
define('DISALLOW_FILE_EDIT', true);

// Force SSL admin
define('FORCE_SSL_ADMIN', true);

// Limit revisions
define('WP_POST_REVISIONS', 5);

// Auto-save interval
define('AUTOSAVE_INTERVAL', 300);

// Security keys (generate at https://api.wordpress.org/secret-key/1.1/salt/)
define('AUTH_KEY', 'unique-phrase');
define('SECURE_AUTH_KEY', 'unique-phrase');
define('LOGGED_IN_KEY', 'unique-phrase');
define('NONCE_KEY', 'unique-phrase');
define('AUTH_SALT', 'unique-phrase');
define('SECURE_AUTH_SALT', 'unique-phrase');
define('LOGGED_IN_SALT', 'unique-phrase');
define('NONCE_SALT', 'unique-phrase');
```

---

## 2. Theme Development

### Block Theme Structure (WordPress 5.9+)

```
theme-name/
├── style.css                 # Theme metadata
├── theme.json                # Global styles and settings
├── functions.php             # Theme setup (minimal)
├── templates/
│   ├── index.html            # Fallback template
│   ├── single.html           # Single post
│   ├── page.html             # Single page
│   ├── archive.html          # Archive pages
│   ├── 404.html              # Not found
│   └── parts/
│       ├── header.html       # Header template part
│       └── footer.html       # Footer template part
├── patterns/                 # Block patterns
│   └── hero.php
└── assets/
    ├── css/
    ├── js/
    └── images/
```

### theme.json Configuration

```json
{
  "$schema": "https://schemas.wp.org/trunk/theme.json",
  "version": 2,
  "settings": {
    "color": {
      "palette": [
        { "slug": "primary", "color": "#0073aa", "name": "Primary" },
        { "slug": "secondary", "color": "#23282d", "name": "Secondary" }
      ]
    },
    "typography": {
      "fontFamilies": [
        {
          "fontFamily": "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
          "slug": "system",
          "name": "System"
        }
      ],
      "fontSizes": [
        { "slug": "small", "size": "0.875rem", "name": "Small" },
        { "slug": "medium", "size": "1rem", "name": "Medium" },
        { "slug": "large", "size": "1.5rem", "name": "Large" }
      ]
    },
    "layout": {
      "contentSize": "800px",
      "wideSize": "1200px"
    }
  },
  "styles": {
    "color": {
      "background": "var(--wp--preset--color--white)",
      "text": "var(--wp--preset--color--secondary)"
    }
  }
}
```

### Classic Theme Essentials

```php
<?php
// functions.php - Theme setup

declare(strict_types=1);

namespace ThemeName;

// Autoload classes
spl_autoload_register(function (string $class): void {
    $prefix = 'ThemeName\\';
    $base_dir = __DIR__ . '/inc/';

    $len = strlen($prefix);
    if (strncmp($prefix, $class, $len) !== 0) {
        return;
    }

    $relative_class = substr($class, $len);
    $file = $base_dir . str_replace('\\', '/', $relative_class) . '.php';

    if (file_exists($file)) {
        require $file;
    }
});

add_action('after_setup_theme', function (): void {
    // Theme supports
    add_theme_support('title-tag');
    add_theme_support('post-thumbnails');
    add_theme_support('html5', [
        'search-form',
        'comment-form',
        'comment-list',
        'gallery',
        'caption',
        'style',
        'script',
    ]);
    add_theme_support('responsive-embeds');
    add_theme_support('wp-block-styles');

    // Register menus
    register_nav_menus([
        'primary' => __('Primary Menu', 'theme-name'),
        'footer'  => __('Footer Menu', 'theme-name'),
    ]);
});

add_action('wp_enqueue_scripts', function (): void {
    $theme_version = wp_get_theme()->get('Version');

    // Styles
    wp_enqueue_style(
        'theme-style',
        get_stylesheet_uri(),
        [],
        $theme_version
    );

    // Scripts
    wp_enqueue_script(
        'theme-script',
        get_theme_file_uri('/assets/js/main.js'),
        [],
        $theme_version,
        true
    );
});
```

### Child Theme Setup

```php
<?php
/**
 * Theme Name: Parent Theme Child
 * Template: parent-theme
 * Version: 1.0.0
 */

add_action('wp_enqueue_scripts', function (): void {
    wp_enqueue_style(
        'parent-style',
        get_template_directory_uri() . '/style.css'
    );

    wp_enqueue_style(
        'child-style',
        get_stylesheet_uri(),
        ['parent-style'],
        wp_get_theme()->get('Version')
    );
});
```

---

## 3. Plugin Development

### Plugin Boilerplate

To create a new plugin, use the boilerplate in `assets/plugin-boilerplate/` or run:

```bash
python3 scripts/create-plugin.py my-plugin-name "My Plugin" "Plugin description"
```

### Plugin Structure (PSR-12 + WordPress)

```
plugin-name/
├── plugin-name.php           # Main plugin file
├── uninstall.php             # Cleanup on uninstall
├── composer.json             # Dependencies
├── phpcs.xml                 # Coding standards
├── src/
│   ├── Plugin.php            # Main plugin class
│   ├── Admin/
│   │   ├── Settings.php      # Settings page
│   │   └── MetaBox.php       # Meta boxes
│   ├── Frontend/
│   │   └── Shortcodes.php    # Shortcodes
│   ├── PostTypes/
│   │   └── CustomPost.php    # Custom post types
│   └── Rest/
│       └── Api.php           # REST API endpoints
├── assets/
│   ├── css/
│   ├── js/
│   └── images/
├── templates/
│   └── admin/
├── languages/
│   └── plugin-name.pot
└── tests/
    └── Unit/
```

### Main Plugin File Pattern

```php
<?php
/**
 * Plugin Name: My Plugin
 * Plugin URI: https://example.com/plugin
 * Description: Plugin description here.
 * Version: 1.0.0
 * Requires at least: 6.0
 * Requires PHP: 8.0
 * Author: Your Name
 * Author URI: https://example.com
 * License: GPL v2 or later
 * License URI: https://www.gnu.org/licenses/gpl-2.0.html
 * Text Domain: my-plugin
 * Domain Path: /languages
 */

declare(strict_types=1);

namespace MyPlugin;

// Prevent direct access
defined('ABSPATH') || exit;

// Plugin constants
define('MY_PLUGIN_VERSION', '1.0.0');
define('MY_PLUGIN_FILE', __FILE__);
define('MY_PLUGIN_PATH', plugin_dir_path(__FILE__));
define('MY_PLUGIN_URL', plugin_dir_url(__FILE__));

// Composer autoloader
if (file_exists(MY_PLUGIN_PATH . 'vendor/autoload.php')) {
    require_once MY_PLUGIN_PATH . 'vendor/autoload.php';
}

// Initialize plugin
add_action('plugins_loaded', function (): void {
    load_plugin_textdomain('my-plugin', false, dirname(plugin_basename(__FILE__)) . '/languages');
    Plugin::getInstance()->init();
});

// Activation hook
register_activation_hook(__FILE__, function (): void {
    Plugin::activate();
});

// Deactivation hook
register_deactivation_hook(__FILE__, function (): void {
    Plugin::deactivate();
});
```

### Common Hooks Reference

```php
// Actions - Execute code at specific points
add_action('init', 'register_post_types');                    // After WP loads
add_action('admin_init', 'register_settings');                // Admin initialization
add_action('admin_menu', 'add_menu_pages');                   // Add admin menus
add_action('wp_enqueue_scripts', 'enqueue_frontend_assets');  // Frontend assets
add_action('admin_enqueue_scripts', 'enqueue_admin_assets');  // Admin assets
add_action('save_post', 'save_meta_data', 10, 3);             // Post save
add_action('wp_ajax_my_action', 'ajax_handler');              // Logged-in AJAX
add_action('wp_ajax_nopriv_my_action', 'ajax_handler');       // Guest AJAX
add_action('rest_api_init', 'register_rest_routes');          // REST API routes

// Filters - Modify data
add_filter('the_content', 'modify_content');                  // Post content
add_filter('the_title', 'modify_title');                      // Post title
add_filter('upload_mimes', 'add_mime_types');                 // Allowed uploads
add_filter('plugin_action_links_' . $basename, 'add_links');  // Plugin links
```

### Custom Post Type Registration

```php
<?php

declare(strict_types=1);

namespace MyPlugin\PostTypes;

class Product
{
    public const POST_TYPE = 'product';

    public function register(): void
    {
        add_action('init', [$this, 'registerPostType']);
        add_action('init', [$this, 'registerTaxonomies']);
    }

    public function registerPostType(): void
    {
        $labels = [
            'name'               => __('Products', 'my-plugin'),
            'singular_name'      => __('Product', 'my-plugin'),
            'add_new'            => __('Add New', 'my-plugin'),
            'add_new_item'       => __('Add New Product', 'my-plugin'),
            'edit_item'          => __('Edit Product', 'my-plugin'),
            'new_item'           => __('New Product', 'my-plugin'),
            'view_item'          => __('View Product', 'my-plugin'),
            'search_items'       => __('Search Products', 'my-plugin'),
            'not_found'          => __('No products found', 'my-plugin'),
            'not_found_in_trash' => __('No products found in trash', 'my-plugin'),
        ];

        $args = [
            'labels'              => $labels,
            'public'              => true,
            'publicly_queryable'  => true,
            'show_ui'             => true,
            'show_in_menu'        => true,
            'show_in_rest'        => true,  // Enable Gutenberg
            'query_var'           => true,
            'rewrite'             => ['slug' => 'products', 'with_front' => false],
            'capability_type'     => 'post',
            'has_archive'         => true,
            'hierarchical'        => false,
            'menu_position'       => 5,
            'menu_icon'           => 'dashicons-cart',
            'supports'            => ['title', 'editor', 'thumbnail', 'excerpt', 'custom-fields'],
        ];

        register_post_type(self::POST_TYPE, $args);
    }

    public function registerTaxonomies(): void
    {
        register_taxonomy('product_category', self::POST_TYPE, [
            'labels'            => [
                'name'          => __('Categories', 'my-plugin'),
                'singular_name' => __('Category', 'my-plugin'),
            ],
            'hierarchical'      => true,
            'public'            => true,
            'show_in_rest'      => true,
            'rewrite'           => ['slug' => 'product-category'],
        ]);
    }
}
```

### Settings Page Pattern

```php
<?php

declare(strict_types=1);

namespace MyPlugin\Admin;

class Settings
{
    private const OPTION_GROUP = 'my_plugin_options';
    private const OPTION_NAME = 'my_plugin_settings';
    private const PAGE_SLUG = 'my-plugin-settings';

    public function register(): void
    {
        add_action('admin_menu', [$this, 'addMenuPage']);
        add_action('admin_init', [$this, 'registerSettings']);
    }

    public function addMenuPage(): void
    {
        add_options_page(
            __('My Plugin Settings', 'my-plugin'),
            __('My Plugin', 'my-plugin'),
            'manage_options',
            self::PAGE_SLUG,
            [$this, 'renderPage']
        );
    }

    public function registerSettings(): void
    {
        register_setting(
            self::OPTION_GROUP,
            self::OPTION_NAME,
            [
                'type'              => 'array',
                'sanitize_callback' => [$this, 'sanitize'],
                'default'           => $this->getDefaults(),
            ]
        );

        add_settings_section(
            'general_section',
            __('General Settings', 'my-plugin'),
            null,
            self::PAGE_SLUG
        );

        add_settings_field(
            'enable_feature',
            __('Enable Feature', 'my-plugin'),
            [$this, 'renderCheckbox'],
            self::PAGE_SLUG,
            'general_section',
            ['field' => 'enable_feature']
        );
    }

    public function sanitize(array $input): array
    {
        $sanitized = [];
        $sanitized['enable_feature'] = isset($input['enable_feature']) ? 1 : 0;
        return $sanitized;
    }

    private function getDefaults(): array
    {
        return ['enable_feature' => 0];
    }

    public function renderCheckbox(array $args): void
    {
        $options = get_option(self::OPTION_NAME, $this->getDefaults());
        $field = $args['field'];
        $checked = checked($options[$field] ?? 0, 1, false);

        printf(
            '<input type="checkbox" name="%s[%s]" value="1" %s />',
            esc_attr(self::OPTION_NAME),
            esc_attr($field),
            $checked
        );
    }

    public function renderPage(): void
    {
        if (!current_user_can('manage_options')) {
            return;
        }
        ?>
        <div class="wrap">
            <h1><?php echo esc_html(get_admin_page_title()); ?></h1>
            <form action="options.php" method="post">
                <?php
                settings_fields(self::OPTION_GROUP);
                do_settings_sections(self::PAGE_SLUG);
                submit_button();
                ?>
            </form>
        </div>
        <?php
    }
}
```

### REST API Endpoint

```php
<?php

declare(strict_types=1);

namespace MyPlugin\Rest;

use WP_REST_Request;
use WP_REST_Response;
use WP_Error;

class Api
{
    private const NAMESPACE = 'my-plugin/v1';

    public function register(): void
    {
        add_action('rest_api_init', [$this, 'registerRoutes']);
    }

    public function registerRoutes(): void
    {
        register_rest_route(self::NAMESPACE, '/items', [
            [
                'methods'             => 'GET',
                'callback'            => [$this, 'getItems'],
                'permission_callback' => [$this, 'checkReadPermission'],
            ],
            [
                'methods'             => 'POST',
                'callback'            => [$this, 'createItem'],
                'permission_callback' => [$this, 'checkWritePermission'],
                'args'                => $this->getItemArgs(),
            ],
        ]);

        register_rest_route(self::NAMESPACE, '/items/(?P<id>\d+)', [
            [
                'methods'             => 'GET',
                'callback'            => [$this, 'getItem'],
                'permission_callback' => [$this, 'checkReadPermission'],
            ],
            [
                'methods'             => 'PUT',
                'callback'            => [$this, 'updateItem'],
                'permission_callback' => [$this, 'checkWritePermission'],
            ],
            [
                'methods'             => 'DELETE',
                'callback'            => [$this, 'deleteItem'],
                'permission_callback' => [$this, 'checkDeletePermission'],
            ],
        ]);
    }

    public function checkReadPermission(): bool
    {
        return true; // Public read
    }

    public function checkWritePermission(): bool
    {
        return current_user_can('edit_posts');
    }

    public function checkDeletePermission(): bool
    {
        return current_user_can('delete_posts');
    }

    public function getItems(WP_REST_Request $request): WP_REST_Response
    {
        $items = []; // Fetch items
        return new WP_REST_Response($items, 200);
    }

    public function createItem(WP_REST_Request $request): WP_REST_Response|WP_Error
    {
        $title = sanitize_text_field($request->get_param('title'));

        if (empty($title)) {
            return new WP_Error(
                'missing_title',
                __('Title is required', 'my-plugin'),
                ['status' => 400]
            );
        }

        // Create item
        $item_id = wp_insert_post([
            'post_title'  => $title,
            'post_type'   => 'item',
            'post_status' => 'publish',
        ]);

        if (is_wp_error($item_id)) {
            return $item_id;
        }

        return new WP_REST_Response(['id' => $item_id], 201);
    }

    private function getItemArgs(): array
    {
        return [
            'title' => [
                'required'          => true,
                'type'              => 'string',
                'sanitize_callback' => 'sanitize_text_field',
                'validate_callback' => fn($value) => !empty($value),
            ],
        ];
    }
}
```

---

## 4. Performance Optimization

See `references/performance-optimization.md` for comprehensive optimization techniques.

### Quick Performance Wins

```php
// 1. Disable emojis
remove_action('wp_head', 'print_emoji_detection_script', 7);
remove_action('wp_print_styles', 'print_emoji_styles');

// 2. Remove query strings from static resources
add_filter('script_loader_src', fn($src) => remove_query_arg('ver', $src));
add_filter('style_loader_src', fn($src) => remove_query_arg('ver', $src));

// 3. Disable XML-RPC
add_filter('xmlrpc_enabled', '__return_false');

// 4. Limit post revisions in wp-config.php
define('WP_POST_REVISIONS', 5);

// 5. Increase memory limit
define('WP_MEMORY_LIMIT', '256M');
```

### Database Optimization

```sql
-- Delete all revisions
DELETE FROM wp_posts WHERE post_type = 'revision';

-- Delete orphaned postmeta
DELETE pm FROM wp_postmeta pm
LEFT JOIN wp_posts p ON p.ID = pm.post_id
WHERE p.ID IS NULL;

-- Delete expired transients
DELETE FROM wp_options WHERE option_name LIKE '%_transient_%'
AND option_name NOT LIKE '%_transient_timeout_%';

-- Optimize tables
OPTIMIZE TABLE wp_options, wp_posts, wp_postmeta, wp_comments;
```

### Lazy Loading & Async

```php
// Defer non-critical scripts
add_filter('script_loader_tag', function (string $tag, string $handle): string {
    $defer_scripts = ['theme-script', 'analytics'];

    if (in_array($handle, $defer_scripts, true)) {
        return str_replace(' src', ' defer src', $tag);
    }

    return $tag;
}, 10, 2);

// Native lazy loading for images
add_filter('wp_get_attachment_image_attributes', function (array $attr): array {
    $attr['loading'] = 'lazy';
    $attr['decoding'] = 'async';
    return $attr;
});
```

### Object Caching with Redis

```php
// wp-config.php
define('WP_REDIS_HOST', 'redis');
define('WP_REDIS_PORT', 6379);
define('WP_REDIS_DATABASE', 0);

// Use in plugin/theme
$cache_key = 'my_expensive_query';
$data = wp_cache_get($cache_key);

if (false === $data) {
    $data = expensive_database_query();
    wp_cache_set($cache_key, $data, '', 3600); // 1 hour
}
```

---

## 5. Security Best Practices

See `references/security-checklist.md` for the complete security checklist.

### Input Sanitization

```php
// Text input
$title = sanitize_text_field($_POST['title']);
$email = sanitize_email($_POST['email']);
$url = esc_url_raw($_POST['url']);

// HTML content (allow safe tags)
$content = wp_kses_post($_POST['content']);

// Filename
$filename = sanitize_file_name($_POST['filename']);

// Integer
$id = absint($_POST['id']);

// Array of integers
$ids = array_map('absint', (array) $_POST['ids']);
```

### Output Escaping

```php
// HTML attributes
<input value="<?php echo esc_attr($value); ?>">

// HTML content
<p><?php echo esc_html($text); ?></p>

// URLs
<a href="<?php echo esc_url($url); ?>">Link</a>

// JavaScript
<script>var data = <?php echo wp_json_encode($data); ?>;</script>

// Translations with escaping
echo esc_html__('Translated text', 'text-domain');
echo esc_attr__('Translated attribute', 'text-domain');
```

### Nonce Verification

```php
// Create nonce field in form
wp_nonce_field('my_action_nonce', 'my_nonce');

// Verify nonce on submission
public function handleFormSubmit(): void
{
    // Check nonce
    if (!isset($_POST['my_nonce']) ||
        !wp_verify_nonce($_POST['my_nonce'], 'my_action_nonce')) {
        wp_die(__('Security check failed', 'my-plugin'));
    }

    // Check capability
    if (!current_user_can('manage_options')) {
        wp_die(__('Unauthorized access', 'my-plugin'));
    }

    // Process form...
}

// AJAX nonce
wp_localize_script('my-script', 'myAjax', [
    'url'   => admin_url('admin-ajax.php'),
    'nonce' => wp_create_nonce('my_ajax_nonce'),
]);

// Verify AJAX nonce
public function ajaxHandler(): void
{
    check_ajax_referer('my_ajax_nonce', 'nonce');
    // Process AJAX...
    wp_send_json_success(['message' => 'Success']);
}
```

### Capability Checks

```php
// Check before action
if (!current_user_can('edit_post', $post_id)) {
    wp_die(__('You cannot edit this post.', 'my-plugin'));
}

// Check in REST API
'permission_callback' => function (WP_REST_Request $request): bool {
    $post_id = $request->get_param('id');
    return current_user_can('edit_post', $post_id);
}

// Check for specific capability
if (current_user_can('manage_options')) {
    // Admin only code
}
```

### SQL Injection Prevention

```php
// ALWAYS use $wpdb->prepare()
global $wpdb;

// Wrong - SQL injection vulnerable
$results = $wpdb->get_results(
    "SELECT * FROM {$wpdb->posts} WHERE post_title = '$title'"
);

// Correct - Using prepare
$results = $wpdb->get_results(
    $wpdb->prepare(
        "SELECT * FROM {$wpdb->posts} WHERE post_title = %s",
        $title
    )
);

// Multiple placeholders
$results = $wpdb->get_results(
    $wpdb->prepare(
        "SELECT * FROM {$wpdb->posts} WHERE post_type = %s AND ID = %d",
        $post_type,
        $post_id
    )
);

// IN clause with array
$ids = [1, 2, 3];
$placeholders = implode(',', array_fill(0, count($ids), '%d'));
$results = $wpdb->get_results(
    $wpdb->prepare(
        "SELECT * FROM {$wpdb->posts} WHERE ID IN ($placeholders)",
        ...$ids
    )
);
```

### File Upload Security

```php
public function handleFileUpload(): array|WP_Error
{
    // Check nonce and capability first
    if (!current_user_can('upload_files')) {
        return new WP_Error('unauthorized', 'Cannot upload files');
    }

    $file = $_FILES['my_file'];

    // Validate file type
    $allowed_types = ['image/jpeg', 'image/png', 'image/gif', 'application/pdf'];
    $file_type = wp_check_filetype($file['name']);

    if (!in_array($file_type['type'], $allowed_types, true)) {
        return new WP_Error('invalid_type', 'File type not allowed');
    }

    // Validate file size (5MB max)
    if ($file['size'] > 5 * 1024 * 1024) {
        return new WP_Error('too_large', 'File exceeds maximum size');
    }

    // Use WordPress upload handling
    require_once ABSPATH . 'wp-admin/includes/file.php';
    require_once ABSPATH . 'wp-admin/includes/media.php';
    require_once ABSPATH . 'wp-admin/includes/image.php';

    $upload = wp_handle_upload($file, ['test_form' => false]);

    if (isset($upload['error'])) {
        return new WP_Error('upload_error', $upload['error']);
    }

    return $upload;
}
```

### XSS Prevention Checklist

1. **Always escape output** - Use `esc_html()`, `esc_attr()`, `esc_url()`, `wp_kses_post()`
2. **Never trust user input** - Sanitize all input before processing
3. **Use Content Security Policy** - Add CSP headers
4. **Validate data types** - Ensure integers are integers, emails are emails
5. **Use prepared statements** - Never concatenate SQL queries

---

## Coding Standards

This skill follows **PSR-12 + WordPress** standards:

```xml
<!-- phpcs.xml -->
<?xml version="1.0"?>
<ruleset name="WordPress Plugin">
    <description>PSR-12 with WordPress additions</description>

    <rule ref="PSR12"/>
    <rule ref="WordPress.Security"/>
    <rule ref="WordPress.DB.PreparedSQL"/>
    <rule ref="WordPress.WP.I18n"/>

    <file>./src</file>
    <file>./plugin-name.php</file>

    <exclude-pattern>/vendor/*</exclude-pattern>
    <exclude-pattern>/node_modules/*</exclude-pattern>
</ruleset>
```

Run with: `composer require --dev squizlabs/php_codesniffer wp-coding-standards/wpcs`

---

## Resources

- **Docker setup**: `assets/docker/`
- **Plugin boilerplate**: `assets/plugin-boilerplate/`
- **Theme boilerplate**: `assets/theme-boilerplate/`
- **Security checklist**: `references/security-checklist.md`
- **Performance guide**: `references/performance-optimization.md`
- **Create plugin script**: `scripts/create-plugin.py`
- **Create theme script**: `scripts/create-theme.py`
