---
name: prism
description: Prism checkout orchestration context
---

# Prism Domain Context

## What Is Prism?

Prism is Violet's **core checkout orchestration product**. It enables channels (marketplaces, platforms) to buy products from Violet merchants.

### Prism vs Beam

| | Prism | Beam |
|---|-------|------|
| **Direction** | Read Products, Write Orders | Write Products, Read Orders |
| **Flow** | Ingest products from stores → Create orders there | Publish Violet products to destinations → Read orders back |
| **Customer** | Channels (marketplaces, platforms) | Destination merchants (dropshippers) |

## Key Concepts

### Channels
Platforms and marketplaces that use Violet's API to offer products from multiple merchants to their shoppers.

### Merchants
Sellers who connect their stores (Shopify, BigCommerce, WooCommerce, etc.) to Violet to make their products available through channels.

### Offers
Products listed on Violet, sourced from merchant stores. Each offer represents a product available for purchase through channels.

### Orders / Bags
When a shopper buys products through a channel:
- **Order**: The complete purchase
- **Bag**: Products from a single merchant within an order (multi-vendor support)

## Core Flows

### Merchant Onboarding
1. Merchant connects store via OAuth
2. Products sync to Violet catalog
3. Merchant sets commission rates
4. Products become available to channels

### Checkout Flow
1. Channel displays Violet products
2. Shopper adds to cart
3. Channel creates order via API
4. Violet splits order into bags by merchant
5. Orders created in merchant stores
6. Fulfillment tracked back to channel

## VioletDashboard Patterns

When working with VioletDashboard:

### API Proxy Pattern (MANDATORY)
- ALL backend API calls MUST go through Next.js API routes (`pages/api/`)
- Direct client-side calls to backend services are NOT supported

### Redux for State Management (MANDATORY)
- Use Redux Toolkit thunks and reducers for ALL async operations
- React Query is NOT used
- Follow existing patterns: thunks in `redux/thunks/`, reducers in `redux/reducers/`

### Form Handling
- React Hook Form + Yup validation
- Redux integration for submission

### Feature Flags
- Environment variables (build-time, not runtime)
- Format: `FEATURE_NAME_ENABLED`

## Key Repositories

| Repo | Purpose |
|------|---------|
| `VioletDashboard` | Channel/Merchant dashboards (Next.js) |
| `VioletConnect` | Merchant onboarding app (Next.js) |
| `MerchantService` | Backend merchant API |
| `OrderService` | Order processing |
| `prism-brain` | Product brain (specs, strategy) |

## Key Metrics

| Metric | Purpose |
|--------|---------|
| Checkout Conversion | Orders completed / checkouts started |
| Order Success Rate | Successful orders / total orders |
| Fulfillment Time | Time from order to fulfillment |
| Merchant Connect Rate | Stores connected / signup attempts |
