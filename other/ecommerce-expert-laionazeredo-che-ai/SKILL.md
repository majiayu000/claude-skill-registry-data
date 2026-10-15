---
name: "ecommerce-expert"
description: "Master guide for building high-performance e-commerce systems. Covers MedusaJS, storefront patterns, checkout flows, and payment integrations."
---

# E-commerce Expert Guide

This skill provides the standards for designing and implementing scalable, secure, and user-friendly online stores.

## 📦 Backend (MedusaJS)
- **Modular Architecture**: Use custom modules for specialized logic. Leverage module links for data associations.
- **Workflows**: Use Medusa Workflows for complex, long-running business processes (e.g., order fulfillment).
- **Extensibility**: Extend core entities using decorators and custom repositories.

## 🛒 Storefront Patterns
- **Checkout Flow**: Design frictionless, multi-step checkouts. Ensure state persistence across sessions.
- **Product Discovery**: Implement fast search and filtering (e.g., Meilisearch or Algolia).
- **Cart Management**: Handle local and server-side cart synchronization gracefully.

## 💳 Payments & Security
- **Integration**: Use official plugins for Stripe, PayPal, etc. Implement webhooks for status updates.
- **Compliance**: Ensure PCI DSS compliance. Never store sensitive card data on your servers.
- **Fraud Prevention**: Implement rate limiting and basic fraud checks on checkout attempts.

## 🔗 References
- [Medusa Documentation](https://docs.medusajs.com/)
- [Next.js Commerce Starter](https://github.com/vercel/commerce)
