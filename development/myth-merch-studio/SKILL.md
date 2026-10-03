---
name: myth-merch-studio
description: "Turn symbols, phrases, and fandom lore into merch, collectible, and limited-drop concepts, then output a merch brief. Use when Codex needs to translate fandom canon into products without stripping the meaning out of the source material or crossing licensing lines."
---

# Myth Merch Studio

Use this skill when you need merch or collectible concepts that feel native to the audience's lore instead of generic branded product.

Default product shape: a compact macOS `MenuBarExtra` utility with a source-aware popover for lore loading, concept drafting, and merch export and an optional settings/history window.

## Quick Start

1. Confirm the subject, target audience, and source window.
2. Gather only public or user-authorized material into a working set.
3. Produce a `merch-brief` with the default sections below.
4. If the user wants a richer product concept, keep it menu bar first and native to SwiftUI.

## Accepted Inputs

- canon maps, iconography kits, and known audience symbols or phrases
- product constraints such as format, materials, price bands, and minimum order concerns
- drop timing, event hooks, or seasonality notes
- licensing, trademark, or collaborator boundaries that must stay respected

## Output Artifact

Primary artifact: `merch-brief`

Default sections:
- Merch concepts with audience rationale
- Phrase, symbol, or object mapping for each concept
- Material, format, and packaging notes
- Drop framing, scarcity logic, and no-go ideas
- Rights and risk review before production

## Workflow

### Gather Sources

- Load the strongest symbols and phrases from the audience canon first.
- Separate durable lore from fleeting memes before turning it into product.
- Note the operational constraints early so concepts stay manufacturable.

### Distill Signal

- Match symbols and phrases to product formats that feel earned.
- Reject ideas that flatten the lore into generic slogan merch.
- Flag any likeness, trademark, or collaborator-rights risk before concepting further.

### Build The Artifact

- Export a merch brief with concept, rationale, format, and drop logic.
- Include one stretch concept and one safe concept for each route.
- End with a short rights review so the team knows what needs human approval.

### Mac Product Shape

- Prefer `MenuBarExtra` with these primary actions:
  - `Load Lore`
  - `Draft Concepts`
  - `Review Drop`
  - `Export Brief`
- Keep the popover between 320 pt and 380 pt wide with grouped sections, clear source status, and a strong export action.
- Use a lightweight settings or history window only for source rules, saved exports, or weighting controls.

### Safety Boundaries

- Work only from public or user-authorized material.
- Do not assist with stalking, covert profiling, rumor laundering, harassment, or minors-focused manipulation.
- Do not encourage unlicensed likeness use, collaborator appropriation, or scarcity tactics that lean on pressure instead of meaning.

## Example Prompts

- `Use $myth-merch-studio to turn this artist's canon phrases and symbols into three collectible merch routes with one polished merch brief.`
- `Use $myth-merch-studio to convert this founder-brand lore into tasteful drop concepts that still respect licensing and manufacturing constraints.`

## Resources

- `references/product-spec.md`: product surface, SwiftUI layout, artifact template, icon direction, and first-run behavior.
