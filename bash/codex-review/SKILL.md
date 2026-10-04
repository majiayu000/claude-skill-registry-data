---
name: codex-review
description: Run an independent cross-model code review of any git scope — uncommitted changes, a commit range, a merge commit, a PR, or specific paths — via Codex CLI or context-blind subagents, then triage every finding with an explicit disposition. Use when asked to "review this diff", "codex review", "review PR N", "review the merge commit", or to get a second opinion on changes before or after merge. For reviewing implementation plans rather than code, see plan-review-loop.
user-invocable: true
argument-hint: "[scope] [paths] [--focus \"...\"] [--holistic] [--commit <sha>] [--pr <n>]"
metadata:
  version: "1.2.0"
---

# Codex Review

An independent code review of a **scope you choose**, not a scope some tool chose for you.

**Core principle:** the reviewer must not have seen the conversation that produced the
code. Its value is that it does not already believe the change is correct. Preserve
that — never hand it your reasoning, only the diff.

**No hook, no state file, no loop.** This skill runs start-to-finish inside one
invocation. Nothing can wedge a session, and nothing needs cancelling.

## Lifecycle

```
resolve scope → assemble lanes → run reviewer → triage findings → act
```

---

## Phase 1 — Resolve the scope

Run the resolver and use its output. Do not construct a `git diff` by hand.

```bash
"${CLAUDE_PLUGIN_ROOT:-.}/skills/codex-review/scripts/resolve-scope.sh" <args>
```

Pass the user's scope arguments through unchanged, minus `--focus` and `--holistic`
(those are yours, not the resolver's). It emits `SCOPE_LABEL`, `DIFF_ARGS`,
`PATHSPEC`, `REF_SHA`, `CHANGED_FILES`, `CHANGED_LINES`, `OVERSIZED`.

| The user says | Resolves to |
|---|---|
| *nothing* | dirty tree → `git diff HEAD`; else branch vs merge-base with the default branch; else the last commit |
| `HEAD~3` | everything since that ref |
| `<sha> <sha>` or `a..b` | that range |
| a **merge commit** sha | `git diff <sha>^1 <sha>` — detected automatically |
| `--commit <sha>` | that one commit alone |
| `--pr 140` | the PR's base..head (needs `gh`) |
| `--staged` / `--uncommitted` | index / working tree |
| trailing paths | pathspec-limits any of the above |

**Echo `SCOPE_LABEL` to the user before running the review.** A review of the wrong
range is worse than no review, because it reads as clean.

**If `OVERSIZED=true`** (default threshold 2000 changed lines): say so, and offer to
split by directory rather than proceeding. A reviewer given more than it will read
carefully returns confident shallow findings.

**If the resolver warns of an empty scope**, stop and resolve that first — it is
almost always a reversed range or an over-narrow pathspec.

## Phase 2 — Assemble the lanes

Read `review-lanes.md` (in this skill's directory) and select:

1. **Core lanes** — always.
2. **Detected lanes** — run the detection checks against the target repo.
3. **Project lanes** — if `.claude/code-review-lanes.md` exists in the target repo,
   include its contents verbatim. Read it; do not summarize it.
4. **Focus lane** — from `--focus "..."`, if given.
5. **Holistic lane** — only with `--holistic`.

If a `--focus` was not given but the diff touches something whose correctness depends
on a convention rather than a type (an index base, a unit, an ordering, a locale key),
name it explicitly in the prompt anyway. That class of bug is invisible to a generic
reviewer and obvious to a primed one.

## Phase 3 — Run the reviewer

Preference order:

### 1. Codex CLI

**Never use `codex exec review`.** That subcommand rejects a custom prompt, which
makes lanes and focus impossible. Always use plain `codex exec` pointed at the
resolved diff.

Ensure multi-agent is enabled (idempotent):

```bash
CODEX_CONFIG="${HOME}/.codex/config.toml" && if [ ! -f "$CODEX_CONFIG" ]; then mkdir -p "${HOME}/.codex" && printf '[features]\nmulti_agent = true\n' > "$CODEX_CONFIG" && echo "Created ~/.codex/config.toml with multi_agent enabled"; elif ! grep -qE '^\s*multi_agent\s*=\s*true' "$CODEX_CONFIG"; then if grep -qE '^\[features\]' "$CODEX_CONFIG"; then if [ "$(uname)" = "Darwin" ]; then sed -i '' '/^\[features\]/a\'$'\n''multi_agent = true' "$CODEX_CONFIG"; else sed -i '/^\[features\]/a multi_agent = true' "$CODEX_CONFIG"; fi; else printf '\n[features]\nmulti_agent = true\n' >> "$CODEX_CONFIG"; fi && echo "Enabled multi_agent in ~/.codex/config.toml"; else echo "Codex multi-agent: already enabled"; fi
```

Then run it **in the background** (`run_in_background: true`) so its output stays
visible and it can be killed if it stalls. Use a read-only sandbox — the reviewer
reports findings, it does not edit code:

```bash
codex --sandbox read-only exec "<prompt>" < /dev/null
```

**The `< /dev/null` is not optional.** Without it `codex exec` prints
`Reading additional input from stdin...` and blocks forever: backgrounded, its stdin is
an open pipe that never reaches EOF, so it waits for input no one will send. The tell is
a process that has burned **~0.05 s of CPU over half an hour** and has written no
rollout under `~/.codex/sessions/<yyyy>/<mm>/<dd>/`. It looks exactly like a long review
and is a deadlock before the first token. Verify with a five-second smoke test —
`codex --sandbox read-only exec "Reply with exactly: SMOKE OK" < /dev/null` — before
concluding a real pass is merely slow.

The prompt must contain, in this order:

1. The exact diff command: `git diff <DIFF_ARGS> [-- <PATHSPEC>]`, and an instruction
   to run it first and review **only** what it prints.
2. `SCOPE_LABEL`, so the reviewer knows what it is looking at.
3. One block per selected lane, each ending with the finding format.
4. A consolidation instruction: dedupe overlapping findings, order by severity, return
   the result **as text**.

Per finding: `file:line`, severity (critical/high/medium/low), lane, what is wrong,
why it is wrong, and a concrete fix.

Have Codex return findings as text and write the artifact yourself. Letting the
reviewer write the file is how you end up with a review that ran and produced nothing.

#### Watching the run — two ways to blind yourself

A Codex pass takes tens of minutes. Both of these make a healthy run look identical to a
wedged one, and both are easy to do by reflex.

**Never pipe it through `tail -N` or `head -N`.** They buffer to EOF by definition, so the
background task's output file stays at **0 bytes for the whole run** however much Codex has
written. You then cannot tell progress from a stall without `pgrep`, and the pipe has
silently removed the visibility that `run_in_background` existed to give you.

```bash
# WRONG — nothing readable until the process exits
codex --sandbox read-only exec "$PROMPT" 2>&1 | tail -200
# RIGHT — write it all; filter when you READ the output file
codex --sandbox read-only exec "$PROMPT" 2>&1
```

**Write the guard loop for the OS you are on.** Watch the process itself, not a proxy:

```bash
while pgrep -f "codex --sandbox read-only exec" >/dev/null 2>&1; do sleep 20; done
echo "codex exited; output bytes: $(wc -c < "$OUT")"
```

`until [ ! -d /proc ]` is a real example of getting this wrong: macOS has no `/proc`, so
the condition is true on the first evaluation, the loop body never executes, and the
watcher exits 0 having emitted nothing — which reads exactly like "hasn't finished yet".

Before arming any watcher, ask: **if Codex died right now, what line would appear?** If the
answer is "none", the watcher is decorative. A watcher that ends with no output is a result
to investigate, never a result to report as "still running".

**Check liveness, not just existence.** `pgrep` finding the process proves nothing — a
deadlocked Codex is still a process. Two cheap signals separate working from wedged:

```bash
ps -o etime=,time= -p <pid>                      # elapsed vs CPU TIME consumed
ls -t ~/.codex/sessions/$(date +%Y/%m/%d)/*.jsonl # a live run writes a rollout
```

Minutes of elapsed against ~0.05 s of CPU, and no rollout file, means it never started.
Report elapsed time from a clock (`date`, `ps -o lstart=`), never from how many turns have
gone by — that estimate drifts badly and turns into a confidently wrong status report.

**Don't wait idle.** The pass is long enough to run the diff's own cheap checks alongside
it — the project's linters, its localization or script guards, a targeted test suite. On a
2026-09-10 sixlines-ios run those found a real defect (Traditional orthography in a
Simplified string) before Codex returned anything at all.

### 2. Fallback — context-blind subagents

If `codex` is unavailable or fails: dispatch one subagent per lane, in parallel, each
given only the diff command and its own lane. **Do not tell them anything about the
change's intent or your reasoning** — context-blindness is the entire point of the
fallback. Say plainly in the output that the review was same-model, so its
independence is weaker.

## Phase 4 — Write the artifact

Write to `reviews/review-<YYYYMMDD-HHMMSS>-<REF_SHA>.md`:

```markdown
---
scope: <SCOPE_LABEL>
diff: git diff <DIFF_ARGS> [-- <PATHSPEC>]
files_changed: <n>
lines_changed: <n>
lanes: correctness, contracts, tests, security, nextjs, project(.claude/code-review-lanes.md), focus
reviewer: codex-cli | subagents
reviewed_at: <ISO 8601>
---

## Findings

### [critical] <one-line title>
**Where:** `path/to/file.ts:142` · **Lane:** correctness
<what is wrong, why, and the fix>

...

## Disposition
```

Recording the exact diff command in the frontmatter is not decoration — it is the only
way anyone later can tell what this review did and did not look at.

## Phase 5 — Triage

**Judge every finding yourself.** The reviewer has no context and will be confidently
wrong about deliberate decisions. Verify each claim against the code before accepting
it, and reject the ones that are wrong — a review you agree with entirely is a review
you did not actually read.

Every finding gets exactly one disposition line under `## Disposition`:

- **ACCEPTED** — real, in scope. Fix it.
- **DECLINED** — with the reason. "Deliberate: adjust-during-render is the documented
  React pattern here" is a disposition. Silence is not.
- **PRE-EXISTING** — real, but not caused by this diff. Do not fix it here; that is
  scope creep wearing a helpful hat.

```markdown
## Disposition
- [high] HexagramLines off-by-one on changingLines — ACCEPTED, fixed in <sha>
- [med] bg-accent hardcoded in HexagramDisplay — PRE-EXISTING, filed #212
- [low] extract the combobox into a hook — DECLINED: churn exceeds the value
```

## Phase 6 — Act

**Ask before doing any of these.** This skill reviews; it does not unilaterally
rewrite or publish.

1. **Fix accepted findings** — as follow-up commits, one logical fix per commit.
   Reference the review file in the commit message.
2. **File the rest** — declined-but-real and pre-existing findings become
   `gh issue create` calls, so they survive outside a markdown file nobody reopens.
   Do not fix pre-existing findings in this change.
3. **Commit the review artifact** if the project tracks `reviews/` (check whether the
   directory is in git — many projects gitignore it).
4. **Feed the lesson back.** When a finding was real and would recur, propose adding
   it to `.claude/code-review-lanes.md`. That file is how the review gets sharper each
   time instead of repeating the same generic checks forever.

## Rules

- Echo the resolved scope before reviewing. Always.
- Never `codex exec review` with a custom prompt — it will be rejected.
- Never let the reviewer see your reasoning about the change.
- Never fix pre-existing findings inside the change under review.
- Every finding gets a disposition, including the ones you reject.
- Run the reviewer backgrounded so it can be watched and killed — and never through
  `tail`/`head`, which buffer to EOF and leave the output file empty for the whole run.
- A watcher that produced no output is a broken watcher until proven otherwise.
- Always `< /dev/null` on `codex exec`; without it a backgrounded run blocks on stdin
  forever, looking exactly like a slow review.
- On any tooling failure, report it and continue degraded — never leave the user
  unsure whether a review ran.
