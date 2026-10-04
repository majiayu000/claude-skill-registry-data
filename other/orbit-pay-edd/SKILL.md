---
name: orbit-pay-edd
description: Easy Digital Downloads license-server integration audit — license check + activation + deactivation, license key storage, expired-license handling, EDD Software Licensing API endpoints, plugin-update integration via EDD_SL_Plugin_Updater. Use when the user says "EDD license", "Software Licensing", "plugin update from EDD store", "license server".
---

# 🪐 orbit-pay-edd — EDD Software Licensing integration

Most premium WP plugins distribute via EDD + Software Licensing. This skill audits the integration on the consumer side (your plugin checking its license).

---

## What this skill checks

### 1. EDD_SL_Plugin_Updater integration
**Whitepaper intent:** EDD's plugin updater hooks into WP's update system to deliver updates from your store, not WP.org. Without it, customers don't get updates.

```php
require_once 'EDD_SL_Plugin_Updater.php';

$updater = new EDD_SL_Plugin_Updater(
  'https://store.example.com',  // your EDD store URL
  __FILE__,
  [
    'version' => '2.5.0',
    'license' => $license_key,
    'item_id' => 12345,  // product ID in EDD
    'author'  => 'Your Name',
    'beta'    => false,
  ]
);
```

### 2. License activation / deactivation
```php
// Activate
$response = wp_remote_post( 'https://store.example.com', [
  'body' => [
    'edd_action' => 'activate_license',
    'license' => $license_key,
    'item_id' => 12345,
    'url' => home_url(),
  ],
]);
```

Store the resulting `license_status` and re-check periodically.

### 3. Periodic re-check (don't trust forever)
```php
// Re-check every 24h (don't hammer the store)
if ( time() - get_option( 'last_license_check' ) > DAY_IN_SECONDS ) {
  // Run check_license action
  update_option( 'last_license_check', time() );
}
```

### 4. Expired-license behaviour
**Whitepaper intent:** When license expires, plugin should still WORK (don't ransom the customer's site) but not receive updates. UI surfaces "license expired, renew to keep getting updates."

```php
// ❌ Disable plugin entirely on expiry — bad practice, breaks customer trust
if ( $license_status !== 'valid' ) deactivate_plugins( __FILE__ );

// ✅ Just block updates + show notice
if ( $license_status !== 'valid' ) {
  add_action( 'admin_notices', 'my_plugin_renew_notice' );
}
```

### 5. License-key storage
- Store in `wp_options`, not a custom table (encrypted at rest preferred)
- Don't expose in REST API
- Don't include in plugin export / migration

### 6. Environment-aware (dev / staging / live)
EDD Software Licensing limits "activations per license" — counts based on URL. A dev + staging + production setup uses 3 activations. Document this.

```php
// Skip license activation on dev/staging
if ( wp_get_environment_type() !== 'production' ) {
  return;
}
```

### 7. Beta channel (optional)
For users on a beta tier, set `'beta' => true` in `EDD_SL_Plugin_Updater` to get beta releases.

---

## Output

```markdown
# EDD License Integration — my-plugin

✓ EDD_SL_Plugin_Updater initialized
✓ License key stored in option (not custom table)
✓ Activation + deactivation flow correct
❌ Re-check runs on EVERY admin page load — recommend 24h transient
⚠ On expiry, plugin disables entirely — recommend keeping plugin active, blocking updates only
⚠ License URL hardcoded — won't survive store domain change. Use a constant.
```

---

## Pair with

- `/orbit-pay-freemius` — alt licensing SDK
- `/orbit-life-activation` — activation hook safety
- `/orbit-wp-security` — license key handling

---

## Sources & Evergreen References

### Canonical docs
- [EDD Software Licensing](https://easydigitaldownloads.com/downloads/software-licensing/) — addon docs
- [EDD_SL_Plugin_Updater Source](https://github.com/easydigitaldownloads/EDD-License-handler) — reference impl
- [EDD API](https://easydigitaldownloads.com/docs/edd-api-reference/) — store API

### Last reviewed
- 2026-04-29
