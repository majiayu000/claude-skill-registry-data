---
name: blog-research
description: Research legal technology topics for blog posts on alt-counsel (Ang Hou Fu's blog). Use when the user asks to research topics, find sources, fact-check claims, gather statistics, or find expert opinions for blog content. Prioritizes Singapore/ASEAN perspectives and flags US/EU-centric information. Outputs research findings to research.md in the post folder with proper citations.
---

# Blog Research Skill

Research legal technology topics for alt-counsel blog posts with Singapore/ASEAN prioritization and jurisdictional awareness.

## When to Use This Skill

Trigger this skill when the user requests:
- "Research [topic] for my blog post"
- "Find sources on [legal tech topic]"
- "Fact-check: [claim]"
- "Get statistics on [topic]"
- "Find expert opinions on [subject]"
- Any research task related to blog content creation

## Research Workflow

### Step 0: Verify Research Readiness

Before beginning research, confirm the post has:

**Required inputs:**
- [ ] **Locked thesis** - One-sentence argument the post will make
- [ ] **Section outline** - 3-5 main sections with their specific claims
- [ ] **Evidence gaps** - Specific claims that need external validation

**Stop and ask user if missing:**
- "I see you want research on [topic], but I don't have your post outline yet."
- "Which specific claims in your post need evidence?"
- "What are you trying to prove with this research?"

**Why this matters:** Research without structure leads to gathering interesting information that doesn't make the final cut. Lock the argument first, research second.

### Step 1: Understand the Research Need

**Critical question:** What needs external validation vs what's personal experience?

Ask user to categorize each post section:
- **Personal experience** (✍️) - No research needed, this is your story
- **Needs validation** (🔍) - Your claim needs external support
- **Needs context** (🌍) - Your experience needs broader context

**Example:**
- Section 2: "My 3-page prompt experience" = ✍️ (don't research this)
- Section 3: "Agents changed in Sept 2025" = 🔍 (needs validation)
- Section 4: "Singapore firms struggling too" = 🌍 (needs regional context)

Only research the 🔍 and 🌍 sections.

If the post folder is ambiguous, ask the user to specify (e.g., `posts/contract-automation-tools/`).

### Step 2: Read Reference Files

Before conducting research, read:
1. **references/trusted-sources.md** - Know which sources to prioritize
2. **references/regional-considerations.md** - Understand Singapore/ASEAN vs US/EU differences

These files provide critical context for effective research.


### Step 2.5: Generate Research Brief for Approval

Before conducting searches, output a research brief:
```markdown
# Research Brief: [Post Title]

**Locked thesis:** [One sentence]

**Evidence needed:**
1. Section X: [Specific claim] 
   - Searching for: [What evidence would support this]
   - Stop criteria: [When I have enough]
   
2. Section Y: [Specific claim]
   - Searching for: [Evidence needed]
   - Stop criteria: [When sufficient]

**Not researching:**
- Section Z: Personal experience (no validation needed)

**Estimated searches:** [Number based on sections]
**Stop when:** All sections adequately supported OR regional sources exhausted
```

**Ask user:** "Does this match what you need? Or should I adjust before starting searches?"
```

This creates the checkpoint you're currently missing.

## Integration with Your Workflow

Based on your process patterns, here's how the improved skill would work:

### Current Problem (AI Tools Post):
```
Session 1: Broad research on MCP, CLI patterns, everything
Session 2: More research on security, failures, Singapore (exploratory)
Session 6: Cut 2/3 of research as redundant/not fitting

= 3 sessions, high waste
```

### With Improved Skill:
```
Session 1: 
- User: "I want to research for AI tools post"
- Skill: "What's your locked outline? Which sections need evidence?"
- User: Provides 3 sections that need validation
- Skill: Generates research brief targeting those 3 specific claims
- User: Approves brief
- Skill: Executes focused research (6-9 searches, not 20+)
- Output: Evidence mapped directly to 3 sections

= 1 session, minimal waste

### Step 3: Conduct Research

Use web_search following this priority order:

**Search Strategy:**
1. **Singapore/ASEAN-first search** - Add "Singapore" or "ASEAN" qualifiers to queries
2. **Evaluate regional results** - Check if findings are regionally relevant
3. **Expand to global sources** - If regional sources insufficient, search without geographic qualifiers
4. **Flag jurisdictional concerns** - Note when findings are US/EU-centric

**Search Tactics:**
- Start with 3-5 searches minimum (regional → global)
- Use web_fetch to read full articles from promising results
- Extract specific data points, quotes, and citations
- Cross-reference information across multiple sources

**Search Depth (Evidence-Driven):**
- **Per section claim:** 2-3 searches minimum
  - Stop when: Claim is supported by 2+ credible sources OR you've exhausted regional sources
  
- **Total research session:** Based on outline
  - 3 sections with specific claims = 6-9 searches
  - Stop when: All sections have adequate evidence OR regional sources exhausted
  
**Red flag:** If doing 10+ searches and outline still has evidence gaps, the problem is likely the outline (claims too broad/unsupported), not insufficient research.

### Step 4: Evaluate Sources

Apply source evaluation criteria from references/trusted-sources.md:

1. **Recency** - Prefer sources from last 6-24 months for trends/pricing
2. **Regional relevance** - Singapore/ASEAN > Global > US/EU-specific
3. **Credibility** - Established publications > vendor blogs
4. **Specificity** - Actual data/examples > general claims
5. **Independence** - Journalism > vendor marketing

### Step 5: Apply Regional Lens

For EVERY finding, assess:
- Is this Singapore/ASEAN-relevant?
- Is this US/EU-centric? If so, what differs locally?
- What's the alt-counsel angle (resource-constrained perspective)?

Flag jurisdictional concerns using the protocol from references/regional-considerations.md.

### Step 6: Map Findings to Post Structure

For EACH section in the user's outline, identify:
- **Section X claim:** [The specific point this section makes]
- **Evidence needed:** [What this claim requires for support]
- **Findings that support:** [Which research findings apply here]
- **Findings that don't fit:** [Interesting but not relevant to this section]

**Red flag if:** You have 5+ findings that don't map to any section.
**Action:** Ask user: "I found [X], but it doesn't support your outlined sections. Should I continue researching or is this exploratory?"

**Quality check:** Every finding should answer "Which section needs this?"

### Step 7: Format Research Output

Load assets/research-template.md and populate it with findings:

**Required sections:**
- **Summary** - 2-3 sentence executive summary
- **Key Findings** - Detailed findings with sources and regional context icons
- **Statistics & Data Points** - Specific data with citations
- **Expert Quotes** - Direct quotes from credible sources
- **Jurisdictional Flags** - US/EU-centric content flagged with explanations
- **Alt-Counsel Angle** - How findings relate to blog's resource-conscious mission
- **Additional Sources** - Links for follow-up research

**Citation format:**
- **Source:** [Article Title](URL) - [Publication]
- **Date:** [Publication date]
- **Regional Context:** ✅ Singapore/ASEAN | ⚠️ US/EU-centric | 🌍 Global

### Step 8: Save Research Output

Create research.md in the specified post folder:
- **Path format:** `posts/[post-folder-name]/research.md`
- **Always confirm** the post folder path with the user if ambiguous

## Regional Prioritization Rules

**Always prioritize:**
1. Straits Times, Channel News Asia for Singapore news
2. Artificial Lawyer for global legal tech (but flag when US/EU-centric)
3. Singapore government sources (Courts, Legal Service, IMDA)
4. ASEAN business and legal publications

**Always flag when:**
- Information is US/EU-specific (ethics rules, regulations, market dynamics)
- Pricing assumes enterprise budgets
- Solutions require infrastructure uncommon in ASEAN
- No Singapore/ASEAN-specific information available

## Quality Standards

**Good research includes:**
- Minimum 5-8 quality sources cited
- Mix of regional and global perspectives
- Specific statistics with dates
- Expert quotes from credible sources
- Clear jurisdictional flags where relevant
- Alt-counsel angle articulated

**Bad research avoids:**
- Vendor marketing without independent validation
- Outdated sources (>2 years old for trends)
- Pure US content without regional context
- Vague claims without specific examples
- Missing citations or broken links

## Example Research Queries

**Fact-check query:**
> "Fact-check: Contract lifecycle management systems typically cost $50K+ for enterprises"

*Workflow:* Search for CLM pricing, gather data points from multiple sources, note regional pricing if available, flag if US-centric pricing, provide alt-counsel perspective on accessible alternatives.

**Topic research query:**
> "Research AI document review tools for small legal teams"

*Workflow:* Search for AI document review tools, prioritize solutions for small teams, compare pricing tiers, find Singapore/ASEAN adoption examples, flag enterprise-only solutions, identify practical alternatives.

**Statistics query:**
> "Get statistics on legal tech adoption in Singapore law firms"

*Workflow:* Search Singapore-specific legal tech adoption data, check Law Society publications, look for regional surveys, note data gaps, compare to global trends where relevant.

## Bundled Resources

### References
- **trusted-sources.md** - Curated list of reliable legal tech sources
- **regional-considerations.md** - Singapore/ASEAN vs US/EU differences guide

### Assets
- **research-template.md** - Standard format for research.md output
