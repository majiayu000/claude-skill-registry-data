---
name: snbt-validation
description: Validate and lint FTB SNBT files (FTB Quests SNBT, FTB Library / Chunks / Ultimine / Teams configs, KubeJS data files, vanilla-SNBT typed arrays). Use when adding, editing, or reviewing any ``*.snbt`` file in this repo — including when the pre-commit hook blocks a commit, when CI surfaces an SNBT diagnostic, when authoring FTB Quests chapters, when receiving a quest-validator JSON report, or when porting SNBT between tools. Surfaces precise line:col diagnostics for malformed grammar; never silently passes broken input.
---

# SNBT Validation

Validate FTB Stringified NBT files against the grammar documented at https://docs.feed-the-beast.com/mod-docs/mods/technical/SNBT/. The validator lives at `scripts/validate_snbt.py`; the test suite at `scripts/test_validate_snbt.py`; the pre-commit hook at `.githooks/pre-commit`. None of this requires network access — everything runs offline against the working tree.

## When to use

- Before committing any `*.snbt` change locally (the hook does this automatically; run the validator manually when the hook is bypassed with `--no-verify`).
- When the pre-commit hook blocks a commit and reports one or more `file:line:col` diagnostics.
- When authoring FTB Quests chapters, FTB Library/Chunks/Ultimine/Teams configs, or KubeJS data files.
- When porting SNBT from another tool (JEIT/NBT Studio, Amulet, vanilla `/data get`) into FTB's dialect.
- When CI emits an SNBT validator report and you need to map it back to a fix.

## Quick start

```sh
# Validate every .snbt file under a directory (recursively):
python scripts/validate_snbt.py config/

# Validate explicit files:
python scripts/validate_snbt.py config/ftbchunks-client.snbt kubejs/data.snbt

# JSON output for CI / pipelines:
python scripts/validate_snbt.py --format json config/ > snbt-report.json

# Disable ANSI color when piping or logging:
python scripts/validate_snbt.py --no-color config/
```

Exit codes:

| Code | Meaning |
| ---: | --- |
| `0` | Every target validated cleanly. |
| `1` | One or more diagnostics found. The validator prints each `file:line:col-line:col` issue with a code and human-readable message. |
| `2` | Invocation error (missing path, unreadable file, bad flag). |

## What it checks

The validator enforces the structural FTB SNBT grammar. It does **not** check semantics — a key being the right type for a particular mod's config schema is the mod's job.

- `#` line comments (skipped at the lexer level).
- Single- and double-quoted strings with `\\` escapes; flags unterminated strings precisely.
- All numeric forms: `<int>`, `<float>`, hex `0x...`, with every FTB suffix (`b/B/s/S/l/L/f/F/d/D`); signed numbers (`-128b`, `-1.5d`); the special literals `∞`, `-∞`, `∞F`, `-∞F`, `NaN`, `NanF`.
- Booleans `true` / `false` (unquoted). Quoted `"true"` / `"false"` are strings, not booleans.
- Unquoted identifier keys (and quoted `"with spaces"` keys).
- `{...}` and `[...]` with FTB's defining rule: **same-line multi-element values require `,`; values on different lines are separated by newlines alone**.
- Vanilla SNBT backward-compat typed-array syntax `[B; ...]`, `[I; ...]`, `[L; ...]`.
- Empty containers: `{}`, `[]`, `info_settings: { }`.
- UTF-8 BOM tolerance (FTB-generated configs sometimes include one).
- Duplicate keys inside the same compound (within the scope of a single object — nested objects are independent).

## Reading diagnostics

Every diagnostic has the shape `path:line:col[-end_line:end_col]: code: message`. The `code` is stable and machine-greppable; the message is human-readable with the previous-token context that triggered the report.

| Code | Triggered by |
| --- | --- |
| `lex_error` | Invalid character, unterminated string, malformed number. |
| `expected_token` | A structural token (`:` after a key) is missing. |
| `missing_value` | A key's `:` is followed immediately by `}`, `,`, or EOF. |
| `missing_comma` | Two values appear on the same source line with no `,` between them (FTB requires commas only on same-line sequences). |
| `unterminated_object` / `unterminated_array` | `}` or `]` expected before EOF. |
| `unterminated_string` | Closing quote never found. |
| `invalid_value` | Bare identifier used as a value where a number / string / object was expected. |
| `invalid_key` | Object key position holds a punctuation token (commonly a stray `}`). |
| `duplicate_key` | Same key appears twice in the same compound. |
| `expected_comma_or_close` | The internal fallback when something genuinely unexpected appears after a value (e.g. a stray `}` mid-object). |
| `trailing_comma` | Array / object ends with a stray `,`. |
| `typed_array_syntax` | `[B`/`[I`/`[L` seen without the required `;` separator. |
| `typed_array_element` | `[I; "not a number"]` — wrong element type for the prefix. |
| `trailing_tokens` | Extra tokens after the top-level structure ended. |
| `empty_file` | File is empty. |
| `encoding_error` / `io_error` | File is not valid UTF-8 or cannot be read. |

When a fix is ambiguous (multiple ways to satisfy the grammar), the message includes the previous-item location so you can pick the right one.

## Pre-commit integration

The hook at `.githooks/pre-commit` chains two checks for every commit:

1. `packwiz refresh` (existing — keeps `index.toml` honest and re-stages it).
2. `python scripts/validate_snbt.py --no-color` on every staged `*.snbt` file.

If the validator exits non-zero the commit is aborted; nothing is staged. The hook is **not** active by default — opt in with:

```sh
git config core.hooksPath .githooks
```

Run that once per clone. CI should mirror the same command (see the JSON format for greppable output).

## Validator fallibility — read before trusting a pass

The validator is a **structural grammar checker, not a game**. It proves a file is
well-formed SNBT; it cannot prove the file is *correct for the game*. Both false
negatives (broken file passes) and false positives (working file flagged) exist.
Known limits, each verified by probe:

### False negatives — things it will PASS that are still wrong

- **Semantics are entirely out of scope.** A fully "valid" file can reference
  nonexistent items (`totally_fake_mod:item`), unknown quest fields
  (`not_a_real_field: 42`), broken dependencies, or malformed data-component codecs
  (e.g. an Iron's Spells scroll missing `maxSpells`/`index`) and get a clean pass.
  Schema correctness is the mod's job; use the pack's other checks (`packwiz`
  validation, in-game loading, `docs/vvh/SPELL_SCROLL_FORMAT.md`).
- **Formatting-code corruption is invisible.** `title: "A & B"` parses fine but
  breaks FTB Quests at render time (`Invalid formatting! You must escape whitespace
  after & with \&!`). The validator does not scan string contents.
- **Game-invalid values inside valid syntax.** `level: 99` on a capped spell,
  counts of 0, negative prices — all grammar-clean.

### False positives — things it FLAGS that actually work in game

- **Unquoted strings containing spaces are rejected** (`invalid_value`). Some FTB
  contexts tolerate them, but never rely on it: quote the string. Treat this flag
  as advice to fix your file, not a validator bug to work around.
- **Unquoted keys containing dots or leading digits are rejected** (`lex_error` /
  `invalid_key`). Quote such keys (`"some.key": ...`) if you genuinely need them.
- **Single-quoted strings cannot contain apostrophes** — `'it's'` reports
  `unterminated_string`. FTB has no documented `\'` escape; reword or switch to
  double quotes.

### Practical trust model

1. A **pass** means: balanced structure, legal tokens, no duplicate keys. It does
   NOT mean the quest works.
2. A **flag** usually means real breakage, but read the message — the unquoted-
   string cases above are strictness, not correctness.
3. Grammar-clean is necessary, not sufficient. Always pair it with at least one
   semantic check: in-game load of the chapter, `/createScroll`-style runtime probes,
   or the scripted graph audits used in this repo.

## Authoring tips

- When in doubt about grammar, copy a known-good file (`config/ftbchunks-client.snbt` is a comprehensive real-world sample) and edit from there.
- FTB's multi-line comma rule is the most common stumbling block. The validator reports `missing_comma` only when items share a source line; a fresh newline between entries is always valid.
- Vanilla `[I; 1, 2, 3]` is accepted; the FTB extension just adds multi-line support on top.
- Trailing commas inside `[...]` and `{...}` are rejected. If your editor adds them automatically, configure it not to.
- `[B; ]` (empty typed array) is allowed and is in fact what `ftblibrary-client.snbt` uses to initialize an empty int-array — keep it that way.

## Extending or testing

The validator ships with a self-contained test suite at `scripts/test_validate_snbt.py`. Run it with:

```sh
python scripts/test_validate_snbt.py
```

It walks both synthetic valid/invalid samples and every real `*.snbt` in the repository as an integration check. Add new tests when introducing a new diagnostic code or supporting a new SNBT construct; the existing `ValidSamples` / `InvalidSamples` split is the convention.