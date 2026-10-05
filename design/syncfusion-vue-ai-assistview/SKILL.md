---
name: syncfusion-vue-ai-assistview
description: Implement the Syncfusion Vue AI AssistView component. Use this skill whenever the user needs to create conversational AI interfaces, chatbots, prompt-response systems, or integrate AI services like OpenAI, Gemini, or Claude into Vue applications. Includes setup, prompt management, suggestions, customization, event handling, templates, markdown responses, AI service integration, chain of thoughts visualization, generative UI with dynamic tools, text-to-speech audio conversion.
metadata:
  author: "Syncfusion Inc"
  version: "34.1.29"
---

# Syncfusion Vue AI AssistView Component

The **AI AssistView** component provides a modern conversational interface for building AI-powered applications in Vue. It enables users to submit prompts and receive AI responses in a clean, chat-like interface with support for markdown rendering, custom suggestions, and seamless AI service integration.

## Component Overview

The AI AssistView component provides:
- **Prompt input area** with customizable placeholder and initial text
- **Conversation history** with automatic scrolling to latest messages
- **Suggestion chips** for guided user interactions
- **Custom avatars** for users and AI responses
- **Markdown rendering** for formatted AI responses
- **Event system** for handling prompts and responses
- **Template support** for custom banner and layout designs
- **Theme integration** with Syncfusion's material, bootstrap, and tailwind themes

## Navigation Guide

Choose the reference that matches your task:

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation of `@syncfusion/ej2-vue-interactive-chat`
- Vue 2 project setup with Vue-CLI
- Registering the component
- Importing CSS themes
- Running your first AI AssistView application

### Configuring Prompts & Responses
📄 **Read:** [references/prompt-configuration.md](references/prompt-configuration.md)
- Setting initial prompt text with `prompt` property
- Customizing placeholder text with `promptPlaceholder`
- Managing conversation history with `prompts` collection
- Storing user queries and AI responses
- Clearing conversation history

### Adding Suggestions & Guidance
📄 **Read:** [references/prompt-suggestions.md](references/prompt-suggestions.md)
- Configuring suggestion chips with `promptSuggestions`
- Customizing suggestions header with `promptSuggestionsHeader`
- Updating suggestions dynamically based on context
- Creating task-specific suggestion flows
- Improving user experience with smart suggestions

### Customizing Appearance
📄 **Read:** [references/customizing-appearance.md](references/customizing-appearance.md)
- Customizing user avatar icon with `promptIconCss`
- Changing AI response avatar with `responseIconCss`
- Showing/hiding clear button with `showClearButton`
- Styling the component with themes (material3, bootstrap, tailwind)
- Applying custom CSS classes

### Handling Events
📄 **Read:** [references/events.md](references/events.md)
- All 7 component events (created, promptRequest, promptChanged, beforeAttachmentUpload, attachmentUploadSuccess, attachmentUploadFailure, attachmentRemoved, attachmentClick)
- Processing prompts asynchronously with `addPromptResponse`
- Implementing custom event handlers
- Managing event arguments and properties
- Async/await patterns for AI service calls
- Error handling in event callbacks

### Using Templates
📄 **Read:** [references/templates.md](references/templates.md)
- Creating custom banner templates
- Using template syntax
- Customizing template context and variables
- Styling template content with CSS
- Dynamic template rendering based on state
- Template best practices and patterns

### Templates and Customization
📄 **Read:** [references/templates-and-customization.md](references/templates-and-customization.md)
- Custom footer templates with `footerTemplate`
- Customizing prompt items with `promptItemTemplate`
- Styling suggestion items with `promptSuggestionItemTemplate`
- Customizing response items with `responseItemTemplate`
- Configuring prompt toolbar with `promptToolbarSettings`
- Configuring response toolbar with `responseToolbarSettings`
- Setting up multiple views with `views` property
- Advanced template patterns and best practices

### Chain of Thoughts & Reasoning Blocks
📄 **Read:** [references/chain-of-thoughts.md](references/chain-of-thoughts.md)
- Enabling thinking blocks with `AssistThinking` module
- Visualizing AI reasoning process with thinking blocks
- Configuring stages with status indicators (completed, inprogress, failed)
- Adding inline context items with editable badges
- Customizing thinking blocks with templates
- Configuring timeline stage item templates
- Streaming reasoning blocks in real-time

### Generative UI & Dynamic Components
📄 **Read:** [references/generative-ui.md](references/generative-ui.md)
- Registering custom tools with `registerToolUI` method
- Creating interactive UI components within AI responses
- Configuring tool templates and handler functions
- Adding tool blocks to responses via `addPromptResponse`
- Integrating dynamic gauges, cards, and custom tools
- Configuring AI service for structured JSON responses
- Tool props and component interaction patterns

### Rendering Markdown & Rich Content
📄 **Read:** [references/markdown-and-responses.md](references/markdown-and-responses.md)
- Rendering markdown in AI responses
- Supported markdown syntax (bold, italic, headers, lists, code blocks)
- Streaming markdown content
- HTML response rendering
- Formatting tips for better readability
- Edge cases and troubleshooting

### Advanced Features & AI Integration
📄 **Read:** [references/advanced-features.md](references/advanced-features.md)
- Enabling scroll-to-bottom indicator with `enableScrollToBottom`
- Configuring toolbar with `toolbarSettings`
- Advanced styling techniques
- RTL (Right-to-Left) support
- Performance optimization
- Handling long conversations

### Connecting to AI Services
📄 **Read:** [references/ai-integration.md](references/ai-integration.md)
- Integrating with OpenAI, Gemini, Claude, or other AI APIs
- Managing API credentials securely
- Real-time vs mock response patterns
- Adding responses programmatically
- Error handling and retry logic
- Rate limiting and timeout management

### Component Methods
📄 **Read:** [references/methods.md](references/methods.md)
- `addPromptResponse()` - Add AI responses to prompts
- `executePrompt()` - Programmatically trigger prompts
- `scrollToBottom()` - Scroll to latest message
- Method signatures and parameters
- Streaming responses with isFinalUpdate
- Best practices and common patterns

### Speech-to-Text Integration
📄 **Read:** [references/speech-to-text.md](references/speech-to-text.md)
- Enabling voice input with `speechToTextSettings`
- Configuring microphone button and tooltips
- Language support and interim results
- Speech recognition events (onStart, onStop, transcriptChanged, onError)
- Browser compatibility and permissions
- Real-time transcript display

### Text-to-Speech Conversion
📄 **Read:** [references/text-to-speech.md](references/text-to-speech.md)
- Enabling audio playback with `e-assist-audio` toolbar item
- Built-in Text-to-Speech functionality using Web Speech API
- Customizing speech with `textToSpeechSettings` (language, pitch, rate, volume)
- Configuring voice selection and language support
- Browser compatibility and voice availability
- Handling audio playback controls and status feedback

### File Attachments
📄 **Read:** [references/attachments.md](references/attachments.md)
- Enable file upload with `enableAttachments` property
- Configure `attachmentSettings` (saveUrl, removeUrl, file restrictions)
- File validation (allowedFileTypes, maxFileSize, maximumCount)
- Attachment events (beforeUpload, uploadSuccess, uploadFailure, removed, click)
- Working with attached files in prompts
- Custom attachment templates (attachmentTemplate)
- Upload security and best practices

### Multi-View Navigation
📄 **Read:** [references/views-and-navigation.md](references/views-and-navigation.md)
- Configure multiple views with `views` property
- Switch active view using `activeView` property
- AssistViewModel structure and properties
- Custom view templates
- Dynamic view management
- View type: Assist vs Custom

### Toolbar Configuration
📄 **Read:** [references/toolbar-configuration.md](references/toolbar-configuration.md)
- Configure prompt toolbar with `promptToolbarSettings`
- Configure response toolbar with `responseToolbarSettings`
- Configure footer toolbar with `footerToolbarSettings`
- ToolbarItemModel properties (text, icon, align, tooltip, etc.)
- Toolbar positioning (Bottom, Inline)
- Common toolbar actions and patterns

### Streaming Responses
📄 **Read:** [references/streaming-responses.md](references/streaming-responses.md)
- Enable streaming with `enableStreaming` property
- Implement character-by-character or chunk-based streaming
- Progressive response rendering
- Integration with OpenAI and other APIs
- Stream error handling
- User-controlled streaming speed

### Header, Locale & Sizing
📄 **Read:** [references/header-locale-sizing.md](references/header-locale-sizing.md)
- Control header display with `showHeader` property
- Internationalization with `locale` property (13+ languages)
- Responsive sizing with `height` and `width` properties
- State persistence with `enablePersistence`
- Responsive layout patterns
- Full screen and dialog implementations

## Quick Start Example

Here's a minimal setup using Composition API:

```vue
<template>
  <div id="container" style="height: 500px; width: 700px;">
    <ejs-aiassistview
      id="aiAssistView"
      ref="aiassist"
      prompt="How can I help you today?"
      :prompt-suggestions="suggestions"
      :prompt-request="onPromptRequest"
    />
  </div>
</template>

<script setup>
import { AIAssistViewComponent as EjsAiassistview } from "@syncfusion/ej2-vue-interactive-chat";
import { ref } from "vue";

const aiassist = ref(null);

const suggestions = [
  "What is AI?",
  "How do I get started?",
  "Tell me a joke"
];

const onPromptRequest = (args) => {
  setTimeout(() => {
    const response = `You asked: "${args.prompt}". 
    To connect real AI, use the OpenAI API or similar service with your API key.`;
    aiassist.value.addPromptResponse(response);
  }, 1000);
};
</script>

<style>
@import "../node_modules/@syncfusion/ej2-material3-theme/styles/ai-assistview/index.css";
</style>
```

## Common Patterns

### Pattern 1: Basic AI Chatbot
Use the `promptRequest` event to handle user input and call an AI API:

```javascript
const onPromptRequest = async (args) => {
  try {
    const response = await fetch('https://api.openai.com/v1/completions', {
      method: 'POST',
      headers: { 'Authorization': `Bearer ${apiKey}` },
      body: JSON.stringify({ prompt: args.prompt, max_tokens: 150 })
    });
    const data = await response.json();
    aiassist.value.addPromptResponse(data.choices[0].text);
  } catch (error) {
    aiassist.value.addPromptResponse('Error: Could not process request');
  }
};
```

### Pattern 2: Pre-configured Suggestions
Create domain-specific suggestion flows to guide users:

```javascript
const suggestions = [
  "Show me productivity tips",
  "How do I code in Vue?",
  "Best practices for debugging"
];
```

### Pattern 3: Conversation History
Access and manage the conversation history:

```javascript
// Get all prompts and responses
const history = aiassist.value.ej2Instances.prompts;

// Clear conversation
aiassist.value.ej2Instances.prompts = [];
```
