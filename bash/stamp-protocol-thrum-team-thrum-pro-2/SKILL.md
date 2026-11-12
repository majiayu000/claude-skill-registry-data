---
name: stamp-protocol
description: "Use when stamping a plan, prompt, or snapshot - Authored-against format, derivation commands, never-type rule."
---


# Authored-Against Stamp Protocol
This is the canonical source-of-truth for the Authored-against stamp: its format,
derivation commands, and the never-type rule. Consuming files point here instead of
restating the recipe. Do not run this as a command; it has no terminal action — other skills and commands load it by name.
(To find what currently points here: `grep -rn "thrum:stamp-protocol" claude-plugin/commands/ claude-plugin/skills/`
— a hand-listed consumer roster in this file would rot the moment a new emitter or
reader is added, so none is kept here.)

## Purpose

A date alone cannot tell a reader whether the tree moved since an artifact was
authored. The Authored-against stamp embeds the exact commit SHA the author was
looking at and the configured merge target at authoring time. A reader can later
run the stamped diff command to detect whether any cited file has changed —
converting a qualitative suspicion ("is this stale?") into a falsifiable check.

## Stamp format (emitted artifact — verbatim)

Place these two lines at the appropriate location in the artifact (immediately
after its own date/frontmatter for brainstorm/plan/prompt; immediately after the
`Last updated` line for State.md and project_state.md):

```text
**Authored-against:** `<sha>` target: `<merge_target>`

> ⚠️ Verify base before acting: `git diff <sha>..origin/<merge_target> -- <files cited>` -- non-empty ⇒ cited code moved. (Resolve `<merge_target>` through its remote-tracking ref, never a bare local branch name — a local branch of the same name can be stale or absent.)
```

Always resolve `<merge_target>` through its remote-tracking ref
(`origin/<merge_target>`), never a bare local branch name, in every recipe in
this file — a local branch of the same name can be stale (last fetched days
ago) or simply absent on the reader's machine, while `origin/<merge_target>`
is only ever what's actually on the remote. Fetch before running any of these
diffs if the remote-tracking ref might be stale.

## Derivation commands (run at authoring time)

```bash
# SHA of the current HEAD
git rev-parse HEAD

# Configured merge target -- resolve through .thrum/redirect when present.
# A worktree's .thrum/ holds only a `redirect` file (a single line: the
# absolute path to the MAIN REPO'S .thrum directory itself), not its own
# config.json -- reading .thrum/config.json directly from a worktree
# silently returns empty. Root repos have no redirect file, so CONFIG falls
# through to the direct path.
CONFIG=".thrum/config.json"
[ -f .thrum/redirect ] && CONFIG="$(cat .thrum/redirect)/config.json"
jq -r '.orchestration.merge_target' "$CONFIG"
```

The author must never type or remember either value by hand — both come from the
shell commands above, run at authoring time.

If either command returns empty or `null`, STOP and report — do NOT emit a stamp
with a null/empty field. An artifact with no stamp is honest; an artifact stamped
`null` is a lie the reader cannot detect (the string "null" still matches the
reader's regex, so it reads as a valid stamp instead of UNVERIFIABLE, and the
resulting `git diff <sha>..null` then errors).

Before emitting the stamp, also verify the derived `<sha>` actually resolves:

```bash
git cat-file -e <sha>
# or: git rev-parse --verify <sha>^{commit}
```

If this fails, STOP and report — do NOT emit a stamp citing an unresolvable SHA. This is the same failure class as the
null/empty check above (a stamp the reader cannot trust), catching a different way to get there: `git rev-parse HEAD`
itself can't produce a bad SHA, but a stamp isn't always freshly derived this way — it can be hand-typed, copied from a
stale source, or otherwise introduced without running the command above. Treat this resolve-check as a mandatory guard
regardless of how the SHA was obtained, not an optional sanity check.

## Format conventions

The stamp follows the same literal-match convention as the `THRUM-REVIEW` marker
(canonical form documented in `coordinator-running-brainstorm-cycles` skill
§ "Footer → commit → stamp"): fixed field order, case-sensitive, ASCII-only —
parseable with `grep -F` semantics without regex. The reader-side regex in
`verify-against-plan` anchors on this fixed format; do not reorder or recase any
field.

## Review-object binding (THRUM-REVIEW stamp — plan/prompt binding)

A review stamp's PRESENCE proves a review happened; it does not prove the
stamp still binds the artifact that was reviewed. An edit made after a
`Ready:Yes` verdict leaves a stamp that still reads `Ready:Yes` while
describing a document that no longer exists — the same class of staleness the
Authored-against stamp solves for the tree, applied here to the artifact
itself.

The `THRUM-REVIEW` stamp carries two extra keys per stage, binding it to the
exact git blob it reviewed and the exact source it was reviewed against:

| Stage | Self-binding key | Source-lock key |
| --- | --- | --- |
| `stage=plan` | `plan_obj` | `src_lock` |
| `stage=prompt` | `prompt_obj` | `plan_lock` |

### Derivation (strip-then-hash, run at stamping time)

```sh
# self-object blob: strip EVERY THRUM-REVIEW line, hash the remainder, filters OFF
obj=$(grep -v '^<!-- THRUM-REVIEW:' "$FILE" | git hash-object --no-filters --stdin)
# source-lock blob: the source file is not mutated by the stamp -> plain hash
lock=$(git hash-object --no-filters "$SOURCE_FILE")
```

- Strip set = every line matching `^<!-- THRUM-REVIEW:` (all cycles) — NOT
  `THRUM-GATE`/`THRUM-DEFER`. The stamp cannot bind a hash that includes
  itself, so its own lines are removed before hashing (chicken-and-egg).
- `--no-filters --stdin` bypasses gitattributes clean filters / autocrlf so
  the value emitted here and the value re-derived at read time agree
  byte-for-byte.
- Hash the **working-tree** file, not a committed blob — an uncommitted
  post-review edit must be caught before it is ever committed.
- For `stage=plan`: `$SOURCE_FILE` is the LOCKED brainstorm (plus design spec,
  if any); `src_lock` proves the plan was reviewed against the source that was
  current at review time.
- For `stage=prompt`: `$SOURCE_FILE` is the LOCKED plan; `plan_lock` proves the
  prompt was reviewed against the plan that was current at review time.
- When multiple cycles' `THRUM-REVIEW: stage=<S>` lines coexist, the
  **highest-cycle (last-appended)** line is the binding verdict; earlier
  lines are history, never re-checked. Stamps are only ever appended, never
  reordered, so append-order == cycle-order — select with `tail -1`, never a
  sort (`cycle=10` must beat `cycle=9`, which a lexical sort inverts).

### Null/unresolvable guard

Same failure class as the Authored-against stamp above: if either `obj` or
`lock` comes back empty or `null`, STOP and report — do NOT emit a stamp with
an empty/`null` binding key. A `THRUM-REVIEW` line with `plan_obj=` (or any of
the four binding keys) empty or literal `null` still matches a reader's regex
and reads as a valid binding — the value a reader would trust to prove binding
is exactly the value that never resolved.

### Extended stamp shape (fixed key order preserved)

```text
<!-- THRUM-REVIEW: stage=plan verdict=Ready:Yes cycle=<N> date=<YYYY-MM-DD> verify=<...> plan_obj=<blob> src_lock=<blob> [rev=... notes="..."] -->
<!-- THRUM-REVIEW: stage=prompt verdict=Ready:Yes cycle=<N> date=<YYYY-MM-DD> prompt_obj=<blob> plan_lock=<blob> -->
```

`plan_obj`/`src_lock` and `prompt_obj`/`plan_lock` are appended after the
stage's existing keys, in this order — keeping the fixed-key-order convention
this file already establishes for the Authored-against stamp above.

## Read-time provenance re-derivation

Both checks below are computable from the two fields the stamp already carries
(`<sha>` and `<merge_target>`) — no new stamped field is needed. A reader running
either check for the first time, or re-running it on an artifact read before,
must run them in this exact order; the second is undefined if the first fails
(short-circuit):

1. **SHA-resolves** — `git cat-file -e <sha>` (or
   `git rev-parse --verify <sha>^{commit}`). If this fails, the stamp cites a
   FABRICATED or mistyped SHA — flag RED immediately and do NOT attempt check 2.
   Merge-status has no defined answer for a SHA that does not exist.

2. **Merge-status** — only once check 1 has passed:
   `git merge-base --is-ancestor <sha> origin/<merge_target>`. If this succeeds
   (the SHA IS already an ancestor of the merge target) AND the artifact's own
   prose describes that SHA's work as still open ("in-progress", "awaiting a
   gate", "not yet merged", or similar), flag the claim STALE — the work
   described has already landed; whatever gate the artifact was waiting on
   already happened, or was never blocking to begin with.

This re-derivation must run EVERY TIME the artifact is read, not only once at
authoring time — the same diff-at-read discipline this file already establishes
for the base stamp (`git diff <sha>..origin/<merge_target>`). A check that only
ran once at write time cannot catch drift that accumulates afterward, as the
tree keeps moving.
