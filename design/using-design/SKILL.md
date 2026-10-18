---
name: using-design
description: Master Antigravity Web Design Suite. Coordinates 4 specialized design skills (design-setup for 0->1 prototyping, design-rules for micro-UI CSS/Tailwind rules & LIFT system, design-audit for 30-second first impression reviews, and design-psychology for 3-brain personas & luxury white space). Includes full research video transcript library.
triggers:
  - /design
  - design
  - web design
  - design suite
---

# Master Antigravity Web Design Suite (`design`)

This skill acts as the master orchestrator and entry point for the **Antigravity Web Design Ecosystem**, bringing together 8 world-class web design research frameworks into 4 specialized modular skills and a central research reference library.


> **Anti-slop:** when the page must not look AI-templated, or needs a named style, tokens, or a polish pass, route through **`using-anti-slop`** — it chains back here for the build and to `design-ship-gate` for done. **3D, canvas, motion or scroll effects:** route through **`using-web3d`**.

---

## 🏛️ Suite Structure & Modular Sub-Skills

```
d:\Github\xeno-skills\skills\design\
├── 📄 SKILL.md                 <-- Master Entrypoint & Router (This File)
├── 🎨 design-setup/            <-- 0->1 Setup, 5-Style Wide Net, 3 Body Layouts, MCP Hero, Tweaks Bar
│   └── SKILL.md
├── 📐 design-rules/            <-- Micro-UI CSS/Tailwind Rules, Major Third Scale, LIFT System, 60-30-10
│   └── SKILL.md
├── 🔍 design-audit/            <-- 30-Second First Impression Audit, 50 Portfolio Case Studies, LIFT Audit
│   └── SKILL.md
├── 🧠 design-psychology/       <-- 3-Brain Personas, MAYA Principle, Cognitive Chunking, Space is Wealth
│   └── SKILL.md
└── 📚 references/              <-- Full Untruncated Video Transcript Reference Library (8 Videos)
    ├── README.md
    ├── 01_chase_ai_anti_slop_web_design.md
    ├── 02_flux_academy_50_portfolio_reviews.md
    ├── 03_kole_jain_every_ui_ux_concept.md
    ├── 04_chris_mccoy_psychology_of_perfect_website.md
    ├── 05_chris_mccoy_5_web_design_skills.md
    ├── 06_chris_mccoy_6_habits_of_design_legends.md
    ├── 07_flux_academy_luxury_white_space.md
    └── 08_satori_graphics_layout_composition_lift_system.md
```

---

## 🧭 Sub-Skill Navigation & When to Use Which

| Sub-Skill | Access / Trigger | Primary Use Case & Research Source |
| :--- | :--- | :--- |
| **🎨 `design-setup`** | `/design-setup` | **0 ➔ 1 Prototyping & Layout Building:** Cast a wide net across 5 aesthetic directions, 3 body layout options, 2-pass Higsfield MCP hero background generation, and live Dev Server Tweaks Bar. *(Chase AI, Chris McCoy)* |
| **📐 `design-rules`** | `/design-rules` | **Micro-UI & Engineering Standards:** Headline Pro tracking hack (`-0.025em`), Major Third (`1.25x`) type scale, 60-30-10 color balance, 8pt grid, dark mode elevation, LIFT composition, and Luxury White Space. *(Kole Jain, Ran Segall, Satori Graphics)* |
| **🔍 `design-audit`** | `/design-audit` | **30-Second First Impression & Conversion Audit:** Audits portfolios/landing pages for speed, Open Graph tags, unhidden work, WCAG contrast, trust signals, and LIFT composition flow. *(Ran Segall - Flux Academy)* |
| **🧠 `design-psychology`** | `/design-psychology` | **Behavioral Science & Perceived Value:** Aligns UIs with 3 Brain Personas (Survival/Mental Models, Emotional/MAYA Principle, Rational/3-4 Item Chunking) and "Space is Wealth" luxury positioning. *(Chris McCoy, Ran Segall)* |
| **🚦 `design-ship-gate`** | `/design-ship-gate` | **Done-Gate for a Small Model:** brief-coverage table, then nine executable checks with pass conditions — every script parses, font count, Open Graph, dark mode and stat visibility, 390 px overflow, hero collisions, number/unit wrapping, tracking. Calibrated on nine Qwen3.8-27B pages (#353, #375). Run before calling a page finished. |

### Library skills — load the one the page's code uses (vendored, #382)

Load these **by name with the Skill tool** the moment the page's stack includes the library, before writing that part of the code. They carry the library's API and pitfalls; the design sub-skills above carry none of it.

| the page uses | load | for |
| :--- | :--- | :--- |
| scroll-linked animation, pinning, parallax (GSAP) | **`gsap-scrolltrigger`** | ScrollTrigger config, `scrub`, `pin`, `batch`, cleanup and refresh |
| Three.js animation — GLTF clips, skeletal, morph targets, procedural motion | **`threejs-animation`** | `AnimationMixer`, `AnimationAction`, clip blending |
| React Three Fiber / drei / zustand in the 3D scene | **`r3f-best-practices`** | never `setState` in `useFrame`, delta time, Suspense loading, selectors |
| driving a real browser — open the page, click, read console, screenshot | **`playwright-cli`** | the `playwright-cli` commands; used by the Ship Gate step to look at the rendered page |

---

## 🔄 Cross-Skill Integration Workflow

When building or overhauling a web design, the agent automatically executes across the sub-skills in this order:

1. **Setup Phase (`design-setup`):** Checks preflight dependencies, prompts user for inspiration (or recommends Dribbble/Pinterest/TypographicPosters), and initiates 3-phase wide net generation.
2. **Rule Enforcement (`design-rules`):** Automatically applies `-2%` tracking, 4pt/8pt grid spacing, 4-state buttons, dark mode surface elevation, and 60-30-10 color balance during code generation.
2b. **Library Phase:** before writing GSAP, Three.js or R3F code, load its library skill from the table above (`gsap-scrolltrigger`, `threejs-animation`, `r3f-best-practices`).
3. **Psychology Alignment (`design-psychology`):** Ensures macro layout respects Mental Models (Brain #1), incorporates MAYA pattern breaks (Brain #2), and chunks pricing/features into max 3-4 categories (Brain #3).
4. **Audit & Review (`design-audit`):** Runs the 30-Second First Impression Audit & LIFT Scorecard to verify conversion readiness and visual impact before shipping to production.
5. **Ship Gate (`design-ship-gate`):** Runs the nine executable checks and pastes their outputs; `GATE: 9/9` with outputs is the only "done". To look at the rendered page and its console while fixing what the gate found, load `playwright-cli`.

---

## 📚 Transcript Reference Library

Access full, untruncated research transcripts for all 8 YouTube videos in [references/README.md](../references/README.md).

## At session end — record what actually happened

These design skills are read literally by an agent, so a rule that does not transfer is invisible until a session goes wrong and somebody reconstructs it from a transcript afterwards.

**Before the session ends, report each rule that did not hold** as a `skill-feedback` issue on `xenodeve/xeno-skills`, whichever repo you were working in. Search `--state all` first and **comment on the existing issue rather than opening a second** — one issue per rule, so the comment count is the frequency. Pass `--repo xenodeve/xeno-skills` on every call; `gh` defaults to the repo you are standing in. Record which of these skills fired, which of their rules did not hold, and which rule you followed that still produced the wrong output — **including the embarrassing cases, especially those.** A log of only the memorable sessions is a failure-selected sample.

The rules, the skeleton and the read-trigger live in **`t4-agent-memory`** — load it rather than working from this paragraph. If you cannot reach the tracker, say so in the session report instead of skipping quietly.
