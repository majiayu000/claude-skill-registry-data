---
name: orbit-pay-freemius
description: Freemius SDK integration audit — opt-in flow, license check, plan switching, customer support, telemetry, GDPR / privacy disclosures, opt-out behaviour, Freemius vs alternative SDKs (EDD-SL). Use when the user says "Freemius integration", "Freemius SDK", "fs->is_paying", or has a freemium plugin.
---

# 🪐 orbit-pay-freemius — Freemius SDK integration

Freemius is the all-in-one freemium SDK — handles opt-in, licensing, payments, telemetry. Saves time vs DIY but adds 2MB to plugin + asks customers for telemetry. This skill audits responsible use.

---

## What this skill checks

### 1. SDK initialization
```php
require_once dirname( __FILE__ ) . '/freemius/start.php';

function my_plugin_freemius() {
  global $my_plugin_fs;
  if ( ! isset( $my_plugin_fs ) ) {
    $my_plugin_fs = fs_dynamic_init([
      'id' => '12345',
      'slug' => 'my-plugin',
      'public_key' => 'pk_xxx',
      'is_premium' => false,
      'has_addons' => false,
      'has_paid_plans' => true,
      'menu' => [ 'slug' => 'my-plugin', ... ],
      'is_live' => true,
    ]);
  }
  return $my_plugin_fs;
}
my_plugin_freemius();
```

### 2. Opt-in flow (the controversial part)
**Whitepaper intent:** Freemius asks users to "opt in" on first activation — sending telemetry. Some users hate this. Configure to:
- Skip opt-in for free users (`'is_premium_only' => false` if you want telemetry only on paid)
- Make opt-in clearly skippable
- Document what data is sent in your privacy policy

```php
$my_plugin_fs->add_filter( 'permission_diagnostic_default', '__return_false' );  // diagnostic OFF by default
```

### 3. License check
```php
if ( my_plugin_freemius()->is_paying() ) {
  // Premium feature
} else {
  // Free fallback or upgrade prompt
}
```

Avoid `if (! is_paying() ) { wp_die() }` — disabling free features for free users in a freemium plugin = customer trust issue.

### 4. Plan switching
```php
if ( my_plugin_freemius()->is_plan( 'pro' ) ) {
  // Pro tier
} elseif ( my_plugin_freemius()->is_plan( 'enterprise' ) ) {
  // Enterprise tier
}
```

### 5. Telemetry transparency (GDPR)
Document in privacy policy what Freemius sends:
- WP version, PHP version, plugin version
- Site URL (yes — by default)
- Active themes / plugins (if user opts in)
- Plugin-usage metadata

Update `wp_add_privacy_policy_content` accordingly.

### 6. Opt-out option
The free user must always be able to opt out of telemetry without losing functionality.
```php
$my_plugin_fs->add_filter( 'allow_user_skip_opt_in', '__return_true' );
```

### 7. SDK version pinning
**Whitepaper intent:** Freemius SDK auto-loads from `freemius/start.php` — multiple plugins ship different SDK versions. The newest one wins. Plugins relying on a specific SDK version may break when an older-SDK plugin loads first.

Use `defined( 'FS__SDK_VERSION' )` to check + handle gracefully.

### 8. Plugin info from store
Freemius pulls plugin description / changelog from the Freemius dashboard, not your readme.txt. Keep both in sync.

---

## Output

```markdown
# Freemius Integration — my-plugin

✓ SDK initialized via fs_dynamic_init
✓ is_paying() / is_plan() used for tier checks
⚠ Opt-in not configurable — using Freemius defaults (which may auto-show on first activation)
   → Add `permission_diagnostic_default: __return_false` for friendlier default
❌ Privacy policy doesn't disclose Freemius telemetry
   → Use wp_add_privacy_policy_content
⚠ SDK version not pinned — risk if another Freemius plugin ships incompatible SDK version
✓ Free features remain functional regardless of license status
```

---

## Pair with

- `/orbit-pay-edd` — alt licensing SDK
- `/orbit-gdpr` — privacy disclosure obligations

---

## Sources & Evergreen References

### Canonical docs
- [Freemius for Developers](https://freemius.com/help/) — root
- [SDK Documentation](https://freemius.com/help/documentation/wordpress-sdk/) — full reference
- [Privacy + Opt-in](https://freemius.com/help/documentation/wordpress-sdk/opting-out/) — GDPR considerations
- [Freemius vs Alternatives](https://freemius.com/blog/wp-plugin-monetization-options/) — SDK comparison

### Last reviewed
- 2026-04-29
