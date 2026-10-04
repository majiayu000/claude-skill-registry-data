---
name: flow-for-slack
description: "Use this skill when using Salesforce Flow Core Actions for Slack to send messages, create/archive channels, add users, check user connectivity, or post a Send Message to Launch Flow button — including the Salesforce for Slack managed package and permission-set prerequisites. Triggers on: Send Slack Message from Flow, Create Slack Channel action in Flow, Flow Core Actions for Slack not visible, Slack actions missing in Flow Builder, add users to Slack channel from Flow. NOT for a Slack-native workflow that calls a Flow FROM Slack — use integration/slack-workflow-builder. NOT for connecting the org to the workspace — use integration/slack-salesforce-integration-setup."
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
  - "flow core actions isn't working"
  - "post a Slack message from a record-triggered flow"
  - "send a Slack button that opens a screen flow"
dependencies: []
version: 1.0.1
author: Pranav Nagrecha
updated: 2026-10-03
---

# Flow for Slack

This skill activates when a practitioner needs Flow Core Actions for Slack: the built-in actions that let a Salesforce flow send Slack messages, manage channels, and work with Slack users. It covers the action catalog, prerequisites, metadata, and common failure modes. It does NOT cover Slack Workflow Builder (Slack calling Salesforce) or Agentforce in Slack.

---

## Before Starting

Gather this context before working on anything in this domain:

- Is **Salesforce for Slack Integrations** enabled? The Slack Integrations guide (Summer '26) describes the setup in Setup > **Slack Apps Setup**: accept terms, enable apps, set permissions, then install the Slack apps from the Slack App Directory with a Slack workspace owner or admin. UNVERIFIED (2026-10-03): this skill's earlier claim that Flow Core Actions need a separate "Salesforce for Slack" managed package from AppExchange is not stated in that guide.
- Do the users involved hold the right permissions? The guide lists the **Connect Salesforce with Slack** system permission (required for most Slack apps), the **Slack Sales User** permission set (Sales Cloud for Slack), and **Connect Salesforce with Slack**, **Slack Service User**, and **Run Flows** for Service Cloud for Slack.
- Which Slack app does the action act through? Some flows need the Sales Cloud for Slack App ID `A028VJ1KG3G` in Flow Builder (Slack Integrations guide, "Automating Actions in Slack").
- Is the org in Government Cloud? Salesforce for Slack apps and integrations aren't supported there.

---

## Questions to Ask Before Configuring

| Question | Why it matters | What a good answer adds | What proper configuration adds over just doing it |
|---|---|---|---|
| Which Slack app and workspace will each action use? | The actions run through a connected Slack app; some flows need the Sales Cloud for Slack App ID. | Fixed app and workspace IDs stored in custom metadata, not typed into every action. | Moving between sandbox and production workspaces is a data change, not a flow edit. |
| Who is the running user, and do they have Connect Salesforce with Slack plus the app's permission set? | Each Slack user, including the workspace owner who adds apps, needs a permission set with Connect Salesforce with Slack on a supported license. | A named integration or automated-process user with the right permissions. | Automations don't fail for users whose license can't hold the permission. |
| Should the message start a guided task in Slack? | Send Message to Launch Flow posts a button that launches a **screen** flow; the flow must be saved with the Slack environment. | Picks plain messaging or an interactive launch. | Recipients complete the task without leaving Slack. |
| Where does the channel name come from, and can it break Slack's rules? | Slack channel names may contain only lowercase letters, numbers, hyphens, and underscores, up to 80 characters. | A formula that normalizes names before Create Slack Channel. | Channel creation doesn't fail on a record name with spaces or capitals. |
| What happens when a Slack action fails? | Failures reach the flow as faults; without a fault path they surface only as flow error emails. | A fault path that logs or alerts. | Revoked apps or missing permissions are noticed the same day. |
| Which record data may appear in Slack? | Slack record detail settings and message content decide what non-Salesforce users in a channel can read. | A field list approved for Slack. | Sensitive fields stay in Salesforce. |

---

## Core Concepts

### Flow Core Actions for Slack Catalog

The Slack Integrations guide lists the actions in the Slack category of Flow Builder. The Metadata API names each one as an `InvocableActionType` value:

| Action (Flow Builder) | `actionType` in Flow metadata | API version |
|---|---|---|
| Send Slack Message | `slackPostMessage` | 54.0 |
| Send Message to Launch Flow | `slackSendMessageToLaunchFlow` | 55.0 |
| Create Slack Channel | `slackCreateChannel` | 54.0 |
| Archive Slack Channel | `slackArchiveChannel` | 54.0 |
| Invite Users to Slack Channel | `slackInviteUsersToChannel` | 54.0 |
| Check If Users Are Connected to Slack | `slackCheckUsersAreConnectedToSlack` | 54.0 |
| Get Information about Slack Conversation | `slackGetConversationInfo` | 54.0 |
| Edit Slack Message | `slackUpdateMessage` | 54.0 |
| Pin or Unpin Slack Message (Beta) | `slackPinMessage` | 54.0 |

API 54.0 is Spring '22; 55.0 is Summer '22.

### Prerequisite Stack

1. Salesforce for Slack Integrations enabled in Slack Apps Setup.
2. The relevant Salesforce Slack app installed in the workspace from the Slack App Directory.
3. Users mapped and connected (users add the app to their Slack sidebar and connect their Salesforce account).
4. Permissions: Connect Salesforce with Slack, plus the app's permission set (Slack Sales User or Slack Service User), plus Run Flows where the app requires it.

If a layer is missing, actions can be absent from Flow Builder or fault at runtime.

### Send Message to Launch Flow

This action sends "a message to a Slack channel, direct message, or the Messages tab of a Slack app that includes a button that a recipient can use to launch a screen flow" (Metadata API, `slackSendMessageToLaunchFlow`). The target is a screen flow whose `environments` includes `Slack`; the Slack environment "can run in Slack and the default environment," and you choose it when you save the flow.

### Record-Triggered Flows

UNVERIFIED (2026-10-03): Salesforce Help states that Slack actions in record-triggered flows belong on an asynchronous path. The fetched sources don't say so. Placing them on an `AsyncAfterCommit` path (which "runs asynchronously after a save") is the safe default either way, because the message then reflects committed data.

---

## Send Slack Message: Input Fields

| Input Field | Value | Notes |
|---|---|---|
| Slack App | Sales Cloud for Slack (`A028VJ1KG3G`) or your connected app's ID | Required by some flows (Slack Integrations guide); store it in custom metadata |
| Slack Workspace | Workspace ID (`T...`) | Use the ID, not the name |
| Message Destination ID | Channel ID (`C...`) or user/DM ID | IDs survive channel renames |
| Message | Text with merge fields | Keep sensitive fields out |

UNVERIFIED (2026-10-03): the API names behind these inputs (for example `slackAppIdForToken`, `slackWorkspaceIdForToken`, `slackConversationId`, `slackMessage`) are not in the fetched Metadata API or Actions guides; confirm them by building the action once and retrieving the flow. The full flow XML is in [references/metadata-examples.md](references/metadata-examples.md).

---

## Common Patterns

### Pattern 1: Notify a Channel When a Record Changes

**When to use:** Post to a Slack channel when a record reaches a state (Opportunity stage change, Case escalation).

**How it works:**
1. Record-triggered flow on the object, after save, with entry criteria and "only when updated to meet criteria."
2. Add an `AsyncAfterCommit` path.
3. Add **Send Slack Message** on that path with the app, workspace, channel ID, and message.
4. Add a fault path that logs `$Flow.FaultMessage` and alerts an owner.
5. Activate after testing in a sandbox connected to a test workspace.

### Pattern 2: Create a Deal Room Channel for a New Record

**When to use:** Provision a channel for each new Enterprise Opportunity.

**How it works:**
1. Record-triggered flow on Opportunity, after save, async path.
2. Formula for the channel name: lowercase, spaces replaced, trimmed to well under 80 characters, only letters, numbers, hyphens, and underscores.
3. **Create Slack Channel**, then **Invite Users to Slack Channel** with the owner and team.
4. Store the returned channel ID on the record for later actions.

### Pattern 3: Check Connection Before a Direct Message

**When to use:** Direct-message a Salesforce user only if they connected Slack.

**How it works:** **Check If Users Are Connected to Slack** first, then branch: connected users get **Send Slack Message**, others get email.

---

## Decision Guidance

| Situation | Recommended Approach | Reason |
|---|---|---|
| Notify a channel on record change | Send Slack Message on an async path of an after-save flow | Message reflects committed data |
| User action needed from Slack | Send Message to Launch Flow with a Slack-environment screen flow | The button launches a screen flow |
| Channel per record | Create Slack Channel + Invite Users to Slack Channel | Consistent provisioning |
| Actions missing in Flow Builder | Check Slack Apps Setup, app installation, and permissions | Each layer is required |
| Direct message a user | Check If Users Are Connected to Slack first | Unconnected users can't receive it |
| Update an earlier message | Edit Slack Message with the stored message identifier | Avoids duplicate posts |

---

## Recommended Workflow

1. Confirm Slack Apps Setup is complete, the app is installed in the target workspace, and the running user has Connect Salesforce with Slack plus the app's permission set.
2. Store the Slack app ID, workspace ID, and channel IDs in custom metadata so sandbox and production use different values.
3. Build the flow: after-save trigger, `AsyncAfterCommit` path, the Slack action, and a fault path; for launch buttons, build the screen flow with the Slack environment.
4. Run `python3 skills/flow/flow-for-slack/scripts/check_flow_for_slack.py --manifest-dir force-app` to catch Slack actions on before-save flows or without fault connectors, literal channel names, and launch targets missing the Slack environment.
5. Test in a sandbox against a test workspace, then activate in production.

---

## Review Checklist

- [ ] Salesforce for Slack Integrations enabled; the app installed in the workspace
- [ ] Running user has Connect Salesforce with Slack and the app's permission set
- [ ] Slack actions run on an async path of an after-save flow
- [ ] Every Slack action has a fault connector
- [ ] Channel, workspace, and app IDs come from configuration, not literals
- [ ] Create Slack Channel names follow Slack rules (lowercase, digits, hyphens, underscores, up to 80 characters)
- [ ] Launch-flow targets are screen flows saved with the Slack environment
- [ ] Only approved fields appear in messages

---

## Salesforce-Specific Gotchas

Full write-ups with sources are in [references/gotchas.md](references/gotchas.md).

| Gotcha | One-line summary |
|---|---|
| Setup layers | Actions depend on Slack Apps Setup, app installation, user mapping, and permissions. |
| Permission names | The Sales Cloud for Slack permission set is "Slack Sales User"; most apps also need Connect Salesforce with Slack. |
| Launch target | Send Message to Launch Flow launches a screen flow, not an autolaunched flow. |
| Slack environment | The target screen flow must be saved with the Slack environment. |
| Channel names | Lowercase letters, numbers, hyphens, underscores; 80 characters maximum. |
| Government Cloud | Salesforce for Slack apps aren't supported there. |
| Missing faults | Without a fault path, Slack failures surface only as flow error emails. |

---

## Output Artifacts

| Artifact | Description |
|---|---|
| Configured Salesforce Flow | Record-triggered or scheduled flow using Slack core actions |
| Prerequisite setup checklist | Slack Apps Setup, app installation, user mapping, permissions |
| Channel naming convention | Formula that produces Slack-valid channel names |
| Flow metadata | `flows/*.flow-meta.xml` with `actionType` values from the table above |

---

## Related Skills

- integration/slack-salesforce-integration-setup: for connecting the Salesforce org to the Slack workspace (prerequisite)
- integration/slack-workflow-builder: for the reverse direction: Slack Workflow Builder calling Salesforce flows
- flow/flow-email-and-notifications: for non-Slack notification channels from Salesforce Flow
- agentforce/agentforce-in-slack: for Agentforce agent deployment in Slack channels
