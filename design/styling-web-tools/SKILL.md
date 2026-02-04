---
name: styling-web-tools
description: Applying consistent visual design to HTML tools in this repository. Use when creating new tools, updating UI components, or adding buttons/icons/controls. Based on Vercel Geist design system with Claude app influences.
---

# Web Tools Style Guide

Apply these standards when building or modifying HTML tools.

## Colors

```css
/* Backgrounds */
--background: #0a0a0a;
--background-secondary: #111111;
--background-interactive: #262626;
--background-hover: #333333;

/* Accent */
--blue-500: #0070f3;
--blue-600: #0060d1;

/* Text */
--text-primary: #ededed;
--text-secondary: #a1a1a1;

/* Borders */
--border: #262626;
```

## Buttons

Icon-only circular buttons (44px touch targets):

```css
button {
    background: #262626;
    color: #ffffff;
    border: none;
    width: 44px;
    height: 44px;
    border-radius: 22px;
    cursor: pointer;
    transition: all 0.15s ease;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 0;
}

button:hover { background: #333333; }
button:active { transform: scale(0.95); opacity: 0.9; }
button.primary { background: #0070f3; }
button.primary:hover { background: #0060d1; }
button:disabled { opacity: 0.4; cursor: not-allowed; }
```

Button row layout:
```css
.button-row {
    display: flex;
    gap: 12px;
    justify-content: center;
    align-items: center;
}
```

## Icons

Use Heroicons outline style:
- **Size**: 20x20px inside buttons
- **Stroke width**: 1.5 (not 2)
- Always include `title` attribute

```html
<button title="Action Name">
    <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="..."></path>
    </svg>
</button>
```

```css
button svg { width: 20px; height: 20px; }
```

## Dropdowns

Pill-shaped selects:
```css
select {
    background: #262626;
    color: #a1a1a1;
    border: none;
    padding: 10px 28px 10px 12px;
    border-radius: 22px;
    font-size: 12px;
    height: 36px;
    appearance: none;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='%23a1a1a1'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M19 9l-7 7-7-7'/%3E%3C/svg%3E");
    background-repeat: no-repeat;
    background-position: right 10px center;
    background-size: 12px;
}
```

## Corner Handles

For draggable control points:
```css
.corner-handle {
    width: 22px;
    height: 22px;
    background: #0070f3;
    border: 2px solid #ffffff;
    border-radius: 50%;
    position: absolute;
    transform: translate(-50%, -50%);
    cursor: grab;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.4);
}
```

## iOS PWA

```html
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="App Name">
<link rel="apple-touch-icon" href="icons/app-icon.png">
<meta name="mobile-web-app-capable" content="yes">
<meta name="theme-color" content="#0a0a0a">
```

## Mobile Viewport

```html
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
```

```css
body {
    min-height: 100vh;
    min-height: -webkit-fill-available;
    overflow: hidden;
    touch-action: none;
}
```

## Spacing

- Button gap: 12px
- Control padding: 12px 16px
- Borders: 1px solid #262626
