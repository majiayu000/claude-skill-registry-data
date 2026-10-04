---
name: explore
description: Explore how to do something with a library/API — what options exist, with tested snippets and doc/source references — answered directly in the terminal so it informs YOUR design. Grounded in the installed source and current docs for the pinned version; every load-bearing claim is verified by running it. Exploration only — it helps you design, it does not design or plan the implementation. Use when the user runs /explore, asks "how do I / how would I do X with <library>", "what are my options for X", "explore <topic/library>", or wants to understand an API before building. Output stays in the conversation; writing it up to a file/artifact for sharing is opt-in — ask first.
---

# /explore

Explore how to build something with a library/API and answer **in the terminal**. The deliverable is an **exploration**: what the library offers, the ways to do the thing, tested snippets, and references — enough for the user to make their own design call.

## What this is (and isn't)

- **Explores, doesn't design.** This surfaces the options and the ground truth so the *user* designs. Don't produce a design doc, a recommendation framed as a decision, or an implementation plan. A light "which people usually reach for" is fine as information.
- **Informs; planning is a separate step.** Turning a chosen direction into committable work is `plan-targets`, later — not here.
- **Terminal-first and streamlined.** Answer in the conversation so the user can iterate turn-by-turn. **No file, no artifact by default.** Writing it up to share is opt-in (see "Sharing").
- **Grounded and tested.** Based on the installed source and the current docs for the pinned version, with snippets actually run against the installed library.

## Iron rules (non-negotiable)

1. **Read the source and docstring, never trust `dir()` alone.** `dir()` is misleading on TypeAliases, Protocols, callables, and dataclasses — it can show empty or hide the real contract. For every symbol that matters, open its definition and read its docstring.
2. **No absolute claim without a source grep.** Before saying "the only way is X", "Y is unsupported", "Z is empty/unused" — grep the installed source to confirm. If you can't confirm, say it as a question, not a fact.
3. **Hunt the extension points explicitly.** Escape hatches are where the good options live and where they're most often missed: params typed `Callable`/`Protocol`/`Awaitable`, kwargs like `action=`/`hook=`/`on_*`/`callback_*`/`trace_*`, subclass override points, context managers, event/listener registration. Enumerate them for the relevant surface.
4. **Verify by running.** Every load-bearing claim and every snippet is checked against the *installed* library in a scratch script. Tag each: **VERIFIED** (ran it), **DOCS-ONLY** (in docs, not run), or **UNVERIFIED** (inference — say so).
5. **Pin the version, use current docs.** State the exact installed version; base doc claims on that version's documentation. API facts are version-specific.
6. **Label public vs internal.** Mark each API as public (documented, exported, no leading underscore) or internal (docstring says "internal", underscored, absent from docs). Note upgrade-fragility for internal ones.

## How to explore

1. **Scope & pin.** Restate the goal in a sentence. Record the installed version (`uv run python -c "import lib; print(lib.__version__)"`) and note the current doc URL for that version.
2. **Map the surface (ground truth).** Enumerate the public exports relevant to the goal. For each symbol that matters: read its source + docstring, capture `file:line`. Apply rule 3 — find every extension point.
3. **Verify by running.** Write scratch scripts (in the scratchpad dir, never the repo) that exercise the paths the options depend on. Confirm the behaviors that matter — does this hook fire? does this reject that? what does the wire see? Keep the output as evidence.
4. **Answer in the terminal.** Present the ways available with tested snippets and references (format below). Stop there — the user takes it into their own design.

## Answering in the terminal (format)

Keep it scannable and streamlined — a terminal answer, not a document.

- **Lead with a one-sentence framing** of what the library gives you for this.
- **Present the ways available.** For each option: how it works in a sentence or two, public vs internal, the key tradeoff, and a **tested snippet with its real output**. Cite the `file:line` or doc section that backs it.
- **Tag every load-bearing claim** VERIFIED / DOCS-ONLY / UNVERIFIED.
- **A short recap table** of the options (or symbols) is welcome when there are several — but lead with the prose, not the table.
- **Close with a light steer if it helps** ("most reach for X when …") — as information, not a verdict. No "open decisions for you" section, no repo-migration plan.
- **Don't dump a full write-up.** If the answer is getting long, offer to go deeper on one option rather than expanding all of them.

## Diagrams

- The terminal can't render mermaid — so **default to no diagram**. Prose usually carries a small API surface fine.
- Draw a **small ASCII sketch** only when a control/data flow is genuinely hard to follow in words, or when the user asks. Keep it a few boxes and arrows.
- Save mermaid (small, color-coded) for the shareable write-up only — see below.

## Sharing (opt-in)

Only when the user wants to hand this to someone else, or asks to save it:

- **Ask which they prefer first:** a **Markdown file** (repo `docs/` or the scratchpad) or an **Artifact** (clickable link, renders diagrams, theme-aware). Don't assume.
- Then write it up as a walkthrough — same substance, fuller prose. Here diagrams are worth it: small, color-coded mermaid, one per flow (not one big one). Reuse this palette via `classDef` so color means the same thing across diagrams:
  - `public` green `fill:#d3f9d8,stroke:#2b8a3e` · `internal` amber `fill:#fff3bf,stroke:#e67700` · `client`/your-code blue `fill:#d0ebff,stroke:#1971c2` · `fault`/rejection red `fill:#ffe3e3,stroke:#c92a2a` · add `color:#000` for legible text.
  - Quote any mermaid edge label containing `/ ( ) , [ ]` or the parser breaks and the diagram won't render.
- For an Artifact, publish the Markdown file directly (```mermaid fences render natively). Re-publish the same file path to keep the same URL while iterating.

## Notes

- One topic per exploration. If the ask spans two unrelated questions, explore them separately.
- If exploring contradicts something the user (or you) previously believed, say so plainly — a corrected assumption is a finding, not an embarrassment.
- Scratch scripts live in the scratchpad dir, not the repo.
- Pairs with `plan-targets`: once the user picks a direction from the exploration, `plan-targets` turns it into committable checkpoints.
