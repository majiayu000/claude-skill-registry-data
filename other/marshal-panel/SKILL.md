---
name: marshal-panel
description: >
  Run an adversarial review panel on a plan, a diff, or a commit range, and decide what to do
  with what comes back. A thin, opinionated front end to marshal-adversarial-review: how to
  invoke it, how to route lenses across models, which fields mean a lens is missing rather than
  satisfied, and why a unanimous panel is still not a decision. Use before a risky integrate,
  before opening a PR on a repo you do not own, or on a plan you are about to commit to.
  Trigger on "run a panel", "adversarial review", "review this before I open the PR",
  "second opinion on this diff".
---

# Adversarial panel

The engine fans out and collects. It computes no verdict, and you should not act as though it
did. `marshal-adversarial-review` has the mechanism; this is the operating procedure around it.

## Input

Everything after the skill name is free text. Parse it into these, and resolve what is missing
rather than interrogating the user.

| Var | Shape | Missing -> |
|---|---|---|
| `SUBJECT` | `run:<run_id>` · `range:<base>..<head>` · `plan` (prose or a path) · `audit` (a repo path) | Infer from the working tree: uncommitted changes -> `range` against the tracking base; a plan file just written -> `plan`. Say which you picked. |
| `WORKSPACE` | a marshal workspace name | The repo you are in, via `list_workspaces`. |
| `TEAM` | a name from `list_teams()` | The declared team whose `target` matches `SUBJECT`. If none fits, author one (section 3). |
| `PATHS` | glob(s) to scope a large range | Unscoped, then react to `truncated`. |
| `ROUNDS` | int | 1. Cap at 2-3 ever, and stop if one objection survives twice. |

`SUBJECT` is the only one worth blocking on. A panel on the wrong subject costs N runs and tells
you nothing.

## 0. Before anything spawns

- **Commit first.** Worktrees branch off a commit, so uncommitted work is invisible to every
  reviewer. They will confidently review a file with your change missing from it.
- **`doctor`.** It checks auth, not just PATH. A logged-out backend answers `--version` and then
  dies a second into a real run.
- **Judge your outstanding runs.** A panel is worth nothing if the last batch was never assessed,
  and `routing` cannot rank clients it has no rejections for.

## 1. Keeping the fleet config out of a PR

If the subject is a branch destined for a repo you do not own, the panel's own config must not
appear in the diff.

1. Register the PR worktree as its own workspace: `marshal workspace add <name> <path>`. Do not
   reuse a workspace whose `worktree_setup` builds something unrelated.
2. Append `fleet.config.yaml`, `teams/`, `.marshal/` to `.git/info/exclude` **first**. Not
   `.gitignore`, which would itself be a diff line. `info/exclude` is local and invisible.
3. Verify against the PR's own file list, not `git status`.

## 2. Route each lens to a different model

Vary the **lens**, not the provider. On the same diff, an adversarial lens and a falsifiability
lens returned almost disjoint findings, while two providers holding the same lens returned the
same paragraph twice. Three roles on one client is three samples of one opinion.

A panel that has earned its keep:

| Lens | Ask it for | Model to route it to |
|---|---|---|
| tests | Per test: would this fail if the fix were deleted? Which of these pin nothing? | A strong reasoning model. This lens has repeatedly been the only one to catch a real behaviour flip. |
| contract | Every call site enumerated, not sampled. In-repo precedent that justifies or kills the design. | The model with the best evidence discipline you have. |
| spec | Each Definition-of-Done item walked, quoting the code that meets it. | A cheap model does fine on this narrow lens. |
| correctness | Line-by-line reading of the changed hunks. | Anything. Weight it lowest; it is the broadest lens and the vaguest. |

Two backend traps worth knowing before you trust a report:

- **A clean exit with no text is a missing lens.** One run returned empty after 508s and real
  money spent, with `status: empty` and `has_text: false`. Check `has_text` on every settled run.
- **Some CLIs truncate long final messages.** One measured case generated 11.4k output tokens and
  returned 266 characters. Read `report_path` or `read_run_file`, never the returned `review`
  string, for any backend you have seen do this.

## 3. Writing the lens

A role told to "review this" returns a polite paragraph that reads exactly like findings.

- **One lens per role.** Never "quality".
- **Name the failure modes to hunt.** "bool is an int subclass", "a str raises TypeError which
  the handler misses", "this test still passes with the fix deleted".
- **State the evidence bar.** "A worry with no input that triggers it is not a finding." "Call
  something blocking only with a cited rule clause or a concrete failing input."
- **Read-only clients only.** A reviewer that can edit is not a reviewer.

## 4. Run it

`list_teams()` shows the declared panels and each role's client. A team lives in
`<repo>/teams/<name>.yaml`, one lens per role:

```yaml
description: what this panel is for
target: range          # run | plan | range | audit - must match what you pass
roles:
  - name: tests
    client: <a read-only client from this workspace's fleet.config.yaml>
    rubric: |
      <the lens, written per section 3>
```

Then:

```
run_team(name="<team>", target="range", base="<base>", head="HEAD", paths=[...])
run_team(name="<team>", target="run",   run_id="<candidate>")
run_team(name="<team>", target="plan",  text="<the plan>")
run_team(name="<team>", target="range", pr=<number>)
```

All roles go out under one task id, blind to each other. Expect a real panel to outlive a tool
timeout and land as a background task.

**Section 2 names models, not clients.** `roles[].client` must be a client declared in the
workspace's `fleet.config.yaml`, so every lens you want needs a `permission: read-only` entry
there pointing at the model you want holding it. A workspace with two read-only clients runs a
two-lens panel no matter how many rows the table has.

## 5. Reading the panel

Read `unified_report` to orient, then the individual reports for any objection that matters.

Three checks before trusting any of it:

- `incomplete_roles` - that lens is **missing**, not satisfied.
- `truncated` - the subject was cut at the tail, and git orders paths alphabetically, so `src/`
  and `tests/` are what get lost on a large diff. Scope with `PATHS` or split the review.
- `completed` and `status` per role - a role that did not finish is a missing lens. `has_text`
  is not on the panel payload; to check a role's run for emptiness, take its `run_id` and read
  `has_text` from `get_run`.

Then the part nothing automates:

1. Pull the actual claims out of each Blocking and Findings section.
2. A finding with a concrete failure case outranks a confidently phrased stylistic worry.
3. **Disagreement is the product.** One lens satisfied and another alarmed is where the risk is.
4. **Unanimity is not a decision.** In one measured review all three non-test lenses raised the
   same point and all three called it non-blocking; the right move was still to drop the change,
   because the issue had asked for exactly one invariant. Two lenses also disagreed outright on
   whether touching docs was scope creep, and the repo's CONTRIBUTING settled it, not the panel.

The repo's own rules outrank the panel every time. So does the issue text.

## 6. If the subject is a fleet run's diff

A passing suite is not evidence. **Mutation-test the tests before integrating:** invert the rule
the task was about and re-run. One branch from a strong model had 11 tests that all still passed
after its central invariant was inverted, because they sat behind a guard that never fired. A
free-tier sibling failed 6 of 9 on the same treatment, which is what real tests do. Model tier
did not predict which was which.

## 7. Close it out

- `set_outcome(run_id, "rejected"|"abandoned", note)` on everything you did not integrate.
  Declining to integrate leaves no trace, so a run you reviewed and binned looks identical to one
  nobody opened, and every client's integration rate reads 100% over a sample of judged runs that
  is mostly empty.
- Never show one reviewer another's report, and never re-run a panel with the earlier reports in
  the prompt. Independence is the only thing a panel has.
