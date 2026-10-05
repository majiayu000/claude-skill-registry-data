---
name: sift-sequences
description: Complete guide for creating, managing, and ideating Sift sequences (automations). Use when user needs help setting up sequences, understanding sequence triggers/conditions/actions, troubleshooting sequences, designing automation workflows, or understanding how Events, Tasks, Sequences, and Drip Campaigns work together in Sift.
---

# Sift Sequences

Sequences are automations in Sift that trigger actions when specific events occur. They ensure no lead slips through the cracks by automatically creating tasks, changing statuses, moving cards, and sending notifications.

## Quick Reference

| Component | Purpose | Required |
|-----------|---------|----------|
| Trigger | Event that starts the automation | Yes |
| Condition | Additional rules that must be met | No |
| Action | What happens when triggered | Yes |

## When to Use This Skill

Use this skill when the user wants to:
1. **Create** a new sequence from scratch
2. **Ideate** sequence workflows for their business
3. **Troubleshoot** why a sequence is not working
4. **Understand** how sequences interact with SiftLine, tasks, and statuses
5. **Learn** how Events, Tasks, Sequences, and Drip Campaigns work together

## The Sift Automation Ecosystem

Understanding how the four core components work together is essential before building sequences.

### How Events, Tasks, Sequences, and Drip Campaigns Connect

| Component | What It Is | How It Connects |
|-----------|-----------|-----------------|
| **Events** | Container for Tasks and Appointments in your account | Tasks created by sequences appear here |
| **Tasks** | Individual action items with deadlines | Created manually or automatically via sequences |
| **Task Presets** | Reusable task templates | Used by sequences to auto-create consistent tasks |
| **Sequences** | Automations triggered by status/card/tag changes | Create tasks, move cards, add to drip campaigns |
| **Drip Campaigns** | Delayed SMS/Email sequences over time | Added to records via sequence actions |

### The Integration Flow

```
Status Change → Sequence Triggers → Creates Task (from Preset) → Task appears in Events
                                 → Adds to Drip Campaign → Drip sends SMS/Email over days
                                 → Moves Card on SiftLine

Task Completed → Can trigger another Sequence → Creates next Task in chain
```

### Events Section Overview

The **Events** section of Sift is where you manage all appointments and tasks. Key features:

| Feature | Description |
|---------|-------------|
| All Events Tab | View appointments and tasks combined |
| Filtering | Filter by date range, assigned user, or assigner |
| Task Presets | Access reusable task templates |
| Google Calendar | Sync appointments and tasks with your calendar |

**Appointments vs. Tasks**: Appointments include a location and outcome tracking. Tasks are action items with deadlines and recurrence options.

For complete Events documentation, see: `references/events-overview.md`

---

## Default Account Setup (Accounts Created After 4/16/2025)

**Important**: Default accounts include pre-built sequences, task presets, and boards. Understanding what comes included versus what you need to build yourself prevents confusion.

### What's INCLUDED in Default Accounts

| Category | Included Items |
|----------|---------------|
| **SiftLine Boards** | Lead Management, Acquisitions, Transactions, Wholesale, Flips, Rentals |
| **Sequences** | Lead Management, Acquisitions, and Transactions automations |
| **Task Presets** | Call New Lead, No Contact New Lead, Nurture New Lead, Cold/Warm/Hot Follow-up, Make Offer, Offer Follow-Up, Send Back to LM |
| **Filter Presets** | My Tasks, Acquisitions, Lead Management, Transactions, REISift Base Presets |
| **Property Statuses** | New Lead, No Contact New Lead, Cold/Warm/Hot Lead, Ghosting Lead, Dead Lead, Not Interested, Listed, Sold, Under Contract, Closed |

### Default Task Presets Discovery

When recommending a starting point, explain what each default task preset does:

| Task Preset | Purpose | Default Due | Frequency |
|-------------|---------|-------------|-----------|
| Call New Lead | Initial contact with new lead | Same day | Once |
| No Contact New Lead | Follow-up when lead hasn't responded | 3-5 days | Daily |
| Nurture New Lead | Long-term nurture for unqualified leads | 3-6 months | Weekly |
| Cold Follow-up | Re-engage cold leads | 45 days | Every 45 days |
| Warm Follow-up | Maintain warm lead relationships | 14 days | Every 14 days |
| Hot Follow-up | Aggressive follow-up for hot leads | 7 days | Every 7 days |
| Make Offer | Present offer to qualified lead | Same day | Once |
| Offer Follow-Up | Follow up after offer presented | 1-2 days | Daily |
| Send Back to LM | Return declined offers to Lead Management | 1 day | Once |

### What's NOT INCLUDED (Must Build Yourself)

**Clarification**: The following are recommended patterns from this skill documentation, NOT pre-built defaults:

| Pattern | Description | Why Build It |
|---------|-------------|--------------|
| Follow-up chain sequences (HOT A01-A16) | Task completion triggers next task | Creates automated cadence without manual intervention |
| Custom temperature cadences | Specific timing for your market | Tailors follow-up frequency to your business |
| Board-to-board workflows | Duplicate cards between boards | Tracks KPIs across workflow stages |
| Conditional routing | Route leads based on tags/value | Assigns high-value leads to senior team members |
| Drip campaign triggers | Add to drips on status change | Automates long-term nurture sequences |

---

## Core Philosophy

Sequences should be **rewards for consistency**, not crutches for forgetfulness. The recommended approach:
1. Get consistent with a manual process first
2. Prove the process works
3. Then automate with sequences to save time

---

## Sequence Anatomy

### Triggers (Required)

The event that starts the automation:

| Trigger | Use When |
|---------|----------|
| Property Status Change | Lead status updates (most common) |
| Property Assignee Change | Ownership transfers |
| Property Tags Added/Removed | Tag-based workflows |
| Property Lists Added/Removed | List membership changes |
| Task Created/Completed | Task-driven workflows |
| SiftLine Card Created | New cards on boards |
| SiftLine Card Moved | Cards change phases |

### Conditions (Optional)

Additional rules that filter when the action executes:

| Condition | Example |
|-----------|---------|
| Property Status Change | From "Any" to "New Lead" |
| Property Assignee | Assignee is specific user |
| Property Tags | Has or doesn't have specific tags |
| Property Lists | On or not on specific lists |
| Card Board & Column | Card is on specific board/phase |
| SiftLine Card Moved | From specific board/phase to another |

### Actions (Required)

What happens when trigger fires and conditions are met:

| Action | Common Use |
|--------|------------|
| Change Property Status | Update lead temperature |
| Assign Property | Route to team member (supports round-robin) |
| Add/Remove Property Tags | Categorization |
| Add/Remove Property Lists | List management |
| Clear Property Tasks | Reset task slate |
| Create New Task | Assign follow-up work |
| Create New Card | Add to SiftLine board |
| Move/Duplicate/Delete Card | SiftLine workflow automation |
| Send SMS/Email | Immediate notifications (leads only) |
| Add to Drip Campaign | Long-term nurture |

---

## Creating a Sequence

1. Navigate to Sequences in left sidebar
2. Click "Create New Sequence"
3. Add Trigger (drag and drop)
4. Add Condition if needed (drag and drop)
5. Add Action(s) (drag and drop)
6. Name the sequence
7. Select folder
8. Click "Save Sequence"

To edit existing default sequences: Open sequence folder → Click sequence name → Select "Make Changes" → Edit → Save Sequence

---

## Recommended Starting Points

When helping users get started, provide discovery about what they already have and what they need to build.

### Starting Point 1: Use Default Sequences As-Is

**Best for**: New users who want to test the system before customizing.

**What you already have**:
- Default sequences for Lead Management, Acquisitions, Transactions
- Task presets that auto-assign based on status changes
- Tasks loop automatically (daily → weekly → ghosting)

**Action**: Review your existing sequences under Sequences page. Toggle them on/off as needed.

### Starting Point 2: Customize Default Sequences

**Best for**: Users who want to adjust timing or assignees.

**What to customize**:
- Task due dates and frequencies
- Assignees (change from Sensei to specific users/roles)
- Round-robin distribution for teams

**Action**: Open each default sequence → Make Changes → Adjust settings → Save.

### Starting Point 3: Build Follow-Up Chain Sequences (Custom Build Required)

**Best for**: Users who want automated task chains where completing one task creates the next.

**What you need to build**: Individual sequences for each step in your cadence. For example, a Hot Lead follow-up chain requires 16 separate sequences (A01 through A16).

**See**: `references/lead-management-sequences.md` for complete configurations.

### Starting Point 4: Build Board-to-Board Workflows (Custom Build Required)

**Best for**: Users who want cards to automatically move/duplicate between boards.

**What you need to build**: Sequences triggered by card movement to transition phases.

**See**: `references/board-workflows.md` for complete configurations.

---

## Common Sequence Patterns

For ready-to-use sequence configurations (that you build yourself), see:
- **Lead Management sequences**: `references/lead-management-sequences.md`
- **Acquisitions sequences**: `references/acquisitions-sequences.md`
- **Board-to-board workflows**: `references/board-workflows.md`
- **Drip campaign integration**: `references/drip-campaigns.md`
- **Sequence ideation framework**: `references/sequence-ideation.md`
- **Events overview**: `references/events-overview.md`

---

## Ideating Sequences

When helping users design sequences, ask these questions:

1. **What event should trigger the automation?**
   - Status change? Card movement? Task completion?

2. **Are there any conditions that must be met?**
   - Only for certain statuses? Specific team members?

3. **What should happen automatically?**
   - Create task? Move card? Send notification?

4. **Who should be assigned?**
   - Specific user? Round-robin? Property assignee?

---

## Troubleshooting

### Sequence Won't Save
- Verify at least one trigger AND one action exist
- Ensure sequence has a name

### Sequence Triggered But Didn't Run
- Large batch triggers may take a few minutes
- Check if other actions are running simultaneously

### Card Not Moving/Adding to Board
- Card may already exist on target board (action skips)
- Verify card is on the expected source board/phase

### Sequence Didn't Run on Upload
- Tag/List triggers only work for manual additions, not uploads
- Use Property Status Change trigger for upload-based automations

### Sequence Loop Error
- Sequences cannot trigger other sequences
- Combine related automations into a single sequence

---

## Sequence Limits by Plan

| Plan | Limit |
|------|-------|
| Essentials (grandfathered) | 3 sequences |
| Professional | 8 sequences |
| Business | Unlimited |

---

## User Permissions

These roles can create/edit sequences:
- Sensei (account owner)
- Super Admin
- Admin
- Marketer

---

## SMS/Email in Sequences

**Important**: SMS and Email actions are for leads only, not cold outreach.

For SMS:
- Requires smrtPhone, Twilio, or Plivo integration
- Use @ variables for personalization

For Email:
- Requires Gmail integration
- Use for confirmed email addresses only

For delayed follow-ups, use Drip Campaigns instead of direct SMS/Email actions.

---

## Drip Campaigns vs. Sequence Actions

| Feature | Sequence SMS/Email | Drip Campaigns |
|---------|-------------------|----------------|
| Timing | Immediate | Delayed (minutes/hours/days) |
| Best For | New lead alerts | Long-term nurture |
| Integration | Any SMS provider | smrtPhone, Twilio, Plivo only |

For complete drip campaign setup, see: `references/drip-campaigns.md`

---

## Viewing Sequence Activity

To see what sequences have run on a record:
1. Open the property record
2. Click "Activity Log"
3. Sequence names appear next to automated updates
