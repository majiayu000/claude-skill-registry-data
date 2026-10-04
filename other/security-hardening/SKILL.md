---
name: Security Hardening
description: This skill activates when users discuss WordPress security, OWASP vulnerabilities, CSP headers, XSS prevention, SQL injection, or security hardening. Provides guidance on securing WordPress themes and applications following OWASP Top 10 best practices.
---

# WordPress Security Hardening

Secure WordPress themes and applications against OWASP Top 10 vulnerabilities.

## When This Activates

- "security", "hardening", "vulnerabilities", "OWASP"
- "XSS", "SQL injection", "CSRF", "CSP headers"
- "sanitize", "escape", "nonce verification"
- User asks about WordPress security
- Discussing security best practices

---

## OWASP Top 10 for WordPress

### 1. Injection (SQL, XSS)

**SQL Injection Prevention:**

```php
// ❌ Bad: Direct SQL with user input
global $wpdb;
$user_id = $_GET['user_id'];
$results = $wpdb->get_results("SELECT * FROM users WHERE id = $user_id");

// ✅ Good: Prepared statements
global $wpdb;
$user_id = intval($_GET['user_id']); // Validate first
$results = $wpdb->get_results($wpdb->prepare(
    "SELECT * FROM {$wpdb->users} WHERE id = %d",
    $user_id
));
```

**XSS Prevention:**

```php
// Always escape output
echo esc_html($user_input);           // Plain text
echo esc_attr($user_input);           // HTML attributes
echo esc_url($user_input);            // URLs
echo esc_js($user_input);             // JavaScript
echo wp_kses_post($user_input);       // Allow some HTML (posts)
echo sanitize_text_field($user_input); // Strip tags, encode

// In templates
<h1><?php echo esc_html(get_the_title()); ?></h1>
<a href="<?php echo esc_url(get_permalink()); ?>">
    <?php echo esc_html(get_the_title()); ?>
</a>
<div data-product="<?php echo esc_attr($product_data); ?>"></div>
```

---

### 2. Broken Authentication

**Nonce Verification:**

```php
// Creating nonce
wp_nonce_field('skyyrose_save_product', 'skyyrose_nonce');

// Verifying nonce
if (!isset($_POST['skyyrose_nonce']) ||
    !wp_verify_nonce($_POST['skyyrose_nonce'], 'skyyrose_save_product')
) {
    wp_die('Security check failed');
}

// AJAX nonce
wp_localize_script('skyyrose-app', 'skyyRose', [
    'ajax_url' => admin_url('admin-ajax.php'),
    'nonce' => wp_create_nonce('skyyrose_ajax'),
]);

// In AJAX handler
function skyyrose_ajax_handler() {
    check_ajax_referer('skyyrose_ajax', 'nonce');
    // ... handle request
}
add_action('wp_ajax_skyyrose_action', 'skyyrose_ajax_handler');
```

**Capability Checks:**

```php
// Check user permissions before sensitive operations
if (!current_user_can('edit_posts')) {
    wp_die('Insufficient permissions');
}

// Custom capabilities for custom post types
if (!current_user_can('edit_product', $product_id)) {
    wp_die('You cannot edit this product');
}
```

---

### 3. Sensitive Data Exposure

**Don't Store Sensitive Data in Meta:**

```php
// ❌ Bad: Storing credit card in meta
update_post_meta($order_id, '_credit_card', $_POST['card_number']);

// ✅ Good: Never store sensitive data (let payment gateway handle it)
// Or encrypt if absolutely necessary
function skyyrose_encrypt($data) {
    $key = defined('SKYYROSE_ENCRYPTION_KEY') ? SKYYROSE_ENCRYPTION_KEY : '';
    return openssl_encrypt($data, 'AES-256-CBC', $key);
}
```

**Secure wp-config.php:**

```php
// Move wp-config.php outside web root
// Set proper file permissions: 400 or 440

// Disable file editing in admin
define('DISALLOW_FILE_EDIT', true);

// Force SSL for admin
define('FORCE_SSL_ADMIN', true);

// Change database prefix (not 'wp_')
$table_prefix = 'skyy_';

// Strong auth keys and salts (unique for each site)
define('AUTH_KEY', 'put your unique phrase here');
// ... generate at https://api.wordpress.org/secret-key/1.1/salt/
```

---

### 4. XML External Entities (XXE)

**Disable XML external entity processing:**

```php
// In functions.php
add_filter('wp_check_filetype_and_ext', function($data, $file, $filename, $mimes) {
    // Block XML uploads if not needed
    $filetype = wp_check_filetype($filename, $mimes);
    if ($filetype['ext'] === 'xml') {
        $data['ext'] = false;
        $data['type'] = false;
    }
    return $data;
}, 10, 4);
```

---

### 5. Broken Access Control

**Check User Permissions:**

```php
function skyyrose_save_product_meta($post_id) {
    // Check autosave
    if (defined('DOING_AUTOSAVE') && DOING_AUTOSAVE) return;

    // Check nonce
    if (!isset($_POST['skyyrose_nonce']) ||
        !wp_verify_nonce($_POST['skyyrose_nonce'], 'skyyrose_save_product')
    ) {
        return;
    }

    // Check permissions
    if (!current_user_can('edit_post', $post_id)) {
        return;
    }

    // Now safe to save
    $collection = sanitize_text_field($_POST['skyyrose_collection']);
    update_post_meta($post_id, '_skyyrose_collection', $collection);
}
add_action('save_post_product', 'skyyrose_save_product_meta');
```

**REST API Permissions:**

```php
register_rest_route('skyyrose/v1', '/products/(?P<id>\d+)', [
    'methods' => 'PUT',
    'callback' => 'skyyrose_update_product',
    'permission_callback' => function($request) {
        // Only logged-in users with edit_products capability
        return current_user_can('edit_products');
    },
]);
```

---

### 6. Security Misconfiguration

**Hide WordPress Version:**

```php
// Remove version from head and feeds
remove_action('wp_head', 'wp_generator');
add_filter('the_generator', '__return_empty_string');

// Remove version from scripts/styles
function skyyrose_remove_version($src) {
    return remove_query_arg('ver', $src);
}
add_filter('style_loader_src', 'skyyrose_remove_version', 9999);
add_filter('script_loader_src', 'skyyrose_remove_version', 9999);
```

**Disable Directory Browsing:**

```apache
# .htaccess
Options -Indexes

# Protect sensitive files
<FilesMatch "^(wp-config\.php|\.htaccess|php\.ini|readme\.html)">
    Order allow,deny
    Deny from all
</FilesMatch>
```

---

### 7. Cross-Site Scripting (XSS)

**Always Escape Output:**

```php
// In templates
<div class="product-card">
    <h3><?php echo esc_html($product->name); ?></h3>
    <p><?php echo esc_html($product->description); ?></p>
    <a href="<?php echo esc_url($product->url); ?>">
        View Product
    </a>
</div>

// In JavaScript
<script>
const productName = <?php echo wp_json_encode($product->name); ?>;
</script>
```

**Content Security Policy (CSP):**

```php
function skyyrose_set_csp_headers() {
    if (is_admin()) return; // Don't apply to admin

    $csp = [
        "default-src 'self'",
        "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://cdn.babylonjs.com https://stats.wp.com",
        "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://fonts-api.wp.com",
        "font-src 'self' data: https://fonts.gstatic.com https://fonts-api.wp.com",
        "img-src 'self' data: https: blob:",
        "connect-src 'self' https://stats.wp.com",
        "frame-src 'self' https://widgets.wp.com",
        "object-src 'none'",
        "base-uri 'self'",
        "form-action 'self'",
        "upgrade-insecure-requests",
    ];

    header('Content-Security-Policy: ' . implode('; ', $csp));
}
add_action('send_headers', 'skyyrose_set_csp_headers');
```

---

### 8. Insecure Deserialization

**Avoid unserialize() with User Data:**

```php
// ❌ Bad: Deserializing user input
$data = unserialize($_POST['data']);

// ✅ Good: Use JSON instead
$data = json_decode($_POST['data'], true);

// If you must use serialize, validate rigorously
$data = maybe_unserialize($trusted_data); // WordPress helper
```

---

### 9. Using Components with Known Vulnerabilities

**Keep WordPress Updated:**

```php
// Enable automatic updates
add_filter('auto_update_core', '__return_true');
add_filter('auto_update_plugin', '__return_true');
add_filter('auto_update_theme', '__return_true');

// But test updates in staging first
if (defined('WP_ENVIRONMENT_TYPE') && WP_ENVIRONMENT_TYPE !== 'production') {
    // Updates enabled in staging
}
```

**Scan for Vulnerable Plugins:**

```bash
# Use WPScan
wpscan --url https://skyyrose.co --api-token YOUR_TOKEN
```

---

### 10. Insufficient Logging & Monitoring

**Security Event Logging:**

```php
function skyyrose_log_security_event($event_type, $details) {
    $log_entry = [
        'timestamp' => current_time('mysql'),
        'event_type' => $event_type,
        'user_id' => get_current_user_id(),
        'ip' => $_SERVER['REMOTE_ADDR'],
        'details' => $details,
    ];

    // Log to custom table or file
    error_log('[SECURITY] ' . wp_json_encode($log_entry));
}

// Log failed login attempts
add_action('wp_login_failed', function($username) {
    skyyrose_log_security_event('login_failed', [
        'username' => sanitize_user($username),
    ]);
});

// Log successful admin logins
add_action('wp_login', function($user_login, $user) {
    if (user_can($user, 'manage_options')) {
        skyyrose_log_security_event('admin_login', [
            'username' => $user_login,
        ]);
    }
}, 10, 2);
```

---

## Additional Security Headers

```php
function skyyrose_security_headers() {
    // Prevent clickjacking
    header('X-Frame-Options: SAMEORIGIN');

    // Prevent MIME sniffing
    header('X-Content-Type-Options: nosniff');

    // Enable XSS filter
    header('X-XSS-Protection: 1; mode=block');

    // Referrer policy
    header('Referrer-Policy: strict-origin-when-cross-origin');

    // Permissions policy (formerly Feature-Policy)
    header('Permissions-Policy: geolocation=(), microphone=(), camera=()');
}
add_action('send_headers', 'skyyrose_security_headers');
```

---

## Input Validation & Sanitization

```php
// Comprehensive validation
function skyyrose_validate_product_input($data) {
    $validated = [];

    // Required fields
    if (empty($data['name'])) {
        return new WP_Error('missing_name', 'Product name is required');
    }
    $validated['name'] = sanitize_text_field($data['name']);

    // Email
    if (!empty($data['email'])) {
        $email = sanitize_email($data['email']);
        if (!is_email($email)) {
            return new WP_Error('invalid_email', 'Invalid email address');
        }
        $validated['email'] = $email;
    }

    // URL
    if (!empty($data['url'])) {
        $url = esc_url_raw($data['url']);
        if (!filter_var($url, FILTER_VALIDATE_URL)) {
            return new WP_Error('invalid_url', 'Invalid URL');
        }
        $validated['url'] = $url;
    }

    // Integer
    if (isset($data['quantity'])) {
        $validated['quantity'] = absint($data['quantity']);
    }

    // Float (price)
    if (isset($data['price'])) {
        $validated['price'] = floatval($data['price']);
    }

    // Enum (select from allowed values)
    $allowed_collections = ['signature', 'black_rose', 'love_hurts'];
    if (isset($data['collection'])) {
        if (!in_array($data['collection'], $allowed_collections, true)) {
            return new WP_Error('invalid_collection', 'Invalid collection');
        }
        $validated['collection'] = $data['collection'];
    }

    return $validated;
}
```

---

## File Upload Security

```php
function skyyrose_secure_file_upload($file) {
    // Check file size (5MB max)
    if ($file['size'] > 5 * 1024 * 1024) {
        return new WP_Error('file_too_large', 'File must be under 5MB');
    }

    // Allowed MIME types
    $allowed_types = ['image/jpeg', 'image/png', 'image/webp'];
    $filetype = wp_check_filetype($file['name'], $allowed_types);

    if (!in_array($filetype['type'], $allowed_types, true)) {
        return new WP_Error('invalid_file_type', 'Only JPEG, PNG, WebP allowed');
    }

    // Check actual file contents (prevent fake extensions)
    if (!getimagesize($file['tmp_name'])) {
        return new WP_Error('not_an_image', 'File is not a valid image');
    }

    // Sanitize filename
    $filename = sanitize_file_name($file['name']);
    $file['name'] = $filename;

    // Upload to specific directory
    add_filter('upload_dir', function($dirs) {
        $dirs['path'] = $dirs['basedir'] . '/skyyrose-uploads';
        $dirs['url'] = $dirs['baseurl'] . '/skyyrose-uploads';
        return $dirs;
    });

    $uploaded = wp_handle_upload($file, ['test_form' => false]);

    if (isset($uploaded['error'])) {
        return new WP_Error('upload_failed', $uploaded['error']);
    }

    return $uploaded;
}
```

---

## Database Security

```php
// Use $wpdb->prepare() for all queries
global $wpdb;

// Single value
$user_id = 123;
$wpdb->get_var($wpdb->prepare(
    "SELECT meta_value FROM {$wpdb->usermeta} WHERE user_id = %d AND meta_key = %s",
    $user_id,
    'skyyrose_preference'
));

// Multiple values
$collection_ids = [1, 2, 3];
$placeholders = implode(',', array_fill(0, count($collection_ids), '%d'));
$wpdb->get_results($wpdb->prepare(
    "SELECT * FROM {$wpdb->posts} WHERE ID IN ($placeholders)",
    ...$collection_ids
));

// LIKE queries (escape % and _)
$search = $wpdb->esc_like($_GET['search']) . '%';
$wpdb->get_results($wpdb->prepare(
    "SELECT * FROM {$wpdb->posts} WHERE post_title LIKE %s",
    $search
));
```

---

## Authentication & Authorization

```php
// Multi-factor authentication (with plugin)
// Recommend: Wordfence Login Security, Two-Factor

// Limit login attempts
function skyyrose_check_login_attempts($user, $username, $password) {
    $max_attempts = 5;
    $lockout_duration = 15 * MINUTE_IN_SECONDS;

    $transient_key = 'login_attempts_' . md5($username);
    $attempts = get_transient($transient_key);

    if ($attempts >= $max_attempts) {
        return new WP_Error(
            'too_many_attempts',
            'Too many login attempts. Try again in 15 minutes.'
        );
    }

    return $user;
}
add_filter('authenticate', 'skyyrose_check_login_attempts', 30, 3);

// Track failed attempts
add_action('wp_login_failed', function($username) {
    $transient_key = 'login_attempts_' . md5($username);
    $attempts = get_transient($transient_key) ?: 0;
    set_transient($transient_key, $attempts + 1, 15 * MINUTE_IN_SECONDS);
});
```

---

## Security Checklist for SkyyRose

- [ ] **Input validation**: All user input sanitized/validated
- [ ] **Output escaping**: All dynamic output escaped
- [ ] **SQL injection**: Use $wpdb->prepare() for all queries
- [ ] **XSS prevention**: esc_html(), esc_attr(), esc_url()
- [ ] **CSRF protection**: Nonce verification on all forms
- [ ] **Capability checks**: Verify permissions before actions
- [ ] **CSP headers**: Content Security Policy configured
- [ ] **Security headers**: X-Frame-Options, X-Content-Type-Options
- [ ] **File uploads**: Validate type, size, contents
- [ ] **Authentication**: Strong passwords, limit login attempts
- [ ] **wp-config.php**: Secure, moved outside web root
- [ ] **Updates**: WordPress, plugins, themes up to date
- [ ] **Logging**: Security events logged and monitored
- [ ] **Backups**: Regular automated backups

---

## Security Plugins Recommended

1. **Wordfence Security**: Firewall, malware scanning, 2FA
2. **Sucuri Security**: Security auditing, monitoring
3. **iThemes Security**: Hardening, brute force protection
4. **Limit Login Attempts Reloaded**: Prevent brute force

---

## When User Asks About Security

1. **Assess current state**: Run security scan (Wordfence, WPScan)
2. **Identify vulnerabilities**: Check OWASP Top 10
3. **Prioritize fixes**: Critical → High → Medium → Low
4. **Implement hardening**: Input validation, output escaping, headers
5. **Monitor**: Set up logging, alerts, regular scans

Always follow defense in depth: multiple layers of security.
