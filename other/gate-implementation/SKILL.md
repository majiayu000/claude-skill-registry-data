---
name: gate-implementation
description: Gate 3 — Impl/Producer/Mapper code is shaped right and uses generated types. Use after Gate 2, before writing tests.
---

# Gate 3: Implementation

Code under `src/` is consistent with the generated interface, free of typed-any holes, and ready for tests. `:compile` and `:lint` both pass.

## What to check

```bash
# 1. TypeScript compiles
zbb compile

# 2. ESLint passes
zbb lint

# 3. No Promise<any> in src/
grep -rn "Promise<any>" src/ \
  && echo "✗ Promise<any> in src/" || echo "✓ typed promises"

# 4. No env access in src/
grep -rn "process\.env" src/ \
  && echo "✗ process.env in src/" || echo "✓ src clean"

# 5. ESM imports — every relative import ends in .js
grep -rnE "from '\.\.?\/[^']*'" src/ | grep -v "\.js'" \
  && echo "✗ missing .js extensions" || echo "✓ ESM imports OK"

# 6. Source uses generated types
grep -rn "from '../generated/" src/ | head
# Should print imports; no module wires the Impl without referencing generated/.

# 7. Impl extends the generated connector interface, not an abstract class
ls src/*Impl.ts | while read f; do
  grep -E "implements [A-Z][a-zA-Z]+Connector" "$f" >/dev/null \
    || echo "✗ $f does not implement <Class>Connector"
done

# 8. Connector boilerplate: connect/disconnect/metadata/isConnected/isSupported all present
ls src/*Impl.ts | while read f; do
  for m in connect disconnect metadata isConnected isSupported; do
    grep -qE "async ${m}\s*\(" "$f" || echo "✗ $f missing async ${m}()"
  done
done

# 9. Producer methods don't take connection context as parameters
grep -rnE "(apiKey|token|baseUrl|organizationId|region):\s*string" src/*Producer*.ts 2>/dev/null \
  && echo "✗ connection context leaked into producer signature" \
  || echo "✓ producer signatures clean"

# 10. Mappers prefer map() from util-hub-module-utils
if ls src/mappers/*.ts >/dev/null 2>&1 || [ -f src/Mappers.ts ]; then
  MAPPERS=$(ls src/mappers/*.ts 2>/dev/null; [ -f src/Mappers.ts ] && echo src/Mappers.ts)
  for f in $MAPPERS; do
    if grep -E "new (UUID|Email|URL|DateTime)\(" "$f" >/dev/null; then
      echo "warn: $f constructs core types directly — prefer map() from @zerobias-org/util-hub-module-utils"
    fi
    grep -q "from '@zerobias-org/util-hub-module-utils'" "$f" \
      || echo "warn: $f doesn't import from @zerobias-org/util-hub-module-utils"
  done
fi

# 11. Error handling: producers either let core errors bubble or wrap with named core types
grep -rnE "throw new Error\(" src/*Producer*.ts 2>/dev/null \
  && echo "warn: throwing raw Error — prefer InvalidCredentialsError / NoSuchObjectError / RateLimitExceededError" \
  || echo "✓ no raw Error throws"
```

## Connector method shape

For connectors, the impl needs these methods. The generator scaffolds stubs; Gate 3 is where they get real implementations.

| Method                                  | Returns                                  | Notes                                                            |
|-----------------------------------------|------------------------------------------|------------------------------------------------------------------|
| `connect(profile: ConnectionProfile)`   | `Promise<void>`                          | Persist config, do a credential check (`isConnected()` will be called separately) |
| `disconnect()`                          | `Promise<void>`                          | Release any held resources; idempotent                            |
| `isConnected()`                         | `Promise<boolean>`                       | Light-weight ping; safe to call repeatedly                       |
| `metadata()`                            | `Promise<ConnectionMetadata>`            | Return current `{ status, ... }`. Default stub returns `Down`.    |
| `isSupported(operationId)`              | `Promise<OperationSupportStatus>`        | Default stub returns `Maybe`; specialize only when needed         |
| `get<Tag>Api()` (one per tag in api.yml)| Producer instance                        | Returns the producer for that resource group                     |

The boilerplate the generator scaffolds is fine to ship as long as the module isn't *required* to differentiate `metadata`/`isSupported` behavior; for most modules it's enough. Customize only when there's a real reason.

## Mapper rule: prefer `map()` over constructors

`@zerobias-org/util-hub-module-utils` exports `map(Type, value)` which:

- handles `undefined` / `null` for optional fields without a wrapper check
- delegates to the core type constructor when the value is present
- short-circuits cleanly so mappers stay flat

```typescript
import { map } from '@zerobias-org/util-hub-module-utils';
import type { User } from '../generated/model/index.js';
import type { ApiUser } from '@example/api-types';

export function mapUser(input: ApiUser): User {
  return {
    id:        map(UUID, input.id),
    email:     map(Email, input.emailAddress),
    createdAt: map(DateTime, input.created_at),
    name:      input.displayName,
  };
}
```

Direct `new UUID(input.id)` works too but doesn't gracefully handle missing values and tends to grow into a maze of ternaries.

## Runtime mapper validation (call out separately)

Static checks miss field-name mismatches between API responses and your mappers. After mappers are written, run the runtime validation in `@.claude/skills/mapper-runtime/SKILL.md` — it adds temporary debug logs, runs e2e direct mode, and diffs raw API → mapped output. Gate 3 passes only when that validation shows zero missing fields.

## Pass criteria

- `zbb compile` exits 0
- `zbb lint` exits 0
- `<Class>Impl` implements the generated `<Class>Connector` interface
- All five connector lifecycle methods present and `async`
- No `Promise<any>`, no `process.env` in `src/`
- All relative imports end in `.js`
- Mappers import from `@zerobias-org/util-hub-module-utils`
- Mapper runtime validation completed: zero missing fields

## On failure

- TypeScript errors against generated types — usually an `api.yml` change that wasn't followed by `zbb generate`. Run Gate 2 again.
- ESLint errors — fix the source; only add an eslint-disable comment with a referenced bug, never a bare one.
- "constructor expects X arguments, got Y" — the codegen renamed or repositioned a type after a spec edit. Update the call site.

## Related

- @.claude/skills/implementation-core/SKILL.md — `src/` rules across modules
- @.claude/skills/impl-wrapper/SKILL.md — Impl class layout
- @.claude/skills/producer-implementation/SKILL.md — producer patterns
- @.claude/skills/mapper-patterns/SKILL.md — mapper structure
- @.claude/skills/mapper-runtime/SKILL.md — runtime field validation
- @.claude/skills/type-mapping/SKILL.md — API ↔ core type table
- @.claude/skills/error-handling/SKILL.md — when to throw which core error
