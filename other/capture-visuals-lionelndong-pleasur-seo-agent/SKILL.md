---
name: capture-visuals
description: Resolve bot-walled EXTERNAL visual placeholders (Google SERP, Reddit, competitor UIs) that the headless /generate-visuals pass left `failed`/`manual`. Provider-agnostic by design — a model-neutral headed-browser engine does the work; Claude-in-Chrome is only an optional fallback. Run after /generate-visuals when the manifest has unresolved externals; re-gates visuals when done.
---

# capture-visuals — finish the bot-walled external screenshots (provider-agnostic)

## Why this exists

The main `/generate-visuals` pass captures `type=external` screenshots **headless** (fast). Bot walls
(Google SERP, Reddit, some competitor sites) block headless browsers, so those entries land `failed`
with a `claude_in_chrome` breadcrumb in `content-pipeline/images/<slug>/manifest.json`. Without this
skill they sit forever as `<!-- VISUAL-TODO -->` placeholders and the article ships visually short.

This skill **finishes them as one continuous capture flow** — and it is deliberately **not** tied to any
one model. The heavy lifting is a pure-Python engine that runs the SAME way whether the EO is Claude,
Codex, or anything else. Claude-in-Chrome is only a top-up for the rare site the engine can't reach.

## The backend chain (capability, not a hardcoded tool)

The capability is "capture a bot-walled external screenshot." Backends, in order — best AVAILABLE wins,
and the resulting PNG is identical regardless of the EO's model:

1. **Headed patchright on `:99`** (the engine in `scripts/capture_visuals_resolve.py`) — model-neutral,
   free, no infra. Passes the walls a headless browser can't (proven on Google SERP). If a guessed CSS
   selector misses (common — the EO never saw the live DOM), it falls back to a clean viewport capture.
   **This is the default and handles most externals.**
2. **Claude-in-Chrome MCP** (`mcp__Claude_in_Chrome__*`) — only when the EO is a Claude model. Use it for
   sites the headed engine can't get: **datacenter-IP blocks (e.g. Reddit returns "you've been blocked by
   network security")** and login walls, where a real proxied browser session is needed. It drives the
   dedicated `paperclip-whwi-chrome-1` browser (real Chrome + clean SOCKS proxy + stealth).
3. **Manual** — last resort. Leave the entry `failed`; an editor handles it. **Never bypass real site
   protections** beyond a legitimate session.

## Steps

1. **Run the model-neutral engine.** From the blog-engine root, with the X display set:
   ```bash
   DISPLAY=:99 python3 .claude/skills/capture-visuals/scripts/capture_visuals_resolve.py <slug>
   ```
   It re-attempts every `failed`/`manual` external in the manifest with headed capture, saves
   `content-pipeline/images/<slug>/external-*.png`, rewrites the cited-draft placeholders to
   `![alt](images/<slug>/file.png)` (reusing the main engine's rewrite so output is identical), and flips
   resolved entries to `captured`. It prints `{captured, remaining, still_failed[]}`.

2. **Vision-check every external you captured — this is the honesty gate.** Open each captured PNG (and
   ESPECIALLY any manifest entry flagged `"needs_review": true` — those are viewport fallbacks where the
   selector missed). Confirm it actually shows the thing the placeholder claims. **Reject and delete any
   capture that is a bot-block page, a login wall, a cookie/consent screen, a 404, or otherwise not the
   real content** — e.g. a Reddit "you've been blocked by network security" page must NEVER be presented
   as "a real user complaining…". A wrong/blocked capture is worse than none. Re-mark such entries
   `failed` so they route to step 3 or stay manual.

3. **Top up residuals with Claude-in-Chrome (only if you are a Claude model).** For each `still_failed`
   external (and any you rejected in step 2) that is a REAL, reachable URL, drive Claude-in-Chrome:
   `navigate` to the URL, dismiss consent, find the element the placeholder describes (use the page text,
   not the guessed selector), screenshot it, save to `content-pipeline/images/<slug>/external-<index>-<name>.png`,
   then re-run the engine (step 1) so it picks up the new file and rewrites the draft. If a URL is
   fabricated / dead / genuinely walled, **do not invent a substitute** — leave it `failed` and flag the
   draft (a fabricated source is a content bug; see the honesty rule in `quality-check`).

4. **Re-gate.** `python3 scripts/pipeline_gate.py visuals <slug>` — exit 0 means the visuals stage is
   clean. Surviving placeholders are converted by `/format-for-publish` to invisible
   `<!-- VISUAL-TODO -->` markers (text publish is never blocked).

## Hard rules

- **Provider-agnostic:** never make the outcome depend on Claude-in-Chrome. The engine (step 1) must do
  the bulk; Claude-in-Chrome is a fallback. If the EO is not a Claude model, steps 1, 2 and 4 still fully
  apply and most externals still resolve.
- **Honesty:** never present a block/login/error page, or a screenshot of a fabricated source, as a real
  cited visual. When in doubt, drop the visual.
- **Don't disturb** the byline (`<!-- byline: … -->` line 1), `[GAIN]`, or already-captured visuals.
- **Hardening backlog (not blocking):** a pattern-based block-page detector (`block_check`) could move
  the step-2 reject into the engine; until then the vision check + the VISUAL-CRITIQUE-LOOP gate are the
  honesty backstop.
