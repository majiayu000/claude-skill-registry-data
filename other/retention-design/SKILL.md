---
name: retention-design
description: >
  Design retention and engagement features using the Hook Model. Use when the user says
  "improve retention", "reduce churn", "make it habit-forming", "engagement design",
  "hook model", "trigger action reward", "users aren't coming back", "increase DAU/MAU",
  or wants to design features that bring users back repeatedly
  - even if they don't explicitly say "Hook Model".
---

## Overview

Based on **Hooked** by Nir Eyal. The Hook Model is a four-phase loop that drives habit formation in products. Habits require frequent, perceived utility, and a degree of pain when the habit is disrupted. Products that become habits are harder to churn from - not because users are locked in, but because the product genuinely fills a need they return to automatically.

The four phases: **Trigger - Action - Variable Reward - Investment**

Use this skill ethically. Eyal's own caveat: design habits for products that genuinely improve users' lives. Manipulating users into unhealthy habits is both wrong and unsustainable.

## Workflow

### Step 1: Define the habit you want to create
What behavior should become automatic?
- Frequency target: daily / weekly / monthly?
- Context: when and where does this behavior occur?
- Current alternative: what do users do today instead?

### Step 2: Design the Trigger
Triggers prompt action. Two types:
- **External triggers** - notifications, emails, badges, prompts (used early in habit formation)
- **Internal triggers** - emotions or situations that cue the behavior automatically ("I feel anxious - I open [app]")

The goal: move users from external to internal triggers over time.

For your feature: what external trigger will prompt first use? What internal trigger will sustain it?

### Step 3: Design the Action
Eyal's formula: **Motivation + Ability + Trigger = Action**

Reduce friction on the action:
- How many steps to complete the action?
- What's the minimum viable action? (e.g. one tap, not a form)
- Where does motivation need to be highest? Remove barriers there.

Fogg's six elements of simplicity: time, money, physical effort, brain cycles, social deviation, non-routine. Reduce the one that's the biggest barrier.

### Step 4: Design the Variable Reward
Variable rewards drive repeat behavior (Skinner's research). Three types:
- **Rewards of the tribe** - social validation, belonging (likes, comments, leaderboards)
- **Rewards of the hunt** - seeking resources or information (feed, search results, deals)
- **Rewards of the self** - mastery, completion, consistency (streaks, progress bars, achievements)

Key: variability is what makes rewards compelling. Predictable rewards lose their pull. Design for some uncertainty in the reward.

### Step 5: Design the Investment
Investment makes users more likely to return. Four forms:
- **Data** - users store value (photos, notes, history)
- **Content** - users create things (posts, lists, playlists)
- **Followers** - social capital that exists only in your product
- **Reputation/skill** - progress that would be lost by leaving

Investment also loads the next trigger: "You have 3 unread notifications" brings users back.

### Step 6: Map the full Hook loop
Draw the loop explicitly:

```
Trigger     -> [what prompts the behavior]
Action      -> [the simplest behavior]
Reward      -> [what the user gets, with some uncertainty]
Investment  -> [what the user puts in that makes them return]
             -> Next Trigger: [how investment loads the next trigger]
```

### Step 7: Ethical check
Before shipping: would you be comfortable if users knew exactly how you designed this? Would you use this product yourself? Would you recommend it to someone you care about?

## Anti-Patterns

**1. Designing triggers without investment**
Bad: Sending notifications that bring users in but give them nothing to do.
Good: Every trigger should lead to an action that builds investment.

**2. Predictable rewards**
Bad: "You earned 10 points" every single time.
Good: Variable - sometimes 10 points, sometimes a badge, sometimes a streak milestone. Variability sustains engagement.

**3. Investment that traps instead of enriches**
Bad: Making it painful to leave (dark patterns, data hostage-taking).
Good: Investment that genuinely improves the product for the user over time.

**4. External triggers forever**
Bad: Users still need a push notification to open the app after 6 months.
Good: Design toward internal triggers. If users don't develop internal triggers, the habit hasn't formed.

## Quality Checklist

- [ ] Habit defined: behavior, frequency, context
- [ ] External trigger designed for acquisition
- [ ] Internal trigger identified for sustained habit
- [ ] Action reduced to minimum friction
- [ ] Variable reward designed (not fixed/predictable)
- [ ] Investment mechanism builds value users would lose by leaving
- [ ] Full Hook loop mapped explicitly
- [ ] Ethical check passed
