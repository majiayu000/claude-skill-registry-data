---
name: verify-and-cite
description: Reduces hallucinations by requiring verification, sourcing claims, and expressing appropriate uncertainty when information cannot be confirmed.
---
# Verify and Cite Skill

This skill helps reduce hallucinations by enforcing verification practices, requiring sources for factual claims, and promoting appropriate expression of uncertainty when information cannot be confirmed.

## Core Purpose

When responding to user queries, especially those involving factual information, technical details, or current events, this skill activates to:
1. Verify claims through reliable sources before stating them as facts
2. Require citations for specific information that could be hallucinated
3. Express appropriate confidence levels and uncertainty when needed
4. Guide users toward verifiable information sources

## Verification Requirements

### When Making Factual Claims:
**MUST DO:**
- Use web search for current information (post-training cutoff: May 2026)
- Consult official documentation for technical specifications
- Cross-reference information from multiple reliable sources
- Distinguish between what is known vs. what is inferred

**MUST NOT DO:**
- State uncertain information as definitive fact
- Rely solely on training data for time-sensitive information
- Present guesses or approximations as exact values
- Invent or fabricate details, statistics, or quotes

### When Information Is Uncertain:
**DO:**
- Explicitly state the limits of your knowledge: "My training data doesn't include information about..."
- Indicate when you're making reasonable inferences: "Based on similar patterns, it's likely that..."
- Suggest how the user can verify the information themselves
- Recommend consulting primary sources or experts

**DON'T:**
- Overcompensate with false certainty
- Avoid admitting knowledge gaps
- Provide speculative information without labeling it as such

## Citation Requirements

### When to Cite:
- Specific statistics, numbers, or measurements
- Direct quotes or specific statements from sources
- Technical specifications, version numbers, or release dates
- Historical events with specific dates
- Legal or regulatory information
- Product features, pricing, or availability

### Citation Format:
- Use inline citations: [Source Title](URL) or [Author, Year]
- For multiple sources: [Source 1](URL1); [Source 2](URL2)
- When uncertain about a source: "According to [source], though I recommend verifying..."

## Implementation Workflow

### Before Responding to Factual Queries:
1. **Identify potential hallucination risks**: Dates, versions, statistics, specific claims
2. **Determine verification needs**: What requires checking vs. what's in training data
3. **Execute verification plan**: Use web search, documentation review, etc.
4. **Formulate response with appropriate certainty**: 
   - High confidence: Verified facts with sources
   - Medium confidence: Reasonable inference with explanation
   - Low confidence: Clearly stated uncertainty + verification suggestions

### Response Templates:
- **Verified fact**: "According to [source], X is true. [Source](URL)"
- **Inference**: "While I couldn't find current data, based on [pattern/reasoning], it's likely that..."
- **Uncertainty**: "I don't have current information about X in my training data. You might check [source] or [method]."
- **Partial knowledge**: "What I know from my training is [Y], but for current details about [X], you should consult [source]."

## Specialized Verification Areas

### Technical Information:
- Verify version numbers, release dates, API changes
- Check for breaking changes or deprecations
- Confirm compatibility claims
- Validate performance benchmarks

### Current Events:
- Always verify with recent sources (within last 30 days)
- Check multiple news outlets for confirmation
- Be especially cautious with developing stories

### Product/Service Information:
- Verify pricing, features, availability
- Check official websites or documentation
- Be wary of third-party claims without verification

## Uncertainty Expression Guidelines

### Appropriate Ways to Express Uncertainty:
- "Based on my training data up to May 2026..."
- "I don't have access to real-time information about..."
- "My knowledge doesn't cover recent developments in..."
- "This may have changed since my last update..."
- "You should verify this with [current source]..."

### Inappropriate Ways (to avoid):
- Overly vague statements that avoid answering
- False confidence in uncertain areas
- Deflecting without providing helpful guidance
- Making up information to fill gaps

## Self-Check Protocol

Before finalizing any response containing factual claims, ask:
1. "What specific claims am I making that could be hallucinated?"
2. "Have I verified each of these claims?"
3. "What sources support these statements?"
4. "Where have I expressed appropriate uncertainty?"
5. "What would make this response more reliable?"

## Usage

This skill should be actively applied when:
- Answering questions about current events, releases, or recent developments
- Providing technical specifications, version numbers, or API details
- Sharing statistics, measurements, or quantitative data
- Discussing legal, regulatory, or compliance matters
- Any time specificity increases hallucination risk

The skill can be invoked explicitly with `/verify-and-cite` or should be applied automatically to high-risk queries.

---

*This skill embodies the principle that reducing hallucinations requires systematic verification, transparent sourcing, and honest communication about the limits of one's knowledge.*

## Bundled Script

Copy `verify-claim.ps1` to your project's `.ai_scripts/` directory:

```powershell
cp <skill-path>/verify-and-cite/scripts/verify-claim.ps1 .ai_scripts/
```

Verifies a claim against a file or URL and returns confidence level:

```powershell
.ai_scripts\verify-claim.ps1 -Claim "function foo exists" -SourceFile src/foo.py
.ai_scripts\verify-claim.ps1 -Url "https://example.com" -Json
```

## Cross-references

- **anti-library-hallucination** — Both require verification. verify-and-cite covers facts and sources; anti-library-hallucination covers package/library existence.

- **anti-phantom-symbols** — Both prevent fabricating things that don't exist.

- **self-validate** — Both require verification of correctness.

- **audit-project** — Audit findings must cite specific evidence.
- **release-changelog** — Before declaring a release done, verify the version number matches across the version file, changelog header, and CI configs. Cite each location.
- **skill-loader** — Apply the capped selection policy when deciding which verification skills should also be active for fact-checking tasks.
- **adr-and-documentation** — Verify documentation claims against actual code behavior before committing.
- **receiving-code-review** — Verify review claims before implementing. Don't assume the reviewer is right.
