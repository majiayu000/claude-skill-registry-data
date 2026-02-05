---
name: refining-prompts
description: Refining and improving user prompts for StickerNest development. Use when the user asks to improve a prompt, make a request clearer, help phrase something better, or when they give a vague request and you want to clarify. Covers prompt engineering, StickerNest context injection, and disambiguation.
---

# Refining Prompts for StickerNest

This skill helps transform vague or broad user requests into precise, context-rich prompts that keep AI development on track.

## When to Use This Skill

1. **User explicitly asks**: "improve this prompt", "make this clearer", "help me phrase this"
2. **Vague request detected**: User gives a broad request that could go many directions
3. **Before major features**: Help scope and clarify before implementation
4. **Teaching moment**: Show user how to get better results

## The Refinement Process

### Step 1: Understand Intent
Ask yourself:
- What is the user actually trying to accomplish?
- What problem are they solving?
- What's the expected outcome?

### Step 2: Inject StickerNest Context
Add relevant context about:
- Which system this touches (widgets, spatial, canvas, etc.)
- Existing patterns to follow
- Files/components involved
- Constraints and conventions

### Step 3: Add Specificity
Transform vague terms into specific ones:
- "make it work in VR" → "ensure component renders in SpatialCanvas when spatialMode !== 'desktop'"
- "add a button" → "add a button to [specific location] that [specific action]"
- "fix the bug" → "fix [specific symptom] in [specific file] caused by [hypothesis]"

### Step 4: Include Success Criteria
What does "done" look like?
- Specific behavior expected
- Edge cases to handle
- Testing requirements

## Prompt Refinement Template

When refining a prompt, output:

```
## Refined Prompt

**Original**: [User's original request]

**Refined**:
[The improved prompt with full context]

**Why This Is Better**:
- [Reason 1]
- [Reason 2]

**Clarifying Questions** (if needed):
1. [Question about ambiguous aspect]
```

## StickerNest Context Cheatsheet

Use this to inject relevant context:

### For Widget Work
```
Context: StickerNest widgets use Protocol v3.0 for communication.
- Widgets live in iframes with WidgetAPI injected
- Manifests define ports (inputs/outputs) for pipelines
- State is managed via WidgetAPI.getState()/setState()
- Reference: src/runtime/widgets/, public/test-widgets/
```

### For Spatial/VR/AR Work
```
Context: StickerNest uses parallel rendering (DOM + WebGL).
- Desktop mode uses CanvasRenderer (DOM)
- VR/AR modes use SpatialCanvas (Three.js)
- Check spatialMode via useActiveSpatialMode()
- In XR sessions, avoid <Html> components (use pure 3D)
- Coordinates convert via spatialCoordinates.ts (100px = 1m)
- Reference: src/components/spatial/, src/state/useSpatialModeStore.ts
```

### For UI/Component Work
```
Context: StickerNest uses React + Zustand + CSS tokens.
- Components in src/components/
- Theme tokens in src/styles/tokens.css
- State in Zustand stores (src/state/)
- Follow existing patterns for panels, modals, toolbars
```

### For State Management
```
Context: StickerNest uses Zustand with persist middleware.
- Stores in src/state/
- Use selectors to minimize re-renders
- Persist only what's necessary
- Actions should be atomic and descriptive
```

## Common Refinements

### Vague → Specific Examples

| Original | Refined |
|----------|---------|
| "Add VR support" | "Ensure [Component] renders correctly in SpatialCanvas when spatialMode is 'vr'. Use useActiveSpatialMode() to detect mode and toSpatialPosition() for coordinates. Skip any <Html> components when useXR session is active." |
| "Make a widget" | "Create a new widget with manifest at public/test-widgets/[name]/manifest.json. Include typed input/output ports for pipeline connectivity. Use Protocol v3.0 patterns from existing widgets like BasicTextWidget." |
| "Fix the styling" | "Fix [specific visual issue] in [Component]. Use existing theme tokens from tokens.css. Ensure it works in both light/dark themes and respects spatialMode for VR compatibility." |
| "Improve performance" | "Profile [specific component/page] to identify render bottlenecks. Consider: memoization, virtualization for lists, lazy loading, reducing re-renders via Zustand selectors. Measure before/after." |
| "Add a panel" | "Add a new panel to [location] using the existing panel pattern from LibraryPanel/PropertiesPanel. Register in usePanelsStore for visibility toggle. Include header, close button, and content area." |

### Adding Constraints

Always add relevant constraints:
- **Don't break existing behavior**: "Ensure existing [feature] still works"
- **Follow patterns**: "Use the same pattern as [existing similar feature]"
- **Testing**: "Add tests for [critical paths]"
- **Accessibility**: "Ensure keyboard navigation and screen reader support"

## Interactive Refinement

When the user's intent is unclear, ask:

```
I want to make sure I understand your request correctly. You said:
> "[original request]"

A few clarifying questions:
1. [Specific question about scope]
2. [Question about expected behavior]
3. [Question about edge cases]

Or I can proceed with this interpretation:
> [Your best guess at refined prompt]
```

## Example Refinement Session

**User**: "make the widgets work better in VR"

**Refined Prompt**:
```
Improve widget rendering quality and interaction in VR mode:

1. **Resolution**: Ensure VR_RESOLUTION_SCALE is applied to all widget Html content
2. **Interaction**: Verify pointer events work on widget meshes for grab/resize
3. **XR Session**: Skip <Html> components when isPresenting (use 3D placeholders)
4. **Performance**: Profile widget rendering in VR, optimize if >16ms frame time

Context:
- Widgets render in SpatialWidgetContainer.tsx
- Use useXR((state) => state.session) for XR detection
- Current VR_RESOLUTION_SCALE is 2.5x
- Test on Quest 3 if available

Success criteria:
- Widgets are readable (not pixelated) in VR
- Widgets can be grabbed and moved
- No "flat screen" effect when widgets are present
- Maintains 72+ FPS on Quest 3
```

**Why This Is Better**:
- Breaks "work better" into specific improvements
- References actual files and constants
- Includes success criteria with measurable outcomes
- Provides testing guidance

## Quick Refinement Patterns

For speed, use these patterns:

**Feature Request**: "Add [feature] to [location] that [behavior]. Follow the pattern in [similar feature]. Ensure it works in [modes/contexts]."

**Bug Fix**: "Fix [symptom] in [file:line]. Likely caused by [hypothesis]. Verify fix doesn't break [related functionality]."

**Refactor**: "Refactor [component/function] to [improvement]. Keep the same external API. Add tests for [critical paths]."

**Investigation**: "Investigate [issue]. Check [likely causes]. Report findings with file paths and line numbers."
