---
name: lean-canvas
description: This skill should be used when the user wants to capture, build, or refine their business model on a one-page Lean Canvas — "help me make a lean canvas", "let's document my business model", "fill in the canvas for my idea", "update my lean canvas", "what's my UVP / unfair advantage / revenue model?", or brainstorming model variants (different customer segments, pricing, channels). It writes and versions .lean/canvas.md, working block by block, and flags each entry as an untested assumption. Use it for the "Document your Plan A" step of Running Lean. For ranking which assumptions to test first, use prioritize-risks instead.
version: 0.1.0
---

# Lean Canvas

Capture the business model on one page so it can be shared and tested. You work as the **Strategist** guide role (`../../reference/roles.md`); if the user wants a generative co-creation session, the **Business partner** role pairs well (offer it). Read `../../reference/methodology.md` for where the canvas sits, and `references/canvas-blocks.md` for the per-block guidance before filling blocks.

## When to use

The user wants to get their model out of their head and onto the canvas, or revise an existing one. Also: brainstorming variants (alternate segments, pricing, channels) — capture each as its own canvas. This is the *document Plan A* step; it is **not** where you decide what to test (that's `prioritize-risks`) or test it (that's the interview/experiment skills).

## Core stance

- **Every block is a hypothesis, not a fact.** Fill them confidently but label the whole canvas as untested. The value is making assumptions explicit so they can be attacked later.
- **The model is the product.** Don't let the Solution block balloon. It's one-ninth of the page; the right (market) side is where most ventures actually fail.
- **Fast and concise.** A canvas is an afternoon's work, not a month's. Force short, sharp wording — if a block needs a paragraph, the thinking isn't done yet.
- **Pick a single customer segment per canvas.** Different segments → different problems, channels, and pricing → different canvases. A canvas trying to serve everyone serves no one.

## Procedure

1. **Load context.** If `.lean/canvas.md` exists, read it (you're revising). Read the workspace rules in `../../reference/workspace.md`. If there's no `.lean/`, the coach normally onboards first — create `.lean/` if needed.
2. **Fill block by block, in the recommended order** (not left-to-right). This order front-loads the parts that matter most and that the rest depend on:
   1. **Customer Segments** (and **Early Adopters** within them) — who, specifically.
   2. **Problem** (top 1–3) and **Existing Alternatives** — how they cope today.
   3. **Unique Value Proposition** (+ a **High-Level Concept**, the X-for-Y analogy).
   4. **Solution** — the smallest features that address the top problems.
   5. **Channels** — paths to those customers.
   6. **Revenue Streams** and **Cost Structure** — is there a viable model?
   7. **Key Metrics** — the few numbers that signal health.
   8. **Unfair Advantage** — leave blank if there isn't a real one yet (most aren't; that's honest).
   Use `references/canvas-blocks.md` for what good looks like in each block and the common traps.
3. **Interrogate as you go.** Ask the question that exposes the assumption, not the question that fills the box. "Who *specifically* feels this most?" beats "who are your customers?" Where the user hand-waves, note it.
4. **Write the canvas** to `.lean/canvas.md` using `assets/canvas-template.md`. Keep the block wording terse. Add a dated `## Revisions` line describing what changed and why (per `../../reference/workspace.md`).
5. **Brainstorm variants when useful.** If multiple plausible segments/models exist, capture each as a separate canvas (or a clearly delimited section) rather than mushing them together — you'll rank them in `prioritize-risks`.
6. **Hand off.** A fresh or revised canvas almost always wants `prioritize-risks` next ("now let's find the riskiest assumption to test first"). Say so.

## Output

`.lean/canvas.md` — all nine blocks filled (or honestly blank), terse, with a dated revision note. Then a one-line "riskiest-looking assumption" observation to tee up `prioritize-risks` — but do not rank here.

## Related

- `prioritize-risks` — rank the canvas's assumptions by risk; pick where to start.
- `lean-roles` — Business partner (co-create variants) or Devil's advocate (attack the canvas).
- `references/canvas-blocks.md` — per-block guidance; `assets/canvas-template.md` — the file format.
