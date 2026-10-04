---
name: driftabot
description: Query the DriftaBot Registry for API spec drifts, breaking changes, and provider information. Use when the user asks about API changes, breaking changes, provider specs, or what changed in a specific API.
metadata: {"openclaw.emoji": "🔍", "openclaw.homepage": "https://driftabot.github.io/registry/"}
---

# DriftaBot Registry Skill

DriftaBot Registry (https://github.com/DriftaBot/registry) is a public registry that:
- Tracks 59+ API providers (Stripe, GitHub, Twilio, Slack, Shopify, and many more)
- Crawls specs daily from each provider's canonical GitHub repository
- Generates markdown drift reports when breaking changes are detected

## When to use this skill

- User asks "did X API change?", "what broke in Y's API?", "show me drift for Z"
- User wants to know which providers are tracked in the registry
- User asks about current API spec versions or types (OpenAPI, GraphQL, gRPC)

## How to query the registry

Base URL: `https://raw.githubusercontent.com/DriftaBot/registry/main`

### 1. List all providers
Fetch `{BASE}/provider.companies.yaml` and parse the YAML.
Each entry has: `name` (slug), `display_name`, `specs[].type`, `specs[].repo`.

### 2. Get a drift report for a provider
Fetch `{BASE}/drifts/{org}/{repo}/result.md`
- Find `org/repo` from the provider's `specs[].repo` field in provider.companies.yaml
- Example: stripe → repo `stripe/openapi` → fetch `drifts/stripe/openapi/result.md`
- If the file returns 404 or empty, no breaking changes were detected for that provider.

### 3. Get the current spec file
Fetch `{BASE}/companies/providers/{name}/{type}/{filename}`
- Example: `companies/providers/stripe/openapi/stripe.openapi.json`

## Example queries and responses

**"Did Stripe's API break anything?"**
→ Fetch `drifts/stripe/openapi/result.md` and summarize the breaking changes.

**"What API providers are tracked?"**
→ Fetch `provider.companies.yaml`, list all company names and their spec types.

**"What type of spec does Shopify use?"**
→ Find shopify in provider.companies.yaml, return `specs[].type` (graphql).

## Tool usage

Use the `web` tool (or `bash` with curl) to fetch URLs. Parse YAML with available tools.
Always look up the repo from provider.companies.yaml before constructing drift URLs.
