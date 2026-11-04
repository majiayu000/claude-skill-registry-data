---
name: ai-toolkit-local
description: >-
  Local FLUX.2-dev generation via Ostris ai-toolkit on Mac (MPS). Use for
  Blacksage / venture stills when HF_TOKEN is set. External repo — not vendored.
---

# ai-toolkit Local (FLUX.2-dev)

Thin adapter. Toolkit lives outside ClaudeSkills.

## Preferred access

- Repo: `$AI_TOOLKIT_ROOT` (default `/Users/cbsuperpatch/Desktop/ai-toolkit`)
- Model: [black-forest-labs/FLUX.2-dev](https://huggingface.co/black-forest-labs/FLUX.2-dev)
- CLI: `python run.py <generate.yaml>` or `./run_mac.zsh`
- Org render: `bash scripts/render-blacksage-stills.sh --backend local`

## Env / secrets

| Var | Required |
|-----|----------|
| `HF_TOKEN` | Yes (HF gated accept) |
| `AI_TOOLKIT_ROOT` | Optional path override |

Resolve via Obsidian → `.env.local`. See `scripts/bootstrap-production-secrets.md`.

## Primary ops

1. Accept FLUX.2-dev license on Hugging Face; export `HF_TOKEN`.
2. Write generate YAML from design-brief prompts (see venture `11-brand/refs/ai-toolkit.generate.example.yaml`).
3. Multi-ref: `ctrl_img` / `ctrl_img_1`–`ctrl_img_3` = identity / pose / lighting / environment.
4. Copy outputs into leased `*/assets/` only after photoreal checklist.
5. Sidecar: `generation_used: local/flux-2-dev`, `model_id: black-forest-labs/FLUX.2-dev`, `device: mps`.

## License

FLUX.2-dev is **non-commercial** by default. Marketing/email/site assets need either:

- `license_basis: bfl-self-hosted-commercial`, or
- Re-render via fal (`skills/integrations/fal-media/`) with `generation_used: fal/flux-2-*`

Otherwise `photoreal_qa: draft` only.

## Fallback

- Speed drafts: FLUX.2-klein 4B/9B in same toolkit
- Commercial API: fal FLUX.2 max/pro
- Missing toolkit: do not claim production complete

## Common failures

- Missing `HF_TOKEN` / not accepted model card → download fails
- Treating Cursor GenerateImage as final
- Auto-promoting lab samples without photoreal QA
