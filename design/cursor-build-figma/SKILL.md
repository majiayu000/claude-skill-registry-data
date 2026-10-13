---
name: cursor-build-figma
description: "Use for \"/cursor-build-figma\", a figma.com/design URL with node-id, or \"implement this Figma\" into a web, desktop, or shared UI. Orchestrates Figma MCP intake, maps nodes to the repo's own design system, then a cursor-verify-this visual judge. Do not paste Figma Tailwind."
# Intentionally model-invocable so agents discover it from Figma URLs.
---

## Codex capability boundary

This is source guidance, not an installed connector or a runtime proof. Resolve tools against the current host and read their actual schemas before using them. Preserve the named product and requested outcome. If a required operation is unavailable, report its exact name and leave that step incomplete. Do not invent tool names, connect accounts, install helpers, spend money, or broaden access from this document alone. Current operator authorization and native permissions govern every action.

Use native Codex delegation and the operator model policy. Missing named reviewers produce an incomplete review, never a clean verdict. Cursor plugins and built-in commands are not installed by this mirror. Read the adapted requirements reference before dependent work. Poteto owns its inline principle routing; no additional principle-pack-router pass is needed inside that workflow. System and developer instructions retain their priority. Existing operator authorization persists across turns unless withdrawn; do not ask again solely because a turn changed.

No sticky mode is claimed. Use native completion notifications for running workers. A recurring continuation requires the operator request and a supported native scheduling tool; do not emulate Cursor `/loop`.

# Build Figma

Orchestrator for Figma → production UI. It does **not** replace the skills below. Read each when that phase starts; do not restate them here.

**Requires** `figma` (plugin and connected MCP) and `cursor-team-kit`. Check first with [../cursor-dyl-mode/references/requirements.md](../cursor-dyl-mode/references/requirements.md). Missing → report the exact missing native capability and stop only the dependent step. Do not install a plugin automatically.

Failure modes that shaped the gates: [references/failure-lessons.md](references/failure-lessons.md).

## Delegate to (do not copy)

| Phase | Read |
| --- | --- |
| Figma MCP mechanics | `figma-design-to-code` from the Figma plugin, before every `get_design_context` |
| Design-system inventory | [references/design-system-discovery.md](references/design-system-discovery.md), then any repo-local design-system skill or rule it finds |
| Visual claim / verdict shape | `cursor-verify-this` from `cursor-team-kit` + [references/visual-judge.md](references/visual-judge.md) |
| Drive live UI | `cursor-control-ui` from `cursor-team-kit`, or the repo's own control skill for that surface |

## Gates

```
Build-figma progress:
- [ ] 0. Parse fileKey + nodeId (refuse file-only URLs)
- [ ] 1. Intake done before any product UI edit (see below)
- [ ] 2. Mapped to the repo's primitives/tokens only
- [ ] 3. Styling in the surface's own styling system
- [ ] 4. Visual judge VERIFIED per visual-judge.md (cursor-verify-this claim shape)
```

Gate 1 blocks coding. "Functional first, polish visuals later" is the main failure mode.

## Workflow (thin)

### 0. Parse URL

`figma.com/design/:fileKey/...?node-id=1-2` → `fileKey`, `nodeId` (`1-2` → `1:2`). Branch URLs use `branchKey` as `fileKey`. No `node-id` → stop.

### 1. Intake (blocking)

Follow `figma-design-to-code`. Call `get_design_context` and `get_screenshot`. If the response is sparse or too large, split to implementable **child** nodes. Download brand assets from MCP URLs; never redraw logos.

Run [design-system discovery](references/design-system-discovery.md). Then write `/tmp/cursor-build-figma/<slug>/intake.md`:

- Target surface, code path, and cursor-how you will drive it live.
- Node tree.
- **Metric table.** Figma px → token, or pinned value when no token matches.
- **Node → primitive map.** Each Figma node to an existing component. Mark any node with no match as new, with why.

### 2. Implement

Use the surface's styling system and the mapped components. When Figma px disagree with a primitive's default size, pin the Figma metric in that styling system. Do not bend the primitive's defaults globally. Hard bans below.

### 3. Visual judge (blocking)

Specialize `cursor-verify-this` with [references/visual-judge.md](references/visual-judge.md). Treat the Figma shot as baseline and the live capture as treatment. Match theme polarity first, then apply the rubric and write the verdict. After NOT VERIFIED, fix the failed rows, recapture, and apply the rubric again. Repeat until VERIFIED or INCONCLUSIVE. Stop and report the blocker after INCONCLUSIVE; do not claim Gate 4 complete.

### 4. Report

Intake path, map highlights, verdict + evidence paths, remaining gaps.

## Hard bans

1. Paste Figma MCP Tailwind/React as product code.
2. Invent brand assets when Figma or the repo has them.
3. "Close enough" primitive for a distinct Figma structure.
4. Trust text/button/dialog size tokens without checking Figma px.
5. Claim visual done without the judge.
6. Edit product UI before `intake.md` exists.
