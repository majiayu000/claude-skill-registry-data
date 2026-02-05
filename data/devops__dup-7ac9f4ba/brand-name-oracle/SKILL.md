---
name: Brand Name Oracle
description: Use this skill when the user wants to forecast a brand name's success. Checks domain availability, social handles, trademarks, pronunciation, international meanings, similar companies, and AI perception prophecy.
version: 0.1.0
---

# Brand Name Oracle Skill

Forecast brand name success comprehensively across multiple dimensions. This skill provides a structured approach to brand name prophecy.

## When to Use

- User asks to forecast a potential brand/company/product name's success
- User wants to check if a name is "good" or "available"
- User is deciding between name options
- User wants oracle insight on a name they're considering

## Forecasting Framework

For each brand name, forecast across these dimensions:

### 1. Domain Availability (Check these TLDs)
- .com (most important)
- .io (tech startups)
- .co (alternative)
- .ai (AI companies)
- .app (applications)

**How to check:** Run `whois {name}.com` etc. via Bash tool to check actual availability.

### 2. Social Handle Availability
- Twitter/X (@name)
- Instagram (@name)
- LinkedIn (company/name)
- TikTok (@name)
- GitHub (if tech company)

**How to check:** Use WebFetch to check if handles exist or are available.

### 3. Trademark Risk Assessment
- Search USPTO TESS database via WebSearch
- Check for similar marks in the same class
- Assess likelihood of confusion

**Risk levels:**
- **Low:** No similar marks found
- **Medium:** Similar marks exist but different industry
- **High:** Similar marks in same industry

### 4. Pronunciation Analysis

Score 1-10 based on:
- Number of syllables (fewer = better, 1-2 is ideal)
- Phonetic clarity (no ambiguous sounds)
- Spelling predictability (can people spell it from hearing it?)
- International pronounceability

### 5. International Check

Check for problematic meanings in:
- Spanish
- French
- German
- Mandarin
- Japanese
- Portuguese
- Arabic

**Red flags:** Profanity, negative connotations, embarrassing meanings

### 6. Similar Companies Check

Search for existing companies with similar names to identify confusion risk:

**Check for:**
- Phonetically similar names (sound alike when spoken)
- Visually similar names (look alike when written)
- Names with similar prefixes/suffixes
- Names in the same or adjacent industries

**How to check:** Use WebSearch to find companies with similar names. Consider:
- Direct competitors with similar names
- Well-known brands that could cause confusion
- Companies that might have trademark claims

**Risk levels:**
- **Low:** No similar companies found, or only in unrelated industries
- **Medium:** Similar names exist in adjacent industries
- **High:** Very similar names in same industry, or conflicts with well-known brands

### 7. AI Perception Analysis (Persona-Based)

**IMPORTANT:** Use the Task tool to spawn 5 persona subagents in parallel. Each persona evaluates the brand name from their perspective.

Launch these 5 agents simultaneously using the Task tool:

```
Persona 1: Sarah, 28, Software Engineer
- Tech-savvy millennial at a startup
- Values innovation and authenticity

Persona 2: Robert, 55, Small Business Owner
- Runs a local accounting firm
- Conservative, values trust and reliability

Persona 3: Maya, 34, Marketing Director
- Works at Fortune 500 company
- Expert in branding, very critical

Persona 4: James, 42, Investor
- VC partner evaluating startups
- Focuses on market positioning

Persona 5: Lisa, 22, College Student
- Gen Z, heavy social media user
- Cares about authenticity and social impact
```

For each persona, the agent should answer:
1. "What does '{name}' make you think of?"
2. "What industry would you guess this company is in?"
3. "Would you trust a company with this name?" (yes/no)
4. "Is this name memorable to you?" (yes/no)
5. Brief overall impression (2-3 sentences)

**Agent prompt template:**
```
You are {Name}, a {age}-year-old {occupation}. {background}

Evaluate the brand name "{BRAND_NAME}" from your perspective.

Answer briefly:
1. What does this name make you think of?
2. What industry would you guess?
3. Would you trust this company? (yes/no + why)
4. Is it memorable? (yes/no + why)
5. Overall impression (2-3 sentences)
```

After all 5 agents complete, synthesize their responses:
- Aggregate common themes in what the name evokes
- List industries mentioned
- Calculate trust rate (X/5 would trust)
- Calculate memorability rate (X/5 find it memorable)
- Note any divergent opinions

## Output Format

```
## Brand Evaluation: {NAME}

### Overall Score: {X}/100

### Domain Availability
| TLD | Status |
|-----|--------|
| .com | ✓ Available / ✗ Taken |
| .io | ✓ / ✗ |
| .co | ✓ / ✗ |
| .ai | ✓ / ✗ |
| .app | ✓ / ✗ |

### Social Handles
| Platform | Status |
|----------|--------|
| Twitter | ✓ / ✗ |
| Instagram | ✓ / ✗ |
| LinkedIn | ✓ / ✗ |
| TikTok | ✓ / ✗ |
| GitHub | ✓ / ✗ |

### Trademark Risk: {LOW/MEDIUM/HIGH}
{Brief explanation}

### Pronunciation Score: {X}/10
- Syllables: {N}
- Phonetic clarity: {assessment}
- Spelling predictability: {assessment}

### International Check
{Any issues found, or "No issues detected in major languages"}

### Similar Companies: {LOW/MEDIUM/HIGH} RISK
{List of similar companies found, if any}
- **CompanyName** (industry) - reason for similarity

### AI Perception Analysis (5 Personas)

**Trust Rate:** {X}/5 personas would trust this brand
**Memorability:** {X}/5 personas find it memorable

#### What This Name Evokes
{Synthesized themes from all personas}

#### Industry Associations
{List of industries mentioned by personas}

#### Individual Persona Responses

**Sarah (28, Software Engineer):** {brief response}
**Robert (55, Business Owner):** {brief response}
**Maya (34, Marketing Director):** {brief response}
**James (42, Investor):** {brief response}
**Lisa (22, Student):** {brief response}

### Mission Alignment (if provided)
Score: {X}/10
{Explanation of how well name fits mission}

### Recommendation
{Final assessment and any suggestions}
```

## Scoring Guide

Calculate overall score as weighted average:
- Domain availability: 20% (50 pts for .com, 50 pts split among others)
- Social handles: 10% (equal weight per platform)
- Trademark risk: 20% (low=100, medium=50, high=10)
- Pronunciation: 15% (score * 10)
- International: 15% (100 - 20 per issue found)
- Similar companies: 20% (low=85, medium=60, high=20)

## Example

User: "Evaluate the brand name 'Luminary' for an education technology company"

1. Check domains via whois
2. Check social handles via WebFetch
3. Search USPTO via WebSearch
4. Analyze pronunciation (4 syllables, easy spelling)
5. Check international meanings
6. **Search for similar companies** (e.g., Lumina, Illuminate, Luminari)
7. **Launch 5 persona agents in parallel using Task tool**
8. Synthesize and present results
