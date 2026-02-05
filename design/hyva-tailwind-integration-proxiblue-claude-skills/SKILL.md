---
name: hyva-tailwind-integration
description: Comprehensive guidance on integrating Tailwind CSS and JavaScript in Hyvä Themes, including configuration merging, module registration, and build processes for Magento 2.
---

# Hyvä Theme Tailwind CSS & JS Integration Skill

## Purpose
This skill provides comprehensive guidance on integrating Tailwind CSS and JavaScript in Hyvä Themes, including configuration merging, module registration, and build processes for Magento 2.

## When to Use This Skill
- Setting up a new Hyvä theme with Tailwind CSS
- Creating Hyvä compatibility modules with custom styles
- Configuring Tailwind config merging across modules
- Understanding the Hyvä Tailwind build system
- Troubleshooting CSS compilation issues
- Implementing theme inheritance with proper Tailwind configuration

## Overview of Hyvä Tailwind Architecture

Hyvä Themes uses a sophisticated Tailwind CSS build system that:
- **Automatically merges** Tailwind configurations from multiple modules
- **Scans templates** across theme, parent themes, and modules for CSS classes
- **Supports CSS variables** via the `twProps` utility for dynamic theming
- **Enables module-specific styling** without theme modifications

### Key Components
1. **@hyva-themes/hyva-modules** - NPM package for config/CSS merging
2. **hyva-themes.json** - Registry of modules with Tailwind configs
3. **tailwind.config.js** - Theme-level Tailwind configuration
4. **tailwind-source.css** - Source CSS with @tailwind directives

## Directory Structure

```
app/design/frontend/Vendor/ThemeName/
├── web/
│   ├── css/
│   │   └── styles.css                    # Compiled output (git-ignored)
│   ├── js/
│   │   └── custom.js                     # Custom JavaScript
│   └── tailwind/
│       ├── package.json                  # NPM dependencies
│       ├── postcss.config.js             # PostCSS configuration
│       ├── tailwind.config.js            # Main Tailwind config
│       ├── tailwind-source.css           # Source CSS
│       ├── tailwind.browser-jit.css      # Browser JIT styles (optional)
│       ├── tailwind.browser-jit-config.js # Browser JIT config (optional)
│       └── components/                   # Component-specific CSS
│           ├── typography.css
│           ├── button.css
│           ├── forms.css
│           └── ...
```

## Setup Process

### 1. Install Hyvä Modules Package (Themes < 1.1.14)

Navigate to your theme's `web/tailwind` directory:

```bash
cd app/design/frontend/Vendor/ThemeName/web/tailwind
npm install @hyva-themes/hyva-modules
```

**For Hyvä 1.1.14+**: This package is included by default.

### 2. Configure tailwind.config.js

Update your theme's `tailwind.config.js` to use `mergeTailwindConfig`:

```javascript
const { twProps, mergeTailwindConfig } = require('@hyva-themes/hyva-modules');
const colors = require('tailwindcss/colors');

/** @type {import('tailwindcss').Config} */
module.exports = mergeTailwindConfig({
    content: [
        // Current theme's phtml and layout XML files
        '../../**/*.phtml',
        '../../*/layout/*.xml',
        '../../*/page_layout/override/base/*.xml',

        // Parent theme (for child themes)
        // '../../../../../../../vendor/hyva-themes/magento2-default-theme/**/*.phtml',
        // '../../../../../../../vendor/hyva-themes/magento2-default-theme/*/layout/*.xml',

        // app/code modules (if using custom modules)
        // '../../../../../../../app/code/**/*.phtml',
    ],
    theme: {
        extend: {
            fontFamily: {
                sans: ['Segoe UI', 'Helvetica Neue', 'Arial', 'sans-serif']
            },
            colors: twProps({
                primary: {
                    lighter: colors.blue['600'],
                    DEFAULT: colors.blue['700'],
                    darker: colors.blue['800']
                },
                secondary: {
                    lighter: colors.gray['100'],
                    DEFAULT: colors.gray['200'],
                    darker: colors.gray['300']
                }
            }),
            backgroundColor: twProps({
                container: {
                    lighter: '#ffffff',
                    DEFAULT: '#fafafa',
                    darker: '#f5f5f5'
                }
            }),
            textColor: ({ theme }) => ({
                ...twProps({
                    primary: {
                        lighter: colors.gray['700'],
                        DEFAULT: colors.gray['800'],
                        darker: colors.gray['900']
                    }
                }, 'text')
            }),
            minHeight: {
                'a11y': '44px',
                'screen-25': '25vh',
                'screen-50': '50vh',
                'screen-75': '75vh'
            },
            container: {
                center: true,
                padding: '1.5rem'
            }
        }
    },
    plugins: [
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography')
    ]
});
```

**Key Features:**
- `mergeTailwindConfig()` - Wraps config to enable automatic module merging
- `twProps()` - Generates CSS variables for dynamic theming
- `content` array - Specifies files to scan for Tailwind classes

### 3. Configure postcss.config.js

```javascript
const { postcssImportHyvaModules } = require('@hyva-themes/hyva-modules');

module.exports = {
    plugins: [
        postcssImportHyvaModules({
            excludeDirs: [] // Optionally exclude specific module directories
        }),
        require('postcss-import'),
        require('tailwindcss/nesting'),
        require('tailwindcss'),
        require('autoprefixer')
    ]
};
```

**Purpose:**
- `postcssImportHyvaModules` - Automatically imports CSS from registered modules
- `tailwindcss/nesting` - Enables CSS nesting support (required for JIT)
- `autoprefixer` - Adds vendor prefixes for browser compatibility

### 4. Source CSS Structure (tailwind-source.css)

```css
@import 'tailwindcss/base';
@import 'tailwindcss/components';
@import 'tailwindcss/utilities';

/* Component imports */
@import 'components/typography.css';
@import 'components/button.css';
@import 'components/forms.css';
@import 'components/cart.css';
@import 'components/product-page.css';

/* Custom utilities */
@layer utilities {
    .text-balance {
        text-wrap: balance;
    }
}
```

## Module Integration

### Creating a Compatibility Module with Tailwind Config

#### 1. Module Directory Structure

```
app/code/Vendor/ModuleName/
├── registration.php
├── module.xml
├── etc/
│   └── hyva-themes.json (optional, for non-compatibility modules)
└── view/frontend/
    ├── templates/
    │   └── custom-component.phtml
    ├── web/
    │   ├── css/
    │   │   └── custom-styles.css
    │   └── js/
    │       └── custom-script.js
    └── tailwind/
        └── tailwind.config.js
```

#### 2. Module Tailwind Config (view/frontend/tailwind/tailwind.config.js)

```javascript
module.exports = {
    content: [
        '../templates/**/*.phtml',
        '../layout/**/*.xml'
    ],
    theme: {
        extend: {
            colors: {
                'module-primary': '#3b82f6'
            }
        }
    }
};
```

**Important Notes:**
- Paths are **relative** to the `tailwind.config.js` file location
- Use `${themeDirRequire}` to reference theme's node_modules:

```javascript
const colors = require(`${themeDirRequire}/tailwindcss/colors`);

module.exports = {
    theme: {
        extend: {
            colors: {
                brand: colors.blue['600']
            }
        }
    }
};
```

#### 3. Module CSS (view/frontend/web/css/source/module.css)

```css
@layer components {
    .custom-component {
        @apply bg-module-primary text-white p-4 rounded;
    }
}
```

### Registering Modules in hyva-themes.json

The `app/etc/hyva-themes.json` file automatically regenerates when running:
- `bin/magento setup:upgrade`
- `bin/magento module:enable`
- `bin/magento module:disable`
- `bin/magento hyva:config:generate`

**Example hyva-themes.json:**

```json
{
    "extensions": [
        {
            "src": "app/code/Vendor/ModuleName"
        },
        {
            "src": "vendor/hyva-themes/magento2-some-module/src"
        }
    ]
}
```

### Manual Module Registration

For non-compatibility modules, register via event observer:

**etc/frontend/events.xml:**

```xml
<?xml version="1.0"?>
<config xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:noNamespaceSchemaLocation="urn:magento:framework:Event/etc/events.xsd">
    <event name="hyva_config_generate_before">
        <observer name="Vendor_ModuleName"
                  instance="Vendor\ModuleName\Observer\RegisterModuleForHyvaConfig"/>
    </event>
</config>
```

**Observer/RegisterModuleForHyvaConfig.php:**

```php
<?php
declare(strict_types=1);

namespace Vendor\ModuleName\Observer;

use Magento\Framework\Component\ComponentRegistrar;
use Magento\Framework\Event\Observer;
use Magento\Framework\Event\ObserverInterface;

class RegisterModuleForHyvaConfig implements ObserverInterface
{
    public function __construct(
        private ComponentRegistrar $componentRegistrar
    ) {}

    public function execute(Observer $event): void
    {
        $config = $event->getData('config');
        $extensions = $config->hasData('extensions')
            ? $config->getData('extensions')
            : [];

        $moduleName = implode('_', array_slice(explode('\\', __CLASS__), 0, 2));
        $path = $this->componentRegistrar->getPath(
            ComponentRegistrar::MODULE,
            $moduleName
        );

        $extensions[] = ['src' => substr($path, strlen(BP) + 1)];
        $config->setData('extensions', $extensions);
    }
}
```

## Build Commands

### Development Build

```bash
# From theme's web/tailwind directory
cd app/design/frontend/Vendor/ThemeName/web/tailwind
npm install
npm run build-dev
```

### Production Build

```bash
# Generate Hyvä config
ddev exec bin/magento hyva:config:generate

# Build Tailwind CSS (minified)
npm --prefix app/design/frontend/Vendor/ThemeName/web/tailwind run build-prod
```

### Watch Mode (Development)

```bash
npm --prefix app/design/frontend/Vendor/ThemeName/web/tailwind run watch
```

### With BrowserSync

```bash
PROXY_URL="https://ntotank.ddev.site" npm --prefix app/design/frontend/Uptactics/nto/web/tailwind run browser-sync
```

## Theme Inheritance & Presets

For child themes, use Tailwind's `presets` to inherit parent configuration:

```javascript
const { mergeTailwindConfig } = require('@hyva-themes/hyva-modules');
const parentTheme = require('../../../../../../../vendor/hyva-themes/magento2-default-theme/web/tailwind/tailwind.config.js');

/** @type {import('tailwindcss').Config} */
module.exports = mergeTailwindConfig({
    presets: [parentTheme], // Import parent theme config
    content: [
        '../../**/*.phtml',
        '../../*/layout/*.xml',
        // Parent theme paths
        '../../../../../../../vendor/hyva-themes/magento2-default-theme/**/*.phtml'
    ],
    theme: {
        extend: {
            // Override or extend parent theme settings
            colors: {
                'child-primary': '#ef4444'
            }
        }
    }
});
```

## CSS Variables with twProps

The `twProps` utility generates CSS variables for dynamic theming:

```javascript
const { twProps } = require('@hyva-themes/hyva-modules');

module.exports = mergeTailwindConfig({
    theme: {
        extend: {
            colors: twProps({
                primary: {
                    lighter: '#3b82f6',
                    DEFAULT: '#2563eb',
                    darker: '#1d4ed8'
                }
            })
        }
    }
});
```

**Generated CSS:**

```css
:root {
    --color-primary-lighter: #3b82f6;
    --color-primary: #2563eb;
    --color-primary-darker: #1d4ed8;
}
```

**Usage in CSS:**

```css
.btn {
    background-color: var(--color-primary);
}
```

**Usage in Tailwind classes:**

```html
<button class="bg-primary text-white">Click Me</button>
```

## Browser JIT (Just-In-Time) Compilation

For CMS content with dynamic Tailwind classes:

### tailwind.browser-jit-config.js

```javascript
const colors = require('tailwindcss/colors');

module.exports = {
    theme: {
        container: {
            center: true
        },
        extend: {
            colors: {
                'my-gray': '#888877',
                primary: {
                    lighter: colors.purple['300'],
                    DEFAULT: colors.purple['800'],
                    darker: colors.purple['900']
                }
            }
        }
    }
};
```

### Optional Configuration (etc/cms-tailwind-jit-theme-config.json)

```json
{
  "tailwindBrowserJitConfigPath": "../../../../../app/design/frontend/Vendor/ThemeName/web/tailwind/tailwind.browser-jit-config.js",
  "tailwindBrowserJitCssPath": "../../../../../app/design/frontend/Vendor/ThemeName/web/tailwind/tailwind.browser-jit.css"
}
```

### Merge Browser JIT into Main Config

Add to the **end** of `tailwind.config.js`:

```javascript
// Merge browser JIT config if it exists
if (require('fs').existsSync('./tailwind.browser-jit-config.js')) {
    function isObject(item) {
        return (item && typeof item === 'object' && !Array.isArray(item));
    }

    function mergeDeep(target, ...sources) {
        if (!sources.length) return target;
        const source = sources.shift();

        if (isObject(target) && isObject(source)) {
            for (const key in source) {
                if (isObject(source[key])) {
                    if (!target[key]) Object.assign(target, { [key]: {} });
                    mergeDeep(target[key], source[key]);
                } else {
                    Object.assign(target, { [key]: source[key] });
                }
            }
        }

        return mergeDeep(target, ...sources);
    }

    mergeDeep(module.exports, require('./tailwind.browser-jit-config.js'));
}
```

## Excluding Modules

### Exclude from Compatibility Module Registry (di.xml)

```xml
<config xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:noNamespaceSchemaLocation="urn:magento:framework:ObjectManager/etc/config.xsd">
    <type name="Hyva\CompatModuleFallback\Observer\HyvaThemeHyvaConfigGenerateBefore">
        <arguments>
            <argument name="exclusions" xsi:type="array">
                <item name="Hyva_VendorModule" xsi:type="boolean">true</item>
            </argument>
        </arguments>
    </type>
</config>
```

### Exclude from Event Observer Registration (frontend/events.xml)

```xml
<config xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:noNamespaceSchemaLocation="urn:magento:framework:Event/etc/events.xsd">
    <event name="hyva_config_generate_before">
        <observer name="ObserverName" disabled="true"/>
    </event>
</config>
```

### Exclude from CSS Merging (postcss.config.js)

```javascript
const { postcssImportHyvaModules } = require('@hyva-themes/hyva-modules');

module.exports = {
    plugins: [
        postcssImportHyvaModules({
            excludeDirs: [
                'vendor/hyva-themes/magento2-hyva-checkout/src',
                'app/code/Vendor/ExcludedModule'
            ]
        }),
        // ... other plugins
    ]
};
```

## Safelist Classes

To force include specific classes that Tailwind might not detect:

```javascript
module.exports = mergeTailwindConfig({
    safelist: [
        'mt-10',
        'md:mt-20',
        {
            pattern: /^(bg|text|border)-(primary|secondary)/,
            variants: ['hover', 'focus']
        }
    ],
    // ... rest of config
});
```

## JavaScript Loading

### Module JavaScript (requirejs-config.js)

```javascript
var config = {
    map: {
        '*': {
            'customModule': 'Vendor_ModuleName/js/custom-module'
        }
    },
    paths: {
        'customLib': 'Vendor_ModuleName/js/lib/custom-library'
    },
    shim: {
        'customLib': {
            deps: ['jquery']
        }
    }
};
```

### Alpine.js Components

```javascript
// view/frontend/web/js/alpine/custom-component.js
export default function customComponent() {
    return {
        isOpen: false,
        toggle() {
            this.isOpen = !this.isOpen;
        },
        init() {
            console.log('Component initialized');
        }
    };
}
```

**Usage in templates:**

```html
<div x-data="customComponent()">
    <button @click="toggle">Toggle</button>
    <div x-show="isOpen">Content</div>
</div>

<script>
    require(['Vendor_ModuleName/js/alpine/custom-component'], function(customComponent) {
        window.customComponent = customComponent;
    });
</script>
```

## Troubleshooting

### CSS Not Updating

```bash
# Nuclear cache clear
ddev exec rm -rf var/cache/* var/page_cache/* var/view_preprocessed/* pub/static/*
ddev exec bin/magento cache:flush
ddev exec bin/magento hyva:config:generate

# Rebuild CSS
cd app/design/frontend/Vendor/ThemeName/web/tailwind
npm run build-prod
```

### Module Config Not Merging

1. Check `app/etc/hyva-themes.json` contains your module
2. Regenerate config:
   ```bash
   ddev exec bin/magento hyva:config:generate
   ```
3. Verify module's `tailwind.config.js` path: `view/frontend/tailwind/tailwind.config.js`
4. Check `postcss.config.js` includes `postcssImportHyvaModules`

### Missing CSS Classes

1. Add paths to `content` array in `tailwind.config.js`
2. Use `safelist` for dynamically generated classes
3. Check Tailwind is scanning XML files if classes are in layout XML

### Node Module Errors in Module Config

Use `${themeDirRequire}` instead of direct `require()`:

```javascript
// ❌ Wrong
const colors = require('tailwindcss/colors');

// ✅ Correct
const colors = require(`${themeDirRequire}/tailwindcss/colors`);
```

## Best Practices

1. **Use mergeTailwindConfig()** - Always wrap theme config for module merging
2. **Use twProps() for colors** - Generates CSS variables for dynamic theming
3. **Organize CSS by components** - Keep component styles in separate files
4. **Use safelist sparingly** - Only for truly dynamic classes
5. **Regenerate config after module changes** - Run `hyva:config:generate`
6. **Use presets for child themes** - Inherit parent theme configuration
7. **Document custom utilities** - Add comments for team understanding
8. **Version lock @hyva-themes/hyva-modules** - Prevent breaking changes
9. **Test build in production mode** - Catch purging issues early
10. **Use Browser JIT for CMS content** - Enable dynamic styling in admin-managed content

## Project-Specific Implementation

For the NTOTank project (current directory structure):

**Theme Location:** `app/design/frontend/Uptactics/nto/`
**Tailwind Directory:** `app/design/frontend/Uptactics/nto/web/tailwind/`

**Build Commands:**
```bash
# Development
ddev exec composer build-tailwind

# Production
ddev exec composer build-prod

# Watch mode
ddev exec composer watch
```

**Custom Modules Integration:**
- `Uptactics_NtoTheme` - Core theme module
- `ProxiBlue_SearchDynaTable` - Search filtering with Alpine.js
- `Uptactics_ToolbarFilters` - Custom category filters

Ensure all custom modules have proper Tailwind configs at:
`app/code/Uptactics/ModuleName/view/frontend/tailwind/tailwind.config.js`

## References

- [Hyvä Docs: Tailwind Config Merging](https://docs.hyva.io/hyva-themes/compatibility-modules/tailwind-config-merging.html)
- [Hyvä Docs: Working with TailwindCSS](https://docs.hyva.io/hyva-themes/working-with-tailwindcss/)
- [Hyvä Docs: Building Your Theme](https://docs.hyva.io/hyva-themes/building-your-theme/)
- [TailwindCSS Documentation](https://tailwindcss.com/docs)
- [PostCSS Documentation](https://postcss.org/)
