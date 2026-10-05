---
name: rudder-instrumentation-planning
description: Designs event taxonomies and instrumentation strategies from business requirements. Use when designing event taxonomy from scratch or restructuring existing instrumentation strategy
allowed-tools: "Bash(rudder-cli *), Read, Write, Edit"
---

# Instrumentation Planning

This skill guides you through designing an **instrumentation strategy** - the systematic approach to deciding what events and properties to track in your application.

## Why Planning Matters

Poor instrumentation leads to:
- **Data gaps** - Can't answer business questions
- **Data bloat** - Too many events, high costs, noise
- **Inconsistency** - Same action tracked differently across teams
- **Technical debt** - Constant schema changes breaking dashboards

Good instrumentation provides:
- **Complete funnel visibility** - Every step from acquisition to retention
- **Consistent naming** - Clear conventions everyone follows
- **Maintainable schema** - Easy to extend, hard to break
- **Actionable insights** - Data that drives decisions

## Choose Your Workflow

Different starting points require different approaches:

| Your Situation | Recommended Skill |
|----------------|-------------------|
| Building new feature, events not yet defined | `rudder-design-first-instrumentation` |
| Existing product needs instrumentation | `rudder-code-first-instrumentation` |
| Restructuring existing tracking | `rudder-code-first-instrumentation` |
| General planning guidance | Continue with this skill |

### Design-First vs Code-First

**Design-First:** Start from product requirements → define events → define properties → implement code. Best for new features where events are part of product definition.

**Code-First:** Start from existing code types → derive tracking plan → align with data governance. Best for existing products with domain types already defined.

This skill covers the general planning process. For workflow-specific guidance, see the specialized skills above.

## The Planning Process

```
┌─────────────────────────────────────────────────────────────────────┐
│                     INSTRUMENTATION PLANNING                         │
└─────────────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────┐
│ 1. DISCOVERY    │ ← What questions do we need to answer?
└────────┬────────┘
         ▼
┌─────────────────┐
│ 2. TAXONOMY     │ ← What events and properties will answer them?
└────────┬────────┘
         ▼
┌─────────────────┐
│ 3. BUILD        │ ← Create the YAML definitions
└────────┬────────┘
         ▼
┌─────────────────┐
│ 4. ASSEMBLE     │ ← Group into tracking plans
└────────┬────────┘
         ▼
┌─────────────────┐
│ 5. INTEGRATE    │ ← Generate code, implement in apps
└─────────────────┘
```

## Phase 1: Discovery

### Questions to Ask Stakeholders

**Business Questions:**
- What KPIs do we track? (conversion rate, retention, revenue)
- What funnels do we analyze? (signup, checkout, onboarding)
- What experiments will we run? (A/B tests need specific events)
- What attribution do we need? (marketing channels, campaigns)

**Product Questions:**
- What are the key user journeys?
- What features do we want to measure adoption for?
- What errors/failures do we need to monitor?

**Technical Questions:**
- What platforms exist? (web, iOS, Android, server)
- What existing tracking is in place?
- What tools consume this data? (Amplitude, Mixpanel, warehouse)

### Discovery Template

```markdown
## Business Goals
- [ ] Primary KPIs: _______________
- [ ] Key funnels: _______________
- [ ] Attribution needs: _______________

## User Journeys to Track
1. _______________
2. _______________
3. _______________

## Platforms
- [ ] Web
- [ ] iOS
- [ ] Android
- [ ] Server

## Existing Tracking
- Current events: ___ events
- Issues with current: _______________
```

## Phase 2: Taxonomy Design

### Step 1: Define Event Categories

Group events by business domain:

| Category | Purpose | Examples |
|----------|---------|----------|
| `user-lifecycle` | Account actions | Signed Up, Logged In, Profile Updated |
| `ecommerce` | Purchase funnel | Product Viewed, Added to Cart, Order Completed |
| `engagement` | Feature usage | Feature Used, Content Viewed, Search Performed |
| `errors` | Failure tracking | Error Occurred, Checkout Failed |

### Step 2: Map User Journeys to Events

**Example: E-Commerce Funnel**

```
User Journey                    Events
───────────                    ──────
Browse products         →      Product Viewed
Add to cart            →      Product Added to Cart
Start checkout         →      Checkout Started
Complete purchase      →      Order Completed
```

**Example: SaaS Onboarding**

```
User Journey                    Events
───────────                    ──────
Create account         →      Signed Up
Verify email           →      Email Verified
Complete profile       →      Profile Completed
Use first feature      →      Feature Used (first_time: true)
Invite teammate        →      Team Member Invited
```

### Step 3: Identify Properties

For each event, list required context:

**Product Viewed**
- Required: product_id, product_name, product_price, product_category
- Optional: page_url, referrer_url, session_id
- Context: How did they find it? What were they looking at?

**Order Completed**
- Required: order_id, order_total, products, customer_email
- Optional: discount_code, shipping_method, payment_method
- Context: What did they buy? How much? What discounts?

### Step 4: Identify Shared Patterns

Look for properties used across multiple events:

```
Shared across all events:
- session_id
- user_id (if logged in)
- timestamp (automatic)

Shared across e-commerce events:
- product object (id, name, price, category)

Shared across Order Completed:
- address object (street, city, state, zip)
```

These become **Custom Types**.

## Phase 3: Build the Data Catalog

### Order of Creation

```
1. Custom Types    ← Reusable validation patterns
2. Properties      ← The vocabulary
3. Categories      ← Organization
4. Events          ← The actions (reference properties)
```

### Real-World Example: E-Commerce Store

**Custom Types:**

```yaml
# 1. ProductType - used by multiple events
version: "rudder/v1"
kind: "custom-type"
metadata:
  name: "custom-types"
spec:
  name: "ProductType"
  type: "object"
  description: "Consolidated product information"
  config:
    properties:
      - property: "urn:rudder:property/product_id"
        required: true
      - property: "urn:rudder:property/product_name"
        required: true
      - property: "urn:rudder:property/product_price"
        required: true
      - property: "urn:rudder:property/product_category"
        required: true
---
# 2. AddressType - used for shipping and billing
version: "rudder/v1"
kind: "custom-type"
metadata:
  name: "custom-types"
spec:
  name: "AddressType"
  type: "object"
  description: "US mailing address"
  config:
    properties:
      - property: "urn:rudder:property/street"
        required: true
      - property: "urn:rudder:property/city"
        required: true
      - property: "urn:rudder:property/state"
        required: true
      - property: "urn:rudder:property/zipcode"
        required: true
```

**Properties:**

```yaml
# Product properties
version: "rudder/v1"
kind: "property"
metadata:
  name: "properties"
spec:
  name: "product_id"
  type: "string"
  description: "Unique product identifier"
  config:
    minLength: 1
    maxLength: 128
---
version: "rudder/v1"
kind: "property"
metadata:
  name: "properties"
spec:
  name: "product_category"
  type: "string"
  description: "Product category"
  config:
    enum:
      - "Footwear"
      - "Clothing"
      - "Accessories"
      - "Electronics"
---
# Address properties with validation
version: "rudder/v1"
kind: "property"
metadata:
  name: "properties"
spec:
  name: "zipcode"
  type: "string"
  description: "US ZIP code"
  config:
    pattern: "^[0-9]{5}(-[0-9]{4})?$"
```

**Events:**

```yaml
# The e-commerce funnel
version: "rudder/v1"
kind: "event"
metadata:
  name: "events"
spec:
  name: "Product Viewed"
  description: "User viewed a product detail page"
  category: "urn:rudder:category/ecommerce"
  rules:
    - property: "urn:rudder:property/product"
      required: true
      customType: "urn:rudder:custom-type/product-type"
    - property: "urn:rudder:property/page_url"
    - property: "urn:rudder:property/referrer_url"
---
version: "rudder/v1"
kind: "event"
metadata:
  name: "events"
spec:
  name: "Product Added to Cart"
  description: "User added a product to their cart"
  category: "urn:rudder:category/ecommerce"
  rules:
    - property: "urn:rudder:property/product"
      required: true
      customType: "urn:rudder:custom-type/product-type"
    - property: "urn:rudder:property/quantity"
      required: true
    - property: "urn:rudder:property/cart_total"
---
version: "rudder/v1"
kind: "event"
metadata:
  name: "events"
spec:
  name: "Order Completed"
  description: "Customer completed a purchase"
  category: "urn:rudder:category/ecommerce"
  rules:
    - property: "urn:rudder:property/order_id"
      required: true
    - property: "urn:rudder:property/order_total"
      required: true
    - property: "urn:rudder:property/customer_email"
      required: true
    - property: "urn:rudder:property/shipping_address"
      required: true
      customType: "urn:rudder:custom-type/address-type"
    - property: "urn:rudder:property/billing_address"
      required: true
      customType: "urn:rudder:custom-type/address-type"
    - property: "urn:rudder:property/products"
      required: true
```

## Naming Conventions

### Events

| Pattern | Example | When to Use |
|---------|---------|-------------|
| Object Action | Product Viewed | Standard user actions |
| Past Tense | Order Completed | Completed actions |
| Title Case | Product Added to Cart | Always |

**Good:**
- `Product Viewed`
- `Order Completed`
- `Feature Used`

**Bad:**
- `productView` (camelCase)
- `PRODUCT_VIEWED` (screaming snake)
- `Click Product` (wrong verb)

### Properties

| Pattern | Example | When to Use |
|---------|---------|-------------|
| snake_case | product_id | Always |
| Descriptive | customer_email | Include context |
| Specific | shipping_address | Not just "address" |

**Good:**
- `product_id`
- `order_total`
- `customer_email`

**Bad:**
- `productId` (camelCase)
- `id` (too generic)
- `total` (ambiguous)

### Categories

| Pattern | Example |
|---------|---------|
| kebab-case | ecommerce |
| Lowercase | user-lifecycle |

## Common Event Patterns

See `references/event-patterns.md` for standard event taxonomy patterns (e-commerce funnel, user lifecycle, feature engagement, error tracking) and anti-patterns to avoid.

## Phase 4: Assemble Tracking Plans

Group events by source/application:

```yaml
# Web App - full funnel
spec:
  name: "Web App Tracking Plan"
  events:
    - event: "urn:rudder:event/product-viewed"
    - event: "urn:rudder:event/product-added-to-cart"
    - event: "urn:rudder:event/checkout-started"
    - event: "urn:rudder:event/order-completed"

# Mobile App - simplified
spec:
  name: "Mobile App Tracking Plan"
  events:
    - event: "urn:rudder:event/product-viewed"
    - event: "urn:rudder:event/order-completed"
```

## Phase 5: Integrate

### Validate and Apply

```bash
# Validate all definitions
rudder-cli validate -l ./

# Preview changes
rudder-cli apply --dry-run -l ./

# Apply to workspace
rudder-cli apply -l ./
```

### Generate Type-Safe Code

```bash
# Initialize RudderTyper
rudder-cli typer init

# Generate SDK
rudder-cli typer generate
```

### Implement in Applications

Use generated code for type-safe tracking:

```kotlin
// Type-safe, IDE autocomplete, compile-time validation
analytics.productViewed(
    product = ProductType(
        productId = "shoes-001",
        productName = "Running Shoes",
        productPrice = 89.99,
        productCategory = ProductCategory.FOOTWEAR
    )
)
```

## Credential Security

When planning instrumentation that involves authentication or sensitive data:

- **Never track passwords or tokens** - exclude sensitive fields from event properties
- **Hash or anonymize PII** - user emails, phone numbers should be hashed if tracked
- **Use RudderStack's PII masking** - configure masking rules for sensitive properties
- **Store workspace tokens securely** - use environment variables, never commit to git
- **Add `.env` to `.gitignore`** - protect local development credentials

## Checklist

Before finalizing your instrumentation plan:

- [ ] All business questions can be answered with planned events
- [ ] Naming conventions are documented and consistent
- [ ] Custom types created for repeated property groups
- [ ] Required vs optional clearly defined for each property
- [ ] Categories organize events logically
- [ ] Tracking plans exist for each source/platform
- [ ] Validation passes: `rudder-cli validate -l ./`

## References

- `references/event-patterns.md` - Standard event taxonomy patterns and anti-patterns
- `references/session-lifecycle-patterns.md` - When to use identify, group, and track calls
