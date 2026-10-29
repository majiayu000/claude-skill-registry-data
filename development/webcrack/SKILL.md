---
name: webcrack
description: "Deobfuscate, unminify and unpack bundled JavaScript into readable modules and a deobfuscated copy. Use when a webpack or browserify bundle must be read or fed to jsluice. Not for extracting endpoints directly (use jsluice) or executing untrusted code."
---

# webcrack

webcrack takes minified or obfuscated JavaScript and reverses the common transformations: string-array obfuscation, self-defending wrappers, debug protection, minified names and JSX. If the file is a bundle, it also extracts individual modules and records the bundler structure.

It is a static transformer. It parses and rewrites source; it never runs the input.

## When to use

| Goal | Command shape |
| --- | --- |
| Readable copy of one script | `webcrack app.js -o out/` |
| Unpack a webpack/browserify bundle | `webcrack bundle.js -o out/` |
| Keep the bundle intact, only clean it | `webcrack bundle.js -o out/ --no-unpack` |
| Skip deobfuscation, just unminify | `webcrack bundle.js -o out/ --no-deobfuscate` |
| Keep original formatting, only deobfuscate | `webcrack bundle.js -o out/ --no-unminify` |
| Avoid Babel JSX output | `webcrack bundle.js -o out/ --no-jsx` |
| Overwrite a previous run | `webcrack bundle.js -o out/ --force` |
| Pipe source instead of a file | `cat bundle.js \| webcrack -o out/` |
| Prepare input for jsluice | `webcrack bundle.js -o out/ && jsluice urls out/*.js` |

Use `jsluice` when you only need endpoints or secrets; run webcrack when the code must be understood or when string-array obfuscation hides the URLs.

## Prerequisites

- Binary at `/opt/node/bin/webcrack`; `webcrack --version` prints `2.16.0`.
- Node.js 24.22.1 is installed alongside it.
- Input is a file argument or stdin. Output defaults to stdout; pass `-o` to write a directory.
- The output directory must not exist unless `-f` is given.
- No network access is used. No keys are required.

Option names matter on this build. There are no positive `--unpack`, `--deobfuscate` or `--jsx` flags. All four transforms are enabled by default and are controlled only through their `--no-` forms:

```text
--no-jsx           do not decompile JSX
--no-unpack        do not extract modules from the bundle
--no-deobfuscate   do not deobfuscate the code
--no-unminify      do not unminify the code
```

## Core invocations

```sh
# 1. full pipeline into a fresh directory
webcrack bundle.js -o out/

# 2. stdin input, same output layout
cat bundle.js | webcrack -o out/

# 3. stdout when no output directory is given
webcrack bundle.js > deobfuscated.js

# 4. single-file clean-up, no module extraction
webcrack bundle.js -o out/ --no-unpack

# 5. skip obfuscation reversal, keep unminify and unpack
webcrack bundle.js -o out/ --no-deobfuscate

# 6. preserve original formatting, only reverse obfuscation
webcrack bundle.js -o out/ --no-unminify

# 7. suppress JSX decompilation for non-React code
webcrack bundle.js -o out/ --no-jsx

# 8. overwrite an existing output directory
webcrack bundle.js -o out/ --force

# 9. inspect what the unpacker detected
cat out/bundle.json

# 10. list every produced artifact
find out -type f | sort

# 11. feed the deobfuscated tree to jsluice
find out -name '*.js' | jsluice urls -c 4
```

A full run on a two-module test bundle produced:

```text
out/deobfuscated.js
out/bundle.json
out/0.js
out/2.js
```

`bundle.json` records the detected bundler and the module map:

```json
{
  "type": "webpack",
  "entryId": "",
  "modules": [
    { "id": "0", "path": "./0.js" },
    { "id": "2", "path": "./2.js" }
  ]
}
```

Module filenames come from the bundler's module IDs, not from original paths. `entryId` is empty when the entry cannot be determined.

| Artifact | When it appears | Contents |
| --- | --- | --- |
| `deobfuscated.js` | always | transformed source as one file |
| `bundle.json` | bundle detected and unpack enabled | bundler type, entry, module list |
| `<id>.js` | one per extracted module | individual module source |
| stdout | no `-o` given | the same transformed source, not a directory tree |

With `--no-unpack`, only `deobfuscated.js` is written.

## Flags that matter

| Flag | Effect | Note |
| --- | --- | --- |
| `-o, --output` | output directory | must not exist without `-f` |
| `-f, --force` | overwrite output directory | reuse a previous path |
| `-m, --mangle` | mangle variable names | smaller, less readable output |
| `--no-jsx` | disable JSX decompilation | default JSX handling is on |
| `--no-unpack` | keep the bundle as one file | default unpack is on |
| `--no-deobfuscate` | skip obfuscation transforms | default deobfuscate is on |
| `--no-unminify` | keep original whitespace | default unminify is on |
| `-V, --version` | print version | `2.16.0` |
| `-h, --help` | print options | authoritative for this build |

Transform log lines name the stages that ran: `String Array`, `self-defending`, `debug-protection`, `jsx`, `merge-object-assignments` and `evaluate-globals`. Absence of a stage in the log means it found nothing to change, not that it was skipped.

## Limits

- Obfuscation is best-effort. String arrays protected by a runtime rotation or a decryption function may remain. Control-flow flattening is only partly reversed.
- Values that require execution (network responses, `eval` of an encrypted blob, date-seeded decoding) are not recovered.
- webcrack does not fetch source maps. Check for `//# sourceMappingURL=` first; a real map beats any deobfuscator.
- Bundler support is heuristic. Unusual or custom loaders may yield `deobfuscated.js` with no `bundle.json`.
- React output depends on Babel parsing. If JSX transforms fail, retry with `--no-jsx --no-unminify`.
- Very large bundles can exhaust Node's heap; raise `--max-old-space-size` on the node invocation if needed, or split the bundle.
- When the result is still unreadable, fall back to `jsluice tree` / `jsluice query` for the specific construct, Chrome DevTools pretty-print plus live breakpoints, or manual AST work.

## Workflow

1. **Check for source maps.** A `.map` file or an inline `sourceMappingURL` gives original sources with no guessing.
2. **Fingerprint the file.** Bundler banner, `webpackJsonp`, `__webpack_require__`, browserify wrappers, or `_0x` string arrays tell you what to expect.
3. **Run the full pipeline** into a new directory; keep the original untouched.
4. **Read `bundle.json`.** It tells you whether unpacking worked and which module is the entry.
5. **Run jsluice over the output** to recover endpoints before reading code line by line.
6. **Escalate selectively.** Only the modules reachable from the entry matter; do not audit every vendor chunk.

## OPSEC and telemetry

- webcrack is fully local and makes no network requests. Nothing about the target is transmitted.
- Never execute the input or the output. Obfuscated bundles are a common malware delivery format; run analysis in a disposable container with no credentials mounted.
- Output preserves embedded secrets, tokens and personal data from the original bundle. Store it like the original.
- `--force` deletes the target directory. Point `-o` at a dedicated scratch path, never at a repository root.
- Mangled output (`-m`) is harder to compare across runs; keep the unmangled copy as evidence.

## Failure modes

| Symptom | Cause | Fix |
| --- | --- | --- |
| `output directory already exists` | previous run present | choose a new `-o` or add `--force` |
| No files written | no `-o`, so output went to stdout | redirect or pass `-o` |
| `Cannot find module` / stack trace | input path wrong | check the path, or pipe via stdin |
| Parse error | syntax the parser rejects, often minified JSX | retry with `--no-jsx` or `--no-unminify` |
| `bundle.json` missing | no supported bundler detected | use `deobfuscated.js`; inspect manually |
| Output identical to input | already clean, or all transforms disabled | check flags; this is expected for clean code |
| Still `_0x...` names after run | runtime string-array protection | manual AST work or dynamic instrumentation |
| Process killed | heap exhaustion on a large bundle | raise Node heap, split the file |
| Module files are tiny wrappers | lazy chunk boundaries | locate the entry module and follow imports |

## Verification

```sh
webcrack --version
# 2.16.0

webcrack --help | sed -n '1,20p'
# shows -o, -f, -m and the four --no-* transforms

webcrack bundle.js -o /tmp/wc-check
find /tmp/wc-check -type f | sort
# deobfuscated.js, bundle.json, and one file per module
```

Confirm the output parses and is non-empty before handing it on:

```sh
node --check /tmp/wc-check/deobfuscated.js
wc -l /tmp/wc-check/deobfuscated.js
```

If `node --check` fails, the input was probably not valid standalone JavaScript; try `--no-unminify` before concluding the bundle is hostile.

## Related skills

- [jsluice](../jsluice/SKILL.md) to extract endpoints and secrets from the output
- [web-traffic-js-reversing](../web-traffic-js-reversing/SKILL.md) for the capture-to-OpenAPI pipeline
- [httpx](../httpx/SKILL.md) to find the scripts worth downloading
- [mitmproxy](../mitmproxy/SKILL.md) to capture scripts from a live session
