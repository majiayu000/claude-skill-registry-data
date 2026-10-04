---
name: eos-commit-mine
description: Commit ONLY your own changes when they're entangled — intermixed in the same files — with another session's (or the user's) uncommitted work-in-progress. Produces a clean, single-purpose commit of just your hunks while leaving the parallel WIP byte-for-byte untouched and uncommitted. Use when `git status` shows files you edited that ALSO carry changes you didn't make, and `git add <file>` would bundle both. Codifies CLAUDE.md §Git ("stage/commit only files scoped to the current task; never `git add -A`") down to hunk granularity. NOT for the simple case where your changes are in their own files (just `git add` those) — this is only for the entangled-same-file case.
---

# EmptyOS Commit-Mine

Commit **only your own hunks** when your edits are intermixed, in the same
files, with a parallel session's uncommitted WIP — leaving that WIP byte-exact
and uncommitted for its owner.

`git add <file>` stages the **whole file**, bundling the other session's WIP
into your commit. `git add -p` (patch mode) is interactive and not supported in
this harness. This skill is the deterministic, non-interactive way to get a
clean single-purpose commit anyway, with a byte-exact safety net for the WIP.

Origin: shipped the publish SSG-gap + ranked-search work while a parallel
`publish-site` session had an uncommitted "Editions band" WIP in the same
`builder.py` / `templates.py`. Ran this dance twice; second occurrence → skill.

## When to use

All of these hold:

- `git status --short` shows a file **you edited** that also carries changes
  **you didn't make** (another Claude session, the user, a linter, a background
  track).
- You want a commit of **just your work**, and the other changes to **stay
  uncommitted** (their owner will commit them).
- `git add <file>` would wrongly bundle both.

## When NOT to use

- Your changes are in **their own files** → just `git add <those files>` and
  commit. No entanglement, no skill.
- The parallel changes are **yours too** and ready → commit both together
  (`git add <files>`); simpler and honest.
- You're unsure whose the other changes are → **stop and ask the user** (per
  CLAUDE.md §Git: "decline to commit unfamiliar uncommitted changes"). This
  skill assumes you've already established the split; it does not decide
  ownership for you.

## The problem shape

```
working tree file = HEAD  +  YOUR changes  +  THEIR uncommitted WIP
                              └── want to commit ──┘   └── leave alone ──┘
```

Goal: a commit = `HEAD + YOUR changes`, and a working tree left at
`HEAD + YOUR changes + THEIR WIP` (so `git diff HEAD` afterwards = THEIR WIP
only), byte-identical to what it was before.

## Method — index-only (preferred; never removes their WIP from disk)

Both methods below reset the file with `git checkout HEAD -- F` and rely on a
backup to put their WIP back. That opens a window in which their uncommitted
work exists **only** in your scratchpad — if anything dies in between, it is
gone, because uncommitted work is in no git object. `git apply --cached` writes
to the **index only**, so the working tree is never touched, there is no backup,
no restore, and no window.

```bash
git diff -- F > "$SP/full.patch"          # working tree vs index/HEAD
# …build "$SP/mine.patch" (see step 3 below for the classifier)
git apply --cached --check "$SP/mine.patch" && git apply --cached "$SP/mine.patch"
git add <your-own-untouched-files>
```

Because the working tree still carries their WIP, you cannot test your isolated
change there. Materialise **exactly what is staged** somewhere else and test it
there — also non-destructive:

```bash
rm -rf "$SP/idx" && mkdir -p "$SP/idx"
git checkout-index -a --prefix="$SP/idx/"
(cd "$SP/idx" && python -m pyflakes <your files> && python -m pytest <your test> -q)
```

This is the step that catches a split which *applies* cleanly but does not
*stand alone* — an import you kept whose only user was in their hunks, or a
manifest entry left pointing at a method that landed on their side.

Then commit, and confirm the split held:

```bash
git diff --cached | grep -ci "<THEIRS-marker>"   # MUST be 0 before committing
git diff --stat -- F                              # their WIP, still unstaged
```

### Selecting hunks: prefer `@@` identity over markers

The classifier below keys on **marker strings**, and markers mis-assign more
often than they look like they will: most lines of a feature never mention the
feature's name. A first pass keyed on "every added line in this hunk carries
their marker" classified **zero** of their hunks as theirs, because their code
was mostly plumbing with neutral names.

Worse, the classifier's fallback for a hunk carrying **neither** marker is
`WARN neutral hunk kept` — it keeps it as yours. That is **fail-open**: an
unrecognised hunk of theirs lands silently in your commit.

When you can enumerate your own hunks (you just wrote them), select by `@@`
header instead — it needs no guessing and cannot fail open:

```python
KEEP = ("@@ -18,7", "@@ -38,6", "@@ -378,7")   # your hunks, read off the diff
...
cur, take = [line], line.startswith(KEEP)
```

Print every hunk header with its added-line count first and decide by eye; on a
handful of hunks that is faster and safer than tuning markers.

## Method — patch-classifier (when you must reset the working tree)

Use when your hunks and theirs live in **different regions** and you need the
file itself reset — otherwise prefer the index-only method above.
Fully deterministic; the backup + md5 check is the safety net.

Let `$SP` = your scratchpad dir. For each entangled file `F`:

### 1. Back up the entangled files (ground truth for restore)

```bash
cp F "$SP/BAK_F"
md5sum F "$SP/BAK_F"     # confirm identical
```

### 2. Diff vs HEAD and classify hunks

```bash
git diff HEAD -- F > "$SP/full.patch"
grep -nE "^@@|^\+" "$SP/full.patch" | head -60   # eyeball which hunks are yours vs theirs
```

Pick **marker strings** unique to each side (identifiers, comments, CSS class
prefixes, function names). Yours: things only your change introduces. Theirs:
things only their WIP introduces.

### 3. Build a mine-only patch

Run a classifier that keeps hunks whose added lines carry YOUR markers, drops
hunks with only THEIR markers, and for any **mixed** hunk (both markers in one
`@@` block) strips their added lines and fixes the `+` count in the header:

```python
import sys, re
full, out = sys.argv[1], sys.argv[2]
lines = open(full, encoding="utf-8").read().split("\n")
THEIRS = [ ... ]   # marker substrings unique to the parallel WIP
MINE   = [ ... ]   # marker substrings unique to your change
def has(ms, t): return any(m in t for m in ms)
o=[]; i=0; n=len(lines)
while i < n:
    if lines[i].startswith("diff --git"):
        hdr=[lines[i]]; i+=1
        while i<n and not lines[i].startswith(("@@","diff --git")): hdr.append(lines[i]); i+=1
        hunks=[]
        while i<n and lines[i].startswith("@@"):
            hh=lines[i]; i+=1; body=[]
            while i<n and not lines[i].startswith(("@@","diff --git")): body.append(lines[i]); i+=1
            hunks.append((hh,body))
        kept=[]
        for hh,body in hunks:
            added="\n".join(l for l in body if l.startswith("+") and not l.startswith("+++"))
            if has(THEIRS,added) and has(MINE,added):        # mixed → strip theirs, fix count
                nb=[]; removed=0
                for l in body:
                    if l.startswith("+") and not l.startswith("+++") and has(THEIRS,l) and not has(MINE,l):
                        removed+=1; continue
                    nb.append(l)
                m=re.match(r"@@ -(\d+),(\d+) \+(\d+),(\d+) @@(.*)", hh)
                a1,a2,b1,b2,tail=m.groups()
                kept.append((f"@@ -{a1},{a2} +{b1},{int(b2)-removed} @@{tail}", nb))
            elif has(MINE,added): kept.append((hh,body))
            elif has(THEIRS,added): continue                  # drop
            else: sys.stderr.write("WARN neutral hunk kept: "+hh+"\n"); kept.append((hh,body))
        if kept:
            o.extend(hdr)
            for hh,body in kept: o.append(hh); o.extend(body)
    else: i+=1
open(out,"w",encoding="utf-8",newline="\n").write("\n".join(o).rstrip("\n")+"\n")
```

Sanity-check the result: `grep -c <THEIRS-marker> mine.patch` must be **0**;
`grep -c <MINE-marker> mine.patch` must be > 0.

### 4. Reset the file to HEAD, apply mine-only, verify

```bash
git checkout HEAD -- F
git apply --check "$SP/mine.patch" && git apply "$SP/mine.patch"
python -m py_compile F            # or the relevant fast check
# run the offline/unit test that proves your change (best: a test that exercises it)
```

### 5. Commit only your files

```bash
git status --short --untracked-files=no | grep "^[MA]"   # confirm ONLY your files staged
git add F [other-of-your-files]
git commit -m "..."   # end with the Co-Authored-By trailer per CLAUDE.md
git log -1 --stat --oneline    # verify HEAD is yours
```

### 6. Restore their WIP byte-for-byte + verify the split

```bash
cp "$SP/BAK_F" F
md5sum F "$SP/BAK_F"     # MUST match → their WIP restored exactly
# remaining diff vs your new commit must contain ZERO of your markers:
git diff -- F | grep -cE "<MINE-marker>" && echo "!! MINE LEAKED" || echo "CLEAN"
git diff -- F | grep -cE "<THEIRS-marker>"   # > 0 → their WIP intact + uncommitted
python -m py_compile F   # combined tree (yours committed + their WIP) still compiles
```

## Method — backup + re-apply via Edit (when hunks are messy/moving)

Use when the parallel WIP is large, evolving, or genuinely interleaved with your
hunks so the classifier can't split cleanly. The backup restore is byte-exact,
so **their WIP integrity is guaranteed** regardless:

1. `cp F "$SP/BAK_F"` (their WIP + yours).
2. `git checkout HEAD -- F`.
3. Re-apply **only your** edits with the Edit tool, in dependency order (your
   anchors must exist in the HEAD version; apply an earlier edit first if a
   later edit anchors on text you added).
4. Verify (py_compile + your test) → `git add F` → commit.
5. `cp "$SP/BAK_F" F` → working tree = your-commit + their WIP again.
6. `git diff HEAD -- F` → must be **their WIP only** (no MINE markers). If a
   stray MINE line appears, your re-apply drifted — the working tree is still
   correct (BAK restored), but inspect/amend the commit.

## Load-bearing safety rules

- **Never touch `data/*.db*`, `emptyos.toml`, `apps/personal/`** (CLAUDE.md
  §Daemon/Git). This skill only rewrites tracked source files you edited.
- **The backup is ground truth.** `cp BAK F` restores the parallel WIP exactly;
  the md5 check proves it. If anything goes sideways, `cp BAK F` returns the
  working tree to its pre-skill state losslessly.
- **Two hard post-conditions**, both must pass before you're done:
  1. `git diff -- F` (vs your new commit) contains **0** of your markers.
  2. `md5sum F == md5sum BAK_F` after restore.
- **Verify your committed tree runs** (py_compile + a test) *before* restoring
  the WIP — a broken commit is the real risk, and the WIP restore hides it.
- **Confirm HEAD is yours** (`git log -1`) after committing — a parallel session
  may have moved HEAD under you between steps; the diff/checkout are relative to
  whatever HEAD is, which stays correct, but verify the commit landed as yours.

## Anti-patterns

- `git add -A` / `git add .` / `git add <entangled-file>` — bundles their WIP.
  The whole reason this skill exists.
- Hand-editing `@@` line counts without recomputing — a wrong count makes
  `git apply` reject or silently corrupt. Only the mixed-hunk case needs a count
  fix, and the classifier does it.
- Skipping the md5 restore check — you might leave the parallel WIP subtly
  altered, which is exactly the "don't touch parallel work" rule this protects.
- Using this when your changes are in separate files — over-engineering; just
  `git add` your files.

## Cross-references

- CLAUDE.md §Git / Version Control — "stage/commit only files scoped to the
  current task; never `git add -A`; verify HEAD is yours."
- `.claude/rules/environment.md` §Parallel-session staging — the rule this
  operationalises at hunk granularity.
- memory `feedback_parallel_commit_race_steals_staged` — the failure mode
  (parallel auto-add bundling unrelated files) this prevents.
