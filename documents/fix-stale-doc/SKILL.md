---
name: fix-stale-doc
description: Full-repo documentation sweep. Fans out one sub-agent per module / docs subdir / README cluster to (1) fix stale claims that no longer match the code, (2) remove duplication, and (3) compact verbose prose. Use when the user runs "/fix-stale-doc", asks to "fix stale docs", or "clean up documentation".
---

# /fix-stale-doc — documentation sweep

A full-repo maintenance pass over the docs. Three goals, applied to every doc:

1. **De-stale** — fix claims the code no longer supports: dead file paths, renamed
   functions/types, removed flags / env vars / build tasks / CLI subcommands, changed behavior.
2. **De-duplicate** — collapse repeated content. One canonical home; replace the copy with a
   one-line pointer.
3. **Compact** — tighten verbose phrasing so docs stay digestible for humans. Fewer words, same
   facts.

Run this when nothing in particular changed but the docs have drifted as a whole. (Distinct from a
change-driven sync that updates docs to match one specific diff.)

## The audience rule (read first)

There are two doc audiences. Treat them differently:

- **Human docs** — `README.md`, everything under `docs/**`.
- **LLM docs** — `AGENTS.md`, `CLAUDE.md`, and module/package-level doc comments (e.g. a Go
  `doc.go`, a Python module docstring, a JSDoc header).

Deduplicate **within** an audience. Duplication **across** audiences is **allowed** (not required):
an `AGENTS.md` may restate a fact a `README.md` also covers when the agent genuinely needs it
inline. Prefer a reference (`see X`) when the LLM doc can afford the indirection; keep the copy when
inlining materially helps the agent. Never delete a cross-audience copy just because the other
audience has it.

## Edit vs flag — the core rule (read this before editing anything)

Staleness comes in two flavors, and they get different treatment:

- **Syntactic staleness** — a doc names a concrete code symbol that no longer exists: a dead file
  path, renamed function/type, removed build task / CLI flag / env var / struct field. This is
  verifiable against the code with certainty. **Auto-fix it** (or delete the line if the whole point
  is gone).
- **Behavioral staleness** — a doc describes _what the code does_ and the description may no longer
  match. This is a judgment call, and a confident-but-wrong rewrite degrades a good doc. **Do not
  rewrite it.** Leave the text as-is and add a flag for a human:
  `<!-- ⚠️ stale#<id> verify against <path>: <one-line reason> -->`. The `<id>` (assigned in
  Step 2) is what makes every flag mechanically findable and unambiguous in later steps. Only
  rewrite a behavioral claim when the code _unambiguously_ contradicts it (e.g. the doc says
  "returns an error", the function has no error return) — and say so in your report.

Bias toward flagging **during the fan-out**: a missed stale line a human later catches is cheaper
than a plausible wrong edit that erases a fact nobody notices was lost. A flag is a staging state,
not the final answer — **Step 4 (hardening)** revisits each one and resolves what it can.

## Step 1 — Build the work list

If the project ships a deterministic doc/link checker (e.g. a markdown link linter, a dead-path
checker), run it first and fix what it reports — those findings are certain (a path either resolves
or it doesn't) and cost no model tokens. Only what such a tool _can't_ judge — behavioral drift,
duplication, verbosity — needs the fan-out below.

By default, only sweep docs that have likely **drifted** — docs whose referenced code moved on
without them. Use `--all` to force a full-corpus sweep.

**Default (drift-targeted):** for each candidate doc, compare its last-touched commit against the
last-touched commit of the code it sits next to / references. A doc older than its code is a
drift suspect.

```bash
# last commit that touched the doc
git log -1 --format=%ct -- <doc>
# last commit that touched the adjacent code dir (e.g. the module/package the doc lives in)
git log -1 --format=%ct -- <code-dir>
# doc is a drift suspect when the code timestamp is newer than the doc timestamp
```

Apply this per doc against its co-located code dir (a module README vs its module dir, an
`internal/foo/README.md` vs `internal/foo/`, etc.). Root/cross-cutting docs (`AGENTS.md`,
`CLAUDE.md`, top-level overview docs) have no single co-located dir — always include them.

**`--all`:** skip the drift filter and sweep every tracked doc.

Enumerate the candidate set (tracked markdown):

```bash
git ls-files '*.md' | grep -vE '/(node_modules|vendor)/'
```

In-code doc comments (a Go `doc.go`, a module docstring, a JSDoc header) aren't enumerated here —
they're swept inside each module chunk, since that sub-agent already reads its co-located code dir.

Then partition the surviving docs into many small, independent chunks. One chunk = one sub-agent.
Small chunks keep each context window tiny — that is the whole token strategy.

Group into chunks by logical area, e.g.:

| Chunk                      | Files                                                                     |
| -------------------------- | ------------------------------------------------------------------------- |
| One per **module/package** | a module's `AGENTS.md` + `README.md` (+ its in-code doc comments)         |
| One per **`docs/` subdir** | `docs/development`, `docs/operations`, `docs/overview`, `docs/...`        |
| **root**                   | `AGENTS.md`, `CLAUDE.md`, top-level index/overview docs                   |

A large subdir may be split into 2–3 chunks. Aim for roughly 5–15 doc files per chunk.

**Always exclude:**

- Frozen plan dirs and changelogs — never rewrite history.
- Generated docs and generated source output.
- Personal/experimental scratch dirs, not maintained product docs.
- `vendor/`, `node_modules/`, and any other dependency directory.

## Step 2 — Fan out (one sub-agent per chunk)

Pick this sweep's flag number: 1 + the highest sweep number in any existing `stale#` marker in the
tree (`git grep -ohE 'stale#[0-9]+'`; use 1 if none). A chunk's flags are IDed
`stale#<sweep>-<chunk>-<n>` (chunk index, then a counter from 1) — unique without any coordination
between parallel sub-agents, and mechanically distinguishable from an earlier sweep's kept flags.

Dispatch the chunks as parallel `Agent` calls (`general-purpose`), in batches — issue several in a
single message so they run concurrently. Each sub-agent **edits the files in its chunk directly**.

> If the user opts into orchestration ("use a workflow" / "ultracode"), prefer the `Workflow` tool:
> a `pipeline` over the chunk list, each chunk a stage that returns a structured report. Otherwise
> use plain parallel `Agent` calls — no opt-in needed.

Give every sub-agent this contract (fill in the bracketed parts):

> Before anything else, read `AGENTS.md` / `CLAUDE.md` at the repo root for conventions.
>
> You own these doc files: **[exact list]**. You may read code only under **[the matching code dir(s)]** to verify claims — do not wander the repo; that is the token budget.
>
> For each file:
>
> 1. **De-stale — but mind edit vs flag.** Two cases:
>    - _Syntactic_ (a named symbol that no longer exists — dead path, renamed func/type, removed
>      build task / flag / env var / struct field): verify against the code and **auto-fix or
>      delete**.
>    - _Behavioral_ (a description of what the code does that may have drifted): **do not rewrite.**
>      Leave the text and add `<!-- ⚠️ stale#<prefix>-<n> verify against <path>: <reason> -->`,
>      numbering `<n>` from 1 under your assigned prefix **[sweep-chunk]**. Only rewrite when the
>      code _unambiguously_ contradicts the doc, and note it in your report.
>      If you cannot verify a claim, leave it and flag it; never guess.
> 2. **De-duplicate within your chunk.** Same audience (human vs LLM — see below), same fact stated
>    twice → keep one canonical copy, replace the other with a one-line pointer.
> 3. **Compact.** Tighten verbose prose. Cut filler, redundant preamble, and restated context. Keep
>    every fact; shorten the sentence. Do not change meaning or tone for taste (surgical edits only).
>
> **Audience:** human docs = `README.md` + `docs/**`; LLM docs = `AGENTS.md` / `CLAUDE.md` /
> in-code doc comments. Dedupe within an audience only. Cross-audience duplication is allowed — never
> delete a copy just because the other audience has it.
>
> Keep edits surgical. Do not reorganize files, rename headings for style, or "improve" code. In
> in-code doc-comment files, edit only the comment prose — never the code itself.
>
> Return a **terse** report — no file contents:
>
> - files touched
> - syntactic staleness fixed (one line each: `path: was X → now Y`)
> - behavioral rewrites — unambiguous contradictions only (one line each: `path: was "X" → now "Y"`)
> - behavioral staleness flagged (one line each: `stale#<id>: <path> — <what to verify>`)
> - duplication removed (one line each)
> - approx. lines saved
> - **cross-chunk dup candidates**: content you suspect is also duplicated in another doc outside
>   your chunk (so the orchestrator can resolve it)
> - anything you could not verify

## Step 3 — Cross-chunk dedup pass

Collect the "cross-chunk dup candidates" from every report. For each genuine cross-doc duplication
**within the same audience**, pick one canonical home and replace the other occurrence with a
one-line reference. This is usually a handful of edits — do it inline, no extra fan-out needed.
A `⚠️` flag inside a deduplicated paragraph moves to the surviving copy — never drop a flag while
collapsing a duplicate; Step 4 still has to find it.

## Step 4 — Harden the flags (resolve what you can; keep only real judgment calls)

Scope is mechanical: every flag bearing this sweep's number is in scope — whether or not a report
mentions it — and any other `⚠️` content (an earlier sweep's kept flags, a warning callout in
prose) is not this pass's to touch. Locate them:

```bash
git grep -n 'stale#<sweep>-'
```

For each flag, **read the code it names** and decide:

- **Resolvable at high confidence** — the code unambiguously settles it: the described behavior is
  plainly right, plainly wrong, or the correct line is mechanical once you've read the named symbol.
  **Rewrite the prose correctly and delete the flag.** This is the same "unambiguous → fix" test
  from the Edit-vs-flag rule, now applied with real read scope and full attention on one claim
  instead of a whole chunk.
- **Genuine judgment call** — settling it needs a decision only a human owns: is this the behavior
  we _want_, a product/design intent, a deliberate tradeoff, a "should we even document this"? The
  code alone can't answer. That includes a doc that may describe _intended_ behavior the code fails
  to deliver — when the code itself might be the bug, rewriting the doc to match it enshrines the
  bug. **Keep the flag.**

The bar is genuine confidence, not convenience. If reading the code leaves you unsure, the flag
stays. Never retire a flag by softening the claim to something vaguer — either the prose becomes
_correct_, or the flag remains. And watch for over-broad flags: a sub-agent that saw one caller stop
emitting `X` may write "X is gone" when X still lives elsewhere — the hardening read is where you
catch and narrow that.

For a handful of flags, do this inline. If the sweep raised many (~10+), fan out verifiers — one per
group of flags naming the same file/code dir, not one per flag, so no two verifiers re-read the same
code — the adversarial-verify shape: each **edits its docs directly** (like a Step 2 sub-agent —
rewrite the prose, delete the resolved flag) and returns, per flag, the fixed/kept report line
below. A verifier starts from the files its flags name but may search the repo for a flagged
symbol — that repo-wide check is precisely how over-broad "X is gone" flags get caught.

Report per flag, keyed by ID:
`stale#<id> (path) → fixed: was X, now Y` vs `stale#<id> (path) kept: <why a human must decide>`.

## Step 5 — Verify & report

- If the project uses a markdown formatter (e.g. `prettier`), format the touched markdown — but
  **only the files you edited**, and check the diff. Some docs are hand-aligned and not
  formatter-clean (notably `AGENTS.md` / `CLAUDE.md` and tables with unescaped `|` inside backticks);
  if the formatter reformats lines you didn't touch or breaks a table, revert it and keep your edit
  surgical instead.
- Review with `git diff`. Sanity-check that no stale "fix" deleted a fact that was actually correct.
  Behavioral rewrites carry no `⚠️` in the diff — walk both the hardening report's "fixed" list and
  the Step 2 reports' behavioral-rewrite lines, giving each the same scrutiny a surviving flag would
  have gotten.
- **Do not commit** — the user reviews. Print a short summary: chunks processed, syntactic fixes,
  `⚠️` flags raised → resolved in hardening (one line each: was/now — the user must be able to
  review these from the summary, since they carry no marker in the diff) vs kept (each with its
  reason — only genuine judgment calls should remain), dups removed, total lines saved.

## Token economy (non-negotiable)

- Each fan-out sub-agent (Step 2) reads **only** its own doc files + the narrowly scoped code dir it
  needs — never the whole repo. Step 4 verifiers are the one exception: a targeted repo-wide
  _search_ for the flagged symbol is allowed; wholesale reading still isn't.
- Reports are terse and structured — never echo file contents back.
- Within a Step 2 chunk, read-then-edit in a single pass; no separate detect/fix double read.
  (Step 4's re-read of flagged claims is the designed exception.)
- Small mechanical chunks (e.g. a tiny CLI README cluster) can run on a cheaper model.
