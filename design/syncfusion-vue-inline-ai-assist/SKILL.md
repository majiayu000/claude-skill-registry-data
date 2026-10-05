---
name: syncfusion-vue-inline-ai-assist
description: Implement the Syncfusion Vue Inline AI Assist component for AI-powered text processing. Use this skill when implementing inline AI assistance, prompt-response interactions, custom command popups, response actions, event handling, or when you need to integrate AI-powered features directly into Vue applications for text editing, summarization, or content manipulation workflows.
metadata:
  author: "Syncfusion Inc"
  version: "34.1.29"
---

# Syncfusion Vue Inline AI Assist Component

The **Inline AI Assist** component is a powerful Syncfusion Vue control designed for integrating AI-powered features directly into your applications. It provides intelligent text processing capabilities with real-time response streaming, customizable prompts, command popups, and response actions. This component enables users to interact with AI services seamlessly through an intuitive popup-based interface.

## Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation and package setup
- Basic component integration
- CSS theme imports and configuration
- Running a basic example

### Prompt Configuration
📄 **Read:** [references/prompt-configuration.md](references/prompt-configuration.md)
- Setting and managing prompt text
- Working with prompt-response collection
- Handling prompt-request events
- Dynamic prompt handling with responses

### Command Settings & Customization
📄 **Read:** [references/command-settings.md](references/command-settings.md)
- Configuring command action items
- Setting up command groups and organization
- Adding icons, tooltips, and disabled states
- Handling command selection events

### Inline Toolbar Settings
📄 **Read:** [references/inline-toolbar-settings.md](references/inline-toolbar-settings.md)
- Configure inline toolbar items, position (`toolbarPosition`), and behavior
- Handle toolbar item clicks via the `itemClick` event to perform response or editor actions

### Response Settings & Actions
📄 **Read:** [references/response-settings.md](references/response-settings.md)
- Built-in response items (Accept/Discard)
- Adding custom response actions
- Response item grouping and customization
- Response action event handling

### Events & Methods
📄 **Read:** [references/events-and-methods.md](references/events-and-methods.md)
- Component lifecycle events (created event)
- Prompt request and response event handling
- Public methods: addResponse(), showPopup(), hidePopup(), etc.
- Event argument patterns and usage

### Templates & Localization
📄 **Read:** [references/templates-and-localization.md](references/templates-and-localization.md)
- Customizing editor template for footer area
- Response template customization options
- Localization setup for multiple languages
- RTL support and cultural adaptation

### Advanced Patterns
📄 **Read:** [references/advanced-patterns.md](references/advanced-patterns.md)
- Positioning component with relateTo property
- Popup sizing and dimension configuration
- Integration with contenteditable divs
- Common workflows and edge case handling

## Quick Start Example

Here's a minimal example to get started with Inline AI Assist in Vue:

```vue
<template>
  <div style="height: 350px; width: 650px; margin: 0 auto;">
    <br />
    <button @click="showPopup">Open Inline AI Assist</button>
    <div id="editableText" contenteditable="true" 
         style="min-height:80px; border:1px solid #ccc; padding:8px; margin-top:8px;">
      Editable content goes here.
    </div>
    <ejs-inlineaiassist 
      prompt="What are the benefits of AI?" 
      relate-to="#btn"
      popup-width="500px"
      :prompt-request="onPromptRequest"
      :response-settings="responseSettings"
      ref="inlineAiAssist">
    </ejs-inlineaiassist>
  </div>
</template>

<script setup>
import { InlineAIAssistComponent as EjsInlineaiassist } from "@syncfusion/ej2-vue-interactive-chat";
import { ref } from "vue";

let inlineAiAssist = ref(null);

const responseSettings = {
  itemSelect: (args) => {
    if (args.command.label === 'Accept') {
      const editable = document.getElementById('editableText');
      if (editable && inlineAiAssist.value?.prompts) {
        const lastResponse = inlineAiAssist.value.prompts[inlineAiAssist.value.prompts.length - 1].response;
        editable.innerHTML = '<p>' + lastResponse + '</p>';
      }
      inlineAiAssist.value?.hidePopup();
    } else if (args.command.label === 'Discard') {
      inlineAiAssist.value?.hidePopup();
    }
  }
};

const onPromptRequest = () => {
  setTimeout(() => {
    const defaultResponse = 'Connect to your AI service (OpenAI, Azure, etc.) to get real responses.';
    inlineAiAssist.value?.addResponse(defaultResponse);
  }, 1000);
};

const showPopup = () => {
  inlineAiAssist.value?.showPopup();
};
</script>

<style>
@import "../node_modules/@syncfusion/ej2-material3-theme/styles/inline-ai-assist/index.css";
</style>
```

## Common Patterns

### Pattern 1: Basic Prompt with Response Handler

```vue
<ejs-inlineaiassist 
  prompt="Summarize this text"
  :prompt-request="handlePrompt"
  :response-settings="responseSettings">
</ejs-inlineaiassist>
```

Trigger the component to show a prompt and handle the response through the `prompt-request` event.

### Pattern 2: Multiple Commands with Grouping

```javascript
const commandSettings = {
  commands: [
    { label: 'Summarize', prompt: 'Summarize', groupBy: 'Improve', iconCss: 'e-icons e-collapse-2' },
    { label: 'Shorten', prompt: 'Shorten', groupBy: 'Improve', iconCss: 'e-icons e-shorten' },
    { label: 'Translate', prompt: 'Translate', groupBy: 'Edit', iconCss: 'e-icons e-translate' }
  ],
  itemSelect: (args) => {
    // Handle command selection
  }
};
```

Commands are grouped visually and users select actions from a popup.

### Pattern 3: Custom Response Actions

```javascript
const responseSettings = {
  items: [
    { label: 'Regenerate', iconCss: 'e-icons e-refresh', groupBy: 'Actions' },
    { label: 'Copy', iconCss: 'e-icons e-copy', groupBy: 'Actions' },
    { label: 'Accept' },
    { label: 'Discard' }
  ],
  itemSelect: (args) => {
    // Handle response action
  }
};
```

Customize response popup with built-in and custom action items.

