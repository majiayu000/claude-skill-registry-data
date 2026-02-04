---
name: i18n-helper
description: Handle WordPress internationalization. Use when adding translatable strings.
---

# i18n Helper

## Instructions

When adding translatable strings to the plugin:

1. **Use the correct text domain**: `'retrologin'`
2. **Choose the right function**:
    - `__()` - Return translated string
    - `_e()` - Echo translated string
    - `esc_html__()` - Return escaped translated string
    - `esc_html_e()` - Echo escaped translated string
    - `esc_attr__()` - Return escaped for HTML attributes
3. **Generate POT file**: `composer run make-pot`
4. **Keep strings in English (US)**

## Translation Functions

| Function                     | Output          | Use When                      |
| ---------------------------- | --------------- | ----------------------------- |
| `__($text, $domain)`         | Return          | Strings in PHP variables      |
| `_e($text, $domain)`         | Echo            | Direct output                 |
| `esc_html__($text, $domain)` | Return + escape | Displaying user content       |
| `esc_html_e($text, $domain)` | Echo + escape   | Direct output of user content |
| `esc_attr__($text, $domain)` | Return + escape | HTML attributes               |

## Example

```php
// Basic usage
__('Login Page', 'retrologin');
_e('Welcome back!', 'retrologin');

// With escaping
esc_html__('Please log in to continue', 'retrologin');
esc_attr__('Username', 'retrologin');

// In attributes
<input placeholder="<?php esc_attr_e('Enter username', 'retrologin'); ?>">
```

## Generate Translations

```bash
# Generate POT file for translations
composer run make-pot

# POT file location: inc/languages/retrologin.pot
```

## Guidelines

-   Always include text domain second parameter
-   Use escaping functions for user-generated content
-   Keep strings concise for translation
-   Avoid embedding variables in translatable strings
