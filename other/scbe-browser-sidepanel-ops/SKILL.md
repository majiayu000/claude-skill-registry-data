---
name: scbe-browser-sidepanel-ops
description: Build, improve, and package the local AetherBrowse browser with an AI sidepanel workflow, governance checks, and app-store-ready Android artifacts.
---

# SCBE Browser Sidepanel Ops

Use this skill when work is specifically about improving the local AetherBrowse browser and shipping it toward Google Play or Amazon Appstore.

## Trigger Phrases

- "AetherBrowse in local files"
- "make the browser better"
- "AI side panel browser"
- "package and sell on app store"

## Local System Targets

- Browser core: `src/browser/`
- Native stack launcher: `scripts/system/start_aether_native_stack.ps1`
- App packaging target: `kindle-app/`
- Store packaging script: `scripts/system/package_aetherbrowse_appstore.ps1`

## Workflow

### 1) Research

- Collect source-backed ideas (arXiv abstracts + local docs/notes).
- Focus on measurable upgrades:
  - action success rate,
  - latency,
  - safety gate precision,
  - sidepanel usability.

### 2) Implement

- Make small, testable changes in local browser modules.
- Keep governance paths deterministic.
- Write/update release notes and store listing content.

### 3) Validate

- Run targeted tests first.
- Smoke test sidepanel/browser action flow.
- Verify no regression in safety decision paths.

### 4) Package

- Build AetherBrowse app artifact:
  - Play AAB:
    - `powershell -ExecutionPolicy Bypass -File scripts/system/package_aetherbrowse_appstore.ps1 -Format aab -Store play`
  - Amazon APK:
    - `powershell -ExecutionPolicy Bypass -File scripts/system/package_aetherbrowse_appstore.ps1 -Format apk -Store kindle`
- Confirm release manifest exists under `artifacts/releases/aetherbrowse-appstore/<timestamp>/release_manifest.json`.

### 5) Evidence + Handoff

- Emit cross-talk packet with:
  - what changed,
  - artifact paths,
  - risk and next action.
- Keep a short markdown launch note in `docs/ops/`.

## Output Contract

- Code diff for browser/package improvements
- Test output summary
- Release artifact path + SHA256
- Store listing markdown
- Cross-talk packet id

## Guardrails

- Do not publish/store-submit automatically without explicit user approval.
- Do not bypass governance checks for convenience.
- Keep secrets in env/secret store only.
