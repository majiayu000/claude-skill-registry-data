---
name: wp-activation
description: Handle WordPress plugin activation and deactivation hooks.
---

# WP Activation Handler

## Instructions

When implementing activation/deactivation logic:

1. **Activation hook**: `register_activation_hook(__FILE__, $callback)`
2. **Deactivation hook**: `register_deactivation_hook(__FILE__, $callback)`
3. **Set default options** on activation
4. **Flush rewrite rules** if needed
5. **Clean up** on deactivation

## Activation Pattern

```php
register_activation_hook(retrologin_plugin_file(), 'retrologin_activate');

function retrologin_activate(): void {
    // Set default options
    $defaults = [
        'color' => '#ff6b9d',
        'font' => 'Press Start 2P',
        'enabled' => true,
    ];

    if (! get_option('retrologin_settings')) {
        add_option('retrologin_settings', $defaults);
    }

    // Flush rewrite rules if needed
    flush_rewrite_rules();
}
```

## Deactivation Pattern

```php
register_deactivation_hook(retrologin_plugin_file(), 'retrologin_deactivate');

function retrologin_deactivate(): void {
    // Clear scheduled events
    wp_clear_scheduled_hook('retrologin_daily_task');

    // Optionally: Remove options
    // delete_option('retrologin_settings');
}
```

## Uninstaller Pattern

```php
// In uninstall.php
if (! defined('WP_UNINSTALL_PLUGIN')) {
    exit;
}

// Clean up all plugin data
delete_option('retrologin_settings');
delete_transient('retrologin_cache');

// Clean up user meta if any
delete_metadata('user', '', '_retrologin_preferences', '', true);
```

## Guidelines

-   Keep callbacks in `inc/` directory
-   Don't output anything in activation
-   Handle multi-site activation if needed
-   Test activation on fresh install
