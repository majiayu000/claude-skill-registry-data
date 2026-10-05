---
name: mobile-design-executor
type: executor
description: "Execute mobile design implementations from mobile-design-planner specs."
version: 0.1.0
---

# Mobile Design Executor Skill

## When to Use

**Primary triggers:**
- "generate this mobile screen", "build this mobile flow", "implement this mobile design"
- "execute this mobile design plan", "generate React Native from this spec"
- User has a mobile-design-planner spec and wants React Native/Expo code
- User describes a mobile screen and wants production-ready components

---

## Do Not Use When

- You need to **design** a mobile interface — use `mobile-design-planner` first
- You need to **review** a mobile implementation — use `mobile-design-critic`
- You need a **web page** — use `web-design-executor`
- You need a **dashboard** — use `dashboard-executor`

---

## Resolution Paths

| Situation | Route |
|-----------|-------|
| Have a mobile-design-planner spec, need code | This skill |
| Need to design the interface first | Use `mobile-design-planner`, then come back |
| Have an implementation, need review | Use `mobile-design-critic` |
| Need a web page | Use `web-design-executor` |
| Have Stitch screens for mobile | Use stitch-kit's `stitch-react-native-components` |

---

## What You Get

- **React Native/Expo functional components** with hooks and TypeScript
- **Platform-specific navigation** (React Navigation stack/tab/drawer)
- **Gesture handlers** (swipe, long-press, pull-to-refresh via react-native-gesture-handler)
- **Safe area handling** (notch, home indicator, status bar via SafeAreaProvider)
- **Keyboard avoidance** (KeyboardAvoidingView with platform-specific behavior)
- **All interaction states** implemented: loading, empty, error, offline, disabled
- **Accessibility** roles, labels, and hints for VoiceOver/TalkBack
- **Design tokens** mapped to StyleSheet with platform-appropriate values
- **Dynamic type** support (Accessibility font scaling)

---

## MCP Baseline

None required — code generation skill.

---

## Shared Research Reference

Apply the shared research-backed workflow while executing:
`design-skills/shared-design-core/.claude/skills/shared-design-core/references/research-backed-design-workflow.md`

## Research-Backed Execution Preflight

Before generating mobile code:
- Read the mobile-design-planner spec when present, including `Reference Inventory`, `Design Memory Notes`, `State Matrix`, platform decisions, and `Source/Provenance Notes`.
- Read DESIGN.md and DESIGN_MEMORY.md when present. Preserve token names, semantic roles, visual rationale, navigation decisions, and rejected directions unless the user requests a change.
- If the input came directly from the user, create a compact reference inventory, platform convention matrix, and state matrix before generating code.
- For assistant or agent mobile surfaces, implement visible status, generated UI regions, tool invocation affordances, user confirmation points, cancellation/retry, error recovery, and trust boundaries.
- Translate public references into local design principles only. Do not copy public reference screenshots, branded assets, prompt bodies, or screen structures.
- Use local verification by default: mobile viewport/device checks, dynamic type, safe areas, keyboard avoidance, focus/reader labels, offline/error/loading states, and touch target measurement. Do not use Anthropic API for benchmark execution unless explicitly overridden by the user.

---

## Execution Protocol

### Phase 1 — Input Validation & Parameter Extraction

1a. Detect Input Mode:

| Mode | Detection | Behavior |
|------|-----------|----------|
| **Planner spec** | Input contains: Navigation Model, Screen Inventory, Gesture Model, Platform Target, State Coverage | Parse and extract all parameters |
| **Direct request** | User describes a mobile screen or flow | For simple screens (≤3): proceed with sensible defaults. For complex flows: recommend `mobile-design-planner` first |

1b. Extract Parameters (Planner Spec Mode):
- **Platform target:** iOS / Android / cross-platform (Expo)
- **Navigation model:** Stack, Tab, Drawer, or hybrid
- **Screen inventory:** List of screens with responsibilities
- **Gesture model:** Per-screen gesture requirements
- **State coverage:** Loading, empty, error, offline states per screen
- **Design tokens:** Colors, typography, spacing from planner spec
- **Reference/provenance:** Project-local sources, user references, research-only references, and missing evidence
- **Design memory:** Prior decisions to preserve and new decisions to propose

1c. Validate Completeness:
- Missing platform target → default to Expo (cross-platform), state the documented default in `## Parameter Extraction`, and treat it as the explicit platform target for the rest of execution.
- Missing navigation library → default to React Navigation v6
- No screen list → STOP
- No state coverage → STOP

### Phase 2 — Environment & Dependency Check

2a. Verify project context:
- Check for existing React Native/Expo project structure
- Detect navigation library (React Navigation, expo-router)
- Detect state management (Zustand, Redux, React Query)

2b. Determine output location:
- Default: `~/.agent/artifacts/YYYY-MM-DD-<screen-name>/`

### Phase 3 — Mobile Screen Generation

3a. Navigation Scaffold:
- Generate navigator configuration per planner spec
- Stack for linear flows, Tab for primary sections, Drawer for secondary
- Type-safe route params

3b. Screen Components:
For each screen in the inventory:
- Functional component with TypeScript
- SafeAreaView wrapper
- KeyboardAvoidingView (Platform.OS-aware behavior)
- ScrollView or FlatList as appropriate
- StyleSheet with design tokens
- All specified interaction states

3c. Gesture & Interaction:
- Swipe handlers via react-native-gesture-handler
- Pull-to-refresh on list screens
- Long-press actions where specified
- Haptic feedback (expo-haptics) for confirmations
- Platform-specific back behavior (Android hardware back)

### Phase 4 — Quality Self-Check

4a. Platform Conventions Audit:
- iOS: Large titles, system fonts, bottom tab bar, swipe-back navigation
- Android: Material top bar, FAB placement, system back button
- Cross-platform: Consistent behavior with platform-appropriate UI

4b. Accessibility Verification:
- `accessibilityLabel` on all interactive elements
- `accessibilityRole` matching element purpose
- `accessibilityState` for toggles, checkboxes, disabled states
- Dynamic type: text scales with system font size setting
- Minimum touch target: 44x44pt

4c. State Coverage:
- Loading: skeleton or spinner
- Empty: illustration + action CTA
- Error: message + retry action
- Offline: cached data indicator + retry when connected

4d. Deviation Log:
| # | Spec Requirement | What Was Generated | Reason |

4e. Design Memory Notes:
- Proposed DESIGN_MEMORY.md entry for durable navigation, gesture, visual, token, state, or platform decisions introduced by execution.

4f. Confidence Rating: HIGH / MEDIUM / LOW

### Phase 5 — Output & Critic Handoff

5a. Write component files.
5b. Execution Summary:
- Input, screens generated, navigation type, platform, confidence, deviations

5c. Critic Handoff:
```
Ready for review? Run:
/mobile-design-critic [path-to-components]
```

---

## Hard Gates

- No generation without explicit platform target (RN/Expo/SwiftUI)
- No generation without SafeAreaView handling
- No generation without accessibility roles on interactive elements
- No generation without state coverage (loading/empty/error/offline)
- No generation without keyboard avoidance
- No generation without measurable touch targets (≥44pt)
- No delivery without local mobile/device verification results or an explicit limitation statement
- No generation without Reference Inventory, Source/Provenance Notes, and Design Memory Notes
- No agentic mobile interface without visible status, generated UI region, user control/recovery, and trust boundary affordances
- No public reference copying

---

## Required Output Contract

Use these top-level headings exactly:
- `## Parameter Extraction`
- `## Reference Inventory`
- `## Generated Files`
- `## Implementation Preview`
- `## Verification Notes`
- `## Design Memory Notes`
- `## Deviation Log`
- `## Execution Summary`
