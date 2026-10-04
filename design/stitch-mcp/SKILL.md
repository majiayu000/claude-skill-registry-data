---
name: Stitch MCP
description: >
  Guide for working with Google Stitch — AI-powered UI design generation,
  screen management, and design-to-code workflows via the Stitch MCP proxy
  and CLI. Use this skill whenever the user mentions Stitch, wants to generate
  UI designs from text prompts, convert Stitch screens to code, build multi-page
  sites from Stitch projects, preview designs locally, extract design systems,
  manage Stitch authentication, or work with Stitch projects and screens. Also
  triggers on references to stitch-mcp, Stitch projects/screens, stitch-mcp CLI
  commands, or AI-generated UI design workflows.
---

# Stitch MCP

Work with Google Stitch through the `stitch-mcp` proxy — generate AI-powered
UI designs from text, manage screens, extract code, and scaffold complete sites.

## Prerequisites

- **Install**: `npm install -g @_davideast/stitch-mcp`
- **Authentication**: Run `stitch-mcp init` for guided OAuth setup, or set
  `STITCH_API_KEY` environment variable for API key auth
- **Health check**: Run `stitch-mcp doctor` to verify all 7 config checks pass
- **MCP config** (Claude Code / Codex):
  ```json
  { "command": "stitch-mcp", "args": ["proxy"] }
  ```

## Tool Reference

### Project & Screen Management

| Tool | What it does |
|------|-------------|
| `list_projects` | List all Stitch projects |
| `get_project` | Get details for a specific project |
| `list_screens` | List all screens in a project |
| `get_screen` | Get screen metadata and download URLs |

### Design Generation

| Tool | What it does |
|------|-------------|
| `generate_screen_from_text` | Generate a new screen from a text description |
| `edit_screens` | Edit existing screens via text prompt |
| `generate_variants` | Generate design variants of a screen |

### Code & Asset Extraction (proxy virtual tools)

These are only available when using proxy mode (`stitch-mcp proxy`), not
direct HTTP connections.

| Tool | What it does |
|------|-------------|
| `get_screen_code` | Fetch a screen's full HTML content (follows download URL automatically) |
| `get_screen_image` | Get a screen screenshot as base64 PNG |
| `build_site` | Map screens to routes, fetch HTML for all pages in parallel |
| `list_tools` | List all available tools with their schemas |

## Core Workflows

### 1. Text → Design (generate from prompt)

Generate UI screens directly from natural language descriptions.

1. If the user has an existing project, call `list_projects` to find it.
   Otherwise, create designs in a new or existing project.

2. Call `generate_screen_from_text` with a detailed prompt. The more specific
   the prompt, the better the result — include layout preferences, color
   schemes, content examples, and component types.

3. To refine, call `edit_screens` with the screen ID and an edit prompt
   describing what to change. This preserves the overall design while making
   targeted modifications.

4. Use `generate_variants` to explore alternative takes on the same design.

**Prompt enhancement tip:** Vague prompts produce generic results. Transform
user requests into detailed Stitch-optimized prompts that specify:
- Layout structure (sidebar + main content, hero + cards, etc.)
- Color palette and typography preferences
- Specific UI components (data tables, charts, form fields, navigation)
- Content examples (real text, not lorem ipsum)
- Responsive behavior expectations

**Example:**
```
User: "Make me a dashboard"
Enhanced: "A modern analytics dashboard with a dark sidebar navigation on the
left (240px wide), a top bar with user avatar and notifications, and a main
content area with: a row of 4 KPI cards (revenue, users, conversion, churn),
a line chart showing 12-month trend below, and a data table of recent
transactions at the bottom. Use a clean sans-serif font, blue-purple accent
colors, and subtle card shadows."
```

### 2. Design → Code (extract and implement)

Pull generated designs into your codebase as reference HTML or as a starting
point for component implementation.

1. Call `get_screen_code` with the screen ID to get the full HTML/CSS output.
   This is self-contained HTML you can use as a reference for implementation.

2. Call `get_screen_image` if you want a visual screenshot for comparison
   while building the component in your framework.

3. Adapt the HTML to your project's stack — map to existing components, use
   your design token system, follow project conventions. The Stitch output is
   reference material, not production code.

### 3. Multi-Page Site Scaffolding

Build a complete multi-page site from a Stitch project's screens.

1. Call `list_screens` to see all available screens in the project.

2. Plan the routing — decide which screen maps to which URL path.

3. Call `build_site` with the project ID and an array of
   `{ screenId, route }` mappings. This fetches HTML for all pages in parallel.

4. Use the returned HTML as the basis for an Astro, Next.js, or other
   framework project. The CLI also supports this via `stitch-mcp site -p <id>`.

### 4. Local Preview

Preview Stitch designs locally without extracting code.

```bash
stitch-mcp serve -p <projectId>
```

This spins up a Vite dev server showing all project screens. Useful for
quick visual review and stakeholder demos.

### 5. Design System Extraction

Analyze a Stitch project to extract a coherent design system.

1. List all screens in a project and fetch their code
2. Analyze the HTML/CSS for recurring patterns: colors, typography scales,
   spacing values, component patterns
3. Document as a `DESIGN.md` capturing the design language in semantic terms

## CLI Quick Reference

The `stitch-mcp` CLI is useful for interactive exploration and one-off tasks
outside of agent workflows.

| Command | What it does |
|---------|-------------|
| `stitch-mcp init` | Guided setup wizard (auth, gcloud, MCP client config) |
| `stitch-mcp doctor` | Verify configuration health (7 checks) |
| `stitch-mcp logout` | Revoke credentials |
| `stitch-mcp serve -p <id>` | Local Vite preview of project screens |
| `stitch-mcp screens -p <id>` | Browse screens in terminal |
| `stitch-mcp view` | Interactive resource browser (arrow keys, copy, preview) |
| `stitch-mcp site -p <id>` | Generate deployable Astro project from screens |
| `stitch-mcp snapshot` | Save screen state to file |
| `stitch-mcp tool <name>` | Invoke MCP tools from CLI (`-s` for schema, `-o json`) |
| `stitch-mcp proxy` | Run the MCP proxy for agent connections |

## Official Skills (google-labs-code/stitch-skills)

Google maintains a curated skills repo with higher-level workflows. Install via:
```bash
npx skills add google-labs-code/stitch-skills --skill <name> --global
```

| Skill | What it does |
|-------|-------------|
| `stitch-design` | Unified entry point: prompt enhancement, design system synthesis, screen generation/editing |
| `stitch-loop` | Generate a complete multi-page website from a single prompt |
| `design-md` | Analyze a project and generate comprehensive DESIGN.md |
| `enhance-prompt` | Transform vague UI ideas into polished Stitch-optimized prompts |
| `react:components` | Convert screens to React component systems with design tokens |
| `remotion` | Generate walkthrough videos from Stitch projects |
| `shadcn-ui` | Integrate shadcn/ui components with Stitch output |

When the user's task aligns with one of these skills, check if it's already
installed (look in the workspace skills directory). If installed, defer to it
for that task — it provides more specialized guidance. If not installed, offer
to install it with the `npx skills add` command above, then use this skill's
general guidance as a fallback.

## Tips

- **Prompt quality matters most.** See the prompt enhancement pattern in
  Workflow 1 above — the difference between generic and great output is almost
  entirely in the prompt specificity.
- **Iterate with edit_screens.** Don't regenerate from scratch when a design is
  80% right — use `edit_screens` for targeted refinements.
- **Variants for exploration.** When unsure about direction, `generate_variants`
  is cheaper than manual iteration — generate 3-4 takes and let the user pick.
- **build_site for full projects.** When working with multi-page projects,
  `build_site` fetches all pages in parallel and is much faster than calling
  `get_screen_code` individually for each screen.
- **Preview before extracting.** Use `stitch-mcp serve` for quick visual
  checks before investing time in code extraction and implementation.

## Error Handling

- **Auth failures** (401/403 from Stitch tools): Run `stitch-mcp doctor` to
  diagnose. If OAuth tokens expired, run `stitch-mcp init` to re-authenticate.
  Report the specific doctor check that failed.
- **Project/screen not found** (404): Verify the ID with `list_projects` or
  `list_screens`. IDs are case-sensitive.
- **Generation timeout or failure**: Stitch generation can take 30-60 seconds.
  If it fails, retry once with the same prompt. If it fails again, simplify the
  prompt — overly complex prompts with many constraints can cause failures.
- **Empty HTML from get_screen_code**: The screen may still be generating. Wait
  10 seconds and retry. If still empty, check the screen status with `get_screen`.

## Environment Variables

| Variable | Purpose |
|----------|---------|
| `STITCH_API_KEY` | API key auth (simplest, skips OAuth) |
| `STITCH_ACCESS_TOKEN` | Pre-existing access token |
| `STITCH_USE_SYSTEM_GCLOUD` | Use system gcloud instead of bundled |
| `STITCH_PROJECT_ID` | Override default project ID |
| `STITCH_HOST` | Custom Stitch API endpoint |
