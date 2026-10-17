---
name: aiwf-local-device-security
description: "Use for Windows-first workstation security and Android, Linux, edge, or removable-device protection: accounts, elevation, ACLs, disk encryption, secure boot, endpoint protection, application control, services, credentials, local ports, updates, backups, disposal, and local AI files."
---

# AIWF Local Device Security

## Core Rule

Inspect device edition, version, hardware, encryption and recovery state, user roles, compatibility, and backup readiness before changing a host security control.

## Workflow

1. Identify device owner, OS/build, edition, firmware, TPM/secure-boot state, accounts, admin model, sensitive paths, removable media, and recovery access.
2. Inventory active protections, update state, endpoint protection, application control, local services/ports, remote access, scheduled tasks, startup items, and credential stores.
3. Classify local source, models, datasets, customer files, agent context, secrets, logs, caches, backups, and exports.
4. Prefer least privilege, per-user ACLs, supported credential stores, encrypted storage, protected recovery keys, signed software, and localhost-only development services.
5. Test compatibility and recovery before enforcing encryption, application control, memory integrity, firmware, or access-policy changes.
6. Record observed state, recommended state, impact, rollback, owner, and validation.

Read `references/source-register.json` for current platform behavior. Add the data-privacy skill for lifecycle decisions.

## Hard Gates

- Explicit approval is required before enabling/disabling encryption, changing ACLs, accounts, Defender/firewall/application-control policy, remote access, firmware, recovery keys, quarantine, deletion, or device isolation.
- Never expose, move, or upload recovery keys, credentials, private models, customer data, or agent context.
- Do not claim encryption is active from settings intent alone; verify status and recovery.
- Do not disable UAC, endpoint protection, secure boot, or memory protections as a compatibility shortcut.

## Output

Return device and data inventory, current evidence, prioritized controls, compatibility risks, approval gates, recovery path, and post-change checks.
