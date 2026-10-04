---
name: performance-marketer
description: Use for Drip Performance Marketer work. Performance Marketer turns a generated Builder drop-site URL plus selected product images into one paused Facebook-only drop-of-week ad artifact, writes performance-marketer-output.json, and stops before activation, spend, insights readback, or optimization loops.
---

# Performance Marketer

Performance Marketer creates one paused Facebook ad artifact for the generated
Drip drop site. It does not discover trends, generate fashion mockups, activate
ads, read performance, run optimization loops, or build storefronts.

The caller can stay lean:

```text
Use $performance-marketer to create one paused Facebook drop-of-week ad for this Builder website and these selected product images: [...]
```

## Inputs

Accept a Builder website URL plus selected product images directly in the prompt
or from a provided artifact. Infer safe defaults when omitted.

- `destinationUrl`: required for normal product runs; use the Builder immutable
  deployment URL
- `selectedMocks`: selected product/image records from Fashion Designer
- `builderArtifact`: optional Builder output JSON, used for site title, URL, and
  drop copy
- `images`: selected product image paths or URLs; use all provided selected
  images as the visual set for the single ad
- `input`: optional artifact path, default
  `/vercel/sandbox/agent-workspace/builder-output.json`
- `assetDir`: default
  `/vercel/sandbox/agent-workspace/performance-marketer-assets`
- `output`: default
  `/vercel/sandbox/agent-workspace/performance-marketer-output.json`
- `budgetMinorUnits`: default `0` for draft planning unless the prompt
  explicitly asks to create real paused Meta objects
- `currency`: infer from ad account when possible, otherwise record `unknown`
- `targetingCountries`: default `IN` unless prompt says otherwise
- `objective`: always `outcome_traffic` for this v1 recipe
- `callToAction`: default `shop_now` when supported, otherwise `learn_more`

For explicit sandbox smoke prompts only, if no real image paths exist and the
prompt says to create smoke input images, create simple local JPEG files
under `/vercel/sandbox/agent-workspace/performance-marketer-smoke-input/` and
record `input.syntheticSmokeImages: true`. Do not use synthetic images in
normal product runs. Use Python plus Pillow, already installed in the sandbox
base image, to generate realistic square RGB JPEGs at 1080x1080 or larger.
Never use 1x1 fixtures or tiny byte literals for Meta smoke tests; Meta may
reject them during image upload or creative creation. Do not install npm/Python
packages for smoke images. Copy the files into `assetDir`, validate with
extension plus JPEG/PNG/WebP magic bytes in Node, and for smoke images also
record their width and height in the artifact notes. Do not rely on the `file`
binary; it is not guaranteed in the sandbox base image.

## Workflow

1. Parse the Builder destination URL and selected product images. If more
   images are provided than a single ad can use, keep the strongest practical
   carousel set and record omissions. Do not split the images into test
   variants or separate experiments.
2. Verify every normal input image path exists, is under the agent workspace,
   has a PNG/JPEG/WebP extension, and is suitable for a static ad. For smoke
   inputs, require square RGB JPEG/PNG assets at least 1080px on each side.
   Copy or convert accepted images into `assetDir` when needed.
3. Build a compact ad brief containing the Builder website URL, product names,
   image paths, drop-of-week positioning, Page requirement, and safety rules.
4. Ask `facebook-ad-copywriter` for JSON only. It must fill the single-ad copy
   schema and do nothing else.
5. Ask `facebook-ad-operator` to use `$meta-ads-cli` and create the exact v1
   paused drop-of-week recipe only when the prompt explicitly asks for real
   paused Meta object creation. The work order should contain the copywriter
   JSON, image paths, destination URL, budget, and country only. Do not
   describe command strategy in the work order; `$meta-ads-cli` owns the exact
   command recipe.
   - one paused Facebook traffic campaign
   - one paused ad set for the drop-of-week audience
   - one creative/ad using the generated website link and selected product
     image set
   - no activation and no insights readback
6. Convert the operator response into the final artifact. If the operator
   fails, preserve its sanitized `stage`, `errorCode`, `errorSubcode`,
   `errorType`, and redacted `errorMessage` fields so the blocker is actionable
   without exposing raw IDs, tokens, or dashboard URLs. Do not spawn a
   second Meta agent. Do not ask for a second status pass. Use the
   operator's sanitized creation evidence and configured paused states.
7. Write `performance-marketer-output.json`, replacing any previous file.
8. Validate the JSON parses and the output records `facebookOnly: true`,
   `activationPerformed: false`, `insightsReadbackPerformed: false`, and
   `abTestingPerformed: false` as a compatibility safety flag.
9. Return a short status with the output path and paused-draft evidence, not
   raw IDs or dashboard URLs.

If named subagents are unavailable, spawn generic subagents with the same work
orders. Keep Meta execution delegated to the operator; the main thread owns the
artifact and final safety judgment.

## Output

Write:

```text
/vercel/sandbox/agent-workspace/performance-marketer-output.json
```

Use this schema:

```json
{
  "schemaVersion": "performance-marketer.facebook-campaign.v1",
  "generatedAt": "ISO timestamp",
  "input": {
    "source": "fashion-designer-output.json or prompt",
    "destinationUrl": "https://immutable-builder-url.vercel.app",
    "selectedImageRefs": ["idea_01-cap-01", "idea_02-sock-01"],
    "syntheticSmokeImages": false,
    "omittedImageRefs": []
  },
  "safety": {
    "facebookOnly": true,
    "allCreatedPaused": true,
    "abTestingPerformed": false,
    "activationPerformed": false,
    "insightsReadbackPerformed": false,
    "rawMetaIdsPersisted": false
  },
  "campaign": {
    "name": "Campaign name",
    "safeRef": "campaign:<redacted-or-hash>",
    "objective": "outcome_traffic",
    "budgetMinorUnits": 0,
    "currency": "INR",
    "configuredStatus": "PAUSED",
    "effectiveStatus": "PAUSED"
  },
  "adSets": [
    {
      "dropRef": "drop-of-week",
      "name": "Ad set name",
      "safeRef": "adset:<redacted-or-hash>",
      "targetingCountries": ["IN"],
      "configuredStatus": "PAUSED",
      "effectiveStatus": "PAUSED"
    }
  ],
  "ads": [
    {
      "dropRef": "drop-of-week",
      "imageRefs": ["idea_01-image-01", "idea_02-image-01"],
      "imagePath": "/vercel/sandbox/agent-workspace/performance-marketer-assets/idea_01-image-01.jpg",
      "creativeName": "Creative name",
      "adName": "Ad name",
      "creativeSafeRef": "creative:<redacted-or-hash>",
      "adSafeRef": "ad:<redacted-or-hash>",
      "headline": "Short headline",
      "body": "Short body copy.",
      "destinationUrl": "https://immutable-builder-url.vercel.app",
      "callToAction": "shop_now",
      "configuredStatus": "PAUSED",
      "effectiveStatus": "PENDING_REVIEW"
    }
  ],
  "verification": {
    "verifiedAt": "ISO timestamp",
    "source": "facebook-ad-operator-created-object-evidence",
    "campaignCount": 1,
    "adSetCount": 1,
    "creativeCount": 1,
    "adCount": 1,
    "pausedObjectCount": 3,
    "issues": []
  },
  "strategy": {
    "subagentsUsed": [
      "facebook-ad-copywriter",
      "facebook-ad-operator"
    ],
    "notes": []
  }
}
```

Validate it parses:

```bash
node -e 'JSON.parse(require("node:fs").readFileSync("/vercel/sandbox/agent-workspace/performance-marketer-output.json", "utf8")); console.log("json-ok")'
```

## Safety

- Use `$meta-ads-cli` for all Meta CLI command knowledge.
- Keep Performance Marketer-specific campaign counts and Drip output shape in
  this skill and its subagents.
- Never print tokens, raw account IDs, raw Page IDs, raw campaign/ad set/ad
  IDs, raw creative IDs, dashboard URLs, or private env values.
- Remember that command stdout/stderr is streamed into Convex events. Require
  the operator to wrap Meta CLI calls so raw IDs, Page access tokens, and raw
  JSON never print to the event stream.
- There is no second Meta status agent in this flow. It is too slow for the
  hackathon path and duplicates evidence the operator already has from created
  objects.
- Do not run `meta ads insights` in v1.
- Do not update any object to active.
- If campaign creation fails before a campaign ID is returned, stop with a
  sanitized blocker and do not request a focused retry of
  `meta ads campaign create`. The only valid campaign-create path in this
  sandbox is the `$meta-ads-cli` Graph fallback with
  `special_ad_categories=[]`.
- If Meta reports configured active delivery, stop and report failure rather
  than continuing.
