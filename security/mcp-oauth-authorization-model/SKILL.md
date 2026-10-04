---
name: mcp-oauth-authorization-model
kind: skill
status: ready
provenance:
  principles:
  - P001
  - P003
  - P006
  - P007
  - P013
  - P014
  - P018
  - P020
  - P021
  - P036
  - P045
  - P058
  - P059
  - P066
  - P067
  - P076
  - P077
  - P078
  - P091
  - P101
  - P102
  - P103
  - P121
  - P123
  - P124
  - P126
  - P128
  - P135
  - P136
  - P144
  - P145
  - P157
  - P158
  - P159
  - P161
  - P162
  - P177
  - P192
  - P195
  - P199
  - P207
  - P216
  - P217
  - P219
  - P220
  claims:
  - C00006
  - C00007
  - C00008
  - C00010
  - C00017
  - C00018
  - C00019
  - C00020
  - C00038
  - C00039
  - C00040
  - C00043
  - C00046
  - C00047
  - C00050
  - C00051
  - C00054
  - C00056
  - C00058
  - C00059
  - C00061
  - C00062
  - C00066
  - C00067
  - C00071
  - C00072
  - C00076
  - C00077
  - C00078
  - C00085
  - C00094
  - C00095
  - C00102
  - C00103
  - C00151
  - C00160
  - C00251
  - C00252
  - C00462
  - C00463
  - C00464
  - C00467
  - C00468
  - C00472
  - C00473
  - C00477
  - C00478
  - C00479
  - C00498
  - C00509
  - C00513
  - C00514
  - C00518
  - C00535
  - C00536
  - C00555
  - C00557
  - C00558
  - C00560
  - C00563
  - C00564
  - C00565
  - C00571
  - C00572
  - C00584
  - C00585
  - C00593
  - C00594
  - C00612
  - C00613
  - C00614
  - C00615
  - C00617
  - C00618
  - C00622
  - C00623
  - C00625
  - C00626
  - C00627
  - C00628
  - C00633
  - C00634
  - C00643
  - C00644
  - C00682
  - C00683
  evidence:
  - E00005
  - E00006
  - E00007
  - E00009
  - E00010
  - E00011
  - E00012
  - E00013
  - E00031
  - E00032
  - E00033
  - E00034
  - E00035
  - E00036
  - E00038
  - E00039
  - E00042
  - E00044
  - E00046
  - E00047
  - E00049
  - E00050
  - E00054
  - E00055
  - E00059
  - E00060
  - E00064
  - E00065
  - E00066
  - E00072
  - E00076
  - E00077
  - E00084
  - E00085
  - E00124
  - E00129
  - E00209
  - E00210
  - E00368
  - E00369
  - E00370
  - E00372
  - E00373
  - E00377
  - E00378
  - E00380
  - E00381
  - E00382
  - E00397
  - E00408
  - E00410
  - E00411
  - E00415
  - E00429
  - E00430
  - E00445
  - E00446
  - E00447
  - E00449
  - E00452
  - E00453
  - E00454
  - E00458
  - E00459
  - E00469
  - E00470
  - E00475
  - E00476
  - E00483
  - E00484
  - E00485
  - E00486
  - E00488
  - E00489
  - E00493
  - E00494
  - E00496
  - E00497
  - E00498
  - E00499
  - E00504
  - E00505
  - E00510
  - E00511
  - E00540
  - E00541
  source_anchors:
  - 0d5e0b52d96a-c0000
  - 515304c317e3-c0000
  - 6ff87e35998d-c0000
  - 73827be00a9b-c0000
  - 8aab528164de-c0000
  - 93eb31ae6ea3-c0000
  - b5eaaf20d167-c0000
  - b5eaaf20d167-c0001
  - c8cf335ba0d6-c0000
  - d59e5c41ce9d-c0000
  - dcbba5b2c9ad-c0000
  - ff3fcb8bc185-c0000
  authored_from_digest: c312083d34a0a6daf28d2d5f583530fd8ab60fd9fc9e529027362088456aeb68
---

# MCP OAuth Authorization Model

Review MCP authorization as an OAuth 2.1 identity-and-access system — resource-server/authorization-server split, token validation and audience binding, PKCE, resource indicators, discovery metadata, and redirect/state/token-lifecycle hygiene.

This skill packages 45 grounded principles the mcp-security-advisor applies when this surface is in scope. Each finding names the weakness, the attack it enables, the control, and the trade-off or residual risk.

## When this applies

- an MCP server receives a request bearing an access token.
- an MCP server receives a token from a client and could forward it to a downstream API.
- An MCP server receives a bearer token for a protected resource request.
- The MCP OAuth client is public and uses an authorization-code flow.
- The client cannot safely retain a long-lived client secret.
- An MCP client accesses a remote MCP server on behalf of a user.
- The flow uses an authorization code with a public MCP client.
- A public MCP client receives an authorization code after user approval.
- The client needs to call protected MCP resources.
- An MCP implementation follows the updated authorization model that separates authorization-server responsibilities from MCP-server responsibilities.
- The MCP server trusts a separate authorization server named in its protected-resource metadata.
- A deployment has or can use an external identity provider or OAuth authorization server.
- an MCP client receives a 401 from an MCP server.
- The resource server cannot or should not host metadata at the fixed well-known protected-resource location.
- A client first connects to the protected MCP resource without credentials.
- designing or requesting OAuth scopes for MCP tools and resources.

## Procedure

Apply the principles below in order of the risk they carry, highest first. For each one in scope: identify where untrusted data, a token, or an authorization decision enters, name the attack it enables, apply the control, and state the trade-off or residual risk. Never weaken a defence below what the source and the MCP specification support, and never present a single control as complete MCP security.

1. **P001 (high confidence).** MCP servers MUST validate every access token per OAuth 2.1 Section 5.2, accept only tokens whose intended audience is the server itself, return HTTP 401 for invalid or expired tokens, and never accept or transit tokens issued for othe…
2. **P003 (medium confidence).** Use the authorization-code flow with PKCE for MCP clients, then call protected MCP resources with the issued bearer access token only after a successful token exchange.
3. **P006 (medium confidence).** Use the separated authorization-server model in MCP as the architectural basis for enterprise-ready integrations rather than embedding all authorization behavior in the MCP server itself.
4. **P007 (high confidence).** Deliver Protected Resource Metadata via a WWW-Authenticate resource_metadata parameter on 401 responses or a well-known URI; clients MUST parse WWW-Authenticate headers, react to 401s, prefer the resource_metadata URL when present, an…
5. **P013 (medium confidence).** Adopt a progressive least-privilege scope model: grant a minimal initial scope of low-risk read/discovery operations, elevate incrementally via targeted WWW-Authenticate scope challenges, tolerate down-scoped tokens, emit precise (not…
6. **P014 (high confidence).** Clients MUST implement PKCE (S256 when technically capable) and verify PKCE support before authorizing by checking code_challenge_methods_supported in the authorization-server (or OpenID provider) metadata, refusing to proceed when it…
7. **P018 (medium confidence).** Prefer OAuth authorization-server metadata discovery for MCP OAuth so clients can discover endpoints automatically and avoid manual endpoint configuration errors.
8. **P020 (high confidence).** MCP proxy servers that use static client IDs MUST obtain user consent for each dynamically registered client before forwarding to third-party authorization servers, to prevent confused-deputy exploitation via stolen authorization code…
9. **P021 (high confidence).** Build on OAuth 2.1 and the referenced RFC subset (RFC 8414, RFC 7591, RFC 9728, Client ID Metadata Documents) rather than inventing bespoke authorization; authorization servers MUST implement OAuth 2.1 with appropriate measures for bo…
10. **P036 (high confidence).** Enforce least-privilege secure delegation for MCP servers using OAuth: authenticate users via existing OIDC identity providers, register servers as IAM clients (using Dynamic Client Registration when needed), never pass through user-p…
11. **P045 (high confidence).** Treat every server-supplied OAuth discovery URL as untrusted and apply SSRF defenses: require HTTPS in production, block private/reserved and cloud-metadata IP ranges, use a vetted library instead of hand-rolled IP validation, apply t…
12. **P058 (medium confidence).** For scalable MCP authorization, compose OAuth authorization, protected-resource metadata, authorization-server metadata, Dynamic Client Registration, and PKCE as one coordinated stack.
13. **P059 (medium confidence).** Prefer a capable hosted OAuth or identity platform when MCP auth requires consent lifecycle, token management, revocation, dynamic registration, or multiple external clients.
14. **P066 (high confidence).** Protect against open redirection: pre-register redirect URIs, have the authorization server validate them by exact match, avoid redirecting user agents to untrusted URIs (auto-redirecting only trusted ones), and have clients use and v…
15. **P067 (high confidence).** Run a strict OAuth state lifecycle: generate a cryptographically random state per request, persist it server-side only after the user approves consent and set the tracking cookie immediately before the third-party redirect, then at th…
16. **P076 (medium confidence).** Use OAuth rather than shared credentials or API keys when MCP agents need to access protected user resources, especially across remote or third-party boundaries.
17. **P077 (medium confidence).** Drive MCP OAuth setup from standards-based discovery documents instead of hardcoded provider assumptions or service-specific configuration.
18. **P078 (medium confidence).** Harden Client ID Metadata Document handling per its Section 6: mitigate SSRF when the authorization server fetches an attacker-supplied client_id URL, recognize that CIMD alone cannot prevent localhost redirect-URI impersonation (warn…
19. **P091 (medium confidence).** Construct authorization requests with complete OAuth parameters and present a consent experience that clearly identifies the requesting agent and requested scopes before approval.
20. **P101 (high confidence).** Do not require an MCP authorization server to own user interface, login, or account storage; it may delegate user authentication and account management to another service.
21. **P102 (high confidence).** Clients MUST implement RFC 8707 Resource Indicators and include a resource parameter identifying the target MCP server by its canonical URI in both authorization and token requests, sending it regardless of whether the authorization s…
22. **P103 (high confidence).** Preserve MCP client bootstrap from a single server URL by using protected-resource metadata to point clients from the MCP resource server to the appropriate authorization server metadata.
23. **P121 (medium confidence).** Model an MCP protected endpoint as a resource server and keep the authorization server role explicit, even if both roles are implemented by the same deployment.
24. **P123 (medium confidence).** Design MCP connection flows so users experience account-style authorization and self-service setup instead of managing tokens, scopes, and provider-specific configuration by hand.
25. **P124 (medium confidence).** Keep MCP resource-server authorization state minimal: validate external tokens and enforce local RBAC or permission checks inside the MCP server.
26. **P126 (medium confidence).** On a runtime insufficient-scope error, respond with 403 plus a Bearer WWW-Authenticate header carrying error=insufficient_scope, the required scope set, and resource_metadata; clients should react with a step-up authorization flow (us…
27. **P128 (medium confidence).** Use a dedicated MCP authorization server as a delegation boundary when relying on external identity or OAuth services, so the MCP client sees MCP-specific endpoints while backend identity flows can vary.
28. **P135 (medium confidence).** When delegating user login to a third-party identity provider, preserve the MCP OAuth responsibility for issuing an MCP-server token bound to the third-party session.
29. **P136 (medium confidence).** Validate JWT bearer tokens for signature, issuer, audience, expiry, and scopes before serving protected MCP data, and deny requests that fail those checks.
30. **P144 (medium confidence).** Challenge unauthenticated protected MCP calls and make the OAuth endpoints discoverable through authorization-server metadata, with fallback behavior only when metadata is unavailable.
31. **P145 (medium confidence).** Design token lifetime, refresh, rotation, and revocation behavior so leaked tokens have a limited damage window and user disconnects stop future agent access.
32. **P157 (high confidence).** Model the MCP server as an OAuth 2.1 resource server and the MCP client as an OAuth 2.1 client acting for a resource owner, and treat the authorization server as a separable component (co-hosted or standalone) located via metadata.
33. **P158 (high confidence).** Follow OAuth 2.1 Section 7 security best practices end to end: implement secure token storage, issue short-lived access tokens, and rotate refresh tokens for public clients.
34. **P159 (high confidence).** Advertise required scopes in the WWW-Authenticate scope parameter; clients MUST treat the challenge scopes as authoritative for the current request, MUST NOT assume any subset/superset relationship to scopes_supported, and MUST apply…
35. **P161 (high confidence).** Enforce communication security: serve all authorization-server endpoints over HTTPS, restrict every redirect URI to localhost or HTTPS, and follow OAuth 2.1 Section 1.5.
36. **P162 (high confidence).** Never accept mis-audienced tokens or pass a client-supplied token through to downstream services: audience-validation failure lets attackers reuse tokens across services and token passthrough creates confused-deputy exposure.
37. **P177 (high confidence).** Enforce token and session lifecycle management—expiration, rotation, revocation, reuse/replay control, and idempotency—rather than relying on MCP's optional authorization and unmanaged OAuth 2.1 bearer tokens.
38. **P192 (medium confidence).** When a web frontend hosts MCP authorization, keep the frontend focused on login and consent and leave the code-for-token exchange to the MCP client and token endpoint after redirect.
39. **P195 (medium confidence).** Push login, token issuance, and related authorization complexity into the MCP authorization server so the MCP resource server can stay focused on validating tokens and serving protected resources.
40. **P199 (medium confidence).** Prefer Client ID Metadata Documents for scalable MCP client identity: clients identify with controlled metadata URLs and authorization servers fetch metadata from those URLs.
41. **P207 (medium confidence).** Publish authorization-server metadata so MCP clients can discover login, token, scope, grant-type, key, client-authentication, and registration capabilities automatically.
42. **P216 (medium confidence).** Choose token-validation mechanics from the deployment topology: reuse existing validation in a combined system, or follow the external authorization server token format and validation guidance when authorization is delegated.
43. **P217 (medium confidence).** Build the IdP token-exchange request around the existing user identity assertion, the target resource authorization-server audience, the requested ID Assertion JWT token type, the assertion type, and authenticated requesting-applicati…
44. **P219 (medium confidence).** Configure an OAuth-secured MCP deployment as a coherent set: enabled connected-app behavior, supported scopes, metadata exposure, and runtime validation identifiers and key URLs.
45. **P220 (medium confidence).** At the resource authorization server, accept an ID Assertion JWT as a JWT Bearer authorization grant only after validating issuer, signature, and required assertion claims.

## Anti-patterns to flag

- Trusting server-supplied tool metadata, descriptions, schemas, or outputs as instructions.
- Accepting or forwarding a mis-audienced or client-supplied token (confused deputy / pass-through).
- Presenting one control (a single OAuth flow, one approval, protocol defaults, sandboxing alone) as complete security.
- Omitting the attack a control defends, its trade-off, or the residual risk.

## Grounding

Principles: P001, P003, P006, P007, P013, P014, P018, P020, P021, P036, P045, P058, P059, P066, P067, P076, P077, P078, P091, P101, P102, P103, P121, P123, P124, P126, P128, P135, P136, P144, P145, P157, P158, P159, P161, P162, P177, P192, P195, P199, P207, P216, P217, P219, P220. Every cited claim, evidence record, and source anchor resolves in this package's distilled spine (`analysis/claims.jsonl`, `evidence/evidence-records.yaml`, `sources/anchors/`). Sources are distillation-only: paraphrased, never quoted.
