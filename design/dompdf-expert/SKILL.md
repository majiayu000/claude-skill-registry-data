---
name: dompdf-expert
description: |
  Expert guide for generating beautiful, professional PDFs with DomPDF (barryvdh/laravel-dompdf) in the KLASSCI Laravel project.

  USE THIS SKILL whenever the user asks to:
  - Create or modify a PDF template (bulletin, certificate, report, attendance, timetable, payment export, etc.)
  - Fix a PDF that doesn't look right (missing images, colors, layout broken, fonts wrong)
  - Match a PDF output to the web preview seen in the application
  - Export any data to PDF format
  - Improve PDF design, spacing, or typography
  - Debug DomPDF rendering issues
  - Add headers, footers, or page numbers to a PDF
  - Any task involving Blade views in resources/views/esbtp/*/pdf*, resources/views/pdf/, or any view loaded via PDF::loadView()
---

# DomPDF Expert — KLASSCI

You are a DomPDF expert working in the KLASSCI Laravel project. This skill gives you everything needed to produce professional, pixel-perfect PDFs on the first try.

## 1. Project Overview

**Package:** `barryvdh/laravel-dompdf` v2.0
**PDF templates location:** `resources/views/esbtp/*/` (filename contains `pdf`) and `resources/views/pdf/`
**Centralized theme:** `resources/views/pdf/partials/theme.blade.php` — always `@include` this in new templates
**Settings helper:** `App\Helpers\SettingsHelper::getPdfSettings()` — use for colors, margins, fonts
**Design palette:** `#0453cb` (primary blue), `#64748b` (secondary gray), `#f59e0b` (accent amber), `#1f2937` (text dark)
**Standard controller method:**
```php
use Barryvdh\DomPDF\Facade\Pdf;

$pdf = Pdf::loadView('esbtp.xxx.pdf-xxx', compact('data'))
    ->setPaper('a4', 'portrait')
    ->setOptions([
        'dpi' => 150,
        'defaultFont' => 'sans-serif',
        'isRemoteEnabled' => false,
        'isHtml5ParserEnabled' => true,
        'isPhpEnabled' => false,
        'isFontSubsettingEnabled' => true,
    ]);
return $pdf->download('filename.pdf');
```

---

## 2. DomPDF CSS Cheat Sheet — What Works vs What Doesn't

### ✅ SUPPORTED (Use freely)
| Feature | Notes |
|---------|-------|
| `background-color` on `<td>` | Works — apply to td, NOT tr (see §6) |
| `border`, `border-collapse` | Full support |
| `padding`, `margin` | Full support |
| `font-size`, `font-weight`, `font-style` | Full support |
| `text-align`, `vertical-align` | Full support |
| `width`, `height` in px/mm/% | Full support |
| `@page` (margins, size) | Full support |
| `page-break-before/after/inside` | Full support |
| `:nth-child()`, `:first-child` | Full support |
| `@font-face` with `.ttf` | Full support with storage_path() |
| `border-radius` | Supported (CSS3 partial) |
| `opacity` | Supported |
| `display: block/inline/table` | Full support |
| `position: fixed` (for headers/footers) | Full support |
| `letter-spacing`, `line-height` | Full support |

### ❌ NOT SUPPORTED — Never use these in PDF templates
| Feature | Alternative |
|---------|-------------|
| `display: flex` / `flexbox` | **Use `<table>` layout** |
| `display: grid` | **Use `<table>` layout** |
| `transform` (rotate, translate) | Not available |
| CSS animations / transitions | Not available |
| `box-shadow` | Use `border` instead |
| `backdrop-filter`, `clip-path` | Not available |
| Bootstrap 4+ classes | Write plain CSS |
| Tailwind CSS classes | Write plain CSS |
| Media queries | Not applicable in PDF |
| `float` layouts | Unreliable across pages — use tables |
| External `<link>` CSS (relative URLs) | Use inline `<style>` or `public_path()` |
| `asset()` helper for images | Use `public_path()` or base64 |

---

## 3. Standard KLASSCI PDF Template Structure

Every new PDF template must follow this structure:

```blade
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <title>{{ $title ?? 'Document' }}</title>
    <style>
        /* ── Reset ── */
        * { margin: 0; padding: 0; box-sizing: border-box; }

        body {
            font-family: DejaVu Sans, Arial, sans-serif;
            font-size: {{ $settings['font_size'] ?? 12 }}px;
            color: {{ $settings['text_color'] ?? '#1f2937' }};
            line-height: 1.45;
            background: #ffffff;
        }

        /* ── Page setup ── */
        @page {
            margin: {{ $settings['margin_top'] ?? 15 }}mm
                    {{ $settings['margin_right'] ?? 10 }}mm
                    {{ $settings['margin_bottom'] ?? 15 }}mm
                    {{ $settings['margin_left'] ?? 10 }}mm;
        }

        /* ── Typography ── */
        h1 { font-size: 18px; color: {{ $settings['primary_color'] ?? '#0453cb' }}; margin-bottom: 8px; }
        h2 { font-size: 15px; color: {{ $settings['primary_color'] ?? '#0453cb' }}; margin-bottom: 6px; }
        h3 { font-size: 13px; color: #374151; margin-bottom: 4px; }

        /* ── Tables ── */
        table { width: 100%; border-collapse: collapse; }

        /* ── Utilities ── */
        .text-right { text-align: right; }
        .text-center { text-align: center; }
        .text-muted { color: #6b7280; font-size: 10px; }
        .bold { font-weight: bold; }
        .mt-8 { margin-top: 8px; }
        .mt-16 { margin-top: 16px; }
        .mb-8 { margin-bottom: 8px; }
        .mb-16 { margin-bottom: 16px; }
        .page-break { page-break-before: always; }
        .no-break { page-break-inside: avoid; }
    </style>
</head>
<body>

    {{-- ── HEADER ── --}}
    @include('pdf.partials.header', ['settings' => $settings, 'logoBase64' => $logoBase64 ?? null])

    {{-- ── MAIN CONTENT ── --}}
    <div style="margin-top: 16px;">
        {{-- Your content here --}}
    </div>

    {{-- ── FOOTER ── --}}
    @include('pdf.partials.footer', ['settings' => $settings])

</body>
</html>
```

### Using the centralized theme override
```blade
{{-- After your <style> block, add: --}}
@include('pdf.partials.theme')
{{-- This injects KLASSCI brand colors from SettingsHelper, overriding any hardcoded values --}}
```

---

## 4. KLASSCI Settings System

### Load settings in your controller
```php
// Standard PDF settings (colors, margins, fonts, logo)
$pdfSettings = \App\Helpers\SettingsHelper::getPdfSettings();

// Pass to view
$pdf = Pdf::loadView('esbtp.xxx.pdf', [
    'settings' => $pdfSettings,
    'logoBase64' => $this->prepareLogoBase64($pdfSettings['logo'] ?? null),
    // ... other data
]);
```

### Available settings keys
```php
// Colors
$settings['primary_color']     // default: '#0453cb'
$settings['secondary_color']   // default: '#64748b'
$settings['accent_color']      // default: '#f59e0b'
$settings['text_color']        // default: '#1f2937'
$settings['header_bg_color']   // default: '#0453cb'
$settings['header_text_color'] // default: '#ffffff'

// Margins (mm)
$settings['margin_top']        // default: 20
$settings['margin_bottom']     // default: 20
$settings['margin_left']       // default: 15
$settings['margin_right']      // default: 15

// Typography
$settings['font_size']         // default: 12

// Branding
$settings['show_logo']         // boolean
$settings['logo_position']     // 'left' | 'center' | 'right'
$settings['header_text']       // custom header text
$settings['footer_text']       // custom footer text
$settings['signature_director']
$settings['signature_secretary']
$settings['watermark']
```

---

## 5. Layout Patterns — Tables Only (No Flexbox)

### 2-column layout
```blade
<table width="100%" border="0" cellspacing="0" cellpadding="0">
    <tr>
        <td width="48%" style="vertical-align: top; padding-right: 8px;">
            {{-- Left column content --}}
        </td>
        <td width="4%"></td>{{-- spacer --}}
        <td width="48%" style="vertical-align: top; padding-left: 8px;">
            {{-- Right column content --}}
        </td>
    </tr>
</table>
```

### 3-column layout
```blade
<table width="100%" border="0" cellspacing="0" cellpadding="0">
    <tr>
        <td width="32%" style="vertical-align: top; padding-right: 6px;">Col 1</td>
        <td width="2%"></td>
        <td width="32%" style="vertical-align: top; padding: 0 6px;">Col 2</td>
        <td width="2%"></td>
        <td width="32%" style="vertical-align: top; padding-left: 6px;">Col 3</td>
    </tr>
</table>
```

### Info card (bordered box)
```blade
<table width="100%" border="0" cellspacing="0" cellpadding="0"
       style="border: 1px solid #d1d5db; border-radius: 6px; margin-bottom: 12px;">
    <tr>
        <td style="background-color: {{ $settings['primary_color'] ?? '#0453cb' }};
                   color: #ffffff;
                   padding: 8px 12px;
                   font-weight: bold;
                   font-size: 12px;
                   border-radius: 6px 6px 0 0;">
            {{ $cardTitle }}
        </td>
    </tr>
    <tr>
        <td style="padding: 12px; background-color: #f9fafb;">
            {{-- Card content --}}
        </td>
    </tr>
</table>
```

### Key-value info row
```blade
<table width="100%" border="0" cellspacing="0" cellpadding="4">
    <tr>
        <td width="35%" style="color: #6b7280; font-size: 11px;">Nom :</td>
        <td width="65%" style="font-weight: bold; font-size: 11px;">{{ $etudiant->nom_complet }}</td>
    </tr>
    <tr>
        <td style="color: #6b7280; font-size: 11px;">Matricule :</td>
        <td style="font-size: 11px;">{{ $etudiant->matricule }}</td>
    </tr>
</table>
```

---

## 6. Table Styling — The Critical `tr→td` Fix

**The most common DomPDF bug:** background-color on `<tr>` doesn't render. Always target `<td>` instead.

```blade
<style>
    /* ❌ WRONG — background won't appear */
    .header-row { background-color: #0453cb; }

    /* ✅ CORRECT — target td directly */
    .header-row td {
        background-color: {{ $settings['header_bg_color'] ?? '#0453cb' }};
        color: {{ $settings['header_text_color'] ?? '#ffffff' }};
        padding: 10px 12px;
        font-weight: bold;
        font-size: 11px;
        border-bottom: 2px solid #0343ab;
    }

    /* ✅ ALSO CORRECT — inline style on td */
    /* <td style="background-color: #0453cb; color: white;"> */

    /* Alternating rows (zebra striping) */
    .data-row-even td { background-color: #f9fafb; }
    .data-row-odd td  { background-color: #ffffff; }

    /* Hover effect (static in PDF — use for nth-child instead) */
    tbody tr:nth-child(even) td { background-color: #f3f4f6; }
    tbody tr:nth-child(odd) td  { background-color: #ffffff; }
</style>

<table style="width: 100%; border-collapse: collapse; margin-bottom: 16px;">
    <thead>
        <tr class="header-row">
            <td>Matière</td>
            <td class="text-center">Note /20</td>
            <td class="text-center">Coeff.</td>
            <td class="text-right">Moyenne</td>
        </tr>
    </thead>
    <tbody>
        @foreach($resultats as $i => $resultat)
        <tr class="{{ $i % 2 === 0 ? 'data-row-even' : 'data-row-odd' }}">
            <td style="padding: 8px 12px; border-bottom: 1px solid #e5e7eb;">
                {{ $resultat->matiere->name }}
            </td>
            <td style="padding: 8px 12px; border-bottom: 1px solid #e5e7eb; text-align: center;">
                {{ number_format($resultat->note, 2) }}
            </td>
            <td style="padding: 8px 12px; border-bottom: 1px solid #e5e7eb; text-align: center;">
                {{ $resultat->coefficient }}
            </td>
            <td style="padding: 8px 12px; border-bottom: 1px solid #e5e7eb; text-align: right; font-weight: bold;">
                {{ number_format($resultat->moyenne, 2) }}
            </td>
        </tr>
        @endforeach
    </tbody>
    <tfoot>
        <tr>
            <td colspan="3" style="padding: 10px 12px; background-color: #f3f4f6; font-weight: bold; border-top: 2px solid #d1d5db;">
                Moyenne Générale
            </td>
            <td style="padding: 10px 12px; background-color: #f3f4f6; font-weight: bold; text-align: right; border-top: 2px solid #d1d5db; color: #0453cb;">
                {{ number_format($moyenneGenerale, 2) }} / 20
            </td>
        </tr>
    </tfoot>
</table>
```

---

## 7. Typography & Fonts

### Built-in fonts (use without any setup)
- `DejaVu Sans` — **Best choice for French text** (handles accents: é, è, à, ç, ê)
- `DejaVu Serif`
- `DejaVu Sans Mono` (for code/fixed-width)
- `Arial`, `Helvetica` (basic, limited character set)
- `Times New Roman`, `Courier` (base 14)

**Always use `DejaVu Sans` for French documents:**
```css
body {
    font-family: DejaVu Sans, Arial, sans-serif;
}
```

### Custom font via @font-face (if needed)
```blade
<style>
    @font-face {
        font-family: 'CustomFont';
        font-weight: normal;
        font-style: normal;
        src: url("{{ storage_path('fonts/CustomFont-Regular.ttf') }}") format('truetype');
    }
    @font-face {
        font-family: 'CustomFont';
        font-weight: bold;
        src: url("{{ storage_path('fonts/CustomFont-Bold.ttf') }}") format('truetype');
    }
    body { font-family: 'CustomFont', DejaVu Sans, sans-serif; }
</style>
```

### Typography scale (KLASSCI standard)
```css
.pdf-h1     { font-size: 20px; font-weight: bold; color: #0453cb; }
.pdf-h2     { font-size: 16px; font-weight: bold; color: #0453cb; }
.pdf-h3     { font-size: 13px; font-weight: bold; color: #374151; }
.pdf-body   { font-size: 11px; line-height: 1.5; }
.pdf-small  { font-size: 9px; color: #6b7280; }
.pdf-label  { font-size: 10px; color: #6b7280; text-transform: uppercase; letter-spacing: 0.5px; }
```

---

## 8. Images & Logos — Always Base64 or public_path()

**The golden rule:** `asset()` generates relative URLs that DomPDF cannot resolve. Use `public_path()` for file system paths or encode images as base64.

### In controller — prepare base64 logo
```php
private function prepareLogoBase64(?string $logoPath): ?string
{
    // Priority list of paths to try
    $paths = [
        $logoPath ? storage_path('app/public/' . $logoPath) : null,
        public_path('images/logo.png'),
        public_path('images/esbtp_logo.png'),
        public_path('images/logo.jpeg'),
    ];

    foreach (array_filter($paths) as $path) {
        if (file_exists($path)) {
            $mime = mime_content_type($path);
            $data = base64_encode(file_get_contents($path));
            return "data:{$mime};base64,{$data}";
        }
    }
    return null;
}

private function preparePhotoBase64(?string $photoPath): ?string
{
    if (!$photoPath) return null;

    $fullPath = storage_path('app/public/' . $photoPath);
    if (!file_exists($fullPath)) return null;

    // Convert to JPEG for best PDF compatibility
    $image = imagecreatefromstring(file_get_contents($fullPath));
    if (!$image) return null;

    ob_start();
    imagejpeg($image, null, 85);
    $data = base64_encode(ob_get_clean());
    imagedestroy($image);

    return "data:image/jpeg;base64,{$data}";
}
```

### In Blade template — display base64 or public_path
```blade
{{-- Logo (base64, self-contained) --}}
@if($logoBase64)
    <img src="{{ $logoBase64 }}"
         style="max-height: 60px; max-width: 160px;"
         alt="Logo">
@else
    {{-- Fallback to public_path --}}
    <img src="{{ public_path('images/logo.png') }}"
         style="max-height: 60px; max-width: 160px;"
         alt="Logo">
@endif

{{-- Student photo --}}
@if($photoBase64)
    <img src="{{ $photoBase64 }}"
         style="width: 80px; height: 80px; border: 2px solid #d1d5db; border-radius: 4px;"
         alt="Photo">
@endif

{{-- Direct public_path for static assets --}}
<img src="{{ public_path('images/stamp.png') }}"
     style="width: 100px; opacity: 0.4;"
     alt="">
```

---

## 9. Headers, Footers & Page Numbers

### Repeating header on every page (position: fixed)
```blade
<style>
    /* Fixed header — repeats on every page */
    #pdf-header {
        position: fixed;
        top: -15mm;     /* Negative = in the margin area */
        left: 0;
        right: 0;
        height: 14mm;
        border-bottom: 2px solid {{ $settings['primary_color'] ?? '#0453cb' }};
    }

    /* Fixed footer */
    #pdf-footer {
        position: fixed;
        bottom: -15mm;
        left: 0;
        right: 0;
        height: 12mm;
        border-top: 1px solid #d1d5db;
    }

    /* Push body content below header */
    #content { margin-top: 5mm; }
</style>

<div id="pdf-header">
    <table width="100%">
        <tr>
            <td>
                @if($logoBase64)
                    <img src="{{ $logoBase64 }}" style="height: 10mm;" alt="Logo">
                @endif
            </td>
            <td style="text-align: center; font-weight: bold; font-size: 11px;">
                {{ $settings['header_text'] ?? config('app.name') }}
            </td>
            <td style="text-align: right; font-size: 9px; color: #6b7280;">
                {{ date('d/m/Y') }}
            </td>
        </tr>
    </table>
</div>

<div id="pdf-footer">
    <table width="100%">
        <tr>
            <td style="font-size: 9px; color: #6b7280;">
                {{ $settings['footer_text'] ?? '' }}
            </td>
            <td style="text-align: right; font-size: 9px; color: #6b7280;">
                Page <span class="page"></span> / <span class="topage"></span>
            </td>
        </tr>
    </table>
</div>

<div id="content">
    {{-- Main content --}}
</div>
```

### Page numbers via DomPDF canvas script
```blade
{{-- Requires isPhpEnabled = true in setOptions --}}
<script type="text/php">
    if (isset($pdf)) {
        $pdf->page_script(function ($pageNumber, $pageCount, $canvas, $fontMetrics) {
            $font = $fontMetrics->getFont("DejaVu Sans", "normal");
            $size = 9;
            $color = [0.42, 0.45, 0.50]; // #6b7280
            $text = "Page {$pageNumber} / {$pageCount}";
            $width = $canvas->get_width();
            $height = $canvas->get_height();
            $textWidth = $fontMetrics->getTextWidth($text, $font, $size);
            $canvas->text($width - $textWidth - 20, $height - 20, $text, $font, $size, $color);
        });
    }
</script>
```

---

## 10. Matching App Web Previews Pixel-Perfect

When the user shows a web preview and wants the PDF to look identical:

### Step 1 — Inspect the web view
```bash
# Read the Blade view file for the preview page
# Identify: layout structure, colors, fonts, spacing, tables
```

### Step 2 — Extract the color palette
Look at the view's `<style>` or CSS classes and map them to KLASSCI palette:
- Blue buttons/headers → `#0453cb` (primary)
- Gray text → `#64748b` (secondary)
- Green badges → `#10b981`
- Amber/yellow → `#f59e0b`
- Dark text → `#1f2937`

### Step 3 — Convert layout to DomPDF-safe HTML
| Web element | PDF equivalent |
|-------------|---------------|
| `<div class="row"><div class="col-6">` | `<table><tr><td width="50%">` |
| `<div class="d-flex gap-3">` | `<table><tr><td style="padding-right: 12px;">` |
| `<div class="card">` | Info card pattern (see §5) |
| `<span class="badge bg-success">` | `<span style="background-color: #10b981; color: #fff; padding: 2px 6px; border-radius: 3px; font-size: 9px;">` |
| `<h5 class="card-title">` | `<h3 style="font-size: 13px; color: #0453cb;">` |
| Bootstrap table | Remove classes, add inline styles (see §6) |

### Step 4 — Map measurements
- Bootstrap `col-6` = `td width="48%"` (with 4% spacer)
- Bootstrap `col-4` = `td width="31%"`
- Bootstrap `col-3` = `td width="23%"`
- Bootstrap `p-3` = `padding: 16px`
- Bootstrap `p-2` = `padding: 8px`
- Bootstrap `gap-3` = `cellspacing="12"` or `padding-right: 12px`

### Step 5 — Test at matching DPI
Use DPI 96 for on-screen comparison, DPI 150 for print quality. The visual weight of borders and text shifts with DPI — always compare at the same setting.

---

## 11. Page Breaks & Pagination

```blade
<style>
    /* Force new page */
    .page-break-before { page-break-before: always; }
    .page-break-after  { page-break-after: always; }

    /* Never split this element across pages */
    .keep-together { page-break-inside: avoid; }

    /* Keep heading with its following content */
    h2, h3 { page-break-after: avoid; }

    /* Prevent orphans/widows */
    p { orphans: 3; widows: 3; }
</style>

{{-- Force new page per student (e.g., in bulk bulletin generation) --}}
@foreach($bulletins as $index => $bulletin)
    @if($index > 0)
        <div class="page-break-before"></div>
    @endif

    <div class="keep-together">
        {{-- Bulletin content --}}
    </div>
@endforeach

{{-- Keep table header with first rows --}}
<div class="keep-together">
    <h3>Résultats par matière</h3>
    <table>
        <thead>...</thead>
        <tbody>
            {{-- first few rows --}}
        </tbody>
    </table>
</div>
```

---

## 12. Performance Optimization

```php
// Controller — performance-optimized PDF generation
$pdf = Pdf::loadView('esbtp.bulletins.pdf', $data)
    ->setPaper('a4', 'portrait')
    ->setOptions([
        'dpi'                    => 96,    // 96=web, 150=print (default for KLASSCI bulletins)
        'defaultFont'            => 'DejaVu Sans',
        'isRemoteEnabled'        => false, // Security + speed
        'isHtml5ParserEnabled'   => true,
        'isPhpEnabled'           => false, // Enable only if you need page_script()
        'isFontSubsettingEnabled'=> true,  // ~30% smaller files
    ]);

// For very large documents (>50 pages): increase PHP memory limit
ini_set('memory_limit', '512M');
set_time_limit(120);

// For bulk generation: use Laravel queues
dispatch(new GenerateBulletinPdfJob($bulletin->id));
```

### DPI guide
| Use case | DPI | File size | Notes |
|----------|-----|-----------|-------|
| Web download (email, portal) | 96 | Small | Fast generation |
| Default KLASSCI documents | 150 | Medium | Good balance |
| High-quality print | 300 | Large | Slow, use queues |

---

## 12.5. Blade Pitfalls That Crash PDF Rendering ⚠

These bugs are silent at compile time (`php artisan view:cache` succeeds) but crash PHP at runtime when the PDF actually renders. They affect **all** Blade files but PDF templates are the most common victims because they use `@php(expr)` shortform for logo loading.

### ❌ Pitfall #1 — `@php(expr)` shortform mixed with `@php ... @endphp` blocks

**The bug** : Laravel's Blade compiler regex `(?<!@)@php(.*?)@endphp/s` does NOT distinguish the shortform `@php(expr)` (with parens, no `@endphp` after) from the block form `@php ... @endphp`. If your file uses `@php(expr)` shortform AND has any `@php ... @endphp` block later, the regex captures `@php(` of the shortform as a block opening and **eats everything until the next `@endphp`**.

Symptom: the file compiles silently, but PHP runtime crashes with errors like:
```
syntax error, unexpected token "endforeach", expecting end of file
```
The `@endforeach` (or similar) appears orphaned because its `@foreach` was inside the eaten range and never compiled.

Real incident (2026-05-08, KLASSCI presentation): `liste-appel-pdf.blade.php` had `@php($_logo = ...)` at line 392 and `@php $accProfile = ...; @endphp` at line 472. The regex ate L392→L472, leaving the `@foreach($etudiants)` at L470 as text. PHP crashed at L498's `<?php endforeach; ?>`. 4 PDFs were affected.

**Fix** : NEVER use `@php(expr)` shortform in a file that also contains `@php ... @endphp` blocks. Always use the block form, even on a single line:

```blade
{{-- ❌ FRAGILE — eaten by next @endphp in file --}}
@php($_logo = \App\Helpers\SettingsHelper::resolveLogoBase64())

{{-- ✅ ROBUST — self-contained block --}}
@php $_logo = \App\Helpers\SettingsHelper::resolveLogoBase64(); @endphp
```

**Detection** :
```bash
# Quick audit on any Blade file
grep -n "@php(" resources/views/path/to/file.blade.php

# Validate compiled output catches the bug:
rm storage/framework/views/*.php
php artisan view:cache
php -l storage/framework/views/<hash>.php
# → Should output "No syntax errors detected"
```

### ❌ Pitfall #2 — `@directive` literal in JS/HTML comments

Blade scans the entire file for `@xxx` patterns, **including inside JavaScript and HTML comments**. Writing `@can`, `@if`, `@foreach`, `@endif`, etc. literally inside a comment triggers Blade's directive parser.

Real incident (2026-05-07): a JS comment `// gating @can côté Blade` in `inscriptions/create.blade.php` was parsed as an unclosed `@can(...)` directive → 500 error on the entire page.

**Fix** : Reformulate the comment to avoid the directive name, or escape with `@@xxx` (Blade outputs `@xxx` literal):

```blade
{{-- ❌ Triggers Blade --}}
<script>
    // gating @can côté Blade
</script>

{{-- ✅ Safe (reformulation) --}}
<script>
    // gating Blade côté serveur
</script>

{{-- ✅ Safe (escape with @@) --}}
<script>
    // see @@can directive in the partial
</script>
```

### Audit checklist before deploying any new Blade

```bash
# 1. Count balanced directives
grep -oE "@(if|endif|foreach|endforeach|php|endphp|can|endcan|push|endpush|once|endonce|section|endsection)\b" file.blade.php | sort | uniq -c
# Each pair must have equal counts.

# 2. Look for shortform @php( in files with later @endphp
grep -n "@php(" file.blade.php
# If found AND there's a @endphp later → convert to block form.

# 3. Look for directives in comments
grep -nE "//.*@(can|if|foreach|endif)" file.blade.php
grep -nE "<!--.*@(can|if|foreach|endif)" file.blade.php
# Either remove the @ from the comment text or escape with @@.

# 4. Force lint compiled output (catches both pitfalls above)
rm storage/framework/views/*.php
php artisan view:cache
for f in storage/framework/views/*.php; do php -l "$f" 2>&1 | grep -v "No syntax errors"; done
```

---

## 12.6. Pièges payés en production (bulletins Abidjan, août 2026)

Quatre bugs réels, chacun vu sur un bulletin imprimé avant d'être compris :

1. **Spécificité contre les resets de table.** `.parent td { border:none; padding:0 }` = (0,1,1)
   et bat TOUTE simple classe `.ma-cellule` = (0,1,0). Conséquence : bordure/padding d'une
   cellule « spéciale » silencieusement annulés. Règle : dans un tableau qui a un reset sur
   `td`, toute cellule particulière se cible `.parent td.ma-cellule`. Ce piège a frappé 3 fois
   dans la même session (filet vertical invisible, cellule sans padding, valeur collée aux
   deux points du libellé).
2. **Un flag qui gate `@page`.** Si le template n'émet son bloc `@page` que sous condition
   (`@if($isPdfExport ?? false)`), TOUT chemin de rendu PDF doit poser ce flag. Un chemin
   l'oubliait → DomPDF appliquait ses marges par défaut (~27mm) et les réglages de marges
   étaient sans effet. Vérifier avec grep que chaque `PDF::loadView` du domaine pose le flag.
3. **`inline-block` n'aligne pas les lignes de base.** Deux spans `inline-block` côte à côte
   (libellé + valeur) apparaissent décalés verticalement. Seul montage fiable : deux `<td>`
   d'une même `<tr>`. Largeur du libellé en `em` pour suivre `bulletin_font_size`.
4. **`td:first-child` traverse les tableaux imbriqués.** Une règle sur
   `.outer td:first-child` (cellule photo) attrape aussi la première cellule de chaque ligne
   d'un tableau imbriqué dans une autre cellule. Toujours une classe explicite.

Et le rappel du §6 vécu en vrai : `background` sur `<tr>` n'est pas rendu mais `color:#fff`
EST hérité par les `td` → bandeau blanc avec texte blanc, invisible à l'impression.

---

## 13. Debugging Tips

### Check if images load
```blade
{{-- Debug: show the path being used --}}
@if(config('app.debug'))
    <!-- Logo path: {{ $logoBase64 ? 'base64 (ok)' : public_path('images/logo.png') }} -->
@endif
```

### Common errors and fixes

| Error | Cause | Fix |
|-------|-------|-----|
| Images not showing | Using `asset()` | Use `public_path()` or base64 |
| Background on rows not showing | CSS on `<tr>` | Target `<tr> td` or put on `<td>` |
| Broken layout | Using flexbox/grid | Convert to `<table>` layout |
| Font with accents broken | Using Arial/Helvetica | Use `DejaVu Sans` |
| PDF cuts element mid-way | No page-break control | Add `page-break-inside: avoid` |
| Colors not matching brand | Hardcoded colors | Use `$settings['primary_color']` |
| Huge file size | DPI 300 + no font subsetting | Use DPI 150 + `isFontSubsettingEnabled: true` |
| Memory exhausted | Large dataset | Add `ini_set('memory_limit', '512M')` or use queues |
| CSS from `theme.blade.php` not applying | Missing `@include` | Add `@include('pdf.partials.theme')` after `</style>` |

### Test the template in browser first
```php
// Add a /preview route alongside the /pdf route
Route::get('/bulletins/{id}/preview', function ($id) {
    $bulletin = ESBTPBulletin::findOrFail($id);
    // ... same data preparation as genererPDF()
    return view('esbtp.bulletins.pdf-configurable', $data);
});
```
Browser preview uses CSS normally — fix layout issues there first, then generate PDF.

---

## 14. Ready-to-Copy Snippets

### Document header block (with logo + school info + title)
```blade
<table width="100%" border="0" cellspacing="0" cellpadding="0"
       style="border-bottom: 2.5px solid {{ $settings['primary_color'] ?? '#0453cb' }};
              padding-bottom: 10px;
              margin-bottom: 16px;">
    <tr>
        {{-- Left: Logo --}}
        <td width="20%" style="vertical-align: middle;">
            @if($logoBase64)
                <img src="{{ $logoBase64 }}" style="max-height: 55px; max-width: 110px;" alt="Logo">
            @endif
        </td>

        {{-- Center: School name + document title --}}
        <td width="60%" style="text-align: center; vertical-align: middle;">
            <div style="font-size: 11px; color: #6b7280; margin-bottom: 2px;">
                RÉPUBLIQUE DE CÔTE D'IVOIRE
            </div>
            <div style="font-size: 14px; font-weight: bold; color: {{ $settings['primary_color'] ?? '#0453cb' }};">
                {{ config('app.school_name', 'ESBTP') }}
            </div>
            <div style="font-size: 16px; font-weight: bold; color: #1f2937; margin-top: 4px;">
                {{ strtoupper($documentTitle ?? 'BULLETIN DE NOTES') }}
            </div>
            <div style="font-size: 10px; color: #6b7280; margin-top: 2px;">
                {{ $anneeUniversitaire->name ?? '' }} — {{ $periode ?? '' }}
            </div>
        </td>

        {{-- Right: Student photo --}}
        <td width="20%" style="text-align: right; vertical-align: middle;">
            @if($photoBase64)
                <img src="{{ $photoBase64 }}"
                     style="width: 65px; height: 75px; border: 1px solid #d1d5db; border-radius: 3px;"
                     alt="Photo">
            @endif
        </td>
    </tr>
</table>
```

### Badge / status indicator
```blade
@php
$badgeColors = [
    'validé'     => ['bg' => '#d1fae5', 'text' => '#065f46'],
    'en_attente' => ['bg' => '#fef3c7', 'text' => '#92400e'],
    'rejeté'     => ['bg' => '#fee2e2', 'text' => '#991b1b'],
    'default'    => ['bg' => '#f3f4f6', 'text' => '#374151'],
];
$colors = $badgeColors[$status] ?? $badgeColors['default'];
@endphp
<span style="
    display: inline-block;
    background-color: {{ $colors['bg'] }};
    color: {{ $colors['text'] }};
    padding: 2px 8px;
    border-radius: 10px;
    font-size: 9px;
    font-weight: bold;
    border: 1px solid {{ $colors['text'] }}40;
">{{ ucfirst($status) }}</span>
```

### Signature block (director + secretary)
```blade
<table width="100%" border="0" cellspacing="0" cellpadding="0"
       style="margin-top: 30px; page-break-inside: avoid;">
    <tr>
        <td width="45%" style="text-align: center; vertical-align: top;">
            <div style="font-size: 10px; color: #6b7280; margin-bottom: 6px;">
                LE DIRECTEUR
            </div>
            @if($settings['signature_director'])
                <img src="{{ public_path('storage/' . $settings['signature_director']) }}"
                     style="max-height: 45px; max-width: 120px;" alt="Signature">
            @else
                <div style="height: 45px;"></div>
            @endif
            <div style="border-top: 1px solid #374151; margin-top: 4px; padding-top: 4px; font-size: 10px; font-weight: bold;">
                {{ $settings['director_name'] ?? '' }}
            </div>
        </td>
        <td width="10%"></td>
        <td width="45%" style="text-align: center; vertical-align: top;">
            <div style="font-size: 10px; color: #6b7280; margin-bottom: 6px;">
                LA SCOLARITÉ
            </div>
            @if($settings['signature_secretary'])
                <img src="{{ public_path('storage/' . $settings['signature_secretary']) }}"
                     style="max-height: 45px; max-width: 120px;" alt="Signature">
            @else
                <div style="height: 45px;"></div>
            @endif
            <div style="border-top: 1px solid #374151; margin-top: 4px; padding-top: 4px; font-size: 10px; font-weight: bold;">
                {{ $settings['secretary_name'] ?? '' }}
            </div>
        </td>
    </tr>
</table>
```

### Document footer
```blade
<div style="margin-top: 20px;
            padding-top: 8px;
            border-top: 1px solid #e5e7eb;
            text-align: center;
            font-size: 9px;
            color: #9ca3af;
            page-break-inside: avoid;">
    {{ $settings['footer_text'] ?? config('app.name') }}
    — Généré le {{ now()->format('d/m/Y à H:i') }}
    @if($settings['watermark'])
        — {{ $settings['watermark'] }}
    @endif
</div>
```

### Stat card row (KPIs)
```blade
<table width="100%" border="0" cellspacing="0" cellpadding="0" style="margin-bottom: 16px;">
    <tr>
        @foreach($stats as $stat)
        <td width="{{ floor(100 / count($stats)) }}%"
            style="padding: @if(!$loop->first)0 0 0 8px@else 0 8px 0 0@endif; vertical-align: top;">
            <table width="100%" style="border: 1px solid #e5e7eb; border-radius: 6px;">
                <tr>
                    <td style="background-color: #f9fafb;
                               padding: 10px 12px;
                               border-radius: 6px 6px 0 0;
                               font-size: 9px;
                               color: #6b7280;
                               text-transform: uppercase;
                               letter-spacing: 0.3px;">
                        {{ $stat['label'] }}
                    </td>
                </tr>
                <tr>
                    <td style="padding: 8px 12px 10px;
                               font-size: 18px;
                               font-weight: bold;
                               color: {{ $settings['primary_color'] ?? '#0453cb' }};">
                        {{ $stat['value'] }}
                    </td>
                </tr>
            </table>
        </td>
        @endforeach
    </tr>
</table>
```
