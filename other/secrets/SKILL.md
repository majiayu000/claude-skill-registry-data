---
name: secrets
description: >-
    Owns secret custody over 1Password and Doppler — op the permanent local store and
    SSH-key custodian, Doppler the runtime backend. Use when creating a secret, token, or env key
    or when one fails to resolve, creating and managing them, the op agent key, a tool or code logic
    needs a scoped token, or a config file needs secret material. Minting tokens and creating projects,
    configs, or scopes is Pulumi topology in Parametric_Forge/services/topology.ts — the pulumi skill.
---

# [SECRETS]

`op` owns permanent local and session custody. Doppler owns project configuration and explicit process delivery.

Topology — projects, environments, configs, service tokens, directory scopes — lives as IaC rows in `Parametric_Forge/services/topology.ts`, materialized by `estate.ts` and applied by `driver.ts` over the Pulumi Automation API. `doppler` reads and writes secret values against declared configs; `doppler run` and owner-specific downloads inject values at the consuming process; `~/.doppler` holds CLI scope and authentication state.

## [01]-[ROUTING]

- [01]-[PATTERNS](references/patterns.md): pattern doctrine — template rendering, mounts, multi-command wrappers, plan-gated features.

## [02]-[RESOLUTION]

- `~/.doppler` is the CLI config dir; scopes ride `~/.doppler/.doppler.yaml`, written by `doppler configure set` through the driver's `scopes apply`.
- A repo-local `doppler.yaml` is vendor setup guidance, not the estate scope owner; the estate carries none.
- Precedence, highest first: a service token's embedded project/config, runtime flags, env vars, config-file scope.
- Config-file scope resolves an exact directory match before the nearest ancestor.
- Scope env vars: `DOPPLER_TOKEN`, `DOPPLER_PROJECT`, `DOPPLER_CONFIG`, `DOPPLER_CONFIG_DIR`, `DOPPLER_PASSPHRASE`.
- Agents pass `--project`/`--config` explicitly; env carries only token custody.
- An ambient `DOPPLER_TOKEN` outranks flags and represents one config; strip it with `env -u DOPPLER_TOKEN` when fetching more than one source.

## [03]-[DOPPLER_CLI]

| [INDEX] | [TASK]                            | [COMMAND]                                                                                  |
| :-----: | :-------------------------------- | :----------------------------------------------------------------------------------------- |
|  [01]   | Binary and version proof          | `doppler --version`                                                                        |
|  [02]   | Effective options, token stripped | `doppler configure debug --json \| jq 'with_entries(.value \|= del(.token))'`              |
|  [03]   | Every scope row, token stripped   | `doppler configure --all --json \| jq 'with_entries(.value \|= del(.token))'`              |
|  [04]   | One directory's scope             | `doppler configure get project config --scope <dir> --json`                                |
|  [05]   | Set a scope row                   | `doppler configure set project=<p> config=<c> --scope <dir>`                               |
|  [06]   | Unset a scope row                 | `doppler configure unset project config --scope <dir>`                                     |
|  [07]   | Key inventory                     | `doppler secrets download --project <p> --config <c> --no-file --format json \| jq 'keys'` |
|  [08]   | Inject env into a process         | `doppler run --project <p> --config <c> --command '<cmd>'`                                 |
|  [09]   | Render a template                 | `doppler secrets substitute <template>`                                                    |

- One directory's scope keys land as `enclave.project`, `enclave.config`; the set is driver-owned and scope `/` stays untouched.
- Secret downloads pipe to `jq 'keys'` or `jq 'length'`; configure reads strip the root token with `del(.token)`, since a bare `configure debug` or `configure --all` prints it.
- Receipts, transcripts, and logs carry key names and counts, never values or tokens.

## [04]-[OP_CLI]

`op` reads the local store directly; the field suffix is `token`, `credential`, or `password` per item. An exported `OP_SERVICE_ACCOUNT_TOKEN` pins `op` to the `Tokens` vault, so `Personal` (the SSH key) resolves only under `env -u OP_SERVICE_ACCOUNT_TOKEN`.

| [INDEX] | [TASK]                          | [COMMAND]                                                                      |
| :-----: | :------------------------------ | :----------------------------------------------------------------------------- |
|  [01]   | Auth proof                      | `op whoami`                                                                    |
|  [02]   | Vault inventory                 | `op vault list`                                                                |
|  [03]   | Tokens item names               | `op item list --vault Tokens --format json \| jq -r '.[].title'`               |
|  [04]   | Read one secret                 | `op read "op://Tokens/<ITEM>/<token\|credential\|password>"`                   |
|  [05]   | Resolve the rebuild template    | `op inject -i ~/.config/op/env.template -o <out>`                              |
|  [06]   | Personal-vault SSH item         | `env -u OP_SERVICE_ACCOUNT_TOKEN op item get "Forge SSH Key" --vault Personal` |
|  [07]   | Rename an item to its real name | `op item edit "<old-title>" title="<official-name>" --vault Tokens`            |

- `op` serves the SSH key to `ssh`, `git`, WezTerm, Yazi, and rclone through the 1Password agent socket; the item ref lives in `1Password/ssh/agent.toml`, never a private key on disk.
- Read a secret only to verify presence or wire a one-off; standing local consumption rides the activation-generated session cache.

## [05]-[SESSION_CUSTODY]

`op inject` resolves `~/.config/op/env.template` into the mode-600 `~/.config/hm-op-session.sh` cache on every `forge-redeploy --switch`. Interactive shells source that cache through `forge-session-secrets.sh`; `gui-op-secrets` projects the same names into the launchd GUI domain for newly spawned applications. Process-specific Doppler consumers fetch their material explicitly with the owning project and config.

- `~/.config/op/env.template` owns the local session key set; activation keeps values outside the Nix store.
- `forge-session-secrets.sh` is the shell source path; `gui-op-secrets` is the GUI projection path.
- Doppler delivery stays at the process boundary through `doppler run` or an owner-specific `doppler secrets download`.

## [06]-[CUSTODY]

Local custody is `op`, never the OS keychain: every service and IaC token and the SSH key live in a `Tokens` or `Personal` vault item. A personal `doppler login` is the one credential Doppler keeps in the keychain, used for the operator's ad-hoc interactive work alone — no rail depends on it.

| [INDEX] | [CLASS]                          | [CUSTODY]                                    | [USE]                           |
| :-----: | :------------------------------- | :------------------------------------------- | :------------------------------ |
|  [01]   | Config-scoped service token      | Pulumi stack secret output                    | Explicit runtime reads          |
|  [02]   | IaC admin token                  | `op://Tokens/DOPPLER_IAC_TOKEN/token`        | Topology writes via Pulumi only |
|  [03]   | Pulumi stack passphrase          | `op://Tokens/PULUMI_FORGE_SERVICES/password` | Stack state decryption          |
|  [04]   | Provider PATs (GitHub and peers) | `op://Tokens` items, mirrored into configs   | Activation or process injection |

- Config-scoped service token: minted by topology rows; static Developer-plan tokens are revoked and reminted, never rotated in place.
- IaC admin token and stack passphrase: brokered by `driver.ts`; an ambient `DOPPLER_TOKEN` or `PULUMI_CONFIG_PASSPHRASE` short-circuits the op read per run.
- Provider PATs are never topology identity.

## [07]-[LAW]

- One item, one official name: an item carries the credential's real published name, never a handrolled synonym; a consumer needing a different env-var name renames the item at the source and repoints every reader, never adds a second item or a duplicate export aliasing the same secret. A naming mistake is fixed by renaming in `op` and Doppler, never papered over.
- A new project lands as project/config rows in `Parametric_Forge/services/topology.ts` and a directory scope row, then `pulumi up`; retiring it deletes its rows.
- A repo carries zero Doppler files; its agents resolve through scope and hook automatically.
- Rendered secret material is ephemeral: `--mount`/`--mount-template` over durable renders; plaintext binds only where the target owner requires it.
