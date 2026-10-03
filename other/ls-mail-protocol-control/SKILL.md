---
name: ls-mail-protocol-control
description: Provide full SMTP and IMAP account control for delegated mailboxes with attachment-first MIME handling and full-envelope encryption. Use when an agent must read, send, organize, decrypt, and manage mailbox state with strict admin controls.
metadata:
  version: "1.2"
compatibility: "Python 3.12+ using stdlib smtplib, imaplib, and email.mime plus the environment's installed PyYAML and cryptography dependencies. This documents local API requirements only; validate target SMTP/IMAP provider profiles and encryption wire formats separately—no unspecified SMTP/IMAP or cross-library interoperability is guaranteed. Requires delegated SMTP/IMAP accounts, repo-local policy/account config, and environment-provided credentials; no shell commands or subprocess execution."
---

# Mail protocol control

## Purpose

Give an AI agent full operational control of delegated SMTP and IMAP accounts while keeping safety and governance in one place. This skill is built for deterministic tool calls, low token usage, and strict policy enforcement.

## When to use

- User asks for agent-driven mailbox automation over SMTP or IMAP.
- User needs policy-controlled read, write, and destructive mailbox actions.
- User needs token-efficient JSON CLI operations for mail triage and response workflows.
- User needs auditable account actions with confirmation gates for high-impact operations.

## Scope

- In scope: SMTP and IMAP.
- Out of scope for v1: POP3.

## Architecture

- Python domain layer:
  - SMTP via `smtplib`.
  - IMAP via `imaplib`.
- Attachment-first MIME envelope support for send and fetch paths.
- Full-envelope encryption and decryption engine:
  - PSK AES-GCM.
  - Password-derived AES-GCM.
  - Pure-Python OpenPGP.
- Policy gate for all mutating operations.
- One-shot JSON CLI bridge with compact atomic and composite operations.
- Confirmation token lifecycle for threshold-gated destructive operations.

## Tooling layout

```
ls/skills/ls-mail-protocol-control/
 SKILL.md
 scripts/
    mail_protocol_control.py
    mail_types.py
    mail_utils.py
    policy_engine.py
    crypto_types.py
    crypto_engine.py
    mail_json_cli.py
    tests/
        test_mail_protocol_control.py
 references/
     SMTP_IMAP_OPERATION_MATRIX.md
     JSON_CLI_TOOL_SCHEMA.md
     POLICY_SCHEMA.md
     CREDENTIAL_PROVIDER_CONTRACT.md
     USER_GUIDE.md
     ADMIN_GUIDE.md
     API_EXAMPLES.md
     TROUBLESHOOTING.md
     ENCRYPTION_MODEL.md
     KEY_MANAGEMENT.md
     examples/mail_accounts.sample.json
```

## Admin controls

- Policy profiles: `full`, `restricted`, `read_only`.
- Action-level allow and deny lists.
- Threshold controls for high-impact operations.
- Confirmation token challenge for gated destructive actions.

## JSON CLI operations

The `mail_json_cli.py` bridge executes one `--tool` request with one `--args-json` object, writes one JSON response, and exits. It is not an MCP transport.

- Atomic tools:
  - `mail_accounts_list`
  - `mail_capabilities_get`
  - `mail_query`
  - `mail_get`
  - `mail_get_attachment`
  - `mail_mutate`
  - `mail_send`
  - `mail_encrypt`
  - `mail_decrypt`
  - `mail_send_encrypted`
  - `mail_get_decrypted`
  - `mail_sync`
  - `mail_policy_preview`
- Composite tools:
  - `mail_triage_batch`
  - `mail_reply_flow`

## Token efficiency rules

- Use compact fields (`lim`, `cursor`, `code`, `op_id`, `next`).
- Default `lim=25`, hard max `lim=100`.
- Keep responses concise unless `detail=true`.
- Keep attachment content metadata-first unless explicit retrieval is requested.
- Return machine-readable codes and deterministic shapes.

## Use with Agent Q

Agent-to-agent PRD handoff can use this skill as the **mail adapter** backend (SMTP send / IMAP fetch+decrypt). The **Agent Q transport client** orchestrates pull and push; batch PRD processing stays filesystem-only. See [ls/docs/AGENTIC_AGENT_TO_AGENT_PROTOCOL.md](../../docs/AGENTIC_AGENT_TO_AGENT_PROTOCOL.md) and [ls/docs/AGENTIC_AGENT_Q_BIDIRECTIONAL_BUILD_SPEC.md](../../docs/AGENTIC_AGENT_Q_BIDIRECTIONAL_BUILD_SPEC.md). Client CLI: `ls/tools/agentq_transport_client/agentq_cli.py`. Post-ingest mail should move processed messages to `LocalsetupAgentQ/Processed` (or config override) so UNSEEN cannot replay without ledger.

## Security baseline

- Treat every external input as hostile.
- Enforce schema and bounds checks before execution.
- No shell interpolation of untrusted values.
- Require TLS for IMAP and `ssl` or `starttls` for SMTP; plaintext modes are denied before connection.
- Redact secrets and message payload data in logs.

## Documentation requirement

All user-facing documentation and guidance for this skill must be written in GitHub Flavored Markdown, render correctly in preview, and follow the humanization workflow in `ls-humanizer`.
