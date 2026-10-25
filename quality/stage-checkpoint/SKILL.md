---
name: stage-checkpoint
description: Closes a stage with evidence. Runs the checks, the relevant agents and the time measurement, updates the logs and writes the stage report. Use at the end of every stage before asking the owner to merge.
---

# Stage checkpoint

1. Record the end time with `date` and compute elapsed time from the stage start logged in `docs/ai-log.md`,
   and the budget used since the first commit (`docs/PLAN.md`).
2. Run the checks that exist and keep their output: lint, typecheck, tests, `node scripts/brand/generate-tokens.mjs --check`,
   `node scripts/brand/contrast.mjs --check`, `node scripts/validate-claude-config.mjs`. From Stage 2, Lighthouse for
   any change to config, layout or the page shell.
3. Run `code-reviewer` on the diff, plus the agents whose scope the diff touches. Fix blockers before continuing.
4. Re-read every changed doc against the code.
5. Update `docs/ai-log.md` (delegated, corrected, rejected, how validated, time), `docs/ASSUMPTIONS.md` and
   `docs/DECISIONS.md`.
6. Confirm no process you started is still running (`lsof -i :<port>`).
7. Report to the owner, in Spanish: what was done, decisions and why, manual checks, risks, measured time, and the
   PR link. Wait for "continue".
