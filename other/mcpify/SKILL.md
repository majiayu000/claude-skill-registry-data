---
name: mcpify
description: "Take an existing application through the full MCP lifecycle: analyze capabilities, generate and test a secure server, package or deploy it, connect clients, publish registry metadata, and operate releases. Use for production-oriented MCP work, especially TypeScript and Next.js repositories; do not use to bulk-expose arbitrary functions or bypass release authorization."
---

# MCPify

Turn an existing application's user-level capabilities into a narrow MCP interface, then take the approved server through packaging, deployment, discovery, client integration, publication, and operations.

## Select the mode

Infer the mode from the request; if it is genuinely ambiguous, default to `analyze`.

- `analyze`: inspect the repository, create or update `mcp-manifest.yaml`, and write an analysis report. Do not change application logic or add MCP runtime code. Read [analysis workflow](references/mode-analyze.md).
- `generate`: implement only entries whose manifest status is `approved`. Read [generation workflow](references/mode-generate.md).
- `audit`: inspect an existing manifest and MCP implementation without changing it unless the user separately asks for fixes. Read [audit workflow](references/mode-audit.md).
- `test`: build and exercise the MCP integration safely. Read [test workflow](references/mode-test.md).
- `package`: prepare a reproducible local package, container, MCPB artifact, or public remote-server metadata without publishing it. Read [release lifecycle](references/release-lifecycle.md) and [registry publication](references/registry-publication.md).
- `deploy`: prepare or perform an explicitly requested deployment, including remote transport, authorization metadata, health checks, rollback, and gateway controls. Read [deployment](references/deployment.md).
- `connect`: generate client/host configuration and verify discovery for a specified MCP host. Read [client distribution](references/client-distribution.md).
- `publish`: publish an already tested package and/or `server.json` to an explicitly named registry, then verify the resulting listing. Read [registry publication](references/registry-publication.md).
- `operate`: version, update, deprecate, restore, or respond to a security incident for a published server. Read [operations](references/operations.md).

Invocation examples:

```text
Use $mcpify in analyze mode on this repository.
Use $mcpify generate from the approved mcp-manifest.yaml.
Use $mcpify audit and report unsafe or unnecessary exposure.
Use $mcpify test without production credentials or destructive calls.
Use $mcpify package and create validated server.json, but do not publish anything.
Use $mcpify deploy this approved remote server to the named staging environment.
Use $mcpify connect this server to the specified MCP client and smoke-test discovery.
Use $mcpify publish the tested release to the official MCP Registry.
Use $mcpify operate to deprecate the affected version and document migration.
```

## Non-negotiable invariants

1. Model agent goals, not implementation callables. Never bulk-convert routes, server actions, ORM methods, internal functions, SQL, command execution, secret access, or arbitrary argument forwarding into tools.
2. Treat `mcp-manifest.yaml` as the reviewed source of truth. Analysis may propose entries; generation may implement only `status: approved` entries.
3. Default critical capabilities to `excluded`. Default high-risk or uncertain authorization mappings to `disabled_pending_review`. Do not interpret repository access or a generation request as approval.
4. Reuse the narrowest existing service or business-logic function that already enforces domain rules. Keep wrappers thin and preserve existing identity, authorization, and transaction boundaries.
5. Make the smallest reasonable changes. Do not refactor unrelated code, change database schemas without necessity, overwrite `.env` files, or commit credentials.
6. Enforce safety in server code. MCP annotations and client confirmation UX are hints, not security controls.
7. Never use production credentials or perform destructive production actions during validation.
8. Before choosing protocol APIs or packages, verify current official MCP specification and SDK documentation. Record the date and exact URLs in generated documentation. Read [current standards](references/current-standards.md).
9. Treat package publication, deployment, registry publication, marketplace submission, lifecycle status changes, and client-account changes as distinct external mutations. Perform only the stages the user explicitly authorized, against the exact target verified immediately beforehand.
10. Never publish secrets, credentials, private endpoints, internal repository URLs, unsafe default arguments, production tokens, or environment-variable values in packages, images, `server.json`, logs, examples, or marketplace descriptions.

## Shared workflow

1. Read repository instructions (`AGENTS.md`, contributor docs) and inspect the working tree before edits.
2. Establish repository boundaries and inventory architecture. Use `scripts/repo_probe.py` for deterministic evidence when Python is available, then verify findings in source. Read [architecture detection](references/architecture-detection.md); for Next.js also read [Next.js guidance](references/framework-nextjs.md).
3. Identify user outcomes, map them to existing domain operations, and choose whether each surface belongs as a tool, resource, or prompt. Read [capability design](references/capability-design.md) and [protocol surface design](references/protocol-surface-design.md).
4. Trace identity, authorization, data sensitivity, side effects, external effects, and failure behavior end to end. Classify risk with [security and risk model](references/security-risk.md).
5. Create or validate `mcp-manifest.yaml` against [manifest specification](references/manifest-spec.md) and `assets/mcp-manifest.schema.json`. Run `scripts/validate_manifest.py` before generation.
6. Apply the selected mode workflow. For implementation decisions, read [MCP implementation](references/mcp-implementation.md).
7. Produce the mode's report using [reporting](references/reporting.md). Separate observed facts, inferences, decisions, exclusions, test evidence, and unresolved review items.
8. For release-facing modes, preserve one traceable version across source, package/container, `server.json`, documentation, and listing. Capture artifact digests, provenance, publication targets, and verification evidence.

## Stop conditions

Stop before implementing a capability when its source mapping, caller identity, ownership check, side effects, or required authorization cannot be established. Leave it disabled and state the missing evidence.

Stop before installs, deployment, external writes, real account changes, or privileged operations when they require authorization not already granted. Continue with safe analysis and local validation where possible.

For `publish` and `operate`, stop after local validation unless the user explicitly authorized the exact external action and registry/account/namespace. Preview the target, server name, version, artifacts, remote URLs, and lifecycle change before executing it. Do not use non-interactive confirmation-bypass flags unless the user explicitly requested unattended automation and the workflow has equivalent protected-environment controls.
