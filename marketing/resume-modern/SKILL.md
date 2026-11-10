---
name: resume-modern
description: Modern Resume (Open Design) — use only when explicitly invoked, not for general design requests
---

<!-- generated:open-design-agent-kit -->

Use the Open Design skill `od:prototype:resume-modern` (Modern Resume).

Treat the rest of the user's message as the brief. If nothing more specific was given, use: "Use the Modern Resume template to turn my content into a modern minimal single-page A4 resume ready for print or PDF export. Preserve the template's visual signature, use real content and data, and avoid lorem ipsum or placeholder images."

Call `prepare_open_design_brief` (the open-design MCP server's tool) with skillId "od:prototype:resume-modern" and this brief — call `list_open_design_design_systems` first if the user names a brand or visual direction, or `recommend_open_design_design_systems` if they name none and no design system is active. Author the files yourself with your own file-editing tools per the returned instructions, then call `register_open_design_artifact`.
