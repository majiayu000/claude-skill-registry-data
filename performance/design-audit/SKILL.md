---
name: design-audit
description: Web design & portfolio audit framework based on Ran Segall's (Flux Academy) 30-Second First Impression Test and Satori Graphics' LIFT System. Evaluates UIs for instant clarity, visual hierarchy, work visibility, trust signals, LIFT composition flow, and conversion readiness.
triggers:
  - /design-audit
  - design-audit
  - design audit
  - audit portfolio
  - audit web UI
  - review portfolio
  - lift audit
---

# Web & Portfolio Design Audit Framework (`design-audit`)

This skill audits and optimizes web user interfaces, landing pages, and portfolio websites using Ran Segall's (Flux Academy) **30-Second First Impression Audit Criteria** and Satori Graphics' **LIFT System Composition Protocol**.

---

## ⏱️ The 30-Second First Impression Rule

Recruiters and prospective clients review hundreds of portfolios and websites. They decide whether to hire a designer or leave the site in **30 seconds or less**.

```
0s ─────────────── 5s ────────────────── 15s ────────────────── 30s
[Load & OG Check]  [Hero Hook & Visibility]  [Hierarchy & Work Audit]  [Conversion Decision]
```

---

## 🔍 6-Point Audit Checklist (Including LIFT Protocol)

### 1. Load Performance & Social Sharing (0s - 5s)
* ⚡ **Page Load Speed:** Page must load fully in under 3 seconds. Avoid heavy JS spinners.
* 🖼️ **Open Graph (OG) Image & Title:** Social links shared on X, LinkedIn, or Discord MUST have custom high-res OG preview images and clear titles.

### 2. Immediate Work Visibility & Clarity (5s - 15s)
* 👁️ **Don't Hide the Work:** NEVER force visitors to click, unlock, or hover endlessly just to see core work. Show high-fidelity visual mockups immediately upon scrolling.
* 🚫 **Avoid Confusing Over-Creativity:** Do not build complex mini-game UIs or OS desktop simulators where visitors get lost.
* 🙋 **Clear Identity & Photo:** For freelancers and designers, displaying a professional photo builds instant trust.

### 3. Design Fundamentals, Hierarchy & Luxury Space (15s - 20s)
* 🔤 **Typography Hierarchy:** Limit to max 2 font families with clear scale contrast (e.g. Major Third 1.25x scale).
* 🎨 **Color & 60-30-10 Distribution:** High WCAG contrast ratios. No color chaos.
* 📐 **"Space is Wealth" (Luxury White Space):** Ensure generous white space around elements. Eliminate unnecessary divider lines (`<hr>`) or heavy card borders.

### 4. Micro-Interactions & Experience (20s - 25s)
* ✨ **Tasteful Micro-Interactions:** Subtle hover scaling, smooth preview transitions.
* 📱 **Mockup Authenticity:** Show realistic device mockups without overly distorted perspective angles.

### 5. 🏗️ The LIFT System Composition Audit (25s - 28s)
* 🎯 **L — Leverage Point Check:** Is there ONE dominant visual hero element that commands immediate attention? Are competing elements pushed back?
* 👁️ **I — Internal Rhythm Check:** Does the eye flow logically from the Leverage Point through secondary details without confusion?
* 🌶️ **F — Friction & Flow Check:** Is visual friction (overlapped text, tight line-heights) used sparingly like seasoning, or is it creating chaotic noise?
* 📱 **T — Transferability Check:** Does the layout hold up when scaled down to a mobile thumbnail or transferred across light/dark backgrounds?

### 6. Trust Signals & Conversion CTA (28s - 30s)
* 🤝 **Social Proof:** Display client logos, industry awards, or testimonials prominently.
* 🎯 **Prominent Call-to-Action (CTA):** Follow the Scrolling CTA Frequency Rule (1 in Hero, 1 in Nav, visible CTA every 2-3 seconds of scrolling).

---

## 📊 Audit Scorecard & Agent Execution Protocol

When executing `/design-audit` or reviewing a webpage/portfolio, the agent MUST generate a structured audit report using this scorecard format:

```markdown
# 🔍 30-Second & LIFT Design Audit Report

## 📈 Executive Summary Score: [88 / 100]

| Audit Dimension | Status | Key Observations & Required Fixes |
| :--- | :---: | :--- |
| **1. Speed & OG Sharing** | ✅ PASS | Loads in 1.2s. Custom OG Image verified. |
| **2. Work Visibility & Hero Hook**| ⚠️ WARN | Hero text is clear, but work is hidden behind hover tabs. Show 2 featured projects immediately. |
| **3. Typography & Hierarchy** | ❌ FAIL | 4 font families used. Heading contrast is too low (light gray on white). |
| **4. Micro-Interactions** | ✅ PASS | Smooth hover scale on cards. |
| **5. LIFT Composition Protocol** | ⚠️ WARN | Leverage point is weak; primary CTA competes with secondary badges. Increase CTA contrast. |
| **6. Trust & Conversion CTA** | ⚠️ WARN | CTA button is too small. Add client logos or testimonial section. |

## 🛠️ Priority Action Plan
1. **Fix Work Visibility:** Unhide case study cards; render top 2 featured projects directly in the body flow.
2. **Strengthen Leverage Point:** Increase scale and contrast of the primary CTA button.
3. **Consolidate Fonts:** Reduce font families to 2 (e.g., Playfair Display + Manrope).
```

---

## 💡 Quick Fix Code Patterns

### OG Image Head Tags Template
```html
<meta property="og:title" content="Jane Doe — Senior Product Designer" />
<meta property="og:description" content="Building high-impact digital products and design systems." />
<meta property="og:image" content="https://yourdomain.com/og-preview.jpg" />
<meta name="twitter:card" content="summary_large_image" />
```

### Bento Grid Clean Work Section Layout
```html
<section class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 p-8 max-w-7xl mx-auto">
  <div class="group relative overflow-hidden rounded-2xl border border-neutral-200 bg-neutral-50 p-6 transition-all hover:shadow-xl">
    <img src="/work-preview-1.jpg" alt="Case Study 1" class="rounded-lg object-cover transition-transform duration-300 group-hover:scale-105" />
    <h3 class="mt-4 text-xl font-bold tracking-tight text-neutral-900">Project Alpha</h3>
    <p class="text-sm text-neutral-600">Product Design & Mobile App</p>
  </div>
</section>
```
