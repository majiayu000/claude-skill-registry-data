---
name: preview-mode
description: >
  Show-before-commit previews — after completing work, present what changed as
  a live dev-server URL or a concise plain-language description so the user can
  confirm or request changes with confidence. Use when delivering visible
  changes (pages, components, styling) to a running project.
user-invocable: false  # internal — model-invoked via toh-* commands, not a user /command
---
# 👁️ Preview Mode Skill

> **Purpose:** Show users what will change before applying
> **Version:** 1.0.0
> **Author:** Toh Framework Team

## Overview

This skill enables AI to show previews of changes before applying them, giving users confidence in what's being created.

## Core Principle

```
AI completes work
    ↓
Show preview (description + URL if available)
    ↓
User confirms or requests changes
    ↓
Apply changes (or iterate)
```

**SEE BEFORE COMMIT**

---

## Preview Types

### Type 1: Dev Server Preview (Live)

When dev server is running:

```markdown
✅ **สร้าง Dashboard เสร็จแล้ว!**

👁️ **Preview:**
🌐 http://localhost:3000/dashboard

📸 **สิ่งที่สร้าง:**
- Header พร้อม navigation
- Stats cards (4 ตัว)
- Sales chart
- Recent orders table

เปิด URL ด้านบนเพื่อดู preview ได้เลยครับ!

💡 ต้องการแก้ไขอะไรไหมครับ?
```

### Type 2: Description Preview (No Server)

When dev server isn't running:

```markdown
✅ **เตรียม Dashboard พร้อมแล้ว!**

📋 **Preview สิ่งที่จะสร้าง:**

**Layout:**
┌─────────────────────────────────────┐
│ 🔵 Header (Logo + Nav + Profile)   │
├─────────────────────────────────────┤
│ 📊 Stats Cards (4 columns)          │
│ ┌───┐ ┌───┐ ┌───┐ ┌───┐            │
│ │ $ │ │ 📦│ │ 👥│ │ 📈│            │
│ └───┘ └───┘ └───┘ └───┘            │
├─────────────────────────────────────┤
│ 📈 Sales Chart (Line/Bar)          │
│ [Chart area]                        │
├─────────────────────────────────────┤
│ 📋 Recent Orders Table             │
│ ID | Customer | Amount | Status     │
└─────────────────────────────────────┘

**Components:**
- StatsCard.tsx (reusable)
- SalesChart.tsx (with Recharts)
- OrdersTable.tsx (with pagination)

สร้างเลยไหมครับ? หรือต้องการปรับอะไรก่อน?
```

### Type 3: Before/After Preview (Modifications)

When modifying existing code:

```markdown
🔄 **Preview การเปลี่ยนแปลง:**

**Before:**
```tsx
<Button>Submit</Button>
```

**After:**
```tsx
<Button 
  onClick={handleSubmit}
  disabled={isLoading}
>
  {isLoading ? <Spinner /> : 'Submit'}
</Button>
```

**Changes:**
- ✅ เพิ่ม onClick handler
- ✅ เพิ่ม loading state
- ✅ เพิ่ม Spinner component

Apply การเปลี่ยนแปลงนี้ไหมครับ?
```

---

## Auto Dev Server Detection

AI should detect if dev server is running:

```javascript
// Check if localhost:3000 is accessible
// If yes → Provide live URL
// If no → Provide description preview
```

### With Dev Server

```markdown
👁️ **Live Preview พร้อมแล้ว:**
🌐 http://localhost:3000/[path]

(เปิดดูได้เลยครับ!)
```

### Without Dev Server

```markdown
💡 **เปิด preview ได้โดย:**
```bash
npm run dev
```
แล้วไปที่ http://localhost:3000/[path]
```

---

## Preview Confirmation Flow

### Standard Flow

```
1. AI creates/modifies files
2. AI shows preview
3. User reviews
4. Options:
   - "OK" / "ได้เลย" → Continue
   - "แก้ไข [detail]" → AI modifies
   - "ยกเลิก" → AI reverts
```

### Quick Flow (For Simple Changes)

```
1. AI shows preview inline
2. Applies immediately
3. User can undo if needed
```

---

## Preview Templates by Task Type

### New Page Preview

```markdown
📄 **New Page: /dashboard**

**Layout:**
[ASCII art layout]

**Features:**
- [Feature list]

**Components Used:**
- [Component list]

**Files to Create:**
- app/dashboard/page.tsx
- components/dashboard/StatsCard.tsx
- components/dashboard/SalesChart.tsx

สร้างเลยไหมครับ?
```

### New Component Preview

```markdown
🧩 **New Component: ProductCard**

**Preview:**
┌─────────────────┐
│    [Image]      │
│  Product Name   │
│     ฿199        │
│  [Add to Cart]  │
└─────────────────┘

**Props:**
- product: Product
- onAddToCart: () => void

**Features:**
- Responsive
- Hover effect
- Loading state

สร้างเลยไหมครับ?
```

### Design Change Preview

```markdown
✨ **Design Changes:**

**Color Palette:**
- Primary: #3B82F6 → #2563EB (darker)
- Background: #F9FAFB → #F3F4F6 (warmer)

**Typography:**
- Headings: font-semibold → font-bold
- Body: text-gray-600 → text-gray-700

**Spacing:**
- Cards: p-4 → p-6 (more breathing room)
- Sections: gap-4 → gap-6

**Before/After:**
[Side by side comparison if possible]

Apply changes ไหมครับ?
```

### Logic Change Preview

```markdown
⚙️ **Logic Changes: handleSubmit**

**What changes:**
1. Add validation before submit
2. Add loading state
3. Add success/error toast
4. Clear form on success

**Flow:**
```
User clicks Submit
    ↓
Validate form (Zod)
    ↓
Show loading state
    ↓
Call API
    ↓
Success? → Show toast + Clear form
Error? → Show error message
```

Apply changes ไหมครับ?
```

---

## Multi-File Change Preview

When changes span multiple files:

```markdown
📁 **Files to Change:**

**Create:**
- components/checkout/PaymentForm.tsx
- lib/stripe.ts
- app/api/checkout/route.ts

**Modify:**
- app/cart/page.tsx (add checkout button)
- types/index.ts (add PaymentIntent type)

**Total:** 3 new files, 2 modified

ดู diff แต่ละไฟล์ไหมครับ? หรือ apply เลย?
```

---

## Preview for Destructive Actions

Extra confirmation for risky operations:

```markdown
⚠️ **Warning: Destructive Action**

**จะลบ:**
- app/old-dashboard/ (3 files)
- components/old-chart/ (2 files)

**Total:** 5 files จะถูกลบ

⚡ ก่อนลบ:
- [x] สร้าง backup checkpoint แล้ว
- [x] ไฟล์ใหม่พร้อมใช้แทนแล้ว

พิมพ์ 'confirm' เพื่อยืนยันการลบ
หรือ 'cancel' เพื่อยกเลิก
```

---

## Preview Settings

User can configure preview behavior:

```markdown
/toh-settings preview

**Preview Mode:**
- [x] Always show preview (default)
- [ ] Quick mode (apply without preview)
- [ ] Ask each time

**Preview Detail:**
- [ ] Minimal (layout only)
- [x] Normal (layout + components)
- [ ] Verbose (everything)
```

---

## Integration with Other Skills

| Skill | Integration |
|-------|-------------|
| Version Control | Auto-checkpoint before apply |
| Error Handling | Preview potential issues |
| Smart Suggestions | Suggest improvements in preview |
| Progress Tracking | Show progress after apply |

---

## Best Practices

### DO:
- ✅ Always show preview for major changes
- ✅ Provide live URL when possible
- ✅ Use ASCII art for layout preview
- ✅ List all files that will change
- ✅ Highlight breaking changes

### DON'T:
- ❌ Skip preview for destructive actions
- ❌ Show too much technical detail
- ❌ Assume user wants to proceed
- ❌ Apply without any confirmation for major changes

---

## ASCII Art Templates

### Dashboard Layout

```
┌─────────────────────────────────────────┐
│ Header                                  │
├─────────┬───────────────────────────────┤
│ Sidebar │ Main Content                  │
│         │                               │
│ Nav     │ Cards / Charts / Tables       │
│ Items   │                               │
│         │                               │
└─────────┴───────────────────────────────┘
```

### Card Grid

```
┌───────┐ ┌───────┐ ┌───────┐
│ Card  │ │ Card  │ │ Card  │
│   1   │ │   2   │ │   3   │
└───────┘ └───────┘ └───────┘
```

### Form Layout

```
┌─────────────────────────────┐
│ Form Title                  │
├─────────────────────────────┤
│ Label          [Input     ] │
│ Label          [Input     ] │
│ Label          [Textarea  ] │
│                [         ]  │
├─────────────────────────────┤
│         [Cancel] [Submit]   │
└─────────────────────────────┘
```

### Table Layout

```
┌────┬──────────┬────────┬────────┐
│ ID │ Name     │ Amount │ Status │
├────┼──────────┼────────┼────────┤
│ 1  │ Item 1   │ ฿100   │ ✅     │
│ 2  │ Item 2   │ ฿200   │ ⏳     │
└────┴──────────┴────────┴────────┘
```

---

*Last Updated: 2024-12-03*
