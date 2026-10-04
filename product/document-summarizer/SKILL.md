---
name: document-summarizer
description: Extract and condense key information from any document or text while preserving critical details. Use when you need to summarize PRDs, specifications, technical documents, articles, reports, emails, or any text that needs a condensed, structured overview. Produces output in sections with bullet points, intelligently combining extracted quotes with rewritten insights. Always use this skill whenever the user asks to "summarize", "condense", "brief", "extract key points", "make a summary", "create an overview", "reduce this", or provides a document/text saying "please summarize this" — even if they mention it informally.
metadata:
  author: Ronnasayd Machado - github.com/Ronnasayd
  version: "1.0.0"
---

# Document Summarizer

## When to use this skill

Use this skill when you need to:

- **Condense lengthy documents** while maintaining critical details (dates, numbers, names, decisions)
- **Extract key concepts** from technical specs, PRDs, reports, research papers
- **Create executive summaries** of emails, meeting notes, or project documentation
- **Prepare briefings** that highlight what matters most
- **Generate structured overviews** for quick understanding and reference

The summarizer works with ANY text type: Product Requirements, Technical Specifications, Articles, Reports, Meeting Notes, Research Papers, Emails, Code Documentation, etc.

## How the summarizer works

The summarizer uses a **hybrid approach**:

1. **Identify the document type and intent** — What kind of document is this? (PRD, technical spec, article, etc.)
2. **Extract critical information** — Pull essential facts: dates, decisions, key entities, metrics, specific requirements
3. **Distill to key themes** — What are the 3-5 essential concepts or sections?
4. **Rewrite for clarity** — Combine extracts with natural language, keeping it concise and coherent
5. **Structure as sections** — Organize into logical sections with bullet points for scannability

## Output format

ALWAYS use this exact structure for your summary:

```
# Summary: [Document Title or Topic]

## Overview
[1-2 sentence executive summary capturing the core purpose/essence]

## Key Sections

### [Section Name]
- **Point 1**: High-level extracted insight
- **Point 2**: Essential detail or decision
- **Point 3**: Another critical fact

### [Section Name]
- [bullet points]

## Critical Information
- **Dates/Deadlines**: [if relevant]
- **Key Metrics**: [if relevant]
- **Decision/Outcome**: [core decision or result]
- **Next Steps/Recommendations**: [if applicable]

## Notes
[Any important caveats, assumptions, or context that shouldn't be missed]
```

### Guidelines for sections and bullets

- **Section names** should reflect the document's natural structure (use its headings if present, invent logical ones if implicit)
- **Bullets should be scannable** — aim for 3-7 bullets per section, not more
- **Preserve specificity** — Keep exact names, numbers, dates, quotes where critical
- **Combine quotes with paraphrase** — Mix direct quotes ("verbatim") with plain English for readability
- **Critical Information section** is mandatory — Always highlight dates, decisions, and key metrics here if they exist

## Compression strategy

The amount of condensing depends on source length and density:

- **Short documents (< 500 words)**: Reduce to 40-50% of original (light summary)
- **Medium documents (500–3000 words)**: Reduce to 20-35% (moderate summary)
- **Long documents (> 3000 words)**: Reduce to 10-25% (aggressive summary)

**Exception**: If a section is ambiguous or dense, keep slightly MORE detail to preserve clarity.

## What NOT to lose

ALWAYS preserve:

- **Decisions and conclusions** — Never omit what was decided or concluded
- **Specific numbers, dates, names** — These are anchors for understanding
- **Constraints and blockers** — If something says "can't do X because of Y", keep it
- **Dependencies** — Relationships between concepts or tasks
- **Assumptions** — If there's an explicit "we assume...", include it

What's safe to condense or drop:

- Lengthy explanations or justifications (replace with concise paraphrase)
- Repeated statements (consolidate into one mention)
- Style/formatting commentary (only preserve content)
- Filler or wordy transitions

## Examples

### Example 1: Technical PRD

**Input**: 2500-word Product Requirements Document describing a new authentication system with 8 sections

**Output**:

```
# Summary: Multi-Factor Authentication System

## Overview
Build a flexible MFA system supporting SMS, TOTP, and hardware keys, launching in Q3 2026 with phased rollout to enterprises first.

## Requirements
- Support SMS (primary), TOTP (Google Authenticator, Authy), hardware keys (FIDO2)
- Integrate with existing IdP (Okta, Entra) via OIDC
- **Backward compatible** — existing users fall back to email verification if needed

## Architecture
- New `/auth/mfa` endpoint for MFA flow
- Redis cache for OTP validation (TTL: 5 mins)
- Audit logging to CloudWatch for compliance (HIPAA, SOC2)

## Rollout
- **Phase 1** (Week 1–4): Enterprise beta, SMS + TOTP
- **Phase 2** (Week 5–8): Hardware key support
- **Phase 3** (Week 9–12): Public GA

## Critical Information
- **Deadline**: Q3 2026 (June 30)
- **Team**: 4 engineers, 1 security reviewer
- **Blockers**: Okta API limits (need escalation)
- **Success metric**: 85% enterprise adoption by end of Phase 2
```

### Example 2: Email thread

**Input**: 15-message email chain about a product pivot

**Output**:

```
# Summary: Product Strategy Pivot Discussion

## Overview
Marketing recommends deprioritizing Feature X in favor of Feature Y based on customer feedback and competitive analysis. Decision pending exec sign-off.

## Why the Pivot
- Customer surveys show 70% prefer Feature Y over Feature X
- Competitor Z just launched similar Feature X; ours no longer differentiated
- Feature Y aligns with Q2 GTM strategy (cost optimization narrative)

## Proposal
- **Delay Feature X** to Q4 2026
- **Accelerate Feature Y** to late Q2
- **Restaff**: 3 engineers from X team → Y team

## Open Questions
- Existing commitments to enterprises expecting Feature X?
- Y's technical feasibility in compressed timeline?

## Decision
Awaiting CTO + CEO sign-off (likely by Friday).
```

## Tips for better summaries

1. **Read the whole document first** — Scan for structure BEFORE starting the summary. Identify natural sections.
2. **Ask yourself: Why would someone need this summary?** — That shapes what's critical.
3. **Keep signal-to-noise high** — Remove nice-to-knows unless they're surprising or urgent.
4. **Use section names from the source when possible** — This keeps context anchored.
5. **If something seems critical but unclear, mention it in Notes** — Don't suppress important ambiguity.

---

## Common usage patterns

**"Summarize this PRD for a quick read"**
→ Follow the output format exactly, aim for 20-30% of original

**"Extract just the key decisions from this"**
→ Focus the Critical Information section; minimize everything else

**"I'm new to this project, give me a briefing"**
→ Emphasize Overview and Critical Information; make it introduction-friendly

**"Condition this for exec presentation"**
→ Lead with a wow statement in Overview; emphasize metrics and decisions
