---
name: runpod-launch
description: Use when adding or changing a "Run on Runpod" launch card for an article, writing or editing runpod/profiles/<id>.yaml, creating a Runpod template for an article, or deciding whether a card carries the referral code.
---

# Runpod Launch

The design and the reasons live in `ops/adr/2026-09-30-runpod-poc.md` and `runpod/README.md`. Read them first.

## Rules

- One Runpod template per article, created by the owner under the Matatabi AI account. Settings: the template table in `runpod/README.md`.
- The card is `{% runpod %}` in the article. It reads the profile whose `article` is the page, so the profile must have `template:`.
- **Check the model licenses before adding a card.** If any model in the profile forbids commercial use (research or evaluation only, non-commercial, and so on), write `referral: false` in the profile with a comment naming the license. The card then has no referral code and no disclosure line. Read the license text itself (the model's LICENSE file), not only the Hugging Face tag. When unsure, ask the owner.
- The template's creator earnings (1% of spend in Runpod credits) cannot be turned off per template as far as the public docs say. Tell the owner when a non-commercial model gets a template.
- Do not run Pods or local GPU tests without asking the owner first.

## Steps

1. Profile: follow "新しいプロファイルを足すとき" in `runpod/README.md`.
2. License check: list every model in the profile and read its license. Set `referral: false` if one is non-commercial.
3. The owner creates the template; put its ID in `template:` and the starred GPUs in `gpu.recommended`.
4. Place `{% runpod %}` in the JA article (EN/ZH only when localization is asked for).
5. Check the card on localhost (see [preview-site](../preview-site/SKILL.md)).

## Checks

- `npm run check:runpod`
- `npm run build`
