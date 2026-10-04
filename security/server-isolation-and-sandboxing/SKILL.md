---
name: server-isolation-and-sandboxing
kind: skill
status: ready
provenance:
  principles:
  - P008
  - P017
  - P019
  - P022
  - P023
  - P026
  - P030
  - P038
  - P042
  - P051
  - P056
  - P064
  - P068
  - P070
  - P071
  - P072
  - P073
  - P080
  - P086
  - P099
  - P100
  - P114
  - P125
  - P133
  - P137
  - P153
  - P154
  - P163
  - P166
  - P172
  - P173
  - P176
  - P178
  - P181
  - P193
  - P208
  claims:
  - C00002
  - C00003
  - C00110
  - C00111
  - C00126
  - C00127
  - C00156
  - C00157
  - C00174
  - C00175
  - C00179
  - C00180
  - C00186
  - C00204
  - C00206
  - C00207
  - C00236
  - C00239
  - C00243
  - C00244
  - C00249
  - C00267
  - C00268
  - C00316
  - C00317
  - C00358
  - C00359
  - C00372
  - C00373
  - C00374
  - C00375
  - C00392
  - C00393
  - C00401
  - C00402
  - C00656
  - C00657
  - C00668
  - C00669
  - C00693
  - C00703
  - C00704
  - C00819
  - C00820
  - C00878
  - C00880
  - C00902
  - C00903
  - C00906
  - C00907
  - C00953
  - C00954
  - C00963
  - C00964
  - C01102
  - C01103
  - C01188
  - C01194
  - C01195
  - C01210
  - C01211
  - C01218
  - C01227
  - C01228
  - C01266
  - C01267
  - C01272
  - C01273
  - C01285
  - C01333
  - C01338
  evidence:
  - E00001
  - E00002
  - E00091
  - E00092
  - E00104
  - E00105
  - E00127
  - E00128
  - E00141
  - E00142
  - E00146
  - E00147
  - E00153
  - E00171
  - E00173
  - E00174
  - E00199
  - E00201
  - E00205
  - E00206
  - E00208
  - E00216
  - E00217
  - E00261
  - E00262
  - E00303
  - E00304
  - E00317
  - E00318
  - E00319
  - E00320
  - E00336
  - E00337
  - E00344
  - E00345
  - E00521
  - E00522
  - E00529
  - E00530
  - E00546
  - E00556
  - E00557
  - E00659
  - E00660
  - E00695
  - E00697
  - E00712
  - E00713
  - E00716
  - E00717
  - E00756
  - E00757
  - E00766
  - E00767
  - E00831
  - E00832
  - E00875
  - E00879
  - E00880
  - E00889
  - E00890
  - E00896
  - E00905
  - E00906
  - E00926
  - E00927
  - E00931
  - E00932
  - E00937
  - E00961
  - E00964
  source_anchors:
  - 2c66587b05e5-c0000
  - 2c66587b05e5-c0001
  - 2c66587b05e5-c0002
  - 347696d03493-c0000
  - 347696d03493-c0001
  - 347696d03493-c0003
  - 38612cf35377-c0000
  - 457ef5c30a3b-c0002
  - 515304c317e3-c0000
  - 515304c317e3-c0001
  - 515304c317e3-c0002
  - 6ff87e35998d-c0000
  - b5eaaf20d167-c0000
  - ceb67441a627-c0000
  - ceb67441a627-c0001
  - ceb67441a627-c0003
  - cf7957044f40-c0000
  - d59e5c41ce9d-c0000
  - d59e5c41ce9d-c0001
  - dcbba5b2c9ad-c0000
  - e6ab8dd9a85c-c0000
  - fa0ccb38ff81-c0000
  - fa0ccb38ff81-c0002
  authored_from_digest: 3acb1877057960f295623d911794e33a231cbf3a9889495b86dc4e77306467da
---

# Server Isolation and Sandboxing

Isolate MCP servers by deployment pattern — sandboxing, TEEs, transport and session hardening, SSRF and DNS-rebinding defence, and mediated cross-server and cross-tenant data flows.

This skill packages 36 grounded principles the mcp-security-advisor applies when this surface is in scope. Each finding names the weakness, the attack it enables, the control, and the trade-off or residual risk.

## When this applies

- MCP servers are exposed through remote HTTP or SSE transports and track user sessions or tokens.
- An MCP server exposes tools whose execution reaches sensitive operations.
- MCP traffic needs identity binding, message integrity, replay protection, or cryptographic audit evidence.
- MCP messages pass through proxies, middleware, host agents, or other components that could alter payloads after transport protection terminates.
- Message signing or replay protection is configured for an MCP channel.
- Developing or selecting the transport for an MCP server.
- choosing or reviewing an MCP server or client transport.
- an MCP server interacts with the host or runs model-generated code.
- MCP triggers shell commands, database queries, or external API calls.
- choosing an MCP HTTP transport.
- choosing a transport for a new or updated MCP client.
- Deploying or reviewing MCP servers that run on a local host.
- When MCP servers can initiate outbound network or file-like requests.
- MCP context, embeddings, retrieval indexes, memory, prompts, reasoning traces, or interaction history may persist or be reused across identities, workflows, trust domains, departments, or tenants.
- selecting and hardening a specific MCP deployment pattern.
- Designing MCP HTTP, WebSocket, SSE, proxy, credential, or session controls.

## Procedure

Apply the principles below in order of the risk they carry, highest first. For each one in scope: identify where untrusted data, a token, or an authorization decision enters, name the attack it enables, apply the control, and state the trade-off or residual risk. Never weaken a defence below what the source and the MCP specification support, and never present a single control as complete MCP security.

1. **P008 (high confidence).** Bind every MCP authorization decision to the identity of the caller that triggers the invocation, and re-authorize when a new caller interacts; authorization enforced only at the server or resource level, without being scoped to the c…
2. **P017 (high confidence).** Use a cryptographic MCP message envelope to bind JSON-RPC traffic to agent identity, message integrity, timestamp freshness, nonce-based replay resistance, and auditability, while pairing it with application-layer controls for command…
3. **P019 (high confidence).** Select MCP transport by deployment target: stdio for local servers (low-latency, no network overhead) and HTTP/S with streaming for remote servers (adds standard authentication); do not assume one transport fits both.
4. **P022 (high confidence).** Run agents and MCP servers with least privilege, always sandbox any server that touches the host (files, commands, network) or executes LLM-generated code, and do not rely on containers alone as a security boundary—add stronger isolat…
5. **P023 (high confidence).** Do not adopt or standardize on the SSE-over-HTTP transport: it is deprecated in the MCP specification (and client migration to the recommended streamable HTTP transport lags), so use streamable HTTP instead.
6. **P026 (high confidence).** Run local MCP servers inside isolation boundaries and restrict their filesystem and network access to the minimum required for their intended function.
7. **P030 (high confidence).** Treat MCP context as a boundary-sensitive asset and enforce strict context isolation and lifecycle controls with per-user, per-agent, per-workflow, and per-tenant namespaces, isolated retrieval stores, sensitivity tagging, TTL and pur…
8. **P038 (high confidence).** Harden according to the deployment pattern: for all-local use stdio transport (which eliminates DNS-rebinding risk) plus sandboxing; for single-tenant remote require client-server authentication, secure OS-keychain/secret-manager cred…
9. **P042 (medium confidence).** Protect MCP transport and sessions with endpoint authentication, secure credential storage, audience-bound tokens, short-lived sessions, rotation, invalidation, and session observability.
10. **P051 (high confidence).** Because authorization correctness in MCP servers is an execution-time property, complement static analysis with selective dynamic validation: issue controlled invocations to resource-affecting paths and interpret success without an au…
11. **P056 (medium confidence).** Constrain MCP runtime environments and external resource access with isolation, least privilege, authentication, authorization, sandboxing, trusted bindings, filesystem roots, outbound network filters, and parameter validation.
12. **P064 (high confidence).** Enforce transport-layer controls matched to the transport in use: payload limits and integrity checks on all transports; client-server and downstream authentication, mutual TLS, TLS encryption, plus CORS and CSRF protection on HTTP tr…
13. **P068 (high confidence).** Close the stdio proxy escalation path by eliminating its enabling vulnerabilities (OAuth URL validation, CSP, input sanitization) and hardening the proxy itself: sandbox/containerize spawned processes, restrict their filesystem access…
14. **P070 (high confidence).** Use agent passports, trust levels, capability lists, mutual authentication, revocation, and self-hostable trust authority operations to bind MCP agent identity, permissions, and server acceptance to verifiable credentials.
15. **P071 (high confidence).** Use hardware TEEs with remote attestation to isolate MCP clients and servers from compromised hardware, malicious infrastructure operators, and co-tenancy threats, rejecting shadow or compromised servers whose measurements fail attest…
16. **P072 (high confidence).** Identify the security-relevant tool entry as the moment a protocol-level tools/call invocation commits to concrete execution — not an exported function or callback — because MCP dispatch is dynamic and implementation-specific (name-to…
17. **P073 (high confidence).** Prevent cross-tenant leakage through shared efficiency optimizations: sharing key-value caches or vector indexes across tenants creates covert side channels even without an explicit bug (the PROMPTPEEK attack reconstructs another user…
18. **P080 (medium confidence).** Cloud-hosted MCP deployments must pair scaling convenience with managed authentication, scoped authorization, secure session state, privacy controls, data residency handling, latency design, tenant isolation, and runtime sandboxing.
19. **P086 (medium confidence).** Prevent privilege persistence by revoking credentials during updates, synchronizing privilege changes, expiring versioned sessions, validating tokens centrally, and supporting explicit revocation events.
20. **P099 (high confidence).** Treat MCP authorization as optional, but when it is used apply this specification to HTTP-based transports (SHOULD conform), keep STDIO transports on environment-supplied credentials (SHOULD NOT use this flow), and require established…
21. **P100 (high confidence).** Enforce authentication and role-based access control (including CRUD-level permissions) on MCP components and bind each session to an identity, since MCP leaves identity and RBAC optional and many implementations omit them.
22. **P114 (high confidence).** Flag any MCP tool that passes tool parameters into a system-command invocation without authentication, caller verification, or input sanitization: it becomes an unauthenticated remote-command-execution endpoint running at the server p…
23. **P125 (medium confidence).** Do not rely on the MCP protocol itself for security guarantees; add authentication, authorization, and transport controls in the host, client, and server implementation.
24. **P133 (medium confidence).** Isolate MCP servers with explicit cross-server dataflow and authority boundaries instead of giving all connected servers unrestricted influence in one agent context.
25. **P137 (medium confidence).** Use system-level enforcement (sandboxing, mandatory access control, capability-based execution, or container isolation) to limit the blast radius of unauthorized tool invocations, but recognize it is coarse-grained, does not address t…
26. **P153 (medium confidence).** For action-capable MCP assistants and IDE integrations, evaluate data compatibility, permission management, isolation, distributed-call latency, and tool chaining risk.
27. **P154 (medium confidence).** Assess security impact with a resource-centric view: classify each tool invocation by the type of resource it ultimately affects — system-level execution, persistent data access, network or external communication, or physical/human-in…
28. **P163 (high confidence).** When sessions are used for state, make session IDs secure random values (e.g., UUIDs from a CSPRNG), bind them to user-specific identity such as <user_id>:<session_id>, and rotate or expire them to limit hijacking impact.
29. **P166 (high confidence).** Establish explicit trust boundaries/zones between MCP components, gate dynamic tool discovery behind origin verification or authorization, align tools and models to data-classification zones, prefer local MCP servers for private data,…
30. **P172 (high confidence).** Secure MCP deployments with defense-in-depth—zero-trust architecture, hardware isolation via TEEs, rigorous supply-chain vetting, and continuous monitoring—because documented incidents show that failures of authentication, session man…
31. **P173 (high confidence).** Do not rely on MCP protocol guarantees for security; enforce it through implementation rigor and standard external controls (reverse proxies, middleware firewalls, application sandboxing/containment), because the protocol cannot enfor…
32. **P176 (high confidence).** Execute agent-produced commands, queries, file operations, and API calls only through validated tool boundaries that use allowlists, metacharacter rejection, path normalization, structured APIs, parameterization, sandboxing, least pri…
33. **P178 (high confidence).** Design MCP servers so the initialize phase is the sole entry point for session creation: bind the OAuth token, caller identity (for example client_id), and connection context into an isolated per-connection session, verify the caller…
34. **P181 (high confidence).** Treat sensitive-API usage as a first-class audit surface for MCP servers, scanning for five threat classes - network request (exfiltration or SSRF), code execution (eval, exec, Function), system command (os.system, subprocess, child_p…
35. **P193 (medium confidence).** Require an authorization design whenever an MCP server accesses protected remote services; do not assume the MCP server process identity is enough.
36. **P208 (medium confidence).** Apply heightened review before connecting third-party MCP servers in contexts that contain credentials, sensitive files, or sensitive external services.

## Anti-patterns to flag

- Trusting server-supplied tool metadata, descriptions, schemas, or outputs as instructions.
- Accepting or forwarding a mis-audienced or client-supplied token (confused deputy / pass-through).
- Presenting one control (a single OAuth flow, one approval, protocol defaults, sandboxing alone) as complete security.
- Omitting the attack a control defends, its trade-off, or the residual risk.

## Grounding

Principles: P008, P017, P019, P022, P023, P026, P030, P038, P042, P051, P056, P064, P068, P070, P071, P072, P073, P080, P086, P099, P100, P114, P125, P133, P137, P153, P154, P163, P166, P172, P173, P176, P178, P181, P193, P208. Every cited claim, evidence record, and source anchor resolves in this package's distilled spine (`analysis/claims.jsonl`, `evidence/evidence-records.yaml`, `sources/anchors/`). Sources are distillation-only: paraphrased, never quoted.
