---
name: hyva-module-compatibility
description: Identify and fix Magento 2 module compatibility issues with Hyvä Themes. Covers block plugin bypasses, RequireJS/Knockout replacements, ViewModels, and Alpine.js integration for modules that work in admin but fail on Hyvä frontend.
---

# Hyvä Module Compatibility Skill

## Overview
This skill helps identify and fix Magento 2 module compatibility issues with Hyvä Themes. Hyvä uses Alpine.js and TailwindCSS instead of Luma's Knockout.js and RequireJS, which often breaks modules designed for the default Luma theme.

## When to Use This Skill
- A Magento 2 module works in admin but not on Hyvä frontend
- Plugins targeting Magento blocks don't apply on frontend
- JavaScript-based features are missing or broken
- Custom rendering/UI components don't appear correctly

## Common Hyvä Compatibility Issues

### 1. **Block Plugins Don't Execute**
**Symptom:** Plugins that modify block HTML output (e.g., `after*Html()` methods) don't apply on frontend.

**Root Cause:** Hyvä often uses custom ViewModels and templates that bypass standard Magento blocks.

**Example from this project:**
```php
// ❌ This plugin doesn't work with Hyvä
class SelectPlugin {
    public function afterGetValuesHtml(Select $subject, string $result): string {
        // Modifies HTML - but Hyvä doesn't call getValuesHtml()
    }
}
```

**Solution:** Instead of plugins, use:
- Template overrides in your theme
- Custom ViewModels injected via `ViewModelRegistry`
- Alpine.js for client-side rendering

### 2. **RequireJS/Knockout Dependencies**
**Symptom:** JavaScript features don't load; console errors about missing modules.

**Root Cause:** Hyvä doesn't include RequireJS or Knockout.js by default.

**Solution:**
- Replace RequireJS modules with vanilla JavaScript or Alpine.js
- Use `<script>` tags with modern ES6+ JavaScript
- Leverage Hyvä's ViewModels for data injection

### 3. **Layout XML Blocks Not Rendering**
**Symptom:** Blocks defined in layout XML don't appear on frontend.

**Root Cause:** Hyvä templates may not include the block reference points.

**Solution:**
- Check if Hyvä has an equivalent template
- Override Hyvä templates in your theme to add missing blocks
- Use `$block->getChildHtml()` in templates

## Hyvä Compatibility Workflow

### Step 1: Identify the Issue
```bash
# Test in admin first (should work)
# Then test on frontend with Hyvä theme

# Check browser console for errors
# Check var/log/system.log for PHP errors

# Verify theme is actually Hyvä
bin/magento theme:list
```

### Step 2: Locate the Incompatible Code

**Check for these patterns:**
```php
// ❌ Block HTML modification plugins
public function afterGetHtml(...) {}
public function afterToHtml(...) {}

// ❌ RequireJS dependencies
<script type="text/x-magento-init">
require(['jquery', 'mage/...'], function($) {});

// ❌ Knockout.js data-bind
<div data-bind="scope: 'component'">
```

**Find Hyvä equivalents:**
```bash
# Search Hyvä theme templates
find vendor/hyva-themes -name "*.phtml" | xargs grep -l "pattern"

# Check if Hyvä has a compatibility module
ls app/code/Hyva/*/
```

### Step 3: Implement Hyvä-Compatible Solution

#### Pattern A: Template Override with ViewModel

**File:** `app/design/frontend/YourVendor/your-theme/Module_Name/templates/your-template.phtml`

```php
<?php
use Hyva\Theme\Model\ViewModelRegistry;
use Your\Module\ViewModel\YourViewModel;

/** @var ViewModelRegistry $viewModels */
$viewModels = $viewModels ?? \Magento\Framework\App\ObjectManager::getInstance()
    ->get(ViewModelRegistry::class);

/** @var YourViewModel $customViewModel */
$customViewModel = $viewModels->require(YourViewModel::class);

// Get data from ViewModel
$data = $customViewModel->getData();
?>

<!-- Use Alpine.js for interactivity -->
<div x-data="{
    myData: <?= $escaper->escapeHtmlAttr(json_encode($data)) ?>,
    myMethod() {
        // Alpine.js method
    }
}" x-init="myMethod()">
    <span x-text="myData.someValue"></span>
</div>
```

#### Pattern B: Alpine.js Integration

**When:** You need client-side reactivity (dropdowns, filters, dynamic updates)

```javascript
// In your template .phtml file
<script>
function initYourFeature() {
    return {
        // Data properties
        selectedValue: null,
        options: <?= /* @noEscape */ json_encode($options) ?>,

        // Initialization
        init() {
            this.$nextTick(() => {
                this.applyDefaults();
            });
        },

        // Methods
        applyDefaults() {
            // Set default values
            if (this.defaultValue) {
                this.selectedValue = this.defaultValue;
                // Update DOM
                const element = document.querySelector('#my-select');
                if (element) {
                    element.value = this.defaultValue;
                }
            }
        },

        // Event handlers
        handleChange($dispatch, value) {
            this.selectedValue = value;
            $dispatch('custom-event', { value });
        }
    }
}
</script>

<div x-data="initYourFeature()" x-init="init()">
    <select x-on:change="handleChange($dispatch, $event.target.value)">
        <template x-for="option in options">
            <option :value="option.value" x-text="option.label"></option>
        </template>
    </select>
</div>
```

#### Pattern C: ViewModel for Data Preparation

**File:** `app/code/Your/Module/ViewModel/YourViewModel.php`

```php
<?php
declare(strict_types=1);

namespace Your\Module\ViewModel;

use Magento\Framework\View\Element\Block\ArgumentInterface;

class YourViewModel implements ArgumentInterface
{
    private $yourModel;

    public function __construct(
        \Your\Module\Model\YourModel $yourModel
    ) {
        $this->yourModel = $yourModel;
    }

    /**
     * Get data for Alpine.js/frontend
     *
     * @param int $entityId
     * @return array
     */
    public function getData(int $entityId): array
    {
        return [
            'key' => 'value',
            'items' => $this->yourModel->getItems($entityId),
        ];
    }

    /**
     * Get data as JSON for Alpine.js
     *
     * @param int $entityId
     * @return string
     */
    public function getDataJson(int $entityId): string
    {
        return json_encode($this->getData($entityId), JSON_THROW_ON_ERROR);
    }
}
```

**Usage in template:**
```php
<?php
/** @var Your\Module\ViewModel\YourViewModel $viewModel */
$viewModel = $viewModels->require(\Your\Module\ViewModel\YourViewModel::class);
?>

<div x-data='<?= $viewModel->getDataJson($product->getId()) ?>'>
    <!-- Your Alpine.js component -->
</div>
```

### Step 4: Testing

```bash
# Clear caches
ddev exec bin/magento cache:flush

# Check for errors in console
# Browser DevTools → Console

# Check for errors in logs
tail -f var/log/system.log var/log/exception.log

# Test all option types if applicable
# - Select dropdowns
# - Radio buttons
# - Checkboxes
# - Multi-select
```

## Real-World Example: Custom Option Default Values

### Original (Luma-Compatible) Approach
```php
// Plugin: Plugin/Catalog/Block/Product/View/Options/Type/SelectPlugin.php
class SelectPlugin
{
    public function afterGetValuesHtml(Select $subject, string $result): string
    {
        // Modify HTML to add selected="selected" attribute
        // ❌ Doesn't work with Hyvä - method never called
    }
}
```

### Hyvä-Compatible Approach

**1. Created ViewModel:**
```php
// ViewModel/CustomOptionImage.php
class CustomOptionImage implements ArgumentInterface
{
    public function getDefaultValuesForProduct(int $productId): array
    {
        return $this->defaultValueResource->getDefaultValuesForProduct($productId);
    }
}
```

**2. Modified Template:**
```php
// app/design/frontend/Uptactics/nto/Magento_Catalog/templates/product/view/options/options.phtml

use Uptactics\CustomOptionImage\ViewModel\CustomOptionImage;

/** @var CustomOptionImage $customOptionImageViewModel */
$customOptionImageViewModel = $viewModels->require(CustomOptionImage::class);

$defaultValues = $customOptionImageViewModel->getDefaultValuesForProduct((int)$product->getId());
```

**3. Added Alpine.js Logic:**
```javascript
function initOptions() {
    return {
        defaultValues: <?= /* @noEscape */ json_encode($defaultValues) ?>,

        applyDefaultValues($dispatch) {
            Object.entries(this.defaultValues).forEach(([optionId, optionTypeId]) => {
                const selectElement = document.querySelector(`select[name="options[${optionId}]"]`);
                if (selectElement) {
                    selectElement.value = optionTypeId;
                    this.updateCustomOptionValue($dispatch, optionId, selectElement);
                }
            });
        }
    }
}
```

**4. Called on Initialization:**
```html
<div x-data="initOptions()"
     x-init="$nextTick(() => { applyDefaultValues($dispatch); })">
```

## Hyvä Theme Patterns Reference

### Alpine.js Directives
```html
<!-- Data binding -->
<div x-data="{ count: 0 }"></div>

<!-- Conditionals -->
<div x-show="isVisible"></div>
<div x-if="shouldRender"></div>

<!-- Loops -->
<template x-for="item in items" :key="item.id">
    <div x-text="item.name"></div>
</template>

<!-- Events -->
<button x-on:click="handleClick()">Click</button>
<select x-on:change="handleChange($event)">

<!-- References -->
<div x-ref="myElement"></div>
<!-- Access via this.$refs.myElement -->

<!-- Initialization -->
<div x-init="init()"></div>

<!-- Lifecycle -->
<div x-init="$nextTick(() => { /* code */ })"></div>
```

### ViewModelRegistry Usage
```php
// In templates
/** @var ViewModelRegistry $viewModels */

// Require a ViewModel
$myViewModel = $viewModels->require(MyViewModel::class);

// Check if ViewModel exists
if ($viewModels->has(MyViewModel::class)) {
    $myViewModel = $viewModels->require(MyViewModel::class);
}
```

### Data Passing Patterns
```php
// Simple data (use escapeHtmlAttr for attributes)
<div x-data='{ value: "<?= $escaper->escapeHtmlAttr($value) ?>" }'></div>

// Complex data (use json_encode)
<div x-data='<?= $escaper->escapeHtmlAttr(json_encode($data)) ?>'></div>

// Don't escape JSON in JavaScript context
<script>
const data = <?= /* @noEscape */ json_encode($data) ?>;
</script>
```

## Common Gotchas

### 1. **ViewModels Must Implement ArgumentInterface**
```php
// ✅ Correct
class MyViewModel implements ArgumentInterface { }

// ❌ Wrong - won't work
class MyViewModel { }
```

### 2. **JSON Encoding for Alpine.js**
```php
// ✅ Correct - no escaping in JavaScript context
defaultValues: <?= /* @noEscape */ json_encode($defaults) ?>,

// ❌ Wrong - breaks JSON
defaultValues: <?= $escaper->escapeHtml(json_encode($defaults)) ?>,
```

### 3. **Alpine.js Method Context**
```javascript
// ✅ Correct - use arrow function to preserve 'this'
x-init="$nextTick(() => { this.myMethod() })"

// ❌ Wrong - 'this' refers to wrong context
x-init="$nextTick(function() { this.myMethod() })"
```

### 4. **Template Override Location**
```
app/design/frontend/
  └── YourVendor/
      └── your-theme/
          └── Magento_Catalog/          ← Module name
              └── templates/
                  └── product/
                      └── view/
                          └── options/
                              └── options.phtml
```

## Checklist for Hyvä Compatibility

- [ ] Module works in admin (sanity check)
- [ ] Identified incompatible code (plugins, RequireJS, Knockout)
- [ ] Found Hyvä equivalent templates
- [ ] Created ViewModel for data preparation (if needed)
- [ ] Created template override with Alpine.js
- [ ] Tested on frontend with Hyvä theme
- [ ] Tested all variations (dropdowns, radios, checkboxes)
- [ ] Checked browser console for errors
- [ ] Checked var/log for PHP errors
- [ ] Performance tested (no N+1 queries in ViewModel)

## Resources

### Hyvä Documentation
- Official docs: https://docs.hyva.io
- Alpine.js docs: https://alpinejs.dev
- Hyvä compatibility modules: https://gitlab.hyva.io/hyva-themes/magento2-hyva-checkout

### Hyvä Theme Locations
- Base theme: `vendor/hyva-themes/magento2-default-theme/`
- Theme module: `vendor/hyva-themes/magento2-theme-module/`
- Your theme: `app/design/frontend/YourVendor/your-theme/`

### Common Hyvä ViewModels
- `Hyva\Theme\ViewModel\CustomOption` - Custom options rendering
- `Hyva\Theme\ViewModel\ProductPage` - Product page utilities
- `Hyva\Theme\ViewModel\ProductPrice` - Price formatting
- `Hyva\Theme\ViewModel\SvgIcons` - Icon rendering

## Tips

1. **Start with Hyvä's templates** - Always check if Hyvä has a template for what you're modifying
2. **Use ViewModels for logic** - Keep templates clean, put logic in ViewModels
3. **Leverage Alpine.js** - Don't fight it, use it for reactivity
4. **Test thoroughly** - Hyvä caching can mask issues
5. **Check Hyvä's compatibility module list** - Someone may have already solved your problem

## Example Commands

```bash
# Find Hyvä template
find vendor/hyva-themes -name "select.phtml"

# Check if ViewModel exists
grep -r "class CustomOption" vendor/hyva-themes

# Clear all caches
ddev exec bin/magento cache:flush

# Check for Alpine.js errors in browser
# Open DevTools → Console → Filter for "Alpine"
```
