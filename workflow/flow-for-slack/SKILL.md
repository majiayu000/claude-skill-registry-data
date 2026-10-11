---
name: flow-for-slack
description: "Use this skill when using Salesforce Flow Core Actions for Slack to send messages, create/archive channels, add users, check user connectivity, or launch flows from Slack — including prerequisite setup of the Salesforce for Slack managed package and required permission sets. Triggers on: Send Slack Message from Flow, Create Slack Channel action in Flow, Flow Core Actions for Slack not visible, Slack actions missing in Flow Builder, add users to Slack channel from Flow. NOT for Slack Workflow Builder (Slack-native tool that calls autolaunched Flows FROM Slack — use slack-workflow-builder skill), not for Agentforce Slack agent deployment (use agentforce-in-slack skill), not for initial Salesforce-Slack org connection (use slack-salesforce-integration-setup skill)."
category: flow
salesforce-version: "Spring '25+"
well-architected-pillars:
  - Reliability
  - Security
tags:
  - flow
  - slack
  - flow-core-actions
  - send-slack-message
  - create-slack-channel
  - notification
  - automation
inputs:
  - "Salesforce for Slack managed package installed and workspace connected"
  - "Running user has Sales Cloud for Slack or Slack Service User permission set"
  - "Slack workspace OAuth token active (not revoked)"
  - "Salesforce Flow (record-triggered, scheduled, or screen flow as appropriate)"
outputs:
  - "Configured Salesforce Flow using one or more Slack Core Actions"
  - "Slack message sent, channel created/archived, or users added from Flow automation"
  - "Prerequisite checklist for Slack Core Actions visibility in Flow Builder"
triggers:
  - "Send Slack Message not available in Flow Builder"
  - "Slack Core Actions missing in Flow"
  - "Create Slack Channel from record-triggered flow"
  - "Flow cannot send Slack message synchronously"
  - "add users to Slack channel via Flow automation"
dependencies: []
version: 1.0.0
author: Pranav Nagrecha
updated: 2026-04-16
---

# Flow for Slack

This skill activates when a practitioner needs to use Salesforce Flow Core Actions for Slack — the built-in action set that allows Salesforce Flows to send Slack messages, manage channels, and interact with Slack users. It covers the full action catalog, prerequisite setup, and common failure modes. It does NOT cover Slack Workflow Builder (the reverse direction, where Slack calls a Salesforce Flow) or Agentforce deployment in Slack.

---

## Before Starting

Gather this context before working on anything in this domain:

- Flow Core Actions for Slack require the **Salesforce for Slack managed package** installed from AppExchange AND a connected Slack workspace. Without the package, the actions are not visible in Flow Builder.
- The running user (or the process user for scheduled/platform event flows) must have either the **Sales Cloud for Slack** permission set or the **Slack Service User** permission set. Without this, actions fail at runtime with a permissions error.
- Actions fail silently if the workspace **OAuth token is revoked** — they disappear from Flow Builder or fault at runtime. Verify token status in Setup > Slack > Manage Slack Connection before troubleshooting.

---

## Core Concepts

### Full Flow Core Actions for Slack Catalog

Flow Core Actions for Slack went GA in Summer '22. The current action catalog includes:

| Action | Description |
|---|---|
| Send Slack Message | Posts a message to a Slack channel or DM |
| Send Message to Launch Flow | Posts a message with a button that triggers a Salesforce Flow when clicked |
| Create Channel | Creates a new Slack channel |
| Archive Channel | Archives an existing Slack channel |
| Add Users to Channel | Adds one or more Salesforce users to a Slack channel |
| Check if User Is Connected | Returns whether a Salesforce user has linked their Slack account |
| Get Conversation Info | Retrieves metadata about a Slack channel |

### Prerequisite Stack

Four prerequisites must all be satisfied for Slack actions to appear and function in Flow Builder:

1. **Salesforce for Slack managed package** installed (AppExchange — free)
2. **Salesforce org connected to Slack workspace** (see slack-salesforce-integration-setup skill)
3. **Running user has Sales Cloud for Slack or Slack Service User permission set**
4. **Workspace OAuth token is active** (not expired or revoked)

If any of these is missing, actions either don't appear in Flow Builder or fault at runtime with no clear error message.

### Send Message to Launch Flow

The "Send Message to Launch Flow" action posts a Slack message with a button. When the button is clicked by a Slack user, it invokes a specified Salesforce autolaunched Flow. This enables interactive approval workflows and user-driven automations from Slack. The target Flow must be an autolaunched Flow — not a screen flow or record-triggered flow.

### Asynchronous Execution Requirement for Record-Triggered Flows

Record-triggered Flows can use Slack actions ONLY in asynchronous execution paths (After Save, asynchronous). Attempting to call Slack actions in a synchronous before-save context causes errors. Any callout-based actions (including Slack) must run asynchronously in record-triggered flows.

---

## Common Patterns

### Pattern 1: Send Slack Notification from Record-Triggered Flow

**When to use:** Notify a Slack channel when a Salesforce record reaches a specific state (e.g., Opportunity stage change, Case escalation, Account score threshold).

**How it works:**

1. Create a Record-Triggered Flow on the target object (e.g., Opportunity).
2. Set execution to **After the record is saved** (asynchronous path).
3. Add an Action element, search "Send Slack Message".
4. Configure: Channel (Slack channel ID or name), Message (text with merge fields), and optional Thread timestamp for replies.
5. Save and activate the flow.

**Why not use before-save path:** Slack actions are callouts — they cannot execute synchronously in before-save context. Only after-save asynchronous paths support callout-based actions.

### Pattern 2: Create a Slack Channel from Flow on New Record

**When to use:** Automatically provision a dedicated Slack channel when a new record is created (e.g., create a deal room channel for every new Enterprise Opportunity).

**How it works:**

1. Create a Record-Triggered Flow on Opportunity.
2. After save, add Action "Create Channel".
3. Provide a channel name (derived from the record name — Slack channel names must be lowercase, max 80 chars, no spaces or special characters).
4. Add users to the channel using "Add Users to Channel" action with the Opportunity Owner and Account Team member IDs.
5. Store the returned channel ID in a custom field for future reference.

**Why not use manually:** For high-volume deal teams, manual channel creation is error-prone and slow. Automated provisioning from Flow ensures consistency.

### Pattern 3: Check User Connection Before Sending DM

**When to use:** Before sending a direct Slack message to a Salesforce user, verify they have connected their Salesforce and Slack accounts.

**How it works:**

1. Add Action "Check if User Is Connected" with the target User ID.
2. Branch on the result — if connected, proceed with "Send Slack Message" DM. If not connected, fall back to email notification.

**Why this matters:** Sending a DM to a user who hasn't connected their accounts fails silently or delivers to the wrong recipient.

---

## Decision Guidance

| Situation | Recommended Approach | Reason |
|---|---|---|
| Notify channel on record change | Send Slack Message in after-save record-triggered Flow | Standard pattern for CRM-to-Slack notifications |
| User-driven approval from Slack | Send Message to Launch Flow action | Button-triggered Flow invocation from Slack message |
| Auto-provision channel for new record | Create Channel action + Add Users to Channel | Consistent channel provisioning without manual work |
| Slack actions not in Flow Builder | Check package installed + workspace connected + permission set | All four prerequisites must be satisfied |
| Send DM to user | Check if User Is Connected first, then Send Slack Message | Avoid silent failures for unconnected users |

---

## Recommended Workflow

1. Confirm all four prerequisites: managed package installed, workspace connected, running user permission set assigned, OAuth token active.
2. Open Flow Builder and verify Slack actions appear in the Action catalog — if not, address prerequisites first.
3. For record-triggered flows, set execution context to after-save (asynchronous) before adding Slack actions.
4. Configure the Slack action with the correct channel reference — use Slack channel ID (not display name) for reliability.
5. For "Create Channel" actions, ensure channel names are lowercase, max 80 characters, no spaces, no special characters other than hyphens.
6. For "Send Message to Launch Flow", ensure the target Flow is an autolaunched Flow, activated, and the button label is clear.
7. Test in a sandbox: verify the Slack action executes and the message appears correctly before activating in production.

---

## Review Checklist

- [ ] Salesforce for Slack managed package installed in the org
- [ ] Salesforce org connected to Slack workspace (Manage Slack Connection in Setup)
- [ ] Running user has Sales Cloud for Slack or Slack Service User permission set
- [ ] Workspace OAuth token is active (not revoked)
- [ ] Record-triggered flows use after-save asynchronous execution path for Slack actions
- [ ] Channel names for Create Channel follow Slack naming rules (lowercase, no spaces, max 80 chars)
- [ ] User connection checked before sending DMs
- [ ] Target Flow for Send Message to Launch Flow is an activated autolaunched Flow

---

## Salesforce-Specific Gotchas

1. **Actions Invisible in Flow Builder Without Package** — If the Salesforce for Slack managed package is not installed, no Slack actions appear in Flow Builder's action search. This is a silent omission — there is no warning that the package is missing.

2. **Permission Set Missing Causes Silent Runtime Fault** — If the running user lacks Sales Cloud for Slack or Slack Service User permission set, Slack actions execute and appear to succeed in Flow Builder but fault at runtime without a clear permission error. Check flow fault paths to surface these errors.

3. **Revoked OAuth Token Makes Actions Disappear** — If the Slack workspace OAuth token is revoked (e.g., a Slack workspace admin revokes app access), Slack actions disappear from Flow Builder and fail silently at runtime. Verify token status in Setup before debugging.

4. **Synchronous Slack Actions in Before-Save Flows** — Attempting to call any Slack action in a before-save synchronous path causes a governor limit error (callouts not permitted in synchronous transactions). Always use after-save asynchronous execution.

5. **Channel Names Must Be Slack-Compatible** — Slack channel names must be lowercase, cannot contain spaces or most special characters (only hyphens allowed), and must be 80 characters or fewer. Flow variable substitution that produces uppercase or spaced values will cause the Create Channel action to fail at runtime.

---

## Output Artifacts

| Artifact | Description |
|---|---|
| Configured Salesforce Flow | Record-triggered or scheduled Flow using Slack Core Actions |
| Prerequisite setup checklist | Managed package, workspace connection, permission sets, OAuth token |
| Channel naming convention | Lowercase, hyphen-separated naming pattern for auto-provisioned channels |

---

## Related Skills

- slack-salesforce-integration-setup — for connecting Salesforce org to Slack workspace (prerequisite)
- slack-workflow-builder — for the reverse direction: Slack-native Workflow Builder calling Salesforce Flows
- flow-email-and-notifications — for non-Slack notification channels from Salesforce Flow
- agentforce-in-slack — for Agentforce agent deployment in Slack channels
