---
name: odui-apply
description: Apply an existing Open Design UI component in OpenMotion Studio. Use when wiring a shared control into a Studio feature, replacing a native button or range input, or reviewing whether a call site reuses the component library.
---

# Apply an Open Design UI component

Read the repository [instructions](../../../AGENTS.md), the [component registry](../../../packages/open-design-ui/registry.json), and the [component guide](../../../packages/open-design-ui/README.md) before editing. The registry is the source for each component alias, implementation, example and consumer.

1. Inspect the target call site and record its behavior, accessible name, layout and visual states.
2. Use the registry import alias, such as `open-design-ui/button` or `open-design-ui/slider`. Keep product state and handlers in the feature and preserve layout classes that remain necessary.
3. Preserve native button `type`, handler, disabled behavior and label. For Slider, preserve its accessible label, range, step and controlled value. Use `onPreview` for temporary feedback and `onCommit` for persisted values when that matches the feature.
4. If the change removes a native JSX button or range input tracked by `scripts/studio-native-controls.json`, lower only the matching count for that file and remove a zero-count entry.
5. Run `npm run design:check` and the affected Studio checks. Exercise the real consumer with keyboard input and both themes when the change affects interaction or appearance.

Report the component and call site changed, the behavior exercised and any verification still pending.
