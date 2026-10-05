---
name: mapper-runtime
description: Runtime validation for detecting missing mapped fields. Use when validating that all API response fields are properly mapped to output types.
---

# Mapper Runtime Validation Process

**PURPOSE**: Detect missing fields by comparing raw API responses with mapped outputs.

This process catches field mapping bugs that static analysis misses:
- Field name mismatches (e.g., API uses `mobilePhone`, mapper looks for `phoneNumber`)
- Fields present in API but not in spec
- Fields in spec but not mapped
- Type conversion errors

## When to Run Runtime Validation

**MANDATORY for:**
- New module creation (after all operations implemented)
- Adding new operations to existing module
- API spec updates
- After mapper refactoring

**RECOMMENDED for:**
- Periodic validation (quarterly)
- Before major releases
- After API version upgrades

## 4-Step Runtime Validation Process

### Step 1: Add Temporary Debug Logs

Add `[TEMP-RAW-API]` debug logs in each Producer API implementation **BEFORE mapping**:

```typescript
// In UserProducerApiImpl.ts
import { LoggerEngine } from '@zerobias-org/logger';

export class UserProducerApiImpl implements UserProducerApi {
  private readonly logger = LoggerEngine.root().get('UserProducerApiImpl');

  async list(results: PagedResults<User>, organizationId: string): Promise<void> {
    const response = await this.httpClient.get(`/orgs/${organizationId}/users`);

    // 🎯 CRITICAL: Log BEFORE any mapping
    this.logger.debug('[TEMP-RAW-API] listUsers:', JSON.stringify(response.data, null, 2));

    // Then map
    results.items = response.data.data.map(toUser);
    results.count = response.data.totalCount || 0;
  }
}
```

**Key Points:**
- Use `[TEMP-RAW-API]` prefix for easy identification
- Log `response.data` (the raw API payload)
- Log BEFORE any mapper calls
- Add to ALL operations in ALL producers

### Step 2: Run Tests with Debug Logging

```bash
# Run all e2e tests (direct mode) with debug output
cd package/<vendor>/[<suite>/]<service>
LOG_LEVEL=debug zbb testDirect --slot local > /tmp/debug-full.log 2>&1

# Or set LOG_LEVEL on the slot once, then run normally
zbb env set LOG_LEVEL debug --slot local
zbb testDirect --slot local > /tmp/debug-full.log 2>&1

# Or run a focused subset (pass mocha args via --)
LOG_LEVEL=debug zbb testDirect --slot local -- --grep "User Producer" > /tmp/user-debug.log 2>&1
```

**This captures:**
- Raw API responses (from [TEMP-RAW-API] logs)
- Mapped results (from test debug logs)
- All field values before and after transformation

### Step 3: Compare Raw vs Mapped

**Manual Analysis:**
```bash
# 1. Extract raw API response
grep -A 100 "\[TEMP-RAW-API\] listUsers" /tmp/user-debug.log > /tmp/raw-api.txt

# 2. Extract mapped result
grep -A 50 "userApi.list" /tmp/user-debug.log > /tmp/mapped-result.txt

# 3. Compare field-by-field
diff /tmp/raw-api.txt /tmp/mapped-result.txt
```

**Automated Analysis (RECOMMENDED):**

Use parallel mapping-engineer agents to analyze each producer:

```typescript
// Launch one agent per producer
Task(mapping-engineer, {
  prompt: `Analyze User producer for missing fields:
  1. Read /tmp/user-debug.log
  2. Extract [TEMP-RAW-API] responses
  3. Compare with mapper in src/Mappers.ts
  4. List ALL missing fields
  5. Update mapper if needed`
})
```

Run all 11 in parallel for fastest results.

### Step 4: Fix Missing Fields

For each missing field found:

1. **Check if field is in API spec** (api.yml)
   - YES → Update mapper immediately
   - NO → Escalate to schema-specialist to update spec first

2. **Update mapper** to include field:
```typescript
// Before (missing field)
const output: User = {
  id: String(raw.id),
  name: raw.name,
  email: map(Email, raw.email)
  // Missing: phoneNumber
};

// After (field added)
const output: User = {
  id: String(raw.id),
  name: raw.name,
  email: map(Email, raw.email),
  phoneNumber: optional(raw.mobilePhone)  // ← Added (note field name difference!)
};
```

3. **Re-run validation** to verify fix

4. **Remove temp debug logs** when complete:
```bash
# Find all temp logs
grep -r "\[TEMP-RAW-API\]" src/

# Remove them after validation passes
```

## Common Issues Found by Runtime Validation

### Issue 1: Field Name Mismatches

**Example:** API uses `mobilePhone`, spec defines `phoneNumber`

```typescript
// ❌ WRONG - Looking for wrong field name
phoneNumber: optional(raw.phoneNumber)  // API doesn't have this field!

// ✅ CORRECT - Use actual API field name
phoneNumber: optional(raw.mobilePhone)  // Maps API field to interface field
```

**Detection:** Raw API log shows `mobilePhone`, mapped output has `phoneNumber: undefined`

### Issue 2: Missing Nested Object Fields

**Example:** API returns `identity.namespace` with 3 fields, mapper only maps 1

```typescript
// ❌ WRONG - Incomplete nested mapping
function toIdentityNamespace(raw: any): IdentityNamespace {
  return {
    id: raw.id
    // Missing: nickname, namespaceType
  };
}

// ✅ CORRECT - All fields mapped
function toIdentityNamespace(raw: any): IdentityNamespace {
  ensureProperties(raw, ['id']);
  return {
    id: raw.id,
    nickname: optional(raw.nickname),
    namespaceType: mapWith(toNamespaceType, raw.namespaceType)
  };
}
```

**Detection:** Raw API log shows 3 fields in namespace, mapped output only has `id`

### Issue 3: API Returns Fields Not in Spec

**Example:** API returns `boundary`, `contactName`, `contactPhone` but spec doesn't define them

```bash
# Raw API response
{
  "id": 1239,
  "name": "Site 1",
  "boundary": null,        ← NOT in spec
  "contactName": null,     ← NOT in spec
  "contactPhone": null     ← NOT in spec
}
```

**Action:**
1. **DO NOT add to mapper** (will cause TypeScript error)
2. **Escalate to schema-specialist** to update api.yml
3. **Document in issue tracker**
4. **After spec updated** → regenerate types → update mapper

### Issue 4: Array Element Mapping Incomplete

**Example:** API returns array with 5 fields per item, mapper only maps 3

```typescript
// ❌ WRONG - Array elements incompletely mapped
entries: raw.entries?.map((e: any) => ({
  id: e.id,
  name: e.name
  // Missing: 3 more fields per element
}))

// ✅ CORRECT - Use helper mapper
function toEntry(raw: any): Entry {
  ensureProperties(raw, ['id', 'name']);
  return {
    id: String(raw.id),
    name: raw.name,
    zone: mapWith(toZone, raw.zone),
    acu: mapWith(toAcu, raw.acu),
    status: optional(raw.status)
    // All 5 fields mapped
  };
}

entries: Array.isArray(raw.entries) ? raw.entries.map(toEntry) : undefined
```

**Detection:** Raw API shows 5 fields per array element, mapped shows only 2

## Runtime Validation Checklist

Before marking mapper validation complete:

- [ ] Added [TEMP-RAW-API] debug logs to all operations
- [ ] Ran e2e tests (`zbb testDirect --slot local`) with LOG_LEVEL=debug
- [ ] Captured debug output to file(s)
- [ ] Extracted raw API responses
- [ ] Extracted mapped results
- [ ] Compared field-by-field for each operation
- [ ] Verified ZERO missing fields
- [ ] Checked for field name mismatches
- [ ] Validated nested object completeness
- [ ] Validated array element mapping
- [ ] Fixed any missing fields
- [ ] Re-ran validation to confirm fix
- [ ] Removed [TEMP-RAW-API] debug logs
- [ ] Documented any API-spec gaps

## Parallel Agent Pattern

For modules with multiple producers, use parallel agents for efficiency:

```typescript
// Launch one mapping-engineer agent per producer
const producers = [
  'Auth', 'User', 'Group', 'Entry', 'Site', 'Zone',
  'Audit', 'Schedule', 'Role', 'Credential', 'IdentityProvider'
];

// Single message with multiple Task invocations
producers.map(producer =>
  Task(mapping-engineer, {
    description: `Analyze ${producer} mapper`,
    prompt: `
      1. Read /tmp/${producer.toLowerCase()}-debug.log
      2. Extract [TEMP-RAW-API] responses
      3. Compare with mapper in src/Mappers.ts
      4. List ALL missing fields
      5. Update mapper if needed
      6. Return detailed report
    `
  })
);
```

**Benefits:**
- All producers analyzed simultaneously
- 10-20x faster than sequential
- Each agent focuses on one producer
- Clear separation of concerns

## Example Session Output

When runtime validation finds issues:

```
✅ Auth Producer      - 0 missing fields (10/10 mapped)
❌ User Producer      - 14 missing fields found:
   - fullName, initials, opal
   - mobilePhone (field name mismatch: API uses mobilePhone, mapper looks for phoneNumber)
   - isEmailVerified, idpUniqueIdentifier, language
   - nicknames, needsPasswordChange
   - createdAt, updatedAt
   - IdentityNamespace.nickname, IdentityNamespace.namespaceType
✅ Group Producer     - 0 missing fields (12/12 mapped)
... etc
```

## Integration with Validation Gates

This runtime validation should be added to **Gate 3: Implementation Validation**:

```bash
# After all operations implemented
zbb testDirect --slot local       # All e2e tests pass
zbb build                         # Build succeeds

# THEN run runtime mapper validation
LOG_LEVEL=debug zbb testDirect --slot local > /tmp/validation.log 2>&1
# Analyze for missing fields (manual or agent-assisted)
```

Gate 3 should not pass until:
- [ ] All e2e tests pass (`zbb testDirect --slot local`)
- [ ] Runtime validation shows ZERO missing fields
- [ ] No API-spec gaps documented

## Tools and Scripts

Save per-producer logs for easier analysis:

```bash
#!/bin/bash
# run-producer-validation.sh

PRODUCERS=(
  "Auth Producer:auth"
  "User Producer:user"
  "Group Producer:group"
  # ... etc
)

for producer in "${PRODUCERS[@]}"; do
  IFS=':' read -r pattern name <<< "$producer"
  LOG_LEVEL=debug zbb testDirect --slot local -- --grep "$pattern" > /tmp/debug-$name.log 2>&1
done
```

Then analyze each file separately.

## References

- Static validation: @.claude/skills/mapper-validation/SKILL.md
- Mapper patterns: @.claude/skills/mapper-patterns/SKILL.md
- Mapping engineer: @.claude/agents/mapping-engineer.md
- Operation engineer: @.claude/agents/operation-engineer.md
- Gate 3 validation: @.claude/workflows/implementation-validation.md
