---
name: business-context
description: >
  Maps a business type the user mentions (coffee shop, restaurant, e-commerce,
  clinic, gym, hotel, school and more) to its industry-standard feature set —
  POS, inventory, orders, booking, reports, staff — and auto-includes those
  features with no questions asked. Fuels zero-question planning for /toh-vibe
  and /toh-plan whenever a request names a business or industry.
user-invocable: false  # internal — model-invoked via toh-* commands, not a user /command
---
# 🏢 Business Context Skill

> **Purpose:** AI understands business domains and auto-includes standard features
> **Version:** 1.0.0
> **Author:** Toh Framework Team

## Overview

This skill enables AI to understand business context from minimal user input and automatically include industry-standard features without asking.

## Core Principle

```
User says: "ร้านกาแฟ" or "coffee shop"
AI understands: Need POS, Inventory, Menu, Orders, Reports, Staff Management
```

**NO QUESTIONS ASKED** - AI makes intelligent decisions based on business type.

---

## Business Templates

### 🍽️ Food & Beverage (F&B)

**Trigger Words:** ร้านอาหาร, ร้านกาแฟ, คาเฟ่, restaurant, cafe, coffee shop, bakery, bar

**Auto-Include Features:**

| Feature | Priority | Description |
|---------|----------|-------------|
| POS System | 🔴 Must | Point of sale, order taking |
| Menu Management | 🔴 Must | Products, categories, prices |
| Order Management | 🔴 Must | Order status, kitchen display |
| Inventory | 🟡 Should | Stock tracking, low stock alerts |
| Reports & Analytics | 🟡 Should | Daily sales, top products |
| Staff Management | 🟢 Could | Shifts, permissions |
| Customer Loyalty | 🟢 Could | Points, rewards |
| Table Management | 🟢 Could | For dine-in restaurants |

**Default Pages:**
```
/                    → Dashboard (today's sales summary)
/pos                 → POS interface
/menu                → Menu management
/orders              → Order list & status
/inventory           → Stock management
/reports             → Sales reports
/settings            → Store settings
```

**Default Data Models:**
```typescript
// Core models for F&B
Product { id, name, price, category, image, inStock }
Order { id, items, total, status, createdAt, paymentMethod }
Category { id, name, sortOrder }
Inventory { productId, quantity, lowStockThreshold }
```

---

### 🛒 E-commerce

**Trigger Words:** ขายของออนไลน์, ร้านค้าออนไลน์, e-commerce, online store, shop

**Auto-Include Features:**

| Feature | Priority | Description |
|---------|----------|-------------|
| Product Catalog | 🔴 Must | Products, variants, images |
| Shopping Cart | 🔴 Must | Add/remove, quantity |
| Checkout | 🔴 Must | Address, payment |
| Order Management | 🔴 Must | Status, tracking |
| Customer Accounts | 🟡 Should | Login, order history |
| Payment Integration | 🟡 Should | Stripe, PromptPay |
| Shipping | 🟡 Should | Rates, tracking |
| Reviews | 🟢 Could | Product reviews |
| Wishlist | 🟢 Could | Save for later |
| Promotions | 🟢 Could | Coupons, discounts |

**Default Pages:**
```
/                    → Homepage (featured products)
/products            → Product listing
/products/[id]       → Product detail
/cart                → Shopping cart
/checkout            → Checkout flow
/account             → Customer account
/account/orders      → Order history
/admin               → Admin dashboard
/admin/products      → Product management
/admin/orders        → Order management
```

---

### 📅 Booking & Appointments

**Trigger Words:** จองคิว, นัดหมาย, booking, appointment, reservation, clinic, salon, spa

**Auto-Include Features:**

| Feature | Priority | Description |
|---------|----------|-------------|
| Service Catalog | 🔴 Must | Services, duration, price |
| Calendar View | 🔴 Must | Available slots |
| Booking Flow | 🔴 Must | Select service → time → confirm |
| Staff/Resource | 🟡 Should | Assign to staff/room |
| Reminders | 🟡 Should | Email/SMS notifications |
| Customer Management | 🟡 Should | Contact info, history |
| Online Payment | 🟢 Could | Deposit, full payment |
| Cancellation | 🟢 Could | Cancel/reschedule policy |

**Default Pages:**
```
/                    → Homepage (services overview)
/book                → Booking flow
/services            → Service list
/admin               → Admin dashboard
/admin/calendar      → Appointment calendar
/admin/services      → Service management
/admin/customers     → Customer list
```

---

### 📊 SaaS Dashboard

**Trigger Words:** dashboard, admin panel, management system, ระบบจัดการ, backoffice

**Auto-Include Features:**

| Feature | Priority | Description |
|---------|----------|-------------|
| Authentication | 🔴 Must | Login, register, password reset |
| Dashboard | 🔴 Must | Key metrics, charts |
| User Management | 🟡 Should | Roles, permissions |
| Settings | 🟡 Should | Profile, preferences |
| Data Tables | 🟡 Should | CRUD operations |
| Search & Filter | 🟡 Should | Find records |
| Export | 🟢 Could | CSV, PDF export |
| Notifications | 🟢 Could | In-app, email |
| Audit Log | 🟢 Could | Activity tracking |

**Default Pages:**
```
/                    → Redirect to dashboard or login
/login               → Login page
/register            → Registration
/dashboard           → Main dashboard
/[resource]          → Resource list (e.g., /users, /products)
/[resource]/[id]     → Resource detail
/settings            → User settings
```

---

### 🏪 Marketplace

**Trigger Words:** marketplace, ตลาด, platform, multi-vendor

**Auto-Include Features:**

| Feature | Priority | Description |
|---------|----------|-------------|
| Vendor Registration | 🔴 Must | Seller onboarding |
| Product Listings | 🔴 Must | Multi-vendor products |
| Search & Discovery | 🔴 Must | Find products/vendors |
| Order Routing | 🔴 Must | Route to correct vendor |
| Vendor Dashboard | 🟡 Should | Sales, products |
| Commission System | 🟡 Should | Platform fees |
| Reviews & Ratings | 🟡 Should | Trust building |
| Messaging | 🟢 Could | Buyer-seller chat |
| Disputes | 🟢 Could | Issue resolution |

---

## Usage Instructions

### For AI Agents

When user describes a project:

1. **Detect Business Type** - Match trigger words
2. **Select Template** - Load appropriate template
3. **Auto-Include Must-Have Features** - No asking needed
4. **Mention Should-Have Features** - Brief mention, include by default
5. **Offer Could-Have Features** - Quick mention at end

### Response Format

```markdown
เข้าใจครับ! จะสร้าง **[Business Type]** ให้

📦 Features ที่จะสร้าง:
- ✅ [Must-have 1]
- ✅ [Must-have 2]
- ✅ [Should-have 1]
- ✅ [Should-have 2]

💡 Features เสริม (บอกได้ถ้าต้องการ):
- [Could-have 1]
- [Could-have 2]

🚀 เริ่มสร้าง UI เลยนะครับ...
```

---

## Customization

User can always:
- Add features: "เพิ่มระบบ loyalty ด้วย"
- Remove features: "ไม่ต้องมี inventory"
- Modify features: "อยากให้ POS รองรับหลายสาขา"

AI should adapt the template based on user's additional input.

---

## Integration with Other Skills

This skill works with:
- `ui-first-builder` - Creates UI based on business template
- `engineer-harness` - Suggests next steps based on business type
- `integrations` - Recommends relevant integrations (e.g., payment for e-commerce)

---

*Last Updated: 2024-12-03*
