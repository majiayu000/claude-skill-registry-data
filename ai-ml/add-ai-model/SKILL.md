---
name: add-ai-model
description: Add a new AI image model to myimageupscaler.com, including model costs, provider configuration, model registry, quality tiers, scale capabilities, feature flags, tests, and free versus paid access rules.
---

# Add AI Model Skill

When adding a new AI model to the image upscaler, follow these steps in order. Each file must be updated for the model to work correctly.

## Overview

- **Provider**: Replicate (primary), Gemini (alternative)
- **Pricing**: USD cost per API call + credit multiplier
- **Tiers**: Models can be restricted to subscription tiers (free, hobby, pro, business)
- **Scale Support**: Models must accurately report which scales they actually support
- **Capabilities**: Models must correctly declare 'upscale' vs enhancement-only capabilities

## Important: Scale Support Accuracy

**DO NOT claim scales that the model doesn't natively support:**

- If the model has no scale parameter → `supportedScales: []` and remove 'upscale' capability
- If the model caps at 4x → `supportedScales: [2, 4]` (NOT [2, 4, 8])
- Only models with native 8x+ support should include 8 in `supportedScales`

**Common mistakes to avoid:**

- ❌ Setting `supportedScales: [2, 4, 8]` when the model only supports 2x and 4x
- ❌ Including 'upscale' capability for enhancement-only models
- ❌ Using "two-pass hacks" to simulate unsupported scales

## Edge Case: Free Tier Models (Direct Access Only)

Some models should be available to **free users** without creating a quality tier. Examples include `p-image-edit` and `flux-kontext-fast`.

**For free tier models:**

1. **DO NOT add a quality tier** - Skip steps 4 (QualityTier, QUALITY_TIER_CONFIG, QUALITY_TIER_SCALES) and 5 (validation schema)
2. **Set `tierRestriction: null`** in MODEL_CONFIG (not `'hobby'`, `'pro'`, etc.)
3. **Add to FREE_MODELS array** in addition to HOBBY_MODELS, PRO_MODELS, BUSINESS_MODELS

```typescript
// shared/config/model-costs.config.ts
FREE_MODELS: ['real-esrgan', 'gfpgan', 'nano-banana', 'p-image-edit', 'flux-kontext-fast'],

// In MODEL_CONFIG - note tierRestriction is null (not a string)
'flux-kontext-fast': {
  cost: MODEL_COSTS.FLUX_KONTEXT_FAST_COST,
  multiplier: 2, // Use lower multiplier for free tier (1-2x)
  qualityScore: 9.1,
  processingTime: MODEL_COSTS.PROCESSING_TIME_MEDIUM,
  maxInputResolution: MODEL_COSTS.MAX_INPUT_RESOLUTION,
  maxOutputResolution: MODEL_COSTS.MAX_OUTPUT_RESOLUTION,
  supportedScales: [], // Enhancement-only
  tierRestriction: null, // null = free tier, not 'hobby'/'pro'/'business'
},
```

4. **In model-registry.ts** - use `tierRestriction: undefined` (not a string):

```typescript
{
  id: 'flux-kontext-fast',
  displayName: 'Flux Kontext',
  // ...
  isEnabled: true, // Always enabled for free tier
  tierRestriction: undefined, // undefined = free tier
}
```

**Free tier vs Paid tier models:**

| Aspect            | Free Tier                     | Paid Tier (hobby/pro/business)       |
| ----------------- | ----------------------------- | ------------------------------------ |
| Quality Tier      | NO - direct model access only | YES - added to PREMIUM_QUALITY_TIERS |
| tierRestriction   | `null` or `undefined`         | `'hobby'`, `'pro'`, or `'business'`  |
| FREE_MODELS array | ✅ Included                   | ❌ Not included                      |
| isEnabled         | `true`                        | `serverEnv.ENABLE_PREMIUM_MODELS`    |
| Credit multiplier | 1-2x                          | 3-8x                                 |

## Required Files (in order)

### 1. Cost Configuration

**File**: `shared/config/model-costs.config.ts`

Add the USD cost per API call:

```typescript
export const MODEL_COSTS = {
  // ... existing costs
  NEW_MODEL_COST: 0.03, // USD per call
};
```

Add to tier arrays (HOBBY_MODELS, PRO_MODELS, BUSINESS_MODELS):

```typescript
HOBBY_MODELS: [
  // ... existing models
  'new-model-id',
],
```

Add MODEL_CONFIG entry:

```typescript
'new-model-id': {
  cost: MODEL_COSTS.NEW_MODEL_COST,
  multiplier: 3,           // Credit multiplier
  qualityScore: 9.2,       // 1-10 quality rating
  processingTime: MODEL_COSTS.PROCESSING_TIME_MEDIUM,
  maxInputResolution: MODEL_COSTS.MAX_INPUT_RESOLUTION,
  maxOutputResolution: MODEL_COSTS.MAX_OUTPUT_RESOLUTION,
  // IMPORTANT: Only include scales the model ACTUALLY supports
  // - If no scale param: [] (enhancement-only)
  // - If 2x/4x only: [2, 4]
  // - If native 8x: [2, 4, 8]
  supportedScales: [2, 4], // Adjust based on actual model support
  tierRestriction: 'hobby', // null for free, 'hobby'/'pro'/'business' for paid
},
```

If adding a new quality tier, add to PREMIUM_QUALITY_TIERS:

```typescript
PREMIUM_QUALITY_TIERS: ['auto', 'new-tier', 'hd-upscale', ...] as const,
```

---

### 2. Credit Multiplier

**File**: `shared/config/credits.config.ts`

Add the credit multiplier constant:

```typescript
export const CREDIT_COSTS = {
  // ... existing multipliers
  NEW_MODEL_MULTIPLIER: 3, // Credits = base_cost * multiplier
};
```

Add MODEL_CREDIT_COSTS entry:

```typescript
'new-model-id': {
  upscale: CREDIT_COSTS.BASE_UPSCALE_COST * CREDIT_COSTS.NEW_MODEL_MULTIPLIER,
  enhance: CREDIT_COSTS.BASE_ENHANCE_COST * CREDIT_COSTS.NEW_MODEL_MULTIPLIER,
  both: CREDIT_COSTS.BASE_BOTH_COST * CREDIT_COSTS.NEW_MODEL_MULTIPLIER,
  custom: CREDIT_COSTS.BASE_CUSTOM_COST * CREDIT_COSTS.NEW_MODEL_MULTIPLIER,
},
```

---

### 3. Model Registry Types

**File**: `server/services/model-registry.types.ts`

Add to ModelId type:

```typescript
export type ModelId =
  | 'real-esrgan'
  // ... existing models
  | 'new-model-id';
```

---

### 4. Shared Types (Duplicate ModelId)

**File**: `shared/types/coreflow.types.ts`

Add to ModelId type (there's a duplicate here):

```typescript
export type ModelId =
  | 'real-esrgan'
  // ... existing models
  | 'new-model-id';
```

If adding a new quality tier, update QualityTier type:

```typescript
export type QualityTier =
  | 'auto'
  | 'quick'
  | 'face-restore'
  | 'new-tier' // Add in credit order
  | 'hd-upscale';
// ...
```

And add QUALITY_TIER_CONFIG entry:

```typescript
'new-tier': {
  label: 'New Tier Label',
  credits: 3,
  modelId: 'new-model-id',
  description: 'Short description',
  bestFor: 'Use case description',
  smartAnalysisAlwaysOn: false,
},
```

**IMPORTANT:** Add QUALITY_TIER_SCALES entry (defines which scales the tier's model supports):

```typescript
export const QUALITY_TIER_SCALES: Record<QualityTier, (2 | 4 | 8)[]> = {
  // ... existing tiers
  'new-tier': [2, 4], // Must match model's actual supportedScales
  // ...
};
```

---

### 5. Validation Schema

**File**: `shared/validation/upscale.schema.ts`

If adding a new quality tier, update the Zod enum:

```typescript
qualityTier: z
  .enum(['auto', 'quick', 'face-restore', 'new-tier', 'hd-upscale', ...])
  .default('auto'),
```

---

### 6. Model Registry

**File**: `server/services/model-registry.ts`

Add to DEFAULT_MODEL_VERSIONS:

```typescript
const DEFAULT_MODEL_VERSIONS: Record<string, string> = {
  // ... existing versions
  'new-model-id': 'provider/model-name', // Replicate model identifier
};
```

Add to MODEL_COSTS map:

```typescript
const MODEL_COSTS: Record<string, number> = {
  // ... existing costs
  'new-model-id': CONFIG_MODEL_COSTS.NEW_MODEL_COST,
};
```

Add to MODEL_CREDIT_MULTIPLIERS map:

```typescript
const MODEL_CREDIT_MULTIPLIERS: Record<string, number> = {
  // ... existing multipliers
  'new-model-id': CREDIT_COSTS.NEW_MODEL_MULTIPLIER,
};
```

Add to getModelVersion overrides:

```typescript
private getModelVersion(modelId: string): string {
  const overrides: Record<string, string | undefined> = {
    // ... existing overrides
    'new-model-id': serverEnv.MODEL_VERSION_NEW_MODEL,
  };
  return overrides[modelId] || DEFAULT_MODEL_VERSIONS[modelId];
}
```

Add model config to loadModelsFromEnvironment():

```typescript
{
  id: 'new-model-id',
  displayName: 'Display Name',
  provider: 'replicate',
  modelVersion: this.getModelVersion('new-model-id'),
  // CRITICAL: Only include 'upscale' if the model actually changes dimensions
  // - Enhancement-only models: remove 'upscale', keep 'enhance', 'denoise', etc.
  capabilities: ['upscale', 'enhance', 'denoise'],
  costPerRun: MODEL_COSTS['new-model-id'],
  creditMultiplier: MODEL_CREDIT_MULTIPLIERS['new-model-id'],
  qualityScore: 9.2,
  processingTimeMs: TIMEOUTS.CLARITY_UPSCALER_PROCESSING_TIME,
  maxInputResolution: CONFIG_MODEL_COSTS.MAX_INPUT_RESOLUTION,
  maxOutputResolution: CONFIG_MODEL_COSTS.MAX_OUTPUT_RESOLUTION,
  // IMPORTANT: Match this to the model's actual scale support
  // - Enhancement-only: []
  // - 2x/4x max: [2, 4]
  // - Native 8x+: [2, 4, 8]
  supportedScales: [2, 4], // Adjust based on actual model support
  isEnabled: serverEnv.ENABLE_PREMIUM_MODELS,
  tierRestriction: 'hobby',
},
```

---

### 7. Replicate Service

**File**: `server/services/replicate.service.ts`

Add input interface (check Replicate docs for exact params):

```typescript
interface INewModelInput {
  prompt: string;
  image: string[];
  // ... model-specific params
}
```

Update buildModelInput return type:

```typescript
private buildModelInput(...):
  | IFluxKontextInput
  // ... existing types
  | INewModelInput {
```

Add case in buildModelInput switch:

```typescript
case 'new-model-id': {
  let effectivePrompt = customPrompt;
  if (!effectivePrompt) {
    effectivePrompt = enhance
      ? `Upscale and enhance this image to ${scale}x resolution.`
      : `Upscale this image to ${scale}x resolution.`;
    // Add enhancement instructions...
  }
  return {
    prompt: effectivePrompt,
    image: [imageDataUrl],
    // ... model-specific params
  };
}
```

---

### 8. Environment Variables

**File**: `shared/config/env.ts`

Add to serverEnvSchema:

```typescript
MODEL_VERSION_NEW_MODEL: z.string().optional(),
```

Add to loadServerEnv():

```typescript
MODEL_VERSION_NEW_MODEL: process.env.MODEL_VERSION_NEW_MODEL,
```

---

## Verification Checklist

After making all changes, run:

```bash
yarn verify
```

Then test:

1. Select the new quality tier in UI
2. Process an image
3. Verify credits are deducted correctly
4. Check Replicate dashboard for API call

## Credit Economics Reference

| Cost Range   | Suggested Multiplier | Example                  |
| ------------ | -------------------- | ------------------------ |
| $0.001-0.005 | 1x                   | real-esrgan              |
| $0.005-0.01  | 2x                   | gfpgan                   |
| $0.01-0.05   | 3-4x                 | qwen-image-edit, clarity |
| $0.05-0.10   | 5-6x                 | flux-2-pro               |
| $0.10+       | 7-8x                 | nano-banana-pro          |
