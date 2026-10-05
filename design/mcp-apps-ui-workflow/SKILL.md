---
name: mcp-apps-ui-workflow
description: Use this skill when designing, reviewing, migrating, or debugging MCP Apps / SEP-1865 interactive UI resources for MCP servers, including dashboards, forms, visualizations, tool-driven workflows, OpenAI Apps SDK migration, MCP-UI compatibility, sandboxing, host support, security review, provenance, and fallback UX.
---

# MCP Apps UI Workflow

Plan MCP Apps as MCP integrations with a visible UI surface, not as ordinary frontend widgets. The UI, tool contract, host permissions, and audit path must be designed together.

## Workflow

1. Verify current sources before implementation:
   - MCP Apps overview, stable spec, and client support matrix.
   - Official MCP security guidance and project-local MCP inventory.
   - Existing server SDK, transport, auth, and tool schemas.
2. Classify the UI job: dashboard, form/wizard, data visualization, design canvas, media player, configuration flow, or human approval screen.
3. Choose the smallest path:
   - Add an MCP App to an existing MCP server when tools and auth already exist.
   - Convert an existing web app only when it has a durable conversational workflow.
   - Use a normal web UI when inline chat rendering adds no user value.
4. Declare the app boundary:
   - Predeclare UI resources and tool metadata.
   - Keep tool input/output schemas typed and minimal.
   - Route every UI-initiated action through the same consent, audit, and validation path as direct tool calls.
5. Design the host contract:
   - Check supported clients before promising behavior.
   - Provide text or structured-data fallback for unsupported hosts, reduced motion, and low-power devices.
   - Avoid depending on host-specific globals unless the target host explicitly documents them.
6. Apply source ranking before adopting SDKs or examples. Prefer official MCP Apps docs and SDKs, then MCP-UI patterns when license and compatibility are confirmed.
7. Run MCP security review for auth scopes, prompt/tool boundaries, untrusted UI content, data exfiltration, clickjacking-like confusion, SSRF, command/file paths, and destructive tool flows.
8. Validate with the narrowest checks that prove the integration:
   - schema validation for resources and tool metadata;
   - local MCP inspector or host smoke test;
   - browser screenshot/interaction check for the iframe UI;
   - accessibility, keyboard, responsive, and reduced-motion checks;
   - sanitized audit log review.

## Checklist

- The MCP App solves a real interactive workflow that text output cannot handle well.
- Resource declarations, content types, and tool metadata follow the current stable spec.
- Host compatibility and fallback behavior are explicit.
- UI actions cannot bypass typed MCP tools, user consent, or audit logging.
- External examples, components, and assets have license/provenance notes before reuse.
- Security review covers OAuth/session handling, secrets exposure, untrusted content, and destructive actions.
- Performance budget covers bundle size, asset size, startup time, and mobile behavior.

## Guardrails

- Do not install or enable MCP servers, publish registry packages, deploy production servers, or grant OAuth scopes without explicit approval.
- Do not embed secrets, tokens, private URLs, or personal data in UI resources, logs, screenshots, or tool metadata.
- Do not copy MCP App examples, frontend components, or assets without confirming license and source provenance.
- Do not treat sandboxed UI as trusted input; validate every message, URL, file path, and tool argument server-side.
- Do not claim ChatGPT, Claude, VS Code, or another host supports a feature without checking current official docs.
