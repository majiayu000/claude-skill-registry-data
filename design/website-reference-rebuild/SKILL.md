---
name: website-reference-rebuild
description: Capture a reference website for RESEARCH, extract its design patterns/animations/layout techniques, then rebuild an ORIGINAL, OPC-branded version. Use when Priscila drops a site she wants the OPC website to "feel like", says "copy the feel of this", "rebuild this in our brand", "I like how this site looks", or wants a fancier/animated section modeled on something she saw. Reference capture + ethical rebuild — NEVER a 1:1 clone, NEVER ships the source site's assets. Registered under /opc-website.
---

# /website-reference-rebuild — Reference Capture + Ethical OPC Rebuild

## What this is (and is NOT)

**IS:** a free, self-owned workflow to study a website Priscila likes and rebuild its *design patterns* (layout, motion, glass/glow, scroll behavior) as an **original, OPC-branded** component or page.

**IS NOT:** a website cloner. We do not ship the source site's images, logos, fonts, copy, or code into production. We learn the *technique*, then build OUR version with OUR brand and OUR content.

This skill exists so we never pay for a third-party "site mirror" skill — the engine (HTTrack / SingleFile / curl) is free and open, and the rebuild is what Claude already does. Decision locked 2026-06-23 (Priscila + Codex audit).

---

## 🔒 GUARDRAILS — read every run, non-negotiable

1. **Ethical use only.** Capture for *research/inspiration* on sites we have the right to study. Rebuild ORIGINAL. Never reproduce proprietary design 1:1 for production; never ship their assets (images/logos/fonts/copy).
2. **No "clones every site" promise.** Heavy JS, logged-in/paywalled pages, anti-bot systems, canvas/WebGL/video effects often will NOT capture cleanly and need manual reconstruction. Say so honestly in the report — do not pretend a partial capture is complete.
3. **Brand override.** Output always uses the OPC palette + type + real OPC content. The reference dictates *structure and motion*, never *look-and-feel verbatim*.
   - Palette: obsidian `#0A0A0A` / cream `#F0EBE3` / lime `#CBCC10` / walnut `#8B5A2B`
   - Type: Anton (display) · Cormorant Garamond italic (serif accent) · Roboto Mono (labels) · Inter (body)
4. **STATE.md write rule (from Codex audit):** only append to `OPC_WEBSITE_STATE.md` / the tracker when a rebuild **actually becomes part of the OPC website**. Pure experiments stay out of the master plan — log them only in this skill's scratch notes or a Backlog "tried" note.
5. **Agents are for later.** This skill is a single-site workflow. For big sweeps ("compare 25 contractor sites, rank best hero/gallery/contact patterns") spin up a research/comparison agent separately — not this skill.

---

## Tools (free) — what I run vs what Priscila installs once

| Tool | What it does | Who installs |
|------|-------------|--------------|
| `curl` | Fetch a single page's HTML/CSS to read the technique | ✅ already on macOS |
| **HTTrack** | Recursive site capture (multi-page, assets) | ⚙️ one-time `brew install httrack` (Claude can run if Homebrew present) |
| **SingleFile** | Browser extension — saves a full rendered page (incl. JS-built DOM) to one HTML file | 👤 Priscila installs in her browser once; she exports + drops the file |
| Playwright (already in workspace) | Headless render + desktop/tablet/mobile screenshots for capture + validation | ✅ available |

**Default:** start with `curl` + Playwright (already here). Only reach for HTTrack/SingleFile when the page is JS-heavy and a static fetch misses the design.

---

## Workflow — URL → captured reference → original OPC rebuild

1. **Intake.** Priscila drops a URL + what she likes about it ("the sideways scroll", "the glow", "the hero"). Record her words verbatim.
2. **Capture (research).**
   - Static first: `curl -sL <url>` to read HTML/CSS + identify the animation system (GSAP/Lenis/Framer/CSS/Three.js).
   - If JS-built: Playwright render → screenshot desktop/tablet/mobile; if still missing assets, HTTrack or ask Priscila for a SingleFile export.
   - Capture goes to a scratch folder, NOT the repo: `~/ClaudeWorkspace/opc-website/_reference-capture/<slug>/` (gitignored).
3. **Extract patterns.** Write a short `patterns.md`: layout structure, motion technique + params, scroll behavior, what's reusable. This is the deliverable that matters — the *recipe*, not their pixels.
4. **Rebuild ORIGINAL.** Build the OPC version using our palette/type/real content (brothers, 9 services, counties, license, real Mike photos). Reuse our existing components/classes where possible.
5. **Validate.** Playwright screenshots at desktop / tablet / mobile. Confirm it reads on all three.
6. **Report honestly.** What captured cleanly, what needed manual rebuild, what's blocked (anti-bot/paywall/video), fidelity gaps, and the source URL + usage note for attribution-of-inspiration.
7. **Promote (only if approved + used).** When Priscila approves it onto the live site: THEN follow `/opc-website` auto-rules (lab-banner/cache-bust/tracker/STATE.md/activity log/commit). Until then it stays a candidate.

---

## Integration with /opc-website hub

- This skill is a **tool** under the `/opc-website` project hub. The hub is the brain; this is one recipe it can pull in.
- When a rebuilt component ships to the live site, the **`/opc-website` auto-rules take over** (cache-bust, tracker Prototypes row, STATE.md activity log, commit). This skill hands off at that point — it does not duplicate that logging.
- `_reference-capture/` is scratch only and must be in `.gitignore` — never commit captured third-party assets.

## Quick start (when Priscila says a site)

> "Capture <url> as reference — I like <X>. Rebuild it as OPC."

Then: intake → capture → patterns.md → original OPC rebuild → 3-viewport validate → honest report. Promote to live only on her approval.
