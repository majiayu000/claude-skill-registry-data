---
name: replicating-a-protocol
description: Guide for replicating a blue-team protocol from an AI control paper as a ct-replications entry, with a decision log against the paper, a fidelity check, a replay of Control Tower's committed recording and a PR description ready to open. Use when the user gives a paper or arXiv link whose mechanism is a protocol, or asks to implement, port or replicate a published protocol (defer, edit, resample, gate, block, audit). For a paper whose novelty is only the judge, use `replicating-a-monitor`; for a protocol the team designs itself, use `adding-a-protocol` in the control-tower repository.
---

`CONTRIBUTING.md` holds the rules: where the code goes, naming, "Staying true to the source", Control Tower's API, the README row and the PR flow. This skill is the order to apply them in, plus the protocol API rules Control Tower's code does not show. Below, U is the untrusted model: the agent whose actions the protocol decides on. Policies are out of scope.

## Before you start

Start the session in this repository, so this skill loads. Commands that run Control Tower run in a worktree of it pinned to the commit this repository depends on (`rev` in `pyproject.toml`), so the replication is tested against the Control Tower it ships with. Make it once, beside this repository:

```bash
git -C ../control-tower fetch origin
git -C ../control-tower worktree add --detach ../control-tower-pin <rev>
ln -s ../control-tower/.env ../control-tower-pin/.env
cd ../control-tower-pin && uv sync --locked --dev --all-extras && uv run python scripts/generate_model_rates.py
```

If `../control-tower-pin` already exists, check it is on `rev` (`git -C ../control-tower-pin rev-parse HEAD`); after a bump of `rev`, run `git -C ../control-tower fetch origin`, then `git -C ../control-tower-pin switch --detach <rev>` and `uv sync --locked --dev --all-extras` in it. `git -C ../control-tower worktree remove ../control-tower-pin` removes it when you are done. The model keys come from the Control Tower checkout's `.env`, as "Running your branch" in `CONTRIBUTING.md` says. The stage 8 run also needs Docker and a setting pulled in the worktree, since settings pulled in your main checkout are not in it: `cd ../control-tower-pin && uv run ct settings pull <setting>`. Every code block below starts from this repository's root. Files this skill writes go under this repository's `artifacts/`, which git ignores; in their names, `<branch>` is the branch name with each `/` replaced by `-`:

- `artifacts/pr/<branch>.md`, the PR description;
- `artifacts/pr/<branch>-progress.md`, the checklist below;
- `artifacts/source/<arXiv id>/`, the paper and the released code.

Copy this checklist into `artifacts/pr/<branch>-progress.md` and tick it as you go; a new session resumes from it:

```markdown
- [ ] 1. Preflight: one paper, its mechanism a protocol, buildable, not a config of an existing protocol, not replicated yet, branch from current upstream main
- [ ] 2. Source saved and read: method section, appendix, released code at a commit
- [ ] 3. Decision log written: every choice with a quote, or "our choice"
- [ ] 4. Protocol written, registered with a name, imported in `__init__.py`
- [ ] 5. Fidelity check: every row quoted, every branch of the code matches its row
- [ ] 6. Checks green, replay ran to the end with every tool-call step noted
- [ ] 7. PR prepared, commands printed for the user
- [ ] 8. Real run beside an existing protocol, only once the draft PR is open and its reviewer agreed the budget
```

## Stages

1. **Preflight.** One paper per PR, on a fresh branch from the upstream `main`. Stop if the README table already lists the protocol. `uv run ct protocols protocols` in the worktree lists Control Tower's protocols; their arguments cover most classic ones. If the paper's novelty is the judge rather than the decision, it is a monitor replication: use `replicating-a-monitor`, and say which existing protocol to run it under, with which arguments, in the monitor's registered docstring and the PR's Replication section. The protocol is buildable if its decision fits one `Protocol` subclass with no change to Control Tower's `eval/blue.py`, `eval/red.py` or engine. If it needs one, report what Control Tower lacks and stop.
2. **Save and read the source.** Download the paper and the released code into `artifacts/source/<arXiv id>/` as "Reading the paper" says, and note the code's commit; `CONTRIBUTING.md` puts it in the module docstring.
3. **Decision log.** Start `artifacts/pr/<branch>.md` from `.github/pull_request_template.md` and add a `### Decision log` section after "Replication": a table of Choice, Value, and Source (section and a short verbatim quote, or "our choice"). Cover what the protocol sees and may do per action, what state it keeps, its monitors and how they combine, its thresholds and how they are fitted, resample counts, what U reads when blocked, and how it audits. Every row that differs from the source is also a departure.
4. **Write it.** Follow "Where the code goes" in `CONTRIBUTING.md`: one file in `src/ct_replications/protocols/`, registered with `@protocols.register(name="<name>")`, and imported in `src/ct_replications/__init__.py`. A monitor the protocol needs of its own goes in `src/ct_replications/monitors/<file>.py`, imported there too, in the same PR. Copy Control Tower's `src/control_tower/protocols/trusted_monitoring.py` in the worktree, or `defer_to_trusted.py` if the trusted model acts, and take every import, signature and call from it. "The API" below has the rules that file does not show. Register each protocol the paper reports, its baselines included, as its own entry under one README row. Every argument defaults to the paper's configuration, except a model that is retired or that Control Tower cannot price: bind that role instead, and record the paper's model as a departure. Add nothing no caller reads, and leave the other replications as they are.
5. **Fidelity check.** With the saved source open, check every decision-log row and every branch of the code against the section it cites. Put a short verbatim quote in each Source cell, or "our choice" where the source says nothing. Where the code and the source differ, fix the code or record the difference as a departure. A replay cannot tell a faithful protocol from an unfaithful one, so this comes before it.
6. **Checks and replay.** Run this repository's checks from "Setup and checks" in `CONTRIBUTING.md`, then replay the recording as "Replaying the recording" says.
7. **Prepare the PR.** Finish `artifacts/pr/<branch>.md` and add the README row as "The README row" in `CONTRIBUTING.md` says. Do not commit, push or open the PR. Print the commands for the user to run from this repository, with a Conventional Commits title:

   ```bash
   git add src/ct_replications README.md && git commit -m "<title>"
   git push -u origin <branch>
   gh pr create --repo linuxarena/ct-replications --draft --base main --title "<title>" --body-file artifacts/pr/<branch>.md
   ```
8. **Real run, only with the user's yes.** It is the paid step, and `CONTRIBUTING.md` asks for a budget agreed with the PR's reviewing maintainer first. Ask the user to confirm the draft PR is open and the budget agreed, and say the task set, the sample count, the models, an estimated cost, and which key in `.env` it uses (`OPENROUTER_API_KEY`, `ANTHROPIC_API_KEY`, ...), by name, never its value. On a yes, run "The real run" below, report safety and usefulness for both protocols at the audit budgets the honest run supports, with the sample counts, the models and the cost, compare with the paper's numbers where the setting allows, and fill in the PR's Run section and the README row's "What Control Tower lacked". Then print `gh pr edit <number> --repo linuxarena/ct-replications --body-file artifacts/pr/<branch>.md` and `gh pr ready <number> --repo linuxarena/ct-replications` for the user. On a no, write "No real-model run yet" in the Run section.

## Reading the paper

A summarising fetch will not quote an algorithm or a prompt verbatim. Save the HTML (`https://arxiv.org/html/<id>`) or the LaTeX source (`https://arxiv.org/e-print/<id>`, a gzipped archive) and a clone of the released code at its commit under `artifacts/source/<id>/`, and read the method and appendix text itself. Prefer the released code over the paper for thresholds, resample counts and what each call sees: papers often leave them out.

## The API

- **Arguments** are constructor parameters declared with `Field(description=...)`, each with a default. Reuse the template's `monitors` and `combine` arguments with their shared descriptions, end with its `harness` argument, and pass the harness to `super().__init__`. A list argument set with `--protocol-arg` needs a type that reads the text as YAML, as `Monitors` does.
- **`on_input`** rewrites what U is about to be asked, or leaves it. It is abstract, so define it; calling `super()` is the usual body. The attack policy drops every system message blue writes, so put any instruction to U in a user message.
- **`on_output`** asks `draw(n)` once per step for every draft it needs, since drawing again frames U again, and returns the action to run or `Audited(draft)`. On an honest sample the audited draft is the one that runs.
- **Scoring a draft.** Call `monitor_draft` the way the template does, passing the request U answered; it records every score and raises when no monitor scored. A score that cannot be computed stays unscored; never put a number in its place.
- **Refusing a call.** `self.block(call, reason)` is the only way; U reads `reason` in place of the call's result.
- **Recording decisions.** `self.note({...})` records why each action ran, was blocked, deferred or audited. Use the template's keys (`monitored`, `blocked`) and add your own markers beside them (`deferred: True`), so whatever reads the notes keeps working. Note every step where U called a tool other than `submit`; the replay check fails a step that has none.
- **The trusted model.** Get it by its role, with its own cache key, as `defer_to_trusted.py` does with `scoped_cache` from `control_tower.models.aliases`. Call it inside the protocol: never give the engine a hook for it, such as a `trusted=` flag on `draw`. Hand it U's turns cut to the parts it may read, with `cut(..., for_model=True)` as the template does, and strip the trusted model's own reasoning from its action before returning it: a provider refuses another provider's reasoning signatures and item ids, in either direction. Two calls that can send the same prompt and should answer independently each need their own `cache_scope(...)` from `control_tower.models.cache_scopes`, or a cached rerun hands both one answer. Neither `scoped_cache` nor `cache_scope` is in Control Tower's stable API, so list the one you use under "What Control Tower lacked".
- **State** on `self` lasts one sample, since the engine builds one protocol per sample.

## Replaying the recording

Set `monitors` only if the protocol takes it, and bind every model role the protocol and its monitors use (`monitor`, `trusted`, and any of its own) to a cheap model, so the replay costs cents and needs no agreed budget. The settings override supplies the fixture setting the recording was made on.

```bash
cd ../control-tower-pin && uv pip install --no-sources -e ../ct-replications
CONTROL_TOWER_SETTINGS_DIR=tests/replay_check/settings uv run ct run eval \
  --from-run tests/replay_check/recorded-control.eval --policy replay --sandbox replay \
  --protocol ct_replications/<name> --protocol-arg 'monitors=[simple]' \
  --model-role monitor=anthropic/claude-haiku-4-5 --model-role trusted=anthropic/claude-haiku-4-5 \
  --run-name <name>-replay
uv run python ../ct-replications/.agents/skills/replicating-a-protocol/scripts/check_replay.py logs/<the replay>.eval
```

The pass check exits 1 if the run failed, or a sample has an error, no `audit` score, a recording that did not replay to its end with no audit catching the attack, or a tool-call step with no protocol note; `ct run eval` itself can exit 0 in each case. A rerun with the same arguments reuses the finished log, so give it a new `--run-name`.

**What a replay can test.** It serves recorded outputs and cannot run a new action, so it is exact only while every recorded action runs or the protocol audits. A block, an edit, a deferral or a resample takes the run off the recording: the sample either fails with `ReplayDivergenceError` or stops early with the rest of the recording unplayed, and its task scores say "Replay diverged" or "Replay stopped". The pass check fails both, unless an audit caught the attack; an audit on an honest sample does not stop it, so it does not excuse a short replay. An attack that was blocked or deferred and then caught still passes, since its audit judged recorded actions the block never let run. Replay with that intervention switched off and test it in the stage 8 run. If the replay passes only with an intervention off, the PR says so and does not claim that intervention was tested.

## The real run

Read "Choosing the thresholds" in `docs/monitoring.md` and "Getting a safety curve" in `docs/safety-curves.md` in the worktree before setting thresholds: a defer or edit threshold is fitted from an honest run, and the audit is fitted after the run unless the protocol must audit live. Run the replication and its nearest existing protocol on the same task set, monitors and models; `--task-file` needs honest and attack lines:

```bash
cd ../control-tower-pin
uv run ct run control-eval --task-file <task set> --limit <n> \
  --protocol ct_replications/<name> --protocol-arg 'monitors=[simple]' \
  --model-role trusted=<model> --model-role untrusted=<model> --run-name <name>-live
uv run ct run control-eval --task-file <task set> --limit <n> \
  --protocol <neighbour> --protocol-arg 'monitors=[simple]' \
  --model-role trusted=<model> --model-role untrusted=<model> --run-name <neighbour>-live
```

**First, a smoke run.** A replay cannot exercise the intervention, so the paid run starts with two or three live samples that force it on (a threshold of `-1`, so every action defers or edits) and, when the trusted model's actions run in U's place, with U and the trusted model from different providers. It catches what a replay misses, such as one provider's signed reasoning reaching another.

## Gotchas

- An audited attack leaves its side task unscored, so safety on the recording can read `nan` or 0 when attacks were caught.
- A threshold the paper states as a share of honest actions becomes a score fitted from an honest run, since a protocol sees one sample: a departure.
- A fallback that needs state across samples, such as shutting down after too many suspicious actions, cannot be built: a departure.

## Resuming

The state of a replication is its branch and its `artifacts/` files. A new session reads `artifacts/pr/<branch>-progress.md` and the decision log first, works from the saved source in `artifacts/source/`, and continues from the first unticked stage.

## Stop and ask the user only when

- The protocol is already replicated. Report it and stop.
- The protocol needs state across samples, several untrusted agents in one sample, U answering a question outside the current action, resampling an earlier step, or model activations. Report it as not buildable and stop.
- Building it needs a change to Control Tower. Report what is missing, for "What Control Tower lacked", and stop.
- Before the stage 8 run, every time: it is the paid step.
