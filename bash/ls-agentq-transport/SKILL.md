---
name: ls-agentq-transport
description: Use for Agent Q signed encrypted file-drop or mail ship and ingest, private registry v2 setup, queue status, and transport maintenance.
metadata:
  version: "1.0"
compatibility: "LocalSetup Python 3.12+ with its locked dependencies and GnuPG; mail requires configured ls-mail-protocol-control SMTP/IMAP accounts."
---

# Agent Q transport

## Purpose

Use the existing `agentq_transport_client` to send and receive a signed,
encrypted binary OpenPGP manifest across an allowed file-drop or mail carrier.
Both carriers use the same shared `ls.core.openpgp` seal/open and exact receipt
before queue promotion. Installing this skill never generates a key or enrolls a
peer. Pre-ship checks accept argv-only `pytest` or `uv run --locked pytest`
commands and execute without a shell.

## When to use

- Shipping or receiving an Agent Q PRD, bundle, acknowledgement, or artifact.
- Editing the private v2 registry, selected trust stores, manifest schema, or CLI.
- Operating file-drop polling, mail pull, queue status, or archive pruning.
- Setting up same-machine different-repo handoff; see the scenario guide.

## Key paths

| Path | Role |
|------|------|
| `ls/tools/agentq_transport_client/agentq_cli.py` | CLI entrypoint and current command help |
| `ls/tools/agentq_transport_client/docs/USER_GUIDE.md` | Commands and examples |
| `ls/tools/agentq_transport_client/docs/ADMIN_GUIDE.md` | Registry, rotation, and mail operation |
| `ls/config/agent_trust_registry.example.yaml` | Version 2 registry fields, illustrative pins only |
| `ls/config/manifest.schema.json` | Inner manifest schema |

## Related packages

- `ls-workflow-openpgp-lifecycle` owns key adoption, protected backup, rotation,
  revocation and independent authority recovery. Keep trust state private and
  persistent outside application installation versions.
- `ls-mail-protocol-control` is the policy-gated mail carrier. File drops need no
  mail account. Mail exposes routing addresses, generic subject/body and one
  opaque binary attachment; it does not run a second crypto engine.
- `ls-workflow-queue-batch-implement` consumes authenticated `in/` entries after
  this client has verified and promoted them.

## Handoff flow

1. Select the peer by exact configured agent ID before decrypt. Verify its
   pinned full signing fingerprint and role from the persistent authority store.
   Check the local recipient authority and exact encrypted recipient set.
2. Use the allowed file-drop root or mail account/address. File drops have a
   random opaque `.agentq.lspgp` stem and ready marker written last. Mail uses
   one opaque octet-stream attachment. The manifest and identities are encrypted.
3. After a full shared-envelope open, bind the inner sender and recipients to
   the selected registry entry. Recheck authority and record exact ciphertext
   acceptance before promoting the queue item. Duplicate receipts stay terminal;
   revoked, stale, tampered or unbound messages are rejected.
4. Process the accepted PRD only within its authorized scope. Validate a return
   manifest and destination through the same registry before shipping a reply.
   Record the queue and transport outcome without exposing private key material.

The `--force` option can request reprocessing of a verified item; it cannot
bypass cryptographic verification, identity matching, or transport policy.
Legacy unsigned, PGPy, armored `.agentq.asc`, and version 1 registry content is
retained for explicit migration. It does not enter the normal queue. Historical
opening requires an exact persisted receipt and cannot promote old content.

## References

- [Agent Q protocol](../../docs/AGENTIC_AGENT_TO_AGENT_PROTOCOL.md)
- [Agent Q scenarios](../../docs/AGENTIC_AGENT_Q_SCENARIOS.md)
- [Agent Q build specification](../../docs/AGENTIC_AGENT_Q_BIDIRECTIONAL_BUILD_SPEC.md)
- [Agent Q package README](../../tools/agentq_transport_client/README.md)

## Verify

From the repository root, run the current CLI help and the package tests:

```bash
uv run --locked python ls/tools/agentq_transport_client/agentq_cli.py --help
uv run --locked pytest -q ls/tools/agentq_transport_client/tests/
```

The package tests include focused denial fixtures. Release acceptance also uses
real disposable keyrings and the actual installed artifact consumer.
