---
name: integrations
description: >
  One-request, complete setup of external services — payment (Stripe, PromptPay,
  Omise, 2C2P), email, auth, analytics, storage and other integrations, including
  Thai-market services. Installs SDKs, creates API routes, env templates, and UI
  components in one pass. Use when the user asks to add payments, email, login,
  analytics, or any third-party service (e.g. "เพิ่มระบบชำระเงิน").
user-invocable: false  # internal — model-invoked via toh-* commands, not a user /command
---
# 🔌 Integrations Skill

> **Purpose:** One-click setup for external services
> **Version:** 1.0.0
> **Author:** Toh Framework Team

## Overview

This skill enables easy integration with external services like payment, email, analytics, etc. User just says what they want, AI handles all the setup.

## Core Principle

```
User says: "เพิ่มระบบชำระเงิน"
AI does: Install SDK, create API routes, setup env template, create UI components
User sees: "เพิ่ม Stripe/PromptPay แล้วครับ! ใส่ API key ใน .env แล้วใช้ได้เลย"
```

**ONE REQUEST = COMPLETE SETUP**

---

## Available Integrations

### 💳 Payment

| Service | Trigger Words | Thai Market |
|---------|---------------|-------------|
| Stripe | stripe, credit card, บัตรเครดิต | ✅ |
| PromptPay | promptpay, พร้อมเพย์, QR | ✅ Thai |
| Omise | omise, โอมิเซะ | ✅ Thai |
| 2C2P | 2c2p | ✅ Thai |

### 📧 Email

| Service | Trigger Words |
|---------|---------------|
| Resend | resend, email |
| SendGrid | sendgrid |
| Nodemailer | nodemailer, smtp |
| Postmark | postmark |

### 📊 Analytics

| Service | Trigger Words |
|---------|---------------|
| Google Analytics | ga, google analytics, วิเคราะห์ |
| Plausible | plausible, privacy analytics |
| Mixpanel | mixpanel |
| PostHog | posthog |

### 🔐 Authentication

| Service | Trigger Words |
|---------|---------------|
| Supabase Auth | supabase, auth (default) |
| NextAuth | nextauth, oauth |
| Clerk | clerk |
| Auth0 | auth0 |

### 📱 Messaging

| Service | Trigger Words |
|---------|---------------|
| LINE Notify | line notify, แจ้งเตือน line |
| LINE Messaging API | line messaging, line bot |
| Twilio SMS | twilio, sms |
| Firebase FCM | push notification, fcm |

### 📁 Storage

| Service | Trigger Words |
|---------|---------------|
| Supabase Storage | storage (default) |
| Cloudinary | cloudinary, image upload |
| AWS S3 | s3, aws storage |
| Uploadthing | uploadthing |

---

## Integration Templates

### 💳 Stripe Integration

**Trigger:** "เพิ่มระบบชำระเงิน Stripe" / "add payment"

**AI Creates:**

```
lib/
├── stripe.ts              # Stripe client setup
├── stripe-helpers.ts      # Helper functions
app/api/
├── checkout/route.ts      # Create checkout session
├── webhook/route.ts       # Handle webhooks
components/
├── PaymentButton.tsx      # Checkout button
├── PaymentSuccess.tsx     # Success page
.env.local (template)
├── STRIPE_SECRET_KEY=
├── STRIPE_PUBLISHABLE_KEY=
├── STRIPE_WEBHOOK_SECRET=
```

**Response:**

```markdown
✅ **เพิ่มระบบชำระเงิน Stripe แล้วครับ!**

📁 ไฟล์ที่สร้าง:
- lib/stripe.ts - Stripe client
- app/api/checkout/route.ts - API สร้าง checkout
- app/api/webhook/route.ts - รับ webhook
- components/PaymentButton.tsx - ปุ่มชำระเงิน

⚙️ **ขั้นตอนถัดไป:**
1. ไปที่ https://dashboard.stripe.com/apikeys
2. Copy API keys ใส่ใน `.env.local`:
   ```
   STRIPE_SECRET_KEY=sk_test_xxx
   STRIPE_PUBLISHABLE_KEY=pk_test_xxx
   ```
3. ใช้งานได้เลย!

💡 ต้องการทดสอบ payment flow ไหมครับ?
```

---

### 💳 PromptPay QR Integration

**Trigger:** "เพิ่ม PromptPay" / "พร้อมเพย์"

**AI Creates:**

```
lib/
├── promptpay.ts           # PromptPay QR generator
components/
├── PromptPayQR.tsx        # QR display component
├── PaymentConfirm.tsx     # Manual confirmation
app/api/
├── generate-qr/route.ts   # Generate QR API
```

**Response:**

```markdown
✅ **เพิ่มระบบ PromptPay แล้วครับ!**

📁 ไฟล์ที่สร้าง:
- lib/promptpay.ts - สร้าง QR code
- components/PromptPayQR.tsx - แสดง QR
- components/PaymentConfirm.tsx - ยืนยันการชำระ

⚙️ **ตั้งค่า:**
ใส่เบอร์โทร/เลขบัตรประชาชน ใน `.env.local`:
```
PROMPTPAY_ID=0812345678
```

💡 หมายเหตุ: PromptPay ไม่มี webhook
ต้องให้ user กดยืนยันว่าโอนแล้ว หรือเชื่อม bank API ครับ
```

---

### 📧 Email with Resend

**Trigger:** "เพิ่มระบบส่งอีเมล" / "add email"

**AI Creates:**

```
lib/
├── email.ts               # Email client
├── email-templates/       # Email templates
│   ├── welcome.tsx
│   └── order-confirmation.tsx
app/api/
├── send-email/route.ts    # Send email API
```

**Response:**

```markdown
✅ **เพิ่มระบบส่งอีเมลแล้วครับ!**

📁 ไฟล์ที่สร้าง:
- lib/email.ts - Email client (Resend)
- lib/email-templates/ - Email templates
- app/api/send-email/route.ts - API ส่งอีเมล

⚙️ **ตั้งค่า:**
1. ไปที่ https://resend.com/api-keys
2. ใส่ API key ใน `.env.local`:
   ```
   RESEND_API_KEY=re_xxx
   ```

💡 พร้อมใช้งานแล้ว! ต้องการเพิ่ม template อีเมลไหมครับ?
```

---

### 📊 Google Analytics

**Trigger:** "เพิ่ม analytics" / "google analytics"

**AI Creates:**

```
components/
├── GoogleAnalytics.tsx    # GA script component
app/
├── layout.tsx             # (modified to include GA)
lib/
├── analytics.ts           # Track events helper
```

**Response:**

```markdown
✅ **เพิ่ม Google Analytics แล้วครับ!**

📁 ไฟล์ที่สร้าง/แก้ไข:
- components/GoogleAnalytics.tsx
- lib/analytics.ts - Helper functions
- app/layout.tsx - เพิ่ม GA script

⚙️ **ตั้งค่า:**
1. ไปที่ https://analytics.google.com
2. สร้าง property ใหม่ แล้ว copy Measurement ID
3. ใส่ใน `.env.local`:
   ```
   NEXT_PUBLIC_GA_ID=G-XXXXXXXXXX
   ```

💡 ใช้ `trackEvent('button_click', { name: 'buy' })` เพื่อ track events ครับ
```

---

## Quick Integration Commands

User can say:

| Command | AI Does |
|---------|---------|
| "เพิ่ม payment" | Add Stripe (default) |
| "เพิ่ม PromptPay" | Add PromptPay QR |
| "เพิ่ม email" | Add Resend |
| "เพิ่ม analytics" | Add Google Analytics |
| "เพิ่ม auth" | Add Supabase Auth (usually already there) |
| "เพิ่ม push notification" | Add Firebase FCM |
| "เพิ่ม LINE notify" | Add LINE Notify |
| "เพิ่ม image upload" | Add Cloudinary/Supabase Storage |

---

## Smart Recommendations

Based on business type, AI suggests relevant integrations:

| Business Type | Recommended Integrations |
|--------------|-------------------------|
| E-commerce | Stripe, PromptPay, Email (order confirm), Analytics |
| F&B | PromptPay, LINE Notify (orders), Receipt/Bill |
| Booking | Email (reminders), Calendar sync, SMS |
| SaaS | Stripe (subscription), Email, Analytics, Auth |

**AI Prompt:**

```markdown
💡 สำหรับ [Business Type] แนะนำให้เพิ่ม:
1. [Integration 1] - [why]
2. [Integration 2] - [why]

ต้องการเพิ่มตัวไหนครับ?
```

---

## Environment Variables Template

After adding integrations, AI updates `.env.local.example`:

```bash
# === Supabase ===
NEXT_PUBLIC_SUPABASE_URL=
NEXT_PUBLIC_SUPABASE_ANON_KEY=
SUPABASE_SERVICE_ROLE_KEY=

# === Stripe ===
STRIPE_SECRET_KEY=
STRIPE_PUBLISHABLE_KEY=
STRIPE_WEBHOOK_SECRET=

# === PromptPay ===
PROMPTPAY_ID=

# === Email (Resend) ===
RESEND_API_KEY=

# === Analytics ===
NEXT_PUBLIC_GA_ID=

# === LINE ===
LINE_NOTIFY_TOKEN=
LINE_CHANNEL_SECRET=
LINE_CHANNEL_ACCESS_TOKEN=
```

---

## Error Handling

If user requests integration that needs prerequisite:

```markdown
⚠️ **ก่อนเพิ่ม [Integration]**

ต้องมี [Prerequisite] ก่อนครับ:
- [What's missing]

💡 ต้องการให้เพิ่ม [Prerequisite] ก่อนไหมครับ?
```

---

## Best Practices

### DO:
- ✅ Create complete, working integration
- ✅ Include all necessary files
- ✅ Provide clear .env setup instructions
- ✅ Add error handling in API routes
- ✅ Include example usage

### DON'T:
- ❌ Leave incomplete setup
- ❌ Forget webhook handling
- ❌ Skip error handling
- ❌ Use hardcoded credentials

---

*Last Updated: 2024-12-03*
