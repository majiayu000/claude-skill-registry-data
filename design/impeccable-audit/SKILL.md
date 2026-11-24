---
name: impeccable-audit
description: "Audit Mikka interface craft and UX resilience using an adapted Impeccable quality lens. Use for visual hierarchy, density, touch, motion, typography, focus and responsive correctness; never introduce a competing design system or modify paid UI internals."
---

# Impeccable audit — Mikka adapter

Inspired by https://github.com/pbakaus/impeccable (audit skill). This is Mikka-authored guidance, **not** a copied upstream command pack, and does not include the upstream setup scripts.

The operating surface is a dense coding/work SaaS: precision and restraint override generic landing-page polish. Read `docs/design/README.md`, `docs/design/rules.md`, `docs/design/components.md`, accepted Figma and the running official UI. In any conflict use Mikka's documented authority. Never regenerate tokens, fonts, palette, buttons or an alternative shell. BoardUI Pro, affectUI and beUI Pro retain their native supplied internals.

At local production-renderer sizes, inspect: information hierarchy and scan path; navigation and affordance visibility; popover/dialog/tooltip placement; keyboard/focus and touch targets; responsive split panes and wrapping; long localized content and zoom; theme contrast and icon+label meaning; loading/empty/error/success recovery; reduced motion and perceived input latency. Check consistency of meaningful business behavior before cosmetic matching.

Each concern requires a real screen/route, exact input, screenshot or accessible-tree evidence, severity and impact, the existing component that should implement the correction, and a regression plan. If only source or an old screenshot was inspected, mark unverified. Audit output routes to issue ownership and verified fixes; this skill does **not** authorize speculative full-screen redesign.
