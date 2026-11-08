---
name: whatsapp
description: "Read, search, archive, or send WhatsApp messages using the authorized account."
disable-model-invocation: true
---

# WhatsApp

Perform only the requested operation. Bind it to the authorized account and conversation; sending or replying also requires an explicitly requested recipient and message content.

Use `me` when the user explicitly asks to inspect their messages or act on their behalf. Otherwise use `agent` for requested sends or replies from the agent. Do not switch accounts to work around a failure.
Resolve the recipient from the request or machine-local contact preferences only when needed for delivery. Ask when the account, recipient, or requested action remains ambiguous, not to reconfirm settled authorization.

## Choose the operation

Load only the matching reference section. The commands are alternatives, not a setup checklist.

| Request | Reference |
| --- | --- |
| Read or search the primary archive | [Archive reads](references/operations.md#archive-reads) |
| Inspect a named account's stored messages or uncertain auth state | [Account inspection](references/operations.md#account-inspection) |
| Send or reply | [Sending and attachments](references/operations.md#sending-and-attachments) |
| Refresh data or monitor replies | [Refresh and monitoring](references/operations.md#refresh-and-monitoring) |
| Import media or back up the archive | [Archive imports and backups](references/operations.md#archive-imports-and-backups) |
| Resolve a missing CLI or interactive authentication | [Troubleshooting](references/Troubleshooting.md) |

## Authorization boundaries

- Sending does not authorize creating groups, changing membership, attaching files, recording audio, monitoring replies, or starting persistent sync. Reuse the intended existing conversation. Obtain explicit scope for these additional operations.
- Monitoring requires a specified account, conversation, and finite deadline. Ask for a bounded window if none was provided. Stop earlier on the requested event or cancellation, and stop the run-owned watcher no later than that deadline. A one-off send leaves no watcher behind.
- Use `--read-only` or `WACLI_READONLY=1` for `wacli` inspection and `--json` for parsing. Archive inspection must not trigger an unrequested refresh.
- Keep named accounts in isolated stores. Do not write `session.db` directly or merge accounts into one `wacli.db`. Use `--store` only for authorized legacy-store debugging.
- Preserve private-network restrictions, including Tailscale-only access where configured. Never expose services publicly without an explicit user request and double confirmation. Do not change network or account settings as a diagnostic probe.

## Completion

Reuse valid account, auth, and process evidence instead of repeating setup or starting duplicate sync sessions.
Report the requested result and relevant coverage or delivery uncertainty. Check an uncertain send's receipt or stored result before retrying; do not send a duplicate just to obtain clearer output.
Stop after the operation or the exact access, tool, or authorization blocker. Tool installation and interactive account setup are separate authorized work, not automatic troubleshooting steps.
