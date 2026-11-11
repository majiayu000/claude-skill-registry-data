---
name: north-star
description: |
  Capture an aspirational direction-setting thought as a north-star file at
  .claude/north-stars/<YYYY-MM-DD>-<slug>.md. North-stars are the
  WHAT-WE-WANT register; distinct from JOURNAL.md (lessons from what already
  happened) and contracts (concrete tasks). Read by data-architect Step 0.5
  on every /design-first and reviewed via /north-star-review to emit ranked
  suggestions of contracts that would move the codebase toward the aspiration.

  Use when: the user types `/north-star "<aspiration>"`, or says "capture
  this as a goal", "record this direction", "I want the system to eventually X",
  or describes a future-state intent that should influence design decisions
  beyond the current task.
user_invocable: true
---

# /north-star — Capture an aspirational direction

When invoked, create one new north-star file from the user's thought. The thought is the artifact — preserve the user's words; don't paraphrase.

## Step 0: Read the template

Read `.claude/templates/north-star.md` to confirm the exact section structure. The file has 7 required sections: Aspiration, Why this matters, Anti-patterns, Current gap (Claude-maintained), Suggested next steps (Claude-maintained), Related, Lifecycle footer.

## Step 1: Detect the project

Take the project name from the `project.name` slot of `.claude/project-profile.md`. If the profile is absent, fall back to the last path component of the repo root. Stop and ask the user via `AskUserQuestion` if the project is ambiguous.

If the project subfolder under `.claude/north-stars/` doesn't exist, create it later, inside the worktree from Step 3.5 — never in the starting tree.

## Step 2: Gather the thought

The user typed `/north-star "<aspiration>"` or pasted a longer paragraph after the slash command. Use that as the **Aspiration** section verbatim — do NOT compress or rephrase. The user's framing is the artifact.

If the user only gave a short phrase (< 15 words), ask one follow-up via `AskUserQuestion`:

> "Expand on the aspiration: a sentence or two on what it would look like when achieved, and why it matters."

Don't ask more — north-stars are low-friction by design.

## Step 3: Derive the title and slug

- **Title**: scannable one-liner derived from the aspiration. Examples: `Testing/eval/deploy pipeline is dynamic, user-friendly, production-ready`, `No local filesystem reliance`. Land it as the `# ` heading.
- **Slug**: kebab-case, ≤ 40 chars. Examples: `testing-model-production-ready`, `no-local-filesystem`. Must match the filename suffix.
- **Filename**: `<YYYY-MM-DD>-<slug>.md` at `.claude/north-stars/`.

## Step 3.5: Cut the workspace — a new worktree and branch from master

A north-star is its own deliverable, so it never lands in the tree the session happens to be standing on. This is the same isolation `/task` Step 5c gives a work item, reused for the one file this skill creates. Run it after the slug is fixed and after any hard refusal below has had its chance to stop the run, so a refused thought leaves nothing behind.

**Pre-flight.** Read the current branch in the starting tree (`git rev-parse --abbrev-ref HEAD` prints `HEAD` when detached). Also look for a rebase or merge in progress: `git rev-parse --git-path rebase-merge`, `git rev-parse --git-path rebase-apply` and `git rev-parse --git-path MERGE_HEAD` each name a path, and any of those paths existing means one is under way. A detached HEAD or either state halts here: tell the user to resolve it first and create nothing.

**The base is always freshly fetched `origin/master`** — never local `master` (routinely stale) and never the current `HEAD`. This holds even when the session is already inside another item's worktree, including when `/task` Step 3.5d invoked this skill. The north-star must merge on its own, not ride along with an unrelated item's commits.

Name the directory `<YYYYMMDD>-docs-north-star-<slug>` (date the worktree is cut, no separators) and the branch `docs/north-star-<slug>`. The slug is the one from Step 3.

**Anchor the path to the main checkout, as an absolute path.** A relative `.claude/worktrees/...` resolves against the current directory, so from inside an item's worktree the new tree would nest inside that item's tree. Removing the item's worktree later would then refuse or take the north-star tree with it, and the long nested path breaks SqlClient. Compute the anchor once and call the result `<wt>`:

```bash
MAIN="$(dirname "$(git rev-parse --path-format=absolute --git-common-dir)")"
WT="$MAIN/.claude/worktrees/<YYYYMMDD>-docs-north-star-<slug>"
```

```bash
git fetch origin master
git worktree add --no-track "$WT" -b docs/north-star-<slug> origin/master
```

`--no-track` matters: without it, branching from `origin/master` sets that ref as the upstream, and a later push would aim at master.

**Verify the base before writing anything.** Both SHAs must match, and the branch must be the new one:

```bash
git rev-parse origin/master
git -C "$WT" rev-parse HEAD
git -C "$WT" rev-parse --abbrev-ref HEAD
```

If the SHAs differ, remove the worktree with `git worktree remove` and redo it. Do not repair it with a rebase.

**Collisions halt.** If the directory or the local branch already exists, or `git ls-remote --heads origin docs/north-star-<slug>` prints a line (an earlier capture left it on the remote), stop and name it. Never overwrite, reuse or delete one that is already there; it may be another session's work. Ask the user whether to pick a different slug.

**Keep it out of the parent's status.** Confirm `.claude/worktrees/` is listed in `.gitignore`.

From here on, every path in Steps 4–7 is relative to `$WT`, not to the starting tree. Reading the active north-stars for the contradiction refusal below also uses `$WT`, which holds the master copy of the register. In particular the read-back in Step 7 reads the file from the worktree.

## Step 4: Author the Anti-patterns section

This is the load-bearing section — `contract-critic` checklist item 13 reads it to decide whether a future contract is in DIRECT CONTRADICTION with the aspiration.

Propose 3–6 anti-patterns based on the aspiration. Each anti-pattern MUST contain at least one **backticked snippet** (a code identifier, file path fragment, class name, or class-attribute string) that `north_star_review.py` can grep against the codebase. Examples:

- `New code that calls \`System.IO.File.WriteAllText\` against a path under the project repo`
- `A new feature that requires the operator user to author conditions in a frontend application root`
- `Hardcoding \`var(--mat-sys-primary)\` inside a \`style="..."\` attribute (already caught by architecture-guard, listed here for completeness)`

Anti-patterns without backticked snippets degrade to manual review only — they are still valid but don't surface gap signals.

Present the draft anti-patterns via `AskUserQuestion` and let the user refine.

## Step 5: Populate the Why this matters + Related sections

- **Why this matters**: one or two sentences. Concrete business value or UX improvement. NOT motivational filler.
- **Related**:
  - **Mechanisms**: cite slugs from `MECHANISMS.md` or the `MECHANISMS/*.md` domain files that this aspiration would extend or replace.
  - **Areas**: cite slugs from `.claude/area-mapping.json` that are implicated.
  - **Adjacent north-stars**: other thoughts in the same project that cluster with this one (siblings, the WHAT/HOW split, the precondition relationship).
  - **Lessons**: journal entries (`JOURNAL.md` or `JOURNAL/*.md`) whose `Apply when:` pattern matches this aspiration's anti-patterns.

## Step 6: Leave the Claude-maintained sections empty

The two Claude-maintained sections must be initialized as:

```
_Last updated: not yet reviewed_

- (to be populated by `/north-star-review`)
```

Do NOT pre-fill them. They are computed by `north_star_review.py` from the live codebase grep + cross-references.

## Step 7: Write the file and confirm

Use `Write` to create the file at `<worktree>/.claude/north-stars/<filename>` — the worktree from Step 3.5, never the starting tree. Then run a single read-back of that path to confirm the structure is intact. Tell the user:

> "Created `<filename>` in worktree `<worktree path>` on branch `docs/north-star-<slug>`, cut from `origin/master`. It becomes active and discoverable for every session once it merges. Nothing is committed or pushed yet: run `/ship` from that worktree (it commits, pushes and opens the draft pull request), then `/north-star-review` to populate the gap signal and concrete next-step suggestions. After the merge, data-architect reads the aspiration on every `/design-first`."

## What this skill does NOT do

- Does NOT populate Current gap / Suggested next steps — that's `north_star_review.py`'s job.
- Does NOT cross-reference against existing contracts — that's `north_star_review.py`'s job.
- Does NOT generate the first suggestions — same reason.
- Does NOT modify any other file. North-stars are append-only entries; new aspirations get new files.
- Does NOT commit, push or open a pull request. It stops after writing the file in its own worktree; `/ship` owns the rest.
- Does NOT write into the starting tree or reuse the current branch. The only thing it creates outside the new worktree is the worktree registration itself.

## Hard refusals

If the user provides an "aspiration" that is actually a concrete task (e.g. "Add a new endpoint that returns active strategies"), refuse:

> "That sounds like a concrete task, not an aspiration. Run `/design-first '<task>'` instead — north-stars are the long-horizon WHAT-WE-WANT register, not the short-horizon backlog."

If the user provides an "aspiration" that contradicts an already-active north-star:

> "There's an active north-star `<slug>` at `<path>` that says `<aspiration excerpt>`. Your new thought contradicts it. Choose: (a) refine the existing one in place, (b) supersede it (rename to `.superseded.md`, cite the new one as `Supersedes:`), or (c) clarify how both can be active simultaneously."
