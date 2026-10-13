---
name: feature-flags
description: Introduce, gate, manage, and safely retire feature toggles across a codebase
triggers: [feature flag, feature toggle, flag, dark launch, canary, rollout, kill switch]
audience: engineer
---

# Feature Flags

## Context
Feature flags (toggles) decouple deployment from release. They allow you to ship code to production without making it visible to users — enabling dark launches, gradual rollouts, A/B tests, and emergency kill switches. They are essential for trunk-based development and continuous delivery.

Use this skill when:
- Shipping an incomplete feature safely
- Performing a gradual/canary rollout
- Needing a kill switch for risky changes
- Running A/B tests or experiments

## Instructions

### Types of Feature Flags
Choose the right type before writing any code:
| Type | Purpose | Expected Lifespan |
|------|---------|-------------------|
| **Release toggle** | Hide incomplete feature in production | Days to weeks |
| **Ops toggle** | Kill switch for risky behavior | Months (remove after confidence) |
| **Experiment toggle** | A/B test or multivariate experiment | Short — remove after decision |
| **Permission toggle** | Enable feature per user/role/tenant | Long-lived — managed via config |

### Implementation Rules

1. **Flags at the entry point, not buried in logic.** Place the flag check as high as possible in the call stack — at the controller/handler or feature boundary.

2. **Name flags with intent:**
   - `enable_new_checkout_flow` not `flag_123`
   - Use the format: `enable_<feature_name>` or `use_<feature_name>`

3. **One flag per feature.** Do not reuse a flag for a different purpose after its original use is retired.

4. **Default to the safe/existing behavior** when a flag is absent or the config service is unavailable. Fail safe.

5. **Log flag evaluations on significant paths.** Include the flag name and the resolved value so you can correlate behavior in production logs.

6. **Never nest flags.** `if flag_a && flag_b` is a sign the design needs to be reconsidered.

### The Flag Lifecycle

```
1. Introduce → flag defaults OFF, new code is dark
2. Test → enable for internal users / test environments
3. Rollout → enable % of production traffic gradually
4. Full release → enable for 100%, monitor
5. Retire → remove flag AND old code path within 1–2 sprints of full release
```

### Retiring Flags (Critical — Flags Are Tech Debt)
A flag that outlives its purpose is tech debt that increases code complexity. Follow this process:
1. Set a removal date when you create the flag (add it as a comment in the code)
2. After full rollout, create a ticket to remove the flag in the next sprint
3. Delete: the flag check, the old code path, and the flag from the config/service
4. Confirm tests still pass with the new behavior as the permanent path

### In a Monolith
- Use an in-process flag store (env var, config file, or database row)
- Consider a library like Flipper, Unleash, or LaunchDarkly for dynamic evaluation

### In Distributed Systems
- Use a centralized flag service shared across services
- Ensure consistent evaluation: the same user should get the same flag value across services for the same request

## Principles
- Source: [Feature Toggles — Martin Fowler](https://martinfowler.com/articles/feature-toggles.html)
- Key idea: *"Feature toggles introduce complexity. Every active toggle is a source of conditional code that must be tested and understood. The only cure is to remove them as soon as they've served their purpose."*

## Output Format
When applying this skill, the agent should:
- Identify the flag type and expected lifespan
- Show the flag check implementation at the correct entry point
- Add a removal comment with a suggested date
- Produce the rollout plan (internal → canary → full)
- Flag any existing toggles that appear overdue for retirement
