---
summary: "Optimize post-signup user activation and engagement."
---

# Onboarding CRO Skill

This skill focuses on optimizing the user onboarding experience immediately after signup to improve activation rates, reduce churn, and increase initial engagement.

## When to use this skill:
Use this skill when you need to:
- Analyze post-signup user journeys to identify drop-off points or friction.
- A/B test different onboarding flows, welcome messages, or guided tours.
- Personalize the onboarding experience based on user segments.
- Improve feature adoption and product stickiness in the early stages.
- Develop strategies to convert new users into active, retained users.

## Capabilities:
- **Onboarding Flow Analysis:** Maps and analyzes the sequence of steps a user takes after signup.
- **Personalization Engine:** Helps segment users and deliver tailored onboarding content or paths.
- **A/B Testing Framework:** Supports experimentation with different onboarding elements (e.g., tutorials, checklists, prompts).
- **Engagement Tracking:** Monitors key activation metrics like first feature use, profile completion, or critical action taken.
- **Feedback Collection:** Facilitates gathering user feedback during the onboarding process to identify pain points.

## Examples:

### Example 1: Analyze an onboarding flow for a new user segment
```
/onboarding-cro analyze --segment="premium_users" --start-event="first_login" --end-event="first_project_creation"
```
This command analyzes the onboarding journey for 'premium_users' from their first login to creating their first project.

### Example 2: Suggest A/B tests for a welcome email sequence
```
/onboarding-cro recommend-ab-test --channel="email" --element="welcome_series" --objective="increase_feature_x_adoption"
```
This command would suggest A/B test variations for a welcome email sequence aimed at increasing the adoption of 'feature X'.

### Example 3: Get activation rates for a specific onboarding milestone
```
/onboarding-cro get-metrics --milestone="tutorial_completion" --timeframe="last_month"
```
This command retrieves the activation rate for users completing the tutorial over the last month.
