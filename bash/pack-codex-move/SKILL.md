---
name: pack-codex-move
description: Inventory, classify, and safely package a user's local Codex workflow before changing computers. Use when the user asks to move, export, back up, pack, “收拾行李”, or prepare Codex on an old macOS, Windows, or Linux device for restoration elsewhere.
---

# Pack Codex Move

Create a versioned, checksummed migration package without changing source Codex state.

## Workflow

1. Read [migration-policy.md](references/migration-policy.md). Select exactly one complete interaction contract from the user's language:
   - Simplified Chinese → [zh-CN](references/user-interaction-zh.md)
   - English → [en-US](../../locales/en-US/pack.md)
   - Japanese → [ja-JP](../../locales/ja-JP/pack.md)
   - Traditional Chinese → [zh-Hant](../../locales/zh-Hant/pack.md)
   Read the selected contract completely and use its staged prompts and result states. Do not mix locales or improvise away required warnings and confirmations.
2. Ask for the output location and target OS. Warn that the package can contain private work context.
3. Resolve Python 3.11 or newer. Try `python3`, `python`, then `py -3`.
4. Choose a profile:
   - `core`: memories, guidance, rules, personal Skills, portable preferences.
   - `standard`: core plus personal plugin source, redacted MCP/Hook candidates, managed-plugin inventory, environment inventory, and project metadata.
   - `complete`: standard plus private history and automation definitions.
5. Run inventory before packing:

   ```bash
   python3 "<skill-directory>/scripts/pack_codex_move.py" \
     --output "/absolute/output/directory" --profile standard --dry-run
   ```

6. Summarize categories, size, skipped items, sensitive exclusions, target-OS risks, plugins, and projects. Use `complete`, `--include-history`, or `--include-automations` only after explicitly confirming their privacy and activation implications. The two flags allow adding either optional category to `core` or `standard` independently.
7. Add each project that must be reconstructed with `--project "/absolute/project/path"`. This records metadata only; it never bundles the repository.
8. Prefer authenticated encryption for untrusted transfer or storage:

   ```bash
   python3 "<skill-directory>/scripts/pack_codex_move.py" \
     --output "/absolute/output/directory" --profile standard \
     --age-recipient "<age-recipient>"
   ```

   Require the external `age` command for encrypted packages. Otherwise produce a ZIP and tell the user to use a trusted channel.
9. Run the final pack command. Report the exact path, size, SHA-256, package ID, encryption state, and warnings. Tell the user to carry the SHA-256 separately.
10. Tell the user to transfer the package and invoke `$restore-codex-move` on the new device.

## Non-negotiable safety

- Never include `auth.json`, keychains/keyrings, OAuth state, API keys, tokens, `.env`, shell profiles, raw config, logs, caches, databases, browser state, or installation IDs.
- Never scan arbitrary projects or the whole home directory. Include project metadata only for explicit `--project` paths.
- Never follow symlinks or junctions, overwrite a package, or modify source files.
- Treat review config as a redacted candidate, not active destination configuration.
- Treat managed plugins as a reinstall/reauthorize list; never package downloaded caches.
- Treat automation definitions as inactive data. The receiver must quarantine them.
- Do not promise chat-sidebar, desktop-database, or UI-state restoration.

## Communication contract

- Follow the exact localized contract selected in workflow step 1. Infer the locale from the user's current language; if the user explicitly requests a locale, that request wins.
- Never expose raw script JSON as the user-facing answer. Parse it, humanize sizes and action names, and retain exact paths, hashes, and package IDs.
- Announce each material phase. For long packing, provide a short stage update at least every 30–60 seconds without inventing percentages.
- Require the localized confirmation phrase defined by the selected product contract after the dry run and before creating a package.
- End in exactly one state: completed, completed-with-warnings, safely-refused, or failed-with-partial-output.

## Resources

- Run [pack_codex_move.py](scripts/pack_codex_move.py) for deterministic collection.
- Read [migration-policy.md](references/migration-policy.md) for classification and platform policy.
- Read [package-format.md](references/package-format.md) when diagnosing compatibility or changing the schema.
- Read exactly one user-facing contract for each run: [zh-CN](references/user-interaction-zh.md), [en-US](../../locales/en-US/pack.md), [ja-JP](../../locales/ja-JP/pack.md), or [zh-Hant](../../locales/zh-Hant/pack.md).
