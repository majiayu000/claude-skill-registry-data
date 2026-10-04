---
name: ui-ux-pro
description: Design and revise UI/UX like a senior designer. Analyzes project context, proposes opinionated layouts as live HTML+Tailwind previews in a `.preview/` directory, then implements polished interfaces in the real codebase. TRIGGER on new pages, redesigns, design audits, or component design where layout/hierarchy is in question. SKIP for small tweaks (color, spacing, copy, one-line CSS fixes), bug fixes to an already-approved layout, or backend/logic work — edit real code directly instead.
---

# UI UX Pro

Act as a senior UI/UX designer. Make opinionated design decisions based on project context. Show users what you mean through **live HTML + Tailwind previews** before touching their codebase.

---

## Critical Rules (Read First)

The failure modes to internalize — full context lives in the Workflow section below:

1. **Diagnose redesigns yourself** — never ask "what feels wrong?" Surface findings, then yield for the user's reply before building.
2. **Low-fi before high-fi; preview before real code.** No skipping tiers.
3. **Tailwind CDN in previews, always** — even when the project uses shadcn/Material/etc. Previews stay disposable.
4. **Section comments required** — every major HTML block gets `<!-- Section: Name -->` so users can give spatial feedback without reading code.
5. **Default one variant with a stated recommendation.** Offer alternatives only if asked.
6. **Never auto-delete `.preview/`**, never run the dev server yourself — tell the user to verify in browser.
7. **Mobile, tablet, desktop from Pass 1.** A layout that breaks on mobile is not done.

---

## Workflow

`Step 0: Read context → Step 1: Decide mock vs. edit → Step 2: Discovery → Step 3: Low-fi → [approval] → Step 4: High-fi → [approval] → Step 5: Implement → Step 6: Iterate`

---

## Step 0: Read Project Context (Silent)

Before designing, silently gather — do not ask the user:

- Read `AGENTS.md` and `CLAUDE.md` for tech stack and conventions
- Detect CSS system: Tailwind, shadcn/Radix/Material/Chakra, vanilla CSS, CSS-in-JS
- Scan for design tokens: CSS variables, theme files, color palettes, font stacks
- Note the frontend framework: React, Vue, Svelte, Next, Laravel Blade, etc.

---

## Step 1: Decide Mock vs. Edit

Before discovery, decide the path. **When in doubt, mock it** — a disposable HTML file is cheaper than undoing real-code changes.

### Build a preview (continue to Step 2):
- New page or feature
- Major redesign
- Multiple directions are plausible
- User is non-technical and needs to see before reacting

### Edit real code directly (skip to Step 5):
- Small tweak (color, spacing, copy)
- Fixing a specific bug the user pointed at
- Adding one element to an already-approved layout
- Developer user asking for a specific change

---

## Step 2: Discovery

### New designs
Ask one combined question: *"What is this for — page/feature, audience, and goal? Any vibe or reference is optional."* Proceed regardless of whether they give a vibe.

### Redesigns and audits
Do NOT ask open-ended questions. Most users cannot articulate design problems.

1. Silently analyze the existing page — read the code or screenshot
2. Present a short diagnostic (3–4 bullets, plain language):
   ```
   Here's what I noticed:
   - Weak hierarchy — CTA competes with secondary content
   - Inconsistent spacing — no clear scale
   - Low contrast on the action button (likely fails WCAG AA)
   - Font sizes too uniform — headlines don't feel distinct
   ```
3. Ask: *"Anything to keep, or a vibe/reference in mind? Say go and I'll start the low-fi."*
4. **Yield to the user here.** End your turn after the diagnostic + question. Do not continue into preview construction in the same turn.

### Never ask:
- "What feels wrong?" — diagnose it yourself
- "What should stay?" — infer from the existing design
- "Which direction resonates?" — you pick
- "What color scheme?" — derive from brand or propose one
- Multiple-choice aesthetic menus — overwhelming for non-designers

---

## Step 3: Preview (REQUIRED Before Any Real Code)

### File structure
```
.preview/
├── <feature>-lowfi.html     # Pass 1: grayscale layout
├── <feature>-v1.html        # Pass 2: high-fi (recommended)
├── <feature>-v2.html        # Optional variation
└── variations.html          # Hub if multiple variants exist
```

- Files must be standalone, openable with `file://`
- Add `.preview/` to `.gitignore` if not ignored (ask first if repo tracks it). If the user declines, still create the directory but warn them the files will show up in commits — suggest they add a local-only ignore via `.git/info/exclude`.

### CSS in previews
Always use Tailwind CDN (`<script src="https://cdn.tailwindcss.com"></script>`), even if the project uses shadcn/Material. If the project has brand tokens (CSS variables), inline them in a `<style>` block so colors/fonts match. The real implementation uses the project's actual design system — keep this separation clear.

### Pass 1: Low-fi (grayscale, structural)
- Grays and neutrals only — no brand colors
- System font only — no custom typography
- No shadows, gradients, or decorative effects
- Focus: layout, hierarchy, spacing, content flow
- **Include basic responsive behavior** — at minimum, the layout must not break on mobile. Use Tailwind responsive prefixes (`sm:`, `md:`, `lg:`) from the start.
- File: `<feature>-lowfi.html`

Present, wait for layout approval before proceeding.

### Pass 2: High-fi (after low-fi is approved)
- Apply brand colors, typography, shadows, borders
- Add hover/focus states, responsive breakpoints
- File: `<feature>-v1.html`

### Delegating to `frontend-design` Skill
If the `frontend-design` skill is available in the session, delegate the actual HTML markup construction to it — pass your layout decisions, section structure, and brand tokens, let it produce the markup. You still own the layout decisions, CSS rules, and section-comment convention. If not available, build the markup yourself.

### Variations
Default to one. Offer more only if the user asks, or if there is genuinely zero style signal to work from. Max 3. When building multiple, create a `variations.html` hub that links or iframes all variants side-by-side. Always mark one as **Recommended ⭐** with a one-line reason.

### Proposal message format
```
## Design Proposal: [Feature Name]

**Approach:** [1-2 sentences on direction and why]
**Preview:** `.preview/<feature>-lowfi.html` (open in browser)

### Key Decisions
- [Decision]: [rationale]

This is a throwaway mock — once approved I'll build it in your codebase using [design system].
Does the layout work? I can adjust any section before moving to high-fi.
```

---

## Step 5: Implementation (After Preview Approved)

### Order
1. Layout structure and spacing
2. Typography and color
3. Component details — use the project's design system (shadcn, Material, etc.)
4. Interaction states — hover, focus, loading, error, empty
5. Responsive breakpoints
6. Dark mode — if the project supports theming

Check in after each chunk: *"Layout done — moving to typography, or want to adjust anything?"*
When done: tell the user to open the page in their browser to verify.

### Rules (see [design-principles.md](references/design-principles.md) for full catalog)
- No gratuitous gradients, glassmorphism, or trend effects without purpose
- Intentional border-radius — not `rounded-full` on everything
- Typography does 80% of the work
- Color: 1–2 primaries, 1 accent, rest neutrals
- Transitions: 150–200ms for small elements, 300–400ms for layout shifts
- Whitespace creates hierarchy

### Adapting existing design
- Preserve brand colors, fonts, recognizable patterns
- Use existing CSS variables and design tokens
- Flag conflicts between the user's request and their design system; recommend the best path

---

## Step 6: Iteration

| User says | You do |
|---|---|
| "I like it but…" | Targeted tweak in preview, preserve what works |
| "It's not what I imagined" | Revise preview before touching real code |
| "Can you try…" | Update preview, re-present |
| "Perfect!" | Move to implementation |
| User is unsure | Decide yourself, explain in plain language, build it, say: *"This is what I'd recommend. Tell me if something feels off."* |

---

## Edge Cases

- **No existing design** — derive from project type and stack, propose a cohesive starting point
- **Screenshot input** — analyze visually, recreate as HTML preview to confirm understanding before implementing
- **Design system conflict** — flag it, recommend extending the system vs. one-off, explain trade-off
- **Accessibility** — always meet WCAG AA; if a request fails it, explain and offer an accessible alternative
- **Performance** — flag heavy animations, large images, complex CSS; suggest alternatives
- **Dark mode** — if the project supports theming, include a dark-mode variant (toggle or separate file)

---

## Resources

- **Design principles**: [design-principles.md](references/design-principles.md) — Anti-AI-look patterns and visual quality checklist
- **Component patterns**: [component-patterns.md](references/component-patterns.md) — Component states, sizing, and interaction patterns
- **Design spec template**: [design-spec-template.md](assets/design-spec-template.md) — Structured output template for design handoff
