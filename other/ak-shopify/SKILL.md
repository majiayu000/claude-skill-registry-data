---
name: ak-shopify
description: "Build Shopify apps, extensions and themes with Shopify CLI, GraphQL/REST APIs, Polaris UI and Liquid."
when_to_use: "Invoke for checkout customization, webhooks or billing integration."
category: engineering
keywords: [shopify, polaris, liquid, checkout]
argument-hint: "[extension-type] [feature]"
metadata:
  author: agentkit
  version: "1.1.1"
---

# Shopify development

Resolve app, extension or theme from the request and project config. Read the installed CLI
and configured API version before commands; do not scaffold an app to edit a theme.

- App: `references/app-development.md` (OAuth, webhooks, billing).
- Extension: `references/extensions.md` (target and extension API).
- Theme: `references/themes.md` (Liquid, sections, preview).
- New setup: `references/setup-and-workflow-recipes.md` only when needed.

Preserve minimal OAuth scopes, webhook signature verification, server-owned billing state
and idempotency. Use development stores/preview themes for verification. Live deployment
requires the exact selected store/theme and authorized effects; preview does not imply live
publication. Track and clean up owned dev-server/tunnel processes.

## Essential Patterns

Load `references/essential-patterns.md` for the copyable code patterns:
a paginated GraphQL product query, a React checkout UI extension, and a
Liquid product-display loop.

## Best Practices

**API Usage:**
- Prefer GraphQL over REST for new development
- Request only needed fields to reduce costs
- Implement pagination for large datasets
- Use bulk operations for batch processing
- Respect rate limits (cost-based for GraphQL)

**Security:**
- Store API credentials in environment variables
- Verify webhook signatures
- Use OAuth for public apps
- Request minimal access scopes
- Implement session tokens for embedded apps

**Performance:**
- Cache API responses when appropriate
- Optimize images in themes
- Minimize Liquid logic complexity
- Use async loading for extensions
- Monitor query costs in GraphQL

**Testing:**
- Use development stores for testing
- Test across different store plans
- Verify mobile responsiveness
- Check accessibility (keyboard, screen readers)
- Validate GDPR compliance

## Reference Documentation

Detailed guides for advanced topics:

- **[App Development](references/app-development.md)** - OAuth, APIs, webhooks, billing
- **[Extensions](references/extensions.md)** - Checkout, Admin, POS, Functions
- **[Themes](references/themes.md)** - Liquid, sections, deployment

## Scripts

**[shopify_init.py](scripts/shopify_init.py)** - Initialize Shopify projects interactively
```bash
python scripts/shopify_init.py
```

## Troubleshooting

**Rate Limit Errors:**
- Monitor `X-Shopify-Shop-Api-Call-Limit` header
- Implement exponential backoff
- Use bulk operations for large datasets

**Authentication Failures:**
- Verify access token validity
- Check required scopes granted
- Ensure OAuth flow completed

**Extension Not Appearing:**
- Verify extension target correct
- Check extension published
- Ensure app installed on store

**Webhook Not Receiving:**
- Verify webhook URL accessible
- Check signature validation
- Review logs in Partner Dashboard

## Resources

**Official Documentation:**
- Shopify Docs: https://shopify.dev/docs
- GraphQL API: https://shopify.dev/docs/api/admin-graphql
- Shopify CLI: https://shopify.dev/docs/api/shopify-cli
- Polaris: https://polaris.shopify.com

**Tools:**
- GraphiQL Explorer (Admin → Settings → Apps → Develop apps)
- Partner Dashboard (app management)
- Development stores (free testing)

**API Versioning:**
- Quarterly releases (YYYY-MM format)
- Resolve the configured API version from the project and current official support policy
- 12-month support per version
- Test before version updates

---

Verify version-sensitive recipes against the project API/CLI version and official documentation.
