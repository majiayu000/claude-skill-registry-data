---
name: verdict-flags
description: a skill that contains all the best practices for using Verdict Flags in shopify codebases. It should be uses whenever the agent is creating, updating or removing flags
---

# Shopify Verdict Flags Testing Skill

Help manage Verdict feature flags in Shopify tests using proper test helpers instead of stubs.

## When to Use

Use this skill when:
- Replacing `Verdict::Flag.stubs` calls (forbidden by RuboCop)
- Testing features controlled by Verdict flags
- Creating new flags in the Experiments Dashboard
- Setting up tests that need flag configuration
- Testing both enabled and disabled flag states

## Core Principles

1. **NEVER stub Verdict::Flag** - RuboCop cop enforces this (Cops/VerdictStubbing)
2. **Always use test helpers** - Shopify provides dedicated helpers for flag management
3. **Test both states** - Use patterns to test enabled AND disabled behavior
4. **Default to enabled** - Usually enable flags 100% in setup to test new behavior
5. **Subject type matters** - Different helpers for shop, api_client, organization, etc.

## Flag Helper Methods

### Shop Flags (Most Common)

```ruby
# Enable/disable for ALL shops (100% rollout in tests)
enable_shop_flag("f_my_flag")
disable_shop_flag("f_my_flag")

# Enable/disable for SPECIFIC shop
enable_shop_flag_for("f_my_flag", shop)
disable_shop_flag_for("f_my_flag", shop)

# Enable with percentage rollout (test percentage-based rollouts)
enable_shop_flag_with_percentage("f_my_flag", 50)

# Block syntax for temporary enable
with_shop_flag("f_my_flag") do
  # Code here runs with flag enabled
end
```

### API Client Flags

```ruby
# Enable/disable for all API clients
enable_api_client_flag("f_my_flag")
disable_api_client_flag("f_my_flag")

# Enable/disable for specific API client
enable_api_client_flag_for("f_my_flag", api_client)
disable_api_client_flag_for("f_my_flag", api_client)

# Block syntax
with_api_client_flag("f_my_flag") do
  # Code here
end

with_api_client_flag_for("f_my_flag", api_client) do
  # Code here
end
```

### Other Subject Types

```ruby
# Organization flags
enable_organization_flag("f_my_flag")
enable_organization_flag_for("f_my_flag", organization_id)

# Generic non-PII flags (sessions, etc.)
enable_generic_non_pii_flag("f_my_flag")
enable_generic_non_pii_flag_for("f_my_flag", subject_id)

# Checkout flags
enable_checkout_flag_for("f_my_flag", checkout_subject)
disable_checkout_flag_for("f_my_flag", checkout_subject)
```

### Generic Helpers (When Subject Type Varies)

```ruby
# Enable/disable with explicit subject type
enable_flag("f_my_flag", subject_type: "shop")
disable_flag("f_my_flag", subject_type: "api_client")

# Enable/disable for specific subjects
enable_flag_for("f_my_flag", subject_ids: [123, 456], subject_type: "shop")
disable_flag_for("f_my_flag", subject_ids: [123, 456], subject_type: "shop")

# Configure flag with custom options
config_flag("f_my_flag", subject_type: "shop", percent: 50)
```

## Testing Patterns

### Pattern 1: Explicit Enable/Disable Tests (Recommended for Simple Cases)

Best for testing specific behavior in each state.

```ruby
class MyTest < ActiveSupport::TestCase
  include Verdict::FlagTestHelper  # or include Flags::TestHelper

  setup do
    @shop = create(:shop)
    enable_shop_flag("f_my_feature")  # Default state for most tests
  end

  test "feature works when flag is enabled" do
    result = MyService.call(@shop)
    assert_equal(expected_new_behavior, result)
  end

  test "feature falls back when flag is disabled" do
    disable_shop_flag("f_my_feature")

    result = MyService.call(@shop)
    assert_equal(expected_old_behavior, result)
  end
end
```

### Pattern 2: Auto-Generate Tests with `run_all_with_flag` (Class-Level)

Best for running ALL tests in a class with different flag combinations.

```ruby
class MyTest < ActiveSupport::TestCase
  include Flags::ToggleHelper

  # Runs ALL tests with both flag states (ON and OFF)
  run_all_with_flag("f_my_flag", state: :both, subject_type: "shop")

  # Can add multiple flags - creates cartesian product
  # (f1:ON,f2:ON), (f1:ON,f2:OFF), (f1:OFF,f2:ON)
  # Note: All flags OFF is skipped by default
  run_all_with_flag("f_another_flag", state: :both, subject_type: "shop")

  test "my test" do
    # This test will run multiple times with different flag combinations
    # Check current state with: flag_enabled?("f_my_flag")

    if flag_enabled?("f_my_flag")
      assert_new_behavior
    else
      assert_old_behavior
    end
  end
end
```

### Pattern 3: Auto-Generate Tests with `flags:` Tag (Test-Level)

Best for running specific tests with flag variations.

```ruby
class MyTest < ActiveSupport::TestCase
  include Flags::ToggleHelper

  # Single flag - runs twice (ON and OFF)
  test "my test", flags: "f_my_flag" do
    # Test code
  end

  # Multiple flags - runs with all combinations
  test "my test", flags: ["f_flag1", "f_flag2"] do
    # Test code
  end

  # With explicit subject types
  test "my test", flags: [
    { name: "f_flag1", subject_type: "shop" },
    { name: "f_flag2", subject_type: "api_client" }
  ] do
    # Test code
  end

  # Check current state in test
  test "my test", flags: "f_my_flag" do
    if flag_enabled?("f_my_flag")
      assert_new_behavior
    else
      assert_old_behavior
    end
  end
end
```

### Pattern 4: Block Syntax for Inline Comparison

Best for comparing behavior within a single test.

```ruby
test "feature behaves differently with flag" do
  # Test without flag
  result1 = MyService.call(@shop)
  assert_equal(old_behavior, result1)

  # Test with flag
  with_shop_flag("f_my_flag") do
    result2 = MyService.call(@shop)
    assert_equal(new_behavior, result2)
  end
end
```

## Flag Creation Workflow

When you encounter a missing flag:

### Step 1: Check if Flag Exists

```ruby
# Use MCP tool to check flag status
mcp__experiments-mcp__flag_status(flag_handle: "f_my_flag")
```

### Step 2: Create Flag if Missing

```ruby
# Use MCP tool to create the flag
mcp__experiments-mcp__flag_create(
  handle: "f_my_flag",
  title: "My Feature Flag",
  description: "Enables my new feature",
  subject_type: "shop"  # or api_client, organization, etc.
)
```

### Step 3: Sync Flags

```bash
# Wait 20 seconds for flag to propagate
sleep 20

# Run dev up to download new flag configuration
/opt/dev/bin/dev up
```

### Step 4: Verify Tests Pass

```bash
/opt/dev/bin/dev test path/to/test_file.rb
```

## Flag Naming Conventions

- **MUST start with `f_`** (enforced by Experiments Dashboard)
- Use **snake_case**: `f_my_feature_name`
- Be **descriptive**: `f_enable_shop_channel_markets` not `f_ecm`
- Examples from codebase:
  - `f_channels_skip_destroy_publishables`
  - `f_customer_entity_draft_order_customer_repository`
  - `f_use_core_trial_extension_verifier`

## Subject Types Reference

Common subject types:
- `shop` - Most common, for shop-level features
- `api_client` - For app/API client features
- `organization` - For organization-level features
- `checkout` - For checkout process features
- `generic_non_pii` - For non-PII identifiers (sessions, etc.)
- `email` - For Shopify employee features
- `identity_user` - For identity/user features

## Common Errors & Solutions

### Error: "Validation failed: Feature is invalid"

**Cause:** Flag doesn't exist in Experiments Dashboard or flags.yml

**Solution:**
1. Use MCP tool to check if flag exists: `flag_status`
2. If not found, create it: `flag_create`
3. Wait 20 seconds and run `dev up`
4. Retry tests

### Error: Tests failing after replacing stubs

**Cause:** Using wrong helper method (global vs per-subject)

**Solution:**
- If implementation uses `subject: @shop` → use `enable_shop_flag()` (global)
- If implementation uses `subject_id: @shop.id` → can use either global or `enable_shop_flag_for()`
- Check implementation to see how flag is checked

### Error: "Handle must start with 'f_'"

**Cause:** Flag handle doesn't follow naming convention

**Solution:** Rename flag to start with `f_` prefix

### Error: RuboCop violation "Do not stub Verdict::Flag"

**Cause:** Using `Verdict::Flag.stubs()` instead of test helpers

**Solution:** Replace stubs with appropriate helper:
```ruby
# BAD
Verdict::Flag.stubs(:enabled?).with(handle: "f_my_flag", subject: @shop).returns(true)

# GOOD
enable_shop_flag("f_my_flag")
```

## Quick Reference Examples

### Replace Simple Stub

```ruby
# Before
setup do
  @shop = create(:shop)
  Verdict::Flag.stubs(:enabled?).with(handle: "f_my_flag", subject: @shop).returns(true)
  Verdict::Flag.stubs(:disabled?).with(handle: "f_my_flag", subject: @shop).returns(false)
end

# After
setup do
  @shop = create(:shop)
  enable_shop_flag("f_my_flag")
end
```

### Test Both States

```ruby
# Before
test "returns true when flag is disabled" do
  Verdict::Flag.stubs(:disabled?).with(handle: "f_my_flag", subject: @shop).returns(true)
  assert_predicate(service, :disabled?)
end

# After
test "returns true when flag is disabled" do
  disable_shop_flag("f_my_flag")
  assert_predicate(service, :disabled?)
end
```

### Per-Subject Enable

```ruby
# Before
setup do
  @shop1 = create(:shop)
  @shop2 = create(:shop)
  Verdict::Flag.stubs(:enabled?).with(handle: "f_my_flag", subject: @shop1).returns(true)
  Verdict::Flag.stubs(:enabled?).with(handle: "f_my_flag", subject: @shop2).returns(false)
end

# After
setup do
  @shop1 = create(:shop)
  @shop2 = create(:shop)
  enable_shop_flag_for("f_my_flag", @shop1)
  disable_shop_flag_for("f_my_flag", @shop2)
end
```

## Additional Resources

**Key Files:**
- Test Helpers: `components/platform/essentials/app/utils/flags/test_helper.rb`
- Toggle Helper: `components/platform/essentials/app/utils/flags/toggle_helper.rb`
- Flag Config: `db/data/verdict/flags.yml`

**RuboCop Cops:**
- `Cops/VerdictStubbing` - Prevents stubbing Verdict::Flag
- `Cops/VerdictFlagSubject` - Enforces subject_id over subject

**Commands:**
```bash
# Lint flag configuration
bundle exec rake verdict:lint_flags

# Generate new flag
bin/rails g flag f_my_new_flag

# Sync flags from Experiments Dashboard
/opt/dev/bin/dev up
```
