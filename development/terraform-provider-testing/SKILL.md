---
name: terraform-provider-testing
description: Comprehensive test-driven development for Terraform providers with iterative co-development of tests, generators, and schemas. NEVER skip development or refactoring - always fix root causes in generators, schemas, or test code. Only skip resources requiring external credentials (AWS/Azure/GCP) or premium licensing. Uses terraform-plugin-testing SDK with modern assertion patterns.
tools: Read, Write, Edit, Bash, Glob, Grep
---

# Terraform Provider Testing Skill

**Comprehensive test-driven development** for Terraform providers emphasizing iterative co-development of tests, generators, and schemas. This skill drives the development of production-ready provider code through systematic testing and root cause analysis.

---

## Core Philosophy: Never Skip, Always Fix

### The Co-Development Mindset

Tests, generators, and schemas are **interdependent systems** that evolve together. When tests fail, the response is **ALWAYS** to fix the root cause - never to skip, disable, or work around.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     CO-DEVELOPMENT TRIANGLE                                  │
│                                                                              │
│                           ┌─────────┐                                        │
│                           │  TESTS  │                                        │
│                           └────┬────┘                                        │
│                                │                                             │
│              ┌─────────────────┼─────────────────┐                           │
│              │                 │                 │                           │
│              ▼                 ▼                 ▼                           │
│       ┌──────────┐      ┌──────────┐      ┌──────────┐                      │
│       │GENERATORS│◄────►│ SCHEMAS  │◄────►│ RESOURCES│                      │
│       └──────────┘      └──────────┘      └──────────┘                      │
│                                                                              │
│   Tests drive → Generator fixes → Schema corrections → Resource updates     │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Never Skip Rules (CRITICAL)

**ALWAYS develop and fix** unless ONE of these conditions applies:

| Skip Condition | Example | Action |
|----------------|---------|--------|
| External cloud credentials required | AWS VPC Site needs `AWS_ACCESS_KEY_ID` | `t.Skip("requires AWS credentials")` |
| Premium/enterprise licensing required | Bot defense needs advanced license | `t.Skip("requires premium licensing")` |
| Third-party service account needed | External OIDC provider | `t.Skip("requires external service account")` |

**NEVER skip for these reasons** - fix them instead:

| Invalid Skip Reason | Correct Action |
|--------------------|----------------|
| "Schema attribute missing" | Fix generator, regenerate |
| "State drift on nested blocks" | Fix generator's Read/Schema handling |
| "Import produces diff" | Fix ImportState function in generator |
| "API returns unexpected format" | Fix client types or resource parsing |
| "Test is too complex" | Break into smaller tests, still implement |
| "Generator doesn't support this" | Enhance generator to support it |

### Development Priority Order

When a test fails, investigate and fix in this order:

```
1. GENERATOR ISSUE?
   │ Symptoms: Same failure across ALL resources of similar type
   │ Fix: tools/generate-all-schemas.go → go generate ./...
   │
2. SCHEMA ISSUE?
   │ Symptoms: Attribute handling, type mismatches, nested block problems
   │ Fix: Generator's schema generation logic → regenerate
   │
3. RESOURCE IMPLEMENTATION ISSUE?
   │ Symptoms: Single resource fails, API-specific parsing
   │ Fix: The specific resource's CRUD methods
   │
4. TEST ISSUE?
   │ Symptoms: Wrong assertions, incorrect config, test logic error
   │ Fix: Test code only AFTER ruling out 1-3
```

---

## Coding Standards (MANDATORY)

### Go Indentation: Tabs (gofmt Standard)

**CRITICAL**: All Go source code MUST use **tabs for indentation** - this is enforced by `gofmt`.

| File Type | Indentation | Standard |
|-----------|-------------|----------|
| Go source files (`.go`) | Tabs | `gofmt` enforced |
| Embedded Terraform/HCL in heredocs | 2 spaces | Terraform convention |

**Why tabs for Go:**
- `gofmt` is the canonical Go formatter and uses tabs
- All Go code MUST pass `gofmt` before commit
- This is non-negotiable - it's the Go community standard
- CI/CD will fail if code doesn't match `gofmt` output

### Go Test File Formatting

```go
// ✅ CORRECT: Tabs for Go code indentation (gofmt standard)
func TestAccExampleResource_basic(t *testing.T) {
	t.Parallel()

	rName := acctest.RandomWithPrefix("tf-acc-test")
	resourceName := "f5xc_example.test"

	resource.ParallelTest(t, resource.TestCase{
		PreCheck:                 func() { testAccPreCheck(t) },
		ProtoV6ProviderFactories: testAccProtoV6ProviderFactories,
		Steps: []resource.TestStep{
			{
				Config: testAccExampleConfig_basic(rName),
			},
		},
	})
}
```

### Embedded Terraform Configuration Formatting

Terraform/HCL inside Go heredocs uses **2 spaces** (Terraform convention):

```go
// ✅ CORRECT: Tabs for Go, 2 spaces for embedded HCL
func testAccExampleConfig_basic(rName string) string {
	return fmt.Sprintf(`
resource "f5xc_namespace" "test" {
  name = %[1]q
}

resource "f5xc_example" "test" {
  name      = %[1]q
  namespace = f5xc_namespace.test.name

  nested_block {
    attribute = "value"
  }
}
`, rName)
}
```

**Key distinction:**
- The `func` and `return fmt.Sprintf` lines use **tabs** (Go code)
- The HCL content inside the backticks uses **2 spaces** (Terraform convention)

### Formatting Verification

Always run `gofmt` before committing:

```bash
# Format all Go files in place
gofmt -w .

# Check formatting without modifying (CI mode)
gofmt -d . | grep -q . && echo "Formatting needed" || echo "OK"

# Format with goimports (also organizes imports)
goimports -w .
```

### Editor Configuration

Configure your editor for Go's tab standard:

**VS Code settings:**
```json
{
  "[go]": {
    "editor.insertSpaces": false,
    "editor.tabSize": 4,
    "editor.formatOnSave": true
  }
}
```

**Vim settings:**
```vim
" For Go files - use tabs (gofmt standard)
autocmd FileType go setlocal noexpandtab tabstop=4 shiftwidth=4
```

---

## Part 1: Iterative Development Workflow

### The Test-Fix-Verify Cycle

Every test development follows this iterative pattern:

```bash
# Phase 1: Write Initial Test
vim internal/provider/example_resource_test.go

# Phase 2: Run Test (expect failures)
F5XC_API_URL="https://tenant.console.ves.volterra.io" \
F5XC_P12_FILE="/path/to/cert.p12" \
F5XC_P12_PASSWORD="password" \  # pragma: allowlist secret
TF_ACC=1 go test -v -timeout 15m \
  -run TestAccExampleResource_basic ./internal/provider/...

# Phase 3: Analyze Failure - Determine Root Cause
# Ask: Is this a GENERATOR issue affecting all resources?
#      Is this a SCHEMA issue with attribute handling?
#      Is this a RESOURCE issue with this specific API?
#      Is this a TEST issue with my assertions?

# Phase 4: Fix at the Appropriate Level
# If generator: vim tools/generate-all-schemas.go && go generate ./...
# If schema: Fix in generator, regenerate
# If resource: Fix specific resource implementation
# If test: Fix test assertions/config

# Phase 5: Re-run and Verify
TF_ACC=1 go test -v -timeout 15m \
  -run TestAccExampleResource_basic ./internal/provider/...

# REPEAT until test passes - NEVER skip
```

### Failure Analysis Decision Tree

```
Test Failed
│
├── Error mentions "attribute not found in schema"?
│   └── FIX: Generator schema generation → regenerate ALL resources
│
├── Error shows state drift on nested blocks?
│   └── FIX: Generator's Read method handling of nested structures
│
├── ImportStateVerify shows diff?
│   └── FIX: Generator's ImportState function
│
├── API returns 400/422 with field error?
│   └── FIX: Generator's Create/Update request building
│
├── Computed field not populated after Read?
│   └── FIX: Generator's Read response → state mapping
│
├── Same error pattern across multiple resource types?
│   └── FIX: Generator (systemic issue) → regenerate
│
├── Error only in this specific resource?
│   └── FIX: Resource implementation OR client types
│
└── Assertion doesn't match expected value?
    └── INVESTIGATE: Is expected value correct? Is resource behavior correct?
        ├── Resource behavior wrong → Fix resource
        └── Assertion wrong → Fix test
```

### Generator-Test Co-Development Examples

**Example 1: Nested Block State Drift**

```
TEST FAILURE: inconsistent result after apply
  - default_route_pools.0.pool.namespace: "" => "test-ns"

ANALYSIS: Generator's Read method doesn't populate nested blocks correctly

FIX LOCATION: tools/generate-all-schemas.go
FIX TYPE: Update nested block flattening logic

STEPS:
1. Identify pattern in generator for nested block handling
2. Fix the flattening/expansion logic
3. go generate ./...
4. Re-run test
5. Verify ALL similar resources now work
```

**Example 2: Missing Schema Attribute**

```
TEST FAILURE: attribute "labels" not found in schema

ANALYSIS: Generator doesn't include labels attribute from OpenAPI spec

FIX LOCATION: tools/generate-all-schemas.go
FIX TYPE: Add labels field to schema generation

STEPS:
1. Check OpenAPI spec confirms labels exists
2. Update generator to include labels in schema
3. go generate ./...
4. Re-run test
5. Verify all resources with labels now have the attribute
```

**Example 3: Import State Incomplete**

```
TEST FAILURE: ImportStateVerify found differences:
  - description: "test" => ""

ANALYSIS: ImportState doesn't set all attributes from API response

FIX LOCATION: Generator's ImportState template or Read method
FIX TYPE: Ensure Read populates all importable attributes

STEPS:
1. Check API response includes description
2. Fix generator's Read to map description to state
3. go generate ./...
4. Re-run import test
5. Verify import now preserves all attributes
```

---

## Part 2: Comprehensive Test Structure

### TestCase Architecture

```go
func TestAccExampleResource_basic(t *testing.T) {
    t.Parallel()

    rName := acctest.RandomWithPrefix("tf-acc-test")
    resourceName := "f5xc_example.test"

    resource.ParallelTest(t, resource.TestCase{
        PreCheck:                 func() { testAccPreCheck(t) },
        ProtoV6ProviderFactories: testAccProtoV6ProviderFactories,
        CheckDestroy:             testAccCheckExampleDestroy,
        Steps: []resource.TestStep{
            // Step 1: Create and verify
            {
                Config: testAccExampleConfig_basic(rName),
                ConfigPlanChecks: resource.ConfigPlanChecks{
                    PreApply: []plancheck.PlanCheck{
                        plancheck.ExpectResourceAction(resourceName,
                            plancheck.ResourceActionCreate),
                    },
                },
                ConfigStateChecks: []statecheck.StateCheck{
                    statecheck.ExpectKnownValue(resourceName,
                        tfjsonpath.New("name"), knownvalue.StringExact(rName)),
                },
            },
            // Step 2: Import and verify state roundtrip
            {
                ResourceName:      resourceName,
                ImportState:       true,
                ImportStateVerify: true,
            },
        },
    })
}
```

### Comprehensive Test Coverage Requirements

Every testable resource MUST have:

| Test Type | Purpose | Skip Only If |
|-----------|---------|--------------|
| `_basic` | Create, Read, basic attributes | External credentials/licensing |
| `_update` | Modify mutable attributes | External credentials/licensing |
| `_import` | Import existing resource | External credentials/licensing |
| `_disappears` | Handle external deletion | External credentials/licensing |
| Data source test | Verify data source reads resource | External credentials/licensing |

```go
// REQUIRED test structure for each resource
func TestAccExampleResource_basic(t *testing.T) { ... }
func TestAccExampleResource_update(t *testing.T) { ... }
func TestAccExampleResource_disappears(t *testing.T) { ... }
func TestAccExampleDataSource_basic(t *testing.T) { ... }
```

---

## Part 3: Modern Assertion Framework

### ConfigPlanChecks (Plan-Time Validation)

Validate Terraform plan **before** resources are applied:

```go
{
    Config: testAccConfig,
    ConfigPlanChecks: resource.ConfigPlanChecks{
        PreApply: []plancheck.PlanCheck{
            // Verify expected action
            plancheck.ExpectResourceAction("f5xc_namespace.test",
                plancheck.ResourceActionCreate),

            // Verify known values in plan
            plancheck.ExpectKnownValue("f5xc_namespace.test",
                tfjsonpath.New("name"),
                knownvalue.StringExact("test-ns")),

            // Verify unknown values (computed)
            plancheck.ExpectUnknownValue("f5xc_namespace.test",
                tfjsonpath.New("id")),
        },
        PostApply: []plancheck.PlanCheck{
            // After apply, plan should be empty (no drift)
            plancheck.ExpectEmptyPlan(),
        },
    },
}
```

### ConfigStateChecks (State Validation)

Validate Terraform state **after** resources are applied:

```go
{
    Config: testAccConfig,
    ConfigStateChecks: []statecheck.StateCheck{
        // Verify exact string value
        statecheck.ExpectKnownValue("f5xc_namespace.test",
            tfjsonpath.New("name"),
            knownvalue.StringExact("test-ns")),

        // Verify boolean
        statecheck.ExpectKnownValue("f5xc_app_firewall.test",
            tfjsonpath.New("blocking"),
            knownvalue.Bool(true)),

        // Verify list size
        statecheck.ExpectKnownValue("f5xc_http_lb.test",
            tfjsonpath.New("domains"),
            knownvalue.ListSizeExact(2)),

        // Verify nested object
        statecheck.ExpectKnownValue("f5xc_http_lb.test",
            tfjsonpath.New("default_route_pools").AtSliceIndex(0),
            knownvalue.ObjectPartial(map[string]knownvalue.Check{
                "weight":   knownvalue.Int64Exact(1),
                "priority": knownvalue.Int64Exact(1),
            })),
    },
}
```

### knownvalue Reference

| Check Type | Usage | Example |
|------------|-------|---------|
| `StringExact` | Exact string match | `knownvalue.StringExact("value")` |
| `StringRegexp` | Regex match | `knownvalue.StringRegexp(regexp.MustCompile(`^tf-`))` |
| `Bool` | Boolean value | `knownvalue.Bool(true)` |
| `Int64Exact` | Exact integer | `knownvalue.Int64Exact(42)` |
| `ListExact` | Exact list | `knownvalue.ListExact([]knownvalue.Check{...})` |
| `ListSizeExact` | List length | `knownvalue.ListSizeExact(3)` |
| `ListPartial` | Partial list match | `knownvalue.ListPartial(map[int]knownvalue.Check{0: ...})` |
| `ObjectExact` | Exact object | `knownvalue.ObjectExact(map[string]knownvalue.Check{...})` |
| `ObjectPartial` | Partial object | `knownvalue.ObjectPartial(map[string]knownvalue.Check{...})` |
| `Null` | Null value | `knownvalue.Null()` |
| `NotNull` | Not null | `knownvalue.NotNull()` |

### tfjsonpath Navigation

```go
// Simple attribute
tfjsonpath.New("name")

// Nested attribute
tfjsonpath.New("metadata").AtMapKey("labels")

// List index
tfjsonpath.New("domains").AtSliceIndex(0)

// Complex nested path
tfjsonpath.New("spec").AtMapKey("routes").AtSliceIndex(0).AtMapKey("match")
```

---

## Part 4: Namespace Requirements (CRITICAL)

### Always Use Custom Namespaces

**RULE**: Create a custom test namespace unless the API spec EXPLICITLY requires `system`, `default`, or `shared`.

```go
// ✅ CORRECT: Custom namespace
func testAccExampleConfig_basic(rName string) string {
    return fmt.Sprintf(`
resource "f5xc_namespace" "test" {
  name = %[1]q
}

resource "f5xc_example" "test" {
  name      = %[1]q
  namespace = f5xc_namespace.test.name
}
`, rName)
}

// ❌ WRONG: Using system namespace without spec requirement
func testAccExampleConfig_wrong(name string) string {
    return fmt.Sprintf(`
resource "f5xc_example" "test" {
  name      = %[1]q
  namespace = "system"  // NEVER unless spec requires it
}
`, name)
}
```

### Namespace Decision Tree

```
Does the OpenAPI spec require a specific namespace?
├── YES: system/default/shared required
│   ├── Document WHY in test comments with spec reference
│   └── Use the required namespace
└── NO: Custom namespace allowed
    └── ALWAYS create f5xc_namespace.test and reference it
```

---

## Part 5: Resource Testing Patterns

### Complete CRUD Test

```go
func TestAccExampleResource_basic(t *testing.T) {
    t.Parallel()

    rName := acctest.RandomWithPrefix("tf-acc-test")
    resourceName := "f5xc_example.test"

    resource.ParallelTest(t, resource.TestCase{
        PreCheck:                 func() { testAccPreCheck(t) },
        ProtoV6ProviderFactories: testAccProtoV6ProviderFactories,
        CheckDestroy:             testAccCheckExampleDestroy,
        Steps: []resource.TestStep{
            // Create
            {
                Config: testAccExampleConfig_basic(rName),
                ConfigPlanChecks: resource.ConfigPlanChecks{
                    PreApply: []plancheck.PlanCheck{
                        plancheck.ExpectResourceAction(resourceName,
                            plancheck.ResourceActionCreate),
                    },
                },
                ConfigStateChecks: []statecheck.StateCheck{
                    statecheck.ExpectKnownValue(resourceName,
                        tfjsonpath.New("name"), knownvalue.StringExact(rName)),
                },
            },
            // Update
            {
                Config: testAccExampleConfig_updated(rName),
                ConfigPlanChecks: resource.ConfigPlanChecks{
                    PreApply: []plancheck.PlanCheck{
                        plancheck.ExpectResourceAction(resourceName,
                            plancheck.ResourceActionUpdate),
                    },
                },
                ConfigStateChecks: []statecheck.StateCheck{
                    statecheck.ExpectKnownValue(resourceName,
                        tfjsonpath.New("description"),
                        knownvalue.StringExact("updated")),
                },
            },
            // Import
            {
                ResourceName:      resourceName,
                ImportState:       true,
                ImportStateVerify: true,
            },
        },
    })
}
```

### CheckDestroy Implementation

```go
func testAccCheckExampleDestroy(s *terraform.State) error {
    client := testAccProvider.Meta().(*client.Client)

    for _, rs := range s.RootModule().Resources {
        if rs.Type != "f5xc_example" {
            continue
        }

        namespace := rs.Primary.Attributes["namespace"]
        name := rs.Primary.Attributes["name"]

        _, err := client.GetExample(context.Background(), namespace, name)
        if err == nil {
            return fmt.Errorf("f5xc_example %s/%s still exists", namespace, name)
        }

        if !client.IsNotFoundError(err) {
            return fmt.Errorf("error checking f5xc_example %s/%s: %w",
                namespace, name, err)
        }
    }

    return nil
}
```

### Import with Composite ID

```go
{
    ResourceName:      resourceName,
    ImportState:       true,
    ImportStateVerify: true,
    ImportStateIdFunc: func(s *terraform.State) (string, error) {
        rs, ok := s.RootModule().Resources[resourceName]
        if !ok {
            return "", fmt.Errorf("resource not found: %s", resourceName)
        }
        return fmt.Sprintf("%s/%s",
            rs.Primary.Attributes["namespace"],
            rs.Primary.Attributes["name"]), nil
    },
}
```

---

## Part 6: Data Source Testing

### Data Source Test Pattern

```go
func TestAccExampleDataSource_basic(t *testing.T) {
    t.Parallel()

    rName := acctest.RandomWithPrefix("tf-acc-test")
    resourceName := "f5xc_example.test"
    dataSourceName := "data.f5xc_example.test"

    resource.ParallelTest(t, resource.TestCase{
        PreCheck:                 func() { testAccPreCheck(t) },
        ProtoV6ProviderFactories: testAccProtoV6ProviderFactories,
        Steps: []resource.TestStep{
            {
                Config: testAccExampleDataSourceConfig(rName),
                Check: resource.ComposeAggregateTestCheckFunc(
                    // Compare data source to resource
                    resource.TestCheckResourceAttrPair(
                        dataSourceName, "name",
                        resourceName, "name"),
                    resource.TestCheckResourceAttrPair(
                        dataSourceName, "id",
                        resourceName, "id"),
                    resource.TestCheckResourceAttrPair(
                        dataSourceName, "namespace",
                        resourceName, "namespace"),
                ),
            },
        },
    })
}

func testAccExampleDataSourceConfig(rName string) string {
    return fmt.Sprintf(`
resource "f5xc_namespace" "test" {
  name = %[1]q
}

resource "f5xc_example" "test" {
  name      = %[1]q
  namespace = f5xc_namespace.test.name
}

data "f5xc_example" "test" {
  name      = f5xc_example.test.name
  namespace = f5xc_example.test.namespace
}
`, rName)
}
```

---

## Part 7: Common Failures and Fixes

### Failure Resolution Matrix

| Failure | Root Cause | Fix Location | Fix Action |
|---------|------------|--------------|------------|
| `attribute not found in schema` | Generator schema incomplete | Generator | Add attribute to schema generation |
| `planned value does not match` | Computed attribute not set | Generator Read | Map API response to state |
| `inconsistent result after apply` | Read not populating state | Generator Read | Fix response → state mapping |
| `import produces diff` | ImportState incomplete | Generator ImportState | Ensure all attributes set |
| `CheckDestroy failed` | Delete not working | Resource Delete | Fix delete API call |
| `namespace not found` | Using system namespace | Test config | Use custom namespace |
| `permission denied` | Wrong namespace | Test config | Check namespace permissions |
| `ExpectResourceAction failed` | Wrong action detected | Resource/Test | Check ForceNew attributes |
| State drift on nested blocks | Flattening logic wrong | Generator | Fix nested block handling |
| Boolean always false | Type conversion issue | Generator Schema | Fix bool type handling |

### Systematic Debugging Approach

```bash
# Step 1: Enable debug logging
TF_LOG=DEBUG TF_ACC=1 go test -v -timeout 15m \
  -run TestAccExampleResource_basic ./internal/provider/... 2>&1 | tee test.log

# Step 2: Find the API request/response
grep -A 20 "HTTP Request" test.log
grep -A 50 "HTTP Response" test.log

# Step 3: Compare API response to state
# Look for fields in response not making it to state
# Look for type mismatches (string vs int, etc.)

# Step 4: Identify fix location
# If API has data but state doesn't → Generator Read method
# If state has data but plan shows change → Generator Schema/Defaults
# If API returns error → Generator Create/Update request building
```

---

## Part 8: Test Eligibility

### Testable Resources (ALWAYS develop tests)

| Category | Examples | Action |
|----------|----------|--------|
| Core resources | namespace, healthcheck, origin_pool | Full test suite |
| Security policies | app_firewall, service_policy, rate_limiter | Full test suite |
| Load balancers | http_loadbalancer, tcp_loadbalancer | Full test suite |
| Network config | virtual_network, network_policy | Full test suite |
| DNS resources | dns_zone, dns_domain | Full test suite |
| Configuration objects | Any policy, rule, or config resource | Full test suite |

### Skip-Eligible Resources (document reason)

| Category | Examples | Skip Reason |
|----------|----------|-------------|
| Cloud sites | aws_vpc_site, azure_vnet_site, gcp_vpc_site | Requires cloud credentials |
| Cloud integrations | cloud_credentials (AWS/Azure/GCP type) | Requires cloud credentials |
| Premium features | bot_defense*, advanced_* | Requires premium licensing |
| Third-party | External OIDC, external integrations | Requires external accounts |

```go
// Proper skip documentation
func TestAccAWSVPCSite_basic(t *testing.T) {
    t.Skip("Skipping: requires AWS credentials (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)")
}

func TestAccBotDefenseAdvanced_basic(t *testing.T) {
    t.Skip("Skipping: requires F5 XC premium/enterprise licensing")
}
```

---

## Part 9: Running Tests

### Environment Setup

```bash
# Required for ALL acceptance tests
export F5XC_P12_FILE="/path/to/api-certificate.p12"
export F5XC_P12_PASSWORD="your-password"  # pragma: allowlist secret
export F5XC_API_URL="https://tenant.console.ves.volterra.io"
export TF_ACC=1
```

### Test Execution Commands

```bash
# Single test
go test -v -timeout 15m -run=TestAccNamespaceResource_basic ./internal/provider/...

# All tests for a resource
go test -v -timeout 30m -run=TestAccNamespace ./internal/provider/...

# With debug logging
TF_LOG=DEBUG go test -v -timeout 15m -run=TestAccNamespaceResource_basic ./internal/provider/...

# With parallel limit
go test -v -timeout 30m -parallel=4 ./internal/provider/...

# Multiple specific tests
go test -v -timeout 30m -run="TestAccNamespaceResource_basic|TestAccHealthcheckResource_basic" ./internal/provider/...
```

---

## Part 10: Checklist for New Tests

### Pre-Development Checklist

- [ ] Resource is testable (no external credentials/premium licensing required)
- [ ] OpenAPI spec reviewed for namespace requirements
- [ ] Generator supports all required attributes for this resource type
- [ ] Client types exist for API interactions

### Test Implementation Checklist

- [ ] Create test with **custom namespace** (unless spec requires otherwise)
- [ ] Use **ConfigPlanChecks** for plan assertions
- [ ] Use **ConfigStateChecks** for state assertions
- [ ] Add import test with proper ImportStateIdFunc
- [ ] Implement CheckDestroy
- [ ] Enable parallel execution with `t.Parallel()`
- [ ] Data source test if data source exists

### Post-Failure Checklist

- [ ] Analyzed failure to determine root cause location
- [ ] If generator issue: Fixed generator, regenerated ALL resources
- [ ] If schema issue: Fixed in generator, regenerated
- [ ] If resource issue: Fixed specific resource implementation
- [ ] If test issue: Fixed test code (only after ruling out above)
- [ ] Re-ran test to verify fix
- [ ] Checked that fix didn't break other tests

### Never Do

- ❌ Skip tests because "the schema doesn't support it" - fix the schema
- ❌ Skip tests because "state drift is expected" - fix the state handling
- ❌ Skip tests because "import doesn't work" - fix the import logic
- ❌ Comment out failing assertions - fix the root cause
- ❌ Use `ImportStateVerifyIgnore` without documented reason
- ❌ Use system/default/shared namespace without spec requirement
