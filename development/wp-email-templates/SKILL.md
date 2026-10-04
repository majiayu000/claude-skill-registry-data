---
name: wp-email-templates
description: "Use when adding or refactoring transactional emails in a WordPress plugin — extracting inline HTML strings into reusable templates sharing a branded base shell, implementing the render_template helper (ob_start / include / ob_get_clean), passing variables safely with extract(EXTR_SKIP), sending via wp_mail(), testing with MockPHPMailer / tests_retrieve_phpmailer_instance(), applying table-based HTML layout and inline CSS for email clients, or handling wp_mail send-failure branches. Triggers: \"send an email from my plugin\", \"wp_mail not working\", \"add an email template\", \"style my plugin emails\", \"HTML email in WordPress\", \"branded email wrapper\", \"email not arriving\", \"test my wp_mail\", \"add a CTA button to the email\", \"make emails look good in Outlook\", \"transactional email template\", \"render_template helper\", \"ob_start for email\", \"extract EXTR_SKIP\", \"MockPHPMailer in tests\", \"tests_retrieve_phpmailer_instance\", \"pre_wp_mail filter to test failure\", \"inline CSS email\", \"dark mode email support\", \"table-based email layout\", \"wp_mail headers\", \"email not sending in tests\". Not for: REST API webhooks, push notifications, or transactional email in themes."
---

# Reusable HTML Email Templates (WordPress plugin)

> **Model note:** Mechanical refactoring — extract strings, create template files, wire `wp_mail()`. `haiku` handles end-to-end.

Move email bodies out of inline PHP strings into `templates/emails/`, where every message reuses one branded shell. Adding a new email = adding one content file.

## When to use

- "Move email content to templates", "branded/HTML emails", "reuse an email template".
- Any plugin building messages inline with `wp_mail()` heredocs.

**Not for:** REST API webhooks, push notifications, or Slack integrations. Transactional email in themes — this skill targets plugin-delivered mail only.

## Structure

```
templates/emails/
  base.php          shared shell: header, body slot ($content), footer
  <name>.php        per-email content (greeting, copy, CTA button)
```

- **base.php** — table-based, inline-CSS responsive shell (email clients ignore `<style>`/external CSS). Receives `$subject`, `$preheader`, `$content`, `$site_name`, `$site_url`. Echoes `$content` raw (`// phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped` — content templates escape their own values).
- **content templates** — escape every variable (`esc_html`, `esc_url`); wrap copy in `__()`/`esc_html__()` with the text domain; use `_n()` for plurals. Guard each `$var = $var ?? default;` so the file is robust if rendered standalone.

## Render helpers (in your Helpers class)

```php
public static function render_template( string $path, array $vars = [] ): string {
    if ( ! is_readable( $path ) ) return '';
    // phpcs:ignore WordPress.PHP.DontExtract.extract_extract -- controlled template vars
    extract( $vars, EXTR_SKIP );
    ob_start();
    include $path;
    return (string) ob_get_clean();
}

public static function render_email( string $template, array $vars = [] ): string {
    $dir = (string) plugin_config( 'templates' ) . 'emails/';   // your assets/templates path helper
    $vars['content']   = self::render_template( $dir . $template . '.php', $vars );
    $vars['site_name'] = $vars['site_name'] ?? get_bloginfo( 'name' );
    $vars['site_url']  = $vars['site_url'] ?? home_url( '/' );
    return self::render_template( $dir . 'base.php', $vars );   // always wrap in the shell
}
```

A missing content template yields an empty body but the shell still renders — callers always get a valid document.

## Sending

```php
$body    = Helpers::render_email( 'welcome', [ 'subject' => $subject, 'user_name' => $u->display_name, ... ] );
$headers = [ 'Content-Type: text/html; charset=UTF-8' ];   // REQUIRED for HTML
return wp_mail( $to, $subject, $body, $headers );
```

Drive any TTL/expiry copy from the same constant the code uses (e.g. a token transient TTL) so email text can't drift from behavior.

## Gotchas

- Entities in translated strings: `&copy;` double-escapes through `esc_html__` → use the literal `©`.
- Don't assign WordPress globals in templates (`$year` etc. trip `WordPress.WP.GlobalVariablesOverride`) — inline `gmdate('Y')` instead.

## Testing

WP's test suite captures `wp_mail` via MockPHPMailer:

```php
reset_phpmailer_instance();
// ... trigger the send ...
$sent = tests_retrieve_phpmailer_instance()->get_sent();
$this->assertStringContainsString( 'text/html', $sent->header );
$this->assertStringContainsString( '<!DOCTYPE html', $sent->body );   // base shell used
$this->assertStringContainsString( $expected_cta, $sent->body );
```

Force a send failure with `add_filter( 'pre_wp_mail', '__return_false' )` to test the error branch.

## References

- `references/base.php` — the full responsive HTML base shell (header/body/footer, inline CSS), copy into `templates/emails/base.php`.
- `references/content-example.php` — an example content template (greeting, CTA button, optional expiry, fallback link) to copy and adapt per email.
- `references/html-email-patterns.md` — HTML email patterns: table-based layout rules, inline CSS requirements, dark-mode support, and Outlook-specific fixes
- `references/wp-mail-api.md` — WordPress mail API reference: `wp_mail()` parameters, `phpmailer_init` hook, SMTP configuration, and deliverability checklist
