---
name: add-use-case-tier
description: Add a new quality tier or use-case tier that reuses an existing image model, covering QualityTier types, tier config, scale config, validation schema, model cost categorization, UI exposure, and tests.
---

# Add Quality Tier (Use Case) Skill

When adding a new quality tier that reuses an existing model (e.g., a "Budget Old Photo" tier using `p-image-edit`), follow these steps. This is simpler than adding a new model — no provider integration needed.

## Required Files (all must be updated)

### 1. QualityTier type + config + scales

**File**: `shared/types/coreflow.types.ts`

Add to QualityTier union:

```typescript
export type QualityTier =
  | 'auto'
  | 'quick'
  // ...
  | 'new-tier-name'; // kebab-case
```

Add to QUALITY_TIER_CONFIG:

```typescript
'new-tier-name': {
  label: 'Tier Label',
  credits: 2,                    // Match existing model's credit cost
  modelId: 'existing-model-id',  // Reuse existing model
  description: 'Short description',
  bestFor: 'Target use case',
  smartAnalysisAlwaysOn: false,
  useCases: ['tag1', 'tag2'],    // Searchable tags for gallery filter
  previewImages: null,           // null until before/after images exist
},
```

Add to QUALITY_TIER_SCALES:

```typescript
'new-tier-name': [],  // Match the model's supportedScales
                      // [] for enhancement-only, [2, 4] for upscale models
```

### 2. Zod validation schema

**File**: `shared/validation/upscale.schema.ts`

Add to the qualityTier z.enum array:

```typescript
qualityTier: z
  .enum([
    'auto',
    'quick',
    // ...
    'new-tier-name',  // Add here
  ])
  .default('auto'),
```

**This is the one people forget.** Without it, the API returns 400 `invalid_enum_value`.

### 3. Tier categorization (FREE vs PREMIUM)

**File**: `shared/config/model-costs.config.ts`

Add to either `PREMIUM_QUALITY_TIERS` or `FREE_QUALITY_TIERS`:

```typescript
// If model has tierRestriction (hobby/pro/business):
PREMIUM_QUALITY_TIERS: [
  // ...existing
  'new-tier-name',
] as const,

// If model is free tier (no tierRestriction):
FREE_QUALITY_TIERS: ['quick', 'face-restore', 'bg-removal', 'new-tier-name'] as const,
```

**Without this, the tier won't appear in the Select Model modal** (it gets filtered out).

### 4. (Optional) Use case assignment in model registry

**File**: `server/services/model-registry.ts`

If this tier represents a new use case for auto-selection:

Update `loadUseCaseAssignments()`:

```typescript
this.useCaseAssignments = {
  // ...existing
  newUseCase: serverEnv.MODEL_FOR_NEW_USE_CASE,
};
```

Update `getModelForUseCase()` type:

```typescript
getModelForUseCase(
  useCase: 'generalUpscale' | 'portraits' | ... | 'newUseCase'
): IModelConfig | null {
```

### 5. (Optional) Env var for use case override

**File**: `shared/config/env.ts`

Add to Zod schema and fallback:

```typescript
// Schema (~line 242)
MODEL_FOR_NEW_USE_CASE: z.string().default('existing-model-id'),

// Fallback (~line 362)
MODEL_FOR_NEW_USE_CASE: process.env.MODEL_FOR_NEW_USE_CASE || 'existing-model-id',
```

**File**: `.env.api.example`

```
MODEL_FOR_NEW_USE_CASE=existing-model-id
```

### 6. Tests

**File**: `tests/unit/shared/quality-tier-config.unit.spec.ts`

Add `'new-tier-name'` to all hardcoded tier arrays:

- `expectedTiers` list (appears twice — config and scales tests)
- `enhancementOnlyTiers` list (if enhancement-only model)

## Checklist

- [ ] `shared/types/coreflow.types.ts` — QualityTier, QUALITY_TIER_CONFIG, QUALITY_TIER_SCALES
- [ ] `shared/validation/upscale.schema.ts` — Zod enum (causes 400 if missing)
- [ ] `shared/config/model-costs.config.ts` — FREE or PREMIUM tier list (invisible in modal if missing)
- [ ] `server/services/model-registry.ts` — use case assignment (optional)
- [ ] `shared/config/env.ts` — env var for use case (optional)
- [ ] `.env.api.example` — document env var (optional)
- [ ] `tests/unit/shared/quality-tier-config.unit.spec.ts` — update hardcoded tier arrays
- [ ] Run `yarn verify`

## Common Mistakes

| Symptom                              | Cause                                   | Fix                                      |
| ------------------------------------ | --------------------------------------- | ---------------------------------------- |
| API returns 400 `invalid_enum_value` | Missing from Zod enum                   | Add to `upscale.schema.ts`               |
| Tier not in Select Model modal       | Missing from FREE/PREMIUM_QUALITY_TIERS | Add to `model-costs.config.ts`           |
| Tests fail with count mismatch       | Hardcoded tier count in tests           | Remove magic numbers, use dynamic counts |
