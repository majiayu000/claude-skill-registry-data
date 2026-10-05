---
name: rudder-typer-workflow
description: Generates type-safe SDKs (Swift/Kotlin) from tracking plans with compile-time validation. Use when generating type-safe event tracking code from tracking plans using RudderTyper
allowed-tools: "Bash(rudder-cli *), Read, Write, Edit"
---

# RudderTyper Workflow

This skill teaches how to use **RudderTyper** to generate type-safe SDKs from your tracking plan, enabling compile-time validation of analytics calls.

## What is RudderTyper?

RudderTyper generates native code from your tracking plan so developers:
- Get **compile-time validation** of event names and properties
- Have **autocomplete** for events and properties in their IDE
- Catch **instrumentation errors before runtime**
- See **documentation** from your tracking plan inline

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Tracking Plan  │────▶│   RudderTyper   │────▶│  Generated SDK  │
│     (YAML)      │     │   (Generator)   │     │ (Swift/Kotlin)  │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                                                        │
                                                        ▼
                                               ┌─────────────────┐
                                               │   Mobile App    │
                                               │  (Type-safe!)   │
                                               └─────────────────┘
```

## Supported Platforms

| Platform | Language | Status | Use Case |
|----------|----------|--------|----------|
| iOS | Swift | Available | iOS, macOS, tvOS, watchOS apps |
| Android | Kotlin | Available | Android apps, JVM applications |
| Web | TypeScript | Manual | Web apps, Node.js (see [TypeScript Type Alignment](#typescript-type-alignment-manual)) |

## Quick Start

### Step 1: Initialize RudderTyper

```bash
rudder-cli typer init
```

Creates `ruddertyper.yml`:

```yaml
version: "1.0.0"
trackingPlan:
  id: "tp_abc123"              # Your tracking plan ID
  workspace: "ws_xyz789"       # Your workspace ID
language: kotlin               # or "swift"
output:
  path: ./generated            # Where to generate code
```

### Step 2: Generate Code

```bash
rudder-cli typer generate
```

### Step 3: Integrate

Add the generated directory to your project and import the Analytics class.

## Real-World Example: E-Commerce App

### Your Tracking Plan

```yaml
# tracking-plan.yaml
version: "rudder/v1"
kind: "tracking-plan"
metadata:
  name: "tracking-plans"
spec:
  name: "Mobile App Tracking Plan"
  events:
    - event: "urn:rudder:event/product-viewed"
    - event: "urn:rudder:event/product-added-to-cart"
    - event: "urn:rudder:event/order-completed"
```

### Generated Kotlin Code

RudderTyper generates:

```kotlin
// generated/Analytics.kt

/**
 * User viewed a product detail page
 */
fun productViewed(
    product: ProductType,
    pageUrl: String? = null,
    referrerUrl: String? = null
) {
    track("Product Viewed", mapOf(
        "product" to product.toMap(),
        "page_url" to pageUrl,
        "referrer_url" to referrerUrl
    ))
}

/**
 * User added a product to their cart
 */
fun productAddedToCart(
    product: ProductType,
    quantity: Int,
    cartTotal: Double? = null,
    productCount: Int? = null
) {
    track("Product Added to Cart", mapOf(
        "product" to product.toMap(),
        "quantity" to quantity,
        "cart_total" to cartTotal,
        "product_count" to productCount
    ))
}

/**
 * Customer completed a purchase
 */
fun orderCompleted(
    orderId: String,
    orderTotal: Double,
    customerEmail: String,
    products: List<ProductType>,
    shippingAddress: AddressType,
    billingAddress: AddressType
) {
    track("Order Completed", mapOf(
        "order_id" to orderId,
        "order_total" to orderTotal,
        "customer_email" to customerEmail,
        "products" to products.map { it.toMap() },
        "shipping_address" to shippingAddress.toMap(),
        "billing_address" to billingAddress.toMap()
    ))
}

// Custom type classes
data class ProductType(
    val productId: String,
    val productSku: String,
    val productName: String,
    val productCategory: ProductCategory,
    val productPrice: Double,
    val productMsrp: Double? = null
)

enum class ProductCategory {
    FOOTWEAR,
    CLOTHING,
    ACCESSORIES
}

data class AddressType(
    val address: String,
    val city: String,
    val state: String,
    val zipcode: String
)
```

### Using Generated Code

**Before RudderTyper** (error-prone):

```kotlin
// Typos won't be caught until runtime
analytics.track("Product Viewd", mapOf(   // Typo in event name!
    "product_id" to "shoes-001",
    "proudct_name" to "Running Shoes",    // Typo in property!
    "price" to "89.99"                    // Wrong type (string vs number)!
))
```

**After RudderTyper** (type-safe):

```kotlin
// IDE autocomplete, compile-time validation
analytics.productViewed(
    product = ProductType(
        productId = "shoes-001",
        productSku = "RUN-001",
        productName = "Running Shoes",
        productCategory = ProductCategory.FOOTWEAR,
        productPrice = 89.99
    )
)
```

Compile errors catch:
- ✓ Wrong event name (method doesn't exist)
- ✓ Wrong property name (parameter doesn't exist)
- ✓ Wrong type (compiler type mismatch)
- ✓ Missing required property (non-optional parameter)

### Swift Example

```swift
// generated/Analytics.swift

/// User viewed a product detail page
func productViewed(
    product: ProductType,
    pageUrl: String? = nil,
    referrerUrl: String? = nil
) {
    track("Product Viewed", properties: [
        "product": product.toDictionary(),
        "page_url": pageUrl,
        "referrer_url": referrerUrl
    ])
}

struct ProductType {
    let productId: String
    let productSku: String
    let productName: String
    let productCategory: ProductCategory
    let productPrice: Double
    let productMsrp: Double?
}

enum ProductCategory: String {
    case footwear = "Footwear"
    case clothing = "Clothing"
    case accessories = "Accessories"
}
```

## Configuration Options

### ruddertyper.yml

```yaml
version: "1.0.0"

trackingPlan:
  id: "tp_abc123"
  workspace: "ws_xyz789"

language: kotlin                    # "kotlin" or "swift"

output:
  path: ./app/src/main/java/analytics   # Output directory

# Optional: customize naming
naming:
  eventPrefix: ""                   # Prefix for event methods
  eventSuffix: ""                   # Suffix for event methods

# Optional: include/exclude events
events:
  include:
    - "Product Viewed"
    - "Product Added to Cart"
  # OR
  exclude:
    - "Internal Debug Event"
```

## Iteration Workflow

When your tracking plan changes:

```
┌──────────────────┐
│ 1. Update YAML   │ ← Add/modify events, properties, custom types
└────────┬─────────┘
         ▼
┌──────────────────┐
│ 2. Validate      │ ← rudder-cli validate -l ./
└────────┬─────────┘
         ▼
┌──────────────────┐
│ 3. Apply         │ ← rudder-cli apply -l ./
└────────┬─────────┘
         ▼
┌──────────────────┐
│ 4. Regenerate    │ ← rudder-cli typer generate
└────────┬─────────┘
         ▼
┌──────────────────┐
│ 5. Fix Compile   │ ← Update app code to match new schema
│    Errors        │
└────────┬─────────┘
         ▼
┌──────────────────┐
│ 6. Commit Both   │ ← Spec changes + generated code together
└──────────────────┘
```

### Commands

```bash
# 1. Validate tracking plan
rudder-cli validate -l ./

# 2. Apply changes to workspace
rudder-cli apply -l ./

# 3. Regenerate code
rudder-cli typer generate

# 4. Build app to check for errors
./gradlew build          # Android
xcodebuild               # iOS
```

## CI/CD Integration

See `references/ci-cd-integration.md` for GitHub Actions workflows, pre-commit hooks, multi-platform project patterns, and monorepo configurations.

## Troubleshooting

### Generated Code Not Updating

```bash
# Ensure tracking plan is applied first
rudder-cli apply -l ./

# Then regenerate
rudder-cli typer generate
```

### Type Mismatch Errors

Check property types in YAML match expected usage:

```yaml
# Wrong: price as string
spec:
  name: "product_price"
  type: "string"

# Right: price as number
spec:
  name: "product_price"
  type: "number"
```

### Missing Required Properties

Generated methods require all `required: true` properties as non-optional parameters:

```kotlin
// This won't compile if productId is required
analytics.productViewed(
    product = ProductType(
        // productId missing - compile error!
        productName = "Test"
    )
)
```

### Custom Types Not Generating

Ensure custom types are:
1. Defined in YAML with correct schema
2. Referenced in event rules
3. Applied to workspace before generating

```bash
rudder-cli validate -l ./
rudder-cli apply -l ./
rudder-cli typer generate
```

## Command Reference

```bash
# Initialize RudderTyper configuration
rudder-cli typer init

# Generate code from tracking plan
rudder-cli typer generate

# Generate with specific config file
rudder-cli typer generate --config path/to/ruddertyper.yml

# Generate with verbose output
rudder-cli typer generate --verbose
```

---

## TypeScript Type Alignment (Manual)

Until automated TypeScript generation is available, manually align types with your tracking plan.

### Deriving Types from Tracking Plan

Given this property definition:

```yaml
# properties/product-properties.yaml
version: "rudder/v1"
kind: "property"
metadata:
  name: "properties"
spec:
  name: "product_category"
  type: "string"
  config:
    enum:
      - "footwear"
      - "clothing"
      - "accessories"
```

Create matching TypeScript:

```typescript
// src/analytics/types.ts

export type ProductCategory = "footwear" | "clothing" | "accessories";

export interface ProductType {
  product_id: string;
  product_sku: string;
  product_name: string;
  product_price: number;
  product_category: ProductCategory;
}

export interface ProductViewedEvent {
  product: ProductType;
  page_url?: string;
  referrer_url?: string;
}

export interface OrderCompletedEvent {
  order_id: string;
  order_total: number;
  currency: string;
  products: ProductType[];
}
```

### Using in Instrumentation

```typescript
import { ProductType, ProductCategory, ProductViewedEvent } from './analytics/types';
import analytics from './analytics/client';

function trackProductViewed(product: ProductType, pageUrl?: string) {
  const event: ProductViewedEvent = {
    product,
    page_url: pageUrl,
  };

  analytics.track('Product Viewed', event);
}

// Usage - compiler validates everything
trackProductViewed({
  product_id: "shoes-001",
  product_sku: "RUN-001",
  product_name: "Running Shoes",
  product_price: 89.99,
  product_category: "footwear",  // TypeScript ensures valid category
});
```

### Compile-Time Validation

TypeScript compiler catches:

| Error Type | Example | Compiler Message |
|------------|---------|------------------|
| Wrong enum value | `product_category: "shoes"` | Type '"shoes"' is not assignable |
| Missing required property | `{ product_name: "Test" }` | Property 'product_id' is missing |
| Type mismatch | `product_price: "89.99"` | Type 'string' is not assignable to 'number' |
| Typo in property name | `produt_id: "123"` | Object literal may only specify known properties |

### Type Alignment Workflow

```
┌──────────────────────────────────────────────────────────────────────┐
│                   TYPESCRIPT TYPE ALIGNMENT                          │
└──────────────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────┐
│ 1. Define YAML  │ ← Properties with enums, types, constraints
└────────┬────────┘
         ▼
┌─────────────────┐
│ 2. Create TS    │ ← Mirror YAML definitions in TypeScript
│    Types        │
└────────┬────────┘
         ▼
┌─────────────────┐
│ 3. Build App    │ ← Compiler validates alignment
└────────┬────────┘
         ▼
┌─────────────────┐
│ 4. Fix Errors   │ ← Compiler tells you what's wrong
└────────┬────────┘
         ▼
┌─────────────────┐
│ 5. Commit Both  │ ← YAML + TypeScript stay in sync
└─────────────────┘
```

### Keeping Types in Sync

When the tracking plan changes:

1. Update YAML definitions
2. Update TypeScript types to match
3. Build app - compiler errors show what needs updating
4. Fix instrumentation code
5. Commit YAML + TypeScript + instrumentation together

> "TypeScript for LLMs is the greatest teacher. It puts it in guardrails."

---

## TypeSpec for Multi-Platform (Future)

Microsoft's TypeSpec can define constraints once, generate for multiple languages:

```typescript
// tracking-plan.tsp
model ProductType {
  product_id: string;
  product_sku: string;
  product_name: string;
  product_price: float64;
  product_category: ProductCategory;
}

enum ProductCategory {
  footwear,
  clothing,
  accessories,
}

model ProductViewedEvent {
  product: ProductType;
  page_url?: string;
  referrer_url?: string;
}
```

Generate to:
- TypeScript interfaces
- Swift structs
- Kotlin data classes
- JSON Schema for validation

**Note:** This is a future integration opportunity that would unify type generation across all platforms.
