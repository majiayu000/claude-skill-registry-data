---
name: ccr
description: >-
  ccr — reversible payload compression: shrink any blob (tool output, log, RAG
  chunk, file) BEFORE it enters an LLM's context, while caching the full
  original locally so it can be expanded byte-for-byte on demand. The
  payload-axis counterpart to a knowledge-graph loader (the retrieval axis):
  the model sees a compact lossy view + a handle (ccr://<sha256>), and calls
  retrieve(handle) only when it needs the bytes back. Content-routed
  deterministic compactors (json skeleton / code outline / text head-tail);
  stdlib-only, no ML. Lifted from the CCR component of github.com/chopratejas/headroom.
  USE WHEN — a tool output / log / RAG chunk / file is too large for context and
  you want to compress it reversibly; "compress this payload", "shrink this
  before the model", "reversible compression", "cache the original and give me a
  handle". NOT FOR — loading knowledge-graph entities (that's the kg loader,
  the retrieval axis); lossless whole-file compression (use gzip); semantic
  summarization that does not need byte-exact recovery.
---

# ccr — reversible payload compression (the payload axis)

`ccr compress <file|->` · `ccr retrieve <handle>` · `ccr stats`

Shrink any blob — a tool output, a log, a RAG chunk, a file — **before** it
enters context, while keeping the original recoverable. The **payload-axis**
counterpart to a knowledge-graph loader (the **retrieval axis**): kg shrinks
*which* entities reach the model; ccr shrinks *each blob* that does.

Lifted from the **CCR / reversible-compression** component of
[Headroom](https://github.com/chopratejas/headroom) (28.5k★, Apache-2.0). We
lifted the *pattern*, not the dependency. Anchor: **BRO-1521**.

## The one idea

> Compression is reversible because the **full original is cached locally**,
> keyed by content hash. The model sees a compact lossy *view* + a handle
> (`ccr://<sha256>`); it calls `retrieve(handle)` only when it needs the bytes.

So the view can be aggressively lossy without losing information — the loss is
recoverable on demand. Same shape a KG loader uses on the other axis: a lossy
catalog projection that expands to the full entity body on load.

## Mechanism

Dispatch by detected content type (a file-extension hint beats the content
heuristic, which beats nothing):

| Type | Compact view | Reversible? |
|---|---|---|
| `json` | type/shape skeleton (keys + value types + collection sizes; **no leaf data**) | yes (cache) |
| `code` | structural outline (imports + `def`/`class`/`fn` signatures w/ line numbers; **bodies elided**) | yes (cache) |
| `text` | head + tail **by line**, then head + tail **by character** on any over-long line | yes (cache) |

Deterministic, **stdlib-only, no ML** — the value is the reversible-cache
architecture, not the compression ratio. Identical payloads are
content-addressed (idempotent: one handle, one record). The view is never
emitted larger than the original (tiny inputs fall back to the payload).

**Two budgets, and they apply on both line-oriented paths.** `--head`/`--tail`
bound the number of lines; `--line-budget` (default **2000 chars**, `0`
disables) bounds each line. Without the second, a payload that is *one enormous
line* — a minified or **truncated** JSON blob, a single-line dump — compressed
to exactly 0%, because `len(lines) <= head + tail` returned the whole thing as
the "compact view". Truncated JSON lands here by construction: `detect_type`
needs a *successful* `json.loads`, so a streamed/cut-off document routes to
`text`.

The budgets are **independent**: `--line-budget 0` (or any value `≤ 0`)
disables the *character* budget only, and `--head`/`--tail` keep eliding. It
used to disable neither cleanly — for multi-line input `len(ln) <= 0` was false
for every non-empty line, so *disabling* the budget routed the payload down the
join path it was meant to avoid: `compact_text("a\r\nb\r\n", line_budget=0)`
returned `"a\nb"`, dropping a trailing newline, normalising CRLF, and reporting
a 50% saving with nothing marked elided. A "no compression" flag that silently
rewrites bytes is worse than one that does nothing.

The char budget applies to the **code** outline too. It initially did not:
`compact_code(payload, **_)` swallowed `line_budget`, so a minified JS/TS
bundle — one enormous line that still matches `_DEF_RE`, and the canonical
artifact this skill exists to shrink — emitted that whole line as its "outline"
and still compressed to 0.0%, with no flag able to work around it. The same
defect, surviving on the sibling path. Signature lines and the no-structure
`compact_text` fallback now both carry the caller's budgets.

## Guarantees

Each row names the mechanism that holds the invariant, and is backed by a
mutation-proven test — revert the fix and the named test fails.

One scope note, stated rather than glossed. `_is_confined`'s `is_symlink()`
guard is **defence-in-depth with no reachable behavioural difference**: delete
it and the suite stays green, because content-addressing means a symlink can
only ever serve content whose sha256 matches the requested handle, and no
content hashes to the link's own name. It is an *equivalent mutant*, not an
untested guard, so no test is claimed for it.

That distinction is the point. An earlier revision of this file asserted
"each is backed by a mutation-proven test" as a blanket claim; adversarial
review showed it was false for the hex-validation row, whose *outcome* was
upheld by a neighbouring guard while its stated **ordering** went unpinned.
That gap is now closed by
`test_malformed_handle_is_refused_BEFORE_the_filesystem_is_touched`, which
distinguishes the two by pointing the cache at a nonexistent directory so the
guards would give different errors. A blanket "everything is proven" line is
itself an unverified claim — the exact failure mode this skill's review process
exists to catch.

| Invariant | What holds it |
|---|---|
| **Byte-exact.** `retrieve` returns the input's exact bytes: CRLF, lone CR, missing trailing newline, NUL, BOM, 4-byte UTF-8, lone surrogates, and raw non-UTF-8 bytes all survive. | `compress` reads **bytes** (`read_bytes` + `surrogateescape`) — `read_text` applies universal-newline translation, which rewrote `\r\n` → `\n` *before hashing*, destroying the original. `retrieve` writes through `stdout.buffer`. |
| **Confined.** A handle is `[0-9a-f]{8,64}` and nothing else, validated **before** it touches the filesystem; the resolved record must be a real file inside the cache dir. | Handles come back from *model output* — the untrusted side. `Path.__truediv__` silently discards the cache dir for an absolute token and keeps `..` for a relative one, and a `<sha>.json` symlink can point anywhere. |
| **Atomic.** A concurrent reader never observes a partial record. | Records are published by temp-file + `os.replace`, never streamed into the final name. |
| **Verified.** Every read recomputes the sha256 and refuses a mismatch — `retrieve`, `compress`'s self-heal check, **and `stats`**. | A content-addressed store that hands back unverified bytes is not content-addressed. `stats` was the one read that opted out, so a record `retrieve` refused as tampered was still rolled into the totals. |
| **Honest rollup.** `stats` derives its totals from the digest-covered field (`len(original)`), and reports every excluded entry **with the reason that excluded it** (`unusable_reasons`), never a lump sum. | The sha256 covers `original` and nothing else, so the stored `original_chars` counter sits *outside* it: editing it to `1e9` kept the digest valid and reported `cumulative_saved_pct: 100.0`. `compact_chars` cannot be recomputed (the view is not stored), so it is accepted only inside the range every record satisfies by construction: `0 ≤ compact ≤ original`. A lump `unusable` count invited the CLI to narrate a cause it never checked — "digest mismatch … re-compress to heal" is false for a stray `hello.json`, a dangling symlink, or a directory named `adir.json`. |
| **Self-healing.** A truncated or tampered record is treated as *absent*, so the next `compress` of that payload rewrites it. | The old `if not rec_path.exists()` short-circuit made a partial record permanent. |
| **Self-collecting.** A `.ccr-tmp-*.part` orphaned by SIGKILL or power loss is unlinked at the next cache open, once older than a 6h TTL. | `_write_record`'s cleanup covers a *failed* publish; a hard kill runs no handler, and nothing else in the store looks at `.part` names, so the leak was permanent. **Age**, not an exclusivity check, gates the delete: mtime advances while a live publish writes, so an hours-stale temp file cannot be one. The window is measured — instrumenting `os.replace` across 640 concurrent publishes puts the longest a `.part` was ever live at **15ms** (median 0.1ms), so a 6h TTL carries ~10⁶× margin on its own evidence. Held under concurrency by `test_concurrent_writers_and_a_reaper_produce_no_corrupt_records` (4 writers + a continuously-reaping 5th, in CI, ~0.15s); an ad-hoc 16-writer run of the same shape produced 640 records, 0 failures, 0 corrupt. |
| **Private.** Cache dir `0700`, records `0600`. | The cache holds full plaintext originals. |
| **Linear.** Both code regexes are line-bounded (`[ \t]*`, `[^\n]*`). | `^\s*` matches `\n`, so `_IMPORT_RE` ran to EOF and backtracked at every line start — quadratic (32KB of blank lines took 5.6s), reachable from `--type auto`. |

`--json` is a **machine envelope**: always pure ASCII, so it stays pipeable even
when the payload holds bytes no JSON reader could otherwise decode.

**Addressing.** For valid-UTF-8 input the handle is exactly
`sha256(<the file's bytes>)`. Input that is *not* valid UTF-8 is addressed by
its `surrogateescape`-decoded form instead, so the handle is not
`sha256sum` of the file — this keeps the digest collision-free (a
`surrogateescape` digest maps a lone-surrogate string and a file holding the
corresponding raw bytes onto the same handle). Byte-exact recovery holds either
way.

## Usage

```bash
python3 scripts/ccr.py compress path/to/big.json          # view on stdout, savings on stderr
cat huge.log | python3 scripts/ccr.py compress - --type text --head 30 --tail 10
python3 scripts/ccr.py compress minified.json --line-budget 4000   # per-line char budget
python3 scripts/ccr.py retrieve ccr://<sha256> > out.bin  # byte-exact original (full handle or unique prefix)
python3 scripts/ccr.py stats --json                       # cache size + cumulative savings
```

Exit codes: `0` ok · `1` no such / malformed handle, bad payload, user error ·
`2` internal error.

As a library:

```python
import ccr
r = ccr.compress(payload, filename="server.ts")   # auto-detects code
context_blob = r["view"]                            # feed this to the model
original = ccr.retrieve(r["handle"])                # expand on demand
```

`BROOMVA_CCR_HOME` relocates the content-addressed cache (default
`~/.cache/broomva/ccr/`, created `0700`) for CI runners and non-standard layouts.

## Tests

```bash
python3 -m pytest skills/knowledge/ccr/tests/ -q     # 55 tests
python3 skills/knowledge/ccr/tests/test_ccr.py       # no pytest needed
```

Core invariant under test: the view is lossy, but `retrieve(handle)` returns the
original **byte-for-byte** — asserted **through the CLI** over a byte-level
fixture matrix (`\r\n`, lone `\r`, no trailing newline, NUL, BOM, 4-byte UTF-8,
lone surrogate, raw non-UTF-8) as well as through the Python API. Plus:
64-char traversal/absolute/symlink handle rejection, cache atomicity + digest
verification + self-healing, `0700`/`0600` permissions, ReDoS bounds on **both**
code regexes, the character budget, head/tail clamping, and deep-JSON recursion.

The temp-file reaper is tested at the shape that produced it: a child process
`SIGKILL`s itself from inside `os.replace`, and the test asserts the whole
lifecycle — the orphan appears, no record lands at the canonical path, a
*young* orphan survives (it is indistinguishable from another process's live
publish), and only a stale one is collected. A second test races the reaper
against a real in-flight publish rather than asserting the mtime rule
statically: remove the age guard and the publish dies with `FileNotFoundError`.
A third runs the whole thing **concurrently** — 4 writer processes plus a fifth
reaping continuously — because a delete path in a shared directory is where a
reaper's regressions actually live, and a claim about concurrency that only
exists in a changelog is not re-verifiable. It asserts the reaper collected
*nothing*: every `.part` in that directory belongs to a running writer.

**Scope limit, stated rather than left implicit.** Age does not cover a forward
clock step larger than the TTL (VM snapshot restore, an RTC that NTP then
corrects). Forcing that case — a reaper at `ttl=0` against 640 concurrent
publishes — makes publishes fail *loudly* with `FileNotFoundError` (6.2% on one
run, 12.7% on an independent reviewer's; load-dependent) and corrupted **0**
records in both. An availability fault on a retryable operation, not an
integrity one.

Tests assert at the layer that can actually break. `test_small_text_not_mangled`
asserts `compact_text` **directly** — routed through `compress()` it cannot
fail, because the `len(view) >= len(payload)` clamp rescues even a deleted
compactor. Likewise the traversal tests assert `_resolve_sha` directly, since
the downstream digest check would otherwise mask an escape.

## Install

```bash
npx skills add broomva/skills --skill ccr
```

## Provenance

- Origin: `/checkit github.com/chopratejas/headroom` → entity `tool/headroom`
- Pattern sibling: the `kg` loader (retrieval axis) / `llm-as-index-architecture`
- Ticket: BRO-1521
