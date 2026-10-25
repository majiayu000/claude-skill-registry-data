---
name: saas-asset-spec
description: "Author per-asset visual specs, SVG dimensions, and generation prompts from PRDs and design tokens. After design tokens."
argument-hint: "[feature:<name> | screen:<name> | brand:<name>] [--review full|lean|solo]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Edit, Agent, AskUserQuestion, Bash(bash "*/.claude/skills/saas-asset-spec/../../hooks/yaml-helper.sh" resolve_config *)
model: sonnet
---

!`bash "${CLAUDE_SKILL_DIR}/../../hooks/yaml-helper.sh" resolve_config --keys locale,review_mode,automation`

# Asset Spec

> **Interaction Localization Rule**:
> When `locale: pt-BR` (or user speaks Portuguese), ALL questions (`AskUserQuestion` / `ask_question`), confirmation prompts, and selectable options MUST be translated and presented in **Brazilian Portuguese (PT-BR)**.
> Any English question text or options in this skill are illustrative examples — NEVER display English questions or options to a Portuguese developer.
> Internal reasoning, code synthesis, tests, and documentation files MUST remain in English.

The **Asset Spec** skill produces precise, production-ready specifications for all visual,
vector, and media assets required by the SaaS application (brand logos, UI icons, empty-state illustrations,
marketing hero graphics, OG social preview cards, and email templates).

If no argument is provided, check whether `design/assets/entity-inventory.md` exists:
- If it exists: read it, find the first asset or screen with status "Needed" but no spec file yet, and prompt the user.
- If no inventory: check `design/assets/asset-manifest.md`.
- If neither exists: **start the Entity & Screen Inventory flow** (Phase 0b below).

---

## Phase 0b: Entity & Screen Inventory (runs when no arguments and no existing inventory)

This flow produces `design/assets/entity-inventory.md` — the master list of everything
the SaaS application needs visually. Run once before individual asset spec work begins.

### Step 1 — Gather from docs
Read all available product design documents:
- `design/prd/*.md` — feature requirements, data tables, empty states
- `design/ux/*.md` — screen layouts, user flows, app shell
- `design/ui/design-tokens.md` — visual foundation, color tokens, typography

### Step 2 — Build proposed inventory
Categorize needed assets:
- **Brand Assets**: Primary logo, dark/light variations, app icon (square, circle), favicon bundle (`favicon.ico`, `apple-touch-icon.png`), social cards (`og-image.png`).
- **UI Screens & Components**: Dashboard views, settings panels, table views, modal dialogs.
- **Empty States & Illustrations**: "No projects found", "No invoices yet", "Search returned 0 results", "Invite your team".
- **Marketing & Email Media**: Feature preview graphics, hero illustrations, transactional email headers.

### Step 3 — Write inventory
Write to `design/assets/entity-inventory.md`.

---

## Phase 0: Parse Arguments

Parse target:
- `feature:<name>` — specify assets for a specific feature (e.g. `feature:billing`, `feature:analytics`)
- `screen:<name>` — specify assets for a specific screen (e.g. `screen:dashboard`, `screen:onboarding`)
- `brand:<name>` — specify brand identity assets (e.g. `brand:logos`, `brand:favicons`)

---

## Phase 1: Gather Context

Read required design documents:
1. `design/ui/design-tokens.md` — color palette, radius, typography, asset budget rules
2. `design/product-concept.md` — product positioning and tone
3. Target PRD or UX spec (`design/prd/[name].md` or `design/ux/[name].md`)

---

## Phase 2: Asset Identification

List every required asset for the target:
- Format: SVG (vectors, icons, logos), WebP/PNG (illustrations, photos), JSON (Lottie animations)
- Viewport and density targets (1x, 2x for retina displays, responsive mobile)
- Dark mode variant needed? (Yes / No)

---

## Phase 3: Spec Generation

Derive technical specifications and prompt descriptions:
- **Dimensions**: ViewBox dimensions (e.g., `24x24` for icons, `400x300` for empty states, `1200x630` for OG cards).
- **Color Mapping**: Bind SVG fills and strokes to semantic design tokens (`var(--primary)`, `var(--muted-foreground)`).
- **File Size Budget**: Max file size in KB (e.g. icon < 5KB, illustration < 50KB, OG image < 200KB).
- **Generation Prompt**: High-fidelity AI generation prompt (Midjourney, DALL-E, Recraft) if the asset will be procedurally generated.

---

## Phase 4: Compile Spec

Format each asset:

```markdown
### ASSET-[NNN]: [Asset Name]
- **Type**: Icon | Illustration | Brand | Template
- **Format**: SVG | WebP | PNG
- **Target Path**: `public/assets/[category]/[name].[ext]`
- **Dimensions**: [Width x Height in px / viewBox]
- **Theme Variants**: Light / Dark
- **Size Budget**: [N] KB
- **Design Tokens Used**: `primary`, `card`, `border`
- **Accessibility**: Alt text / ARIA label (`aria-hidden="true"` if decorative)
- **Generation / Design Brief**:
  > "[Detailed visual description: composition, palette, lighting, vector style matching design tokens]"
```

---

## Phase 5: Write Spec File & Manifest

Write to `design/assets/specs/[target-name]-assets.md`.
Update `design/assets/asset-manifest.md` with status `Specified`.
