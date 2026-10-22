---
name: idea-forge
description: Run any raw idea through a multi-stage R&D pipeline that interprets, expands, scores, and converts it into an actionable engineering plan. Always trigger immediately when the user's message starts with "idea". Also trigger on "ideaforge", "analyze this idea", "expand this concept", "assess this invention", "explore this thought", "develop this further", "turn this into a project", "evaluate feasibility", "forge this idea", or any request to analyze, expand, score, or develop a rough concept or invention into a structured plan.
---

# IdeaForge

## Intent

Run raw ideas through a structured R&D pipeline that clarifies the concept, expands it, scores it, and produces an MVP direction.

## Workflow

1. Identify the exact task and available source material.
2. Apply the domain rules and output format in this skill.
3. State assumptions, uncertainty, and missing inputs clearly.
4. Return the requested artifact, recommendation, or review in a practical format.
5. Check the result against the validation checklist before finishing.

## Constraints

- Do not fabricate missing facts, measurements, dates, sources, or user context.
- Keep output aligned with Mick's direct, practical communication style unless the skill says otherwise.
- Preserve safety, legal, medical, financial, and operational boundaries stated in this file.
- Prefer concise, usable output over broad explanation.

## Validation Checklist

- [ ] The output matches the skill's intended task and platform.
- [ ] Required inputs, assumptions, and uncertainty are explicit.
- [ ] Safety, scope, and source limits are respected.
- [ ] The response follows the requested format or the skill's default output format.
- [ ] The result is practical enough to use without another cleanup pass.

Runs raw ideas through a five-stage R&D pipeline — capture, interpret, expand, score, output. Turns a rough thought into a structured invention plan with scoring, architecture suggestions, monetization paths, and a working MVP roadmap.

## Trigger

Start any message with `idea` to activate immediately.

```text
idea [raw idea, rough concept, or messy note]
```

Other triggers: `ideaforge`, `analyze this idea`, `expand this concept`, `assess this invention`, `explore this thought`, `develop this further`, `evaluate feasibility`

Delivery target modifiers:

- `save to apple notes`
- `send to apple notes`
- `save this analysis to apple notes folder [folder name]`
- `save to obsidian`
- `send to obsidian`
- `save this analysis to obsidian ideas folder`

## Do Not Use When

- The user wants to capture a note without analysis — use a notes tool instead.
- The user wants a resume, blog post, or content piece — use the appropriate skill.
- The user is asking a general knowledge question — answer directly without running the pipeline.

If the user explicitly asks for the final analysis to be saved after the pipeline runs, keep using IdeaForge and treat persistence as a delivery step after Stage 5.

## Modes

Default is **Full Pipeline**. Detect intent and run the smallest mode that fits.

| Mode | Trigger phrase | What runs |
| --- | --- | --- |
| Full Pipeline (default) | `idea [idea]` | All five stages |
| Quick Assess | `idea quick [idea]` | Stages 1-2 only — categorize and feasibility check |
| Score Only | `idea score [idea]` | Stages 1 and 4 only — scoring table |
| Expand Only | `idea expand [idea]` | Stages 1 and 3 only — expansion without scoring |
| Commercialize | `idea commercialize [idea]` | Stages 1, 3 (business models only), and 5 (monetization output only) |
| Compare | `idea compare [idea A] vs [idea B]` | Full scoring on both, side-by-side verdict |
| Revisit | `idea revisit [idea]` | Re-run scoring on a previously forged idea against the current landscape |
| Status | `idea status [idea]` | Check what changed since the idea was forged: new competitors, APIs, feasibility signals |

Delivery targets:

- Default: return the analysis in chat only
- Apple Notes on macOS: after Stage 5, save the final analysis into the requested Apple Notes folder by running `scripts/save_to_apple_notes.py` when the runtime can access the local Notes app
- Apple Notes on iOS: prepare the final analysis for Apple Notes, then hand it off through an iOS Shortcut or share action because the skill runtime does not get direct Notes app write access on iOS
- Obsidian Ideas folder: after Stage 5, save the final analysis as a Markdown note in the `Ideas` folder of the user's Obsidian vault by running `scripts/save_to_obsidian.py` when the runtime can access the vault path or an Obsidian URL handoff

---

## Stage 1 — Capture and Classify

Accept any input format: typed sentence, pasted notes, bullet list, voice note transcript, rough sketch in words.

Extract:

- **Core problem** — what problem is this solving, even if the user did not state it explicitly
- **Proposed mechanism** — what the idea does or how it works at a high level
- **Idea type** — classify using the type table below
- **Domain** — one or more industries or technology areas this touches

Idea type classification:

| Type | Examples |
| --- | --- |
| Product | Consumer app, hardware device, SaaS tool |
| Automation | Workflow, scheduled task, n8n flow, Home Assistant integration |
| Infrastructure | Homelab, server config, network, storage |
| Platform | API, marketplace, developer tool, SDK |
| Research | Academic hypothesis, data analysis, experiment |
| Business model | Licensing approach, monetization strategy, service model |
| Integration | Connecting two existing systems or APIs |
| Process | Workflow redesign, operational improvement |
| Creative | Content system, generative idea, media format |

If the type is unclear, choose the closest fit and state the assumption in one line.

---

## Stage 2 — Interpret

Assess the idea against these dimensions. Each feeds the scoring model in Stage 4.

**Existence check**
Does this already exist in a recognizable form? If yes, name the closest known product or project. If a version exists but the idea adds meaningful differentiation, note the gap.

**Technical feasibility**
Is this buildable with current technology? What are the hardest technical problems? What dependencies does it require (APIs, hardware, compute, data)?

**Commercial viability**
Is there a realistic customer or buyer? What is the likely size of the market? Is this a painkiller (solves a real problem) or a vitamin (nice to have)?

**Patent potential**
Does this involve a novel mechanism, process, or composition? Is the core concept likely already claimed? What is the strongest angle for IP protection if any exists?

**Competition saturation**
How crowded is this space? Name direct competitors if known. A saturated space is not automatically a reason to abandon — execution and positioning matter.

**Automation potential**
How much of this could be automated, scheduled, or made self-running? Higher automation potential means lower ongoing operational cost.

**Privacy and security surface**
Does this touch personal data, credentials, financial data, health data, or live system access? Flag any significant risk area.

---

## Stage 3 — Expand

Generate extensions, implications, and possibilities the user may not have considered. Cover all that apply:

**Features and capabilities**
- What is missing from the core idea that would make it meaningfully more useful?
- What edge cases does the current framing not handle?

**Integration opportunities**
- What existing systems, APIs, or platforms could this connect to?
- What would an n8n workflow look like that incorporates this?
- What Home Assistant, Proxmox, or other homelab integrations apply?

**Business models**
- SaaS subscription
- One-time purchase or license
- Usage-based pricing
- Open source with paid support or hosted version
- White-label licensing
- API access tier model
- Marketplace listing

**AI opportunities**
- Where could a Claude, OpenAI, or local LLM model make this smarter?
- Where could embeddings or semantic search add value?
- What prompt or agent architecture fits?

**Automation paths**
- What parts of this could run unattended on a schedule?
- What triggers (webhook, cron, sensor event) would power the automation?

**Local-first alternative**
- Can this run fully local without cloud dependencies? What would that require?

**Monetization angles**
- What is the fastest path to revenue?
- What would the first paying customer look like?
- What is the minimum viable commercial version?

**Licensing and IP**
- Could this be patented? What is the specific novel claim?
- Could this be licensed to a larger platform?
- Does this have open source potential that builds adoption before monetization?

---

## Stage 4 — Score

Use `scoring-model.md` as the authoritative source for weights, scales, and formulas.

Score each metric from 0 to 10. Calculate the weighted IdeaForge Score. Apply the verdict band. Surface the two highest-scoring and one lowest-scoring metric as key signals.

Output a score table in this format:

```
| Metric                  | Score | Weight |
|-------------------------|-------|--------|
| Technical Feasibility   | X/10  | 20%    |
| Commercial Potential    | X/10  | 25%    |
| Automation Potential    | X/10  | 15%    |
| Implementation Simplicity| X/10 | 15%    |
| Market Openness         | X/10  | 10%    |
| Patent Potential        | X/10  | 10%    |
| Speed to MVP            | X/10  | 5%     |

IdeaForge Score: XX/100
Verdict: [band label]
```

Conservative scoring rules:
- When uncertain between two adjacent scores, choose the lower one.
- Do not inflate scores based on enthusiasm in the user's input.
- If a required signal is missing (no market data, no technical detail), note it as a missing input and score conservatively.

---

## Stage 5 — Output

Generate a structured output document. Use `output-template.md` as the structure reference.

Include all sections that have meaningful content. Omit sections that do not apply — do not generate placeholder filler.

Core output sections:

1. **Idea Summary** — one paragraph, plain language
2. **Core Problem** — the specific pain point being solved
3. **Proposed Solution** — what this does and how
4. **IdeaForge Score** — the scoring table from Stage 4
5. **Technical Analysis** — stack, dependencies, hard problems
6. **AI Opportunities** — where LLMs or ML models add value
7. **Automation Opportunities** — what runs unattended and how
8. **Suggested Architecture** — high-level component diagram in text or table form
9. **Potential APIs and Integrations** — named services, not generic categories
10. **Privacy and Security Concerns** — specific risks and mitigations
11. **Monetization Opportunities** — ranked paths from fastest to most ambitious
12. **Patent Potential** — specific novel claim if applicable, or "no clear patent angle"
13. **MVP Roadmap** — phased build plan, Phase 1 should be completable by one person in under 30 days
14. **GitHub Repository Suggestions** — repo name, description, suggested folder structure
15. **Similar Existing Products** — named competitors or analogues with key differentiators noted
16. **Future Expansion Ideas** — 3-5 next-level directions the idea could grow toward
17. **Risk Assessment** — top 3 risks with likelihood and mitigation
18. **Long-Term Strategic Value** — what this becomes if it works at scale

For Quick Assess mode, return only sections 1-5.
For Score Only mode, return only the scoring table.
For Expand Only mode, return sections 6-16.
For Commercialize mode, return sections 1, 11, 12, 13, 17.

If the user requests Apple Notes delivery, add this post output step:

1. Build the final analysis first.
2. Use the title format `IdeaForge - YYYY-MM-DD - [short idea name]`.
3. Save the analysis to the requested Apple Notes folder.
4. If no folder name is supplied, ask for one or use `IdeaForge` if the user has already implied a default folder.
5. Preserve the full analysis body. Do not save only the score unless the user asked for Score Only mode.

Platform handling:

- macOS: write directly by running `scripts/save_to_apple_notes.py --folder "Ideas" --title "<title>" --body-file "<file>"` when the helper script is available.
- iOS: do not claim direct note creation from the skill itself. Instead, return a Shortcut ready payload or a clearly delimited note body that can be passed into Apple Notes by the calling app or Shortcut.
- Non Apple platforms: return the analysis in chat and state that Apple Notes delivery requires macOS or an iOS Shortcut handoff.

If the user requests Obsidian delivery, add this post output step:

1. Build the final analysis first.
2. Use the title format `IdeaForge - YYYY-MM-DD - [short idea name]`.
3. Save the analysis as Markdown in the `Ideas` folder of the target Obsidian vault.
4. If the vault path or vault name is not known, ask for it unless the user already established a default vault.
5. Preserve the full analysis body. Do not reduce it to a summary unless the user asked for that.

Obsidian platform handling:

- macOS: write directly to the vault folder by running `scripts/save_to_obsidian.py --vault-path "<vault path>" --folder "Ideas" --title "<title>" --body-file "<file>"` when the helper script is available, or use an Obsidian URL or Shortcut handoff if that is the established local path.
- iOS: do not claim raw filesystem access from the skill itself. Instead, return a Shortcut ready payload or Obsidian ready Markdown body and title for handoff into the `Ideas` folder.
- If the user only says "output to Obsidian" and gives no vault details, assume the destination folder name is `Ideas` but do not guess the vault name.

---

## Idea Library

Persisted analyses form a reusable library. The library is the set of `IdeaForge - YYYY-MM-DD - [name]` notes saved through the Apple Notes or Obsidian delivery steps; no separate database is needed.

- When the user references a past idea by name, ask for or load its saved analysis as the baseline instead of re-deriving it from scratch.
- When forging a new idea, mention an obviously related library entry if the user has referenced one this session; related ideas often share an MVP path.
- When a library note is provided, treat its scores and assumptions as the prior state for Revisit and Status modes.

## Compare Mode

For `idea compare [A] vs [B]`:

1. Run Stages 1, 2, and 4 on both ideas with the same conservative rules.
2. Present both score tables side by side in one combined table with a delta column.
3. Compare on the dimensions where they genuinely differ; note shared weaknesses once.
4. End with a verdict: which to build first and why, or whether they combine into one stronger idea.

## Revisit Mode

For `idea revisit [idea]`:

1. Load the prior analysis from the library, or ask the user to paste it if unavailable.
2. Re-run Stage 2 and Stage 4 explicitly accounting for what has changed in the AI, API, and hardware landscape since the prior date.
3. Output the new score table with a column showing prior score, new score, and what moved each changed metric.
4. State plainly whether the verdict band changed and what single factor matters most now.

## Status Mode

For `idea status [idea]`:

1. Take the previously forged idea and check what has changed: new competitors shipped, relevant APIs launched or died, costs dropped, the problem got solved elsewhere.
2. Verify current facts rather than answering from memory when the landscape question is checkable.
3. Output a short delta report: still open, partially closed, or overtaken, with the evidence for each claim.
4. Recommend forge again, build now, or archive.

## Principles

- **Do not inflate potential.** Score and expand honestly. An idea with a fatal flaw should have that flaw named clearly in Stage 2.
- **Do not fabricate market data.** If market size is unknown, say so. Use directional language: "likely a narrow market", "potentially large B2B opportunity".
- **Do not invent patent claims.** Only assert patent potential when there is a clear novel mechanism or process to describe.
- **Generate specific outputs.** "Consider APIs" is not useful. "Integrates with the Alpaca Markets API for paper trading" is.
- **Keep MVP scope honest.** A Phase 1 that requires three engineers and six months is not an MVP. Push toward the smallest thing that demonstrates value.
- **Keep platform claims honest.** Apple Notes write back is native on macOS when the runtime has local automation access. On iOS it requires a Shortcut or app level handoff.
- **Keep vault assumptions honest.** Obsidian folder name can default to `Ideas` only when the user asked for that. Vault name or path still needs to be known or requested.

## Operational Constraints

- If the helper scripts under `scripts/` are available, use them for direct macOS Apple Notes or Obsidian saves instead of describing a save abstractly.
- If `scoring-model.md` cannot be read, use the weights and scales documented inline in Stage 4 and note that the file was unavailable.
- If `evaluation-framework.md` cannot be read, continue using the inline criteria in Stages 2-3.
- If `output-template.md` cannot be read, use the section list in Stage 5 directly.
- Accept messy, incomplete, or poorly articulated input. Part of the value is finding the idea inside the noise.

## Help And Examples

If the user is not sure how to use this skill, asks what it needs, or asks for examples:

- Explain in plain language what this skill can do.
- Tell the user the minimum input needed for a useful first pass.
- Show the example prompts below.
- Offer the fastest next prompt the user can send.

Minimum useful input:

- A raw idea, product concept, or problem statement.

Example prompts:

- `Use idea-forge to evaluate this automation idea and score whether it is worth building.`
- `Run this raw product concept through the full idea-forge pipeline and give me the MVP path.`
- `Show me a sample prompt for using this skill when I only have a rough idea paragraph.`

