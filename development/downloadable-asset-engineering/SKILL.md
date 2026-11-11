---
name: downloadable-asset-engineering
description: "Builds and releases self-contained downloadable ZIP assets (skill packs, template kits, example projects, small local tools) so the released bytes, not just the source folder, are proven to work: deterministic packaging, a manifest and checksums, archive-safety checks, validators with negative fixtures, and honest PASS/BLOCKED/NOT RUN evidence. Use when someone says 'package this as a download', 'make a release zip', 'ship this kit', 'is this zip safe to publish', or when a lead magnet or skill bundle must install cleanly for a stranger. Bundled scripts are Python standard library only."
---

# Downloadable Asset Engineering

Ship a ZIP that works for a stranger, and prove it from the bytes you publish.

```
source folder  !=  staged package  !=  released ZIP  !=  extracted install
```

Test each layer on its own. Passing one never proves the next.

## Inputs to pin down first

Write these as a short contract before building (ask for anything missing):

1. Archive name and top-level folder name (for example `acme-skill-pack-1.2.0.zip` / `acme-skill-pack/`).
2. Required file tree and where the version number lives.
3. How it is installed (copy a folder, unzip into `~/.claude/skills/`, npm, etc.).
4. The promise: what a user can do after installing. Anything not promised is out of scope.
5. Data: only public, fictional or explicitly authorised content goes inside.

## Steps

1. **Write the checks before the asset is "done".** For anything executable
   (validators, builders), add one behavioural test, watch it fail for the right
   reason, implement, rerun, repeat. Good first tests: missing required file,
   malformed frontmatter, unsafe archive path, two builds identical.
2. **Make it standalone.** Every template, schema, example and script the
   promise depends on is inside the ZIP. No hidden dependency on a paid service,
   private repo, credential or network call unless the promise says so.
3. **Package validator** (write one per asset, keep it stdlib-only): required
   tree, frontmatter fields, unique names, every referenced local path exists,
   UTF-8, no symlinks, no machine paths (`/Users/`, `/home/<name>`, `C:\Users`),
   no secret-looking strings. Report file and category only, never the value.
4. **Build deterministically:**
   ```bash
   python scripts/build_zip.py ./my-kit dist/my-kit-1.0.0.zip --top my-kit
   python scripts/build_zip.py ./my-kit /tmp/rebuild.zip --top my-kit
   cmp dist/my-kit-1.0.0.zip /tmp/rebuild.zip && echo reproducible
   ```
   The builder sorts entries, fixes timestamps and permissions, drops `.git`,
   caches, `.DS_Store`, `.env*`, old zips and symlinks, and writes `MANIFEST.json`
   plus `SHA256SUMS` inside the archive (neither lists itself).
5. **Verify the released bytes:**
   ```bash
   python scripts/verify_zip.py dist/my-kit-1.0.0.zip --sha256 <digest from build> --extract-to /tmp/fresh
   ```
   Checks traversal, absolute paths, symlinks, duplicate and case-colliding names,
   single top folder, manifest and checksum agreement, then extracts and re-hashes.
6. **Use the extracted copy, not the source.** In `/tmp/fresh`: rerun the package
   validator, run the included sample, follow the README install steps word for
   word on a clean path.
7. **Host tests, reported separately.** If the asset runs inside Claude Code,
   Claude.ai or another app, test and record each of these on its own:
   discovered/listed, explicit invocation works, automatic selection works,
   safe behaviour on missing or bad input, end-to-end output. A skill showing up
   in a list does not prove it runs.
8. **Write the release evidence** using the template in
   `references/release-testing-and-evidence.md`.

## Evidence labels (use only these)

- **PASS**: the command reached the behaviour and the assertions held.
- **EXPECTED FAIL**: a deliberately bad fixture was rejected for the intended reason.
- **BLOCKED**: a prerequisite (auth, licence, host outage) stopped the test before the behaviour.
- **NOT RUN**: no execution evidence.

Never upgrade BLOCKED or NOT RUN to PASS. Finish every independent layer anyway
and state the remaining gap at the top of the handoff.

## Decision rules

- Two builds differ: find the nondeterministic input (timestamps in generated
  files, unsorted globbing, a manifest written into the source) and fix it. Do
  not publish until `cmp` is silent.
- Any file over ~5 MB: question it. Media in a first release needs a reason and a
  metadata scrub.
- The sample output is a golden file: it shows the expected shape, not proof
  that today's model produced it. Label it that way.
- A secret or personal detail found by the scan: remove it from the source,
  rebuild, re-verify. If it was ever published, treat it as leaked and rotate it.

## Output

Deliver: the ZIP, its SHA-256 (published next to the download), and
`RELEASE-EVIDENCE.md`. Example summary line for the handoff:

```
my-kit-1.0.0.zip  18,432 bytes  sha256 3f9a...c21e  14 entries
Reproducible: PASS (2 builds identical)  Archive safety: PASS
Extracted sample: PASS  Claude Code discovery: PASS  Auto-selection: BLOCKED (no host auth)
```

## Pitfalls

- Calling "zip created" a release check.
- Validating the source sample but never the extracted copy.
- Builder machine paths leaking into docs or generated outputs.
- Leaving caches, debug output or old archives inside the ZIP.
- SHA-256 proves integrity against a trusted digest, not who made the file.
