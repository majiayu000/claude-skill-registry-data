---
name: orbit-multisite
description: Multisite (network) compatibility testing for a WordPress plugin — network activation, super-admin capability checks, per-site vs network-wide settings, sub-directory and sub-domain installs, switch_to_blog() safety, and uninstall on a network. Use when the user says "multisite", "network activation", "super admin", "WP MU", or before claiming "multisite compatible" in the plugin header.
---

# 🪐 orbit-multisite — Multisite / network compatibility

WordPress Multisite runs ~5-10% of all WP installs. If your plugin works on single but breaks on multisite, you'll get the bug report. This skill catches it first.

---

## Quick start

```bash
# Spin up a multisite test environment
bash ~/Claude/orbit/scripts/create-test-site.sh --plugin . --port 8881 --multisite subdir

# Run the multisite spec
PLUGIN_SLUG=my-plugin npx playwright test --project=multisite

# Audit code
claude "/orbit-multisite Audit ~/plugins/my-plugin for multisite-safe patterns. Output markdown."
```

---

## What this skill checks

### Activation
- ❌ `register_activation_hook` runs only on the activation site (not network-wide)
- ❌ Network-activate triggers `register_activation_hook` once for the network — your plugin must handle this case
- ✅ Use `is_multisite()` and `wp_is_large_network()` to branch behaviour
- ✅ For network-wide tables, run `dbDelta` with `switch_to_blog()` per site OR create on `wpmu_new_blog`

### Capability checks
```php
// ❌ Wrong — 'manage_options' is per-site, super-admin can manage anything
if ( ! current_user_can( 'manage_options' ) ) wp_die( 'Unauthorised' );

// ✅ For network-level settings:
if ( ! current_user_can( 'manage_network_options' ) ) wp_die( 'Unauthorised' );

// ✅ For per-site settings (default):
if ( ! current_user_can( 'manage_options' ) ) wp_die( 'Unauthorised' );
```

### Settings storage
```php
// ❌ Wrong on multisite — same option on every site, can't differ per site
update_option( 'my_plugin_settings', $data );  // BAD if you want per-site

// ✅ Network-wide settings (single value across all sites):
update_site_option( 'my_plugin_network_setting', $data );

// ✅ Per-site (default — same as single install):
update_option( 'my_plugin_settings', $data );

// ✅ Read with auto-fallback to network if site doesn't have it:
$val = get_option( 'my_plugin_x' );
if ( $val === false && is_multisite() ) {
  $val = get_site_option( 'my_plugin_x' );
}
```

### `switch_to_blog()` safety
```php
// ❌ Forgot to restore
foreach ( $sites as $site ) {
  switch_to_blog( $site->blog_id );
  do_stuff();
  // CRITICAL: restore_current_blog() missing — leaks switched state
}

// ✅
foreach ( $sites as $site ) {
  switch_to_blog( $site->blog_id );
  try {
    do_stuff();
  } finally {
    restore_current_blog();
  }
}

// ✅ Or use wp_get_sites() + iterate without switching when possible
```

### Uninstall on a network
`uninstall.php` runs on plugin deletion. On multisite, decide:
- Should every site's data be deleted?
- Or only the network-level data?

```php
// uninstall.php
if ( ! defined( 'WP_UNINSTALL_PLUGIN' ) ) exit;

if ( is_multisite() ) {
  // Iterate every site
  $sites = get_sites( [ 'fields' => 'ids' ] );
  foreach ( $sites as $site_id ) {
    switch_to_blog( $site_id );
    delete_option( 'my_plugin_settings' );
    $wpdb->query( "DROP TABLE IF EXISTS {$wpdb->prefix}my_plugin_data" );
    restore_current_blog();
  }
  // Network-level cleanup
  delete_site_option( 'my_plugin_network_setting' );
} else {
  // Single-site cleanup
  delete_option( 'my_plugin_settings' );
  $wpdb->query( "DROP TABLE IF EXISTS {$wpdb->prefix}my_plugin_data" );
}
```

### File uploads
```php
// ❌ Wrong on multisite — uses single-site upload dir
$upload = wp_upload_dir();

// ✅ Right — wp_upload_dir() handles multisite automatically
// But verify $upload['basedir'] points to per-site dir on multisite
```

### Sub-domain vs sub-directory
- Sub-directory: `example.com/site1/`, `example.com/site2/` — uses path
- Sub-domain: `site1.example.com`, `site2.example.com` — uses host

Cookies, auth, and `home_url()` differ. Test both:
```bash
bash scripts/create-test-site.sh --multisite subdir
bash scripts/create-test-site.sh --multisite subdomain
```

---

## Test plan

```js
// tests/playwright/multisite.spec.js
test('Network activate', async ({ page }) => {
  await gotoAdmin(page, '/wp-admin/network/plugins.php');
  await page.click('button:has-text("Network Activate")');
  await expect(page.getByText('Plugin network activated')).toBeVisible();
});

test('Per-site settings work', async ({ page }) => {
  await gotoAdmin(page, '/site1/wp-admin/admin.php?page=my-plugin');
  await page.getByLabel('API Key').fill('site1-key');
  await page.click('Save');

  await gotoAdmin(page, '/site2/wp-admin/admin.php?page=my-plugin');
  await expect(page.getByLabel('API Key')).toHaveValue('');  // empty on site2
});
```

---

## Plugin header

If your plugin works on multisite, declare it:
```php
/**
 * Network: true
 */
```

This makes "Network Activate" the default activation mode.

---

## Common multisite-specific bugs

| Bug | Cause | Fix |
|---|---|---|
| Settings page 500 on subsite | Capability check uses `manage_network_options` | Use `manage_options` for per-site |
| Plugin works on main site, not subsites | Activation hook didn't run for new sites | Hook into `wpmu_new_blog` |
| Custom table missing on subsites | `dbDelta` runs only on main site | Iterate sites in activation |
| Uninstall left data on subsites | `uninstall.php` runs once for network | Use the multisite uninstall pattern above |
| `home_url()` returns wrong URL | Caching across `switch_to_blog` | Clear cache: `wp_cache_switch_to_blog` |

---

## When to run

- Before declaring "Multisite compatible" in plugin header
- Before any release that touches `register_activation_hook`, settings, or DB tables
- Customer reports "doesn't work on multisite" — start here

---

## Pair with `/orbit-uninstall-test`

`/orbit-uninstall-test` covers single-site uninstall. This skill covers the multisite-network variant. Both must pass before claiming clean uninstall.
