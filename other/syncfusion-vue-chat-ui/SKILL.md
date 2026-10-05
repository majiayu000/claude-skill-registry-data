---
name: syncfusion-vue-chat-ui
description: Implement the Syncfusion Vue Chat UI component for Vue chat interfaces, messaging applications, conversational UI, chat widgets, real-time messaging, user-to-user communication, bot integrations, customer support chat, collaborative messaging, instant messaging features, chat rooms, or when user mentions "chat ui", "chat component", "messaging interface", "conversation view", or @syncfusion/ej2-vue-interactive-chat package.
metadata:
  author: "Syncfusion Inc"
  version: "34.1.29"
---

# Syncfusion Vue Chat UI Component

The Syncfusion Vue Chat UI component provides a modern, feature-rich interface for building conversational applications. It supports real-time messaging, user avatars, typing indicators, file attachments, message replies, mentions, timestamps, and bot integrations.

## Component Overview

The Vue Chat UI component (`ejs-chatui`) provides:

- **Message Management**: Add, update, and display messages with rich metadata (author, timestamp, status)
- **User System**: Define current user and other participants with avatars, names, and status indicators
- **Interactive Features**: Message replies, pinning, forwarding, toolbar actions, and @mentions
- **File Attachments**: Upload, preview, and display files with drag-and-drop support
- **Templates**: Customize messages, suggestions, empty states, typing indicators, attachments, and time breaks
- **Events**: Handle message sending, user typing, attachment uploads, mention selection, and toolbar clicks
- **Accessibility**: Built-in WCAG compliance, keyboard navigation, and RTL support
- **Bot Integration**: Connect with Microsoft Bot Framework and Dialogflow

**Package**: `@syncfusion/ej2-vue-interactive-chat`  
**Vue Support**: Vue 3
**Dependencies**: Base, Inputs, Navigations, Buttons, Popups, Dropdowns, Splitbuttons

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation and package setup (`@syncfusion/ej2-vue-interactive-chat`)
- Basic Chat UI implementation
- CSS imports and Material3 theme configuration
- Component registration and first render
- Defining messages with `<e-messages>` and `<e-message>` directives
- Setting up current user

### Messages Configuration
📄 **Read:** [references/messages.md](references/messages.md)
- Message model structure (text, author, timestamp, id)
- Adding messages with `<e-message>` selector
- Message properties: isPinned, isForwarded, replyTo
- Message status with icons and tooltips
- Attached files in messages
- Mention users in message text
- Message IDs for tracking and updates

### Users and Avatars
📄 **Read:** [references/users.md](references/users.md)
- User model configuration (id, user, avatarUrl)
- Current user vs other participants
- Avatar display (URL or initials fallback)
- Avatar background colors customization
- Status icons with cssClass
- Typing users list and indicators
- User CSS class customization

### Appearance and Styling
📄 **Read:** [references/appearance.md](references/appearance.md)
- Component dimensions (height, width)
- CSS class customization with cssClass property
- RTL (right-to-left) support
- Compact mode layout (all messages left-aligned)
- Empty chat template for no messages
- Persistence across page reloads
- Theming with Material3, Bootstrap, Fabric

### Header and Footer Configuration
📄 **Read:** [references/header-footer.md](references/header-footer.md)
- Header text and icon configuration
- Header toolbar settings and items
- Toolbar item configuration (text, icon, tooltip, align)
- Show/hide header with showHeader property
- Show/hide footer with showFooter property
- Footer template customization
- Placeholder text for input textarea
- Toolbar item click events

### Timestamps and Time Breaks
📄 **Read:** [references/timestamps-timebreaks.md](references/timestamps-timebreaks.md)
- Show/hide timestamps with showTimeStamp
- Timestamp format customization
- Time breaks for date-based grouping
- Custom time break templates
- Localization and culture-specific formats
- Per-message timestamp formats

### Advanced Features
📄 **Read:** [references/advanced-features.md](references/advanced-features.md)
- @Mention functionality with trigger character
- Mention users list and suggestion popup
- File attachments configuration (saveUrl, allowed types, max size)
- Drag-and-drop attachments
- Message toolbar (Reply, Pin, Delete, Copy, Forward)
- Message toolbar customization and events
- Load on demand for message history
- Auto scroll to bottom for new messages
- Suggestions above input textarea

### Templates
📄 **Read:** [references/templates.md](references/templates.md)
- Message template for custom message rendering
- Suggestion template for suggestion items
- Typing users template for typing indicators
- Empty chat template for no messages state
- Footer template for custom footer
- Attachment template for file display in footer
- Preview template for attachment previews
- Time break template for date separators
- Template context data (message, index, suggestion)

### Events and Methods
📄 **Read:** [references/events-methods.md](references/events-methods.md)
- created event (component initialization)
- messageSend event (before message sent)
- userTyping event (typing indicators)
- mentionSelect event (mention selection)
- Attachment events (beforeUpload, success, failure, removed)
- Toolbar item click events (header and message toolbars)
- addMessage() method to append messages
- updateMessage() method to modify messages
- scrollToBottom() method for navigation
- scrollToMessage() method to scroll to specific message
- focus() method for input textarea

### Bot Integrations
📄 **Read:** [references/bot-integrations.md](references/bot-integrations.md)
- Integration with Microsoft Bot Framework
- Integration with Google Dialogflow
- Bot message handling and responses
- Connecting to bot services
- Sample bot conversation flows
- Handling bot-initiated messages

## Quick Start

### Basic Chat UI

```vue
<template>
  <div id="container" style="height: 400px; width: 500px;">
    <ejs-chatui :user="currentUser">
      <e-messages>
        <e-message 
          :author="currentUser" 
          text="Hello! How can I help you today?"
        ></e-message>
        <e-message 
          :author="supportUser" 
          text="Hi! I need assistance with my order."
        ></e-message>
      </e-messages>
    </ejs-chatui>
  </div>
</template>

<script setup>
import { 
  ChatUIComponent as EjsChatui, 
  MessagesDirective as EMessages, 
  MessageDirective as EMessage 
} from "@syncfusion/ej2-vue-interactive-chat";

const currentUser = {
  id: "user1",
  user: "Albert",
  avatarUrl: "./albert.png"
};

const supportUser = {
  id: "user2",
  user: "Support Agent",
  avatarUrl: "./support.png"
};
</script>

<style>
@import "../node_modules/@syncfusion/ej2-material3-theme/styles/chat-ui/index.css";
</style>
```

## Common Patterns

### Dynamic Message Handling

```vue
<script setup>
import { ref } from 'vue';
import { ChatUIComponent as EjsChatui } from "@syncfusion/ej2-vue-interactive-chat";

const chatRef = ref(null);

// Add message dynamically
const sendMessage = (text) => {
  chatRef.value.addMessage({
    text: text,
    author: currentUser,
    timestamp: new Date()
  });
};

// Handle message send event
const onMessageSend = (args) => {
  console.log('Message sent:', args.message);
  // Send to backend or bot service
};
</script>

<template>
  <ejs-chatui 
    ref="chatRef"
    :user="currentUser"
    :messageSend="onMessageSend"
  ></ejs-chatui>
</template>
```

### Message Replies and Threading

```vue
<e-message 
  :author="currentUser" 
  text="I've completed the review."
  :replyTo="{
    messageID: 'msg-123',
    text: 'Can you review the document?',
    user: otherUser,
    timestamp: new Date('2026-03-27T10:00:00')
  }"
></e-message>
```

### File Attachments

```vue
<ejs-chatui 
  :user="currentUser"
  :enableAttachments="true"
  :attachmentSettings="{
    saveUrl: 'https://api.example.com/upload',
    allowedFileTypes: '.jpg,.png,.pdf,.docx',
    maxFileSize: 5242880,
    maximumCount: 3
  }"
  :beforeAttachmentUpload="handleBeforeUpload"
  :attachmentUploadSuccess="handleUploadSuccess"
></ejs-chatui>
```

### @Mentions

```vue
<ejs-chatui 
  :user="currentUser"
  mentionTriggerChar="@"
  :mentionUsers="[
    { id: 'u1', user: 'Alice' },
    { id: 'u2', user: 'Bob' },
    { id: 'u3', user: 'Charlie' }
  ]"
  :mentionSelect="handleMentionSelect"
></ejs-chatui>
```
