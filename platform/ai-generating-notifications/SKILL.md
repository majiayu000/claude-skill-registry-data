---
name: ai-generating-notifications
description: Generate smart notification messages from structured events using AI. Use when writing push notification copy, creating alert messages from events, building weekly digest emails, summarizing incidents from logs, personalizing notification text, generating Slack alerts from system events, smart email subject lines, aggregating multiple events into one digest message, notification copy for mobile apps, incident summary notifications, AI-powered alert messages, context-aware push notifications.
---

# Build an AI Notification Generator

Guide the user through building AI that turns structured events into useful, channel-appropriate notification messages. Uses DSPy to produce consistent, personalized notification copy with urgency calibration and digest aggregation.

## Step 1: Understand the notification task

Ask the user:
1. **What events trigger notifications?** (system alerts, user activity, scheduled digests, thresholds crossed?)
2. **What channels do you target?** (push/iOS/Android, email, Slack, SMS?)
3. **Do you need personalization?** (user name, role, preferences, history?)
4. **Real-time or digest?** (one notification per event, or aggregate multiple events into one message?)

## Step 2: Build a single-event notifier

### Basic signature

```python
import dspy
from typing import Literal

lm = dspy.LM("openai/gpt-4o-mini")  # or "anthropic/claude-sonnet-4-5-20250929", etc.
dspy.configure(lm=lm)

class GenerateNotification(dspy.Signature):
    """Write a clear, concise notification message for the target channel and recipient."""
    event: str = dspy.InputField(desc="Structured event data or description")
    recipient_profile: str = dspy.InputField(desc="Who receives the notification - role, name, preferences")
    channel: Literal["push", "email", "slack", "sms"] = dspy.InputField(desc="Delivery channel")
    notification_text: str = dspy.OutputField(desc="The notification message, respecting channel length limits")
    urgency_level: Literal["low", "medium", "high", "critical"] = dspy.OutputField(
        desc="Urgency level - low=informational, medium=needs attention, high=act soon, critical=act now"
    )

notifier = dspy.ChainOfThought(GenerateNotification)

result = notifier(
    event="User account login from new device - IP 203.0.113.42, Berlin, Germany",
    recipient_profile="Account owner, security-conscious, email preferred",
    channel="email",
)
print(result.notification_text)
print(result.urgency_level)
```

## Step 3: Channel-specific constraints

Each channel has hard limits. Define them explicitly and enforce with a reward function.

| Channel | Title limit | Body limit | Format |
|---------|-------------|------------|--------|
| Push (iOS/Android) | 50 chars | 100 chars | Plain text |
| Email | ~60 chars subject | 1-3 short paragraphs | HTML or plain |
| Slack | N/A | ~500 chars | Markdown blocks |
| SMS | N/A | 160 chars total | Plain text only |

```python
CHANNEL_LIMITS = {
    "push": 150,    # title + body combined
    "email": 500,   # subject + preview text
    "slack": 500,
    "sms": 160,
}

def channel_length_reward(args, pred):
    """Hard penalty for exceeding channel length limits."""
    limit = CHANNEL_LIMITS.get(args["channel"], 300)
    text_len = len(pred.notification_text)
    if text_len <= limit:
        return 1.0
    # Hard fail above 2x limit, graduated penalty between limit and 2x
    if text_len > limit * 2:
        return 0.0
    return max(0.0, 1.0 - (text_len - limit) / limit)

notifier_enforced = dspy.Refine(
    module=dspy.ChainOfThought(GenerateNotification),
    N=3,
    reward_fn=channel_length_reward,
    threshold=0.9,
)
```

## Step 4: Digest aggregation

Group multiple events into a single summary notification — reduces alert fatigue.

```python
from pydantic import BaseModel, Field

class DigestOutput(BaseModel):
    subject: str = Field(description="Email subject line, max 60 chars")
    headline: str = Field(description="One-sentence summary of the most important event")
    event_groups: list[str] = Field(description="Events grouped by type, e.g. '3 new comments, 2 deployments'")
    call_to_action: str = Field(description="What the user should do next, if anything")

class GenerateDigest(dspy.Signature):
    """Aggregate multiple events into a single digest notification. Group similar events, highlight the most important, and keep it scannable."""
    events: list[str] = dspy.InputField(desc="List of events to include in the digest")
    recipient_profile: str = dspy.InputField(desc="Who receives the digest")
    time_period: str = dspy.InputField(desc="Time window covered - e.g. 'last 24 hours', 'this week'")
    digest: DigestOutput = dspy.OutputField()

class DigestNotifier(dspy.Module):
    def __init__(self):
        self.group = dspy.ChainOfThought("events -> grouped_events: list[str]")
        self.write = dspy.ChainOfThought(GenerateDigest)

    def forward(self, events, recipient_profile, time_period):
        # Group similar events first, then write the digest
        grouped = self.group(events=events).grouped_events
        return self.write(
            events=grouped,
            recipient_profile=recipient_profile,
            time_period=time_period,
        )
```

## Step 5: Urgency calibration

Prevent over-alerting by calibrating urgency against event severity and recipient fatigue.

```python
class CalibrateUrgency(dspy.Signature):
    """Assess the urgency of this event for this recipient. Consider event severity, recipient role, and whether action is required."""
    event: str = dspy.InputField(desc="Event description")
    recipient_profile: str = dspy.InputField(desc="Recipient role and preferences")
    recent_notification_count: int = dspy.InputField(
        desc="Number of notifications sent to this recipient in the last hour"
    )
    urgency_level: Literal["low", "medium", "high", "critical"] = dspy.OutputField()
    should_send: bool = dspy.OutputField(
        desc="False if recipient is already overloaded with high-urgency alerts"
    )
    rationale: str = dspy.OutputField(desc="One sentence explaining the urgency decision")

def urgency_reward(args, pred):
    """Penalize assigning high/critical urgency to clearly informational events."""
    score = 1.0
    informational_keywords = ["viewed", "logged in", "updated preferences", "exported"]
    event_lower = args["event"].lower()
    if any(kw in event_lower for kw in informational_keywords):
        if pred.urgency_level in ("high", "critical"):
            score -= 0.5  # soft: informational events should not be urgent
    return score

urgency_calibrator = dspy.Refine(
    module=dspy.ChainOfThought(CalibrateUrgency),
    N=3,
    reward_fn=urgency_reward,
    threshold=0.8,
)
```

## Step 6: Personalization

Recipient context should influence tone, detail level, and channel preference.

```python
class PersonalizedNotification(dspy.Signature):
    """Write a notification tailored to the recipient. Match tone to their role, include relevant context, and use their preferred channel style."""
    event: str = dspy.InputField(desc="Structured event data")
    recipient_name: str = dspy.InputField(desc="Recipient's name")
    recipient_role: str = dspy.InputField(desc="e.g. 'developer', 'executive', 'end user'")
    recipient_preferences: str = dspy.InputField(
        desc="e.g. 'brief and technical', 'plain language', 'include numbers'"
    )
    channel: Literal["push", "email", "slack", "sms"] = dspy.InputField()
    notification_text: str = dspy.OutputField()
    urgency_level: Literal["low", "medium", "high", "critical"] = dspy.OutputField()
```

**Tone by role example:**

```python
ROLE_HINTS = {
    "developer": "technical details, stack traces welcome, use markdown in Slack",
    "executive": "business impact only, no jargon, one sentence if possible",
    "end_user": "plain language, friendly tone, tell them exactly what to do",
    "on_call": "all relevant details, include timestamp, severity, and system affected",
}
```

## Step 7: Evaluate and optimize

### Notification quality metric

```python
class JudgeNotification(dspy.Signature):
    """Judge the quality of a notification message on clarity, actionability, and channel fit."""
    event: str = dspy.InputField(desc="Original event that triggered the notification")
    channel: str = dspy.InputField()
    notification_text: str = dspy.InputField()
    urgency_level: str = dspy.InputField()
    clarity: float = dspy.OutputField(desc="0.0-1.0 - is the message immediately understandable?")
    actionability: float = dspy.OutputField(desc="0.0-1.0 - does the recipient know what to do?")
    channel_fit: float = dspy.OutputField(desc="0.0-1.0 - is length and format right for the channel?")

def notification_metric(example, prediction, trace=None):
    judge = dspy.Predict(JudgeNotification)
    result = judge(
        event=example.event,
        channel=example.channel,
        notification_text=prediction.notification_text,
        urgency_level=prediction.urgency_level,
    )
    return (result.clarity + result.actionability + result.channel_fit) / 3

optimizer = dspy.BootstrapFewShot(metric=notification_metric, max_bootstrapped_demos=4)
optimized = optimizer.compile(notifier, trainset=trainset)
# Typical improvement: baseline ~0.61 avg score → ~0.83 after BootstrapFewShot with 4 demos
# Channel-fit jumps most (length compliance); actionability gains ~15-20 points
```

## When NOT to use AI notifications

- **Transactional messages** (order confirmations, password resets, receipt emails) — use templates. The text must be exact and predictable; AI adds variability without value.
- **Regulatory or compliance messages** (GDPR notices, financial disclosures, legal alerts) — wording is fixed by requirement; AI-generated copy introduces compliance risk.
- **Simple threshold alerts** ("CPU > 90%", "balance below $10") — a format string is faster, cheaper, and more reliable than an LM call.

## Key patterns

| Pattern | Use when |
|---------|----------|
| `ChainOfThought(GenerateNotification)` | Single event, single channel |
| `DigestNotifier` (GroupEvents + Write) | Multiple events → one message |
| `dspy.Refine` + `channel_length_reward` | Enforcing hard character limits per channel |
| `CalibrateUrgency` | Preventing alert fatigue |
| `PersonalizedNotification` | Different tone/detail for different roles |

## Gotchas

- **Claude generates text that exceeds channel limits.** Passing `max_chars=160` in a field description is not enough — the model treats it as a suggestion. Always wrap with `dspy.Refine` and a programmatic length check reward function that reads `len(pred.notification_text)`.
- **Claude treats all events as equally urgent.** Without explicit calibration, routine events ("user viewed a file") get marked `high` urgency. Add a `CalibrateUrgency` step and a reward function that penalizes over-classification of low-severity events.
- **Claude uses `dspy.Assert`/`dspy.Suggest` for constraints.** Use `dspy.Refine` with a reward function instead — it handles retries with feedback and is the current DSPy pattern for enforcing output constraints.
- **Claude generates generic notifications that ignore recipient context.** Without `recipient_profile` in the signature, every user gets the same message. Always pass name, role, and preferences as inputs to get personalized copy.
- **Claude creates digests by listing events sequentially instead of grouping.** "3 events happened: X, Y, Z" is not a digest — it is a log. Build a separate GroupEvents step before the notification writer to cluster similar events and count them before writing copy.

## Cross-references

> Install any skill: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill <name>`

- Aggregate events intelligently before notifying — see `/ai-summarizing`
- Parse structured event payloads (JSON, logs) before feeding to notifier — see `/ai-parsing-data`
- Score notification quality automatically — see `/ai-scoring`
- Enforce output constraints with retry loops — see `/dspy-refine`
- Sample multiple notification variants and pick the best — see `/dspy-best-of-n`
- Write DSPy signatures for input/output contracts — see `/dspy-modules`
- **Install `/ai-do` if you do not have it** — it routes any AI problem to the right skill and is the fastest way to work: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill ai-do`

## Additional resources

- For worked examples (push notifications, weekly digest, incident Slack alerts), see [examples.md](examples.md)
- For DSPy API signatures, parameter tables, and reward function patterns, see [reference.md](reference.md)
