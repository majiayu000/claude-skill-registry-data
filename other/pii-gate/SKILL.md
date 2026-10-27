---
name: pii-gate
description: >-
  Installs a PII/secret gate into a git repo — pre-commit + pre-push hooks and a
  CI workflow that block personal names and secrets from reaching a remote. Fires
  BEFORE a repo can leak: on `git init`, "new repo", "set up a repo", "add a
  remote", "push this to GitHub", "publish this", "make this repo public", "first
  push", or "is it safe to push this?". Also fires on the retrofit case — an
  existing repo that already has a remote and needs the gate plus a full-history
  scan. Use when a repo will hold real names, client identifiers, addresses, or
  any personal context that must never enter git history. Covers denylist setup,
  the write-only `PII_DENYLIST` Actions secret, gitleaks secret scanning, and the
  armed-run proof that the gate actually blocks. Not for scanning a repo you are
  not about to push, and not a substitute for gitleaks alone.
---

# PII gate — install it before the first push

**Seed question:** *Once this repo has a remote, every name in its history is
permanent — so is the gate in place BEFORE that, or are we retrofitting after the
window already closed?*

## Why the ordering is the whole skill

Pushed history is effectively permanent. Deleting the file that carried a name
does not remove it from the commits that carried it, and a private repo is one
visibility toggle away from public. So the gate only makes "person-clean" durable
if it exists **before the first byte reaches the remote**. Retrofitting after a
push means the unprotected window already happened, and no amount of later
scanning closes it.

The installer is idempotent and takes seconds. There is no cost case for
deferring it.

## Install

```
bash "${CLAUDE_PLUGIN_ROOT}/pii-gate/install.sh" /path/to/repo
```

That copies the hooks into `.githooks/`, adds the CI workflow, appends the
gitignore entries, points `core.hooksPath` at `.githooks`, and — only if the repo
has no denylist under either accepted name — seeds an **empty**
`pii-denylist.local` at the repo root. A repo that already has one keeps it,
under whichever name it uses.

Re-running it updates the hooks and workflow in place and never touches an
existing denylist.

**It can refuse, and a refusal is information rather than a fault.** In every
case below it writes nothing at all and exits non-zero. There are three:

1. **The target is a linked worktree.** `core.hooksPath` is shared across
   worktrees while these files are not, so installing there would disable hooks
   in all the others. Run it against the main worktree instead; the message names
   the path.
2. **The repo runs hooks somewhere else that would go quiet** — a `.husky`
   directory, a machine-wide hooks dir, or the default `.git/hooks`. Pointing
   `core.hooksPath` at `.githooks` makes git stop looking there. Nothing is
   deleted; they simply stop running.
3. **`.githooks/` already holds hooks that are not this gate's.** Here the files
   would be **overwritten**, not merely silenced — so this is the one to slow
   down on.

**Keeping another hook alongside the gate means merging, not copying.** The gate
owns five filenames in `.githooks/` — `pre-commit`, `pre-push`,
`overwrite-ci-denylist` and the two test suites — and git dispatches one hook per
event, so a second `pre-commit` cannot sit beside the gate's under any name git
will call. Copying `.husky/pre-commit` into `.githooks/` therefore just trades
refusal 2 for refusal 3, and the override would then overwrite the very file you
were trying to keep.

What actually works, in preference order: fold the other hook's *body* into the
gate's `.githooks/pre-commit` (the gate's own runs a global `pre-commit` first
for exactly this reason, so there is a precedent to follow); or move the other
hook to a name git does not dispatch and call it from the gate's; or, if you have
decided you do not need it here, re-run with `PII_GATE_REPLACE_HOOKSPATH=1` and
accept the loss — which for refusal 3 means an overwrite that nothing in the
installer can undo.

**Both merge routes cost you the edit on the next install, and nothing warns.**
The installer tells its own hooks from foreign ones by looking for the gate's own
denylist references in the file. A gate hook you have edited still carries them,
so it is classed as the gate's, overwritten in place, and no refusal fires — the
folded-in body is simply gone, along with the line that called your renamed hook.
That is the same "re-running is silent" property that makes ordinary updates
painless, and it cannot tell your edit from an older version of the file it is
meant to replace. So keep the merged hook under version control, and re-apply the
edit after any re-run. Only the third route announces its cost; the two better
ones charge it later.

The one case it passes over quietly is a *global* hooks dir whose only hook is a
`pre-commit` — this gate chains that one, so nothing is lost. Re-running over an
installation of this gate is likewise silent: it tells its own hooks from
someone else's by content, not by filename.

## Then, in order

1. **The operator populates the denylist — never you.** One term per line; `#`
   comments and blanks ignored. Do not invent, guess, or type personal terms into
   it yourself, and do not read the finished file back into the conversation: the
   point of the gate is that those terms live in exactly one gitignored file and
   nowhere else. Ask them to fill it in and tell you when it's done.

   **Use the filename the installer printed**, which is `pii-denylist.local` on a
   fresh repo but `pii-denylist.txt` on a retrofit that already had one. Creating
   a `.local` beside an existing `.txt` is the shadowing trap described under the
   arming probe below: the hooks take the first name they find, so the operator's
   real list would go unread while the gate reported itself active on the new,
   nearly-empty file.
2. **Commit the gate files before adding a remote.**
3. **Once a GitHub remote exists**, the operator runs
   `.githooks/overwrite-ci-denylist` themselves to set the `PII_DENYLIST` Actions
   secret. It needs an authenticated `gh` and a typed `Yes`. Pushing only *warns*
   when the local file has drifted from the secret — it never writes it, because
   an Actions secret is write-only and an overwrite destroys a value nobody can
   read back.

## Prove it can fail — this step is not optional

An empty denylist leaves the denylist layers honestly **INACTIVE**, and they say
so. That means every green run before the first *armed* run is no evidence at
all: a gate that has never blocked anything looks identical to a gate with
nothing to find.

So once terms are in, arm it once on purpose:

```
cd /path/to/repo                                   # the probe file must be INSIDE the repo
DL=$([ -f pii-denylist.local ] && echo pii-denylist.local || echo pii-denylist.txt)
echo "throwaway-term" >> "$DL"
echo "throwaway-term" > probe.md && git add probe.md
git commit -m probe        # MUST be blocked
```

Watch it block, then `git rm --cached probe.md && rm probe.md` and remove the
throwaway term from `$DL`.

**Append to the denylist the repo actually uses — that is what `$DL` is for.**
The hooks accept two filenames and take the **first** one they find, checking
`pii-denylist.local` before `pii-denylist.txt`, with no union between them. So on
a repo retrofitted with a `pii-denylist.txt`, writing the probe term to
`pii-denylist.local` *creates* that file and shadows the real one: the probe
passes, having proved only itself, while every real term goes unread. Delete the
throwaway term afterwards and you are left with an empty `.local` that normalizes
to nothing — the gate reports INACTIVE with the operator's list sitting one
filename away. If you did create a `.local` this way, remove the **file**, not
just the line.

**The probe file has to be inside the working tree.** Writing it to `/tmp` and
staging it makes `git add` fail with *"is outside repository"*, so nothing is
staged and the hook has an empty diff to scan — it matches nothing and produces
no block.

What you actually see is a non-zero exit from `git commit`, because with an empty
index git refuses on its own ("nothing added to commit"). That is the trap: the
failed command looks like the gate doing its job, when the gate never ran on
anything. Read the output, not the exit code — a real block says
`pre-commit BLOCKED: a denylisted term is in the staged changes`. Anything else
means the probe never reached the hook, which is a false negative in the one step
that exists to rule false negatives out.

If it did *not* block with the probe staged inside the repo, the gate really is
not installed the way you think — check that `git config core.hooksPath` returns
`.githooks`.

The same applies to CI: the workflow's first *armed* run (secret set, terms
present) is its first real test. Read that run's log rather than inferring from a
green check.

## Retrofitting a repo that already has a remote

Install the gate first, then scan the **full history**, not just the tree — a
tree scan reports clean on a branch where a name was added and later removed,
because the tree genuinely is clean. The shipped workflow's `history` job does
this in CI. The local equivalent greps history against *your denylist*:

```
# Same four stages the hooks apply, so one denylist does not behave differently by hand.
norm() { tr '|' '\n' | tr -d '\r' \
         | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//' \
         | grep -v -e '^[[:space:]]*$' -e '^[[:space:]]*#'; }
DL=$([ -f pii-denylist.local ] && echo pii-denylist.local || echo pii-denylist.txt)
git log -p -m --all --text --no-ext-diff --no-textconv --pretty=fuller \
  | grep -a -i -F -w -f <(norm < "$DL")
```

Every flag there is load-bearing, and the gate passes each for a reason worth
knowing before you drop one. Each defeats a different way the scan can come back
clean about content it was never shown:

- `--no-ext-diff --no-textconv` stop a repo-local `.gitattributes` diff driver
  from rewriting or blanking content before grep is shown it.
- `--text` covers the neighbouring case: a path marked `-diff` in
  `.gitattributes` makes git emit "Binary files ... differ" instead of the diff,
  and the gate records this as measured — without `--text` the name is simply
  absent from the stream.
- `--pretty=fuller` prints the **Commit** (committer) identity, which the default
  format omits — it shows Author only. A commit whose *committer* identity
  carries the name is invisible without it, and amends and rebases are exactly
  where the two identities diverge.
- `-m` makes `git log -p` emit a diff for merge commits, so a name introduced
  only in a conflict resolution is still scanned.
- `grep -a` forces the stream to be treated as text. Its opposite, `-I`, declares
  the *whole* stream binary at the first NUL byte and abandons it — so a single
  generated blob anywhere in your history would hide a name in every other
  commit.

**Never hand the raw denylist to `grep -f`** — here or anywhere. Every layer of
the gate runs `norm()` first, and a hand-run command that skips it is not the
same scan. All four of its stages earn their place, and this codebase has been
bitten by three of them:

- `grep -v` drops comments and blanks. The shipped template is *entirely*
  comments, eight of them a bare `#`; loaded as a pattern, `#` matches any line
  containing one, drowning a real hit in noise.
- `tr -d '\r'` strips carriage returns. A denylist saved on Windows, or pasted
  through a CRLF editor, leaves every pattern ending in `\r` so it matches
  **nothing** — measured here: a CRLF denylist that the full pipeline matches
  returns zero hits without this stage.
- The `sed` trims leading and trailing blanks, so an indented entry still counts.
- `tr '|' '\n'` splits the single-line form used by the CI secret field.

Two of those turn a real hit into a clean result, on the one scan you run to
answer "has a name already leaked". That is why the stages are reproduced here
rather than approximated.

One deliberate difference from the hooks' own `norm()`: theirs ends by reading
grep's exit status (`gs=$?; [ "$gs" -le 1 ]`) so that grep's *own* failure cannot
be laundered into an empty pattern list. Both commands above wrap this in
`<(norm < "$DL")`, and a process substitution discards the status either way, so
carrying it here would be decoration. If you lift this function somewhere that
does read its status, take the brace group from `.githooks/pre-push` instead.

Reach for gitleaks for the other half — **secrets**, not names. It runs both in
pre-commit (over staged changes) and in the workflow's separate `secrets` job
(over full history). It is never handed the denylist in either place, so it cannot
find a personal name and will return clean while one sits in your history. Two
scans, two different questions; neither substitutes for the other.

The two venues do not use the same ruleset. CI runs gitleaks with its built-in
rules. pre-commit passes `--config "$HOME/.config/gitleaks/config.toml"` when
that file exists, and falls back to the built-ins when it does not — so if you
keep a personal gitleaks config, your commit-time scan is the one it governs, and
a supplied config replaces the defaults unless it sets `[extend] useDefault`.
Worth knowing before you conclude the two layers look for the same things.

Say plainly that a retrofit does not undo an earlier exposure. If a real name is
already in pushed history, the honest options are history rewrite plus a force
push, or accepting the exposure — not a gate that starts from now.

## What the gate is and isn't

Three layers: pre-commit (gitleaks over the staged changes, then the denylist
scan of the staged diff), pre-push (every commit being pushed, plus the ref name,
commit message, author identity and tag message — each is a route a name takes to
the remote on its own), and CI (tree + full history + gitleaks).

**gitleaks runs locally as well as in CI, and can block a commit on its own.**
pre-commit prefers a global `pre-commit` hook if you have one, else runs the
`gitleaks` binary directly against the staged changes, and stops the commit with
"pre-commit BLOCKED: gitleaks findings". If neither is present it says so and
skips that layer — "no global pre-commit hook and no gitleaks binary — secret
scan skipped (CI still scans)". That warning is the signal to install gitleaks;
the denylist layers are unaffected either way.

**Everything fails closed.** An unreadable denylist, a failed `mktemp`, a `grep`
that errored rather than not-matched — each blocks instead of passing. "Could not
check" must never read the same as "checked, clean."

Matching is case-insensitive, fixed-string, and **whole-word everywhere it reads
content** — staged diffs, pushed history, and both CI content scans. No
wildcards, so list diacritic and ASCII spellings as separate terms. A matched
term is never echoed by any layer — not in hook output, not in CI logs.

**One deliberate exception: CI's scan of tracked file *paths* is a substring
match.** A filename concatenates where prose does not — `assets/<name>scan.png`
offers no word boundary — so whole-word matching there would miss exactly the
case that scan exists to catch. The consequence to know before it bites: with the
term `Ana`, a tracked file named `banana.png` fails CI. That job logs counts
only, never the offending path (a path can itself contain the term), so the
failure arrives without a filename. To find it, run the same substring match
locally:

```
DL=$([ -f pii-denylist.local ] && echo pii-denylist.local || echo pii-denylist.txt)
git ls-files | grep -i -F -f <(norm < "$DL")   # norm() as defined above
```

Same `norm()` as above, and for an overlapping reason. Two extra ways the raw
file misfires here, both verified on GNU grep 3.11: a **blank** line becomes an
empty pattern that matches every line, and a **comment** line becomes a literal
pattern — a bare `#` then matches any path containing one. This scan has no `-w`,
so neither is filtered out and you get most of your file list back.

A note on `-w`, since this document leans on it as the content scans' safety
property: it tests the characters **around** a match, not the characters in the
pattern. The match has to start at line start or after a non-word character and
end at line end or before one. So `-w` does stop a bare `#` matching
`banana#1.png`, and does stop `Ana` matching `banana.png` — but it still lets `#`
match a comment-shaped line, where the `#` sits at line start with a space after
it. Running `norm()` first is what removes those patterns; `-w` was never going
to.

The local hooks are armed **per clone** (`core.hooksPath`), so a fresh clone that
skipped that step has no local coverage while still being able to push. That is
exactly what the CI layer is the backstop for — don't treat the hooks alone as
coverage.

## The blind spot: Office files pass, and look clean doing it

**No layer of this gate can read inside a `.docx`, `.xlsx` or `.pptx`.** They are zip
archives, so gitleaks and the denylist grep are both handed compressed bytes rather than
words. A denylisted name inside a Word document commits, pushes, and passes CI — and that
outcome is byte-identical to a genuinely clean scan. Nothing distinguishes "scanned and
clean" from "never looked."

Measured 2026-08-19: two `.docx` scanned in place returned **zero** findings; extracting
`word/document.xml` from the same two and scanning that returned **three**, across two
rules. In that sample 60% of the findings were invisible to the gate.

This bites harder than the file count suggests, because Office documents are where prose
that was never written for a repo ends up — exported reports, meeting notes, client
material. That is a higher-than-average base rate for exactly the names and account
details the gate exists to stop, arriving in the one format it structurally cannot read.

**Until it is fixed, scan Office files by hand before committing them.** Unzip and scan
the inner XML rather than the archive, and scan the STAGED blob rather than the working
tree, since staged bytes are what commit:

```
git show ":path/to/doc.docx" > "$TMPDIR/d.docx"
unzip -p "$TMPDIR/d.docx" word/document.xml | sed -e 's/<[^>]*>/ /g' \
  | grep -i -F -w -f <(norm < "$DL")     # norm() and $DL as defined above
```

`xl/sharedStrings.xml` is the equivalent for `.xlsx`, `ppt/slides/*.xml` for `.pptx`.

Do not read a green gate as coverage of a commit that contains one of these. Tracked as
issue #228, which carries the shape of a fix and its acceptance test — put a denylisted
term inside a `.docx` and confirm the gate **blocks** before trusting any version that
claims to have closed this.

## Vasana

A vasana is a pattern that persists across unrelated contexts. If during this
task you notice such a pattern emerging, it may be worth capturing. This skill
works best alongside the `vasana` skill and `vasana` hook from the Vasana System
plugin.
