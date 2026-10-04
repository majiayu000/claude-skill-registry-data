---
name: builder
description: Use for Drip Builder work. Builder turns the user's selected Fashion Designer product images into a reviewed, deployed, one-page limited-drop site and writes builder-output.json.
---

# Builder

Builder creates the customer-facing website for the selected Fashion Designer
products. It does not discover trends, design a product line, run ads, create
checkout logic, or update Drip app code.

The caller can stay lean:

```text
Use $builder to create a live drop page for these selected drop products: [...]
```

Builder owns the plan, subagent orchestration, final page judgment, deployment,
and output JSON.

## Inputs

Accept selected Fashion Designer products directly in the prompt or from an
artifact path.
Infer reasonable defaults when omitted.

- `selectedMocks`: selected Fashion Designer products/images, idea references,
  product names, image paths, audience, positioning, and drop copy
- `input`: optional artifact path; use any provided path before defaults
- `siteDir`: default `/vercel/sandbox/agent-workspace/builder-site`
- `output`: default `/vercel/sandbox/agent-workspace/builder-output.json`
- `countdownHours`: default `24`
- `ctaLabel`: default `Buy now`
- `ctaBehavior`: always `dummy`
- `maxReviewRounds`: default `1`
- `deploymentProject`: default env `DRIP_DROP_SITES_VERCEL_PROJECT`, expected
  value `drip-websites`

If the price is missing, choose a plausible display price for the product
category and record that it was inferred in `strategy.notes`. The price is only
display copy; do not create payment or checkout behavior.

## Workflow

1. Parse the selected Designer products, source artifact paths, product
   categories, approved product image references, price, audience, positioning,
   and drop copy.
2. Create a concise site brief with title, slug, visual thesis, content plan,
   interaction thesis, countdown hours, price, CTA copy, and avoid-list.
   The default layout must be a single no-scroll viewport: top urgency timer,
   large centered product-image carousel, price, and dummy Buy now action.
3. Ask `drop-site-builder` to create the static site. Its work order must
   include `siteDir`, the full drop brief, any approved product image paths,
   and the required page contract.
4. Require `drop-site-builder` to use `$frontend-skill` for art direction and
   `$imagegen` for raster product imagery. It should save all site assets under
   `builder-site/.vercel/output/static/assets`.
5. Check that the static output exists:
   - `builder-site/.vercel/output/config.json`
   - `builder-site/.vercel/output/static/index.html`
   - `builder-site/.vercel/output/static/assets/styles.css`
   - `builder-site/.vercel/output/static/assets/site.js`
   - at least one real raster product image in `assets/`
6. Ask the verifier subagent, `drop-site-reviewer`, to inspect the local static
   preview with `agent-browser` at standard desktop ratios: 16:10 (`1440x900`)
   and 16:9 (`1920x1080`). Keep this delegated to a subagent so the main
   Builder thread does not hand-wave visual QA. If the runtime cannot expose
   the named `drop-site-reviewer` role, spawn a generic subagent and paste the
   verifier brief from this workflow; do not review in the main thread. The
   verifier must return compact JSON with pass/fail, `agentBrowserUsed: true`,
   desktop 16:10/16:9 browser checks, screenshots when available,
   overflow/clipping evidence, and focused fixes. Builder must not accept a
   passing review unless actual agent-browser desktop inspection ran.
7. If review fails, send only the focused fixes back to `drop-site-builder` and
   run one more review pass by default. Review fixes must be quick HTML/CSS/JS
   edits. Do not regenerate images or rebuild the whole site unless product
   imagery is missing or invalid. Do not loop endlessly.
8. When review passes, ask `drop-site-deployer` to deploy `siteDir` with Vercel
   CLI using `--prebuilt`, `--archive=tgz`, and `--target preview`.
   Deployment commands must have hard timeouts and must fail loudly rather than
   waiting indefinitely. The deployer gets one bounded deploy attempt and one
   bounded HTTP check; if either fails or times out, it must return compact
   failure JSON with `issues` instead of continuing to wait.
9. Use the immutable Vercel deployment URL from the deployer as both
   `site.deploymentUrl` and `site.canonicalHistoricalUrl`. Do not use or return
   the mutable project alias as the historical live link.
10. Write `builder-output.json`, replacing any previous file.
11. Validate that `builder-output.json` parses, the referenced site files
    exist, and the deployer verified HTTP 200 for the live URL.
12. Return a short status with the output path and immutable deployment URL.

## Static Site Contract

Create one prebuilt static site:

```text
/vercel/sandbox/agent-workspace/builder-site/
  .vercel/output/
    config.json
    static/
      index.html
      assets/
        styles.css
        site.js
        product-hero.png
        product-angle-01.png
        product-angle-02.png
```

`config.json` must be valid JSON for Vercel Build Output API v3:

```json
{
  "version": 3
}
```

The page is a single document. Do not create route trees, catalogs,
dashboards, checkout flows, generated docs, or extra app scaffolding.

## Page Contract

The finished page must be clean, bright, elegant fashion work:

- full-bleed one-page composition that fits in one desktop viewport without
  normal page scrolling
- timer/urgency strip pinned or placed at the top of the page before product,
  price, and CTA content
- selected product as the first-viewport signal
- centered product image carousel dominating the page
- two or three same-product angle images as carousel slides when practical
- automatic carousel advancement with subtle manual controls or indicators
- short drop copy tied to the selected products and cultural moment, kept
  compact enough to preserve the no-scroll one-screen layout
- visible price
- large 24-hour countdown
- dummy `Buy now` button
- sizing or fit guidance only when relevant to the product category
- striking fashion art direction: bright, premium, memorable, and product-led

The dummy button may update local page text, open a small non-checkout note, or
use an inert `button type="button"`. It must not submit payment, collect
shipping details, or navigate to checkout.

## Subagent Responsibilities

- `drop-site-builder`: static HTML/CSS/JS, product angle generation through
  `$imagegen`, visual polish through `$frontend-skill`, and focused fixes.
- `drop-site-reviewer`: local browser QA through `agent-browser`, desktop
  16:10/16:9 screenshots/checks, visual and functional issues.
- `drop-site-deployer`: Vercel CLI deployment, immutable URL capture, HTTP 200
  verification, and no secret leakage.

Builder is the final taste judge. It can reject technically valid pages that
look generic, dark, cluttered, off-brand, or not product-led.

## Deployment Rules

Normal Builder runs deploy preview only:

```bash
vercel deploy /vercel/sandbox/agent-workspace/builder-site \
  --prebuilt \
  --archive=tgz \
  --project "$DRIP_DROP_SITES_VERCEL_PROJECT" \
  --scope "${DRIP_DROP_SITES_VERCEL_SCOPE:-$VERCEL_TEAM_ID}" \
  --token "$VERCEL_DEPLOY_TOKEN" \
  --target preview \
  --yes
```

Do not pass `--prod`. Do not promote the deployment. Do not forward or rely on
`VERCEL_PROJECT_ID` or `VERCEL_ORG_ID`; those can belong to the sandbox host
project and confuse the deploy.

Required env:

- `DRIP_DROP_SITES_VERCEL_PROJECT`
- `VERCEL_DEPLOY_TOKEN`

Optional env:

- `DRIP_DROP_SITES_VERCEL_SCOPE`
- `VERCEL_TEAM_ID` as the scope fallback

Never print token values, project IDs, org IDs, deployment IDs, dashboard URLs,
or private env values in logs or final responses.

## Output

Write the final artifact to:

```text
/vercel/sandbox/agent-workspace/builder-output.json
```

Validate it parses:

```bash
node -e 'JSON.parse(require("node:fs").readFileSync("/vercel/sandbox/agent-workspace/builder-output.json", "utf8")); console.log("json-ok")'
```

Use this schema:

```json
{
  "schemaVersion": "builder.drop-site.v1",
  "generatedAt": "ISO timestamp",
  "input": {
    "selectedMockRefs": ["idea_01-cap-01", "idea_02-sock-01"],
    "sourceArtifacts": []
  },
  "site": {
    "title": "Drop name",
    "slug": "drop-name",
    "siteDir": "/vercel/sandbox/agent-workspace/builder-site",
    "assetDir": "/vercel/sandbox/agent-workspace/builder-site/.vercel/output/static/assets",
    "deploymentUrl": "https://immutable-preview-url.vercel.app",
    "canonicalHistoricalUrl": "https://immutable-preview-url.vercel.app"
  },
  "page": {
    "sections": ["urgency", "carousel", "purchase"],
    "countdownHours": 24,
    "ctaLabel": "Buy now",
    "ctaBehavior": "dummy"
  },
  "strategy": {
    "visualThesis": "Bright elegant fashion direction.",
    "contentPlan": "Short drop narrative and product-specific fit guidance.",
    "interactionThesis": "Countdown urgency with inert purchase intent.",
    "subagentsUsed": [
      "drop-site-builder",
      "drop-site-reviewer",
      "drop-site-deployer"
    ],
    "notes": []
  },
  "review": {
    "passed": true,
    "agentBrowserUsed": true,
    "browserChecks": {
      "desktop16x10": {
        "viewport": "1440x900",
        "screenshot": "/vercel/sandbox/agent-workspace/builder-review-desktop-16x10.png",
        "horizontalOverflow": false,
        "rightEdgeClipping": false,
        "clippedRightEdgeElements": []
      },
      "desktop16x9": {
        "viewport": "1920x1080",
        "screenshot": "/vercel/sandbox/agent-workspace/builder-review-desktop-16x9.png",
        "horizontalOverflow": false,
        "rightEdgeClipping": false,
        "clippedRightEdgeElements": []
      }
    },
    "issues": [],
    "fixesApplied": [],
    "screenshots": []
  },
  "deployment": {
    "provider": "vercel",
    "project": "drip-websites",
    "target": "preview",
    "url": "https://immutable-preview-url.vercel.app",
    "verifiedAt": "ISO timestamp"
  }
}
```

Record review failures honestly. If deployment cannot run because env or CLI
auth is missing, fail loudly and write a JSON artifact only if it clearly marks
deployment as unavailable and does not pretend to have a live URL.
