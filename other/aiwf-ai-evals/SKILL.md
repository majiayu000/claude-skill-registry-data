---
name: aiwf-ai-evals
description: AIWF evaluation skill for local AI models and routes. Use for lm-eval readiness, custom prompt suites, image and video smoke receipts, before and after model comparisons, baseline selection, acceptance thresholds, regression gates, training promotion checks, and release-facing validation artifacts.
---

# AIWF AI evals

Use this skill when the task needs proof that a model, route, trainer output, or serving endpoint is better, working, or safe enough to promote.

## Safety gate

Do not run expensive benchmarks, long generations, or GPU-heavy evals unless Shawn explicitly asks. Planning, readiness checks, tiny prompt probes, artifact inspection, and receipt validation are allowed.

## Workflow

1. Read project guidance, existing QA matrices, smoke receipts, eval folders, and model or route metadata.
2. Classify the eval target:
   - LLM model file, adapter, or server.
   - Image or video generation route.
   - UI/API route behavior.
   - Training before/after comparison.
   - Serving latency or stability check.
3. Read `references/eval-gates.md` before choosing tasks or thresholds.
4. Create an eval plan when the work is more than a one-off probe:

```powershell
python <this-skill>\scripts\create_eval_plan.py --target <model-or-route> --modality llm --out <plan.json>
```

5. Define baseline and candidate. Never compare a post-training result without naming the baseline model, adapter state, prompt suite, and runtime settings.
6. Choose the smallest useful eval:
   - LLM: lm-evaluation-harness readiness, custom prompt suite, local regression prompts, or API-compatible server probe.
   - Image: fixed prompts, seed policy, dimensions, scheduler, LoRA state, artifact metadata, and visual receipt checks.
   - Video: prompt, duration, FPS, resolution, seed, frame count, decode path, and output artifact checks.
   - UI/API: payload shape, response status, progress states, cancellation, and saved output paths.
7. Set acceptance gates before running:
   - pass/fail criteria
   - metric or artifact location
   - tolerated regressions
   - manual review fields when visual quality matters
8. Store receipts with enough context to reproduce: model path, commit or config, prompt file, seed, command, endpoint, hardware, timestamp, and result.

## Output

Report:

- target, baseline, and candidate
- eval suite and why it fits
- thresholds and promotion rule
- commands run
- receipt paths
- pass/fail result
- caveats that block promotion

Use `aiwf-local-ai-training` for trainer-output promotion and `aiwf-inference-serving` for endpoint latency or stability gates.
