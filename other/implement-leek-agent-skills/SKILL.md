---
name: implement
description: "Implement one work item end to end, or every ticket of a spec in one run: scope and claim it when trackable, TDD at chosen seams, commit, review, verify, resolve it, and open a PR when asked."
disable-model-invocation: true
argument-hint: "A ticket or spec path; add `all` to build every ticket of the spec on one branch, delivered as one PR or a stack (omit to use the conversation scope)"
---

# Implement

Implement exactly one work item per session, test-first and verified end to end. A work item is a **ticket**, a spec small enough for one session, or an agreed conversation scope. The one exception is a **spec run**, which builds every ticket of a spec in one session.

**Spec runs and PR delivery** live in [`references/spec-run.md`](references/spec-run.md). Read it before step 1 on every run: its **Choose the delivery shape** question comes first (current branch, a PR, or a stack of PRs for a whole spec). Its spec-run and follow-up sections apply when the user asks to build a whole spec (`all`, "implement all of …") or to change work already delivered as a PR.

Pipeline position: `wayfinder` (decide) → `to-spec` (write the spec) → `to-tickets` (break it into tickets) → **`implement` (build one ticket per session, review and verify inside)**.

## Guardrails

- **Never** reset, roll back, drop, or truncate a database, or run another destructive data operation, without explicit approval. Put schema changes in new migrations; sequence live-table changes expand–contract.
- Verify identifiers before using them: route names, config keys, enum values, icon names, and package APIs. A manifest entry alone does not prove registration or use.

**Stack references.** Identify the stack from its manifests. If a matching file exists below, read it before step 1: it names that stack's destructive commands, formatter, test command, and worktree setup.

- Laravel (`laravel/framework` in `composer.json`): [`references/laravel.md`](references/laravel.md)

## Process

### 1. Scope and claim the work

Classify the input and make its acceptance criteria explicit:

- **Ticket**: fetch its full body and comments. From its parent spec, load the **Build Contract** section first when present, then the headings the ticket names or the implementation reaches. Read direct blockers' `Resolution` sections for handed-forward seams; load other closed tickets and the map only on demand. A `wayfinder` decision ticket is eligible only when its type is `task`; stop on the other types because they decide rather than build. A `task` is manual unblocking work, not code, do it yourself where you can, otherwise hand the human the precise checklist from `ticket-types`; get explicit approval before any destructive or irreversible step, record the resulting facts, and Resolve. It skips the seams/TDD/commit/review/verify loop (steps 2–7), which assume code changes. The ticket is the work item.
- **Delivery ticket** (`delivery: true`): the spec's last ticket, which proves the spec shipped whole. Work it per [`to-tickets/DELIVERY-TICKET.md`](../to-tickets/DELIVERY-TICKET.md): pass 1 before merge, pass 2 after deploy (a `ready-for-human` delivery ticket is waiting for pass 2). It skips steps 2–5; steps 6–8 run per that file.
- **Spec**: fetch its full body and comments. If it holds more than one independently deliverable ticket or cannot fit one session, it needs tickets: with its `tickets/` published and a spec run asked for, run the spec run; otherwise stop and tell the user to run `to-tickets`. A spec that fits one session is itself the work item.
- **Conversation**: restate the scope and behavior criteria in a few lines. It has no tracker claim or resolution.

Work items are markdown files under `.scratch/`: there is no external tracker. When launch context already identifies the selected file, its status, and blockers, revalidate those exact files rather than rereading the tracker layout. Otherwise read the layout once through `.agents/issue-tracker.md` (written by `/setup`). If it's missing, try `docs/agents/issue-tracker.md` (legacy), then the `setup` skill's seed. Confirm every direct blocker is closed through the item's `blocked-by` frontmatter, and stop before claiming if any remain open. Then claim before building:

- On a ticket from `to-tickets`, or a directly implemented spec, set its frontmatter `status: in-progress` and `claimed-by:` to a session-unique value, then re-read to confirm you won the claim (compare-after-write, see the tracker's Working in parallel rules). A spec built directly is claimed exactly like a ticket; it is the file you build from, not a parent to leave alone.
- On a `wayfinder` decision ticket, use the Wayfinding **Claim** operation (`claimed-by`).

A ticket or spec is **trackable**: its frontmatter `status` is the state of record. Some repos also keep a ledger or prose summary of efforts in their tracker doc; update it when the repo asks, but it never replaces the frontmatter write. Building in a linked worktree changes nothing: write and commit the frontmatter there, and it reaches the main checkout when the branch merges.

If the item is already claimed or in progress, stop; treat the claim as stale only when its work is visibly committed or clearly abandoned.

After claiming, or after scoping conversation-only work, record the output of `git rev-parse HEAD` as immutable `base_sha`. Use that exact SHA for review and for proving failures pre-existing.

Finish this step only when the work fits one session, its acceptance criteria are explicit, every trackable item is claimed with blockers closed, and `base_sha` is recorded.

### 2. Choose the seams

Use the ranking and selection rules in the `tdd` skill's **Seams: where tests go** section. Reuse seams already recorded in the spec; otherwise **choose them yourself and state the choice**: one line per seam, no approval round. Seam placement is test structure, which `grilling`'s **What still earns a question** hands to you, and the rules are the single source of truth. Ask only on a genuine fork the rules rank equally where the two placements would make materially different work.

Finish this step when every acceptance criterion has a seam.

### 3. TDD loop

Run the `tdd` skill at the chosen seams. Discover the repository's focused-test and static-analysis commands from its scripts and existing usage; filter every test run during the loop to the single test or file covering the change (`--filter=<test name>` or the exact test file path, never neighboring or demo suites in the same directory), and run static analysis regularly when configured. If the user explicitly asks to skip tests in this session, honor that for the rest of the session and note it in step 8.

Finish the loop only when every acceptance criterion is covered at a chosen seam, every focused test passes (when the user asked to skip tests, the last focused result stands instead), and configured static analysis is green.

### 4. Format and commit a reviewable checkpoint

Run the repository's configured formatter on the paths you touched only (Pint, Prettier, Black, gofmt: whatever it configures), so a parallel session's uncommitted files stay as they are. Check `git status --porcelain`, stage only work-item files by explicit path, and leave foreign changes unstaged. Changes under `.claude/agent-memory/` are always yours too, whoever wrote them: they are the notes of agents with `memory: project`, not a parallel session's work in progress, so they ride along in your commit (`git add -- .claude/agent-memory`). Commit to the current branch (PR delivery created it before step 1); this step creates no branch or worktree. Record the paths you touched; review scopes to them (next step), so a parallel session's commits on the same branch neither get staged here nor reviewed there.

Finish this step with every work-item change committed, every foreign change untouched, and the checkpoint commit SHA recorded.

### 5. Review

Run the `code-review` skill against `base_sha`, scoped to the work-item paths you recorded (so concurrent commits on the shared branch stay out of the range). Resolve every actionable finding through the `tdd` loop, rerun affected focused checks and static analysis, format, stage explicit paths, and commit the fixes. Re-run `code-review` after each fix commit as a re-review, passing the previous round's findings and head. Two review rounds is the budget. When the second still has BLOCKING or MAJOR findings, fix those in one more round without asking, its re-review covering only them; list whatever is left for the user with the commit each round reviewed. A PR body carries each finding left open as a `Left open:` line.

`code-review`'s Correctness axis hunts bugs and failure modes; its BLOCKING and MAJOR findings are actionable like any other. A fix that adds a mechanism (job, lock, claim, retry) is new surface, so the re-review after that fix commit covers it. Whatever this step misses goes to the PR's review bots, one round per push.

Finish this step only when review reports no unresolved actionable findings (or the round budget is spent and the rest are listed) and every work-item change is committed.

### 6. Run the final automated checks

Skip the full-suite question when the repo's rules or the user's saved preferences already settle it (CI runs the suite, or "do not run the full suite unless asked"), and follow that answer. Otherwise ask once (via `AskUserQuestion` where available, otherwise a plain question in chat) whether to run the full test suite as the final automated gate. If the answer is no, skip the full run (the focused tests from step 3 stand as the automated evidence) and record the skip so step 8 reports it plainly.

When approved, run the repository's documented full-suite command: its `AGENTS.md` or `CLAUDE.md`, package scripts (`composer.json`, `package.json`, a `Makefile`), or CI workflow names it; fall back to the stack's default test runner only when none does. A run that can outlast the foreground limit goes to the background (Bash `run_in_background` where available). Then end the turn with no reply and let its completion notification wake you; a check-in that only says it is still running costs the user a turn. Fix failures caused by the work. Prove an unrelated failure pre-existing against `base_sha`, then note it plainly instead of expanding scope.

Any code fix returns to steps 3–5 before this gate runs again. Finish this step when the full run was skipped (declined, or settled by rules or preferences), or when every caused check passes and every remaining failure has base-SHA evidence.

### 7. Verify end to end

Run the `verify` skill. A product failure returns to steps 3–6 before verification runs again. Successful verification is required to resolve a trackable work item.

If an external dependency prevents verification, keep the committed implementation, report the exact blocker, and leave the work item open. Mark nothing verified on inference alone.

### 8. Close the loop

After successful verification, record what was built, any justified deviation, verification evidence, the implementation commit SHA or SHAs, and any public seam a direct successor should reuse; check off every satisfied acceptance criterion. This `Resolution` is the successor handoff, so keep the seam and evidence concrete without retelling the parent spec. Resolve the work item according to its branch:

- **Ticket, or a directly implemented spec**: set its frontmatter `status: closed` and append `## Resolution`. Write `closed` exactly, never an invented value such as `built` or `done`. A delivery ticket with after-deploy steps left goes to `ready-for-human` instead, per its file.
- **`wayfinder` decision ticket**: use the Wayfinding **Resolve** operation.
- **Conversation**: report the result without touching any file under `.scratch/`.

Leave every parent open; a ticket never closes its spec, and `implement` never touches the map (the map was already closed by `to-spec`, or by a spec-less `to-tickets`, when the spec or tickets were written). A spec is **complete** when every ticket in its `tickets/` is closed; a derived state you report, not a status you write onto the spec. When the spec itself was the one-session work item, close that spec directly. Keep the resolution write out of code commits: if `.scratch/` is tracked, commit it separately; never fold it into an implementation commit. Resolution text cites the implementation commits, never its own closure commit.

For trackable work, re-read the markdown file after writing it and verify its frontmatter reads `status: closed` with a `## Resolution` section.

Finish when the implementation commits and any separate resolution commit are recorded and the tracker's final state is verified, or the conversation-only result is reported. Then stop; any next work item gets a fresh session with a clean context.

## When you're done

Print the end-of-session block using the frame in [`wayfinder/references/pipeline-end-block.md`](../wayfinder/references/pipeline-end-block.md). For a trackable work item with a parent, check the markdown tracker for the remaining frontier before writing the block, don't guess at what's left.

```text
---
Pipeline: decide → spec → tickets → **build**   (4 of 4)
Done: <what now works, the work-item ref if any, commit(s), verification state>
Next:
  • <condition> → /<skill> <ref>
```

Stage-specific **Next** conditions (only those that apply, most likely first):

- **A PR is open and review bots are still running** → `/resolve-review-comments <PR>` once they post; name the PR and the worktree path
- **A stack of PRs is open** → `/triage-github-pr <every PR, bottom-up>` to land it bottom-up with merge commits
- **More frontier tickets on the parent spec** → `/clear`, then `/implement <next frontier ticket>` (resume your own claimed-but-unfinished ticket first if you stopped mid-work), or `/implement <spec path> all` to build the rest in one run, or `/implement-spec <spec path>` to build them in parallel; name it and how many remain
- **Every ticket on the spec is closed** → nothing to run; say the spec is complete and name anything deferred out of scope
- **Only the delivery ticket is open, at `ready-for-human`** → deploy, then `/implement <delivery ticket>` for its after-deploy steps; list them
- **Remaining tickets are all blocked** → `/implement <the blocker>` first, or `/grill-me` if the blocker is a decision
- **The build exposed a decision nobody made** → `/grill-me` on it, then re-run `/to-spec` if the spec is now wrong
- **Verification is externally blocked** → keep the work item open and name the exact unblock condition
- **Stopped mid-work** → say what passes, what is committed or uncommitted, the claim state, and the next red test to write; resume that ticket next session before taking a fresh one, or Release it to hand it back to the frontier
