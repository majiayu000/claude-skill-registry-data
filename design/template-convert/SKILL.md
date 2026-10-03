---
name: template-convert
description: Use when converting monolithic HTML/CSS templates into modular section architectures, replicating designs with 100% visual fidelity from reference images, purging all third-party vendor branding (e.g., Viding), integrating Framer Motion spring animations into standalone vanilla web applications, or creating automated build pipelines for multi-section static templates.
---

# Template Convert

## Overview
A comprehensive engineering methodology to convert web templates (e.g., digital invitations, broadsheets, microsites, landing pages) into ultra-modular, high-performance standalone architectures. It enforces **100% visual fidelity to reference designs**, **complete de-branding and vendor sanitization** (purging third-party platforms like Viding), **Framer Motion spring physics** in vanilla JS/CSS, and an automated modular build pipeline.

```
                    ┌───────────────────────────────┐
                    │ Raw Template / Reference Media│
                    └───────────────┬───────────────┘
                                    │
                    ┌───────────────▼───────────────┐
                    │ 1. Complete De-Branding &     │
                    │    Vendor Sanitization (Zero  │
                    │    Viding / Platform Traces)  │
                    └───────────────┬───────────────┘
                                    │
                    ┌───────────────▼───────────────┐
                    │ 2. 100% Reference Visual      │
                    │    Fidelity Match & Layout    │
                    └───────────────┬───────────────┘
                                    │
                     ┌──────────────┴──────────────┐
                     ▼                             ▼
       ┌───────────────────────────┐ ┌───────────────────────────┐
       │ Modular Section Splitting │ │ Responsive Broadsheet Fix │
       │      (sections/*.html)    │ │   (Desktop + Mobile Fit)  │
       └─────────────┬─────────────┘ └─────────────┬─────────────┘
                     │                             │
                     └──────────────┬──────────────┘
                                    │
                     ┌──────────────▼──────────────┐
                     │ Framer Motion Spring Engine │
                     │  (Observer + CSS Keyframes) │
                     └──────────────┬──────────────┘
                                    │
                     ┌──────────────▼──────────────┐
                     │ Python Compilation Pipeline │
                     │    (build.py -> index.html) │
                     └──────────────┬──────────────┘
                                    │
                     ┌──────────────▼──────────────┐
                     │ Playwright Multi-Viewport QA│
                     └─────────────────────────────┘
```

---

## When to Use
- Converting monolithic or vendor-exported `index.html` files into clean, maintainable modular components (`sections/*.html`).
- **Replicating reference images with 100% visual fidelity** (exact typography, palette, ornaments, spacing, and micro-layouts).
- **Completely stripping vendor branding and identity** (e.g., removing all traces of Viding, watermarks, proprietary CDN links, tracking scripts, and platform logos) to create clean, reusable, white-labeled standalone templates.
- Adding Framer Motion physics-based entrance transitions, scroll reveals, stagger cascades, and micro-interactions to vanilla JavaScript/CSS stacks without React runtime overhead.
- Fixing responsive viewport bugs: eliminating unwanted side whitespace, image shrinking on 1366x768 / 1440x900 laptops, text overflow, and bad mobile aspect ratios.
- Implementing an opening gate/envelope sequence that smoothly unlocks and triggers subsequent animated sections.
- Establishing automated single-command compilation scripts (`build.py`) with zero external dependencies.

---

## 1. Automated Online Asset Downloader & WebP Conversion Pipeline

When converting a live or scraped template, extract all remote media assets, download them locally, convert raster formats to optimized WebP, and replace all remote URLs with clean local relative paths.

### Asset Downloader & WebP Converter Script (`download_assets.py`):
```python
import os
import re
import urllib.request
from PIL import Image

def download_and_convert_assets(source_files, output_img_dir='assets/images', output_font_dir='assets/fonts'):
    os.makedirs(output_img_dir, exist_ok=True)
    os.makedirs(output_font_dir, exist_ok=True)

    url_pattern = r'https?://[^\s"\'\)\<]+'
    found_urls = set()

    for file_path in source_files:
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                matches = re.findall(url_pattern, content)
                for m in matches:
                    if any(m.lower().endswith(ext) or ext in m.lower() for ext in ['.png', '.jpg', '.jpeg', '.webp', '.gif', '.ttf', '.otf', '.woff', '.woff2']):
                        found_urls.add(m)

    print(f"Found {len(found_urls)} remote media URLs to download and process.")

    for url in found_urls:
        try:
            filename = url.split('/')[-1].split('?')[0]
            base, ext = os.path.splitext(filename)
            ext = ext.lower()

            if ext in ['.ttf', '.otf', '.woff', '.woff2']:
                target_path = os.path.join(output_font_dir, filename)
                urllib.request.urlretrieve(url, target_path)
                print(f"Downloaded font: {filename}")
            else:
                raw_path = os.path.join(output_img_dir, f"temp_{filename}")
                urllib.request.urlretrieve(url, raw_path)

                # Convert raster images to WebP
                webp_name = f"{base}.webp"
                webp_path = os.path.join(output_img_dir, webp_name)
                
                with Image.open(raw_path) as im:
                    im.save(webp_path, 'WEBP', quality=85, method=6)
                
                if os.path.exists(raw_path) and raw_path != webp_path:
                    os.remove(raw_path)
                print(f"Converted & Saved WebP: {webp_name}")
        except Exception as e:
            print(f"Failed to process {url}: {e}")

if __name__ == '__main__':
    download_and_convert_assets(['studio.viding.co/index.html'])
```

---

## 2. Standard Workspace Directory Structure

Every converted template MUST adhere to this exact clean, root structure:

```
project_root/
├── assets/
│   ├── css/
│   │   └── style.css            # Core CSS with design tokens & Framer Motion engine
│   ├── fonts/
│   │   └── *.otf / *.ttf        # Localized webfonts (Recoleta, Meow Script, etc.)
│   ├── images/
│   │   └── *.webp               # 100% Optimized, localized WebP assets
│   └── js/
│       ├── app.js               # Global app & UI logic
│       └── framer-animations.js # Spring observer & interaction engine
├── sections/
│   ├── cover.html               # Opening Gate / Hero Cover
│   ├── header.html              # Main Headline & Countdown
│   ├── couple.html              # Bride & Groom Profile
│   ├── story.html               # Timeline / Story Narrative
│   ├── gallery.html             # Media Splide / Carousel Slider
│   ├── venue.html               # Event Cards & Map Modals
│   ├── stream.html              # Embedded Live Player
│   ├── rsvp.html                # Form Confirmation
│   ├── wishes.html              # Interactive Guestbook Feed
│   ├── egift.html               # Gift & Bank Account Registry
│   ├── apology.html             # Courtesy Protocol
│   └── thankyou.html            # Closing & Credits
├── build.py                     # Python SSG compiler
├── handover.md                  # Complete technical hand-off documentation
└── index.html                   # Compiled production artifact
```

> [!IMPORTANT]
> Raw scraped directories (e.g. `studio.viding.co`, `cdn-builder...`, `_DataURI`, `tools/`) MUST be purged after conversion so that only the clean root structure remains.

---

## 3. Complete De-Branding & Vendor Sanitization Protocol

When adapting templates from third-party platforms (such as Viding or proprietary microsite builders), execute a thorough sanitization pass to eliminate all vendor traces and make the codebase 100% generic and clean.

### Sanitization Checklist:
1. **Purge Brand Keywords & Metadata:**
   - Remove all occurrences of `viding`, `studio.viding.co`, `viding-app`, `powered-by`, or any third-party vendor names from:
     - `<title>` and `<meta name="author|description|generator">` tags.
     - Open Graph & Twitter meta tags (`og:site_name`, `og:url`, `og:image`).
     - Favicons and apple-touch-icons (replace with generic template assets).
     - HTML comments, docstrings, and inline metadata.
2. **Purge Proprietary Assets & Watermarks:**
   - Remove platform badges, "Made with...", powered-by footers, or floating watermark overlays.
   - Replace vendor CDN URLs (e.g. `https://assets.viding.co/...` or `https://studio.viding.co/...`) with clean, local relative asset paths (`assets/images/*.webp`, `assets/fonts/*`).
   - Replace proprietary SVG icons/logos with standard open-source equivalents.
3. **Strip Tracking & Platform Scripts:**
   - Remove third-party tracking scripts, analytics pixels, remote error trackers, and platform-specific JS bridges.
   - Eliminate hardcoded proprietary API keys, backend endpoints, and session identifiers.
4. **Normalize DOM & Class Naming:**
   - Rename vendor-prefixed classes (e.g., `.vd-wrapper`, `.viding-container`) to clean, semantic BEM or generic component classes (`.invitation-wrapper`, `.template-container`).

---

## 4. Reference-to-HTML 100% Visual Matching Protocol

The primary objective is achieving a **pixel-accurate 100% visual match** against the target reference image or mockups.

### Step-by-Step Visual Replication:
1. **Visual Breakdown & Design Token Extraction:**
   - **Color Palette:** Extract exact HEX/HSL values for backgrounds, surface tones, text, borders, accents, and overlay gradients. Define them as CSS custom properties in `:root`.
   - **Typography System:** Identify and match exact font families (Google Fonts or local webfonts), weights, `letter-spacing` (tracking), `line-height` (leading), and text transformations (`uppercase`, `italic`, `small-caps`).
   - **Textures & Backgrounds:** Recreate paper textures, grain, borders, ornamental dividers, seals, and botanical/vintage illustrations using CSS overlays or SVG assets.
2. **Layout & Spatial Proportions:**
   - Replicate the exact grid, column splits, margins, paddings, and alignment rules observed in the reference.
   - Maintain the editorial hierarchy: Header, sub-headers, kicker text, dates, quotes, and body copy must match reference sizing proportions.
3. **Aspect Ratios & Framing:**
   - Match exact photo frame styles (arch cuts, newspaper borders, Polaroid cards, oval vignettes).
   - Use `object-fit: cover` and calibrated `object-position` (e.g., `center 20%`) to ensure subjects are never cropped unnaturally.
4. **Visual Comparison Loop:**
   - Compare the rendered output against reference screenshots across standard viewports (Desktop 1920x1080, Laptop 1366x768, Mobile 390x844).
   - Adjust padding, font sizes, line heights, and element alignments until there is zero visual discrepancy.

---

## 5. Modular Section Architecture & Build Pipeline (`build.py`)

```python
import os
import re

sections_order = [
    'cover.html', 'header.html', 'couple.html', 'story.html',
    'gallery.html', 'venue.html', 'stream.html', 'rsvp.html',
    'wishes.html', 'egift.html', 'apology.html', 'thankyou.html'
]

def build():
    combined_body = ""
    for sec_file in sections_order:
        sec_path = os.path.join('sections', sec_file)
        if os.path.exists(sec_path):
            with open(sec_path, 'r', encoding='utf-8') as sf:
                combined_body += f"\n<!-- BEGIN: {sec_file} -->\n" + sf.read().strip() + f"\n<!-- END: {sec_file} -->\n"

    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    new_html = re.sub(r'(<main[^>]*>).*?(</main>)', rf'\1\n{combined_body}\n\2', html, flags=re.DOTALL)
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(new_html)
    print("index.html successfully updated from sections/ directory!")

if __name__ == '__main__':
    build()
```

---

## 4. Framer Motion Vanilla CSS Engine (Text, Image & Physics)

Add GPU-accelerated spring physics, text letterpress reveals, photo entrance dynamics, and stagger definitions directly to `style.css`:

```css
:root {
    --framer-ease: cubic-bezier(0.16, 1, 0.3, 1);
    --framer-spring: cubic-bezier(0.34, 1.56, 0.64, 1);
    --framer-bounce: cubic-bezier(0.68, -0.55, 0.265, 1.55);
    --framer-smooth: cubic-bezier(0.25, 0.8, 0.25, 1);
}

/* Base InView Transitions */
.framer-fade-up, .framer-fade-down, .framer-fade-in,
.framer-scale-up, .framer-zoom-in, .framer-slide-left,
.framer-slide-right, .framer-newspaper-unfold,
.framer-text-focus, .framer-image-reveal {
    opacity: 0;
    will-change: transform, opacity, filter;
    transition-property: transform, opacity, filter;
    transition-duration: 0.85s;
    transition-timing-function: var(--framer-ease);
}

/* Triggered State: InView */
.framer-fade-up.is-visible, .framer-scale-up.is-visible,
.framer-slide-left.is-visible, .framer-slide-right.is-visible,
.framer-newspaper-unfold.is-visible, .framer-text-focus.is-visible,
.framer-image-reveal.is-visible {
    opacity: 1;
    transform: translate3d(0, 0, 0) scale(1) rotate(0);
    filter: blur(0px) contrast(100%) brightness(100%);
}

/* Text Animations: Focus Sharpen & Decorative Line Draw */
.framer-text-focus {
    transform: translate3d(0, 25px, 0);
    filter: blur(6px);
    transition-duration: 0.9s;
}

.is-visible .line, .is-visible .line2 {
    animation: framerLineExpand 0.9s var(--framer-ease) forwards;
}
@keyframes framerLineExpand {
    0% { transform: scaleX(0); opacity: 0; }
    100% { transform: scaleX(1); opacity: 1; }
}

/* Image Animations: Contrast Reveal & Photo Hover Physics */
.framer-image-reveal, .image-wrapper, .np-img-frame {
    transition: transform 0.95s var(--framer-spring), opacity 0.95s ease, filter 0.95s ease;
}
.image-wrapper:hover img, .np-img-frame:hover img {
    transform: scale(1.04) rotate(-0.5deg);
    filter: contrast(108%) brightness(102%);
}

/* Micro-interactions (whileHover / whileTap) */
.framer-btn {
    transition: transform 0.25s var(--framer-spring), box-shadow 0.25s ease;
}
.framer-btn:hover {
    transform: translateY(-3px) scale(1.025);
    box-shadow: 0 12px 28px rgba(0, 0, 0, 0.18);
}
.framer-btn:active {
    transform: translateY(1px) scale(0.96);
}

.framer-card {
    transition: transform 0.35s var(--framer-ease), box-shadow 0.35s ease;
}
.framer-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 14px 30px rgba(0, 0, 0, 0.1);
}

/* Accessibility */
@media (prefers-reduced-motion: reduce) {
    .framer-fade-up, .framer-scale-up, .framer-slide-left,
    .framer-slide-right, .framer-newspaper-unfold,
    .framer-text-focus, .framer-image-reveal, .line, .line2 {
        opacity: 1 !important;
        transform: none !important;
        filter: none !important;
        transition: none !important;
        animation: none !important;
    }
}
```

---

## 5. Framer Motion Observer Engine (`framer-animations.js`)

```javascript
(function () {
  'use strict';

  function initFramerMotion() {
    // 1. IntersectionObserver for viewport scroll triggers
    const observer = new IntersectionObserver(function (entries, obs) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          const el = entry.target;
          el.classList.add('is-visible');

          // Trigger nested framer elements with stagger cascade
          const children = el.querySelectorAll('.framer-fade-up, .framer-scale-up, .framer-slide-left, .framer-slide-right, .framer-newspaper-unfold');
          children.forEach(function (child, idx) {
            setTimeout(function () {
              child.classList.add('is-visible');
            }, idx * 80);
          });

          obs.unobserve(el);
        }
      });
    }, { rootMargin: '0px 0px -50px 0px', threshold: 0.1 });

    document.querySelectorAll('.framer-fade-up, .framer-scale-up, .framer-slide-left, .framer-slide-right, .framer-newspaper-unfold, .main-section, .moveable-section').forEach(function (el) {
      observer.observe(el);
    });

    // 2. Opening Gate Unlock Hook -> Instantly trigger Header Entrance
    const unlockBtn = document.getElementById('btn-envelope');
    if (unlockBtn) {
      unlockBtn.addEventListener('click', function () {
        setTimeout(function () {
          const header = document.querySelector('.header-section');
          if (header) {
            header.classList.add('is-visible');
            header.querySelectorAll('.framer-newspaper-unfold, .framer-fade-up, .framer-scale-up').forEach(function (c, i) {
              setTimeout(function () { c.classList.add('is-visible'); }, i * 100);
            });
          }
        }, 300);
      });
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initFramerMotion);
  } else {
    initFramerMotion();
  }
})();
```

---

## 6. Broadsheet & Fullscreen Layout Rules

### Fullscreen Desktop vs Mobile Responsive Grid
```css
/* Opening Gate Desktop: Broadsheet Split Grid (No Gutters) */
@media (min-width: 992px) {
    .cover-newspaper-paper {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 2.5rem;
        width: 100%;
        min-height: 100vh;
        align-items: stretch;
    }
    
    .np-col-photo {
        display: flex;
        flex-direction: column;
        height: 100%;
        min-height: 0;
    }

    .np-img-frame.np-img-frame-full {
        flex: 1 1 100%;
        width: 100%;
        height: 100%;
        min-height: 520px;
    }

    .np-img-frame.np-img-frame-full img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        object-position: center 20%;
    }
}

/* Mobile Viewport: Single Stack */
@media (max-width: 991.98px) {
    .cover-newspaper-paper {
        display: flex;
        flex-direction: column;
        width: 100%;
    }
    
    .np-img-frame.np-img-frame-full {
        width: 100%;
        aspect-ratio: 4 / 3;
    }
}
```

---

## 7. Playwright Verification Protocol

Always execute automated visual and console verification across multiple viewports:
```python
import asyncio
from playwright.async_api import async_playwright

async def verify_template():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        
        # Test Laptop (1366x768), Desktop (1920x1080), Mobile (390x844)
        viewports = [
            {"width": 1366, "height": 768, "name": "laptop"},
            {"width": 1920, "height": 1080, "name": "desktop"},
            {"width": 390, "height": 844, "name": "mobile"}
        ]
        
        for vp in viewports:
            page = await browser.new_page(viewport={"width": vp["width"], "height": vp["height"]})
            errors = []
            page.on("pageerror", lambda err: errors.append(str(err)))
            await page.goto("file:///path/to/index.html", wait_until="networkidle")
            
            # Click Unlock Button
            await page.click("#btn-envelope")
            await page.wait_for_timeout(800)
            
            # Scroll & check errors
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await page.wait_for_timeout(1000)
            
            assert len(errors) == 0, f"Errors found on {vp['name']}: {errors}"
            print(f"Viewport {vp['name']} verified successfully.")
            
        await browser.close()

if __name__ == '__main__':
    asyncio.run(verify_template())
```

---

## 8. Common Mistakes & Solutions

| Anti-Pattern | Root Cause | Solution |
|---|---|---|
| **Remaining vendor links or branding (e.g., Viding)** | Incomplete sanitization of meta tags, external CDNs, or badge footers | Grep for `viding`, `studio.viding`, `powered-by`, and replace all remote URLs with local generic assets |
| **Visual discrepancy from reference image** | Using standard browser typography & arbitrary spacing instead of extracting tokens from reference | Extract exact HEX codes, font weights, letter-spacing, line-height, and ornamental borders from the reference |
| **Image shrinks to corner on laptop (1366x768)** | Parent flex container has `align-items: center` and child lacks `min-height: 0` | Use `flex: 1 1 100%; width: 100%; height: 100%; object-fit: cover;` |
| **Animations don't fire when opening gate unlocks** | Sections below cover are initially hidden from observer rootMargin | Add unlock event listener on `#btn-envelope` to explicitly trigger header entrance |
| **Monolithic changes break compiled file** | Direct edits made to `index.html` instead of `sections/` | Edit only in `sections/*.html` and always run `python build.py` |
| **Image cropping cuts essential subject faces** | Default `object-position: center center` cuts top heads in portrait/landscape mismatches | Use `object-position: center 20%` to keep faces and focal points perfectly framed |

