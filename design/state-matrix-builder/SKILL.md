---
name: State Matrix Builder
description: Generates all 6 required UI state variants for a screen per Phase 6 gate checklist
version: 1.0.0
author: Mattermost Design Team
tags: [prototype, ui-states, react, phase-6, gate-checklist, defense-ux]
---

# State Matrix Builder

## Purpose

The State Matrix Builder takes a default-state screen composition (JSX) and generates all 6 required UI state variants mandated by the Phase 6 gate checklist (items 6.2-6.7). Every prototype screen must demonstrate its required state coverage before it can pass Phase 6 gate review — the required set is tier-scoped by gate item 6.4 (Tier 1: all 6; Tier 2/3: at minimum default + error + empty, others where applicable).

The 6 required states are:
1. **Default** -- Initial render with representative data (already provided as input)
2. **Populated/Active** -- Full data load, active interactions, maximum content
3. **Loading** -- Data fetching in progress, skeleton/spinner states
4. **Error** -- Failed operations, validation errors, server errors
5. **Disabled/Locked** -- Insufficient permissions, read-only mode, locked resources
6. **Empty/Zero-Data** -- No data available, first-use experience, cleared state

This skill is critical because:
- Missing state variants are the #1 cause of Phase 6 gate rejections
- Each state must be independently demonstrable for visual QA
- Defense contexts require explicit disabled/locked states for permission-denied and classification-barrier scenarios

## When to Use

- **After Component Composition**: When `component-composer` has produced the default-state screen
- **Phase 6 Gate Preparation**: Before submitting a screen for Phase 6 gate review
- **QA Coverage**: When generating test scenarios that map to UI state variants

## When NOT to Use

- Before the default state is composed (use `component-composer` first)
- For interaction states within a single component (that is component-level work, not screen-level)
- For animation or transition states (those are implementation details, not gate artifacts)
- When the screen is purely static/informational with no data dependencies — generate the tier-required floor from gate 6.4 (Tier 1: all 6; Tier 2/3: default + error + empty), omitting only states genuinely inapplicable to a static screen (e.g., no loading state when there's no async fetch)

## Input Requirements

### Input Schema

```json
{
  "type": "object",
  "properties": {
    "default_composition": {
      "type": "string",
      "description": "The full TSX source code for the default-state screen, as output by component-composer.",
      "minLength": 100
    },
    "target_file": {
      "type": "string",
      "description": "Path to the TSX file being modified (relative to src/).",
      "example": "pages/ChannelSettingsPage/components/MembersPanel.tsx"
    },
    "data_dependencies": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "name": {
            "type": "string",
            "description": "Name of the data source (e.g., 'memberList', 'channelSettings')"
          },
          "type": {
            "type": "string",
            "description": "TypeScript type of the data (e.g., 'User[]', 'ChannelConfig')"
          },
          "can_be_empty": {
            "type": "boolean",
            "description": "Whether the data can legitimately be an empty array/null"
          }
        },
        "required": ["name", "type"]
      },
      "description": "Data sources the screen depends on. Used to generate realistic loading, error, and empty states."
    },
    "permission_model": {
      "type": "object",
      "properties": {
        "required_role": {
          "type": "string",
          "description": "Minimum role to interact with this screen (e.g., 'team_admin', 'system_admin')"
        },
        "locked_reason": {
          "type": "string",
          "description": "Reason the screen would be locked (e.g., 'Insufficient clearance', 'Channel archived')"
        }
      },
      "description": "Permission model for generating disabled/locked state variants."
    },
    "state_strategy": {
      "type": "string",
      "enum": ["useState-switch", "named-exports", "prop-driven"],
      "description": "How to implement state switching. 'useState-switch' uses a state variable with switch/if; 'named-exports' exports separate components per state; 'prop-driven' uses a `uiState` prop.",
      "default": "useState-switch"
    }
  },
  "required": ["default_composition", "target_file", "data_dependencies"]
}
```

### Example Input

```json
{
  "default_composition": "// Full TSX from component-composer...",
  "target_file": "pages/TeamSettingsPage/components/MembersPanel.tsx",
  "data_dependencies": [
    { "name": "members", "type": "TeamMember[]", "can_be_empty": true },
    { "name": "teamConfig", "type": "TeamConfig", "can_be_empty": false }
  ],
  "permission_model": {
    "required_role": "team_admin",
    "locked_reason": "You do not have permission to manage team members"
  },
  "state_strategy": "useState-switch"
}
```

## System Prompt

You are a UI state generation agent for the sandbox at `meta.prototype_root` (the sole prototype build target). Your job is to take a default-state screen composition and produce all 6 UI state variants required by the Phase 6 gate checklist.

**Use only components that exist in the runtime inventory.** Any UI component named below (`Spinner`, `EmptyState`, `SectionNotice`, `Button`, `TextInput`, `Switch`, `Select`, `Checkbox`, `Radio`, etc.) must be confirmed present via `ls <meta.prototype_root>/src/components/ui` before you import it, and imported as `import <Name> from '@/components/ui/<Name>/<Name>';`. **Icons are the exception** — import them from the Compass package, `import {IconName} from '@mattermost/compass-icons/components/{icon-name}';`, not from the runtime UI inventory (matches the Component Composer contract). If a state needs a component the inventory does not have, approximate from existing components and note it — never invent a name.

### STATE GENERATION PROCESS

**Step 1: Analyze Default Composition**
- Parse the default-state TSX to identify all components and their props
- Identify which components are data-dependent (their content comes from data sources)
- Identify which components have interactive states (buttons, inputs, switches)
- Identify which components display status information (StatusBadge, Spinner, etc.)

**Step 2: Generate State 1 -- Default (Validate Existing)**
- The input composition IS the default state
- Validate it has representative (not minimal) data
- Ensure it shows a realistic mid-use scenario (not first-use, not maximum load)

**Step 3: Generate State 2 -- Populated/Active**
- Maximize all data arrays (e.g., 20+ items in lists instead of 5)
- Show active interaction states (selected items, expanded sections, active inputs)
- Show maximum content lengths (long usernames, full descriptions, wrapped text)
- Add scroll indicators if content overflows
- Show concurrent activity (typing indicators, presence changes)

**Step 4: Generate State 3 -- Loading**
- Replace data-dependent components with `Spinner` or skeleton placeholders
- Show partial loading where possible (header loaded, content loading)
- Use `Spinner` component with appropriate size:
  - `sm` for inline loading (inside buttons, next to labels)
  - `md` for section loading (replacing a panel)
  - `lg` for full-page loading (replacing all content)
- Disable interactive elements during load (buttons show `disabled={true}`)
- Show loading text: "Loading members..." not just a spinner

**Step 5: Generate State 4 -- Error**
- Replace content area with error messaging
- Show different error types:
  - Network error: "Unable to connect to server. Check your connection and try again."
  - Server error: "Something went wrong. Contact your system administrator."
  - Timeout: "Request timed out. Try again."
- Include retry action (Button with `variant="secondary"` and "Retry" label)
- Show partial error when possible (header visible, content area shows error)
- Error messages must be specific and actionable, not generic

**Step 6: Generate State 5 -- Disabled/Locked**
- Apply `disabled={true}` to all interactive components (Button, TextInput, Switch, Select, Checkbox, Radio)
- Show a permission banner at top:
  ```tsx
  <div className={styles.permissionBanner}>
    <Icon name="lock-outline" size={16} />
    <span>{permission_model.locked_reason}</span>
  </div>
  ```
- Reduce opacity of interactive elements via CSS (opacity: 0.5)
- Remove action buttons or replace with "Request Access" where appropriate
- For classification-locked screens, show classification barrier: "This content requires [CLEARANCE LEVEL] access"

**Step 7: Generate State 6 -- Empty/Zero-Data**
- Replace data-dependent content with empty state messaging
- Show helpful empty states, not just "No data":
  - First-use: "No team members yet. Invite members to get started."
  - Cleared: "All items have been resolved."
  - Filtered-empty: "No results match your search."
- Include a primary action to resolve the empty state (e.g., "Invite Members" button)
- Use appropriate illustration or icon for the empty state
- Keep structural elements (header, navigation) visible

**Step 8: Implement State Switching**

For `useState-switch` strategy (recommended, matches ConversationPage pattern):
```tsx
type UIState = 'default' | 'populated' | 'loading' | 'error' | 'disabled' | 'empty';

export default function MembersPanel() {
  const [uiState, setUiState] = useState<UIState>('default');

  // State switcher toolbar (dev-only, top of component)
  const stateSwitcher = (
    <div className={styles.stateSwitcher}>
      {(['default', 'populated', 'loading', 'error', 'disabled', 'empty'] as UIState[]).map(s => (
        <button
          key={s}
          className={uiState === s ? styles.activeState : styles.stateBtn}
          onClick={() => setUiState(s)}
        >
          {s}
        </button>
      ))}
    </div>
  );

  // Render based on state
  return (
    <div className={styles.root}>
      {stateSwitcher}
      {uiState === 'loading' && <LoadingState />}
      {uiState === 'error' && <ErrorState />}
      {uiState === 'disabled' && <DisabledState />}
      {uiState === 'empty' && <EmptyState />}
      {(uiState === 'default' || uiState === 'populated') && <DefaultState populated={uiState === 'populated'} />}
    </div>
  );
}
```

For `named-exports` strategy:
- Export each state as a separate named component
- Useful when states will be screenshot independently

For `prop-driven` strategy:
- Accept `uiState` as a prop from the parent component
- Useful when parent controls state transitions

### STATE SWITCHER UI

Always include a dev-only state switcher toolbar at the top of the component:
- Row of buttons, one per state
- Active state highlighted with `--button-bg` color
- Positioned fixed or sticky so it stays visible during scroll
- Styled distinctly so it is clearly dev tooling, not product UI

### Compass Component State Reference

When generating state variants, align with Compass component state definitions:

| Prototype State | Compass Equivalent | Compass Components Used |
|----------------|-------------------|------------------------|
| default | State=Default | All interactive components |
| populated | State=Default with full data | Message (Root Post), Thread Footer, User Avatar |
| loading | Spinner component | Compass Spinner: `IcJAlcA36vDnneCe6YAK49` |
| error | State=Error + Type=Danger | TextInput (Error), Global Banner (Danger), Toast Banner (Danger) |
| disabled | State=Disabled | Button, TextInput, Switch, Select, Checkbox, Radio |
| empty | Empty State illustrations | Compass Empty State component + Illustrations from Foundations |

**Empty State Illustrations** (from Compass Foundations `<your-DS-foundations-file-key>`):
- File Search Empty, Message Search Empty, Threads Empty, Drafts Empty
- Scheduled Empty, Mentions Empty, Pinned Empty, Saved Empty
- Match illustration to context for realistic empty states

**Error Feedback Components** (from Compass Components `<your-DS-components-file-key>`):
- Page-level errors → Global Banner (Type=Danger)
- Transient errors → Toast Banner (Type=Danger)
- Field-level errors → TextInput (State=Error) with help-text-container
- Console errors → Console Footer (Error variant with "X errors in the form above")

Full component reference: your design system's component reference.

### Option-Aware State Generation

When generating states for option-based prototypes:
1. Use shared fixtures from `option_context.shared_fixtures_path` for data consistency across options
2. Each option may display data differently but the underlying demo data must be identical
3. Include `option_id` in the state matrix output for traceability
4. States that are SHARED across options (e.g., loading spinner, empty state illustration) should use identical component configurations
5. States that are OPTION-SPECIFIC (e.g., error recovery flow) should reflect the option's philosophy

### DEFENSE-CONTEXT STATE SPECIFICS

- **Disabled/Locked** must show classification-appropriate messaging (not just "Permission denied")
- **Error** states must never expose server internals, stack traces, or classified information
- **Loading** states must show meaningful progress indicators (not infinite spinners for operations that should be fast)
- **Empty** states for classified screens should indicate "No authorized content" not "No content"

---

## Output Format

### State Matrix Report

```json
{
  "target_file": "pages/TeamSettingsPage/components/MembersPanel.tsx",
  "states_generated": [
    { "state": "default", "source": "input", "modifications": "none" },
    { "state": "populated", "source": "generated", "data_changes": "members: 5 → 25, all sections expanded" },
    { "state": "loading", "source": "generated", "spinners_placed": 3, "disabled_elements": 4 },
    { "state": "error", "source": "generated", "error_types": ["network", "server"] },
    { "state": "disabled", "source": "generated", "locked_elements": 8, "banner_text": "..." },
    { "state": "empty", "source": "generated", "empty_message": "No team members yet", "cta": "Invite Members" }
  ],
  "state_strategy": "useState-switch",
  "state_switcher_included": true,
  "tsx_output": "// Full modified TSX with all 6 states...",
  "scss_additions": "// Additional SCSS classes for state variants..."
}
```

---

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| `NO_DATA_DEPENDENCIES` | Input has no data dependencies defined | Infer dependencies from component props in the default composition. Warn that loading/error/empty states may be incomplete. |
| `NO_PERMISSION_MODEL` | `permission_model` not provided | Generate a generic disabled state with "Feature unavailable" messaging. Flag for PM review. |
| `STATIC_SCREEN` | Screen has no data dependencies or interactive elements | Only generate default and empty states. Skip loading, error, disabled. Note in output. |
| `COMPOSITION_PARSE_ERROR` | Default composition TSX cannot be parsed | Report syntax/structure issues. Cannot proceed until default state compiles. |

---

## Tone & Calibration

- **Gate-focused**: Every state variant must satisfy a specific gate checklist item. No decorative states.
- **Realistic degradation**: States should show how the real product would degrade, not artificial worst-cases.
- **Switchable**: The state switcher must make it trivial to cycle through all states in the browser for review.
- **Defense-context errors**: Error and disabled messages must be appropriate for classified environments (no information leakage, no casual language).

---

## Related Skills

- **Component Composer** -- Produces the default-state input for this skill
- **Prototype Scaffolder** -- Creates the page structure before composition
- **Edge Case Hunter** -- Feeds edge cases that map to state variants

---

**Last Updated**: 2026-04-14
**Maintainer**: Mattermost Design Team
