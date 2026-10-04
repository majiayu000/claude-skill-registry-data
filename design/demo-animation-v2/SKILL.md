---
name: demo-animation-v2
description: Generate the recommended responsive self-playing HTML product demo. Creates a single-file index.html with intro screen, dashboard mockup, step-by-step animation, captions, timeline controls, piano music, cursor animation, highlights, ending screen, mobile controls, touch gestures, fullscreen API, landscape hint, and prefers-reduced-motion support.
metadata:
  version: 3.0.0
---

# Demo Animation v2

Generate the recommended responsive self-playing HTML product demo. Output: `demo/index.html`.

## How it works

This skill uses `assets/template.html` as the reusable demo engine. Read the template, fill in all `{{PLACEHOLDER}}` markers with project-specific content, and write the completed single-file demo to `demo/index.html`.

The template contains the complete reusable engine: CSS framework, JS animation system, mobile controls, touch gestures, fullscreen, piano music, and accessibility support.

## Workflow

### 1. Read the project

Read CLAUDE.md, README, main files. Identify: product name, tagline, color palette, font stack, 6-10 key features, UI layout type.

### 2. Plan steps briefly

List 6-10 demo steps for the user. Do not wait for confirmation unless unsure. Start generating.

### 3. Read the template

Read `assets/template.html` from this skill folder. This is your base file.

### 4. Fill placeholders and write

Read the template, replace all `{{PLACEHOLDER}}` markers, and write the result to `demo/index.html`.

#### Placeholder reference

**Metadata:**
- `{{PAGE_TITLE}}` - e.g. "My Project Demo"
- `{{GOOGLE_FONTS_LINK}}` - `<link href="https://fonts.googleapis.com/css2?family=...&display=swap" rel="stylesheet">`

**CSS variables:**
`{{PRIMARY_DARK}}`, `{{PRIMARY_DARK_LIGHT}}`, `{{ACCENT}}`, `{{ACCENT_LIGHT}}`, `{{ACCENT_GLOW}}`, `{{BG_LIGHT}}`, `{{BG_LIGHT_DARK}}`, `{{BORDER}}`, `{{TEXT}}`, `{{TEXT_LIGHT}}`, `{{FONT_SERIF}}`, `{{FONT_SANS}}`

**Content:**
- `{{PANE_CSS}}` - CSS for tab pane layouts.
- `{{INTRO_CONTENT}}` - Logo, subtitle, and tagline divs. The button is already in the template.
- `{{NAV_BRAND_NAME}}` / `{{NAV_APP_NAME}}` - Navbar text.
- `{{NAV_TABS}}` - Tab buttons: `<div class="nav-tab active" id="tab-NAME">Label</div>`.
- `{{TAB_PANES}}` - Tab content: `<div class="tab-pane active pane-NAME" id="pane-NAME">...</div>`.
- `{{TIMELINE_STEPS}}` - `<div class="tl-step-v" data-step="N"><div class="tl-dot"></div><div class="tl-label">Name</div></div>`.
- `{{ENDING_CONTENT}}` - Title, subtitle, and URL divs.

**JavaScript:**
- `{{TOTAL_STEPS}}` - Number, e.g. `8`.
- `{{RESET_ALL_UI}}` - `function resetAllUI(){ ... }` resets all DOM changes.
- `{{STEP_FUNCTIONS}}` - All `async function stepN(id){ ... }` functions.
- `{{STEPS_ARRAY}}` - `step0,step1,...,stepN`.
- `{{EXTRA_JS}}` - Project-specific JS, or an empty string.

## Step function pattern

```js
async function step0(id){
  showTab('tabname');
  updateTimeline(0);
  setCaption('Step 1 of N','Headline','Detail.');
  await wait(1200,id);if(dead(id))return;

  const el=$('#element');
  await moveCursor(getCenter(el).x,getCenter(el).y,500,id);
  if(dead(id))return;
  showHighlight(el);
  await wait(1000,id);if(dead(id))return;
  hideHighlight();
  hideCursor();
}
```

**Rules:**
1. `showTab()` and `updateTimeline()` first.
2. Add `if(dead(id))return;` after every `await`.
3. Pass `id` to `moveCursor(x,y,dur,id)` and `wait(ms,id)`.
4. Call `hideCursor()` at the end of each step.

**Available helpers:** `showTab(name)`, `setCaption(step,text,detail)`, `hideCaption()`, `moveCursor(x,y,dur,id)`, `hideCursor()`, `showHighlight(el)`, `hideHighlight()`, `showToast(msg)`, `updateTimeline(idx)`, `typeText(el,text,speed)`, `scrollToShow(el,container)`, `getCenter(el)`, `getLocalPos(el)`, `wait(ms,id)`, `dead(id)`.

## Rules

- File must be self-contained except Google Fonts.
- Every `$('#id')` must target an element that exists.
- Design realistic UI matching the actual product.
- Keep wait times reasonable: 800-1500ms for reading, 300-600ms for animations.

## Output

Write to `demo/index.html`. Tell the user:

```text
Demo created at `demo/index.html`. Open it in a browser to preview. Fully responsive: desktop, tablet, and mobile.
```
