---
name: producing-ai-newsletter
description: >
  Operates a multi-configuration AI newsletter production system with shared workflow
  engine (research, draft, edit, format, deliver) and switchable brand profiles.
  Ships with Loxihart configuration (3-tier audience, Teams and SharePoint delivery,
  continuity tracking) and FlashFusion configuration (single-tier creator-tech audience,
  Substack and email delivery). Activates when the user mentions newsletter, weekly
  briefing, The Prompt, AI brief, edition drafting, research brief, newsletter research,
  tier content, continuity log, FlashFusion newsletter, or any reference to newsletter
  production. Also triggers on research week, draft week, draft edition, continuity
  update, format for email or docx, editorial plan, or newsletter status checks.
version: "2.0.0"
---

# Producing AI Newsletters

Brand-agnostic newsletter production system with a shared workflow engine and switchable configurations. Declare your mode at session start — the engine adapts research depth, audience profiles, and delivery formats automatically.

## Quick-Start Decision Tree

```
Which newsletter?
  ├─ "Loxihart" / "The Prompt" ────── MODE: Loxihart (3 tiers, Teams + SharePoint + .docx)
  ├─ "FlashFusion" ────────────── MODE: FLASHFUSION (1 tier, Substack + email)
  ├─ Neither specified ─────────── Ask: "Which newsletter? Loxihart or FlashFusion?"
  └─ Custom ────────────────────── Use the workflow engine with custom audience profile
```

**To set mode:** Say "Loxihart mode" or "FlashFusion mode" at session start. Mode persists for the session.

---

## Usage Examples

**Example 1 — Loxihart full production run**
User: "Loxihart mode. Research week 24, then draft all three tiers."
→ Set MODE: Loxihart. Run research workflow: scan AI news sources, score for relevance to each tier, produce structured research brief. Then draft Non-Tech, Tech Dept, and AI Team editions from the brief. Quality check all three. Format for Teams markdown.

**Example 2 — FlashFusion weekly issue**
User: "FlashFusion mode. Draft this week's newsletter on Claude Code updates."
→ Set MODE: FLASHFUSION. Research the topic with creator-tech lens. Draft single-tier issue with technical depth layering. Format for Substack. Include the AI tools roundup section.

**Example 3 — Continuity update (Loxihart)**
User: "Continuity update for week 24."
→ Load previous edition summaries. Generate "Last Week We Said" callbacks. Update running story threads. Produce continuity log for reference during drafting.

---

## Shared Workflow Engine

Both configurations use the same 5-stage pipeline. Only the audience profiles and delivery formats change.

### Stage 1 — Research
Scan AI news sources for the target week. Score each story for relevance. Produce a structured research brief with source URLs, confidence ratings, and tier routing (Loxihart) or depth tagging (FlashFusion).

**Source requirements:** Every claim needs a source URL. No exceptions. Flag unverified claims as `[UNVERIFIED — needs source]`. Never fabricate URLs.

### Stage 2 — Draft
Generate edition content from the research brief. Apply audience profile (tone, depth, length, action items). Include all required sections per the configuration's template.

### Stage 3 — Edit
Self-check against quality gates. Verify word count, section completeness, source attribution, and no placeholder text. Flag anything uncertain for human review.

### Stage 4 — Format
Convert draft to the configuration's delivery format(s): HTML email, .docx, Teams markdown, Substack, or SharePoint. Apply brand colors and layout.

### Stage 5 — Deliver
Present the formatted output with: reading time estimate, quality gate results, items flagged for review, and delivery instructions.

---

## Command Router

| Trigger | Action |
|---------|--------|
| `research week [N]` | Run research sweep, produce structured brief |
| `draft week [N]` | Draft all editions from research brief |
| `draft [edition-name]` | Draft single edition |
| `continuity update` | Generate/review continuity log (Loxihart only) |
| `format [type]` | Convert draft to specific delivery format |
| `special edition [topic]` | Draft breaking/event edition |
| `editorial plan` | Review/update content calendar |
| `quality check` | Audit a draft against quality scorecard |

If ambiguous, ask: "Which mode? Research, draft, continuity, or something else?"

---

## Configuration: Loxihart ("The Prompt")

**Newsletter identity:** The Prompt by Loxihart. Tagline: "Your weekly AI intelligence brief." Visual signature: `> THE PROMPT█` (terminal cursor aesthetic). Brand colors: Orange #E2690E, Light Blue #5391AA, Dark Blue #00405F.

**Delivery:** Teams markdown, SharePoint, .docx, HTML email.

**Continuity system:** "Last Week We Said..." callbacks, running story threads, client talking point consistency. See the continuity workflow reference.

### Three Independent Audiences

**Tier 1 — Non-Tech Edition**
Audience: All employees + leadership. They read for: "What changed? Should I be worried? What do I tell clients?" Tone: confident, clear, zero jargon. Length: weekly ~500 words, monthly ~1200 words. Content filter: only stories affecting business, client conversations, or market position. Action items: what to say when clients ask.

**Tier 2 — Tech Department Edition**
Audience: Service desk, engineers, infrastructure staff. They read for: "What tools changed? What should we test?" Tone: technical, practical, implementation-focused. Length: weekly ~800 words, monthly ~2000 words. Content filter: API changes, tool updates, benchmarks, deprecation notices, security advisories.

**Tier 3 — AI Team Edition**
Audience: AI delivery and consulting team. They read for: strategic implications, positioning changes, architecture patterns. Tone: full analyst depth. Length: weekly ~1200 words, monthly ~3000 words. Content filter: everything — competitive intel, vendor strategy, pricing, regulatory, open-source disruption.

### Content Routing Matrix (Loxihart)

| Story Type | Non-Tech | Tech Dept | AI Team |
|------------|----------|-----------|---------|
| Major model release | Business impact only | Benchmarks + API | Full competitive analysis |
| API deprecation | Skip | Migration guide | + client impact |
| Enterprise partnership | What it means | Skip | Competitive positioning |
| Security vulnerability | "Are we affected?" | Technical advisory | + vendor response eval |
| MCP/integration update | Skip | What to test | + architecture pattern |
| Pricing change | Budget impact | Cost comparison | + vendor strategy read |
| Regulatory update | Plain English | Implementation reqs | + client advisory draft |

### Anti-Generic Enforcement (Loxihart)

Every deliverable must reference the organization's specific context — tools, service lines, client verticals, positioning. Content that could run unchanged in any company's newsletter is rejected.

See the Loxihart Configuration reference for full template structures, hidden gem features spec, and brand guide.

---

## Configuration: FlashFusion

**Newsletter identity:** FlashFusion newsletter. Creator-tech focused. Dark-mode primary aesthetic.

**Delivery:** Substack (primary), email.

**Audience:** Single-tier but depth-layered. Target: creators, developers, and AI power users who want actionable tool intelligence without enterprise fluff.

### Content Structure (FlashFusion)

**They read for:** "What AI tools should I try this week? What workflows are people using? What's worth the subscription vs. free tier?"

**Tone:** Opinionated, practical, first-person-knowledgeable. Like getting a recommendation from someone who actually uses these tools daily, not a press release roundup.

**Sections per issue:**
1. **Lead story** — One deep-dive on a tool, workflow, or trend (400–600 words)
2. **Quick hits** — 3–5 tool updates or releases, 2–3 sentences each
3. **Workflow of the week** — Step-by-step automation or prompt chain (practical, reproducible)
4. **Free tier spotlight** — One free tool or feature that punches above its weight
5. **What I'm building** — Personal project update or experiment result

**Length:** 800–1200 words per issue. Reading time: 4–6 minutes.

**Content filter:** AI tools (Claude, ChatGPT, Midjourney, Cursor, v0, etc.), personal productivity, creator-tech trends, prompt engineering, automation (n8n, Zapier, Make). No enterprise procurement, no analyst-style market sizing, no compliance deep-dives.

See the FlashFusion Configuration reference for Substack formatting, section templates, and depth-layering guidelines.

---

## Quality Gates (Both Configurations)

**Automated self-check before output:**
- [ ] Word count within range for edition type
- [ ] All required sections present
- [ ] No placeholder text (`[TODO]`, `[TBD]`, `[INSERT]`)
- [ ] Source URL for every factual claim
- [ ] Reading time estimate included
- [ ] Correct newsletter name in header (not a generic title)

**Flag for human review:**
- [ ] Any claim that cannot be verified from search results
- [ ] Deliverables referencing specific tools or processes
- [ ] Content where framing could be controversial
- [ ] Anything marked `[UNVERIFIED]`

---

## Edge Cases

**Mode not declared:** Ask before proceeding. Never assume Loxihart or FlashFusion — they have different audiences, tones, and delivery formats.

**Cross-pollination:** A story may appear in both newsletters but with different framing. Loxihart Tier 3 might analyze a tool strategically while FlashFusion covers how to actually use it. Never copy content between modes.

**Special edition:** Both configurations support event-driven special editions. Use the same workflow engine but compress the research stage (focus on single topic rather than weekly scan).

---

## Self-Verification Checklist

Before delivering any newsletter output:
1. Mode is declared (Loxihart or FlashFusion)
2. Research brief has source URLs for all claims
3. Draft matches audience profile (tone, depth, length, action items)
4. All required sections present per configuration template
5. Quality gates passed
6. Items flagged for human review are clearly marked
7. Formatted for correct delivery channel
8. No content mixing between configurations

---

## CLAIMS
- The shared workflow engine (research, draft, edit, format, deliver) covers all newsletter production regardless of brand or audience
- Three-tier audience segmentation (Loxihart) produces meaningfully different content per tier, not just rewrites at different reading levels

## COUNTEREXAMPLE
- A weekly newsletter with no continuity tracking (Loxihart's "Last Week We Said" system) loses the trust-building effect of running story threads over months
- FlashFusion's single-tier model works only because the audience is homogeneous — a broader audience would need tier segmentation

## CONTRADICTIONS
- "Anti-generic enforcement" (Loxihart) requires company-specific context, but this makes the skill's template less reusable for other organizations
- "Never copy between modes" creates duplication when the same story is genuinely relevant to both audiences
