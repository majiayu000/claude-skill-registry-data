---
name: wordpress-accessibility-patterns
description: WordPress accessibility (a11y) patterns and WCAG 2.1 compliance guidelines. Use when reviewing WordPress themes, templates, forms, or interactive elements for accessibility, implementing WCAG standards, or checking keyboard navigation, screen reader compatibility, and ARIA patterns.
---

# WordPress Accessibility Patterns

Comprehensive WCAG 2.1 Level AA compliance patterns for WordPress development. This skill provides the knowledge base for building and reviewing accessible WordPress sites.

## WCAG 2.1 Principles

**POUR Principles:**
- **Perceivable** - Information must be presentable to users in ways they can perceive
- **Operable** - Interface components must be operable by all users
- **Understandable** - Information and operation must be understandable
- **Robust** - Content must be robust enough for assistive technologies

## Semantic HTML Structure

### Heading Hierarchy (WCAG 1.3.1, 2.4.6)

**Required Pattern:**
```php
// ✅ CORRECT - Logical hierarchy
<h1><?php the_title(); ?></h1>
<h2>Section Title</h2>
<h3>Subsection Title</h3>
<h4>Detail Title</h4>

// ❌ WRONG - Skips levels
<h1>Page Title</h1>
<h3>Section</h3> <!-- Skipped h2 -->
```

**Rules:**
- One h1 per page (typically page/post title)
- Never skip heading levels
- Don't use headings for styling only
- Headings should describe content structure

### Landmark Regions (WCAG 1.3.1, 2.4.1)

**Required HTML5 Landmarks:**
```php
// ✅ CORRECT - Semantic structure
<header class="site-header">
    <!-- Site header content -->
</header>

<nav aria-label="<?php esc_attr_e('Primary Navigation', 'textdomain'); ?>">
    <!-- Navigation menu -->
</nav>

<main id="main" class="site-main">
    <!-- Primary content -->
</main>

<aside aria-label="<?php esc_attr_e('Sidebar', 'textdomain'); ?>">
    <!-- Complementary content -->
</aside>

<footer class="site-footer">
    <!-- Footer content -->
</footer>

// ❌ WRONG - Divs without semantic meaning
<div class="header">
<div class="nav">
<div class="content">
```

**Multiple Landmarks:**
```php
// When multiple nav elements exist, distinguish them:
<nav aria-label="<?php esc_attr_e('Primary Navigation', 'textdomain'); ?>">
<nav aria-label="<?php esc_attr_e('Footer Navigation', 'textdomain'); ?>">
<nav aria-label="<?php esc_attr_e('Social Media', 'textdomain'); ?>">
```

### Lists (WCAG 1.3.1)

**Required Pattern:**
```php
// ✅ CORRECT - Semantic lists
<ul>
    <li><a href="#">Item 1</a></li>
    <li><a href="#">Item 2</a></li>
</ul>

// ❌ WRONG - Styled divs
<div class="list">
    <div class="item">• Item 1</div>
    <div class="item">• Item 2</div>
</div>
```

### Tables (WCAG 1.3.1)

**Required Pattern:**
```php
// ✅ CORRECT - Accessible table
<table>
    <caption><?php esc_html_e('User Data', 'textdomain'); ?></caption>
    <thead>
        <tr>
            <th scope="col"><?php esc_html_e('Name', 'textdomain'); ?></th>
            <th scope="col"><?php esc_html_e('Email', 'textdomain'); ?></th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><?php echo esc_html($name); ?></td>
            <td><?php echo esc_html($email); ?></td>
        </tr>
    </tbody>
</table>

// For row headers:
<th scope="row"><?php echo esc_html($label); ?></th>

// For complex tables:
<th id="header1"><?php esc_html_e('Header', 'textdomain'); ?></th>
<td headers="header1"><?php echo esc_html($data); ?></td>
```

## Keyboard Navigation (WCAG 2.1)

### Focus Management (WCAG 2.4.7, 2.1.1, 2.1.2)

**Required CSS:**
```css
/* ✅ CORRECT - Visible focus indicator */
a:focus, button:focus, input:focus, select:focus, textarea:focus {
    outline: 2px solid #0073aa;
    outline-offset: 2px;
}

/* ❌ WRONG - Removes focus */
*:focus {
    outline: none;
}

/* ✅ ACCEPTABLE - Custom focus with sufficient contrast */
.button:focus {
    outline: 3px solid #005a87;
    box-shadow: 0 0 0 3px rgba(0, 115, 170, 0.25);
}
```

**Focus Indicator Requirements:**
- Minimum 2px solid or 3px dotted
- Color contrast 3:1 with background
- Visible on all focusable elements
- Should not rely on color alone

### Skip Links (WCAG 2.4.1)

**Required Pattern:**
```php
// ✅ CORRECT - Skip link as first focusable element
<body <?php body_class(); ?>>
<a class="skip-link screen-reader-text" href="#main">
    <?php esc_html_e('Skip to content', 'textdomain'); ?>
</a>

<!-- CSS for skip link -->
<style>
.skip-link {
    position: absolute;
    top: -40px;
    left: 0;
    z-index: 100000;
    padding: 8px 15px;
    background: #0073aa;
    color: #fff;
    text-decoration: none;
}

.skip-link:focus {
    top: 0;
}
</style>
```

### Interactive Elements (WCAG 2.1.1, 2.1.3)

**Button Pattern:**
```php
// ✅ CORRECT - Semantic button
<button type="button" onclick="doAction()">
    <?php esc_html_e('Click Me', 'textdomain'); ?>
</button>

// ❌ WRONG - Div as button
<div class="button" onclick="doAction()">Click Me</div>

// ✅ ACCEPTABLE - Div with ARIA (if semantic HTML not possible)
<div role="button" tabindex="0" 
     onclick="doAction()" 
     onkeydown="if(event.key==='Enter'||event.key===' '){doAction()}">
    <?php esc_html_e('Click Me', 'textdomain'); ?>
</div>
```

**Link vs Button:**
```php
// ✅ Links navigate (have href)
<a href="<?php echo esc_url($url); ?>">
    <?php esc_html_e('Go to Page', 'textdomain'); ?>
</a>

// ✅ Buttons perform actions
<button type="button" onclick="openModal()">
    <?php esc_html_e('Open Dialog', 'textdomain'); ?>
</button>

// ❌ WRONG - Link without href used as button
<a onclick="doAction()">Click</a>
```

### Tab Order (WCAG 2.4.3)

**Rules:**
```php
// ✅ Use natural tab order (avoid tabindex > 0)
// Elements tab in DOM order by default

// ✅ CORRECT - Make non-focusable element focusable
<div tabindex="0" role="button">Custom Element</div>

// ✅ CORRECT - Remove from tab order
<div tabindex="-1">Not keyboard accessible</div>

// ❌ WRONG - Forces tab order (avoid)
<input tabindex="3">
<input tabindex="1">
<input tabindex="2">
```

## Form Accessibility (WCAG 3.3)

### Labels (WCAG 1.3.1, 3.3.2)

**Required Pattern:**
```php
// ✅ CORRECT - Explicit label
<label for="email">
    <?php esc_html_e('Email Address', 'textdomain'); ?>
    <span class="required" aria-hidden="true">*</span>
    <span class="screen-reader-text">
        <?php esc_html_e('(required)', 'textdomain'); ?>
    </span>
</label>
<input type="email" id="email" name="email" required aria-required="true">

// ❌ WRONG - No label
<input type="text" placeholder="Name">

// ❌ WRONG - Placeholder as label only
<input type="text" name="email" placeholder="Email Address">
```

**Label Association Methods:**
```php
// Method 1: Explicit (recommended)
<label for="field-id">Label</label>
<input id="field-id" name="field">

// Method 2: Implicit (works but less flexible)
<label>
    <?php esc_html_e('Label', 'textdomain'); ?>
    <input name="field">
</label>
```

### Required Fields (WCAG 3.3.2)

**Required Pattern:**
```php
// ✅ CORRECT - Multiple indicators
<label for="username">
    <?php esc_html_e('Username', 'textdomain'); ?>
    <span class="required" aria-hidden="true">*</span>
</label>
<input type="text" id="username" name="username" 
       required aria-required="true">

// Page should also have:
<p class="form-instructions">
    <?php esc_html_e('Fields marked with * are required', 'textdomain'); ?>
</p>
```

### Error Messages (WCAG 3.3.1, 3.3.3)

**Required Pattern:**
```php
// ✅ CORRECT - Accessible error handling
<?php if (is_wp_error($error)): ?>
    <div class="error" role="alert" aria-live="assertive">
        <?php echo esc_html($error->get_error_message()); ?>
    </div>
<?php endif; ?>

<label for="email"><?php esc_html_e('Email', 'textdomain'); ?></label>
<input type="email" id="email" name="email"
       aria-invalid="<?php echo is_wp_error($error) ? 'true' : 'false'; ?>"
       aria-describedby="email-error">
<?php if (is_wp_error($error)): ?>
    <span id="email-error" class="error-message">
        <?php echo esc_html($error->get_error_message()); ?>
    </span>
<?php endif; ?>
```

### Instructions (WCAG 3.3.2)

**Required Pattern:**
```php
// ✅ CORRECT - Associated instructions
<label for="password"><?php esc_html_e('Password', 'textdomain'); ?></label>
<input type="password" id="password" name="password"
       aria-describedby="password-hint">
<span id="password-hint" class="description">
    <?php esc_html_e('Must be at least 8 characters with one number', 'textdomain'); ?>
</span>
```

### Fieldsets (WCAG 1.3.1)

**Required Pattern for Related Inputs:**
```php
// ✅ CORRECT - Grouped radio buttons
<fieldset>
    <legend><?php esc_html_e('Notification Preferences', 'textdomain'); ?></legend>
    <label>
        <input type="radio" name="notifications" value="all">
        <?php esc_html_e('All notifications', 'textdomain'); ?>
    </label>
    <label>
        <input type="radio" name="notifications" value="important">
        <?php esc_html_e('Important only', 'textdomain'); ?>
    </label>
    <label>
        <input type="radio" name="notifications" value="none">
        <?php esc_html_e('No notifications', 'textdomain'); ?>
    </label>
</fieldset>
```

## Images & Media (WCAG 1.1.1, 1.2)

### Alternative Text

**Decision Tree:**
```
Is the image decorative only?
├─ YES → alt=""
└─ NO → Is it functional (button, link)?
    ├─ YES → alt="[function]" (e.g., "Search")
    └─ NO → Is it informative?
        ├─ Simple → alt="[brief description]"
        └─ Complex → alt="[brief]" + aria-describedby="[detailed]"
```

**Patterns:**
```php
// ✅ Decorative image
<img src="divider.png" alt="" role="presentation">

// ✅ Informative image
<img src="chart.png" alt="<?php esc_attr_e('Sales increased 50% in Q4', 'textdomain'); ?>">

// ✅ Functional image (in link)
<a href="<?php echo esc_url(home_url('/')); ?>">
    <img src="logo.png" alt="<?php echo esc_attr(get_bloginfo('name')); ?>">
</a>

// ✅ Icon button
<button type="submit">
    <svg aria-hidden="true" focusable="false"><!-- icon --></svg>
    <span class="screen-reader-text"><?php esc_html_e('Search', 'textdomain'); ?></span>
</button>

// ✅ Complex image with description
<img src="infographic.png" 
     alt="<?php esc_attr_e('2024 Sales Data', 'textdomain'); ?>"
     aria-describedby="sales-desc">
<div id="sales-desc" class="screen-reader-text">
    <?php esc_html_e('Sales grew from $10k in January to $50k in December, with steady growth each month.', 'textdomain'); ?>
</div>

// ❌ WRONG - Missing alt
<img src="photo.jpg">

// ❌ WRONG - Generic alt
<img src="chart.png" alt="chart">

// ❌ WRONG - Filename as alt
<img src="img_1234.jpg" alt="img_1234.jpg">
```

### Video & Audio (WCAG 1.2)

**Required Pattern:**
```php
// ✅ CORRECT - Video with captions and transcript
<video controls>
    <source src="<?php echo esc_url($video_url); ?>" type="video/mp4">
    <track kind="captions" src="<?php echo esc_url($captions_url); ?>" 
           srclang="en" label="English">
    <?php esc_html_e('Your browser does not support video', 'textdomain'); ?>
</video>
<details>
    <summary><?php esc_html_e('Video Transcript', 'textdomain'); ?></summary>
    <?php echo wp_kses_post($transcript); ?>
</details>

// ❌ WRONG - Autoplay without user control
<video autoplay>

// ❌ WRONG - No captions
<video controls>
    <source src="video.mp4">
</video>
```

## Color & Contrast (WCAG 1.4.3, 1.4.6, 1.4.11)

### Contrast Ratios

**Level AA Requirements:**
- Normal text (< 18pt): **4.5:1** minimum
- Large text (≥ 18pt or ≥ 14pt bold): **3:1** minimum
- UI components: **3:1** minimum

**Level AAA (recommended):**
- Normal text: **7:1** minimum
- Large text: **4.5:1** minimum

**Examples:**
```css
/* ✅ CORRECT - Sufficient contrast (4.63:1) */
.text {
    color: #595959;
    background: #ffffff;
}

/* ✅ CORRECT - Large text acceptable (3.05:1) */
.heading {
    font-size: 24px;
    color: #767676;
    background: #ffffff;
}

/* ❌ WRONG - Insufficient for normal text (3.05:1) */
.text {
    color: #767676;
    background: #ffffff;
}

/* ❌ WRONG - Very poor contrast (2.37:1) */
.text {
    color: #999999;
    background: #ffffff;
}
```

### Color Alone (WCAG 1.4.1)

**Required Pattern:**
```php
// ✅ CORRECT - Multiple indicators
<span class="required-field">
    <?php esc_html_e('Email', 'textdomain'); ?>
    <span style="color: red;">*</span>
    <span class="screen-reader-text"><?php esc_html_e('(required)', 'textdomain'); ?></span>
</span>

// ✅ CORRECT - Icon + color for status
<div class="status-success">
    <svg aria-hidden="true"><!-- checkmark icon --></svg>
    <span><?php esc_html_e('Success', 'textdomain'); ?></span>
</div>

// ❌ WRONG - Color only
<span style="color: red;">Required field</span>
```

## ARIA Patterns (Use Sparingly)

### First Rule of ARIA
**Don't use ARIA if semantic HTML works!**

```php
// ❌ WRONG - Unnecessary ARIA
<div role="button" tabindex="0">Click</div>

// ✅ CORRECT - Semantic HTML
<button type="button">Click</button>
```

### When ARIA Is Appropriate

**Live Regions (WCAG 4.1.3):**
```php
// Status messages (polite - doesn't interrupt)
<div role="status" aria-live="polite">
    <?php esc_html_e('Saving...', 'textdomain'); ?>
</div>

// Critical alerts (assertive - interrupts)
<div role="alert" aria-live="assertive">
    <?php esc_html_e('Error: Save failed', 'textdomain'); ?>
</div>
```

**Expanded/Collapsed States:**
```php
// ✅ CORRECT - Accordion
<button aria-expanded="false" aria-controls="section-1" 
        onclick="toggleSection()">
    <?php esc_html_e('Show Details', 'textdomain'); ?>
</button>
<div id="section-1" hidden>
    <?php echo wp_kses_post($content); ?>
</div>

<script>
function toggleSection() {
    const button = event.target;
    const section = document.getElementById(button.getAttribute('aria-controls'));
    const expanded = button.getAttribute('aria-expanded') === 'true';
    
    button.setAttribute('aria-expanded', !expanded);
    section.hidden = expanded;
}
</script>
```

**Modal Dialogs:**
```php
// ✅ CORRECT - Accessible modal
<div role="dialog" aria-modal="true" aria-labelledby="modal-title">
    <h2 id="modal-title"><?php esc_html_e('Confirm Action', 'textdomain'); ?></h2>
    <p><?php esc_html_e('Are you sure?', 'textdomain'); ?></p>
    <button type="button"><?php esc_html_e('Confirm', 'textdomain'); ?></button>
    <button type="button"><?php esc_html_e('Cancel', 'textdomain'); ?></button>
</div>
```

**Current Page (WCAG 2.4.8):**
```php
// ✅ CORRECT - Navigation with current page
<nav aria-label="<?php esc_attr_e('Primary', 'textdomain'); ?>">
    <ul>
        <li>
            <a href="/" <?php if (is_front_page()) echo 'aria-current="page"'; ?>>
                <?php esc_html_e('Home', 'textdomain'); ?>
            </a>
        </li>
    </ul>
</nav>
```

## WordPress-Specific Patterns

### Screen Reader Text

**Required CSS Class:**
```css
/* WordPress standard screen-reader-text class */
.screen-reader-text {
    border: 0;
    clip: rect(1px, 1px, 1px, 1px);
    clip-path: inset(50%);
    height: 1px;
    margin: -1px;
    overflow: hidden;
    padding: 0;
    position: absolute;
    width: 1px;
    word-wrap: normal !important;
}

.screen-reader-text:focus {
    background-color: #f1f1f1;
    border-radius: 3px;
    box-shadow: 0 0 2px 2px rgba(0, 0, 0, 0.6);
    clip: auto !important;
    clip-path: none;
    color: #21759b;
    display: block;
    font-size: 0.875rem;
    font-weight: 700;
    height: auto;
    left: 5px;
    line-height: normal;
    padding: 15px 23px 14px;
    text-decoration: none;
    top: 5px;
    width: auto;
    z-index: 100000;
}
```

### WordPress Menus

**Required Pattern:**
```php
// ✅ CORRECT - Accessible menu
wp_nav_menu(array(
    'theme_location' => 'primary',
    'container' => 'nav',
    'container_aria_label' => __('Primary Navigation', 'textdomain'),
    'menu_class' => 'primary-menu',
    'fallback_cb' => false,
));
```

## Mobile & Touch (WCAG 2.5)

### Touch Targets (WCAG 2.5.5)

**Required Size:**
- Minimum: **44×44 pixels**
- Adequate spacing between targets

```css
/* ✅ CORRECT - Sufficient touch target */
.mobile-button {
    min-width: 44px;
    min-height: 44px;
    padding: 12px;
}

/* ❌ WRONG - Too small */
.mobile-button {
    width: 30px;
    height: 30px;
}
```

### Viewport (WCAG 1.4.10)

**Required Meta Tag:**
```html
<!-- ✅ CORRECT - Allows zooming -->
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<!-- ❌ WRONG - Prevents zooming -->
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
```

## Animation & Motion (WCAG 2.3)

### Reduced Motion (WCAG 2.3.3)

**Required CSS:**
```css
/* ✅ CORRECT - Respects user preference */
@media (prefers-reduced-motion: reduce) {
    *,
    *::before,
    *::after {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
        scroll-behavior: auto !important;
    }
}
```

## Testing Checklist

### Automated Testing
- WAVE browser extension
- axe DevTools
- Lighthouse accessibility audit
- WordPress Accessibility Checker plugin

### Manual Testing
1. **Keyboard Navigation**
   - Tab through entire page
   - Verify all interactive elements reachable
   - Check focus indicators visible
   - Test skip links

2. **Screen Reader Testing**
   - NVDA (Windows - free)
   - JAWS (Windows - commercial)
   - VoiceOver (Mac - built-in)
   - Test heading navigation
   - Test landmark navigation
   - Verify form labels announced

3. **Color Contrast**
   - Use WebAIM Contrast Checker
   - Test all text/background combinations
   - Check UI component contrast

4. **Zoom Testing**
   - Test at 200% zoom
   - Verify no horizontal scrolling
   - Check content remains accessible

## Common WordPress Violations

1. ❌ Missing alt text on images
2. ❌ Links with "click here" text
3. ❌ Form inputs without labels
4. ❌ Insufficient color contrast
5. ❌ Skipped heading levels
6. ❌ Missing skip links
7. ❌ Icon buttons without labels
8. ❌ Keyboard inaccessible menus
9. ❌ Focus indicator removed
10. ❌ Autoplay videos

## Priority Levels

**CRITICAL (Level A) - Blocks Access:**
- Missing labels
- Keyboard inaccessible elements
- No skip links
- Images without alt text

**HIGH (Level AA) - Significantly Impairs:**
- Insufficient contrast
- Missing heading hierarchy
- Unlabeled landmarks
- Forms without error handling

**MEDIUM (Level AAA) - Could Improve:**
- Enhanced contrast
- Advanced ARIA patterns
- Detailed descriptions
- Extra context

## References

- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [WordPress Accessibility Handbook](https://make.wordpress.org/accessibility/handbook/)
- [WebAIM Resources](https://webaim.org/)
- [A11y Project](https://www.a11yproject.com/)
