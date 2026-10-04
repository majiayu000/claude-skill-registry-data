---
name: lfg
description: "User-invoked side-route for a proof of concept: short shaping conversation, then AFK to a stamped PR. Auto-sizes a one-off fix to a tiny path. Stops only for a credential, a destructive action, a spend, or a product fork. Not for production features, not for work you intend to keep without a later /pre-merge, not model-invoked."
disable-model-invocation: true
sources:
  primary:
    - "The Pragmatic Programmer — Andrew Hunt & David Thomas"
    - "Growing Object-Oriented Software, Guided by Tests — Freeman & Pryce"
  secondary:
    - "Shape Up — Ryan Singer"
    - "The Good News Factory — Kent Beck"
---

# LFG

Take an ask to a demoable proof of concept with one short conversation, then run
unattended to a reviewed PR.

The output is a **walking skeleton of tracer bullets**, not a prototype. Each slice
is thin, production-structured code that runs end to end, proven by one test that
also drives the demo path. What a run cuts is *completeness and robustness*, and
every cut is filed as an issue. It never cuts structure. That is the Hunt & Thomas
distinction between a tracer and a prototype, and it is why the code can later be
promoted or discarded by a human decision rather than by accident. Promotion needs
judgment from outside the run that built it (Beck's 3X: moving from Explore to
Expand is a call someone else makes).

## Invocation Position

**Side-route, user-invoked only.** It fires when a human types `/lfg <ask>`;
`disable-model-invocation: true` keeps its description out of every other
session's context. Use it when a demo window is closing, such
as a hackathon or a spike you want to show someone, and the full pipeline's
human gates would cost more than the build.

**Send it as its own message, not as the first message of a fresh workspace.**
A slash command is recognized only at the start of a message, and a host that
prepends anything to your first one — Conductor prepends a workspace preamble —
displaces it. The command is then read as ordinary prose, and because this skill
is hidden from the model by the flag above, the model cannot look it up: three of
the first six field invocations were lost this way, and the runs that followed
had no shape-lite, no marker, and no ledger. Nothing in this file can catch that,
because this file is what failed to load. If a session did work that looks like
an `/lfg` run but has none of those artifacts, this is why; retype `/lfg` and
start over (#383).

It stands beside `/shape` → `/research` → `/write-a-prd` → `/prd-to-issues` →
`/execute` and **reconnects to the main workflow at `/pre-merge --loop`**. From
there the PR is an ordinary stamped PR: the user settles its ledger, and
`/closeout` merges it if the user decides to keep the code.

Use the full pipeline instead for production features, and for any work you mean
to keep without a later human review.

**What this skill never does.** It never writes the review-currency stamp.
`/pre-merge` is that stamp's only writer, pinned by
`scripts/test-review-currency-marker.sh`. It never fixes a `/pre-merge` finding
in-run, never merges, never runs `/closeout` or `/compound`, and never creates
per-slice issues.

## Locked vocabulary

The recap, the gap issues, and the calibration in #372 read these values. Change
one here and nowhere else.

| Name | Value |
|---|---|
| Stop classes | defined once, in **Stops** below |
| Slice cap | 4 slices per run; slice 1 is always the walking skeleton |
| Attempt cap | 2 verification attempts per slice |
| Gap label | `lfg-gap` |
| Ledger transition this skill may write | `open → filed` |
| PR banner first line | `> **LFG proof of concept** — built unattended; not production-reviewed. Promote or discard by human decision.` |

## Stops

After shape-lite ends, ask the user a question only for one of these stop
classes:

- **credential**: an account, key, or login only the user can supply.
- **destructive**: an irreversible action, such as dropping data, force-pushing, or deleting something the run did not create.
- **spend**: anything that costs money, such as a paid tier, a purchase, or metered usage beyond a free tier.
- **product-fork**: two directions that would produce materially different demos, where the shape-lite summary does not settle which one.

For every other decision, take the recommended answer, keep going, and add the
decision to the recap's decision log. A question outside these classes stalls a
run that nobody is watching, which defeats the point of an unattended run.

A stop ends the turn, so it is an exit path (see **Exit paths**). Remove the marker
before you ask. When the user answers, run the marker-creation block again and
resume where the run stopped. Count every stop by class for the recap's tally.

## Process

### 0. Auto-size

Read the ask against the conditions in
[references/trivial-task-rule.md](references/trivial-task-rule.md). An ask typed
into `/lfg` is not tied to an issue, PRD, or QA bug unless the user named one.

- **Every condition holds → tiny path.**
- **Any one fails, or you are unsure → feature path.**

State the verdict and the condition that decided it in one line, then proceed
without asking.

**Branch.** Mirror `/execute` Step 0. If the host provisioned the worktree
(`.claude/settings.json` `worktree.provisioning: host`, or the block below prints
`host_owned=yes`), build on the current branch. Otherwise, create `lfg/<slug>`
from the default branch. This skill provisions no worktree of its own.

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

A bare `CONDUCTOR_WORKSPACE_PATH` is not enough: it leaks into shells started
under Conductor and can name another repository's workspace.

### Tiny path

1. Create the skip marker, exactly as the trivial rule directs:
   ```bash
   mkdir -p "$CLAUDE_PROJECT_DIR/.claude" && touch "$CLAUDE_PROJECT_DIR/.claude/.tdd-skipped"
   ```
2. Make the fix.
3. Run it. Execute whatever proves the fix: the command, the page, or the existing test. A fix you only read counts as unverified.
4. Remove the skip marker, then commit:
   ```bash
   rm -f "$CLAUDE_PROJECT_DIR/.claude/.tdd-skipped"
   ```
5. Run the feature path's Close step from item 3, **Open the PR**, skipping item 7. The tiny path creates no PRD-lite issue and no tracer test, so its recap omits those lines.

### Feature path

#### 1. Shape-lite (HITL, the only human phase)

1. State 3–5 assumptions you are making about the ask.
2. Ask `/shape` Phase 1's five questions, one per turn, each with your recommended answer. Point at `/shape` for the questions and do not rephrase them.
3. Print `/shape` Phase 3's closing summary in its four categories.

Stop there. Skip the rest of `/shape`: no name test, no branch walking, no stress
test of decisions. Human involvement ends when the summary is printed, and the
next question the user sees must belong to a stop class.

#### 2. Research-lite (AFK)

Run `/research` Phase 0 only, which covers the manifest version check and the
spec-anchor check. Write the result to the per-user archive at the path `/research`
uses. Resolve every `Uncertain` assumption toward the choice that keeps the demo
path shortest, and log it.

#### 3. PRD-lite issue (AFK)

File one GitHub issue with five sections: **Problem**, **Solution**,
**Rabbit Holes**, **No-gos**, and a **Slices** checklist. Slice 1 is the walking
skeleton, the thinnest path that runs end to end through every layer the demo
touches. The slice cap applies. File every slice past the cap as a gap issue (step
5) before building starts. Do not create per-slice issues.

**Reader:** `/pre-merge --loop` Phase 1 takes this issue's number as its PRD, and
the PR body's `Closes #N` closes it.

#### 4. Scaffold (AFK)

Invoke `/init-pipeline` and **declare Path B** in the invocation: say that no user
is present and that the trigger-surface question takes its default. Invoke it only
now, after shape-lite has ended. Otherwise it sees a present user, takes Path A,
and asks the trigger-surface question. If a hook is already installed, run
`/execute` Step 0's pipeline hooks gate and hand its verdict to `/init-pipeline`:
`hooks-stale` is Path C. Run the gate, do not restate it — it is the list of
terms that decides this, and a second copy of that list here is the drift
`docs/restated-claims.md` describes. Git guardrails stay on.

This matters more to this skill than to any other, because `.claude/.lfg-active`
is the newest marker: a project whose hook predates it accepts every other marker
and not this one, so the stand-down this step is about is exactly the one missing.
An inert marker does not fail loudly — the hook goes on refusing implementation
writes, and the refusal names `/tdd`, which the feature path does not use.

When `/init-pipeline` returns, create the run marker. This is the only
marker-creation block in this skill:

```bash
: "${CLAUDE_PROJECT_DIR:=$(git rev-parse --show-toplevel)}"
mkdir -p "$CLAUDE_PROJECT_DIR/.claude"
touch "$CLAUDE_PROJECT_DIR/.claude/.lfg-active"
```

While the marker exists, the classification hook stands down for implementation
writes. The feature path uses no `/tdd`, because the tracer test is the test.

#### 5. Build loop (AFK)

For each slice, in order:

1. Write the tracer test **outside-in**, against the running app, for the slice's demo path. Use [references/tracer-test.md](references/tracer-test.md) for the recipe.
2. Write the code that makes it pass.
3. Run the tracer test. Passing means the runner exits 0.
4. Commit the slice.

**Attempt cap.** A failed run in step 3 is one attempt. When a slice reaches the
attempt cap without a passing run, stop working it. Reduce it to a stub that keeps the skeleton wired,
commit the stub, file a gap issue, and move to the next slice. This is `/execute`'s
plateau stop rule at a smaller scale: attempts that do not advance end the slice
rather than earning another try.

**Filing a gap issue.** Use this for a slice past the slice cap, a slice stubbed
at the attempt cap, and each `open` ledger row in step 7. The body follows
`/execute`'s continuation-comment shape: what was done, what remains, the gotchas,
and the exact error output when an error caused it. Link the PRD-lite issue. The
label reader is the user deciding what to promote. Create the label if it is
missing (look up `gh label create --help` at runtime).

```bash
gh issue create --label "<gap label>" --title "<what was cut>" --body-file "$GAP_BODY_FILE"
```

#### 6. Prove (AFK)

Run the whole tracer suite in one invocation. The config in
`references/tracer-test.md` captures a screenshot for every test, so each passing
test leaves one under `test-results/`. For a non-web app, the proof is the
transcript file each tracer writes. Record every artifact path for the recap.

**Optional walk.** If `command -v agent-browser` resolves, walk the demo path once
and save a final screenshot. Load its current command reference with
`agent-browser skills get core` at runtime instead of writing commands from memory.
If it does not resolve, skip the walk, because the tracer screenshots already
prove the path.

#### 7. Close (AFK)

1. Remove the marker (see **Exit paths**, success path).
2. Commit anything outstanding.
3. **Open the PR** with the recap as its body (see **Recap**). The banner is the body's first line, and the body includes `Closes #<PRD-lite>` on the feature path.
4. Invoke `/pre-merge --loop`, passing the PRD-lite issue number, or "none" on the tiny path. Loop-mode updates the existing PR, reviews it, writes its ledger, and stamps it.
5. Read the PR body back. If the banner is no longer the first line, put it back with the guarded `mktemp` → fetch-with-exit-check → byte-count → edit → refuse-if-shorter → `gh pr edit --body-file` shape `/pre-merge` Phase 5 uses for its ledger.
6. For each ledger row in state `open`, file a gap issue and set that row's state to `filed` with the issue number, using the same guarded write. That is the ledger transition in **Locked vocabulary**, and the only ledger write this skill makes. Rows marked `fixed`, `accepted`, or `dropped` are decisions for the user.
7. Post one roll-up comment on the PRD-lite issue that lists every gap issue and the stop tally.
8. Print the handoff (see **Handoff**). Render no next-step menu: nobody is present to answer it, so the printed line is the whole handoff.

## Exit paths

The marker must not outlive the run, and removing it must come before
`/pre-merge --loop` writes the stamp. A stamped branch never carries a
classification marker, and the post-review edit lock depends on that. Every way
out of the feature path runs this block:

```bash
rm -f "$CLAUDE_PROJECT_DIR/.claude/.lfg-active"
```

- **Success path**: Close step 1, before the PR is opened and before `/pre-merge --loop`.
- **Stop path**: before asking the user any stop-class question. Recreate the marker with step 4's block when the run resumes.
- **Error path**: when something outside the attempt cap ends the run, such as a failed tool, a lost dev server, or an `/init-pipeline` that does not return. Remove the marker first. Then leave a comment on the PRD-lite issue in `/execute`'s continuation shape, with the exact error. If slices were committed, run Close from step 2 so the partial work still reaches `/pre-merge --loop`.

## Recap

The PR body is the recap, and its reader is the user deciding whether to demo,
promote, or discard. It carries, in this order:

1. The banner first line, then a `cut:` line naming what the run left out and a `gaps:` line linking the gap issues.
2. **Decisions taken without you**, one line each, including every assumption resolved in research-lite.
3. **Stop tally**, with each stop by class. A stop outside the stop classes is a defect in the run, so list it anyway.
4. **Proof**, with each screenshot or transcript path and the command that produced it.
5. On the feature path, `Closes #<PRD-lite>`.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "This choice is important enough to ask about." | If it is not a stop class, pick the recommendation and log it. The recap is where the user reviews it. |
| "It's a proof of concept, so skip the test." | The tracer test is what makes "demoable" a checked claim. Without it, the demo is an assertion. |
| "One more attempt will fix this slice." | The attempt cap exists because a run cannot tell progress from churn. Stub it, file it, and move on. |
| "I'll leave the marker; `/pre-merge` runs right after." | The stamp must land on a branch with no marker. Remove it first on every path. |
| "This slice is small, so I can fit a fifth." | The slice cap is the appetite. File the extra slice as a gap issue. |
| "The finding is trivial, so I'll fix it now." | Loop-mode findings belong to the user. File each open row, and never fix it in-run. |

## Red Flags

- A question to the user after shape-lite that names no stop class.
- A tracer test that never ran, or a slice committed without a passing run or a gap issue.
- `.claude/.lfg-active` present when `/pre-merge --loop` starts, or present after the run ends.
- A ledger row this skill set to anything other than `filed`.
- A PR body whose first line is not the banner.
- Per-slice issues, a `/tdd` invocation on the feature path, or a `/closeout`.

## Handoff

- **Expected input:** an ask typed as `/lfg <ask>`, plus a user present for shape-lite on the feature path.
- **Produces:** a stamped PR whose body is the recap (banner, decisions, gap issues, stop tally, proof paths); a PRD-lite issue on the feature path; gap issues carrying the gap label; `open` ledger rows moved to `filed`.
- **May invoke:** `/init-pipeline` (Path B), `/pre-merge --loop`.
- **Returns control to:** the user, who demos the branch and then decides whether to promote or discard it.
- **Comes next by default:** the user. To keep the code, settle the ledger and run `/closeout`. To discard it, close the PR.

Print, substituting the real values:

```
**Next session:** /closeout
**Input:** PR #<n> on branch <branch-name> — an LFG proof of concept; read its banner and ledger before merging
```
