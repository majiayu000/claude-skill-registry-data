---
name: meta-ad-builder
metadata: {packVersion: 1.3.0}
description: >-
  Publish finished creatives as live Meta (Facebook/Instagram) ads via the Meta
  Marketing API, plus research and ad-copy support. Uploads an image or video,
  builds a multi-variant creative (5 bodies / 5 titles / 3 descriptions in an
  asset feed), and creates a PAUSED ad in an
  existing ad set. Also pulls top-performing ads (ranked by ROAS) and competitor
  ads from the Ad Library to inform copy. Use when the user asks to deploy /
  publish / launch a creative as a Meta or Facebook ad, build a Meta ad, push a
  video or image into an ad set, pull their top ads, or research competitor ads.
  Not for generating creative (use the image/video skills) and not for writing
  ad-table rows.
---

# Meta ad builder

Turn a finished creative — typically the output of a generative-AI skill in this
workspace — into a live Meta ad. The skill covers three phases: **research**
(optional) → **copy** → **deploy**. It talks to the Meta Marketing API directly
via ported, parameterized Python scripts.

> **Meta credentials required before any deploy work.** Run
> `bash scripts/check-meta-env.sh` first — before uploading a creative, before
> creating anything in the ad account, before the first Meta call of any phase.
> On a non-zero exit, stop and ask the user for what it printed. It has already
> uncommented the two required lines in `.env` and opened the file, so the ask
> is "paste these two values", not "go find the docs". Read its Live-app warning
> out to them: a development-mode app passes every check and then fails at ad
> creation. Until the check passes, nothing is uploaded, no partial ad or
> creative exists and nothing is charged — which is exactly why it runs first,
> since a deploy that dies halfway orphans uploaded assets in a live ad account.
> This key is deliberately lazy: the pack asks for it here, at the moment
> someone wants to publish, and never during setup.

## When to use this skill

Trigger on phrases like:
- "deploy this video to Meta" / "publish this as a Facebook ad"
- "build/launch a Meta ad" / "push this creative into <ad set>"
- "create a Meta ad with this image and copy"
- "pull my top-performing ads" / "what are my best ads by ROAS"
- "research competitor ads" / "pull <brand>'s ads from the Ad Library"

Do **not** use this skill to *generate* creative — that's `pixar-ad`,
`claymation-ad`, `chatgpt-image-ad`, `nano-banana-image-ad`,
`generate-youtube-thumbnail`, etc. Do not use it to write ad-table rows. This
skill is the *direct Meta Marketing API* deployment step.

## Read order

1. **This file** — workflow, decision tree, safety rules.
2. **[prompting/copy-guide.md](prompting/copy-guide.md)** — the 5-body / 5-title /
   3-description frameworks and the `--copy-file` JSON shape.
3. **[reference/deploy-patterns.md](reference/deploy-patterns.md)** — creative
   spec mechanics, video polling, retry, failure modes.
4. **[reference/meta-api-cheatsheet.md](reference/meta-api-cheatsheet.md)** — the
   full Meta Marketing API reference (campaigns, ad sets, ads, enums, gotchas,
   Ad Library). Consult as needed; don't read end-to-end.

## Prerequisites

> **REST key required. A Novoads MCP connector is not a substitute.** If
> `NOVOADS_API_KEY` is missing or still the placeholder, stop before any
> generation work and tell the user: "Before continuing, create an API key at
> <https://novoads.ai/dashboard/settings?tab=api> and paste it into `.env`."
> That holds even when `mcp__novoads__*` tools are connected and authenticated in
> the session. Never call `mcp__novoads__*` tools from this repo's workflows: they
> are a different surface with different behavior, including the units they quote
> costs in. Repo installs verify with `./scripts/check-novoads-env.sh`; a solo
> install checks `NOVOADS_API_KEY` in the environment.

**Pack version.** Every `/v1` response carries `X-Novoads-Pack-Version`; mention a newer pack at <https://github.com/novoads/agent-skills> only when that header names a version NEWER than this file's `metadata.packVersion` — equal or older is nothing to say, and it is never a reason to stop.

### The Meta app must be published (Live) — check this first

**A development-mode app cannot create ad creatives.** `POST /act_*/ads` fails
with **code 100 / subcode 1885183** ("Ads creative post was created by an app
that is in development mode"). Every other prerequisite can be perfect and the
deploy still cannot succeed.

Allowlisting the ad account under **App settings → Advanced → Authorized ad
account IDs** does **not** work around it — tested live on 2026-08-03 and it
does not help. Publishing the app is the only fix: App Dashboard → toggle the
app from *Development* to *Live*.

No Graph endpoint reports app mode for a user token, so `check-meta-env.sh`
cannot test this for you. Ask the user to confirm the app is Live before the
first deploy against a given app.

### Everything else

- **Env** (in `.env` — see your repo's `.env.example`):
  - `META_ACCESS_TOKEN` (required) — long-lived token with `ads_management` scope
  - `META_AD_ACCOUNT_ID` (required) — with or without the `act_` prefix
  - `META_PAGE_ID`, `META_IG_USER_ID`, `META_PIXEL_ID` (optional defaults for deploy)
  - `META_API_VERSION` (optional, default `v23.0`)
- **Python deps — install into a virtualenv:**

  ```bash
  python3 -m venv .venv-meta
  .venv-meta/bin/python -m pip install -r scripts/requirements.txt
  # then run the scripts with .venv-meta/bin/python, not bare python3
  ```

  Bare `python3 -m pip install` **fails on a Homebrew python** with
  `error: externally-managed-environment` (PEP 668), and macOS is this repo's
  first target. Do not suggest `--break-system-packages`; use the venv.
- **A target ad set** that already exists. The skill deploys ads into an existing
  ad set — it does not create campaigns or ad sets. If the user needs a new ad
  set, create it in Ads Manager or via the cheatsheet §3–§4 first.
- **The finished creative on disk** — an image or video file path. Chat-pasted
  files are not accessible; ask the user for a real path.

Run `bash scripts/check-meta-env.sh` to verify credentials before anything else.
It checks the token, the `ads_management` scope, ad-account reachability and the
Page — a token that passes `/me` but carries no ads scopes is a real failure mode
it now catches.

**When credentials are missing it sets the user up rather than only complaining.**
It uncomments the two required lines in `.env` (they ship commented out, and a
token typed onto a commented line fails the next run identically — the most
likely way this path breaks in practice), opens the file, and prints where each
value comes from plus the Live-app warning. Relay what it printed; it is written
to be read out. It leaves the four optional keys commented, never touches a line
the user has already edited, and exits 1 either way.

## Workflow

### Phase 1 — Research (optional, when copy should model winners)

```bash
# Rank the account's ads and pull the winning copy
python scripts/pull-top-ads.py --date-preset last_30d --min-spend 100 --limit 15

# Pull a competitor's ads from the Ad Library
python scripts/pull-competitor-ads.py --pages "BrandName" --limit 50
```

Both write JSON under `OUTPUT_BASE` (or `./outputs/meta-ads/`). Read the top-ad
`copy` fields to identify winning hook/proof/CTA patterns before writing new copy.

### Phase 2 — Copy

Write a `copy.json` following **[copy-guide.md](prompting/copy-guide.md)**:
5 bodies (one per framework angle), 5 titles, 3 descriptions. If Phase 1 ran,
mirror the voice and patterns of the winners — new creative + proven copy DNA.
Save `copy.json` somewhere under `outputs/` so it isn't committed.

### Phase 3 — Deploy

**Always dry-run first** — it prints the creative payload **in full**
(no truncation) plus a dedicated Advantage+ enhancement section, and makes no
API calls:

```bash
.venv-meta/bin/python scripts/deploy-ad.py --dry-run \
  --adset-id <AD_SET_ID> --copy-file copy.json --link <DESTINATION_URL> \
  --image path/to/creative.png
```

Review the payload with the user, then deploy for real:

```bash
.venv-meta/bin/python scripts/deploy-ad.py \
  --adset-id <AD_SET_ID> --copy-file copy.json --link <DESTINATION_URL> \
  --video clip-a.mp4 --video clip-b.mp4 --cta SIGN_UP --pixel-id <PIXEL_ID>
```

- `--image` / `--video` are repeatable — each becomes its own ad in the ad set.
- Every ad is created **PAUSED**. Tell the user to review and un-pause in Meta
  Ads Manager. The skill never launches a spending ad automatically.
- Results are written to `deployment_results.json` under `OUTPUT_BASE`:
  `ads` (created), `failures` (each with the verbatim Meta error), `orphans`,
  and a `summary` count.

#### Read the exit code

`deploy-ad.py` **exits 1 if any requested ad failed**, and prints each failure
with Meta's own code / subcode / message / `fbtrace_id`. It no longer prints a
`DONE.` line on a run that created nothing. If you are wrapping this script,
branch on the exit code — do not parse stdout for success.

#### Advantage+ enhancements and burned-in captions

The dry run lists every `degrees_of_freedom_spec` enrollment Meta will apply,
with a one-line note on what each one does to a shipped creative. Read that
section aloud to the user before a first deploy — several enrollments **modify
the creative**, and the defaults are opt-in.

By default the script sets `--burned-in-captions`, which forces to `OPT_OUT`
the enrollments that would deface a creative with text baked into the pixels
(`video_uncrop`, `video_auto_crop`, `video_filtering`, `creative_stickers`,
`reveal_details_over_time`, `show_summary`, `show_destination_blurbs`, and the
`text_extraction` customizations) plus `text_translation`, which rewrites copy
the user approved verbatim. Everything this workspace produces carries burned-in
text — captions on video from `caption-video`, typography on images from the
image-ad skills — so this is the right default here.

Pass `--no-burned-in-captions` to send Meta's full enrollment instead. Say so
explicitly when you do; it is the user's creative that gets modified.

## Decision tree

| User intent | Phases |
|---|---|
| "Deploy this creative to Meta" + copy provided | Phase 3 only |
| "Build a Meta ad, write the copy too" | Phase 2 → 3 |
| "Make ads modeled on my winners" | Phase 1 → 2 → 3 |
| "What are my best ads / competitor research" | Phase 1 only |

## Safety rules

- **Ads deploy PAUSED.** Never add an `--active` override or un-pause ads without
  an explicit user instruction. Confirm the user knows the ads are paused.
- **Dry-run before every real deploy.** Show the payload; get a go-ahead.
- **Confirm the target ad set and destination URL** with the user before
  deploying — an ad in the wrong ad set spends against the wrong budget.
- **Deploying ads is a shared-state, money-adjacent action.** Treat the live
  `deploy-ad.py` run as something to confirm, not assume.
- The skill creates ads only — it does **not** create or edit campaigns, ad sets,
  budgets, or audiences. Those stay manual.

## Quirks and pitfalls

- **App in development mode → code 100 / subcode 1885183.** See Prerequisites.
  This is the single most likely reason a first deploy fails.
- **Video processing is async.** `deploy-ad.py` polls the uploaded video until
  Meta finishes processing before creating the ad — a video deploy can take a
  few minutes. See [deploy-patterns.md](reference/deploy-patterns.md).
- **Transient `OAuthException` (code 2).** Retried automatically with backoff.
- **`act_` prefix** is added automatically if missing from `META_AD_ACCOUNT_ID`.
- **A failed run can leave uploaded assets behind.** The video/image upload
  succeeds before ad creation is attempted, so a rejected ad orphans the asset.
  `deploy-ad.py` prints every orphan with a ready-to-run `curl` cleanup line and
  records them under `orphans` in `deployment_results.json`. It does **not**
  delete anything automatically — deleting objects in a live ad account is the
  user's call. Offer the cleanup commands; don't run them unprompted.
- **`link_urls` is sent for image ads only — this is deliberate, not a bug.**
  `build_image_creative` puts `link_urls` in `asset_feed_spec`;
  `build_video_creative` does not. A live video deploy (2026-08-03) confirmed the
  ad resolves its destination correctly without it, carrying the link through
  `object_story_spec.video_data.call_to_action` instead. Leave the asymmetry
  alone; it is verified working.
- **`TEXT_LIQUIDITY` does not read back on the live creative.** The skill sends
  `text_transformation_types: ["TEXT_LIQUIDITY"]` and
  `degrees_of_freedom_type: "USER_ENROLLED"`, but reading the created creative
  back does not show either field (verified 2026-08-03). The functional part
  *does* persist — the 5/5/3 asset feed was present on the live ad. **Verify by
  asset feed, not by flag:**

  ```bash
  curl -s -G "https://graph.facebook.com/v23.0/<AD_ID>" \
    --data-urlencode "fields=creative{asset_feed_spec,degrees_of_freedom_spec}" \
    --data-urlencode "access_token=$META_ACCESS_TOKEN" | python3 -m json.tool
  ```

  Confirm `asset_feed_spec.bodies/titles/descriptions` carry the counts you sent.
  Do not claim multi-variant text rotation is enabled on the basis of the flag
  you sent — say what read back.
- **Account-specific data stays out of git.** All output routes through
  `outputs/` (gitignored): ad IDs, pulled spend/revenue, competitor data.
- **Special Ad Categories** (credit, employment, housing, social issues) change
  ad-set targeting rules — flag to the user; see cheatsheet §3.5.

## Cost note

The Meta Marketing API itself is free to call. **Ad spend is real money** — but
because every ad deploys PAUSED, nothing spends until the user un-pauses it in
Ads Manager. There are no per-call credits to estimate.
