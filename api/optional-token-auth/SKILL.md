---
name: optional-token-auth
description: How optional JWT bearer authentication works - left out unless the solution was created with --include-auth, every endpoint asks for authorization, the few that stay anonymous, and how to add it later. Use when protecting a new endpoint, making one public, adding authentication to a solution without it, or changing authentication settings.
metadata:
  scope: shared
---

# Optional token authentication

## The rule

Authentication is a choice made when the solution is created. With `--include-auth`, `--authority` and usually `--audience`, every request needs a valid JWT bearer token from that authority (an OAuth access token in the MCP server), and those options fill in `Authentication:Authority` and `Authentication:Audience`. Without `--include-auth` there's no authentication code at all: no settings, no package, no policy and nothing asking for authorization. If `AuthenticationSettings` isn't in the solution, it was created without `--include-auth`; see "Adding it later".

With `--include-auth`, endpoints always ask for authorization. An empty `Authentication:Authority` still runs everything open, because the default policy then lets every request through, which is how the tests run unless they set an authority. Only health checks and the API reference (where a template has them) are anonymous. The version endpoint is protected like everything else; telemetry carries `service.version` for anyone who needs to know what's deployed. The Lambda template has no token authentication; API Gateway or the caller's IAM role does that job.

Settings are read through `AuthenticationSettings.FromConfiguration` (`Enabled` is true when the authority isn't empty).

## Steps

1. In a solution with authentication, a new endpoint or group gets `.RequireAuthorization()` (or the presentation layer's equivalent). That's the default; don't skip it. Without it there's nothing to call.
2. Only make something anonymous if it has to work without a token: health and the API reference. Say why in a comment.
3. When authentication is on, the template tells clients how to get a token: a bearer scheme in the OpenAPI document where a template has one, and the protected resource metadata in MCP.
4. Test both modes: one test with no authority (anonymous works), one with an authority and no token (401).

## Adding it later

A solution created without `--include-auth` can have it added by hand. The quickest way to see every line is to create a second solution with the same name and `--include-auth --authority https://login.example.com`, then diff the two. The difference is the authentication package reference in the Presentation project, the `Authentication` folder and its settings section in `appsettings.json`, the authentication regions in startup, the anonymous health checks, the call that asks every endpoint or group for authorization, the OpenAPI or MCP metadata that tells clients how to get a token, and the authentication tests. Copy all of it, including the tests, so coverage stays at 95%.

## Don't

- Check `Enabled` inside an endpoint. The policy setup in startup handles both modes.
- Put a real authority, client id or secret in `appsettings.json`.
- Use `[AllowAnonymous]` to get a test to pass.

## Check

``` bash
dotnet test --filter "FullyQualifiedName~Authentication"
```
