---
name: premium-ui-design-stack
description: A layered design process for making Claude's UI output look premium instead of generic "AI slop". Use whenever the user asks Claude to build, redesign, polish, critique, or audit any frontend UI — landing pages, marketing sites, dashboards, app screens, components, portfolios, design systems — or says things like "make it look good", "premium", "unslop", "avoid AI-looking design", "design system", or "taste". Also use when setting up Claude Code for better design output (Impeccable, Anthropic frontend-design, taste-skill, UI UX Pro Max, Emil Kowalski skills, 21st.dev MCP, Vercel Web Interface Guidelines). Use it even for small UI tasks; scale the process down rather than skipping it.
---

# Premium UI Design Stack

Claude's default UI output converges on the same look: centered hero, purple-blue gradient, three identical feature cards, generic "Unlock your potential" copy, emoji icons, no motion or arbitrary motion. This skill replaces "jump straight to code" with a design process made of five layers plus a review pass.

The process comes from two creator videos (see `references/source-notes.md`). The tools they name are optional accelerators. The process works without them, so never block on a missing plugin.

## Step 0: See what is available

Check which of these are installed or reachable in this environment: `impeccable`, `frontend-design`, `taste-skill`, `ui-ux-pro-max`, Emil Kowalski's skills, a 21st.dev MCP server. Use what exists. For each missing layer, follow its fallback in `references/layers.md`. Never say you used a tool that is not installed.

If the user wants to install the stack, give them the commands from `references/layers.md` and tell them to verify against each project's own README, since versions change.

## The workflow

Run the layers in order. Keep each one short. Write results into the project (`PRODUCT.md`, `DESIGN.md`) when the project is a real codebase, or state them in two or three lines in chat when it is a one-off artifact.

1. **Product layer.** Establish who the page or app is for, the single action that makes it a success, the tone, and the constraints. Read existing `PRODUCT.md`, `DESIGN.md`, README and any design comp first. Treat figures, testimonials and copy in a comp as placeholders, never as facts, and mark invented content clearly (for example in a `PLACEHOLDERS.md`). Ask the user only what you cannot infer; otherwise state your assumptions in one line and proceed.
2. **Structure layer.** Choose the page structure and a distinct aesthetic direction before touching code. Pick one bold, specific direction (editorial, brutalist, quiet-luxury, technical, playful…) and commit. Define the type pairing, grid and section order. Avoid the generic template.
3. **Taste layer.** Turn references (screenshots, sites the user likes, a mood) into explicit rules: type scale, colour tokens, spacing scale, radii, borders and shadows, imagery style, copy voice. The output is a consistent design language that every component then follows.
4. **Knowledge layer.** Pick layouts, typography, colour palettes and UX patterns suited to the product category (fintech, education, health, developer tools…), not from habit. Use structured design knowledge if a tool provides it; otherwise reason from category conventions and say why you chose them.
5. **Motion layer.** Decide how things should move and when they should stay still. Motion needs a purpose (orientation, feedback, hierarchy). Do not animate everything. Define durations and easing once, prefer CSS over main-thread JS, and honour `prefers-reduced-motion`.
6. **Build** against the design language from steps 2–5.
7. **Review pass.** Run `references/review-checklist.md` against the result. If Impeccable is installed, also run its critique/audit/polish commands. Render the page at desktop and mobile widths and look at screenshots when you can; fix what you see rather than trusting the code.
8. **Components (optional).** If a 21st.dev MCP is connected, pull components for sections you would otherwise hand-build, then restyle them to the design language so they do not look pasted in.

## Scaling the effort

- **New design system, flagship page, or "highest quality" request:** run all five layers and the full review.
- **Small prototype or single component:** run the product layer, one aesthetic decision, and the review checklist. Skip the rest.
- **Redesign of an existing UI:** read what is there first, keep the brand's real constraints, and run the review checklist before and after.

Be honest about overlap. The taste and Impeccable layers cover similar ground (both are anti-slop systems with strong opinions) but catch different things. Running one gives most of the gain. When they disagree, treat the disagreement as a decision to make deliberately, not noise to average away. Running all five costs more tokens and context, which is not worth it for every small task.

## What to tell the user afterwards

Two or three sentences: the direction you chose, the assumptions you made (especially invented placeholder content), and which layers or tools you actually used. Do not narrate the whole process.
