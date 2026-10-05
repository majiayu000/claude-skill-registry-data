---
name: dreamifly-batch
description: 批量调用 Dreamifly 生成并下载图片或视频。Use when the user asks to batch-generate images, edit images with references, create text-to-video or image-to-video, queue prompts, validate or estimate generation cost, retry failed media jobs, or summarize Dreamifly outputs.
compatibility: Requires Python 3 and network access to dreamifly.com. High-cost models require explicit user confirmation before real API calls.
metadata:
  category: media-generation
---

# Dreamifly 批量生图 / 生视频

把用户的提示词队列转成 Dreamifly 图片/视频生成任务，下载媒体到 `images/`，并用 `results.jsonl` / `failed.jsonl` 给 Agent 稳定汇报和重试。

## Trigger Boundary

Use this skill for:
- 批量生图、图生图编辑、统一排队出图
- 文生视频、图生视频、多参考图生视频
- 校验 prompt 队列、估算积分、重试失败项、汇总生成结果

Do not use this skill for generic image prompt writing if the user does not want Dreamifly generation, local files, or queue execution.

## Execution Protocol

Always run this sequence for real jobs:

1. Choose the model and write one task per line to `prompts.txt`, or use `--prompts jobs.jsonl`.
2. Run `python3 dreamify.py --validate`.
3. Run `python3 dreamify.py --estimate`.
4. Run `python3 dreamify.py --dry-run`.
5. Run `python3 dreamify.py --check`.
6. If any item is 5+ credits, video, or `nano-banana-2`, stop and ask for explicit user approval.
7. Run `./run.sh` or `python3 dreamify.py -n N`.
8. Report with `python3 dreamify.py --summary`, then inspect `results.jsonl` and `run.log` if needed.

Cheap image models (`Wai-*`, `Z-Image-Turbo`, `Qwen-Image-Edit`) can run without extra approval after validation passes.

## Queue Formats

Inline text:

```
a neon cat | model=Z-Image-Turbo | 16:9 | x2 | seed=123 | neg=blurry
edit this, add snow | model=Qwen-Image-Edit | img=ref.png
city timelapse | model=happyhorse-1.0 | secs=5 | res=720P
```

JSONL:

```json
{"prompt":"a neon cat in rain","model":"Z-Image-Turbo","aspectRatio":"16:9","batch_size":1}
{"prompt":"edit this, add snow","model":"Qwen-Image-Edit","images":["ref.png"]}
```

## Required Safety Rules

- Never print, commit, copy, or summarize `config/cookie.txt`; only say whether a cookie was loaded and its length if needed.
- Never run video, `nano-banana-2`, or any 5+ credit item without explicit approval.
- Do not blindly retry 401/402; ask the user to update the cookie or credits first.
- Video jobs are expensive and must not be auto-retried.

## Progressive References

Read these only when needed:

- Model routing and parameters: `references/model-selection.md`
- Output files and reporting contract: `references/output-contract.md`
- Failure lessons and hard boundaries: `references/gotchas.md`
- Skill routing eval cases: `references/evals.md`
- JSONL examples: `examples/prompts.jsonl`
