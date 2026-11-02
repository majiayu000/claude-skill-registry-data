---
name: run-checks
description: Re-run this repository's automated skill-loading checks against the installed harnesses (Antigravity CLI, Claude Code, Codex CLI, Copilot CLI), compare the verdicts with the previous run, and publish the changes. Use when asked to run or re-run the checks, test the harnesses on new releases, see whether skill behavior changed, bump agentsummons/agentminutes/skillxp and re-test, regenerate the platform reports or site, or write a changelog entry for a run.
---

# Run the checks

The full procedure, with the reasoning behind each step, is in
[benchmark-runner/RUNNING-CHECKS.md](../../../benchmark-runner/RUNNING-CHECKS.md).
Read it first; this file only tells an agent how to carry it out from
inside a session. When the two disagree, the document wins and this file
needs fixing.

## Division of labor

The maintainer runs the **Claude Code** portion from their own terminal.
The sandbox needs an OAuth token that is not in your environment, and a
headless `claude` run from inside this session shares the session's
subscription: the first time that was tried, the session limit hit
mid-run and every later finding was scored against a synthetic
"You've hit your session limit" message. Do not run `claude` through the
runner from this session, sandboxed or not.

You run the other three harnesses, validate everything, and prepare the
comparison and the publication steps.

## Steps

1. **Settle the tooling.** If the request includes a dependency bump,
   do it in `benchmark-runner/go.mod`, then build, vet, and test, then
   regenerate the reports from the existing results into the scratchpad
   and confirm they are byte-identical to `reports/`. Record the
   installed harness versions.

2. **Name the run.** Use `results/checks-YYYY-MM-DD`. Every harness,
   including the maintainer's Claude Code run, writes into that one
   directory.

3. **Hand off Claude Code immediately**, before starting your own
   processes, so both halves run in parallel. Give the maintainer this,
   with the directory filled in:

   ```bash
   export CLAUDE_CODE_OAUTH_TOKEN="<token from: claude setup-token>"
   cd benchmark-runner
   go run . -sandbox -harness claude-code -out results/checks-YYYY-MM-DD
   ```

   (If they keep the token in 1Password: export the `op://` reference
   instead and prefix the command with `op run --`.)

4. **Run the other three sandboxed, in parallel, in the background.**
   One process per harness, same `-out` directory. Fixtures are per-run
   temporary directories, so parallel processes are safe. Expect about
   25 minutes.

5. **Validate before comparing.** For every harness including the
   maintainer's: no `<synthetic>` or `isApiErrorMessage` in any
   transcript, a `model` on every observed finding, no activation check
   finishing in under about four seconds. A contaminated directory moves
   to the scratchpad, never gets deleted, and the harness is rerun.

6. **Rerun anything inconclusive** with `-runs 3` into the same
   directory before drawing conclusions.

7. **Ledger first, then diff.** `-ledger` the new results directory into
   `ledger/`, then `-ledger-diff` it against every ledger that made up
   the previous published state. The ledger must exist before the
   reports are regenerated or the new run gets no change markers.

8. **Classify, with transcripts open.** For each moved verdict, decide
   platform-level or model-level and say why, citing the finding's own
   notes and the transcript. A model swap between runs leans model-level;
   harness-injected text that changed is platform-level. Put the
   classification in front of the maintainer as a recommendation; the
   published call is theirs.

9. **Draft the changelog entry** at the top of
   `site/content/changelog/_index.md` in the established shape, then
   regenerate reports and site with every contributing results directory
   listed. Update hand-written pages that quote releases or now-stale
   behavior, setting `lastmod` on each. Build the site into the
   scratchpad and check the changelog, the comparison markers, and the
   guidance list order.

10. **Stop before committing** and report: what ran, what was validated,
    what moved and why, what is left for the maintainer.

## Reporting back

Lead with whether any verdict moved and whether the platform or the model
moved it. Say plainly what was not run or not verified. Take model names
and versions from the ledger, not from memory.
