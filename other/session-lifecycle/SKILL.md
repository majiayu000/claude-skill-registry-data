---
description: "The session bookends, codified — one skill that makes every repo start, run, and end sessions the same way."
---

# /session-lifecycle

The session bookends, codified — one skill that makes every repo start, run, and end sessions the same way. It bundles the Resume protocol (session start), the during-session reporting conventions, the end-of-session checklist, and the follow-on protocol into a single installable unit, composing the component skills (`/catchup`, `/learn`, `/visual-brief`, `/create-issue`, `/decide`, `/pulse`) by reference. Natural-language cues like *"resume"*, *"let's start"*, *"wrap up"*, or *"close out the session"* should route here.

This skill is a **bundle head**: it does not re-implement the components, it drives them. Where a component skill is not yet installed in this repo, the install-on-miss rule applies — run `skill add <name>` first, then invoke it.

## Arguments

- `$ARGUMENTS` — optional subcommand:
  - `start` — run the session-start (Resume) protocol only.
  - `end` — run the end-of-session checklist only.
  - *(empty)* — infer from context: fresh session with no work done yet → `start`; work shipped and the user is wrapping up → `end`; otherwise ask which bookend is meant.

## Instructions

### Session start — the Resume protocol

Run these in order; each step re-derives state rather than trusting memory:

1. **Conventions** — read `CLAUDE.md` (project root). If the repo has none, note it and continue.
2. **Working tree** — `git status && git log --oneline -5`. Name anything dirty; never assume a clean tree. Record the branch you will work on as `SESSION_BRANCH` — this is the session's *claim*, and every write from here on is checked against it (see "During the session"). On resume, changes that match this run's recorded checkpoint may be recovered as its unfinished work after verifying ownership. Treat other dirty files as belonging to another session: report them, leave them alone, and never stage them. Re-claim it whenever you deliberately switch branches — creating the feature branch you will write to is a legitimate switch, and a SESSION_BRANCH still pinned to `main` would make every later write assertion fail on correct work. The assertion exists to catch a branch that moved under you, not one you moved on purpose.
3. **Open PRs, split by author** — the split matters so external contributions aren't lost before autonomous work starts:
   ```bash
   gh pr list --state open --author "@me"
   gh pr list --state open --search "-author:@me"
   ```
4. **Skill drift** — run `/skill outdated` and report any drifted skills (fix now only if the session will use them).
5. **Global-conventions sync** — `~/.fleet/AGENTS.md` and `assets/AGENTS.md` in the registry
   are **both authored**, so they drift in both directions at once and a bare `diff -q` cannot say
   which side is right. Run the class-split root, provider-adapter and size check instead:

   ```bash
   python3 ~/.claude/scripts/fleet-check.py    # 0 = floor intact · 1 = FLOOR drift · 2 = could not verify
   ```

   Exit 1 is a stop: reconcile the named floor rule before long work (land the machine's delta in
   the registry, then copy out). Exit 0 with default drift is information — it names the direction,
   act on it when convenient. Exit 2 means it could not verify a root, adapter, instruction size or configuration (the `git fetch` is a
   hard precondition, never softened) — that is *not* agreement; say so rather than proceeding as if
   it passed.

   Then `/next` itself, which is distributed **verbatim** (no rule classes, no customization markers), so a
   plain `diff -q` is its whole drift detector — and **a missing file is not drift**:

   ```bash
   if [ ! -f ~/.claude/commands/next.md ]; then
     echo "/next is not installed on this machine — cp assets/next.md ~/.claude/commands/next.md"
   else
     diff -q ~/.claude/commands/next.md ~/Projects/skill-templates/assets/next.md
   fi
   ```

   Without the guard `diff` just errors on a machine that has never installed `/next`, which reads
   as a failed check rather than as "install it". Install (or copy) first, then compare.
6. **Prior-session state** — read this scope's seed, `$CLAUDE_HANDOFF_DIR/NEXT-<scope>.md` (default dir `~/Obsidian/no-it-all/handoffs/`), plus the current `autonomous-session-*.md` STATE header when present. `<scope>` is the main worktree's directory basename, resolved from git — `python3 ~/.claude/scripts/session-seed.py path` prints the exact file to open — so every worktree of a repo resolves to the same seed and no `$PWD` test is involved. There is exactly **one** canonical seed per scope, so nothing has to be ranked: no newest-wins rule, no mtime, no tie to resolve. Sibling files named `NEXT-<scope>.<UTC>-<sid>.md`, or `…-<sid>-<n>.md` when two archives landed in one second, are **archived** seeds — a previous session's, parked when this one collided with it. Do not read them by default, but if the canonical seed is missing, say so and list them: the newest archive is usually an unconsumed handoff, and a session that silently starts from nothing is how work gets repeated. Read the seed's header and TL;DR plus the ledger's STATE header — not the full history. Seeds are **perishable**: each is superseded by the next, and anything in one still worth reading after it is consumed belongs in `docs/records/`, linked from the seed. `/catchup` is the component skill for reconstructing a prior session where installed.
   Before using a seed as actionable context, validate its content with
   `python3 ~/.claude/scripts/session-seed.py verify --file /absolute/path/to/seed.md`.
   This also works for an explicitly selected archive. It checks the same filled-content
   contract as writing, and prints `content valid (NOT canonical proof):`; it never prints
   `seed:` or proves the prior session is this session. A hollow legacy seed is context to
   reconstruct through `/catchup`, not an executable work order. Do not invent missing
   state or treat that refusal as permission to abandon already authorized work.
   Read `Today's task` and state it as the selected work package with its observable
   acceptance, unless the user's newer scope instruction supersedes it. The seed supplies
   context and carries existing authority; it grants no new execution authority.
7. **Verify the last claimed merge** — if the prior session's notes claim a merge, confirm it (`gh pr view <n>` reports `MERGED`) before building on it. State is re-derived, not trusted.

Then state, in one short block: branch/HEAD, dirty files, open PRs (mine/others), drifted skills, the delegated outcome and observable acceptance, what is usable now, the selected work package and mode. Normal development is the default; `/prime-directive` or an explicit autonomous continuing mission selects prime mode. Preserve that mode on resume; user presence does not change it. Reuse the user's existing authorization; a seed is context, not a request for another scope approval.

### During the session

- **Every user-facing message ends with the mechanical `**Status:**` block** — a `**Status:**` lead on its own line, then four fixed slots as one bullet each (done · in flight · blocked · DECISION), `none` when empty. This is the global reporting rule in `~/.claude/CLAUDE.md` ("End-of-message summary"); follow it from there — do not restate or fork it here, and in particular do not emit the retired one-line `·`-separated form. Subagents' final messages carry their own `**Status:**` block.
- **Session boundaries** — follow the global mode distinction: normal development ends after delivering the selected work package through merge and ledger update; prime mode checkpoints and continues its authorized mission through supported auto-compaction. A wave boundary or second compaction alone does not end a prime run.
- **Assert the branch before you write.** `git` state is global to the working copy and several sessions share it, so re-check `git branch --show-current` against `SESSION_BRANCH` (claimed at start, step 2) **immediately before your first edit** and **again immediately before staging**. A checkout from earlier in the session proves nothing — another session can move HEAD in between, and your edits then land on its branch. Re-check, never remember; if HEAD has moved, stop and re-establish the branch before writing anything.
- **Stage explicit paths.** `git status --short`, then `git add` the files you changed, **by name**. Never `git add -A`, `git add .`, `git add -u`, `git add <dir>/`, or `git commit -a` — a foreign file in a shared tree is the normal case, so a bulk add commits someone else's work into your PR. `-u` is not the safe one: it restages every *tracked* file whose worktree copy differs, including files a clean/smudge filter rewrote without you touching them — that is how `git add -u` turned a tracked 21KB `.docx` into a git-lfs pointer and committed it as an edit.
- **Prefer a per-session worktree.** Where the harness gives this session its own `git worktree`, use it; where it does not, the two rules above are the whole of the protection and apply verbatim.

### The interactive flow — use the authority already granted

An operator watching does not itself require a pause. Resolve routine implementation choices and verified adequate fallbacks autonomously; preserve genuine owner-reserved decisions and repository gates.

1. **Scope and implement.** State the outcome, acceptance and selected work package. Inspect shared code/analogous flows for reuse, record a proportional plan, and delegate implementation to the suitable available model under the tiering policy. The coordinator owns the result. Ask only for missing authority or an indispensable preference.
2. **Review and merge.** Run `/full-review`, including posted Copilot feedback and independent review, triage by impact, and satisfy final-commit CI and repository gates. Delegated implementation includes routine gated merge in both normal and prime mode; do not ask again. Review-only/planning-only work, unrelated PRs and an explicit user hold do not grant it. Required external approvals and real permission restrictions still apply. Handle in-scope PR dependencies in order and reverify dependent PRs after their base changes.
3. **Record delivery.** Confirm `MERGED` into the target branch and update the ledger with the actual merge SHA, acceptance evidence and follow-up issues before declaring delivery complete.

**For already-authorized steps, act.** Specifically, never ask:

- *"want a PR?"* — PR-first is already the workflow; open it.
- *"merge or review?"* — review is mandatory; run it, never offer to skip it.
- *"shall I fix the findings?"* — fix them and re-run the gates.
- *"shall I merge?"* — within delegated implementation, satisfy the gate and merge; name a real restriction if one prevents it.

Ask only when a needed decision is outside delegated authority or cannot be resolved from available evidence. Put that precise decision in the `DECISION` slot and continue independent authorized work. An authorized fallback verified to preserve safety, correctness, required runtime/cost constraints and essential capability needs no owner pause: record the evidence, file the underlying problem and continue. If it cannot be verified, block only the affected item with the reason.

**Unattended sessions use the same review and safety gates.** Delegation does not grant missing signing, hardware, deployment or merge authority. A genuine reservation blocks its dependent work; it does not stop all other work toward the outcome.

Before a wait-only handoff, advance independently actionable slices through their authorized review and delivery gates within the remaining limits. Ask the owner only for the reserved prerequisite; retain the agent's already-delegated execution in the handoff and resume it when the prerequisite arrives through the supported continuation mechanism.

**Clearing the session** follows the global mode rule. Preserve every PR's verified state (merged on `origin/main`, or safely retained open with its remaining gate), in-flight work, follow-ups, outcome, mode and consumed limits. In **normal mode**, after completing the selected work package, write the seed and instruct the user to start a fresh session with its absolute path; other backlog items do not keep this session running. In **prime mode**, checkpoint and continue the selected mission using supported host continuation/compaction; a fresh successor must be accepted, with its identifier recorded, before claiming a handoff is executing. During unfinished work in either mode, a needed restart preserves state and names any actual host limitation. A second compaction is not itself a stop or a user decision.

> Codified from a 9-session flow audit (skill-templates#237): the zero-wait configuration ran 19 PRs with 0 rollbacks and 9/9 clean endings, while the only measured overhead came from overstaying a boundary, not from asking questions. The cost of a Path-B wait is still unmeasured — when a mid-flow wait *does* happen, timestamp the ask and the reply in the status flow so the counterfactual can close.

### Session end — the checklist

Run in order; skip a step only by saying so with a reason. **Steps 1–3 are the two ending artifacts and the one check that proves the seed the next session opens is the one this session wrote; a session that skips either artifact has not ended.**

1. **Handoff seed (artifact ②)** — **the seed is written outside every worktree, at an absolute path:** `$CLAUDE_HANDOFF_DIR/NEXT-<scope>.md`, default dir `~/Obsidian/no-it-all/handoffs/`. It holds what shipped, what remains, and *why* each remaining item is blocked or deferred. Not in the repo, not in this session's worktree, not on a branch — an absolute path outside every *session's* workspace has **no worktree to be torn down with, no branch to be unreachable from, and no index to be confused with**, which is why nothing downstream has to be gated on it. Three earlier attempts to keep the seed inside a session's own workspace failed on exactly those surfaces, the last of them on a "committed" proof that had only staged the file. Read the property precisely: the default handoff dir is itself a git repo (the vault is versioned, and should be), and that takes nothing away — what the seed must be outside is the tree *this session* edits, branches and tears down, which is exactly what the write checks it against.

   **Resolve the next task before writing.** If you are about to write a seed with more
   than one next task, invoke `/decide` first. Pick and record a choice that is authorized
   and reversible. For an owner-reserved choice, proactively use the host question UI
   before the seed write, with concrete options, trade-offs, a recommendation and a
   default. A default records the recommended plan only; no answer grants no reserved
   execution authority. Keep the affected task blocked and record the open question in
   DECISION with `recommend:` and `default:` until answered. Continue independent
   authorized work. Select one next task with `(agent name)` or `OWNER: name`; alternatives
   go only in the seed body. The task's observable acceptance belongs in `--next`.

   **Capture the boundary pulse.** Run the offline reader before the full seed write:

   ```bash
   PULSE_SNAPSHOT=$(mktemp "${TMPDIR:-/tmp}/session-pulse.XXXXXX")
   python3 ~/.claude/scripts/session-pulse.py --boundary --snapshot-file "$PULSE_SNAPSHOT"
   ```

   It prints eight lines and always exits zero; read WARN and snapshot-save failures.
   Add `--source claude`, `codex` or `chroxy` only for the actual host. Without a named
   source usage stays `n/a`; Claude's meter also requires its actual harness session ID.
   Optional `--signals-file` takes already cached measurements under `/pulse`'s contract.
   No network requests or test runs belong in this readout. A threshold warns, never stops
   authorized work. Carry the resulting snapshot with `--pulse-file` below; if snapshot
   creation failed, report that limitation and omit the unavailable snapshot rather than
   inventing one. The full seed write remains subject to its content checks.

   **One command writes it.** It resolves the scope, resolves this session's id, archives whatever it collides with, writes the seed, and proves the result — all of it in `session-seed.py`, none of it transcribed here:

   ```bash
   python3 ~/.claude/scripts/session-seed.py write \
     --picks-up-at "Add the remaining script tests (agent Sol)" \
     --boundary-reason "package complete" \
     --next "Add coverage for the remaining script assets. Acceptance: their sibling suites pass." \
     --alt "Review the queued documentation changes (agent Sol)" \
     --pulse-file "$PULSE_SNAPSHOT" \
     --body-file /tmp/handoff-body.md
   ```

   It prints `seed: <absolute path>` — which is step 7's one line to paste — or a `REFUSE:` line with a nonzero exit. **A REFUSE never destroys an existing seed**: the archive is what earns the right to write, so a failed archive aborts before the write. It does *not* mean nothing happened, and reading it that way is the trap — the last thing the write does is run step 3's proof, so a REFUSE from *there* arrives after the seed is already on disk. Do not infer from the exit code; read the lines above it, which say what was done and in what order: `archived: <path>` iff an incumbent was moved, then `seed: <path>` iff the proof passed. Add `--topic <name>` for a fleet session with a named topic; never anywhere else.

   `--body-file` carries the filled context, written first to a scratch path (`-` reads
   stdin): `## STATE` (branch/HEAD, working tree, CI, tests, open PRs and issues), a
   **"Verify before building on any of this — re-derive, don't trust"** block with each
   command's expected answer, `## TL;DR — what shipped`, and remaining gaps or deliberate
   deferrals. STATE and TL;DR must contain actual content; other useful headings are welcome.
   The script requires this body and never writes a skeleton when it is omitted.

   `--next` renders the single `## Today's task` section: one imperative task in one
   paragraph, followed by `Acceptance:` and an observable result. `--alt` renders
   `## Alternatives` and may be repeated zero to two times. Keep these generated sections
   out of the body file. The short `picks_up_at` dispatch line must be at most 140 characters,
   name one task and identify its executor with `(agent name)` or `OWNER: name`. It refuses
   the case-insensitive multiple-task markers ` or `, `;`, `·`, `candidate` and `Next runs`.
   Keep choices in alternatives rather than the dispatch line.

   Carry every unresolved owner choice with `--decisions-file /tmp/handoff-decisions.json`:
   a JSON list of objects with filled `text`, full UTC `opened_at`, and filled `default`.
   Preserve each choice's original timestamp until it is answered. The default records the
   proposed plan only. Omission writes an explicit empty list, so omit it only when no
   decisions remain. Structured `decisions` and `last_pulse` use single-line JSON flow syntax
   in YAML frontmatter; block-style YAML is not accepted by these stdlib-only readers.

   Both write and verify refuse missing or `unstated` boundary reasons, hollow task or
   context sections, the retired skeleton's explicit placeholders, and generic angle
   placeholders outside fenced code. The proposed content is validated before an incumbent
   is archived or any seed is written. These checks enforce a filled structure; they do not
   prove that the claims are true or replace the resume protocol's evidence checks.

   Fill the body with the **delegated outcome and observable acceptance**, **what is usable today** (build/install and evidence, or unknown), **the remaining gap**, and **the actual execution state**: continuing/accepted next run, ready for user QA, budget/retry limit, specific blocker, host continuation limit, or complete. Preserve the stable run identity, authority, configured limits with their scope, consumed usage and attempts including pre-PR failures. Missing accounting remains unknown; recover it before spending against an uncertain allowance. Name a user action only when genuinely needed, with what it unblocks. The script writes and verifies the file; it does not infer these answers or schedule continuation.

   **Why a script and not a snippet.** This step was prose containing bash, transcribed and executed by an agent, and tested by extracting the fenced blocks back out and running them. Five rounds of review each fixed their findings and each introduced new ones, because every fix added more shell to a document: scope resolution, path sanitising, collision archiving, id resolution and a re-derivation of all three appeared twice, in near-copies that drifted. The logic is one implementation now, with its own test suite; what stays here is the doctrine, which is the part a customized copy must not be able to drop. **Do not hand-write the seed** or re-derive the scope, the id, the archive name or the proof by hand at the boundary — a second implementation is the drift that cost five rounds.

   **`<scope>` is the main worktree's directory basename**, resolved from git. Not the origin slug, which two different repos can share (`chroxy` and `chroxy-daemon` do), and never a `$PWD` prefix test, which reports the wrong answer from a linked worktree — where sessions actually run. Every worktree, subdirectory and detached HEAD of one repo therefore resolves to one seed. A session that is not in a repo at all is `fleet`, or `NEXT-fleet-<topic>.md` with `--topic`. Anything that is *not* "this is not a git repository" — a dubious-ownership refusal, a git too old for the flag — is a REFUSE rather than a fallback to `fleet`: filing the seed under a scope nobody reads looks exactly like success.

   **The session id is `--session`, else `$CLAUDE_CODE_SESSION_ID`, else a REFUSE.** There is no third source, and specifically no "most recently modified transcript" pick: that is fleet-wide, so on a machine running several sessions it names whichever session last wrote a turn — neither stable across the two places the id is used nor necessarily this session at all. A session that cannot name itself writes nothing: an anonymous seed is one the next session cannot archive (it reads as `unknown`) and this one cannot prove, so an unresolvable id is a reason to halt, not a value to carry. `$CLAUDE_CODE_SESSION_ID` truncated to 8 characters is exactly what `usage-benchmark-row.py` prints in artifact ①'s id column, so the seed and the benchmark row name the session with the same string.

   **Archive on collide — never overwrite a seed this session did not write.** If the canonical file exists carrying a different `session:`, the incumbent is renamed to `NEXT-<scope>.<UTC>-<sid>.md` (`-<n>` appended when two archives land in one second) and only then is the seed written. **The archive is what earns the right to write, so the write is conditional on it: an archive that fails aborts the step rather than falling through.** Unchecked, this destroys the incumbent with no race and no hostile actor — `rename(2)` needs the write bit on the *directory* while overwriting a file inside it does not, so a read-only handoff dir silently turns "archive then write" into "write over it". Re-running the same session's own write is not a collision and overwrites in place.

   Archiving preserves the incumbent byte for byte and frees the canonical name immediately, which is what keeps *"one line to paste"* working. Per-session-unique filenames would preserve the old seed too, and would destroy that affordance: the next session would have to be told which of N files to read, which is the thing the seed exists to avoid.

   Required header — `session:` is what makes archive-on-collide decidable *and* what step 3 reads back, so it is never decorative; `picks_up_at:` is the only line `/next` quotes:

   ```markdown
   ---
   type: handoff
   date: 2026-08-11T21:40Z          # full UTC timestamp
   scope: skill-templates           # the main worktree's directory basename, or fleet
   session: a1b2c3d4                # this session's id
   picks_up_at: "Extract the seed logic into a tested script (agent Sol)"
   sensitivity: public              # public | vault
   ---
   ```

   The script generates all of it; `session-seed.py header <path>` reads it back. The seed's own home is private, so `sensitivity: vault` needs no separate outlet; what still may not go in is a secret, in any file, ever.

2. **Usage checkpoint (artifact ①)** — capture cumulative parent and child usage at every end or continuation boundary with `python3 ~/.claude/scripts/usage-checkpoint.py --session "$CLAUDE_CODE_SESSION_ID" --run-id <stable-run-id> --status partial --out-dir ~/.claude/usage-history/checkpoints` (use `final` only when the session is truly finished). Checkpoints are immutable; `--aggregate-dir` selects the latest checkpoint per run/session, never their sum. The historical effective-unit benchmark row may be appended once via `usage-benchmark-row.py`, with its workload note and emitted suffixes retained; a session that delivered one package passes its tier (`--tier low`, `medium`, `high-single` or `high-panel`) and keeps the emitted `· cost:` suffix with the other two, and one whose suffix reads `over` says why in the workload note; a session that delivered several packages, or only part of one, passes no tier and says so in the note. If a row already exists, leave it intact; **still record the new checkpoint** so continued work is visible.
3. **Prove the seed the next session will read is *this* session's.** Step 1 already ran this proof and its verdict was step 1's exit code; run it again after anything that could have moved underneath you, and to re-print the paste line:

   ```bash
   python3 ~/.claude/scripts/session-seed.py verify     # + the same --topic the write used
   ```

   `seed:` must print and `REFUSE:` must not. The proof re-derives the scope, the handoff dir and the path from scratch in a fresh process — it is handed nothing the write computed — and then reads the seed's `session:` back. **Existence is not the property worth proving**: a file is at the canonical path in every failure mode this checklist has, and the two that matter fail in different halves.

   - **Wrong file.** The scope was keyed on something other than the main worktree — the *linked* worktree's basename is the near miss — so a perfectly well-formed seed sits at a path nobody opens while the previous session's stale seed still occupies the canonical name. Only re-deriving the scope catches this. **A check handed the write's own path reads back the very file the write misfiled, finds its own id, and passes — structurally incapable of failing for the mistake it exists to catch.**
   - **Right file, wrong author.** The archive was destroyed and overwritten, so the canonical path holds someone else's seed. Reading `session:` back is what distinguishes "I wrote the seed" from "a seed exists": the same field the archive decides on, used a second time as the proof.

   A bare `[ -f "$SEED" ]` calls both a pass, and an unresolvable session id is a REFUSE too — otherwise an empty id matches a seed with no `session:` line and the check passes on nothing. There is no commit to make, no branch to push, and no `cat-file` to run: the previous three rounds of this checklist all failed inside that machinery. Whether the vault repo itself is committed and pushed is ordinary vault hygiene, not a precondition — the seed already exists at a stable absolute path that nothing this session does can delete.
4. **Executive brief** — when a pulse delta crosses a WARN threshold or at package close, run `/visual-brief` into the vault (`$CLAUDE_BRIEF_DIR`) and open it. A warning is a reporting trigger, not a work-stopping gate.
5. **Capture learnings** — run `/learn` for genuinely novel lessons; "nothing novel" is a valid outcome, stated.
6. **Cleanup** — remove this session's worktrees (leave other sessions' worktrees alone), prune branches only after verifying each had a `MERGED` PR, stop dev daemons/servers started this session, restore any test-env mutations (none; this registry has no product service to stop).

   This step is **ungated on purpose**: `git worktree remove --force` deletes untracked files without prompting, and the seed is not in any worktree to be deleted. Anything else durable that got written into a worktree is committed and pushed before removal, or it is lost — so do not write durable things there.
7. **Closing message** — lead with the outcome, usable state and remaining gap from the seed. Include the verified absolute seed path (`seed:` from step 1) and any open PR number. End with the global `**Status:**` block and one `**Next:**` sentence. Both `Next` and `picks_up_at` name exactly one imperative task with executor `(agent name)` or `OWNER: name`; alternatives stay in the seed body, never as candidates in `Next`. Use exactly one of the four tokens: 🟢 RUNNING for authorized work actually continuing or an accepted continuation, ⚪ IDLE only when nothing waits on anyone, 🔴 BLOCKED whenever owner action, an external prerequisite or non-`none` DECISION remains, and 🟠 FAILED for a stopped job, budget, retry or host limit. Keep every pending choice in DECISION with `recommend:` and `default:`; a reserved choice stays blocked until answered, and its default records a recommended plan without granting execution authority. A required manual restart or owner QA is owner action and therefore BLOCKED. The stable seed path is the one line to paste when that restart is required; its existence alone is never evidence that work will continue.

### Follow-on protocol (when a task completes and work remains)

The canonical rules live in `~/.claude/CLAUDE.md` under **"Follow-on protocol"** — fold-in vs file-an-issue vs comment-and-skip. Follow them from there; this skill deliberately does not duplicate the text, so the global file stays the single source of truth. The one repo-local hook: filing a scoped follow-up goes through `/create-issue` where installed.

## Component skills (the bundle)

| Component | Role | If missing |
|---|---|---|
| `/catchup` | Reconstruct prior-session state at start | `skill add catchup` |
| `/visual-brief` | End-of-session HTML executive brief | `skill add visual-brief` |
| `/learn` | Persist novel lessons at end | `skill add learn` |
| `/create-issue` | File scoped follow-on issues | `skill add create-issue` |
| `/decide` | Select one next task or surface an owner-reserved choice | `skill add decide` |
| `/pulse` | Read and record offline boundary signals | `skill add pulse` |

Installing `session-lifecycle` should be followed by installing any missing components in the same pass — the bundle head without its components is a checklist that can't execute.

**The machine-level scripts back the End steps** and other skills; bootstrap them
together per machine because End step 1 and `/next` use the same installed copies:

```bash
mkdir -p ~/.claude/scripts ~/.claude/usage-history
cp assets/scripts/session-seed.py assets/scripts/session-pulse.py assets/scripts/usage-benchmark-row.py \
   assets/scripts/usage-checkpoint.py assets/scripts/usage_accounting.py \
   assets/scripts/usage-pace.py assets/scripts/usage-trend.py assets/scripts/filed-from.py \
   assets/scripts/review-result.py assets/scripts/rework-lag.py \
   assets/scripts/session-distill.py assets/scripts/pr-record.py \
   assets/scripts/gate-ledger.py ~/.claude/scripts/
cp assets/scripts/usage-trend.py assets/scripts/usage_accounting.py \
   ~/.claude/usage-history/
```

The second copy updates the existing scheduled `~/.claude/usage-history/usage-trend.py`
path and gives it a sibling shared module. Confirm that schedule before rollout;
neither copy command is run by installing this repository alone.

`session-seed.py` owns artifact ② (scope, session id, archive-on-collide, the write, the proof);
`session-pulse.py` imports that scope implementation and reports eight offline lines under
one shared subprocess deadline. It reads cached tests/CI, source-labelled signals and the
previous snapshot, without fetching or launching tests. `/pulse` persists a new snapshot
only through `session-seed.py write --refresh-pulse`, with the actual session ID; that mode
preserves the seed's date and body, carries decisions, and keeps archive and proof checks.
`usage-checkpoint.py` emits artifact ①'s cumulative measurement; `usage-benchmark-row.py`
emits the historical index row once; `usage-pace.py` answers "how much of the meter
week is spent", records meter readings, and — on macOS with the Claude desktop app — measures
the cap outright with `--calibrate`, by regressing spend against the meter samples the app
already writes every ~15 minutes. On a machine without that app the flag explains itself and
exits non-zero; every other path is unaffected and the cap falls back to a recorded reading.
`filed-from.py` (#268) owns the `Filed from:` linkage every skill-filed issue carries — `check`
flags an issue whose body has no valid line, `chain` walks the source chain (issue -> PR -> issue
filed from it -> ...) both ways — and is what makes "did this PR spawn work" and a rework chain
computable without a human re-reading every issue body. `review-result.py` (#267) owns the
structured review-result schema and the commands that produce, capture and read it
(`schema`/`validate`/`record`/`harvest`/`list`) — the machine-readable verdict a review skill's
final report carries, recorded beside the subagent sidecar rather than left as prose only.
`rework-lag.py` (#271) owns the LAGGING signal — did a merged PR get reworked later? — by
content-matching a PR's added lines against a later PR's removed lines rather than flagging any
later touch to the same file, which overcounts rework by roughly 10x; it reports a PR whose
rework window has not yet elapsed as `immature`, never as falsely `clean`, and reuses
`filed-from.py`'s `parse_filed_from` for its two issue-based measures instead of a second copy of
that grammar. `session-distill.py` (#269, epic #266) owns the asked -> understood/delivered ->
later-wrong chain per RUN — a run being one brief-to-final-report span, either a subagent
sidecar transcript (at either of review-result.py's two sidecar levels) or one human-turn span of
the MAIN transcript, because a distiller that reads only `subagents/**` cannot see anything a
session did on its own thread. Each run's evidence quality is classified against a CLOSED,
nine-label vocabulary — enforced in CODE, not trusted from the model's prompt-following: the
`--json-schema` handed to the model carries the label set as an enum, and the returned document
is re-checked against the same frozen label tuple before it is written, so an invented label
becomes `"unclassified"` with the offending string recorded rather than passed through.
`pr-record.py` (#270, epic #266) is the join table across all of the above: one JSON-line record
per merged PR, keyed on `(repo, pr)`, written at merge time from the session that merged (or
later, with `--session` given explicitly, for backfill). A session id is never searched for, only
validated once given — its main transcript must nominate the PR (the same nomination grammar
`rework-lag.py`'s `--attribute` uses, imported rather than copied), and an env-sourced session
additionally REFUSEs unless the PR's `mergedAt` falls inside that transcript's own span. An agent
is linked to the PR only with recorded evidence (its `.result.json`'s own `pr`, or its first
message naming the PR or its branch), never by session membership alone, and `rounds_missing`
makes visible what `review-result.py`'s no-overwrite-without-`--force` rule otherwise hides — a
PR reviewed three times by the same agent leaves only its last round on disk.
`gate-ledger.py` (#272, epic #266) records, for every gate — a `skill-guards.json` guard, a hook,
a CI step, a script-check, a doctrine rule — the failure mode it targets (a label from
`session-distill.py`'s closed vocabulary, imported rather than restated) and the evidence chain
that justified adding it, then joins that against `session-distill.py` output by exact
`(session, run)` and against `pr-record.py`'s ledger by exact `(repo, pr)` — no substring, no
fallback guessing either way. #263/#264 is the case it exists for: a guard was built for a frozen
sample file, the freeze was never real, and nothing recorded that the guard targeted a sensor
defect while the trace named a reasoning defect, so nothing could compare them. Each ships with a
sibling `<name>.test.sh` in
the registry, run by CI, and that is where their behaviour is pinned — this file states the
doctrine, not the code. Bootstrap all or none: a machine with a stale
`usage-benchmark-row.py` writes step 2's row on a different scale from every row above it, and
step 2 forbids repairing it; a machine without `usage-pace.py` silently has no pace check at all,
which is the failure the check exists to prevent.

**`meter` is an optional shell alias, not a shipped command.** The global rules refer to it
because it is short, but it is one line over `usage-pace.py` and nothing in the registry defines
it — a machine that bootstrapped only the scripts above has the script and not the alias. The
canonical, always-available form is the script; add the alias per machine if wanted:

```bash
meter() { python3 "$HOME/.claude/scripts/usage-pace.py" --record "$@"; }
```

Run with no arguments it prompts for the two `/usage` percentages, so neither form needs
placeholder substitution — which is the point: a documented command carrying `<angle brackets>`
is read by the shell as a redirection and cannot be run as written.
