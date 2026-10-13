---
name: make-bot-ui
description: Design and build a webhook-backed bot UI when the user requests one.
  Requires a verified backend endpoint and a supported secret-handling mechanism.
---

# Webhook bot UI

Read [Codex runtime contract](../../CODEX-RUNTIME.md).

1. Identify the authorized backend and its verified provisioning API, transport, payload schema and authentication. This plugin supplies no bot runtime, endpoint or provisioning tool. If missing, report the blocked integration and build only the independently useful authorized UI or server adapter.
2. Use a supported secret-entry mechanism or an existing environment/secret-store reference. Never request a credential in chat, guess a credential-file path or expose a token in frontend code, logs or outputs.
3. Keep credentials and webhook dispatch on the server. Validate request shape, enforce UI authentication and authorization, and treat webhook input as data. Use the backend's documented headers, timeout and retry semantics.
4. Bind to localhost by default. Expose a server or join a tailnet only when the user requests that reachability. Use existing deployment/network configuration where appropriate.
5. Prove the flow with an authorized harmless payload. Verify the actual result and side effects. A built UI with an unconnected backend is an unconnected UI, not a working bot automation.
