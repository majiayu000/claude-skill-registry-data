---
name: syncfusion-vue-speech-to-text
description: Implement the Syncfusion Vue Speech-to-Text component. Instructions for integrating voice input, real-time transcription, language configuration, programmatic control, event handling, UI customization, browser compatibility, and security considerations for microphone-enabled applications.
metadata:
  author: "Syncfusion Inc"
  version: "34.1.29"
---

# Syncfusion Vue Speech-to-Text Component

The Syncfusion Vue Speech-to-Text component converts spoken words into text using the browser's Speech Recognition API. This skill covers setup, configuration, event handling, customization, and security considerations for implementing real-time voice transcription in Vue 3 applications.

## Browser Support & Requirements

The Speech-to-Text component requires:
- **Browser Support:** Chrome 25+, Edge 79+, Safari 12+, Opera 30+ (Firefox not supported)
- **API Dependency:** HTML5 Speech Recognition API
- **Internet Connection:** Required for speech processing
- **User Permission:** Microphone access consent

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Vue 3 project setup with Vite
- Package installation and configuration
- CSS theme imports
- Component registration
- Browser compatibility requirements

### Speech Recognition & Configuration
📄 **Read:** [references/speech-recognition.md](references/speech-recognition.md)
- Retrieving transcribed text with `transcript` property
- Setting language with `lang` property
- Managing real-time results with `allowInterimResults`
- Understanding listening states (Inactive, Listening, Stopped)
- Showing/hiding tooltips with `showTooltip`
- Disabling the component
- Error handling and troubleshooting

### Methods & Programmatic Control
📄 **Read:** [references/methods.md](references/methods.md)
- Starting speech recognition with `startListening()`
- Stopping recognition with `stopListening()`
- Programmatic control patterns and use cases

### Events & Lifecycle
📄 **Read:** [references/events.md](references/events.md)
- Component initialization with `created` event
- Speech recognition lifecycle: `onStart`, `onStop`
- Error detection with `onError` event
- Real-time transcription with `transcriptChanged` event
- Event argument structures and practical examples

### Appearance & Customization
📄 **Read:** [references/appearance.md](references/appearance.md)
- Customizing button text and content
- Button icon configuration and positioning
- Primary button styling
- Tooltip content and positioning
- CSS class styling (e-primary, e-outline, e-info, e-success, e-warning, e-danger)
- Custom styling examples

### Globalization & Localization
📄 **Read:** [references/globalization.md](references/globalization.md)
- Localization with `L10n.load()` method
- Translation key identifiers and default values
- Language configuration with `locale` property
- Right-to-Left (RTL) support with `enableRtl` property
- Multi-language examples

### Security Considerations
📄 **Read:** [references/security.md](references/security.md)
- Online dependency and offline fallback
- Data transmission security risks
- Privacy concerns with third-party servers
- Man-in-the-Middle (MITM) attack vectors
- Mitigation strategies and best practices

## Quick Start

**Basic Setup with Composition API:**

```vue
<template>
  <div id="container">
    <ejs-speechtotext id="speechtotext" @transcript-changed="onTranscriptChange"></ejs-speechtotext>
    <ejs-textarea v-model="textareaValue" rows="5" cols="50" resizeMode="None" placeholder="Transcribed text will be shown here..."></ejs-textarea>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { SpeechToTextComponent as EjsSpeechtotext, TextAreaComponent as EjsTextarea } from "@syncfusion/ej2-vue-inputs";

const textareaValue = ref('');

const onTranscriptChange = (args) => {
  textareaValue.value = args.transcript;
};

</script>

<style>
@import "../node_modules/@syncfusion/ej2-material3-theme/styles/speech-to-text/index.css";
</style>
```

## Common Patterns

### Pattern 1: Real-Time vs Final Transcription

Display results as the user speaks (interim results) or wait for complete speech:

```vue
<!-- Real-time results (default, allowInterimResults=true) -->
<ejs-speechtotext @transcript-changed="onTranscriptChange"></ejs-speechtotext>

<!-- Final results only (allowInterimResults=false) -->
<ejs-speechtotext @transcript-changed="onTranscriptChange" :allow-interim-results="false"></ejs-speechtotext>
```

### Pattern 2: Multi-Language Support

Set language for speech recognition:

```vue
<!-- English (US) -->
<ejs-speechtotext lang="en-US" @transcript-changed="onTranscriptChange"></ejs-speechtotext>

<!-- French -->
<ejs-speechtotext lang="fr-FR" @transcript-changed="onTranscriptChange"></ejs-speechtotext>
```

### Pattern 3: Programmatic Control

Trigger speech recognition from buttons:

```vue
<template>
  <div>
    <button @click="startRecognition">Start Listening</button>
    <button @click="stopRecognition">Stop Listening</button>
    <ejs-speechtotext ref="speechToTextInstance"></ejs-speechtotext>
  </div>
</template>

<script setup>
const speechToTextInstance = ref(null);

const startRecognition = () => {
  speechToTextInstance.value.startListening();
};

const stopRecognition = () => {
  speechToTextInstance.value.stopListening();
};
</script>
```

### Pattern 4: Listening State Monitoring

Track component state changes:

```vue
<template>
  <div>
    <p>Status: {{ listeningState }}</p>
    <ejs-speechtotext @start="(args) => listeningState = args.listeningState" @stop="(args) => listeningState = args.listeningState"></ejs-speechtotext>
  </div>
</template>

<script setup>
const listeningState = ref('Inactive');
</script>
```

### Pattern 5: Error Handling

Capture and respond to speech recognition errors:

```vue
<template>
  <ejs-speechtotext @error="onError"></ejs-speechtotext>
</template>

<script setup>
const onError = (args) => {
  console.error('Speech recognition error:', args);
};
</script>
```
