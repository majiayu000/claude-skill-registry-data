---
name: social-carousel
description: social-carousel (Open Design) — use only when explicitly invoked, not for general design requests
---

<!-- generated:open-design-agent-kit -->

Use the Open Design skill `od:prototype:social-carousel` (social-carousel).

Treat the rest of the user's message as the brief. If nothing more specific was given, use: "Design a 3-card cinematic social carousel — ‘onwards.’, ‘to the next one.’, ‘looking ahead.’. 1080×1080 squares, drop-into-Instagram ready."

Call `prepare_open_design_brief` (the open-design MCP server's tool) with skillId "od:prototype:social-carousel" and this brief — call `list_open_design_design_systems` first if the user names a brand or visual direction, or `recommend_open_design_design_systems` if they name none and no design system is active. Author the files yourself with your own file-editing tools per the returned instructions, then call `register_open_design_artifact`.
