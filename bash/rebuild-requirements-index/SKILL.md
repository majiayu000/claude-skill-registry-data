---
name: rebuild-requirements-index
model: claude-haiku-5-5
category: requirements-kb
description: Rebuild search index for requirements repository
userInvocable: true
allowed-tools: Read, Bash, Task, AskUserQuestion
---

# Rebuild Requirements Index

Rebuild the search index for the team's requirements repository.

## Purpose

Fix corrupted, outdated, or missing index.json file that enables fast search of archived requirements.

## When to Use

- Index file corrupted (invalid JSON)
- Search failing or returning incorrect results
- After manual changes to requirements repository
- Index out of sync with actual requirements
- After repository cleanup or archival
- As part of maintenance routine

## What Gets Rebuilt

The index contains:
- List of all tickets with metadata
- Tag frequencies (for browsing)
- Component frequencies (for filtering)
- Project counts (for multi-project repos)
- Last updated timestamp

## Process

### Step 1: Check Configuration

Read project configuration:
```bash
# Source resolve-config: marketplace installs get ${CLAUDE_PLUGIN_ROOT} substituted
# inline before bash runs; legacy local copies fall back to ~/.claude. If neither
# path resolves, fail loudly rather than letting resolve_artifact be undefined.
if [ -f "${CLAUDE_PLUGIN_ROOT}/shared/resolve-config.sh" ]; then
  source "${CLAUDE_PLUGIN_ROOT}/shared/resolve-config.sh"
elif [ -f "$HOME/.claude/shared/resolve-config.sh" ]; then
  source "$HOME/.claude/shared/resolve-config.sh"
else
  echo "ERROR: resolve-config.sh not found — reinstall the nexus plugin: /plugin install nexus@claude-skills" >&2
  exit 1
fi
# Rebuilding WRITES to the knowledge base, so it gates on the strict resolver,
# never on resolve_artifact_typed. The advisory one fabricates
# .claude/requirements for an install that never configured a KB, which would
# make the "not configured" branch below unreachable and rebuild an index into
# a directory nobody set up. Same rule the archivist and /archive-requirements
# gate on.
if _RESOLVED=$(resolve_artifact_strict requirements requirements); then
  IFS='|' read -r REPO _TYPE <<< "$_RESOLVED"
else
  REPO=""   # not configured — print the block below and stop
fi

# ECHO BOTH VALUES. Shell state does not survive between Bash tool calls, so
# anything resolved here and not printed is invisible to every later step —
# which would leave the storage-type branch in Steps 2, 4 and 5 to be GUESSED.
# A guess toward "git" runs the bypass push against the user's own trunk. Read
# these two values out of this block's output and substitute them literally
# into every later command; never re-resolve, and never assume.
echo "REPO=$REPO"
echo "TYPE=$_TYPE"
```

**Also resolve `TICKET` here**, from the caller's context — the current branch
name, the active work session, or whatever the host project uses. **Check its
shape before carrying it: it must match `[A-Z][A-Z0-9]*-[0-9]+` or be the
literal `none`.** A branch name can contain `$(`, a backtick or a quote, and
this value is substituted into a `git commit -m "[...]"` line, so an unchecked
one is a command-injection surface in the user's own repository. If it does not
match, treat it as `none` and use a subject with no bracketed prefix rather than
passing it through — the prefix is a convenience, and no prefix is always safe. It is only
needed for a `directory`-type commit subject, which lands in the user's own
history. If there is no ticket in context, it is the literal string `none` and
the commit subject carries no bracketed prefix. Never leave `{TICKET}`
unsubstituted: it would appear verbatim in their log.

**Carry `REPO` and `TYPE` forward as literal values, not as shell variables.**
Every later `cd` in this skill uses the literal path this block printed. `cd ""`
**succeeds** and stays put, so a `cd "$REPO"` in a later call — where `REPO` is
unset — silently runs the rest of the step against whatever repository the
session is sitting in, which is the user's own project. Same reason the push in
Step 4 resolves its branch inline on one line.

**Only if `TYPE` (as printed above) is `git`**, sync before reading — a
`directory` KB has no remote to pull from. Substitute the literal path:

```bash
[ -n "<REPO printed above>" ] || exit 1
cd "<REPO printed above>" || exit 1
git pull
```

`cd "$REPO"`, not its parent: `git pull` operates on the containing repository
from any directory inside it, so no separate base variable is needed — and a
parent is not reliably the location root anyway (a multi-segment `subdir`, or
`subdir: .` where the resolver already returns the root). `|| exit 1` because
`cd` to an empty or missing path **succeeds or fails silently otherwise**, and a
`git pull` in the wrong repository is exactly the failure this skill must not
have.

**`TYPE` decides behaviour at every write site below.** It is resolved once, in
Step 1, and printed; every later step reads it from that output. No step in this
skill may write without stating what it does for both `git` and `directory`, and
no step may re-resolve or guess it. `directory` is the DEFAULT — it is what an
install with no explicit `type:` resolves to — so it is the common case, not the
exotic one.

> **`<REPO printed above>` is a placeholder, not a shell variable.** It stands for
> the literal `REPO` value Step 1 printed, substituted directly into the command
> before it runs. Nothing in this skill sets a `repo_path` shell variable, and
> nothing may rely on one surviving between Bash tool calls.
>
> **It is spelled `<… printed above>` rather than `${…}` on purpose.** A
> placeholder written in shell-variable syntax is indistinguishable from a real
> shell read — to a reader skimming a fence, and to any scanner checking that
> nothing relies on state surviving between Bash calls. This file used to spell
> the same value both ways, and the `${…}` half read as fifteen unbound variable
> reads. `<TYPE printed above>` follows the same rule — Step 1's fence echoes it.
>
> **`{TICKET}` is spelled differently on purpose, because its provenance is
> different, and it is spelled with that exact name because the name is
> already on the checked-shape allowlist in
> `tests/validators/placeholder-quoting.test` — `[A-Z]+-[0-9]+`, constrained by
> `plugin/CLAUDE.md`. A new spelling would have been a new allowlist entry for a
> value whose shape nothing checks.** Step 1 echoes `REPO` and `TYPE`; it does not echo `TICKET`,
> which you resolve from the caller's context — a branch name, an active work
> session. A value produced by an earlier fence is `<X printed above>` and is
> guarded with `-n`/`-d` at every use; a value you substitute from context is
> `{name}` whose SHAPE is checked somewhere, with the allowlist in
> `tests/validators/placeholder-quoting.test` recording where. Quoting is not
> what makes the second kind safe — a value of `a";id;"` closes the quote
> whatever wraps it — so a name with no shape check does not belong on a command
> line at all, quoted or not. The two kinds look identical in the source, and
> only the provenance tells them apart.
>
> **Every `cd` on it is preceded by an emptiness test, and that test is the
> guard — `cd … || exit 1` is not one.** `cd ""` returns 0 and stays put, so an
> empty substitution sails through the `||` and every command after it runs
> against whatever repository the session is in. The `||` only catches a path
> that exists nowhere.

**If not configured** — `resolve_artifact_strict` exited non-zero, so `REPO` is
empty. Print this and stop; do not delegate, and do not rebuild against a
default path:

> A non-zero exit is not always "not configured". Exit `5` means a configured
> value would resolve outside its storage location — a broken config, not a
> missing one — and the resolver's stderr names the key. Surface that message
> rather than the setup instructions above, which would send the user to fix
> something that is already set.

```
Requirements storage not configured

Configure in .claude/configuration.yml to rebuild index.
See: ${CLAUDE_PLUGIN_ROOT}/templates/requirements-repo/README.md (or ~/.claude/templates/requirements-repo/README.md for local/dev copies)
```

### Step 2: Confirm Rebuild

Use AskUserQuestion:

```
Rebuild requirements index?

Repository: <REPO printed above>
Current index: ${index_status}

This will:
- Scan all requirement directories
- Extract metadata from each
- Rebuild index.json
- Validate integrity

Existing index will be backed up to:
  index.json.backup.${timestamp}
  (kept locally, never committed; older backups pruned to the last 3)

On first run this also adds one line to <REPO printed above>/.gitignore
so backups stay untracked. Committed with the index.

Storage type: <TYPE printed above>
On success the rebuilt index will be:
  - git      → committed to the KB repo and pushed
  - directory → committed to THIS project's repo, not pushed

Time estimate: ~1 second per 100 requirements

Continue? [y/n]
```

**Name the storage type and the commit destination in the prompt.** Under
`directory` storage the commit lands in the user's own repository, which is a
materially different thing to consent to than a commit in a separate KB repo.
A confirmation that hides which one is happening is not informed consent.

### Step 3: Backup Current Index

This is a **write site**, and its rule is the same for both storage types:
**a backup is a local safety net, never a tracked artifact.** It is created on
disk, ignored by git, and pruned — it is never staged, committed, or pushed on
either branch.

Why ignored rather than committed: the real recovery mechanism is version
history, not these files. For a `git` KB the previous index is
`git show HEAD~1:index.json`; for a `directory` KB it is the same command in
the host project. Committing the backups would push clutter to a shared KB on
one branch and dirty the user's own working tree on the other, while adding
nothing history does not already provide.

```bash
# Call 1 — create the backup.
[ -n "<REPO printed above>" ] || exit 1
cd "<REPO printed above>" || exit 1
cp index.json "index.json.backup.$(date +%Y%m%d_%H%M%S)"
```

```bash
# Call 2 — make backups untrackable, idempotently. Without this they show up
# as untracked files in `git status` and can be swept into an unrelated
# `git add -A`, which under directory storage is the user's OWN repository.
#
# This is the KB's OWN .gitignore (<REPO printed above>/.gitignore), never the host
# project's root one — hence the `cd` and `|| exit 1`, which is load-bearing:
# `cd ""` succeeds and stays put, and appending this line to a user's project
# root .gitignore would be a surprising edit to a file this command has no
# business touching.
[ -n "<REPO printed above>" ] || exit 1
cd "<REPO printed above>" || exit 1
# Append a newline first if the file exists and does not end in one. Without
# this, `printf >>` concatenates onto the last entry — turning `node_modules`
# into `node_modulesindex.json.backup.*` and silently un-ignoring it.
[ -s .gitignore ] && [ -n "$(tail -c1 .gitignore)" ] && printf '\n' >> .gitignore
grep -qxF 'index.json.backup.*' .gitignore 2>/dev/null \
  || printf '%s\n' 'index.json.backup.*' >> .gitignore
```

```bash
# Call 3 — retention: keep the 3 newest, delete the rest. Backups are created
# on every rebuild and previously accumulated without bound.
#
# NUL-delimited end to end, deliberately. The obvious
# `ls -1t ... | tail -n +4 | xargs -r rm --` splits on whitespace, so a single
# backup filename containing a space becomes two rm arguments and can delete an
# unrelated file. That is not hypothetical here: on a git-backed KB, Step 1
# pulls before this runs, so any filename in the shared KB is content someone
# else can author. This deletes user files — it gets the strict form.
[ -n "<REPO printed above>" ] || exit 1
cd "<REPO printed above>" || exit 1
find . -maxdepth 1 -name 'index.json.backup.*' -printf '%T@ %p\0' 2>/dev/null \
  | sort -zrn | tail -zn +4 | cut -zd' ' -f2- | xargs -0r rm --
```

> **Sorted by mtime, not by the name's timestamp.** Deliberate: a
> restored-then-re-backed-up file has a newer mtime than its name suggests, and
> keeping what was most recently *touched* is what an operator reaching for a
> backup actually wants. `-maxdepth 1` so nothing below the KB root is ever
> considered, `xargs -0r` so an empty list is a no-op, and `rm --` so a filename
> beginning with a dash is never read as an option. `rm` on a symlink removes
> the link, never its target.
>
> `find -printf` and `sort -z`/`tail -z`/`cut -z` are GNU. On a system without
> them, prune by hand rather than reaching for the whitespace-splitting form —
> deleting the wrong file is worse than keeping too many backups.

If Call 2 created or modified `.gitignore`, it **is** a tracked change and
travels with the index commit in Step 4 — but only if the caller has no staged
changes of their own to that same file. Check before including it:

```bash
[ -n "<REPO printed above>" ] || exit 1
cd "<REPO printed above>" || exit 1
git diff --cached --name-only -- .gitignore
```

If that prints anything, the caller already staged their own `.gitignore` edit.
Commit `index.json` alone, and tell the user the ignore rule is written but
uncommitted — committing it would sweep up their change, and unstaging on
failure would discard it. Otherwise include `.gitignore` in Step 4's path list.
Either way it is a one-time cost: every later rebuild finds the line present and
writes nothing.

### Step 4: Delegate to Archivist

Use Task tool with `subagent_type: "archivist"`:

```
Task(archivist, "Rebuild requirements index

Repository: <REPO printed above>
Storage type: <TYPE printed above>
Commit .gitignore alongside index.json: {gitignore_decision}   (`include` or `omit` — the trackability check above decides)
Host project ticket: {TICKET}   (or "none" — then use a subject with no prefix)

Substitute all four as LITERALS before dispatching. The
archivist runs in its own context and cannot see this skill's shell state, its
Bash output, or its earlier steps — a step-9 branch on a value that was never
put in this prompt is a branch on nothing.

Process:
1. Scan all directories in repository root
2. For each directory with metadata.json:
   a. Read metadata.json
   b. Extract: id, title, description, tags, components, etc.
   c. Add to index tickets array
   d. Update tag/component/project frequencies
3. Skip directories: templates/, archive/, .git/
4. Handle missing or malformed metadata gracefully
5. Sort tickets by date (newest first)
6. Generate new index.json
7. Validate JSON structure
8. Write to repository
9. Commit the rebuilt index. Branch on the `Storage type` given at the top of
   this prompt — a literal, resolved before you were dispatched. Never
   re-derive it, and never guess: you cannot see the caller's shell or its
   config.

   > **`cd` and `git commit`/`git push` never share a Bash call.** The
   > mutation guard's credential scan is anchored to a command *starting with*
   > `git commit` (`^\s*git\s+commit`), so a `cd … && git commit …` call
   > begins with `cd` and the scan is silently skipped — the exact hazard
   > [`kb-write-pattern.md`](../../shared/kb-write-pattern.md) rule 2 exists to
   > close. The `cd` (with `git add`) goes in ONE call; the commit LEADS the
   > next one. **The working directory persists across Bash tool calls**, so the
   > earlier `cd` still applies — it is shell *variables* that do not survive,
   > which is why `TYPE` is carried as a literal instead.

   **First, confirm the KB path is trackable — before anything is staged.**
   Many projects gitignore `.claude/`, and the default directory KB lives at
   `.claude/requirements`. There, `git add` adds nothing and the commit fails
   with "nothing to commit", which must be reported as a failed rebuild rather
   than a quiet success. Asking after staging would get the answer too late to
   change what happened. It is read-only, so it may share a call with its `cd`:

   ```bash
   [ -n "<REPO printed above>" ] || exit 1
   cd "<REPO printed above>" || exit 1
   git check-ignore -q -- index.json \
     && echo "IGNORED — the KB path is gitignored; the rebuilt index cannot be committed"
   ```

   The `cd` is not optional: run from the caller's directory instead and this
   returns non-zero for a reason that has nothing to do with the KB, which reads
   as "not ignored" and disables the very guard it is. `check-ignore` also exits
   non-zero when the path is not in a git repository at all — if
   `git rev-parse --is-inside-work-tree` is false there is nothing to commit to,
   which is a different message again.

   **If it reports IGNORED, stop here**: the index was rebuilt on disk and is
   usable, but it will not travel with the repository. Report that plainly and
   do not stage or commit.

   **Then stage explicitly, and only what this rebuild produced.** On both
   branches — this is the call that establishes the working directory for the
   commit that follows:
   ```bash
   [ -n "<REPO printed above>" ] || exit 1
   cd "<REPO printed above>" || exit 1
   git add -- index.json .gitignore   # include .gitignore only if this prompt's decision says yes
   ```
   Never `git add -A` or `git add .`: the backups are gitignored but any other
   incidental change in the tree is not, and under directory storage that tree
   is the user's own project.

   **If the repository is a directory-type location** (the default),
   commit locally and STOP — no push, and never `NEXUS_KB_WRITE=1` /
   `SECURITY_AUDITOR_BYPASS=1`, since that KB is inside the host project's own
   repo and those variables would disable that project's branch protection and
   audit gate against its own trunk. This branch mirrors archivist STORE step 7
   branch B, and the three details that make it safe are not optional:

   a. **The trackability check above has already run.** If it reported
      IGNORED you are not here.

   b. **Scope the commit with `--`.** Under directory storage the KB is the SAME
      repository the caller is working in, so a bare `git commit -m` sweeps up
      everything that caller already staged:
      The commit LEADS its own Bash call — no `cd`, no `&&`, nothing before it.
      The working directory is already the KB from the staging call above:
      ```bash
      git commit -m "[{TICKET}] chore(requirements): rebuild the requirements index" -- index.json .gitignore
      ```
      `{TICKET}` is the `Host project ticket` value from the top of this
      prompt — this commit lands in the user's own history alongside their
      code, so it follows their convention, not this plugin's. If that value is
      `none`, drop the bracketed prefix entirely. Include `.gitignore` in the
      path list only if `Commit .gitignore alongside index.json` above says yes.

      A pathspec commit is refused outright during a merge or rebase ("cannot
      do a partial commit during a merge"). That is not a rebuild failure —
      report it as "finish the in-progress merge, then re-run", not as a
      generic commit error.

   c. **Unstage on failure.** If the commit fails for any reason, leaving these
      paths staged means the caller's next commit silently absorbs them,
      reintroducing exactly the contamination `--` prevents:
      ```bash
      [ -n "<REPO printed above>" ] || exit 1
      cd "<REPO printed above>" || exit 1
      git restore --staged -- index.json .gitignore
      ```
      (`git restore` is not a guarded mutation verb, so it may share a call
      with its `cd`; only `git commit` and `git push` must lead.)
      Restrict this to the paths this step actually staged. `git restore
      --staged` resets to HEAD, so including a path the caller had staged
      themselves would discard their staged version — which is why
      `.gitignore` is only ever in the list when this prompt's decision says so.

   Verify a commit object was actually created before reporting success.

   **If the repository is a git-backed KB location**: commit and push using the
   sanctioned KB-write pattern (see
   ${CLAUDE_PLUGIN_ROOT}/shared/kb-write-pattern.md) — `cd` into `<REPO printed above>`
   (never `git -C`). The commit is scoped with `--` here too, for consistency
   with the directory branch and because a separate KB repo can still hold
   unrelated staged work. It LEADS its own Bash tool call so the credential
   scan runs — a compound `cd && git commit` starts with `cd` and the guard's
   anchored regex silently skips the scan:

   ```bash
   git commit -m "Rebuild requirements index" -- index.json .gitignore
   ```
   **Anchor and verify the working directory in the call immediately before the
   push.** The push leads its own call and therefore carries no `cd`, so it
   inherits whatever cwd is current. Confirm it is the KB before sending a
   double-bypass push anywhere:

   ```bash
   [ -n "<REPO printed above>" ] || exit 1
   cd "<REPO printed above>" || exit 1
   git rev-parse --is-inside-work-tree >/dev/null 2>&1 || exit 1
   [ -f index.json ] || exit 1
   ```

   Mechanical, not eyeballed: each line exits non-zero rather than printing
   something for a human to check. A non-zero exit means do not push.

   > **Not** `[ "$(git rev-parse --show-toplevel)" = "$(pwd -P)" ]`. The KB is
   > normally a SUBDIRECTORY of its repository — the shipped configuration is
   > `requirements: { location: team-knowledge, subdir: requirements }`, so the
   > toplevel is the location root and cwd is one level below it. That
   > comparison fails on a correct setup and would silently stop every push.
   >
   > What needs proving is that cwd is a knowledge base and not somewhere else.
   > These two lines carry exactly that and no more: cwd is inside a work tree
   > at all, and an `index.json` exists here. That is a location check, not a
   > freshness one — `[ -f index.json ]` does not prove the file is the one this
   > run rebuilt, and nothing here should be read as claiming it does. It is
   > enough for the hazard it guards: if `<REPO printed above>` were empty, `cd ""`
   > would succeed and leave cwd in the host project, which has no `index.json`
   > at its root.

   Then, in a SEPARATE call, the `git push` must ALSO lead its own call so the
   guard's push block engages and logs the bypass WARNs (if anything precedes
   `git push` — e.g. a `default_branch=...` assignment — the anchored regex
   misses and the whole push block, WARNs included, is silently skipped). Since
   shell variables do not survive across Bash calls, resolve the branch INLINE
   in the push argument on one line:

   ```bash
   NEXUS_KB_WRITE=1 SECURITY_AUDITOR_BYPASS=1 git push origin -- "$(git symbolic-ref --short refs/remotes/origin/HEAD 2>/dev/null | sed 's#^origin/##' | grep . || timeout 10 git ls-remote --symref origin HEAD 2>/dev/null | awk '/^ref:/{sub("refs/heads/","",$(2));print $(2);exit}' | grep . || echo master)"
   ```
   Both bypasses are logged; do NOT call `record-audit.sh`, which would
   rubber-stamp an audit that never ran.
10. Report statistics and issues

Return:
- Tickets scanned
- Tickets added to index
- Issues found (missing metadata, malformed JSON, etc.)
- Tag and component counts
- Backup location
")
```

### Step 5: Report Results

**Success:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ Index Rebuilt Successfully
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Repository: <REPO printed above>
Execution time: 2.3 seconds

SCAN RESULTS
────────────────────────────────────────────────
Directories scanned: 28
Requirements found: 25
Added to index: 24
Skipped: 1 (issues)

STATISTICS
────────────────────────────────────────────────
Unique tags: 45
Unique components: 78
Projects: 3
Date range: YYYY-MM-DD to YYYY-MM-DD

TAG FREQUENCIES (top 10)
────────────────────────────────────────────────
api              : 15
database         : 12
export           : 8
authentication   : 5
integration      : 4
...

COMPONENT FREQUENCIES (top 10)
────────────────────────────────────────────────
UserController   : 8
AuthService      : 5
ExportService    : 3
ApiController    : 3
...

ISSUES FOUND
────────────────────────────────────────────────
⚠ USER-100: Missing metadata.json (skipped)

Recommendation: Add metadata.json or move to archive/

BACKUP
────────────────────────────────────────────────
Old index backed up to:
  index.json.backup.20260203_143022
Backups pruned: 2 removed, 3 kept (never committed — gitignored)

WHERE IT WENT                       (storage type: directory)
────────────────────────────────────────────────
Committed to THIS project's repository, not pushed:
  commit abc123: "[PROJ-42] chore(requirements): rebuild the requirements index"
  paths: index.json

Push it with your normal review flow — the KB travels with this repo.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Test search: /search-requirements "export"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**The "WHERE IT WENT" block is required and must name the storage type**, since
the two destinations differ in a way the user acts on. Substitute for a
git-backed KB:

```
WHERE IT WENT                       (storage type: git)
────────────────────────────────────────────────
Committed and pushed to the KB repository:
  commit abc123: "Rebuild requirements index"
  pushed to: origin/master
```

And when the directory-type KB path turned out to be gitignored (Step 4's
check-ignore guard fired), report that instead of a commit — the rebuild
succeeded on disk but produced nothing tracked:

```
WHERE IT WENT                       (storage type: directory)
────────────────────────────────────────────────
NOT committed — the KB path is gitignored in this project.
The rebuilt index is on disk and search works; it will not travel with the repo.
```

**With Issues:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠ Index Rebuilt with Issues
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Directories scanned: 30
Requirements found: 27
Added to index: 24
Skipped: 3 (issues)

ISSUES
────────────────────────────────────────────────
❌ USER-100: Missing metadata.json
   → Add metadata or move to archive/

❌ USER-101: Malformed metadata.json (invalid JSON)
   → Fix JSON syntax or regenerate metadata

⚠ USER-102: Missing required fields (title, description)
   → Update metadata.json with required fields

RECOMMENDATIONS
────────────────────────────────────────────────
1. Fix or archive problematic requirements:
   - USER-100: Add metadata.json
   - USER-101: Fix JSON syntax
   - USER-102: Add missing fields

2. Or move to archive/:
   mv USER-100 archive/2025/USER-100

3. Rebuild after fixing:
   /rebuild-requirements-index

Index is functional but incomplete.
Search will work but won't include skipped requirements.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Examples

### Example 1: Simple Rebuild

```bash
/rebuild-requirements-index
```

Rebuilds index from all requirements in repository.

### Example 2: After Manual Changes

```bash
# After manually editing metadata
/rebuild-requirements-index
```

Ensures index reflects manual changes.

### Example 3: After Cleanup

```bash
# After moving old requirements to archive/
mv USER-* archive/2025/
/rebuild-requirements-index
```

Removes archived requirements from index.

## When to Rebuild

### Required

- **Index corrupted** - Invalid JSON, cannot parse
- **Index missing** - File deleted or never created
- **Search fails** - Errors when searching

### Recommended

- **After bulk operations** - Archiving multiple requirements
- **After manual edits** - Direct changes to metadata.json
- **After cleanup** - Moving requirements to archive/
- **Periodic maintenance** - Monthly or quarterly

### Optional

- **After single archive** - Automatic in `/archive-requirements`
- **Normal usage** - Index auto-updated on archive

## Safety

### Non-Destructive

- Original requirements files unchanged
- Old index backed up before rebuild
- Backup includes timestamp
- Can restore from backup if needed

### Restore from Backup

If rebuild caused issues. `<REPO printed above>` and `<TYPE printed above>` are the literal values
Step 1 printed — this path branches on the storage type exactly as Step 4 does,
and is not exempt from any of its rules:

```bash
[ -n "<REPO printed above>" ] || exit 1
cd "<REPO printed above>" || exit 1

# Find backups (the last 3 are kept; older ones are pruned on each rebuild)
ls -lt index.json.backup.*
```
```bash
# Restore from backup (cwd persists from the call above)
cp index.json.backup.20260203_143022 index.json
```

**If no backup survives the retention window**, version history is the fallback
and works on both storage types — `git show HEAD~1:index.json > index.json` in
`<REPO printed above>`, or a further-back revision. Backups are a convenience for the
operator who just ran the rebuild; history is the durable record. That is why
they are gitignored rather than committed.

Then commit — **and push only if the KB is git-backed**. Branch on `<TYPE printed above>`
as printed by Step 1, exactly as archivist STORE step 7 does; the restore path
is not exempt from that rule, and it must not re-derive the type either.

**Call 1 — re-establish the working directory, then stage.** Do not rely on the
`cd` further up surviving a user pause; redo it here, guarded. `git add` is not
a guarded verb, so it may share this call.

```bash
[ -n "<REPO printed above>" ] || exit 1
cd "<REPO printed above>" || exit 1
git add -- index.json
```

**Call 2 — the commit, and nothing before it.** Both branches commit, and both
scope with `--`: under directory storage this is the caller's OWN repository, so
a bare commit would sweep up whatever they had already staged.

> The fence below opens with `git commit` on its very first byte, and that is
> load-bearing. The mutation guard matches `^[[:space:]]*git[[:space:]]+commit`
> against the whole tool input — a `#` is not whitespace, so a call that opens
> with even a COMMENT never matches and the credential scan is silently
> skipped, exactly as a leading `cd` would do it. Explanations go in prose
> above the fence, never inside it.

```bash
git commit -m "Restore index from backup" -- index.json
```

**If `<TYPE printed above>` is `directory`: stop here.** Do not push, and do not use
`NEXUS_KB_WRITE=1` or `SECURITY_AUDITOR_BYPASS=1`. Under directory storage the KB
lives inside the host project's own repository, so those variables would disable
that project's branch protection and audit gate against its own trunk — and this
is the DEFAULT storage type, so it is the common case. The restored index travels
with the operator's normal review-and-merge flow.


**Anchor the working directory in the call immediately before the push.** The
push must lead its own call, so it cannot carry a `cd` — which means it inherits
whatever cwd is current, and on this path that `cd` may be many steps and a user
pause earlier. A drifted cwd sends a double-bypass push at the host project's own
trunk. Verify first, and push only if every line below passes:

```bash
[ -n "<REPO printed above>" ] || exit 1
cd "<REPO printed above>" || exit 1
git rev-parse --is-inside-work-tree >/dev/null 2>&1 || exit 1
[ -f index.json ] || exit 1
```

Each line exits non-zero rather than printing for a human to check. Not a
toplevel/cwd comparison — the KB is normally a subdirectory of its repository,
so that would fail on a correct setup; see Step 4's note.

**If `<TYPE printed above>` is `git`**, push with the sanctioned KB-write pattern
(`${CLAUDE_PLUGIN_ROOT}/shared/kb-write-pattern.md`): the push leads its own Bash
call and resolves the branch inline (shell variables do not persist across Bash
tool calls).

**Call 3 — git-backed KB only.** The push leads the call, on ONE line, so the
guard engages and logs the bypass WARNs. Same rule as the commit above: no
comment, no assignment, no `cd` inside this fence.

```bash
NEXUS_KB_WRITE=1 SECURITY_AUDITOR_BYPASS=1 git push origin -- "$(git symbolic-ref --short refs/remotes/origin/HEAD 2>/dev/null | sed 's#^origin/##' | grep . || timeout 10 git ls-remote --symref origin HEAD 2>/dev/null | awk '/^ref:/{sub("refs/heads/","",$(2));print $(2);exit}' | grep . || echo master)"
```

## Validation

The rebuild process validates:

**Required fields:**
- id (must be unique)
- title
- description
- status

**Optional fields:**
- tags (array)
- components (array)
- date (ISO format)
- project

**Structure:**
- Valid JSON syntax
- No duplicate ticket IDs
- All dates parseable
- Arrays are arrays (not strings)

## Troubleshooting

### Permission Denied

```
❌ Cannot write to repository

Path: /path/to/requirements-repo/index.json
Error: Permission denied

Check:
1. File permissions: chmod 644 index.json
2. Directory permissions: chmod 755 /path/to/requirements-repo
3. Git permissions

Fix and retry: /rebuild-requirements-index
```

### Git Conflicts

Only reachable on a **git-backed** KB — a `directory` KB has no second writer
to conflict with, since it lives in the host project's own tree and its commits
go through that project's normal flow.

```
❌ Git conflict when committing index

Another developer may have rebuilt simultaneously.

To resolve:
1. cd <REPO printed above>
2. git pull --rebase
3. Retry: /rebuild-requirements-index
```

### Nothing to Commit (directory-type KB)

```
⚠ Index rebuilt on disk, but nothing was committed

The KB path is gitignored in this project (commonly: the KB is under .claude/
and .claude/ is ignored).

Search works — the index is on disk and current. It simply will not travel with
the repository.

To change that, either un-ignore the KB path, or point the requirements
artifact at a git-backed location in .claude/configuration.yml.
```

### Invalid Metadata

```
⚠ Found 3 requirements with invalid metadata

Details:
- USER-100: Missing metadata.json
- USER-101: Invalid JSON syntax
- USER-102: Missing required field: title

Options:
1. Fix metadata in these requirements
2. Move to archive/: mv USER-100 archive/2025/
3. Skip and rebuild anyway (index will be incomplete)

How to proceed? [fix/archive/skip]
```

## Maintenance Schedule

**Recommended:**

- **After bulk operations** - Immediately
- **After manual changes** - Immediately
- **Routine maintenance** - Monthly
- **Before important searches** - If index seems stale

**Signs index needs rebuild:**
- Search returns unexpected results
- Missing recent requirements
- Duplicate results
- Search errors

## See Also

- `/search-requirements <query>` - Search using the index
- `/archive-requirements [id]` - Archive (auto-updates index)
- `/load-requirements <id>` - Load specific requirement
