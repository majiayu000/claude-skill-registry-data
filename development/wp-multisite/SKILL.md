---
name: wp-multisite
description: "Use when building or adapting a WordPress plugin for Multisite/Network — network activation (register_activation_hook with $network_wide), network admin pages (network_admin_menu), per-site vs network-wide options (get_option / get_network_option / update_network_option), looping sites with get_sites() + switch_to_blog() / restore_current_blog(), super admin capabilities (is_super_admin(), manage_network, is_network_admin()), table prefix handling ($wpdb->prefix vs $wpdb->base_prefix), blog ID awareness (get_current_blog_id), or detecting multisite context (is_multisite(), is_plugin_active_for_network()). Triggers: \"make my plugin multisite compatible\", \"network activate\", \"network admin page\", \"per-site settings\", \"switch_to_blog()\", \"restore_current_blog()\", \"super admin only feature\", \"why does my plugin break on multisite\", \"run this for every site in the network\", \"network-wide option\", \"plugin only on certain sites\", \"blog ID handling\", \"is_multisite()\", \"is_network_admin()\", \"is_plugin_active_for_network()\", \"get_network_option()\", \"wpdb base_prefix\", \"manage_network capability\", \"network options page\", \"multisite table prefix\", \"site-aware hook registration\", \"get_sites() loop\". Not for: WP-CLI multisite ops; MU-plugins auto-load behaviour (no activation hooks fire)."
---

# WordPress Multisite Plugin Development

> **Model note:** Adapting an existing plugin for multisite involves scattered conditional changes — requires reading across many files to find all `get_option`/`update_option` and activation hooks. Use `sonnet`; `haiku` may miss indirect callers. New builds with multisite in mind from the start are straightforward and can use `haiku`.

Adapt and build plugins that work correctly on WordPress multisite networks. Covers activation scope, option storage, network admin UI, capability model, and safe site-switching patterns.

## When to use

- "Make my plugin multisite compatible", "support network activation".
- "Add a network admin settings page", "store a network-wide option".
- "Loop over all sites and do X", "run a task on every blog".
- "Why does my plugin break on multisite?", "fix table prefix issues".
- "Check if a user is super admin", "restrict to network admin only".

**Not for:** WP-CLI multisite operations — use `wp-wpcli-and-ops` (official skill). General plugin architecture — use `wp-plugin-development`.

## Method

### 1. Detection and guarding

```php
// Is this a multisite network?
if ( is_multisite() ) { ... }

// Is the current screen the network admin?
if ( is_network_admin() ) { ... }

// Is the plugin network-activated?
if ( is_plugin_active_for_network( plugin_basename( __FILE__ ) ) ) { ... }

// Is the user a super admin?
if ( current_user_can( 'manage_network' ) ) { ... }  // preferred
if ( is_super_admin() ) { ... }                       // also fine
```

Never assume `is_multisite()` is false — always write code that handles both cases unless the plugin explicitly requires multisite.

### 2. Activation scope

A plugin can be:
- **Site-activated** — active on one site, hooks run only on that site.
- **Network-activated** — active on all sites, activation hook runs once on the network.

```php
register_activation_hook( __FILE__, 'my_plugin_activate' );

function my_plugin_activate( $network_wide ) {
    if ( $network_wide && is_multisite() ) {
        // Run setup for every existing site
        $sites = get_sites( [ 'number' => 0, 'fields' => 'ids' ] );
        foreach ( $sites as $site_id ) {
            switch_to_blog( $site_id );
            my_plugin_setup_site();
            restore_current_blog();
        }
    } else {
        my_plugin_setup_site();
    }
}

// Also run setup when a new site is created (for network-activated plugins)
add_action( 'wp_initialize_site', function( WP_Site $new_site ) {
    if ( is_plugin_active_for_network( plugin_basename( __FILE__ ) ) ) {
        switch_to_blog( $new_site->blog_id );
        my_plugin_setup_site();
        restore_current_blog();
    }
} );
```

### 3. Option storage: site vs network

| Function | Scope | Storage |
|---|---|---|
| `get_option()` / `update_option()` | Current site | `{prefix}options` (per site) |
| `get_network_option()` / `update_network_option()` | Entire network | `{main_prefix}sitemeta` |
| `get_site_meta()` / `update_site_meta()` | Per-site record | `{main_prefix}blogmeta` |

```php
// Network-wide setting (same value for all sites)
$api_key = get_network_option( null, 'my_plugin_api_key' );
update_network_option( null, 'my_plugin_api_key', sanitize_text_field( $key ) );

// Per-site setting (different value per site)
$setting = get_option( 'my_plugin_site_setting', 'default' );
update_option( 'my_plugin_site_setting', $value );

// Per-site metadata on the site object
$site_note = get_site_meta( get_current_blog_id(), 'my_plugin_note', true );
update_site_meta( get_current_blog_id(), 'my_plugin_note', sanitize_textarea_field( $note ) );
```

### 4. Network admin settings page

```php
// Register under network admin menu
add_action( 'network_admin_menu', function() {
    add_menu_page(
        __( 'My Plugin Network', 'my-plugin' ),
        __( 'My Plugin', 'my-plugin' ),
        'manage_network',             // super admin only
        'my-plugin-network',
        'my_plugin_render_network_page'
    );
} );

// Network admin settings must use wp_redirect — Settings API not available in network admin
add_action( 'network_admin_edit_my_plugin_network_settings', function() {
    check_admin_referer( 'my_plugin_network_settings' );
    if ( ! current_user_can( 'manage_network' ) ) wp_die( -1 );

    update_network_option( null, 'my_plugin_api_key',
        sanitize_text_field( wp_unslash( $_POST['api_key'] ?? '' ) )
    );

    wp_redirect( add_query_arg( [ 'updated' => 'true' ], network_admin_url( 'settings.php?page=my-plugin-network' ) ) );
    exit;
} );

function my_plugin_render_network_page() {
    if ( isset( $_GET['updated'] ) ) {
        echo '<div class="notice notice-success"><p>' . esc_html__( 'Settings saved.', 'my-plugin' ) . '</p></div>';
    }
    $api_key = get_network_option( null, 'my_plugin_api_key', '' );
    ?>
    <div class="wrap">
        <h1><?php esc_html_e( 'My Plugin Network Settings', 'my-plugin' ); ?></h1>
        <form method="post" action="<?php echo esc_url( network_admin_url( 'edit.php?action=my_plugin_network_settings' ) ); ?>">
            <?php wp_nonce_field( 'my_plugin_network_settings' ); ?>
            <table class="form-table">
                <tr>
                    <th scope="row"><?php esc_html_e( 'API Key', 'my-plugin' ); ?></th>
                    <td><input type="text" name="api_key" value="<?php echo esc_attr( $api_key ); ?>" class="regular-text" /></td>
                </tr>
            </table>
            <?php submit_button( __( 'Save Settings', 'my-plugin' ) ); ?>
        </form>
    </div>
    <?php
}
```

### 5. Looping over sites

```php
function my_plugin_run_for_all_sites( callable $callback ) {
    if ( ! is_multisite() ) {
        $callback();
        return;
    }

    $sites = get_sites( [
        'number'     => 0,     // no limit — consider chunking for large networks
        'fields'     => 'ids',
        'archived'   => 0,
        'deleted'    => 0,
        'spam'       => 0,
    ] );

    foreach ( $sites as $site_id ) {
        switch_to_blog( $site_id );
        try {
            $callback( $site_id );
        } finally {
            restore_current_blog(); // always restore, even on exception
        }
    }
}

// Usage
my_plugin_run_for_all_sites( function( $site_id ) {
    update_option( 'my_plugin_version', MY_PLUGIN_VERSION );
} );
```

**Chunked loop for large networks:**
```php
$page  = 1;
$limit = 100;
do {
    $sites = get_sites( [ 'number' => $limit, 'offset' => ( $page - 1 ) * $limit, 'fields' => 'ids' ] );
    foreach ( $sites as $site_id ) {
        switch_to_blog( $site_id );
        my_plugin_process_site();
        restore_current_blog();
    }
    $page++;
} while ( count( $sites ) === $limit );
```

### 6. Custom DB tables on multisite

Each site has its own table prefix. Create per-site tables in the setup function (called per-site in activation):

```php
function my_plugin_setup_site() {
    global $wpdb;
    $table_name      = $wpdb->prefix . 'my_plugin_data'; // $wpdb->prefix is site-specific
    $charset_collate = $wpdb->get_charset_collate();

    $sql = "CREATE TABLE IF NOT EXISTS {$table_name} (
        id bigint(20) NOT NULL AUTO_INCREMENT,
        data longtext NOT NULL,
        PRIMARY KEY (id)
    ) {$charset_collate};";

    require_once ABSPATH . 'wp-admin/includes/upgrade.php';
    dbDelta( $sql );
}
```

For **network-wide** tables (one table shared by all sites), use `$wpdb->base_prefix`:
```php
$network_table = $wpdb->base_prefix . 'my_plugin_network_log';
```

### 7. Capabilities on multisite

```php
// Super admin (network administrator) check
if ( current_user_can( 'manage_network' ) ) { ... }

// Site admin on the CURRENT site
if ( current_user_can( 'manage_options' ) ) { ... }

// Grant a cap only to super admins (can't remove built-in super admin caps)
add_filter( 'user_has_cap', function( $caps, $cap_to_check, $args, $user ) {
    if ( 'manage_network_plugins' === $cap_to_check && ! is_super_admin( $user->ID ) ) {
        $caps['manage_network_plugins'] = false;
    }
    return $caps;
}, 10, 4 );
```

## Notes

- `switch_to_blog()` is expensive — it changes `$wpdb->prefix`, flushes object cache per-site, and swaps several globals. Minimise calls; batch work per site.
- Always wrap `switch_to_blog()` / `restore_current_blog()` in `try/finally` to guarantee restoration even on errors.
- Avoid `BLOG_ID_CURRENT_SITE` constant — use `get_current_blog_id()` and `get_main_site_id()` instead.
- Network admin pages can't use the WordPress Settings API (`register_setting`, `add_settings_section`) — handle saves via `network_admin_edit_{action}` hooks with manual `wp_redirect`.
- On large networks (1000+ sites), avoid `get_sites( [ 'number' => 0 ] )` — chunk with `number`/`offset` or use Action Scheduler (`wp-background-processing`) to process sites asynchronously.

## References

- `references/multisite-patterns.md` — detection helpers, site switching, options API, get_sites() params, table prefix, capabilities, activation hooks.
- `references/network-admin-patterns.md` — network admin menu, network settings save via network_admin_edit_{action}, network option storage, network-wide transients.
- `references/multisite-testing.md` — PHPUnit multisite bootstrap, data-isolation tests, network-activation tests, new-site hook tests, gotchas.
