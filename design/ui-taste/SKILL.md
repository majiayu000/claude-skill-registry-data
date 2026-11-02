---
name: ui-taste
description: Give your coding agent better UI taste. Build and polish web and iOS interfaces with Uizze's anti-ui-slop playbooks and optional real-product references. Use for UI design, implementation, redesign, critique, or a final visual review in Claude Code, Codex, Cursor, or Copilot.
license: Apache-2.0; see LICENSE and NOTICE for third-party attribution
metadata:
  version: "0.3.0"
  author: "UIZZE <business@uizze.com>"
  compatibility: "Designed for Claude Code, Codex, Cursor, and GitHub Copilot; works in any agent that can read project files and fetch a URL."
  tags: "ui-design, design-system, design-review, frontend, web-ui, ios-ui"
category: frontend-visual-taste
---

![Stop Making UI Slop with UIZZE](https://uizze.com/landing/anti-ui-slop-skill-banner.png)

# UI Taste by Uizze

**Stop shipping the same AI slop.**

“Make it look better” gets old after the tenth prompt. Give your agent a workflow for choosing layouts, fixing visual hierarchy, and polishing the details you notice when you use the app.

Built on [Uizze's](https://uizze.com) anti-ui-slop workflow. Focused design playbooks for web and iOS, including native audits, with optional real-product references, fonts and icons through Uizze MCP.

**Free skill. No account required.** Agent-connected references and materials use the optional paid MCP.

## Prerequisites

- A screen or component to build, redesign, or review — a file path or a short description.
- Existing components, design tokens, and visual language, when available. For a new project, establish a small coherent system from the brief rather than requiring an existing one.
- Optional access to the paid Uizze MCP for focused references and hosted materials.

## Authentication

- The free skill and public catalogue work without an account, token, MCP connection, dependency, script, or executable.
- The optional full UIZZE MCP may use the host's normal connection and authentication flow. Never claim it is connected without an actual host result.

## Work from the product

Read the brief, existing UI, components, tokens, assets, and any PRODUCT.md or DESIGN.md before designing. The user's request and project constraints outrank this skill. Preserve an established visual system for extensions and polish; replace it only for an approved redesign. A new project does not require those files.

Identify the audience, primary task, important states, and intended result. Ask only about missing choices that would materially change the work. A precise request is enough to proceed; do not turn a small fix into a discovery workshop.

## Image first, then implement

Follow [Uizze's image-to-UI workflow](references/uizze-image-to-ui.md) before visual implementation. When an authorized image-generation tool is available, new visual work and approved redesigns start with a realistic UI image, inspected before code. An approved supplied image takes precedence. Save its actual dimensions and build the target 1:1 with semantic components and real controls, not a screenshot background.

Render at that viewport once assets and fonts load, compare with the stable target, correct visible mismatches and inspect again. Preserve the approved identity at other sizes. A small technical fix or read-only audit does not need a new image; if image tools are unavailable, explain that and use an existing target or the project's conventions without pretending generation or visual verification succeeded.

## Select the workflow

Load the playbook for the requested action, plus the platform and craft guidance needed to execute it:

- New interface or major redesign: [new-work](reference/new-work.md)
- Product or dashboard work: [operate](reference/operate.md)
- Refinement and polish: [polish](reference/polish.md)
- Simplification: [distill](reference/distill.md)
- Explicit web audit: [audit](reference/audit.md), read-only unless fixes were requested
- Native iOS: [iOS](reference/ios.md), alongside the action's playbook; for an audit, use [native audit](reference/audit.native.md) instead of a DOM scan
- Explicit `/overdrive`, “Uizze Overdrive”, or a request for exceptional interaction work: [Overdrive](reference/overdrive.md)

For implementation, use [craft](reference/craft.md) after the direction is settled. Load only relevant files; multiple complementary playbooks are allowed. Overdrive is opt-in, not the default for ordinary UI work. It requires a chosen direction before implementation.

“Use Uizze Overdrive on this screen” works through this router; a native slash command depends on the host. These are self-contained Markdown playbooks, not an installer, background service, or executable engine.

## Optional Uizze evidence

Read [the reference policy](references/uizze-reference-policy.md) before using `find_ui_references` or `find_ui_materials`. Inspect relevant visual evidence when it can inform the layout, state, interaction, or assets. Use the host's available tools, not invented calls or connections. Paid retrieval is optional; missing access does not block local design work.

Distinguish an exact reference, a related example, no match, and a service error. Briefly disclose a limitation that affected the result. Never claim an image was inspected or a state was found without evidence.

## Finish

Build the requested scope and exercise its important states. Render and inspect the real result at representative desktop/mobile sizes or native device classes, including the user's reported failing size. Compare it with the chosen direction or supplied reference, not just with the absence of runtime errors.

Fix material problems in a batch, then render and inspect again. Stop once the requested result is verified; do not keep inventing work. If a bounded pass cannot resolve an issue, report it instead of claiming a pass. When rendering is unavailable, distinguish code checks from visual verification.

Keep the handoff concise: what changed, what was actually tested, and any remaining limitation. A skill does not authorize publishing, purchases, new dependencies, account changes, or destructive actions.
