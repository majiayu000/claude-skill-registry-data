---
name: "naive-ui-skills"
description: "Naive UI Skills Library - A comprehensive skill library for AI agents to understand and utilize Naive UI components. Invoke when user needs to work with Naive UI components, theming, i18n, dark mode, or design specifications."
metadata:
  author: jiaiyan
  version: "1.0.0"
---

# Naive UI Skills Library

A comprehensive skill library for Naive UI framework, designed for AI agents to understand and utilize Naive UI components effectively.

## When to Invoke

Invoke this skill when:
- User needs to implement any Naive UI component
- User asks about Naive UI configuration or setup
- User wants to customize themes or use dark mode
- User needs internationalization (i18n) support
- User asks about design specifications (colors, borders, typography)
- User encounters issues with Naive UI components

## Skill Library Overview

This library contains **107 skills** organized into the following categories:

| Category | Count | Description | Path Pattern |
|----------|-------|-------------|--------------|
| Component Skills | 95 | Individual component documentation | `./components/n-{name}/SKILL.md` |
| Design Specifications | 5 | Border, Color, Layout, Typography, Overview | `./naive-ui-design-{name}/SKILL.md` |
| Foundation Skills | 6 | Quickstart, Theming, i18n, Dark Mode, SSR, Components | `./naive-ui-{name}/SKILL.md` |

## How to Locate Skills

### 1. Component Skills (95 skills)

All component skills follow the naming convention `n-{component-name}` and are located in the `components/` directory.

**Path Pattern:**
```
./components/n-{component-name}/SKILL.md
```

**Examples:**
- Button: `./components/n-button/SKILL.md`
- Form: `./components/n-form/SKILL.md`
- DataTable: `./components/n-data-table/SKILL.md`
- Dialog: `./components/n-dialog/SKILL.md`

### 2. Design Specification Skills (5 skills)

Design skills provide guidance on Naive UI design system.

| Skill Name | Path | Description |
|------------|------|-------------|
| Border | `./naive-ui-design-border/SKILL.md` | Border styles, radius, shadows |
| Color | `./naive-ui-design-color/SKILL.md` | Color palette and semantics |
| Layout | `./naive-ui-design-layout/SKILL.md` | Grid system and layout |
| Typography | `./naive-ui-design-typography/SKILL.md` | Font conventions |
| Overview | `./naive-ui-design-overview/SKILL.md` | Design system overview |

### 3. Foundation Skills (6 skills)

Foundation skills cover core setup and configuration.

| Skill Name | Path | Description |
|------------|------|-------------|
| Quickstart | `./naive-ui-quickstart/SKILL.md` | Installation and setup |
| Theming | `./naive-ui-theming/SKILL.md` | Theme customization |
| i18n | `./naive-ui-i18n/SKILL.md` | Internationalization |
| Dark Mode | `./naive-ui-dark-mode/SKILL.md` | Dark mode implementation |
| SSR | `./naive-ui-ssr/SKILL.md` | Server-side rendering |
| Components | `./naive-ui-components/SKILL.md` | Component overview index |

## Skill Invocation Guide

### Step 1: Identify User Intent

Analyze the user's request to determine which skill category is needed:

| User Request Pattern | Skill Category | Example Skill |
|---------------------|----------------|---------------|
| "Create a button/form/table..." | Component | `n-button`, `n-form`, `n-data-table` |
| "How to set up Naive UI" | Foundation | `naive-ui-quickstart` |
| "Customize theme colors" | Foundation | `naive-ui-theming` |
| "Add multi-language support" | Foundation | `naive-ui-i18n` |
| "Implement dark mode" | Foundation | `naive-ui-dark-mode` |
| "What colors are available?" | Design | `naive-ui-design-color` |
| "How does the grid work?" | Design | `naive-ui-design-layout` |

### Step 2: Locate the Skill File

Use the path patterns above to locate the appropriate skill file:

```markdown
# For component skills
./components/n-{component-name}/SKILL.md

# For design skills
./naive-ui-design-{name}/SKILL.md

# For foundation skills
./naive-ui-{name}/SKILL.md
```

### Step 3: Read and Apply Skill Content

Each skill file contains:
- **When to Invoke**: Specific conditions for using the skill
- **Features**: Component capabilities and options
- **API Reference**: Attributes, events, slots, exposes
- **Usage Examples**: Code snippets for common patterns
- **Best Practices**: Recommended implementation guidelines

## Component Skill Index

### Common Components (15)

| Component | Skill Path | Description |
|-----------|------------|-------------|
| Avatar | `./components/n-avatar/SKILL.md` | User avatars |
| Button | `./components/n-button/SKILL.md` | Buttons with various types and states |
| Card | `./components/n-card/SKILL.md` | Card containers |
| Carousel | `./components/n-carousel/SKILL.md` | Image carousel |
| Collapse | `./components/n-collapse/SKILL.md` | Collapsible panels |
| Divider | `./components/n-divider/SKILL.md` | Dividing lines |
| Dropdown | `./components/n-dropdown/SKILL.md` | Dropdown menu |
| Ellipsis | `./components/n-ellipsis/SKILL.md` | Text ellipsis |
| Float Button | `./components/n-float-button/SKILL.md` | Floating button |
| Gradient Text | `./components/n-gradient-text/SKILL.md` | Gradient text effect |
| Icon | `./components/n-icon/SKILL.md` | Icon wrapper component |
| Page Header | `./components/n-page-header/SKILL.md` | Page header |
| Tag | `./components/n-tag/SKILL.md` | Tags and labels |
| Typography | `./components/n-typography/SKILL.md` | Typography components |
| Watermark | `./components/n-watermark/SKILL.md` | Watermark |

### Data Input Components (21)

| Component | Skill Path | Description |
|-----------|------------|-------------|
| Auto Complete | `./components/n-auto-complete/SKILL.md` | Input with suggestions |
| Cascader | `./components/n-cascader/SKILL.md` | Cascading selection |
| Checkbox | `./components/n-checkbox/SKILL.md` | Checkboxes |
| Color Picker | `./components/n-color-picker/SKILL.md` | Color picker |
| Date Picker | `./components/n-date-picker/SKILL.md` | Date picker |
| Dynamic Input | `./components/n-dynamic-input/SKILL.md` | Dynamic input fields |
| Dynamic Tags | `./components/n-dynamic-tags/SKILL.md` | Dynamic tags input |
| Form | `./components/n-form/SKILL.md` | Form management |
| Input | `./components/n-input/SKILL.md` | Text input |
| Input Number | `./components/n-input-number/SKILL.md` | Number input |
| Input OTP | `./components/n-input-otp/SKILL.md` | OTP input |
| Mention | `./components/n-mention/SKILL.md` | Mention input |
| Radio | `./components/n-radio/SKILL.md` | Radio buttons |
| Rate | `./components/n-rate/SKILL.md` | Star rating |
| Select | `./components/n-select/SKILL.md` | Dropdown select |
| Slider | `./components/n-slider/SKILL.md` | Slider input |
| Switch | `./components/n-switch/SKILL.md` | Toggle switch |
| Time Picker | `./components/n-time-picker/SKILL.md` | Time picker |
| Transfer | `./components/n-transfer/SKILL.md` | Transfer panels |
| Tree Select | `./components/n-tree-select/SKILL.md` | Tree select |
| Upload | `./components/n-upload/SKILL.md` | File upload |

### Data Display Components (21)

| Component | Skill Path | Description |
|-----------|------------|-------------|
| Calendar | `./components/n-calendar/SKILL.md` | Calendar view |
| Code | `./components/n-code/SKILL.md` | Code display |
| Countdown | `./components/n-countdown/SKILL.md` | Countdown timer |
| Data Table | `./components/n-data-table/SKILL.md` | Advanced data table |
| Descriptions | `./components/n-descriptions/SKILL.md` | Description list |
| Empty | `./components/n-empty/SKILL.md` | Empty state |
| Equation | `./components/n-equation/SKILL.md` | Math equation |
| Heatmap | `./components/n-heatmap/SKILL.md` | Heatmap visualization |
| Highlight | `./components/n-highlight/SKILL.md` | Code highlight |
| Image | `./components/n-image/SKILL.md` | Image with preview |
| Infinite Scroll | `./components/n-infinite-scroll/SKILL.md` | Infinite scroll |
| List | `./components/n-list/SKILL.md` | List container |
| Log | `./components/n-log/SKILL.md` | Log display |
| Number Animation | `./components/n-number-animation/SKILL.md` | Animated numbers |
| QR Code | `./components/n-qr-code/SKILL.md` | QR code generator |
| Statistic | `./components/n-statistic/SKILL.md` | Statistics display |
| Table | `./components/n-table/SKILL.md` | Basic table |
| Thing | `./components/n-thing/SKILL.md` | Thing container |
| Time | `./components/n-time/SKILL.md` | Time display |
| Timeline | `./components/n-timeline/SKILL.md` | Timeline display |
| Tree | `./components/n-tree/SKILL.md` | Tree view |

### Navigation Components (9)

| Component | Skill Path | Description |
|-----------|------------|-------------|
| Affix | `./components/n-affix/SKILL.md` | Sticky positioning |
| Anchor | `./components/n-anchor/SKILL.md` | Anchor navigation |
| Back Top | `./components/n-back-top/SKILL.md` | Back to top button |
| Breadcrumb | `./components/n-breadcrumb/SKILL.md` | Breadcrumb navigation |
| Loading Bar | `./components/n-loading-bar/SKILL.md` | Loading bar |
| Menu | `./components/n-menu/SKILL.md` | Navigation menu |
| Pagination | `./components/n-pagination/SKILL.md` | Pagination |
| Steps | `./components/n-steps/SKILL.md` | Steps guide |
| Tabs | `./components/n-tabs/SKILL.md` | Tabs |

### Feedback Components (16)

| Component | Skill Path | Description |
|-----------|------------|-------------|
| Alert | `./components/n-alert/SKILL.md` | Alert messages |
| Badge | `./components/n-badge/SKILL.md` | Badges and marks |
| Dialog | `./components/n-dialog/SKILL.md` | Modal dialog |
| Drawer | `./components/n-drawer/SKILL.md` | Drawer panel |
| Marquee | `./components/n-marquee/SKILL.md` | Marquee animation |
| Message | `./components/n-message/SKILL.md` | Toast message |
| Modal | `./components/n-modal/SKILL.md` | Modal container |
| Notification | `./components/n-notification/SKILL.md` | Notification |
| Popconfirm | `./components/n-popconfirm/SKILL.md` | Popconfirm |
| Popover | `./components/n-popover/SKILL.md` | Popover |
| Popselect | `./components/n-popselect/SKILL.md` | Popover select |
| Progress | `./components/n-progress/SKILL.md` | Progress bar |
| Result | `./components/n-result/SKILL.md` | Result page |
| Skeleton | `./components/n-skeleton/SKILL.md` | Loading skeleton |
| Spin | `./components/n-spin/SKILL.md` | Loading spinner |
| Tooltip | `./components/n-tooltip/SKILL.md` | Tooltip |

### Layout Components (6)

| Component | Skill Path | Description |
|-----------|------------|-------------|
| Flex | `./components/n-flex/SKILL.md` | Flex container |
| Grid | `./components/n-grid/SKILL.md` | Grid system |
| Layout | `./components/n-layout/SKILL.md` | Layout container |
| Legacy Grid | `./components/n-legacy-grid/SKILL.md` | Legacy grid |
| Space | `./components/n-space/SKILL.md` | Spacing |
| Split | `./components/n-split/SKILL.md` | Split panels |

### Config Components (3)

| Component | Skill Path | Description |
|-----------|------------|-------------|
| Config Provider | `./components/n-config-provider/SKILL.md` | Global config |
| Element | `./components/n-element/SKILL.md` | Element wrapper |
| Global Style | `./components/n-global-style/SKILL.md` | Global styles |

### Utility Components (4)

| Component | Skill Path | Description |
|-----------|------------|-------------|
| Collapse Transition | `./components/n-collapse-transition/SKILL.md` | Collapse animation |
| Discrete | `./components/n-discrete/SKILL.md` | Discrete API |
| Scrollbar | `./components/n-scrollbar/SKILL.md` | Custom scrollbar |
| Virtual List | `./components/n-virtual-list/SKILL.md` | Virtual scroll list |

## Usage Examples

### Example 1: User asks about button implementation

**User Request:** "How do I create a primary button with loading state?"

**Agent Action:**
1. Identify intent: Component skill - Button
2. Locate skill: `./components/n-button/SKILL.md`
3. Read skill content
4. Provide response with API reference and code example

**Response:**
```vue
<template>
  <n-button type="primary" :loading="loading" @click="handleClick">
    {{ loading ? 'Loading...' : 'Submit' }}
  </n-button>
</template>

<script setup>
import { ref } from 'vue'

const loading = ref(false)

const handleClick = async () => {
  loading.value = true
  try {
    await submitData()
  } finally {
    loading.value = false
  }
}
</script>
```

### Example 2: User asks about form validation

**User Request:** "How do I create a form with validation?"

**Agent Action:**
1. Identify intent: Component skill - Form
2. Locate skill: `./components/n-form/SKILL.md`
3. Read skill content
4. Provide response with validation example

**Response:**
```vue
<template>
  <n-form ref="formRef" :model="form" :rules="rules">
    <n-form-item label="Name" path="name">
      <n-input v-model:value="form.name" />
    </n-form-item>
    <n-form-item>
      <n-button type="primary" @click="submitForm">Submit</n-button>
    </n-form-item>
  </n-form>
</template>

<script setup>
import { ref, reactive } from 'vue'

const formRef = ref()
const form = reactive({
  name: ''
})

const rules = {
  name: [
    { required: true, message: 'Please input name', trigger: 'blur' }
  ]
}

const submitForm = async () => {
  await formRef.value?.validate()
  // Submit logic
}
</script>
```

### Example 3: User asks about theme customization

**User Request:** "How do I customize Naive UI theme colors?"

**Agent Action:**
1. Identify intent: Foundation skill - Theming
2. Locate skill: `./naive-ui-theming/SKILL.md`
3. Read skill content
4. Provide response with theme override example

**Response:**
```vue
<template>
  <n-config-provider :theme-overrides="themeOverrides">
    <App />
  </n-config-provider>
</template>

<script setup>
const themeOverrides = {
  common: {
    primaryColor: '#18a058',
    primaryColorHover: '#36ad6a',
    primaryColorPressed: '#0c7a43'
  },
  Button: {
    textColor: '#18a058'
  }
}
</script>
```

### Example 4: User asks about dark mode

**User Request:** "How do I implement dark mode in Naive UI?"

**Agent Action:**
1. Identify intent: Foundation skill - Dark Mode
2. Locate skill: `./naive-ui-dark-mode/SKILL.md`
3. Read skill content
4. Provide response with implementation example

**Response:**
```vue
<template>
  <n-config-provider :theme="isDark ? darkTheme : null">
    <App />
  </n-config-provider>
</template>

<script setup>
import { ref } from 'vue'
import { darkTheme } from 'naive-ui'

const isDark = ref(false)
</script>
```

## Configuration Requirements

### Prerequisites

Before using this skill library, ensure:

1. **Vue 3.0+** is installed
2. **Naive UI 2.44+** is installed
3. **Node.js 18+** for development

### Installation

```bash
npm install naive-ui
# or
pnpm add naive-ui
```

### TypeScript Support

Naive UI is written in TypeScript and provides full type definitions out of the box.

## Input Parameters

When invoking skills, consider these parameters:

| Parameter | Type | Description | Required |
|-----------|------|-------------|----------|
| component | string | Component name (e.g., "button", "form") | Yes |
| feature | string | Specific feature needed (e.g., "validation", "loading") | No |
| context | object | Additional context (framework, TypeScript usage) | No |

## Output Format

Each skill provides:

1. **API Reference**: Complete attributes, events, slots, exposes
2. **Code Examples**: Working code snippets
3. **Best Practices**: Recommended implementation patterns
4. **Common Issues**: Troubleshooting tips
5. **Component Interactions**: How to use with other components

## Important Notes

### 1. Skill Priority

When multiple skills could apply, prioritize in this order:
1. Component-specific skills (most specific)
2. Foundation skills (configuration)
3. Design specification skills (guidelines)

### 2. Cross-References

Many skills reference related skills. Always check:
- Related components in the same category
- Foundation skills for configuration
- Design skills for styling guidelines

### 3. Version Compatibility

This skill library is based on Naive UI 2.44+. Some features may not be available in earlier versions.

### 4. Naming Conventions

- Component skills use `n-{name}` format (matches Vue component tags)
- Foundation skills use `naive-ui-{name}` format
- Design skills use `naive-ui-design-{name}` format

### 5. File Structure

```
naive-ui-skills/
├── SKILL.md                          # This file (main entry)
├── README.md                         # English documentation
├── README_CN.md                      # Chinese documentation
├── AGENTS.md                         # Agents documentation
├── LICENSE                           # MIT License
├── components/                       # 95 component skills
│   ├── n-button/
│   │   └── SKILL.md
│   ├── n-form/
│   │   └── SKILL.md
│   └── ...
├── naive-ui-quickstart/              # Foundation skills
├── naive-ui-theming/
├── naive-ui-i18n/
├── naive-ui-dark-mode/
├── naive-ui-ssr/
├── naive-ui-components/
├── naive-ui-design-border/           # Design skills
├── naive-ui-design-color/
├── naive-ui-design-layout/
├── naive-ui-design-typography/
└── naive-ui-design-overview/
```

## Best Practices for Agents

1. **Always start with this file** when user mentions Naive UI
2. **Locate the specific skill** based on user intent
3. **Read the complete skill file** before responding
4. **Provide code examples** from the skill documentation
5. **Reference related skills** when applicable
6. **Include best practices** from the skill content
7. **Mention common issues** if relevant to user's context

## Related Resources

- [Naive UI Documentation](https://www.naiveui.com/)
- [Vue 3 Documentation](https://vuejs.org/)
- [Naive UI GitHub](https://github.com/tusen-ai/naive-ui)
