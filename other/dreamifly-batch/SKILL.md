---
name: dreamifly-batch
description: Batch-generate Dreamifly images/videos from prompt queues. Use when the user asks to batch-generate images, edit images with references, create text-to-video or image-to-video, validate or estimate Dreamifly job cost, retry failed media jobs, or summarize Dreamifly outputs.
compatibility: Requires Python 3 and network access to dreamifly.com. High-cost models require explicit user confirmation.
metadata:
  category: media-generation
---

# Dreamifly Batch

## Quick Start

1. Write real prompts to `prompts.txt` or provide `--prompts jobs.jsonl`.
2. Run `python3 dreamify.py --validate`.
3. Run `python3 dreamify.py --estimate`.
4. Run `python3 dreamify.py --dry-run`.
5. Run `python3 dreamify.py --check`.
6. If any item costs 5+ credits, stop and ask for explicit confirmation before running.
7. Run `./run.sh` or `python3 dreamify.py -n N`.
8. Report with `python3 dreamify.py --summary`; inspect `results.jsonl` and `run.log` only if needed.

## Useful Commands

- `python3 dreamify.py --validate`
- `python3 dreamify.py --estimate`
- `python3 dreamify.py --summary`
- `python3 dreamify.py --retry-failed`
- `python3 dreamify.py --prompts jobs.jsonl --results-file results.jsonl`

## References

- Model choice and cost rules: `references/model-selection.md`
- Output and reporting contract: `references/output-contract.md`
- Failure lessons and hard boundaries: `references/gotchas.md`
- Trigger eval cases: `references/evals.md`
- JSONL job examples: `examples/prompts.jsonl`
