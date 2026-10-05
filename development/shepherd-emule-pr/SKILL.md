---
name: shepherd-emule-pr
description: Take an open tt-emule PR to a mergeable, ethos-compliant state. Use when asked to review a PR, address its comments, and prepare it to land — verifies every review point by build (not by trusting "addressed"), runs an emule-ethos pass for the bug classes reviewers miss, then rebases onto main locally and hands the developer a change+verification summary (with a drafted per-point comment and the exact push command) to review and push. The skill never force-pushes the author's branch itself — the human stays in the loop for that.
user_invocable: true
---

# Shepherd an emule PR to mergeable

The job: take an open PR and get it ready to land — review it against the repo
ethos, confirm every review comment is *actually* resolved, fix what's still
wrong, rebase onto `origin/main` **locally**, and hand the developer a
change+verification summary (with a drafted per-point comment) to review and
push. The PR author's later commits usually *claim* to have addressed the review
("Address review …"); an automated reviewer (Copilot) and a human reviewer have
usually weighed in. None of that is trustworthy on its own.

**Human-in-the-loop for the push.** The skill rebases and prepares, but it does
**not** force-push the author's branch or post the comment on its own — force
pushing a shared branch rewrites someone else's history and is a human decision.
The deliverable is a rebased local branch plus a summary the developer signs off
on before pushing.

The governing principle, learned across three PRs: **verify by building and
reading, not by trusting an "addressed in commit X" claim or a green CI label —
and always run your own ethos pass, because the reviewers miss the emule-specific
bug classes.** In #237/#238/#239, the human + Copilot reviewers *each* missed a
hard JIT-compile bug that a 5-line compile-probe surfaces immediately.

The ethos you are enforcing (from `.claude/CLAUDE.md`): faithful to the canonical
silicon implementation, a **single** code path (no divergent duplicate), the
**minimal** `jit_hw` surface, surface caller bugs rather than mask them, and be
**skeptical of automated-reviewer suggestions** — judge each against these rules,
don't apply reflexively.

## When to invoke

- You're asked to review an open PR, address its comments, and prepare it to land
  (rebase locally, then hand off a summary for the developer to push/comment).
- A PR is `CONFLICTING` or behind main and needs a rebase plus a review pass.

Not this skill:
- A pin bump turned the regression red (device-open crash, broad JIT-compile
  drift, hang) → `/uplift`.
- Reviewing your *own* uncommitted working diff for quality → `/code-review`
  (built-in). Generic GitHub PR review with no landing → `/review` (built-in).
- This skill is for shepherding a **feature / shim** PR to merge against review +
  ethos, and it borrows `/uplift`'s prove-by-build discipline and rebase mechanics.

## Step 0 — Gather the full picture

Read **every** comment surface — reviews live in three different API buckets and
`gh pr view` only shows one:

- `gh pr view <n> --json number,title,state,headRefName,baseRefName,author,mergeable,body,files,commits,statusCheckRollup`
- Issue comments: `gh pr view <n> --json comments`
- Review bodies (CHANGES_REQUESTED / APPROVED verdicts): `gh api repos/<owner>/tt-emule/pulls/<n>/reviews`
- Inline (line-level) comments: `gh api repos/<owner>/tt-emule/pulls/<n>/comments`

Note **who** requested changes vs approved, and reconcile: a reviewer may approve
*after* leaving unresolved concerns. **Read the CI artifact, not the label** — a
"pass" can hide smoke/JIT failures, and a `FAILURE` row named "All checks passed"
is a required-check quirk, not the signal. Beware the rtk wrapper summarizing
`git status` to `ok`; get real status with `git status --porcelain | wc -l`.

## Step 1 — Check out and measure the rebase

```
git fetch origin <branch> && git checkout <branch>
git merge-base --is-ancestor origin/main HEAD && echo up-to-date || echo REBASE NEEDED
git log --oneline origin/main..HEAD          # commits to replay
git merge-tree $(git merge-base origin/main HEAD) origin/main HEAD | grep -i conflict
```

The branch may carry force-pushed "agent-storm" history (transient symbols,
`edits`, repeated `docs: refresh structure index`). Work from the **actual tip**
(`git ls-remote origin refs/heads/<branch>`), not the commit-message narrative.

## Step 2 — Verify each review point against *current* code, in the ethos lens

For every comment, confirm the fix **in the tree** — a commit titled "Address
review" often only partially fixes, or fixes one call site. Categorize each point:

| Verdict | Meaning |
|---|---|
| **resolved** | fixed in the tree; confirm it compiles / matches the ethos |
| **partial** | one instance fixed, another remains (e.g. one `requires` converted, two left) |
| **open** | not addressed; you must fix or register it |
| **moot** | the flagged file/line no longer exists after a force-push |

Judge against the ethos, not just "does it compile" — a change can compile and
still be a divergent duplicate or a silent silicon divergence.

## Step 3 — Own ethos pass (the catalog reviewers miss)

Sweep the diff for these recurring emule bug classes:

1. **Dangling refactored symbol.** A bare `__emule_dst` (the DST file moved into
   `__emule_compute_ctx().dst` in #223), or any symbol a `git grep` finds only in
   comments plus the new code. A non-dependent name in a plain `inline`/non-template
   function errors at **parse** time, so *any* TU that `#include`s the header fails
   to compile — even if the function is never instantiated. Bit #238
   (`gelu_tanh_tile`) and #239 (`transpose_wh_dest`). *Fix:* route through the
   current accessor, match the sibling ops in the same file, add the
   `__emule_dst_check` those siblings use.
2. **Divergent-duplicate / ODR.** The same symbol defined in two headers under one
   `#ifdef` guard with **non-identical** bodies (#239 `sigmoid_tile_pack` forwarded
   to two different `sigmoid_tile` overloads); or a header that `inline`-defines a
   symbol the tt-metal runner *also* defines (#237 `asan_cb_state.h` vs
   `emulated_program_runner.cpp`). *Fix:* one definition site; the other path defers
   to it.
3. **Silent silicon divergence.** A core-op special-case that masks an upstream bug
   rather than reproducing silicon — e.g. skipping zero-multiplier lanes so
   `inf*0` doesn't become `NaN`, when silicon FP *does* produce NaN (#239). Not
   faithful. *Fix:* fix the upstream inf source, or — when that's blocked —
   register it in `/workarounds` with the root cause + removal path and a code-site
   `WORKAROUND` comment. Never ship it silently.
4. **C++ standard mismatch.** A `requires`-expression / C++20 construct in a JIT
   header. Confirm the JIT `-std`: it is `TT_EMULE_CXX_STANDARD` = **20**
   (documented in `docs/metal-integration.md`), so C++20 is fine on the real
   path; a doc still claiming C++17 is stale and a separate cleanup, not a
   blocker (#237).
5. **Superseded-by-main.** Main independently solved the PR's problem a *different*
   way. Check current `origin/main` **and the pinned tt-metal runner** for the
   symbols the branch reworks. If so, a mechanical rebase re-introduces a parallel
   path — trim the PR to what's still needed instead (#237: ASAN restructure was
   dead; runner already defined the symbols and the log moved to the fiber ctx).

## Step 4 — Prove by build (the JIT compile-probe)

The load-bearing verification. It catches classes 1, 2, and 4 in seconds without a
full build. Reconstruct the JIT flags from
`tt_metal/impl/emulation/emulated_program_runner.cpp` (`-std=c++<TT_EMULE_CXX_STANDARD>`,
`-I jit_inc`, `-I parent_inc`, `-DTT_EMULE_USE_L1_POOL`):

```bash
# probe.cpp — include the umbrella FIRST so the compute ctx / VectorMode / ALWI
# exist, THEN the header under test. A jit_hw header alone usually can't be the
# first include.
cat > probe.cpp <<'EOF'
#include "jit_hw/api/compute/compute_kernel_api.h"
#include "jit_hw/<header under review>"          // e.g. api/compute/eltwise_unary/gelu.h
EOF

clang++-20 -std=c++20 -fsyntax-only \
  -DTT_EMULE_USE_L1_POOL -DARCH_WORMHOLE -DNUM_DRAM_BANKS=12 -DNUM_L1_BANKS=64 \
  -I <tt-emule>/include/jit_hw -I <tt-emule>/include \
  -I <tt-metal>/tt_metal/hostdevcommon/api  probe.cpp
```

- For a header on the matmul AVX2 path, add `-DEMULE_MATMUL_USE_AVX2 -mavx2 -mfma`.
- For the fused-activation aggregator, define `SFPU_ACTIVATION` and include
  `compute_kernel_hw_startup.h` after the umbrella.
- To decide a C++20-vs-17 concern, run the probe at both `-std=c++20` and
  `-std=c++17` — clean at 20 / error at 17 proves it's std-only, and the JIT is 20.
- Grep-corroborate class 1: `git grep '<symbol>'` should find a real definition,
  not only comments; `emule_thread_ctx.h` records what a symbol "was".

This is a **targeted** probe of the changed headers, not the full suite — see the
Step 8 caveat.

## Step 5 — Make changes as needed

- **Faithful fix.** Match the file's existing idiom and sibling ops; single code
  path; no defensive divergence (`/verify-mock`, `/memory-debug` for residuals).
- **Register a workaround.** When the faithful fix is blocked, add a `/workarounds`
  entry (what it is, why it bends a rule, real root cause, removal path, tracking
  issue) and a `WORKAROUND (WA-n)` code-site comment. Don't leave a silent
  divergence.
- **Trim superseded work.** Drop the parts main already provides; keep the genuinely
  new contribution.
- **Surface scope-changing calls to the user** *before* putting them in the
  handoff — trimming a large chunk (#237) or keeping-vs-reverting a workaround
  (#239) is the reviewer's decision, not yours. Use AskUserQuestion with a
  concrete recommendation.

## Step 6 — Rebase onto `origin/main` (supersession-aware)

```
git fetch origin main && git rebase origin/main
```

- Resolve each conflict by asking **"does main + the pinned runner already provide
  this?"** — `git grep` the tt-metal runner (`.../impl/emulation/`) for the
  symbols. Favor main's evolved model over a superseded branch approach.
- `structure.yaml` conflicts: resolve crudely (take either side), finish the
  rebase, then **regenerate against the final tree**:
  `python3 scripts/gen_structure.py --write`, and confirm
  `python3 scripts/gen_structure.py --check` + `git diff --check`.
- **Trimming pattern:** after the rebase, a single self-documenting cleanup commit
  is cleaner than commit surgery (interactive rebase is unavailable here) —
  `git checkout origin/main -- <superseded files>`, `git rm <orphaned files>`,
  regenerate `structure.yaml`, commit with the rationale. The net tree is what
  ships.
- Keep the branch's own PR ref intact — detach/rebase, don't reset a shared branch
  onto something unexpected.
- The rebase stays **local**. Pushing the rewritten history is Step 7's handoff,
  performed by the developer — the skill never pushes it.

## Step 7 — Hand the developer a summary (don't push)

Stop at the rebased **local** branch. Do **not** `git push` — force-pushing a
shared branch rewrites the author's history and is the developer's call, not the
skill's. Instead present a handoff the developer can act on:

- **What changed and why** — per fix: the review point / ethos-class it resolves,
  the mechanism (not just "done"), and the file:line.
- **Verification evidence** — the compile-probe command(s) you ran and the result
  (the actual `use of undeclared identifier` line, or a clean exit), plus the
  honest caveat (a targeted header probe is not `run_regression.sh`).
- **The drafted per-point PR comment** (Step 8) for the developer to post.
- **The exact commands to run**, so the human performs the branch mutation:

  ```
  git push --force-with-lease origin <branch>   # rebase rewrote history; --force-with-lease
                                                 # guards a concurrent update to the tip you based on
  gh pr comment <n> --body-file <file>
  ```

The developer reviews the summary, then pushes and posts (or tells you to). If the
user explicitly directs you to push a specific branch, that direction is the
authorization for that branch only — don't extend it to others, and still surface
the summary first.

## Step 8 — Draft the per-point comment (developer posts it)

Draft the comment as part of the handoff — `gh pr comment <n> --body-file <file>`
is the command the developer runs (Step 7). Include:

- **Per-point verdict** for every review comment: resolved / fixed-here /
  registered (WA-n) / trimmed / moot — with the mechanism, not just "done".
- **Any extra bug you found**, with the **compile-error proof** pasted (the
  `use of undeclared identifier` line, etc.) so it's not an assertion.
- The **honest verification caveat**: targeted compile-probes are **not** a full
  `run_regression.sh` (there is usually no `build_emule` in-workspace) → recommend a
  per-arch regression before merge.
- The **alternative you didn't take** (e.g. "revert vs register the workaround —
  say the word") so the reviewer can redirect.

## Anti-patterns (consolidated)

1. **Trusting "addressed in commit X"** without reading the resulting tree.
2. **Trusting a green CI label** — or rtk's filtered `git status` `ok`. Read the
   artifact; get `--porcelain` status.
3. **Skipping the own-ethos pass.** Reviewers missed a hard compile bug in all
   three reference PRs; the compile-probe finds it in seconds.
4. **Blindly rebasing a superseded PR** — re-introducing a divergent parallel path
   main already replaced.
5. **Pushing the author's branch yourself.** The skill rebases *locally* and
   hands off; the developer reviews the summary and runs the `--force-with-lease`
   push (and posts the comment). Never force-push a shared branch on your own —
   it rewrites someone else's history. This is doubly true for a scope-changing
   reconciliation (a trim, a revert), which needs explicit sign-off besides.
6. **Claiming verification you didn't do** — a targeted header compile is not the
   regression suite; say which you ran.
7. **Applying Copilot/automated suggestions reflexively** — judge each against the
   ethos (a suggested defensive clamp is usually the wrong fix).

## References

- `/uplift` — prove-by-build discipline, rebase/pin & cross-repo push mechanics,
  reading the CI artifact over the label.
- `/workarounds` — how to register a deliberate divergence (Step 5 / class 3).
- `/memory-debug`, `/verify-mock` — residual triage and mock-completeness checks.
- `.claude/CLAUDE.md` — the ethos rules this skill enforces.
- `scripts/gen_structure.py` (`--write` / `--check`), `scripts/find_symbol.py`
  (`--supports` / `--shadows` to probe whether a symbol/include is modelable).
