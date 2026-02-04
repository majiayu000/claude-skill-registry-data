---
name: howdy-structure
description: Create PHP classes following Howdy framework conventions. Use when creating new classes or files in the plugin.
---

# Howdy Structure Helper

## Instructions

When creating new PHP classes or files:

1. **Place in correct directory**:

    - Classes: `app/Namespace/Class.php`
    - Includes: `inc/` directory

2. **Apply namespace**:

    - Base: `Retrologin\`
    - Example: `Retrologin\Admin\Settings`

3. **Add required file header**:

    - `declare(strict_types=1);`
    - Docblock with description and `@since`

4. **Include ABSPATH check** at the top

## File Structure Pattern

```
retrologin.php          # Main plugin file (header only)
app/
  Admin/
    Settings.php        # Class: Retrologin\Admin\Settings
  Frontend/
    Login.php           # Class: Retrologin\Frontend\Login
inc/
  bootstrap/
    app.php             # Bootstrap file
```

## Class Template

```php
<?php

declare(strict_types=1);

/**
 * Short description of the class.
 *
 * Longer description if needed.
 *
 * @package Retrologin
 * @since   0.1.0
 */

namespace Retrologin\Admin;

if (! defined('ABSPATH')) {
    exit;
}

/**
 * Class description.
 *
 * @since 0.1.0
 */
class Settings {

    /**
     * Constructor.
     *
     * @since 0.1.0
     */
    public function __construct() {
        // Hooks, filters, etc.
    }

    /**
     * Method description.
     *
     * @param string $param Description.
     * @return void
     * @since 0.1.0
     */
    public function method( string $param ): void {
        // ...
    }
}
```

## Key Conventions

-   Autoloading: Composer's PSR-4 maps `Retrologin\` to `app/`
-   Don't manually `require` files - use autoloading
-   Coding standard: Syntatis (configured in phpcs.xml.dist)
-   Linter: `composer run lint`
-   Auto-fix: `composer run format`
