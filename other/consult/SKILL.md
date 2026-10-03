---
name: consult
description: >-
  One-shot cross-model CONSULT — fan the same question out to Codex and agy in parallel (repo-isolated, advisory), then reconcile their answers into one. Use when the user wants a "second opinion", to "ask Codex and agy", a "panel" or "cross-model" check, or an independent gut-check on a decision/design/doc before committing — and does NOT need an iterative build/review loop. NOT a relay: a relay is an iterative 1:1 Producer↔Reviewer loop that converges an artifact; a consult is a parallel 1-shot 1:N second opinion, reconciled once. Depends on the codex + agy CLIs and the relay-automation shims; runs in any repo that ships them at the repo root OR in a vendored `.xyz/` install (the skill resolves either).
---

# Consult

**One question → N independent models in parallel → one reconciled answer.**

A consult asks Codex and agy the *same* question at the same time, isolated from your real tree, and then a
coordinator (Claude) reconciles their answers — surfacing where they **agree**, where they
**disagree**, and giving a single reconciled **call**. It is the fast "ask the other brains before I
commit" move: no copy-paste, no window-shuttling, one step.

## Consult vs. relay — pick the right tool

| | **consult** (this skill) | **relay** |
|---|---|---|
| shape | parallel fan-out, 1 question → N models | iterative loop, 2 agents |
| rounds | exactly **one** | many, until `Approved` |
| writes | **none** — advisory only | Producer edits the artifact |
| output | reconciled answer + divergences | a converged artifact |
| use for | a decision, a design gut-check, "is this doc sound?" | building/fixing an artifact under review |

If after a consult you decide the work needs iteration, *start a relay* — the consult is the cheap
first look, the relay is the build loop.

## When to use

- "Get a second opinion." "Ask Codex and agy." "What do the other models think?"
- "Panel review" / "cross-model check" / "sanity-check this before I commit."
- An independent gut-check on a plan, design, schema, or doc — where you want *divergent* reads, not
  a single model's confident answer.

Do **not** use it to build or fix an artifact iteratively — that's `relay`.

## How it works

`relay-automation/consult.sh` (path is relative to **this repo's root**, not your cwd) fans the question
out to both advisors **in parallel** and writes each transcript to a per-run dir
`relay-system/<today>/<label>-<HHMMSS>/`. The synthesis is **yours** — the script only gathers the raw
opinions.

**Locating the script — resolve it cwd-independently; never assume your cwd is the repo root.** A bare
`consult.sh` or `relay-automation/consult.sh` only resolves when you happen to be sitting at the root,
so invoke it through its repo-root anchor instead. Two homes are supported so consult works both in
the XYZ-forge (or XYZ mini) checkout **and** in any repo that has a vendored `.xyz/` install: the
top-level `relay-automation/` if present, otherwise the vendored `.xyz/relay-automation/`.

```
ROOT="$(git rev-parse --show-toplevel)"
SCRIPT="$ROOT/relay-automation/consult.sh"
[ -f "$SCRIPT" ] || SCRIPT="$ROOT/.xyz/relay-automation/consult.sh"
# CONSULT_ROOT MUST be the repo root: consult.sh otherwise infers its root as the script's parent-of-
# parent, which for the vendored copy is `.xyz/` (wrong). Setting it pins the consult to the real repo
# and its `relay-system/` output. Harmless (a no-op) for the top-level copy.
CONSULT_ROOT="$ROOT" "$SCRIPT" --prompt "…" --label …
```

`git rev-parse --show-toplevel` works from any subdirectory of the repo. If you are not inside a repo
that has consult (no top-level `relay-automation/` and no `.xyz/`), either `cd` into the
XYZ-forge/XYZ mini checkout, or (XYZ-forge only) vendor a `.xyz/` into the target repo first
(`relay-automation/xyz-vendor.sh <repo>`). (Do **not** go hunting the disk for `consult.sh`; the
anchor above always finds it.)

**Repository isolation (CWD-level, not a process sandbox).** Advisors run with their working directory set to a
**throwaway git worktree** checked out from your *current* state — tracked WIP (via `git stash create`)
plus untracked-non-ignored files copied in — so they see your working state (minus `.gitignore`d
files), including a brand-new file under
review. Anything an advisor writes lands in that disposable worktree and is destroyed with it; your
real working tree is **never** the advisors' surface, so there is nothing to revert and ambient WIP
cannot be clobbered. (Codex additionally runs `-s read-only`.) This replaced an earlier best-effort
post-hoc revert that the skill's own first dogfood flagged as unsafe.

```
consult.sh --prompt-file Q.md            # question is the file's contents (may reference repo paths)
consult.sh --prompt "Is X sound?"        # inline question
  [--models codex,agy]                   # default pair; claude is also supported (Python runtime)
  [--out DIR]                            # parent dir (default relay-system/<today>/)
  [--label SLUG]                         # run-subdir + transcript stem (default "consult")
```

For native Claude, follow [subscription setup](https://github.com/HiQS-Labs/XYZ-forge/blob/development/relay-automation/README.md#claude-subscription-mode).
`--models claude` is a single advisory answer, not cross-model consensus. Claude uses read-only
built-in tools in native restricted mode; user/project/local settings are ignored in both
authentication modes, and outside-checkout reads are denied by the CLI. See the setup guide
for the CLI requirement and effort settings. Relay reviews separately retain protocol writes.

Each run gets its own `<label>-<HHMMSS>/` subdir, so two consults the same day never overwrite each
other. Behavior is covered by `test/consult.sh` in XYZ-forge's `validate.sh` (WIP preservation, no advisor leak,
graceful degrade, non-git refusal).

Exit `0` = at least one advisor answered; `5` = all failed; `3` = not a git repo (isolation needs
one); `2` = usage. Per-model failures are reported, not fatal — if Codex's backend is down, Gemini's
answer still comes back (**graceful degrade**, and the degrade is stated, never silent).

## Steps (the coordinator's job)

1. **Frame one sharp question.** Put it in a prompt file when it references repo paths (the advisors
   read the files themselves). Be explicit about what "good" looks like, just like a relay's
   Definition of Done.
2. **Fan out:** run the script through its repo-root anchor (see "Locating the script" above — prefer
   `$ROOT/relay-automation/consult.sh`, fall back to `$ROOT/.xyz/relay-automation/consult.sh`, and
   always pass `CONSULT_ROOT="$ROOT"`) with the prompt + a `--label`. Both models run at once. Don't
   invoke a bare `consult.sh`; it only resolves at the repo root.
3. **Read both transcripts** in `relay-system/<today>/<label>-<HHMMSS>/<label>.codex.md` and `…agy.*`.
4. **Reconcile — this is the load-bearing step.** Produce a synthesis with four parts, in this order:
   - **TLDR** (new — one to two sentences, before anything else): the reconciled call and how confident
     it is, so the operator can stop reading right there if that's all they need. e.g. *"Both models
     agree the migration is safe — go ahead. Codex flagged one edge case worth a follow-up (see below)."*
   - **Disagree** (it's the whole point of asking two models): every point the two differ on, with your
     adjudication and *why*. Never in the TLDR — the TLDR previews the call, it doesn't bury the split.
   - **Agree:** what both independently converged on (higher confidence because it's cross-model).
   - **Sorted categories** (new — closes the synthesis, replaces a bare prose recommendation): bucket
     every point either advisor raised — agreements and adjudicated disagreements alike — into exactly
     one:
     - **Blocking** — a real risk either advisor surfaced; must address before proceeding.
     - **Worth doing, optional** — a real improvement; the operator's call.
     - **Skip / out of scope** — noted and dismissed, named so it doesn't resurface.
     Drop empty buckets. For a short, clean consult (both advisors agree, one or two minor notes),
     skip the buckets and give the recommendation as plain prose instead — don't force structure on a
     synthesis with nothing to sort.
5. **Hand the synthesis back** to the operator. If it reveals the work needs iteration, offer to
   start a `relay`.

## The one rule that makes a consult worth running

**Surface disagreement; never average it away.** The entire value of asking two models is the *delta*
between them — the place one caught what the other missed. A synthesis that smooths two answers into
one confident paragraph throws that away and is worse than asking one model, because it launders two
guesses into false consensus. Lead with the disagreements, adjudicate them explicitly, and if you
can't adjudicate one, say so and flag it for the human. (Same failure mode as a review that only
hunts overclaims and misses silent drops: the easy direction satisfices.)

## Honest caveats

- **Two models, not ground truth.** Cross-model agreement raises confidence; it does not prove
  correctness — both can share a blind spot or a wrong prior. Treat a unanimous answer as *strong
  signal*, not proof, especially when correctness rides on runtime behavior neither model ran.
- **Repo-isolated, not process-sandboxed.** Advisors run in a throwaway worktree, so an advisor that
  ignores the "advisory only" instruction edits the worktree, not your checkout. Be precise about the
  boundary: the worktree shares the repository's Git object store and the advisor CLI runs with the
  host's normal permissions (agy is launched with `--dangerously-skip-permissions`), so this protects
  your *working tree*, not the *host* or *Git state*.
  Codex additionally runs `-s read-only`; agy runs with `--dangerously-skip-permissions` and is
  repo-isolated but not a sandboxed process (it can still reach the network / the host outside the
  worktree). For a hard process boundary, run consult inside your own sandbox. If a fix is needed,
  *you* (or a relay) apply it — the independent check stays independent.
- **The worktree shows tracked + untracked state, not ignored files.** `.gitignore`d local context is
  excluded from what advisors see; reference it inline in the question if it matters.
- **Cost capture is not available for agy.** agy has no JSON/token output, so an agy lane is cost-blind
  (a floor). Codex token parsing is also still deferred. Neither lane captures `tick cost` events in a consult.
- **Needs the shims present, but is not tied to one repo.** Unlike `relay` (model-agnostic, file-only),
  consult hard-depends on the `codex` + `agy` CLIs being installed and authed and on the
  `relay-automation` shims. Those shims can live at the repo root **or** in a vendored `.xyz/` install,
  so any repo carrying a `.xyz/` (see `relay-automation/xyz-vendor.sh` in XYZ-forge) can run consult standalone.

## Gotcha: run consult OUTSIDE Claude Code's Bash sandbox

If you launch `consult.sh` from a Claude Code session, **disable the Bash sandbox for that call**
(`dangerouslyDisableSandbox: true`). **Both advisors fail under the sandbox:**
- **Codex** — the sandbox blocks the macOS keychain (`no native root CA certificates found` / `No keychain is available`) and does not allowlist `chatgpt.com`.
- **agy** — the sandbox blocks agy's backend network; `agy -p` exits 0 with **empty output** (the shim treats this as a hard failure, exit 5).

The symptom is a two-sided `0 answered, 2 failed` degrade. Disabling the sandbox here is safe:
consult's isolation comes from its **throwaway worktree** (and Codex's own `-s read-only`), not from
the Bash sandbox, so nothing is weakened.

## What success looks like

The operator asks one question and gets back a single, honest, reconciled answer that **shows its
seams** — what the two models agreed on, where they split, and which way the coordinator called it and
why — in one step, with both raw transcripts on disk for audit.
