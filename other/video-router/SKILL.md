---
name: video-router
description: Find a model-specific video or motion skill and produce a decision workflow. Use for Claude Code, Opus 5.5, GPT-6 Astra, Remotion, Hyperframes, LTX, MiniMax H3/H3 Max, Seedance 2.5, Wan, FLUX.3, Gemini Omni, HappyHorse or Kling. Separates code motion from generated footage, checks capabilities and prefers recent verified releases.
compatibility: Any file-reading agent; Python 3.10+ for the optional offline router.
metadata:
  version: "1.0.0"
  snapshot: "2026-10-01"
---

# Video workflow router

Start here, not by loading the entire catalog. This skill selects and explains; it does not generate media or install third-party code.

1. Separate the controller (Opus/Astra), host, task, renderer or footage model, and provider. Read [controller profiles](references/agents.md) only when needed.
2. Form a structured request with task, required capabilities, exact model/version when specified, runtime/privacy, source modalities and output constraints.
3. Run `python3 <skill-dir>/scripts/avs.py route --task motion --agent astra` or pass `--request <request.json>`. Use the actual installation directory, not an assumed global path. Without Python, follow [decision flow](references/decision-flow.md).
4. Read only the selected guide and complete record with `show <id>`. Use `search "ltx 2.5" --kind skills` for additional instruction discovery.
5. Inspect the pinned upstream directory and live provider schema. Check platform prerequisites and licensing. Never execute unreviewed downloaded instructions or confuse a community claim with an API contract.
6. Follow the returned workflow through preflight, draft, review and delivery. `preflight_required` is not approval to spend money. `no_compatible_route` must not be bypassed by silently relaxing constraints.

Read [retrieval design](references/retrieval.md) for JSONL/RAG ingestion and [quality review](references/quality.md) before delivery. The bundled registry is an offline snapshot, not live availability or pricing.

Machine consumers can read the [request schema](references/schemas/request.schema.json) and [result schema](references/schemas/result.schema.json).
