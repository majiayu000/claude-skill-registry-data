---
name: nick-v0-design
description: DEPRECATED — replaced by stitch-design as primary design tool. Use stitch-design instead. This skill is kept as fallback only if Stitch is unavailable.
---

> ⚠️ **DEPRECATED (2026-03-19)**: Google Stitch is now the primary design tool. Use `stitch-design` skill instead.
> Only use this as a fallback if Stitch MCP is down or unavailable.

# v0 Design Generation Skill

## Purpose
Generate production-ready React/Tailwind UI components and pages via the v0.dev API before building any project. Every build starts with v0-generated design, then backend (Supabase, auth, etc.) is wired in.

## Prerequisites
- v0 API key stored in TOOLS.md (V0_API_KEY)
- v0-sdk installed: `npm install v0-sdk` (in workspace)
- Node.js available

## Generator Script
`scripts/v0-generate.js` — CLI tool that prompts v0 and saves generated files locally.

```bash
V0_API_KEY="<key>" node skills/nick-v0-design/scripts/v0-generate.js \
  --prompt "Your detailed design prompt" \
  --output ~/Projects/<project>/v0-output \
  --follow-up "Refine: add dark mode" \
  --follow-up "Refine: make mobile responsive"
```

### Flags
- `--prompt` / `-p` — Main design prompt (required for new chats)
- `--output` / `-o` — Output directory for generated files
- `--follow-up` / `-f` — Additional refinement messages (can use multiple)
- `--chat-id` — Continue an existing v0 chat

### Output
- React/Tailwind component files saved to output dir
- `v0-manifest.json` with chat ID, URLs, and file list
- Demo URL for live preview

## Workflow: Design-First Build Pipeline

### Step 1: Write a Rich v0 Prompt
For EVERY new project, write a detailed prompt that includes:
- App name and purpose
- Target audience
- Color scheme and visual style (reference nick-design-system)
- ALL sections needed (minimum 12-15 for landing pages)
- Specific components: hero, navigation, feature cards, pricing, testimonials, FAQ, footer
- Device mockups, trust signals, stats sections
- Responsive requirements
- Dark/light mode

Example prompt structure:
```
Build a complete landing page for [APP NAME] — [description].

Visual style: [reference design system — dark hero, enterprise polish, Inter font]
Color palette: [primary, secondary, accent colors]

Sections (in order):
1. Navigation — sticky, logo left, links center, CTA right
2. Hero — dark gradient bg, headline, subtext, dual CTAs, device mockup showing the app
3. Trust bar — "As seen in" logos
4. How it works — 3-4 numbered steps with icons
5. Features for [audience 1] — alternating text+visual layout
6. Features for [audience 2] — reversed layout  
7. Stats — large numbers on dark bg
8. Testimonials — star ratings, avatars, quotes
9. Pricing — tiered cards with feature lists
10. FAQ — accordion with 6+ items
11. CTA section — dark gradient, compelling headline, buttons
12. Footer — multi-column with links, social icons, legal

Requirements:
- Fully responsive (mobile-first)
- Tailwind CSS only
- shadcn/ui components where appropriate
- Static demo data (no API calls)
- Semantic HTML with accessibility
- Smooth hover/transition effects
```

### Step 2: Generate with v0
Run the generator script. Review the demo URL. If quality isn't right, send follow-ups.

### Step 3: Integrate into Project
1. Copy v0-generated components into the Next.js project
2. Install any missing dependencies from v0's package.json
3. Wire up Supabase backend (auth, database)
4. Add dynamic data where static demo data exists
5. Deploy to Vercel

### Step 4: Iterate
Use `--chat-id` and `--follow-up` to refine without starting over.

## Key Rules
- NEVER skip the v0 design step for any new project
- ALWAYS review the v0 demo URL before integrating
- ALWAYS write prompts that reference the nick-design-system standards
- Use follow-ups to refine — don't settle for first output
- v0 handles design; Claude Code handles backend integration
- Save chat IDs in project memory for future iterations

## API Reference
The v0 SDK provides:
```javascript
const { v0 } = require('v0-sdk');
// Create new chat
const chat = await v0.chats.create({ message: '...' });
// Send follow-up
const response = await v0.chats.sendMessage({ chatId: chat.id, message: '...' });
// Access files: chat.latestVersion.files or chat.files
// Access demo: chat.demo
// Access screenshot: chat.latestVersion.screenshotUrl
```
