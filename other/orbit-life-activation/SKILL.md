---
name: orbit-life-activation
description: Audit `register_activation_hook` for safety + idempotency — does the hook handle multisite network-activate, does it create tables via `dbDelta` (not `CREATE TABLE`), does it gracefully handle re-activation (already-installed state), does it trigger expensive ops on activation that should be deferred. Use when the user says "activation hook", "register_activation_hook", "plugin install fails", "activation safety".
---

# 🪐 orbit-life-activation — Activation hook safety

Activation runs once. If it fails, the plugin is half-installed and the user is confused. This skill catches the patterns that bite.

---

## What this skill checks

### 1. Hook registered against the MAIN plugin file
**Whitepaper intent:** `register_activation_hook( __FILE__, ... )` only fires if `__FILE__` is the main plugin file. If you put the hook inside `includes/class-setup.php`, it never fires.

```php
// my-plugin.php (main file)
register_activation_hook( __FILE__, [ 'My_Plugin\Setup', 'activate' ] );

// includes/class-setup.php
class Setup {
  public static function activate() {
    // ... runs ONCE on activation ...
  }
}
```

### 2. Idempotent (re-activation safe)
Activation can run multiple times (user toggles plugin). Every operation must be safe to repeat:

```php
// ❌ Throws if table exists
$wpdb->query( "CREATE TABLE wp_my_plugin (...)" );

// ✅ dbDelta is safe to re-run
require_once ABSPATH . 'wp-admin/includes/upgrade.php';
dbDelta( "CREATE TABLE {$wpdb->prefix}my_plugin (...)" );

// ✅ Option write — idempotent
update_option( 'my_plugin_version', '2.5.0' );

// ❌ Insert that fails on duplicate
$wpdb->insert( $wpdb->options, [ 'option_name' => 'foo', ... ] );

// ✅ Use WP API
add_option( 'foo', 'bar' );  // safe — doesn't replace if exists
```

### 3. Multisite network-activate
**Whitepaper intent:** Network-activation fires the hook once for the network, not per-site. Tables / options must be created on every site.

```php
register_activation_hook( __FILE__, function( $network_wide ) {
  if ( is_multisite() && $network_wide ) {
    foreach ( get_sites( [ 'fields' => 'ids' ] ) as $site_id ) {
      switch_to_blog( $site_id );
      my_plugin_create_tables();
      restore_current_blog();
    }
  } else {
    my_plugin_create_tables();
  }
});
```

### 4. Capability check (defence in depth)
```php
if ( ! current_user_can( 'activate_plugins' ) ) {
  wp_die( __( 'Insufficient permissions.', 'my-plugin' ) );
}
```

### 5. Defer heavy operations
**Whitepaper intent:** Activation runs synchronously during the admin request. If it takes > 5 sec the user sees a timeout / hung browser. Move heavy ops (importing default content, fetching from API) to a deferred cron task.

```php
register_activation_hook( __FILE__, function() {
  my_plugin_create_tables();          // fast, do now
  my_plugin_set_default_options();    // fast, do now

  // Defer slow stuff
  wp_schedule_single_event( time() + 10, 'my_plugin_post_activation_setup' );
});

add_action( 'my_plugin_post_activation_setup', function() {
  my_plugin_import_default_content();   // slow, in cron
});
```

### 6. Don't redirect from activation hook
Activation runs as part of plugin-activation HTTP response. Calling `wp_safe_redirect()` mid-activation breaks the response.

Instead, use `transient + admin_init`:
```php
// In activation hook
register_activation_hook( __FILE__, function() {
  set_transient( 'my_plugin_just_activated', 1, 30 );
});

// Then on next admin load
add_action( 'admin_init', function() {
  if ( get_transient( 'my_plugin_just_activated' ) ) {
    delete_transient( 'my_plugin_just_activated' );
    wp_safe_redirect( admin_url( 'admin.php?page=my-plugin-welcome' ) );
    exit;
  }
});
```

### 7. Don't echo / wp_die mid-activation (silent failure)
WP swallows output during activation. Use `set_transient` for a notice on next page load instead.

---

## Output

```markdown
# Activation Audit — my-plugin

✓ register_activation_hook in main plugin file
✓ Uses dbDelta (idempotent)
❌ Doesn't handle multisite network-activate — tables only created on main site
✓ Has capability check
⚠ Imports 50MB of default content synchronously — defer to cron
❌ Calls wp_redirect inside activation hook — silently fails

Severity: HIGH — multisite + redirect issues will surface as customer reports
```

---

## Pair with

- `/orbit-life-upgrade` — version migration
- `/orbit-life-rollback` — downgrade safety
- `/orbit-uninstall-test` — reverse — uninstall hygiene
- `/orbit-multisite` — network-activation

---

## Sources & Evergreen References

### Canonical docs
- [register_activation_hook](https://developer.wordpress.org/reference/functions/register_activation_hook/) — function ref
- [Activation Hooks Best Practices](https://developer.wordpress.org/plugins/plugin-basics/activation-deactivation-hooks/) — handbook
- [dbDelta](https://developer.wordpress.org/reference/functions/dbdelta/) — schema migrations

### Last reviewed
- 2026-04-29
