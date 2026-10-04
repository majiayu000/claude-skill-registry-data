---
name: build-obsidian-vault
description: Interview a user about knowledge-work goals and habits, then plan, create, or audit a maintainable local Obsidian vault made from ordinary Markdown, YAML properties, folders, and core-plugin-compatible templates. Use when a user asks to build, initialize, reorganize, or standardize an Obsidian knowledge base or vault. Prefer a new vault; extend an existing vault only after an explicit preview and never overwrite existing notes or settings.
---

# Build an Obsidian vault

Translate actual habits into a small, durable vault. Do not install community plugins or build an elaborate taxonomy before the user has demonstrated a need.

## Runtime boundary

- Use Python 3.11–3.14 on macOS or Linux. The secure filesystem and locking guarantees are POSIX-only.
- Before any mutating operation, the script requires `fcntl`, directory-FD operations, `O_NOFOLLOW`, `O_DIRECTORY`, directory `fsync`, atomic no-replace rename, and atomic exchange rename. If the platform cannot provide them, stop with `UNSUPPORTED_PLATFORM`; do not substitute an unsafe implementation.
- The script prints exactly one JSON object on stdout with empty stderr and exit 0 for success. An expected failure leaves stdout empty and prints exactly one redacted JSON error on stderr. Consume those objects rather than parsing prose.
- Repository-wide failure codes are: 2 for arguments, schemas, or unsafe inputs/paths; 3 for unavailable dependencies, models, or platform capabilities; 4 for locks, conflicts, recovery conflicts, or stale plans; 5 for external-tool, network, or runtime I/O failures; 7 for contract, identity, or file-evidence integrity failures; and 130 for interruption.
- Keep the skill independently runnable. It uses only its own vendored contracts and the Python standard library at runtime.

## Interview

Use short multi-turn questions. Ask one coherent group at a time and accept “use defaults” at any point.

1. **Purpose and outputs:** What should this vault help produce—learning, research, projects, content, decisions, or personal records? What are the two most common inputs and outputs?
2. **Capture and retrieval:** Where should quick captures land? Does the user retrieve by search, links/maps, folders, dates, or a mix? How much weekly maintenance is realistic?
3. **Conventions and constraints:** Preferred language, filename style, Wikilinks versus portable Markdown links, daily notes, attachment policy, sync/backup method, and target path.

Challenge contradictory requirements. For example, “zero maintenance” is incompatible with a deep manual taxonomy; choose a shallow inbox-plus-search workflow instead.

Read [profiles.md](references/profiles.md) after the first answer. Select the closest profile, then customize only what the user's answers justify.

## Build workflow

1. Write one config JSON conforming to [config-schema.md](references/config-schema.md). Keep it outside the target vault until validated.
2. For an existing vault, run the read-only audit before planning:

   ```bash
   python3 scripts/vault_builder.py audit --vault "<absolute-vault-path>"
   ```

   An existing directory not previously built by this skill is reported with `managed_by_builder: false`. That is not permission to modify it: inspect the plan and use `--extend-existing` only after the user accepts every destination and conflict.
3. Validate and preview:

   ```bash
   python3 scripts/vault_builder.py validate-config "<config.json>"
   python3 scripts/vault_builder.py plan "<config.json>" --vault "<absolute-vault-path>"
   ```

4. Read the `plan_sha256` from the `plan` JSON. Summarize the target path, folders, capture destination, source/attachment locations, templates, link style, unchanged files, and conflicts. Ask the user to confirm that exact plan because applying it creates local files.
5. Apply the confirmed plan by passing its full digest:

   ```bash
   python3 scripts/vault_builder.py build "<config.json>" \
     --vault "<absolute-vault-path>" --apply \
     --expected-plan-sha256 "<plan_sha256>"
   ```

   For an explicitly approved existing vault, add `--extend-existing`:

   ```bash
   python3 scripts/vault_builder.py build "<config.json>" \
     --vault "<absolute-vault-path>" --apply --extend-existing \
     --expected-plan-sha256 "<plan_sha256>"
   ```

   Never reuse a digest after the config or observed vault contents change. The builder recomputes the plan while holding the exclusive vault lock and returns `STALE_PLAN` if it no longer matches. Run `plan` again and obtain fresh confirmation.
6. Run the post-build audit and require the formal build receipt:

   ```bash
   python3 scripts/vault_builder.py audit \
     --vault "<absolute-vault-path>" --require-build-receipt
   ```

7. Report the vault path, receipt, created/unchanged files, conflicts, and the one manual action: open that folder as a vault in Obsidian. If daily notes are enabled in the profile, explain that the builder creates the folder and template but does not toggle or configure the Obsidian core plugin.

All lock-taking commands accept `--lock-timeout`; the default is 30 seconds. A timeout returns `VAULT_BUSY`.

## Contract, identity, and recovery

- The input remains `awesome-capture.vault-config/v1`.
- A successful build publishes `<vault>/.awesome-capture/vault-build.json` last. It is an `awesome-capture.vault-build-receipt/v1` object recording the config and contract digests, layout and link style, vault identity, confirmed plan digest, and relative managed paths with their initial hashes.
- Generated Markdown and templates are independent of the execution date. Timestamps belong only in the receipt. Reapplying an identical config to intact managed content returns `unchanged`; it does not create a cross-day diff.
- Build files, the journal, and the receipt are published without clobbering existing paths and are synced with their parent directories. A conflicting destination is never overwritten.
- A build transaction uses an `awesome-capture.transaction/v1` journal below `<vault>/.awesome-capture/transactions/`; the receipt is the final completion marker.
- Before a new build, the script automatically finishes a provably matching pending build transaction. To recover explicitly:

  ```bash
  python3 scripts/vault_builder.py recover --vault "<absolute-vault-path>"
  ```

  Recovery only completes steps whose staged and published hashes agree. Unknown entries, unsafe paths, or mismatched content return `RECOVERY_CONFLICT`; the script does not delete or overwrite them.

## Locking and audit

- Vault build and knowledge ingest share the persistent `<vault>/.awesome-capture/vault.lock`. Build and recovery take an exclusive lock; both audit commands take a shared lock.
- `audit` is read-only and never invokes recovery. It checks the formal build receipt, config identity, managed directories and templates, symlinks, hashes, and pending transactions.
- Without `--require-build-receipt`, an otherwise valid unowned vault reports `managed_by_builder: false`. Post-build acceptance must use `--require-build-receipt`.
- Any invalid or unknown receipt, missing or changed managed content, unsafe link, or pending transaction makes the required audit unhealthy. Run `recover` only as an explicit mutating operation.

## Guardrails

- Keep source files portable: Markdown, ordinary attachments, and the skill-owned JSON receipt.
- Create the `.obsidian` marker directory, but do not write undocumented `.obsidian/*.json` application settings. Obsidian may change those private formats.
- Use Obsidian properties as flat YAML. Do not invent nested property schemas that the Properties UI does not support.
- Prefer stable folder paths and links. Avoid characters Obsidian documents as unsafe in links.
- Do not modify Obsidian's global vault registry or launch the GUI.
- Do not enable Sync, publish content, or copy settings from another vault.
- Reject filesystem roots, the user's home directory, `.obsidian` itself, and a target nested inside another vault.
- Reject parent traversal, symbolic-link path components, special files, hardlinked managed files, unsafe ownership, and directories writable by other users. Path display via `resolve()` is not a security boundary.
- Keep `.awesome-capture`, its lock, receipts, and journals private. Ordinary vault Markdown remains readable as normal `0644` content.
- Do not overwrite. A conflict must be resolved by the user or by generating a new path.
- Keep templates minimal; add automation only after the base vault works.
