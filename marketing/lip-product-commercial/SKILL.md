---
name: lip-product-commercial
description: Use for a lip-color commercial with model, packaging, shade, finish, application, texture, and natural product-interaction proof held consistent across planned shots. Unlike generate-video (relationship 0.63), choose this when lip-specific evidence and anchor gates own the deliverable; choose generate-video for a general product shot. Unlike product-detail-page (0.67), choose this for moving commercial media rather than a static commerce page. Do not use for skincare or eye-makeup campaigns.
---
# Lip Product Commercial

## Catalog

- Display name: Lip Product Commercial
- Categories: Commercial Production, Video
- Status: Ready
- Route label: Lip-color proof commercial production
- Tone: pink
- Short description: Plan and produce an anchor-locked lip-product commercial with application, texture, shade, and packshot evidence.
## What this skill does

- Locks a model/face reference, product reference, and approved storyboard before moving media.
- Plans beauty, texture, application, model-product, and closing-packshot proof without obscuring lips or labels.
- Preserves product silhouette, shade, cap, label placement, and visible finish across accepted shots.

## How to use

Provide product/model references or a brief, target ratio/duration, copy rules, and music if required; no copyright authorization is required. A Canvas-capable Agent may retain approved anchors and storyboard there; otherwise it uses chat or local delivery.

#### Example

```text
用这支唇釉做 20 秒 16:9 广告：保留瓶身、豆沙色和玻璃唇光泽；需要模特上唇、质地特写、自然拿取和收尾 packshot，不要背景音乐。
```

## Workflow

1. Lock product and model evidence; use the current verified image route to create missing approved anchors only when needed.
2. Create a storyboard with one proof claim per shot. Keep text in safe negative space and never over lips, face, applicator, or label.
3. Then route each atomic shot through `$generate-video`; use the product/model anchors as named references and preserve only source-supported brand facts.
4. Persist an `operationKey` per asset, poll receipts, and assemble accepted clips through `$combine-videos` only on request. Do not fabricate music or readable package copy.

## User-facing output

- Media type: Approved storyboard and requested MP4 shots or assembly
- Default quantity: One commercial cut
- Content per video: Lip beauty, texture/application proof, and packshot
- Default layout: User-requested ratio
- Model policy: Verified image route for anchors and catalog-selected video route for shots
- Downstream use: Lipstick, tint, gloss, oil, and glaze campaigns

## Route

- Upstream assets: Product and optional model references
- Downstream handoff: `$combine-videos` for accepted shot assembly
