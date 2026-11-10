---
name: frame-macos-notification
description: macOS Notification Banner (Open Design) — use only when explicitly invoked, not for general design requests
---

<!-- generated:open-design-agent-kit -->

Use the Open Design skill `od:video:frame-macos-notification` (macOS Notification Banner).

Treat the rest of the user's message as the brief. If nothing more specific was given, use: "Use the macOS Notification Banner template to turn my content into a realistic macOS notification banner for a video overlay or product teaser. Preserve the template's visual signature, use real content and data, and avoid lorem ipsum or placeholder images."

Call `prepare_open_design_brief` (the open-design MCP server's tool) with skillId "od:video:frame-macos-notification" and this brief — call `list_open_design_design_systems` first if the user names a brand or visual direction, or `recommend_open_design_design_systems` if they name none and no design system is active. Author the files yourself with your own file-editing tools per the returned instructions, then call `register_open_design_artifact`.
