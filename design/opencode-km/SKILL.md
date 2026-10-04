---
name: opencode
description: "Use Open Design as the local professional design agent: Claude Code-first runs, design systems, skills, plugins, media generation, previews, and MCP/CLI/HTTP control. Use when Kosta says Open Design, opencode, design agent, design system, deck, landing page, prototype, visual polish, or asks for professional design output."
argument-hint: "[brief] [mode: web|deck|prototype|media|audit|plugin] [design-system]"
metadata:
  version: "2026-05-28"
  owner: KM
  skill_group: Open Design
---

# opencode — Open Design operator

Use this skill when Kosta wants Open Design wired into a design workflow, or when a design task should produce a polished artifact instead of generic implementation notes.

Open Design is local-first. On the Mac Studio it is installed at `~/LocalDev/.studio-only/open-design`, uses data dir `~/.open-design`, runs the daemon at `http://127.0.0.1:7456`, and the web UI at `http://127.0.0.1:5176`. The default Open Design agent is Claude Code (`agentId: claude`, model `default`).

## Quick health check

```bash
export PATH="$HOME/.local/bin:/opt/homebrew/bin:$PATH"
od status --json | jq
curl -sS http://127.0.0.1:7456/api/health | jq
curl -sS http://127.0.0.1:7456/api/app-config | jq '.config | {agentId, agentModels}'
```

Expected: health is OK, `agentId` is `claude`, and `/api/agents` shows Claude Code available. If the daemon is down, start it from the repo with `pnpm tools-dev`, or run the packaged app if installed.

## Surfaces

Use the smallest surface that fits:

- MCP: best default inside Hermes/Codex/Claude when the `open-design` MCP tools are available. Use it for listing skills/design systems, starting runs, reading artifacts, and refreshing live previews.
- CLI: best for repeatable shell work and quick inspection: `od skills list --json`, `od design-systems list --json`, `od run ... --json --follow`, `od project list --json --daemon-url http://127.0.0.1:7456`.
- HTTP API: best for stateless reads and custom scripts: `/api/health`, `/api/skills`, `/api/design-systems`, `/api/projects`, `/api/plugins`, `/api/agents`, `/api/mcp/install-info`.
- Skills only: best when the daemon is unavailable but a template skill can still guide a normal code agent.

## Modes

### web
Use for landing pages, product pages, dashboards, and app screens. Default plugin: `od-new-generation`. Ask for real HTML/CSS/React output, visible hierarchy, responsive states, and screenshot/preview evidence.

Prompt shape:

```text
Use Open Design with Claude Code as the agent. Mode: web. Create a polished <surface> for <product/audience>. Prefer a professional design-system-backed result over generic Tailwind blocks. Use design system <name or let Open Design choose>. Produce runnable artifact files, then report the preview URL/artifact path and the specific visual QA checks performed.
```

### deck
Use for slide decks, pitch decks, research stories, explainers, and visual narratives. Ask for slide count, audience, tone, and constraints when missing.

Prompt shape:

```text
Use Open Design with Claude Code as the agent. Mode: deck. Build a <N>-slide <deck type> for <audience>. Structure the story first, then generate a polished deck artifact with strong typography, pacing, and speaker-readable hierarchy. Include slide titles, visual direction, and final artifact path.
```

### prototype
Use for app flows, interaction design, clickable concepts, and multi-state UI. Require states and transitions.

Prompt shape:

```text
Use Open Design with Claude Code as the agent. Mode: prototype. Create a prototype for <flow>. Include states for <empty/loading/error/success/etc.>, responsive behavior, and realistic content. Verify the preview visually and list the unresolved UX risks.
```

### media
Use for image/video/audio generation through Open Design's media provider layer. Prefer Kosta's configured RTX/image workflow outside Open Design only when he explicitly wants RTX-first generation rather than Open Design artifact generation.

Prompt shape:

```text
Use Open Design media mode to generate <image/video/audio> for <purpose>. Specify surface, aspect ratio, model/provider if configured, prompt, output path, and any negative constraints. Return generated file paths and provider errors if any.
```

### audit
Use for visual critique, design-system conformance, screenshot-to-improvement, and “make this less AI-slop” passes.

Prompt shape:

```text
Use Open Design as a design critic. Inspect <artifact/screenshot/project>. Judge hierarchy, spacing, typography, color, brand fit, accessibility, responsiveness, and interaction polish. Give concrete fixes, then apply the smallest high-impact changes if files are available.
```

### plugin
Use for installing/applying Open Design plugins, seeded examples, or repeatable scenarios.

Prompt shape:

```text
Use Open Design plugin mode. Inspect available plugins, choose the best match for <goal>, apply it, run with prompt <brief>, stream events, and return the artifact paths plus any plugin inputs that matter for reruns.
```

## Run patterns

List capabilities:

```bash
od skills list --json | jq '.skills[].name'
od design-systems list --json | jq '.designSystems[].id'
curl -sS http://127.0.0.1:7456/api/agents | jq '.agents[] | select(.available) | {id,name,path,version}'
```

Create a project through HTTP:

```bash
curl -sS -X POST http://127.0.0.1:7456/api/projects \
  -H 'content-type: application/json' \
  -d '{
    "name": "Hermes design run",
    "metadata": {"kind": "prototype"},
    "pendingPrompt": "A polished landing page for an AI agent CLI",
    "pluginId": "od-new-generation",
    "autoSendFirstMessage": true
  }' | jq
```

Fetch MCP install info from the live daemon instead of hand-writing config:

```bash
curl -sS http://127.0.0.1:7456/api/mcp/install-info | jq
```

## Operating rules

- Default to Claude Code inside Open Design unless Kosta asks for Codex, Gemini, Hermes, or another runtime.
- For high-stakes visual work, inspect the generated artifact visually before calling it done. A successful run is not proof of good design.
- Prefer named design systems when the brand/aesthetic is known; otherwise ask Open Design to select a matching design system and explain why.
- Keep outputs artifact-first: preview URL, local file paths, screenshots, and concrete QA notes.
- Do not store API keys or provider tokens in skill files, prompts, screenshots, or artifacts.
- If `od doctor` crashes, do not treat that as fatal if `od status`, `/api/health`, CLI listing, MCP, and project runs still work.

## Completion checklist

Before telling Kosta it is done, verify the relevant path:

- setup/config: `od status --json`, `/api/health`, `/api/app-config`
- capability discovery: `/api/skills`, `/api/design-systems`, `/api/agents`
- artifact generation: project/run exists, artifact file exists, preview or screenshot checked
- MCP wiring: `/api/mcp/install-info` plus the client sees `open-design` tools
