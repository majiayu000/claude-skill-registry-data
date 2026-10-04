---
name: build-funnel
description: Build conversion-optimized marketing funnels and landing pages with psychological triggers, animations, and analytics tracking.
---

# Build Conversion Funnel

**IMPORTANT**: For full-stack funnels with backend, see @project-scaffolding.md for the complete master project template.

## Funnel Flow
Traffic -> Landing Page -> Lead Magnet -> Email Sequence -> Sales Page -> Checkout -> Upsell -> Thank You -> Retention

## Required Sections (in order)
1. **Hero** — Gradient bg, animated particles, power headline, CTA, social proof badges
2. **Problem/Agitation** — 3-5 pain points with icons, emotional language
3. **Solution** — Feature showcase with animations, video demo embed
4. **Social Proof** — Testimonials, case studies, stats counters, real-time notification popup
5. **Pricing** — 3-tier anchor pricing, "Most Popular" badge, comparison table, guarantee
6. **FAQ** — Accordion, addresses top objections
7. **Final CTA** — Urgency (countdown timer), risk reversal, exit-intent popup

## Design System
- Background: gray-950 (#030712)
- Primary gradient: cyan-500 (#06b6d4) to pink-500 (#ec4899)
- Urgency: red-500, yellow-400
- Fonts: Inter (body), Poppins (headings), Space Grotesk (accents)
- ALL animations use Framer Motion (scroll-triggered, hover, entrance)
- Mobile-first responsive

## Analytics (wire up all of these)
- Google Analytics 4 (page views, events)
- Facebook Pixel (standard events)
- Track: CTA clicks, form submissions, scroll depth, time on page

## Tech
- Next.js 15 App Router + Tailwind + Framer Motion + shadcn/ui
- Deploy to Cloudflare Pages
