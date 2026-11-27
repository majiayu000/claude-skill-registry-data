---
name: service-onboard
description: Add a platform service consistently, covering placement, networking, secrets, persistence, automation, monitoring, backup, recovery, and docs.
---
# Onboard service
Answer first: why it is needed; which node and why (RAM/CPU/disk budget against PROJECT-CONTEXT §2 — MongoDB needs AVX, i.e. node4); ports and clients; exposure (overlay-only unless it goes through Caddy); persistent data; secrets (ansible-vault today, Vault after init); health signal; backup and restore; failure behaviour; upgrade path. Then: an Ansible role with a pinned image in inventory/group_vars/all/images.yml, a playbook added to site.yml, a bind on wg_overlay_ip with an assertion it is not 0.0.0.0, a backup entry, a restore runbook if it holds state, and a row in the service catalog in docs/architecture/overview.md. Validate restart behaviour and the restore, not just that the container starts.
