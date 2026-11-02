---
name: mcp-tool-permission-audit
description: Review an MCP server's exposed tools, scopes, credentials, and side effects before connecting it to an AI workflow.
---

# Mcp Tool Permission Audit

## Goal

Reduce accidental over-privilege by matching each MCP tool to the smallest justified capability and a clear approval boundary.

## Inputs to inspect

Server documentation or source, tool schemas, transport and scope, credential handling, data classifications, and expected user workflow.

## Workflow

1. Inventory every exposed tool and classify it as read-only, local write, remote write, destructive, administrative, or capable of moving data outside the environment.
2. Trace identity and credential flow from client configuration to server execution. Separate user-level credentials from project-shared configuration and never copy secrets into examples or committed files.
3. Map each tool to the minimum filesystem, network, database, or account permissions it needs. Identify wildcard access, arbitrary shell execution, unrestricted URL fetches, and ambient credentials.
4. Define human approval for irreversible or externally visible actions. Separate discovery/read tools from mutation tools where the server design allows it.
5. Run tests with a low-privilege account and benign fixtures; verify rejected operations, audit logs, and behavior when credentials are missing or expired.

## Validation checklist

- [ ] Each tool has documented inputs, side effects, identity, and output sensitivity.
- [ ] Least privilege is enforced by the server or credentials, not only by prompt instructions.
- [ ] Untrusted tool output is treated as data and cannot override system or project instructions.
- [ ] Secrets are redacted from logs and failure messages.
- [ ] Risk acceptance and unresolved questions are recorded before enabling the integration.

## Required output

Deliver a tool inventory with risk tier, required permission, data exposure, approval rule, test evidence, and enable/disable decision.

## Boundaries and failure handling

Do not trust tool descriptions as proof of behavior; do not connect an unknown service with broad production credentials merely to see what it does.

When repository evidence is incomplete, label the gap explicitly and request only the missing information that changes the decision. Do not claim commands, benchmarks, tests, or runtime checks passed unless their outputs were observed.
