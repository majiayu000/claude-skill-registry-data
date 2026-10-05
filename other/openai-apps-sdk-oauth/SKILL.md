---
name: openai-apps-sdk-oauth
description: Use when building a website, MCP server, or ChatGPT app that needs OpenAI Apps SDK custom auth with OAuth 2.1. Covers protected-resource metadata, per-tool securitySchemes, WWW-Authenticate challenges, token verification, and rollout checks for user-linked tools.
metadata:
  short-description: Build Apps SDK OAuth 2.1 flows
  runtime_support_files: true
runtime_projection: true
source_of_truth: registry/skills/openai-apps-sdk-oauth/SKILL.md
---

> Runtime projection for consumer agents.
> First-read entrypoint: `runtime/skills/openai-apps-sdk-oauth/SKILL.md`
> Source of truth: `registry/skills/openai-apps-sdk-oauth/SKILL.md`
> Use this runtime file first. Follow rewritten registry links only when this runtime view points you there.
> Consumer scope: `skill`
# OpenAI Apps SDK OAuth

Use this skill when the user is implementing OpenAI Apps SDK authentication for a website-backed product or MCP app that needs account linking through OAuth.
This skill focuses on the Apps SDK custom auth flow described in the OpenAI auth guide, not on generic website sign-in.

Official source of truth:

- `https://developers.openai.com/apps-sdk/build/auth`

## Use this skill for

- Add custom OAuth to an MCP server used by a website or ChatGPT app
- Decide how the website, MCP server, and identity provider split responsibilities
- Implement protected-resource metadata and tool-level `securitySchemes`
- Trigger ChatGPT account-linking UI correctly
- Verify end-user access tokens on every tool call
- Produce a practical local-test and rollout checklist
- Compare Auth0 and Stytch for Apps SDK and MCP auth work

## Do not use this skill for

- Plain OpenAI API key integration
- Generic website login without Apps SDK or MCP
- Replacing a mature identity provider with a hand-rolled OAuth server
- Deep vendor-specific IdP setup when the user only needs the OpenAI-side contract

## Workflow

### 1. Confirm the auth architecture

Read [references/architecture.md](references/architecture.md).

Produce a short boundary map covering:

- website frontend, if one exists
- MCP server as the resource server
- identity provider or authorization server
- tools that are public vs tools that require linking
- scopes needed per tool group

Prefer an existing identity provider. The OpenAI auth guide explicitly recommends using an established provider instead of building auth from scratch.

### 2. Check OAuth 2.1 and MCP prerequisites

Read [references/oauth-requirements.md](references/oauth-requirements.md).

Validate that the chosen IdP can support:

- discovery metadata
- dynamic client registration
- correct handling of the `resource` parameter
- Authorization Code with PKCE for public-client flows

If any of these are missing, call that out early as an architecture blocker.

If the user already chose an identity provider, load the matching vendor guide as well:

- [references/auth0.md](references/auth0.md)
- [references/stytch.md](references/stytch.md)

### 3. Publish protected-resource metadata

Read [references/mcp-resource-metadata.md](references/mcp-resource-metadata.md).

Expose a well-known protected-resource metadata document for the MCP server.
Treat the MCP server as the resource being protected, not the browser frontend.

### 4. Describe tool auth policy with `securitySchemes`

Read [references/tool-auth-patterns.md](references/tool-auth-patterns.md).

Rules:

- Prefer per-tool `securitySchemes`, even if the entire server shares one provider
- Use `oauth2` for tools that require account-linked access
- Use both `noauth` and `oauth2` only when anonymous access is intentionally supported and linked access unlocks more

### 5. Trigger ChatGPT linking UI correctly

Read [references/tool-auth-patterns.md](references/tool-auth-patterns.md).

The OpenAI guide requires both:

- metadata that advertises OAuth availability
- runtime auth failures carrying `_meta["mcp/www_authenticate"]`

Without both halves, ChatGPT will not present the linking UI for the tool.

### 6. Verify tokens inside the MCP server

Read [references/token-verification-checklist.md](references/token-verification-checklist.md).

Assume every incoming bearer token is untrusted until verified.
Check signature, issuer, audience or resource, expiry, not-before, and required scopes before running tool logic.

### 7. Test and roll out

Read [references/testing-and-rollout.md](references/testing-and-rollout.md).

Start with short-lived development tokens and test these cases:

- first-time linking
- expired token
- missing token
- insufficient scope
- relinking after scope changes
- optional-auth tools falling back to anonymous mode

If the deployment uses ChatGPT connector authentication, keep mTLS and OAuth responsibilities separate:

- mTLS authenticates ChatGPT as the MCP client
- OAuth authenticates the end user and authorizes tool access

## Output contract

For each implementation or review, output these sections in order:

1. architecture summary
2. auth boundary decisions
3. scope design
4. protected-resource metadata requirements
5. tool `securitySchemes` plan
6. runtime challenge behavior
7. token verification checklist
8. local test plan
9. rollout risks

## Reference loading guide

- Load [references/architecture.md](references/architecture.md) first.
- Load [references/oauth-requirements.md](references/oauth-requirements.md) before choosing or approving an IdP.
- Load [references/auth0.md](references/auth0.md) when the user is implementing with Auth0 or comparing Auth0 against alternatives.
- Load [references/stytch.md](references/stytch.md) when the user is implementing with Stytch or wants a more MCP-native hosted OAuth pattern.
- Load [references/mcp-resource-metadata.md](references/mcp-resource-metadata.md) when implementing the well-known metadata endpoint.
- Load [references/tool-auth-patterns.md](references/tool-auth-patterns.md) when wiring tool declarations or auth-triggering errors.
- Load [references/token-verification-checklist.md](references/token-verification-checklist.md) before writing the MCP auth middleware.
- Load [references/testing-and-rollout.md](references/testing-and-rollout.md) when preparing local validation or production rollout.

Load only the file needed for the step in front of you.
