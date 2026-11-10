---
name: vfx-text-cursor
description: VFX Text Cursor (Open Design) — use only when explicitly invoked, not for general design requests
---

<!-- generated:open-design-agent-kit -->

Use the Open Design skill `od:video:vfx-text-cursor` (VFX Text Cursor).

Treat the rest of the user's message as the brief. If nothing more specific was given, use: "Use the VFX Text Cursor template to turn my content into a video-intro quote reveal with cursor light trails, chromatic rays, and directional flares. Preserve the template's visual signature, use real content and data, and avoid lorem ipsum or placeholder images."

Call `prepare_open_design_brief` (the open-design MCP server's tool) with skillId "od:video:vfx-text-cursor" and this brief — call `list_open_design_design_systems` first if the user names a brand or visual direction, or `recommend_open_design_design_systems` if they name none and no design system is active. Author the files yourself with your own file-editing tools per the returned instructions, then call `register_open_design_artifact`.
