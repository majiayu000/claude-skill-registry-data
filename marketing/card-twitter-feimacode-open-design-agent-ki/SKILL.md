---
name: card-twitter
description: Twitter Share Card (Open Design) — use only when explicitly invoked, not for general design requests
---

<!-- generated:open-design-agent-kit -->

Use the Open Design skill `od:prototype:card-twitter` (Twitter Share Card).

Treat the rest of the user's message as the brief. If nothing more specific was given, use: "Use the Twitter Share Card template to turn my content into a Twitter quote or data card designed to pair with a post. Preserve the template's visual signature, use real content and data, and avoid lorem ipsum or placeholder images."

Call `prepare_open_design_brief` (the open-design MCP server's tool) with skillId "od:prototype:card-twitter" and this brief — call `list_open_design_design_systems` first if the user names a brand or visual direction, or `recommend_open_design_design_systems` if they name none and no design system is active. Author the files yourself with your own file-editing tools per the returned instructions, then call `register_open_design_artifact`.
