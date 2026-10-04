---
name: fix-unicode-decode
description: Diagnose and fix UnicodeDecodeError, UnicodeEncodeError, mojibake, and corrupted Chinese text in Codex coding tasks. Use when Python or another tool cannot decode a file or subprocess stream; Chinese text displays as replacement characters or strings such as "ä¸­æ–‡" or "涓枃"; file, terminal, CSV, JSON, HTTP, Git, or Windows encoding behavior is unclear; or a repository needs a safe migration to UTF-8.
---

# Fix Unicode Decode

Treat encoding as a byte-to-text contract. Identify the byte source and actual encoding before changing code or files; never make an error disappear with `errors="ignore"` or an unverified bulk rewrite.

## Workflow

1. Preserve the original bytes. Check Git status before editing and make a backup only when Git cannot restore the file.
2. Capture the full exception, including codec, byte offset, operation, platform, and the code that opened or decoded the data.
3. Identify the boundary that converts bytes to text: `open`, `Path.read_text`, CSV/JSON parser, subprocess, HTTP response, database driver, or terminal.
4. Inspect bytes without first decoding them. Check BOM and run:

   ```powershell
   python scripts/diagnose_encoding.py path/to/file
   ```

5. Select an encoding using provenance first, then BOM/specification, then strict decoding and content plausibility. A successful decode alone is not proof; `latin-1` and `gb18030` accept many byte sequences.
6. Reproduce with strict decoding and a focused test containing Chinese, ASCII, punctuation, and an emoji where the format supports it.
7. Fix the narrowest owning boundary. Specify `encoding=` at file boundaries, configure subprocess or terminal encoding, or correct the producer when its declared charset is wrong.
8. Verify semantic text, byte round-trip behavior when required, tests, and the diff. Do not normalize unrelated files.

## Decision Rules

- Prefer UTF-8 for new repository text and explicit `encoding="utf-8"` in Python.
- Use `utf-8-sig` only when consuming or intentionally producing a UTF-8 BOM, commonly for Excel interoperability.
- Use `gb18030` for legacy Simplified Chinese data only when provenance or byte evidence supports it. Prefer it over `gbk` for broader compatibility.
- Use `utf-16` when a BOM is present. Without a BOM, establish endianness from the format or producer before choosing `utf-16-le` or `utf-16-be`.
- Keep `bytes` as bytes until the correct boundary. Decode once and encode once.
- Use `errors="replace"` only for deliberate lossy display or telemetry and report the data loss. Never use it to migrate source data.
- Do not attempt to repair text containing `U+FFFD` unless the original bytes are available; the replacement may already have destroyed information.

## Common Fixes

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
    encoding="utf-8",  # Match the child process, not a guess.
    errors="strict",
    check=True,
)
```

For CSV, JSON, HTTP, Windows console, Git, and mojibake repair patterns, read [references/encoding-playbook.md](references/encoding-playbook.md). Load only the relevant section.

## Verification

- Confirm the exact failing input now decodes under `errors="strict"`.
- Assert representative Chinese text such as `中文，编码测试。` rather than only checking that no exception occurs.
- Re-run the smallest relevant test suite, then inspect `git diff --word-diff` or a byte-level diff for unexpected churn.
- State the detected source encoding, chosen target encoding, evidence, changed boundary, and whether any decoding was lossy.

## Diagnostic Script

Run `scripts/diagnose_encoding.py` on one or more files. Add `--json` for machine-readable output or `--encodings` to test known producer-specific codecs. The script is read-only, uses strict decoding, and ranks candidates heuristically; treat its ranking as evidence, not certainty.
