---
name: rtl-ui
description: Implements right-to-left (RTL) UI patterns for Arabic interfaces using Tailwind CSS, covering layout direction, icon mirroring, typography, and spacing constraints for bidirectional applications
---

# RTL UI Development Standards

This skill provides comprehensive guidelines for building right-to-left (RTL) user interfaces, primarily targeting Arabic language support with Tailwind CSS.

## 🚨 CRITICAL REQUIREMENTS - READ FIRST

### MANDATORY Rules (Application Will Break if Violated)

**❌ NEVER USE THESE CLASSES - WILL CAUSE RTL BUGS:**
```tsx
// BANNED - Physical properties
ml-*, mr-*, pl-*, pr-*        // ❌ NEVER
left-*, right-*                // ❌ NEVER  
text-left, text-right         // ❌ NEVER
rounded-l-*, rounded-r-*      // ❌ NEVER
border-l-*, border-r-*        // ❌ NEVER
```

**✅ ALWAYS USE THESE INSTEAD - MANDATORY:**
```tsx
// REQUIRED - Logical properties
ms-*, me-*                    // ✅ REQUIRED (margin-inline-start/end)
ps-*, pe-*                    // ✅ REQUIRED (padding-inline-start/end)
start-*, end-*                // ✅ REQUIRED (positioning)
text-start, text-end          // ✅ REQUIRED (alignment)
rounded-s-*, rounded-e-*      // ✅ REQUIRED (border-radius)
border-s-*, border-e-*        // ✅ REQUIRED (borders)
```

**⚠️ ZERO TOLERANCE POLICY:**
- Every `ml-*` must be `ms-*`
- Every `pl-*` must be `ps-*`  
- Every `text-left` must be `text-start`
- **NO EXCEPTIONS** - Even for "temporary" code

### Next.js 14 Server Actions - MANDATORY PATTERN

**❌ ANTI-PATTERN - NEVER DO THIS:**
```tsx
// app/login/page.tsx
'use client';

export default function LoginPage() {
  // ❌ WRONG - Server action inside client component file
  async function loginAction(formData: FormData) {
    'use server';  // ❌ Mixed directives in same file
    // ...
  }
  
  return <form action={loginAction}>...</form>
}
```

**✅ REQUIRED PATTERN - ALWAYS DO THIS:**
```tsx
// app/actions/login.ts
'use server';  // ✅ Dedicated server action file

export async function loginAction(formData: FormData) {
  const supabase = await createClient()
  // ... implementation
}

// app/login/page.tsx  
'use client';  // ✅ Separate client component file

import { loginAction } from '@/app/actions/login'

export default function LoginPage() {
  return <form action={loginAction}>...</form>
}
```

**📁 REQUIRED File Structure:**
```
app/
├── actions/              ✅ MANDATORY - All server actions here
│   ├── login.ts         ('use server')
│   ├── register.ts      ('use server')
│   └── ...
├── (auth)/
│   ├── login/
│   │   └── page.tsx     ('use client')
│   └── register/
│       └── page.tsx     ('use client')
```

**🔒 RULE: One directive per file**
- Files with `'use server'` → Only server code
- Files with `'use client'` → Only client code
- **NEVER mix both in same file**

## Core Principles

### 1. Directional Layout System

**Always use logical properties over physical properties:**

```jsx
// ❌ WRONG - Physical properties
<div className="ml-4 pl-6 text-left">

// ✅ CORRECT - Logical properties (auto-flips in RTL)
<div className="ms-4 ps-6 text-start">
```

**Tailwind RTL-Safe Utilities:**
- `ms-*` / `me-*` instead of `ml-*` / `mr-*` (margin-inline-start/end)
- `ps-*` / `pe-*` instead of `pl-*` / `pr-*` (padding-inline-start/end)
- `start-*` / `end-*` instead of `left-*` / `right-*` (positioning)
- `text-start` / `text-end` instead of `text-left` / `text-right`
- `rounded-s-*` / `rounded-e-*` instead of `rounded-l-*` / `rounded-r-*`
- `border-s-*` / `border-e-*` instead of `border-l-*` / `border-r-*`

### 2. HTML Direction Attribute

Set the direction at the root level:

```html
<!-- For Arabic content -->
<html dir="rtl" lang="ar">

<!-- For English content -->
<html dir="ltr" lang="en">
```

**Dynamic direction switching:**

```jsx
// React/Next.js example
<html dir={locale === 'ar' ? 'rtl' : 'ltr'} lang={locale}>
```

### 3. Icon Mirroring Strategy

**Icons that MUST mirror in RTL:**
- Arrows: → ← ↗ ↙
- Chevrons: › ‹
- Navigation: back, forward, next, previous
- Directional actions: undo, redo, reply, forward (email)
- Timeline and progress indicators
- List indicators and bullet points

**Icons that NEVER mirror:**
- Media controls: play ▶, pause ⏸, stop ⏹
- Shopping cart 🛒
- Magnifying glass 🔍
- Checkmarks ✓
- Close/X buttons ✕
- Clocks and time 🕐
- Symmetrical icons: +, ×, gear ⚙

**Implementation:**

```jsx
// Using Lucide React or similar icon library
import { ChevronRight } from 'lucide-react';

// Option 1: CSS transform
<ChevronRight className="rtl:scale-x-[-1]" />

// Option 2: Conditional rendering
{isRTL ? <ChevronLeft /> : <ChevronRight />}

// Option 3: Rotate class (for arrows)
<ArrowRight className="rtl:rotate-180" />
```

### 4. Arabic Typography Rules

**Font Selection:**
- Use Arabic-optimized fonts: Cairo, Almarai, Tajawal, Noto Sans Arabic
- Ensure proper font stack: `'Cairo', 'Segoe UI Arabic', -apple-system, system-ui`

**Font Sizing:**
- Arabic text needs 10-15% larger font size for equivalent readability
- Line height: Use 1.7-1.8 for Arabic (vs 1.5-1.6 for English)

```css
/* Tailwind config extension */
.font-arabic {
  font-family: 'Cairo', 'Segoe UI Arabic', sans-serif;
  line-height: 1.75;
}

/* Apply via CSS */
html[dir="rtl"] {
  font-size: 105%; /* Slightly larger base size */
}
```

**Letter Spacing:**
```jsx
// ❌ NEVER use letter-spacing with Arabic
<h1 className="tracking-wide">مرحبا</h1>

// ✅ Default spacing only
<h1>مرحبا</h1>
```

### 5. Spacing and Layout Constraints

**Flexbox Direction:**

```jsx
// ❌ WRONG - Hardcoded direction
<div className="flex flex-row">

// ✅ CORRECT - Auto-reverses in RTL
<div className="flex flex-row">
  {/* Flex items automatically reverse in RTL context */}
</div>

// For explicit control when needed
<div className="flex flex-row rtl:flex-row-reverse">
```

**Grid Layouts:**

```jsx
// Grids work naturally in RTL - no changes needed
<div className="grid grid-cols-3 gap-4">
  {/* Items flow naturally based on dir attribute */}
</div>
```

**Asymmetric Spacing:**

```jsx
// ❌ WRONG - Physical spacing
<div className="mr-4 ml-2">

// ✅ CORRECT - Logical spacing
<div className="me-4 ms-2">
```

### 6. Forms and Inputs

**🚨 MANDATORY Form Pattern:**

```jsx
// ✅ REQUIRED - Complete form input with RTL support
<div className="space-y-6">
  <div>
    <label 
      htmlFor="email" 
      className="block text-start mb-2 font-medium"  // ✅ block + text-start
    >
      {locale === 'ar' ? 'البريد الإلكتروني' : 'Email'}
    </label>
    <input
      id="email"
      name="email"
      type="email"
      dir="auto"  // ✅ MANDATORY - Detects input direction
      className="w-full ps-4 pe-4 py-3 text-start rounded-lg border"  // ✅ ps-4 pe-4, NOT px-4
      placeholder={locale === 'ar' ? 'أدخل بريدك الإلكتروني' : 'Enter your email'}
      required
    />
  </div>
  
  <div>
    <label 
      htmlFor="password" 
      className="block text-start mb-2 font-medium"
    >
      {locale === 'ar' ? 'كلمة المرور' : 'Password'}
    </label>
    <input
      id="password"
      name="password"
      type="password"
      dir="auto"  // ✅ MANDATORY
      className="w-full ps-4 pe-4 py-3 text-start rounded-lg border"  // ✅ Logical padding
      placeholder={locale === 'ar' ? 'أدخل كلمة المرور' : 'Enter password'}
      required
    />
  </div>
  
  <button 
    type="submit"
    className="w-full py-3 bg-primary text-white rounded-lg"
  >
    {locale === 'ar' ? 'تسجيل الدخول' : 'Sign In'}
  </button>
</div>

// ❌ WRONG - Common mistakes
<input className="px-4" />              // ❌ NOT px-4
<input className="pl-4 pr-10" />       // ❌ NOT pl-/pr-
<label className="text-left" />        // ❌ NOT text-left
<input />                               // ❌ Missing dir="auto"
```

**📋 Form Input Checklist (MANDATORY):**
- [ ] All labels have `className="block text-start"`
- [ ] All inputs have `dir="auto"` attribute
- [ ] All inputs use `ps-*` and `pe-*` (NEVER `px-*`, `pl-*`, `pr-*`)
- [ ] All inputs have `text-start` class
- [ ] All placeholders are localized
- [ ] Button text is localized

### 7. Positioning and Absolute Elements

```jsx
// ❌ WRONG - Physical positioning
<div className="absolute right-4 top-4">

// ✅ CORRECT - Logical positioning
<div className="absolute end-4 top-4">

// Dropdowns and tooltips
<div className="absolute start-0 top-full mt-2">
  {/* Will appear on correct side in both LTR/RTL */}
</div>
```

### 8. Border Radius and Decorative Elements

```jsx
// ❌ WRONG
<div className="rounded-l-lg rounded-r-sm">

// ✅ CORRECT
<div className="rounded-s-lg rounded-e-sm">

// Asymmetric borders
<div className="border-s-4 border-e-2 border-primary">
```

## Common Patterns

### Navigation Menu

```jsx
<nav className="flex gap-4">
  <Link href="/" className="flex items-center gap-2">
    <Home className="rtl:scale-x-[-1]" />
    <span>{t('home')}</span>
  </Link>
  <Link href="/about" className="flex items-center gap-2">
    <span>{t('about')}</span>
    <ChevronRight className="rtl:rotate-180" />
  </Link>
</nav>
```

### Card Layouts

```jsx
<div className="flex gap-4 p-6">
  <img src={avatar} className="w-12 h-12 rounded-full" />
  <div className="flex-1 text-start">
    <h3 className="font-semibold">{name}</h3>
    <p className="text-sm text-gray-600">{description}</p>
  </div>
  <button className="ms-auto">
    <MoreVertical />
  </button>
</div>
```

### Breadcrumbs

```jsx
<nav className="flex items-center gap-2">
  {breadcrumbs.map((item, i) => (
    <>
      <Link href={item.href}>{item.label}</Link>
      {i < breadcrumbs.length - 1 && (
        <ChevronRight className="rtl:rotate-180 text-gray-400" />
      )}
    </>
  ))}
</nav>
```

### Modal Dialogs

```jsx
<div className="fixed inset-0 flex items-center justify-center">
  <div className="bg-white rounded-lg p-6 max-w-md w-full">
    <div className="flex items-start gap-4">
      <AlertCircle className="text-red-500 flex-shrink-0" />
      <div className="flex-1 text-start">
        <h2 className="font-bold mb-2">{t('warning')}</h2>
        <p className="text-gray-600">{t('message')}</p>
      </div>
      <button className="ms-auto">
        <X />
      </button>
    </div>
  </div>
</div>
```

## Testing Checklist

Before marking RTL implementation as complete:

**🚨 CRITICAL - Zero Tolerance Items:**
- [ ] **ZERO instances of `ml-*`, `mr-*`, `pl-*`, `pr-*` in entire codebase**
- [ ] **ZERO instances of `left-*`, `right-*` for positioning**
- [ ] **ZERO instances of `text-left`, `text-right`**
- [ ] **ZERO instances of `rounded-l-*`, `rounded-r-*`**
- [ ] **ZERO instances of `border-l-*`, `border-r-*`**
- [ ] **ALL server actions in separate `app/actions/` files**
- [ ] **NO files with both 'use client' and 'use server'**

**✅ Required Implementations:**
- [ ] `dir="rtl"` and `lang="ar"` attributes set on `<html>` tag
- [ ] All physical direction classes replaced with logical equivalents
- [ ] Directional icons properly mirrored or rotated
- [ ] Arabic font applied with appropriate line-height
- [ ] NO `letter-spacing` on Arabic text
- [ ] Form inputs have `dir="auto"` attribute
- [ ] Form labels have `block text-start` classes
- [ ] Form inputs use `ps-*` and `pe-*` (NOT `px-*`)
- [ ] Navigation flows in correct direction
- [ ] Dropdown menus and tooltips positioned correctly
- [ ] Asymmetric spacing (margins, padding) uses logical properties
- [ ] Tables use `text-start`/`text-end` (NEVER `text-left`/`text-right`)
- [ ] Absolute positioned elements use `start-*` / `end-*`
- [ ] Tested on actual RTL content (not just English text flipped)
- [ ] Responsive breakpoints work in RTL mode

**🔍 Code Search Commands (Run These):**
```bash
# Search for banned classes - ALL must return 0 results
grep -r "ml-" src/
grep -r "mr-" src/
grep -r "pl-" src/  
grep -r "pr-" src/
grep -r "text-left" src/
grep -r "text-right" src/
grep -r "left-" src/
grep -r "right-" src/

# Search for correct classes - Should find many results
grep -r "ms-" src/
grep -r "me-" src/
grep -r "ps-" src/
grep -r "pe-" src/
grep -r "text-start" src/
grep -r "text-end" src/
```

## Common Mistakes to Avoid

1. **Using transform: scaleX(-1) on text** - Never flip text itself
2. **Applying letter-spacing to Arabic** - Breaks Arabic ligatures
3. **Hardcoding left/right in JavaScript** - Use getBoundingClientRect() carefully
4. **Forgetting dir="auto" on user input fields** - Breaks mixed content
5. **Over-mirroring icons** - Play buttons should never mirror
6. **Using physical properties "temporarily"** - Always use logical from the start
7. **Testing only with flipped English** - Arabic has unique rendering needs
8. **❌ Mixing 'use client' and 'use server' in same file** - Separate into different files
9. **❌ Using `px-*` on form inputs** - Always use `ps-*` and `pe-*`
10. **❌ Using `text-left` on tables** - Always use `text-start`

## Resources

- [Tailwind RTL Support Documentation](https://tailwindcss.com/docs/hover-focus-and-other-states#rtl-support)
- [MDN Logical Properties](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Logical_Properties)
- [Material Design RTL Guidelines](https://material.io/design/usability/bidirectionality.html)

## Progressive Enhancement

For older browsers without logical property support, consider a fallback:

```css
/* tailwind.config.js - Add RTL plugin */
module.exports = {
  plugins: [
    require('tailwindcss-rtl'),
  ],
}
```

This ensures comprehensive RTL support across all browsers and contexts.