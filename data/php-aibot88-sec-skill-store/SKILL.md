---
name: php
description: PHP development — OOP patterns, Laravel basics, WordPress plugin development, REST API endpoints, wpdb queries, security (sanitization, nonces)
version: 1.0.0
author: veekunth217
tags: [php, oop, laravel, wordpress, plugin, rest-api, wpdb, security, sanitization, nonces]
platforms: [claude-code, cursor, codex]
---

# PHP Skill

Modern PHP development with a focus on WordPress plugin development, OOP patterns, and security.

**RULE: Always show generated class/function signatures before writing full implementation. Wait for GO.**

> **🚧 Status: Stub — implementation pending**
>
> This reference skill has the structure but the snippet content is still being filled in
> (you'll see `<!-- TODO -->` placeholders below). It activates and tells Claude the topic
> exists, but won't yield deep snippets yet.
>
> **Want to help?** Pick any TODO, write the snippet, open a PR. See [CONTRIBUTING.md](../../CONTRIBUTING.md).
> Each contribution moves the skill closer to "Ready" status.

---

## Capabilities

### OOP PHP Patterns
<!-- TODO: Singleton, Factory, Observer patterns in PHP -->
<!-- TODO: Interfaces, abstract classes, traits -->
<!-- TODO: PHP 8.x features: named args, match, fibers, readonly, enums -->
<!-- TODO: Composer autoloading, PSR-4 namespace setup -->

### Laravel Basics
<!-- TODO: Routes, controllers, middleware, request validation -->
<!-- TODO: Eloquent ORM, migrations, factories, seeders -->
<!-- TODO: Blade templates, Livewire basics -->
<!-- TODO: Artisan commands, queues, jobs -->

### Custom Plugin Development
<!-- TODO: Plugin bootstrap pattern (main class, loader, activator, deactivator) -->
<!-- TODO: Admin pages, settings API, options -->
<!-- TODO: Shortcodes, widgets, Gutenberg blocks in PHP -->
<!-- TODO: Plugin update checker (custom update server) -->

### REST API Endpoints
<!-- TODO: register_rest_route, WP_REST_Controller base class -->
<!-- TODO: Authentication (nonce, application passwords, JWT) -->
<!-- TODO: Custom endpoints for WooCommerce data -->
<!-- TODO: Rate limiting, input validation, error responses -->

### Database Queries (wpdb)
<!-- TODO: $wpdb->get_results, get_row, get_var, insert, update, delete -->
<!-- TODO: Prepared statements — never interpolate user input -->
<!-- TODO: Custom table creation in plugin activation -->
<!-- TODO: Query optimization, EXPLAIN, slow query identification -->

### Security (Sanitization, Nonces)
<!-- TODO: sanitize_text_field, sanitize_email, esc_html, esc_attr, esc_url -->
<!-- TODO: wp_nonce_field, check_admin_referer, wp_verify_nonce -->
<!-- TODO: current_user_can() capability checks -->
<!-- TODO: SQL injection prevention, XSS prevention, CSRF protection -->

---

## Patterns Reference

### Secure wpdb query
```php
global $wpdb;
$results = $wpdb->get_results(
    $wpdb->prepare(
        "SELECT * FROM {$wpdb->prefix}my_table WHERE user_id = %d AND status = %s",
        $user_id,
        $status
    )
);
```

### REST API endpoint
```php
add_action( 'rest_api_init', function() {
    register_rest_route( 'myplugin/v1', '/data/(?P<id>\d+)', [
        'methods'             => 'GET',
        'callback'            => 'myplugin_get_data',
        'permission_callback' => function() {
            return current_user_can( 'read' );
        },
        'args' => [
            'id' => [ 'required' => true, 'validate_callback' => 'is_numeric' ]
        ],
    ]);
});

function myplugin_get_data( WP_REST_Request $request ): WP_REST_Response {
    $id   = absint( $request->get_param( 'id' ) );
    $data = get_post_meta( $id, '_my_meta', true );
    return new WP_REST_Response( [ 'data' => $data ], 200 );
}
```

### Nonce verification
```php
// In form
wp_nonce_field( 'myplugin_action', 'myplugin_nonce' );

// On save
if ( ! isset( $_POST['myplugin_nonce'] ) ||
     ! wp_verify_nonce( $_POST['myplugin_nonce'], 'myplugin_action' ) ) {
    wp_die( 'Security check failed' );
}
```

<!-- TODO: Add full interactive workflows for each capability above -->
