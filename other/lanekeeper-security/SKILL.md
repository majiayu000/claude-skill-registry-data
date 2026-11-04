---
name: lanekeeper-security
description: Security requirements and proof patterns for Lanekeeper (S1–S25). Covers Entra sign-in and sessions, default-deny authorization, agent and sentinel identity, mTLS and the KMS-backed CA, Secret Manager, the GitHub token vault, the tamper-evident audit chain, path, regex and upload validation, Markdown sanitising, CSP, MCP redaction and prompt injection, container and network hardening, and the supply chain. Use this skill whenever a change touches auth, tokens, secrets, file paths, user input, uploads, HTML rendering, MCP output, logging, environment variables, agent or sentinel code, Helm charts, CI or dependencies. Also use it when reviewing or threat-modelling. Security is the project's top priority, and most violations come from overlooking a requirement rather than misunderstanding it.
---

# Lanekeeper security

Security comes first in this project's priorities (D61). The requirements live in `docs/security.md`. This skill helps you find the ones that apply to your change, implement them the way the rest of the codebase does, and prove each one with a test.

## Step 1: Find the requirements that apply

Start with the S# list in your prompt's metadata table, then add any the change touches:

| Change touches | Requirements |
|---|---|
| Routes, handlers, MCP tools | S4 (guard), S11 (validation), S12 (output), S14 (MCP), S14b (redaction) |
| Sign-in, sessions, users, roles | S1, S2, S3, S4 |
| Tokens, keys, webhook URLs, any secret | S7, S8, S21 |
| Audit events | S9 |
| File paths, NFS operations | S11 (`NfsPath`), S17 (cap-std, deny globs) |
| User regexes, search | S11 (linear-time `regex` with size limits) |
| Markdown, docs, any HTML | S12 (ammonia, CSP, Trusted Types) |
| Agent or sentinel | S5, S6, S16, S17, S25 |
| Helm, NetworkPolicy, Dockerfile | S16, S18, S20 |
| `Cargo.toml`, `package.json`, CI workflows | S19, S20 |
| Logs, metrics, errors | S10, S21 (no contents, secrets or environment values) |

## Step 2: Implement it the house way

- **Authorization is declared, not scattered.** Register each route with `#[guarded(role = …)]` and use the `RequireRole<R>` or `ActiveUser` extractors. Pending and disabled users fail before your handler runs. Never check roles inside handler bodies as the only control.
- **Validate at the edge with typed parsers:**
  - `NfsPath`, `CompareRef`, `PathMappingRule` and `TenantId`;
  - never a raw `String` path into the agent or sentinel;
  - inside the agent, every file operation goes through the cap-std `Dir` rooted at the mount.
- **No blind writes.** Every NFS write and delete carries the expected hash. A mismatch returns a conflict and writes nothing.
- **Secrets are `Secret<T>`.**
  - Constant-time comparisons.
  - Envelope encryption for GitHub tokens: a fresh AES-256-GCM data key per token, wrapped with KMS. The associated data is the user id plus the credential id, which binds each ciphertext to its owner.
  - Secret Manager for runtime secrets.
- **Treat untrusted text as data.**
  - Config and doc text in MCP output goes inside a labelled data block.
  - Values flagged by the secret scan are redacted (`[REDACTED: N chars, rule]`).
  - No server component sends user content to an LLM.
- **Render safely.** Markdown goes through pulldown-cmark, then ammonia's allowlist, on the server. The web app never uses `dangerouslySetInnerHTML`; the lint enforces it, with one sanitised-docs exception.
- **Read environment variable names, not values.** The agent reads values only for the allowlist (D88).
- **Least privilege everywhere.**
  - The agent's RBAC has no Secret list permission.
  - Containers are non-root, with a read-only root filesystem, the RuntimeDefault seccomp profile and all capabilities dropped.
  - NetworkPolicies deny by default.
  - The sentinel's systemd unit has an empty capability bounding set.
  - Nothing listens that doesn't need to.

## Step 3: Prove it

Every S# you touch needs a named test that fails if the protection is removed. `references/proof-patterns.md` lists the test shape that suits each requirement. The ones reviewers ask for most:

- the route-table guard test, extended with your new routes;
- a log-capture test asserting no secret, file content or environment value appears;
- traversal and symlink tests for any path input;
- a 409 test for every write path;
- an XSS corpus test for anything that renders HTML;
- a test that a planted fake key never appears in MCP output.

## Step 4: Update the threat model

Add or update your component's section in `docs/threat-model.md` using STRIDE: Spoofing, Tampering, Repudiation, Information disclosure, Denial of service, and Elevation of privilege. For each threat, name its mitigation and the S# it maps to, then list any residual risk honestly. A human signs this off before go-live.

## Red flags (stop and fix, or escalate)

- A handler or tool without a declared role.
- `String` paths crossing into the agent or sentinel.
- `unwrap` or `expect` on input-derived data.
- Any `unbounded_channel`, `OFFSET` pagination, or query without a `LIMIT`.
- A secret inside `format!`, `tracing` fields or error messages.
- A new dependency that isn't justified, fails `cargo deny`, or is less than 14 days old.
- GitHub Actions referenced by tag instead of commit SHA.
- Exported HTML from the design handoff pasted into the app.
- Calling the config-server's `/update-resources` from anywhere except the agent's `NotifyConfigServer` path. The endpoint is unauthenticated (Q37), so every call must be audited and require Operator.

## When a requirement conflicts with a feature

Don't trade security away quietly. Write the conflict in your plan or PR: which requirement, which feature, and what options you see. Then stop. Only a human can relax a requirement, and only by recording it in `docs/decisions.md`.
