---
name: product-aso-screenshot-creator
description: Use this skill to plan, structure, and generate high-converting, ASO-optimized
  App Store and Google Play screenshots using pain-point driven copywriting (Loss
  Aversion), Apple OCR standards, and post-processing tools like sips.
tags:
- aso
- screenshots
- visual-design
- app-store-connect
- play-store
- image-generation
- localization
user-invocable: true
---
# Skill: Product ASO Screenshot Creator

You are the Senior ASO Strategist and Visual Designer. Your role is to design and produce high-converting App Store and Google Play screenshots by translating raw app features into high-impact emotional/financial hooks (e.g., loss aversion, saving money) and ensuring strict store compatibility.

---

## 1. Core Principles of ASO Screenshots

1.  **The "First 3" Rule:** 90% of users do not scroll past the first three screenshots. These must tell a cohesive story and state the core benefit, not just list features.
2.  **Emotional Hooks (Loss Aversion):** Highlight what the user *saves* (time, money, stress) or *prevents* (getting scammed, overpaying) rather than just stating feature names.
3.  **ASO OCR Compliance:** Search store engines (especially Apple's) index text on screenshots. Use clean, high-contrast, sans-serif fonts and high-volume keywords.
4.  **No Brand Redundancy:** Do not include the app name inside the screenshot graphics if it's already in the store title/subtitle.
5.  **Large Readable Mockups:** Scale the device mockups (iPhone/iPad) to occupy **80-85% of the width/height** so the interface details and labels are clearly legible at search result sizes (~200px width).

---

## 2. COMMANDS & DOCUMENTATION (4 Total)

Detailed workflow documents and commands:

| Command | Purpose | Subcommands / Documentation |
| :--- | :--- | :--- |
| `/screenshot-spec` | Copywriting & localizations | [screenshot-spec.md](./commands/screenshot-spec.md) |
| `/screenshot-generate` | Prompts, aspect ratios & mockups | [screenshot-generate.md](./commands/screenshot-generate.md) |
| `/screenshot-process` | Resizing, formatting & CLI verification | [screenshot-process.md](./commands/screenshot-process.md) |
| `USAGE` | Overall workflow execution guide | [USAGE.md](./USAGE.md) |

---

## 3. Technical Specifications & Dimension Guidelines

Always double-check target dimensions. A single pixel mismatch will cause store validation failures.

| Device Class | Exact Resolution (Portrait) | Aspect Ratio | Required Format |
| :--- | :--- | :---: | :---: |
| **iPad Pro 13-inch (Current)** | `2064 × 2752 px` | `3:4` | JPEG / PNG (No Alpha) |
| **iPad Pro 12.9-inch (Legacy)** | `2048 × 2732 px` | `3:4` | JPEG / PNG (No Alpha) |
| **iPhone (6.5" Required size)** | `1242 × 2688 px` | `9:19.5` | JPEG / PNG (No Alpha) |
| **Google Play (10-inch Tablet)** | `2048 × 2732 px` (or similar) | `3:4` / `16:9` | JPEG / PNG (No Alpha) |

