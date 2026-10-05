---
name: cm-growth-hacking
description: "Bottom-sheet and popup growth system: booking CTAs, calendars, lead capture, surveys, re-engagement, with CRO tracking hooks. Zero-deps; works static or dynamic sites. Works with cm-booking-calendar, cm-ads-tracker, cm-google-form, cm-readit, cm-ux-master."
allowed-tools: Read, Write, Edit, Glob, Grep, Browser
version: 1.0
priority: HIGH
skills:
  - cm-booking-calendar
  - cm-ads-tracker
  - cm-google-form
  - cm-readit
  - cm-ux-master
---

# CM Growth Hacking

> **Bottom Sheet + Calendar + Trigger + Tracking = Growth Hacking Engine.**
> Đa ngành, đa mục đích, zero dependencies.
> 1 skill = mọi growth hacking pattern bạn cần.

---

## 🎯 When to Use

| Trigger | Action |
|---------|--------|
| User says "bottom sheet", "popup" | Activate — start Phase 1 |
| User says "đặt lịch popup", "booking bottom sheet" | Activate — focus booking sheet |
| User says "lead capture", "exit intent" | Activate — focus lead capture |
| User says "nhắc lịch", "google calendar", "apple calendar" | Activate — focus calendar CTA |
| User says "flash sale popup", "countdown" | Activate — focus promo sheet |
| User says "survey", "đánh giá", "feedback" | Activate — focus survey sheet |
| User says "tăng conversion", "giảm bounce" | Activate — explain + build |

---

## 📖 Selective Reading Rule (MANDATORY)

| File | Status | When to Read |
|------|--------|--------------|
| [bottom-sheet-engine.md](bottom-sheet-engine.md) | 🔴 REQUIRED | Any bottom sheet implementation |
| [trigger-system.md](trigger-system.md) | 🔴 REQUIRED | Setting up when/how sheets appear |
| [calendar-integration.md](calendar-integration.md) | ⚪ Optional | When sheet includes calendar CTA |
| [tracking-events.md](tracking-events.md) | ⚪ Optional | When tracking engagement events |

> 🔴 **Always read `bottom-sheet-engine.md` + `trigger-system.md` first.**

---

## 🧭 Quick Decision Tree

```
"I need an engagement popup"
│
├─ Booking / Appointment
│  └─ bottom-sheet-engine + calendar-integration + cm-booking-calendar
│     └─ Form → Sheet: cm-google-form
│     └─ Post-submit: Calendar CTA (GCal + ICS)
│
├─ Lead Capture / Exit Intent
│  └─ bottom-sheet-engine + trigger-system (exit-intent)
│     └─ Form → Sheet: cm-google-form
│     └─ Tracking: cro_lead_capture
│
├─ Flash Sale / Promo
│  └─ bottom-sheet-engine + trigger-system (timer)
│     └─ Countdown timer + CTA
│     └─ Optional: Calendar deadline
│
├─ Survey / Feedback
│  └─ bottom-sheet-engine + trigger-system (post-interaction)
│     └─ Star rating or NPS
│     └─ Form → Sheet: cm-google-form
│
├─ Event / Webinar Registration
│  └─ bottom-sheet-engine + calendar-integration
│     └─ Register → Add to Calendar
│     └─ Tracking: cro_event_register
│
├─ Re-engagement (Return Visitor)
│  └─ bottom-sheet-engine + trigger-system (return-visitor)
│     └─ "Welcome back" + personalized CTA
│
└─ Chat / Contact CTA
   └─ bottom-sheet-engine + trigger-system (scroll)
      └─ Zalo / Messenger / Hotline buttons
```

---

## 📋 6-Phase Workflow

```
Phase 1: DISCOVER → Scan site, detect industry, identify existing popups/forms
Phase 2: SOCRATIC GATE → Ask strategic questions (max 5)
Phase 3: CONFIGURE → Select engagement pattern + customize
Phase 4: BUILD → Generate bottom sheet + triggers + calendar + tracking
Phase 5: INTEGRATE → Wire to site + link skills
Phase 6: VERIFY → Test all interactions + tracking events
```

> 🔴 **Rule:** NEVER skip Phase 1 & 2. Always scan first, ask second.

---

## Phase 1: DISCOVER

Scan the website to understand:

```bash
# Find existing popups/modals/sheets
grep -ri "modal\|popup\|bottom-sheet\|overlay\|dialog" --include="*.html" --include="*.astro" --include="*.css" .

# Find existing forms
grep -ri "data-form-type\|onsubmit\|<form" --include="*.html" --include="*.astro" .

# Find existing calendar code
grep -ri "VCALENDAR\|google.com/calendar\|\.ics\|VEVENT" --include="*.js" --include="*.html" .

# Find existing tracking
grep -ri "dataLayer\|fbq\|ttq\|gtag" --include="*.js" --include="*.html" .
```

**Output:** Discovery Report with detected industry, existing UI, and recommended pattern.

---

## Phase 2: SOCRATIC GATE

> 🔴 **MANDATORY.** Ask ALL in ONE message. Max 5 questions.

1. **Mục tiêu chính** — Bạn muốn popup/bottom sheet để làm gì? (đặt lịch / thu lead / khuyến mãi / survey / khác)
2. **Trigger** — Khi nào hiện? (ngay khi vào trang / scroll X% / sau X giây / khi sắp thoát / click nút)
3. **Nội dung** — Trong popup cần gì? (form / calendar CTA / countdown / rating / nút chat)
4. **Calendar** — Có cần thêm Google Calendar / Apple Calendar không? Nhắc trước bao lâu?
5. **Tracking** — Đang chạy ads platform nào? (Facebook / TikTok / Google / không)

---

## Phase 3: CONFIGURE

Based on answers, select from `references/engagement-patterns.md` and build config:

```javascript
const ENGAGEMENT_CONFIG = {
  type: 'booking',           // booking | lead | promo | survey | event | chat | reengagement
  trigger: {
    type: 'scroll',          // scroll | time | exit | click | return | interaction
    value: 0.3,              // scroll % or ms or selector
    delay: 0,                // additional delay after trigger
  },
  sheet: {
    size: 'standard',        // compact | standard | full
    title: 'Đặt Lịch Khám',
    icon: '📅',
    dismissible: true,
    swipeToDismiss: true,
  },
  calendar: {
    enabled: true,
    providers: ['gcal', 'ics'],  // gcal | ics | outlook
    reminderMinutes: [1440, 120], // 1 day + 2 hours before
    location: 'Google Maps URL',
  },
  tracking: {
    events: ['cro_sheet_shown', 'cro_booking_submit', 'cro_calendar_add'],
    conversionValue: 500000,
    currency: 'VND',
  },
  session: {
    dismissKey: 'eng_booking_dismissed',
    storage: 'sessionStorage',   // sessionStorage | localStorage
    maxShowPerSession: 1,
  }
};
```

---

## Phase 4: BUILD

Read and use templates from `templates/` directory:

| Template | Purpose |
|----------|---------|
| `templates/bottom-sheet.css` | Universal responsive bottom sheet CSS |
| `templates/bottom-sheet.js` | `BottomSheetEngine` class — create, show, hide, swipe, stack |
| `templates/calendar-cta.js` | Calendar button generators (GCal + ICS + device detection) |
| `templates/trigger-manager.js` | `TriggerManager` class — scroll, time, exit, click triggers |
| `templates/tracking-events.js` | DataLayer push helpers for engagement events |

---

## Phase 5: INTEGRATE

### Wire to Existing Skills

```
cm-growth-hacking (this skill)
│
├── UI Layer ──────────── templates/bottom-sheet.css + .js
│
├── Form Submit ───────── @skills/cm-google-form
│   └── submitToGoogleSheet() → success callback → show calendar CTA
│
├── Calendar Logic ────── @skills/cm-booking-calendar
│   └── calendar-engine.js (scheduling)
│   └── calendar-export.js (ICS + GCal deep link)
│   └── reminder-config.js (VALARM + industry patterns)
│
├── CRO Tracking ──────── @skills/cm-ads-tracker
│   └── dataLayer.push() → GTM → FB/TikTok/Google
│
└── Design Principles ─── @skills/cm-ux-master
    └── Color, typography, animation standards
```

---

## Phase 6: VERIFY

| # | Test Case | Expected |
|---|-----------|----------|
| 1 | Bottom sheet opens | Slides up with animation |
| 2 | Swipe down to dismiss | Sheet closes + state saved |
| 3 | Trigger fires correctly | Sheet appears at configured trigger |
| 4 | Form submit (if applicable) | Toast success → Calendar CTA appears |
| 5 | Google Calendar click | New tab with pre-filled event |
| 6 | ICS download click | .ics file downloads |
| 7 | .ics on iOS | Opens Apple Calendar with reminders |
| 8 | Tracking events fire | dataLayer shows correct events |
| 9 | Session dismiss works | Sheet doesn't reappear after dismiss |
| 10 | Mobile responsive | Sheet adapts to viewport |
| 11 | Accessibility | aria-labels, focus trap, Escape key |
| 12 | No conflict with existing UI | Doesn't break page layout |

---

## ❌ Anti-Patterns

| ❌ Don't | ✅ Do |
|----------|------|
| Hardcode content in sheet | Use config object |
| Show popup immediately on page load | Use trigger system with delay |
| No dismiss option | Always allow close + swipe |
| Forget mobile safe-area | Pad for notched devices |
| Skip tracking | Track every interaction |
| One-size-fits-all sheet | Use compact/standard/full variants |
| Autoplay anything | Require user interaction |
| Show on every page visit | Respect session/localStorage dismiss |
| Build calendar logic from scratch | Inherit from `cm-booking-calendar` |
| Build tracking from scratch | Inherit from `cm-ads-tracker` |

---

## 📑 Templates

| File | Purpose |
|------|---------|
| `templates/bottom-sheet.css` | Universal bottom sheet CSS (3 sizes) |
| `templates/bottom-sheet.js` | BottomSheetEngine class |
| `templates/calendar-cta.js` | Calendar CTA buttons + auto device route |
| `templates/trigger-manager.js` | TriggerManager class |
| `templates/tracking-events.js` | Engagement tracking helpers |

## 📚 References

| File | Purpose |
|------|---------|
| `references/engagement-patterns.md` | 10+ engagement patterns by industry |

---

## 🔗 Related Skills

| Need | Skill |
|------|-------|
| Calendar scheduling + export | `@[skills/cm-booking-calendar]` |
| Form → Google Sheet | `@[skills/cm-google-form]` |
| Full CRO tracking setup | `@[skills/cm-ads-tracker]` |
| Audio engagement | `@[skills/cm-readit]` |
| UI/UX design principles | `@[skills/cm-ux-master]` |
