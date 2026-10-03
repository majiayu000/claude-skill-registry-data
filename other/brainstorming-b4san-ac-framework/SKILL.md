---
name: brainstorming
description: Generates comprehensive questions about decisions before implementing. Explores requirements, constraints, success criteria, edge cases, and hidden assumptions in a SINGLE comprehensive prompt. Use when starting any significant work to surface unknowns early.
license: MIT
metadata:
  author: AC Framework
  version: "2.0"
---

# Brainstorming - Comprehensive Question Generation

Surface unknowns, challenge assumptions, and explore the problem space BEFORE committing to a solution.

## When to Use This Skill

Use this skill when:
- Starting a new project or major feature
- Facing ambiguous requirements
- Need to explore multiple approaches
- Want to identify risks early
- Before creating any OpenSpec change

**CRITICAL: This skill generates ALL questions in ONE prompt, not sequentially.**

---

## Instructions

### Step 1: Analyze the Context

Read and understand:
1. The user's stated goal/requirement
2. Any existing project context from `project-index`
3. Constraints mentioned or implied
4. Success criteria (explicit or assumed)

### Step 2: Generate Comprehensive Brainstorming Questions

**⚠️ IMPORTANT: Generate ALL questions in a SINGLE comprehensive prompt.**

Do NOT ask questions one by one. Instead, present a complete brainstorming document with ALL relevant questions organized by category.

Structure your response as:

```
## 🧠 Brainstorming Analysis: [Feature/Project Name]

### Context Summary
[Brief summary of what you're building and why]

### Category 1: Requirements & Scope
Questions to clarify WHAT we're building:
- Q1: [Specific question about requirements]
- Q2: [Question about scope boundaries]
- Q3: [Question about feature completeness]
- ...

### Category 2: Constraints & Limitations
Questions about boundaries and restrictions:
- Q1: [Technical constraint question]
- Q2: [Time/budget constraint question]
- Q3: [Regulatory/compliance question]
- ...

### Category 3: User Experience & Interface
Questions about HOW users will interact:
- Q1: [User flow question]
- Q2: [Accessibility concern]
- Q3: [Error handling UX question]
- ...

### Category 4: Technical Architecture
Questions about implementation approach:
- Q1: [Technology stack question]
- Q2: [Integration point question]
- Q3: [Scalability concern]
- Q4: [Data model question]
- ...

### Category 5: Edge Cases & Failure Modes
Questions about what could go wrong:
- Q1: [Edge case scenario question]
- Q2: [Failure recovery question]
- Q3: [Security vulnerability question]
- Q4: [Performance degradation scenario]
- ...

### Category 6: Success Criteria & Metrics
Questions about how we measure success:
- Q1: [Success metric question]
- Q2: [Quality threshold question]
- Q3: [User adoption question]
- ...

### Category 7: Dependencies & Blockers
Questions about external factors:
- Q1: [Third-party dependency question]
- Q2: [Team/resource dependency]
- Q3: [Upstream/downstream system question]
- ...

### Category 8: Alternative Approaches
Questions exploring different solutions:
- Q1: [Alternative technology question]
- Q2: [Simpler approach question]
- Q3: [Trade-off analysis question]
- ...

---

## 🎯 Next Steps

Please answer the questions above. Once clarified, we can proceed to:
1. `openspec-new-change` - Create structured change
2. `openspec-ff-change` - Fast-forward to implementation
3. Continue brainstorming if needed

**Your answers will shape the entire implementation approach.**
```

### Step 3: Wait for Comprehensive Answers

After presenting ALL questions:
- Wait for the user to answer them (may be partial or complete)
- Ask follow-up questions ONLY if answers reveal new unknowns
- Do NOT re-ask questions already answered

### Step 4: Synthesize Insights

Once you have answers:
1. Summarize key decisions made
2. Identify any remaining ambiguities
3. Document assumptions being made
4. Suggest the best path forward

---

## Question Categories Reference

Always consider questions from these categories:

**1. Requirements & Scope**
- What exactly needs to be built?
- What is explicitly OUT of scope?
- Are there different user types with different needs?
- What is the minimum viable version?

**2. Constraints & Limitations**
- Technical stack constraints?
- Time/deadline constraints?
- Budget/resource constraints?
- Regulatory/compliance requirements?
- Legacy system constraints?

**3. User Experience**
- Who are the users?
- What is their technical sophistication?
- What devices/platforms will they use?
- Accessibility requirements?
- Localization needs?

**4. Technical Architecture**
- Integration points with existing systems?
- Data storage requirements?
- Scalability expectations?
- Security requirements?
- Performance requirements (latency, throughput)?

**5. Edge Cases & Failure Modes**
- What happens when [X] fails?
- How does the system handle invalid input?
- What about concurrent access?
- What's the behavior at scale limits?
- Disaster recovery needs?

**6. Success Metrics**
- How do we know this is working?
- What are the KPIs?
- User satisfaction measures?
- Technical performance thresholds?

**7. Dependencies**
- External APIs or services needed?
- Other team dependencies?
- Infrastructure requirements?
- Third-party licenses or approvals?

**8. Alternatives**
- What simpler approaches exist?
- What are the trade-offs?
- Buy vs build decisions?
- Short-term vs long-term considerations?

---

## Example Output

**User says:** "Build a user authentication system"

**Your brainstorming (SINGLE PROMPT):**

```
## 🧠 Brainstorming Analysis: User Authentication System

### Context Summary
Building an auth system for user login/signup. Critical security component affecting all users.

### Category 1: Requirements & Scope
- Q1: What authentication methods? (email/password, OAuth, SSO, magic links, 2FA?)
- Q2: Do users need profiles, or just auth?
- Q3: Session duration? Remember me feature?
- Q4: Account recovery options?
- Q5: Admin/moderator roles needed?

### Category 2: Constraints & Limitations
- Q6: Any compliance requirements? (GDPR, HIPAA, SOC2)
- Q7: Password complexity requirements?
- Q8: Rate limiting needs for brute force protection?

### Category 3: User Experience
- Q9: Login/signup flow preference? (modal, separate page, inline)
- Q10: Error message style? (specific vs generic for security)
- Q11: Email verification required before access?

### Category 4: Technical Architecture
- Q12: JWT vs session cookies vs other?
- Q13: Database for user storage?
- Q14: Password hashing algorithm? (bcrypt, Argon2)
- Q15: Token refresh strategy?

### Category 5: Edge Cases & Failure Modes
- Q16: What if email provider is down during signup?
- Q17: Handle concurrent login attempts from different devices?
- Q18: Account lockout after failed attempts?
- Q19: Session invalidation on password change?

### Category 6: Success Criteria
- Q20: Login success rate target?
- Q21: Maximum acceptable login latency?
- Q22: Security audit requirements?

### Category 7: Dependencies
- Q23: Email service provider? (SendGrid, AWS SES, etc.)
- Q24: Existing user database to migrate?
- Q25: Frontend framework constraints?

### Category 8: Alternative Approaches
- Q26: Use Auth0/Firebase Auth instead of building?
- Q27: Start with simple email/pass, add OAuth later?
```

---

## Guardrails

- **ALWAYS ask ALL questions in ONE prompt** - Never sequential
- **Be thorough** - Better to ask too much than miss critical context
- **Organize clearly** - Categories help the user answer systematically
- **Wait for answers** - Don't proceed until user responds
- **Synthesize** - After answers, provide clear summary and recommendation
- **No implementation** - This is thinking only, no code yet

---

## Integration with OpenSpec

After brainstorming is complete:

1. Summarize decisions made
2. Recommend next step:
   - `openspec-new-change` for structured approach
   - `openspec-ff-change` if ready to fast-forward
3. Include brainstorming insights in the change proposal

---

## Requirements

- Understanding of the problem domain
- Ability to think systematically about edge cases
- Familiarity with common software architecture patterns
- Knowledge of security, performance, and UX best practices
