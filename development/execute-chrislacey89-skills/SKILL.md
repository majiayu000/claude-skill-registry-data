---
name: execute
description: "Primary pipeline execution step after /prd-to-issues or for clearly scoped implementation work. Use to build, verify, and commit a concrete slice, delegating to /tdd for backend work and behavior-heavy frontend logic when red-green-refactor will reduce risk. Not for shaping or pre-merge review."
sources:
  secondary:
    - "The Checklist Manifesto — Atul Gawande"
    - "Extreme Programming Explained — Kent Beck"
    - "Continuous Delivery — Jez Humble & David Farley"
    - "The Twelve-Factor App — Adam Wiggins"
    - "Release It! — Michael Nygard"
    - "Growing Object-Oriented Software, Guided by Tests — Freeman & Pryce"
---

# Execute

Execute a complete unit of work: plan it, build it, verify the actual outcomes, commit it.

## Invocation Position

This is a primary pipeline skill used after `/prd-to-issues` has produced a concrete slice, or when the user already has a clearly scoped implementation task.

Use `/execute` when the work is ready to build, verify, and commit.

Use HITL `/execute` when the slice still needs active user judgment, supervision, or acceptance decisions during implementation. Use AFK `/execute` only when the next slice is already durable in GitHub, unblocked, and legible from its issue, boundary map, and any linked research artifact (archive file or spike issue) or `docs/solutions/` context.

Legible to a reader holding none of it — which is what an AFK iteration is. `/prd-to-issues` §4's context completeness check is the gate behind that condition: it requires every AFK slice to carry a `### Context` block, or explicit empty declarations, before the issue is filed. A slice marked AFK with no such block was never checked against this condition, only assumed to meet it. Treat that as a reason to run the slice HITL, or to send it back through `/prd-to-issues`, rather than as a formality to wave through.

See **Step 0: Prerequisites** below for the mandatory Ralph auto-detection and TDD marker gates.

Do not use it to replace `/shape`, `/research`, or `/write-a-prd` when the problem or shape is still unresolved. Do not use it as a substitute for `/pre-merge` once implementation is complete and ready for review.

## Workflow

### 0. Prerequisites

**Branch isolation gate.** Before any implementation work, ensure you are working on a clean branch created for this specific task — not a leftover feature branch from previous work.

**Isolation already provided — stand down (check this first, before the numbered rules).** Some environments hand the session a dedicated, isolated worktree+branch *before* `/execute` runs — Conductor workspaces, GitHub Codespaces, devcontainers, and similar hosts each provision "one workspace = one branch, auto-forked from the base," with setup scripts already run. When that is the case the pipeline does not own provisioning: creating a worktree here would nest one *inside* the host's, and the host's branch (named for the *workspace*, not the task) is not "stale." Read the environment's signal and cede the worktree to whoever already owns it (Norman — read the world's signifier instead of carrying an in-head assumption that the pipeline always provisions; Meadows — one actor per stock, so the pipeline *defers* rather than adding a competing manager).

Resolve the provisioning mode from `.claude/settings.json` `worktree.provisioning` — `"host" | "pipeline" | "auto"`, default `"auto"` when the key is absent (mirroring the existing `research.storage` precedent):

- **`host`** — isolation is host-owned. Stand down unconditionally.
- **`pipeline`** — the pipeline provisions. Skip this stand-down and run the numbered gate below.
- **`auto`** (default) — stand down if *either* signal fires:
  - a host environment variable describes *this* tree — the block below prints `host_owned=yes`. This is the cheapest, primary discriminator: the pipeline's only detection mechanism is Bash, and these vars are visible in the agent's shell. Presence alone is not enough: `CONDUCTOR_WORKSPACE_PATH` is inherited by any shell started under Conductor and can name a workspace of a different repository, so it counts only when it contains the current toplevel. (Do **not** detect via a `.conductor` directory in the cwd — Conductor keeps it under `$CONDUCTOR_ROOT_PATH`, not the workspace.)
  - the current working tree is not the repo's primary working tree — `git rev-parse --show-toplevel` differs from the first path in `git worktree list --porcelain`.

```bash
# host-signal: does a host env var describe THIS tree, not just this shell?
host_owned=no
top=$(cd "$(git rev-parse --show-toplevel)" && pwd -P)
if [ -n "${CONDUCTOR_WORKSPACE_PATH:-}" ]; then
  ws=$(cd "$CONDUCTOR_WORKSPACE_PATH" 2>/dev/null && pwd -P) || ws=
  if [ -n "$ws" ]; then
    case "$top/" in "$ws"/*) host_owned=yes ;; esac
  fi
fi
if [ -n "${CODESPACES:-}" ] || [ -n "${REMOTE_CONTAINERS:-}" ]; then host_owned=yes; fi
echo "host_owned=$host_owned"
```

`CODESPACES` and `REMOTE_CONTAINERS` carry no path to compare and are read for presence; they are container-scoped, so a shell that sees them is inside the container whose repos they describe. The same block appears in `/closeout`, `/lfg`, and `/init-pipeline`, byte-identical, pinned by `scripts/test-host-signal-containment.sh` in the pack's own repo.

When standing down: **skip worktree creation and `EnterWorktree`, and work in place on the current branch.** The numbered rules below are already satisfied — in particular **rule 3 does not apply** (a host-provisioned branch is neither base nor task-named, but it is not stale; do not nest a worktree and do not stop). The host has already seeded git-ignored config and dependencies, so most of the "Worktree setup checklist" is informational only — spot-check `.env.local`/deps if a command fails, but do not re-provision. **Its git-hooks item is the exception and still applies.** Hosts provision *tracked* files plus dependencies; git hooks live in `.git/hooks`, which is per-worktree and untracked, so a host-provisioned workspace characteristically has none. Check that item even when standing down. Continue to the issue-shape gate.

This stand-down is deliberately *asymmetric* with `/closeout`'s teardown check. Inflow only needs to answer *"am I already isolated?"* — generic detection (toplevel ≠ primary) and the env-var hint each settle that. The outflow question — *"who owns teardown?"* — is stricter and cannot rely on the generic heuristic alone, because a pipeline-made worktree also satisfies toplevel ≠ primary; `/closeout` keys off the explicit setting or host env var only.

1. Check the current branch: `git branch --show-current`
2. If the current branch is the base branch (e.g., `main`, `prod`, `master`), create a new feature branch for this task.
3. If the current branch is a **different feature branch** (not the base branch and not a branch named for this task), you are on a stale branch from previous work. Do not commit new work here. **Exception:** if the current branch is a sibling slice branch named in this task's `Consumes from #N` declaration, you are intentionally about to fork from it for a stacked-PR slice — proceed. **Exception (host-provisioned):** if the stand-down check above fired, this branch is the host's isolated workspace branch — it is not stale; work in place.

**To create an isolated branch**, use one of these approaches (in order of preference):

- **Worktrunk** (if `wt` is available): `wt switch --create <branch-name>` — creates a new worktree + branch from the appropriate base and switches to it, giving full filesystem isolation. Use the `/worktrunk` skill for guidance.
- **Plain git**: `git checkout <base> && git checkout -b <branch-name>` — creates a new branch from the appropriate base in the current working directory.

The **appropriate base** is the repo's own base branch by default — whatever the repo declares (`git symbolic-ref refs/remotes/origin/HEAD --short | sed 's@^origin/@@'`). Do not assume `main`. For a slice with an unmerged `Consumes from #N` dependency that produces symbols this slice imports, branch from that sibling slice's branch instead so the stacked PR can target the sibling's PR (Hammant *Trunk-Based Development* Ch. 13: multiple PRs per story; the sibling's PR must still merge to the repo's base branch within 2 days).

Derive the branch name from the task: e.g., `issue-5-landing-page`, `landing-page`, or the issue slug. Do not reuse branch names from previous work.

**Enter the worktree as a session (when you created a worktree).** Creating the worktree is not the same as the session *running inside* it — `wt switch --create` resets the shell cwd back to the project root after each command, so without a further step the session stays anchored at the original checkout and the reported cwd lies about where work is happening. After creating the worktree, enter it with the harness `EnterWorktree` tool so the session's working directory genuinely *is* the worktree:

- Call `EnterWorktree { path: <absolute-worktree-path> }`. The path must already appear in `git worktree list` for this repo (it will, because you just created it). This persistently switches the session into the worktree.
- Keep the creation step exactly as above — `wt switch --create` / `git worktree add` runs the worktrunk `pre-start` hooks that seed `.env.local` and dependencies. `EnterWorktree` only switches the cwd; it does not run those hooks. Create first (to seed env/deps), then enter.
- This puts the knowledge in the world, not the head: the cwd tells the truth about where edits and commits land (a watching operator can see it), and there is no per-command `cd` prefix to forget — eliminating the slip class where one un-prefixed command writes to the wrong tree.
- The **Plain git** option (`git checkout -b`, no worktree) creates the branch in the current checkout — there is no worktree to enter, so skip `EnterWorktree` and work in place.

**AFK / headless fallback.** If `EnterWorktree` is unavailable (headless runs, AFK Ralph, cron), fall back to cwd-prefix discipline: the shell cwd resets to the project root after every Bash command, so prefix every Bash call in this session with `cd <absolute-worktree-path> &&`. Use this only when the harness tool is genuinely unavailable — it is the old workaround, retained for environments without the native mechanism.

This worktree's teardown is owned by `/closeout` at the pipeline tail — after the PR merges, `/closeout` re-anchors the shell to the base checkout, removes the worktree, and prunes the merged branch. `/execute` is the inflow side of the worktree lifecycle; `/closeout` is the outflow. Step 6 cleanup below removes only the `.tdd-*` markers — it deliberately does not remove the worktree.

**After creating the worktree, set it up.** A new worktree inherits tracked files but not git-ignored ones (`.env.local`, per-worktree deps, build caches). Two paths:

**Preferred — configure once via worktrunk hooks** (`.config/wt.toml` in the project):

```toml
[pre-start]
copy = "wt step copy-ignored"
install = "pnpm install"
```

`pre-start` hooks are blocking — the worktree is not reported ready until they finish. Use `pre-start` (not `post-start`) for both, because `post-start` runs in the background and subsequent commands that need `.env.local` or `node_modules` will race the hook. See `/worktrunk` for the full recipe. One-time per project.

**Fallback — manual setup for plain `git worktree add`** (no worktrunk):

- `cp <source-repo>/.env.local <worktree>/.env.local` (and any other git-ignored config the project uses).
- Run the project's install command (`pnpm install`, `npm ci`, `pip install -r requirements.txt`, etc.) from the worktree.

**Worktree setup checklist (DO-CONFIRM — perform each step, then verify before proceeding).** Applies regardless of how the worktree was created:

- [ ] Git-ignored config copied — `.env.local` (and any other `.env.*`, `*.local`, or project-specific ignored config) exists in the worktree
- [ ] Dependencies installed — install command (`pnpm install`, `npm ci`, etc.) ran without error in the worktree
- [ ] Session is inside the worktree — `pwd` reports the worktree path because you entered it via `EnterWorktree { path }` (not the project root). In the AFK/headless fallback only, this item instead means the `cd <absolute-worktree-path> &&` prefix is being applied to every Bash call
- [ ] `$CLAUDE_PROJECT_DIR` scoping correct — if the project references this env var in scripts, verify it resolves to the worktree path, not the primary repo
- [ ] **Local git hooks are installed and their manager is on `PATH`** — `ls "$(git rev-parse --git-dir)/hooks/" | grep -v '\.sample$'` lists something, and the manager the repo declares (`lefthook`, `husky`, `pre-commit`, …) resolves. Hooks live in `.git/hooks`, which is **per-worktree and untracked**, so a fresh worktree inherits none of them — and the failure is silent in the worst direction: every commit succeeds, and every guarantee the repo documents at commit time simply did not run. If the manager is absent, either install it (`lefthook install`) or record in the Step 6 review notes that local gates were inactive for this branch, so nobody reads a green local run as the merge gate
- [ ] Classification marker absent — `.claude/.tdd-active`, `.claude/.tdd-skipped`, and `.claude/.lfg-active` do not exist in the worktree (fresh slate; Step 3 creates one)
- [ ] **Post-review lock flags absent** — `.claude/.review-stamped` and `.claude/.fix-findings-active` do not exist. Both belong to the *previous* branch's review: `/pre-merge` Phase 4 writes the first, `/fix-findings` writes the second, and `/closeout` and `/fix-findings` respectively remove them at the end of that branch. A leaked `.review-stamped` refuses every implementation write on this slice before it starts; a leaked `.fix-findings-active` holds the lock open for the whole slice, which is the silent direction. Delete either one you find — you are at the start of a branch that has had no review, so neither can be describing this one

**Issue-shape detection gate.** If the task is a GitHub issue, verify it is a slice (implementation-ready), not an undecomposed PRD. Run `gh issue view <n> --comments` and check for a comment matching `^Decomposed into: #\d+`.

- If such a comment exists: proceed. The PRD has been decomposed; the operator is presumably working on one of its child slices (and should have supplied that slice's number, not the PRD's).
- If no such comment exists AND the issue body contains shaped-pitch markers (sections named `Appetite`, `Rabbit Holes`, `No-gos`, `User Stories`, or `Implementation Decisions`): halt. This is an undecomposed PRD. Invoke `/prd-to-issues <this-issue-number>` to produce implementation-ready slices, then restart `/execute` against one of the child slice issues.
- If multiple `Decomposed into:` comments exist, read the most recent; `/prd-to-issues` is responsible for ensuring only one is authoritative.

Skip this gate for one-off tasks not tied to a GitHub issue.

**Blocked-slice gate.** Still on the issue, confirm the slice is actually takeable before implementing it. Read the edges themselves rather than a summary count, which can be served stale right after a mutation:

```bash
gh issue view <n> --json blockedBy \
  --jq '{open_blockers: [.blockedBy.nodes[] | select(.state == "OPEN") | {number, title}],
         ever_wired: .blockedBy.totalCount}'
```

`open_blockers` empty means takeable — proceed. Any open blocker means **stop**: name the blocking issues to the user and let them decide whether to work the blocker first, or to override because the dependency is stale or irrelevant to this slice. Do not start implementing and discover the gap halfway in.

**Read `ever_wired` before trusting an empty list.** Empty has two causes: the slice genuinely has no open blockers, or the repo predates the edge wiring in `/prd-to-issues` §7 and has no edges at all. `totalCount` counts blockers in every state, so it separates them — `ever_wired > 0` means this slice *was* wired and its blockers have since closed, so the empty list is real. `ever_wired == 0` means no edge was ever written and the empty list proves nothing; if the issue body carries a prose `Blocked by #N` line, trust the prose and check those blockers' state by hand.

Note `state` here is the GraphQL enum — uppercase `OPEN`, not the REST endpoint's lowercase `open`.

Skip this gate for one-off tasks not tied to a GitHub issue.

**Ralph auto-detection gate.** Evaluate all three conditions:

- [ ] The task comes from a GitHub issue (not a one-off verbal request)
- [ ] The issue has multi-slice scope (PRD, big-batch appetite, or multiple user stories)
- [ ] No `ralph-once.sh` or `ralph.sh` exists in the repo root

If all three are true, invoke `/setup-ralph-loop` now. Do not proceed to Step 1 until Ralph setup is complete or the conditions are not met.

**Pipeline hooks gate.** The hook file existing is not the same as the hook carrying the post-review edit lock, and this gate tests both. A project that ran `/init-pipeline` before the post-review edit lock shipped carries a hook that never reads `.claude/.review-stamped`: the lock is inert there, and a `/fix-findings` fixer holding `.claude/.fix-findings-active` is refused anyway — by the classification clause, under a message that names `/tdd` and never names the route the fixer is standing on. Both halves fail silently, which is why an existence-only check is not enough: an inert lock looks from the outside exactly like a branch nobody edited after review.

```bash
HOOK="${CLAUDE_PROJECT_DIR:-$(git rev-parse --show-toplevel)}/.claude/hooks/enforce-classification.sh"
# Every path the hook's own clause 1 tests. A path missing from this list is a
# boundary this gate cannot see, so an install predating it reports current
# forever. scripts/test-lfg-marker.sh section 7 pins this list against that
# clause; add a path here in the commit that adds it there, or the suite fails.
GATE_TERMS=".claude/.review-stamped .claude/.tdd-active .claude/.tdd-skipped .claude/.lfg-active"
if [ ! -f "$HOOK" ]; then
  echo "hooks-absent"
else
  missing=""
  for term in $GATE_TERMS; do
    grep -qF -- "$term" "$HOOK" || missing="$missing $term"
  done
  if [ -n "$missing" ]; then
    echo "hooks-stale"
    echo "missing:$missing" >&2
  else
    echo "hooks-lock-present"
  fi
fi
```

`hooks-absent` and `hooks-stale` both mean **invoke `/init-pipeline` now**, and do not proceed to Step 1 until it reports. The first scaffolds enforcement hooks into a project that has none. The second re-scaffolds § 2's hook body over an existing install and re-runs § 6's `.gitignore` append, which that install never ran for the lock's two flags — without it both land as untracked files that can be committed, holding the lock shut or open across every future branch in that repo. `/init-pipeline` § 2 carries an existing `IMPL_PATTERNS` line through a re-scaffold rather than re-asking, so an upgrade does not reset a trigger surface the project customized. `hooks-lock-present` proceeds.

**What this gate cannot see, since its third verdict would otherwise read as a claim it does not make.** It greps for every path the hook's own clause 1 tests, so it recognizes one version boundary per path and reports which side of each an install is on. That is sound in one direction only. A hook missing any of those terms provably predates it, so `hooks-stale` is right whenever it fires; but once a project has been upgraded the terms are there forever, so a *later* change to `/init-pipeline` § 2's hook body that adds no new path — a reordering, a rewritten refusal message, a fix to a clause's logic — still reports `hooks-lock-present` and is never distributed by this gate. The third verdict is therefore named for the terms it found rather than for currency, which the check cannot establish.

`GATE_TERMS` is the whole of that claim, and `scripts/test-lfg-marker.sh` section 7 pins it against the hook's clause 1, so a marker added to the hook and not to this list fails the suite in the commit that adds it. That replaces the rule this paragraph used to state in prose — *give the boundary its own term, in the commit that introduces it* — which #370 read and did not follow, shipping `.claude/.lfg-active` with no distribution term and leaving it inert in every project installed before it (#385). A distribution boundary that is not a new path still has no mechanism, and still owns its own distribution.

**TDD classification gate.** Step 3 requires classifying the work before writing any code. `/tdd` automatically creates `.claude/.tdd-active` via harness preprocessing when loaded (not LLM-dependent); visual frontend creates `.claude/.tdd-skipped`; `/lfg` creates `.claude/.lfg-active`. A PreToolUse hook blocks all `.ts` file writes unless one of these markers exists. Step 6 removes every one of them after commit.

**Trivial-task exception.** A single-commit cleanup unrelated to active feature work may skip classification by creating `.claude/.tdd-skipped` directly. The four conditions that all have to hold, and what to do when one does not, are stated once in [references/trivial-task-rule.md](references/trivial-task-rule.md).

**Assumptions validation gate.** If the task is a GitHub issue with an "Assumptions from Parent PRD" section, spend 60 seconds checking each listed assumption against current reality before proceeding. For each:

- Is the external service still available at the expected API and pricing tier?
- Does the parent PRD's approach still hold given what you now know?
- Are the packages this slice depends on still at compatible versions *and entrypoints*? A subpath swap (e.g. `pkg` → `pkg/http`, or any `pkg/<sub>` → `pkg/<other-sub>`) for a multi-runtime package is a runtime-affecting change disguised as a type-only diff — treat it as an assumption shift, not a free-pass type-equivalent edit.

If all assumptions still hold, proceed to Step 1. If any assumption has changed, stop and flag it to the user — this slice needs a targeted `/research` + mini-PRD cycle before execution, not a patch during implementation. Do not proceed with stale assumptions and attempt to work around them mid-execution.

Skip this gate entirely for one-off tasks without an "Assumptions from Parent PRD" section.

**Un-discharged feasibility check (advisory).** If the task's research artifact (archive file or spike issue) still carries `Uncertain` or `Speculative` assumptions whose verdicts are cheaply settled by 10 lines of throwaway code — does the library actually expose this, does the streaming path emit partial tags, does this format render where we need it — surface them now and suggest `/prototype` FEASIBILITY before main implementation. This is advisory, not blocking (per XP's *slack* principle); the user may have a reason to proceed and discover the answer mid-implementation. But the cost asymmetry is real (XP's *Defect Cost Increase*): a spike at this moment costs minutes, while the same assumption discovered mid-implementation costs hours of pivot. State the un-discharged assumptions explicitly and let the user decide. Skip this check for one-off tasks without a research artifact or when every assumption is already tagged `Verified` / `Refuted`.

**Consumes verification gate.** Only for issue-based slice work. If the task comes from a GitHub issue created by `/prd-to-issues`, and its `## Boundary Map` / `### Consumes` section references an already-closed upstream slice, spend 60 seconds verifying each listed symbol exists at the declared path in the current tree. This catches upstream boundary-map drift before implementation starts.

For each Consumes entry:

1. If it names a file path — check the file exists.
2. If it names a function, type, or exported symbol — grep for the export.
3. If it names a shape (e.g. "Effect Layer", "Zod schema", "React component", "Context provider") — confirm the *shape* matches, not just the name. A pure helper function does not satisfy a claim of "Effect Layer." A plain object does not satisfy a claim of "Zod schema."
4. If the Consumes entry names a typed symbol from a sibling slice (per `/prd-to-issues` Boundary Map guidance), confirm the consumer code derives its input type from the producer via `import type` (or the language's equivalent) rather than re-declaring the shape. A local re-declaration that happens to match the producer is a DRY violation that will silently drift when the producer evolves; the typed import is the structural fix that makes that drift class impossible.

If any Consumes symbol is missing or wrong-shaped, **stop**. The upstream boundary map is stale. Choose one of:

1. **Expand scope in this slice** to fill the gap. Note the expansion in the first commit's message, in the PR description, and file a post-hoc correction comment on the upstream closed issue so future slices don't trust the stale claim.
2. **Backtrack via `/correct-course`** to update the upstream boundary map and reshape the affected slices.
3. **File a new slice** for the missing work and block this one on it.

Do not silently absorb the gap — leave a breadcrumb for the next slice.

Skip this gate for one-off tasks, sibling slices still being planned, or issues without upstream `Consumes` entries.

This gate is scoped to intra-repo symbols (paths, exports, shapes). The mirror check for *externally-resolvable* declarations — package names, public API symbols, and pinned versions against the research snapshot — runs at `/pre-merge`'s Boundary Map Contracts dimension under "Spec-reality check." Step 0 sees the registry at slice-start; `/pre-merge` sees it at merge time. Both windows are intentional; do not widen this gate to duplicate the review-time check.

### 1. Understand the Task

Read any referenced plan, PRD, or GitHub issue. Explore the codebase to understand the relevant files, patterns, and conventions. If the task is ambiguous, ask the user to clarify scope before proceeding.

**Read the issue comment thread (issue-based work only).** When the task is a GitHub issue, read its comment thread before implementing — do not stop at the body. Step 0's issue-shape detection gate already ran `gh issue view <n> --comments`, so the thread is in context; reuse it rather than re-fetching. The comments are where the pipeline's continuation state lives: prior-iteration handoff notes (what was done, what remains, the exact error output a previous context window hit), plateau-stop notes naming what did *not* advance, post-hoc correction comments filed against this issue when an upstream boundary map drifted, and explicit human scope changes added after the issue was authored. In AFK Ralph loops this is load-bearing — iteration N+1 is designed to continue from what iteration N wrote into the thread, so skipping it re-derives or repeats work the previous iteration already explained.

**Precedence rule.** The issue body remains the durable contract. Comments augment it; they do not silently override it. A comment is an authoritative addition only when it is (a) a pipeline-authored continuation or correction comment, or (b) an explicit human scope change. Freeform discussion is context, never an override. If a comment appears to contradict the body on scope, and it is not a clear pipeline-authored correction or human scope change, flag the conflict to the user rather than acting on the comment.

**Disposal rule.** Classifying a comment is not the whole job — decide what happens to the part of the thread the body does *not* cover. This applies when this slice's PR will close the issue (`Closes #N`). The body is this pipeline's baseline: acceptance criteria live there, `/prd-to-issues` decomposes bodies, `Closes #N` closes on a body's terms. A capability that stays in a comment is outside every one of those mechanisms, so the close silently discards it — and the loss emits no signal, because the issue closes green and the PR merges clean.

The discriminator is a single test, and it is **not** "is the idea good": **can you name the consumer?** If you can point at the issue, slice, PRD, or shipped code that would use the capability, it qualifies. If you cannot — a design musing, a "we might want," an approach the author was thinking aloud about with no identified caller — it does **not** qualify and must not be promoted; promoting it manufactures scope and invents dependencies. When in doubt, it does not qualify.

For a comment that does qualify, surface it to the user before finishing the slice and offer the two disposals:

1. **Promote it into the body** — add it to this issue's acceptance criteria and build it in this slice, when it is genuinely the same seam and the appetite absorbs it.
2. **File its own issue** with a `Blocks #N` link naming the consumer you identified — when it is real work that belongs elsewhere.

Either one gives the capability an owner that survives the close. Do not silently absorb it, do not widen scope unilaterally, and do not implement it just because you noticed it — the choice is the user's. On AFK runs there is no user to ask, so default to filing the follow-up issue with the `Blocks #N` link; promotion into the body widens the slice without approval.

Skip this read — and the disposal rule with it — for one-off tasks not tied to a GitHub issue (the same scope guard Step 0 uses).

**Read the research artifact for this feature.** The PRD's "Research Reference" section names where it lives — one of two locations depending on the project's `research.storage` mode:

1. **Spike-issue mode** — the PRD references a closed `research`-labeled GitHub issue (`Refs #<spike-issue-number>`). Read it with:
   ```bash
   gh issue view <spike-issue-number>
   ```
   This works on any machine — fresh clones, CI sandboxes, recovered laptops, or contributor environments.

2. **Archive mode** (default) — the PRD references `~/.claude/research/<repo-slug>/<feature-slug>-<YYYY-MM-DD>.md`. Read the file directly. If you are running on a machine other than the one that produced the research, the file will not exist; flag this to the user and either re-run `/research` or proceed with explicit acknowledgment of the missing context.

Some legacy PRDs may still reference `research.md` in the repo root or `plans/` — read it if present. Whatever the location, the research artifact contains cached technical research that should inform your approach. Do not re-research what has already been decided.

**Read the slice's `### Context` block before the grep below (issue-based work only).** When the slice issue's `## Boundary Map` carries a `### Context` subsection, read its anchors, gotchas, and research pointer *first*. `/prd-to-issues` wrote that block so this session would not have to re-derive it: the anchors name the existing files to read or imitate, and the research pointer goes straight to the artifact instead of walking the parent PRD to find it. Reading it is not optional — a block that is written and never preferentially read is not neutral overhead, it is a section readers learn to skip, which taxes the Boundary Map around it.

Treat it as pointers, not truth. The anchors were written at decomposition time and siblings may have merged since; the code and the research artifact still win on any conflict, per the precedence rule below. A stale anchor is a correction to file on the issue, not a reason to skip the block.

Consult `docs/solutions/` for relevant past solutions before starting implementation:

```bash
grep -rl "relevant-keyword" docs/solutions/ 2>/dev/null
```

If past solutions exist for this problem domain, incorporate their lessons and avoid their documented pitfalls.

**Artifact precedence:** When the research artifact and `docs/solutions/` give conflicting guidance, follow the research artifact — it was verified against the current installed versions. Storage location does not affect trust: a spike issue and an archive entry carry equivalent authority. If the conflict is significant enough that you are uncertain, flag it to the user before proceeding. Load `docs/solutions/` selectively: grep for relevant keywords first, then read only matching files.

### 2. Plan the Implementation (optional)

If the task has not already been planned, create a plan for it. If the GitHub issue includes boundary maps (Produces/Consumes sections), use them to understand the interfaces you need to implement or code against.

### Stack-Specific References

Before implementing, check the project's stack and load relevant best practices.

- **Next.js / React projects**: If `package.json` includes `next` or `react`, load these skills before writing code:
  - `/vercel-react-best-practices` — performance optimization and React Server Component guidance
  - `/vercel-composition-patterns` — component composition patterns that scale without prop sprawl
  - `/next-best-practices` — file conventions, data patterns, metadata, and error handling
  - `/next-cache-components` — cache components, `use cache`, `cacheLife`, and `cacheTag`

### 3. Implement

**STOP — classify before writing any code:**

- [ ] **Backend code** → invoke `/tdd` now (creates `.claude/.tdd-active`)
- [ ] **Behavior-heavy frontend** (reducers, state machines, validation, accessibility, interaction regressions) → invoke `/tdd` now (creates `.claude/.tdd-active`)
- [ ] **Visual/layout/styling/copy frontend** → run: `mkdir -p .claude && touch .claude/.tdd-skipped`

A PreToolUse hook blocks all `.ts` file writes unless one of these markers exists. Do not write implementation code until you have classified the work.

If `/tdd` is not available, follow this minimum discipline:

1. Write a single failing test for the smallest vertical slice of behavior
2. Run the test — confirm it fails (red)
3. Write the minimum code to make it pass (green)
4. Repeat from step 1 for the next slice of behavior
5. Refactor if needed while keeping tests green

Do not write all tests upfront — write one, make it pass, then move to the next.

**[TypeScript projects] Library callback returns.** When a logical unit implements a callback the library asks the application to provide (agent hooks, middleware, proxy, tool handlers, render props, lifecycle methods), anchor the returned value to the library's declared return type with `satisfies LibraryReturnType`, a fresh object literal, or a derived type (`ReturnType<typeof …>`). Never return a typed local variable — TypeScript's excess-property check does not run on returns of typed values, so fields the library's signature does not declare are silently dropped at runtime. See `/tdd` Refactor step for the full rationale; if the research artifact (archive file or spike issue) carries a Library Callback Contracts snapshot (`/research` Phase 1.25), use its accepted-fields list as the pinned source.

**Comment the code, not the incident.** A comment you write here carries the *current* why — what this code does, and why it is shaped this way. The incident that led you here goes to the commit message and the PR body instead: what the prior behavior was, which earlier attempt this supersedes, what you rejected on the way. Before committing a unit, reread the comments you added to it and move any sentence that explains history rather than code. **Write the comment to the next person who edits this file, never to the reviewer of this diff.** A sentence that answers an objection the review might raise — why this and not the adapter, that the component is the real shipped one, that the parallel path is deliberate — is addressed to the reviewer, and it goes in the PR body with the rest of the review-facing account. The tell is emphasis: a capitalized REAL, SAME, or DELIBERATE is a comment arguing with someone who is not the file's next editor. Say each thing once: a comment that repeats a sentence already in the file, or already on the declaration beside it, is the copy to delete.

#### Commit after each logical unit

Do not accumulate all changes into one commit. Commit after each self-contained unit of progress. A logical unit is the smallest change that leaves the codebase in a working state — typecheck passes, tests pass, nothing is half-wired. Examples:

- One red-green-refactor TDD cycle (test + implementation for one behavior)
- A new module, type, or schema with its tests
- A wiring change (route registration, dependency injection, config)
- A refactor that improves structure without changing behavior
- A migration or seed file
- A cross-file type or interface refactor whose intermediate per-file steps would leave typecheck broken — the whole ripple is one logical unit

After completing each logical unit:

1. Run `pnpm run typecheck` and `pnpm run test` (or the project's equivalent). Fix any failures before committing.
2. Stage only the files for that unit — do not stage unrelated changes.
3. Commit with a message that says what this unit accomplished, not "WIP" or "progress". When the unit corrects earlier behavior, write the incident history the paragraph above routes here — and put it in the PR body as well, not the commit message alone. A squash merge collapses these per-unit messages into one, and `/closeout` treats squash as the common convention, so the commit message alone is not a durable destination. The PR body is the copy that survives intact for a reader running `git blame` months later.

If a unit touches both a test and its implementation, they belong in the same commit. If a refactor was triggered by the unit but is conceptually separate, commit the refactor separately.

### 4. Verify

**"All steps done" is NOT verification. Check the actual outcomes.**

By this point, each logical unit has already been committed with passing typecheck and tests. Step 4 is the full-slice verification pass — confirming the whole feature works end-to-end, not just that individual units pass.

Run the full feedback loops one final time:

```
pnpm run typecheck
pnpm run test
```

Fix any issues. If fixes are needed, commit them as a separate commit (e.g., "fix integration between X and Y").

Then apply the verification ladder — use the strongest tier you can reach:

#### Tier 1: Static Verification
- Files that should exist actually exist
- Exports are present (not just declared but actually exported)
- Imports between modules are wired correctly (not importing from a path that doesn't resolve)
- Implementation is substantive (not stubs, not console.log placeholders, not TODO comments where real code should be)

**Deletion Completeness (when this slice's diff deletes or renames a module).** Read the trigger off the diff, which you already have, rather than off a section header nothing in the pipeline writes:

```bash
BASE_BRANCH=$(git symbolic-ref refs/remotes/origin/HEAD --short 2>/dev/null | sed 's@^origin/@@')
if [ -z "$BASE_BRANCH" ]; then
  for candidate in main master prod develop trunk; do
    if git rev-parse --verify "$candidate" >/dev/null 2>&1; then BASE_BRANCH=$candidate; break; fi
  done
fi
# A name is not a ref. $BASE_BRANCH names the branch (for `--base`, `git switch`);
# $BASE_REF points at it, and is the only thing safe as a range endpoint.
if git rev-parse --verify "origin/$BASE_BRANCH" >/dev/null 2>&1; then
  BASE_REF="origin/$BASE_BRANCH"
else
  BASE_REF="$BASE_BRANCH"
  echo "note: origin/$BASE_BRANCH does not resolve — measuring against the local branch, which may be stale" >&2
fi
git diff --diff-filter=DR --name-status "$BASE_REF...HEAD"
```

**Residual:** `$BASE_REF` is only as fresh as the last `git fetch`, and on a triangular fork (or a remote not named `origin`) `origin/$BASE_BRANCH` may be absent or track your fork rather than upstream — the `else` branch then falls back to the local branch, which is the stale-ref behavior this guard exists to avoid. It says so on stderr rather than falling back silently, because a plausible wrong answer with no signal is what let this defect live for five months. If the counts look wrong, `git fetch` and re-run, or set `BASE_REF` by hand.

Deleted paths print as `D<TAB><path>`, renames as `R<score><TAB><old><TAB><new>`. Any output at all fires the rung; empty output skips it. Gate on the output, not the exit status — the command exits 0 either way. A `### Deletes` section in the slice body is an optional hint that names which surfaces to sweep; it is not the trigger.

For each deleted or renamed module, enumerate its external consumer surfaces — the symbolic names callers were taught to emit for it to consume, beyond its exports. Typical surfaces:

- DOM data-attributes the module read (`data-*`)
- CSS class names and selectors the module applied or queried
- Global or custom event names (`addEventListener('foo-bar')`, `dispatchEvent(new CustomEvent('foo-bar'))`)
- `window`, `localStorage`, or `sessionStorage` keys
- Route names, config keys, or feature-flag names the module owned

Infer surfaces from the module body as it existed before deletion (`git show <base>:<path>`, or the `Deletes` hint notes when the slice body happens to carry them). Grep the merged tree for each surface across every source-text file type the project uses — templates, source code, styles, config, docs. Do not restrict to a fixed extension list; the relevant surfaces depend on the stack (`.py`/`.rb`/`.go`/`.rs` for imports, `.vue`/`.svelte`/`.astro`/`.tsx` for templates, `.css`/`.scss`/`.sass`/`.less`/`.styl` for styles, `.yml`/`.toml`/`.json` for config, `.md`/`.mdx` for docs that ship). Zero matches required to pass. Non-zero matches: restore the module, migrate the consumers, or declare them as intentionally inert and track the cleanup as a follow-up slice. Imports alone are the narrowest possible definition of "consumer"; the surface may be wider.

**Upstream shape sweep.** After the consumer-surface sweep above, list each export touched on a shared module in this slice (context fields, builder return-type fields, interface or type members, schema fields, exported map or record entries). For each such export, grep the post-delete tree for non-self-reference reads. Zero matches required to pass. Non-zero matches: confirm the readers are live and intentional. Zero matches: drop the export in the same PR — the migration window closes the moment the legacy consumer is deleted, and a retained-but-unread export widens the import contract so a future cleanup becomes a breaking change rather than a silent removal. Dead-export linters (`knip`, `ts-prune`, TypeScript `noUnusedLocals`) cover many shapes of this but not exported context, interface, or schema fields — those are read by the type itself and look live to the tool, so the targeted post-delete grep is doing work the linter cannot.

#### Tier 2: Command Verification
- Tests pass (not just "no test failures" — confirm tests actually exist and ran)
- Test wall-clock duration didn't unexpectedly jump. A sudden multi-second increase in a previously fast test, especially after adding retry, sleep, backoff, or interval code, signals a real-time primitive was introduced without being injected. See `/tdd` § Timing-coupled primitives. Fix via injection, not `testTimeout` bumps.
- Build succeeds
- Lint is clean
- Any command the diff documents — a CLI the feature exposes, or a command block a reader is expected to copy and run — was actually invoked, not written from memory

#### Tier 2.5: Runtime Startup Verification
**Mandatory when the slice touches schema, migrations, environment config, server initialization, or new routes. Skip only for pure-logic changes to existing modules where nothing about app startup changed.**

- Database is ready: run pending migrations or `db:push` — do not assume the dev database has the latest schema just because tests passed (tests often use in-memory databases that run their own migrations)
- Dev server starts from cold without errors: `pnpm run dev` (or equivalent) boots and responds, not just builds
- The new or changed routes load without 500 errors: `curl -s -o /dev/null -w '%{http_code}' http://localhost:<port>/` returns 200
- Required environment variables are present and valid (check `.env.local` or equivalent)
- No unhandled errors in the server console output during startup

If you cannot start the dev server (e.g., missing external services), note which checks you skipped and why in **both** the Step 5 checklist and the Step 6 review notes. The checklist reaches the user; the review notes reach the reviewer. Sending the note only to the checklist means it dies there on any run that never presents one — which is every AFK run — and skipped verification invisible to review is the exact gap this tier exists to close.

#### Tier 2.6: Non-Dry Path Sanity Check (CLI + orchestration slices only)

**Mandatory when the slice ships a CLI, scheduled job, cron worker, or orchestration entrypoint that has a dry-run or preview mode.**

Dry-run success does not imply real-run success. A dry-run can short-circuit before storage or side-effects and hide placeholder functions wired into the production path.

For each function wired as a default in the production code path (layer construction, DI container, config object, CLI flag handler), check:

1. Is the function named, documented, or commented as a placeholder, stub, TODO, or follow-up?
2. If yes, is it either (a) guarded by a fail-fast check that throws in non-dry mode, or (b) bound only to the dry-run code path?

If any placeholder is wired as the default for a non-dry path without a fail-fast guard, **flag it now**. Options:

- Add a runtime guard: `if (!process.env.ALLOW_PLACEHOLDER) throw new Error(...)` or equivalent
- Bind the stub only when `dryRun === true` and require a real implementation for the non-dry path
- Gate the slice on the real implementation (larger scope but eliminates the silent-degradation window entirely)

This is a silent-degradation check: if an operator ran this without `--dry-run`, would the output be real, or would placeholder data flow through the production path?

#### Tier 2.7: Production-Runtime Parity (deploy-runtime ≠ test-runtime slices only)

**Conditional — never universal. This rung fires only when at least one of the following holds, and is skipped entirely otherwise. A slice whose tests run in the same runtime it deploys to (most Node-to-Node and Node-to-Vercel work) never sees it.**

- The slice's deploy runtime differs from its test runtime — e.g. workerd vs miniflare/Node, a real browser vs jsdom, an edge/Lambda runtime vs the local dev server.
- The slice ships published or static assets whose paths resolve at **deploy** time — absolute-path `<link>`/`<script>`/`<img>` references, a publish/copy step, a CDN or worker public root.
- The platform imposes a limit the test runtime does not enforce — crypto iteration caps, request/response size, CPU/time budgets, bundle size, or APIs present in the test runtime but absent in production.

**Why this rung exists — and why it is a feedback loop, not an inspection layer.** Green tests certify behavior in the environment the *tests* model, not the one the code *deploys* to. When the test runtime is more permissive than the deploy runtime, or a seam is mocked away from the real artifact, "tests pass" is not evidence of "works in production." This is the dev/prod parity gap (Twelve-Factor Factor X: keep the dev↔prod gap small along the *tools* dimension) and the missing automated feedback loop that Continuous Delivery closes with a smoke test against a production-like environment. The job here is not to add ceremony — it is to make the manual "someone ran the deployed thing and it worked" step *structural*, so the safety net is the pipeline rather than a person's diligence.

**Run it against the real artifact, not the test build:**

- Build and run the **released** artifact in (or against) the runtime it deploys to — `wrangler dev` / the platform's emulator that uses the production runtime, a preview deploy, or the production build served the way it will actually be served — not just `pnpm run dev`.
- Exercise end-to-end the path the failing seam lives on: submit the login, load the published page in a browser and confirm its linked sub-resources (`/_astro/*`, `/assets/*`, fonts, favicon) each return 200, invoke the platform API the test mocked. A 200 on the HTML is not enough if its sub-resources 404.
- If a test passed only because the test runtime is more permissive than production (a limit not enforced, an API present that production lacks), treat that as a **blind** test, not a green one — pin the production limit in the assertion and re-verify against the real runtime.

The deeper fix usually lives upstream in `/tdd`: a seam that had to be mocked to stay green (a platform crypto API, the filesystem, the deploy copy) is exactly the seam GOOS says you should *not* mock — wrap external types you don't own in a thin adapter and integration-test the adapter. This rung catches the parity gap; owned adapters plus a faithful test runtime keep it from recurring.

**Review-cadence note.** Added on convergent grounds (Continuous Delivery's smoke-against-production-like-environment, Twelve-Factor Factor X, Release It! "Design for Deployment", the GOOS walking skeleton) plus one triggering incident (a downstream Cloudflare Workers repo's audit-publish slices, 2026-06-25 — both green under the test suite, both broke only in the workerd/deployed runtime). If after a reasonable sample of slices this rung fires <10% of the time on diffs that had no other issue, demote it to advisory or remove it rather than leave it as ceremony.

#### Tier 3: Behavioral Verification
- API endpoints return the expected responses (use curl or httpie to verify)
- Browser flows work end-to-end (if applicable and you can verify)
- Data flows correctly from input to storage to output

#### Tier 4: Human Verification
- Ask the user only when you genuinely cannot verify yourself
- Be specific about what you need them to check: "Can you verify that the presence indicator shows your name when you open lesson 3 in a second browser tab?"
- Never use human verification as a substitute for Tiers 1-3

**If verification reveals gaps**, fix them and commit the fix as its own commit. Do not amend a prior commit — the history should show what was built and what was corrected.

**Scope check on set-claims.** Before writing any sentence that quantifies over a set, name the set, the enumeration that produced it, and the members not covered. If every member found shares one wording or one kind of file, the enumeration stopped early — see [references/restated-claims.md](references/restated-claims.md).

**Then mutate at the point of consumption (only when this slice ships a test that claims to hold a property).** Skip it when the slice ships no such test — prose, config, and styling work have nothing for it to act on. The rung itself, both readings of a green result, and the rule that the mutating edit must be drawn from the corpus rather than composed are stated once in [references/mutation-at-consumption.md](references/mutation-at-consumption.md).

#### Bug-Fix Verification (when the task is a fix, not a feature)

If this unit of work is fixing a bug, apply these additional checks before committing:

1. **Classify the fix**: Is this a correction (removes the defect — the code error that caused the problem) or a workaround (suppresses the failure while the defect remains)? If a workaround is the pragmatic choice, note it in the commit message and leave the issue open or create a follow-up for the correction.
2. **Structural sibling search**: Search the codebase for the same pattern that caused the defect. If found in other locations, fix all instances or file issues for them. A defect fixed in one location but present in three others is 75% unfixed.
3. **Two-condition confirmation**: Confirm both that (a) the corrupted state is no longer produced, AND (b) the original failure no longer occurs. If only the failure is suppressed but the underlying state is still wrong, the fix is a workaround, not a correction.

### 5. Manual Verification Checklist

Before handing off to `/pre-merge`, present the user with a verification checklist so they can confirm the work is ready.

**Preparation:** Summarize what was built — list the commits made and key files changed. If the task originated from a GitHub issue with acceptance criteria, pull those criteria into the checklist so the user doesn't have to cross-reference.

Present the checklist:

#### Behavior Review
- [ ] Feature works as expected when manually exercised (browser, terminal, API)
- [ ] Edge cases and error states behave correctly
- [ ] No regressions in adjacent functionality

#### Code Quality
- [ ] Diff reviewed — no debug code, console.logs, or commented-out blocks left behind
- [ ] No TODOs that should be resolved before merge
- [ ] No hardcoded values that should be config or env vars

#### Acceptance Criteria

If the task originated from a GitHub issue or PRD with acceptance criteria, read them and generate a concrete verification step for each one. Each step should tell the user exactly what to do and what to expect — not just restate the criterion.

If the slice issue has a `User Stories Addressed` section referencing the parent PRD, read the parent PRD user stories the slice claims to cover. Derived matrix entries (from `/prd-to-issues` Step 5) surface here as verification targets — each mapped commitment needs a concrete step the user can check. Unmapped commitments from the slice are not in scope for this checklist; they belong to other slices or to the post-merge `/pre-merge` reconciliation.

Example — if the AC says "user can reset their password via email":
- [ ] Go to /login → click "Forgot password" → enter test email → confirm reset email arrives → follow link → set new password → log in with new password

After the generated steps, always include:
- [ ] Scope matches what was asked — no unasked-for additions, no missing pieces (this is the in-flight self-check; `/pre-merge`'s Surgical Scope dimension is the diff-time check that runs against the merged hunks)

**Write verified status back to the issue (forcing function).** The slice issue's `## Acceptance Criteria` checklist — authored by `/prd-to-issues` — is the durable contract for "what must be true before this slice merges." Each time a criterion is confirmed verified (by your Step 4 verification or the user's confirmation here), persist that tick to the issue so the tracker reflects reality without anyone reading the chat log. This is not a separate "remember to do it" step: it rides on the verification you already performed, so there is no new judgment to make.

Edit safely — toggle only the checkbox lines you actually verified, and never regenerate the body. `gh issue edit --body*` replaces the *entire* body, so read the current body, flip just the confirmed `- [ ]` lines to `- [x]`, and write it back via `--body-file`:

```bash
BODY_FILE=$(mktemp)  # unique per run — two parallel worktrees / Ralph iterations must not share a temp path

# Guard the read half. A 5xx makes `gh` fail, and the edit below would then
# replace the whole issue body with whatever this file happens to hold.
if ! gh issue view <slice-issue-number> --json body -q .body > "$BODY_FILE"; then
  echo "writeback aborted: issue body fetch failed" >&2; rm -f "$BODY_FILE"; exit 1
fi
[ -s "$BODY_FILE" ] || { echo "writeback aborted: issue body came back empty" >&2; rm -f "$BODY_FILE"; exit 1; }
ORIG_BYTES=$(wc -c < "$BODY_FILE")

# In "$BODY_FILE", change ONLY the verified criterion lines under
# "## Acceptance Criteria" from "- [ ]" to "- [x]". Leave every other line untouched.

# Guard the write half. Flipping "- [ ]" to "- [x]" preserves length exactly,
# so the edited body is never shorter. Shorter means the edit dropped content.
[ "$(wc -c < "$BODY_FILE")" -ge "$ORIG_BYTES" ] || { echo "writeback aborted: edited body is shorter than the body read" >&2; rm -f "$BODY_FILE"; exit 1; }

gh issue edit <slice-issue-number> --body-file "$BODY_FILE"
rm -f "$BODY_FILE"
```

Do not flip a box you did not actually verify, and do not touch lines outside the criteria you confirmed — a careless edit can corrupt issue content. `/execute` is the single writer for these boxes; `/pre-merge` reads them but never writes, so there is no second editor to contradict this one.

**The guards are not optional, and the AFK writeback in Step 6 reuses them.** This is a read-modify-write against an API that returns 5xx under load, and `gh issue edit --body*` replaces the entire body — so a failed fetch here does not lose a stamp, it loses the acceptance criteria `/prd-to-issues` authored and `/pre-merge` Phase 4 reconciles against. `/pre-merge`'s stamp carries the same two guards for the same reason. Retry the fetch **once**; if the second attempt also aborts, leave the boxes unflipped and say so rather than writing.

#### Ready for PR Review

- [ ] Ready to create the PR and run architectural review now (flows directly into `/pre-merge`)?

Wait for the user to review and confirm. If they flag items that need fixing, address them, commit the fixes, and re-present the checklist. Only proceed to Step 6 after user confirmation.

**Optional comprehension pass before review.** If the person who will merge this branch did not author it, or wants to internalize it commit-by-commit before approving, `/walk-commits` is an option *before* `/pre-merge` — an interactive per-commit walkthrough (intent, riskiest line, deliberate oddities, what's absent by design, per-commit sign-off). It is optional and never auto-invoked; name it as a choice, do not run it automatically.

**How the "Ready for PR Review" item drives the handoff:** If the user confirms this final item, Step 6 runs cleanup and then automatically invokes `/pre-merge` with the PRD issue number (if the task originated from one). If the user confirms the behavior, code quality, and acceptance criteria items but answers "no" to the PR review item — because they want to batch with more work, are waiting on external input, or plan to sit on the branch — Step 6 runs cleanup and `/execute` exits cleanly. The user invokes `/pre-merge` manually when ready.

### 6. Cleanup and Handoff

All commits should already be done by this point. This step handles post-implementation cleanup and the transition to `/pre-merge`. It removes only the classification markers — it deliberately does **not** tear down the worktree or branch. That is `/closeout`'s job at the pipeline tail, after the PR merges; removing the worktree here would destroy the branch before it is reviewed and merged.

Remove the classification markers:

```bash
rm -f "$CLAUDE_PROJECT_DIR/.claude/.tdd-active" "$CLAUDE_PROJECT_DIR/.claude/.tdd-skipped" "$CLAUDE_PROJECT_DIR/.claude/.lfg-active"
```

**AFK runs persist verified AC too.** AFK Ralph iterations skip the Step 5 user checklist, so the writeback that rides on it never fires. Before an AFK iteration exits, persist any acceptance criterion verified during Step 4 back to the slice issue using the same `gh issue edit --body-file` toggle described in Step 5 — including both of its guards: check the fetch's exit status and refuse the write if the edited body came out shorter than what was read. AFK is the mode with nobody watching the write, so it is the one that most needs them. AFK is the mode that most needs at-a-glance legibility — leaving its issues fully unchecked despite verified work is exactly the gap this closes.

**Write review notes into the PR body.** `/execute` finishes holding things no artifact records: which verification tiers ran versus were skipped and why, which scope was absorbed under Step 0's Consumes gate, which assumptions shifted, where the implementation is thinnest. Author preparation is the strongest empirical correlate with low defect density (Cohen) and a structured reading plan measurably raises detection (Dunsmore) — but only if the reviewer receives it. Left in the Step 5 checklist alone, that knowledge reaches a user and stops there — and on an AFK run no checklist is ever presented, so it reaches nobody.

Hand it to the reviewer instead, as a `## Review Notes` block in the PR body. GitHub-native, survives a fresh session, no new filesystem state. **`/execute` composes the notes; `/pre-merge` writes them** — on both the author-mode and loop-mode handoffs, pass the block to `/pre-merge`, which emits it into the body at Phase 2 alongside the rest of the PR template. `/pre-merge` owns PR creation, and `/execute` should not start writing PR bodies to deliver a block the very next step is already opening the body to write.

**The notes must be checkable, not trusted.** The reviewer's entire picture of this change comes from the diff plus these notes — and the notes are authored by the agent whose work is under review. A fresh context buys independence from *rationalization* and buys nothing against *misreporting* (Leveson: no control system performs better than its measuring channel). So record **which verification commands ran and their exit status**, in a form the reviewer can re-run. Never assert a conclusion the reviewer has to take on faith: "Tier 2.5 verified" is exactly the claim that cannot be checked.

```markdown
## Review Notes

<!-- review-notes: execute -->

**Verification commands run**

| Command | Exit | Tier |
|---|---|---|
| `pnpm run typecheck` | 0 | 2 |
| `pnpm run test` | 0 | 2 |
| `curl -s -o /dev/null -w '%{http_code}' localhost:3000/reports` → `200` | 0 | 2.5 |
| `shellcheck --version` → `0.9.0` (matches `.shellcheck-version`); `shellcheck scripts/*.sh` | 0 | 2 |

**Name the version whenever the repo pins the tool, and say whether local gates ran.** A bare "lint clean" is a claim about *whichever* binary happened to be on `PATH`, and linters disagree across releases in both directions — so the reviewer cannot tell whether it describes the merge gate or a different instrument. Two lines close it: give the version beside any pinned tool's row, and state once whether the repo's own pre-commit/pre-push hooks were active for this branch. A branch whose hooks never ran is not disqualified; it is *differently evidenced*, and the reviewer needs to know which they are reading.

**Verification skipped, and why**
- Tier 2.7 — not applicable: test runtime and deploy runtime are both Node 22.
- Tier 2.5 dev-server boot — skipped, no Postgres available in this environment.

**Scope absorbed under the Consumes gate**
- #41 declared `ReportSchema` as a Zod schema; the tree had a plain object. Added the schema here; correction comment filed on #41.

**Assumptions that shifted**
- None.

**Known-weak spots**
- The retry path in `lib/fetch.ts` is covered only for the 2-attempt case.
```

**Auto-invoke `/pre-merge`.** Which mode depends on how Step 5 resolved:

- **Step 5 ran and the user confirmed "Ready for PR Review"** → invoke `/pre-merge` in author-mode now, passing the review notes and — if the task originated from a PRD issue — the issue number, so it can gather slice lineage and verify boundary map contracts without asking the user again.
- **AFK Ralph iteration** (Step 5 structurally cannot run — there is no user to ask) → enter **`/pre-merge` loop-mode** rather than exiting to a manual invocation. This moves the AFK boundary from "code exists" to "code has been reviewed and every finding has an owner." Loop-mode records findings in a durable ledger on the PR and makes no commits and no decisions, so what the operator inherits in the morning is a reviewed branch plus a triaged list — not a branch that was quietly edited overnight.
- **The user answered "no" to the PR review item**, or Step 5 was skipped by the trivial-task exception → `/execute` exits here and the user invokes `/pre-merge` manually when ready.

**Next-step menu at the manual exits.** When `/execute` stops *without* auto-invoking `/pre-merge` — the user answered "no" to the PR-review item, or is batching more work — do not drop to a bare text box. Offer the next step as a single `AskUserQuestion` (see `references/next-step-menu.md`) with the recommended step first, each option naming its outcome rather than just its skill: **→ `/pre-merge` now (recommended — open the PR and review it)**, **Batch more work — exit without opening a PR**, **`/walk-commits` first (read the branch commit by commit)**. Beyond the pipeline successor, include 1–3 follow-ups drawn from *this* run — e.g. "verify acceptance criterion N in the running app," "show the diff for the riskiest change" — mirroring `/walk-commits`'s commit-specific deep-dives. The platform's free-text "Other" option is the escape hatch — don't add one. This menu **does not** apply when Step 5 already confirmed PR review (auto-invoke handles that) or on AFK Ralph iterations (no user to ask).

**Print the runtime handoff line.** Whether `/pre-merge` is auto-invoked or the user is exiting to invoke it manually later, print the line so a fresh session can open by copy-paste:

```
**Next session:** /pre-merge
**Input:** the verified commits on branch <branch-name>
```

Substitute `<branch-name>` with the actual branch the commits live on (`git branch --show-current`).

If you cannot complete the task in this context window, leave a comment on the GitHub issue with:

- What was done
- What remains
- Any gotchas or tricky parts for the next iteration
- If the failure was caused by an error (build failure, test failure, unexpected API behavior), include the exact error output — the next iteration benefits from the real error, not a summary

If the error suggests the approach from the research artifact or the PRD is wrong, say so in the comment — this is a signal to backtrack, not to keep retrying the same approach.

**AFK progress and plateau detection.** When running under Ralph, progress is *epistemic state advancement*, not activity. An iteration counts as progress only if at least one of these transitions from unresolved to resolved:

- an unmet acceptance criterion on the active slice
- a failing check (typecheck, test, or verification gate) becoming a passing check
- a named unknown or rabbit hole from the research artifact or the PRD being closed

Code churn without such a transition is a stationary dot. Red flags: the same slice staying active across multiple iterations, tests still failing but "in different ways," recurring error classes with superficial code rewrites, no acceptance checkbox or gate advancing.

**Plateau stop rule.** If two consecutive iterations on the same slice produce stationary dots, stop and leave an issue comment (same shape as the repeated-failure comment above) naming what did *not* advance. Do not start a third iteration. Hysteresis: a single recovering iteration — at least one of the transitions above — resets the stationary counter. This rule complements the existing repeated-failure rule; it is *not* a replacement.

This applies to AFK Ralph iterations only. HITL `/execute` runs are paced by user judgment and do not need the heuristic.

## Handoff

- **Expected input:** a concrete task, issue, or slice with enough scope clarity to implement safely, plus durable upstream artifacts if this is being run AFK
- **Produces:** verified code changes as compartmentalized commits (one per logical unit), and implementation context for the next reviewer or iteration
- **May invoke:** `/tdd` for backend work and behavior-heavy frontend logic, plus stack-specific reference skills when the project stack warrants them
- **Auto-invokes:** `/init-pipeline` when enforcement hooks are missing, and equally when the installed hook exists but predates any term in Step 0's `GATE_TERMS` — the lock's stamp flag or a classification marker — Step 0's `hooks-absent` and `hooks-stale` verdicts both route here; `/setup-ralph-loop` when the task comes from a multi-slice GitHub issue and no Ralph scripts exist in the repo, and `/pre-merge` at the end of Step 6 — in author-mode when Step 5 ran and the user confirmed the "Ready for PR Review" checklist item, in loop-mode on AFK Ralph iterations
- **Comes next by default:** `/pre-merge` — author-mode, auto-invoked after Step 5 user confirmation in HITL mode; loop-mode, auto-entered on AFK Ralph iterations; invoked manually by the user when they answered "no" to the PR review item or the trivial-task exception skipped Step 5
