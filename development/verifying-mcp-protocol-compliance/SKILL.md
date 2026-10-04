---
name: verifying-mcp-protocol-compliance
kind: skill
status: ready
provenance:
  principles:
  - P011
  - P016
  - P017
  - P018
  - P020
  - P031
  - P039
  - P048
  - P051
  - P062
  - P069
  - P072
  - P073
  - P076
  - P077
  - P093
  - P094
  - P096
  - P098
  - P104
  - P105
  - P106
  - P107
  - P108
  - P109
  - P110
  - P111
  - P112
  - P113
  - P114
  - P115
  - P116
  - P127
  - P128
  - P129
  - P134
  - P135
  - P136
  - P146
  - P160
  - P161
  - P162
  - P163
  - P164
  - P165
  - P166
  - P167
  - P168
  - P169
  - P170
  - P171
  - P172
  - P173
  - P174
  - P175
  - P176
  - P177
  - P178
  - P179
  - P180
  - P184
  authored_from_digest: 3db8e1aa2058d2758617517e8132aa8d2c2d6cf2feed38982f9c2ea0b7c9e9d4
---

# Skill: verifying-mcp-protocol-compliance

## Purpose

Verify that an MCP server is protocol-compliant and debuggable at runtime, not only at build time:
the initialize handshake, JSON-RPC 2.0 conformance, transport binding, capability negotiation,
structured error objects, and Inspector / validator / SDK-test coverage [P096], [P069], [P116].

## When to use

- Confirming a server conforms to the MCP specification and its advertised capabilities.
- A client cannot connect, negotiate, or invoke a capability, and you need an ordered diagnosis.
- Building conformance tests, an Inspector session, or SDK-based in-memory tests.

## Procedure

1. **Validate the full compliance surface.** Check the initialize handshake, JSON-RPC 2.0 conformance,
   advertised capabilities (tools/prompts/resources), and structured errors; gate request handling on a
   completed initialization handshake and declare every capability you use at initialize [P096], [P127], [P114].
2. **Respect validator dependency order and never fake a pass.** `protocol` is the foundation validator
   others depend on; never report a missing prerequisite as SKIPPED, because SKIPPED counts as green in
   pass counts, exit codes, and baselines [P116], [P164].
3. **Keep the protocol channel clean.** On stdio, emit only valid JSON-RPC on the message stream — route
   diagnostic and other non-protocol output elsewhere; preserve request/response and session identifiers
   consistently [P016], [P094].
4. **Represent failures as structured errors.** Map tool and server failures to correct JSON-RPC error
   objects; for a failing tool, return `is_error=True` with the message in `content` and read a
   `CallToolResult` as its separate fields [P073], [P093], [P098].
5. **Verify behaviourally at runtime.** A server can compile and match its spec yet still violate
   coordination at runtime — exercise each advertised capability through the connected client session,
   page every list call with a cursor loop, and configure timeouts and cancellation [P069], [P017], [P018], [P020].
6. **Use the Inspector and the SDK test harness.** Reach for the MCP Inspector first (match the launch
   wrapper to how the server is distributed); use InMemoryTransport for in-process unit/integration tests
   and drive the client through its async context manager [P170], [P107], [P115], [P173].
7. **Work connection failures as an ordered checklist.** Client logs → server process → standalone
   Inspector test → protocol-version compatibility → capability negotiation; use absolute paths in config
   and rely on automatic protocol-version negotiation [P175], [P111], [P179].

## Pitfalls / anti-patterns

- Treating a clean build as proof of compliance [P069].
- Emitting logs or diagnostics onto the stdio JSON-RPC stream, corrupting the transport [P016].
- Reporting an un-runnable check as SKIPPED, letting it count as passing [P164].

## Principles applied

- **[P011]** Persist intermediate state, reusable task code, and agent memory outside the transient prompt when workflows need resume capability, repeated execution, continuity, provenance, or auditability.
- **[P016]** Keep diagnostic and other non-protocol output off the JSON-RPC message stream; on the stdio transport, emitting anything other than valid JSON-RPC on standard output corrupts the stream and breaks client parsing.
- **[P017]** Exercise tools through the connected client session and assert both model-facing text content and machine-readable structuredContent, calling listTools first when schema validation depends on cached tool schemas.
- **[P018]** Page every MCP list call with a cursor loop, collecting results until the response has no next cursor rather than assuming the first page is complete.
- **[P020]** Configure timeouts for long-running or streaming operations so active progress prevents premature timeout while cancellation and stream termination still resolve cleanly.
- **[P031]** Derive MCP conformance tests and fault-injection scenarios directly from the leaf fault categories (for example, verifying that timeout violations yield structured error objects, undeclared tool identifiers are rejected, and requests are not processed before initialization completes), and ground reliability benchmarks in observed protocol-level faults rather than generic software bugs.
- **[P039]** Attach runtime validator contracts that check spatial dimensions, tensor channel semantics, and coordinate alignment, and let agents halt, replan, or fall back on invariant violation; schema agreement alone does not prevent scale, modality, or layout failures.
- **[P048]** Persist intermediate visual state in explicit, versioned, semantically namespaced memory with temporal scoping and provenance; undocumented or weak memory scoping is prevalent and produces stale-state warnings.
- **[P051]** Wire progress reporting end-to-end only when requested: the client supplies an onprogress callback/progress token and the server emits progress notifications guarded by that token.
- **[P062]** Design an MCP server for a large-API platform as a capability-oriented interface: expose a small set of generic verb tools and put the intelligence in a declarative registry that maps each resource type to its API operations, rather than wrapping one tool per endpoint.
- **[P069]** Verify MCP servers at the protocol-runtime level, not only at build time: a server can compile successfully and conform to its specification yet still violate its coordination obligations at runtime, so build success and spec conformance do not imply correct runtime behavior.
- **[P072]** Detect MCP faults behaviorally, not only via crashes or explicit errors: many faults return well-formed JSON-RPC success responses while violating coordination semantics (silent/gray failure), so oracles must assert response content, session-state consistency, and the occurrence of required notification events across interaction steps.
- **[P073]** Represent tool and server failures as structured JSON-RPC error objects mapped to the correct error code; never return a success response that carries hidden failure information, and never surface application failures as bare HTTP status codes.
- **[P076]** For multi-server or complex setups, store servers in a --config file (transport auto-detected), rely on automatic selection when there is a single server or one named 'default-server', use the Server Entry / Servers File export to generate mcp.json, and remember query params override localStorage while MCP_AUTO_OPEN_ENABLED is settable only as an env var.
- **[P077]** Choose the transport explicitly and supply its required endpoint and authentication: stdio is the default; HTTP needs --endpoint plus OAuth 2.0 (automatic Dynamic Client Registration, pre-registered credentials, or a personal access token); SSE needs --endpoint plus a Bearer token.
- **[P093]** Treat a failing tool as an ordinary result with `is_error=True` (the exception message is placed in `content` for the model), always check `is_error` before trusting `structured_content` (which is `None` on failure), and remember a Client method raises `MCPError` only when the server returns a JSON-RPC error rather than a result.
- **[P094]** Preserve request-response and session identifiers consistently across message exchange, tool invocation, and result propagation, so requests, results, and related streaming events stay correlated.
- **[P096]** Validate the full MCP compliance surface — the initialize handshake, JSON-RPC 2.0 conformance, advertised capabilities (tools/prompts/resources), security, and registry/OSS conformance — rather than checking connectivity alone.
- **[P098]** Read a `CallToolResult` as three separately-consumed fields — `content` for the model, `structured_content` (JSON matching the tool's output_schema) for application code, and `is_error` for success — and do not conflate the model-facing and code-facing halves.
- **[P104]** OAuth client scopes and registration: with offline_access in the AS scopes_supported a client SHOULD include refresh_token in grant_types (and MAY include offline_access in the request scope); when the server lacks DCR it MUST use pre-registered credentials via context; it should follow the WWW-Authenticate scope from the 401; and it validates the iss parameter when the server advertises it.
- **[P105]** Select the Client transport by the type of its single positional argument: an MCPServer/Server instance for in-process, a URL string for Streamable HTTP, or a transport object (usable as `async with ... as (read, write)`) for anything else.
- **[P106]** Assess SDK tier gates from the required conformance pass rates, triage and P0 responsiveness, stable release status, documentation, dependency policy, and roadmap obligations for Tier 1 or Tier 2; otherwise classify the SDK as Tier 3.
- **[P107]** Match the Inspector launch wrapper to how the server is distributed: `npx <pkg>` for an npm package, `uvx <pkg>` for a PyPI package, `node <entry>.js` for a local TypeScript server, and `uv --directory <path> run <pkg>` for a local Python server.
- **[P108]** In an Inspector session, first verify connectivity and capability negotiation, then exercise each advertised capability surface through its dedicated tab with real inputs and observed results.
- **[P109]** When constructing tool-call requests from form inputs, omit optional fields with empty values unless the schema defines a matching explicit default, preserve explicit defaults (e.g. default: null) that match the current value, always include required fields even when empty, and defer deep parameter validation to the MCP server.
- **[P110]** Design the CLI test suite for safe parallelism: run in parallel across files but sequentially within a file, make each config file unique with crypto.randomUUID(), allocate HTTP/SSE ports dynamically, depend only on built-in MCP test servers, and do not expect coverage numbers because subprocess-run code is untrackable by Vitest.
- **[P111]** Always use absolute paths in server configuration, .env files, and the command executable, because a client-launched stdio server's working directory may be undefined (e.g. / on macOS).
- **[P112]** Use the SDK's built-in ping() for health checks, adding an explicit timeout or deadline when the side being called does not provide one.
- **[P113]** Make long-running calls cancellable end-to-end: the client passes and aborts an AbortSignal, and the server handler polls the signal and stops promptly when cancellation is signalled.
- **[P114]** Declare every capability you will use at initialize (client capabilities in the Client constructor; server capabilities inferred by McpServer from registered handlers, or declared on the low-level Server) — the SDK throws when code uses an undeclared capability.
- **[P115]** Use InMemoryTransport for unit, integration, test, and development in-process MCP wiring, reserving stdio, Streamable HTTP, or local server URLs for transport-level or production paths.
- **[P116]** Treat `protocol` as the mandatory foundation validator and respect validator dependency order (capabilities, ping, errors, security all depend on it); extend validation through the plugin model instead of ad-hoc checks.
- **[P127]** Gate request handling on completion of the initialization handshake so no request is processed before the session is fully initialized; because initialization instability spans several startup steps, expect to harden the whole startup sequence rather than a single step.
- **[P128]** When reviewing MCP state and configuration, check that server-level configuration parameters are actually enforced rather than accepted and silently ignored, that session identifiers are neither stale, reused, absent, nor stripped by middleware, and that server-managed resource state is persisted and kept fresh across operations.
- **[P129]** When reviewing MCP security, check authentication (Authorization header present, token well-formed and unexpired), token validation (token audience and other claims verified on receipt, tokens not forwarded upstream unverified), and authorization (access-control checks enforced after authentication before executing capabilities or tool invocations).
- **[P134]** Emit a structured, timestamped aggregated report: one JSON report per server (named <server>.json under output/), an aggregate servers_validation.json, and a Markdown summary table of per-server status/errors/warnings — recording Name, Command, Status, counts, and report file, and adding an Error_Message on failures.
- **[P135]** Make logging load-bearing and structured: instrument initialization, resource access, tool execution, errors, and performance; use consistent formats, context, timestamps, and request IDs; log stack traces and track error patterns, recovery, timing, resource usage, message sizes, and latency.
- **[P136]** Configure validation reproducibly through named profiles, a .mcp-validation.json config file, or the MCP_VALIDATION_CONFIG / MCP_VALIDATION_PROFILE environment variables (and tune validator parameters there) instead of ad-hoc one-off flags.
- **[P146]** Keep mcp-scan security analysis enabled by default; use --skip-mcp-scan only when speed matters and security is out of scope, and ensure mcp-scan is installed (or explicitly disable the security validator) so runs do not silently lose security coverage.
- **[P160]** Understand the client-mode harness contract: the framework starts a test server for the scenario, appends the server URL as the client's final argument, sets MCP_CONFORMANCE_SCENARIO (and MCP_CONFORMANCE_CONTEXT with scenario data such as credentials), then captures and checks the protocol interactions.
- **[P161]** Model an SDK's example conformance server on the reference everything-server: implement the full feature surface (tools, resources, prompts, all log levels, completion, list-changed, subscribe/update), use the standardized names (test_ prefix for tools/prompts, test:// for resources), and reproduce its automatic behaviors (dynamic registration about 2s after start, watched-resource update about every 3s) so one suite verifies every SDK.
- **[P162]** Read the traceability manifest correctly: it is generated from a real reference-SDK run (so dynamic check IDs resolve), tested means the check ID was emitted (not that any SDK passes — that is tier-check), and a SEP absent from it has no conformance artifacts and is not-started.
- **[P163]** Give a check one slug shared by its SUCCESS and FAILURE outcomes (flip status and errorMessage), optimize the code for Ctrl+F on that slug (repetition beats a clever helper), and reuse ConformanceCheck and other shared types rather than parallel shapes.
- **[P164]** Never report a missing prerequisite as SKIPPED: because SKIPPED counts as green in pass counts, exit codes, and baselines, a check that cannot be exercised (missing fixture, rejected probe, undeclared feature) must FAIL via notTestable()/untestableCheck() naming the missing prerequisite; reserve SKIPPED for genuinely inapplicable checks.
- **[P165]** Import protocol types from the vendored spec-types version that matches the scenario or connection lifecycle, and refresh those generated files rather than hand-editing them.
- **[P166]** MCP request-header validation (server, SEP-2243): reject a request whose Mcp-Method or Mcp-Name header disagrees with the body (or is missing for a name-carrying body) with HTTP 400 and JSON-RPC -32020 (HeaderMismatch); treat header names case-insensitively but values case-sensitively, accept optional whitespace around Mcp-Name per RFC 9110 section 5.5, and reject a request where a custom header is omitted while its value is present in the body.
- **[P167]** Author traceability YAML by mapping each spec-diff normative sentence exactly to a check or excluded reason, leaving to-do rows for ambiguity and flagging paraphrases or unsupported keyword levels.
- **[P168]** Launch the Inspector via npx without cloning its repository (Node.js ^22.7.5 required): pass server arguments directly, set the server's environment variables with -e, and separate inspector flags fro.
- **[P169]** Treat the MCP Inspector as two cooperating parts — the MCPI React web UI and the MCPP Node.js protocol-bridge (an MCP client plus HTTP server spanning stdio, SSE, and streamable-http) — and do not mistake the proxy for a traffic-intercepting network proxy.
- **[P170]** Reach for the MCP Inspector first: use it as an interactive, transport-agnostic way to invoke a server's tools, prompts, and resources and watch its notification stream before deeper debugging.
- **[P171]** Rely on the proxy's default Bearer-token authentication — supplying the token non-interactively via MCP_PROXY_AUTH_TOKEN when automating — and never disable it with DANGEROUSLY_OMIT_AUTH, which enables browser-driven remote compromise (CVE-2025-49596).
- **[P172]** Treat Inspector timeouts (MCP_SERVER_REQUEST_TIMEOUT default 300000 ms; MCP_REQUEST_MAX_TOTAL_TIMEOUT default 60000 ms) as client-side cancels independent of server-side timeouts — whichever elapses first wins — and raise them for elicitation or long-running tools.
- **[P173]** Drive an MCP Client entirely through `async with Client(...)`: entering the block connects and negotiates and leaving it disconnects, so never call a connect()/close() pair and never reuse a Client after its block has exited.
- **[P174]** Use CLI mode for scripting, automation, CI/CD, and coding-assistant feedback loops — invoking tools, resources, and prompts via --method with --tool-arg key=value or JSON — and select remote transport and headers explicitly (SSE by default, --transport http for streamable HTTP, --header for custom headers).
- **[P175]** Work a connection failure as an ordered checklist (client logs, server process, standalone Inspector test, protocol-version compatibility, capability negotiation); treat a -32602 Invalid params error as a likely undeclared-capability mismatch and inspect the initialize exchange.
- **[P176]** Configure the async backend for asynchronous MCP tests: provide an anyio_backend fixture returning "asyncio" (or "trio" when running on trio) and mark async test functions with @pytest.mark.anyio.
- **[P177]** Read connection facts from the four read-only properties populated on entering the block — server_info, server_capabilities, protocol_version, instructions — and treat a `None` capability as 'server l.
- **[P178]** Discover prompts with `list_prompts()` (name, title, required arguments), render one with `get_prompt(name, arguments)` passing a string-to-string arguments dict (prompt arguments are always strings), and hand the returned `messages` (role + content block) straight to the model.
- **[P179]** Rely on the SDK's automatic protocol-version negotiation (client sends LATEST_PROTOCOL_VERSION, server returns the highest mutually supported version from SUPPORTED_PROTOCOL_VERSIONS) but handle the error the client throws when the server's version is unsupported.
- **[P180]** Establish the in-memory connection by running both client.connect() and server.connect() concurrently (e.g. await Promise.all([...])); never connect only one side or await the two connects sequentially, which deadlocks the initialize handshake.
- **[P184]** When reviewing MCP tool handling, check tool identification (tools declared in the capabilities object with valid input/output schemas so they are discoverable and callable), tool execution (input types validated, execution terminates, runtime errors surfaced as error objects), and tool result propagation (result payload present, correctly structured, no success response masking a tool failure, no result-visibility races).

Sources are distillation-only: this skill paraphrases and restructures; no verbatim source quotation.

