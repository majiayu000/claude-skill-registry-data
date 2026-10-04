---
name: create-plan
description: Create concise, actionable plans for coding tasks. Scope work, identify dependencies, and deliver atomic, ordered steps from discovery through validation and rollout.
compatibility:
  use-case: Project planning, task breakdown, implementation roadmaps
  frameworks: Software development, feature implementation, refactoring
---

# Create Plan

## Use This Skill When

- User explicitly asks for a plan for coding or development task
- Breaking down large features into manageable steps
- Refactoring or migrating complex systems
- Setting up new projects or modules
- Planning test strategy and validation approach
- Need to scope work before implementation
- Identifying dependencies and risk factors
- Creating roadmaps for feature delivery

## When NOT to Use

- User asks for immediate implementation (just implement)
- Only general advice or consultation needed (use discussion instead)
- User needs exploratory research (use analysis instead)
- Plans for non-technical projects (use other planning skills)

## Context: Plan Maturity

**Undeveloped**: Vague tasks like "build authentication", no concrete steps.

**Target**: Atomic, ordered steps from discovery to validation, files/commands named, risks identified.

**Optimized**: Risk-mitigated planning with rollback strategies, feature flags, data migration paths, thorough test coverage.

## Core Principle

Good plans are **specific, ordered, and atomic**. Each step should be completable independently and move the work from discovery → changes → tests → rollout.

## Instructions

### Step 1: Quick Context Assessment

**Read quickly (read-only mode only):**

| File/Section | What to Look For |
|-------------|-----------------|
| `README.md` | Project description, tech stack, setup |
| `docs/ARCHITECTURE.md` | System design, module relationships |
| `CONTRIBUTING.md` | Development workflows, code standards |
| Relevant source files | Implementation patterns, existing code style |
| CI/deployment config | Test commands, build process, deploy shape |

**Identify immediately:**
- Language and framework (Python/JS/Rust/etc.)
- Testing framework (`npm test`, `pytest`, etc.)
- Build system (npm/gradle/cargo/etc.)
- Deployment method (Docker/Lambda/K8s/etc.)
- Key constraints (backwards compatibility, performance, security)

### Step 2: Ask Clarifying Questions (If Blocking)

**Only ask 1–2 maximum questions if essential to plan.**

**Good blocking question:**
- "Is backwards compatibility required for the API change?"
- "Should this be feature-flagged or all-at-once?"

**Bad non-blocking question:**
- "What colors do you prefer?" (not needed for plan)
- "Is the team using Prettier?" (make reasonable assumption)

**If unsure but not blocked:** Make a reasonable assumption and note it in the plan.

### Step 3: Create the Plan

**Follow this exact template:**

```markdown
# Plan

<1–3 sentences describing what we're building, why, and the approach.>

## Scope

**In:**
- Specific systems/files affected
- New capabilities added
- Testing requirements
- Rollout strategy

**Out:**
- What won't be changed
- Known limitations
- Future work (not in this plan)

## Action Items

- [ ] **Discovery & Setup**: Identify affected files/modules, understand current implementation
- [ ] **Design**: Document approach/changes, identify dependencies, get feedback
- [ ] **Implementation**: [Specific module/file]: Make core changes
- [ ] **Implementation**: [Module 2]: Additional changes or integration
- [ ] **Tests**: Add unit tests for [specific behavior], add integration tests for [specific flow]
- [ ] **Validation**: Run full test suite, manual testing of [specific scenario]
- [ ] **Risk Mitigation**: [Feature flag/migration/rollback plan]
- [ ] **Documentation**: Update [relevant docs], add code comments
- [ ] **Rollout**: [Staging deploy → production strategy]

## Open Questions

- Question about specific behavior or requirement?
- Uncertainty about dependency or integration?
- Any assumptions needing verification?
```

### Step 4: Checklist Item Quality Standards

**Each item should be:**

| Quality Aspect | Good Example | Avoid |
|-----------|--------------|-------|
| **Specific Files** | "Update src/auth/login.ts" | "Handle backend auth" |
| **Verb-First** | "Add unit tests for", "Refactor", "Verify" | "Do auth", "Make changes" |
| **Ordered** | Discovery → Changes → Tests → Validation → Rollout | Random order |
| **Atomic** | One clear, completable step | Multiple unrelated tasks combined |
| **Concrete Validation** | "Run npm test --watch src/auth", "Manual test: login flow" | "Test it", "Make sure it works" |

**Strong Example Item:**
```
[ ] Add unit tests for UserService.authenticate() covering:
    - Valid credentials → returns token
    - Invalid password → throws AuthError
    - Non-existent user → throws UserNotFoundError
    Run: npm test src/services/user.test.ts
```

**Weak Example Item:**
```
[ ] Do the tests
```

### Step 5: Include Risk & Edge Cases

**When applicable, add items addressing:**

- **Backwards Compatibility**: Migration path for existing data
- **Performance**: Benchmarking, N+1 query prevention
- **Security**: Input validation, auth checks, data leaks
- **Error Handling**: Edge cases, fallback behavior
- **Rollback**: Graceful degradation, feature flags, data recovery

**Example items:**
```
[ ] Add feature flag for gradual rollout (rolled out to 10% → 50% → 100%)
[ ] Test edge case: empty list, null values, unicode characters
[ ] Add monitoring: log errors, track performance metrics
[ ] Data migration: add migration script for existing records
```

### Step 6: Note Open Questions

**Include max 3 open questions:**
- Assumptions that need verification
- Technical uncertainties affecting the plan
- Decisions needed from team/stakeholders

**Example:**
```
## Open Questions
- Should we cache user preferences, or always fetch fresh?
- Does the API need to support pagination immediately, or in phase 2?
- Should we add feature flag for gradual rollout, or deploy all-at-once?
```

### Step 7: Output Plan Only

**Do NOT:**
- Preface with explanations
- Add meta-commentary ("Here's a plan I created...")
- Include reasoning paragraphs (let the plan speak)

**DO:**
- Output the plan directly
- Use the exact template format
- Keep language concise and actionable

## Output

**Deliver:**

1. **Plan Document (exact template)**
   - Single opening paragraph
   - Clear In/Out scope
   - 6–10 atomic, ordered action items with specific files/commands
   - Max 3 open questions

2. **That's it** — no additional explanation or preface

## Example Plan Output

```markdown
# Plan

We're adding email verification to the auth flow. New users will receive 
a verification email; login is blocked until they verify. This improves 
security and reduces spam accounts. Approach: add new User status field, 
send verification email on signup, verify via token link.

## Scope

**In:**
- Add User.emailVerified flag (migrations/schema change)
- SendGrid email integration for verification emails
- New /api/verify-email endpoint
- Block login for unverified users
- Admin bypass for testing

**Out:**
- Email resend logic (phase 2)
- Password reset flow (existing, unchanged)
- Multi-factor authentication (future)

## Action Items

- [ ] **Discovery**: Map current auth flow in src/auth/, identify User model location
- [ ] **Schema**: Add User.emailVerified boolean field, create migration, test migration
- [ ] **Email Service**: Integrate SendGrid in src/services/email.ts, add template
- [ ] **API**: Create POST /api/verify-email?token=X endpoint, validate tokens
- [ ] **Auth Logic**: Modify login to check emailVerified in src/auth/login.ts
- [ ] **Tests**: Unit tests for verification logic, integration test: signup → email → verify → login
- [ ] **Edge Cases**: Expired tokens, duplicate verification attempts, admin bypass
- [ ] **Staging Test**: Test full flow: signup, check email, click link, login
- [ ] **Rollout**: Deploy with feature flag disabled, enable for 10% users, monitor errors

## Open Questions
- Should we send verification emails async or sync on signup?
- What's the token expiration window (24h, 7d)?
- Should unverified users be able to update profile/preferences?
```