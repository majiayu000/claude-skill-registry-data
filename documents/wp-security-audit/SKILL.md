---
name: wp-security-audit
description: Review code for WordPress security vulnerabilities.
---

# WP Security Audit

## Instructions

When reviewing or creating plugin code for security:

1. **Check input sanitization** - All user input must be cleaned
2. **Check output escaping** - All output must be escaped
3. **Verify nonce usage** - Forms need CSRF protection
4. **Check capabilities** - Admin actions need permission checks
5. **Verify ABSPATH check** - All PHP files must have it
6. **Check database queries** - Use prepared statements

## Security Checklist

-   [ ] All `$_GET`, `$_POST`, `$_COOKIE` sanitized
-   [ ] All output uses `esc_*` functions
-   [ ] Forms use nonces (`wp_nonce_field`)
-   [ ] Nonces verified before processing
-   [ ] Capability checks on admin actions (`current_user_can`)
-   [ ] `ABSPATH` check in all PHP files
-   [ ] No direct SQL without `$wpdb->prepare()`
-   [ ] No `eval()` or dynamic code execution
-   [ ] No sensitive data in URLs or logs

## Common Security Functions

### Sanitization

```php
sanitize_text_field()      // General text
sanitize_email()           // Email addresses
absint()                   // Positive integers
esc_url_raw()              // URLs
```

### Escaping

```php
esc_html()    // HTML content
esc_attr()    // HTML attributes
esc_url()     // URLs
esc_textarea() // Textarea content
```

### Nonces

```php
wp_nonce_field('action', 'nonce')           // Generate
wp_verify_nonce($_POST['nonce'], 'action')  // Verify
```

## Example Audit Flow

```php
// BAD: No sanitization
$name = $_POST['name'];

// GOOD: Sanitized
$name = sanitize_text_field($_POST['name']);

// BAD: No escaping
echo $user_input;

// GOOD: Escaped
echo esc_html($user_input);
```
