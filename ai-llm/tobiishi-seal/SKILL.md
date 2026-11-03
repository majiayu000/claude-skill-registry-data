---
name: tobiishi-seal
description: |
  PM-posture terminal pipeline step. Validate the developer marker and real deferrals, take
  main's advance and run the suite for one repository, and join the audit set on both topologies.
  Invoke the delivery executable with the complete contract, independent role metadata and a
  literal caller-owned bookkeeping action. The tool owns delivery merges and delivery worktree/ref
  removal; the caller owns audit cleanup after proved success. Retain terminal output, exit,
  diagnostics and read-only recovery observations in halt_report.md on a delivery halt.
  Halt without prompting. Use when the chain reaches sealing after its audit fan-out ends.
  Do not use for an earlier stage or an interactive hand-driven merge.
license: MIT
metadata:
  version: "4.8.0"
  category: delivery
  risk: safe
---

# Tobiishi Seal

## Purpose

Seal the caller's change through `<CORE>/tools/deliver_change.py`, using the public interface in
`<CORE>/tools/deliver_change.md` § Invoke the executable and § Supply merge metadata and a literal
seal action. This skill owns readiness, advance/suite policy, audit joins, bookkeeping, terminal
validation, recovery reporting and audit cleanup. The executable owns delivery merges and removal
of delivery worktrees and their exact branch refs.

A real developer deferral is recorded verbatim as *sealed with deferrals*. Step 1 checks that it
is real; it does not decide whether it is right. The bookkeeping seal travels into instance `main`
through its delivery merge. Make no further commit on `main` after delivery.

**Produces:** the sealed carving and findings on instance `main`, delivery merges and proved
worktree/ref absence, followed by joined-audit cleanup on success; an existing-folder
`halt_report.md` with retained terminal and recovery evidence on halt.

## Input

**PM role only.** It runs under the `pm` agent (`<CORE>/tools/chain_development.py:160`, the `seal` step). If invoked outside a PM session,
stop and say: "tobiishi-seal is PM work — the flow's terminal seal+merge step."

- **The change key** `<YYYY-MM-DD>_<slug>` — the branch name, worktree suffix, and Tobiishi folder
  name. You know it from the invocation (the change you were asked to deliver).
- **The project name** `<project>` — the `system/projects/<project>/` folder (passed by the
  orchestrator). Needed to locate the right Tobiishi at Step 2
  (`system/projects/<project>/journey/tobiishi/<key>/`).

## One repo or two — resolve once, retain the complete contract

After locating the instance change worktree in Step 1, capture this command's complete JSON in a
stable directory outside every worktree scheduled for removal:

```bash
python3 "<CORE>/tools/development_path.py" resolve --strict --format json \
  --worktree "$WORKTREE" --project "<project>" --key "<key>"
```

Use the returned object whole in the configuration below, including every alias and
`delivery_repos`. The contract is owned by `<CORE>/tools/development_path.py` `build_contract`;
the accepted delivery domain is `<CORE>/tools/deliver_change.md` § Supply all contract fields.
A nonzero resolver exit halts `deliver-precondition-failed` before joining, sealing or delivery.

- **Relative:** run Steps 1, 1a and 1b, then the common caller. The executable runs seal → instance
  delivery → instance cleanup.
- **Fixed:** run Steps 1, 1a's no-suite call and 1b, with no advance or suite on either repository, then the same caller.
  The executable runs product delivery → product cleanup → seal → instance delivery → instance
  cleanup. Use separate metadata for each role; no cross-repository merge occurs. When delivery
  declares the product change branch empty, the product step removes it without a merge, and the
  seal then proves `delivered: instance` with `empty: product`.

Both paths delegate their complete delivery sequence to the executable. Its ordering and recovery
boundary are `<CORE>/tools/deliver_change.md` § Validate targets, observe landing, then remove only
delivered worktrees and § Read the terminal result and retained recovery state.

## Workflow

`<key>` below is the change key; `<project>` the project, both passed by the orchestrator.

### Step 1 — Derive paths and confirm preconditions

Read `git worktree list --porcelain` and locate the entry whose branch is
`refs/heads/<key>`. Record that entry's literal absolute worktree path as `WORKTREE`, including
spaces; never reconstruct it from a guessed directory. Resolve the contract above from that path.
Set `REPO_ROOT` to its `instance_repo`, and `TOBIISHI` to
`system/projects/<project>/journey/tobiishi`. Keep these absolute paths for all preceding gates.

**Move an earlier halt's uncommitted report aside first.** A seal that halted before its seal commit
wrote `halt_report.md` into `$WORKTREE/$TOBIISHI/<key>/` and left it uncommitted (§ *Where a halt
writes its report*); an earlier step's own report at that path is uncommitted too. Delivery
refuses a change worktree holding any untracked file, so a report left there halts every re-run of
this seal on its own report. Before any gate below, when
`git -C "$WORKTREE" status --porcelain -- "$TOBIISHI/<key>/halt_report.md"` prints `?? …`, move that
file to `$REPO_ROOT/system/logs/seal-halt-<key>-<UTC timestamp>.md` (ignored by git, kept for
reading) and name the new path in the outcome. A `halt_report.md` git tracks — a step
committed it — is left where it is.

The caller action runs in the instance change worktree on `<key>`. The executable runs from its
stable invocation directory and targets the contract's main checkouts. Confirm:

- `REPO_ROOT` has `main` checked out (`git -C "$REPO_ROOT" rev-parse --abbrev-ref HEAD` is `main`) —
  the merge target.
- The recorded worktree exists and is registered on `refs/heads/<key>` in
  `git -C "$REPO_ROOT" worktree list --porcelain`; the exact branch ref exists
  (`git -C "$REPO_ROOT" show-ref --verify --quiet refs/heads/<key>`).
- The active Tobiishi folder exists on the branch (`$WORKTREE/$TOBIISHI/<key>/change_request.md`).
- **The developer's closing marker commit is on the branch:**

  ```bash
  git -C "$WORKTREE" log main..<key> --format='%s' | grep -q "implementation complete"
  ```

  `development-implementation` § Step 3 owns that commit and its subject
  (`developer: <key> — implementation complete`). It is an empty marker commit whose body carries the
  run's whole record — the language resolution, the Step 1b review, and the developer's divergence
  notes — so its absence is not a missing formality but the loss of everything the developer stage
  produced besides code. It lands on the **pipeline** worktree for an external product too — the
  instance branch (`development-implementation` § *Where each commit goes*) — so this one check covers
  both paths.

- **Every deferral on the marker is real.** Read the marker's `Deferred:` lines — the bare lines of the
  body of the newest `developer: <key> — implementation complete` commit
  (`git -C "$WORKTREE" log -1 main..<key> --grep='<key> — implementation complete' --format=%B`). The
  `-1` and the `<key>` are both load-bearing. The key keeps out another change's marker carried onto
  the branch by a merge, which the chain also ignores. A re-closed branch carries more than one marker, and the newest supersedes the rest
  (`development-implementation` § Step 3, *A re-close makes a new marker*), so every mention of "the
  marker" in this skill means that newest one, which is also the one the chain read. A marker with none
  has nothing to check. Run the same four checks `development-code-integrity` § *Deferrals* runs, on each
  line, reading the same repositories — this is a check that the deferral is *real*, never that it is
  *right*:

  1. task `<N>` is a `### Task <N>` in `tl_instruction.md`;
  2. no delivered task is deferred, checked by `development-code-integrity` § *Deferrals*, check 2,
     including the evidence required when an earlier landing subject is corrected;
  3. a blocked task's case is in the tree as `change_spec.md` and `tl_instruction.md` state it, and a
     dependent task's `task <M>` is itself named by another `Deferred:` line;
  4. the `<record>` path exists on the branch.

**Halt** (`deliver-precondition-failed`) if `main` isn't checked out, or the branch/worktree/Tobiishi
folder is missing, **or a `Deferred:` line on the marker fails one of the four checks** → write
`halt_report.md` (for a deferral, naming the `Deferred:` line and the check it failed), do not seal, do
not merge, return `status: halt`. No new halt code: an unreal deferral is a precondition the branch does
not meet.

**Halt** (`missing-implementation-marker`) if the marker commit is absent → same treatment: no join,
no seal, no merge, no teardown. It carries its own reason code rather than
`deliver-precondition-failed` because the two are repaired by different people in different places —
a missing worktree is re-run upstream, a missing marker is the developer stage's record to reconstruct
— and the code is what the orchestrator hands the human. Sealing anyway is what happened once: the
substance sat scattered across per-task commit bodies in the **product** repository while this branch
carried nothing from the developer, and nothing between the two stages noticed.

### Step 1a — Take main's advance, then run the suite

The advance and the suite run in `$WORKTREE`, on branch `<key>`, on the one-repo path only. The
gate-tool call at the end of this step is made on both paths.

**The advance.** Take `main`'s advance onto the branch through the builder:

```bash
python3 "<CORE>/tools/commit_builder.py" --repo "$WORKTREE" advance --from main --actor pm \
  --surface "<supplied surface>" --co-authored-by "<supplied model identity>" \
  --reasoning-effort "<resolved runtime effort>"
```

An exit of `0` — with or without a commit — goes on to the suite below. It carries no `--bump`: a
branch never edits a version marker, the same reason Step 1b gives.

**A failed advance.** On a non-zero exit, read two things before aborting anything:

```bash
git -C "$WORKTREE" rev-parse -q --verify MERGE_HEAD          # a merge in progress?
git -C "$WORKTREE" diff --name-only --diff-filter=U          # its unmerged paths
```

Then, when a merge is in progress, `git -C "$WORKTREE" merge --abort`. Halt:

- `merge-conflict` — unmerged paths are present.
- `merge-hook-failed` — a merge is in progress with no unmerged paths.
- `deliver-precondition-failed` — no merge is in progress; quote the builder's stderr.

Write `halt_report.md`, return `status: halt`, and join, seal, merge and tear down nothing. It aborts
rather than leaving the merge in progress because the seal is halt-don't-ask — the branch owner
repairs the branch with the same `advance`.

**The suite.** Run `project.md`'s `Test command:` once, **through the gate tool** (§ *The call*, below),
from `$WORKTREE` — never from `<name>/`, since a card like this project's collects nothing under its
product root. Exit `0` passes. Any other exit from an issued suite halts
`deliver-precondition-failed`, naming the command, the exit code, and each failing case. A command
that collects no tests is a non-zero exit, and the advance commit stays on the branch either way.

**Deferrals.** When the marker reads `Suite: red`, a non-zero exit passes only if every failing case is
named by a marker `Failing:` line. Any case no line names halts as above.

**The call.** The tool runs the card's command in the environment the product's CI calls for, and
prints that environment as its first line. Read `<CORE>/prompts/gate_suite.md` and follow it: it owns
how the evidence is read, where the owner's ask comes from, and the three calls. Call it **once**, after
the advance and not before: the advance is what changes the tree the suite runs on. This skill's own
call, with the evidence file that recipe's Step 3 builds, is:

```sh invocation
python3 "<CORE>/tools/gate_suite.py" run \
  --worktree "<instance change worktree>" --project "<project>" --key "<key>" \
  --gate seal --inputs "<inputs file>" \
  > "<output file>" 2> "<error file>"
```

Where the owner's ask applies, the recipe's second call replaces it, with `--gate seal`. Write the
output and error files in the stable directory Step 2 names, outside every delivery worktree.

- **The line is the tool's, whole.** Copy the output file's first line, `Environment: …`, as printed.
  Never write one from the evidence you read, and never reuse the developer's or the integrity run's
  line: this run's suite is its own.
- **A refusal or an unreachable environment is no suite.** When the exit is non-zero and standard error
  ends with `The test command was not run, on the owner's Mac or anywhere else.`, nothing was issued: a
  refusal or an unreachable environment halts `deliver-precondition-failed`, quoting the first line of
  standard error and the `Environment:` line, with no join, no seal and no merge. Never run the card's
  command by hand, and never fall back to another environment. A failed suite keeps the rule above:
  the tool's exit is the suite's, and the deferral matching applies to it unchanged.
- **An environment that was not ready is no suite result either.** Read the run's lines by `<CORE>/prompts/gate_suite.md` § *Reading the run's lines*. When any of them begins `Environment: not-ready`, the run is not a failed suite, whatever its exit, and the deferral matching never applies to it. Halt `deliver-precondition-failed`, quoting that line, with no join, no seal and no merge. The environment line rule below does not change for such a run, because a run that was not ready seals nothing.

**The environment line.** The printed line is kept as `environment_line` in Step 2's bookkeeping,
written to the caller configuration in the stable directory before any delivery worktree can be
removed: for a product in its own repository the product worktree is removed before the instance seal
is made, and the line has to outlast it. That holds the line outside every worktree.

**The fixed path.** A product in its own repository runs no advance and no suite, and the call is
still made once, from the same place, as `invocation-no-inputs`. Nothing is probed or issued: the tool
prints `Environment: none — no suite ran` and exits `0`, and that line is the one kept.

```sh invocation-no-inputs
python3 "<CORE>/tools/gate_suite.py" run \
  --worktree "<instance change worktree>" --project "<project>" --key "<key>" \
  --gate seal \
  > "<output file>" 2> "<error file>"
```

The same call, on the one-repo path, serves a card with no command: `none`, `N/A`, a `validated by use`
verdict or a skill name (§ *No command*, below). The line is the same `Environment: none — no suite
ran`.

**No command.** A card whose `Test command:` names no command owes the advance alone, and no suite
runs: `none`, `N/A`, a `validated by use` verdict, or a skill name such as `skill-evals`. The gate tool is
still called, for its `Environment: none — no suite ran` line. Of these,
only `none` lets a `Suite: none` marker past the chain's implementation gate, so a product with no
code has its card set to `none`, not any of the others. On a `none` card with a `Behaviour: preserving` change on this path, re-run instead
every after-check in `tl_instruction.md`'s `#### Invariant gate` blocks that is a command, in its between-two-commits form (the
before-checks are meant to fail once the change has landed), from the product root
`tl_instruction.md` names (`$WORKTREE/<Product path>`), after the advance. A product in its own repo
takes no advance here, so code-integrity's re-check is its last. A reading-only check is not re-run. A failing command halts
`deliver-precondition-failed` as a failing suite would, naming the command and the invariant
(`<CORE>/doctrine/flow/change_classification.md` § *A product with no code*).

**Why.** The developer's `Suite:` line was measured before the advance, on a tree that is no longer the
one that merges. A conflict found here sits on the branch, where the work is, not on `main`'s checkout
after the seal. `commit_format.md` § *A branch takes `main`'s advance through `advance`* states the
rule.

### Step 1b — Join the audit branches

Runs on **both** paths (§ *One repo or two*). Run **in the worktree** (`$WORKTREE`, the instance
worktree, on branch `<key>`), **before** Step 2's folder move — every
`development-audit` branch carries `flow_findings/<step>.md` at the change-work folder's **pre-move**
path (`$TOBIISHI/<key>/flow_findings/<step>.md`); joining after the move would land it at a path that
no longer exists on the change branch.

Glob the set from the key alone — nothing is handed to this step that it cannot recompute (the same
convention `development-audit`'s own Step 0 names):

```bash
AUDIT_BRANCHES=$(git -C "$WORKTREE" for-each-ref --format='%(refname:short)' "refs/heads/<key>__audit-*")
```

**A missing audit branch is not a failure.** `development-audit is not a gate`
(`<CORE>/tools/chain_development.py` `gates=False`, `:157`) — an auditor may have died and `AUDIT_BRANCHES` may glob fewer than the audit launched (or
none). Join whatever the glob finds; an empty set skips this step entirely.

For **each** branch in `$AUDIT_BRANCHES`, merge it into `<key>` through the builder — one call per
branch (`commit_builder.py merge` takes one `--branch`; one sequential call per branch is the shape, never an
octopus merge, never a cherry-pick):

```bash
git -C "$WORKTREE" log <key>..<branch> --oneline   # branch commits for the merge body

python3 "<CORE>/tools/commit_builder.py" --repo "$WORKTREE" merge \
  --branch "<branch>" --target-branch "<key>" \
  --description "development-audit findings — <step audited>" \
  --branch-commits "<commit line 1>" ... \
  --actor pm \
  --merge-context "tobiishi-seal <key> — audit fan-out join" \
  --surface "<supplied surface>" --co-authored-by "<supplied model identity>" \
  --reasoning-effort "<resolved runtime effort>"
```

**No `--bump` on any of these merges.** The target is the change branch `<key>`, never `main` — a
branch never edits a version marker (`<CORE>/doctrine/governance/doctrine_structure.md`
§Versioning); the commit that lands a version bump on `main` is the executable's delivery merge, not this one.

A merge conflict here is not expected — each auditor writes only its own `flow_findings/<step>.md`
(`development-audit`'s own Critical Rules) — but is handled like any other merge failure:
`git -C "$WORKTREE" merge --abort`, then **halt** (`merge-conflict` / `merge-hook-failed`) — write
`halt_report.md`, leave every worktree and branch intact, return `status: halt`. Do **not** proceed to
Step 2 on a failed join.

### Step 2 — Prepare the common delivery invocation

Steps 1/1a/1b must finish before this recipe runs. Its bookkeeping input receives only the ordered
`Deferred:` lines already validated in Step 1; acceptance supplies an empty array.

Use one existing absolute directory outside every delivery worktree for the caller configuration
and a materialized `caller-delivery.py`. Write the exact `caller-delivery` block below into that
script, retaining its bytes. The configuration is a JSON object with these fields:

| Field | Supplied value |
|---|---|
| `core` | The executing run's resolved absolute `<CORE>`, outside delivery cleanup; its `tools/deliver_change.py`, `tools/commit_builder.py` and dependencies remain reachable. |
| `caller_source` | Absolute path of the adopted `SKILL.md` actually read, not an older pinned caller. Preparation extracts its `caller-seal-action` bytes once. |
| `contract` | The entire resolver JSON object from above. No projection or alias removal. |
| `merges` | An object keyed by exactly the contract roles: `instance`, or `product` and `instance`. Each record has the public shape below. |
| `bookkeeping` | The object below, using the executing run's supplied values. |

Each independent merge record requires string `description`, `merge_context`, `surface`, and
exactly one string `actor` or `authorizer`. The automated PM run supplies `actor: "pm"`.
Optional strings are `co_authored_by`, `reasoning_effort` and `claude_session`. Optional arrays of
strings are `branch_commits` and `bump`. Retain supplied values and order, empty arrays and optional
absence. Do not copy attribution from an example or fill omitted fields with defaults. These
fields and the builder's `path=patch|minor|major` bump format are owned by
`<CORE>/tools/deliver_change.md` § Supply merge metadata and a literal seal action.

Read preparation-time commit entries separately for each role with
`git -C "<that role's repo>" log main..<key> --oneline`. Choose each role's merge description and
context from its verified change; when real deferrals are present, the instance context says
*sealed with deferrals* and makes no green-suite claim. Obtain changed versioned files with
`git -C "<that role's repo>" diff --name-only main...<key>` and supply a bump entry for each one
under `core/`, `.claude/`, `skills/` or `system/` per
`<CORE>/doctrine/governance/versioning.md` § Bump semantics; skill levels follow
`<CORE>/doctrine/kaizen/skills.md` § The version's three digits. Keep branch markers unchanged.
**No bump names a product's file** — not in the `product` record, and not under `products/` in an
instance record. A product's version lines are its own content, which its tasks set, and the
builder refuses a bump on them (`<CORE>/doctrine/governance/versioning.md` § Whose artifacts).
No supplied commit list predicts the seal SHA: the action records its actual SHA after committing,
and the executable observes the new instance tip for landing.

Bookkeeping requires `date` (the run's seal date), `deferred` (the validated ordered line array),
`environment_line` (the first line this run's Step 1a gate-tool call printed, copied whole — never the
developer's or the integrity run's), `directional` (the full resolved directional line), `surface`, `co_authored_by` and
`reasoning_effort` (the supplied resolved runtime effort). Include `claude_session` only when the
run supplies one. Resolve `directional` under `<CORE>/doctrine/governance/commit_format.md`
§ Directional trailer; preserve its literal value. Preparation hands it to the builder's
`check-directional` before the tool runs, because the seal commits only after a product merge: a
line the builder would refuse halts `deliver-precondition-failed` with nothing merged.

Invoke the materialized block with the configuration path as one literal argument:

```bash
python3 "/absolute/stable/caller-delivery.py" "/absolute/stable/configuration.json"
```

The script creates and retains one absolute temporary directory. It copies the complete contract
and independent merge records without schema defaults, materializes the adopted action and action
configuration, and creates `seal.json` with an absolute Python executable and literal action argv.
Preparation executes no action; its one builder call is the read-only directional check. The actual tool invocation in `Caller.prepare` supplies
`--contract`, `--merges`, `--seal-action` and explicit `--builder`; `Caller.deliver` runs it once
from the stable temporary directory. Keep that directory, its input/configuration/action files,
`before.json`, `invocation.json`, `seal-evidence.json` and `result.json` through outcome handling.
No caller value is shell source.

The `caller-seal-action` block owns bookkeeping only: refuse a missing or empty `environment_line`
before it creates or moves anything, create the trail parent if absent, move the
whole folder before appending the result to the destination request — the `**Sealed:**` line, the
`environment_line` directly after it, then any deferral lines — retain every carving/finding,
mark only the existing current PM-context item Sealed, and use the builder to commit on the instance
branch. It declares both move prefixes and adds the edited request and existing context. It creates
no context when one is absent. The action emits the actual clean seal commit SHA. The executable
verifies that it extends the recorded instance tip before merging
(`<CORE>/tools/deliver_change.md` § Supply merge metadata and a literal seal action).

### Step 3 — Read the terminal result and retained recovery state

Read `result.json` and the returned JSON outcome from the actual process. Success requires exit zero
and the exact topology-appropriate three-line block from `<CORE>/tools/deliver_change.md`
§ Read the terminal result and retained recovery state. For a product in its own repository, one
second complete result is also proved: the four-line block `delivery: complete` /
`delivered: instance` / `empty: product` / `cleanup: complete`, each line ending in a newline, with
exit zero. `empty: product` is delivery's declaration that the product change branch carried no
commits of its own and was removed without a merge. A product inside the instance has no such second
result: the four-line block there halts `delivery-failed`, unproved. Only proved success makes audit
cleanup eligible. A valid halt retains its actual public code, delivered-role prefix, incomplete cleanup,
stdout, stderr and process exit. A missing, malformed or exit-inconsistent result halts
`delivery-failed`, marks landing unproved, and retains raw observations; launch failure has no
invented exit status.

On halt, return the actual `halt_report` path. The report retains recorded main/change tips and
read-only post-call disk, registration, exact-ref, merge-head and unmerged-index evidence, plus
observed main SHAs and their ordered parents. Failed observations are unavailable with diagnostics;
they do not prove absence. Intended landing is proved only when the observed ordered parents match
recorded old main and intended product tip or observed seal tip, with no merge in progress.
These observations never replace the tool's terminal verdict.

Stop the delivery path on any halt. Do not abort conflicts, roll back a landed product, retry the
seal/tool call, remove recovery worktrees/branches, or clean up audits. Preserve `teardown-failed`
after product landing. Advance and audit-join failure policy remains confined to Steps 1a/1b.

### Step 4 — Clean up joined audits only after proved delivery success

The executable has proved delivery worktree/ref absence. Remove only the exact audit branches
successfully joined in Step 1b; keep that list through delivery, never rediscover it with a glob.
Save the executable recipe below in the stable invocation directory and run it with `REPO_ROOT`,
`<key>`, and that joined list as separate argv elements. It reads literal registered paths, including
spaces and nested checkouts. It validates the entire set before removing anything, and rechecks each
entry immediately before removal. No joined audits means an empty list and no cleanup effects.

<!-- caller-audit-cleanup -->
```python
#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys

__version__ = "1.0.0"


def git(repo: str, *args: str) -> str:
    result = subprocess.run(["git", "-C", repo, *args], capture_output=True,
                            text=True, encoding="utf-8", errors="surrogateescape")
    if result.returncode:
        raise ValueError(f"{repo}: git {args!r}: {result.stderr.strip()}")
    return result.stdout


def registrations(repo: str) -> list[dict[str, str]]:
    records = []
    for block in git(repo, "worktree", "list", "--porcelain", "-z").split("\0\0"):
        if block:
            records.append(dict(field.partition(" ")[::2] for field in block.split("\0")
                                if field))
    return records


def checked_path(repo: str, branch: str) -> str:
    matches = [record for record in registrations(repo)
               if record.get("branch") == f"refs/heads/{branch}"]
    if len(matches) != 1 or any(flag in matches[0] for flag in ("locked", "prunable")):
        raise ValueError(f"{branch}: expected one usable registered audit worktree")
    path = matches[0]["worktree"]
    if git(path, "symbolic-ref", "--quiet", "HEAD").strip() != f"refs/heads/{branch}":
        raise ValueError(f"{path}: audit branch identity changed")
    if git(path, "status", "--porcelain", "--untracked-files=all"):
        raise ValueError(f"{path}: audit worktree has uncommitted changes")
    git(repo, "merge-base", "--is-ancestor", f"refs/heads/{branch}", "refs/heads/main")
    return path


def cleanup(repo: str, key: str, branches: list[str]) -> None:
    if len(set(branches)) != len(branches) or any(
        not branch.startswith(f"{key}__audit-") for branch in branches
    ):
        raise ValueError("expected unique joined audit branches for this change")
    if git(repo, "symbolic-ref", "--quiet", "HEAD").strip() != "refs/heads/main":
        raise ValueError("audit cleanup requires the delivered main checkout")
    paths = [(branch, checked_path(repo, branch)) for branch in branches]
    for branch, path in paths:
        if checked_path(repo, branch) != path:
            raise ValueError(f"{branch}: registered path changed before cleanup")
        git(repo, "worktree", "remove", path)
        git(repo, "branch", "-d", branch)
        if any(record.get("worktree") == path or
               record.get("branch") == f"refs/heads/{branch}" for record in registrations(repo)):
            raise ValueError(f"{branch}: audit registration survived cleanup")
        if git(repo, "for-each-ref", "--format=%(refname)", f"refs/heads/{branch}"):
            raise ValueError(f"{branch}: audit ref survived cleanup")


def main(argv: list[str] | None = None) -> int:
    arguments = sys.argv[1:] if argv is None else argv
    try:
        if len(arguments) < 2:
            raise ValueError("supply the main checkout, change key and joined audit branches")
        cleanup(arguments[0], arguments[1], arguments[2:])
        return 0
    except (OSError, ValueError, KeyError) as error:
        print(f"error: teardown-failed: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
```

A nonzero exit halts `teardown-failed`; record stderr and observed survivors in the halt report.
Preserve already-delivered history and remaining audit state; never force deletion. Delivery-worktree
cleanup is never repeated here. This recipe replaces the reconstructed-path shell loop.

### Step 5 — Return the outcome

Return the step-outcome message under `<CORE>/doctrine/flow/step_outcome_contract.md`, using the
actual report path for halt. Make no further commit on `main` after delivery.

## Where a halt writes its report

Use existing destinations only: the retained instance worktree's active change folder before the
move, or its trail folder after the move. If the delivery worktree is absent, use the primary
instance's existing active folder; if that is absent too, use the existing project's tobiishi root.
Recreate neither a removed worktree nor an active change folder. A report in the worktree's active
change folder is not committed, so a re-run of this seal moves it aside before its first gate (Step 1). The `Caller._report_directory`
recipe below implements this order and returns the path actually written. The same placement
applies to pre-delivery halts in Steps 1/1a/1b, and `Caller.refuse` applies it when preparation
refuses before the executable runs.

## Outputs

| Effect | Produced when |
|---|---|
| Main's advance and suite result on the branch | Relative path, Step 1a |
| Audit findings joined on the instance branch | Both topologies, Step 1b |
| Whole-folder seal, acceptance or verbatim deferrals, existing PM item Sealed, clean new branch commit | Caller action invoked by the executable |
| Delivery merges and proved delivery disk/registration/ref absence | Executable complete result |
| Joined audit cleanup | Proved delivery success only, Step 4 |
| Existing-folder halt report, raw terminal observations and read-only recovery evidence | Any halt; delivery halts perform no automatic recovery or audit cleanup |

## Critical Rules

- PM posture only; no seal without the newest developer closing marker or over an unreal deferral.
- Resolve the complete development-path contract once. Both topologies use the same tool invocation.
- Keep relative advance/suite policy and both-topology audit joins before invocation. The suite goes
  through the gate tool, and its printed `Environment:` line is carried in the bookkeeping to the seal's
  record; a refusal or an unreachable environment is a halt, never a pass.
- Keep the builder, inputs, action and its dependencies outside delivery cleanup. Execute from a
  stable absolute directory; materialize the adopted action once before its source can disappear.
- Keep supplied runtime attribution, optional absence, role-specific values and ordered entries.
- Caller bookkeeping moves the whole carving before editing the destination; it commits only on
  the instance branch and emits its actual seal SHA. It performs no delivery merge or cleanup.
- Delivery merges and delivery-worktree/ref removal belong exclusively to the executable.
- Read the complete terminal block together with process exit. Keep every public halt code distinct
  and preserve raw unproved results and unavailable evidence.
- Delivery halt means no abort, rollback, retry, recovery teardown or audit cleanup. Report partial
  landings without rewriting the tool verdict.
- Audit cleanup follows proved delivery success only. No post-delivery commit on `main`.
- Halt without prompting, write in an existing destination, and return the actual report path.

## Runnable caller recipes

These are the executed subject, not illustrative pseudocode. Materialize `caller-delivery` as
specified in Step 2. It extracts and materializes `caller-seal-action` from `caller_source`.
The process and filesystem ports are supplied to their callers; production builds them only at the
entry point, and controlled-result tests supply recording fakes through those same parameters.

<!-- caller-delivery -->
```python
#!/usr/bin/env python3
"""Materialize a literal bookkeeping action and retain delivery observations outside cleanup."""
from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

__version__ = "1.0.0"


class State(str, Enum):
    COMPLETE = "complete"
    HALT = "halt"


class Role(str, Enum):
    PRODUCT = "product"
    INSTANCE = "instance"


class Halt(str, Enum):
    PRECONDITION = "deliver-precondition-failed"
    CONFLICT = "merge-conflict"
    HOOK = "merge-hook-failed"
    PARTIAL = "instance-merge-after-product"
    TEARDOWN = "teardown-failed"
    DELIVERY = "delivery-failed"


def terminal_result(observation: dict, roles: tuple[Role, ...]) -> dict:
    """Recognize only a complete public block for these roles and its matching process exit."""
    delivered = ",".join(role.value for role in roles)
    completes = {f"delivery: complete\ndelivered: {delivered}\ncleanup: complete\n": delivered}
    if roles == (Role.PRODUCT, Role.INSTANCE):
        completes["delivery: complete\ndelivered: instance\nempty: product\n"
                  "cleanup: complete\n"] = Role.INSTANCE.value
    if observation["exit"] == 0 and observation["stdout"] in completes:
        return {"state": State.COMPLETE, "delivered": completes[observation["stdout"]],
                "cleanup": "complete", "code": None, "proved": True}
    prefixes = ["none"] + [",".join(role.value for role in roles[:size])
                            for size in range(1, len(roles) + 1)]
    if observation["exit"] == 1:
        for code in Halt:
            for prefix in prefixes:
                block = (f"delivery: halt\nhalt: {code.value}\ndelivered: {prefix}\n"
                         "cleanup: incomplete\n")
                if observation["stdout"] == block:
                    return {"state": State.HALT, "delivered": prefix, "cleanup": "incomplete",
                            "code": code, "proved": True}
    return {"state": State.HALT, "delivered": "unproved", "cleanup": "unproved",
            "code": Halt.DELIVERY, "proved": False}


class Files:
    def __init__(self, root: Path) -> None:
        self.root = root.resolve()

    def read(self, path: Path) -> str:
        return path.read_text(encoding="utf-8")

    def write(self, path: Path, content: str) -> None:
        path.write_text(content, encoding="utf-8")

    def directory(self) -> Path:
        return Path(tempfile.mkdtemp(prefix="seal-caller-", dir=self.root)).resolve()

    def exists(self, path: Path) -> bool:
        return path.exists()

    def is_directory(self, path: Path) -> bool:
        return path.is_dir()


class Processes:
    def run(self, argv: list[str], *, cwd: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(argv, cwd=cwd, capture_output=True, text=True)


@dataclass(frozen=True)
class Prepared:
    directory: Path
    configuration: dict
    argv: list[str]
    before: dict


class Caller:
    def __init__(self, *, files: Files, processes: Processes) -> None:
        self.files = files
        self.processes = processes

    def _json(self, path: Path, value: object) -> None:
        self.files.write(path, json.dumps(value, indent=2, ensure_ascii=False) + "\n")

    def _observe(self, repo: Path, *arguments: str) -> dict:
        argv = ["git", "-C", str(repo), *arguments]
        try:
            result = self.processes.run(argv, cwd=self.files.root)
            absence_check = arguments[:3] == ("show-ref", "--verify", "--quiet") or (
                arguments == ("rev-parse", "-q", "--verify", "MERGE_HEAD")
            )
            available = result.returncode == 0 or (absence_check and result.returncode == 1)
            return {"argv": argv, "available": available,
                    "exit": result.returncode, "stdout": result.stdout, "stderr": result.stderr}
        except OSError as error:
            return {"argv": argv, "available": False, "exit": None,
                    "stdout": "", "stderr": str(error)}

    def _snapshot(self, contract: dict) -> dict:
        records = {}
        for role in ("product", "instance") if contract.get("kind") == "fixed" else ("instance",):
            if not all(isinstance(contract.get(f"{role}_{name}"), str)
                       for name in ("repo", "worktree")):
                continue
            repo, worktree = Path(contract[f"{role}_repo"]), Path(contract[f"{role}_worktree"])
            try:
                disk = {"available": True, "present": self.files.exists(worktree)}
            except OSError as error:
                disk = {"available": False, "present": None, "diagnostics": str(error)}
            records[role] = {
                "repo": str(repo), "worktree": str(worktree), "disk": disk,
                "main_head": self._observe(repo, "rev-parse", "--verify", "refs/heads/main"),
                "change_head": self._observe(worktree, "rev-parse", "--verify", "HEAD"),
                "main_parents": self._observe(repo, "show", "-s", "--format=%P", "main"),
                "registrations": self._observe(repo, "worktree", "list", "--porcelain"),
                "change_ref": self._observe(repo, "show-ref", "--verify", "--quiet",
                                            "refs/heads/" + str(contract.get("key", ""))),
                "primary_merge_head": self._observe(
                    repo, "rev-parse", "-q", "--verify", "MERGE_HEAD"
                ),
                "primary_unmerged": self._observe(repo, "ls-files", "-u"),
                "change_merge_head": self._observe(
                    worktree, "rev-parse", "-q", "--verify", "MERGE_HEAD"
                ),
                "change_unmerged": self._observe(worktree, "ls-files", "-u"),
            }
        return records

    def prepare(self, path: Path) -> Prepared:
        """Copy public inputs unchanged; extract the adopted action once without executing it."""
        configuration = json.loads(self.files.read(path.resolve()))
        contract = configuration["contract"]
        directory = self.files.directory()
        core = Path(configuration["core"]).resolve()
        builder = core / "tools/commit_builder.py"
        delivery = core / "tools/deliver_change.py"
        for name in ("instance_worktree", "product_worktree"):
            value = contract.get(name)
            if isinstance(value, str):
                removed = Path(value).resolve()
                if any(location.is_relative_to(removed) for location in (directory, core)):
                    raise ValueError("caller inputs, executable and builder must survive cleanup")
        # The seal commits after the product merge, so a directional the builder would refuse
        # is refused here, while nothing has landed.
        check = self.processes.run(
            [sys.executable, str(builder), "--repo", contract["instance_worktree"],
             "check-directional", "--directional", configuration["bookkeeping"]["directional"]],
            cwd=directory,
        )
        if check.returncode:
            raise ValueError(f"bookkeeping.directional refused: {check.stderr.strip()}")
        for name in ("contract", "merges"):
            self._json(directory / f"{name}.json", configuration[name])
        source = self.files.read(Path(configuration["caller_source"]))
        matches = re.findall(r"<!-- caller-seal-action -->\n```python\n(.*?)\n```", source, re.S)
        if len(matches) != 1:
            raise ValueError("adopted source must contain exactly one caller-seal-action block")
        self.files.write(directory / "action.py", matches[0] + "\n")
        self._json(directory / "action-config.json", {
            "contract": contract, "bookkeeping": configuration["bookkeeping"],
            "builder": str(builder), "evidence": str(directory / "seal-evidence.json"),
        })
        self._json(directory / "seal.json", {"argv": [
            sys.executable, str(directory / "action.py"), str(directory / "action-config.json"),
        ]})
        argv = [sys.executable, str(delivery), "--contract", str(directory / "contract.json"),
                "--merges", str(directory / "merges.json"),
                "--seal-action", str(directory / "seal.json"), "--builder", str(builder)]
        self._json(directory / "invocation.json", {"argv": argv, "cwd": str(directory),
                                                   "caller_source": configuration["caller_source"]})
        before = self._snapshot(contract)
        self._json(directory / "before.json", before)
        return Prepared(directory, configuration, argv, before)

    def _seal_evidence(self, prepared: Prepared) -> dict:
        path = prepared.directory / "seal-evidence.json"
        try:
            if not self.files.exists(path):
                return {"available": False, "diagnostics": "no action evidence recorded"}
            return {"available": True, **json.loads(self.files.read(path))}
        except (OSError, ValueError, TypeError) as error:
            return {"available": False, "diagnostics": str(error)}

    def _recovery(self, prepared: Prepared, evidence: dict) -> dict:
        records = self._snapshot(prepared.configuration["contract"])
        for role, record in records.items():
            prior = prepared.before.get(role, {})
            old = prior.get("main_head", {})
            intended = (prior.get("change_head", {}).get("stdout", "").strip()
                        if role == "product" else evidence.get("seal_sha"))
            head, parents = record["main_head"], record["main_parents"]
            merge_head = record["primary_merge_head"]
            known = (old.get("exit") == 0 and head["exit"] == 0 and parents["exit"] == 0
                     and bool(intended) and merge_head["available"])
            record["intended_landing"] = (
                head["stdout"].strip() != old.get("stdout", "").strip()
                and parents["stdout"].split() == [old["stdout"].strip(), intended]
                and merge_head["exit"] == 1
            ) if known else None
            record["intended_tip"] = intended
        return records

    def _report_directory(self, contract: dict) -> Path:
        worktree = Path(contract["instance_worktree"])
        root = Path("system/projects") / contract["project"] / "journey/tobiishi"
        key = contract["key"]
        if self.files.is_directory(worktree):
            candidates = [worktree / root / key, worktree / root / "trail" / key]
        else:
            candidates = [Path(contract["instance_repo"]) / root / key]
        candidates.append(Path(contract["instance_repo"]) / root)
        for candidate in candidates:
            if self.files.is_directory(candidate):
                return candidate
        raise OSError(
            "no existing change folder or primary tobiishi root can hold halt_report.md"
        )

    def _report(self, contract: dict, outcome: dict) -> None:
        path = self._report_directory(contract) / "halt_report.md"
        outcome["halt_report"] = str(path)
        content = (f"# Delivery halt — {outcome['halt_reason']}\n\n"
                   f"Delivered: {outcome['delivered']}\nCleanup: {outcome['cleanup']}\n"
                   f"Terminal landing proved: {outcome['landing_proved']}\n\n"
                   "The captured terminal verdict is retained. Recovery observations below are "
                   "read-only; unavailable observations carry their diagnostics.\n\n```json\n")
        content += json.dumps(outcome, indent=2, ensure_ascii=False) + "\n```\n"
        self.files.write(path, content)

    def refuse(self, path: Path, error: Exception) -> dict:
        """Report a preparation refusal where a delivery halt would go; no tool ran."""
        contract = json.loads(self.files.read(path.resolve()))["contract"]
        outcome = {"step": "tobiishi-seal", "key": contract.get("key"), "artifact": None,
                   "status": "halt", "halt_reason": Halt.PRECONDITION.value,
                   "observations": {"exit": None, "stdout": "",
                                    "stderr": f"preparation refused before delivery: {error}"},
                   "delivered": "none", "cleanup": "incomplete",
                   "audit_cleanup_eligible": False, "landing_proved": False}
        self._report(contract, outcome)
        return outcome

    def deliver(self, prepared: Prepared) -> dict:
        """Invoke once; accept proved terminal results and perform no recovery effects on halt."""
        try:
            result = self.processes.run(prepared.argv, cwd=prepared.directory)
            observation = {
                "exit": result.returncode, "stdout": result.stdout, "stderr": result.stderr,
            }
        except OSError as error:
            observation = {"exit": None, "stdout": "", "stderr": str(error)}
        contract = prepared.configuration["contract"]
        roles = (
            (Role.PRODUCT, Role.INSTANCE) if contract.get("kind") == "fixed" else (Role.INSTANCE,)
        )
        terminal = terminal_result(observation, roles)
        success = terminal["state"] == State.COMPLETE
        outcome = {"step": "tobiishi-seal", "key": contract.get("key"), "artifact": None,
                   "status": "ok" if success else "halt", "observations": observation,
                   "delivered": terminal["delivered"], "cleanup": terminal["cleanup"],
                   "audit_cleanup_eligible": success,
                   "landing_proved": terminal["proved"]}
        evidence = self._seal_evidence(prepared)
        outcome["seal_evidence"] = evidence
        if not success:
            outcome["halt_reason"] = terminal["code"].value
            outcome["recorded_before"] = prepared.before
            outcome["recovery"] = self._recovery(prepared, evidence)
            self._report(prepared.configuration["contract"], outcome)
        self._json(prepared.directory / "result.json", outcome)
        return outcome


def main(argv: list[str] | None = None) -> int:
    arguments = sys.argv[1:] if argv is None else argv
    if len(arguments) != 1:
        print("error: supply the caller configuration JSON path", file=sys.stderr)
        return 1
    caller = Caller(files=Files(Path(tempfile.gettempdir())), processes=Processes())
    try:
        prepared = caller.prepare(Path(arguments[0]))
    except (OSError, ValueError, KeyError, TypeError) as error:
        try:
            outcome = caller.refuse(Path(arguments[0]), error)
        except (OSError, ValueError, KeyError, TypeError, AttributeError) as unplaced:
            print(f"error: {error}; no halt report placed: {unplaced}", file=sys.stderr)
            return 1
        print(json.dumps(outcome, ensure_ascii=False))
        print(f"error: {outcome['halt_reason']}; inspect {outcome['halt_report']}",
              file=sys.stderr)
        return 1
    try:
        outcome = caller.deliver(prepared)
        print(json.dumps(outcome, ensure_ascii=False))
        if outcome["status"] != "ok":
            print(f"error: {outcome['halt_reason']}; inspect {outcome['halt_report']}",
                  file=sys.stderr)
            return 1
        return 0
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
```

<!-- caller-seal-action -->
```python
#!/usr/bin/env python3
"""Caller-owned bookkeeping; delivery and recovery remain outside this action."""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

__version__ = "1.0.0"


class Processes:
    def run(self, argv: list[str], *, cwd: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(argv, cwd=cwd, capture_output=True, text=True)


class Files:
    def read(self, path: Path) -> str:
        return path.read_text(encoding="utf-8")

    def write(self, path: Path, content: str) -> None:
        path.write_text(content, encoding="utf-8")

    def exists(self, path: Path) -> bool:
        return path.is_file()

    def ensure_directory(self, path: Path) -> None:
        path.mkdir(parents=True, exist_ok=True)


class SealAction:
    def __init__(self, *, files: Files, processes: Processes) -> None:
        self.files = files
        self.processes = processes

    def _run(self, worktree: Path, argv: list[str]) -> str:
        result = self.processes.run(argv, cwd=worktree)
        if result.returncode:
            raise OSError(f"{argv!r} exited {result.returncode}: {result.stderr}")
        return result.stdout

    def seal(self, configuration: Path) -> dict:
        supplied = json.loads(self.files.read(configuration))
        contract, bookkeeping = supplied["contract"], supplied["bookkeeping"]
        worktree = Path(contract["instance_worktree"])
        project, key = contract["project"], contract["key"]
        environment = bookkeeping.get("environment_line")
        if not isinstance(environment, str) or not environment.strip():
            raise ValueError("bookkeeping.environment_line is required: the seal's suite run "
                             "printed no environment line")
        root = Path("system/projects") / project / "journey/tobiishi"
        source, destination = root / key, root / "trail" / key
        self.files.ensure_directory(worktree / destination.parent)
        self._run(worktree, ["git", "-C", str(worktree), "mv", str(source), str(destination)])
        request = destination / "change_request.md"
        deferred = bookkeeping["deferred"]
        verdict = "sealed with deferrals" if deferred else "accepted"
        record = (f"\n**Sealed:** {bookkeeping['date']} — {verdict}; "
                  "merged to `main` via `--no-ff`.\n")
        record += environment.rstrip("\n") + "\n"
        record += "".join(line + "\n" for line in deferred)
        self.files.write(worktree / request, self.files.read(worktree / request) + record)
        edited = [str(request)]
        context = Path("system/projects") / project / "contexts/CONTEXT_PM.md"
        if self.files.exists(worktree / context):
            content = self.files.read(worktree / context)
            heading = "## Current change — PM view"
            position = content.find(heading)
            if position < 0:
                raise ValueError("existing PM context has no current change item")
            end = content.find("\n## ", position + len(heading))
            end = len(content) if end < 0 else end
            item = content[position:end]
            updated, count = re.subn(r"(?m)^\*\*Status:\*\* Open$", "**Status:** Sealed", item)
            if count != 1:
                raise ValueError("existing current change must have exactly one Open status")
            self.files.write(worktree / context, content[:position] + updated + content[end:])
            edited.append(str(context))
        argv = [sys.executable, supplied["builder"], "--repo", str(worktree), "commit",
                "--staged", str(source), str(destination), "--add", *edited,
                "--subject", f"seal: {key} — {verdict}, moved to trail/", "--actor", "pm",
                "--directional", bookkeeping["directional"]]
        for name in ("surface", "co_authored_by", "reasoning_effort", "claude_session"):
            if name in bookkeeping:
                argv.extend(["--" + name.replace("_", "-"), bookkeeping[name]])
        self._run(worktree, argv)
        seal_sha = self._run(worktree, ["git", "-C", str(worktree), "rev-parse", "HEAD"]).strip()
        if self._run(worktree, ["git", "-C", str(worktree), "status", "--porcelain"]):
            raise OSError("seal commit left an unclean worktree")
        evidence = {"seal_sha": seal_sha}
        self.files.write(Path(supplied["evidence"]), json.dumps(evidence, indent=2) + "\n")
        return evidence


def main(argv: list[str] | None = None) -> int:
    arguments = sys.argv[1:] if argv is None else argv
    if len(arguments) != 1:
        print("error: supply the action configuration JSON path", file=sys.stderr)
        return 1
    try:
        action = SealAction(files=Files(), processes=Processes())
        print(json.dumps(action.seal(Path(arguments[0]))))
        return 0
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
```
