---
name: competitive-watch
description: Weekly competition scan. Detects if competitors have emerged that could invalidate the project. Run WEEKLY during development.
---

# COMPETITIVE WATCH — MARKET SENTINEL PROTOCOL

> **Frequency**: WEEKLY (minimum)
> **Purpose**: Detect competitive threats before they become problems
> **Action**: Early warning system for pivot decisions

---

## INVOCATION

```
/competitive-watch          # Full scan
/competitive-watch quick    # Quick news scan only
/competitive-watch deep     # Deep analysis mode
```

---

## COMPETITIVE THREAT LEVELS

```
🟢 GREEN  — No new competition, window open
🟡 YELLOW — New entrant detected, monitor closely
🟠 ORANGE — Funded competitor, accelerate timeline
🔴 RED    — Market saturated, consider pivot
```

---

## SCAN PROTOCOL

### 1. News & Announcements Scan

Search for recent news (past 7 days):

```
Queries to run:
- "slopsquatting detection" site:techcrunch.com OR site:venturebeat.com
- "AI hallucination package" security tool
- "supply chain security" AI new startup
- Socket + Snyk + Endor Labs announcements
- PyPI security new tool
```

### 2. Funding Announcements

Check for funding in adjacent space:

```
- Crunchbase: supply chain security funding
- TechCrunch: security startup funding
- LinkedIn: DevSecOps company announcements
```

### 3. Product Launches

Monitor for new products:

```
- ProductHunt: security category
- GitHub Trending: security + python
- HackerNews: security tools
```

### 4. Competitor Feature Updates

Check existing competitors:

```
- Socket.dev blog/changelog
- Snyk blog/releases
- Endor Labs announcements
- GitHub Advanced Security updates
```

---

## SCAN REPORT TEMPLATE

```markdown
# Competitive Scan — YYYY-MM-DD

## Threat Level: [GREEN | YELLOW | ORANGE | RED]

---

## Direct Competitors

### Slopsquatting-Specific Tools
| Name | Status | Funding | Threat |
|:-----|:-------|:--------|:-------|
| [None found] | - | - | - |

### Adjacent Tools (Supply Chain Security)
| Name | Recent Update | Slopsquatting Feature? |
|:-----|:--------------|:-----------------------|
| Socket | [date] | [Yes/No/Partial] |
| Snyk | [date] | [Yes/No/Partial] |
| Endor Labs | [date] | [Yes/No/Partial] |

---

## New Entrants This Week

| Name | Type | Funding | Threat Level |
|:-----|:-----|:--------|:-------------|
| [None] | - | - | - |

---

## News & Announcements

### Relevant Articles
1. [Title](URL) — [Summary]
2. [Title](URL) — [Summary]

### Funding News
- [None this week]

### Product Launches
- [None this week]

---

## Market Window Assessment

**Status**: OPEN / CLOSING / CLOSED

**Reasoning**:
[Analysis of market window]

**Time Remaining**: X months (estimate)

---

## Recommendations

### If GREEN:
- Continue current plan
- No acceleration needed

### If YELLOW:
- Increase scan frequency to 2x/week
- Accelerate MVP timeline if possible

### If ORANGE:
- Consider feature differentiation
- Accelerate to market immediately
- Focus on unique value proposition

### If RED:
- Evaluate pivot options
- Consider acquisition targets
- Reassess project viability

---

## Action Items

| Priority | Action | Deadline |
|:---------|:-------|:---------|
| [P0/P1/P2] | [Action] | [Date] |

---

## Next Scan

Date: [Next week date]
```

---

## THREAT DETECTION TRIGGERS

### YELLOW — Monitor

- New blog post about slopsquatting from major vendor
- GitHub repo with similar functionality appears
- Academic paper on detection methods
- Patent filing in space

### ORANGE — Accelerate

- Startup announces slopsquatting focus
- Any funding in slopsquatting space
- Major vendor (Snyk, Socket) mentions adding feature
- Copilot/Cursor announces protection

### RED — Pivot

- VC-funded startup with $5M+ launches
- GitHub/Microsoft adds native protection
- Snyk/Socket ships full solution
- Market coverage articles appear

---

## RESPONSE PROTOCOLS

### Green Response

```
Continue with current roadmap.
Focus on quality and differentiation.
Run weekly scans.
```

### Yellow Response

```
1. Document the new entrant
2. Analyze their approach
3. Identify differentiation opportunities
4. Continue development, no timeline change
5. Increase scan frequency
```

### Orange Response

```
1. Emergency assessment meeting
2. Cut non-essential features from MVP
3. Focus on fastest path to launch
4. Consider early launch with limited features
5. Prepare differentiation messaging
```

### Red Response

```
1. Stop current development
2. Full competitive analysis
3. Evaluate:
   - Can we differentiate enough?
   - Is there an adjacent niche?
   - Should we pivot entirely?
4. Decision within 48 hours
5. Either: Pivot, Partner, or Exit
```

---

## HISTORICAL SCANS

Record all scans for pattern detection:

```markdown
# .fortress/reports/competitive/SCAN_LOG.md

| Date | Threat Level | Key Finding | Action Taken |
|:-----|:-------------|:------------|:-------------|
| 2025-12-23 | GREEN | No new entrants | Continue |
| ... | ... | ... | ... |
```

---

## DIFFERENTIATION MATRIX

Track what makes Phantom Guard unique:

```markdown
## DIFFERENTIATION MATRIX

| Feature | Phantom Guard | Socket | Snyk | Endor |
|:--------|:--------------|:-------|:-----|:------|
| Hallucination patterns | ✅ Core focus | ❌ | ❌ | ❌ |
| Real-time detection | ✅ | ✅ | ❌ | ❌ |
| pip hook | ✅ | ✅ | ❌ | ❌ |
| OSS core | ✅ | ❌ | ❌ | ❌ |
| AI-focused | ✅ | Partial | ❌ | ✅ |
| Pattern database | ✅ Specialized | ❌ | ❌ | ❌ |
```

---

*Competitive Watch: Because surprise is the enemy of strategy.*
