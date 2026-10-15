---
name: pb-landing-page
description: >-
  Build and launch a landing page: confirmed copy without invented claims, a
  generated page in your brand tokens, UI and SEO review, deploy only after
  GO, then a check on the live URL. Use for "landing page", "launch page for
  this product", "ship a one-pager".
category: design-ui-ux
kind: playbook
trigger: ["landing page", "launch page for this product", "ship a one-pager"]
inputs: [brief, brand_tokens, deploy_target, "launch_video?"]
requires:
  skills: [copywriting, landing-page-generator, godmode-ui-ux, ui-ux-pro-max, seo-audit, bdb-deploy, vercel-deployment, pb-launch-video]
  agents: []
  mcps: [chrome-devtools]
  store: []
go_points: [deploy]
outputs: ["<page source>", "production_artifacts/pb-landing-page-<date>.md"]
verify: "curl -sI <url> returns 200; seo-audit on the live URL has zero blocking items"
difficulty: intermediate
est_time: 1-3 h
---

# Landing page launch
What you get: a live landing page with checked copy, SEO basics and, if you have one, a launch video.

## Inputs
- brief — product brief: audience, offer, proof you can show
- brand_tokens — path to the design tokens or brand notes
- deploy_target — `bdb-deploy` (rsync over SSH) or `vercel`, with the target host or project
- launch_video (optional) — an mp4 from pb-launch-video, used as the hero video

## Steps
1. Ask — brief, brand_tokens, deploy_target, launch_video → run log — all answered; token path exists; `chrome-devtools` is optional, if its tools are not loaded the screenshot in step 3 is skipped and logged
2. copywriting — brief → confirmed brief, then page copy in the run folder — brief confirmed by the human, no claim without a source in the brief (no fabricated numbers, logos or quotes) — stops for approval
3. landing-page-generator + godmode-ui-ux — approved copy, brand_tokens, launch_video → page source in the project — page opens locally; `puppeteer_navigate` and `puppeteer_screenshot` of the local page attached to the run log when chrome-devtools is available
4. ui-ux-pro-max (ui-review instead if the optional StyleSeed package is installed) + seo-audit — page → findings table in the run log — no open blocking finding; fixes applied and rechecked before step 5
5. [GO] deploy — via bdb-deploy (rsync) or vercel-deployment (`vercel deploy`), target host or project and the file list named in the WAITING FOR GO line. The run stops here until the human types GO. Neither command is hook-guarded, so this GO is the only guard. One GO = one deploy.
6. Live check — `curl -sI <url>` and seo-audit on the live URL → run log — status 200 and zero blocking items; otherwise stop and report, no redeploy without a fresh GO at step 5

Run log: `production_artifacts/pb-landing-page-<date>.md` in the start directory, never committed

Rules
- Anything other than the literal GO (case-insensitive) is not a GO; a GO covers only that one step, one time.
- A failed check stops the run: write the failure into the run log and report. No silent retries.
- Write one run-log line per step as it completes (`N. done|skipped|failed — artifact — check result`) and `WAITING FOR GO: <step>` at each gate.
