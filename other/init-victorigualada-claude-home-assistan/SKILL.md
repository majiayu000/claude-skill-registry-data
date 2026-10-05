---
name: ha:init
description: Initialize plugin in a project — install Iron Laws, auto-activation rules, and reference auto-loading into CLAUDE.md. Use when setting up or updating the plugin.
effort: low
argument-hint: [--update]
---

# Plugin Initialization

Install the Home Assistant plugin's behavioral instructions into the project's CLAUDE.md.

## Usage

```
/ha:init           # First-time installation
/ha:init --update  # Update existing installation with latest rules
```

## Iron Laws

1. **NEVER overwrite content outside plugin markers** — User-written CLAUDE.md rules must be preserved verbatim
2. **Always detect the target before generating** — Never assume core checkout vs custom integration vs frontend
3. **Always validate after installation** — Verify markers present and detected target correct

## Workflow

### Step 1: Check Existing CLAUDE.md

Use Glob to check if `CLAUDE.md` exists. Then use Grep to check for existing `HOME-ASSISTANT-PLUGIN:START` marker in `CLAUDE.md`.

### Step 2: Detect Project Target

Three-way detection (see `docs/conversion-guide.md` project-detection table):

| Target | Test |
|---|---|
| HA core checkout | `homeassistant/__init__.py` exists AND `script/` directory exists |
| Custom integration | `custom_components/*/manifest.json` glob matches |
| ha-frontend | `package.json` exists AND contains `"name": "home-assistant-frontend"` |

**Framework-development profile (third install profile)**: a core checkout or
frontend-repo checkout is ALSO a framework-development target — the person may be
developing `homeassistant/` itself or the frontend framework layer, not just an
integration. For these two targets, additionally install the `{FRAMEWORK_DEV_SECTION}`
(C-series/FI-series laws from the plugin's `docs/framework-dev-laws.md` + the
core-internals, dev-tooling, and architecture-process skills). Custom-integration
projects NEVER get this section.

Then refine:

- HA version: `homeassistant/const.py` `__version__` (core) / `hacs.json` or manifest `homeassistant` key (custom)
- Working domain(s): recently-edited `homeassistant/components/<domain>/` or `custom_components/<domain>/`
- Custom integration deps: manifest `requirements`
- Frontend: `yarn --version`, Web Awesome usage (`@home-assistant/webawesome` in package.json)
- Dev instance: devcontainer config / `config/` dir with `configuration.yaml` (core checkout)
- Project size: Glob count of `*.py` under the integration dir(s) or `src/**/*.ts` (frontend)

### Step 3: Handle Installation Modes

**Mode A: Fresh Install** (no CLAUDE.md or no markers)

1. Create/append to CLAUDE.md
2. Insert full behavioral instructions between markers
3. Include only the sections matching the detected target (core / custom integration / frontend)

**Mode B: Update** (`--update` flag or markers exist)

1. Find content between `<!-- HOME-ASSISTANT-PLUGIN:START -->` and `<!-- HOME-ASSISTANT-PLUGIN:END -->`
2. Replace with latest behavioral instructions
3. Preserve everything outside the markers

**CRITICAL: NEVER overwrite or delete existing CLAUDE.md content outside the plugin markers** — user-written rules, project conventions, and other plugin sections must be preserved verbatim

### Step 4: Generate Content

Write the following structure to CLAUDE.md:

```markdown
<!-- HOME-ASSISTANT-PLUGIN:START -->
<!-- Last updated: {date} | Plugin version: 1.0 | Target: {core checkout HA {version} | custom integration | ha-frontend} -->

# Home Assistant Plugin - Auto-Activation Rules

{Include all sections from the Content Template below, filtered by detected target}

<!-- HOME-ASSISTANT-PLUGIN:END -->
```

### Step 5: Output Summary

```
✅ Home Assistant plugin initialized

Detected target:
- {HA core checkout {version} | Custom integration ({domain}) | ha-frontend}
- {Dev instance (hass -c config / devcontainer) detected | not detected}
- {Frontend: Web Awesome era components | not applicable}

Added to CLAUDE.md:
- Auto-activation rules (complexity detection, interview mode)
- Agent trigger patterns ({n} agents available)
- Reference auto-loading ({n} reference docs)
- Iron Laws enforcement ({n} laws)
- Verification rules

Run /ha:init --update after plugin updates.
Run /ha:audit for a full project health check.
```

## Content Template

The exact content to inject is in `${CLAUDE_SKILL_DIR}/references/injectable-template.md`.

**Key structure:**

1. **7-Step Mandatory Procedure** — Claude Code MUST execute before every response
2. **Iron Laws** — STOP behavior on violations
3. **Conditional Sections** — Include based on detected target:
   - `{CORE_CHECKOUT_SECTION}` — If HA core checkout (script/hassfest workflow, dev instance)
   - `{CUSTOM_INTEGRATION_SECTION}` — If custom_components project (no hassfest/quality-scale CI, laws still apply)
   - `{FRONTEND_SECTION}` — If ha-frontend repo (Lit Iron Laws, yarn gates)
   - `{QUALITY_SCALE_SECTION}` — If integration work detected (scaffold + quality_scale.yaml discipline)
   - `{DEV_INSTANCE_SECTION}` — If a runnable dev instance is detected
   - `{FRAMEWORK_DEV_SECTION}` — If core checkout OR frontend repo (framework-development audience: C/FI law tier + core-internals/dev-tooling/architecture-process skills; NEVER for custom integrations)
4. **Verification** — Mandatory after code changes
5. **Quick Reference** — Skill routing table

**Placeholder substitution:**

| Placeholder | Source |
|-------------|--------|
| `{DATE}` | Current date |
| `{HA_VERSION}` | `homeassistant/const.py` / manifest |
| `{TARGET}` | Detection result |
| `{OPTIONAL_STACK}` | Detected optional features |

See `${CLAUDE_SKILL_DIR}/references/injectable-template.md` for full template with all placeholders and conditional sections.

## Validation

After running `/ha:init`:

1. Check CLAUDE.md contains markers
2. Verify detected target matches the actual project
3. New session should:
   - Auto-detect complexity when given tasks
   - Stop on Iron Law violations
   - Offer relevant workflows based on task

## Error Handling

| Scenario | Action |
|----------|--------|
| CLAUDE.md read-only | Error: "Cannot modify CLAUDE.md - check permissions" |
| Markers corrupted | Warn, offer to remove and reinstall |
| Unknown HA version | Use conservative defaults (all features enabled) |
| No target detected | Error: "Not a Home Assistant project — expected a core checkout, custom_components/, or the frontend repo" |

## Relationship to Other Commands

| Command | When to Use |
|---------|-------------|
| `/ha:init` | First time, or after plugin updates |
| `/ha:audit` | Periodic project health check |
| `/ha:verify` | After code changes |
