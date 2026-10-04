---
name: read-codebase
description: >
  Read the full ndestates-io codebase (Laravel 12 + Filament 5 property data/valuations platform), document key findings, and cache the result locally (docs/codebase/ + .grok/.copilot memories/repo) for easy reference and future updates.
  Use for onboarding, major cache refresh, or /read-codebase. Rare for daily work.
argument-hint: "Optional focus: Filament, services, valuations, full"
user-invocable: true
disable-model-invocation: false
---

# Read Codebase + Cache

**Cache the knowledge** for future efficient sessions.

## Mandatory Steps
1. Initial Scan & Intent: ls key dirs, read `.github/copilot-instructions.md`, existing cache state, summarize purpose (property/valuations platform, ignore pandas/Stats artifacts).
2. Deep Exploration: target Filament resources/panel providers, signing/PDF services, Models (Document, SignatureRequest, Signer, Signature + observers), migrations, scripts (ci_security), document embedding flows, DDEV, auth and token security.
3. Cache Locally (Required):
   - Create/update `docs/codebase/` (README, ARCHITECTURE, STRUCTURE for panels, CONVENTIONS, TESTING, CONCERNS, etc.) with [UPDATED date] markers + `.codebase-scan.txt`.
   - Update repo memory ` .copilot/memories/repo/ndestates-io-codebase-cache.md ` + sync to `.grok/memories/`.
   - Update INDEX guidance.
4. Validation: every claim with file paths; end with Cached Knowledge Locations + follow-up prompt examples.

Use read-only subagents for scan steps. Full details in `.grok/prompts/read-codebase.md`.

Follow `.github/copilot-instructions.md` throughout.
