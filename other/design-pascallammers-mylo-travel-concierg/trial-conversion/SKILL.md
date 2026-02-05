---
name: trial-conversion
description: Trial optimization and conversion patterns for SaaS. Covers trial design, activation metrics, conversion funnels, and win-back strategies.
allowed-tools: Read, Glob, Grep, Task, mcp__perplexity__search, mcp__perplexity__reason
---

# Trial Conversion Skill

## When to Use This Skill

Use this skill when:

- **Trial Conversion tasks** - Working on trial optimization and conversion patterns for saas. covers trial design, activation metrics, conversion funnels, and win-back strategies
- **Planning or design** - Need guidance on Trial Conversion approaches
- **Best practices** - Want to follow established patterns and standards

## Overview

Patterns for optimizing trial-to-paid conversion in SaaS applications.

Trial conversion is the critical transition from free to paid. This skill covers trial design strategies, activation metrics, conversion optimization, and win-back campaigns for expired trials.

## Trial Models

```text
+------------------------------------------------------------------+
|                      Trial Types                                  |
+------------------------------------------------------------------+
| Type           | Duration | Payment Req | Conversion |           |
+----------------+----------+-------------+------------+-----------+
| Free Trial     | 7-30 days| No          | 15-25%     | Low risk  |
| Credit Card    | 7-14 days| Yes (no chg)| 40-60%     | Higher    |
| Freemium       | Forever  | No          | 2-5%       | Volume    |
| Reverse Trial  | Start Pro| No          | 25-35%     | New model |
+----------------+----------+-------------+------------+-----------+
```

## Conversion Funnel

```text
+------------------------------------------------------------------+
|                    Trial Conversion Funnel                        |
+------------------------------------------------------------------+
|                                                                   |
|  Signup    Activation   Engagement    Conversion   Expansion      |
|  100%   →    60%     →    40%     →    25%     →    10%          |
|    |          |           |            |            |             |
|    v          v           v            v            v             |
|  Register   First      Weekly      Payment    Upgrade/           |
|  Account    Value      Usage       Complete   Add Seats          |
|                                                                   |
+------------------------------------------------------------------+
```

## Activation Metrics

### Define Your Activation Event

```csharp
public sealed class ActivationService(
    IDbContext db,
    IEventPublisher events)
{
    // Define what "activated" means for your product
    private static readonly ActivationCriteria[] Criteria =
    [
        new("profile_complete", 1),
        new("first_project_created", 1),
        new("first_task_added", 3),
        new("team_member_invited", 1)
    ];

    public async Task<ActivationStatus> GetStatusAsync(
        Guid userId,
        CancellationToken ct)
    {
        var user = await db.Users
            .Include(u => u.ActivationEvents)
            .FirstOrDefaultAsync(u => u.Id == userId, ct);

        if (user == null)
            return ActivationStatus.NotFound();

        var completedCriteria = Criteria.Count(c =>
            user.ActivationEvents.Count(e => e.EventType == c.EventType) >= c.RequiredCount);

        var progress = (decimal)completedCriteria / Criteria.Length * 100;

        return new ActivationStatus
        {
            UserId = userId,
            IsActivated = completedCriteria == Criteria.Length,
            ProgressPercent = progress,
            CompletedCriteria = completedCriteria,
            TotalCriteria = Criteria.Length,
            RemainingCriteria = Criteria
                .Where(c => user.ActivationEvents.Count(e => e.EventType == c.EventType) < c.RequiredCount)
                .Select(c => c.EventType)
                .ToList()
        };
    }

    public async Task TrackEventAsync(
        Guid userId,
        string eventType,
        CancellationToken ct)
    {
        db.ActivationEvents.Add(new ActivationEvent
        {
            UserId = userId,
            EventType = eventType,
            Timestamp = DateTimeOffset.UtcNow
        });
        await db.SaveChangesAsync(ct);

        // Check if this triggered activation
        var status = await GetStatusAsync(userId, ct);
        if (status.IsActivated)
        {
            await events.PublishAsync(new UserActivatedEvent(userId), ct);
        }
    }
}
```

### Key Metrics

```text
Trial Metrics to Track:
+------------------------------------------------------------------+
| Metric                      | Formula                   | Target  |
+-----------------------------+---------------------------+---------+
| Signup Rate                 | Signups / Visitors        | > 5%    |
| Activation Rate             | Activated / Signups       | > 40%   |
| Trial Completion Rate       | Full Trial / Signups      | > 60%   |
| Conversion Rate             | Paid / Trials             | > 20%   |
| Time to Activation          | Median days to activate   | < 3 days|
| Days to Convert             | Median days to payment    | < 10    |
| Revenue per Trial           | Revenue / Total Trials    | $ varies|
+-----------------------------+---------------------------+---------+
```

## Conversion Optimization

### Trial Length Optimization

```text
Trial Length Considerations:
+------------------------------------------------------------------+
| Length  | Pros                    | Cons                         |
+---------+-------------------------+------------------------------+
| 7 days  | Urgency, faster revenue | May not see full value       |
| 14 days | Good balance            | Standard, expected           |
| 30 days | Full evaluation         | Forgetting, less urgency     |
+---------+-------------------------+------------------------------+

Recommendation: Start with 14 days, adjust based on time-to-activation data
```

### Trial Nudges

```csharp
public sealed class TrialNudgeService(
    IUserRepository users,
    INotificationService notifications,
    IActivationService activation)
{
    public async Task SendNudgesAsync(CancellationToken ct)
    {
        var trialUsers = await users.GetTrialUsersAsync(ct);

        foreach (var user in trialUsers)
        {
            var status = await activation.GetStatusAsync(user.Id, ct);
            var daysRemaining = (user.TrialEndsAt - DateTimeOffset.UtcNow).Days;

            // Non-activated users
            if (!status.IsActivated)
            {
                await SendActivationNudgeAsync(user, status, ct);
            }
            // Trial ending soon
            else if (daysRemaining <= 3)
            {
                await SendConversionNudgeAsync(user, daysRemaining, ct);
            }
        }
    }

    private async Task SendActivationNudgeAsync(
        User user,
        ActivationStatus status,
        CancellationToken ct)
    {
        var nextStep = status.RemainingCriteria.FirstOrDefault();
        if (nextStep == null) return;

        await notifications.SendAsync(new ActivationNudge
        {
            UserId = user.Id,
            NextStep = nextStep,
            ProgressPercent = status.ProgressPercent
        }, ct);
    }
}
```

### Trial Extension Strategy

```csharp
public sealed class TrialExtensionService(
    IDbContext db,
    ITenantRepository tenants)
{
    public async Task<ExtensionResult> RequestExtensionAsync(
        Guid tenantId,
        string reason,
        CancellationToken ct)
    {
        var tenant = await tenants.GetAsync(tenantId, ct);
        if (tenant == null)
            return ExtensionResult.NotFound();

        if (tenant.TrialExtensionCount >= 1)
            return ExtensionResult.MaxExtensionsReached();

        // Extend by 7 days
        tenant.TrialEndsAt = tenant.TrialEndsAt!.Value.AddDays(7);
        tenant.TrialExtensionCount++;
        tenant.TrialExtensionReason = reason;

        await db.SaveChangesAsync(ct);

        return ExtensionResult.Success(tenant.TrialEndsAt.Value);
    }
}
```

## Win-Back Campaigns

### Expired Trial Recovery

```csharp
public sealed class WinBackService(
    IUserRepository users,
    IEmailService email)
{
    public async Task SendWinBackCampaignAsync(CancellationToken ct)
    {
        // Users whose trial expired in last 30 days
        var expiredUsers = await users.GetExpiredTrialsAsync(
            since: DateTimeOffset.UtcNow.AddDays(-30),
            ct);

        foreach (var user in expiredUsers)
        {
            var daysSinceExpiry = (DateTimeOffset.UtcNow - user.TrialEndedAt!.Value).Days;

            var campaign = daysSinceExpiry switch
            {
                <= 3 => "expired_3day",
                <= 7 => "expired_7day_discount",
                <= 14 => "expired_14day_extension",
                <= 30 => "expired_30day_survey",
                _ => null
            };

            if (campaign != null)
            {
                await email.SendTemplateAsync(user.Email, campaign, new
                {
                    user.Name,
                    DiscountCode = GenerateDiscountCode(user.Id),
                    ExtensionDays = 7
                }, ct);
            }
        }
    }
}
```

### Win-Back Email Sequence

```text
Win-Back Email Sequence:
+------------------------------------------------------------------+
| Day  | Email                           | Offer                   |
+------+---------------------------------+-------------------------+
| 1    | "We miss you"                   | None (value reminder)   |
| 3    | "Here's what you're missing"    | 20% off first month     |
| 7    | "Extended trial offer"          | 7 more days free        |
| 14   | "Quick question"                | Survey + 30% off annual |
| 30   | "Final offer"                   | 40% off if return today |
+------+---------------------------------+-------------------------+
```

## Pricing Psychology

### Trial-to-Paid Friction Reduction

```text
Reduce Conversion Friction:
1. Pre-fill billing from trial signup
2. Show value delivered during trial
3. Offer annual discount at conversion
4. Allow feature downgrade (cheaper plan)
5. Grace period after trial (don't cut off immediately)
6. Saved data guarantee
```

### Discount Strategies

```csharp
public sealed class ConversionDiscountService(ITenantContext tenant)
{
    public ConversionOffer GetBestOffer()
    {
        return tenant.Current switch
        {
            // Highly engaged - no discount needed
            { ActivationScore: > 80 } => new ConversionOffer(0, "full_price"),

            // Engaged but not converted - small nudge
            { ActivationScore: > 50 } => new ConversionOffer(10, "engaged_10off"),

            // At risk - bigger discount
            { ActivationScore: > 20 } => new ConversionOffer(20, "atrisk_20off"),

            // Likely to churn - significant discount
            _ => new ConversionOffer(30, "winback_30off")
        };
    }
}
```

## A/B Testing

### Conversion Experiments

```text
High-Impact Trial Experiments:
+------------------------------------------------------------------+
| Experiment              | Test Variable    | Typical Impact      |
+-------------------------+------------------+---------------------+
| Trial length            | 7 vs 14 vs 30    | 10-30% conversion   |
| CC required             | Yes vs No        | 2-3x conversion     |
| Onboarding flow         | Guided vs open   | 20-40% activation   |
| Feature limits          | Strict vs loose  | Varies              |
| Email frequency         | 3 vs 7 emails    | 10-20% conversion   |
| Discount offer timing   | Day 10 vs 12     | 5-15% conversion    |
+-------------------------+------------------+---------------------+
```

## Best Practices

```text
Trial Conversion Best Practices:
+------------------------------------------------------------------+
| Practice                    | Benefit                            |
+-----------------------------+------------------------------------+
| Clear activation criteria   | Know what to optimize              |
| Instrument everything       | Data-driven decisions              |
| Early value delivery        | Higher activation                  |
| Personalized nudges         | Higher engagement                  |
| Multiple conversion points  | Capture when ready                 |
| Graceful trial end          | Preserve goodwill                  |
+-----------------------------+------------------------------------+
```

## Anti-Patterns

| Anti-Pattern | Problem | Solution |
| ------------ | ------- | -------- |
| Too long trial | Users forget | 14 days optimal |
| Immediate cutoff | Lost goodwill | Grace period |
| No nurturing | Low activation | Email sequence |
| Generic messaging | Low engagement | Personalize |
| Single conversion point | Missed opportunities | Multiple CTAs |

## Related Skills

- `self-service-onboarding` - Trial onboarding flow
- `subscription-models` - Pricing strategy
- `tenant-lifecycle` - Trial state management

## MCP Research

For current patterns:

```text
perplexity: "SaaS trial conversion optimization 2024" "freemium vs free trial conversion rates"
```
