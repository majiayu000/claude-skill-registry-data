---
name: jujutsu
type: reference
description: Reference for Jujutsu (jj) version control commands. ALWAYS read before performing ANY jj operation (commit, squash, rebase, describe, split, etc.) to ensure correct syntax and best practices.
---

## Jujutsu Command Reference

Working copy is always a commit. Changes are first-class with stable IDs across rewrites.

### Best Practices

- **Local Commit Autonomy**: `jj describe`, `jj commit`, and `jj new` are allowed when they are part of the current requested task and stay local.
- **User Authorization**: NEVER push (`jj git push`) or run destructive/history-rewriting operations (`jj edit`, `jj squash` across bookmarks/shared history, `jj split`, `jj rebase`, `jj abandon`, `jj undo`, `jj op restore`, bookmark moves/deletes, tag moves/deletes) without explicit user confirmation. Routine local amends (`jj squash`, `jj squash --into @- -u`) do not need confirmation.
- **Bookmark Creation**: NEVER run `jj bookmark create` unless the user explicitly asks for a bookmark. When the user does ask, create only the bookmark(s) they requested — do not create a new bookmark per commit unless the user explicitly asked for that.
- **Logical Commits**: Group changes into logical steps; try to make each commit "usable" on its own.
- **Commit + Advance**: Prefer `jj commit -m "msg"` when finalizing the current working-copy commit and moving on. This replaces the common `jj describe <id> -m "msg"` followed by `jj new <id>` sequence.
- **Working Copy After Commit**: After `jj commit` or `jj new`, a new empty commit becomes `@`. This is expected jj behavior — do not attempt to remove or squash it away.
- **Revision References**: Use `@`, `@-`, and revsets for immediate one-off commands when they are clear. Use explicit change IDs for scripts, multi-step instructions, destructive operations, and commands where the target could become ambiguous.
- **Non-Interactive Squashing**: When squashing, if the source revision is abandoned and both source and destination have non-empty descriptions, `jj squash` opens `$EDITOR` to combine descriptions. In automated or agent environments, ALWAYS pass `-u` (`--use-destination-message`) to keep the destination description, or pass `-m "message"` to set a new description explicitly.
- **Squash Direction**: Use `jj squash --from <from-id> --into <to-id>` (or `--to`). Prefer **from newer to older** (descendant to ancestor) to match default `jj squash` and minimize conflicts. Squashing older into newer (e.g., `--from <base> --into <head>`) rewrites head's ancestors, forcing jj to rebase descendants and resolve any overlapping diff conflicts.
- **Splitting**: Use `jj split -r <change-id> -m "<commit-message>" -- <file>`; do not use interactive `jj split` unless human interaction or a diff editor session is required.
- **Commit Messages**: Keep subject line <= 72 characters; body lines <= 72 characters. Use imperative mood ("add feature" not "added feature"). Explain "what" and "why", not "how".

### Key Concepts

- `@` = working copy commit
- `@-` = parent, `@--` = grandparent, `@+` = child
- Revsets: `::@` (ancestors), `main..@` (commits since main), `mutable()` (all non-immutable commits)
- Default `jj log` shows only mutable revisions (plus working-copy + bookmarked context). Use `jj log -r ::` or `all()` to see all visible commits, including immutable ancestors.
- Immutable commits: those in `::immutable_heads()` (default includes `trunk()`-ancestors) are immutable; jj refuses to mutate them. Bypass with `--ignore-immutable` only when you intend to rewrite them.

### Global Options

| Option | Description |
| --- | --- |
| `--ignore-immutable` | Allow rewriting immutable commits (all except root commit) |
| `--at-op=<op-id>` / `--at-operation <op-id>` | Load repository state at a specific past operation (read-only inspect or fork) |
| `--ignore-working-copy` | Do not snapshot or update working-copy commit (useful in prompts/scripts) |
| `--no-integrate-operation` | Run command and print resulting op ID without updating op log or working copy |
| `-R, --repository <path>` | Operate on a specific repository path |
| `--quiet` | Silence non-primary command output |
| `--no-pager` | Disable output pager |

### Day-to-Day Commands

| Task | Command |
| --- | --- |
| Status | `jj status` (alias: `st`) / `jj show <id>` |
| Diff | `jj diff -r <id>` / `jj diff --from <a> --to <b>` |
| Interdiff | `jj interdiff --from <a> --to <b>` |
| Log | `jj log -r <revset>` |
| Finalize current + move on | `jj commit -m "msg"` (alias: `ci`) |
| New working commit on parent | `jj new <parent-id> -m "msg"` |
| Describe without moving | `jj describe <id> -m "msg"` (alias: `desc`) |
| Move to child / parent commit | `jj next` / `jj prev` |
| Navigate / make active | `jj edit <id>` |
| Abandon commit | `jj abandon <id>` |
| Squash changes into parent | `jj squash -u` / `jj squash --into @- -u` |
| Squash between specific commits | `jj squash --from <src> --into <dst> -u` |
| Absorb changes into stack | `jj absorb` / `jj absorb [paths]...` |
| Split commit | `jj split -r <id> -m "msg" -- <path>` |
| Rebase branch | `jj rebase -b <branch> -o <dest>` |
| Rebase single revision | `jj rebase -r <id> -o <dest>` |
| Duplicate revisions | `jj duplicate <id> -o <dest>` |
| Parallelize revisions | `jj parallelize <revset>` |
| Simplify parent edges | `jj simplify-parents -r <id>` |
| Show file at revision | `jj file show <path> -r <id>` |
| Blame file | `jj file annotate <path> -r <id>` |
| Search file content | `jj file search --pattern <pattern> [paths]... -r <id>` |
| Change file permissions | `jj file chmod x <path>` / `jj file chmod n <path>` |
| Format / fix code | `jj fix -s <revset>` |
| Modify metadata | `jj metaedit -r <id> -m "msg"` |
| Tag management | `jj tag set <name> -r <id>` / `jj tag list` |
| Bookmark management | `jj bookmark set <name> -r <id>` / `jj bookmark list` |
| Bisect bug | `jj bisect run --range <revset> -- <cmd>` |
| Sign / unsign commit | `jj sign -r <id>` / `jj unsign -r <id>` |
| Resolve conflicts | `jj resolve -r <id>` |
| Undo / redo operation | `jj undo` / `jj redo` |

---

### Squashing & Amending Changes

`jj squash` moves changes from one revision into another.

#### Command Syntax

```bash
# Squash working copy into parent (@ into @-) discarding @ description
jj squash -u

# Squash working copy into parent with a new description
jj squash -m "new combined description"

# Squash specific revision into its parent
jj squash -r <revset> -u

# Squash from source into destination revision
jj squash --from <from-revset> --into <to-revset> -u

# Squash only specific files or paths
jj squash <paths>... -u
jj squash --from <from-id> --into <to-id> <paths>... -u

# Keep the source revision after moving changes (do not abandon it)
jj squash --keep-emptied -u
```

#### Important Behavior & Flags

- **Editor Prompt Prevention**: If the source revision is abandoned and both source and destination have non-empty descriptions, `jj squash` opens `$EDITOR`. To avoid blocking on an editor:
  - Use `-u` / `--use-destination-message`: Keeps destination's message, discards source's message.
  - Use `-m "<message>"` / `--message "<message>"`: Provides a replacement message directly.
- **Flags**:
  - `-f, --from <REVSETS>`: Source revision(s) to squash from (default: `@`).
  - `-t, --into <REVSET>` (alias: `--to`): Destination revision to squash into (default: `@-` when squashing working copy).
  - `-r, --revision <REVSET>`: Squash specified revision into its single parent.
  - `-u, --use-destination-message`: Discard source description and retain destination description.
  - `-m, --message <MESSAGE>`: Explicit description for squashed revision (avoids editor).
  - `-k, --keep-emptied`: Do not abandon source revision if it becomes empty.
  - `-i, --interactive`: Interactively pick changes to squash via diff editor (`--tool <name>`).
- **Experimental Placement Flags**:
  - `-o, --onto <REVSETS>`: Squash from source into a new commit on top of specified parent.
  - `-A, --insert-after <REVSETS>`: Insert squashed commit after target.
  - `-B, --insert-before <REVSETS>`: Insert squashed commit before target.

#### Recommended Squash Workflow

Always squash from newer into older (descendant into ancestor):

```bash
# Correct: newer into older
jj squash --from @- --into @-- -u
jj squash --from <child-id> --into <parent-id> -u

# Wrong: older into newer — rewrites ancestors and causes rebase conflicts
jj squash --from <parent-id> --into <child-id> -u
```

---

### Absorb Changes

`jj absorb` splits working-copy (or source) changes and automatically moves each hunk into the closest mutable ancestor where the affected lines were last modified.

```bash
# Absorb all working copy changes into mutable ancestors
jj absorb

# Absorb changes only for specific paths
jj absorb src/utils/

# Absorb changes from a specific revision into specific target revisions
jj absorb --from <revset> --into <revsets>
```

- If all changes in the source revision are absorbed and the source has no description, the source is automatically abandoned.
- Review what absorb did using `jj op show -p`.

---

### Tags

Tags mark specific immutable milestones (matching Git tags).

```bash
# Create or update a tag on target revision (default: @)
jj tag set <name> -r <id>

# Move an existing tag to a new revision (requires --allow-move)
jj tag set <name> -r <id> --allow-move

# List tags
jj tag list
jj tag list -a                          # Include all remotes
jj tag list -r 'v1.0::'                 # Filter tags in revset
jj tag list --sort committer-date-      # Sort descending by committer date

# Delete a tag
jj tag delete <name>
```

---

### Bookmarks (Branches)

Bookmarks track named branches (matching Git branches).

```bash
# Create a new bookmark
jj bookmark create <name> -r <id>

# Create or update a bookmark by name
jj bookmark set <name> -r <id>
jj bookmark set <name> -r <id> -B       # Allow moving backwards or sideways (-B/--allow-backwards)

# Move existing bookmark to a revision
jj bookmark move <name> --to <id>
jj bookmark move --from <revset> --to <id>

# Advance closest bookmarks to target revision (default: @)
jj bookmark advance --to <id>

# Rename a bookmark
jj bookmark rename <old> <new>
jj bookmark rename <old> <new> --overwrite-existing

# Delete bookmark (propagates deletion to remote on next push)
jj bookmark delete <name>

# Forget bookmark locally without deleting on remote
jj bookmark forget <name>
jj bookmark forget <name> --include-remotes

# Remote bookmark tracking
jj bookmark track <name> --remote origin
jj bookmark untrack <name> --remote origin

# List bookmarks
jj bookmark list
jj bookmark list -a                     # All remotes
jj bookmark list -t                     # Tracked remotes only
jj bookmark list -c                     # Conflicted bookmarks only
jj bookmark list -r <revset>            # Bookmarks pointing to revset
jj bookmark list --sort name            # Sort by name
```

---

### Navigation & Moving Working Copy

```bash
# Move working copy to parent (equivalent to stepping back 1 commit)
jj prev
jj prev 2                               # Move back 2 commits
jj prev --edit                          # Edit parent directly instead of creating new working commit

# Move working copy to child (equivalent to stepping forward 1 commit)
jj next
jj next 2                               # Move forward 2 commits
jj next --edit                          # Edit child directly instead of creating new working commit
jj next --conflict                      # Jump forward to next conflicted descendant

# Switch working copy to an arbitrary revision
jj edit <id>

# Create a new empty working-copy commit on top of target parent(s)
jj new <parent-id> -m "msg"
jj new @ <other-id>                     # Create a merge commit with 2 parents
jj new --insert-after <parent>          # Insert new commit between parent and its children
jj new --insert-before <child>          # Insert new commit before child
```

---

### Graph Manipulation & Rebasing

#### Rebasing

```bash
# Rebase full branch (source and all descendants) onto destination
jj rebase -b <branch-revset> -o <dest-revset>

# Rebase single revision (rebasing its descendants onto its parents)
jj rebase -r <revset> -o <dest-revset>

# Rebase revision and its descendants onto destination
jj rebase -s <revset> -o <dest-revset>

# Insert rebased revision after a target (rebasing target's descendants on top)
jj rebase -r <id> -A <target>

# Insert rebased revision before a target
jj rebase -r <id> -B <target>

# Create a merge by repeating -o
jj rebase -s <id> -o <parent1> -o <parent2>

# Rebase flags
jj rebase -b @ -o main --skip-emptied       # Abandon commits that become empty
jj rebase -b @ -o main --simplify-parents   # Remove redundant parent edges
jj rebase -b @ -o main --keep-divergent     # Keep divergent commits
```

#### Duplicating Commits

```bash
# Duplicate revision onto destination
jj duplicate <id> -o <dest>
jj duplicate <id> -A <target>
jj duplicate <id> -B <target>
```

#### Parallelizing Commits

```bash
# Convert a linear stack of commits into siblings with common parent
jj parallelize 1::3
```

#### Simplifying Parents

```bash
# Remove redundant transitive parent links in merge commits
jj simplify-parents -r <id>
jj simplify-parents -s <source-revset>
```

#### Interactive Graph Arrangement

```bash
# Interactively rearrange commit stack order
jj arrange [revsets]...
```

---

### Splitting Commits

#### Non-Interactive Split (Automated/Agent Workflows)

```bash
# Split specific files out into a new commit with description
jj split -r <id> -m "feat: extracted module" -- <path/to/file>
```

#### Interactive Split

```bash
# Split commit interactively using diff editor
jj split -r <id>

# Split working copy interactively
jj split -m "First part"
```

---

### Comparing & Inspecting Diffs

```bash
# Show status of working copy and conflicted commits
jj status                               # alias: st

# Inspect commit details and summary
jj show <id>

# Diff revision against its parents
jj diff -r <id>
jj diff -s -r <id>                      # Summary of changed files only (-s / --summary)
jj diff --stat -r <id>                  # Diffstat output

# Diff between two arbitrary revisions
jj diff --from <rev1> --to <rev2>
jj diff --from <rev1> --to <rev2> -- <path>

# Compare diff changes across commit rewrites (evolution diff)
jj interdiff --from <rev1> --to <rev2>
```

---

### File Operations

```bash
# Print file contents at revision
jj file show <path> -r <id>

# Annotate lines with source commits (blame)
jj file annotate <path> -r <id>

# List tracked files in revision
jj file list -r <id>

# Search file content for pattern (supports glob/regex)
jj file search --pattern "regex-pattern" [paths]... -r <id>

# Change executable bit across platforms and revisions
jj file chmod x <path> -r <id>          # Make executable
jj file chmod n <path> -r <id>          # Make normal (non-executable)

# Track and untrack files
jj file track <path>...                 # Track files when auto-track is disabled
jj file untrack <path>...               # Untrack files (retains file in working copy)
```

---

### Automated Bisection

`jj bisect run` uses binary search to pinpoint the commit that introduced a bug or fix.

```bash
# Bisect range running a test command
jj bisect run --range v1.0..main -- npm test
jj bisect run --range v1.0..main -- cargo test

# Bisect to find the first good revision instead of bad
jj bisect run --range v1.0..main --find-good -- pytest

# Run command with inline jj invocation (target commit ID is in $JJ_BISECT_TARGET)
jj bisect run --range v1.0..main -- bash -c 'cargo check'
```

- Exit code `0`: Good revision.
- Exit code `125`: Skip revision.
- Exit code `127`: Abort bisection (command not found).
- Any other non-zero exit code: Bad revision.

---

### Code Formatting & Fixing

`jj fix` runs configured external formatters (e.g. clang-format, black, prettier) and applies fixes across revisions without creating merge conflicts.

```bash
# Fix files in current mutable stack
jj fix

# Fix files in specific revisions and their descendants
jj fix -s <revset>

# Fix all lines instead of modified lines only
jj fix -a -s <revset>

# Include unchanged files
jj fix --include-unchanged-files
```

---

### Metadata Editing

`jj metaedit` modifies commit metadata without touching file contents.

```bash
# Update description without opening editor
jj metaedit -r <id> -m "new message"

# Generate a fresh change ID
jj metaedit -r <id> --update-change-id

# Update author to configured user / specific author
jj metaedit -r <id> --update-author
jj metaedit -r <id> --author "Name <email@example.com>"

# Update author timestamp
jj metaedit -r <id> --update-author-timestamp
jj metaedit -r <id> --author-timestamp "2025-01-01T00:00:00Z"

# Force commit rewrite to update committer signature/timestamp
jj metaedit -r <id> --force-rewrite
```

---

### Cryptographic Signatures

```bash
# Sign revision(s) using configured signing backend (GPG / SSH)
jj sign -r <id>
jj sign -r <id> --key <key-id>

# Drop cryptographic signature
jj unsign -r <id>
```

---

### Working with Remotes & Colocated Repos

#### Remote URLs & Repository Detection

```bash
# List remotes
jj git remote list

# Parse owner/repo from remote URL (for gh CLI)
jj git remote list | grep origin | head -1 | sed -E 's/.*github\.com[:/]([^/]+)\/([^/]+)\.git.*/\1\/\2/'
```

#### Remote Operations

```bash
# Fetch from all remotes or specific remote
jj git fetch
jj git fetch --remote origin

# Push bookmark (auto-tracks remote bookmark)
jj git push --bookmark <name>
jj git push --all

# Push specific revision to remote bookmark
jj git push --bookmark <name> -r <id>
```

#### Colocated Git Repos

In repositories where `.jj/` coexists with `.git/`:

- `jj git import`: Import Git branches/refs into jj.
- `jj git export`: Export jj bookmarks/commits into Git refs.

---

### Conflict Resolution

Conflicts in jj are first-class data stored directly in commits.

```bash
# List conflicts in revision
jj resolve --list -r <id>

# Launch external merge tool to resolve conflicts
jj resolve -r <id>

# Accept ours / theirs automatically
jj resolve --tool=:ours -r <id>
jj resolve --tool=:theirs -r <id>

# Surface conflicts between two heads by merging them into @
jj new @ <other-id>
```

---

### Recovery & Operation Log

The operation log records every mutating operation. Every recovery operation creates a new op.

```bash
# View operation history
jj op log
jj op log -n 10

# Inspect operation diff
jj op show <op-id>
jj op diff --op <op-id>

# Undo the last operation
jj undo

# Redo previously undone operation
jj redo

# Restore repository to the exact state at a past operation
jj --at-op=<op-id> log                  # Preview state at operation
jj op restore <op-id>                   # Restore entire repository

# Revert diff of a specific operation
jj op revert <op-id>

# Evolution log of a specific change ID across rewrites
jj evolog -r <id>
```

#### Content-Level Recovery vs Op Recovery

- **`jj restore`**: Copies file contents from one revision to another without rewriting history.
  ```bash
  jj restore                            # Discard working copy changes (from @-)
  jj restore <path>                     # Restore specific file
  jj restore --from <src> --to <dst>    # Copy file contents from src to dst
  jj restore --changes-in <id>          # Revert diff introduced by commit <id>
  ```
- **`jj revert -r <id> -d <dest>`**: Creates a new commit applying the inverse diff of revision `<id>`.

---

### Revset Syntax

```
# Operators
x-          # Parents of x
x+          # Children of x
::x         # Ancestors of x (inclusive)
x::         # Descendants of x (inclusive)
x..y        # Ancestors of y excluding ancestors of x (y & ~::x)
x & y       # Intersection
x | y       # Union
~x          # Complement (not in x)
x::y        # DAG range (descendants of x that are ancestors of y)

# Functions
mine()                  # Commits authored by you
bookmarks()             # All local bookmarks
remote_bookmarks()      # All remote bookmarks
tags()                  # All tags
mutable()               # All non-immutable commits
immutable_heads()       # Heads of immutable commit tree
author("pattern")       # Filter by author name/email
description("text")     # Filter by commit message text
files("path/**")        # Commits touching files matching pattern
empty()                 # Commits with no diff against parents
conflict()              # Commits containing unresolved conflicts
heads(x)                # Heads in revision set x
roots(x)                # Roots in revision set x
latest(x, [n])          # Latest n commits in set by committer date
reachable(src, domain)  # Commits reachable from src within domain
```

---

### Limiting Output & Templating

```bash
# Output limits
jj log -n 10                            # Limit number of commits (-n / --limit)
jj log --no-graph                       # Plain list without graph rendering
jj diff -s                              # File summary instead of full diff (-s / --summary)
jj diff --stat                          # Diff statistics

# Custom templates (-T / --template)
jj log -r @ -T 'description ++ "\n"'
jj log -T 'commit_id.short() ++ " " ++ description.first_line() ++ "\n"'
jj bookmark list -T 'name ++ " -> " ++ normal_target.change_id.short() ++ "\n"'
```

---

### Workspaces

Workspaces allow multiple working copies attached to the same jj repository.

```bash
# Add a new workspace at path
jj workspace add <path> [name]

# List active workspaces
jj workspace list

# Rename current workspace
jj workspace rename <new-name>

# Forget workspace (stop tracking working copy)
jj workspace forget [name]

# Update stale workspace after remote/concurrent operations
jj workspace update-stale

# Show workspace root directory
jj workspace root
```
