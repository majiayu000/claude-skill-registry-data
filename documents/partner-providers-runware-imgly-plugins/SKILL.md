---
name: partner-providers-runware
description: |
  Discover new Runware AI models from documentation and implement providers.
  Use when: checking for new Runware models, implementing Runware providers,
  updating providers.md status, or working with Runware API integrations.
---

# Runware Provider Management

Manage the lifecycle of Runware AI providers: discover new models from documentation and implement them as IMG.LY providers.

## Key Files

- **Provider Tracking**: `specs/providers/runware/providers.md`
- **Provider Specifications**: `specs/providers/` (schemas, architecture)
- **Provider Implementations**:
  - Image: `packages/plugin-ai-image-generation-web/src/runware/`
  - Video: `packages/plugin-ai-video-generation-web/src/runware/`
- **API Patterns**: `specs/providers/runware/api-patterns.md`
- **README Documentation**:
  - Image: `packages/plugin-ai-image-generation-web/README.md`
  - Video: `packages/plugin-ai-video-generation-web/README.md`

## Workflow Overview

This skill operates in two phases:

1. **Discovery** (automatic): Check Runware docs for new/updated models
2. **Implementation** (user-approved): Create provider files for selected models

## Phase 1: Discovery

Follow the checklist in `DISCOVERY_CHECKLIST.md` to:

1. Read current `specs/providers/runware/providers.md` to understand what's tracked
2. Fetch Runware provider documentation pages listed in the Provider Documentation Links table
3. Compare discovered models against the providers.md table
4. Report findings to user:
   - New models not in providers.md
   - Models with updated capabilities
   - Status recommendations (implement vs skip)

### Discovery Output Format

Present findings as:

```
## Discovery Results

### New Models Found
| Provider | Model | AIR | Capabilities | Recommendation |
|----------|-------|-----|--------------|----------------|
| ... | ... | ... | ... | implement/skip |

### Updated Models
| Provider | Model | Change |
|----------|-------|--------|
| ... | ... | ... |

### Summary
- X new models found
- Y models updated
- Z recommended for implementation
```

After presenting results, ask: "Which models would you like me to implement?"

## Phase 2: Implementation

Only proceed after user approval. Follow `IMPLEMENTATION_CHECKLIST.md` to:

1. Determine provider type (t2i, i2i, t2v, i2v) from capabilities
2. Find existing Runware provider of same type as reference
3. **MANDATORY: Fetch and verify API documentation** (see API Verification below)
4. **For I2I/I2V**: Extract dimension constraints (min/max/multiple) from API docs
5. Create provider implementation following patterns in `specs/providers/schemas/`
   - **For I2I**: Use model-specific `RUNWARE_DIMENSION_CONSTRAINTS` (see `implementation-notes.md`)
6. Export provider from `runware/index.ts`
7. Add translations to `translations.json` - REQUIRED
8. **Add to example app** (`examples/ai/src/runwareProviders.ts`) - REQUIRED
9. Update `specs/providers/runware/providers.md` status to "implemented"
10. **Update README documentation** - Add to plugin's README.md (Providers, API Reference, Panel IDs, Asset History)
11. Run build checks: `pnpm --filter "@imgly/plugin-ai-*" check:all`

### API Verification (MANDATORY)

**CRITICAL**: Before writing ANY provider code, you MUST fetch and verify the exact API parameters from TWO documentation sources:

1. **General API Reference** - For the inference type (image or video):
   - Image: `https://runware.ai/docs/en/image-inference/api-reference.md`
   - Video: `https://runware.ai/docs/en/video-inference/api-reference.md`

   Extract: Allowed top-level parameters, request/response format, delivery methods

2. **Provider-Specific Documentation** - For model-specific settings:
   - `https://runware.ai/docs/en/providers/{vendor}.md` (e.g., `google.md`, `bfl.md`)

   Extract: `providerSettings.{vendor}` options, model-specific parameters, constraints

**Verification Checklist**:
- [ ] Fetched general API reference for inference type
- [ ] Listed all allowed top-level parameters from API docs
- [ ] Fetched provider-specific documentation
- [ ] Identified any `providerSettings.{vendor}` options (e.g., `providerSettings.google.generateAudio`)
- [ ] Verified parameter names match EXACTLY (no assumptions!)
- [ ] Noted any async/polling requirements (video uses `deliveryMethod: "async"`)

**Why This Matters**: Provider-specific features (like audio generation) are often nested under `providerSettings.{vendor}` rather than being top-level parameters. Using wrong parameter names causes API errors.

### Implementation Reference

Based on model capabilities, follow the appropriate schema documentation:

| Capability | Schema Documentation |
|------------|---------------------|
| text-to-image | `specs/providers/schemas/text-to-image.md` |
| image-to-image | `specs/providers/schemas/image-to-image.md` |
| text-to-video | `specs/providers/schemas/text-to-video.md` |
| image-to-video | `specs/providers/schemas/image-to-video.md` |

## Status Values

When updating providers.md:

| Status | When to Use |
|--------|-------------|
| `implemented` | Provider code exists and works |
| `planned` | Will implement (high priority) |
| `skipped` | Intentionally not implementing (older version, limited use) |
| `undecided` | Needs discussion |

## Documentation Access

Runware documentation URLs can be accessed as LLM-friendly markdown by appending `.md` to the path:
- HTML: `https://runware.ai/docs/en/image-inference/api-reference`
- Markdown: `https://runware.ai/docs/en/image-inference/api-reference.md`

Always prefer the `.md` version when fetching documentation for better parsing.

## References

### Skill Files (this folder)
- `DISCOVERY_CHECKLIST.md` - Step-by-step discovery process
- `IMPLEMENTATION_CHECKLIST.md` - Step-by-step implementation process

### Provider Specifications
- `specs/providers/README.md` - Overview of provider system
- `specs/providers/architecture.md` - How providers fit into the plugin system
- `specs/providers/patterns/ui-guidelines.md` - **CRITICAL**: Which parameters to expose/hide in UI
- `specs/providers/patterns/text-to-image.md` - T2I implementation pattern
- `specs/providers/patterns/image-to-image.md` - I2I implementation pattern
- `specs/providers/patterns/text-to-video.md` - T2V implementation pattern
- `specs/providers/patterns/image-to-video.md` - I2V implementation pattern
- `specs/providers/patterns/quick-actions.md` - Quick action support

### Runware-Specific
- `specs/providers/runware/providers.md` - Model inventory and status
- `specs/providers/runware/api-patterns.md` - Runware API conventions
- `specs/providers/runware/implementation-notes.md` - Runware-specific details
