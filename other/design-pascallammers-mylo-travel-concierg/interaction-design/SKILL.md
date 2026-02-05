---
name: interaction-design
description: Create rich, responsive interactive experiences that make applications a joy to use. Use this skill when building components with user interactions, forms, data-heavy interfaces, or any feature requiring thoughtful UX patterns. Complements frontend-design with psychology-driven interaction patterns.
license: Complete terms in LICENSE.txt
---

This skill guides creation of rich interactive experiences that feel alive, responsive, and delightful. While frontend-design focuses on visual aesthetics, this skill focuses on how interfaces behave, respond, and guide users through meaningful interactions.

The user provides interaction requirements: a component needing feedback patterns, a form requiring validation, a data-heavy interface needing loading states, or any feature requiring thoughtful user experience design.

## Interaction Thinking

Before implementing, understand the interaction context:

- **User Goal**: What is the user trying to accomplish? What's their mental model?
- **Friction Points**: Where might users hesitate, make errors, or feel uncertain?
- **Feedback Needs**: What does the user need to know at each moment?
- **Recovery Paths**: How can users undo, retry, or escape from mistakes?

**CRITICAL**: Every interaction should answer three questions instantly: "What can I do?", "What just happened?", and "What's happening now?"

## Core Interaction Principles

### 1. Immediate Feedback (< 100ms)

Users need instant acknowledgment that their action registered. Silence breeds uncertainty.

**Implementation patterns:**

- **Button press**: Scale down slightly (transform: scale(0.97)), subtle color shift, or ripple effect
- **Hover states**: Cursor change, elevation shift, color transition, or subtle glow
- **Touch/click**: Haptic-style visual pulse, brief highlight, or micro-bounce
- **Form inputs**: Border color change on focus, floating labels that animate into position

```css
/* Example: Satisfying button press */
.btn {
  transition:
    transform 0.1s ease,
    box-shadow 0.1s ease;
}
.btn:active {
  transform: scale(0.97);
  box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.1);
}
```

### 2. System Status Visibility

Never leave users wondering what's happening. Make every state explicit and informative.

**Loading states (choose by duration):**

- **< 300ms**: No indicator needed (optimistic UI)
- **300ms - 2s**: Subtle spinner or pulse animation
- **2s - 10s**: Skeleton screens matching content layout
- **> 10s**: Progress bar with percentage or steps remaining

**Skeleton screen principles:**

- Mirror the actual content structure precisely
- Use subtle shimmer/pulse animation (not static gray)
- Transition smoothly to real content (no jarring pop-in)
- Include approximate shapes for images, text lines, avatars

```jsx
/* Example: Content-aware skeleton */
<div className="skeleton-card">
  <div className="skeleton-avatar pulse" />
  <div className="skeleton-lines">
    <div
      className="skeleton-line w-60 pulse"
      style={{ animationDelay: '0.1s' }}
    />
    <div
      className="skeleton-line w-80 pulse"
      style={{ animationDelay: '0.2s' }}
    />
    <div
      className="skeleton-line w-40 pulse"
      style={{ animationDelay: '0.3s' }}
    />
  </div>
</div>
```

### 3. Optimistic UI

Assume success and update immediately. Reconcile with server later.

**When to use optimistic updates:**

- Toggling favorites, likes, bookmarks
- Reordering lists
- Simple form submissions
- Adding/removing items from collections

**Implementation:**

1. Update UI immediately on user action
2. Send request to server in background
3. On success: Do nothing (UI already correct)
4. On failure: Revert UI, show non-intrusive error toast

```jsx
/* Example: Optimistic toggle */
const [isLiked, setIsLiked] = useState(false);

const handleLike = async () => {
  setIsLiked((prev) => !prev); // Optimistic update
  try {
    await api.toggleLike(itemId);
  } catch {
    setIsLiked((prev) => !prev); // Revert on failure
    toast.error("Couldn't save. Try again.");
  }
};
```

### 4. Progressive Disclosure

Reveal complexity gradually. Start simple, unlock depth as needed.

**Patterns:**

- **Staged onboarding**: One concept per screen, not feature avalanche
- **Expandable sections**: Show summary, reveal details on demand
- **Contextual tooltips**: Help appears when relevant, not all at once
- **Feature discovery**: Introduce advanced features after basics are mastered

**Implementation guidelines:**

- Default to the 80% use case; hide the 20% behind expansion
- Use clear affordances (chevrons, "Show more", expand icons)
- Remember user preferences for expanded/collapsed states
- Never hide critical actions behind progressive disclosure

### 5. Forgiving Interactions

Humans make mistakes. Great interfaces expect this and make recovery effortless.

**Undo patterns:**

- **Timed undo**: "Email sent. Undo (5s)" — delay destructive actions
- **History stack**: Cmd+Z for multi-level undo in editors
- **Soft delete**: "Moved to trash" vs permanent deletion
- **Auto-save with versions**: Never lose work, allow rollback

**Confirmation patterns:**

- Use sparingly — only for truly irreversible, high-consequence actions
- Make the consequence explicit: "Delete 47 files permanently?"
- Require deliberate action: Type confirmation text, hold button

**Recovery patterns:**

- Clear "escape hatches" — always show how to go back
- Preserve form data on navigation/error
- Auto-save drafts frequently
- "Start over" option for multi-step flows

```jsx
/* Example: Timed undo toast */
const handleDelete = (item) => {
  const toastId = toast(
    <span>
      Deleted "{item.name}"
      <button
        onClick={() => {
          restoreItem(item);
          toast.dismiss(toastId);
        }}
      >
        Undo
      </button>
    </span>,
    { duration: 5000 }
  );

  // Actually delete after toast expires
  setTimeout(() => performDelete(item.id), 5000);
};
```

### 6. Smart Form Interactions

Forms are where users feel most vulnerable. Make them feel supported, not interrogated.

**Validation timing:**

- **Never validate while typing** — wait for blur or explicit submission
- **Validate on blur** for format checks (email, phone)
- **Validate on submit** for required fields (don't punish exploration)
- **Validate in real-time** only for password strength or username availability

**Error presentation:**

- Place errors inline, adjacent to the problem field
- Use color (red border) + icon + text (never color alone)
- Be specific: "Password needs 8+ characters" not "Invalid password"
- Offer solutions: "Did you mean john@gmail.com?"

**Success feedback:**

- Subtle green checkmark on valid fields (don't overdo it)
- Progress indicators for multi-step forms
- Celebration micro-animation on successful submission

```jsx
/* Example: Inline validation with helpful errors */
<div className="field">
  <input
    type="email"
    className={error ? 'input-error' : value && isValid ? 'input-valid' : ''}
    onBlur={validateEmail}
  />
  {error && (
    <span className="error-message">
      <ErrorIcon /> {error}
      {suggestion && (
        <button onClick={applySuggestion}>Use {suggestion}?</button>
      )}
    </span>
  )}
</div>
```

### 7. Micro-interactions That Delight

Small moments of animation that make interfaces feel alive and responsive.

**High-impact micro-interactions:**

- **Success celebration**: Confetti burst, checkmark draw-on, subtle bounce
- **Pull-to-refresh**: Custom animation matching brand personality
- **Empty states**: Animated illustrations that invite action
- **Transitions**: Elements morphing between states, not jumping

**Dan Saffer's micro-interaction anatomy:**

1. **Trigger**: What initiates it (user action or system event)
2. **Rules**: What happens and in what order
3. **Feedback**: What the user sees/hears/feels
4. **Loops & Modes**: Does it repeat? Different states?

```css
/* Example: Success checkmark draw-on */
@keyframes draw-check {
  0% {
    stroke-dashoffset: 50;
  }
  100% {
    stroke-dashoffset: 0;
  }
}

.success-check {
  stroke-dasharray: 50;
  stroke-dashoffset: 50;
  animation: draw-check 0.4s ease-out forwards;
}
```

### 8. Keyboard & Accessibility

Power users love keyboard shortcuts. Assistive technology users require them.

**Keyboard essentials:**

- **Focus management**: Always visible focus ring, logical tab order
- **Modal trap**: Focus stays within modal until dismissed
- **Arrow key navigation**: Within menus, lists, tabs
- **Escape to close**: Universal dismiss pattern
- **Skip links**: "Skip to main content" for screen readers

**Shortcut implementation:**

- Use standard conventions (Cmd+S save, Cmd+Z undo)
- Don't conflict with browser/OS/screen reader shortcuts
- Provide discoverability (show in tooltips, help menu)
- Make shortcuts optional enhancements, never requirements

```jsx
/* Example: Keyboard-accessible modal */
useEffect(() => {
  const handleKeyDown = (e) => {
    if (e.key === 'Escape') onClose();
    if (e.key === 'Tab') trapFocus(e, modalRef);
  };

  document.addEventListener('keydown', handleKeyDown);
  firstFocusableElement.current?.focus(); // Move focus into modal

  return () => document.removeEventListener('keydown', handleKeyDown);
}, []);
```

### 9. Drag and Drop

Direct manipulation that feels physical and intuitive.

**Visual feedback requirements:**

- **Grab cursor**: Change cursor to grabbing hand on drag start
- **Ghost image**: Semi-transparent preview following cursor
- **Origin placeholder**: Show where item came from (dashed outline)
- **Drop zone highlighting**: Clear indication of valid targets
- **Snap animation**: Items settle into place with subtle ease-out

**Accessibility companion:**

- Always provide keyboard alternative (select, arrow keys, Enter to move)
- Announce drag state to screen readers
- Button-based "Move to..." option as fallback

```css
/* Example: Polished drag states */
.draggable {
  cursor: grab;
}
.draggable:active {
  cursor: grabbing;
}

.dragging {
  opacity: 0.8;
  transform: scale(1.02) rotate(2deg);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  z-index: 1000;
}

.drop-zone.active {
  background: var(--accent-light);
  border: 2px dashed var(--accent);
}
```

### 10. Animation Timing & Easing

Motion should feel natural, not mechanical or sluggish.

**Duration guidelines:**

- **Micro-feedback**: 50-100ms (button press, checkbox toggle)
- **State transitions**: 150-300ms (expand/collapse, page transitions)
- **Complex animations**: 300-500ms (modal appear, route change)
- **Decorative motion**: Variable, but respect prefers-reduced-motion

**Easing recommendations:**

- **ease-out**: For elements entering (fast start, gentle landing)
- **ease-in**: For elements leaving (gentle start, fast exit)
- **ease-in-out**: For elements morphing in place
- **spring/bounce**: For playful, physical-feeling interfaces

```css
/* Example: Respecting motion preferences */
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

## Laws of UX Quick Reference

Apply these psychology principles:

| Law                     | Principle                                  | Application                                         |
| ----------------------- | ------------------------------------------ | --------------------------------------------------- |
| **Hick's Law**          | More choices = slower decisions            | Limit options, use progressive disclosure           |
| **Fitts's Law**         | Larger + closer = easier to click          | Size important buttons, reduce travel distance      |
| **Jakob's Law**         | Users expect your site to work like others | Follow conventions unless improving on them         |
| **Miller's Law**        | ~7 items in working memory                 | Chunk information, limit visible options            |
| **Peak-End Rule**       | Remember peaks and endings                 | Nail the critical moments and final impression      |
| **Doherty Threshold**   | < 400ms keeps flow                         | Optimize response times, use perceived speed tricks |
| **Aesthetic-Usability** | Pretty = perceived as easier               | Visual polish improves perceived usability          |

## Implementation Checklist

Before shipping any interactive component:

- [ ] **Immediate feedback**: Does every action show instant acknowledgment?
- [ ] **Loading states**: Are all async operations visually indicated?
- [ ] **Error handling**: Are errors clear, specific, and recoverable?
- [ ] **Empty states**: Does blank slate invite action, not confuse?
- [ ] **Keyboard accessible**: Can all interactions be completed via keyboard?
- [ ] **Focus visible**: Is focus indicator always clear and visible?
- [ ] **Undo available**: Can destructive actions be reversed?
- [ ] **Motion respectful**: Does it honor prefers-reduced-motion?
- [ ] **Touch-friendly**: Are tap targets at least 44x44px?
- [ ] **Offline resilient**: What happens when connection fails?

## Combining with frontend-design

This skill complements **frontend-design**:

| frontend-design           | interaction-design     |
| ------------------------- | ---------------------- |
| How it looks              | How it behaves         |
| Visual aesthetics         | Behavioral patterns    |
| Typography, color, layout | Feedback, timing, flow |
| Static beauty             | Dynamic responsiveness |

Use both skills together: frontend-design for the visual direction, interaction-design for the experiential polish. The most delightful interfaces nail both — they're visually distinctive AND a joy to interact with.

Remember: Users don't separate "how it looks" from "how it feels." A beautiful interface that feels sluggish or confusing will disappoint. An ugly interface that's responsive and intuitive will frustrate differently. Excellence requires both.
