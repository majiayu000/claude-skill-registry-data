---
name: guard-red-team
description: Use whenever authoring or modifying ANY deny-list, guard regex, lint rule, policy file, or enforcement hook (config/agent-os/policy.json, pretool hooks, lint-source rules, CI gates). A guard that goes green on its own canaries is unproven - adversarially probe the REAL binary end-to-end before trusting it.
triggers: deny-list, guard regex, lint rule, policy file, enforcement hook, policy.json, pretool hook, ci gate, bypass, false positive, adversarial probe, canary green, exit codes, audit the hook
---

# Guard Red-Team

An enforcement layer that has only passed its own happy-path canaries is
**unproven, and worse than nothing** — it reads as safety while providing
none. The first draft of `config/agent-os/policy.json` went green on its
own canaries; a 4-lens adversarial review then ran 31 end-to-end probes
through the real `pretool.mjs` and proved **22 bypasses and 7 false
positives** (PR #1355).

## The rule

**Never trust a green first run of a guard you just wrote.** The check may
be mis-scoped, the regex may anchor wrong, the harness may not even be
invoking it. Green proves the test ran; only adversarial probes prove the
guard guards. Run the mutation BEFORE trusting the first green: on
2026-08-26 **four out of four** first-draft canaries in one session were
blind in ways only the mutation showed — an arm reading stdout while the
banner went to stderr (`expected '' to contain 'SKIPPED'`), a `--root`
fallback silently scanning the live repo and exiting 0, a docstring
assertion satisfied by its own changelog quote, and a discovery arm whose
first run found a fourth subject the hand-audit had missed.

## Protocol

1. **Probe the REAL binary end-to-end.** Feed candidate commands through
   the actual hook/linter process and assert on **exit codes**, not on
   your reading of the regex. **For a DENY canary, a nonzero exit is NOT
   proof** - config and parse errors exit nonzero too (witnessed
   2026-08-27: a dependency-cruiser deny-canary "passed" on a TS18003
   config error, #1935); assert the specific rule/violation id appears
   in the OUTPUT as well. A regex you reason about is a regex you
   excuse. **Attribute before fixing:** this machine runs MULTIPLE guard
   layers (repo pretool + the Claude-harness sandbox), and a block banner
   without the repo's "BLOCKED by repo policy: <id>" attribution is NOT
   the repo policy. Witnessed 2026-08-04: all three false positives that
   session were the harness layer — the repo policy probed clean and the
   only correct repo change was defensive allowExamples (#1364), not a
   "fix" to a rule that never fired.
2. **Run the minimum probe set** — every class below produced a verified
   bypass or false positive in the #1355 red-team:
   - **Tool global-option prefixes** — `git -C <path> push origin main`
     defeated every git rule at once (rules anchored on `git push`).
   - **Implicit / default arguments** — `git push` with no refspec, or
     `HEAD`, reaches the current branch's upstream unnamed; a ban that
     needs the word `main` never fires.
   - **Flag families and bundled short flags** — `prisma migrate reset`
     slipped past a ban written for `--accept-data-loss`; `-rf` is not
     `-r -f` to a naive matcher.
   - **Quoting, here-strings, heredocs** — content smuggled through
     PowerShell `@'...'@` and bash heredocs; also the top FALSE-POSITIVE
     source (the hook blocked its own author three times on
     mention-vs-execution: an e2e test command, a commit message quoting
     a flag, a proposals-file append).
   - **Chaining** — `;`, `&&`, `|`, subshells: does the guard see the
     second command in a compound line? The inverse matters just as much:
     a rule whose scan doesn't STOP at a chain operator can reach INTO an
     unrelated later command. Witnessed 2026-09-01/09: `force-push`'s
     bundled-short-flag arm (`\s-[a-eg-uw-z]*f[a-z]*\b`, written for git's
     own `-f`/`-uf`) matched `gh api`'s unrelated `-f` (field) flag across
     an `&&` boundary — `git push origin <branch> && gh api ... -f
     body="..."` was wrongly denied. `push-to-main` had already solved
     this with a scan restricted to `[^;|&\n]*?`; `force-push` had not.
     Fixed by applying the same restriction (config/agent-os/policy.json,
     verified: the false positive now passes, all denyExamples still
     deny). Any rule using a bare `[^\n]*?` scan after the verb is a
     candidate for the same bug — check it, don't assume the fix in one
     rule propagated to its siblings. Second and third siblings, 2026-10-25:
     `add-all` denied a one-path add chained with `ledger-check.mjs --root .`
     (false positive, hit the manager twice), and `destructive-restore`'s
     `--staged` lookahead let `git restore <file> && git diff --staged`
     through (a bypass). Both now scan `[^;|&\n]`. Rules that cross a chain
     on purpose (destructive-sql, worktree-recursive-delete, the night-shift
     inline-script arm) are listed in `docs/agent-os/README.md` Layer 4.
   - **Reachability chain-tracing** — for any "X is reachable/triggerable"
     claim about an enforcement surface (a canary, a registered tool, a
     cron job), trace the FULL chain to the entry point that will
     ACTUALLY be used (route → auth gate → allowlist → runner), and probe
     the chain, not the registry. Membership in a lookup table is never
     reachability (witnessed 2026-08-25: a staging canary asserted
     `registerAllJobs()` membership and called it reachability, while the
     real trigger route 403'd both staged names via a separate allowlist
     the canary never touched — caught only by an independent review).
   - **Mention vs execution** — text that only QUOTES a forbidden string
     (docs, commit messages, test fixtures) must pass. A guard that
     blocks its own documentation will be disabled by a frustrated
     human, and then it guards nothing. Witnessed at its purest
     2026-08-04: the commit DOCUMENTING two false positives was itself
     blocked because its here-string quoted the cmdlet. **The inverse
     bites assertions:** a changelog or comment quoting an OLD value
     satisfies a bare `toContain` — witnessed 2026-08-26, a docstring
     canary asserting `toContain("65,000")` stayed green when the claim
     was staled to 40,000, because the changelog paragraph recording the
     old wrong value still contained the string. Capture from the
     authoritative sentence and compare VALUES; never assert a mention.
   - **Probe from a script file that builds guarded literals from parts.** A
     Bash command string that QUOTES `git push --dry-run origin main` as probe
     data is itself judged and blocked, which proves the guard but not the
     probe (witnessed 2026-10-18: the manager's rtk-plus-repo-guard probe only
     ran once the literals were assembled inside `probe-rtk-guard.mjs` and the
     command line named only the script).
   - **Drive-qualified paths** — PowerShell `Env:`, `HKLM:`, `Cert:` are
     provider paths, not filesystem paths. Witnessed 2026-08-04: a
     compound command containing the standard env-token removal cmdlet
     was blocked as a system-path "/" delete.
   - **Argument bleed across a compound** — a path/regex-looking literal
     in an ADJACENT argument or statement must not be attributed to the
     guarded verb. Witnessed 2026-08-04: a backup-file delete plus an
     unrelated `'^\s*Tests'` regex in the same command was blocked as
     deleting the path "\s".
3. **Lock every verdict.** Every verified bypass becomes a permanent
   deny-example test; every false positive becomes a permanent
   allow-example test. The probe set only grows.
4. **Re-run the full probe set after ANY edit to the guard** — a fix for
   one bypass routinely reopens another (the #1355 matching-layer rebuild
   took an hour precisely because fixes interacted).
5. **Prove the hook FIRES from its configured command string, on every
   platform sessions run on.** A canary that calls the script directly, or
   one that "normalises" the configured command before running it, proves the
   policy and says nothing about the wiring. Witnessed 2026-09-23: every node
   hook in `.claude/settings.json` named its script with Windows backslashes,
   so on Linux (every cloud session) it was MODULE_NOT_FOUND, exit 1, fail-open:
   all 13 rules were off there, while `memoryHook.test.mjs` passed on Linux CI
   because it rewrote `\` to `/` before running. `scripts/agent-os/hookCommand.test.mjs`
   now runs each configured command verbatim through a shell and asserts the
   deny exit AND the rule id; `scripts/cloud-doctor.mjs` repeats it per session.
6. **A canary that SPAWNS git must strip `GIT_*` env vars before it runs.**
   Hooks inherit `GIT_DIR`/`GIT_INDEX_FILE` from the real commit that
   triggered them; a fixture repo-init under an inherited `GIT_DIR`
   re-initializes the SHARED `.git`, not a scratch one. Witnessed
   2026-08-25: exactly this took down every linked worktree's git ops
   machine-wide, and every commit retry re-planted the damage until the
   env was stripped in both the canary and `stop-check.mjs`'s own runner.
   Red-team every canary in the context it will actually run (hook env),
   never standalone-only.
7. **A shell's exit code for "not found" is not portable** (bash 1, dash 127,
   `where.exe` 1). Any status-to-verdict mapping lives in an exported function
   with a unit test per code (0, 1, 127, 2, ENOENT, a signal), and a branch
   labelled NOT CHECKED may not carry a test that assumes the checked branch's
   behaviour. Witnessed 2026-10-18 (PR 3150): `session-surface.mjs` treated only
   exit 1 from `command -v` as MISSING; Linux CI's `/bin/sh` is dash, exit 127,
   two canaries went red; fixed by an exported `classifyLookup` (95462f05f).

## Red flags

- "The regex obviously covers that" — probe it anyway; 22 bypasses were
  all "obviously covered".
- "I'll add probes after it ships" — an unprobed guard in the merge is
  false safety at its most trusted moment.
- "The canaries pass" — canaries the author wrote test the author's
  imagination, not the adversary's.

## When NOT to use

Pure display/formatting lint (no security or policy consequence), or
guards you are deleting. For verifying a FIX against a bug, use the
mutation-verification discipline in the per-app verify skills instead —
this skill is specifically for enforcement surfaces whose failure mode
is silent permission.
