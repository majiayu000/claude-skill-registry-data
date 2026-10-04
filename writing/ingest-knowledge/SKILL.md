---
name: ingest-knowledge
description: Structure a completed, verified transcript artifact into evidence-linked knowledge notes and write them idempotently into an existing local Obsidian vault. Use when a user asks to archive, deposit, save, or turn transcribed content into durable Obsidian knowledge; when $transcribe-media hands off a completed transcript after user confirmation; or when validating and deduplicating an intended transcript-based knowledge note. Never write before the user has selected or confirmed the target vault.
---

# Ingest knowledge

Create one durable knowledge note plus one preserved source note. Treat the source artifact as evidence and keep model inference visibly separate.

## Runtime boundary

- Use Python 3.11–3.14 on macOS or Linux. The secure path, lock, journal, and recovery guarantees are POSIX-only.
- The script requires `fcntl`, directory-FD operations, `O_NOFOLLOW`, `O_DIRECTORY`, directory `fsync`, atomic no-replace rename, and atomic exchange rename; missing primitives produce `UNSUPPORTED_PLATFORM` rather than an unsafe fallback.
- Runtime validation uses the skill's vendored canonical contracts and the Python standard library. Success is exactly one JSON object on stdout, empty stderr, and exit 0; an expected failure is empty stdout and exactly one redacted JSON error on stderr.
- Repository-wide failure codes are: 2 for arguments, schemas, or unsafe inputs/paths; 3 for unavailable dependencies, models, or platform capabilities; 4 for locks, conflicts, recovery conflicts, or stale plans; 5 for external-tool, network, or runtime I/O failures; 7 for contract, identity, or file-evidence integrity failures; and 130 for interruption.

## Workflow

1. Resolve an existing vault. Prefer a path the user already supplied or a configured `OBSIDIAN_VAULT_PATH`. If neither exists, ask for the vault path. Do not scan the entire home directory.
2. Validate the transcript artifact before using it:

   ```bash
   python3 scripts/knowledge_writer.py validate-transcript "<transcript.json>"
   ```

   Accept only a complete `awesome-capture.artifact/v2` transcript that passes the vendored structural and semantic validator. Reject v1, unknown versions, unknown fields, invalid hashes or timestamps, and contract-digest mismatches. Do not migrate or double-read legacy artifacts.
3. Read the full transcript. Draft a Markdown body outside the vault using [note-schema.md](references/note-schema.md).
   - Use only claims supported by transcript timestamps.
   - Label inference as inference.
   - Put unresolved or externally sourced claims under “待验证”.
   - Do not invent quotations, speakers, dates, or context.
   - Include exactly one H1 and at least two H2 sections. The writer replaces the draft H1 with the explicit `--title` so the body, frontmatter, and filename remain consistent.
4. Choose a collection folder inside the vault. Use the vault's existing convention; otherwise use `00 Inbox`. Keep a separate source folder, default `90 Sources`. Link style defaults to the `$build-obsidian-vault` receipt when present and to portable Markdown links otherwise; pass `--link-style` only to override it.
5. Run a dry run:

   ```bash
   python3 scripts/knowledge_writer.py commit \
     --transcript "<transcript.json>" --document "<draft.md>" \
     --vault "<vault>" --title "<title>" --collection "<folder>" --dry-run
   ```

6. Inspect the returned destinations and copy the full `plan_sha256`. If they are correct and writing is authorized, commit that exact plan:

   ```bash
   python3 scripts/knowledge_writer.py commit \
     --transcript "<transcript.json>" --document "<draft.md>" \
     --vault "<vault>" --title "<title>" --collection "<folder>" \
     --expected-plan-sha256 "<plan_sha256>"
   ```

   Repeat every option used during dry-run, including `--sources-dir`, `--tag`, `--link-style`, or `--allow-plain-folder`. A changed transcript, draft, title, destination, tags, link style, or build receipt that changes the resolved link style requires a new dry-run. The writer recomputes the plan inside the exclusive vault lock and returns `STALE_PLAN` if it changed.

   The writer does not reopen source media by default. Only when the user explicitly asks for that extra check, add `--verify-source-media` to the final command. A missing source then records `not_available`; a present but mismatching source fails integrity validation.
7. Run the read-only ingest audit:

   ```bash
   python3 scripts/knowledge_writer.py audit --vault "<vault>"
   ```

8. Report the absolute knowledge-note path, preserved-source path, receipt path, `plan_sha256`, and whether the operation returned `created` or `reused`. This write is already authorized when the user explicitly invoked this skill or answered yes to `$transcribe-media`.

All lock-taking commands accept `--lock-timeout`; the default is 30 seconds. A timeout returns `VAULT_BUSY`.

## Transcript and receipt contracts

- Validation is internal by default: it verifies the transcript object's structure, identities, segment ordering and bounds, deterministic text, chunk manifest, output hashes recorded in the artifact, and no-speech consistency. It does not require the original media, upstream video artifact, subtitle files, or transcript output files to remain on disk.
- The source note is generated from the validated transcript artifact. Deleting the source media or upstream artifact does not prevent ingest.
- Stable identity is:

  `SHA256("awesome-capture.ingest-id/v1\0" + canonical_transcript_artifact_sha256)`

  The full 64-character digest is both the receipt filename and the `awesome_capture_id` identity carried by generated notes.
- The completion marker is `<vault>/.awesome-capture/receipts/<ingest-id>.json`, conforming to `awesome-capture.ingest-receipt/v1`. It records transcript artifact, semantic, and source hashes; draft, request, and confirmed-plan hashes; relative note paths; link style; initial file hashes and identity markers; source-verification status; and producer contract identity.
- The receipt is published last. A matching transcript, draft, and destination returns `reused`. The same ingest ID with a different draft or destination returns `INGEST_ID_CONFLICT`; an occupied destination without the matching receipt returns `PATH_COLLISION`.
- A legacy receipt for the same source blocks ingest with `UNSUPPORTED_RECEIPT_SCHEMA`. Legacy receipts and artifacts are never silently upgraded, overwritten, or treated as valid completion markers.

## Reliability rules

- Require a completed source artifact. Never turn a failed or metadata-only download into a knowledge note.
- Never overwrite an unrelated note. A path collision without a matching receipt is a hard error.
- Keep writes within the resolved vault and reject absolute or parent-traversing collection paths.
- Reject filesystem roots, the user's home directory, and `.obsidian` itself as write targets.
- Reject symbolic-link path components, hardlinked managed files, special files, unsafe ownership, and directories writable by other users. Keep `.awesome-capture`, receipts, locks, and journals private; generated Markdown is normal `0644` vault content.
- Write through private same-filesystem staging and no-clobber publication. The knowledge note and source note are published before the receipt, using an `awesome-capture.transaction/v1` journal.
- Build and ingest share `<vault>/.awesome-capture/vault.lock`. Commit and recovery take the exclusive lock; audits take a shared lock. Equivalent concurrent commits serialize to one `created` result followed by `reused`.
- Before a commit, the writer automatically completes a provably matching pending ingest transaction. Explicit recovery is:

  ```bash
  python3 scripts/knowledge_writer.py recover --vault "<vault>"
  ```

  Unknown files, unsafe paths, or hash mismatches return `RECOVERY_CONFLICT`; they are not overwritten or removed.
- `audit` is read-only and never repairs. It validates every formal ingest receipt, full stable ID, relative paths, note identity frontmatter, initial hashes, and pending ingest transactions. A modified body with intact identity is a `CONTENT_MODIFIED` warning and is never overwritten; a missing or mismatching identity, forged/legacy receipt, missing note, symlink, or pending transaction makes `healthy` false.
- Never edit Obsidian's global registry or launch its GUI.
- Keep all Cookie values, API keys, private headers, and hidden diagnostics out of notes.
- Do not install community plugins. The output must remain ordinary Markdown/YAML.
