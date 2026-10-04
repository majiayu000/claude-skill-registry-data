---
name: lwc-pubsub-patterns
description: "Legacy pubsub communication between LWCs on the same page (deprecated — prefer LMS). Triggers: pubsub LWC, c-pubsub, pageRef pubsub. NOT for modern cross-component messaging — use lwc/message-channel-patterns. NOT for parent-child events — use lwc/lwc-custom-event-patterns."
category: lwc
salesforce-version: "Spring '25+"
well-architected-pillars:
  - Performance
  - Reliability
triggers:
  - "lwc sibling component communication message channel"
  - "lightning message service lms scope application active"
  - "pubsub utility legacy lwc deprecated migrate"
  - "lwc messagechannel-meta.xml file definition"
  - "subscribe unsubscribe disconnectedcallback leak"
  - "lwc cross app communication aura visualforce"
  - "wire messagecontext lightning messageservice"
tags:
  - lightning-message-service
  - lms
  - pubsub
  - message-channel
  - sibling-communication
inputs:
  - "Communication shape (parent-child, sibling on same page, cross-app, cross-tab)"
  - "Whether subscribers are LWC, Aura, or Visualforce"
  - "Scope requirement (within Lightning app vs across apps in same tab)"
outputs:
  - "Recommendation: parent-child events / LMS / Platform Events"
  - "Message channel metadata file (when LMS is the answer)"
  - "Subscribe / unsubscribe boilerplate that doesn't leak on disconnect"
dependencies: []
version: 1.0.0
author: Pranav Nagrecha
updated: 2026-05-05
---

# LWC Pub/Sub Patterns

Lightning Web Components communicate naturally **down** the
component tree (parent passes props to child) and **up** (child
fires `CustomEvent`, parent listens). The harder case is **sibling**
communication: two components on the same page that have no
parent-child relationship.

Salesforce's modern answer is **Lightning Message Service (LMS)**.
Before LMS shipped, the community converged on a custom `pubsub`
utility (a singleton event-bus pattern in JavaScript). Both
patterns appear in real codebases. This skill maps the choice and
covers the implementation discipline that prevents subscription
leaks.

## When LMS is the right tool

LMS is the right tool when:

- The components are siblings (no shared parent that can mediate).
- The communication is within a single Lightning page or app
  (LMS scope is `APPLICATION` or `ACTIVE`, not cross-tab).
- The publishers / subscribers may be a mix of LWC, Aura, and
  Visualforce — LMS supports all three.

**LMS is NOT the right tool for:**

- **Parent-child.** Use props (down) and `CustomEvent` (up).
  LMS in parent-child is overkill and obscures intent.
- **Cross-tab / cross-window.** LMS does not cross browser tabs.
  Use Platform Events for cross-tab or cross-user signaling.
- **High-frequency streaming.** LMS is for discrete events, not
  100Hz updates.

## The Message Channel definition

Message channels are metadata. Define a channel at
`force-app/main/default/messageChannels/MyChannel.messageChannel-meta.xml`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<LightningMessageChannel xmlns="http://soap.sforce.com/2006/04/metadata">
    <masterLabel>My Channel</masterLabel>
    <isExposed>true</isExposed>
    <description>Sibling sync: search component to results component.</description>
    <lightningMessageFields>
        <fieldName>recordId</fieldName>
        <description>The record selected in the search component.</description>
    </lightningMessageFields>
    <lightningMessageFields>
        <fieldName>action</fieldName>
        <description>One of: 'select', 'clear'.</description>
    </lightningMessageFields>
</LightningMessageChannel>
```

`isExposed = true` means other namespaces can use it. Set to false
for managed-package internal channels.

## Publish / subscribe in LWC

```javascript
import { LightningElement, wire } from 'lwc';
import {
    publish, subscribe, unsubscribe, MessageContext, APPLICATION_SCOPE
} from 'lightning/messageService';
import MY_CHANNEL from '@salesforce/messageChannel/MyChannel__c';

export default class SearchComponent extends LightningElement {
    @wire(MessageContext) messageContext;
    subscription = null;

    connectedCallback() {
        this.subscription = subscribe(
            this.messageContext,
            MY_CHANNEL,
            (msg) => this.handleMessage(msg),
            { scope: APPLICATION_SCOPE }
        );
    }

    disconnectedCallback() {
        unsubscribe(this.subscription);
        this.subscription = null;
    }

    publishSelection(recordId) {
        publish(this.messageContext, MY_CHANNEL, {
            recordId,
            action: 'select'
        });
    }

    handleMessage(msg) { /* ... */ }
}
```

Two things to get right:

1. `@wire(MessageContext)` provides the message context the
   subscribe / publish calls require.
2. **Always** unsubscribe in `disconnectedCallback` to prevent
   memory leaks across page navigations.

## `scope: APPLICATION` vs `scope: ACTIVE`

| Scope | Receives messages from |
|---|---|
| `APPLICATION_SCOPE` | All subscribers anywhere in the Lightning Experience app |
| `ACTIVE` (default) | Only subscribers in the active Lightning navigation context (current tab in console UX, current app) |

`APPLICATION_SCOPE` is broader; use it when the publisher and
subscriber may live in different apps within the same Lightning
session (e.g. utility bar component and main page). `ACTIVE` is
the default and is what you usually want for pages that should
only talk to themselves.

## The legacy `pubsub` utility

Pre-LMS, a community-shared utility module called `pubsub` (often
literally named that in source) provided a singleton event bus.
Pattern:

```javascript
import { fireEvent, registerListener, unregisterListener } from 'c/pubsub';

connectedCallback() {
    registerListener('mySearchEvent', this.handleEvent, this);
}
disconnectedCallback() {
    unregisterAllListeners(this);
}
```

It works but has limits:

- Custom utility you maintain (LMS is platform-supported).
- Cannot be consumed by Aura / Visualforce.
- Singleton state across components — leaks easier.

**Migration.** Replace `c/pubsub` import with
`lightning/messageService`. Replace the event name with a Message
Channel. Most renames are mechanical.

## Recommended Workflow

1. **Confirm sibling communication is required.** Parent-child should use props / `CustomEvent`; only reach for LMS when there is no shared parent.
2. **Confirm cross-tab is not required.** LMS does not cross tabs. For cross-tab, use Platform Events.
3. **Define the Message Channel.** Create `MyChannel.messageChannel-meta.xml` with named fields and a description. Treat the channel as a contract; named fields are the schema.
4. **Implement publish / subscribe.** Use `@wire(MessageContext)`; subscribe in `connectedCallback`; **always** unsubscribe in `disconnectedCallback`.
5. **Pick the scope.** `APPLICATION_SCOPE` for cross-app within the Lightning session; default (`ACTIVE`) for same-page.
6. **Test the unsubscribe.** Navigate away and back; the previous subscription should not fire on the second visit. Memory leaks here surface as duplicate handler invocations.
7. **For legacy `pubsub` users**, migrate to LMS rather than extending the utility. Custom utility maintenance cost compounds.

## What This Skill Does Not Cover

| Topic | See instead |
|---|---|
| Parent-child LWC props / `CustomEvent` | `lwc/lwc-component-communication` |
| Cross-tab or cross-user events | Platform Events / `integration/change-data-capture-patterns` |
| Aura-to-LWC interop generally | `lwc/aura-lwc-interop-patterns` |
| LWC reactivity (`@track`, `@api`, `@wire`) | `lwc/lwc-reactivity-patterns` |
