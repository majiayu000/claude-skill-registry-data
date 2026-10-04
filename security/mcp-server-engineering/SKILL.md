---
name: mcp-server-engineering
description: Design, audit, harden, review, or upgrade MCP servers and MCP Apps with revision-aware protocol profiles, explicit HTTP/deployment boundaries, capability-centered validation, bilingual reporting, and reproducible evidence. Use for MCP server architecture, JSON-RPC or Streamable HTTP bugs, security hardening, protocol-version migration, MCP Apps widget boundaries, review reconciliation, test planning, and public engineering evidence.
---

# MCP Server Engineering

Build or review the real runnable contract of an MCP server. Separate stable engineering invariants from revision-specific protocol rules, transport behavior, deployment policy, and host integration guidance.

Match the user's language. When writing Chinese, use natural Chinese prose while preserving exact English protocol terms, identifiers, headers, methods, error names, commands, and file paths.

## Choose the work mode

Classify the request before loading references:

- **design** — define capabilities, state, transport, deployment, and evidence before implementation;
- **audit** — inspect a pinned implementation and report evidence-backed findings without changing it unless asked;
- **patch-review** — inspect a proposed hardening diff, reproduce findings, implement authorized fixes, and verify regressions;
- **spec-upgrade** — compare the declared revision with a target revision and replace superseded protocol behavior deliberately.

If the user asks for more than one mode, sequence them explicitly. Do not turn an audit request into an unrequested patch or public disclosure.

## Preflight the authority boundary

Before judging behavior, establish:

1. canonical source root, branch, and exact revision;
2. declared MCP revision and any supported compatibility revisions;
3. transport: stdio, Streamable HTTP, custom, or multiple;
4. public entry points and the capability each can reach;
5. intended reachability: subprocess, loopback, LAN, private tunnel, authenticated remote, or public;
6. framework/runtime owner of header parsing, body parsing, task/thread admission, response writing, and cancellation;
7. proxy, tunnel, TLS, authentication, and host owners;
8. whether the task authorizes local edits, dependencies, deployment, public communication, or only read-only review.

Use `unknown` / `未验证` when source or runtime evidence is missing. A variable name, test name, comment, or README promise is not runtime proof.

## Select the protocol profile

Read [references/protocol-selection.md](references/protocol-selection.md).

Always load the base [JSON-RPC 2.0 profile](references/json-rpc-2.0.md). If Streamable HTTP or another HTTP wrapper is in scope, also load the [HTTP RFC 9110 / RFC 9112 profile](references/http-rfc9110-rfc9112.md).

For **audit** or **design**, load the one MCP profile matching the declared or selected revision:

- [references/mcp-2025-06-18.md](references/mcp-2025-06-18.md)
- [references/mcp-2025-11-25.md](references/mcp-2025-11-25.md)
- [references/mcp-2026-07-28.md](references/mcp-2026-07-28.md)

For **spec-upgrade**, load both the declared source profile and the target profile. Compare them explicitly, then inventory behavior to preserve, replace, and retire with [assets/templates/upgrade-retirement-inventory.md](assets/templates/upgrade-retirement-inventory.md). Apply target requirements to the proposed target implementation, not retroactively to the historical baseline.

When current MCP Apps or named-host compatibility is claimed, separately load the dated [integration guidance profile](references/integration-guidance-2026-08-15.md) and recheck its moving official sources. When working in Chinese, use the matching `.zh-CN.md` profile peer.

Rules:

- Review historical servers against the revision they claim.
- When the user asks for “latest,” verify the current official revision before relying on the bundled assessed profile.
- Do not condemn a historical initialize/session flow merely because a later revision removed it.
- Do not bless current design with historical rules merely because an SDK still supports them.
- Treat version migration as behavior replacement, not a version-constant edit.

## Model capabilities before transports

For every externally reachable action, record:

- capability and owner;
- caller identity or possession claim;
- arguments and schema;
- reads, writes, network access, subprocesses, or other effects;
- concurrency and durable state;
- resource budgets;
- retry, idempotency, and cancellation semantics;
- model-visible, component-visible, user-visible, and operator-visible outputs;
- all routes/transports that can invoke it.

Use [assets/templates/threat-model.md](assets/templates/threat-model.md) when a durable artifact helps. Equivalent REST, MCP, UI bridge, or internal routes must converge on one capability authority unless a documented product reason requires different permissions.

For Chinese output, use the matching `.zh-CN.md` template peer where present.

## Inspect the enforcement partial order

Read [references/core-invariants.md](references/core-invariants.md). For Streamable HTTP, especially a direct-socket, standard-library, or thin-framework HTTP server, also read [references/http-low-level-server.md](references/http-low-level-server.md).

For pure stdio owned by a parent process, begin at the parent/SDK framing and dispatch boundary. Mark HTTP Host, Origin, CORS, request-target, socket admission, and HTTP body-framing controls `not applicable` unless an HTTP wrapper is separately in scope.

Trace the real order, including framework-owned steps:

```text
header completion
  -> request-target / authority / framing / early policy
  -> bounded body consumption
  -> strict decode and JSON
  -> revision and JSON-RPC classification
  -> method / authorization / arguments / resource limits
  -> capability effect
  -> projection / serialization / bounded write
  -> disconnect / retry / cancellation handling
```

This is a dependency map, not a claim that every framework exposes one linear hook. A control cannot protect resources or authority already consumed before its enforcement point.

Inspect pre-dispatch behavior explicitly, including `Expect: 100-continue`, header timeouts, connection/thread admission, framework parsers, proxy normalization, and automatic exception logging.

## Separate control families

Do not merge these into one vague “security layer”:

- bind/reachability;
- Host/effective authority;
- Origin validation;
- CORS response policy;
- authentication;
- authorization and scopes;
- framing/body/parser budgets;
- connection admission;
- capability rate/concurrency limits;
- state locking and effect identity;
- result size/write/backpressure;
- deployment TLS/proxy/tunnel policy.

Name what each control protects and where it runs. A tunnel changes reachability. It does not validate tool arguments or make an unsafe parser safe. A capability semaphore acquired after body parsing does not cap incomplete connections.

## Audit evidence, not intent

Read [references/evidence-discipline.md](references/evidence-discipline.md). Build a claim ledger with:

- claim ID;
- public or code-level assertion;
- source location;
- required proof boundary;
- observed evidence;
- status: verified, contradicted, unknown, or not applicable;
- residual risk;
- provenance: `original-observation`, `reproduced`, or `independently-reproduced`.

Use [assets/templates/finding.md](assets/templates/finding.md), [assets/templates/claim-ledger.md](assets/templates/claim-ledger.md), and [assets/templates/evidence-receipt.json](assets/templates/evidence-receipt.json).

Never promote:

- static inspection into runtime proof;
- localhost success into proxy/tunnel/host acceptance;
- process existence into service correctness;
- implementer-authored tests into independent assurance;
- a reviewer's confident inference into an observed fact;
- a sanitized receipt into an independent execution.

## Handle MCP Apps as two interactive consumers with multiple projections

When tools return UI resources or widgets, read [references/mcp-apps.md](references/mcp-apps.md).

Audit separately:

- model-visible content;
- structured data delivered to the component;
- UI-only metadata;
- HTML/DOM rendering and escaping;
- `postMessage` origin/source/message validation;
- widget-to-host tool authority;
- CSP and external resources;
- UI resource URI version/cache identity;
- ephemeral UI state versus authoritative durable state;
- shared MCP Apps behavior versus host-specific compatibility extensions.

Do not call a host-specific bridge portable. Feature-detect extensions and retain a useful non-UI path when the product promises one.

## Design or apply fixes

Prefer the smallest architecture that satisfies the real contract:

- remove fake session/SSE/state claims if the product does not need them;
- centralize capability validators and resource budgets;
- keep transport envelopes separate from capability logic;
- make annotations and docs match real side effects;
- preserve product prompts, UI, and behavior when hardening transport unless change is authorized;
- do not invent partial OAuth, proxy identity, tenancy, or idempotency mechanisms;
- do not add dependencies or frameworks without a concrete requirement;
- remove superseded active paths during a revision upgrade instead of leaving two ambiguous implementations.

For a revision upgrade, record each relevant route/method, header, state store, background task, compatibility adapter, test fixture, documentation claim, and deployment setting as `retained`, `replaced`, `retired`, or `not-applicable`. A target-path test does not prove the superseded path is gone.

If the required control belongs to a proxy, host, authorization server, or deployment owner, state that boundary. Do not simulate an unenforceable control in application code.

## Verify at the narrowest real boundaries

Create a matrix from [assets/templates/test-matrix.md](assets/templates/test-matrix.md). Cover relevant layers:

1. pure capability/validator tests;
2. JSON-RPC and revision classifier tests;
3. HTTP handler/integration tests;
4. raw socket tests for pre-dispatch and wire-order claims;
5. real-process smoke;
6. container/proxy/tunnel tests when claimed;
7. actual host/component rendering when compatibility is claimed;
8. independent review focused on seams not already encoded in tests.

Test failure paths and negative space: malformed envelope, notification side effect, duplicate framing, incomplete body, slow trickle, invalid authority, denied Origin, auth metadata mismatch, capture failure, concurrent state, disconnect after effect, result overflow, and removed-feature absence.

Stop once evidence is sufficient for the requested boundary. Do not add ritual tests unrelated to the contract.

## Review a bundle safely

Read [references/review-bundle-integrity.md](references/review-bundle-integrity.md) before sending or consuming an archive or concatenated bundle.

Use:

```bash
python3 "$SKILL_ROOT/scripts/scan_review_bundle.py" PATH
```

Resolve `SKILL_ROOT` to the directory containing this `SKILL.md`; do not run a same-named script from the target repository by accident.

Reject or downgrade exact-code review when files contain undecodable UTF-8, replacement characters, unexpected counts, missing manifest entries, or a source revision mismatch. Prefer a public pinned commit or a delimited strict-UTF-8 text bundle when archive ingestion is unreliable.

## Validate guide-style artifacts

When a project uses a version register, bilingual peers, or evidence receipts, run the applicable scripts:

```bash
python3 "$SKILL_ROOT/scripts/validate_version_register.py" VERSION-REGISTER.json
python3 "$SKILL_ROOT/scripts/sync_profile_mirrors.py" --check VERSION-REGISTER.json
python3 "$SKILL_ROOT/scripts/check_bilingual_coverage.py" REPOSITORY_ROOT
python3 "$SKILL_ROOT/scripts/check_receipt_schema.py" RECEIPT.json [RECEIPT.json ...]
python3 "$SKILL_ROOT/scripts/validate_skill_package.py" "$SKILL_ROOT"
python3 "$SKILL_ROOT/scripts/check_markdown_links.py" REPOSITORY_ROOT
```

Scripts detect structural inconsistencies; they do not prove semantic translation equivalence or protocol correctness.

## Report the outcome

Lead with the actual result. Include:

- source revision and declared profile;
- capability/deployment boundary;
- findings ordered by impact, each with proof and residual;
- changes made, if authorized;
- exact verification executed and environment;
- what remains unknown, deferred, or owned elsewhere;
- protocol migration implications, if any;
- publication/disclosure state.

For bilingual artifacts, keep profile IDs, section IDs, claim IDs, receipt IDs, code, headers, methods, statuses, and evidence values identical across languages. Translation may improve natural phrasing but must not silently strengthen or weaken a claim.
