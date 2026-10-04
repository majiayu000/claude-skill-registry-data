---
name: orbit-gdpr
description: GDPR / personal-data compliance audit for a WordPress plugin — verifies that the plugin registers with `wp_privacy_personal_data_exporters` and `wp_privacy_personal_data_erasers` for any personal data it stores, declares cookies in the privacy policy template, and handles consent-mode correctly. Use when the user says "GDPR", "personal data export", "right to be forgotten", "privacy policy", "consent mode", or before any plugin release that handles user data.
---

# 🪐 orbit-gdpr — GDPR / privacy compliance

WordPress 4.9.6+ ships personal-data export/erase tools. Plugins that store personal data MUST register with them. Most plugins don't — until a user files a GDPR request and finds out.

---

## Quick start

```bash
bash ~/Claude/orbit/scripts/check-gdpr-full.sh ~/plugins/my-plugin
bash ~/Claude/orbit/scripts/check-gdpr-hooks.sh ~/plugins/my-plugin
```

Output: `reports/gdpr-<timestamp>.md`.

---

## What "personal data" means

Any of:
- Name, email, phone, address
- IP address (yes — IP is personal data under GDPR)
- User-agent + IP combo
- Login times / IPs (if stored)
- Form submissions
- Comments / replies (WP core handles these — your plugin should NOT duplicate)
- User preferences / settings linked to a user
- Browsing behaviour / analytics events

If your plugin stores ANY of the above → mandatory GDPR hooks.

---

## What this skill checks

### 1. Personal data exporter registered
```php
add_filter( 'wp_privacy_personal_data_exporters', 'my_plugin_register_exporter' );

function my_plugin_register_exporter( $exporters ) {
    $exporters['my-plugin'] = [
        'exporter_friendly_name' => __( 'My Plugin', 'my-plugin' ),
        'callback' => 'my_plugin_export_user_data',
    ];
    return $exporters;
}

function my_plugin_export_user_data( $email_address, $page = 1 ) {
    $user = get_user_by( 'email', $email_address );
    if ( ! $user ) return [ 'data' => [], 'done' => true ];

    $data = [];

    // Pull every piece of personal data your plugin stores
    $submissions = $wpdb->get_results( $wpdb->prepare(
        "SELECT * FROM {$wpdb->prefix}my_plugin_submissions WHERE user_id = %d",
        $user->ID
    ) );

    foreach ( $submissions as $sub ) {
        $data[] = [
            'group_id' => 'my_plugin_submissions',
            'group_label' => __( 'My Plugin Form Submissions', 'my-plugin' ),
            'item_id' => 'submission-' . $sub->id,
            'data' => [
                [ 'name' => __( 'Email', 'my-plugin' ),    'value' => $sub->email ],
                [ 'name' => __( 'Submitted on', 'my-plugin' ), 'value' => $sub->created_at ],
                [ 'name' => __( 'IP Address', 'my-plugin' ), 'value' => $sub->ip ],
            ],
        ];
    }

    return [ 'data' => $data, 'done' => true ];
}
```

### 2. Personal data eraser registered (right to be forgotten)
```php
add_filter( 'wp_privacy_personal_data_erasers', 'my_plugin_register_eraser' );

function my_plugin_register_eraser( $erasers ) {
    $erasers['my-plugin'] = [
        'eraser_friendly_name' => __( 'My Plugin', 'my-plugin' ),
        'callback' => 'my_plugin_erase_user_data',
    ];
    return $erasers;
}

function my_plugin_erase_user_data( $email_address, $page = 1 ) {
    global $wpdb;
    $user = get_user_by( 'email', $email_address );
    if ( ! $user ) return [
        'items_removed' => false, 'items_retained' => false,
        'messages' => [], 'done' => true,
    ];

    $removed = $wpdb->delete(
        $wpdb->prefix . 'my_plugin_submissions',
        [ 'user_id' => $user->ID ]
    );

    return [
        'items_removed' => (bool) $removed,
        'items_retained' => false,
        'messages' => [ __( 'Removed all My Plugin submissions for this user.', 'my-plugin' ) ],
        'done' => true,
    ];
}
```

### 3. Privacy policy content suggested
```php
add_action( 'admin_init', 'my_plugin_register_privacy_content' );

function my_plugin_register_privacy_content() {
    if ( ! function_exists( 'wp_add_privacy_policy_content' ) ) return;

    $content = sprintf(
        /* translators: %s: plugin name */
        __( '<h3>%s</h3><p>This plugin stores form submissions including email, IP, and user agent. Data retained for 90 days.</p>', 'my-plugin' ),
        'My Plugin'
    );

    wp_add_privacy_policy_content( 'My Plugin', wp_kses_post( wpautop( $content, false ) ) );
}
```

### 4. Cookies declared
If your plugin sets cookies, they must be declared in the privacy policy:

```php
// When setting:
setcookie( 'my_plugin_session', $token, time() + DAY_IN_SECONDS, '/' );

// Then declare via wp_add_privacy_policy_content:
$content = __( 'My Plugin sets a `my_plugin_session` cookie for 24 hours to track user preferences.', 'my-plugin' );
```

### 5. Consent-mode compliance
For analytics / tracking:
```php
// ❌ Tracks before consent
function my_plugin_track() {
    if ( is_singular() ) wp_remote_post( 'https://analytics.example.com/track', [...] );
}
add_action( 'wp_head', 'my_plugin_track' );

// ✅ Respects consent
function my_plugin_track() {
    if ( ! my_plugin_has_consent() ) return;
    // ... track ...
}

function my_plugin_has_consent() {
    // Check your consent banner state, GA4 consent mode, etc.
    return ! empty( $_COOKIE['cookie_consent_accepted'] );
}
```

---

## Audit output

```markdown
# GDPR Audit — my-plugin

## Personal data inventory
- ✓ Found: email, IP, user_agent in wp_my_plugin_submissions
- ⚠ Found: user_id mapping in wp_usermeta (needs export coverage)

## Hook registration
- ✓ wp_privacy_personal_data_exporters — registered
- ❌ wp_privacy_personal_data_erasers — NOT registered (CRITICAL)
- ✓ wp_add_privacy_policy_content — registered

## Consent mode
- ⚠ Tracking call at wp-tracker.js:18 fires regardless of consent state

## Cookies
- ✓ my_plugin_session declared in privacy policy

## Severity: HIGH (eraser missing — legal risk)

## Test plan
1. WP-Admin → Tools → Export Personal Data — verify your data appears
2. WP-Admin → Tools → Erase Personal Data — verify data is removed
3. Set consent cookie to "rejected" — verify no tracking calls fire
```

---

## Test the export/erase flow

```js
// tests/playwright/gdpr.spec.js
test('Export request includes my-plugin data', async ({ page }) => {
  await gotoAdmin(page, '/wp-admin/tools.php?page=export_personal_data');
  await page.fill('#username_or_email_for_privacy_request', 'test@example.com');
  await page.click('Send Request');
  // Approve the request via email link, then download
  // Verify the JSON includes 'my_plugin_submissions' group
});
```

---

## When this is mandatory

- **EU customers OR processing EU user data** → legally required
- **California (CCPA)** → similar but slightly less strict
- **Brazil (LGPD)**, **India (DPDP Act)** → similar requirements
- **WP.org submission** → strongly recommended, may become required

Even if not legally bound, registering the hooks is the right thing for users — it's literally one filter call.

---

## Pair with `/orbit-cve-check`

`/orbit-gdpr` covers compliance + privacy hooks.
`/orbit-cve-check` covers active threats (data leaks via exploits).
Different angles on user data protection — run both.

---

## Hard rule

If your plugin stores any personal data, **never ship without registering the export + erase hooks**. WP core gives you the API for free — using it is non-negotiable.
