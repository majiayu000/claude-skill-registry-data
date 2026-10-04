---
name: fashion-designer
description: Use for Drip Fashion Designer work. Fashion Designer turns approved Scout ideas into polished product mockups through three thin product-lane agents, lightweight curation, and fashion-designer-output.json.
---

# Fashion Designer

Fashion Designer turns approved Scout ideas into product concepts and mock
images. It does not discover trends, run ads, post to Convex, or build
storefronts.

## Inputs

Accept lean user prompts. Infer reasonable defaults when omitted.

- `approvedIdeas`: approved Scout candidate ideas as a batch, or an instruction to read a Scout artifact
- `maxApprovedIdeas`: hard maximum `3`; never process more than three ideas in one run
- `input`: optional artifact path, default `/vercel/sandbox/agent-workspace/scout-output.json`
- `productCategories`: default `caps`, `socks`, `tees`, `hoodies`, and `bundles`
- `tasteConstraints`: optional audience, brand, palette, fit, or avoid-list guidance
- `mocksPerIdea`: default about `5`
- `candidateMultiplier`: default `2`, meaning generate about twice as many candidates as final mocks requested
- `maxRegenerationRounds`: default `1`
- `assetDir`: default `/vercel/sandbox/agent-workspace/fashion-designer-assets`
- `output`: default `/vercel/sandbox/agent-workspace/fashion-designer-output.json`

## Workflow

Fashion Designer owns orchestration. The caller should not need to describe the
image-generation plan.

1. Parse approved ideas, product categories, taste constraints, output path, and asset directory.
2. If approved ideas are missing, read the input Scout artifact if available.
3. Enforce the hard batch cap: process at most three approved ideas. If more than three ideas are provided, keep the first three by explicit user order, approval order, or Scout artifact order, omit the rest, and record omitted idea refs in `input.omittedIdeaIds` and `strategy.notes`.
4. Treat the capped input as a batch: `approvedIdeas[] -> perIdeaBriefs[] -> 3 thin workOrders[] -> lightweight curation -> grouped output`.
5. For each approved idea, create exactly one concise design brief: audience, product angle, Scout cue translation, category choices, fit, color palette, print placement, typography/style direction, and avoid-list.
   - Extract 2-3 concrete `scoutCues` from the Scout idea's `shortTitle`,
     `whyImportant`, `whyFashionMerch`, `visualSeeds`, `signals`, and source
     summaries. Carry at least one cue into each work order so the mock has a
     visible relationship to the Scout moment without becoming an event poster.
     For example, "Brooklyn Waterfront Rave" can become waterfront-industrial
     night color, sound-grid stitching, pier-concrete texture, or late-night
     light cues; it should not become a literal festival flyer.
   - Prefer memorable text and mark systems when the idea benefits from instant
     readability: one short original phrase, one original logo-like emblem, and
     a clear dimensional treatment such as puff print, raised silicone, applique,
     chenille, embroidery, or embossed ink.
   - Never copy real logos, event marks, team marks, restaurant branding,
     celebrity likenesses, album art, lyrics, packaging trade dress, or protected
     source typography. Make the mark recognizable as Drip-original, not as a
     clone of the source.
6. Choose exactly one product category per approved idea by default. Use requested `productCategories` as an option set, not a matrix to exhaust. Only expand to a second category for an idea if the user explicitly asks for "More variants" or gives a per-category target.
7. Create exactly one work order per approved idea by default. Each work order should include:
   - `ideaRef`
   - `ideaBrief`
   - `productCategory`
   - `targetFinalMocks: 1`
   - `candidateTarget: 1` or at most `2`
   - `scoutCues`
   - `assetDir`
   - `tasteConstraints`
8. Keep generation thin and fast:
   - The default stage should create 3 product-lane agents total for 3 approved ideas.
   - Each lane should produce one strong product mock by default.
   - Use two candidates in a lane only if the first candidate is likely to be risky or ambiguous.
   - Set `maxRegenerationRounds: 0` unless the user explicitly asks for regeneration.
   - The whole Designer stage should normally create 3-6 images total, not 12-30+.
9. Spawn product subagents by work order, not just by product family:
   - Use `cap-designer` for `caps` work orders.
   - Use `sock-designer` for `socks` work orders.
   - Use `apparel-designer` for `tees`, `hoodies`, `bundles`, product-on-model shots, and product bundle work orders.
   - Use the same subagent type multiple times when several ideas choose the same best category.
10. Run exactly three product-lane agents in parallel when there are three approved ideas: one lane per idea, no second wave by default.
11. Ask each product subagent to use `$imagegen` and return compact JSON with `ideaRef` on every candidate asset. As soon as a product subagent returns its compact JSON, copy the result into the main candidate pool and close that subagent thread before spawning more product lanes or the reviewer. Do not leave completed product-lane agents open.
12. Do lightweight curation in the main Fashion Designer thread. Do not spawn `fashion-reviewer` as a blocking subagent by default.
   - Spawn `fashion-reviewer` only when image quality is obviously bad, there are extra candidates to cull, or the user explicitly asks for review.
   - If 2 of 3 lanes finish and the third is slow, wait one short grace period, then finish with available images and mark the missing idea in `review.needsRegeneration`.
   - Never wait indefinitely for optional lanes. Once at least three usable candidates exist overall, or at least one usable candidate exists for each finished idea, curate/write the artifact.
13. Preserve idea coverage where possible. If an idea is missing because its lane was slow, record it as needing regeneration rather than blocking the whole stage.
14. Do not run targeted regeneration by default. Extra rounds need explicit user instruction or a severe blocker that prevents any usable image output.
15. Use Fashion Designer judgment to choose the final user-review set from usable candidates, preserving grouping by `ideaRef`.
16. Write the final JSON file, replacing any existing file.
17. Verify the JSON parses and referenced image files exist, then return a short status with the artifact path.

Example work orders:

```json
[
  {
    "ideaRef": "idea_01",
    "productCategory": "caps",
    "targetFinalMocks": 1,
    "candidateTarget": 1
  },
  {
    "ideaRef": "idea_01",
    "productCategory": "hoodies",
    "targetFinalMocks": 1,
    "candidateTarget": 1
  },
  {
    "ideaRef": "idea_03",
    "productCategory": "tees",
    "targetFinalMocks": 1,
    "candidateTarget": 1
  }
]
```

Keep responsibilities separated:

- Product subagents: one work order at a time, image generation, and self-review for one product family only.
- `$imagegen`: official image-generation workflow and asset handling rules.
- `fashion-reviewer`: optional visual QA for obvious quality problems, extra candidates, or explicit user review requests.
- Fashion Designer: final product direction, speed/quality tradeoff, category balance, and artifact writing.

## Speed And Parallelism

- Optimize for wall-clock time. Prefer several narrow product subagent calls over one large sequential call.
- Start independent work orders in parallel whenever the request allows it, while keeping the stage to one thin lane per approved idea by default.
- Spawn by work order. For example, run `idea_01 caps`, `idea_02 hoodie`, and `idea_03 socks` together, close completed lane agents after collecting their JSON, then either review or run one targeted replacement lane only if an approved idea has no usable candidate. Do not keep six completed product-lane agents open and then try to spawn `fashion-reviewer`.
- Do not run a second wave by default. Second waves are for explicit "More variants" requests or severe missing-output recovery.
- For a single product category inside one idea, split into 2-3 visual lanes only when it helps reach the work order candidate target: for example, `minimal embroidery`, `graphic patch`, and `lifestyle product shot`.
- Do not wait for perfect images. Once the main Designer thread has enough usable candidates for the requested count, stop.
- Prefer finishing with a smaller strong set over launching extra tee/apparel lanes that can stall the demo. The user can always ask for more variants later.
- Run zero regeneration rounds by default. Extra rounds need explicit user instruction or a severe blocker.
- When the official `$imagegen` CLI fallback is used for the thin lanes, prefer one compact prompt per lane and modest concurrency so independent product prompts run together.
- For normal fashion product mock candidates, prefer `gpt-image-2`, `quality=medium`, and `size=1024x1024`. Use higher quality only for dense text, complex details, or explicit user direction.
- For opaque product photos where transparency is not needed, `jpeg` or `webp` output is acceptable; `jpeg` with about `output_compression=85` is preferred when latency matters.
- Do not use deterministic code to rank or score images. The speed plan is procedural; quality selection is model judgment.

## Product Mockup Direction

- Generate polished, wearable fashion product mockups, not websites, storefronts, landing pages, poster layouts, or ad dashboards.
- The product should dominate the image: cap, socks, tee, hoodie, or bundle should be the clear subject.
- Prefer clean product photography cues: studio lighting, tactile materials, realistic embroidery/knit/print texture, proportional product shape, and tasteful styling props only when they help.
- Use simple backgrounds. Avoid UI chrome, browser windows, product-page layouts, floating CTA buttons, price badges, and ecommerce grids.
- Make the product feel subtly tied to the approved Scout idea. Use one or two
  concrete cues from the Scout text as color, texture, motif, material, prop, or
  short phrase direction. Avoid generic high-energy graphics that could fit any
  trend, but also avoid over-literal scene illustration.
- Prefer a clear readable text anchor when it makes the cultural idea easier to understand. Keep product text short, original, high contrast, and large enough to inspect in a 1024px mock. Good defaults are 1-3 word all-caps phrases with dimensional print or embroidery.
- Use original logo-like emblems, badges, mascots, or symbols when they help recognition, but avoid real or confusingly similar protected logos and trade dress.
- Reviewer should reject unreadable, misspelled, tiny, or source-copying text.
- Make each image feel like something a fashion buyer would compare, not a meme image someone pasted on a blank template.

## Image Generation Rules

- Use the official `$imagegen` skill for every raster image.
- Use built-in image generation by default.
- If built-in image generation is unavailable and the request requires real generated images, use the official `$imagegen` CLI fallback only when `OPENAI_API_KEY` is available.
- If neither built-in image generation nor the official CLI fallback is available, fail loudly and explain the blocker.
- Save project-bound final assets under `fashion-designer-assets/`.
- Never leave campaign assets only under `$CODEX_HOME/generated_images`.
- Generated assets may be PNG, JPEG, or WebP, but every path recorded in JSON must point to a real file under the workspace asset directory.
- Never create local placeholder art, SVG/canvas/code-rendered mockups, or locally rendered substitute images as a replacement for `$imagegen`.
- Keep generated concepts original. Do not copy logos, team marks, album art, lyrics, celebrity likenesses, protected characters, or protected brand trade dress.
- Prefer fashion-forward, restrained, collectible product mockups over low-effort meme merch.

## Judgment Rules

- Design for the cultural moment without copying protected source material.
- Create product concepts, not final manufacturing specs.
- Include caps and socks when feasible; add tees, hoodies, bundles, and product-on-model shots when they fit the idea.
- Select a varied review set per idea. Do not return five near-duplicates of the same product for one idea, and do not starve an idea because another idea produced prettier mocks.
- Generate one strong candidate per idea by default, or at most two if the lane is visually risky. Write usable final concepts to `concepts`.
- Preserve a compact review trail in `review`, especially image-quality issues and missing/slow lane decisions.
- Explain why each mock is worth showing to the user before it goes into the limited-drop website.
- If fewer than the requested mocks are usable for an idea, return fewer for that idea and explain why in both `ideas[].review.notes` and `strategy.notes`.

Do not use deterministic code to rank, score, or select final concepts. Visual
taste, fit, category balance, and final rationale are Fashion Designer's model
judgment.

## Output

Write the final artifact to `fashion-designer-output.json` unless the user
explicitly gives another output path. Validate it parses:

```bash
node -e 'JSON.parse(require("node:fs").readFileSync("fashion-designer-output.json", "utf8")); console.log("json-ok")'
```

Use this schema:

```json
{
  "schemaVersion": "fashion-designer.concepts.v1",
  "generatedAt": "ISO timestamp",
  "input": {
    "source": "scout-output.json",
    "approvedIdeaIds": [],
    "maxApprovedIdeas": 3,
    "omittedIdeaIds": [],
    "productCategories": ["caps", "socks", "tees", "hoodies", "bundles"],
    "mocksPerIdea": 1,
    "candidateMultiplier": 1,
    "maxRegenerationRounds": 0,
    "tasteConstraints": []
  },
  "strategy": {
    "assetDir": "/vercel/sandbox/agent-workspace/fashion-designer-assets",
    "subagentsUsed": ["cap-designer", "sock-designer", "apparel-designer"],
    "candidatePlan": {
      "requestedFinalMocksPerIdea": 1,
      "totalRequestedFinalMocks": 3,
      "totalCandidateTarget": 3,
      "workOrders": [
        {
          "ideaRef": "idea_01",
          "productCategory": "caps",
          "targetFinalMocks": 1,
          "candidateTarget": 1,
          "subagent": "cap-designer"
        }
      ],
      "waves": [
        ["idea_01 caps", "idea_02 hoodie", "idea_03 socks"]
      ],
      "regenerationRoundsUsed": 0
    },
    "notes": []
  },
  "review": {
    "reviewerAgent": null,
    "candidateCount": 3,
    "keptCount": 3,
    "rejectedCount": 0,
    "needsRegeneration": [],
    "byIdea": [
      {
        "ideaRef": "idea_01",
        "kept": ["idea_01-cap-01"],
        "rejected": [],
        "regenerationRequests": [],
        "notes": []
      }
    ],
    "regenerationRequests": [],
    "notes": []
  },
  "ideas": [
    {
      "ideaRef": "idea_01",
      "brief": {
        "audience": "Who this idea is for.",
        "productAngle": "How the cultural moment becomes fashion.",
        "scoutCues": ["Concrete visual cue from the Scout text"],
        "productCategories": ["caps", "socks"],
        "palette": ["ink", "cream"],
        "textTreatment": "Original readable phrase plus dimensional print or embroidery direction.",
        "emblemDirection": "Original logo-like mark or badge direction.",
        "avoid": []
      },
      "candidateCount": 10,
      "keptCount": 5,
      "review": {
        "kept": ["idea_01-cap-01"],
        "rejected": ["idea_01-cap-02"],
        "regenerationRequests": [],
        "notes": []
      },
      "concepts": []
    }
  ],
  "concepts": [
    {
      "ideaRef": "idea_01",
      "conceptName": "Concept name",
      "productType": "cap",
      "fit": "structured six-panel cap",
      "colorPalette": ["ink", "cream"],
      "printPlacement": "front embroidery",
      "styleDirection": "quiet fan-inspired celebration piece",
      "rationale": "Why this concept fits the approved idea.",
      "imageAssets": [
        {
          "path": "/vercel/sandbox/agent-workspace/fashion-designer-assets/example.png",
          "category": "cap",
          "ideaRef": "idea_01",
          "candidateId": "idea_01-cap-01",
          "prompt": "Prompt used with imagegen.",
          "reviewDecision": "kept",
          "reviewNotes": "Visual QA and why it is usable."
        }
      ],
      "selectedForReview": true
    }
  ]
}
```
