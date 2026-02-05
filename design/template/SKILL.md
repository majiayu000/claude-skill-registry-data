---
name: template
description: Create or edit Django templates with cotton components, template partials, and proper Tailwind usage. Use when creating/editing HTML templates, adding components, or when the user mentions templates, UI, or frontend work.
allowed-tools: Read, Grep, Glob, Write, Edit, Bash
---

# Template Creation and Editing

This Skill helps create and edit Django templates following established patterns and conventions.

## Template File Locations

### App-Specific Templates

Templates are organized by app in `freedom_ls/<app_name>/templates/`:

```
freedom_ls/
├── accounts/templates/
│   └── accounts/          # App-namespaced templates
├── base/templates/
│   ├── cotton/            # Shared cotton components
│   ├── partials/          # Shared partials
│   ├── allauth/           # Allauth template overrides
│   └── _base.html         # Base template for all pages
├── student_interface/templates/
│   └── student_interface/ # App-namespaced templates
├── educator_interface/templates/
│   └── educator_interface/
└── content_engine/templates/
    └── cotton/            # Content-specific components
```

### Naming Conventions

- **Page templates**: `freedom_ls/<app_name>/templates/<app_name>/<page_name>.html`
- **Cotton components**: `freedom_ls/<app_name>/templates/cotton/<component_name>.html`
- **Partials**: `freedom_ls/<app_name>/templates/partials/<partial_name>.html`
- **Base templates**: Prefixed with `_` (e.g., `_base.html`)

## Template Structure

### Standard Page Template

```django
{% extends '_base.html' %}

{% block title %}Page Title{% endblock %}

{% block content %}
    <div class="space-y-6">
        <h1>{{ page_title }}</h1>

        <!-- Content here -->
    </div>
{% endblock %}
```

### Common Template Blocks

From `_base.html`:
- `{% block head_title %}` - Browser tab title
- `{% block tailwind_css %}` - Override CSS includes
- `{% block extra_head %}` - Additional head content
- `{% block header %}` - Header section (includes header partial by default)
- `{% block body %}` - Entire body wrapper
- `{% block pre-content %}` - Before main content
- `{% block content %}` - Main page content
- `{% block extra_body %}` - After main content

## Tailwind CSS Usage

### CRITICAL: Check `tailwind.input.css` FIRST

**ALWAYS** check `tailwind.input.css` before writing Tailwind classes:

```bash
# Read the component classes available
cat tailwind.input.css
```

### Base Styles (Applied Automatically)

These are applied to all elements via `@layer base`:

**Typography**:
- `h1` - `text-4xl font-bold`
- `h2` - `text-3xl font-bold`
- `h3` - `text-2xl font-bold`
- `h4` - `text-xl font-bold`
- `a` - `underline text-blue-600`
- `ul` - `list-disc list-inside space-y-2`
- `ol` - `list-decimal space-y-2 list-inside`

**Form Elements** (automatically styled):
- `label` 
- `input`, `textarea`, `select` 
- `fieldset`, `legend` 
- `form`

### Tailwind Usage Rules

1. **Use whatever is defined in tailwind.input.css first**: `<ul>` NOT `<ul class="inline-block px-6 py-2 bg-blue-600...">`
2. **Rely on base styles**: Don't add `text-4xl font-bold` to `<h1>` - it's automatic
3. **Only add inline classes for unique styling**: Layout, spacing, positioning that's specific to that element
4. **Keep it DRY**: If writing the same classes multiple times, create a component class in `tailwind.input.css`

### Example: Good vs Bad

**BAD** (duplicating base styles):
```html
<h1 class="text-4xl font-bold">Title</h1>
<a class="underline text-blue-600" href="/">Link</a>
```

**GOOD** (relying on base styles):
```html
<h1>Title</h1>
<a href="/">Link</a>
```

## Cotton Components

Cotton is used for reusable UI components. Components use the `<c-component-name>` syntax.

### Creating a Cotton Component

**Location**: `apps/base/templates/cotton/<component-name>.html`

**Structure**:
```django
<c-vars
    prop1="default value"
    prop2=""
    class=""
/>

<div class="component-wrapper {{ class }}" {{ attrs }}>
    {{ slot }}
</div>

{% comment %}
Usage Examples:

<c-component-name prop1="value">
    Content goes here
</c-component-name>

<c-component-name prop2="something" class="extra-classes" />
{% endcomment %}
```


### Using Cotton Components

```django
<!-- Basic button -->
<c-button>Click me</c-button>

<!-- Button variants -->
<c-button variant="primary">Submit</c-button>
<c-button variant="danger">Delete</c-button>
<c-button variant="outline">Cancel</c-button>

<!-- Button as link -->
<c-button href="/somewhere">Go somewhere</c-button>

<!-- With additional classes -->
<c-button class="w-full">Full width button</c-button>

<!-- Loading indicator -->
<c-loading-indicator id="my-indicator" message="Loading data..." />

<!-- Modal -->
<c-modal id="my-modal" title="Confirm Action">
    Are you sure you want to proceed?
</c-modal>
```

### Cotton Component Best Practices

1. **Define all props in `<c-vars>`** with default values
2. **Include usage examples** in comments at the bottom
3. **Support `class` and `{{ attrs }}`** for flexibility
4. **Use `{{ slot }}` for content** unless specific structure needed
5. **Keep components focused** - one responsibility per component
6. **Don't write custom html when there is a cotton component that does the same thing**

### Example: Good vs Bad

**BAD** (reimplementing a button):
```html
<a class="btn" href="/">Link</a>
<button class="btn">Button</button>
```

**GOOD** (relying on existing components):
```html
<c-button href="/">Link</c-button>
<c-button>Button</c-button>
```
## Template Partials

Partials are template fragments either 
- stored in seperate files and loaded via `{% include %}` or HTMX.
- defined in a template file in which it is used, using `{% partialdef %}` 

### Creating a Partial File

**Location**: `freedom_ls/<app_name>/templates/partials/<partial_name>.html`

**Usage**:
```django
<!-- Include in template -->
{% include "partials/header.html" %}

<!-- Load via HTMX -->
<div hx-get="{% url 'app:partial_view' %}"
     hx-trigger="load"
     hx-indicator="#loading">
</div>
```
### Using Django-template-partials 

Define a new partial inside another template using:

```
{% partialdef "partial_name" %}
    <!-- content -->
{% endpartialdef %}
```

Partials can then be used either using the `partial` or the `include` tag.

```
{% include "path/to/template_file.html#partial-name" %}
{% partial "partial-name" %}
```

Context is passed to a partial using a with block:

```
# GOOD
{% with foo=bar %}
    {% partial "partial-name" %}
{% endwith %}

# BAD 
{% partial "partial-name" foo=bar %}

```

### Partial Best Practices

1. **Keep them focused** - Single responsibility
2. **Pass context explicitly** - Don't rely on implicit context
4. **Name clearly** - `partials/<descriptive_name>.html`, `{% partialdef descriptive_name %}`

## HTMX Integration

HTMX is loaded globally in `_base.html`.

### Common HTMX Patterns

**Load content on page load**:
```django
<div hx-get="{% url 'app:endpoint' %}"
     hx-trigger="load"
     hx-indicator="#loading-indicator">
</div>
<c-loading-indicator id="loading-indicator" message="Loading..." />
```

**Form submission**:
```django
<form hx-post="{% url 'app:submit' %}"
      hx-target="#result"
      hx-swap="innerHTML">
    <!-- form fields -->
    <c-button type="submit" class="btn btn-primary">Submit</c-button>
</form>
<div id="result"></div>
```

**Click to load**:
```django
<c-button hx-get="{% url 'app:more' %}"
        hx-target="#content"
        hx-swap="beforeend"
        >
    Load More
</c-button>
```

### CSRF Token

CSRF token is set globally in `_base.html`:
```html
<body hx-headers='{"X-CSRFToken": "{{ csrf_token }}"}'>
```

No need to add it to individual HTMX requests.

## Alpine.js Integration

Alpine.js is loaded globally for reactive components.

**Example**:
```django
<div x-data="{ open: false }">
    <c-button @click="open = !open">
        Toggle
    </c-button>
    <div x-show="open" class="mt-4">
        Content that appears/disappears
    </div>
</div>
```

## Template Context

### Available in All Templates

From middleware and context processors:

- `site_title` - Current site's title
- `user` - Current user (from Django)
- `request` - Current request
- `csrf_token` - CSRF token

### Template Tags

**Always loaded**:
```django
{% load static %}
{% load i18n %}
```

**Cotton (loaded automatically)**:
Cotton components work without explicit loading.

**Template Partials** (when using partials):
Template Partials work without explicit loading.

```django
{% partialdef "partial_name" %}
    <!-- content -->
{% endpartialdef %}
```

## Creating a New Template: Workflow

### 1. Determine Template Type and Location

- **Page template**: `freedom_ls/<app_name>/templates/<app_name>/<page>.html`
- **Cotton component**: `freedom_ls/<app_name>/templates/cotton/<component>.html`
- **Partial**: `freedom_ls/<app_name>/templates/partials/<partial>.html`

### 2. Read Existing Templates

Check existing templates in the same app or `base/` for patterns:

```bash
# List existing templates
find freedom_ls/<app_name>/templates -name "*.html"

# Read similar template
cat freedom_ls/<app_name>/templates/<app_name>/similar_page.html
```

### 3. Check Available Components

Before writing custom HTML, check what's available:

```bash
# Check cotton components
ls freedom_ls/base/templates/cotton/
ls freedom_ls/*/templates/cotton/

# Read component to see usage
cat freedom_ls/base/templates/cotton/button.html
```

### 4. Check Tailwind Component Classes

**ALWAYS** check `tailwind.input.css` first:

```bash
cat tailwind.input.css
```

Look for:
- Component classes in `@layer components`
- Base styles in `@layer base`
- Utility classes in `@layer utilities`

### 5. Write the Template

Follow the appropriate structure:
- Extend `_base.html` for pages
- Use `<c-vars>` for cotton components
- Keep partials focused

### 6. Use Existing Components and Classes

- Use `<c-button>`, `<c-modal>`, etc. when applicable
- Rely on base styles for typography and forms
- Only add inline Tailwind for unique styling

### 7. Test in Browser

Build CSS if using new Tailwind classes:
```bash
npm run tailwind_build
```

## Editing Existing Templates: Workflow

### 1. Read the Template

```bash
cat freedom_ls/<app_name>/templates/<app_name>/<template>.html
```

### 2. Understand Current Structure

- What blocks are used?
- What components are included?
- What HTMX patterns are present?

### 3. Check for Dependencies

- Are there related partials?
- Are there cotton components being used?
- Is there JavaScript/Alpine.js?

### 4. Make Focused Changes

- Keep edits minimal and focused
- Don't refactor unnecessarily
- Maintain existing patterns
- Use component classes, not inline styles

### 5. Verify CSS Classes

If adding new styling, check `tailwind.input.css` first.

## Common Pitfalls to Avoid

1. **Not checking `tailwind.input.css`** - Always check for existing component classes first
2. **Duplicating base styles** - `h1`, `a`, forms are already styled
3. **Creating cotton components for one-off use** - Use partials or inline HTML
4. **Not including usage examples in cotton components** - Always document
5. **Forgetting app namespacing** - Templates should be in `<app_name>/` subdirectory
6. **Hard-coding values** - Use context variables and settings
7. **Not testing HTMX endpoints** - Verify URLs exist and return correct partial
8. **Using placeholder urls and  hardcoded urls** - project urls should all be correct and derived dynamically

## Example: Complete Cotton Component

```django
<c-vars
    variant="info"
    title=""
    dismissible="false"
    class=""
/>

<div class="surface {{ class }} {% if variant == 'info' %}bg-blue-50 border-blue-300{% elif variant == 'warning' %}bg-yellow-50 border-yellow-300{% elif variant == 'error' %}bg-red-50 border-red-300{% endif %}"
     {{ attrs }}>
    {% if title %}
        <h4 class="mb-2">{{ title }}</h4>
    {% endif %}

    <div class="prose">
        {{ slot }}
    </div>

    {% if dismissible %}
        <c-button class="btn btn-outline mt-4"
                x-data
                @click="$el.closest('.surface').remove()">
            Dismiss
        </c-button>
    {% endif %}
</div>

{% comment %}
Usage Examples:

<!-- Basic alert -->
<c-alert>
    This is an informational message.
</c-alert>

<!-- With title and variant -->
<c-alert variant="warning" title="Warning">
    Please review this carefully.
</c-alert>

<!-- Dismissible error -->
<c-alert variant="error" dismissible="true">
    An error occurred. Please try again.
</c-alert>
{% endcomment %}
```

## Example: Complete Page Template with HTMX

```django
{% extends '_base.html' %}

{% block title %}Student Dashboard{% endblock %}

{% block content %}
    <div class="space-y-8">
        <div class="flex justify-between items-center">
            <h1>Dashboard</h1>
            <c-button href="{% url 'student_interface:profile' %}">
                Edit Profile
            </c-button>
        </div>

        <!-- Static content -->
        <div class="surface">
            <h2 class="mb-4">Welcome, {{ user.first_name|default:user.email }}</h2>
            <p>Here's your current progress.</p>
        </div>

        <!-- Dynamic HTMX content -->
        <div hx-get="{% url 'student_interface:partial_courses' %}"
             hx-trigger="load"
             hx-indicator="#course-loading">
        </div>
        <c-loading-indicator id="course-loading" message="Loading courses..." />

        <!-- Interactive Alpine.js section -->
        <div x-data="{ showArchived: false }">
            <c-button @click="showArchived = !showArchived">
                <span x-text="showArchived ? 'Hide' : 'Show'"></span> Archived
            </c-button>

            <div x-show="showArchived"
                 hx-get="{% url 'student_interface:partial_archived' %}"
                 hx-trigger="revealed">
            </div>
        </div>
    </div>
{% endblock %}
```

## When to Use This Skill

Use this Skill when:
- User asks to create a new template, page, or component
- User wants to edit existing templates
- User mentions "UI", "frontend", "template", "HTML"
- Adding new pages to an app
- Creating reusable components
- Working with HTMX or Alpine.js in templates
- Styling with Tailwind CSS

## Quick Reference Checklist

Before creating/editing templates:

- [ ] Determine correct template location
- [ ] Read similar existing templates
- [ ] Check available cotton components
- [ ] Check `tailwind.input.css` for component classes
- [ ] Check available partials
- [ ] Extend `_base.html` for pages
- [ ] Use component classes instead of inline classes
- [ ] Rely on base styles for typography/forms
- [ ] Include usage examples in cotton components
- [ ] Test HTMX endpoints work
- [ ] Build CSS: `npm run tailwind_build`
