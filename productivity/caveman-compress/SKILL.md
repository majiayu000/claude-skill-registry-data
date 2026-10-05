---
name: caveman-compress
description: "Manual Caveman-style prose compressor for Markdown or plain-text memory and instruction files, with invariant validation, unified-diff preview, explicit approval, atomic replacement, and timestamped backup. Use only when explicitly invoked as $caveman-compress, /caveman-compress, 'Caveman compress', or an unambiguous Caveman memory-file compression request. Never activate for ordinary summarization, ZIP/archive compression, or generic file cleanup; never overwrite during preview. Turkish triggers: Caveman compress, mağara modu metin sıkıştırma."
license: MIT
---

# Caveman Compress

Compress prose without silently changing meaning. The bundled script performs
no network or model call. Use the active agent to draft the candidate, then use
the script for deterministic checks.

Safety-adapted from [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman), MIT licensed. Preserve the included `LICENSE` when redistributing.

Read [compression-safety.md](references/compression-safety.md) before creating
a candidate.

## Supported targets

- UTF-8 Markdown, plain text, or extensionless natural-language files.
- Maximum source size: 1 MiB.
- Never target code/config formats, symlinks, existing backup files, or the
  candidate itself.

## Safe workflow

1. Read the entire source and create a separate candidate file. Do not edit
   the source.
2. Preserve every item listed in the safety reference and perform the semantic
   ledger review.
3. Run the validator in preview mode. Preview is the default and never writes
   the source:

   ```powershell
   py -3 "<skill-dir>\scripts\caveman_compress.py" "<source>" --candidate "<candidate>"
   ```

   If `py -3` is unavailable, use `python` with the same arguments.

4. Review the invariant report, reduction metrics, and unified diff. Fix the
   candidate separately and rerun preview until it passes. Do not weaken the
   validator to make a candidate pass.
5. Show the user the proposed change, validation result, residual semantic
   risk, and backup behavior.
6. Apply only when the user explicitly approved overwriting that exact source
   after seeing the preview, or explicitly requested replacement in the same
   turn. Reuse both hashes printed by preview:

   ```powershell
   py -3 "<skill-dir>\scripts\caveman_compress.py" "<source>" --candidate "<candidate>" --apply --user-approved-write --expected-source-sha256 "<source-hash>" --expected-candidate-sha256 "<candidate-hash>"
   ```

7. Report the timestamped backup path and final hash. Keep the backup until the
   user verifies the result.

## Non-negotiable gates

- Validation errors block apply.
- Source or candidate hash drift blocks apply.
- `--apply` without `--user-approved-write` blocks apply.
- Apply revalidates immediately before an atomic replacement.
- The exact original bytes are copied to a timestamped backup first.
- A validator cannot prove semantic equivalence. Complete the semantic ledger
  and diff review even when every automated check passes.

Do not call a named provider, select a model, install dependencies, or send
file contents to an external service.
