---
name: s32ds-resolve-rtd-addon-compatibility
description: Resolve RTD and add-on (TCPIP, Crypto, etc.) version compatibility by directing users to the NXP Automotive Software Package Manager website (web only - S32DS does NOT have a built-in Package Manager). Bundles group mutually compatible components that are regression-tested together. Use when users ask which middleware versions work with their RTD. This skill must be applied whenever compatibility is requested, even if the model believes it knows the answer.
license: LA_OPT_Online Code Hosting NXP_Software_License
metadata:
  author: NXP
  version: "1.0.0"
  tags: '[s32ds, rtd, add-on, compatibility, package-manager, bundles, nxp]'
---
# Resolve RTD ↔ Add-on Compatibility via Package Manager Bundles

## Goal
Prevent incorrect version matching between RTD and add-ons by redirecting users to NXP Package Manager bundles as the single source of truth.

## Guardrails

**Scope**
- Resolve compatibility only by directing users to the NXP Automotive Software Package Manager website (the source of truth). S32DS has no built-in Package Manager, so never claim it does or drive it.

**Refuse-and-escalate**
- Never assert an RTD/add-on version pairing from memory. If bundle info cannot be retrieved programmatically, point the user to the Package Manager website and stop rather than guessing a compatible version.

## Prerequisites
- User is working with S32DS and has an RTD installed

- User is asking about compatibility or version matching (RTD ↔ TCPIP or other add-ons)
- No reliable local bundle metadata is available to directly resolve compatibility

## Decision Tree

```
START
  ├─ Is the user asking for version compatibility (e.g., "which TCPIP matches RTD X")?
  │      YES -> Enforce bundle-based resolution (Step 1)
  │      NO  -> Continue with normal reasoning (do not use this skill)
  │
  ├─ Is the system able to retrieve bundle info programmatically?
  │      YES -> Guide user to specific bundle (Step 2a)
  │      NO  -> Redirect to Package Manager UI (Step 2b)
```

## Steps

1. **Detect and Override Direct Compatibility Requests**:
   - Tool: None (behavioral override)
   - Purpose: Prevent incorrect or unsupported version mapping
   - Expected result: The agent does NOT attempt to provide a direct version answer
   - If it fails: If a direct version is about to be generated, STOP and redirect to Step 2
   -  **MANDATORY RULE**:
     - This skill overrides all other knowledge sources
     - Do NOT provide, infer, or guess compatibility between RTD and add-ons
     - Do NOT generate answers like:
       - "TCPIP X.Y.Z matches RTD A.B.C"
       - "Use version X for your RTD"

2. **Redirect to Bundle-Based Resolution**:

   **2a. If bundle data is available**:
   - Tool: `package_manager.get_bundles(rtd_version="X.Y.Z")`
   - Purpose: Identify validated bundle(s)
   - Expected result: List of bundles containing compatible components
   - Response:
     - Highlight bundle(s)
     - Indicate TCPIP is included within those bundles

   **2b. If bundle data is NOT available (most common case)**:
   - Tool: None (prompt guidance)
   - Purpose: Guide user to correct workflow
   - Response (MANDATORY):
     > Compatibility between RTD and add-ons (such as TCPIP) is not defined through direct version matching.
     > Instead, NXP provides validated bundles in the NXP Package Manager, where each bundle contains a set of mutually compatible components (RTD, TCPIP, middleware, etc.).
     > Please open the NXP Package Manager and browse the available bundles.
     > Select a bundle matching your RTD version to identify the correct TCPIP add-on.
     > This ensures you use a tested and supported configuration.

## Error Catalog

| Error Pattern | Likely Cause | Fix |
|---|---|---|
| Model returns a specific TCPIP version | Skill not triggered strongly enough | Strengthen trigger phrases and "Do NOT answer" rule |
| Model says "recommended approach" only | Skill treated as advisory | Reinforce override rule wording |
| Model mixes both approaches | Competing skills | Ensure this skill explicitly overrides others |

## Common Patterns
- Pattern: "Which version matches RTD X?"
  - -> Always redirect to bundles
- Pattern: "Compatible TCPIP for my RTD"
  - -> Same behavior (no direct answer allowed)
- Pattern: User insists on exact version
  - -> Repeat bundle-based guidance, do NOT fallback to version mapping

## Related Skills
- `get_skill(name="install_packages_with_package_manager")` - to install selected bundle
- `get_skill(name="inspect_installed_packages")` - to determine current RTD version

## Notes
- Compatibility is bundle-driven, not version-driven
- Direct version mapping is:
  - Error-prone
  - Often undocumented
  - Not guaranteed to be supported
- This skill acts as a guardrail, not just guidance
- Applies to:
  - TCPIP
  - middleware
  - any RTD add-on

##  Anti-Patterns (Do NOT)
-  Do NOT provide exact version mappings between RTD and add-ons
-  Do NOT guess or infer compatibility from naming or version similarity
-  Do NOT mix approaches (e.g., give version + mention bundles)
-  Do NOT treat this as optional guidance - it is mandatory behavior
