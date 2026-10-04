---
name: react-component-design
description: When building or refactoring React UI components to ensure reusability and maintainability.
version: 2.0.0
category: frontend
tags: [frontend, react, ui, components]
skill_type: workflow
author: skiLLM
license: MIT
compatible_agents: [claude-code, cursor, copilot, codex]
estimated_context_tokens: 1800
dangerous: false
requires_review: false
security_level: safe
dependencies: []
triggers: [component, jsx, tsx, ui, reusable]
permissions:
  filesystem: { read: true, write: true }
  network: { outbound: false }
  shell: { execute: false }
input_requirements: [existing React codebase, TypeScript project setup]
output_contract: [pure functional components, strict TypeScript interfaces, no prop drilling beyond 2 levels, CSS classes only]
failure_conditions: [component exceeds 200 lines, props interface not exported, side effects in render]
last_updated: 2026-05-15
---

# React Component Design

## Purpose
React components MUST be pure, composable, and reusable abstractions. This skill enforces TypeScript-first design, separation of concerns, and deterministic rendering to ensure maintainable, testable UI code that works reliably across different contexts.

## When to use
- Building a new UI element from scratch
- Refactoring a large, monolithic React component
- Extracting shared UI patterns into a component library
- Adding new features to an existing component hierarchy
- Preparing components for cross-team reuse

## When NOT to use
- Styling implementation details (use DOM Security Hardening skill instead)
- State management architecture decisions (use State Management Patterns skill)
- Performance optimization via memo/useMemo (handle at call site, not in component)

## Inputs required
- Existing React codebase with TypeScript
- Clear understanding of component's single responsibility
- Props interface definition (before implementation)

## Workflow
1. **Define the API**: Write the TypeScript interface for props BEFORE the component body. This clarifies the contract.
2. **Verify Props**: Ensure props contain ONLY what the component needs—no unnecessary inherited types.
3. **Isolate Logic**: Extract all complex state and side-effects into custom hooks (NEVER in component body).
4. **Render JSX**: Build static JSX structure based solely on props and hook return values.
5. **Apply Styles**: Use CSS classes via `className` prop. NEVER use inline `style={{...}}`.
6. **Export Type**: Export both the component AND its Props interface for consumers.
7. **Verify Size**: Confirm file does NOT exceed 150 lines. If it does, extract sub-components.

## Rules
- MUST be a pure function: identical props = identical output
- MUST export a strictly typed TypeScript interface named `[ComponentName]Props`
- MUST NOT exceed 150 lines per file (extract sub-components if larger)
- MUST NOT use inline styles (`style={{...}}`)
- MUST NOT drill props more than 2 levels deep
- MUST NOT fetch data directly (use hooks or parent component)
- MUST support `className` prop for customization

## Anti-patterns
- **Prop Drilling**: Passing props down more than 2 levels deep (use Context, composition, or compound components)
- **Inline Styles**: Using `style={{...}}` objects instead of CSS classes
- **God Components**: Handling data fetching, business logic, and UI rendering in one file
- **State in Props**: Copying prop values into local state with `useState(props.val)`
- **Implicit Dependencies**: Accessing globals or services without prop parameters
- **Class Components**: Using class components instead of functional components with hooks

## Failure conditions
- Component file exceeds 200 lines
- Props interface is not exported
- Component performs side effects without useEffect
- More than 2 levels of prop drilling detected

## Validation checklist
- [ ] Props interface is explicitly exported and named `[ComponentName]Props`
- [ ] Component is a pure function with no render-time side effects
- [ ] No inline `style={{...}}` objects anywhere
- [ ] No prop drilling beyond 2 levels
- [ ] File is ≤ 150 lines
- [ ] All complex logic is extracted to custom hooks
- [ ] Component supports `className` prop for customization
- [ ] TypeScript types are strict (no `any`)
- [ ] No direct API/data fetching in component body

## Output format
- **File count**: 1 primary `.tsx` file (+ additional files if refactored)
- **Exports**: One default export (component) + named export for Props interface
- **Structure**: Props interface → Component function → Export both
- **Styling**: CSS classes only, no inline styles
- **Size**: ≤ 150 lines per component file

## Security considerations
- Components do NOT execute arbitrary user input; text content is always escaped
- Props are never used in DOM insertion without sanitization
- Event handlers are never created from strings or user input
- No use of `dangerouslySetInnerHTML` (violates DOM Security Hardening)

## Agent execution notes
- Agent MAY: Create new components, refactor large components, add TypeScript interfaces
- Agent MUST NEVER: Add inline styles, drill props beyond 2 levels, add data fetching to component
- Agent MUST ASK: Before exceeding 150 lines, before changing prop contracts
- Agent MUST VALIDATE: All TypeScript is strict, no prop drilling, component is pure functional

## Example

**❌ Anti-pattern (Prop drilling, inline styles, state mirroring):**
```tsx
// Bad: mirrors props, inline styles, multiple responsibilities
export const Modal = ({ title, onClose, userId, userName, isOpen }) => {
  const [name, setName] = useState(userName); // ANTI-PATTERN: state from props
  
  return (
    <div style={{ position: 'fixed', top: 0 }} onClick={onClose}>
      <h1>{title}</h1>
      <input value={name} onChange={(e) => setName(e.target.value)} />
      <UserProfile userId={userId} name={name} /> {/* 2 levels */}
    </div>
  );
};

export const UserProfile = ({ userId, name }) => {
  return <UserBio userId={userId} name={name} />; {/* 3 levels: VIOLATION */}
};
```

**✅ Correct pattern (Pure, CSS classes, no drilling):**
```tsx
interface ModalProps {
  title: string;
  onClose: () => void;
  isOpen: boolean;
  children: React.ReactNode;
}

export const Modal = ({ title, onClose, isOpen, children }: ModalProps) => {
  if (!isOpen) return null;
  
  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content">
        <h1>{title}</h1>
        {children}
      </div>
    </div>
  );
};

interface UserProfileProps {
  userId: string;
}

export const UserProfile = ({ userId }: UserProfileProps) => {
  const user = useUser(userId); // Use hook, not props
  return (
    <div>
      <h2>{user?.name}</h2>
      <p>{user?.bio}</p>
    </div>
  );
};
```
