---
name: stitch-design
description: Generate professional UI designs using Google Stitch before building any frontend. Use this skill when building apps, websites, dashboards, landing pages, or any user-facing interface.
---

<!-- CHANGELOG
2026-03-19 — Added Mandatory Prompt Template (Fix 1) and Passing Design to Claude Code workflow (Fix 2). Fixes generic, cookie-cutter Stitch output and closes the Stitch→Claude Code handoff gap.
-->

# Google Stitch — AI UI Design Tool

## When to Use
- BEFORE building ANY user-facing app, website, dashboard, or landing page
- When the user asks for something to "look good" or mentions design quality
- When building mobile app screens (set layout to mobile)
- When building web apps, dashboards, admin panels

## Access Methods

### Method A: mcporter (preferred — already configured)
```bash
mcporter call stitch.list_projects
mcporter call stitch.create_project title="My App"
mcporter call stitch.generate_screen_from_text --timeout 300000 projectId="ID" deviceType="DESKTOP" modelId="GEMINI_3_1_PRO" prompt="your prompt"
mcporter call stitch.get_screen --timeout 30000 name="projects/ID/screens/SID" projectId="ID" screenId="SID"
mcporter call stitch.list_screens projectId="ID"
mcporter call stitch.edit_screens --timeout 300000 projectId="ID" selectedScreenIds='["SID"]' prompt="changes"
```

### Method B: CLI direct (fallback)
```bash
STITCH_API_KEY="$STITCH_API_KEY" npx @_davideast/stitch-mcp view --projects
STITCH_API_KEY="$STITCH_API_KEY" npx @_davideast/stitch-mcp view --project <project-id>
STITCH_API_KEY="$STITCH_API_KEY" npx @_davideast/stitch-mcp view --project <project-id> --screen <screen-id>
STITCH_API_KEY="$STITCH_API_KEY" npx @_davideast/stitch-mcp serve -p <project-id>
```

## Design-First Build Workflow
1. User describes the app they want built
2. Create a Stitch project: `mcporter call stitch.create_project title="App Name"`
3. Generate each screen with detailed prompts: `mcporter call stitch.generate_screen_from_text`
4. Pull the HTML/CSS for each screen via the download URLs in the response
5. Use the HTML/CSS as visual reference when building React/Next.js/React Native components
6. Extract color tokens, fonts, spacing, and component patterns from the Stitch output
7. Build the actual app to match the design

## Design Prompt Tips
- Always specify: theme (dark/light), accent color, target platform (mobile/web)
- Include component details: "card with status pill, avatar, timestamp"
- Reference design patterns: "Bloomberg terminal style", "Apple-like minimal"
- For multi-screen apps, reference the first screen's style in subsequent prompts
- Use deviceType: MOBILE for phone screens, DESKTOP for web pages
- Use modelId: GEMINI_3_1_PRO for best quality
- Set --timeout 300000 for generate calls (they take 2-3 minutes)

---

## Mandatory Prompt Template

**NEVER send a vague prompt to Stitch.** Generic prompts produce generic output. Every Stitch generate call MUST follow this template structure:

```
Design a [screen name] for [product name].

VISUAL REFERENCES: This should feel like a combination of [site-1.com] and [site-2.com] — not a template, not shadcn defaults.

TYPOGRAPHY:
- Hero headline: [e.g. 72px / font-weight 800 / Inter or Geist]
- Body: [e.g. 16px / font-weight 400 / Inter]
- Labels/caps: [e.g. 11px / font-weight 600 / letter-spacing 0.08em]

HERO TREATMENT: [e.g. Full-bleed dark hero (#0A0A0A background), single centered headline, one CTA button, no image grid, no stock photography]

LAYOUT — section by section:
1. Nav: [exact description — e.g. left logo, right: 3 nav links + CTA button, no hamburger on desktop]
2. Hero: [exact description]
3. [Section 3 name]: [exact description]
4. [Continue for every section on this screen]

ACCENT COLOR: [exact hex, e.g. #6366F1] — used only for CTA buttons and key interactive elements. Not used for backgrounds.

THINGS TO AVOID:
- No shadcn/ui default component styling
- No generic hero with image on right, text on left (the grid layout every SaaS uses)
- No gradient blobs or mesh backgrounds
- No stock photography or placeholder people images
- No card grids with icons as the main hero section
- [Add project-specific avoidances]

THINGS TO NAIL:
- [e.g. Information density — this is a tool, not a marketing page]
- [e.g. Trust — it must look like a company with real customers]
```

### Iteration Requirement (MANDATORY)
**Never accept the first Stitch output.** Always send at least 2 follow-up refinement prompts before using the output:

1. **Refinement 1** — Address what's generic, weak, or off-brand: "The hero feels too much like a standard SaaS template. Make the headline larger (80px+), remove the image grid, and push the CTA higher up the page."
2. **Refinement 2** — Final precision pass: "Tighten the spacing in the nav, make the accent color more saturated (#4F46E5 → #3730A3), and increase font weight in the section headers to 700."

Only use the output after at least 2 rounds of refinement.

---

## Passing Design to Claude Code

After Stitch generates and refines screens, the design must be passed to Claude Code as visual references — not just extracted tokens.

### Step 1 — Download Full-Resolution Screenshots
Stitch returns screenshot URLs in `outputComponents[0].design.screens[0].screenshot.downloadUrl`. By default these are thumbnails. Append `=s0` to get full resolution:

```bash
# Full-res download
curl -sL "STITCH_SCREENSHOT_URL=s0" -o /tmp/stitch-<project>-<screen>.png

# Example
curl -sL "https://storage.googleapis.com/stitch-output/abc123=s0" -o /tmp/stitch-myapp-hero.png
curl -sL "https://storage.googleapis.com/stitch-output/def456=s0" -o /tmp/stitch-myapp-dashboard.png
```

### Step 2 — Pass Images Inline to Claude Code Build Spec

Include the images directly in the Claude Code invocation — not as a separate step. The `--image` flag can be repeated for multiple screens:

```bash
cd ~/Projects/<name> && claude \
  --permission-mode bypassPermissions \
  --print \
  --image /tmp/stitch-<project>-hero.png \
  --image /tmp/stitch-<project>-dashboard.png \
  -p "FULL SPEC HERE — see design instructions below"
```

### Step 3 — Claude Code Spec Must Include Pixel-Match Instructions

The spec passed to Claude Code must explicitly say:

```
DESIGN REFERENCE: The attached screenshots are the exact visual target.
- Pixel-match these screenshots. This is not aspirational — it is the requirement.
- Do NOT use default shadcn/ui, Radix, or Tailwind component styling. Style everything from scratch to match the visual.
- Do NOT approximate colors — extract exact hex values from the screenshot.
- Match font sizes, font weights, spacing, and border radii precisely.
- If anything in the design is unclear, err toward more opinionated and premium-looking, not simpler.
- The attached images are the source of truth. The design tokens below are secondary.
```

**Key rule:** Claude Code must be told to pixel-match the visual, not just "use these design tokens." Tokens alone produce generic output. The image is the spec.

## Screenshot Downloads
Stitch returns screenshot URLs in `outputComponents[0].design.screens[0].screenshot.downloadUrl`
- Default: thumbnail resolution
- Append `=s0` to URL for full resolution
- Example: `curl -sL "URL=s0" -o screen.png`

## Limits
- 350 standard screens/month, 50 experimental screens/month
- Free tier — no usage costs
- Stitch outputs are HTML/CSS — always rebuild properly in the target framework

## Config
- mcporter config: ~/.mcporter/mcporter.json
- API key: stored in mcporter env config
- DO NOT add stitch to openclaw.json — use mcporter or CLI only
- Stitch project for GRWM Studio Website: 11564154195642390915
