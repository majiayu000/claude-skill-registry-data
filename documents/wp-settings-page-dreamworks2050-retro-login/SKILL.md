---
name: wp-settings-page
description: Create WordPress admin settings pages with Settings API.
---

# WP Settings Page

## Instructions

When creating admin settings pages for the plugin:

1. **Register setting**: Use `register_setting()` for storage
2. **Add settings section**: `add_settings_section()`
3. **Add settings fields**: `add_settings_field()`
4. **Create options page**: `add_options_page()`
5. **Sanitize input**: Use callback to clean data

## Pattern

```php
// Register setting
register_setting('retrologin_options', 'retrologin_settings');

// Add section
add_settings_section('retrologin_general', 'General Settings', 'retrologin_section_cb', 'retrologin');

// Add field
add_settings_field('retrologin_color', 'Retro Color', 'retrologin_color_cb', 'retrologin', 'retrologin_general');

// Add menu page
add_options_page('RetroLogin Settings', 'RetroLogin', 'manage_options', 'retrologin', 'retrologin_options_page');
```

## Options Page Structure

```php
function retrologin_options_page(): void {
    ?>
    <div class="wrap">
        <h1>RetroLogin Settings</h1>
        <form action="options.php" method="post">
            <?php
            settings_fields('retrologin_options');
            do_settings_sections('retrologin');
            submit_button();
            ?>
        </form>
    </div>
    <?php
}
```

## Sanitization

```php
function retrologin_sanitize($input): array {
    $sanitized = [];
    if (isset($input['color'])) {
        $sanitized['color'] = sanitize_text_field($input['color']);
    }
    return $sanitized;
}
```

## Guidelines

-   Use single option array for related settings
-   Always sanitize on save
-   Use capabilities check: `manage_options`
-   Store defaults on plugin activation
