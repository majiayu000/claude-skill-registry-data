---
name: self-service-onboarding
description: SaaS onboarding patterns for user activation and time-to-value optimization. Covers signup flows, progressive disclosure, activation metrics, and onboarding UX.
allowed-tools: Read, Glob, Grep, Task, mcp__perplexity__search, mcp__perplexity__reason
---

# Self-Service Onboarding Skill

Patterns for designing effective SaaS onboarding that maximizes activation and minimizes time-to-value.

## When to Use This Skill

Use this skill when:

- **Self Service Onboarding tasks** - Working on saas onboarding patterns for user activation and time-to-value optimization. covers signup flows, progressive disclosure, activation metrics, and onboarding ux
- **Planning or design** - Need guidance on Self Service Onboarding approaches
- **Best practices** - Want to follow established patterns and standards

## Overview

Onboarding is the critical path from signup to "aha moment." Poor onboarding leads to churn before customers experience value. This skill covers proven patterns for self-service SaaS onboarding.

## Onboarding Architecture

```text
+------------------------------------------------------------------+
|                    SaaS Onboarding Flow                           |
+------------------------------------------------------------------+
|                                                                   |
|  +----------+   +----------+   +----------+   +-------------+    |
|  | Signup   |-->| Welcome  |-->| Setup    |-->| Activation  |    |
|  | Form     |   | Screen   |   | Wizard   |   | Milestone   |    |
|  +----------+   +----------+   +----------+   +-------------+    |
|       |              |              |               |             |
|       v              v              v               v             |
|  Email verify   Expectations   Core config    "Aha moment"       |
|  Basic profile  Quick win      Integration    Value realized     |
|  Plan selection Personalize    Team invite    Habit formed       |
|                                                                   |
+------------------------------------------------------------------+
```

## Onboarding Patterns

### 1. Progressive Disclosure

```text
Pattern: Reveal complexity gradually
Benefit: 50% reduction in cognitive load

Levels:
1. Essential only (first session)
2. Core features (week 1)
3. Advanced features (after activation)
4. Power user features (on-demand)

Implementation:
- Feature discovery based on usage
- Contextual tooltips, not upfront tutorials
- Progressive permission requests
```

### 2. Product-Led Growth (PLG)

```text
Pattern: Let the product teach itself
Key Elements:
- Empty states that guide action
- In-app tours triggered by behavior
- Checklists with progress tracking
- Sample data / templates
```

### 3. Time-to-Value Optimization

```text
Goal: Minimize time from signup to "aha moment"

Tactics:
- Pre-fill data where possible
- Smart defaults (no blank forms)
- Skip optional steps initially
- Defer account verification
- Instant access (email verify async)
```

## Signup Flow Design

### Minimal Signup

```csharp
// Minimal signup - just email to start
public sealed record SignupRequest
{
    [Required, EmailAddress]
    public required string Email { get; init; }

    // Optional - can collect later
    public string? Name { get; init; }
    public string? CompanyName { get; init; }
}

// Defer password until after first value
public sealed record SetPasswordRequest
{
    public required string Token { get; init; }
    public required string Password { get; init; }
}
```

### Social/SSO Signup

```text
Priority Order:
1. Google Sign-In (highest conversion)
2. Microsoft (B2B customers)
3. GitHub (developer products)
4. Email/password (fallback)

Benefits:
- 20-30% higher signup conversion
- Pre-verified email
- Profile data auto-filled
```

### Signup with Intent

```csharp
// Capture intent to personalize onboarding
public sealed record SignupWithIntentRequest
{
    public required string Email { get; init; }

    // Personalization questions
    public required string Role { get; init; }        // "developer", "manager", "founder"
    public required string UseCase { get; init; }     // "analytics", "collaboration", "automation"
    public required string TeamSize { get; init; }    // "just_me", "2-10", "11-50", "50+"
}
```

## Welcome Experience

### First-Run Experience (FRX)

```text
Elements:
1. Personalized welcome ("Welcome, Sarah!")
2. Clear next step (single CTA)
3. Quick win opportunity
4. Progress indicator (if multi-step)
5. Escape hatch (skip / do later)
```

### Welcome Checklist

```csharp
public sealed record OnboardingChecklist
{
    public required Guid UserId { get; init; }
    public required List<OnboardingStep> Steps { get; init; }
    public int CompletedCount => Steps.Count(s => s.IsCompleted);
    public decimal ProgressPercent => Steps.Count > 0
        ? (decimal)CompletedCount / Steps.Count * 100
        : 0;
}

public sealed record OnboardingStep
{
    public required string Id { get; init; }
    public required string Title { get; init; }
    public required string Description { get; init; }
    public required string ActionUrl { get; init; }
    public required bool IsCompleted { get; init; }
    public required bool IsRequired { get; init; }
    public int? EstimatedMinutes { get; init; }
    public string? CompletedAt { get; init; }
}
```

### Sample Checklist Items

```text
Typical B2B SaaS Onboarding Checklist:

Required Steps:
[x] Create your account (auto-complete)
[ ] Complete your profile
[ ] Create your first [core object]
[ ] Invite a team member

Optional Steps:
[ ] Connect your [integration]
[ ] Import existing data
[ ] Customize your workspace
[ ] Set up notifications
```

## Setup Wizard Patterns

### Multi-Step Wizard

```text
Design Principles:
1. Show progress (Step 2 of 4)
2. Allow back navigation
3. Save progress (don't lose work)
4. Smart defaults (pre-select common options)
5. Skip optional (complete later)
```

### Wizard Implementation

```csharp
public sealed class SetupWizardController : ControllerBase
{
    // GET: Current step state
    [HttpGet("setup/current")]
    public async Task<ActionResult<WizardState>> GetCurrentStep()
    {
        var state = await _wizardService.GetStateAsync(User.GetTenantId());
        return Ok(state);
    }

    // POST: Complete step and advance
    [HttpPost("setup/steps/{stepId}/complete")]
    public async Task<ActionResult<WizardState>> CompleteStep(
        string stepId,
        [FromBody] StepCompletionData data)
    {
        var result = await _wizardService.CompleteStepAsync(
            User.GetTenantId(),
            stepId,
            data);

        if (result.IsWizardComplete)
        {
            await _onboardingService.MarkOnboardingCompleteAsync(User.GetTenantId());
        }

        return Ok(result.NewState);
    }

    // POST: Skip optional step
    [HttpPost("setup/steps/{stepId}/skip")]
    public async Task<ActionResult<WizardState>> SkipStep(string stepId)
    {
        var result = await _wizardService.SkipStepAsync(
            User.GetTenantId(),
            stepId);

        return Ok(result);
    }
}
```

## Activation Metrics

### Key Metrics

```text
Activation Funnel:
+------------------------------------------------------------------+
| Stage              | Metric              | Target          |
+--------------------+---------------------+-----------------+
| Signup             | Conversion rate     | > 30%           |
| Email verified     | Verification rate   | > 80%           |
| Profile complete   | Completion rate     | > 60%           |
| First [action]     | Activation rate     | > 40%           |
| Aha moment         | Value realization   | > 25%           |
| Day 7 return       | Retention           | > 30%           |
+--------------------+---------------------+-----------------+
```

### Activation Event Tracking

```csharp
public interface IActivationTracker
{
    Task TrackEventAsync(ActivationEvent evt);
    Task<ActivationStatus> GetStatusAsync(Guid userId);
    Task<bool> HasReachedAhaMomentAsync(Guid userId);
}

public sealed record ActivationEvent
{
    public required Guid UserId { get; init; }
    public required string EventType { get; init; }
    public required DateTimeOffset Timestamp { get; init; }
    public Dictionary<string, string>? Properties { get; init; }
}

// Common activation events
public static class ActivationEvents
{
    public const string SignupCompleted = "signup_completed";
    public const string EmailVerified = "email_verified";
    public const string ProfileCompleted = "profile_completed";
    public const string FirstProjectCreated = "first_project_created";
    public const string FirstTeamMemberInvited = "first_team_member_invited";
    public const string FirstIntegrationConnected = "first_integration_connected";
    public const string AhaMomentReached = "aha_moment_reached";
}
```

### Aha Moment Definition

```text
Aha Moment Examples by Product Type:

Project Management:
- Created project AND added 3+ tasks AND invited team member

Analytics:
- Connected data source AND viewed first dashboard

Communication:
- Sent first message AND received reply

Developer Tools:
- Installed SDK AND made first API call

Define YOUR aha moment:
1. Analyze retained vs churned users
2. Find behavior that correlates with retention
3. Optimize onboarding to reach that behavior
```

## Empty States

### Empty State Design

```text
Good Empty State:
+------------------------------------------+
|                                          |
|     [Illustration/Icon]                  |
|                                          |
|     No projects yet                      |
|                                          |
|     Create your first project to         |
|     start collaborating with your team   |
|                                          |
|     [+ Create Project] (Primary CTA)     |
|                                          |
|     or [Import from Trello]              |
|                                          |
+------------------------------------------+

Elements:
1. Visual (not just text)
2. Explanation of what goes here
3. Value proposition
4. Primary action (CTA)
5. Alternative action (if applicable)
```

### Empty State Implementation

```csharp
public sealed record EmptyState
{
    public required string Title { get; init; }
    public required string Description { get; init; }
    public required string IllustrationUrl { get; init; }
    public required EmptyStateAction PrimaryAction { get; init; }
    public EmptyStateAction? SecondaryAction { get; init; }
}

public sealed record EmptyStateAction
{
    public required string Label { get; init; }
    public required string Url { get; init; }
    public required string Icon { get; init; }
}
```

## Onboarding Emails

### Email Sequence

```text
Day 0: Welcome + Quick Start
Day 1: Did you complete [key action]?
Day 3: Feature highlight + tip
Day 7: Check-in + offer help
Day 14: Re-engagement if inactive

Triggers:
- Incomplete onboarding -> reminder
- Stuck on step -> help offer
- Activated -> congratulations + next step
- Churning -> win-back
```

### Email Personalization

```csharp
public sealed class OnboardingEmailService(IEmailService email, IOnboardingService onboarding)
{
    public async Task SendOnboardingEmailAsync(Guid userId, string templateId)
    {
        var status = await onboarding.GetStatusAsync(userId);
        var user = await _userService.GetAsync(userId);

        var data = new OnboardingEmailData
        {
            UserName = user.FirstName,
            NextStep = status.NextRecommendedStep,
            ProgressPercent = status.ProgressPercent,
            DaysInOnboarding = status.DaysSinceSignup,
            // Dynamic content based on status
            Cta = GetNextStepCta(status)
        };

        await email.SendTemplateAsync(user.Email, templateId, data);
    }
}
```

## Best Practices

```text
Onboarding Best Practices:
+------------------------------------------------------------------+
| Practice                    | Impact                             |
+-----------------------------+------------------------------------+
| Reduce signup friction      | +25% conversion                    |
| Progressive disclosure      | -50% cognitive load                |
| Personalized paths          | +40% activation                    |
| Quick win in first session  | +30% day-1 retention               |
| Onboarding checklist        | +45% completion rate               |
| In-context guidance         | -60% support tickets               |
| Smart defaults              | +35% setup completion              |
+-----------------------------+------------------------------------+
```

## Anti-Patterns

| Anti-Pattern | Problem | Solution |
| ------------ | ------- | -------- |
| Feature tour upfront | Users forget before using | Contextual guidance |
| All fields required | Signup abandonment | Minimal signup, defer rest |
| No progress indicator | Users feel lost | Show progress, celebrate wins |
| Generic experience | Low engagement | Personalize based on intent |
| Block until complete | Frustration | Allow exploration, gentle nudges |
| Email before value | Perceived spam | Email after value delivered |

## References

Load for detailed implementation:

- `references/onboarding-flows.md` - Flow diagrams and patterns
- `references/activation-metrics.md` - Metrics framework and benchmarks

## Related Skills

- `subscription-models` - Trial to paid conversion
- `team-management-ux` - Team invitation flows
- `entitlements-management` - Feature gating during trial

## MCP Research

For current onboarding patterns:

```text
perplexity: "SaaS onboarding best practices 2024" "product-led growth activation"
```
