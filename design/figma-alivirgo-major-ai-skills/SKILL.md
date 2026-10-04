---
name: figma
description: "Build Figma plugins, export selected frames, audit components, and map variables to design tokens using the Plugin and REST APIs."
category: design
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["figma", "plugin-api", "rest-api", "design-tokens", "variables", "components", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# Figma Design Systems & Plugin AI Skill Guide (Claude)

## Overview & Engine Architecture
Figma is a collaborative vector design platform with a document model of **Pages → Frames → Nodes**, reusable **Components / Variants**, and **Variables** (design tokens). Automation spans the in-editor **Plugin API** (`figma` global in sandbox) and the cloud **REST API** for file metadata, comments, and exports. Claude operates as a Principal Design Systems Engineer, specializing in **plugin tooling**, **token extraction**, **component audit scripts**, and **REST-based CI export**.

### Figma Document & API Stack

```
┌─────────────────────────────────────────────────────────────┐
│                 Figma Architecture                          │
│                                                             │
│  Document Graph                                             │
│  ├── Document / Page / Frame / Group / Text / Vector        │
│  ├── Components / Component Sets / Instances                │
│  └── Variables / Styles / Auto Layout                       │
│                                                             │
│  In-Editor Automation                                       │
│  ├── Plugin sandbox (TypeScript/JS) + UI iframe             │
│  ├── figma.currentPage.selection / node traversal           │
│  └── clientStorage / notify / exportAsync                   │
│                                                             │
│  Cloud REST                                                 │
│  ├── Files / Nodes / Images / Comments                      │
│  ├── Variables REST (Enterprise surfaces)                   │
│  └── Personal access tokens / OAuth                         │
└─────────────────────────────────────────────────────────────┘
```

---

## Operational Capabilities & Agent Directives

1. **Plugin vs REST**: Use Plugin API for live canvas mutations; use REST for CI exports and metadata outside the editor.
2. **Selection Guards**: Always validate `figma.currentPage.selection` length and node types before mutating.
3. **Token Discipline**: Map Variables → platform tokens (CSS/JSON) with stable names; never invent IDs.
4. **Component Hygiene**: Prefer instances over detached copies; flag detached instances in audits.
5. **Permissions**: REST calls require a token with the minimum scopes; never hardcode secrets in plugins.

---

## Production TypeScript: Figma Plugin - Export Selected Frames as PNG

`code.ts` (plugin main):

```typescript
// ==============================================================================
// Figma Plugin API: export selected frames to PNG bytes and message UI
// ==============================================================================
async function exportSelectedFrames() {
  const selection = figma.currentPage.selection;
  const frames = selection.filter((n) => n.type === "FRAME") as FrameNode[];

  if (frames.length === 0) {
    figma.notify("Select one or more frames to export.");
    return;
  }

  const payloads: { name: string; bytes: Uint8Array }[] = [];
  for (const frame of frames) {
    const bytes = await frame.exportAsync({
      format: "PNG",
      constraint: { type: "SCALE", value: 2 },
    });
    payloads.push({ name: frame.name.replace(/\s+/g, "_"), bytes });
  }

  figma.ui.postMessage({ type: "EXPORT_READY", payloads });
  figma.notify(`Exported ${payloads.length} frame(s) @2x`);
}

figma.showUI(__html__, { width: 360, height: 240 });
figma.ui.onmessage = async (msg) => {
  if (msg.type === "RUN_EXPORT") await exportSelectedFrames();
  if (msg.type === "CLOSE") figma.closePlugin();
};
```

REST export example (CI):

```bash
curl -H "X-Figma-Token: $FIGMA_TOKEN" \
  "https://api.figma.com/v1/images/:file_key?ids=1:2&format=png&scale=2"
```

---

## Technical Troubleshooting Matrix

| Issue & Failure Signature | Root Cause Analysis | Diagnostic & Resolution Pathway |
| :--- | :--- | :--- |
| **Plugin `exportAsync` fails** | Node not exportable / too large. | Export frames/components; reduce scale; check bounds. |
| **REST 403** | Bad token or missing scope. | Regenerate PAT; confirm file access for the user. |
| **Detached instances proliferate** | Designers detached to override. | Audit + re-instance; use preferred values / variables. |
| **UI iframe CSP issues** | External scripts blocked. | Bundle UI assets; follow Figma plugin UI rules. |

---

## Best Practices

1. Traverse with `node.findAll` / `findAllWithCriteria` instead of brittle absolute paths.
2. Use `figma.notify` for operator feedback; keep plugin UI minimal.
3. For design tokens, prefer Variables over hard-coded paint styles when available.

### Essential References
- Plugin typings: `@figma/plugin-typings`
- REST base: `https://api.figma.com/v1`
- Manifest: `manifest.json` (`main`, `ui`, `networkAccess`)

---

## Agent Operational Directive
> **MANDATORY**: Never embed Figma access tokens in plugin source committed to git. Validate selection node types before mutation. Prefer Variables/components for system changes over one-off node edits.
