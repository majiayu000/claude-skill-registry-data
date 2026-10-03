---
name: ls-keepass-secrets
description: Use when validating logical secret-ID maps, config, and reference syntax for a KeePassXC integration; output is redacted and the fake backend is test-only.
metadata:
  version: "1.1"
compatibility: "Linux/WSL2 focused; Python 3.12+; PyYAML; optional keepassxc-cli capability detection only. This skill does not open or manage KeePassXC vaults."
---

# KeePass secret mappings

Use this skill to validate non-secret logical-ID metadata and reference syntax. It does not resolve, display, create, rotate, update, delete, or otherwise access real KeePassXC entries.

## Supported commands

Primary validation commands:

~~~bash
python3 scripts/localsetup_secrets.py map-validate --map examples/map.yaml
python3 scripts/localsetup_secrets.py reference '{{secret:mail.box03.example.admin:password}}'
~~~

Capability check:

~~~bash
python3 scripts/verify_keepassxc.py --format json
~~~

The CLI emits JSON envelopes by default:

~~~json
{
  "ok": true,
  "command": "map-validate",
  "data": {},
  "warnings": [],
  "errors": [],
  "sources": [],
  "sensitive": false,
  "redactions": []
}
~~~

Use --format human only for interactive display. Diagnostics are redacted. Protected values require --show-sensitive.

The default keepassxc backend preserves existing configuration and may check the CLI version. When keepassxc-cli is unavailable it reports missing_backend; otherwise it refuses every vault operation with interactive_backend_required. fake exists only for deterministic tests and examples; it is not a secret store.

## Logical IDs

Canonical IDs are lowercase and may contain letters, digits, dots, underscores, and hyphens:

~~~text
mail.box03.example.admin
postgres.box03.app1
api.box03.stripe.live
~~~

Aliases, including email-like aliases, may be declared in map files. Ambiguous aliases fail clearly.

## References

Supported forms:

~~~text
Secret ID: mail.box03.example.admin
{{secret:mail.box03.example.admin:password}}
secret://localsetup/repo/default/mail.box03.example.admin#field=password
~~~

See [docs/reference-format.md](docs/reference-format.md).

## Config and Maps

Resolution order:

1. CLI flags.
2. LOCALSETUP_SECRETS_* environment variables.
3. Repo-local .localsetup/secrets/config.yaml and map.
4. Legacy secrets/keepass-config.yaml plus secrets/*-secrets-map.yaml.
5. Global ~/.config/localsetup/secrets/config.yaml and ~/.local/share/localsetup/secrets/maps/default.yaml.

Config and map files may contain metadata, entry paths, usernames, URLs, and aliases. They must not contain passwords, tokens, key material, or passphrases.

Examples live in [examples/](examples/). Contract schemas live in [schemas/](schemas/).

## Backends

- keepassxc: the default capability guard. It checks that keepassxc-cli is present for diagnostics but never opens a vault or runs read/write operations.
- fake: deterministic test and example backend for placeholder data only. It must not be used as a secret store.
- PyKeePass: future optional backend only; not installed or required by this skill.

## Safety Rules

- Never put secret values in tracked files.
- Keep .kdbx, keyfiles, and .env files out of Git.
- Treat interactive_backend_required as an explicit refusal, not a request to bypass the vault boundary.
- Use the fake backend only in isolated tests and examples.
- Do not open, create, or inspect real vaults during tests.

## Documentation

- [Architecture](docs/architecture.md)
- [Command reference](docs/command-reference.md)
- [Config resolution](docs/config-resolution.md)
- [Global vs repo-local scope](docs/global-vs-repo-local-scope.md)
- [Vault backends](docs/vault-backends.md)
- [KeePassXC installation and versioning](docs/keepassxc-installation-versioning.md)
- [Portable vault files](docs/portable-vault-files.md)
- [Migration from v1](docs/migration-from-v1.md)
- [Security threat model](docs/security-threat-model.md)
- [Agent usage patterns](docs/agent-usage-patterns.md)
- [Troubleshooting](docs/troubleshooting.md)
- [Update procedure](docs/update-procedure.md)
- [Source ledger](docs/source-ledger.md)
- [Version ledger](docs/version-ledger.md)
