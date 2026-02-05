---
name: shared-libraries-guidelines
description: Shared libraries guidelines for Quantum Skincare's TypeScript shared code (types, validation, utils). Covers type definitions, Zod validation schemas, utility functions, contract maintenance, DB vs App type separation, enum patterns, reusable refinements, and cross-project consistency. Use when working with @quantum/shared-types, @quantum/shared-validation, @quantum/shared-utils, or maintaining shared contracts.
---

# Shared Libraries Guidelines - Quantum Skincare

## Purpose

Quick reference for Quantum Skincare's shared TypeScript libraries that provide types, validation schemas, and utilities across all applications (frontend, backend, data-access).

## When to Use This Skill

- Creating or modifying shared types
- Creating or modifying Zod validation schemas
- Working with shared utility functions
- Maintaining API contracts across apps
- Defining DB vs App type separations
- Creating reusable enum patterns
- Adding cross-project constants
- Updating validation schemas
- Ensuring type/validation consistency

---

## Quick Start

### New Type Checklist

- [ ] Add to appropriate file in `libs/shared/types/src/lib/`
- [ ] Export from `libs/shared/types/src/index.ts`
- [ ] Document with JSDoc comments
- [ ] Separate DB types (suffixed with `DB`) from App types
- [ ] Use consistent naming conventions
- [ ] Build library: `pnpm nx build shared-types`
- [ ] Update consuming apps if breaking change

### New Validation Schema Checklist

- [ ] Add to `libs/shared/validation/src/lib/validation.ts`
- [ ] Export from `libs/shared/validation/src/index.ts`
- [ ] Use consistent Zod patterns
- [ ] Add custom error messages
- [ ] Reuse existing enum schemas
- [ ] Add refinements if needed
- [ ] Write unit tests
- [ ] Document with JSDoc
- [ ] Build library: `pnpm nx build shared-validation`

---

## Library Structure

```
libs/shared/
├── types/                   # @quantum/shared-types
│   └── src/
│       ├── lib/
│       │   ├── user.types.ts       # User models (DB, App, Auth)
│       │   ├── scan.types.ts       # Scan models
│       │   ├── tier.types.ts       # Tier models
│       │   ├── skin-analysis.types.ts  # Analysis results
│       │   ├── treatment.types.ts  # Treatment cycles
│       │   ├── streak.types.ts     # Daily streaks
│       │   └── quota.types.ts      # Quota tracking
│       └── index.ts                # Public API exports
│
├── validation/              # @quantum/shared-validation
│   └── src/
│       ├── lib/
│       │   ├── validation.ts       # Zod schemas
│       │   └── streak.ts           # Streak validation logic
│       └── index.ts                # Public API exports
│
└── utils/                   # @quantum/shared-utils
    └── src/
        ├── lib/
        │   ├── constants.ts        # Shared constants
        │   ├── date-utils.ts       # Date handling utilities
        │   └── utils.ts            # General utilities
        └── index.ts                # Public API exports
```

---

## Core Principles

### 1. Single Source of Truth

All shared types, validation, and utilities live in `libs/shared/*`:

```typescript
// ✅ GOOD: Import from shared library
import { UserApp, ConsentProfile } from '@quantum/shared-types';
import { personalInfoSchema } from '@quantum/shared-validation';

// ❌ BAD: Duplicate type definition
interface UserApp {
  id: string;
  email: string;
  // ...
}
```

### 2. DB vs App Type Separation

Always separate database types from application types:

```typescript
/**
 * Represents the full user object from the 'users' table
 */
export interface UserDB {
  id: string;
  email: string;
  full_name: string;
  clerk_user_id: string;
  tier_id: string;  // Foreign key
  email_verified: boolean;
  consent_id: string | null;
  created_at: Date;
  updated_at: Date;
  deleted_at: Date | null;
}

/**
 * Safe, application-level representation
 * Omits sensitive fields and includes joined data
 */
export type UserApp = Omit<UserDB, 'tier_id'> & {
  tier: 'Standard' | 'Premium' | 'Admin';  // Joined tier name
  analysis_quota: number;
  consent?: UserConsentDB | null;
};
```

**Pattern:**
- **DB types** (`*DB`): Match database schema exactly (snake_case fields, UUIDs, timestamps)
- **App types**: Camel case, joined relations, omit sensitive data

### 3. Type-First, Schema-Second

Define TypeScript types first, then create matching Zod schemas:

```typescript
// 1. Define type in shared-types
export interface PersonalInfoUpdate {
  age: number;
  sex: SurveySex;
  skinType: string;
  ethnicity: string;
  country: string;
}

// 2. Create matching Zod schema in shared-validation
export const personalInfoSchema = z.object({
  age: z.number().int().min(13).max(120),
  sex: surveySexSchema,
  skinType: z.string(),
  ethnicity: z.string(),
  country: countryCodeSchema,
});

// Type should match schema inference
type PersonalInfoUpdate = z.infer<typeof personalInfoSchema>;
```

### 4. Reusable Enum Schemas

Define enums once, reuse everywhere:

```typescript
// validation.ts
const SURVEY_SEX_VALUES = ['male', 'female', 'non_binary', 'prefer_not_to_say'] as const;
export const surveySexSchema = z.enum(SURVEY_SEX_VALUES, {
  message: 'Please select a valid option',
});
export type SurveySex = z.infer<typeof surveySexSchema>;

// Reuse in multiple schemas
export const surveySchema = z.object({
  sex: surveySexSchema,  // ✅ Reused
  // ...
});

export const personalInfoSchema = z.object({
  sex: surveySexSchema,  // ✅ Reused
  // ...
});
```

### 5. Custom Error Messages

Always provide clear, user-friendly error messages:

```typescript
export const emailSchema = z
  .string({
    required_error: 'Email is required',
    invalid_type_error: 'Email must be a string',
  })
  .email('Please enter a valid email address')
  .min(3, 'Email must be at least 3 characters')
  .max(255, 'Email must be less than 255 characters');

export const ageSchema = z
  .number({
    required_error: 'Age is required',
    invalid_type_error: 'Age must be a number',
  })
  .int('Age must be a whole number')
  .min(13, 'You must be at least 13 years old')
  .max(120, 'Please enter a valid age');
```

---

## Type Patterns

### User Types

```typescript
// Core user types with documentation
export interface UserDB {
  id: string;
  email: string;
  full_name: string;
  clerk_user_id: string;
  tier_id: string;
  email_verified: boolean;
  consent_id: string | null;
  created_at: Date;
  updated_at: Date;
  deleted_at: Date | null;
}

export type UserApp = Omit<UserDB, 'tier_id'> & {
  tier: 'Standard' | 'Premium' | 'Admin';
  analysis_quota: number;
  consent?: UserConsentDB | null;
};

export type AuthUser = UserApp;  // Semantic alias
```

### Enum Types

```typescript
export type ConsentProfile = 'GDPR' | 'BIPA' | 'CCPA' | 'ROW';
export type TierName = 'Standard' | 'Premium' | 'Admin';
export type TreatmentGroup = 'GROUP_A' | 'GROUP_B' | 'GROUP_C' | 'UNGROUPED';
```

### API Response Types

```typescript
export interface QuotaStatus {
  currentPeriod: {
    used: number;
    limit: number;
    remaining: number;
  };
  lifetime: {
    total: number;
  };
  tier: TierName;
}

export interface AnalysisResult {
  success: boolean;
  data?: SkinAnalysisData;
  error?: string;
}
```

---

## Validation Patterns

### Basic Schemas

```typescript
export const emailSchema = z
  .string()
  .email('Please enter a valid email address')
  .min(3)
  .max(255);

export const passwordSchema = z
  .string()
  .min(8, 'Password must be at least 8 characters')
  .max(100, 'Password must be less than 100 characters');
```

### Object Schemas

```typescript
export const personalInfoSchema = z.object({
  age: z.number().int().min(13).max(120),
  sex: surveySexSchema,
  skinType: z.string(),
  ethnicity: z.string(),
  country: countryCodeSchema,
  skinConcerns: z.array(skinConcernSchema).optional(),
});

export type PersonalInfoData = z.infer<typeof personalInfoSchema>;
```

### Refinements (Complex Validation)

```typescript
export const changePasswordSchema = z
  .object({
    currentPassword: z.string().min(1, 'Current password is required'),
    newPassword: passwordSchema,
    confirmPassword: z.string().min(1, 'Please confirm your password'),
  })
  .refine((data) => data.newPassword === data.confirmPassword, {
    message: 'Passwords do not match',
    path: ['confirmPassword'],
  });
```

### Transformations

```typescript
export const countryCodeSchema = z
  .string()
  .length(2, 'Country code must be 2 characters')
  .transform((c) => c.toUpperCase());  // Auto-uppercase

export const emailNormalizedSchema = z
  .string()
  .email()
  .transform((e) => e.toLowerCase().trim());
```

### Optional Fields

```typescript
export const updateUserSchema = z.object({
  fullName: z.string().min(1).optional(),
  age: z.number().int().min(13).max(120).optional(),
  skinConcerns: z.array(skinConcernSchema).optional(),
});
```

---

## Utility Patterns

### Date Utilities

```typescript
// libs/shared/utils/src/lib/date-utils.ts

/**
 * Get today's date in YYYY-MM-DD format
 */
export function getTodayYmd(): string {
  return new Date().toISOString().split('T')[0];
}

/**
 * Parse YYYY-MM-DD string to Date object
 */
export function parseYmd(ymd: string | undefined): Date | null {
  if (!ymd) return null;
  const [y, m, d] = ymd.split('-').map((s) => Number(s));
  if (!y || !m || !d) return null;
  const date = new Date(Date.UTC(y, m - 1, d));
  return isNaN(date.getTime()) ? null : date;
}

/**
 * Convert Date object to YYYY-MM-DD string
 */
export function toYmd(date: Date): string {
  const y = date.getUTCFullYear();
  const m = String(date.getUTCMonth() + 1).padStart(2, '0');
  const d = String(date.getUTCDate()).padStart(2, '0');
  return `${y}-${m}-${d}`;
}
```

### Constants

```typescript
// libs/shared/utils/src/lib/constants.ts

export const API_VERSION = 'v1';
export const MAX_FILE_SIZE = 10 * 1024 * 1024; // 10MB
export const SUPPORTED_IMAGE_TYPES = ['image/jpeg', 'image/png'];
```

---

## Common Workflows

### Adding a New Type

1. **Create type in appropriate file:**
   ```typescript
   // libs/shared/types/src/lib/feature.types.ts
   export interface FeatureDB {
     id: string;
     user_id: string;
     data: string;
     created_at: Date;
   }

   export interface FeatureApp {
     id: string;
     userId: string;
     data: string;
     createdAt: Date;
   }
   ```

2. **Export from index:**
   ```typescript
   // libs/shared/types/src/index.ts
   export * from './lib/feature.types.js';
   ```

3. **Build library:**
   ```bash
   pnpm nx build shared-types
   ```

### Adding a New Validation Schema

1. **Define schema:**
   ```typescript
   // libs/shared/validation/src/lib/validation.ts
   export const featureSchema = z.object({
     data: z.string().min(1).max(1000),
   });

   export type FeatureData = z.infer<typeof featureSchema>;
   ```

2. **Export from index:**
   ```typescript
   // libs/shared/validation/src/index.ts
   export { featureSchema } from './lib/validation.js';
   export type { FeatureData } from './lib/validation.js';
   ```

3. **Write tests:**
   ```typescript
   // libs/shared/validation/src/lib/validation.spec.ts
   describe('featureSchema', () => {
     it('should validate valid data', () => {
       const result = featureSchema.safeParse({ data: 'test' });
       expect(result.success).toBe(true);
     });
   });
   ```

4. **Build library:**
   ```bash
   pnpm nx build shared-validation
   ```

### Using Shared Libraries

```typescript
// Backend controller
import { UserApp, QuotaStatus } from '@quantum/shared-types';
import { personalInfoSchema } from '@quantum/shared-validation';

export async function updatePersonalInfo(req: Request, res: Response) {
  const result = personalInfoSchema.safeParse(req.body);
  if (!result.success) {
    return res.status(400).json({ errors: formatZodErrors(result.error) });
  }
  // ...
}

// Frontend component
import type { UserApp } from '@quantum/shared-types';
import { personalInfoSchema } from '@quantum/shared-validation';

export function ProfileForm() {
  const handleSubmit = async (data: unknown) => {
    const result = personalInfoSchema.safeParse(data);
    if (!result.success) {
      setErrors(result.error.flatten().fieldErrors);
      return;
    }
    await submitProfile(result.data);
  };
}
```

---

## Anti-Patterns

### ❌ Don't Duplicate Types

```typescript
// BAD: Duplicating type in backend
interface UserApp {
  id: string;
  email: string;
  // ...
}

// GOOD: Import from shared
import { UserApp } from '@quantum/shared-types';
```

### ❌ Don't Skip Type/Schema Sync

```typescript
// BAD: Type and schema out of sync
export interface PersonalInfo {
  age: number;
  country: string;  // Type has country
}

export const personalInfoSchema = z.object({
  age: z.number(),
  // Missing country in schema!
});

// GOOD: Keep in sync
export interface PersonalInfo {
  age: number;
  country: string;
}

export const personalInfoSchema = z.object({
  age: z.number(),
  country: countryCodeSchema,
});
```

### ❌ Don't Use DB Types in API Responses

```typescript
// BAD: Exposing DB type
export function getUser(): UserDB {
  // Exposes internal IDs, timestamps
}

// GOOD: Use App type
export function getUser(): UserApp {
  // Safe for API responses
}
```

---

## Testing

### Type Tests

```typescript
// libs/shared/types/src/lib/__tests__/scan.types.spec.ts
import type { ScanDB, ScanApp } from '../scan.types';

describe('Scan types', () => {
  it('should have ScanDB with DB fields', () => {
    const scan: ScanDB = {
      id: '123',
      user_id: '456',
      created_at: new Date(),
      // ...
    };
    expect(scan).toBeDefined();
  });
});
```

### Validation Tests

```typescript
// libs/shared/validation/src/lib/validation.spec.ts
import { personalInfoSchema } from './validation';

describe('personalInfoSchema', () => {
  it('should validate valid data', () => {
    const result = personalInfoSchema.safeParse({
      age: 25,
      sex: 'male',
      skinType: 'normal',
      ethnicity: 'asian',
      country: 'US',
    });
    expect(result.success).toBe(true);
  });

  it('should reject invalid age', () => {
    const result = personalInfoSchema.safeParse({
      age: 12, // Too young
      sex: 'male',
      skinType: 'normal',
      ethnicity: 'asian',
      country: 'US',
    });
    expect(result.success).toBe(false);
  });
});
```

---

## Building & Publishing

### Build Single Library

```bash
pnpm nx build shared-types
pnpm nx build shared-validation
pnpm nx build shared-utils
```

### Build All Shared Libraries

```bash
pnpm nx run-many -t build -p shared-types shared-validation shared-utils
```

### Watch Mode (Development)

```bash
pnpm nx watch shared-types -- pnpm nx build shared-types
```

---

## Reference

- **Types**: [libs/shared/types/src/lib/](../../libs/shared/types/src/lib/)
- **Validation**: [libs/shared/validation/src/lib/validation.ts](../../libs/shared/validation/src/lib/validation.ts)
- **Utils**: [libs/shared/utils/src/lib/](../../libs/shared/utils/src/lib/)
- **CLAUDE.md**: Shared Contracts section
- **Zod Docs**: https://zod.dev

---

## Related Skills

- **backend-dev-guidelines** - Backend usage of shared types
- **frontend-dev-guidelines** - Frontend usage of shared types
- **data-access-guidelines** - DB type mappings

---

**Skill Status**: Created for Quantum Skincare ✅
**Stack**: TypeScript, Zod, Nx Monorepo
**Libraries**: @quantum/shared-types, @quantum/shared-validation, @quantum/shared-utils
**Line Count**: Under 500 lines (following Anthropic best practices) ✅
