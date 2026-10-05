---
name: map-feature-gates
description: Use when you need to understand why capabilities differ across configurations, user types, or deployment environments, or when investigating feature flags and capability gates
---

## Announce at start: "Using codebase-analyzer to map feature gates."

## Overview

Map the gates that control which capabilities are available under which conditions. Gates are the control plane -- understanding them reveals what the system was designed to restrict and to whom.

**Prerequisite:** Reads `docs/analysis/tool-graph.md` (from extract-tool-graph) and `docs/analysis/build-pipeline.md`.

## Five Gate Types with Detection

### Build-Time Gates

Tools filtered during compilation. These never reach the runtime artifact.

- **Where to look:** Build config, preprocessor directives, build scripts
- **Detection patterns:** `#ifdef` / `#ifndef`, `process.env` checks in build scripts, conditional exports in `package.json`, webpack `DefinePlugin`, tree-shaking directives
- **Example:** `if (process.env.NODE_ENV === 'production') includeAnalytics();`

### Runtime Gates

Tools enabled or disabled based on runtime state.

- **Where to look:** Feature flag checks, config reads, state conditionals
- **Detection patterns:** `flags.isEnabled('x')`, `user.type === 'admin'`, `env === 'production'`, `version >= '2.0'`, capability checks like `'speechRecognition' in navigator`
- **Example:** `if (user.type === 'admin') registerAdminTools();`

### Permission Gates

Tools restricted by role or permission level.

- **Where to look:** Auth checks, role verification, access control logic
- **Detection patterns:** `user.role === 'admin'`, `user.can('write')`, `token.scope.includes('api:write')`, `acl.check(resource, action)`
- **Example:** `if (hasPermission('write')) { enableEditTools(); }`

### Provider Gates

Tools available only for specific backends or providers.

- **Where to look:** Provider-specific code paths, backend routing
- **Detection patterns:** `config.provider === 'openai'`, `typeof openai !== 'undefined'`, `switch(provider) { case 'aws': ... }`
- **Example:** `if (provider === 'openai') registerOpenAITools();`

### Config Gates

Tools controlled by environment variables, settings files, or feature flag services.

- **Where to look:** Feature flag services (GrowthBook, Unleash, LaunchDarkly), environment variables, database flag tables, remote config endpoints
- **Detection patterns:** `config.featureEnabled('x')`, `process.env.ENABLE_X`, feature_flags table queries, `/api/config` responses
- **Example:** `if (config.featureEnabled('beta-api')) exposeBetaEndpoint();`

## Hidden Capability Detection

Tools defined but never registered in any gate configuration are dead, hidden, or upcoming. Cross-reference with dead-code analysis.

**Detection approach:**
1. Enumerate all tool definitions found in `docs/analysis/tool-graph.md`
2. For each tool, trace registration path through all five gate types
3. Tools with no gate controlling their registration fall into three categories:
   - **Dead code:** Once used, now orphaned
   - **Hidden features:** Intentionally unregistered, awaiting activation
   - **Upcoming:** Implemented but not yet wired into the product
4. Cross-reference with dead-code analysis to distinguish categories

## SECURITY_SIGNAL

Gates are a security boundary. Flag the following:

- Gates that bypass authentication in non-production environments
- Capability escalation paths through gate chaining
- Hidden admin gates not documented in access control policies
- Feature flags that disable security controls without audit logging
- Provider gates that fall back to less-secure backends without warning

## Adversarial Lens

If a gate was designed to be bypassable, what would it look like? Check: gates that check permissions but have a fallback that grants access, feature flags that default to "on" in production, admin checks that can be bypassed via API parameter. The most dangerous gate is one that looks like it works but doesn't.

## Red Flags

- Only finding explicit gates, missing implicit ones (like build-time filtering)
- Not checking for gate bypass conditions (what happens when a gate fails open?)
- Treating all gates as equal -- a build-time gate and a runtime gate have different threat models
- Missing dynamic tool registration patterns that create gates at runtime

## Output Contract

Write `docs/analysis/gate-map.md` using standard contract.

Include:
- Gate inventory grouped by type
- Tool-to-gate mapping (which gates control which tools)
- Hidden capabilities section
- Security signal findings
- Cross-reference with tool-graph and build-pipeline outputs
