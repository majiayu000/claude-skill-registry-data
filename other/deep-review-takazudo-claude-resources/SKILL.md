---
name: deep-review
description: "Deep code review — runs the built-in /code-review together with /codex-review, which carries the depth. Use when: (1) User says 'deep review', (2) A substantial change needs a pre-merge quality gate, (3) A general review already ran and more coverage is wanted. For an ordinary review, invoke /code-review directly instead — this skill exists only for the two-reviewer pass. Fixes are applied inline by default; -t delegates them to /x-wt-teams when the work is genuinely large. Unfixed findings become agent-found GitHub issues by default (-nori to suppress)."
argument-hint: "[low|medium|high|xhigh|max] [-t|-nt] [-ri|-nori] [target]"
---

# Deep Review

Two reviewers on the same change, in parallel:

| Reviewer | What it brings |
| --- | --- |
| `/code-review` (built-in) | Correctness bugs, CLAUDE.md adherence, reuse/simplification. Runs in its own context, so findings cost this session almost nothing. |
| `/codex-review` | An independent model's read of the same diff. Catches what a single model's blind spots miss. |

Everything else this skill does is routing: synthesize the two reports, apply or delegate the fixes, and file what stays unfixed.

> **Never invoke `/code-review ultra` from here.** Ultra is a paid cloud review that only the user can start by typing it — a skill cannot launch one, and attempting it silently degrades to a local review. If a change warrants ultra, say so in the final report and let the user decide.

> **On Claude Code on the web** (`$CLAUDE_CODE_REMOTE=true`): follow [`web/web-mode.md`](../../web/web-mode.md). Codex is unavailable there, so run `/code-review` alone. Fixes are still inline by default, same as everywhere else; only when `-t` is explicitly passed does the delegation happen — and there it fans out **subagents** rather than an `/x-wt-teams` session, since web has no agent teams. GitHub work goes through the MCP, not `gh`.

## Arguments

**Effort** — `low` | `medium` | `high` | `xhigh` | `max`, forwarded verbatim to `/code-review`. Default `medium`: **codex is the half that goes deep here**, so paying for a wide, lower-confidence built-in pass alongside it mostly buys duplicate findings and false positives to triage. Raise it when codex is unavailable and the built-in is carrying the review alone. `ultra` is not accepted (see above).

**Target** — a PR number, branch, path, or ref range, forwarded verbatim to `/code-review` and used to resolve `--base` for codex. Omit it to review the current branch's commits plus uncommitted changes, which is the right default nearly always.

**Fix routing** — inline by default: apply the fixes in this session. `-t` / `--team` opts into delegating them to a fresh `/x-wt-teams` session instead, which is worth it only when the fix work is genuinely large (a multi-file refactor, or findings spanning subsystems this session hasn't loaded). `-nt` / `--no-team` names the default explicitly. Neither path runs when the review comes back clean.

Team-fix used to be the default because collecting findings left the manager token-heavy. `/code-review` runs in its own context window now, so that premise is gone — spawning a worktree and an agent to apply a handful of fixes costs more than it saves.

**Issue raising** — `-ri` / `--raise-issues` (default) files unfixed findings as GitHub issues; `-nori` / `--no-raise-issues` keeps them in the terminal report. Callers that own their own issue-raising pass `-nori` so a session has exactly one raise-owner.

## Process

### Step 1: Launch both reviewers in parallel

Single message, both calls:

```
Skill(skill="code-review", args="<effort> [target]")
Skill(skill="codex-review", args="[target]")
```

**Both reviewers must be pointed at the same changes.** `/codex-review` resolves its own base when given nothing — PR base, else the repo default branch — which is correct only when no target was passed. If this invocation *did* carry a target, forward it, so the two halves don't review different diffs and produce a synthesis that silently mixes scopes. When the target is a form codex can't take directly (a path, or a PR number), resolve it to the equivalent base ref first and pass that.

Do **not** pass `--fix` to `/code-review` here — this skill owns the fix routing in Step 3, and a background `--fix` would edit the tree while the codex half is still reading it. (`--fix` edits also land outside session checkpoints, so `/rewind` cannot undo them.)

`/codex-review` returns findings without touching files, and never stalls this step or surfaces a quota error.

**When it returns "codex unavailable — no findings", this stopped being a deep review.** You have one reviewer, not two, so Step 2's consensus rule has nothing to work with — do not rank anything as cross-model-corroborated, and say plainly in the report that the codex half didn't run so the user knows what they did and didn't get.

### Step 2: Synthesize

Merge both reports into one list. Deduplicate — the same bug reported by both reviewers is one finding, and **a finding both reviewers raised independently is the highest-confidence signal available here**; rank those first. Where they disagree, prefer the one that cites specific code over the one that reasons abstractly.

This rule holds only while the two reports come from genuinely different models. If the codex half didn't run, skip the consensus ranking entirely rather than applying it to one reviewer's output.

Present the merged list, then stop if it is empty — Steps 3 and 4 do not run on a clean review.

### Step 3: Fix

**Default — inline.** Apply the fixes here. Fix high-priority findings without asking; fix medium ones when the change is clearly safe; leave low-priority and style-only findings for Step 4. Then run the project's type-check, commit, and — on a PR — invoke `/pr-revise`.

**`-t` — delegate.** Only when the fix work is genuinely large. Hand it to a fresh team session:

```
Skill(skill="x-wt-teams", args="--no-review -nf -nori --stay Fix the review findings below. Single topic — all fixes in one worktree. <findings with file:line, what to change, why>")
```

The three guard flags are mandatory, never omit them: `--no-review` stops the inner session from calling `/deep-review` again and looping forever; `-nf -nori` stop it from auto-fixing beyond the brief or filing its own issues, both of which this session owns.

Bundle everything into **one** topic so a single agent works in a single worktree — parallel topics on overlapping files conflict. Split only when the findings touch genuinely disjoint file sets.

If any finding sits inside a workspace package that consumers import through a built artifact (an `exports` map pointing at `./dist/...`), add a rebuild instruction to the brief naming the packages and the project's build command. Without it the fix agent commits source-only changes and ships stale compiled output.

When `/x-wt-teams` returns, fixes are committed, merged into the current branch, and pushed. There is nothing further to commit here, and **do not re-run `/deep-review` to verify** — that starts another `-t` cycle.

### Step 4: File what stayed unfixed

Skip when `-nori` was passed or everything was fixed.

Findings that need a human decision (a product or design call, a behavior/API/schema change) and findings the fix pass could not apply become GitHub issues, so the decision survives the session:

```bash
gh label create agent-found --color D93F0B --description "Found by agent during automated work" 2>/dev/null || true
gh issue list --label agent-found --state open
```

Check that list first and skip anything already tracked — repeated reviews must not re-raise duplicates. One issue per distinct finding (group tightly-related ones), each with `file:line` refs, what was found, and why it was deferred. Fixed findings never get an issue; the commit is the record.

### Step 5: Reap the codex broker

Once, at the very end, after every exit path — success, fallback, team-fix, or inline:

```bash
node $HOME/.claude/scripts/codex-sweep.js --workspace "$PWD"
```

Never run this mid-flow: a broker is shared per workspace, so an early reap kills a review still in flight. It is a quiet no-op when no broker exists.

## Notes

- **`/code-review` alone is the general review.** Reach for `/deep-review` when the cross-model second opinion is worth the extra time — a large change, a pre-merge gate, an area where one model already missed something. Routine passes should call `/code-review` directly.
- **The built-in runs in its own context window.** That is why this skill no longer spawns a fleet of `code-reviewer` subagents with a log-file return protocol: the context problem those solved no longer exists.
- **Effort is the dial, and it is not a model dial.** `low`→`max` trades false positives against coverage by changing how much the reviewer reasons per step; the model itself is the session model (a forked subagent inherits it, unless `CLAUDE_CODE_SUBAGENT_MODEL` is set). Change the reviewer's model with `/model`, not with a flag here — Claude Code ignores skill-level model overrides.
- **Only half of this skill tracks the session model, and that is the point.** The `/code-review` half rides whatever `/model` is set to, so switching models shifts what it catches. The `/codex-review` half is a different provider entirely and does not move with it. So a deep review's floor holds even on a lighter session model — the depth comes from codex, not from being on the strongest Claude available. That is what makes `-co` the right lever for "review this harder," and a higher effort the wrong one.
