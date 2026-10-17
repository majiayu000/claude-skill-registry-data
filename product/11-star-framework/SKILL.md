---
name: 11-star-framework
description: Rate any product, feature, or experience on the 11-star scale (Brian Chesky's Airbnb thought experiment). Use when user says "rate this experience", "11-star", "star rating", "experience audit", "how good is this", "experience rating", "product audit", "quality assessment", or wants to evaluate product quality and identify improvement paths. Also trigger when user wants to benchmark a feature, assess where a product stands, or map out what "great" looks like - even if they don't explicitly say "11-star".
---

# 11-Star Experience Framework

Brian Chesky (Airbnb) thought experiment: "What would a 1-star through 11-star experience look like?"

Forces teams to think beyond "good enough" and imagine transformative experiences.

## The Scale

| Star Level | Definition |
|------------|-----------|
| **1-star** | Broken, unusable |
| **2-star** | Barely functional |
| **3-star** | Meets basic need |
| **4-star** | Reliable, useful |
| **5-star** | Delights |
| **6-star** | Memorable |
| **7-star** | Magical |
| **8-star** | Personalized magic |
| **9-star** | Science fiction |
| **10-star** | Impossible today |
| **11-star** | Transforms the domain |

## How to Use

### Step 1: Rate Your Feature

Describe what each star level looks like for THIS specific feature or product.

**Example - E-Commerce Checkout:**

| Star | Experience |
|------|-----------|
| 1-star | Page crashes; payment fails silently; user gives up |
| 3-star | Checkout works; basic form fields; no saved payment methods |
| 5-star | One-click checkout; saved cards; instant confirmation with ETA |
| 7-star | Predicts what you want before you search; auto-applies best discount; delivery arrives same day |
| 9-star | Knows you need something before you do; orders it; perfect every time |
| 11-star | Commerce friction doesn't exist - things you need appear when you need them |

### Step 2: Choose Target

- **Below 5-star:** Acceptable for MVP, communicate clearly
- **5-7 star:** Sweet spot for v1 release
- **Above 7-star:** Aspirational; roadmap for future

### Step 3: Use as Scope Filter

- "4-star to 5-star?" - Worth it
- "5-star to 5.2-star?" - Probably not
- "Gets us to 7-star" - Realistic for current phase?

## Common Benchmarks

These benchmarks apply across product categories. Adapt the specific examples to your domain.

| Domain | 3-star | 5-star | 7-star |
|--------|--------|--------|--------|
| Onboarding | Basic docs with commands | Guided walkthrough, validation at each step, troubleshooting | Interactive course, adapts to user's level |
| Documentation | Single page covering basics | Multi-page docs, examples, architecture guide | Inline help, contextual guidance, video walkthroughs |
| Output quality | Raw data dump | Rich formatting, severity indicators, actionable next steps | Trend tracking, executive summaries, copy-paste actions |
| Extensibility | Hardcoded defaults | Config file, multiple output formats | Plugin system, custom extensions, API access |
| Trust & safety | No explanation of what runs | Permissions documented, read-only by default | Dry-run default, full audit trail, airgapped mode |

## Output Format

When rating a project or feature:

| Star Level | Experience Description | Realistic Now? |
|------------|----------------------|----------------|
| 1-star | [broken version] | -- |
| 3-star | [basic version] | -- |
| 5-star | [delightful version] | Yes/No |
| 7-star | [magical version] | Yes/No |
| 9-star | [sci-fi version] | No |
| 11-star | [transformative version] | No |

**Target Star Level:** {N} - {rationale}

## Dimension-by-Dimension Rating

For a thorough audit, rate each dimension independently:

| Dimension | Rating | Evidence |
|-----------|--------|----------|
| **Onboarding** | X.X | [specific evidence] |
| **Documentation** | X.X | [specific evidence] |
| **Output quality** | X.X | [specific evidence] |
| **Trust & safety** | X.X | [specific evidence] |
| **Extensibility** | X.X | [specific evidence] |
| **Code quality** | X.X | [specific evidence] |

Then identify:
- **Strengths that push above 5-star** (numbered list with evidence)
- **Remaining gaps to next star level** (table with gap, impact)
- **Path to next star level** (prioritized action items)

## Anti-Patterns

**1. Rating everything 3-star**
Bad: Defaulting every dimension to "meets basic need" without investigating actual behavior
Good: Test the real experience, check edge cases, rate based on evidence not assumptions

**2. Skipping dimensions**
Bad: Rating only the dimensions you feel confident about, ignoring the rest
Good: Rate every dimension. Gaps in your knowledge are themselves evidence of a lower rating (if you can't tell, the user probably can't either)

**3. Aspirational scoring**
Bad: "We plan to add X next sprint" bumps the rating from 3 to 5
Good: Rate what exists today. Plans are roadmap items, not current-state evidence

**4. Flat improvement list**
Bad: "Improve onboarding, improve docs, improve output" with no priority
Good: Rank by impact - which gap, if closed, moves the overall experience up a full star level?

**5. Ignoring the 1-star description**
Bad: Jumping straight to 5-star and above
Good: Describing the 1-star experience grounds the team in what "broken" actually looks like and makes higher ratings more calibrated
