---
name: ui-storybook-docs
description: Generate consumer-facing documentation for a shared UI component — MDX docs page, Storybook 8 stories file, and prop table — sourced directly from a ui-component-spec output. Use this after a component is implemented and the team needs publishable documentation for a design system or shared UI library.
status: draft
---

# UI Storybook Docs

A skill for bridging the gap between an internal component spec and a public-facing UI library. It reads the `ui-component-spec` output and produces three files: an MDX documentation page, a Storybook 8 stories file, and a prop table. The documentation is written for component consumers — developers who did not write the component and want to know when to use it, what props it accepts, and which variant to reach for first.

## When to use this skill

Use this skill when:
- A `ui-component-spec` output exists for the component.
- The component is implemented and shared (lives in a design system, shared UI library, or component package used by more than one team or project).
- The team uses Storybook and wants published, browsable documentation.
- The user says "write the docs for this component" or "set up Storybook stories."

Do **not** use this skill when:
- No `ui-component-spec` exists. The output would be invented props and invented usage guidance. Run `ui-component-spec` first and get it approved.
- The component is a one-off (used in exactly one screen, not shared). Documentation overhead is not justified.
- The component is not yet implemented. Writing stories for a non-existent component produces docs that go stale the moment the API changes.
- The team does not use Storybook. In that case produce only the prop table and usage guidelines in plain markdown.

## Core principle

**Good component documentation shows the WHY, not just the WHAT.** A prop table describes the API. Usage guidelines explain when to reach for this component, when not to, which variant is the default, and what mistakes consumers make. The `ui-component-spec` is author-facing — it explains how the component is built. The MDX page is consumer-facing — it explains how to use it. They are different documents for different audiences. Never copy-paste the spec into the docs.

## Pre-flight check

Before drafting, confirm:

1. **The `ui-component-spec` is approved.** Do not write docs for a spec in draft status — the API may still change.
2. **The component name.** Confirm the exact export name (e.g., `Button`, `TextInput`, `DataTable`) — this becomes the file name and the Storybook title.
3. **The framework.** React is assumed by default. If the component is Vue, Svelte, or another framework, note it — the stories syntax differs.
4. **The Storybook version.** This skill targets Storybook 8. If the team is on 6 or 7, the CSF syntax is the same but some block imports differ.

If any is missing, ask. Do not guess the component name or framework.

## Output: 3 files

### File 1 — `ComponentName.mdx` (Storybook docs page)

The MDX file is the human-readable page that appears in the Storybook Docs tab. It explains the component to a developer who has never used it before.

**Structure:**

```mdx
import { Meta, Canvas, Controls, Story } from '@storybook/blocks';
import * as ComponentStories from './ComponentName.stories';

<Meta of={ComponentStories} />

# ComponentName

> One sentence. What does this component do and why does it exist in the system? Not a list of props — a statement of purpose.

## When to use

- <Specific use case — e.g., "Use when a user must confirm a destructive action before proceeding.">
- <Second use case>
- <Third use case if needed; stop at 4–5 maximum>

## When NOT to use

- <Anti-use-case — e.g., "Do not use for primary navigation — use NavItem instead.">
- <Second anti-use-case>
- <Note the preferred alternative component where one exists>

## Default variant

The default story shows the most common usage. Start here.

<Canvas of={ComponentStories.Default} />
<Controls />

## All variants

<Canvas of={ComponentStories.Disabled} />
<Canvas of={ComponentStories.Loading} />
<Canvas of={ComponentStories.Error} />
<Canvas of={ComponentStories.Empty} />

(Include a Canvas block for each story that exists. Do not include stories that are not defined.)

## Prop reference

(Insert prop table — see File 3)

## Accessibility notes

- <Note derived from the component spec's a11y section — e.g., "The trigger element must have an accessible name. Use the `label` prop or wrap with a visually hidden span.">
- <Note 2 — e.g., "When `loading` is true, the component sets `aria-busy="true"` automatically.">
- <Note 3 if applicable>

## Keyboard behavior

| Key | Action |
|---|---|
| Tab | Move focus to next interactive element |
| Enter / Space | Activate (buttons, checkboxes, toggles) |
| Escape | Close (popovers, dialogs, dropdowns) |
| Arrow keys | Navigate within component (menus, tabs, date pickers) |

(Include only keys that apply to this component, sourced from the component spec keyboard map.)
```

**Rules for the MDX page:**
- The one-sentence description must state what the component does and why it exists in the system. It must not list props.
- When-to-use bullets must be specific enough that a developer can make a yes/no decision. "Use for actions" is not specific. "Use when a user submits a form or triggers a server-side operation" is specific.
- When-NOT-to-use must name an alternative where one exists.
- Do not copy prose from the component spec. Re-write for a consumer audience.

---

### File 2 — `ComponentName.stories.ts` (Storybook stories)

The stories file defines every story that the MDX page references. Use Storybook 8 Component Story Format (CSF 3).

**Structure:**

```typescript
import type { Meta, StoryObj } from '@storybook/react';
import { ComponentName } from './ComponentName';

const meta: Meta<typeof ComponentName> = {
  title: 'Components/ComponentName',
  component: ComponentName,
  parameters: {
    layout: 'centered',
  },
  tags: ['autodocs'],
  argTypes: {
    // One entry per prop from the component spec.
    // Format: propName: { control: '<control-type>', description: '<one sentence from spec>' }
    // Control types: 'text' | 'number' | 'boolean' | 'select' | 'radio' | 'color' | 'date' | 'object' | 'file'
    label: {
      control: 'text',
      description: 'Visible label text. Used as the accessible name when no aria-label is provided.',
    },
    disabled: {
      control: 'boolean',
      description: 'When true, the component is non-interactive and visually muted.',
    },
    loading: {
      control: 'boolean',
      description: 'When true, shows a loading indicator and prevents interaction.',
    },
    // ... continue for all props
  },
};

export default meta;
type Story = StoryObj<typeof meta>;

// Default — the most common usage, matching the component spec's "default" state.
export const Default: Story = {
  args: {
    label: 'Button label',
    disabled: false,
    loading: false,
  },
};

// One story per state defined in the component spec's states matrix.
export const Disabled: Story = {
  args: {
    ...Default.args,
    disabled: true,
  },
};

export const Loading: Story = {
  args: {
    ...Default.args,
    loading: true,
  },
};

export const Error: Story = {
  args: {
    ...Default.args,
    error: 'Something went wrong. Please try again.',
  },
};

export const Empty: Story = {
  args: {
    // Set props to produce the empty state as defined in the component spec.
  },
};
```

**Rules for stories:**
- Every story corresponds to a state defined in the component spec's states matrix. Do not invent states.
- The `Default` story must show the most typical usage — the one a developer should reach for first.
- Use `...Default.args` spread in derived stories to avoid repeating the full args object.
- `argTypes` must include every prop the component accepts. Do not omit props because they seem "obvious."
- `description` in each `argType` must be sourced from the component spec — do not invent descriptions.
- `layout: 'centered'` is the default. Change to `layout: 'fullscreen'` only for layout-level components (page shells, navigation bars).

---

### File 3 — Prop table (markdown block for MDX or README)

The prop table is the authoritative API reference. It is included inline in the MDX page and can also stand alone in a README.

**Structure:**

```markdown
## Props

| Prop | Type | Default | Required | Description |
|---|---|---|---|---|
| `label` | `string` | — | Yes | Visible label text. Used as accessible name when no `aria-label` is provided. |
| `disabled` | `boolean` | `false` | No | When `true`, the component is non-interactive and visually muted. |
| `loading` | `boolean` | `false` | No | When `true`, shows a loading indicator and prevents repeated interaction. |
| `variant` | `'primary' \| 'secondary' \| 'ghost'` | `'primary'` | No | Visual style variant. |
| `onClick` | `() => void` | — | No | Callback fired on click, unless `disabled` or `loading` is true. |
| `aria-label` | `string` | — | No | Accessible label override. Provide when the visual label alone is insufficient. |
```

**Rules for the prop table:**
- Include every prop the component accepts, including ARIA overrides and event handlers.
- The `Type` column must use TypeScript union notation for enums.
- The `Default` column must state the actual default value, not "optional." Use `—` only when the prop has no default (i.e., undefined until provided).
- The `Description` column must be sourced from the component spec anatomy section. Do not invent descriptions.
- Never mark a prop Required unless the component will throw or render incorrectly without it.

---

## Workflow

### Step 1 — Read the component spec

Open the `ui-component-spec` output. Extract and note:
- Component name and one-sentence purpose
- Anatomy section (prop list with types and descriptions)
- States matrix (one row per state)
- Keyboard map (one row per key action)
- Accessibility requirements section
- Any explicitly stated When-to-use and When-NOT-to-use notes

Do not proceed to writing until you have the complete states matrix. A partial states matrix means partial stories — the docs will not cover the full component surface.

### Step 2 — Draft the MDX page

Write the MDX page in order: description → When-to-use → When-NOT-to-use → Canvas blocks → Prop reference → Accessibility notes → Keyboard behavior.

The When-to-use and When-NOT-to-use sections should be written fresh for a consumer audience. They should not duplicate the component spec language. Ask: "What would a developer on another team need to know to decide whether to use this component?"

### Step 3 — Build the argTypes block

For each prop in the spec's anatomy section, select the appropriate Storybook control type:

| Prop type | Storybook control |
|---|---|
| `string` | `'text'` |
| `number` | `'number'` |
| `boolean` | `'boolean'` |
| Union of string literals | `'select'` (add `options` array) |
| Color value | `'color'` |
| Object | `'object'` |
| Function / callback | Omit control (use `action` from `@storybook/addon-actions`) |

### Step 4 — Create a story per state

For each row in the component spec's states matrix, create one story. The story name should match the state name (Default, Disabled, Loading, Error, Empty, etc.). Use `...Default.args` spread and override only the props that change for that state.

### Step 5 — Populate the prop table

Build the prop table from the anatomy section of the component spec. Every prop in `argTypes` must appear in the prop table, and every row in the prop table must have a matching `argType` entry.

### Step 6 — Cross-check and confirm

Before delivering, verify:
- Every story referenced in the MDX `<Canvas of={...} />` block has a matching export in the stories file.
- Every prop in the prop table has a matching `argType` entry.
- No props were invented that do not appear in the component spec.
- Accessibility notes trace back to the component spec's accessibility section.

---

## Anti-pattern rules

1. **Do not invent props not in the component spec.** If the spec does not list a `size` prop, do not add one to the stories or prop table. If you believe a prop is missing from the spec, surface it as an open question rather than inventing it.
2. **Do not write usage guidelines that duplicate the component spec.** The spec is author-facing (how it is built). The MDX page is consumer-facing (when and how to use it). Duplication produces two sources of truth that drift apart.
3. **Do not skip the When-NOT-to-use section.** This section prevents the most common misuse. If the spec does not provide explicit anti-use-cases, derive them from the When-to-use cases: if the component is right for X, name the adjacent cases where it is wrong and name the correct alternative.
4. **Do not use `layout: 'fullscreen'` unless the component is a layout-level component.** Most components should be centered in the story canvas.
5. **Do not omit the `Default` story.** The Default story is what `<Controls />` binds to in the docs. Omitting it breaks the interactive controls panel.
6. **Do not leave `argTypes` descriptions blank.** A blank description in the Storybook controls panel tells the consumer nothing. Every prop must have a one-sentence description sourced from the spec.

---

## Acceptance criteria for this skill's output

A documentation package produced by this skill is acceptable only if every one of these is true:

- [ ] All three files are present: `ComponentName.mdx`, `ComponentName.stories.ts`, and the prop table (either inline in the MDX or as a standalone markdown block).
- [ ] Every story in the MDX `<Canvas of={...} />` blocks has a matching named export in the stories file — no Canvas block references an undefined story.
- [ ] Every state in the component spec's states matrix has exactly one story. No state is omitted; no story is invented for a state not in the spec.
- [ ] Every prop in the component spec's anatomy section appears in both `argTypes` and the prop table. No props are invented; none are omitted.
- [ ] The MDX When-to-use and When-NOT-to-use sections are written for a consumer audience — they do not copy prose from the component spec verbatim.
- [ ] The Accessibility notes section contains at least one note sourced from the component spec's accessibility requirements. It is not empty.
- [ ] The prop table `Default` column states the actual default value (or `—` for undefined); it never uses the word "optional" as a value.

If any check fails, revise before delivering.

---

## Promotion checklist

Complete every item before changing `status: draft` to `status: stable`.

### Evidence on the settings-page fixture

- [ ] Running this skill against `examples/settings-page/component-specs/profile-form.md` produces a documentation package (MDX + stories) that passes every Acceptance criteria item above.
- [ ] Every state in the profile-form component spec's state matrix has exactly one corresponding story — no state is omitted, no story is invented.
- [ ] The MDX When-to-use section is written for a consumer audience and does not copy prose from the spec verbatim.

### Evidence on the spec-recovery-create fixture

- [ ] Running this skill against the `ChannelPicker` component spec (once written, see `screen-spec.md §6`) produces a complete documentation package.
- [ ] The stories file includes at least a `Default`, `Loading`, and `Empty` story matching the component spec states.

### Regression: no invented props

- [ ] Given a component spec with exactly 3 props, the `argTypes` object contains exactly 3 entries — no convenience props are invented.
- [ ] No Canvas block in the MDX references a story that is not a named export in the stories file.

### State parity

- [ ] Running this skill on a component with an `error` state: the error story is present in both the MDX Canvas and the stories file.
- [ ] Running this skill on a component with a `loading` state: the loading story correctly renders an in-progress state (not an empty state labelled "loading").

### Skill integration

- [ ] `validate-skill.py` passes for this skill with `status: stable` (no missing sections).
- [ ] `skills.json` entry for `ui-storybook-docs` has been updated to `"status": "stable"`.
- [ ] README Skill Map table has been updated to show `stable`.
