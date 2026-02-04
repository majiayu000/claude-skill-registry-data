---
name: surgical-injector
description: "Safely inject new code into legacy codebases with risk containment. Use for feature flags, gradual rollouts, A/B testing new logic, or refactoring critical paths. Implements try-catch fallbacks, feature toggle architecture, and surgical separation of old/new code."
---

# Surgical Injector

Inject new code into legacy systems with zero-downtime safety. Keep dirty legacy code and clean new code physically separated.

## Core Philosophy

**Do NOT rewrite old code.** Instead:
1. Extract new logic into a separate helper function
2. Add a feature toggle (config/env variable)
3. Wrap in try-catch that falls back to old behavior
4. Document the surgery for future cleanup

## The Surgery Pattern

Always follow this structure:

```javascript
// [SURGERY] YYYY-MM-DD - Feature: X | Task: #123 | Deprecate: YYYY-MM-DD
function legacyFunction(input) {
  // NEW CODE PATH (Guarded)
  try {
    if (shouldUseNewFeatureX()) {
      return newFeatureXLogic(input);
    }
  } catch (error) {
    // Fail silent - fall through to old logic
    console.error('[SURGERY-FAIL] newFeatureXLogic:', error.message);
    // TODO: Send to monitoring/bug tracking
  }

  // OLD CODE PATH (Original - Keep untouched)
  return originalLogic(input);
}

// New logic extracted to separate function
function newFeatureXLogic(input) {
  // Clean, isolated implementation
}
```

## Step-by-Step Workflow

### 1. Locate the Target

Find the function or logic block to modify using Grep/Read:

```bash
Grep pattern: "function targetFunction|def target_function|class TargetClass"
```

Read the file to understand the current implementation.

### 2. Design the Toggle

Check if the project has existing config management:

```bash
# Look for environment files
Glob pattern: ".env*"
Glob pattern: "config/*"
Glob pattern: "config.js"
Glob pattern: "settings.py"
```

**Toggle naming convention:**
- Format: `ENABLE_NEW_<FEATURE_NAME>` or `USE_<FEATURE>_V2`
- Default: `false` (old behavior)
- Example: `ENABLE_NEW_PAYMENT_FLOW=true`

**Add the toggle flag:**

In `.env`:
```
ENABLE_NEW_FEATURE_X=false
```

In `config.js`:
```javascript
module.exports = {
  ENABLE_NEW_FEATURE_X: process.env.ENABLE_NEW_FEATURE_X === 'true'
};
```

In `settings.py`:
```python
ENABLE_NEW_FEATURE_X = os.environ.get('ENABLE_NEW_FEATURE_X', 'false') == 'true'
```

### 3. Extract New Logic

Create a NEW helper function with the new implementation:

```javascript
// NEW: Clean implementation
function newFeatureXLogic(input) {
  // Pure, testable logic
  // No side effects where possible
  return process(input);
}
```

**Key principles:**
- Keep it pure (same input = same output)
- Make it testable in isolation
- Add JSDoc/docstring explaining behavior

### 4. Add the Guard Clause

Inject the toggle check at the TOP of the original function:

```javascript
function targetFunction(input) {
  // === SURGERY GUARD ===
  if (shouldUseNewFeatureX()) {
    try {
      return newFeatureXLogic(input);
    } catch (error) {
      logger.error('[SURGERY-FAIL] newFeatureXLogic', { error, input });
      // Fall through to old logic
    }
  }
  // === END SURGERY ===

  // Original code untouched below
  return oldImplementation(input);
}
```

**Safety rules:**
- NEW code runs first (top of function)
- Wrap in try-catch
- Log errors but NEVER re-throw
- Always fall back to old logic

### 5. Add Surgery Metadata

Add a comment block above the modified function:

```javascript
/**
 * [SURGERY] 2025-12-30
 * Feature: New payment processing flow
 * Task: #PROJ-123
 * Toggle: ENABLE_NEW_PAYMENT_FLOW
 *
 * NEW: newPaymentFlow() - Uses Stripe API v3
 * OLD: original code below - Uses Stripe API v2
 *
 * Deprecation: Remove old path by 2025-06-30 if stable
 * Monitoring: Track 'surgery_payment_flow_fail' metric
 */
function processPayment(amount) {
  // ... surgery pattern ...
}
```

### 6. Add Monitoring (Optional but Recommended)

Log the toggle state and failures:

```javascript
try {
  if (shouldUseNewFeatureX()) {
    metrics.increment('surgery_feature_x_attempt');
    return newFeatureXLogic(input);
  }
} catch (error) {
  metrics.increment('surgery_feature_x_fail');
  console.error('[SURGERY-FAIL]', error);
}
```

## Language-Specific Patterns

### JavaScript/Node.js

```javascript
// Toggle helper
function shouldUseNewFeatureX() {
  return process.env.ENABLE_NEW_FEATURE_X === 'true';
}

// Surgery (Sync)
function legacyFunction(input) {
  if (shouldUseNewFeatureX()) {
    try {
      return newFeatureXLogic(input);
    } catch (error) {
      console.error('[SURGERY-FAIL]', error);
    }
  }
  return oldLogic(input);
}

// Surgery (Async)
async function legacyFunctionAsync(input) {
  if (shouldUseNewFeatureX()) {
    try {
      return await newFeatureXLogicAsync(input);
    } catch (error) {
      console.error('[SURGERY-FAIL]', error);
    }
  }
  return await oldLogicAsync(input);
}

// Async with dynamic toggle check (e.g., from database/remote config)
async function legacyFunctionDynamicToggle(input) {
  if (await shouldUseNewFeatureXFromConfig()) {
    try {
      return await newFeatureXLogicAsync(input);
    } catch (error) {
      console.error('[SURGERY-FAIL]', error);
    }
  }
  return await oldLogicAsync(input);
}
```

### Python

```python
import os
import logging

logger = logging.getLogger(__name__)

# Toggle
def should_use_new_feature_x():
    return os.environ.get('ENABLE_NEW_FEATURE_X', 'false') == 'true'

# Surgery (Sync)
def legacy_function(input):
    if should_use_new_feature_x():
        try:
            return new_feature_x_logic(input)
        except Exception as e:
            logger.error('[SURGERY-FAIL] new_feature_x_logic', exc_info=e)
    return old_logic(input)

# Surgery (Async)
async def legacy_function_async(input):
    if should_use_new_feature_x():
        try:
            return await new_feature_x_logic_async(input)
        except Exception as e:
            logger.error('[SURGERY-FAIL] new_feature_x_logic_async', exc_info=e)
    return await old_logic_async(input)

# Async with dynamic toggle (e.g., from Redis/remote config)
async def legacy_function_dynamic_toggle(input):
    if await should_use_new_feature_x_from_config():
        try:
            return await new_feature_x_logic_async(input)
        except Exception as e:
            logger.error('[SURGERY-FAIL] new_feature_x_logic_async', exc_info=e)
    return await old_logic_async(input)
```

### TypeScript

```typescript
const ENABLE_NEW_FEATURE_X = process.env.ENABLE_NEW_FEATURE_X === 'true';

// Surgery (Sync)
function legacyFunction(input: InputType): OutputType {
  if (ENABLE_NEW_FEATURE_X) {
    try {
      return newFeatureXLogic(input);
    } catch (error) {
      console.error('[SURGERY-FAIL]', error);
    }
  }
  return oldLogic(input);
}

// Surgery (Async)
async function legacyFunctionAsync(input: InputType): Promise<OutputType> {
  if (ENABLE_NEW_FEATURE_X) {
    try {
      return await newFeatureXLogicAsync(input);
    } catch (error) {
      console.error('[SURGERY-FAIL]', error);
    }
  }
  return await oldLogicAsync(input);
}

// Async with dynamic toggle check
async function legacyFunctionDynamicToggle(input: InputType): Promise<OutputType> {
  if (await shouldUseNewFeatureXFromConfig()) {
    try {
      return await newFeatureXLogicAsync(input);
    } catch (error) {
      console.error('[SURGERY-FAIL]', error);
    }
  }
  return await oldLogicAsync(input);
}
```

### Go

```go
var enableNewFeatureX = os.Getenv("ENABLE_NEW_FEATURE_X") == "true"

func legacyFunction(input Input) Output {
    if enableNewFeatureX {
        if result, err := newFeatureXLogic(input); err == nil {
            return result
        } else {
            log.Printf("[SURGERY-FAIL] newFeatureXLogic: %v", err)
        }
    }
    return oldLogic(input)
}
```

### Java

```java
private static final boolean ENABLE_NEW_FEATURE_X =
    "true".equals(System.getenv("ENABLE_NEW_FEATURE_X"));

public Output legacyFunction(Input input) {
    if (ENABLE_NEW_FEATURE_X) {
        try {
            return newFeatureXLogic(input);
        } catch (Exception e) {
            log.error("[SURGERY-FAIL] newFeatureXLogic", e);
        }
    }
    return oldLogic(input);
}
```

### C#

```csharp
using Microsoft.Extensions.Logging;

// Toggle helper (in appsettings.json: "EnableNewFeatureX": false)
private static bool ShouldUseNewFeatureX() =>
    bool.TryParse(Environment.GetEnvironmentVariable("ENABLE_NEW_FEATURE_X"), out var enabled) && enabled;

// Or using IConfiguration
private readonly IConfiguration _config;
private bool ShouldUseNewFeatureX() => _config.GetValue<bool>("EnableNewFeatureX", false);

// Surgery
public Output LegacyFunction(Input input)
{
    if (ShouldUseNewFeatureX())
    {
        try
        {
            return NewFeatureXLogic(input);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "[SURGERY-FAIL] NewFeatureXLogic");
        }
    }
    return OldLogic(input);
}

// Async version
public async Task<Output> LegacyFunctionAsync(Input input)
{
    if (ShouldUseNewFeatureX())
    {
        try
        {
            return await NewFeatureXLogicAsync(input);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "[SURGERY-FAIL] NewFeatureXLogicAsync");
        }
    }
    return await OldLogicAsync(input);
}
```

**Configuration in `appsettings.json`:**
```json
{
  "EnableNewFeatureX": false,
  "FeatureFlags": {
    "EnableNewFeatureX": false
  }
}
```

**Or using `appsettings.Development.json`:**
```json
{
  "EnableNewFeatureX": true  // Enable locally for testing
}
```

### Angular (TypeScript + Services)

```typescript
// config.service.ts - Feature toggle management
@Injectable({ providedIn: 'root' })
export class ConfigService {
  private featureFlags = new Map<string, boolean>();

  constructor(@Inject(PLATFORM_ID) private platformId: Object) {}

  // Load from environment or API
  loadFeatureFlags(): void {
    if (isPlatformBrowser(this.platformId)) {
      this.featureFlags.set('ENABLE_NEW_FEATURE_X',
        environment.enableNewFeatureX === true
      );
    }
  }

  isFeatureEnabled(featureName: string): boolean {
    return this.featureFlags.get(featureName) ?? false;
  }
}

// component.ts - Surgical pattern in component methods
@Component({ /* ... */ })
export class PaymentComponent implements OnInit {
  constructor(private config: ConfigService, private logger: LoggerService) {}

  processPayment(amount: number): PaymentResult {
    // === SURGERY GUARD ===
    if (this.config.isFeatureEnabled('ENABLE_NEW_PAYMENT_FLOW')) {
      try {
        return this.newPaymentFlow(amount);
      } catch (error) {
        this.logger.error('[SURGERY-FAIL] newPaymentFlow', error);
        // Fall through to old logic
      }
    }
    // === END SURGERY ===

    return this.oldPaymentFlow(amount);
  }

  // NEW: Clean implementation
  private newPaymentFlow(amount: number): PaymentResult {
    return this.paymentServiceV3.process(amount);
  }

  // OLD: Original implementation
  private oldPaymentFlow(amount: number): PaymentResult {
    return this.paymentServiceV2.process(amount);
  }
}

// Async version for HTTP calls
processPaymentAsync(amount: number): Observable<PaymentResult> {
  if (this.config.isFeatureEnabled('ENABLE_NEW_PAYMENT_FLOW')) {
    return this.paymentServiceV3.process(amount).pipe(
      catchError((error) => {
        this.logger.error('[SURGERY-FAIL] newPaymentFlow', error);
        // Fall back to old logic
        return this.paymentServiceV2.process(amount);
      })
    );
  }

  return this.paymentServiceV2.process(amount);
}
```

**Configuration in `environment.ts`:**
```typescript
export const environment = {
  production: false,
  enableNewFeatureX: false  // Default to false
};
```

**Configuration in `environment.prod.ts`:**
```typescript
export const environment = {
  production: true,
  enableNewFeatureX: false  // Control rollout in production
};
```

**Angular-specific considerations:**
- Use `isPlatformBrowser` check to avoid SSR issues
- Leverage RxJS `catchError` for Observable-based surgery
- Store feature flags in a service for easy toggling
- Consider remote config services (LaunchDarkly, Firebase Remote Config) for runtime toggles

## Rollback Procedure

If new code causes issues:

1. **Immediate rollback:** Set toggle to `false`
   ```bash
   # .env
   ENABLE_NEW_FEATURE_X=false
   ```

2. **No redeploy needed** - toggle takes effect on restart/reload

3. **Investigate logs** for `[SURGERY-FAIL]` entries

4. **Fix new logic** and increment toggle version
   ```bash
   ENABLE_NEW_FEATURE_X_V2=false  # Fixed version, disabled by default
   ```

## Cleanup and Deprecation

After the new code proves stable (typically 2-4 weeks):

1. **Remove the old code path**
2. **Remove the toggle check**
3. **Update function to call new logic directly**
4. **Remove the helper function** (inline if simple)

```javascript
// BEFORE: Surgery pattern
function processPayment(input) {
  if (shouldUseNewFlow()) {
    try { return newFlow(input); } catch (e) { /* log */ }
  }
  return oldFlow(input); // Remove this
}

// AFTER: Clean implementation
function processPayment(input) {
  return newFlow(input); // Direct call
}
```

Update surgery comment to document completion:
```javascript
/**
 * [SURGERY-COMPLETE] 2025-12-30 -> 2025-01-15
 * Feature: New payment flow
 * Status: Stable. Old path removed.
 * Migration: PROJ-123
 */
function processPayment(input) {
  return newFlow(input);
}
```

## When to Use This Skill

Trigger for these user requests:
- "Add a feature flag to this function"
- "I want to A/B test this new logic"
- "Safely refactor this critical function"
- "Add a kill switch to this feature"
- "I need to deploy this but can't afford downtime"
- "Gradually roll out this change"

Do NOT use for:
- Simple variable renaming
- Adding comments or documentation
- Non-critical code paths
- Greenfield projects (no legacy code)

## Anti-Patterns to Avoid

**DON'T:** Modify the old code path
- Keep original implementation untouched

**DON'T:** Re-throw exceptions in the catch block
- Let it fall through to old logic silently

**DON'T:** Skip the toggle
- Hardcoding `true` defeats the safety mechanism

**DON'T:** Forget logging
- Without `[SURGERY-FAIL]` logs, debugging is impossible

**DON'T:** Make the new function depend on the old code's state
- Keep new logic independent and pure
