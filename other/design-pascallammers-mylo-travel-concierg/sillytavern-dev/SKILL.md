---
name: sillytavern-dev
description: Expert skill for developing SillyTavern frontend interfaces and scripts using Tavern Helper framework. Use when users request creating interactive UI for character cards, background scripts for automation, MVU variable visualization, or any SillyTavern extension development. Provides complete tech stack (Vue/React/PixiJS), API documentation, development best practices, and live preview workflows.
---

# SillyTavern Development Expert

Expert guidance for developing frontend interfaces and background scripts for SillyTavern using the Tavern Helper framework.

## When to Use This Skill

Use this skill when users request:

- ✅ **Frontend interfaces** - Interactive UI in message floors (status bars, game systems, multimedia displays)
- ✅ **Background scripts** - Automation, chat enhancement, external service integration
- ✅ **Character card features** - Enhanced gameplay, visual effects, data visualization
- ✅ **MVU variable framework** - Message floor variable management and display
- ✅ **SillyTavern UX improvements** - UI tweaks, workflow automation, custom tools

## Core Concepts

### Project Types

Projects live in `src/项目名/` folders:

**Frontend Interface** (`index.ts` + `index.html`):
- Runs as **sandboxless iframe** in message floor (foreground)
- Has visual UI with styles and interactions
- **Preferred stack**: Vue 3 + Pinia + Vue Router

**Script** (`index.ts` only):
- Runs as **sandboxless iframe** in background
- No visual UI, code-only
- jQuery operates on parent SillyTavern page: `window.$ = window.parent.$`

### Data Persistence: Tavern Variables

Use `getVariables()` / `replaceVariables()` for persistent storage:

- `global` - Shared across entire tavern
- `character` - Bound to specific character card
- `chat` - Bound to specific chat file
- `message` - Bound to specific message floor
- `script` - Bound to specific script
- `extension` - Bound to specific extension

### MVU Variable Framework

Separate Tavern Helper script enhancing message floor variables:

- Set variables in world info
- Auto-update variables from AI output
- Provides `display_data` and `delta_data` for visualization
- **Must initialize**: `await waitGlobalInitialized('Mvu')`

See `references/mvu_framework.md` for detailed API.

## Quick Start

### 1. Choose Project Type

Determine frontend interface or script based on whether UI is needed.

### 2. Select Tech Stack

**For frontend interfaces**:
- Simple UI: Vue 3 + Tailwind CSS
- Complex game: PixiJS + @pixi/react
- React preference: React + hooks

**For scripts**:
- DOM manipulation: jQuery + jQueryUI
- State management: Pinia + Zod
- Animations: GSAP

See `references/tech_stack.md` for full dependency list and usage patterns.

### 3. Development Workflow

```bash
# Install dependencies (pnpm only)
pnpm install

# Development build
pnpm run build:dev

# Watch mode (auto-rebuild)
pnpm run watch

# Production build
pnpm run build
```

### 4. Live Preview

**Option 1: Soft link (recommended)**
```bash
ln -s /path/to/dist/项目名/index.html /root/web-dev/preview.html
```

**Option 2: Copy**
```bash
cp /path/to/dist/项目名/index.html /root/web-dev/
```

**Access**: https://dev.piepia.space/preview.html

Use browsermcp to test in real browser environment.

## Development Best Practices

### TypeScript Required

```typescript
// ✅ Correct: TypeScript with Zod validation
import { z } from 'zod';

const Settings = z.object({
  volume: z.number().min(0).max(1).default(0.5),
  autoPlay: z.boolean().default(true),
}).prefault({});

type Settings = z.infer<typeof Settings>;
```

### Use Third-Party Libraries

```typescript
// ✅ jQuery for DOM
$('#button').on('click', handler);

// ✅ GSAP for animations (including typewriter)
gsap.to('#text', {
  duration: 2,
  text: { value: "New text", delimiter: "" },
  ease: "none"
});

// ✅ Zod for validation
const result = Schema.safeParse(data);
if (!result.success) {
  console.error(z.prettifyError(result.error));
}
```

### Correct Loading/Unloading Timing

```typescript
// ✅ Correct: jQuery ready handler
$(() => {
  toastr.success('Loaded');
  // Initialization logic...
});

// ✅ Correct: Cleanup on unload
$(window).on('pagehide', () => {
  toastr.info('Unloaded');
  // Cleanup: remove listeners, stop timers...
});

// ❌ Wrong: DOMContentLoaded doesn't fire on network load
document.addEventListener('DOMContentLoaded', () => {
  // Won't execute when loaded via $('body').load(url)!
});
```

### Reload on Chat Change

```typescript
let chat_id = SillyTavern.getCurrentChatId();

eventOn(tavern_events.CHAT_CHANGED, new_chat_id => {
  if (chat_id !== new_chat_id) {
    chat_id = new_chat_id;
    window.location.reload();
  }
});
```

## Frontend Interface Development

### index.html Rules

```html
<head>
  <!-- Keep empty - webpack auto-injects styles/scripts -->
</head>
<body>
  <!-- Static content only -->
  <div id="app"></div>

  <!-- ❌ NO <link rel="stylesheet" href="./index.css"> -->
  <!-- ❌ NO <script src="./index.ts"> -->
  <!-- ❌ NO <img src=""> empty placeholders -->
</body>
```

### Styling Approaches

```typescript
// Method 1: Tailwind CSS (simple styles)
import './tailwind.css'; // Content: @import 'tailwindcss';

// Method 2: Vue component styles (recommended)
// Component.vue
<template>...</template>
<style lang="scss" scoped>
  .my-class { color: red; }
</style>

// Method 3: Global SCSS
import './index.scss';
```

### iframe Adaptation

```scss
// ✅ Use width + aspect-ratio (NOT vh)
.container {
  width: 100%;
  aspect-ratio: 16 / 9;
}

// ❌ Avoid forcing parent height
.bad {
  min-height: 500px; // Not recommended
  overflow: auto;    // May cause scrollbars
}

// ✅ Fit container width, no horizontal scroll
body {
  max-width: 100%;
  overflow-x: hidden;
}

// ✅ Card style: transparent background (unless explicitly requested)
.card {
  background: transparent;
}
```

### Vue Development Template

See `references/vue_template.md` for complete Vue 3 + Pinia + Vue Router setup.

### PixiJS Multimedia Interface

See `references/pixijs_usage.md` for game-like interfaces with heavy multimedia assets.

## Script Development

### jQuery Scope

```typescript
// ⚠️ $ operates on SillyTavern page, not iframe
$('body'); // Selects SillyTavern <body>

// Select iframe elements
$('body', document); // document = script iframe
```

### Using Vue in Scripts

```typescript
// 1. Create mount point with jQuery
const $app = $('<div>').attr('id', 'my-app').appendTo('body');

// 2. Create Vue app
const app = createApp(App);
app.use(createPinia());

// 3. Mount to jQuery element
app.mount($app[0]); // Note [0] to get DOM element

// 4. Cleanup
$(window).on('pagehide', () => {
  app.unmount();
  $app.remove();
});
```

### Teleporting Styles to SillyTavern Page

```typescript
// Script styles only apply to iframe - manually teleport to parent

export function teleport_style() {
  $(`<div>`)
    .attr('script_id', getScriptId())
    .append($(`head > style`, document).clone())
    .appendTo('head'); // Appends to SillyTavern <head>
}

export function deteleport_style() {
  $(`head > div[script_id="${getScriptId()}"]`).remove();
}

$(() => teleport_style());
$(window).on('pagehide', () => deteleport_style());
```

### Script Settings UI

See `references/script_patterns.md` for Pinia + Zod settings management pattern.

### Registering Script Buttons

```typescript
// Triggered when user clicks button in Tavern Helper script library
eventOn(getButtonEvent('Reload'), () => {
  window.location.reload();
});

eventOn(getButtonEvent('Clear Data'), () => {
  if (confirm('Clear all data?')) {
    replaceVariables({}, { type: 'script', script_id: getScriptId() });
    toastr.success('Data cleared');
  }
});
```

## API Priority

**Priority order**: Tavern Helper API > STScript Commands > SillyTavern Native API

```typescript
// ❌ Don't: STScript
await triggerSlash('/setvar key=score 100');
const score = await triggerSlash('/getvar score');

// ✅ Do: Tavern Helper API
replaceVariables({ score: 100 }, { type: 'chat' });
const score = getVariables({ type: 'chat' }).score;

// ✅ Do: toastr instead of /echo
toastr.success('Hello');

// ✅ Do: Tavern Helper functions
const messages = getChatMessages(); // Instead of SillyTavern.chat
replaceWorldbook(data);             // Instead of /setentryfield
```

**Reason**: Tavern Helper API provides:
- ✅ Type safety (full TypeScript support)
- ✅ Higher abstraction (semantic operations)
- ✅ Better error handling
- ✅ Better performance (less string parsing)

## Resources

### references/

Detailed documentation loaded as needed:

- `tech_stack.md` - Complete dependency list and usage patterns
- `api_reference.md` - Tavern Helper API documentation
- `stscript_commands.md` - All 264 STScript commands with examples
- `type_definitions.md` - TypeScript type system overview
- `vue_template.md` - Vue 3 + Pinia + Router setup
- `script_patterns.md` - Common script development patterns
- `pixijs_usage.md` - PixiJS multimedia interface guide
- `mvu_framework.md` - MVU variable framework API
- `best_practices.md` - Development do's and don'ts

### assets/

Template files for quick project initialization:

- `frontend-template/` - Vue 3 frontend interface boilerplate
- `script-template/` - Background script boilerplate
- `tailwind.css` - Tailwind CSS import file

## Common Patterns

### Reactive Data + Tavern Variable Sync

```typescript
const data = ref({ score: 0, hp: 100 });

// Load initial values
data.value = getVariables({ type: 'chat' });

// Auto-save (remove Vue Proxy with klona)
watchEffect(() => {
  replaceVariables(klona(data.value), { type: 'chat' });
});
```

### Listening to Tavern Events

```typescript
import { tavern_events, eventOn } from '@types/iframe/event';

// AI message received
eventOn(tavern_events.MESSAGE_RECEIVED, (message_id) => {
  console.log('New message', message_id);
});

// Message updated
eventOn(tavern_events.MESSAGE_UPDATED, (message_id) => {
  console.log('Message updated', message_id);
});
```

### Calling LLM

```typescript
// Simple generation (with chat history + character card)
const result = await generate({
  prompt: 'Summarize the conversation',
  quietPrompt: 'Summarize in 50 words or less',
});

// Raw generation (no chat history)
const result = await triggerSlash(`
  /genraw instruct=off Why is the sky blue?
`);
```

### Error Handling with Zod

```typescript
const UserInput = z.object({
  name: z.string().min(1),
  age: z.number().int().positive(),
});

const result = UserInput.safeParse(data);

if (!result.success) {
  toastr.error(z.prettifyError(result.error));
  return;
}

const { name, age } = result.data; // Type-safe
```

## Forbidden Practices

❌ Node.js libraries (fs, path, http, etc.)
❌ `<link>` / `<script>` tags in index.html for local files
❌ `DOMContentLoaded` for load timing
❌ `vh` units in frontend interface styles (use `aspect-ratio`)
❌ Direct code execution in global scope (use `$(() => {})`)
❌ Saving Vue reactive data directly (use `klona()` first)

## Output Requirements

When developing features for users:

1. **Confirm project type** - Frontend interface or script?
2. **Choose tech stack** - Vue (recommended) / React / PixiJS?
3. **Data persistence plan** - Which variable type?
4. **Provide complete code**:
   - Clear TypeScript types
   - Use recommended libraries
   - Follow best practices
   - Include error handling
5. **Test with preview** - Build and preview on dev.piepia.space via browsermcp
6. **Code documentation** - Comment key logic, explain special usage

## Working Directory

**Current directory**: `/root/tavern_helper_template`
