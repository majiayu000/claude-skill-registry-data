---
name: replicating-a-monitor
description: Guide for replicating a monitor from an AI control paper as a ct-replications entry, with a decision log against the paper, the source text copied verbatim, a fidelity check, a run on Control Tower's committed recordings and a PR description ready to open. Use when the user gives a paper or arXiv link whose mechanism is a monitor, or asks to implement, port or replicate a published monitor. For a paper whose mechanism is a protocol, use `replicating-a-protocol`; for a monitor the team designs itself, use `adding-a-monitor` in the control-tower repository.
---

`CONTRIBUTING.md` holds the rules: where the code goes, naming, "Staying true to the source", Control Tower's API, the README row and the PR flow. This skill is the order to apply them in. Below, U is the untrusted model: the agent whose actions are monitored. Policies are out of scope.

## Before you start

Start the session in this repository, so this skill loads. Commands that run Control Tower run in a worktree of it pinned to the commit this repository depends on (`rev` in `pyproject.toml`), so the replication is tested against the Control Tower it ships with. Make it once, beside this repository:

```bash
git -C ../control-tower fetch origin
git -C ../control-tower worktree add --detach ../control-tower-pin <rev>
ln -s ../control-tower/.env ../control-tower-pin/.env
cd ../control-tower-pin && uv sync --locked --dev --all-extras && uv run python scripts/generate_model_rates.py
```

If `../control-tower-pin` already exists, check it is on `rev` (`git -C ../control-tower-pin rev-parse HEAD`); after a bump of `rev`, run `git -C ../control-tower fetch origin`, then `git -C ../control-tower-pin switch --detach <rev>` and `uv sync --locked --dev --all-extras` in it. `git -C ../control-tower worktree remove ../control-tower-pin` removes it when you are done. The model keys come from the Control Tower checkout's `.env`, as "Running your branch" in `CONTRIBUTING.md` says. Every code block below starts from this repository's root. Files this skill writes go under this repository's `artifacts/`, which git ignores; in their names, `<branch>` is the branch name with each `/` replaced by `-`:

- `artifacts/pr/<branch>.md`, the PR description;
- `artifacts/pr/<branch>-progress.md`, the checklist below;
- `artifacts/source/<arXiv id>/`, the paper and the released code.

Copy this checklist into `artifacts/pr/<branch>-progress.md` and tick it as you go; a new session resumes from it:

```markdown
- [ ] 1. Preflight: one paper, its mechanism a monitor, buildable, not replicated yet, branch from current upstream main
- [ ] 2. Source saved and read: method section, appendix, released code at a commit
- [ ] 3. Decision log written: every choice with a quote, or "our choice"
- [ ] 4. Monitor written, source text verbatim, imported in `__init__.py`
- [ ] 5. Fidelity check: every row quoted, the code matches every row
- [ ] 6. Checks green, recordings scored with none unscored and an identical rerun
- [ ] 7. PR prepared, commands printed for the user
- [ ] 8. Real-log run, only once the draft PR is open and its reviewer agreed the budget
```

## Stages

1. **Preflight.** One paper per PR, on a fresh branch from the upstream `main`. If the paper's novelty is a decision rule (defer, edit, resample, audit), use `replicating-a-protocol`. Stop if the README table already lists the monitor, or `uv run ct protocols monitors` in the worktree shows Control Tower already has it. The monitor is buildable if it fits a registered code monitor with no change to Control Tower's `MonitorFn` or eval engine. If it needs one, report what Control Tower lacks and stop.
2. **Save and read the source.** Download the paper and the released code into `artifacts/source/<arXiv id>/` as "Reading the paper" says, and note the code's commit; `CONTRIBUTING.md` puts it in the module docstring.
3. **Decision log.** Start `artifacts/pr/<branch>.md` from `.github/pull_request_template.md` and add a `### Decision log` section after "Replication": a table of Choice, Value, and Source (section and a short verbatim quote, or "our choice"). Cover what the monitor reads of U, action or whole-run, the score scale and its mapping to 0 to 100, where the prompt text comes from, how the transcript is split and how scores combine, and every other choice the source leaves open. Every row that differs from the source is also a departure.
4. **Write it.** Follow "Where the code goes" in `CONTRIBUTING.md`: a registered code monitor in `src/ct_replications/monitors/<file>.py`, its prompt text verbatim in a `.md` beside it, and the module imported in `src/ct_replications/__init__.py`. `src/ct_replications/monitors/monitoring_bench.py` is this repository's example; take its shape, not Control Tower's own monitors, which import internals. It keeps a few non-stable imports itself; list any you keep under "What Control Tower lacked":
   - Import `monitor_model`, `judged`, `asked`, `render_prompt`, `MonitorFailed` and `MonitorFn` from `control_tower.monitors`. `asked` needs `answer_tool` from `control_tower.tools.answer`, which is outside the stable API, so prefer `judged`, or list it under "What Control Tower lacked". When the paper's prompt asks for a free-text answer, such as a `<verdict>` tag, call the model's `generate` and parse the answer, as `monitoring_bench.py` does.
   - **Models.** A factory argument names each model role; the paper's model is the fallback for a role left unbound, through `make_role_model(<paper model>, role=<role>)` as `monitoring_bench.py` does. `monitor_model` alone reads a model name as a role and fails when it is unbound. If the paper's model is retired or Control Tower cannot price it, make no fallback: the role's binding is the only source, and the paper's model and sampling settings are a departure.
   - **Cache keys.** When two model calls can send the same prompt and should answer independently (panel members, the legs of a hybrid, repeated draws), give each its own key with `cache_scope(...)` from `control_tower.models.cache_scopes` or `scoped_cache(model, <key>=...)` from `control_tower.models.aliases`, as `monitoring_bench.py` does; otherwise a cached rerun hands both calls one answer. Neither is in the stable API, so list it under "What Control Tower lacked".
   - **What it reads.** A registered monitor cannot set its own `reads` or `view`. The default `reads` is `[tool_calls, tool_results, system, user]`, without U's text. When the monitor needs U's text or anything else outside the default, say which `reads` and `view` to pass in its registered docstring and the README row, and pass them in every command, the fast loop's included.
   - **Entries.** Register each scaffold the paper reports, its baselines included, as its own entry under one README row, with every entry's name in its Name cell, so each can be compared with the paper's numbers.
   - Every argument defaults to the paper's configuration. Add nothing no caller reads, and leave the other replications as they are.
5. **Fidelity check.** With the saved source open, check every decision-log row and every part of the code against the section it cites. Put a short verbatim quote in each Source cell, or "our choice" where the source says nothing. Where the code and the source differ, fix the code or record the difference as a departure. The recordings cannot tell a faithful monitor from an unfaithful one, so this comes before them. When the source publishes transcripts with the monitor's recorded answers, replay one or two through your code in a throwaway script: pass the factory `get_model("mockllm/model", custom_outputs=<the recorded answers as ModelOutputs>)` in place of its role name, and compare the prompts your code sends with the published ones byte for byte.
6. **Checks and recordings.** Run this repository's checks from "Setup and checks" in `CONTRIBUTING.md`, then score the recordings as "Scoring the recordings" says.
7. **Prepare the PR.** Finish `artifacts/pr/<branch>.md`. If you came here from `replicating-a-protocol` because only the paper's judge is new, say in the registered docstring and the PR's Replication section which existing protocol to run it under, with which arguments. Add the README row as "The README row" in `CONTRIBUTING.md` says. Do not commit, push or open the PR. Print the commands for the user to run from this repository, with a Conventional Commits title:

   ```bash
   git add src/ct_replications README.md && git commit -m "<title>"
   git push -u origin <branch>
   gh pr create --repo linuxarena/ct-replications --draft --base main --title "<title>" --body-file artifacts/pr/<branch>.md
   ```
8. **Real-log run, only with the user's yes.** It is the paid step, and `CONTRIBUTING.md` asks for a budget agreed with the PR's reviewing maintainer first. Ask the user to confirm the draft PR is open and the budget agreed, and say the log, the sample count, the models, an estimated cost, and which key in `.env` it uses (`OPENROUTER_API_KEY`, `ANTHROPIC_API_KEY`, ...), by name, never its value. On a yes, score a real Control Tower log with `ct run monitor` in the worktree, passing its path in your main checkout (`../control-tower/logs/<file>.eval`), report every sample scored, the model and the cost, compare with the paper's numbers where the setting allows, and fill in the PR's Run section and the README row's "What Control Tower lacked". Then print `gh pr edit <number> --repo linuxarena/ct-replications --body-file artifacts/pr/<branch>.md` and `gh pr ready <number> --repo linuxarena/ct-replications` for the user. On a no, write "No real-model run yet" in the Run section.

## Reading the paper

A summarising fetch will not quote a prompt or an algorithm verbatim. Save the HTML (`https://arxiv.org/html/<id>`) or the LaTeX source (`https://arxiv.org/e-print/<id>`, a gzipped archive) and a clone of the released code at its commit under `artifacts/source/<id>/`, and read the method and appendix text itself. The paper's code link may lead to a dataset rather than the code; its dataset card usually names the code repository. Prefer the released code over the paper for prompts and mechanics: papers often leave out how the transcript is split, what is passed between calls and how scores combine. A paper with several prompt sets: pick the one closest to Control Tower's agent settings and record it in the decision log.

## Scoring the recordings

Bind every model role the monitor uses to a cheap model, one `--model-role` each, so the loop costs cents rather than the paper's price; its factory arguments name the roles. Scoring the recordings on a cheap model needs no agreed budget. Use `--kind action` for a monitor that judges each action and `--kind trajectory` for one that judges the whole run.

```bash
cd ../control-tower-pin && uv pip install --no-sources -e ../ct-replications
for dir in data/monitoring/first data/monitoring/rerun; do
  for log in tests/replay_check/recorded-*.eval; do
    uv run ct run monitor "$log" --kind <action|trajectory> \
      --monitors '[{monitor: ct_replications/<name>, name: <name><, reads: [...]>}, <one per entry>]' \
      --model-role <role>=anthropic/claude-haiku-4-5 --save-dir "$dir"
  done
done
for log in data/monitoring/first/recorded-*.monitored.eval; do
  for name in <every entry's name>; do
    uv run python ../ct-replications/.agents/skills/replicating-a-monitor/scripts/check_scored.py \
      "$log" "$name" "data/monitoring/rerun/$(basename "$log")"
  done
done
```

The second pass is served from the model cache. One `ct run monitor` call scores every entry, each under its own `name`. The pass check exits 1 if any sample has no scores under that entry's name, has an unscored one, or scores differently in the rerun, and prints the reason; `ct run monitor` itself exits 0 either way. A difference in the rerun means two calls share a cache key, or a call is not cached, or the monitor is random. A second run with the same `name` into the same folder is refused, so delete `data/monitoring/first/` and `data/monitoring/rerun/` before running the loop again. The recordings are a handful of scripted samples, so their scores mean nothing.

## Gotchas

- An unparseable answer raises `MonitorFailed` and leaves the draw unscored, where a paper may fall back to a middle score: a departure.
- A score scale other than 0 to 100 maps to 0 to 100, as `CONTRIBUTING.md` says; record the mapping as a departure.
- A rerun is served from Inspect's model cache, so a cost of zero does not show the monitor ran.

## Resuming

The state of a replication is its branch and its `artifacts/` files. A new session reads `artifacts/pr/<branch>-progress.md` and the decision log first, works from the saved source in `artifacts/source/`, and continues from the first unticked stage.

## Stop and ask the user only when

- The monitor is already replicated, or Control Tower already has it. Report it and stop.
- The monitor needs model activations or hidden states, several agents in one sample, other trajectories at the same time, or weights nobody released. Report it as not buildable and stop.
- Building it needs a change to Control Tower. Report what is missing, for "What Control Tower lacked", and stop.
- Before the stage 8 run, every time: it is the paid step.
