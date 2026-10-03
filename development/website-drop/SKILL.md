---
name: website-drop
description: Audit a local web app, choose the simplest host, and get it to a live URL fast. Use when Codex needs to prep a site for deploy, confirm the build path, and ship it with minimal hosting overhead.
---

# Website Drop

Use this skill when the user wants a web project checked, deployment-ready, and live with the shortest sensible path.

## Quick Start

1. Detect the app type, install command, build command, and output directory first.
2. Prefer the lightest host that matches the project and user constraints.
3. Keep the goal simple: audit, build, deploy, and return the live link.
4. Add platform config only when the target host actually needs it.
5. If a platform-specific deploy skill fits better, route to it instead of duplicating the flow.

## Workflow

### Choose The Path

- For static or framework sites, prefer straightforward hosts such as Vercel, Netlify, or Cloudflare when they match the project.
- If the user names a platform, align the deployment flow to that platform instead of abstracting it away.
- If deployment depends on environment variables, call that out before shipping.
- If the repo already contains deployment config, preserve it and finish the flow instead of replacing it.

### Prepare The Project

- Confirm the install, build, and output directory commands from the existing project files.
- Keep deployment config as small as possible.
- Avoid adding hosting-specific files that duplicate what the framework already provides.
- Verify that the built output actually exists before claiming the site is ready to deploy.

### Required Deliverables

- One clear hosting recommendation with a short reason.
- The exact build command and output directory.
- The minimum config or command needed to deploy.
- The resulting live URL or the exact user handoff needed to get it.

### Routing Rules

- If the user explicitly wants Vercel, use the `vercel-deploy` skill when available.
- If the user explicitly wants Netlify, use the `netlify-deploy` skill when available.
- If the user explicitly wants Cloudflare, use the `cloudflare-deploy` skill when available.
- If no host is named, choose the simplest stable path based on the project and explain why.

### Editing Guidance

- Optimize for one repeatable deploy flow, not every possible host.
- Keep outputs short, specific, and action-oriented.
- Return the exact command or handoff needed to get a live URL.
- Avoid adding deployment clutter for hosts the user is not using.

## Resources

- `agents/openai.yaml`: UI metadata and default invocation prompt.
- `assets/`: branded icons for repo listings and skill chips.
- `references/deploy-heuristics.md`: quick matrix for choosing a host and minimizing config.
