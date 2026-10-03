---
name: crun-account-credits
description: Check a Crun API account credit balance and estimate whether a validated media task is affordable. Use before every new Crun media task, including user-specified models, and when a request reports insufficient credits.
---

# Crun Account Credits

Use `../../runtime/crun_cli.py`. Let it resolve `CRUN_API_KEY` (the `~/.crun/.env` file first, then the environment variable). If configuration is missing, the error carries `configuration_options`; recommend the first option — the ready-to-run `python "<absolute path>/crun_cli.py" config set-api-key <your_api_key>` command, which persists the key into `~/.crun/.env` — without exposing or requesting the key in chat.

## Check the balance

```text
python <runtime>/crun_cli.py credits
```

Report the numeric `balance` exactly as returned. Do not infer currency or generation count from the balance alone.

## Check affordability

Estimate the final model and exact validated input before every new task:

```text
python <runtime>/crun_cli.py task estimate --model <model> --input-file <input.json>
```

Use `estimated_credits`, `balance`, and `affordable` from the response. Do not submit when `affordable` is false or missing. Re-estimate after changing the model or any price-sensitive input, and before each batch unless the user explicitly accepts partial completion.

When the balance is insufficient, report the current model, estimate, and balance. Obtain explicit permission before proposing a different model, then validate and estimate the replacement. Follow `../crun-task-runner/SKILL.md` for every creation and authorization gate.
