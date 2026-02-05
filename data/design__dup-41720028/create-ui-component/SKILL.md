---
name: Create UI Component
description: Use this skill when creating a new React UI component. It provides a consistent Lumina-style template.
---

# Create UI Component

Use this skill to create new React components that match the current **Lumina** look (clean, light, slate/sky tones).

## When to use

- The user asks to create a new component/view/modal/panel.
- You are introducing a new interaction surface in the UI.

## Guidelines

1. **Styling**: use Tailwind classes matching the current Lumina look (light backgrounds, slate text, subtle borders/shadows).
2. **No new stylesheets**: avoid adding `.css` / CSS modules unless unavoidable.
3. **Prefer existing primitives**: check `src/lumina/components/common/` before introducing new UI patterns.
4. **Icons**: use `lucide-react`.
5. **Extensibility**: accept `className` + standard HTML props where reasonable.

## Steps

1. Start from `template.tsx` in this folder.
2. Place the component under the appropriate folder (`src/components/...`, `src/lumina/...`, or feature folder).
3. Keep responsibilities separated (UI vs logic hook vs service calls).
4. Validate interaction states if it’s interactive (hover/focus/disabled/loading/error).

