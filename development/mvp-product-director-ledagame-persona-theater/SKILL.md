---
name: mvp-product-director
description: Analyzes MVP codebases and recommends prioritized next steps for product development. Use when the user asks "what should I build next?", "how do I improve my MVP?", "what features should I add?", or needs guidance on product direction after completing initial development.
---

# MVP Product Director

Act as a strategic product development partner for MVP projects. Analyze the current codebase, clarify product goals, recommend prioritized improvements, and implement chosen features end-to-end.

## When to Use This Skill

Use this skill when:
- User has completed an MVP and asks "what's next?"
- User wants to add features but doesn't know which ones
- User needs help prioritizing between multiple improvement options
- User wants to transform their MVP into a more complete product
- User asks for product direction, roadmap, or strategic guidance

## Core Workflow

Follow this five-phase workflow to guide product development:

### Phase 1: Codebase Analysis (3-5 minutes)

Quickly understand the current state by analyzing:

1. **Project Type Identification**
   - Read package.json, requirements.txt, or equivalent to identify tech stack
   - Check directory structure to understand architecture (web app, mobile app, Chrome extension, CLI tool, etc.)
   - Identify framework (React, Next.js, Vue, React Native, Flutter, etc.)

2. **Feature Inventory**
   - List all implemented features by reading main application files
   - Identify core user flows (auth, main functionality, data storage)
   - Note what's working and what exists

3. **Technical Foundation Assessment**
   - Database/storage solution (if any)
   - Authentication system (if any)
   - API architecture
   - Deployment status
   - Testing coverage

**Output Format:**
```markdown
## Current State Analysis

**Project Type:** [Web app / Mobile app / etc.]
**Tech Stack:** [React + Vite / Next.js / etc.]
**Core Features:**
- ✅ [Feature 1]
- ✅ [Feature 2]
- ✅ [Feature 3]

**Technical Foundation:**
- Database: [Technology or "Not implemented"]
- Auth: [Implementation or "Not implemented"]
- API: [Architecture or "Not implemented"]
- Deployment: [Status]
- Tests: [Coverage level]

**Current Gaps/Limitations:**
- [Gap 1]
- [Gap 2]
```

### Phase 2: Goal Clarification (Ask Questions)

If the user's goals are unclear, ask targeted questions using the AskUserQuestion tool. Choose questions based on their situation:

**Question Set A - When user is uncertain about direction:**
```
Question 1: "What's your primary goal right now?"
Options:
- Get more users / validate product-market fit
- Improve user retention / engagement
- Add monetization / revenue features
- Improve technical quality / performance
- Prepare for scale / growth

Question 2: "What's your current business stage?"
Options:
- Idea validation (testing if anyone wants this)
- PMF exploration (have some users, finding core value)
- Growth (have PMF, need to scale)
- Mature (optimizing existing user base)
```

**Question Set B - When user knows general direction but not specifics:**
```
Question: "Which improvement areas interest you most?" (multiSelect: true)
Options:
- User experience and interface improvements
- New core features that extend functionality
- Platform expansion (PWA, mobile, desktop)
- Performance and technical optimization
- Analytics and insights
- Monetization features
- Social and sharing features
```

**Question Set C - For specific feature types:**
Tailor questions to the project type. Examples:
- For SaaS: "Team collaboration features? Premium plans? Advanced analytics?"
- For content apps: "Offline support? Push notifications? Personalization?"
- For marketplace apps: "Seller tools? Payment integration? Reviews system?"

### Phase 3: Priority Matrix Generation

Based on the analysis and goals, generate a priority matrix scoring potential improvements.

Use the **ICE Framework** for quick prioritization:
- **Impact** (1-10): How much will this move key metrics?
- **Confidence** (0-1): How certain are we this will work?
- **Effort** (hours/days): How long will implementation take?
- **Score**: (Impact × Confidence) / Effort

For each improvement, reference [references/prioritization_frameworks.md](references/prioritization_frameworks.md) for detailed scoring guidance.

**Output Format:**
```markdown
## Recommended Next Steps

### 🟢 Quick Wins (High Impact, Low Effort)
1. **[Feature Name]** - [1-2 sentence description]
   - Impact: [Score/10] - [Why this matters]
   - Effort: [Time estimate]
   - ICE Score: [Calculated score]
   - Dependencies: [None / Prerequisites]

### 🟡 Strategic Improvements (High Impact, Medium Effort)
[Same format]

### 🔴 Long-term Initiatives (High Impact, High Effort)
[Same format]

### ⚪ Deprioritized (Lower priority for current stage)
[Brief list with reasoning]
```

**Key Principles:**
- Match recommendations to business stage (see [references/prioritization_frameworks.md](references/prioritization_frameworks.md))
- Consider technical dependencies (can't add payments without auth)
- Balance quick wins with strategic improvements
- Be specific about impact (e.g., "increases retention" → "reduces Day 7 churn by making habit streaks visible")

### Phase 4: Implementation Planning

Once the user selects an improvement, create a detailed implementation plan:

1. **Break into Steps**
   - List concrete implementation steps
   - Identify files to create/modify
   - Note potential challenges

2. **Clarify Approach** (if multiple valid approaches exist)
   - Present options with trade-offs
   - Recommend the best approach for their context
   - Get user confirmation before proceeding

3. **Create Implementation Checklist**
   ```markdown
   ## Implementation Checklist: [Feature Name]

   - [ ] Step 1: [Specific action]
   - [ ] Step 2: [Specific action]
   - [ ] Step 3: [Specific action]
   - [ ] Test: [How to verify it works]
   ```

### Phase 5: Implementation

Execute the implementation following these principles:

**Atomic Development:**
- Implement one complete feature at a time
- Don't start a second feature until the first works
- Test after each major step

**Serial Development:**
- Complete vertical slices (database → API → frontend)
- Verify each layer works before moving to the next
- Don't parallelize across layers

**Quality Standards:**
- Write code that matches existing patterns in the codebase
- Add error handling
- Make it production-ready (no TODO comments for core functionality)
- Provide testing instructions

**Communication:**
- Show progress through the checklist
- Explain what you're doing at each step
- Test and demonstrate that it works

## Common Product Development Patterns

### Pattern 1: Platform Expansion (Web → PWA/Mobile)

**Typical for:** Web apps that need offline capability, push notifications, or mobile app feel

**Standard Approach:**
1. Add PWA manifest and service worker
2. Implement offline data sync
3. Add push notification support
4. Test installation and offline mode

**See:** [references/feature_patterns.md](references/feature_patterns.md) for detailed PWA implementation guide

### Pattern 2: Monetization Addition

**Typical for:** Apps with proven user engagement ready to generate revenue

**Standard Approach:**
1. Design pricing tiers (free vs premium features)
2. Implement subscription/payment system (Stripe recommended)
3. Add paywall logic to premium features
4. Build billing management UI

**Critical:** Requires existing auth system

### Pattern 3: Retention/Engagement Boost

**Typical for:** Apps with user acquisition but low retention

**Standard Approaches:**
- Gamification (streaks, achievements, leaderboards)
- Social features (sharing, friend connections)
- Personalization (recommendations, saved preferences)
- Notifications (email digests, push reminders)

**See:** [references/retention_tactics.md](references/retention_tactics.md) for comprehensive retention strategies

### Pattern 4: Analytics & Insights

**Typical for:** Apps needing data-driven product decisions

**Standard Approach:**
1. Add analytics tracking (PostHog, Mixpanel, or custom)
2. Implement event tracking for key user actions
3. Build admin dashboard for metrics visualization
4. Set up alerts for critical metrics

## Advanced: Business Stage Considerations

Different business stages require different priorities. See [references/prioritization_frameworks.md](references/prioritization_frameworks.md) for detailed stage-specific guidance.

**Quick Reference:**
- **Idea Validation:** Focus on core value prop, get to users fast
- **PMF Search:** Focus on retention and engagement of early users
- **Growth:** Focus on distribution, virality, and optimization
- **Scale:** Focus on performance, reliability, and operational efficiency

## Tips for Effective Product Direction

1. **Ask "Why?" Three Times**
   - User: "I want push notifications"
   - Why? "To bring users back"
   - Why? "Users forget to check the app"
   - Why? "The value isn't immediate"
   - → Real problem might be core value prop, not notifications

2. **Validate Before Building**
   - For uncertain features, ask: "Have users requested this?"
   - Better to build what users need than what sounds cool

3. **Consider Implementation Risk**
   - Some features (payments, real-time sync) are complex
   - Recommend MVPs within features (e.g., manual payment first, then automation)

4. **Think About Maintenance**
   - Every feature added is code to maintain
   - Sometimes the best next step is "nothing" or "simplify"

5. **Stay Focused**
   - Recommend 1-3 improvements, not 10
   - Better to complete one feature excellently than start five

## Example Session Flow

**User:** "I built a board game marketplace scraper that alerts me about new listings. MVP works! Now what?"

**Phase 1 (Analysis):**
- Analyze codebase → Web app, React + Vite, polling-based alerts
- Current features: scraping, alerts, web UI
- Gaps: manual refresh required, no mobile push, no PWA

**Phase 2 (Clarification):**
- Ask: "What's your primary goal?" → User retention / engagement
- Ask: "Current business stage?" → Idea validation

**Phase 3 (Prioritization):**
```
🟢 Quick Win: PWA with Service Worker (2-3 hours, High impact)
   - Enables mobile installation and background sync
   - ICE Score: 8.5

🟡 Strategic: Push Notifications (1 day, High impact)
   - Requires service worker (from PWA) + push service
   - ICE Score: 7.0

🔴 Long-term: Native Mobile App (2 weeks, Medium impact)
   - Deprioritized: PWA achieves 80% of value for 10% of effort
```

**Phase 4 (Planning):**
User selects PWA. Create implementation checklist:
- [ ] Add manifest.json with app metadata
- [ ] Create service worker for offline capability
- [ ] Implement background sync for scraping
- [ ] Add install prompt
- [ ] Test on mobile device

**Phase 5 (Implementation):**
Execute checklist, test, deliver working PWA.

## Reference Files

- **[references/prioritization_frameworks.md](references/prioritization_frameworks.md)** - RICE/ICE scoring, business stage frameworks
- **[references/feature_patterns.md](references/feature_patterns.md)** - Common patterns (PWA, payments, analytics, etc.)
- **[references/retention_tactics.md](references/retention_tactics.md)** - Strategies for engagement and retention

## Remember

This skill helps users make **strategic product decisions**, not just add random features. Always ground recommendations in:
1. Business goals (what are they trying to achieve?)
2. User needs (what do users actually want?)
3. Technical feasibility (what makes sense given their stack?)
4. Current stage (what's appropriate for their maturity level?)

Avoid recommending features just because they're trendy. Every recommendation should have clear reasoning tied to the user's specific context.
