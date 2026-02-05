---
name: platform-mechanics
description: Convert verified algorithmic research into structured, machine-readable frameworks describing how social media platforms rank, reward, and penalize content. Provides factual, updatable platform rules for strategy agents (social-media, content, brand) to reference when developing or evaluating strategic decisions. Use this skill when needing to extract algorithmic mechanics from research, create posting playbooks, or validate content strategies against current platform rules.
---

# Platform Mechanics

## Overview

Transform algorithmic research into actionable, version-controlled platform mechanics frameworks. This skill extracts verified data from `/research/` and converts it into structured references (MECHANICS.md, SCHEMA.json, CHANGELOG.md) that enable strategy agents to make evidence-based decisions aligned with current platform realities.

**Primary outputs** saved to `/skills/platform-mechanics/{platform}/`:
- Machine-readable schemas for agent consumption
- Human-readable mechanics guides for strategists
- Historical changelogs for trend analysis

## When to Use This Skill

Trigger this skill when:
- "Reference the latest platform-mechanics/twitter skill to guide our content strategy"
- "Update platform-mechanics with newest algorithm research before campaign planning"
- "Generate a posting playbook using platform-mechanics/twitter"
- "Evaluate if our content plan aligns with current algorithmic priorities"
- "Check if link-heavy posts are penalized under latest mechanics"
- "Summarize how the X algorithm currently prioritizes content types"

**Do not use** for:
- Creating original research (use `research` skill instead)
- Developing brand strategy (use `brand-strategy` skill instead)
- General social media advice without platform-specific evidence

## Platform Mechanics Framework (PMF)

The PMF follows a five-phase extraction and normalization process:

### Phase 1: Extract

Pull verified data from completed research execution folders:

**Input sources:**
- `/research/{platform}-algorithm-updates/{YYYY-MM-DD}/RESEARCH.md`
- `/research/{platform}-algorithm-updates/{YYYY-MM-DD}/artifacts/citations.md`

**Extract these data types:**
1. **Engagement signals** - Actions that boost/lower content visibility (likes, replies, shares)
2. **Weight values** - Numerical importance of each signal (e.g., reply = +75 points)
3. **Content type preferences** - Video, image, text, poll performance
4. **Penalty factors** - What triggers algorithmic suppression
5. **Boost factors** - What triggers preferential treatment
6. **Account credibility signals** - Verification, age, follower ratio impacts
7. **Temporal factors** - Recency, posting time, response speed effects
8. **Feature updates** - New platform capabilities affecting reach
9. **Version metadata** - Research execution date, sources, confidence levels

### Phase 2: Normalize

Convert findings into consistent schema format:

```json
{
  "signal_name": {
    "type": "engagement|content|account|temporal",
    "impact": "positive|negative|neutral",
    "weight": <numerical_value>,
    "confidence": <0.0-1.0>,
    "evidence": ["citation_reference_1", "citation_reference_2"],
    "last_verified": "YYYY-MM-DD",
    "notes": "Additional context"
  }
}
```

**Confidence scoring:**
- 1.0: Official platform documentation
- 0.9: Platform leadership direct statements
- 0.7-0.8: Multiple independent expert analyses confirm
- 0.5-0.6: Single credible source
- <0.5: Informed speculation, flag as assumption

### Phase 3: Categorize

Organize normalized data into strategic categories:

**1. Content Type Performance**
- Video (watch time thresholds, priority level)
- Images/GIFs (engagement rates)
- Text-only (limitations, best practices)
- Polls/Interactive (participation signals)
- Links (penalty status, contextualization requirements)

**2. Engagement Signal Hierarchy**
- Primary signals (highest weight)
- Secondary signals (moderate weight)
- Tertiary signals (low weight but cumulative)

**3. Penalty Triggers**
- Content violations (offensive, spam, NSFW)
- Behavioral patterns (all-caps, excessive links)
- User signals (blocks, mutes, reports)
- Account reputation (ban history, authenticity)

**4. Boost Factors**
- Account credibility (verification, age)
- Historical performance (viral track record)
- Engagement velocity (rapid initial response)
- Content quality (dwell time, conversation depth)

**5. Temporal Dynamics**
- Posting time optimization
- Response speed windows
- Recency decay curves
- Trending topic windows

### Phase 4: Summarize

Generate human-readable MECHANICS.md with this structure:

```markdown
# {Platform} Platform Mechanics

**Version:** {version_number}
**Last Verified:** {YYYY-MM-DD}
**Source Research:** /research/{platform}-algorithm-updates/{YYYY-MM-DD}/

## Quick Reference

[1-2 paragraph executive summary of current mechanics state]

## Content Type Rankings

### 1. Video
- Priority: [High/Medium/Low]
- Key threshold: [e.g., 10+ second watch time]
- Weight: [numerical if available]
- Best practices: [bullet points]

[Continue for each content type...]

## Engagement Signal Hierarchy

| Signal | Weight | Impact | Confidence | Notes |
|--------|--------|--------|------------|-------|
| [signal] | [value] | [+/-] | [0-1.0] | [context] |

## Algorithmic Penalties

[Structured list with severity levels]

## Boost Factors

[Prioritized list with activation conditions]

## Posting Strategy Implications

[Tactical recommendations derived from mechanics]

## Recent Changes

[Highlight what changed since last version]

## Evidence Sources

[Link to research citations]
```

### Phase 5: Version

Save outputs with proper version control:

**Directory structure:**
```
/skills/platform-mechanics/
├── {platform}/
│   ├── MECHANICS.md          # Current version (human-readable)
│   ├── SCHEMA.json          # Current version (machine-readable)
│   ├── CHANGELOG.md         # Historical record
│   └── archive/
│       ├── v1-YYYY-MM-DD/
│       │   ├── MECHANICS.md
│       │   └── SCHEMA.json
│       └── v2-YYYY-MM-DD/
│           ├── MECHANICS.md
│           └── SCHEMA.json
```

**Versioning rules:**
- Increment version on major algorithmic changes
- Date-stamp each version with research execution date
- Archive previous version before updating
- Update CHANGELOG.md with summary of changes

## Workflow Decision Tree

```
Is there new algorithm research available?
├─ YES → Has research been verified and completed?
│   ├─ YES → Extract data using Phase 1
│   │   └─ Normalize data using Phase 2
│   │       └─ Categorize using Phase 3
│   │           └─ Generate MECHANICS.md using Phase 4
│   │               └─ Version and save using Phase 5
│   └─ NO → Wait for research completion
│
└─ NO → Use existing platform-mechanics/{platform}/ files
    └─ Reference MECHANICS.md for strategy decisions
```

## Platform-Specific Implementations

### Twitter/X

**Input:** `/research/x-algorithm-updates/{YYYY-MM-DD}/`
**Output:** `/skills/platform-mechanics/twitter/`

**Key mechanics to extract:**
- Feed types (For You, Following, Explore) and their algorithms
- Engagement weight table (reply, like, retweet values)
- Rich media preferences (video, image, GIF priorities)
- Link handling policies
- Verification/credibility impacts
- Grok AI customization features (if launched)
- RealGraph relationship modeling

**Schema extensions for Twitter:**
```json
{
  "feed_types": {
    "for_you": {...},
    "following": {...},
    "explore": {...}
  },
  "grok_features": {
    "conversational_customization": {...},
    "ai_evaluation": {...}
  }
}
```

### Adding New Platforms

To create mechanics for a new platform:

1. Complete research using `research` skill
2. Create `/skills/platform-mechanics/{platform-name}/` directory
3. Run PMF phases 1-5 using platform-specific research
4. Customize schema for platform-unique features
5. Document platform-specific extraction notes in MECHANICS.md

## Usage Examples

### Example 1: Update Twitter Mechanics from New Research

```
User: "We just completed X algorithm research for October 2025. Update the platform-mechanics skill."

Process:
1. Read /research/x-algorithm-updates/2025-10-25/RESEARCH.md
2. Extract engagement weights, penalties, boosts, content types
3. Normalize into schema format with confidence scores
4. Categorize by PMF categories
5. Generate updated MECHANICS.md
6. Archive previous version
7. Save new version with date 2025-10-25
8. Update CHANGELOG.md with key changes
```

### Example 2: Reference Mechanics for Strategy Validation

```
User: "Check if our Twitter content plan aligns with current algorithm priorities."

Process:
1. Read current /skills/platform-mechanics/twitter/MECHANICS.md
2. Review content plan against:
   - Content type rankings (video > images > text)
   - Engagement optimization (reply generation priority)
   - Penalty avoidance (link handling, all-caps)
   - Posting time recommendations
3. Flag misalignments
4. Suggest adjustments based on current mechanics
```

### Example 3: Generate Posting Playbook

```
User: "Create a Twitter posting playbook using platform-mechanics."

Process:
1. Read /skills/platform-mechanics/twitter/MECHANICS.md
2. Read /skills/platform-mechanics/twitter/SCHEMA.json
3. Generate playbook sections:
   - Optimal content types (prioritized list)
   - Posting frequency/timing (from temporal factors)
   - Engagement tactics (from signal hierarchy)
   - Penalty avoidance checklist
   - Account optimization (from credibility signals)
4. Include confidence levels and evidence sources
5. Add "last updated" date for shelf-life awareness
```

## Quality Standards

**Before finalizing platform mechanics:**

✅ **Evidence verification**
- Every claim linked to research citation
- Confidence scores assigned to all signals
- Contradictions flagged and explained
- Source recency within platform-specific window

✅ **Schema completeness**
- All signal types represented
- Weights included where available
- Impact direction clearly specified
- Evidence trail maintained

✅ **Usability**
- MECHANICS.md readable by non-technical strategists
- SCHEMA.json parseable by agents
- Examples included for complex mechanics
- Tactical implications clearly stated

✅ **Version control**
- Previous version archived
- CHANGELOG.md updated
- Version number incremented appropriately
- Research execution date stamped

## Integration with Other Skills

**With `research` skill:**
- Research produces `/research/{platform}-algorithm-updates/{date}/RESEARCH.md`
- Platform-mechanics extracts and structures that research
- Maintains bidirectional citations

**With `brand-strategy` skill:**
- Platform-mechanics provides factual constraints
- Brand-strategy references mechanics when developing tactical plans
- Strategy validates content recommendations against current mechanics

**With `social-media` workflow:**
- Content strategies reference platform-mechanics/{platform}/
- Campaign planning checks mechanics for optimization opportunities
- Performance analysis uses mechanics to diagnose reach issues

## Maintenance

**When to update platform mechanics:**
- New algorithm research completed (every 1-3 months typically)
- Major platform feature launches
- Significant performance pattern changes observed
- User requests updated mechanics

**Shelf-life awareness:**
- Algorithm mechanics become stale (platforms change constantly)
- Include "Last Verified" date prominently
- Recommend re-research intervals by platform volatility:
  - Twitter/X: 60-90 days (high volatility)
  - Instagram: 90-120 days (moderate)
  - LinkedIn: 120-180 days (lower volatility)

## Resources

### references/

`schema-template.json` - Base template for platform mechanic schemas with all standard fields and confidence scoring structure.

### workflows/

`extract-mechanics.md` - Detailed step-by-step workflow for executing the Platform Mechanics Framework on new research.

### twitter/

Platform-specific mechanics implementation for Twitter/X, including current MECHANICS.md, SCHEMA.json, and version history.

---

**Next steps after creating mechanics:**
1. Reference in strategy development
2. Share with content teams for tactical implementation
3. Schedule next research/update based on platform volatility
4. Monitor for performance changes indicating mechanics drift
