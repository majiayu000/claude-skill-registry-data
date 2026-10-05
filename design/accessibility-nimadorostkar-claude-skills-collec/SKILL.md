---
name: accessibility
description: Use when auditing or building accessible interfaces. Covers WCAG 2.2 AA conformance, semantic HTML, keyboard navigation, screen-reader behavior, focus management, and contrast.
metadata:
  category: frontend
  version: 1.0.0
  tags: [accessibility, a11y, wcag, aria, keyboard]
---

# Accessibility

## Purpose

Make interfaces usable without a mouse, without sight, and without perfect colour perception — and be able to prove it against WCAG 2.2 AA rather than assert it.

## When to Use

- Auditing a page or component for accessibility.
- Building an interactive component: modal, menu, combobox, tabs.
- Before a release with a legal or contractual accessibility requirement.
- Fixing findings from an automated scan (which catch roughly a third of real issues).

## Capabilities

- WCAG 2.2 AA audit against the actual success criteria.
- Semantic HTML and correct ARIA (including when to use none).
- Keyboard navigation, focus order, and focus trapping.
- Screen-reader testing and announcement design.
- Colour contrast and non-colour signalling.

## Inputs

- The page, component, or flow.
- The conformance target (usually WCAG 2.2 AA).
- The assistive technologies in scope.

## Outputs

- Findings mapped to specific WCAG success criteria, with severity.
- The fix for each, at the code level.
- A keyboard and screen-reader walkthrough of the corrected flow.

## Workflow

1. **Use the keyboard first** — Tab through the entire flow. Can you reach every control? Can you see where you are? Can you escape every trap? This single test finds most serious defects.
2. **Check the semantics** — Headings in order, landmarks present, lists as lists, buttons as `<button>`. A `<div onclick>` is invisible to a screen reader and unreachable by keyboard.
3. **Run the automated scan** — axe or Lighthouse. It catches contrast, missing labels, and ARIA misuse. It will not catch a wrong reading order or a meaningless label.
4. **Test with a screen reader** — VoiceOver on macOS, NVDA on Windows. Listen to the flow: does the announcement make sense without the visual context?
5. **Verify contrast** — 4.5:1 for body text, 3:1 for large text and for UI component boundaries. Do not rely on the design tool's claim; measure the rendered result.
6. **Fix and re-verify** — Each fix is re-tested by keyboard and screen reader, not just by the scanner.

## Best Practices

- The first rule of ARIA is not to use ARIA. A native `<button>`, `<select>`, or `<dialog>` is accessible for free; a re-implementation with `role="button"` is a maintenance liability that will drift.
- Never remove the focus outline without providing a visible replacement. `outline: none` with nothing after it is a WCAG 2.4.7 failure.
- `aria-label` overrides the visible text for screen-reader users. If they differ, a voice-control user saying the visible label cannot activate the control (WCAG 2.5.3).
- Colour alone must never carry meaning. A red border on an invalid field needs an icon or text as well.
- Focus must move into a modal when it opens, be trapped while it is open, and return to the trigger when it closes. Almost no hand-rolled modal does all three.
- Announce dynamic changes with a live region. A form that submits and updates silently leaves screen-reader users with no feedback.

## Examples

**Accessible modal: focus management and semantics:**

```tsx
function Modal({ open, onClose, title, children }: ModalProps) {
  const dialogRef = useRef<HTMLDialogElement>(null);

  useEffect(() => {
    const dialog = dialogRef.current;
    if (!dialog) return;
    if (open) dialog.showModal();      // native focus trap + inert background + Esc handling
    else dialog.close();
  }, [open]);

  return (
    <dialog
      ref={dialogRef}
      aria-labelledby="modal-title"
      onClose={onClose}
      onClick={(e) => { if (e.target === dialogRef.current) onClose(); }}
    >
      <h2 id="modal-title">{title}</h2>
      {children}
      <button onClick={onClose}>Close</button>
    </dialog>
  );
}
```

The native `<dialog>` element with `showModal()` provides the focus trap, background inertness, `Esc` to close, and focus restoration — all of which a `<div role="dialog">` requires you to implement and maintain by hand.

**Error state that does not rely on colour, and is announced:**

```html
<div>
  <label for="email">Email address</label>
  <input id="email" type="email" aria-invalid="true" aria-describedby="email-error" />
  <p id="email-error" role="alert">
    <svg aria-hidden="true" ...></svg>
    Enter an email address in the format name@example.com
  </p>
</div>
```

## Notes

- Automated tools detect roughly 30-40% of WCAG issues. A clean axe report is a starting point, not a conformance claim.
- WCAG 2.2 added target size (2.5.8, 24×24 CSS pixels minimum) and focus appearance criteria. Interfaces that passed 2.1 may fail 2.2 on small icon buttons.
- Skip links must be the first focusable element and must become visible on focus. A skip link that stays hidden when focused helps nobody.
