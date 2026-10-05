---
name: wp-ux-design
description: WordPress UX and design enforcement — Core Web Vitals, mobile-first layout, typography, color systems, navigation, page builder patterns, image optimization, form UX, loading and error states, admin UX, and performance checklists with concrete CSS/HTML/PHP examples.
tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
---

# WordPress UX/Design Enforcement

Definitive standards for building WordPress sites that are fast, accessible, and visually consistent. Every rule below is enforceable in code review.

---

## 1. Core Web Vitals for WordPress

### LCP (Largest Contentful Paint) < 2.5s

The hero image or heading is almost always the LCP element. Prioritize it explicitly.

```html
<!-- Preload the hero image in <head> -->
<link rel="preload" as="image" href="/wp-content/uploads/hero.webp"
      fetchpriority="high" type="image/webp">

<!-- Mark the hero img element -->
<img src="hero.webp" alt="Hero banner" fetchpriority="high"
     width="1280" height="720" decoding="async">
```

WordPress-specific: disable lazy-load on the first image via filter.

```php
// functions.php — skip lazy-load on above-fold images
add_filter( 'wp_img_tag_add_loading_attr', function( $value, $image, $context ) {
    if ( str_contains( $image, 'hero-banner' ) ) {
        return false; // no loading="lazy"
    }
    return $value;
}, 10, 3 );
```

### CLS (Cumulative Layout Shift) < 0.1

Every replaced element MUST have explicit dimensions.

```css
/* Reserve space for images before load */
img, video, iframe {
    max-width: 100%;
    height: auto;
    aspect-ratio: attr(width) / attr(height);
}

/* Prevent font-swap layout shift */
@font-face {
    font-family: 'Brand';
    src: url('brand.woff2') format('woff2');
    font-display: swap;
    size-adjust: 105%; /* match fallback metrics */
    ascent-override: 95%;
}

/* Reserve ad/embed space */
.ad-slot { min-height: 250px; }
.embed-container { aspect-ratio: 16 / 9; }
```

### INP (Interaction to Next Paint) < 200ms

```js
// Debounce expensive scroll/resize handlers
function debounce(fn, ms = 150) {
    let id;
    return (...args) => { clearTimeout(id); id = setTimeout(() => fn(...args), ms); };
}
window.addEventListener('scroll', debounce(handleScroll), { passive: true });

// Break long tasks with yield
async function processItems(items) {
    for (const item of items) {
        doWork(item);
        if (performance.now() - start > 50) {
            await new Promise(r => setTimeout(r, 0)); // yield to main thread
        }
    }
}
```

Keep DOM under 1500 nodes. Audit with: `document.querySelectorAll('*').length`.

---

## 2. Mobile-First WordPress Design

### Breakpoint Strategy

```css
/* Mobile-first: base styles are mobile (320px+) */
/* Small phones handled by fluid units, no breakpoint needed */

@media (min-width: 480px)  { /* Large phones */  }
@media (min-width: 768px)  { /* Tablets */        }
@media (min-width: 1024px) { /* Small desktop */  }
@media (min-width: 1280px) { /* Large desktop */  }
```

### Touch Targets and Viewport

```css
/* Minimum 44x44px touch targets — WCAG 2.5.8 */
button, a, input, select, textarea {
    min-height: 44px;
    min-width: 44px;
}

/* Prevent iOS zoom on input focus */
input, select, textarea {
    font-size: 16px; /* >= 16px prevents auto-zoom */
}
```

```html
<meta name="viewport" content="width=device-width, initial-scale=1">
```

### Mobile Menu Patterns

Hamburger menu for primary nav on mobile. Place critical actions in thumb zone (bottom 40% of screen).

```css
/* Bottom nav for high-frequency actions */
.mobile-bottom-nav {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    height: 56px;
    display: flex;
    justify-content: space-around;
    align-items: center;
    background: var(--wp--preset--color--base);
    box-shadow: 0 -1px 3px rgb(0 0 0 / 0.1);
    z-index: 100;
    padding-bottom: env(safe-area-inset-bottom);
}

@media (min-width: 768px) {
    .mobile-bottom-nav { display: none; }
}
```

---

## 3. Typography System

### Modular Scale (ratio 1.25 — Major Third)

```css
:root {
    --step--2: clamp(0.64rem, 0.58rem + 0.28vw, 0.80rem);
    --step--1: clamp(0.80rem, 0.73rem + 0.35vw, 1.00rem);
    --step-0:  clamp(1.00rem, 0.91rem + 0.43vw, 1.25rem);  /* body */
    --step-1:  clamp(1.25rem, 1.14rem + 0.54vw, 1.56rem);  /* h4 */
    --step-2:  clamp(1.56rem, 1.43rem + 0.68vw, 1.95rem);  /* h3 */
    --step-3:  clamp(1.95rem, 1.78rem + 0.85vw, 2.44rem);  /* h2 */
    --step-4:  clamp(2.44rem, 2.23rem + 1.07vw, 3.05rem);  /* h1 */
}
```

### WordPress theme.json Typography

```json
{
    "settings": {
        "typography": {
            "fluid": true,
            "fontSizes": [
                { "slug": "small",  "size": "clamp(0.80rem, 0.73rem + 0.35vw, 1.00rem)", "name": "Small" },
                { "slug": "medium", "size": "clamp(1.00rem, 0.91rem + 0.43vw, 1.25rem)", "name": "Medium" },
                { "slug": "large",  "size": "clamp(1.56rem, 1.43rem + 0.68vw, 1.95rem)", "name": "Large" },
                { "slug": "x-large","size": "clamp(2.44rem, 2.23rem + 1.07vw, 3.05rem)", "name": "Extra Large" }
            ],
            "fontFamilies": [
                { "slug": "brand", "fontFamily": "'Brand', system-ui, sans-serif", "name": "Brand" },
                { "slug": "mono",  "fontFamily": "'JetBrains Mono', monospace",    "name": "Mono"  }
            ]
        }
    }
}
```

### Line Length and Spacing

```css
/* Optimal measure: 45-75 characters */
.entry-content p,
.entry-content li {
    max-width: 65ch;
    line-height: 1.6;
}

h1, h2, h3 { line-height: 1.2; }
h4, h5, h6 { line-height: 1.3; }
```

### Font Loading Strategy

```php
// Preload critical fonts in <head>
add_action( 'wp_head', function() {
    echo '<link rel="preload" href="' . get_theme_file_uri('fonts/brand.woff2')
       . '" as="font" type="font/woff2" crossorigin>' . "\n";
}, 1 );
```

---

## 4. Color System

### theme.json Color Palette

```json
{
    "settings": {
        "color": {
            "palette": [
                { "slug": "primary",    "color": "#1a56db", "name": "Primary"    },
                { "slug": "secondary",  "color": "#6b7280", "name": "Secondary"  },
                { "slug": "accent",     "color": "#f59e0b", "name": "Accent"     },
                { "slug": "base",       "color": "#ffffff", "name": "Base"       },
                { "slug": "contrast",   "color": "#111827", "name": "Contrast"   },
                { "slug": "success",    "color": "#059669", "name": "Success"    },
                { "slug": "warning",    "color": "#d97706", "name": "Warning"    },
                { "slug": "error",      "color": "#dc2626", "name": "Error"      }
            ]
        }
    }
}
```

### Semantic Token Usage

```css
/* Use WordPress preset variables everywhere */
.btn-primary {
    background: var(--wp--preset--color--primary);
    color: var(--wp--preset--color--base);
}

.alert-error {
    border-left: 4px solid var(--wp--preset--color--error);
    background: color-mix(in srgb, var(--wp--preset--color--error) 8%, white);
}
```

### WCAG AA Contrast (4.5:1 text, 3:1 large text/UI)

```css
/* Dark mode via media query */
@media (prefers-color-scheme: dark) {
    :root {
        --wp--preset--color--base: #111827;
        --wp--preset--color--contrast: #f9fafb;
    }
}
```

Always verify contrast ratios. Minimum 4.5:1 for body text, 3:1 for large text (18px+ or 14px bold) and UI components.

---

## 5. Navigation UX

### Breadcrumbs

```php
// Output semantic breadcrumbs (works with Yoast, Rank Math, or custom)
function zentratec_breadcrumbs() {
    if ( function_exists('rank_math_the_breadcrumbs') ) {
        rank_math_the_breadcrumbs();
    } elseif ( function_exists('yoast_breadcrumb') ) {
        yoast_breadcrumb('<nav aria-label="Breadcrumb">', '</nav>');
    }
}
```

### Pagination: Prefer Numbered Over Infinite Scroll

Infinite scroll breaks footer access and disables back-button history. Use numbered pagination or "Load More" with URL state.

```php
// Accessible numbered pagination
the_posts_pagination([
    'mid_size'  => 2,
    'prev_text' => '<span aria-label="Previous page">&laquo;</span>',
    'next_text' => '<span aria-label="Next page">&raquo;</span>',
]);
```

### Back-to-Top

```css
.back-to-top {
    position: fixed;
    bottom: 2rem;
    right: 2rem;
    opacity: 0;
    transition: opacity 200ms ease;
    pointer-events: none;
}
.back-to-top.visible {
    opacity: 1;
    pointer-events: auto;
}
```

```js
const btn = document.querySelector('.back-to-top');
const observer = new IntersectionObserver(([e]) => {
    btn.classList.toggle('visible', !e.isIntersecting);
}, { rootMargin: '-300px 0px 0px 0px' });
observer.observe(document.querySelector('header'));
```

---

## 6. Page Builder UX

### Section / Row / Column Hierarchy

All builders (Tatsu, Elementor, WPBakery) share this pattern. Enforce consistent spacing at each level.

```css
/* Consistent section spacing */
.tatsu-section,
.elementor-section,
.vc_section {
    padding-block: var(--section-spacing, clamp(3rem, 6vw, 6rem));
}

/* Content width management */
.tatsu-row,
.elementor-container,
.vc_row {
    max-width: var(--content-width, 1200px);
    margin-inline: auto;
    padding-inline: clamp(1rem, 3vw, 2rem);
}
```

### Builder CSS Override Pattern

Use specificity, not `!important`. Target the builder's own wrapper classes.

```css
/* Override builder defaults cleanly with specificity */
body .tatsu-section .tatsu-column .tatsu-text-block p {
    font-size: var(--step-0);
    line-height: 1.6;
    max-width: 65ch;
}

/* For Elementor: use the widget wrapper */
.elementor-widget-text-editor .elementor-widget-container p {
    font-size: var(--step-0);
}
```

---

## 7. Image Optimization UX

### Responsive Images with Art Direction

```html
<picture>
    <source media="(min-width: 768px)"
            srcset="wide-800.webp 800w, wide-1200.webp 1200w, wide-1600.webp 1600w"
            sizes="(min-width: 1280px) 1200px, 100vw"
            type="image/webp">
    <source srcset="square-400.webp 400w, square-600.webp 600w"
            sizes="100vw" type="image/webp">
    <img src="fallback-800.jpg" alt="Descriptive alt text"
         width="800" height="600" loading="lazy" decoding="async">
</picture>
```

### WordPress Lazy Loading Rules

- Above-fold images: NO `loading="lazy"`, YES `fetchpriority="high"`
- Below-fold images: YES `loading="lazy"`, YES `decoding="async"`
- Background images: use `content-visibility: auto` on the container

### Placeholder Strategy (LQIP)

```php
// Generate inline low-quality placeholder
function get_lqip_style( $attachment_id ) {
    $thumb = wp_get_attachment_image_url( $attachment_id, [32, 32] );
    if ( ! $thumb ) return '';
    return sprintf(
        'background: url(%s) center/cover no-repeat; filter: blur(20px);',
        esc_url( $thumb )
    );
}
```

```html
<div class="img-wrapper" style="<?php echo get_lqip_style($id); ?>">
    <img src="full.webp" loading="lazy" decoding="async"
         onload="this.parentElement.style.background='none'"
         width="800" height="600" alt="Photo description">
</div>
```

---

## 8. Form UX

### Inline Validation and Smart Defaults

```html
<form novalidate>
    <div class="field-group">
        <label for="email">Email address</label>
        <input id="email" type="email" name="email" required
               autocomplete="email" inputmode="email"
               aria-describedby="email-error"
               pattern="[^@]+@[^@]+\.[a-zA-Z]{2,}">
        <p id="email-error" class="field-error" role="alert" hidden>
            Enter a valid email address
        </p>
    </div>
</form>
```

```js
// Inline validation on blur, not on input
document.querySelectorAll('input[required]').forEach(input => {
    input.addEventListener('blur', () => {
        const error = document.getElementById(input.getAttribute('aria-describedby'));
        if (!error) return;
        const invalid = !input.validity.valid;
        error.hidden = !invalid;
        input.setAttribute('aria-invalid', String(invalid));
    });
});
```

### Multi-Step Forms

```css
/* Progress indicator */
.form-steps {
    display: flex;
    gap: 0.5rem;
    counter-reset: step;
}
.form-step { counter-increment: step; }
.form-step::before {
    content: counter(step);
    display: grid;
    place-items: center;
    width: 2rem;
    height: 2rem;
    border-radius: 50%;
    background: var(--wp--preset--color--secondary);
    color: white;
    font-weight: 700;
}
.form-step[aria-current="step"]::before {
    background: var(--wp--preset--color--primary);
}
```

### Autocomplete Attributes Checklist

Always set: `name`, `email`, `tel`, `street-address`, `postal-code`, `country`, `cc-number`, `cc-exp`, `cc-csc`, `given-name`, `family-name`, `organization`.

---

## 9. Loading States

### Skeleton Screens Over Spinners

Skeletons preserve layout and feel faster than spinners. Use them for content regions.

```css
.skeleton {
    background: linear-gradient(90deg,
        var(--wp--preset--color--base) 25%,
        color-mix(in srgb, var(--wp--preset--color--contrast) 8%, transparent) 50%,
        var(--wp--preset--color--base) 75%);
    background-size: 200% 100%;
    animation: shimmer 1.5s infinite;
    border-radius: 4px;
}
@keyframes shimmer { to { background-position: -200% 0; } }

.skeleton-text { height: 1em; margin-bottom: 0.75em; }
.skeleton-text:last-child { width: 60%; }
.skeleton-image { aspect-ratio: 16 / 9; }
```

### Transition Timing

- Micro-interactions (hover, focus): 150ms
- Content transitions (modals, accordions): 250ms
- Page-level transitions: 300ms
- Easing: `cubic-bezier(0.4, 0, 0.2, 1)` for standard, `cubic-bezier(0, 0, 0.2, 1)` for deceleration

### WordPress AJAX Pattern

```js
async function wpAjaxLoad(action, container) {
    container.setAttribute('aria-busy', 'true');
    container.innerHTML = '<div class="skeleton skeleton-text"></div>'.repeat(3);
    try {
        const res = await fetch(wpApiSettings.root + action, {
            headers: { 'X-WP-Nonce': wpApiSettings.nonce }
        });
        if (!res.ok) throw new Error(res.statusText);
        container.innerHTML = await res.text();
    } catch (err) {
        container.innerHTML = '<p class="error-message">Failed to load. <button onclick="wpAjaxLoad(\'' + action + '\', this.closest(\'[aria-busy]\'))">Retry</button></p>';
    } finally {
        container.removeAttribute('aria-busy');
    }
}
```

---

## 10. Error States

### 404 Page Requirements

Every 404 must include: (1) clear "not found" message, (2) search form, (3) popular/recent content links, (4) link back to homepage.

```php
// 404.php template
get_header(); ?>
<main class="error-404" role="main">
    <h1><?php esc_html_e('Page not found', 'theme'); ?></h1>
    <p><?php esc_html_e('The page you requested does not exist or has moved.', 'theme'); ?></p>
    <?php get_search_form(); ?>
    <h2><?php esc_html_e('Popular pages', 'theme'); ?></h2>
    <ul>
    <?php
    $popular = new WP_Query(['posts_per_page' => 5, 'orderby' => 'comment_count']);
    while ($popular->have_posts()) : $popular->the_post(); ?>
        <li><a href="<?php the_permalink(); ?>"><?php the_title(); ?></a></li>
    <?php endwhile; wp_reset_postdata(); ?>
    </ul>
    <a href="<?php echo esc_url(home_url('/')); ?>"><?php esc_html_e('Back to homepage', 'theme'); ?></a>
</main>
<?php get_footer();
```

### Form Error Recovery

Never clear valid fields on error. Scroll to the first error. Announce errors to screen readers with `role="alert"`.

### Graceful Degradation

```php
// Fallback when external service fails
function get_external_data() {
    $cached = get_transient('external_data');
    if ($cached !== false) return $cached;

    $response = wp_remote_get('https://api.example.com/data', ['timeout' => 5]);
    if (is_wp_error($response) || wp_remote_retrieve_response_code($response) !== 200) {
        $stale = get_option('external_data_fallback', []);
        return $stale; // serve stale data rather than fail
    }

    $data = json_decode(wp_remote_retrieve_body($response), true);
    set_transient('external_data', $data, HOUR_IN_SECONDS);
    update_option('external_data_fallback', $data);
    return $data;
}
```

---

## 11. WordPress Admin UX

### Custom Settings Pages

Match WordPress admin styling. Use the Settings API.

```php
add_action('admin_menu', function() {
    add_options_page('Brand Settings', 'Brand', 'manage_options', 'brand-settings', 'render_brand_settings');
});

add_action('admin_init', function() {
    register_setting('brand_group', 'brand_primary_color', ['sanitize_callback' => 'sanitize_hex_color']);
    add_settings_section('brand_colors', 'Color Settings', null, 'brand-settings');
    add_settings_field('primary_color', 'Primary Color', function() {
        $val = get_option('brand_primary_color', '#1a56db');
        echo '<input type="color" name="brand_primary_color" value="' . esc_attr($val) . '">';
    }, 'brand-settings', 'brand_colors');
});

function render_brand_settings() {
    echo '<div class="wrap"><h1>Brand Settings</h1><form method="post" action="options.php">';
    settings_fields('brand_group');
    do_settings_sections('brand-settings');
    submit_button();
    echo '</form></div>';
}
```

### Admin Notices

```php
// Dismissible success notice
add_action('admin_notices', function() {
    if (!get_transient('brand_saved')) return;
    delete_transient('brand_saved');
    echo '<div class="notice notice-success is-dismissible"><p>Settings saved.</p></div>';
});
```

Use `notice-success`, `notice-error`, `notice-warning`, `notice-info`. Always add `is-dismissible` for non-critical messages.

---

## 12. Performance UX Checklist

Run this checklist before any page is considered complete.

| Metric               | Target          | How to Verify                          |
|----------------------|-----------------|----------------------------------------|
| LCP                  | < 2.5s          | Lighthouse, CrUX, `web-vitals` JS lib |
| CLS                  | < 0.1           | Lighthouse, Layout Instability API     |
| INP                  | < 200ms         | CrUX, `web-vitals` JS lib             |
| Above-fold render    | < 1s            | WebPageTest filmstrip                  |
| Time to Interactive  | < 3s            | Lighthouse                             |
| DOM nodes            | < 1500          | `document.querySelectorAll('*').length`|
| Font display         | No FOIT/FOUT    | Network tab, font-display: swap        |
| Scroll performance   | 60fps           | DevTools Performance panel             |
| Touch response       | < 100ms         | INP measurement                        |
| Image dimensions     | All set         | `img:not([width])` selector audit      |
| Lazy loading         | Below-fold only | Verify first image has no lazy attr    |
| Critical CSS inlined | Above-fold CSS  | View source, check `<style>` in head   |

### Quick Audit Script

```js
// Paste in DevTools console
(() => {
    const imgs = document.querySelectorAll('img:not([width]), img:not([height])');
    const bigDOM = document.querySelectorAll('*').length;
    const noAlt = document.querySelectorAll('img:not([alt])');
    const smallTargets = [...document.querySelectorAll('a, button')].filter(el => {
        const r = el.getBoundingClientRect();
        return r.width < 44 || r.height < 44;
    });
    console.table({
        'Images missing dimensions': imgs.length,
        'DOM nodes': bigDOM,
        'Images missing alt': noAlt.length,
        'Touch targets < 44px': smallTargets.length,
    });
})();
```

---

## Enforcement Rules

When reviewing WordPress code, flag violations of these standards:

1. **No dimensions on images** -- always require width/height attributes
2. **lazy loading on above-fold images** -- first viewport image must not be lazy
3. **Touch targets below 44px** -- buttons and links must meet minimum size
4. **Missing autocomplete attributes on forms** -- all identity/payment fields need them
5. **Spinner instead of skeleton** -- prefer skeleton screens for content regions
6. **Infinite scroll without URL state** -- pagination must preserve browser history
7. **!important in builder overrides** -- use specificity instead
8. **Hardcoded colors instead of CSS custom properties** -- use semantic tokens
9. **Missing error states** -- every async operation needs failure handling
10. **No font-display on @font-face** -- always set font-display: swap
