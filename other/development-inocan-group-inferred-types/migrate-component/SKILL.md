---
name: migrate-component
description: Migrate WordPress components from v1 (page-parts/) or v2 (layouts/) to v3 (vendi-theme-parts/components/) structure. Use when migrating components, moving layouts to v3, or converting component files.
---

# Component Migration Skill: v1/v2 to v3

You are helping migrate WordPress theme components to the v3 structure (`vendi-theme-parts/components/`). There are two migration paths:

- **v2 → v3**: ACF Flexible Layout components from `layouts/`
- **v1 → v3**: Utility/site components from `page-parts/site/` or `page-parts/page/`

## Your Role

Guide the user through migrating WordPress theme components one at a time. Each component migration includes:
1. Moving files with git mv
2. Creating a component class
3. Refactoring the main template
4. Migrating sub-layouts (if applicable)
5. Creating documentation

The user will handle `git add` and `git commit` commands - you should NOT run these.

## Cleanup After Migration

After successfully migrating a component, clean up the old v2 folders:

1. **Check for leftover files**: Look for any files in `layouts/[component_name]/` that weren't migrated
2. **Handle dead/unused files**:
   - If you find old sub-layouts or files that aren't referenced in the current code, move them to `_LEGACY/`
   - Only create the `_LEGACY/` folder if there are actually dead files to preserve
   - Example: `git mv layouts/[component_name]/layouts/old_file.php vendi-theme-parts/components/[component_name]/_LEGACY/old_file.php`
3. **Remove empty directories**: After all files are moved, remove the empty v2 directories
   - Use `rmdir` to safely remove only empty directories
   - Example: `rmdir layouts/[component_name]/layouts && rmdir layouts/[component_name]`

This ensures the codebase stays clean and old unused code is preserved in _LEGACY folders if needed.

## Reference Components

### v2 Components (Content/Layout):
- **Simple**: `basic_copy_block`, `form`
- **With custom root setup**: `accordion`, `content_callout_block`
- **With sub-layouts**: `accordion`, `media_block`, `events`, `carousel_resources`
- **Without region/wrap pattern**: `media_block`
- **Using VendiComponent**: `ad_row`

### v1 Components (Utility/Site):
- **Utility component**: `ad-slot`

---

# v2 to v3 Migration (Content Components)

## File Structure Transformation

### v2 Structure (layouts/)
```
layouts/[component_name]/
├── component.php
├── render.css
├── admin.css (optional, kept as-is)
└── thumbnail.png
```

### v3 Structure (vendi-theme-parts/components/)
```
vendi-theme-parts/components/[component_name]/
├── [component_name].php          (was component.php)
├── [component_name].class.php    (new)
├── [component_name].css          (was render.css)
├── [component_name].docs.yaml    (new)
├── [component_name].thumbnail.png (was thumbnail.png)
├── admin.css                      (kept as-is, not used in v3)
└── docs/
    ├── overview.md
    └── accessibility.md
```

## Migration Steps

### Step 1: Examine the v2 Component

First, explore the existing component:
```bash
find layouts/[component_name] -type f
```

Read the main files:
- `layouts/[component_name]/component.php` (or `[component_name].php`)
- `layouts/[component_name]/render.css`
- Any sub-layout files in `layouts/[component_name]/layouts/`

### Step 2: Move Files with git mv

Create the v3 directory and move files:
```bash
mkdir -p vendi-theme-parts/components/[component_name]
git mv layouts/[component_name]/component.php vendi-theme-parts/components/[component_name]/[component_name].php
git mv layouts/[component_name]/render.css vendi-theme-parts/components/[component_name]/[component_name].css
git mv layouts/[component_name]/thumbnail.png vendi-theme-parts/components/[component_name]/[component_name].thumbnail.png
```

If `admin.css` exists:
```bash
git mv layouts/[component_name]/admin.css vendi-theme-parts/components/[component_name]/admin.css
```

### Step 3: Create Component Class

Create `[component_name].class.php` in the component directory.

**Component Class Hierarchy:**
- `BaseComponent` - Full component with auto-generated wrappers (`<section>`, `<div class="region">`, `<div class="content-wrap">`)
- `VendiComponent` - Simplified version with only root tag, no extra HTML wrappers

**Conventions:**
- Top-level components typically extend `BaseComponent`
- Sub-layouts commonly extend `VendiComponent`
- Choice depends on needed HTML structure, not strict rules

**Purpose**: Enable automatic asset loading (CSS/JS only loaded when component is used) and provide helper methods for cleaner templates.

**Minimal Class Template:**
```php
<?php

namespace Vendi\Theme\Component;

use Vendi\Theme\BaseComponent;

class [component_name] extends BaseComponent
{
    public function __construct()
    {
        parent::__construct('[css-class-name]');
    }

    protected function initComponent(): void
    {
        parent::initComponent();

        // Add dynamic classes or attributes to root element
        // Example: $this->addRootClass('variant-' . get_sub_field('variant'));
        // Example: $this->addRootAttribute('data-role', 'carousel');
    }

    // Override wrapper class names if v2 used different names
    protected function getContentWrapClassName(): string
    {
        return 'wrap';  // Default is 'content-wrap'
    }

    protected function getRegionWrapClassName(): string
    {
        return 'region';  // Default is 'region' (rarely needs override)
    }
}
```

**With Helper Methods (for complex templates):**
```php
<?php

namespace Vendi\Theme\Component;

use Vendi\Theme\BaseComponent;

class [component_name] extends BaseComponent
{
    public function __construct()
    {
        parent::__construct('[css-class-name]');
    }

    protected function abortRender(): bool
    {
        if (!$this->getRequiredField()) {
            return true;
        }
        return parent::abortRender();
    }

    public function getRequiredField(): ?array
    {
        $field = $this->getSubField('field_name');
        if (!is_array($field)) {
            return null;
        }
        return $field;
    }

    // Add getter methods to simplify template
    public function getHeadline(): ?string
    {
        return $this->getSubField('headline');
    }
}
```

**Important Notes:**
- Add helper methods ONLY when templates have complex logic
- Don't create simple pass-through methods
- Keep templates simple and readable

### Step 4: Refactor Main PHP Template

**Understanding Auto-Generated Wrappers:**

v3 automatically wraps content with:
```html
<section class="[component-class]">
  <div class="region">
    <div class="content-wrap">
      <!-- your content -->
```

**Remove these wrappers** from the template - they're handled by `renderComponentWrapperStart()`.

**Standard v2 to v3 Conversion:**

**Before (v2):**
```php
<section class="section-[name] <?php esc_attr_e('dynamic-class-'.get_sub_field('field')); ?>">
    <div class="region">
        <div class="wrap">
            <!-- content -->
        </div>
    </div>
</section>
```

**After (v3):**
```php
<?php

use Vendi\Theme\Component\[component_name];
use Vendi\Theme\ComponentUtility;

/** @var [component_name] $component */
$component = ComponentUtility::get_new_component_instance([component_name]::class);

if (!$component->renderComponentWrapperStart()) {
    return;
}

?>
    <!-- content only (all wrappers removed) -->
<?php

$component->renderComponentWrapperEnd();
```

**Important Cases:**

1. **If v2 used `<div class="wrap">` instead of `<div class="content-wrap">`:**
   Override `getContentWrapClassName()` in the class to return `'wrap'` to preserve existing CSS.

2. **If component doesn't follow region/wrap pattern:**
   Some components have custom structures like `<section><div class="custom-class">...</div></section>`.
   In these cases, ONLY remove the outer `<section>` tag. Keep all other markup as-is.

   Example:
   ```php
   // v2: <section class="media-block-container"><div class='narrow-left-aligned'>...</div></section>
   // v3: Only remove <section>, keep <div class='narrow-left-aligned'>...</div>
   ```

### Step 5: Handle Sub-Layouts (if applicable)

If the component has sub-layouts in `layouts/[component_name]/layouts/`:

**Move Sub-Layout Files:**
```bash
# For each sub-layout, create its own directory
mkdir -p vendi-theme-parts/components/[component_name]/[field_name]/[layout_name]
git mv layouts/[component_name]/layouts/[layout].php vendi-theme-parts/components/[component_name]/[field_name]/[layout_name]/[layout_name].php
```

**Create Loader File:**

Create `[field_name]/[field_name].php`:
```php
<?php

while (have_rows("[field_name]")) {
    the_row();
    $layout = get_row_layout();

    if (!in_array($layout, ['layout1', 'layout2'], true)) {
        continue;
    }

    vendi_load_component_v3(['component_name', 'field_name', $layout]);
}
```

**Update Sub-Layout Files:**

Critical: The global variable for state has been renamed in v3.

```php
// v2 (OLD - don't use)
global $vendi_layout_component_object_state;
$data = $vendi_layout_component_object_state['key'] ?? null;

// v3 (NEW - use this)
global $vendi_component_object_state;
$data = $vendi_component_object_state['key'] ?? null;
```

When sub-layouts need to pass state to other sub-layouts:
```php
vendi_load_component_v3(['component_name', 'field_name', 'layout'], ['key' => $value]);
```

Note: There is NO `vendi_load_component_v3_with_state` function. State is passed as the second parameter to `vendi_load_component_v3`.

**Sub-Layout Classes (Optional):**

Sub-layouts can have their own class files for complex logic. They commonly extend `VendiComponent`:

```php
<?php

namespace Vendi\Theme\Component;

use Vendi\Theme\VendiComponent;

class [sub_layout_name] extends VendiComponent
{
    public function __construct()
    {
        parent::__construct('[css-class-name]');
    }

    public function getEvents(): array
    {
        return tribe_get_events(['posts_per_page' => 4, 'start_date' => 'now']);
    }

    protected function abortRender(): bool
    {
        if (!$this->getEvents()) {
            return true;
        }
        return parent::abortRender();
    }
}
```

Reference `events/events/recent_events` for a complete example.

### Step 6: Create Documentation

Create documentation structure:
```bash
mkdir -p vendi-theme-parts/components/[component_name]/docs
```

**Create `[component_name].docs.yaml`:**
```yaml
component-name: [Human Readable Name]
role: component
example-prefix: [component-name]
parent-field: content_components
pages:
    - Overview
    - Accessibility
```

**Create `docs/overview.md`:**
Describe:
- Component purpose and functionality
- When to use this component
- When to choose a different component
- Available component options and fields
- Visual elements and features
- Any special behaviors

Infer content from the component template, class, and CSS.

**Create `docs/accessibility.md`:**
Document accessibility considerations:
- Heading hierarchy
- Color and contrast requirements
- Semantic HTML structure
- Image alt text requirements
- Interactive element accessibility
- Keyboard navigation
- Screen reader announcements
- Focus management
- Motion and animation considerations

Reference `basic_copy_block`, `content_callout_block`, `media_block`, or `carousel_resources` for examples.

## Code Style Guidelines

### Template Structure

Templates follow a three-part structure:

```php
<?php
// === TOP: Setup ===
use Vendi\Theme\Component\example;
use Vendi\Theme\ComponentUtility;

/** @var example $component */
$component = ComponentUtility::get_new_component_instance(example::class);

if (!$component->renderComponentWrapperStart()) {
    return;
}

// Pre-calculate any needed variables
$items = $component->getItems();

?>
    <!-- === MIDDLE: Template with alternative syntax === -->
    <?php if ($condition): ?>
        <div class="example">Content</div>
    <?php endif; ?>

    <?php foreach ($items as $item): ?>
        <p><?php echo $item; ?></p>
    <?php endforeach; ?>
<?php
// === BOTTOM: Cleanup ===
$component->renderComponentWrapperEnd();
```

### Alternative PHP Syntax

**ALWAYS use alternative PHP syntax in the middle (template) section:**

✅ **Correct:**
```php
<?php if ($condition): ?>
    <div>Content</div>
<?php endif; ?>

<?php foreach ($items as $item): ?>
    <p><?php echo $item; ?></p>
<?php endforeach; ?>

<?php while (have_rows('field')): ?>
    <?php the_row(); ?>
<?php endwhile; ?>
```

❌ **Incorrect (don't use curly braces in template section):**
```php
<?php if ($condition) { ?>
    <div>Content</div>
<?php } ?>

<?php foreach ($items as $item) { ?>
    <p><?php echo $item; ?></p>
<?php } ?>
```

### HTML Attributes

Always use **double quotes** for HTML attributes:

✅ `<div class="example" data-role="carousel">`
❌ `<div class='example' data-role='carousel'>`

### SVG Loading

Use the `vendi_get_svg()` helper function:

✅ `<?php vendi_get_svg('/svgs/icon.svg'); ?>`
❌ `<?php echo file_get_contents(VENDI_CUSTOM_THEME_PATH . '/svgs/icon.svg'); ?>`

### Variable Usage

Echo variables directly - don't create intermediate variables:

✅ `<?php echo vendi_fly_get_attachment_picture($id, 'size'); ?>`
❌ `<?php $image = vendi_fly_get_attachment_picture($id, 'size'); echo $image; ?>`

### Class Methods

**Avoid rendering from class methods.** Classes should not output to the HTTP stream.

Use getter methods that return data, then render in templates:

✅ **Correct:**
```php
// Class
public function getItems(): array
{
    return ['item1', 'item2'];
}

// Template
<?php foreach ($component->getItems() as $item): ?>
    <p><?php echo $item; ?></p>
<?php endforeach; ?>
```

❌ **Incorrect:**
```php
// Class - DON'T DO THIS
public function renderItems(): void
{
    foreach ($this->getItems() as $item) {
        echo "<p>{$item}</p>";
    }
}
```

Exception: Very rare cases where rendering from class is absolutely necessary.

## Key Principles

1. **One file per commit** - User handles git add/commit, NOT you
2. **Preserve template logic** - Don't refactor working code unless necessary
3. **Dynamic classes** go in `initComponent()` using `addRootClass()` or `addRootAttribute()`
4. **Admin.css** is kept but not used in v3
5. **Helper methods** only for complex template needs, not simple pass-throughs
6. **Alternative PHP syntax** in template sections (if:/endif, foreach:/endforeach)
7. **Double quotes** for all HTML attributes
8. **No rendering** from class methods - return data, render in templates

## Common Patterns

### Loading Function Calls

**v2 to v3 conversions:**

| v2 Function | v3 Function | Notes |
|------------|-------------|-------|
| `vendi_load_layout_based_sub_component(basename(__DIR__), 'layout')` | `vendi_load_component_v3(['component_name', 'field_name', 'layout'])` | Array syntax in v3 |
| `vendi_load_layout_based_sub_component_with_state(...)` | `vendi_load_component_v3(['...'], ['state' => $value])` | State is second parameter |
| `$vendi_layout_component_object_state` | `$vendi_component_object_state` | Renamed global variable |

### Dynamic Root Classes

Add dynamic classes in `initComponent()`:

```php
protected function initComponent(): void
{
    parent::initComponent();

    // Add class based on field value
    $this->addRootClass('variant-' . get_sub_field('variant'));

    // Conditional class
    if ($this->shouldShowAd()) {
        $this->addRootClass('show-ad');
    }

    // Add data attributes
    $this->addRootAttribute('data-role', 'carousel-container');
}
```

## v2 Migration Workflow

When the user asks to migrate a v2 component:

1. **Explore**: Read the v2 component files to understand structure
2. **Move Files**: Use git mv to move files to v3 structure
3. **Create Class**: Build component class with appropriate methods
4. **Refactor Template**: Update main PHP file to v3 pattern
5. **Handle Sub-Layouts**: Migrate any sub-layouts if present
6. **Document**: Create docs.yaml and markdown documentation
7. **Clean Up**: Remove empty v2 directories with rmdir
8. **Remind**: Tell user the component is ready to commit (they handle git add/commit)

Use the TodoWrite tool to track progress through these steps for complex migrations.

Always reference the existing migrated components for patterns and examples.

---

# v1 to v3 Migration (Utility/Site Components)

## Overview

v1 components are utility components stored in `page-parts/site/` or `page-parts/page/` directories. These are **not** flexible content components - they're called from other components using loader functions.

### Key Differences from v2:

- **Single files**, not directories (e.g., `page-parts/site/ad-slot.php`)
- **No CSS/JS files** to migrate (assets stored elsewhere or inline)
- **No sub-layouts** (simple utility components)
- **Documentation**: Only `overview.md` (no accessibility.md for utility components)
- **Loader functions**: Called via `vendi_load_site_component()` or `vendi_load_page_component()`
- **State via global**: Use `$vendi_component_object_state` global for passed parameters

## File Structure Transformation

### v1 Structure (page-parts/)
```
page-parts/site/ad-slot.php    (single file)
```

### v3 Structure (vendi-theme-parts/components/)
```
vendi-theme-parts/components/ad-slot/
├── ad-slot.php          (migrated from page-parts/site/)
├── ad-slot.class.php    (new)
├── ad-slot.docs.yaml    (new)
└── docs/
    └── overview.md      (only overview, no accessibility)
```

## Migration Steps

### Step 1: Identify Component Type

v1 components are loaded via:
- `vendi_load_site_component('component-name')`
- `vendi_load_site_component_with_state('component-name', ['key' => $value])`
- `vendi_load_page_component('component-name')`

These map to v3 as:
- `vendi_load_component_v3(['component-name'])`
- `vendi_load_component_v3(['component-name'], ['key' => $value])`

### Step 2: Move File

```bash
mkdir -p vendi-theme-parts/components/[component-name]
git mv page-parts/site/[component-name].php vendi-theme-parts/components/[component-name]/[component-name].php
```

### Step 3: Create Class File

Create `[component-name].class.php` extending **VendiComponent** (utility components don't need full wrappers):

```php
<?php

namespace Vendi\Theme\Component;

use Vendi\Theme\VendiComponent;

class component_name extends VendiComponent
{
    public function __construct()
    {
        parent::__construct('component-class-name');
    }

    protected function abortRender(): bool
    {
        if (!$this->getRequiredData()) {
            return true;
        }
        return parent::abortRender();
    }

    // Getter methods for state data
    public function getStateValue(): mixed
    {
        global $vendi_component_object_state;
        return $vendi_component_object_state['key'] ?? null;
    }

    // Helper methods for data from state objects
    public function getSomething(): ?string
    {
        return get_field('field_name', $this->getStateValue());
    }
}
```

**Important**: Utility components still use `$vendi_component_object_state` global to access passed state.

### Step 4: Refactor Template

Update the template to use component class:

```php
<?php

use Vendi\Theme\Component\component_name;
use Vendi\Theme\ComponentUtility;

/** @var component_name $component */
$component = ComponentUtility::get_new_component_instance(component_name::class);

if (!$component->renderComponentWrapperStart()) {
    return;
}

// Extract data using component methods
$value = $component->getSomething();

?>
<div class="content">
    <?php if ($value): ?>
        <?php echo esc_html($value); ?>
    <?php endif; ?>
</div>
<?php

$component->renderComponentWrapperEnd();
```

**Code Style**:
- Use alternative PHP syntax (if:/endif, foreach:/endforeach)
- Double quotes for HTML attributes
- Inline variable assignment for single-use variables

### Step 5: Update All Loader References

Find all instances of the old loader functions and update them:

**Find references**:
```bash
grep -r "vendi_load_site_component.*'component-name'" --include="*.php"
```

**Update pattern**:
```php
// Old v1
vendi_load_site_component_with_state('component-name', ['key' => $value]);

// New v3
vendi_load_component_v3(['component-name'], ['key' => $value]);
```

Update ALL occurrences across:
- Other v3 components
- v2 components (layouts/)
- v1 components (page-parts/)

### Step 6: Create Documentation

**docs.yaml** (minimal for utility components):
```yaml
component-name: [Human Readable Name]
role: component
example-prefix: [component-name]
parent-field: site  # or 'page' depending on origin
pages:
    - Overview
```

**docs/overview.md**:
- Describe component purpose and function
- Mark as "Utility Component" or "Site Component"
- Document that it's called from other components, not flexible content
- List required state parameters with types
- Show usage example with `vendi_load_component_v3()`
- Document any special behaviors or integrations

**No accessibility.md** - Utility components don't need accessibility documentation.

### Step 7: No CSS/JS Migration

v1 components typically don't have dedicated CSS/JS files in their directories. Assets are:
- Inline in the template (keep as-is)
- Loaded from external sources (keep as-is)
- In global theme files (leave alone)

**Do not search for or migrate CSS/JS files** - they're optional and stored elsewhere.

### Step 8: Clean Up

The original file was moved with `git mv`, so no cleanup needed. The empty `page-parts/site/` or `page-parts/page/` directory will remain (it may contain other components).

## v1 Migration Workflow

When the user asks to migrate a v1 component:

1. **Identify**: Confirm it's from page-parts/ directory
2. **Move File**: Use git mv to move single file to v3 structure
3. **Create Class**: Build utility component class (VendiComponent)
4. **Refactor Template**: Update to use component class and state from global
5. **Update References**: Find and replace ALL loader function calls across codebase
6. **Document**: Create docs.yaml and overview.md (no accessibility.md)
7. **Remind**: Tell user the component is ready to commit (they handle git add/commit)

Use the TodoWrite tool to track progress through these steps.

## Key Reminders for v1 Migrations

- **Use VendiComponent** - Utility components don't need full BaseComponent wrappers
- **Access state via global** - `$vendi_component_object_state` still used in class methods
- **Update ALL references** - Search entire codebase for loader function calls
- **No CSS/JS** - Don't search for or migrate asset files
- **Only overview.md** - No accessibility documentation for utility components
- **Single file** - No sub-layouts or complex directory structures
