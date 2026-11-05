---
name: specwright-review
description: "Reviewer routes and the pre-ship review for Specwright changes. Chooses the reviewer (codex, claude, omp CLI or the specwright-reviewer subagent) from review.order, runs it isolated and read-only through scripts/review-run.sh, validates the output and fails closed. Pre-ship mode reviews the finished main...HEAD diff before the first PR or a local merge, blocks on P0/P1 findings, and sets the rules for fixes, waivers and spec amendments. Triggers: 'review before ship', 'run the pre-ship review', a design review step (FULL tier, roadmap baseline) choosing its reviewer, or specwright-commit, specwright-pr ship and specwright-finish calling it."
metadata:
  version: 0.11.0
---

# Specwright Review

The script lives in `${CLAUDE_SKILL_DIR}/scripts/` (in other harnesses: the `scripts/` folder next to this SKILL.md); below, `scripts/review-run.sh` means that path, and other skills call it `<specwright-review>/scripts/review-run.sh`. Run it with `bash` (Git Bash on Windows) from the code checkout. It needs bash, git and Python 3.8+, makes no `gh` call, and prints one JSON document per call. Exit 0 = ok, 1 = stop (show its `message`), 2 = usage error, 3 = failed review.

## Settings

Read from `openspec/specwright.yaml`; every key is optional:

```yaml
review:
  cross_model: true          # false = the specwright-reviewer subagent only, no CLI
  order: [codex, claude, omp] # routes tried in order; the current harness is skipped
  models:                    # per route; omit = the CLI's default
    omp: "@default"          # an OMP role (@slow) or provider/id
  thinking: {}               # per route: codex reasoning effort, claude --effort, omp --thinking (provider/id only)
  timeout: 20m               # per review run; the reviewer is killed after it
  max_diff_kb: 1024          # pre-ship input bound (code + store diff); over it, no review runs
  preship: true              # false = no pre-ship review and no ship/merge gate
```

## Routes

Every review (design or pre-ship) picks its reviewer the same way:

1. **Select:** `bash scripts/review-run.sh select --runtime <claude|codex|omp|other>`, where `--runtime` is the harness you are running in (`other` skips nothing). It prints `route` (`codex`, `claude`, `omp` or `subagent`), `skipped` (each route with its reason: `current runtime`, `not installed`, a failed probe, or OMP's `Model "<m>" not found`), `model` and `thinking`. Save the output to a temp file: `run` takes it as `--selection` so the receipt lists the skipped routes. Exit 1 (an unknown name in `review.order`) → stop and show the message.
2. **CLI route** → `run` (below). The script holds one fixed, read-only command line per CLI; never build or change a reviewer command line yourself.
3. **`subagent`** → dispatch the `specwright-reviewer` agent with file paths, never your reasoning, then validate what it wrote with `record` (below). If no such agent is installed, stop and tell the user.
4. **Background.** A review takes minutes, up to `review.timeout`. Start `run` in the background (Claude Code: `run_in_background`; other harnesses: their background or blocking exec) and wait for it to finish; do not poll it.
5. **Exit 3 is a failed review** (`status: invalid`, `timeout`, or the reviewer crashed): nothing was reviewed. Never try the next route, never review the change yourself, and never treat it as a pass. Report the route, the status and the error, and offer to run it again. A failed pre-ship review stops ship and the local merge until a review passes.
6. **Receipt.** Report the receipt from the output: the route, the skipped routes with their reasons, and the requested and actual model and level (`unknown` when the CLI does not say). The receipt's `process_group` says how the reviewer's processes were held together (`job` on Windows, `session` on POSIX); `none` (with `process_group_reason`) means Windows could not make a job object, and a stopped reviewer's tree was then stopped from the reviewer's own process.

## Design reviews

The schema's review step (FULL tier) and the `specwright-roadmap` baseline review use the routes above:
- **CLI route:** write the review request (the same request the review step describes: the files to read, the installed project skills that apply, the review template) to a temp file, then `bash scripts/review-run.sh run --kind design --route <route> --prompt-file <request file> --out <review file> --change <change-name> --selection <select output>` (store-backed: `--store <store toplevel>`, so the Claude route can read the planning files). `<review file>` is the change's `review.md`; for the roadmap baseline it is `openspec/architecture-review.md` and `<change-name>` is `baseline`. The script writes it only after the output has exactly one `VERDICT: <v>` line (`<v>` is `APPROVE`, `APPROVE_WITH_CHANGES` or `REVISE`) and exactly one `CHANGES_APPLIED: <c>` line (`no` or `yes` after `APPROVE_WITH_CHANGES`, `n/a` after the other two); `BLOCKED`, `USER_OVERRIDE`, `SKIPPED_LIGHT`, `DEFERRED`, `WAIVED` or any other value is invalid, and the error names it. On exit 3 the file is untouched. `codex` on Windows needs Python 3.11+ for the script to pass on your `windows.sandbox` setting (see the Windows note below); without it the review still runs, but codex may not be able to read the checkout, and the check above then refuses a `BLOCKED` result.
- **`subagent`:** first ask the script for a result file, `bash scripts/review-run.sh record --kind design --change <change-name> --scratch`, which prints `scratch`, a fresh result file under the state dir, outside the change. The `specwright-reviewer` agent writes its review to that file, never to the review file. Then `bash scripts/review-run.sh record --kind design --change <change-name> --result <scratch> --out <review file> --route subagent --selection <select output>`: it writes `<review file>` atomically only when the review validates (the same check as above) and removes the scratch file. Report its `receipt` (Routes step 6). Exit 3 → the review is invalid: `<review file>` is left as it was (an earlier review stays), the output names the scratch file, the tasks step does not start; run the review again. Bare `record` without `--out` still validates a file in place, but design reviews do not use it.

**Windows and codex.** The codex route always ignores the user's codex config (`--ignore-user-config`). On Windows only, when that config's `[windows] sandbox` is a plain name (such as `elevated`), the script passes just that setting as `-c windows.sandbox="<name>"` and lists it in the receipt as `windows_sandbox`; nothing else in the file is used. Reading the file needs Python 3.11+ (`tomllib`); on an older Python nothing is passed.

## Pre-ship review

Reviews the finished change, `<main>...HEAD` of the code repo and, store-backed, of the store, before the change's first PR or a local merge. With `review.preship: false`, skip this whole section and the gate.

**When.** `specwright-commit` step 3 runs it once every task is committed. `specwright-pr` ship (before the change's first PR) and `specwright-finish` (before a local merge) run the **gate** first and come here only on `missing`.

1. **Review.** Resolve the planning repo as the calling skill does. Select (Routes step 1), then:
   - CLI route, in the background: `bash scripts/review-run.sh run --kind preship --route <route> --change <change-name> --out <findings file> --base <main> --prefix <P> --selection <select output>`, store-backed adding `--store <store toplevel> --store-base <store main>`. `<P>` is the planning prefix, as `specwright-pr` defines it (default `openspec`, relative to the code toplevel). The script builds the input itself (both diffs, the changed files, the change's artifact paths, `references/brief.md`), checks it against the findings schema, and records the result for the reviewed head.
   - `subagent`: first `bash scripts/review-run.sh preflight --kind preship --change <change-name> --base <main> --prefix <P>` (store-backed: `--store <store toplevel> --store-base <store main>`) and save its output. It applies `review.max_diff_kb` to the same combined diff `run` reads, before any reviewer starts (exit 1 `diff_too_large`: handle it as below), and prints the heads the review covers. Then dispatch `specwright-reviewer` in pre-ship mode with the change name, the preflight `artifacts` (the artifact paths to read: archived ones once the change is archived), the base, the planning root (`root.path`) and `<P>`, the store id when the session selected a store (the agent passes it to `openspec list --json` as `--store <id>`), the store toplevel and base when store-backed, `references/brief.md`, `references/findings.schema.json` and the path of the findings file to write; then `bash scripts/review-run.sh record --kind preship --change <change-name> --result <findings file> --route subagent --preflight <preflight output> --selection <select output>` (store-backed: `--store <store toplevel>`). If HEAD moved since the preflight, `record` exits 3 with `heads_moved` and writes nothing: run the review again.
   - Exit 1 `diff_too_large` → no reviewer ran. Report the size and ask the user to raise `review.max_diff_kb` or set `review.preship: false`. Never review a cut-down diff.
   - Exit 3 → Routes step 5.
2. **Read the result.** P0 and P1 findings block; P2 and P3 do not. No P0/P1 → the review passed: report it and hand back to the caller. Leave P2/P3 findings as they are: the PR description lists them, and fixing them now would leave the new head without a pass. Fix them only when the user asks, or in a round commit you make anyway (step 4).
3. **Blocked.** Show every open P0/P1 finding (id, file, title) with the options: fix, or waive. A waiver comes only from the user: run `bash scripts/review-run.sh waive --change <change-name> --prefix <P> --finding <id> --reason "<the user's reason>"` (store-backed: `--store <store toplevel>`) only after the user explicitly answers that this finding is accepted, with their reason. Never waive a finding on your own judgement. No answer → no pass, and ship does not start. Once every P0/P1 is waived, `gate` reports `pass`.
4. **Fix round.** Before fixing anything, `bash scripts/review-run.sh rounds --change <change-name>` (store-backed: `--store <store toplevel>`) gives `n`, the highest `Preship-Round:` trailer on the branch in either repo. When `n` is 2 or more and the review still has an unwaived P0/P1, stop fixing: list the open findings and ask the user how to proceed (another round, waive, or stop). Otherwise this is round `n+1`:
   - fix each `code` and `test` finding, test-first where it changes behaviour, and run the tests;
   - commit the fixed files by name under the `specwright-commit` rules (`bash <specwright-pr>/scripts/vcs.sh commit --repo <toplevel> --role code --branch <branch> --message-file <msgfile> -- <files>`; the store: `--repo "<store toplevel>" --role store --code "<code toplevel>"`), one commit per changed repo (store-backed: the store first, same subject and trailer in both), with the subject `<type>(<change-name>): address pre-ship review` and the trailer `Preship-Round: <n+1>`. Never use `address review feedback` or a `Feedback-Round:` trailer for these: those count PR fix rounds;
   - run a new pre-ship review (step 1): the new head has no pass until one passes.
5. **Spec findings** (`category: spec`) carry the reviewer's `spec_class`:
   - **clarification:** one reading of the spec fits every other scenario, and the code and tests already match it. Check that yourself. If it holds, edit the wording in the planning repo and commit it by name (`vcs.sh commit`, as above) as `<type>(<change-name>): amend specs` with the trailer `Amendment: clarification`, then run a new pre-ship review. If it does not hold, treat it as a behaviour change.
   - **behaviour_change:** after the edit, the requirement or scenario would allow something different. Do not edit the spec. Ask the user whether to change the behaviour (the spec, then the code) or the code to fit the spec. Only on their approval: follow the apply drift rule (an `amend specs` commit with the trailer `Amendment: behaviour-change`, a new design review step when the tier is FULL, test and code updates), then run a new pre-ship review.
   - You may treat a clarification as a behaviour change and ask; never the other way round.
6. **Report:** the route and receipt, the findings by priority, what was fixed, amended or waived, and the P2/P3 findings left open.

## Gate

`bash scripts/review-run.sh gate --change <change-name> --prefix <P>` (store-backed: `--store <store toplevel>`) prints `status`:
- `pass`: a record for the current head (or the head before the change's archive commit) has no unwaived P0/P1. Continue.
- `missing`: no record for this head (a new commit, another machine, a lost state dir). Run the pre-ship review.
- `blocked`: the record has open P0/P1 findings (`open`). Go to Pre-ship review step 3.
Records are machine-local (ADR 0007), so a `missing` from another checkout only costs a review.

## Archive-only check

`specwright-pr` watch runs `bash scripts/review-run.sh archive-only --base <ready head> --head <archive head> --change <change-name> --dir <planning repo toplevel> --prefix <P>` after the archive push. `archive_only: true` means the only commit is the change's `archive change` commit and it touches only the archive paths and the synced main specs.

## Credits

The reviewer brief and findings format draw on compound-engineering's [`ce-code-review`](https://github.com/EveryInc/compound-engineering-plugin) skill and oh-my-pi's [`reviewer.md`](https://github.com/can1357/oh-my-pi) agent.
