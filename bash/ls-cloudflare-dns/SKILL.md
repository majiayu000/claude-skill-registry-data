---
name: ls-cloudflare-dns
description: Use the cf CLI for Cloudflare zones, DNS records, settings, DNSSEC, scans, imports, exports, batches, analytics, and zone transfers.
metadata:
  version: "3.0"
compatibility: "Requires cf."
---

# Cloudflare DNS

## Commands

```bash
cf --help
cf zones --help
cf dns --help
cf dns records --help
cf dns settings --help
cf dns dnssec --help
cf dns analytics --help
cf dns usage --help
cf dns zone-transfers --help
```

Use focused help and command schemas for the operation being run:

```bash
cf dns records create --help
cf schema dns records create
```

## Authentication

```bash
cf auth --help
cf auth login
cf auth whoami
cf auth list
```

Use `--profile <name>` to select a named profile. Ask the user before login, logout, profile creation, deletion, activation, or deactivation.

## Zones and records

Pass `--zone <zone-id-or-domain>` or `-z <zone-id-or-domain>` to select the DNS zone.

```bash
cf zones list
cf dns records list --zone example.com
cf dns records list --zone example.com --name-exact app.example.com
cf dns records get --zone example.com <dns-record-id>
```

Create and edit commands accept a JSON request body:

```bash
cf dns records create --zone example.com --dry-run \
  --body '{"type":"A","name":"app.example.com","content":"192.0.2.10","ttl":300,"proxied":false}'

cf dns records edit --zone example.com <dns-record-id> --dry-run \
  --body '{"content":"192.0.2.20"}'

cf dns records update --zone example.com <dns-record-id> --dry-run \
  --body '{"type":"A","name":"app.example.com","content":"192.0.2.20","ttl":300,"proxied":false}'

cf dns records delete --zone example.com <dns-record-id> --dry-run
```

Use `edit` for a partial record change and `update` for a full replacement. Use `list` with exact name and type filters before selecting a record ID. Before creating a record, check the selected name and type for an existing record.

## Batch, import, export, and scan

```bash
cf dns records batch --help
cf dns records import --help
cf dns records export --help
cf dns records scan --help
cf dns records scan-trigger --help
cf dns records scan-list --help
cf dns records scan-review --help
```

Use `--body '<json>'` for batch and scan-review requests. Use `--file <bind-file>` for BIND imports.

## Settings and DNS features

```bash
cf zones settings --help
cf dns settings account --help
cf dns settings zone --help
cf dns dnssec get --help
cf dns dnssec edit --help
cf dns zone-transfers --help
```

## Mutations

Before a non-dry-run command, inspect focused help and use `--dry-run` when offered. For create, list the selected name and type first. For an existing record, get the selected record ID first. For batch, import, scan-review, settings, DNSSEC, zone, and zone-transfer changes, inspect the complete body or file first.

Show the exact profile, zone, target, request body or file, and command. Ask the user to approve that exact action before running it. After it runs, list or get the changed resource. Do not accept scan records without approval of the scan-review body.

## Dynamic DNS

List the A or AAAA record by zone, name, and type. If its content differs from the required address, run `cf dns records edit` with that record ID and a body containing the required fields.
