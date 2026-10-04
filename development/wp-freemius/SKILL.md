---
name: wp-freemius
description: "Use when integrating Freemius SDK into a WordPress plugin for monetisation — SDK bootstrap with fs_dynamic_init, feature gating with can_use_premium_code() / is__premium_only() / is_plan() / is_trial() / is_paying(), license management, free/pro dual-zip build using __premium_only__ file suffix, generating upgrade URLs with get_upgrade_url(), opt-in analytics dialog, multisite licensing, affiliate program, or debugging Freemius dashboard (Plans, Pricing, Licenses, Updates). Triggers: \"add Freemius to my plugin\", \"gate this feature behind pro\", \"show the pricing page\", \"check if user has a license\", \"Freemius not initialising\", \"can_use_premium_code()\", \"is_plan()\", \"is_trial()\", \"is_paying()\", \"fs_dynamic_init\", \"my_plugin_fs()\", \"__premium_only__ file\", \"set up free and pro versions\", \"Freemius opt-in dialog\", \"trial period setup\", \"license key validation\", \"monetise my plugin\", \"get_upgrade_url()\", \"Freemius affiliate\", \"is_org_compliant\", \"Freemius SDK error\", \"free and premium zip\", \"Freemius multisite\", \"Freemius GlotPress translations\". Not for: WooCommerce payments — use `wp-woocommerce`; WP.org trialware compliance — use `wp-org-submission`."
---

# Freemius SDK Integration

> **Model note:** SDK bootstrap and basic feature-gating are pattern-matching (`haiku`). Trialware compliance audit and pricing-plan architecture decisions require careful judgment — use `sonnet` for those.

Integrate Freemius into a WordPress plugin for commercial distribution: SDK bootstrap, free/pro feature gating, license management, trials, pricing page, and the Freemius dashboard. Freemius handles payments, license keys, update delivery, and analytics.

## When to use

- "Add Freemius to my plugin", "set up free/pro version", "implement license management".
- "Gate premium features behind a license", "add a trial period".
- "Create a pricing page", "set up a Freemius affiliate program".
- "Debug Freemius SDK not loading", "fix opt-in dialog not showing".
- "Configure Freemius for multisite licensing".

**Not for:** General WooCommerce payment flows — use `wp-woocommerce`. WP.org trialware compliance (Freemius-powered upsells must follow WP.org Guideline 5 — use `wp-org-submission`, which contains `references/trialware-compliance.md`).

## Method

### 1. Create a Freemius account and app

1. Sign up at `https://freemius.com`
2. Create a new **Plugin** product in the Freemius dashboard
3. Note down: **Plugin ID**, **Public Key**, **Secret Key**
4. Configure pricing plans (Free, Pro, etc.) in the dashboard

### 2. Install the SDK

**Via Composer (recommended):**
```bash
composer require freemius/wordpress-sdk
```

**Manual:** Download from `https://github.com/Freemius/wordpress-sdk` and place in `vendor/freemius/`.

### 3. Bootstrap the SDK

Create `includes/freemius.php` (the Freemius singleton init file):

```php
<?php
if ( ! function_exists( 'my_plugin_fs' ) ) {
    function my_plugin_fs() {
        global $my_plugin_fs;

        if ( ! isset( $my_plugin_fs ) ) {
            // Include the Freemius SDK
            require_once plugin_dir_path( __FILE__ ) . '../vendor/freemius/wordpress-sdk/start.php';

            $my_plugin_fs = fs_dynamic_init( [
                'id'             => '12345',                            // Plugin ID from dashboard
                'slug'           => 'my-plugin',                       // WP.org slug
                'type'           => 'plugin',
                'public_key'     => 'pk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx', // Public key
                'is_premium'     => false,                              // true if this IS the premium build
                'has_premium_version' => true,                          // true if premium version exists
                'has_addons'     => false,
                'has_paid_plans' => true,
                'trial'          => [
                    'days'               => 14,
                    'is_require_payment' => false,                      // true = credit card required
                ],
                'menu'           => [
                    'slug'    => 'my-plugin',
                    'contact' => false,
                    'support' => false,
                ],
            ] );
        }

        return $my_plugin_fs;
    }

    // Init Freemius
    my_plugin_fs();

    // Hook Freemius after initial plugin setup
    do_action( 'my_plugin_fs_loaded' );
}
```

**Load from main plugin file:**
```php
// At the top of my-plugin.php, before any premium-gated code
require_once plugin_dir_path( __FILE__ ) . 'includes/freemius.php';
```

### 4. Feature gating

Gate premium features consistently throughout the codebase:

```php
// Check if user has an active paid plan (or trial)
if ( my_plugin_fs()->can_use_premium_code() ) {
    // Show/run premium feature
    require_once plugin_dir_path( __FILE__ ) . 'includes/class-premium-feature.php';
}

// Check if the premium code file is loaded (for the __premium_only__ pattern)
if ( my_plugin_fs()->is__premium_only() ) {
    // Always true when premium file is present
}

// Specific plan check
if ( my_plugin_fs()->is_plan( 'professional', true ) ) {
    // $true = or_greater: matches 'professional' and any higher plan
}

// Trial check
if ( my_plugin_fs()->is_trial() ) {
    echo 'Trial active: ' . my_plugin_fs()->get_trial_plan()->title;
}

// Free user upsell prompt
if ( ! my_plugin_fs()->is_paying() ) {
    // Show upgrade CTA
    $upgrade_url = my_plugin_fs()->get_upgrade_url();
}
```

**`__premium_only__` file pattern** — Freemius strips these files from the free build:
```
my-plugin/
├── includes/
│   ├── class-core.php              # Free + premium
│   └── premium/                    # Only in premium zip
│       └── class-advanced.php__premium_only__
```

### 5. Pricing page

Freemius generates a hosted pricing page. Embed in the plugin's admin:

```php
add_action( 'my_plugin_fs_loaded', function() {
    my_plugin_fs()->add_submenu_link_item(
        __( 'Upgrade', 'my-plugin' ),
        my_plugin_fs()->get_upgrade_url(),
        'upgrade',
        'manage_options',
        51,
        'dashicons-star-filled',
        true  // is_external: opens pricing in new tab
    );
} );

// Or embed the pricing page directly inside WP admin
function my_plugin_pricing_page() {
    echo my_plugin_fs()->get_pricing_js_tag( true );
}
```

### 6. Opt-in analytics

Freemius prompts users to opt into anonymous data collection on activation. Customise the dialog:

```php
$my_plugin_fs = fs_dynamic_init( [
    // ...
    'opt_in' => [
        'type'        => 'dialog',     // 'dialog', 'inline', or 'none'
        'is_enabled'  => true,
        'anonymous_mode_enabled' => true, // allow "skip" without opting in
    ],
    'is_org_compliant' => true,  // WP.org: must allow "skip"
] );

// Skip opt-in programmatically (for white-label / privacy-first)
add_action( 'my_plugin_fs_loaded', function() {
    my_plugin_fs()->skip_connection();
} );
```

### 7. Multisite licensing

Configure in `fs_dynamic_init()`:

```php
'is_premium'               => false,
'has_premium_version'      => true,
'license_key_grace_period' => 7,     // days after expiry before locking
'bundle_id'                => null,  // set if part of a bundle
'network_key_type'         => 'per-site',  // 'per-site', 'per-domain', 'unlimited'
```

Options:
- `per-site` — each subsite needs its own license activation
- `per-domain` — one license covers all subsites on the same domain
- `unlimited` — one license covers all

### 8. Freemius dashboard integration

**Key dashboard pages to configure:**
- **Plans** — name, price, features per plan, billing cycle (monthly/annual)
- **Pricing** — set currency, pricing page URL
- **Affiliates** — enable affiliate program, commission rate
- **Licenses** — activation limits per license key
- **Updates** — premium zip is auto-served via Freemius CDN on license activation

**SDK update delivery** — authenticated users receive updates via the Freemius API (not WP.org). The SDK hooks into WP's update mechanism automatically:
```php
// No extra code needed — Freemius handles wp_update_plugins transparently
```

### 9. Common SDK issues

**Opt-in dialog not showing:**
- Check `'opt_in' => [ 'type' => 'dialog' ]` in init config
- Verify user has `manage_options` capability
- Clear `fs_accounts` option: `delete_option( 'fs_accounts' )`

**"Invalid API Secret Key" error:**
- Never expose secret key in client-side JS or public code
- Rotate key in Freemius dashboard if exposed

**Premium features visible without license:**
- Ensure `can_use_premium_code()` wraps ALL premium code paths
- Check that the free zip doesn't include `__premium_only__` files

**SDK conflicts with other Freemius plugins:**
- Freemius uses a global `$fs_active_plugins` object. Conflicts resolved by SDK auto-loader — ensure only one copy of the SDK is loaded (use `if ( ! function_exists( 'fs_dynamic_init' ) )`).

## Notes

- Freemius `is_org_compliant` must be `true` for WP.org–hosted plugins. Without it, the opt-in dialog blocks deactivation — a violation of WP.org guidelines.
- The free version (on WP.org) and premium version (via Freemius) are separate zips. Build both from the same codebase using the `__premium_only__` suffix.
- Never gate plugin activation behind a license key (Guideline 5 / trialware). Freemius `can_use_premium_code()` returns `false` but the plugin must remain fully functional in free mode.
- Secret key must never be committed to git. Store in a CI secret or server env var; inject at build time.
- For WooCommerce extensions sold on WooCommerce.com, consider WooCommerce's own licensing API instead of Freemius.

## References

- `references/feature-gating.md` — Freemius feature gating patterns: `can_use_premium_code()`, `is_paying()`, plan-level checks, and free-tier fallback patterns
- `references/freemius-config.md` — `fs_dynamic_init()` full parameter reference: all config keys, common configurations, and multi-plugin setup
- `references/pricing-page.md` — Freemius pricing page URLs, checkout flow, upgrade redirect patterns, and dashboard link generation
