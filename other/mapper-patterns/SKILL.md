---
name: mapper-patterns
description: Data mapping and transformation patterns between API and core types. Use when implementing mapper functions or converting between type systems.
---

# Mapper Implementation Patterns

## Core Mapper Principles

1. **API spec drives mapper logic** - NOT the other way around
2. **ZERO MISSING FIELDS** - Interface field count MUST EQUAL mapped field count
3. **PREFER map() utility** over constructors
4. **ALWAYS validate required fields** from API spec
5. **Use const output pattern** in all mappers
6. **Convert snake_case to camelCase** consistently
7. **Apply core types** (UUID, Email, URL, DateTime) via map()
8. **Use `optional()` for optional fields** - Normalize null to undefined, preserve "", 0, false
9. **NEVER weaken API spec** to make mapper easier
10. **Use InvalidState for validation errors** - throw immediately on missing required fields
11. **Declare helpers before exports** - nested mappers declared BEFORE main mapper but NOT exported
12. **map() handles null/undefined** - No ternary checks needed with map(), it returns undefined automatically
13. **No fallbacks between different fields** - If API has 2 fields, output has 2 fields. No merging, no defaults
14. **Use any for raw parameters** - All raw parameters should be `any` for simplicity
15. **Extract complex inline mappings** - Nested objects with 3+ properties should be helper functions
16. **Helper functions MUST validate** - All helper functions need `ensureProperties()` for required fields
17. **Enum arrays use map pattern** - `raw.field?.map((d: any) => toEnum(EnumType, d))`

See @.claude/skills/type-mapping/SKILL.md for complete type conversion reference.

## Mapper Function Naming Convention

**MANDATORY**: All mapper functions MUST use the `to<Model>` naming pattern.

### Pattern: to<Model>

```typescript
// ✅ CORRECT - to<Model> pattern with any
export function toUser(raw: any): User { }
export function toGroup(raw: any): Group { }
export function toEntry(raw: any): Entry { }

// Helper functions (non-exported) also use to<Model>
function toUserIdentity(raw: any): UserIdentity { }
function toAddress(raw: any): Address { }

// ❌ WRONG - Using 'map' prefix
export function mapUser(raw: any): User { }      // NO!
export function mapGroup(raw: any): Group { }    // NO!
```

### Rationale

1. **Concise and clear** - "to" clearly indicates conversion/transformation
2. **Consistent with helpers** - Internal helpers already use `to` prefix
3. **Industry standard** - Common pattern in TypeScript/JavaScript
4. **Matches other utilities** - toEnum(), toString(), toDate() convention

### Naming Rules

- **Exported mappers**: `export function to<Model>(raw: any): <Model>`
- **Helper mappers**: `function to<NestedModel>(raw: any): <NestedModel>` (not exported)
- **Model name**: Exact TypeScript interface name (User, Group, Entry, UserIdentity, etc.)
- **NO map prefix**: `toUser` not `mapUser`
- **NO get prefix**: `toUser` not `getUser`

### Examples

```typescript
// Main resource mappers
export function toUser(raw: any): User { }
export function toGroup(raw: any): Group { }
export function toRole(raw: any): Role { }
export function toSite(raw: any): Site { }
export function toEntry(raw: any): Entry { }
export function toZone(raw: any): Zone { }

// Nested object helpers (not exported)
function toUserIdentity(raw: any): UserIdentity { }
function toAddress(raw: any): Address { }
function toContactInfo(raw: any): ContactInfo { }
function toOrganizationRef(raw: any): OrganizationRef { }

// Extended models
export function toUserInfo(raw: any): UserInfo { }
export function toGroupInfo(raw: any): GroupInfo { }
```

## Standard Mapper Function Structure

### Canonical Format

All mapper functions MUST follow this exact structure:

```typescript
export function to<Resource>(raw: any): <Resource> {
  // 1. Check for required fields
  ensureProperties(raw, ['id', 'required_field']);
  // Or manual validation:
  // if (!raw.id) {
  //   throw new InvalidStateError('Missing required field: id');
  // }

  // 2. Create output object
  const output: <Resource> = {
    // Property mappings here
  };

  return output;
}
```

### Complete Example with All Patterns

```typescript
// src/Mappers.ts
import { map } from '@zerobias-org/util-hub-module-utils';
import { UUID, Email, URL, DateTime, InvalidStateError } from '@zerobias-org/types-core-js';
import { User, Address, UserStatus, UserRole } from '../generated/model';
import { mapWith, ensureProperties, optional } from './util';  // Import helpers

// Helper function - NOT exported, declared BEFORE main mapper
function toAddress(raw: any): Address {
  // 1. Check for required fields
  ensureProperties(raw, ['street']);

  // 2. Create output object
  const output: Address = {
    street: raw.street,
    city: optional(raw.city),
    zipCode: optional(raw.zip_code)
  };

  return output;
}

// Main mapper - exported, uses helper
export function toUser(raw: any): User {
  // 1. Check for required fields
  ensureProperties(raw, ['id', 'email', 'first_name', 'status']);

  // 2. Create output object
  const output: User = {
    id: raw.id.toString(),                              // ID conversion
    email: raw.email,                                   // Direct mapping (required)
    firstName: raw.first_name,                          // snake_case → camelCase (required)
    lastName: optional(raw.last_name),                  // Optional - normalizes null to undefined, keeps ""
    createdAt: map(DateTime, raw.created_at),          // map() handles required/optional automatically
    updatedAt: map(DateTime, raw.updated_at),          // map() returns undefined if null/undefined
    dateOfBirth: map(Date, raw.date_of_birth),         // No ternary needed - map() handles it
    status: toEnum(UserStatus, raw.status),            // Enum conversion
    phoneNumber: optional(raw.phone_number),           // Optional - null→undefined, keeps "", 0, false
    address: mapWith(toAddress, raw.address),          // Nested object with mapWith
    roles: raw.roles?.map((r: any) => toEnum(UserRole, r))  // Array mapping
  };

  return output;
}
```

## Property Mapping Patterns

### 1. Direct Mapping (Same Type)

**For required fields** - direct mapping:

```typescript
{
  email: raw.email,        // Required - direct mapping
  firstName: raw.first_name // Required - snake_case → camelCase
}
```

**For optional fields** - use `optional()`:

```typescript
{
  description: optional(raw.description), // Optional - null→undefined, keeps ""
  count: optional(raw.count),        // Optional - null→undefined, keeps 0
  active: optional(raw.active)       // Optional - null→undefined, keeps false
}
```

**Rule:** Direct mapping for required fields. Use `optional()` for optional fields to normalize null.

### 2. ID Conversion

Always convert numeric IDs to strings:

```typescript
{
  id: raw.id.toString()  // or raw.id if already string
}
```

### 3. Constructor-Based Conversion with map()

Use `map()` helper for types with constructors (Date, UUID, Email, URL, etc.):

```typescript
import { map } from '@zerobias-org/util-hub-module-utils';
import { UUID, Email, URL, DateTime } from '@zerobias-org/types-core-js';

{
  createdAt: map(DateTime, raw.created_at),    // Required or optional - map() handles both
  updatedAt: map(DateTime, raw.updated_at),    // map() returns undefined if raw.updated_at is null/undefined
  userId: map(UUID, raw.user_id),
  email: map(Email, raw.email)
}
```

**Rule:** `map()` handles undefined/null automatically and returns undefined. No need for ternary checks.

**❌ WRONG - Don't use ternary with map():**
```typescript
{
  dateOfBirth: raw.dateOfBirth ? map(Date, raw.dateOfBirth) : undefined  // ❌ Redundant
}
```

**✅ CORRECT - map() handles it:**
```typescript
{
  dateOfBirth: map(Date, raw.dateOfBirth)  // ✅ map() returns undefined if raw.dateOfBirth is null/undefined
}
```

**Why map() is preferred:**
- Handles optional/undefined values automatically - returns undefined if input is null/undefined
- Provides consistent error handling
- Validates input during conversion
- Cleaner, more concise code - no ternary needed

### 4. Enum Conversion with toEnum()

Use `toEnum()` helper for enum properties:

```typescript
{
  status: toEnum(StatusEnum, raw.status)
}
```

**Default behavior:** Values are converted to `snake_case` before enum lookup.

**Custom transformation:** Pass a second parameter transformation function:

```typescript
{
  type: toEnum(TypeEnum, raw.type, (v) => v.toUpperCase()),
  format: toEnum(FormatEnum, raw.format, (v) => v.toLowerCase())
}
```

### 5. Optional/Nullable Properties

**Use `optional()` helper to normalize null while preserving all other values:**

```typescript
{
  description: optional(raw.description),  // null→undefined, preserves "", 0, false
  phoneNumber: optional(raw.phone_number), // Normalizes only null
  name: optional(raw.name),                // Keeps empty strings
  count: optional(raw.count),              // Keeps 0 as 0
  active: optional(raw.active)             // Keeps false as false
}
```

**Why `optional()`?**
- Normalizes `null` → `undefined` (consistent "no value" representation) ✅
- Preserves empty strings `""` (legitimate value) ✅
- Preserves zeros `0` (legitimate value) ✅
- Preserves `false` (legitimate boolean value) ✅
- One "no value" state (`undefined`) instead of two (`null` and `undefined`)
- Cleaner, more semantic than `?? undefined` ✅

**❌ WRONG - Logical OR destroys legitimate values:**
```typescript
{
  name: raw.name || undefined,  // ❌ Converts "", 0, false to undefined (data loss!)
  count: raw.count || 0,        // ❌ Converts null/undefined to 0 (default injection!)
  active: raw.active || false,  // ❌ Converts null/undefined to false (default injection!)
  description: raw.description ? raw.description : undefined  // ❌ Converts "", 0, false to undefined
}
```

**✅ CORRECT - optional() preserves legitimate falsy values:**
```typescript
{
  name: optional(raw.name),        // ✅ null→undefined, keeps ""
  count: optional(raw.count),      // ✅ null→undefined, keeps 0
  active: optional(raw.active),    // ✅ null→undefined, keeps false
  description: optional(raw.description)  // ✅ null→undefined, keeps ""
}
```

**IMPORTANT - No Fallbacks or Defaults Between Different Fields:**

**❌ WRONG - Don't merge different API fields:**
```typescript
{
  phoneNumber: raw.mobilePhone || raw.phoneNumber || undefined  // ❌ NO!
}
```

**✅ CORRECT - Map each API field to its own output field:**
```typescript
{
  mobilePhone: optional(raw.mobilePhone),
  phoneNumber: optional(raw.phoneNumber)
}
```

**Rule:** If the API has 2 different fields, your output should have 2 different fields. No fallbacks, no defaults, no merging. Use `optional()` for optional fields.

### 6. Nested Objects

**For single nested objects:** Use non-exported helper functions with `mapWith()`:

```typescript
// Helper function - NOT exported, declared BEFORE main mapper
// Does NOT check for null - mapWith() handles that
function toSubResource(raw: any): SubResource {
  // 1. Check for required fields
  ensureProperties(raw, ['id']);

  // 2. Create output object
  const output: SubResource = {
    id: raw.id.toString(),
    name: optional(raw.name)
  };

  return output;
}

// Main mapper - exported, uses helper with mapWith()
export function toResource(raw: any): Resource {
  // 1. Check for required fields
  ensureProperties(raw, ['id']);

  // 2. Create output object
  const output: Resource = {
    id: raw.id.toString(),
    nestedObject: mapWith(toSubResource, raw.nested_object)  // ✅ mapWith handles null/undefined
  };

  return output;
}
```

**For arrays:** Call mapper directly (NO mapWith):

```typescript
// Helper for array items - call directly, NO mapWith
function toSubResource(raw: any): SubResource {
  // 1. Check for required fields
  ensureProperties(raw, ['id']);

  // 2. Create output object
  const output: SubResource = {
    id: raw.id.toString(),
    name: optional(raw.name)
  };

  return output;
}

// Main mapper - arrays call helper directly
export function toResource(raw: any): Resource {
  const output: Resource = {
    id: raw.id.toString(),
    items: raw.items?.map(toSubResource)  // ✅ Direct call, no mapWith
  };

  return output;
}
```

**Rules:**
- Nested mappers are declared BEFORE the parent mapper but are NOT exported
- **Helper functions assume valid input** - they don't check for null/undefined
- **Single objects:** Use `mapWith()` - handles null/undefined at boundary
- **Arrays:** Call mapper directly (NO mapWith) - `raw.items?.map(toMapper)`
- **Return type:** Helpers return plain `T`, not `T | undefined` (mapWith adds the undefined)

## Function Ordering Rules

Mapper functions in `Mappers.ts` MUST be ordered as follows:

### 1. Helper Functions First

All non-exported helper functions declared BEFORE any exported functions:

```typescript
// Helper 1 - NOT exported
function toAddress(raw: any): Address {
  // Implementation
}

// Helper 2 - NOT exported
function toContactInfo(raw: any): ContactInfo {
  // Implementation
}

// Exported mapper that uses helpers
export function toUser(raw: any): User {
  const output: User = {
    address: toAddress(raw.address),
    contact: toContactInfo(raw.contact)
  };
  return output;
}
```

### 2. Dependency Order

If mapper A uses mapper B, B MUST be declared first:

```typescript
// B declared first
function toAddress(raw: any): Address { }

// A declared second (depends on B)
function toUser(raw: any): User {
  return {
    address: toAddress(raw.address)  // Uses B
  };
}
```

### 3. Alphabetical Within Groups

Within each group (helpers, exports), order functions alphabetically:

```typescript
// Helpers in alphabetical order
function toAddress(raw: any): Address { }
function toContactInfo(raw: any): ContactInfo { }
function toMetadata(raw: any): Metadata { }

// Exports in alphabetical order
export function toOrganization(raw: any): Organization { }
export function toUser(raw: any): User { }
export function toWebhook(raw: any): Webhook { }
```

**Exception:** Dependency order overrides alphabetical order.

## Common Patterns Quick Reference

```typescript
// Required field validation - use ensureProperties helper
ensureProperties(raw, ['id', 'email', 'status']);
// ✅ Correctly handles 0, "", false - only rejects null/undefined

// Core type conversion - map() handles undefined automatically
id: map(UUID, raw.id)
email: map(Email, raw.email)
url: map(URL, raw.url)
createdAt: map(DateTime, raw.created_at)
dateOfBirth: map(Date, raw.dateOfBirth)  // No ternary needed!

// Enum conversion
status: toEnum(StatusEnum, raw.status)
type: toEnum(TypeEnum, raw.type, (v) => v.toUpperCase())

// Optional field handling - use optional() to normalize null
name: optional(raw.name)           // null→undefined, keeps ""
description: optional(raw.description)  // null→undefined, preserves ""
phoneNumber: optional(raw.phone_number) // null→undefined, keeps "", 0, false
count: optional(raw.count)         // null→undefined, keeps 0
active: optional(raw.active)       // null→undefined, keeps false

// Single nested object - use mapWith()
config: mapWith(toConfig, raw.config)      // mapWith handles null/undefined at boundary
address: mapWith(toAddress, raw.address)

// Array of nested objects - call mapper directly (NO mapWith)
items: raw.items?.map(toSubResource)       // toSubResource assumes valid input
contacts: raw.contacts?.map(toContact)     // toContact returns Contact

// Array of enums
roles: raw.roles?.map((r: any) => toEnum(UserRole, r))

// ❌ NEVER use logical OR - destroys legitimate values
name: raw.name || undefined        // ❌ WRONG - converts "" to undefined
count: raw.count || 0              // ❌ WRONG - default injection

// ❌ NEVER merge different API fields
phoneNumber: raw.mobilePhone || raw.phoneNumber  // ❌ WRONG - fallback between fields

// ✅ Use optional() for optional fields
name: optional(raw.name)        // ✅ CORRECT - null→undefined, keeps ""
count: optional(raw.count)      // ✅ CORRECT - null→undefined, keeps 0

// ✅ Map each field separately
mobilePhone: optional(raw.mobilePhone)  // ✅ CORRECT
phoneNumber: optional(raw.phoneNumber)  // ✅ CORRECT
```

## Success Criteria

Mapper implementation MUST meet all criteria:

- ✅ All mappers use **const output pattern**
- ✅ **map() utility preferred** over constructors
- ✅ **Required fields validated** per API spec
- ✅ **Optional fields handled** correctly (still map them!)
- ✅ **snake_case converted** to camelCase consistently
- ✅ **Core types applied** (UUID, Email, URL, DateTime)
- ✅ **No API spec weakening** for mapper convenience
- ✅ **ZERO MISSING FIELDS** - all interface fields mapped
- ✅ One mapper function per type
- ✅ Nested objects use separate mapper functions
- ✅ Arrays use array mapper pattern with filter
