---
name: jjba-website
description: Build a complete JoJo's Bizarre Adventure themed website template with 9 Part color themes, GSAP animations, Three.js particle fields, and full legal pages. Use when Rick wants a JJBA-anime styled business website.
---

# JJBA Website Template Build

Build a complete, production-ready JJBA-themed website template for RJ Business Solutions.

## The Build Order

Execute the complete JJBA website build as specified in the master prompt. This includes:

### Design System
- 9 Part color palettes (Phantom Blood through The JoJolands)
- Part Switcher that globally changes all CSS variables
- Manga effects: halftone dots, speed lines, panel borders, screen tones
- Typography: Bebas Neue, Cinzel, Inter, JetBrains Mono

### Animation Stack
- GSAP: Stand summon entrances, scroll reveals, counter animations
- Framer Motion: React transitions
- Three.js: Star particle field hero background

### Pages (All Required)
- Home (/): 9 sections with hero, features, stats, testimonials, pricing, CTA
- About (/about)
- Services (/services)
- Pricing (/pricing)
- Portfolio (/portfolio)
- Team (/team)
- Blog (/blog, /blog/[slug])
- Contact (/contact) with form + API endpoint
- FAQ (/faq)
- Legal: Privacy Policy, Terms of Service, Cookie Policy, Refund Policy, Disclaimer, Accessibility

### Components
- Navbar with Part Switcher
- Footer with newsletter
- 4 Popups: Cookie Consent, Welcome/Part Selector, Newsletter Exit-Intent, Service Inquiry
- Stand Stats Badge (A-E rank system)
- All UI components styled in JJBA theme

### Technical Requirements
- Next.js 15 App Router
- TypeScript strict mode
- Tailwind CSS
- shadcn/ui base
- Zustand for state
- Zod validation
- Resend for email
- Full SEO metadata + JSON-LD
- GDPR/CCPA compliant

### Deployment
- Vercel deployment
- GitHub Actions CI/CD
- Professional README.md
- CITATIONS.md

## Company Branding
- Company: RJ Business Solutions
- Owner: Rick Jefferson
- Email: rjbizsolution23@gmail.com
- Address: 1342 NM 333, Tijeras, New Mexico 87059

## Tech Stack
- Next.js 15, TypeScript, Tailwind CSS 3.4
- GSAP 3.12, Framer Motion 11, Three.js 0.162
- shadcn/ui, Zustand, React Hook Form, Zod
- Resend, Vercel

## Execution
Begin building from the project scaffold. Build every file completely with zero placeholders. Run tests and lint before completing. Deploy to Vercel and push to GitHub.

## After Building
1. Run `pnpm build` to verify
2. Run tests: `pnpm test:unit` and `pnpm test:e2e`
3. Deploy to Vercel
4. Push to github.com/rjbizsolution23-wq
