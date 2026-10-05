---
name: stitch-mcp-design
description: >-
  Router for Google Stitch design-to-code in this pack. Use when starting any
  Stitch workflow, choosing Stitch vs Aura vs Figma vs Claude Design, or before
  calling generate/edit MCP tools. Enforces ~400 Stitch credits/day. Points to
  phased pack skills: enhance-prompt → generate-design → extract → build → loop.
---

# Google Stitch — pack router + credit budget

Remote MCP: `https://stitch.googleapis.com/mcp`  
Setup: [Stitch MCP docs](https://stitch.withgoogle.com/docs/mcp/setup/)  
Upstream skill bodies: [google-labs-code/stitch-skills](https://github.com/google-labs-code/stitch-skills) (Apache-2.0) — bundled here as `stitch-*` skills.  
Phase map: [`STITCH_PHASES.json`](../STITCH_PHASES.json)

## Credits (~400 / day) — non-negotiable

- Prefer **read** MCP tools first (`list_projects`, `get_project`, `list_screens`, `get_screen`, `list_design_systems`).
- Generate/edit/variant **only when the user asked** for new or changed UI.
- One strong prompt > many regenerations; batch into one `edit_screens` when possible.
- Default model **`GEMINI_3_FLASH`**; use `GEMINI_3_1_PRO` only if the user asks.
- Avoid high-count `generate_variants` unless requested.
- On quota errors: **stop** and report — no retry-spam.

## Phases (load these skills)

| Phase | Skills | Purpose |
|-------|--------|---------|
| **0 Router** | `stitch-mcp-design` (this) | Budget + path choice vs Aura/Figma/Claude Design |
| **1 Prompt** | `stitch-enhance-prompt`, `stitch-taste-design` | Strengthen brief / taste before spending credits |
| **2 Design** | `stitch-generate-design`, `stitch-manage-design-system`, `stitch-upload-to-stitch` | Create/iterate screens & systems in Stitch via MCP |
| **3 Extract** | `stitch-extract-design-md`, `stitch-extract-static-html`, `stitch-design-md`, `stitch-code-to-design` | Pull design DNA / HTML / MD out of Stitch or code |
| **4 Build** | `stitch-react-components`, `stitch-shadcn-ui`, `stitch-react-vite-dashboard`, `stitch-react-native`, `stitch-remotion` | Implement extracted design in app frameworks |
| **5 Iterate** | `stitch-loop` | Closed-loop refine after verify |

Always open the **phase skill’s** `skills/<slug>/SKILL.md` (not only this router).

## vs Aura / Figma / Claude Design

Canonical copy: repo `AGENTS.md` § Design path matrix

| Path | Skill | When |
|------|-------|------|
| **1D Stitch** | this + phase skills | Greenfield NL → Stitch screens → code |
| **1C Aura** | `aura-screenshot-clone` | Clone a **live URL/screenshot** |
| **1B Figma** | Figma MCP / figma-design-to-code | Designer Figma file is SoT |
| **1A Claude Design** | `claude-design` | Claude Design canvas / brand system mockups |
| Assets | `mengto-aura-asset-images` | Stock imagery only |

## MCP setup (Cursor)

User MCP config (`%USERPROFILE%\.cursor\mcp.json`) — **never commit keys**:

```json
"stitch": {
  "url": "https://stitch.googleapis.com/mcp",
  "headers": { "X-Goog-Api-Key": "<STITCH_API_KEY>" }
}
```

Example (no secret): [`docs/mcp.stitch.example.json`](../../docs/mcp.stitch.example.json)

## Suggested flow

0. Credit check — skip generate if a local craft skill is enough.  
1. Phase 1 prompt skills if the brief is vague.  
2. Phase 2 `stitch-generate-design` (Flash).  
3. Phase 3 extract.  
4. Phase 4 build into the product.  
5. Verify (`ui-fix-observe-first` / `frontend-audit`) → Phase 5 `stitch-loop` if needed.

## Security

Never commit API keys. Prefer env `STITCH_API_KEY`. Revoke in Stitch Settings if leaked.
