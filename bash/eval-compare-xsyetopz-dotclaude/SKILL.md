---
name: eval-compare
description: Compares the eval scores of two plugin folders, such as a plugin and a variant of it. Use when the user wants to know whether a change to a plugin raises or lowers its eval score.
disable-model-invocation: true
---

<task>
Compare the eval scores of two plugin folders for the user.
</task>

<procedure>
Each run costs money and takes minutes, so confirm the two folders with the user before the run.

1. Find the two plugin folders.
   Each one has a `.claude-plugin/plugin.json` file and an `evals/` folder.
   If the user names a git ref instead of a folder, ask for a folder, or tell the user to check out the ref in a `git worktree`, because the command reads folders and not refs.

2. Run the comparison:

   ```bash
   claudetto-eval-compare A B
   ```

   Replace `A` and `B` with the two folders.
   Add `claude plugin eval` options after them when the user asks for them.
   The command adds `--max-cost-usd 5` for each run when the options set no bound.
   The command adds no `--scaffold` and no `--allow-tools`, because they run the scripts and the tools of the suite as the user.
   If the cases need them, ask the user before you add them, and name the folders whose suites will run.
   The skill grants no tool, so Claude Code asks the user before each run.
   If a run stops at the cost bound, tell the user, and do not raise the bound without the user.

3. Read the two result tables.
   Compare the `WITH` column of table A with the `WITH` column of table B, case by case.
   Do not compare the `WITHOUT` column of the two tables as a plugin result, because it is the shared baseline.
   If the two baseline scores differ by more than the gap between the arms, say so, because the model varies between runs and the gap is then weak evidence.
</procedure>

<output>
Give the user a short table of the cases, with the score of each arm.
Then say in one sentence which arm scores better, and by how much.
</output>
