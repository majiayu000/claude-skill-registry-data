---
name: docs-routing
description: Route requests for current library, framework, SDK, API, CLI, or cloud-service documentation through available documentation tools and primary sources.
---

# Documentation Routing

Use this route for current product documentation unless a higher-authority product-specific documentation workflow applies.

Before each lookup:

- Ask for the missing documentation fact or closely related facts, rather than passing the whole implementation task to the provider.
- Separate independent products or topics into focused queries. Combine them when the question concerns their interaction or a comparison.
- Include the exact product and requested version; add the repository owner or technical context when names are ambiguous (for example, `mistral.rs` with Apple's Metal backend). Set the tool's `product` field when available.

Follow this provider order for each lookup:

1. Query `mintlify_index` once with focused product and requested-version terms.
2. Accept the result only when it is nonempty, relevant, covers the requested version, and includes traceable source URLs.
3. Otherwise use `context7` to resolve the exact library and version. The plugin default is anonymous, but native same-name configuration may replace it with an authenticated connection. Do not repeat an equivalent Mintlify query.
4. When `context7` is anonymous and rate-limited, unavailable, or still insufficient, use `context7_auth` if it is available.
5. Then fall back to official primary documentation or source.
6. Never send secrets, credentials, private code, full prompts, or non-public internal content to either provider.
7. If a named tool is absent, advance to the next stage without automatically installing, authenticating, or retrying it. A host authentication prompt leaves the current call pending; after it is resolved or dismissed, apply the same acceptance test to the returned result and continue when it is insufficient.
