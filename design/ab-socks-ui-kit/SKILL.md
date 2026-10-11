---
name: ab-socks-ui-kit
description: >
  Protocol and catalog for reusing and authoring frontend components, JavaScript utilities,
  and CSS design tokens in the AB-Socks admin panel. Load this skill whenever writing or
  modifying admin UI, forms, tables, modals, autocomplete/search fields, toasts, image uploaders,
  or CSS styling. Enforces the Reuse-First protocol, declarative data-ab-* usage, and zero
  inline script bloat.
---

# AB-Socks UI & Component Kit Skill

This skill enforces the **Reuse-First Protocol (`AGENTS.md` Rule 11)** and guides the
consumption and creation of reusable UI components in the AB-Socks project.

---

## 1. Golden Rules for Front-end Development

1. **Check `docs/COMPONENTS.md` First**: Before writing any new UI interaction, formatter, modal, search field, or component, look up existing implementations.
2. **Zero Duplicate Helpers**: Never re-declare functions like `showToast`, `escapeHtml`, `formatBytes`, `toFaDigits`, `toPersianDigits`, or custom debounce listeners.
3. **Declarative Views (`data-ab-*`)**: Admin views must **never** contain heavy inline `<script>` tags (hard limit 20 lines). UI behavior is driven by HTML data-attributes (`data-ab-*`) or external registered scripts.
4. **CSS Token Single Source of Truth**: Colors and design tokens must strictly reference `:root` CSS variables in `admin.css`. Individual page stylesheets must never declare competing `:root` palettes or hardcode raw `#hex` values.
5. **The Rule of Two**: If interaction logic or a UI pattern is needed in ≥ 2 places, extract it to a shared component and register it in `docs/COMPONENTS.md`.

---

## 2. Standard Interaction Patterns

### 2.1 Displaying Notifications & Toasts
Use the global helper from `assets/js/admin.js`:
```javascript
showToast('تغییرات با موفقیت ذخیره شد.', 'success');
showToast('خطا در پردازش اطلاعات.', 'error');
```
*Never write a page-specific `showToast()` function.*

### 2.2 Modals & Overlays
Use native `<dialog>` or declarative modal attributes:
```html
<button type="button" class="btn btn-secondary" data-ab-modal-open="myModal">باز کردن</button>

<div id="myModal" class="admin-modal" data-ab-modal hidden>
    <div class="admin-modal-backdrop" data-ab-modal-close></div>
    <div class="admin-modal-content">
        <header class="admin-modal-header">
            <h3>عنوان</h3>
            <button type="button" class="btn-close" data-ab-modal-close aria-label="بستن"></button>
        </header>
        <div class="admin-modal-body">...</div>
    </div>
</div>
```

### 2.3 Autocomplete & Tokenizer Fields
For product search, tag selection, or customer search:
```html
<div class="ab-autocomplete" data-ab-autocomplete="products" data-ab-multiple="false">
    <input type="text" class="form-input" placeholder="جست‌وجوی محصول..." autocomplete="off">
    <div class="ab-autocomplete-suggestions" hidden></div>
</div>
```
Backend queries are routed centrally through `ajax/admin_search.php?type=products&q=...`.

### 2.4 Live Table Filtering
To filter a table live on keyup:
```html
<input type="search" class="form-input" placeholder="فیلتر..." data-ab-filter-target="#dataTable">
<table id="dataTable">
    <tbody>
        <tr data-search="کد 1001 جوراب مشکی">...</tr>
    </tbody>
</table>
```

### 2.5 Image Upload & Optimization
Offload image processing to the client browser via `assets/js/admin-image-optimizer.js`:
```html
<input type="file" name="image" accept="image/*" data-optimize-image class="aio-input">
```
Handles client-side WebP conversion, HEIC decoding, EXIF stripping, and visual zoom/pan inspection automatically.

---

## 3. Pre-Commit Checklist for UI Changes
- [ ] No inline `<script>` tag in any view exceeds 20 lines.
- [ ] No duplicate JS helper was created (checked `docs/COMPONENTS.md`).
- [ ] No page-specific `:root` block was added to any CSS file.
- [ ] All colors reference `var(--color-...)`.
- [ ] `php tools/verify.php` passes with 0 errors and satisfies the ratchet baseline.
