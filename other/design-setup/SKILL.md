---
name: design-setup
description: Complete end-to-end web design setup & prototyping framework faithful to Chase AI's methodology with production robustness gates. Automatically enforces design-rules (micro-UI typography hacks, 4pt/8pt grid, dark mode surface elevation, 4-state buttons) and legend mastery principles (unconventional inspiration, signature calling cards). Interactively guides users to cultivate design taste, enforces preflight checks, decision gates, exploratory code isolation, 4-part prompts, 3-phase build sequence, and token commit finalization.
triggers:
  - /design-setup
  - design-setup
  - design setup
  - initialize web design
  - setup website UI
  - overhaul web design
---

# Complete Web Design Setup Framework (`design-setup`)

This skill guides AI agents and users through setting up bespoke, high-taste web UIs and landing pages from scratch while systematically eliminating **AI Slop** (generic dark slate modes, cyan/purple gradients, default Inter fonts, 3D blobs, uniform 3-column cards, and cliché copy).

*Automatic Skill Integration:* During UI component and layout generation, this skill **automatically enforces micro-design rules from `design-rules`** (e.g., `-2%` headline tracking hack, 4pt/8pt grid spacing, dark mode surface elevation, 4-state buttons, semantic colors, and progressive backdrop blur overlays).

---

## ⛔ 0. Environment Preflight Check (Mandatory Pre-Run Audit)

Before initiating the design setup workflow, the agent MUST run a brief preflight check to verify that all necessary dependencies are in place:

1. **Skills Audit:** Verify if **Impeccable Skill** (`impeccable.style`), **Taste Skill** (v2), **UI/UX Pro Max**, and **`design-rules`** are active.
2. **MCP Connectivity:** Verify that **Higsfield MCP** CLI (`higsfield.ai`) is active and authenticated if background hero imagery/video is required.
3. **Dev Server Status:** Ensure local dev server (e.g., Vite, Next.js) and preview environment are ready.
4. **Inspiration Check:** Confirm if the user has provided reference screenshots, URLs, or an Inspiration Library brief.

*Action:* If any dependency is missing, prompt the user immediately before starting execution to prevent getting stuck midway.

---

## 🚫 1. Anti-Slop Guardrails & Micro-Rules Enforced

Enforce these strict negative constraints on EVERY UI generation task:

* ❌ **NO Generic Color Palettes:** Never default to `#0f172a` slate dark mode with cyan (`#06b6d4`) to purple (`#a855f7`) gradients.
* ❌ **NO Font Defaulting:** Never use `Inter` font without an explicit font scale and intentional pairing (e.g., Serif headline + Monospace label).
* ⚡ **Headline Pro Typography Hack (via `design-rules`):** Apply `-2%` to `-3%` letter-spacing (`tracking-tight`) and `110%-120%` line-height (`leading-tight`) on large heading text.
* 📐 **4pt/8pt Spacing Grid (via `design-rules`):** All padding, margin, and gap values MUST be exact multiples of 4 or 8.
* 🌙 **Dark Mode Surface Elevation (via `design-rules`):** Create depth in dark mode using lighter background surface colors (`#09090b` ➔ `#18181b` ➔ `#27272a`), NOT black drop shadows.
* 🔘 **4-State Buttons & Icon Line-Height (via `design-rules`):** Render Default, Hover, Active, Disabled button states. Match icon size to text line-height.
* ❌ **NO Cliché Elements:** No 3D glowing glassmorphism blobs, uniform 3-column feature cards with gray `border-slate-800`, or floating neon rings.
* ❌ **NO Vague Copywriting:** No generic AI headings like *"Ship products that think for themselves"*. Use authentic, product-specific copy.

---

## 🧭 2. Step 1: Cultivate & Curate Taste (Inspiration & Reference Protocol)

AI has no inherent taste and defaults to "regression to the mean." Before writing code, the user MUST cultivate taste and gather high-level design inspiration.

### 2.1 Standard & Unconventional Inspiration Sources
When asking the user for inspiration or references, provide these primary and unconventional sources:

#### Standard Sources:
1. **Dribbble (`dribbble.com`):** Search `web design` + filter by `Popular` to discover high-level landing page layouts.
2. **Pinterest (`pinterest.com`):** Search `web design` or `UI hero section` to find unconventional hero compositions.
3. **Twitter / X:** Follow active UI/UX design creators for cutting-edge, experimental UI patterns.

#### 🌟 Unconventional Sources (Look Where No One Else is Looking):
4. **Typographic Posters (`typographicposters.com`):** High-impact poster layouts & unconventional type arrangements.
5. **Savee (`savee.it`):** High-curation design community free of ad noise.
6. **Cross-Disciplinary Inspiration:** Architecture movements, design history books, museum exhibition layouts (synthesizing non-web fields creates ultra-original UIs).

### 2.2 Inspiration Library Web App & Copy Brief / Copy Image Prompt
To organize inspiration, the user can have Claude Code build a simple **Inspiration Library Web App** that groups screenshots into aesthetic categories and provides:
* **Design Vocabulary & Keywords:** Tags describing the visual style (e.g., *Voxel rendered landscape, Monolithic scale, High-contrast index*).
* **Copy Image Prompt Button:** Copies the image prompt to generate background hero imagery.
* **Copy Brief Button:** Copies the foundational design brief to paste directly into Claude Code.

*Agent Action:* Prompt the user:
> *"Before we build, do you have reference screenshots, URLs, or a copied Brief from your Inspiration Library? If not, tell me which aesthetic family (e.g., Print Tech, Dither Mono, Vast Quiet, Classical Remix) fits your vision!"*

---

## 🧰 3. Step 2: Equip External Tools & Calling Card Superpowers

### 3.1 ⚠️ Beware Going Down the Tool Rabbit Hole
Do NOT fall into the trap of installing hyper-prescriptive skills that promise to solve all design problems with one click. Narrow, prescriptive skills only produce one rigid output. Favor **flexible, non-prescriptive tools** (Impeccable, Taste Skill, Higsfield MCP) while utilizing popular UI repositories like UI/UX Pro Max for extra baseline rules.

### 3.2 External Ecosystem & Calling Card Matrix

| Tool / Skill | Access / Command | Primary Function |
| :--- | :--- | :--- |
| **`design-rules`** | Automatic Integration | Micro-UI engineering rules (Headline hack, 4pt/8pt grid, dark mode elevation, button states). |
| **Impeccable Skill** | `impeccable.style` | Audits 46 anti-slop patterns across 7 dimensions (*Typography, Color, Spatial, Responsiveness, Interaction, Motion, UX Writing*). Provides 23 commands (e.g., `/boulder`, `/clarify`, `/overdrive`) and Live Mode on Dev Server. |
| **Taste Skill (v2)** | `npx skills add Leonxlnx/taste-skill` | Enforces custom typography scales, spacing systems, and motion curves (`tasteskill.dev`). |
| **UI/UX Pro Max** | `github.com/nextlevelbuilder/ui-ux-pro-max-skill` | Popular comprehensive UI/UX design skill repository providing structured design guidelines, component patterns, and prompt rules. |
| **Higsfield MCP** | `higsfield.ai` (MCP CLI) | Model Context Protocol integration for generating custom background hero images (e.g., GPT Images 2) and ambient video loops (e.g., Seed Dance). |
| **21st.dev** | `21st.dev` | Component-level inspiration (Buttons, Cards, Pricing tables). Allows copying precise component prompts. |
| **Calling Card Tech** | GSAP / Spline 3D / WebGL | Signature interactive superpower technique (e.g., GSAP ScrollTrigger, 3D interactive assets) creating a distinct visual calling card. |

---

## 📁 4. Exploratory Code Scoping Policy

To prevent cluttering production codebase with abandoned components during design exploration:
* **Exploration Directory:** Place all multi-style explorations in isolated exploration routes/folders (e.g., `/design-exploration/style-1`, `/design-exploration/style-2`).
* **Production Route Protection:** Do NOT overwrite main production routes (e.g., `app/page.tsx` or `index.html`) until the user explicitly approves the final design direction.

---

## 📐 5. The 4-Part Prompt Structure

Every design setup prompt passed to the agent SHOULD contain these 4 components:

```markdown
1. Aesthetic Family: [e.g., Print Tech Paper, Dither Mono, Vast Quiet / Cinematic, Classical Remix, or Custom Hybrid]
2. Reference Image / URL: [Screenshots, Live URL, or Copied Brief from Inspiration Library]
3. Intent & Target Audience: [Product purpose, target audience, primary CTA e.g., Book Demo]
4. Guardrails: [Explicit constraints e.g., No purple gradients, no 3D blobs, no default Inter font]
```

---

## 🔄 6. Step 3: The 3-Phase Build Sequence & Hard Decision Gates

Never attempt a "One-Shot" design setup. Execute this exact iterative build sequence with **Hard Decision Gates**:

### Phase 1: Cast a Wide Net (5 Styles Comparison Grid)
Prompt the agent to generate **5 distinct versions** of the page across 5 different aesthetic styles in isolated exploration routes:
* Example Prompt: *"Setup a landing page for [Product Name], [Intent & CTA]. Guardrails: no purple gradients, no 3D blobs, no Inter font. Create 5 versions of the page in 5 different directions in /design-exploration/ (e.g., Print Tech Paper, Vast Quiet, Dither Mono, Classical Remix, Industrial Minimal)."*
* *Micro-Rule Enforcement:* Apply `design-rules` headline tracking (`-0.025em`) and 4pt/8pt grid spacing across all 5 versions.

> 🛑 **HARD GATE 1:** STOP. Do NOT proceed to Phase 2 until the user explicitly selects ONE direction from Phase 1.

---

### Phase 2: Explore Body Layout Variants (1 Style ➔ 3 Variants)
Once the user selects a preferred style from Phase 1 (e.g., *Vast Quiet*):
* Prompt the agent: *"Let's go with the Vast Quiet version. Generate 3 versions of that aesthetic for me, namely changing the body layout formats (e.g., Minimal Vertical Stack, Quiet Ledger with sticky left index, Framed Border Structure)."*
* *Micro-Rule Enforcement:* Render components using 4-state buttons, ghost buttons, and dark mode surface elevation.

> 🛑 **HARD GATE 2:** STOP. Do NOT proceed to Phase 3 until the user explicitly selects ONE body layout variant from Phase 2.

---

### Phase 3: 2-Pass Hero Image Generation via Higsfield MCP
Execute a 2-Pass image generation process using Higsfield MCP for the background hero asset:
1. **Pass 1 (Composition Options):** Prompt the agent: *"Let's nail that hero image. Give me 4 different high-quality 2K image compositions that fit our quiet aesthetic hero section using Higsfield MCP."* (e.g., *Aerial view, Crag mountain, Watercolor, Cloud Sea*).
2. **User Selection 1:** Select 1 composition (e.g., *Option 4: Cloud Sea*).
3. **Pass 2 (Color & Lighting Options):** Prompt the agent: *"Let's go with Option 4. Create multiple versions of that adding a splash of color (e.g., Dawn, Golden Hour, Alpenglow, Duotone)."*
4. **User Selection 2:** Select the final hero image (e.g., *Alpenglow*).

> 🛑 **HARD GATE 3:** STOP. Do NOT implement the final production page until the final hero asset is selected by the user.

---

## 🛠️ 7. Tweaks Bar & Page Motion Directives

### 7.1 Natural Prompting for Dev Server Tweaks Bar
Instead of guessing fixes in terminal text, prompt the agent to add an interactive **Tweaks Bar** to the preview page:

> **Prompt:** *"Can we sort of mimic what happens inside of Claude Design and add a tweaks bar that pops up on this dev server so I can change a number of things? Whether that's font size, font type, accent colors, hero asset variations, motion speed, reveal distance, or element weight. Go pretty aggressive with what you offer me."*

The agent will inject a floating control overlay on the dev server allowing visual tweaking of:
* Heading & Body Fonts (with Italics toggle and Font Size sliders)
* Hero Image Asset Variations toggle
* Motion Speed, Reveal Distance, and Element Weight / Stagger Delay
* Accent Colors and Spacing

### 7.2 Page Loading Weight & Transition Directives
* **Hero Transition:** The hero background MUST smoothly fade out into the body section upon scrolling (no sudden color cuts).
* **Page Loading Weight:** Page loading **MUST feel heavy and carry weight**. Use staggered reveal animations so elements load sequentially into place with tangible weight.

---

## 🏁 8. Finalization & Production Commit Phase

Once the design is approved by the user, execute this finalization checklist:

1. **Commit Selected Tweaks Values:** Extract the user's final selected values from the Tweaks Bar (fonts, accent colors, spacing, stagger delay) and commit them permanently into production design tokens (e.g., `tailwind.config.js` or global CSS variables).
2. **Clean Up Exploratory Code:** Remove the temporary Tweaks Bar overlay and delete unused exploration routes (`/design-exploration/`).
3. **Promote to Production Route:** Move the finalized page into the main production route (e.g., `app/page.tsx` or `index.html`).
4. **Quality Checks:**
   * Verify micro-design compliance against `design-rules` (headline tracking, button states, dark mode elevation).
   * Verify responsive layout across Mobile, Tablet, and Desktop.
   * Verify basic accessibility (contrast ratios, heading hierarchy).
   * Respect `prefers-reduced-motion` for animations.
   * Compare final screenshot against the original selected inspiration direction.

---

## 📚 9. Source Video References & Transcripts

For complete untruncated transcripts and raw video research:
* 📄 [01_chase_ai_anti_slop_web_design.md](../references/01_chase_ai_anti_slop_web_design.md) — Chase AI
* 📄 [05_chris_mccoy_5_web_design_skills.md](../references/05_chris_mccoy_5_web_design_skills.md) — Self-Made Web Designer
* 📄 [06_chris_mccoy_6_habits_of_design_legends.md](../references/06_chris_mccoy_6_habits_of_design_legends.md) — Self-Made Web Designer
* 📄 Full Reference Index: [README.md](../references/README.md)
