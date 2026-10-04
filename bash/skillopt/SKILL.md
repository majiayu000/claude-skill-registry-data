---
name: skillopt
description: >
  Use when the user asks about Microsoft SkillOpt, optimizing or training agent skill documents with reflective loops, evaluating skill changes with validation gates, or running SkillOpt experiments. This is a wrapper around the local reviewed source checkout and must not run installs, training, WebUI, or model/API calls unless explicitly requested.
tags:
  - research
  - skills
  - optimization
  - agentic
version: 1
---

# SkillOpt

SkillOpt is a Microsoft research framework for optimizing agent skill documents through reflective training loops, validation gates, and benchmark-specific evaluation.

Local source checkout:
- `~/.hermes/external-repos/SkillOpt`
- Upstream: `https://github.com/microsoft/SkillOpt`
- Reviewed checkout: `75b5c7f31c040b4e8845877f1f2dd664bf366b11`

## Safety Contract

Treat this repository as executable research code, not a passive markdown skill pack.

Do not run these without explicit user approval:
- `pip install -e .` or optional extras such as `.[alfworld]`, `.[claude]`, `.[qwen]`, `.[webui]`
- `python scripts/train.py`
- `python scripts/eval_only.py`
- `python -m skillopt_webui.app`
- `python -m skillopt_webui.app --share`
- `alfworld-download`
- commands that source `.env`, write secrets, or call model APIs

Risk notes from intake:
- Requires or consumes Azure OpenAI, OpenAI, Anthropic, or Qwen endpoint credentials for real runs.
- Training and evaluation scripts call external model backends and write run artifacts under output directories.
- WebUI uses Gradio and can create a public share link when `--share` is used.
- Some benchmark paths execute generated code or subprocesses inside benchmark work directories.

## When To Use

Use this wrapper for:
- Explaining SkillOpt concepts and workflow.
- Inspecting local docs, configs, prompts, and source before a proposed experiment.
- Designing a safe SkillOpt experiment plan.
- Reviewing generated skill-document changes before promotion.
- Mapping SkillOpt ideas onto Hermes skill governance.

## Safe Workflow

1. Read local docs first:
   - `README.md`
   - `docs/guide/skill-document.md`
   - `docs/guide/training-loop.md`
   - `docs/guide/configuration.md`
   - `docs/reference/cli.md`
2. If a run is requested, ask for explicit approval of:
   - backend/provider,
   - credential source,
   - benchmark/data split,
   - output directory,
   - whether generated code/subprocess execution is allowed.
3. Prefer a dry-run plan and config review before any package install or model/API call.
4. Keep generated artifacts outside source-controlled runtime skill directories unless the user asks to promote them.
5. Before promoting any optimized skill, require validation evidence from held-out data or a predeclared benchmark gate.

## Common Commands

Only run after explicit approval and environment review:

```bash
cd ~/.hermes/external-repos/SkillOpt
python scripts/train.py --config configs/searchqa/default.yaml --split_dir /path/to/split
python scripts/eval_only.py --config configs/searchqa/default.yaml --skill outputs/run/best_skill.md --split valid_unseen --split_dir /path/to/split
```

For read-only inspection, use ordinary file reads and `rg`; no install is needed.
