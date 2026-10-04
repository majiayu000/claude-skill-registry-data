---
name: dev-storefront
description: Coding patterns for Shopify storefront customer-facing UI. Auto-apply when writing Preact components, Theme App Extensions, storefront scripts, or code in extensions/ directory. Focus on lightweight bundle and performance.
allowed-tools: Read, Grep, Glob, Bash, Edit, Write, WebSearch, WebFetch
argument-hint: [component hoặc feature cần implement]
---

# Shopify Storefront — Development Conventions

Áp dụng conventions này khi develop code cho **storefront** (customer-facing UI). Performance là ưu tiên số 1.

## Tech Stack

| Layer | Technology | Notes |
|-------|-----------|-------|
| UI Framework | Preact | ~3KB gzipped — KHÔNG dùng React (45KB+) |
| Extensions | Theme App Extensions | Liquid + App Blocks |
| Language | TypeScript | Strict mode, tree-shakeable |
| Styling | Vanilla CSS / CSS Modules | KHÔNG Tailwind, KHÔNG CSS-in-JS |
| Bundler | Vite | Tree-shaking, code splitting |
| State | Preact Signals | Lightweight reactive state (~1KB) |

## Performance Budget

| Metric | Target | Hard Limit |
|--------|--------|------------|
| **JS Bundle** | < 15KB gzipped | 30KB gzipped |
| **CSS** | < 5KB gzipped | 10KB gzipped |
| **First Paint** | < 100ms | 200ms |
| **LCP Impact** | < 50ms | 100ms |
| **No layout shift** | CLS = 0 | CLS < 0.1 |

Merchant không accept app làm chậm storefront. Mọi byte đều quan trọng.

## Core Principles

1. **Performance First**: Mỗi KB thêm vào đều phải justify. Prefer vanilla JS nếu Preact không cần thiết
2. **Progressive Enhancement**: Storefront phải work khi JS disabled (basic Liquid), Preact enhance thêm
3. **Lazy Loading**: Chỉ load JS khi component visible (Intersection Observer)
4. **No External Dependencies**: Không thêm npm packages cho storefront — viết tay hoặc inline
5. **Minimal DOM**: Ít DOM nodes nhất có thể, tránh deep nesting
6. **CSS First**: Animation/transition dùng CSS, không JS khi có thể

## Directory Structure

```
extensions/
├── theme-app-extension/
│   ├── assets/
│   │   ├── app-widget.js          # Bundled Preact component
│   │   └── app-widget.css         # Scoped styles
│   ├── blocks/
│   │   ├── app-block.liquid       # App Block definition
│   │   └── promo-banner.liquid    # App Block definition
│   ├── snippets/
│   │   └── app-tracking.liquid    # Shared snippet
│   └── locales/
│       └── en.default.json        # Translations
└── src/                            # Preact source (pre-build)
    ├── components/
    │   ├── AppWidget.tsx
    │   └── PromoBanner.tsx
    ├── hooks/
    │   └── useTracking.ts
    ├── utils/
    │   └── api.ts
    └── index.tsx                   # Entry point
```

## Code Patterns

Xem chi tiết tại [patterns.md](patterns.md) bao gồm:
- Preact component pattern (functional, minimal)
- Signals state management pattern
- Lazy loading / code splitting pattern
- Theme App Extension block pattern (Liquid)
- Storefront API fetch pattern
- Tracking pixel pattern (lightweight)
- CSS scoping pattern (no leaks)
- Intersection Observer pattern

## Do's and Don'ts

### DO
- Dùng Preact `h()` hoặc JSX pragma — KHÔNG React
- Dùng Preact Signals thay vì useState cho shared state
- Lazy load components bằng `IntersectionObserver`
- Scope CSS bằng unique prefix (e.g., `.app-widget__title`)
- Dùng `<script type="module">` cho modern browsers
- Test bundle size trước mỗi PR (`npx bundlesize`)
- Dùng Liquid `{% schema %}` settings cho merchant customization
- Provide fallback Liquid content khi JS disabled

### DON'T
- KHÔNG import React, ReactDOM, hoặc bất kỳ React package nào
- KHÔNG dùng CSS-in-JS (styled-components, emotion) — overhead quá lớn
- KHÔNG dùng Tailwind CSS — utility classes bloat storefront
- KHÔNG fetch Shopify Admin API từ storefront — chỉ Storefront API hoặc App Proxy
- KHÔNG dùng `document.write`, `eval`, hoặc inline scripts
- KHÔNG blocking render — async/defer tất cả scripts
- KHÔNG install npm packages > 5KB cho storefront code
- KHÔNG dùng `localStorage` cho sensitive data (tokens, secrets)
- KHÔNG modify merchant's theme CSS/DOM ngoài app block

## Banned Imports (Storefront)

```typescript
// NEVER import these in storefront code:
// ❌ import React from 'react'
// ❌ import { useState } from 'react'
// ❌ import styled from 'styled-components'
// ❌ import { css } from '@emotion/react'
// ❌ import tw from 'tailwind-styled-components'
// ❌ import axios from 'axios'
// ❌ import lodash from 'lodash'
// ❌ import moment from 'moment'

// ✅ Use these instead:
// import { h, render } from 'preact'
// import { signal, computed } from '@preact/signals'
// import { useEffect, useRef } from 'preact/hooks'
```

$ARGUMENTS
