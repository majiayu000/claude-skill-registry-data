---
name: responsive-images
description: Modern responsive image techniques using picture element, srcset, sizes, and modern formats. Use when adding images that need to adapt to different screen sizes, resolutions, or support modern image formats.
allowed-tools: Read, Write, Edit
---

# Responsive Images Skill

This skill covers modern responsive image techniques: resolution switching with `srcset` and `sizes`, art direction with `<picture>`, and modern format support with graceful fallbacks.

## Philosophy

Images should:
1. **Serve optimal files** - Right size for the display context
2. **Use modern formats** - AVIF, WebP with JPEG/PNG fallback
3. **Prioritize correctly** - LCP images load first, others lazy load
4. **Work everywhere** - Fallbacks for older browsers

---

## The Image Loading Attributes

Every image should have appropriate loading attributes:

```html
<img src="photo.jpg"
     alt="Descriptive text"
     loading="lazy"
     decoding="async"
     fetchpriority="auto"/>
```

### Attribute Reference

| Attribute | Values | Purpose |
|-----------|--------|---------|
| `loading` | `eager`, `lazy` | When to load the image |
| `decoding` | `sync`, `async`, `auto` | How to decode the image |
| `fetchpriority` | `high`, `low`, `auto` | Network priority hint |

### Loading Strategy by Context

| Image Type | `loading` | `fetchpriority` | `decoding` |
|------------|-----------|-----------------|------------|
| Hero/LCP image | `eager` | `high` | `async` |
| Above fold | `eager` | `auto` | `async` |
| Below fold | `lazy` | `auto` | `async` |
| Thumbnails | `lazy` | `low` | `async` |
| Background decorative | `lazy` | `low` | `async` |

---

## Resolution Switching with `srcset` and `sizes`

### The Problem

A single image file can't serve all contexts:
- A 2000px image wastes bandwidth on mobile
- A 400px image looks blurry on retina displays
- Screen size and pixel density vary widely

### The Solution: `srcset` and `sizes`

```html
<img src="photo-800.jpg"
     srcset="photo-400.jpg 400w,
             photo-800.jpg 800w,
             photo-1200.jpg 1200w,
             photo-1600.jpg 1600w"
     sizes="(max-width: 600px) 100vw,
            (max-width: 1200px) 50vw,
            800px"
     alt="Product photograph"
     loading="lazy"
     decoding="async"/>
```

### How It Works

1. **`srcset`** lists available image files with their widths (`w` descriptor)
2. **`sizes`** tells the browser how wide the image will display
3. Browser calculates optimal file based on viewport + pixel density
4. **`src`** provides fallback for browsers without `srcset` support

### The `sizes` Attribute

`sizes` uses media conditions to describe rendered width:

```html
sizes="(max-width: 600px) 100vw,
       (max-width: 1200px) 50vw,
       800px"
```

This means:
- At 600px viewport or less: image displays at 100% viewport width
- At 601-1200px viewport: image displays at 50% viewport width
- Above 1200px: image displays at 800px fixed width

### Common `sizes` Patterns

| Context | `sizes` Value |
|---------|---------------|
| Full-width hero | `100vw` |
| Content image (max 800px) | `(max-width: 800px) 100vw, 800px` |
| Two-column grid | `(max-width: 600px) 100vw, 50vw` |
| Three-column grid | `(max-width: 600px) 100vw, (max-width: 900px) 50vw, 33vw` |
| Card thumbnail | `(max-width: 600px) 100vw, 300px` |
| Gallery thumbnail | `(max-width: 600px) 50vw, 220px` |

---

## Art Direction with `<picture>`

### When to Use `<picture>`

Use `<picture>` when you need **different images** for different contexts:
- Different crops (portrait mobile, landscape desktop)
- Different aspect ratios
- Showing/hiding details at different sizes
- Different content entirely

### Basic Art Direction

```html
<picture>
  <source media="(max-width: 600px)"
          srcset="photo-mobile.jpg"/>
  <source media="(max-width: 1200px)"
          srcset="photo-tablet.jpg"/>
  <img src="photo-desktop.jpg"
       alt="Product photograph"
       loading="lazy"
       decoding="async"/>
</picture>
```

### Art Direction with `srcset`

Combine art direction with resolution switching:

```html
<picture>
  <!-- Mobile: portrait crop -->
  <source media="(max-width: 600px)"
          srcset="photo-mobile-400.jpg 400w,
                  photo-mobile-600.jpg 600w"
          sizes="100vw"/>

  <!-- Tablet: square crop -->
  <source media="(max-width: 1200px)"
          srcset="photo-tablet-600.jpg 600w,
                  photo-tablet-900.jpg 900w"
          sizes="50vw"/>

  <!-- Desktop: landscape crop -->
  <img src="photo-desktop-800.jpg"
       srcset="photo-desktop-800.jpg 800w,
               photo-desktop-1200.jpg 1200w,
               photo-desktop-1600.jpg 1600w"
       sizes="800px"
       alt="Product photograph"
       loading="lazy"
       decoding="async"/>
</picture>
```

---

## Modern Image Formats

### Format Comparison

| Format | Compression | Browser Support | Use Case |
|--------|-------------|-----------------|----------|
| AVIF | Best (50% smaller than JPEG) | Chrome, Firefox, Safari 16+ | Primary modern format |
| WebP | Very good (25-35% smaller) | All modern browsers | Fallback for AVIF |
| JPEG | Good | Universal | Final fallback |
| PNG | Lossless | Universal | Transparency, screenshots |

### Format Fallback Pattern

```html
<picture>
  <source srcset="photo.avif" type="image/avif"/>
  <source srcset="photo.webp" type="image/webp"/>
  <img src="photo.jpg"
       alt="Descriptive text"
       loading="lazy"
       decoding="async"/>
</picture>
```

### Complete Pattern: Formats + Resolution + Art Direction

```html
<picture>
  <!-- Mobile: AVIF -->
  <source media="(max-width: 600px)"
          type="image/avif"
          srcset="photo-mobile-400.avif 400w,
                  photo-mobile-600.avif 600w"
          sizes="100vw"/>

  <!-- Mobile: WebP -->
  <source media="(max-width: 600px)"
          type="image/webp"
          srcset="photo-mobile-400.webp 400w,
                  photo-mobile-600.webp 600w"
          sizes="100vw"/>

  <!-- Mobile: JPEG -->
  <source media="(max-width: 600px)"
          srcset="photo-mobile-400.jpg 400w,
                  photo-mobile-600.jpg 600w"
          sizes="100vw"/>

  <!-- Desktop: AVIF -->
  <source type="image/avif"
          srcset="photo-800.avif 800w,
                  photo-1200.avif 1200w"
          sizes="(max-width: 1200px) 50vw, 800px"/>

  <!-- Desktop: WebP -->
  <source type="image/webp"
          srcset="photo-800.webp 800w,
                  photo-1200.webp 1200w"
          sizes="(max-width: 1200px) 50vw, 800px"/>

  <!-- Desktop: JPEG fallback -->
  <img src="photo-800.jpg"
       srcset="photo-800.jpg 800w,
               photo-1200.jpg 1200w"
       sizes="(max-width: 1200px) 50vw, 800px"
       alt="Descriptive text"
       loading="lazy"
       decoding="async"/>
</picture>
```

---

## Common Image Patterns

### Hero Image (LCP)

```html
<picture>
  <source type="image/avif"
          srcset="hero-800.avif 800w,
                  hero-1200.avif 1200w,
                  hero-1920.avif 1920w"
          sizes="100vw"/>
  <source type="image/webp"
          srcset="hero-800.webp 800w,
                  hero-1200.webp 1200w,
                  hero-1920.webp 1920w"
          sizes="100vw"/>
  <img src="hero-1200.jpg"
       srcset="hero-800.jpg 800w,
               hero-1200.jpg 1200w,
               hero-1920.jpg 1920w"
       sizes="100vw"
       alt="Hero image description"
       loading="eager"
       fetchpriority="high"
       decoding="async"/>
</picture>
```

### Content Image

```html
<picture>
  <source type="image/avif"
          srcset="content-400.avif 400w,
                  content-800.avif 800w,
                  content-1200.avif 1200w"
          sizes="(max-width: 800px) 100vw, 800px"/>
  <source type="image/webp"
          srcset="content-400.webp 400w,
                  content-800.webp 800w,
                  content-1200.webp 1200w"
          sizes="(max-width: 800px) 100vw, 800px"/>
  <img src="content-800.jpg"
       srcset="content-400.jpg 400w,
               content-800.jpg 800w,
               content-1200.jpg 1200w"
       sizes="(max-width: 800px) 100vw, 800px"
       alt="Content image description"
       loading="lazy"
       decoding="async"/>
</picture>
```

### Card Thumbnail

```html
<picture>
  <source type="image/avif"
          srcset="thumb-300.avif 300w,
                  thumb-450.avif 450w"
          sizes="(max-width: 600px) 100vw, 300px"/>
  <source type="image/webp"
          srcset="thumb-300.webp 300w,
                  thumb-450.webp 450w"
          sizes="(max-width: 600px) 100vw, 300px"/>
  <img src="thumb-300.jpg"
       srcset="thumb-300.jpg 300w,
               thumb-450.jpg 450w"
       sizes="(max-width: 600px) 100vw, 300px"
       alt="Card thumbnail description"
       loading="lazy"
       decoding="async"/>
</picture>
```

### Gallery Image

```html
<picture>
  <source type="image/avif"
          srcset="gallery-220.avif 220w,
                  gallery-330.avif 330w,
                  gallery-440.avif 440w"
          sizes="(max-width: 600px) 50vw, 220px"/>
  <source type="image/webp"
          srcset="gallery-220.webp 220w,
                  gallery-330.webp 330w,
                  gallery-440.webp 440w"
          sizes="(max-width: 600px) 50vw, 220px"/>
  <img src="gallery-220.jpg"
       srcset="gallery-220.jpg 220w,
               gallery-330.jpg 330w,
               gallery-440.jpg 440w"
       sizes="(max-width: 600px) 50vw, 220px"
       alt="Gallery image description"
       loading="lazy"
       decoding="async"/>
</picture>
```

---

## Simplified Patterns

### When Full `<picture>` Is Overkill

For simpler cases, `srcset` alone may suffice:

```html
<!-- Resolution switching only, no format variants -->
<img src="photo-800.jpg"
     srcset="photo-400.jpg 400w,
             photo-800.jpg 800w,
             photo-1200.jpg 1200w"
     sizes="(max-width: 600px) 100vw, 50vw"
     alt="Description"
     loading="lazy"
     decoding="async"/>
```

### Minimum Viable Responsive Image

At minimum, always include:

```html
<img src="photo.jpg"
     alt="Descriptive text"
     loading="lazy"
     decoding="async"
     width="800"
     height="600"/>
```

The `width` and `height` attributes prevent layout shift.

---

## Image Sizing Strategy

### Images in Container-Queried Components

The HTML `sizes` attribute uses **viewport** media queries, not container queries. For images inside container-queried components, the `sizes` may not accurately describe rendered width.

**Strategies:**

1. **Generous `sizes` estimation** - Provide srcset that covers the full range:

```html
<!-- Inside a container-queried card that could be 300-800px wide -->
<img srcset="photo-300.jpg 300w,
             photo-450.jpg 450w,
             photo-600.jpg 600w,
             photo-800.jpg 800w"
     sizes="(max-width: 600px) 100vw, 800px"
     alt="Product photo"/>
```

2. **CSS-controlled sizing** - Let CSS and container queries control the rendered size:

```css
@layer components {
  product-card {
    container-type: inline-size;
  }

  product-card img {
    width: 100%;
    height: auto;
    aspect-ratio: 4/3;
    object-fit: cover;
  }

  @container (min-width: 500px) {
    product-card img {
      width: 40%;
    }
  }
}
```

The browser still selects from `srcset` based on rendered size after CSS is applied.

3. **Use `object-fit` with container units** for fluid sizing:

```css
product-card img {
  width: min(100%, 20cqi);
  aspect-ratio: 1;
  object-fit: cover;
}
```

**Note:** Future CSS may support container-based image selection, but for now, provide a robust `srcset` range.

### Standard Breakpoints for `srcset`

Generate images at these widths to cover common scenarios:

| Width | Use Case |
|-------|----------|
| 400w | Mobile thumbnails |
| 600w | Mobile full-width |
| 800w | Tablet/small desktop |
| 1200w | Desktop content |
| 1600w | Large desktop/retina |
| 1920w | Full-width heroes |

### Calculating `sizes`

1. **Measure rendered width** at key breakpoints
2. **Use viewport units** (`vw`) for fluid images
3. **Use fixed pixels** for constrained images
4. **Order conditions** from narrowest to widest

---

## Accessibility

### Alt Text Requirements

Every image needs meaningful `alt` text:

```html
<!-- Informative: describe the content -->
<img alt="Team members collaborating around a whiteboard"/>

<!-- Decorative: empty alt -->
<img alt="" role="presentation"/>

<!-- Functional: describe the action -->
<img alt="Search"/>
```

### Avoid Redundant Alt Text

```html
<!-- Bad: redundant with adjacent text -->
<figure>
  <img alt="Photo of our office building"/>
  <figcaption>Our office building in Seattle</figcaption>
</figure>

<!-- Good: complementary description -->
<figure>
  <img alt="Modern glass-walled building with green roof"/>
  <figcaption>Our office building in Seattle</figcaption>
</figure>
```

---

## Checklist

When adding images:

- [ ] Include `alt` attribute (descriptive or empty for decorative)
- [ ] Add `loading` attribute (`eager` for LCP, `lazy` for others)
- [ ] Add `decoding="async"` for all images
- [ ] Add `fetchpriority="high"` for LCP/hero images
- [ ] Include `width` and `height` to prevent layout shift
- [ ] Use `srcset` for resolution switching when image > 400px
- [ ] Calculate appropriate `sizes` based on rendered width
- [ ] Use `<picture>` for format fallbacks (AVIF > WebP > JPEG)
- [ ] Use `<picture>` for art direction (different crops)
- [ ] Test with network throttling to verify lazy loading

## Related Skills

- **images** - Umbrella coordinator for image handling with automation
- **css-author** - Container queries for component-scoped image sizing
- **performance** - Write performance-friendly HTML pages
- **xhtml-author** - Write valid XHTML-strict HTML5 markup
- **placeholder-images** - Generate SVG placeholder images for prototypes
