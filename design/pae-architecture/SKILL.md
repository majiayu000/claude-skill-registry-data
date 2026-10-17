---
name: pae-architecture
category: How Milo works
blurb: The canonical blueprint of the Personal Analytics Engine — its modules, zero-knowledge design, and how the flagship is put together.
example: Walk me through the PAE architecture, module by module.
---
# PAE — Personal Analytics Engine (Canonical Reference)

PAE is Nrupal's flagship investment product: institutional-grade financial analytics for individuals, zero-knowledge encryption, 11 Aladdin-parity modules. Repo: `nrupala/pae` (AGPL-3.0). It fits as **Segment 6** in the ZKPC stealth product portfolio.

## Master spec (three documents)
1. **PAE Part 1 — Project Spec:** https://www.town.com/content/document/nx7dxdmg2qd1wkv3p138jmjjd186j96d — core architecture, zero-knowledge encryption, 11 Aladdin-parity modules, regulatory framework (FINRA 2214 + CSA), open-source building blocks, 6-phase roadmap.
2. **PAE Part 2 — Beyond Aladdin:** https://www.town.com/content/document/nx7bkc0zcjwdfkgje12m4brbv586j6t7 — Aladdin's 5 structural blind spots, 8 PAE-original capabilities, the **revised** architecture, FOSS business model, 8 first-principles capabilities institutions can't build, 5-layer hierarchy of value, PAE Academy, Personal Knowledge Engine (PKE).
3. **PAE References & Sources:** https://www.town.com/content/document/nx71a58k8x56x8vttx0rz2hqjn86j35n — ~154 sources across 13 categories.

Flagship development session: https://www.town.com/assistant/j57c5gw53d8g2hs125zpbz5wx586j3aq

## Canonical architecture (Part 2 wins)
- **Rust** hot path
- **Python** analytics
- **C** numerical core
- **Vanilla TypeScript + Web Components** UI

**Critical:** Part 1's tech-stack section still references Next.js / React / Tailwind. That is **superseded**. Never reintroduce Next.js/React for PAE — the canonical stack is the one above. A consolidated v2 merging Part 1 + Part 2 is the next priority.

## Design principles
1. **Tool calculates, user decides.** PAE never crosses into advice — it surfaces analytics; the user makes the call.
2. **Zero-knowledge, zero-trust, user-held keys.**
3. The Rust/Python/C + vanilla TS split above is the architecture.
4. PAE = Segment 6 of the ZKPC stealth portfolio.
5. **Revenue from certification (PCA / PCRE / PCDA), membership, and developer licenses — not from gating features.** The product stays open; money comes from the ecosystem around it.

## Regulatory frame
FINRA Rule 2214 + CSA. Keep PAE on the "tool, not adviser" side of the line at all times.