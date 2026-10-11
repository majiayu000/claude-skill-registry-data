---
name: prove-file-integrity-not-renderer-loss
description: "Settle a suspected file-corruption or \"the edit dropped lines\" scare in this environment before editing anything — distinguish renderer/tool-proxy artifacts (compressed reads, rtk-reshaped git stdout, CRLF-vs-LF hashes, text-scan guard tests) from real on-disk damage. Use whenever a read looks garbled, a hash mismatches, or a repo guard test flags code you just wrote."
---

# Prove file integrity, don't infer it

In this environment most "the file is corrupted" alarms are **instrument failures**, not
defects. Editing based on a lossy render is how real corruption gets introduced. Settle the
question with tools that cannot compress, then act.

## The three instruments that lie

| Symptom | Looks like | Actually is |
|---|---|---|
| Read comes back with words dropped mid-sentence | File damaged by an edit | Renderer compressing a large read |
| `sha256sum file` ≠ `git show HEAD:file \| sha256sum` | Working file diverged | `git show` emits LF, working tree is CRLF (autocrlf) — **and** rtk reshapes git stdout. Two independent reasons it can never match |
| Repo guard test flags a pattern in new code | Real defect introduced | Guard is a **text scan**: e.g. a tuple field named `Result` trips a `.Result` sync-over-async guard |

## Arbiters that don't lie

Run these before believing any corruption claim:

```bash
# 1. Exact content, independent of the renderer — quote a long literal from the region
grep "<40+ chars of the exact literal>" path/to/File.cs      # grep TOOL, not shell grep

# 2. Is the working file identical to what was committed? EXIT CODE, not text
git diff --quiet HEAD -- path/to/File.cs; echo $?            # 0 = identical
git diff --quiet HEAD; echo $?                               # whole tree
git status --porcelain | wc -l                               # 0 = clean

# 3. Only if you must read the region, read raw in SMALL slices
read path/to/File.cs:raw:826-846                             # ~12-20 lines survives intact
```

**Never** byte-compare through a git proxy (rtk) — its stdout is reshaped by design. Exit
codes are the only trustworthy signal through it.

## Order of operations

1. A render looks garbled → re-read `:raw` in a ~12-line slice. Usually clean.
2. Still suspicious → `grep` the exact literal. Found verbatim = content is fine, stop.
3. Claim is "differs from commit" → `git diff --quiet HEAD -- <file>`, read the exit code.
4. Only if 1–3 disagree with each other is there real damage. Then recover from
   `git show HEAD:<file>` rather than retyping from a render.

## Guard-test false positives

A repo text-scan guard (sync-over-async detectors, forbidden-API scans) cannot see types.
When it flags code you believe is correct:

- Confirm the mechanism by reading the cited line (`(await FooAsync()).Result` on a tuple is
  not `Task.Result`).
- Then **still rename the shadowing identifier**. If the guard can't tell, neither can the
  next reader. Renaming beats suppressing the guard or arguing with it.

## What a compile actually proves

A green build bounds damage to **whitespace, comments, and string literals** — none of which
the compiler checks. So a passing build plus a suspicious render means: check literals and
comments specifically (step 2 above), not structure.
