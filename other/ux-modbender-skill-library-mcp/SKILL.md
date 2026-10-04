---
name: UX
description: Design and analyze user experiences that are intuitive, efficient, and aligned with user mental models.
metadata: {"clawdbot":{"emoji":"🧠","os":["linux","darwin","win32"]}}
---

## Flow Analysis

- Map every step to complete key tasks—identify unnecessary steps
- Each step is a potential dropout—minimize count and friction
- Question every required field—if not essential now, defer or remove
- Identify points requiring user memory—provide recognition instead

## Mental Model Alignment

- Use vocabulary users would expect—not internal/technical terms
- Match familiar patterns before inventing—innovation has learning cost
- Consistent metaphors throughout—don't mix paradigms in same product
- Align with platform conventions—users bring expectations from other apps

## Friction Reduction

- Smart defaults reduce decisions—good default better than more options
- Pre-fill from available context—location, previous selections, account data
- Auto-save progress—never lose user work
- Don't ask for information already available—or not yet needed

## Progressive Disclosure

- Show only what's needed for current task—hide advanced options until relevant
- Reveal complexity gradually—basic path first, power features discoverable
- Empty states guide to first action—not just "Nothing here"
- Teach by doing, not explaining—inline hints over tutorials

## Feedback Design

- Every action gets acknowledgment—visual, haptic, or audible
- Progress indication for waits over 1 second
- Error messages: what happened + what to do next
- Success confirmation for significant actions

## Error Prevention

- Design to prevent errors—constraints, confirmations, smart defaults
- Confirmation dialogs only for destructive/irreversible actions
- Undo available for reversible actions—reduces fear of exploring
- Inline validation catches errors before submission

## Cognitive Load

- One primary action per screen—clear visual hierarchy
- Group related information—chunking aids comprehension
- Limit simultaneous choices—too many options cause paralysis
- Consistent patterns across product—learned once, applied everywhere

## Edge Cases to Design

- Empty state: first time, cleared, filtered with no results
- Loading state: skeleton preferred over spinner for known layouts
- Error state: what went wrong, how to recover
- Partial state: some data available, some loading/failed
- Offline state: what works, what's queued, what's unavailable

## Reversibility

- Trash over permanent delete—recovery possible
- Preview before commit—show effect of action
- Draft states for complex work—don't require completion in one session
- Settings and decisions easy to change—not buried or locked

## Task Completion

- Define what success looks like for each flow
- First value delivered quickly—quick win before complex setup
- Clear next step always visible—no dead ends
- Completion feels complete—confirmation, celebration for big tasks

## Accessibility Integration

- Keyboard/switch navigation works for all flows
- Screen reader announces what's needed—labels, states, updates
- Sufficient contrast without relying on color alone
- Respects user preferences—motion, text size, dark mode

## Copy and Labels

- Button labels describe outcome—"Save Changes" not "Submit"
- Headings scannable—user finds what they need quickly
- Error text actionable—not just "Invalid input"
- Microcopy reduces uncertainty—helper text where questions arise

## Consistency Checks

- Same words for same concepts—create glossary if needed
- Same interaction patterns—swipe/tap/long-press mean same things
- Visual similarity reflects functional similarity
- Exceptions rare and justified
