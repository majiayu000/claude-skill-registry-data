---
name: syncfusion-vue-inputs
description: Comprehensive guide for implementing Syncfusion Vue 3 input components including Uploader, NumericTextBox, TextBox, TextArea, CheckBox, OTP Input, Signature, RangeSlider, ColorPicker, MaskedTextBox, and Rating. Use this when building file upload UIs with async/chunk uploads, drag-and-drop functionality, numeric inputs with validation and formatting, text inputs with floating labels, custom adornments, form integration, accessibility compliance, and styling in Vue 3 applications.
metadata:
  author: "Syncfusion Inc"
  version: "34.1.29"
  category: "Inputs"
---

# Implementing Syncfusion Vue 3 Inputs

## Uploader

The Syncfusion Vue **UploaderComponent** provides a rich file upload control with async upload, drag-and-drop, chunk upload with pause/resume/cancel, validation, templates, form integration, and accessibility support.

### Navigation Guide

> 🛑 **Agentic use:** Do not execute multiple steps autonomously. Confirm with the user before each action (install, run, file creation).

#### Getting Started
📄 **Read:** [references/uploader-getting-started.md](references/uploader-getting-started.md)
- Installing `@syncfusion/ej2-vue-inputs` 🛑 *STOP — Do not install packages autonomously. Ask the user to run: `npm install @syncfusion/ej2-vue-inputs`. Verify with `npm audit`*
- License registration
- Basic `UploaderComponent` usage in Vue 3 SFC (Single File Component)
- CSS theme imports
- Drop area configuration
- Success and failure event handling with Composition API

#### Asynchronous Upload
📄 **Read:** [references/uploader-async-upload.md](references/uploader-async-upload.md)
- `asyncSettings` with `saveUrl` and `removeUrl` in Vue data()
- Multiple vs. single file upload (`multiple`)
- Auto upload vs. manual upload (`autoUpload`)
- Sequential upload (`sequentialUpload`)
- Preloaded files (`files` property)
- Adding custom HTTP headers via `uploading`/`removing` events
- Server-side save/remove action examples
- Vue 3 Composition API patterns for reactive state

#### Chunk Upload
📄 **Read:** [references/uploader-chunk-upload.md](references/uploader-chunk-upload.md)
- Enabling chunk upload with `asyncSettings.chunkSize`
- Retry configuration (`retryCount`, `retryAfterDelay`)
- Pause and resume chunked uploads (`pause`, `resume` methods)
- Cancel uploads (`cancel` method)
- `chunkSuccess` and `chunkFailure` events
- Server-side chunk handling (C#)
- Vue ref() pattern for imperative component access

#### Validation
📄 **Read:** [references/uploader-validation.md](references/uploader-validation.md)
- Allowed file extensions (`allowedExtensions`)
- File size limits (`minFileSize`, `maxFileSize`)
- Maximum file count using `selected` event
- Duplicate file prevention
- Drag-and-drop image validation

#### File Sources
📄 **Read:** [references/uploader-file-source.md](references/uploader-file-source.md)
- Clipboard paste upload
- Directory/folder upload (`directoryUpload`)
- Drag-and-drop with custom drop area (`dropArea`)
- Customizing drop area appearance

#### Templates and Customization
📄 **Read:** [references/uploader-template-customization.md](references/uploader-template-customization.md)
- File list `template` property (Vue slots)
- Custom upload UI with `showFileList: false`
- Customizing action buttons (`buttons` property)
- Progress bar customization
- Hiding the default drop area
- Style and appearance overrides
- Vue slot patterns and scoped slots

#### Advanced How-To Scenarios
📄 **Read:** [references/uploader-advanced-how-to.md](references/uploader-advanced-how-to.md)
- Programmatic file upload (`upload` method, `getFilesData`)
- Invisible/background upload
- Image preview before uploading
- Resize images before upload
- Sort selected files
- Check file size / MIME type before upload
- Confirm dialog before file removal
- Open/edit uploaded files
- Trigger file browser from external button
- Convert uploaded image to binary
- JWT authentication for secure upload ⚠️ *Never hardcode tokens. Retrieve from a secure session store at runtime. Do not log request headers or token values.*
- Form support (HTML form, v-model, reactive forms)
- Localization (custom locale strings)
- Accessibility and keyboard navigation

#### API Reference
📄 **Read:** [references/uploader-api.md](references/uploader-api.md)
- All properties (`allowedExtensions`, `asyncSettings`, `autoUpload`, `buttons`, `cssClass`, `directoryUpload`, `dropArea`, `dropEffect`, `enabled`, `files`, `htmlAttributes`, `locale`, `maxFileSize`, `minFileSize`, `multiple`, `sequentialUpload`, `showFileList`, `template`, and more)
- All methods (`upload`, `remove`, `cancel`, `pause`, `resume`, `retry`, `clearAll`, `getFilesData`, `bytesToSize`, `createFileList`, `sortFileList`)
- All events (`uploading`, `success`, `failure`, `selected`, `removing`, `change`, `progress`, `chunkSuccess`, `chunkFailure`, `chunkUploading`, `actionComplete`, `beforeRemove`, `beforeUpload`, `canceling`, `clearing`, `fileListRendering`, `pausing`, `resuming`, `created`)

### Quick Start Example (Vue 3 Composition API)

```vue
<template>
  <div class="uploader-container">
    <h1>File Uploader</h1>
    <UploaderComponent
      ref="uploaderRef"
      :asyncSettings="asyncSettings"
      :autoUpload="false"
      :multiple="true"
      @success="onSuccess"
      @failure="onFailure"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { UploaderComponent } from '@syncfusion/ej2-vue-inputs';
import '@syncfusion/ej2-base/styles/material.css';
import '@syncfusion/ej2-buttons/styles/material.css';
import '@syncfusion/ej2-inputs/styles/material.css';
import '@syncfusion/ej2-popups/styles/material.css';
import '@syncfusion/ej2-vue-inputs/styles/material.css';

// Component reference for imperative access
const uploaderRef = ref(null);

// Async settings with server endpoints
// ⚠️ Replace with your own server-side endpoints.
// Never use third-party demo URLs in production — files will be sent to that external server.
const asyncSettings = {
  saveUrl: '/api/upload/save',
  removeUrl: '/api/upload/remove'
};

// Success handler
const onSuccess = (args) => {
  console.log('Upload operation:', args.operation, 'File:', args.file.name);
};

// Failure handler
const onFailure = (args) => {
  console.error('Upload failed:', args.file.name);
};
</script>

<style scoped>
.uploader-container {
  padding: 20px;
  max-width: 600px;
  margin: 0 auto;
}
</style>
```

### Common Patterns (Vue 3)

#### Auto Upload with Validation
```vue
<template>
  <UploaderComponent
    :asyncSettings="{ saveUrl: '/api/upload/save', removeUrl: '/api/upload/remove' }"
    :allowedExtensions="'.pdf,.doc,.docx'"
    :maxFileSize="5000000"
    :multiple="true"
    :autoUpload="true"
  />
</template>

<script setup>
import { UploaderComponent } from '@syncfusion/ej2-vue-inputs';
</script>
```

#### Manual Upload with Custom Buttons
```vue
<template>
  <UploaderComponent
    ref="uploaderRef"
    :asyncSettings="{ saveUrl: '/api/upload/save', removeUrl: '/api/upload/remove' }"
    :autoUpload="false"
    :buttons="{ browse: 'Choose File', clear: 'Clear All', upload: 'Upload All' }"
    @success="onSuccess"
  />
</template>

<script setup>
import { ref } from 'vue';
import { UploaderComponent } from '@syncfusion/ej2-vue-inputs';

const uploaderRef = ref(null);

const onSuccess = (args) => {
  console.log('Files uploaded successfully');
};
</script>
```

---

## NumericTextBox Component

Use the **NumericTextBox** for numeric input with formatting, validation, spinners, and decimal precision.

#### Getting Started
📄 **Read:** [references/numerictextbox-getting-started.md](references/numerictextbox-getting-started.md)

#### Formats & Validation
📄 **Read:** [references/numerictextbox-formats-and-validation.md](references/numerictextbox-formats-and-validation.md)

#### Precision & Decimals
📄 **Read:** [references/numerictextbox-precision-decimals.md](references/numerictextbox-precision-decimals.md)

#### API Reference
📄 **Read:** [references/numerictextbox-api.md](references/numerictextbox-api.md)

### Quick Start Example (Vue 3)

```vue
<template>
  <div class="numeric-input">
    <label>Enter Amount:</label>
    <NumericTextBoxComponent
      v-model="amount"
      :format="'c2'"
      :min="0"
      :max="10000"
      @change="onAmountChange"
    />
    <p v-if="amount">Total: {{ amount }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { NumericTextBoxComponent } from '@syncfusion/ej2-vue-inputs';

const amount = ref(100);

const onAmountChange = (args) => {
  console.log('Amount changed to:', args.value);
};
</script>
```

---

## TextBox Component

Use the **TextBox** for text input with floating labels, icons, and validation.

#### Getting Started
📄 **Read:** [references/textbox-getting-started.md](references/textbox-getting-started.md)

#### API Reference
📄 **Read:** [references/textbox-api.md](references/textbox-api.md)

### Quick Start Example (Vue 3)

```vue
<template>
  <div class="textbox-container">
    <TextBoxComponent
      v-model="userName"
      placeholder="Enter your name"
      :floatLabelType="'Auto'"
      @change="onTextChange"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { TextBoxComponent } from '@syncfusion/ej2-vue-inputs';

const userName = ref('');

const onTextChange = (args) => {
  console.log('Username:', args.value);
};
</script>
```

---

## TextArea Component

Use the **TextArea** for multi-line text input with auto-resize, character count, and floating labels.

#### Getting Started
📄 **Read:** [references/textarea-getting-started.md](references/textarea-getting-started.md)

#### API Reference
📄 **Read:** [references/textarea-api.md](references/textarea-api.md)

### Quick Start Example (Vue 3)

```vue
<template>
  <div class="textarea-container">
    <TextAreaComponent
      v-model="message"
      placeholder="Enter your message"
      :floatLabelType="'Auto'"
      :maxLength="500"
    />
    <p>{{ message.length }} / 500</p>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { TextAreaComponent } from '@syncfusion/ej2-vue-inputs';

const message = ref('');

const characterCount = computed(() => message.value.length);
</script>
```

---

## CheckBox Component

Use the **CheckBox** for single and grouped selections with accessibility support.

#### Getting Started
📄 **Read:** [references/checkbox-getting-started.md](references/checkbox-getting-started.md)

#### API Reference
📄 **Read:** [references/checkbox-api.md](references/checkbox-api.md)

### Quick Start Example (Vue 3)

```vue
<template>
  <div class="checkbox-container">
    <div class="checkbox-group">
      <CheckBoxComponent
        v-for="option in options"
        :key="option.id"
        v-model="selectedOptions"
        :value="option.id"
        :label="option.name"
      />
    </div>
    <p>Selected: {{ selectedOptions.join(', ') }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { CheckBoxComponent } from '@syncfusion/ej2-vue-inputs';

const selectedOptions = ref([]);
const options = ref([
  { id: 1, name: 'Option 1' },
  { id: 2, name: 'Option 2' },
  { id: 3, name: 'Option 3' }
]);
</script>
```

---

## Additional Input Components

For complete documentation on other input components, refer to these guides:

- **ColorPicker** — [references/colorpicker-getting-started.md](references/colorpicker-getting-started.md)
- **MaskedTextBox** — [references/maskedtextbox-getting-started.md](references/maskedtextbox-getting-started.md)
- **OTP Input** — [references/otp-input-getting-started.md](references/otp-input-getting-started.md)
- **Rating** — [references/rating-getting-started.md](references/rating-getting-started.md)
- **RangeSlider** — [references/range-slider-getting-started.md](references/range-slider-getting-started.md)
- **Signature** — [references/signature-getting-started.md](references/signature-getting-started.md)

### Reactive Data with ref() and reactive()

```vue
<script setup>
import { ref, reactive } from 'vue';

// Simple scalar value
const count = ref(0);

// Complex object (used for component state)
const formData = reactive({
  name: '',
  email: '',
  phone: ''
});

// Access reactive values
formData.name = 'John';
console.log(count.value); // Note: .value required in script, not in template
</script>
```

### Two-Way Binding with v-model

```vue
<template>
  <!-- Vue 3 component v-model -->
  <NumericTextBoxComponent v-model="amount" />
  
  <!-- Native HTML element -->
  <input v-model="userName" />
</template>

<script setup>
import { ref } from 'vue';

const amount = ref(0);
const userName = ref('');
</script>
```

### Event Handling

```vue
<template>
  <UploaderComponent @success="onSuccess" @failure="onFailure" />
</template>

<script setup>
const onSuccess = (args) => {
  console.log('Event args:', args);
};

const onFailure = (args) => {
  console.error('Error:', args);
};
</script>
```

### Component References with ref()

```vue
<template>
  <UploaderComponent ref="uploaderRef" />
  <button @click="uploadFiles">Upload</button>
</template>

<script setup>
import { ref } from 'vue';

const uploaderRef = ref(null);

const uploadFiles = () => {
  if (uploaderRef.value) {
    uploaderRef.value.upload(); // Call component method
  }
};
</script>
```

### Computed Properties

```vue
<template>
  <p>Total: {{ total }}</p>
</template>

<script setup>
import { ref, computed } from 'vue';

const items = ref([
  { price: 10, quantity: 2 },
  { price: 20, quantity: 1 }
]);

const total = computed(() => {
  return items.value.reduce((sum, item) => sum + item.price * item.quantity, 0);
});
</script>
```

### Watchers for Reactive Side Effects

```vue
<script setup>
import { ref, watch } from 'vue';

const amount = ref(0);

watch(amount, (newValue, oldValue) => {
  console.log(`Amount changed from ${oldValue} to ${newValue}`);
  // Perform side effect (API call, etc.)
});

// Deep watch for complex objects
watch(
  () => formData,
  (newValue) => {
    console.log('Form data changed:', newValue);
  },
  { deep: true }
);
</script>
```

### Lifecycle Hooks in Composition API

```vue
<script setup>
import { ref, onMounted, onUnmounted } from 'vue';

const isLoading = ref(false);

onMounted(() => {
  console.log('Component mounted');
  isLoading.value = true;
});

onUnmounted(() => {
  console.log('Component unmounted');
  // Cleanup resources
});
</script>
```

### Slots in Vue 3

```vue
<template>
  <!-- Parent component -->
  <CustomComponent>
    <template #header>
      <h1>Custom Header</h1>
    </template>
    <template #default="{ item }">
      <p>{{ item.name }}</p>
    </template>
  </CustomComponent>
</template>

<script setup>
import CustomComponent from './CustomComponent.vue';
</script>
```

---

## Migration from React to Vue 3

### For React Developers: Migration Reference

| React Hook | Vue 3 Equivalent | Purpose |
|-----------|-----------------|---------|
| `useState(value)` | `ref(value)` | Reactive state |
| `useContext(Context)` | `inject('key')` | Access provided values |
| `useEffect()` | `watch()`, `onMounted()` | Side effects |
| `useCallback()` | Inline functions or `computed()` | Memoized functions |
| `useMemo()` | `computed()` | Memoized values |
| `useRef()` | `ref()` | DOM/component reference |
| `useReducer()` | `reactive()` + state logic | Complex state management |

### React Component Props → Vue Props

**Vue 3:**
```vue
<script setup>
defineProps({
  label: String,
  disabled: Boolean
});

defineEmits(['click']);
</script>

<template>
  <button @click="$emit('click')" :disabled="disabled">{{ label }}</button>
</template>
```

### React Event Handlers → Vue Event Handlers

**Vue 3:**
```vue
<template>
  <button @click="handleClick">Click</button>
</template>

<script setup>
const handleClick = (e) => {
  console.log(e.currentTarget);
};
</script>
```

### React Conditional Rendering → Vue Conditional Rendering

**Vue 3:**
```vue
<p v-if="isVisible">Visible</p>
<component :is="condition ? 'A' : 'B'" />
```

### React Lists → Vue Lists

**Vue 3:**
```vue
<div v-for="item in items" :key="item.id">{{ item.name }}</div>
```

---

## Installation & Setup

### 1. Install Dependencies

```bash
npm install @syncfusion/ej2-vue-inputs
npm install @syncfusion/ej2-base
```

### 2. Register License (if using enterprise version)

```typescript
// main.ts or main.js
import { registerLicense } from '@syncfusion/ej2-base';

registerLicense('Your_License_Key');
```

### 3. Import Styles

```vue
<script setup>
import '@syncfusion/ej2-base/styles/material.css';
import '@syncfusion/ej2-inputs/styles/material.css';
</script>
```

### 4. Use Components

```vue
<template>
  <UploaderComponent ref="uploaderRef" :asyncSettings="asyncSettings" />
</template>

<script setup>
import { ref } from 'vue';
import { UploaderComponent } from '@syncfusion/ej2-vue-inputs';
</script>
```

---

## Common Patterns & Best Practices

### Form Integration

Use `v-model` for two-way binding and form submission handling:

```vue
<template>
  <form @submit.prevent="submitForm">
    <NumericTextBoxComponent v-model="form.amount" />
    <TextBoxComponent v-model="form.name" />
    <button type="submit">Submit</button>
  </form>
</template>

<script setup>
import { ref } from 'vue';
import { reactive } from 'vue';

const form = reactive({
  amount: 0,
  name: ''
});

const submitForm = () => {
  console.log('Form submitted:', form);
};
</script>
```

### Error Handling

Handle errors gracefully with try-catch and error states:

```vue
<template>
  <div v-if="error" class="error">{{ error }}</div>
  <UploaderComponent v-else @failure="handleError" />
</template>

<script setup>
import { ref } from 'vue';

const error = ref(null);

const handleError = (args) => {
  error.value = `Error: ${args.statusText}`;
  setTimeout(() => {
    error.value = null;
  }, 5000);
};
</script>
```

### Accessibility

Always include proper ARIA labels and semantic HTML:

```vue
<template>
  <div class="form-group">
    <label for="name">Name:</label>
    <TextBoxComponent id="name" aria-label="Full name" />
  </div>
</template>

<script setup>
import { TextBoxComponent } from '@syncfusion/ej2-vue-inputs';
</script>
```

---

## Troubleshooting

### Issue: Component not rendering
**Solution:** Ensure you've imported styles and registered the component correctly.

### Issue: Two-way binding not working
**Solution:** Use `v-model` for Vue 3 components, not `.sync` (deprecated).

### Issue: Events not firing
**Solution:** Ensure event names are in camelCase and use `@` prefix for event binding.

### Issue: Ref undefined in script
**Solution:** Remember to call `.value` in script setup, not in template.

