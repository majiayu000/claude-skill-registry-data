---
name: implementation-core
description: Core implementation rules applying to all code. Use when implementing any TypeScript code to ensure compliance with fundamental standards.
---

# Implementation Core Rules

## 🚨 CRITICAL RULES (Apply to ALL Code)

### Rule #2: No Environment Variables in Module Source

- **FORBIDDEN**: `process.env.*` in `src/` directory
- **ONLY EXCEPTION**: `test/Common.ts` may read env vars
- **MANDATORY**: All params from method arguments or connection profile

```typescript
// ✅ ALLOWED: test/Common.ts
export const TEST_API_KEY = process.env.TEST_API_KEY || '';

// ❌ FORBIDDEN: Any src/ file
const apiKey = process.env.API_KEY; // NEVER
```

### Rule #3: Core Error Usage

- **NEVER** use generic `Error` class
- **ALWAYS** use errors from `@zerobias-org/types-core-js`
- See [error-handling.md](./error-handling.md)

### Rule #4: Type Generation Workflow

**MANDATORY SEQUENCE:**
```bash
# 1. Update API spec
vim api.yml

# 2. IMMEDIATELY generate types (MANDATORY)
zbb generate

# 3. THEN implement using generated types
vim src/SomeProducer.ts

# 4. Build and validate
zbb build
```

- **NEVER use `any`** in producer method signatures
- **ALWAYS use generated interfaces** from generated/api/

### Rule #5: API Specification is Source of Truth

**🚨 CRITICAL: NEVER modify API spec to match mapper logic**

```typescript
// ❌ WRONG APPROACH: Weakening API spec because mapper has issues
// api.yml - removing 'id' from required because mapper can't handle it
Organization:
  type: object
  properties:    # ❌ NO! Don't remove required to fix mapper
    id:
      type: string

// ✅ CORRECT APPROACH: Mapper validates required fields from API spec
// api.yml - Keep spec accurate to API documentation
Organization:
  type: object
  required:
    - id       # ✅ YES! Spec reflects API reality
  properties:
    id:
      type: string

// Mapper validates required field
export function toOrganization(data: any): Organization | undefined {
  if (!data) return undefined;

  if (!data.id && data.id !== 0) {  // ✅ YES! Validate required fields
    throw new InvalidInputError('organization', 'Missing required field: id');
  }

  return {
    id: String(data.id),
    name: data.name || undefined,
  };
}
```

**RULE**: API spec drives implementation, NOT the other way around.
- API spec reflects API documentation (source of truth)
- Mappers validate and throw errors for missing required fields
- NEVER weaken spec (remove required, add nullable) to make mapper easier

**WHY**:
- API spec is contract with external API
- Type safety depends on accurate spec
- Validation belongs in mappers, not spec modification

### Rule #6: Build Gate Compliance

- `zbb build` MUST pass before ANY implementation
- If build fails at ANY point, STOP immediately
- No implementation while build is broken

### Rule #6 (duplicate): Never Use Python

- Only Bash and Node.js when needed
- Prefer curl for API testing

### Rule #7: Never Create Module Root Files Manually

- **FORBIDDEN**: Manually creating module root files (package.json, tsconfig.json, api.yml, etc.)
- **MANDATORY**: Use Yeoman generator to create module scaffolding
- **EXCEPTION**: Documentation files (.md) may be created manually

```bash
# ✅ CORRECT - Use Yeoman generator
yo @zerobias-org/module

# ❌ FORBIDDEN - Manual file creation
touch package.json  # NO!
touch api.yml       # NO!
touch tsconfig.json # NO!

# ✅ ALLOWED - Documentation files
touch USERGUIDE.md  # YES!
touch README.md     # YES!
```

**WHY**: Yeoman generator ensures consistent structure, proper dependencies, and correct configuration across all modules.

## File Organization

```
src/
├── {Service}Client.ts          # HTTP client only
├── {Service}ConnectorImpl.ts   # Main connector
├── {Resource}Producer.ts       # One per resource
├── Mappers.ts                  # ALL mappers in single file
├── util.ts                     # Error handler
└── index.ts                    # Exports + factory function
```

## src/index.ts Pattern - MANDATORY Factory Function

**CRITICAL**: The `src/index.ts` file MUST export a factory function following this exact pattern:

```typescript
import { {Service}Connector } from '../generated/api';
import { {Service}ConnectorImpl } from './{Service}ConnectorImpl';

export * from '../generated/api';
export * from '../generated/model';

export function new{Service}(): {Service}Connector {
  return new {Service}ConnectorImpl();
}
```

**Examples**:
```typescript
// ✅ CORRECT - Avigilon Alta Access
export function newAvigilonAltaAccess(): AvigilonAltaAccessConnector {
  return new AvigilonAltaAccessConnectorImpl();
}

// ✅ CORRECT - ReadyPlayerMe
export function newReadyPlayerMe(): ReadyPlayerMeConnector {
  return new ReadyPlayerMeImpl();
}

// ❌ WRONG - Missing factory function
export * from '../generated/api';
export * from '../generated/model';
export { MyConnectorImpl } from './MyConnectorImpl';  // NO! Need factory function
```

**WHY**:
- Consistent instantiation pattern across all modules
- Consumers call `newServiceName()` instead of using `new`
- Hides implementation details from consumers
- Allows for future initialization logic in factory

**NAMING CONVENTION**:
- Function name: `new{Service}` in camelCase
- Return type: `{Service}Connector` interface from generated code
- NO "Impl" suffix in public API

## Connector Implementation - CRITICAL RULES

### 🚨 ConnectorImpl Class

```typescript
// ✅ CORRECT - Extends ONLY the generated interface
export class GitHubConnectorImpl extends GitHubConnector {
  // NO other base classes, NO AbstractConnector, JUST the generated interface
}
```

### NEVER GUESS METHOD SIGNATURES

1. **READ** the generated interface in `generated/api/index.ts`
2. **CHECK** what methods the generated connector interface defines
3. **IMPLEMENT** exactly those methods with exact signatures
4. **VERIFY** against the generated file

### Discovery Process for ConnectorImpl

1. Run `zbb generate` (must be done first)
2. Open `generated/api/index.ts`
3. Find the `{Service}Connector` interface
4. Read ALL methods defined in that interface
5. Implement EXACTLY those methods in `{Service}ConnectorImpl`
6. Check parameter types, return types from the generated interface

### 🚨 CRITICAL: metadata() and isSupported() Methods

**These methods MUST be implemented with EXACT boilerplate - NEVER customize them!**

```typescript
// ✅ CORRECT - EXACT boilerplate (always the same)
export class GitHubConnectorImpl extends GitHubConnector {

  async metadata(): Promise<ConnectionMetadata> {
    return { status: ConnectionStatus.Down } satisfies ConnectionMetadata;
  }

  async isSupported(_operationId: string) {
    return OperationSupportStatus.Maybe;
  }

  // Then implement actual API operation methods
  async getUser(userId: string): Promise<User> { ... }
  async listUsers(results: PagedResults<User>): Promise<void> { ... }
}

// ❌ WRONG - Customizing these methods
export class GitHubConnectorImpl extends GitHubConnector {
  async metadata(): Promise<ConnectionMetadata> {
    return {
      status: ConnectionStatus.Up,  // NO! Always Down
      version: '1.0.0',  // NO! Don't add fields
      capabilities: []  // NO! Don't add fields
    } satisfies ConnectionMetadata;
  }

  async isSupported(operationId: string) {
    if (operationId === 'getUser') return OperationSupportStatus.Yes;  // NO! Always Maybe
    return OperationSupportStatus.No;
  }
}
```

**WHY**: Hub manages actual connector metadata and operation support. These are placeholder implementations that the hub overrides at runtime.

**RULES**:
- ✅ metadata() is `async`, returns `Promise<ConnectionMetadata>`
- ✅ metadata() ALWAYS returns `{ status: ConnectionStatus.Down } satisfies ConnectionMetadata`
- ✅ isSupported() is `async`, parameter named `_operationId` (underscore - unused)
- ✅ isSupported() ALWAYS returns `OperationSupportStatus.Maybe`
- ❌ NEVER customize these methods
- ❌ NEVER add logic to determine status or support
- ❌ NEVER add additional properties to metadata

**NEVER**:
- ❌ Guess method signatures - READ from generated interface
- ❌ Extend classes other than the generated interface
- ❌ Customize `metadata()` method (always DOWN)
- ❌ Customize `isSupported()` method (always Maybe)
- ❌ Implement methods not in the generated interface

## Error Handler Pattern

```typescript
// src/util.ts
import {
  InvalidCredentialsError,
  NoSuchObjectError,
  UnauthorizedError,
  RateLimitExceededError,
  UnexpectedError
} from '@zerobias-org/types-core-js';

export function handleAxiosError(error: any): never {
  const status = error.response?.status || 500;
  const message = error.response?.data?.message || error.message;

  switch (status) {
    case 401:
      throw new InvalidCredentialsError();
    case 403:
      throw new UnauthorizedError();
    case 404:
      throw new NoSuchObjectError('resource', 'unknown');
    case 429:
      throw new RateLimitExceededError();
    default:
      throw new UnexpectedError(`API error: ${message}`, status);
  }
}
```

## TypeScript Configuration

Add to tsconfig.json:
```json
{
  "compilerOptions": {
    "skipLibCheck": true
  }
}
```

## Import Organization

```typescript
// Core types - from @zerobias-org packages
import { URL, UUID, Email } from '@zerobias-org/types-core-js';
import { toEnum, map } from '@zerobias-org/util-hub-module-utils';

// NEVER from Node.js built-ins
// ❌ import { URL } from 'url';
```

## Type Discovery Priority

1. Check generated/api/index.ts for exact names
2. Check library .d.ts files
3. Check existing Mappers for patterns
4. Check OpenAPI spec (adapt to TypeScript)
5. Never guess

## Producer Implementation Patterns

### Class Structure

```typescript
export class UserProducerApiImpl implements UserProducerApi {
  private readonly httpClient: AxiosInstance;  // ✅ readonly modifier required

  constructor(private readonly client: AvigilonAltaAccessClient) {  // ✅ readonly
    this.httpClient = client.getHttpClient();
  }

  // ... methods
}
```

**Requirements:**
- ✅ All class properties MUST use `readonly` modifier
- ✅ Constructor parameters should be `readonly` when stored
- ✅ Use `private readonly` for internal properties

### GET Method Pattern - Response Validation Required

```typescript
async get(organizationId: string, userId: string): Promise<UserInfo> {
  const response = await this.httpClient.get(`/orgs/${organizationId}/users/${userId}`);

  // ✅ REQUIRED - Validate response before mapping
  const rawData = response.data.data || response.data;
  if (!rawData) {
    throw new NoSuchObjectError('user', userId);
  }

  return toUserInfo(rawData);
}
```

**Rules:**
- ✅ ALWAYS validate response exists with `if (!rawData)` check
- ✅ Use `NoSuchObjectError` with resource type and ID
- ✅ Support both `response.data.data` and `response.data` structures
- ❌ NEVER return undefined or null without throwing

### LIST Method Pattern - Array Validation Required

```typescript
async list(results: PagedResults<User>, organizationId: string): Promise<void> {
  const params: Record<string, number> = {};

  // ✅ REQUIRED - Initialize offset even when pagination not provided
  if (results.pageNumber && results.pageSize) {
    params.offset = (results.pageNumber - 1) * results.pageSize;
    params.limit = Math.min(Math.max(results.pageSize, 1), 1000);
  } else {
    params.offset = 0;  // ✅ MANDATORY else clause
  }

  const response = await this.httpClient.get(`/orgs/${organizationId}/users`, { params });

  // ✅ REQUIRED - Validate array before mapping
  if (!response.data || !Array.isArray(response.data.data)) {
    throw new UnexpectedError('Invalid response format: expected data array');
  }

  // ✅ Map without ternary (validation ensures array exists)
  results.items = response.data.data.map(toUser);
  results.count = response.data.totalCount || 0;
}
```

**Rules:**
- ✅ ALWAYS include `else { params.offset = 0; }` for pagination
- ✅ ALWAYS validate `Array.isArray(response.data.data)` before mapping
- ✅ Use `UnexpectedError` for invalid response structure
- ✅ No ternary operators after validation - array is guaranteed to exist
- ❌ NEVER assign `pageToken` for offset/limit pagination (use token-based pagination pattern instead)
- ❌ NEVER return empty array without validation

### URL Path Consistency

```typescript
// ✅ CORRECT - Use /orgs/ prefix consistently
const response = await this.httpClient.get(`/orgs/${organizationId}/users`);
const response = await this.httpClient.get(`/orgs/${organizationId}/groups/${groupId}`);

// ❌ WRONG - Mixing /organizations/ and /orgs/
const response = await this.httpClient.get(`/organizations/${organizationId}/users`);  // NO!
```

**Rules:**
- ✅ ALL operations use `/orgs/` prefix (not `/organizations/`)
- ✅ Consistent URL patterns across all producers
- ❌ NEVER mix different URL prefixes

### Imports Pattern

```typescript
// ✅ REQUIRED imports for error handling
import { AxiosInstance } from 'axios';
import { PagedResults, NoSuchObjectError, UnexpectedError } from '@zerobias-org/types-core-js';
import { UserProducerApi } from '../generated/api/UserApi';
import { User, UserInfo } from '../generated/model';
import { AvigilonAltaAccessClient } from './AvigilonAltaAccessClient';
import { toUser, toUserInfo } from './Mappers';
```

**Requirements:**
- ✅ Import `NoSuchObjectError` for GET methods
- ✅ Import `UnexpectedError` for LIST methods
- ✅ Import all mapper functions used

## Stub Implementation Pattern

When operations exist in api.yml but aren't ready for full implementation, create stub methods that throw errors:

```typescript
// ✅ CORRECT - Stub with error throw
/* eslint-disable @typescript-eslint/no-unused-vars, class-methods-use-this */
async listZoneShares(
  results: PagedResults<ZoneShare>,
  _organizationId: string,
  _zoneId: string
): Promise<void> {
  throw new Error('Not implemented');
}

async listOtherStub(
  results: PagedResults<OtherType>,
  _param1: string
): Promise<void> {
  throw new Error('Not implemented');
}
/* eslint-enable @typescript-eslint/no-unused-vars, class-methods-use-this */

// ❌ WRONG - Empty implementation (returns silently)
async listZoneShares(
  results: PagedResults<ZoneShare>,
  organizationId: string,
  zoneId: string
): Promise<void> {
  results.items = [];  // NO! Will silently fail
  results.count = 0;
}

// ❌ WRONG - Line-by-line disable comments
// eslint-disable-next-line @typescript-eslint/no-unused-vars, class-methods-use-this
async listZoneShares(...): Promise<void> {
  // This doesn't suppress warnings on parameter lines
}
```

**Rules**:
- ALL methods from generated API interfaces MUST be implemented
- Use `throw new Error('Not implemented')` for stubs - NEVER return empty results
- Use block-style `/* eslint-disable */` comments for multiple stubs
- Prefix unused parameters with underscore (e.g., `_organizationId`)
- Group multiple stubs within a single disable/enable block
- Build must succeed even with stub implementations

**Why**:
- Stubs that throw errors clearly signal unimplemented functionality vs. silently returning empty data
- Block-style comments properly suppress warnings for all parameter lines
- TypeScript requires all interface methods to be implemented for the build to pass

## Mapper Creation Rule

**Only create mappers when used by producers**, not for every schema in api.yml.

```typescript
// ✅ CORRECT - Mapper used by producer
export function mapUser(raw: any): User {
  return new User(
    String(raw.id),
    raw.name,
    map(Email, raw.email)
  );
}

// ❌ WRONG - Mapper for unused schema
export function mapUnusedSchema(raw: any): UnusedSchema {
  // This schema isn't referenced by any producer
}
```

**When to create mappers**:
- Producer implementation calls it to map API responses
- Schema is returned by an operation you're implementing

**When NOT to create mappers**:
- Schema exists in api.yml but no producer uses it yet
- Schema is only used for request bodies (not responses)

## <Product>Impl Pattern

The main connector implementation follows the `<Product>Impl` pattern:

```typescript
// ✅ CORRECT - AccessImpl for Avigilon Alta Access
export class AccessImpl implements AccessConnector {
  private client: AvigilonAltaAccessClient;
  private userApiProducer?: UserApi;
  private roleApiProducer?: RoleApi;
  // ... all API producers

  getUserApi(): UserApi {
    if (!this.userApiProducer) {
      const producer = new UserProducerApiImpl(this.client);
      this.userApiProducer = wrapUserProducer(producer);  // Generated wrapper
    }
    return this.userApiProducer;
  }

  getRoleApi(): RoleApi {
    if (!this.roleApiProducer) {
      const producer = new RoleProducerApiImpl(this.client);
      this.roleApiProducer = wrapRoleProducer(producer);  // Generated wrapper
    }
    return this.roleApiProducer;
  }
  // ... implement getter for ALL API tags
}
```

**Critical Rules**:
- Pattern: `<Product>Impl` (e.g., `AccessImpl`, `GitHubImpl`)
- Must implement getters for **ALL API tags** defined in api.yml
- API wrappers (`wrapUserProducer`, `wrapRoleProducer`) are **GENERATED** - never hand-written
- Producer implementations (`UserProducerApiImpl`) are hand-written
- Use lazy initialization pattern for API producers

**Example**: If api.yml has tags: `[user, role, site, group, entry, zone]` → `<Product>Impl` needs 6 getters.

## Cleanup After Success

After implementing changes and verifying they work:

### Remove Backup Files

```bash
# Remove backup files when new implementation works
rm -f *.backup *.bak *.bak2 *.bak3 *.OLD

# Check for backup files
find . -type f \( -name "*.backup" -o -name "*.bak*" -o -name "*.OLD" \)
```

### Remove Unused Schemas

```bash
# After api.yml changes, remove schemas not referenced anywhere
# 1. List all schemas
yq eval '.components.schemas | keys' api.yml

# 2. For each schema, check if it's referenced
grep -r "schemas/SchemaName" api.yml

# 3. Remove unused schemas from api.yml
```

**When to clean up**:
- After successful build and tests pass
- After refactoring schema names (e.g., EntryDetails → Entry)
- Before committing changes

**What to remove**:
- Backup files (.backup, .bak, etc.)
- Unused/deprecated schemas from api.yml
- Old test fixtures that don't match new structure

## TypeScript Generation Workflow

After any api.yml changes:

```bash
# 1. Regenerate TypeScript types (gradle handles invalidation under the hood)
zbb generate

# 2. Verify generated types match expectations
ls generated/api/
ls generated/model/

# 3. Implement/update producers using new types
# ... make code changes

# 4. Build and verify
zbb build
```

**Critical**: Always regenerate types before implementing code changes that depend on api.yml updates.

## Code Style

- No comments unless specifically requested
- Clear, self-documenting code
- Follow existing patterns in codebase
- Consistent naming throughout

## API Quirks Handling

### APIs Returning 200 for Errors

Apply "fake error handler":

```typescript
async someOperation(): Promise<Resource> {
  const response = await this.httpClient.get('/resource');

  if (response.status === 200 && response.data.error) {
    if (response.data.error === 'NOT_FOUND') {
      throw new NoSuchObjectError('resource', 'unknown');
    }
    throw new UnexpectedError(response.data.error_message);
  }

  return toResource(response.data);
}
```

### Rate Limiting

Simple - just throw:
```typescript
case 429:
  throw new RateLimitExceededError();
```

## Dependency Management

### Required Dependencies (package.json)

**MANDATORY packages that MUST be in dependencies:**

```json
{
  "dependencies": {
    "@zerobias-org/types-core-js": "^4.5.19",
    "@zerobias-org/util-hub-module-utils": "^1.0.0",
    "@zerobias-org/logger": "^4.0.9"
  },
  "peerDependencies": {
    "@zerobias-org/types-core": "^4.9.1",
    "@zerobias-org/types-core-js": "^4.10.2"
  }
}
```

**What each package provides:**

- **`@zerobias-org/types-core-js`** - Hub framework core functionality, interfaces
- **`@zerobias-org/util-hub-module-utils`** - **MANDATORY** - Provides `map()`, `toEnum()`, `mapArray()` functions for type mapping
- **`@zerobias-org/logger`** - Logging utilities (winston wrapper)
- **`@zerobias-org/types-core`** - Core type schemas
- **`@zerobias-org/types-core-js`** - Core TypeScript types (UUID, Email, URL, DateTime, Errors, etc.)

**Why util-hub-module-utils is mandatory:**
- Provides `map()` function used in ALL mappers
- Handles optional value mapping automatically
- Ensures consistent type conversion patterns
- Without it, mappers will fail to compile

## Validation Scripts

### Validate Core Rules Compliance

```bash
# Check no process.env in src/ (except test/Common.ts)
grep -r "process\.env" src/ --exclude="*/test/Common.ts" && echo "❌ Found process.env in src/!" || echo "✅ No process.env in src/"

# Check using core errors (not generic Error)
grep -E "throw new Error\(" src/ && echo "❌ Using generic Error!" || echo "✅ Using core errors"

# Check build passes
zbb build && echo "✅ Build passes" || echo "❌ Build failed!"

# Check factory function exists
grep -E "export function new[A-Z]" src/index.ts && echo "✅ Factory function present" || echo "❌ Missing factory function"
```

### Validate Connector Implementation

```bash
# Check metadata() returns correct boilerplate
grep -A 1 "async metadata()" src/*ConnectorImpl.ts | grep "ConnectionStatus.Down" && echo "✅ metadata() correct" || echo "❌ metadata() incorrect"

# Check isSupported() returns Maybe
grep -A 1 "async isSupported" src/*ConnectorImpl.ts | grep "OperationSupportStatus.Maybe" && echo "✅ isSupported() correct" || echo "❌ isSupported() incorrect"
```

### Validate Dependencies

```bash
# Check required dependencies present
grep -E "(@zerobias-org/types-core-js|@zerobias-org/util-hub-module-utils|@zerobias-org/logger)" package.json && echo "✅ Required deps present" || echo "❌ Missing required dependencies"
```
