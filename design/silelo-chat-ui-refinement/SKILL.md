---
name: silelo-chat-ui-refinement
description: Refine SILELO-style AI chat interfaces from mobile or desktop reference images. Use when adjusting chat layout, mobile drawers, message bubbles, safe external links, or honest loading indicators while preserving a real server-backed chat flow and validating responsive behavior.
---

# SILELO Chat UI Refinement

## Scope and Package Boundary

Use this skill for **chat-interface refinement** after a SILELO-like application already has a working chat flow. Use `silelo-ai-studio-workflow` for the broader application workflow, `silelo-api-gateway` for provider boundaries, and `silelo-chat-acceptance` for acceptance testing. Keep those packages intact; this is a focused sibling skill, not a replacement.

## Workflow

### 1. Turn the reference into testable requirements

Inspect the reference image and the current interface before editing. Convert visible requirements into an explicit checklist: header height and controls, primary/secondary colors, drawer width and dismissal, message alignment, bubble corner direction, composer placement, typography, and mobile viewport behavior.

Preserve the actual chat mutation and pending state. Do not seed fabricated assistant messages merely to make a screenshot look complete. If the reference shows messages but the current browser state has none, verify bubble rules in code and record that exact limitation.

### 2. Preserve the chat-state contract

Keep message state, request submission, error handling, and duplicate-send protection independent from visual styling. Render the waiting state only from a real pending value such as `isPending` or `isTyping`, and remove it when the request resolves or fails.

Do not call a provider from the browser just to animate the interface. Keep service URLs and secrets server-side.

### 3. Implement responsive navigation and message layout

Use a persistent rail on wide screens only when it suits the product. At mobile breakpoints, use a fixed off-canvas drawer with all of the following: a menu trigger, an explicit close button, a scrim that closes on click, a visible focus state, and an escape route back to the chat.

Use the reference to set concrete visual tokens, rather than copying a screenshot as a background. Keep text legible against the selected palette. Use CSS transitions under 300ms and restrict motion to `opacity` and `transform` where possible.

Align user messages to the trailing edge and assistant messages to the leading edge. Differentiate them with color and bubble geometry, but do not make color the only signal. Preserve timestamps and author labels where present.

### 4. Render external links safely

Parse only `http` and `https` fragments from model output. Split plain text and link fragments rather than using `dangerouslySetInnerHTML`. Trim sentence punctuation only after parsing, validate with `new URL`, and render accepted URLs as anchors with `target="_blank"` and `rel="noopener noreferrer"`.

Keep the parser pure and cover it with unit tests: valid HTTPS, trailing punctuation, and non-HTTP text. Do not convert `javascript:`, `data:`, or bare unvalidated strings into links.

### 5. Add an honest, accessible loading indicator

Place the indicator in the assistant-message position. Use wording such as “กำลังรอคำตอบ” or “กำลังประมวลผลข้อความของคุณ”; do not claim hidden model reasoning, progress percentage, or a completed action without evidence.

Use `role="status"`, `aria-live="polite"`, and `aria-atomic="true"` so assistive technology receives a concise update. Combine a readable label with subtle dots, bars, or a halo animation. Respect `prefers-reduced-motion` by removing non-essential animation while retaining the text status.

### 6. Verify before delivery

Run the project type check, unit tests, and production build. Capture at least one desktop and one mobile screenshot after the change. Test a real non-destructive message where access is available: confirm pending state appears, send is disabled during the request, the indicator disappears on reply/error, and an `http(s)` link opens safely.

State evidence precisely: distinguish code verified, unit tested, browser verified, and live-provider verified. Record any unverified visual state or provider behavior in project notes rather than implying that it was seen.

## Delivery Checklist

- Keep old SILELO skills and application behavior intact.
- Mark related `todo.md` items only after completing the documented work.
- Save a checkpoint after reviewing the full todo list.
- Report the exact checks run and any performance warnings, such as a large optional media/ONNX bundle.
