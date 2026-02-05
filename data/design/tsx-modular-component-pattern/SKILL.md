---
name: tsx-modular-component-pattern
description: Guide for outputting React/TSX components by prioritizing reusable sub-components, controlling length, and declaring them as const before the main component to ensure clear structure and maintainability.
---

## Component Structure

When generating React/TSX components, follow these structural points to maintain information focus under Primacy/Recency:
1. Decompose logically related UI modules into independent sub-components, ensuring each handles a single responsibility.
2. Declare all sub-components as `const` before the main component, making dependency order clear at a glance.
3. Keep each sub-component within 30-40 lines, continue decomposing to finer granularity if needed.
4. Use semantic naming (e.g., `VideoOverlay`, `ActionButton`, `CreatorInfo`) for quick retrieval and reuse.
5. Use Props to clarify data and event flow, let main component only handle assembly and state dispatch.
6. Regularly review if sub-components can be extracted to shared directory to avoid duplicate implementations.

Reference example:
```tsx
// Sub-components defined first
const PlayOverlay = ({ isPlaying, onToggle }: PlayOverlayProps) => (
  <div className="...">...</div>
)

const ActionButtons = ({ likes, comments }: ActionButtonsProps) => (
  <div className="...">...</div>
)

// Main component uses sub-components
export function VideoFeed({ videos }: VideoFeedProps) {
  return (
    <div>
      {videos.map(v => (
        <PlayOverlay ... />
        <ActionButtons ... />
      ))}
    </div>
  )
}
```

Final confirmation: Main component handles orchestration, sub-components handle details, achieving a stable pipeline of "decompose first, then compose".
