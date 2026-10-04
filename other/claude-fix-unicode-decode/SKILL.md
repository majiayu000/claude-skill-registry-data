---
name: claude-fix-unicode-decode
description: Diagnose and fix UnicodeDecodeError, UnicodeEncodeError, mojibake, and corrupted Chinese text in Claude Code tasks. Use this skill whenever a file, command, test, CSV, JSON, HTTP response, Git diff, or Windows terminal shows broken Chinese, replacement characters, strings such as "ä¸­æ–‡" or "涓枃", an unknown codec, or any decode/encode exception. Use it even when the user only says Chinese text is garbled or a file cannot be read.
---

# Fix Unicode Decode in Claude Code

Treat encoding as a byte-to-text contract. Identify the original bytes, producer, and actual codec before editing. Do not suppress errors with `errors="ignore"`, and do not overwrite a file after decoding it with an unverified codec.

## Diagnose

1. Inspect Git status and preserve the original bytes. Do not revert unrelated user changes.
2. Capture the full exception, codec name, byte offset, failing operation, platform, and exact file or process boundary.
3. Locate the first bytes-to-text conversion: `open`, `Path.read_text`, parser, subprocess, HTTP client, database driver, or terminal.
4. Do not infer the source encoding from Claude Code's `Read` output alone because the display has already crossed a decoding boundary.
5. Use Bash or PowerShell to inspect raw bytes and run the bundled read-only diagnostic:

   ```bash
   python scripts/diagnose_encoding.py path/to/file
   ```

   If the current directory is not this skill directory, resolve the script from the loaded skill's directory first.
6. Prefer evidence in this order: producer or format contract, BOM, protocol declaration, strict decode success, then content plausibility. A successful decode alone is not proof; codecs such as `latin-1` and `gb18030` accept many byte sequences.
7. Reproduce with strict decoding and a representative sample containing Chinese, ASCII, punctuation, and an emoji when the format supports it.

## Repair

- Fix the narrowest boundary that owns the wrong assumption. Add an explicit `encoding=`, configure the child process or terminal, or correct a producer that declares the wrong charset.
- Prefer UTF-8 for new repository text and `encoding="utf-8"` for Python file I/O.
- Use `utf-8-sig` only for a verified UTF-8 BOM or an explicit interoperability requirement such as some Excel CSV workflows.
- Use `gb18030` for legacy Simplified Chinese only when provenance or byte evidence supports it. Prefer it over `gbk` for broader character coverage.
- Use `utf-16` when a BOM exists. Without a BOM, establish endianness from the producer or format.
- Keep byte values as bytes until the intended decoding boundary. Decode once and encode once.
- Use `errors="replace"` only for deliberate lossy display or telemetry, and disclose data loss.
- Do not promise recovery after `U+FFFD` replacement characters or ignored bytes appear unless original bytes or a backup exists.

```python
from pathlib import Path

text = Path(path).read_text(encoding="utf-8")
Path(path).write_text(text, encoding="utf-8", newline="\n")
```

```python
result = subprocess.run(
    command,
    capture_output=True,
    text=True,
    encoding="utf-8",  # Match the child's documented output contract.
    errors="strict",
    check=True,
)
```

Read [references/encoding-playbook.md](references/encoding-playbook.md) for the relevant CSV, JSON, HTTP, database, Windows console, Git migration, or mojibake section. Do not load unrelated sections unless needed.

## Verify

1. Confirm the original failing input now decodes with `errors="strict"`.
2. Assert semantic text such as `中文，编码测试。`; checking only that no exception occurs is insufficient.
3. Run the smallest relevant tests, then inspect `git diff --word-diff` and `git diff --check` for replacement characters, newline churn, or unrelated rewrites.
4. Report the source codec, target codec, supporting evidence, changed boundary, and any lossy operation.

## Diagnostic Output

Use `--json` for machine-readable output and `--encodings` for producer-specific candidates. Treat candidate scores as hints rather than detection guarantees. For ambiguous valid results such as GB18030 versus Big5, ask for provenance or compare known text instead of selecting the top score blindly.
