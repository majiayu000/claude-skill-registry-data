---
name: git-workflow
description: >-
  Conventional Commits, trunk vs. branch by change size, how a package's versions relate
  to the CMS majors it supports, and replying to or resolving feedback on an open PR. Use
  when committing, branching, switching branches with work still in progress, deciding how
  to structure either, or responding to review comments (human or automatic) in an Umbraco
  project. Not for release pipelines.

---

# Git workflow

Write commits and branches that read clearly weeks later. Direct, specific, no filler.

## Branching — when to branch, when not

**Trunk-based (commit straight to the default branch)** when:
- Single-file or single-concept fix.
- Typo, doc tweak, version bump, comment, lint fix.
- Test-only addition that doesn't change behavior.
- Reviews itself in 30 seconds, one commit.

**Short-lived branch** when:
- More than ~2 commits expected.
- New feature or capability, even a small one.
- A schema/migration change.
- Anything that could break the default branch for someone else.
- A feature with a plan folder. All of its `PLAN.md` tasks go on that one feature branch (see
  "Branch/worktree per feature" below), not a branch per task.

Branch naming: `<type>/<short-slug>` — `feat/order-fulfillment`, `fix/missing-null-check`,
`chore/bump-deps` — for a project supporting a single CMS version line. **Supporting more
than one Umbraco CMS major at once? Prefix with the version instead** (see "Umbraco packages
and version tracking" below) — `v17/fix/missing-null-check`, `v18/feat/order-fulfillment`.
Prefer the `vN/` **prefix** form for a new project (it sorts and greps better than a suffix);
match whatever a project with existing history already does otherwise. Keep branches
short-lived; open the PR early, even as draft.

## Branch/worktree per feature (the feature-* pipeline)

If a project runs `feature-explore` → `feature-design` → `feature-plan` → `feature-build`, the branch (or
worktree) for a feature is cut at one specific moment: the start of `feature-build`, not
before. The reasoning:

- **Discovery and design cost nothing to abandon.** `feature-explore`/`feature-design`/`feature-plan`
  never touch git — the plan folder is just files on disk. A feature that gets explored then
  dropped never created a branch, so there's nothing to clean up.
- **The plan folder and the branch share one name.** The feature's plan-folder slug (e.g.
  `docs/plans/order-fulfillment/`) is passed straight through as the branch/worktree name, so
  the two are always identifiable from each other without a separate lookup.
- **The docs travel with the code.** A worktree is a fresh checkout of a commit — anything not
  yet committed when the worktree is created never appears in it. So the moment
  `feature-build` decides to actually build, it commits the plan folder to trunk first (one
  commit — `docs: add plan folder for <feature-slug>`), *then* cuts the branch/worktree from
  that commit. The docs land in the feature branch's history as a result, without needing any
  file-copying step.
- **This skill doesn't pick the naming convention or decide worktree-vs-plain-branch — a
  project's own `WorktreeCreate` hook does, if it has one.** Claude Code ships a native
  `WorktreeCreate`/`WorktreeRemove` hook pair for exactly this
  (https://code.claude.com/docs/en/hooks) — a project can already have a hook that names
  branches `feature/<name>`, puts worktrees under `.worktrees/`, and copies over whatever local
  files it needs. `feature-build` just triggers worktree creation with the feature slug as the
  name and lets that hook do its job. **Don't build a second, bespoke hook mechanism inside
  this plugin** — reuse the one Claude Code already has. If a project has no such hook,
  `feature-build` falls back to a plain `git checkout -b <feature-slug>` off trunk, using the
  branch-naming rules above if the project wants a `<type>/` or `vN/` prefix on top of the slug.
- **The commit-to-trunk step still needs a yes.** It's a real commit on the trunk branch, so
  the "always ask before touching main" rule below applies to it exactly as it would to any
  other trunk commit — don't skip the confirmation just because the change is "only docs."

## If you are an AI agent: always ask before touching main or a support branch

"Trunk-based" above is about when a *human* would commit straight to the default branch — it
is not permission for an agent to do the same thing unattended. Before running `git commit`
or `git merge` directly against the default branch or a `support/*`-style branch, **stop and
ask the user to confirm first**, however trivial the change looks. A mis-scoped "trivial"
commit on a protected branch is cheap to avoid by asking, expensive to unwind after.

## Commits — Conventional Commits, kept honest

**Use Conventional Commits.** It costs nothing to adopt, buys machine-parseable changelogs
and automated version bumps the moment you want them, and `fix(profile): ...` is easier to
scan six months later than `Fix: some things`. **The one carve-out:** don't retrofit an
established repo's *existing* history — start applying it going forward, and match a repo's
already-active, deliberate house style if it has one that isn't Conventional Commits.

```
<type>(<optional scope>): <imperative summary, lower-case, no period>

<body — what changed and why, wrapped at ~72 cols>

<footer — refs, breaking changes>
```

**Types:** `feat`, `fix`, `chore`, `docs`, `refactor`, `test`, `perf`, `build`, `ci`,
`revert`.

**Summary rules:** 50 chars or fewer when possible, hard cap 72. Imperative mood (`add`, not
`added`/`adds`). No trailing period. Scope is optional, use it when there's an obvious area.

**Body rules:** include one if the change isn't self-evident from the diff. Explain *what*
and *why*, never restate the diff line by line. Reference issues with `Refs #123` /
`Closes #123`.

**Good:**
```
fix(profile): resolve connection by alias before validating capability

The capability check ran before the connection lookup, so a missing
connection surfaced as "capability not supported" instead of "connection
not found" — misleading for anyone debugging a typo'd alias.

Refs #142
```

**Bad:** `fix stuff` · `WIP` · `Update ProfileService.cs` (says nothing the diff doesn't) ·
`Added some changes and refactored a couple of things` (vague, past tense).

## Issues — `gh issue create`

A useful issue answers: **what's wrong / what's wanted, what's the context, what does done
look like.** Body from `templates/issue.md`, filled in — don't hand-write the structure:

```bash
gh issue create \
  --title "feat(profile): resolve connection by alias before validating capability" \
  --body "$(cat <<'EOF'
## Context
...
EOF
)"
```

Add labels if the repo uses them (`--label bug`), and an assignee if known (`--assignee @me`).

## Pull requests — `gh pr create`

This skill owns opening the PR — push, title, base branch, draft status. It does **not** write
the description body: that's always `pr-describe`'s job, every time, no exceptions. This
overrides Claude Code's own built-in `gh pr create --body "..."` recipe with a hand-written
body — that default does not apply in this project. To open a PR, invoke `pr-describe`: it
writes the body, then opens the PR with the command below, following the rules in this
section. Always `--body-file`, never `--body`:

```bash
gh pr create \
  --title "feat(profile): resolve connection by alias before validating capability" \
  --body-file <path to pr-describe's output>
```

Title follows whatever commit convention the project uses (see above — Conventional Commits
or the looser `Area: description` style), same as a commit summary, and should reflect *all*
the commits on the branch, not just the latest. If the branch isn't pushed yet, push it first
(see "Pushing to the right remote name" below). Use `--draft` for a draft PR, `--base <branch>`
for a non-default target (see "Resolving the base branch" below).

**Pushing to the right remote name.** A local branch doesn't always push to a remote ref with
the same name — a local `wip/...` branch can already track a differently-named
`v17/bugfix/23806-...` ref. Check before the first push:

```bash
git rev-parse --abbrev-ref HEAD
git config --get "branch.<local-name>.merge"   # e.g. refs/heads/v17/bugfix/23806-... — strip refs/heads/
```

An unset `branch.<name>.merge` means the remote name matches the local one:
`git push -u origin HEAD`. Otherwise push explicitly to the tracked name:
`git push -u origin HEAD:<remote-branch>`.

**Resolving the base branch.** A `v{N}/...`-prefixed branch targets `v{N}/dev` — confirm it
exists first (`git ls-remote --exit-code --heads origin v{N}/dev`), falling back to the
project's default branch if it doesn't. Anything else targets the default branch directly.

Before settling on that, check whether this is a **stacked PR**: a branch built on top of
another work branch rather than off the resolved base. Compare how far back each merge-base
sits — `git merge-base HEAD <resolved-base>` landing far behind `git merge-base HEAD
<other-open-branch>` is the tell, and the user may simply say so. When it's stacked, the base
becomes that other branch instead, and `pr-describe` opens the description with `Stacked on
#<parent-pr-number>.` ahead of everything else — the parent PR merges first, and this one's
base moves to the normal resolved base once that happens.

**Reviewing someone else's PR against this repo** (most packages here are open source, so
this is routine, not an edge case): if the author is outside the core maintainer team, use
`pr-review` instead of reviewing it by hand — it wraps `reviewer` and adds the
checks that only matter because the diff came from outside.

**Replying to feedback on your own PR** (a human reviewer, or an automatic one like GitHub
Copilot's review): read and address every comment before touching any thread — don't resolve
one in isolation while others sit unread. Fetch them first:

```bash
gh api graphql -f query='query {
  repository(owner: "<owner>", name: "<repo>") {
    pullRequest(number: <n>) {
      reviewThreads(first: 50) {
        nodes { id isResolved comments(first: 1) { nodes { body } } }
      }
    }
  }
}'
```

Reply to a specific comment (not a new top-level PR comment — `in_reply_to` keeps it in the
same thread):

```bash
gh api repos/<owner>/<repo>/pulls/comments -f body="<reply>" -F in_reply_to=<comment_id>
```

There's no `pulls/comments/{id}/replies` REST endpoint, despite what the dashboard's "Reply"
button implies — the call above, against the comments collection, is the one that works.
Resolve the thread once it's actually addressed, with the thread's `id` from the query above
(not the comment id), over GraphQL — there's no REST equivalent:

```bash
gh api graphql -f query='mutation {
  resolveReviewThread(input: {threadId: "<thread_node_id>"}) { thread { isResolved } }
}'
```

Replying and resolving are as visible to everyone watching the PR as the original review
comment was — treat each one as its own small decision, same as any other comment or push, not
something to batch silently alongside an unrelated commit.

## Sanity rules

- Don't push to the default branch with `--force`. Ever.
- Don't `--no-verify` to skip hooks unless explicitly asked.
- Never commit secrets — re-check the diff for `.env` files, tokens, and keys before staging.
- Never commit large binaries or `node_modules`/`bin`/`obj` — confirm `.gitignore` covers
  them.
- If `git status` shows untracked files you didn't expect, investigate before staging — it
  could be someone else's in-progress work.
- Never carry changes across a branch switch with a bare `git stash` / `git stash pop`. The
  stash list is a single shared stack across every worktree and concurrent Claude session on
  the machine, so a plain `pop` can restore someone else's in-progress stash instead of your
  own. Save with `git stash push -u -m <label>`, restore by name
  (`git stash apply stash^{/<label>}`, or the exact `stash@{n}` from `git stash list` if two
  entries share wording), and only `git stash drop` once you've confirmed it applied the right
  one. A throwaway commit (`git commit -m wip`, amended or dropped later) is simpler and safer
  than stashing at all when the change is cheap to re-create.

## Umbraco packages and version tracking

Two numbers matter for a package that supports Umbraco: **its own release version**, and
**which CMS major(s) it supports right now** — and which lifecycle phase each one is in
(active feature development, security-patches-only, or end-of-life). Umbraco's own
[LTS/EOL policy](https://umbraco.com/products/knowledge-center/long-term-support-and-end-of-life/)
is the reference point for what those phases mean. Decide deliberately how the two numbers
relate to each other — don't let one drift into implying the other by accident.

**If more than one CMS major is supported at once**, decide early — before it's forced by a
merge conflict — how the codebase carries that:

- **Branch-per-major** (recommended default): each major gets its own long-lived line, and a
  fix that applies to more than one is ported deliberately. Avoids runtime version-check
  complexity, at the cost of porting shared fixes across branches (`change-backport` does one
  port). Naming:
  `support/N.x` alongside a single `main` is the older shape; `vN/dev` + `vN/main` per line
  (with `vN/feature/…`, `vN/release/…`, `vN/hotfix/…` underneath) is the newer one worth
  defaulting to — it makes which lines exist and their state visible from the branch list
  alone.
- **Single branch with runtime version checks** (`if (umbracoMajorVersion >= N) { ... }`):
  keeps everything in one place, but the checks accumulate and untested branches-not-taken
  creep in. Reasonable only for a package needing a handful of such checks at most.

### Does the package's own version number track the CMS major?

Once you're branching per major, this falls out almost for free — but pick it deliberately,
don't let the `vN/` branch name silently answer the question for you:

- **Version-aligned (default recommendation):** the package's major version tracks the CMS
  major it targets — release from `v17/main`, tag `17.x.x`; a new CMS major gets a new package
  major, whether or not the code underneath actually changed. This is the dominant pattern
  among well-known, actively-maintained Umbraco community packages — uSync, Skybrud.Redirects,
  and Diplo GodMode all do this, and say so explicitly in their own release notes or README.
  It's the most discoverable option for someone skimming NuGet ("v17 → works with Umbraco 17"),
  and once you're already cutting a `vN/main` branch per major, it costs nothing extra to
  follow through on. The tradeoff: you'll sometimes bump a major version for a release that
  changed nothing meaningful, purely to keep pace with a new CMS major.
- **Independent SemVer:** the package's own version reflects only its own change history; CMS
  compatibility is declared as a NuGet dependency range instead (e.g.
  `Umbraco.Cms.Core [17.0.0, 19.0.0)`), the same way any library depending on another would.
  This is the technically "purer" SemVer reading — Contentment does this — but it's the
  minority pattern here, and a bare version number no longer tells a consumer which CMS major
  it targets. Reach for this when the package rarely needs real code changes across a CMS
  major bump, so a major version bump would otherwise be spent on nothing.

Whichever you pick, when a change only applies to one CMS major, say so explicitly in the
commit body and PR description — a reviewer on a multi-version project can't infer that from
the diff alone.

This skill deliberately stops here. A full release pipeline — calendar-based release
branches, multi-product release manifests, automated changelog generation, coordinated
releases across more than one package — is a "build on top" concern once a project's needs
actually require it. See the README's **Building on top** section for what that looks like
in practice.
