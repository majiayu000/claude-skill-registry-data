---
name: chat-ui-audit
description: Audit and fix chat-based AI UI (chatbots, agents, floating chat) against production best practices from Claude, ChatGPT, and modern conversational AI interfaces. Use when building, reviewing, or improving any chat UI.
disable-model-invocation: true
---

Audit and iteratively fix chat UI against conversational AI best practices.

Target: $ARGUMENTS (component path, page route, or "all" for full chat surface audit)

## Scope

This skill covers ALL chat-based UI surfaces:
- AI Lab main chat (`/ai-lab`)
- Floating chat button + panel (site-wide)
- Full-page chat (`/chat`)
- Any future conversational AI interface

## Before Starting

1. Read the target component(s) to understand current implementation
2. Read `src/app/globals.css` for chat-specific CSS (search for `chat-bench`, `chat-response-prose`)
3. Read `src/lib/config/tenant.config.ts` for chat config (placeholder, labels, feature flags)
4. If auditing layout/frame, also read the parent layout (`PublicLayoutClient.tsx`, `SiteBar.tsx`)

## Audit Checklist

Evaluate across all 10 dimensions. Each item is pass/fail with specific code evidence.

---

### 1. LAYOUT & CONTAINER

- [ ] **Full-viewport height**: Container uses `100dvh` (with `100vh` fallback) or equivalent flex/grid strategy that fills the available viewport
- [ ] **Three-zone structure**: Header (sticky), scrollable message area (`flex: 1; overflow-y: auto`), and sticky input area — implemented via flexbox column
- [ ] **Sticky header**: Header uses `sticky top-0` with appropriate z-index (z-10+), remains visible during message scroll
- [ ] **Sticky input**: Input area uses `sticky bottom-0` or is flex-anchored to bottom, stays visible above virtual keyboard
- [ ] **Z-index discipline**: Follows a clear layering: messages (auto) < header/input (10) < scroll FAB (20) < drawers/overlays (30) < toasts (40)
- [ ] **No scroll chaining**: `overscroll-behavior: contain` on chat container prevents bounce/pull-to-refresh leaking to parent
- [ ] **No horizontal overflow**: `overflow-x: hidden` or equivalent prevents code blocks or long URLs from causing horizontal scroll
- [ ] **Safe area insets**: Input area applies `padding-bottom: env(safe-area-inset-bottom)` for notch/home-indicator devices
- [ ] **Max-width constraint**: Chat column has a max-width (640-768px) centered on desktop; full-width on mobile
- [ ] **Viewport offset alignment**: Container correctly accounts for any persistent nav bars (SiteBar height, etc.) via CSS custom properties or calc()

---

### 2. MESSAGE RENDERING

- [ ] **Alignment convention**: User messages right-aligned; assistant messages left-aligned
- [ ] **Visual differentiation**: Distinct backgrounds using semantic tokens (`bg-primary` for user, `bg-muted` for assistant) — no hardcoded colors
- [ ] **Avatar placement**: Assistant avatar left; user avatar right (or omitted). Size 32-40px, rounded-full
- [ ] **Message max-width**: Bubbles capped at `max-width: 85%` (mobile) or `max-width: min(70ch, 85%)` (desktop) for readability
- [ ] **Markdown rendering**: Assistant messages rendered through react-markdown with: bold, italic, lists, links, headings, blockquotes, tables, code
- [ ] **Code block rendering**: Fenced code blocks have syntax highlighting, horizontal scroll (`overflow-x: auto`), and a copy button
- [ ] **Inline code styling**: Monospace font, subtle background, `px-1.5 py-0.5 rounded`
- [ ] **Streaming cursor**: Blinking cursor or indicator visible at the end of streaming text
- [ ] **Message grouping**: Consecutive same-sender messages grouped with reduced spacing (4-8px within group vs 16-24px between groups)
- [ ] **Error message styling**: Failed messages show destructive accent, error icon, and retry button

---

### 3. INPUT AREA

- [ ] **Auto-expanding textarea**: Starts at 1 row, grows with content up to max-height (150-200px), then scrolls internally
- [ ] **Auto-grow implementation**: Uses scrollHeight reset technique or CSS grid trick — not fixed rows
- [ ] **Enter to send**: Plain Enter submits; Shift+Enter inserts newline
- [ ] **Submit button states**: Disabled/dimmed when empty; active when text present; shows stop icon during streaming
- [ ] **Disabled during streaming**: Input and/or send button disabled while assistant is responding; stop button shown instead
- [ ] **Placeholder text**: Contextual, tenant-configurable placeholder that disappears on focus
- [ ] **Focus management**: Auto-focus on load (desktop only); refocus after send, after drawer close, after modal dismiss
- [ ] **Minimum font size 16px**: Textarea font-size >= 16px to prevent iOS Safari auto-zoom on focus
- [ ] **Input area backdrop**: Semi-transparent backdrop blur (`backdrop-filter: blur(8px)`) so messages scrolling behind are subtly visible
- [ ] **Touch target compliance**: Send button minimum 44x44px tap target

---

### 4. RESPONSIVENESS

- [ ] **Mobile-first breakpoints**: Designed for mobile (<640px) first, enhanced for tablet (640-1024px) and desktop (>1024px)
- [ ] **Safe-area-inset handling**: Outermost container or input area uses `env(safe-area-inset-*)` padding
- [ ] **Touch-friendly targets**: All buttons, links, interactive elements are minimum 44x44px with 8px spacing between adjacent targets
- [ ] **No hover-only interactions**: Every hover interaction (tooltips, timestamp reveal, action buttons) has a tap/click equivalent
- [ ] **Sidebar behavior**: On mobile, any sidebar/drawer is off-canvas (slide-in), not permanently visible
- [ ] **Responsive typography**: Message text is readable at all breakpoints (minimum 14px mobile, 15-16px desktop)
- [ ] **Landscape mode**: Chat remains usable in landscape orientation with reduced vertical space
- [ ] **Container queries or breakpoints**: Toolbar/action buttons collapse gracefully (icons-only on mobile, icons+text on desktop)

---

### 5. SCROLL BEHAVIOR

- [ ] **Auto-scroll on new messages**: Scrolls to bottom when user sends a message and when assistant starts streaming
- [ ] **Respect manual scroll-up**: Does NOT auto-scroll when user has manually scrolled up — uses IntersectionObserver or scroll position check
- [ ] **Scroll-to-bottom FAB**: Floating button appears when scrolled up >100px; hides when at bottom; bottom-center or bottom-right positioned
- [ ] **Smooth scrolling**: Programmatic scrolls use `smooth` behavior for user-initiated, `instant` during rapid streaming
- [ ] **Initial load scroll**: Scrolls to bottom instantly (not smooth) on conversation load
- [ ] **Streaming scroll**: During streaming, incrementally scrolls to keep latest token visible (only if user was at bottom)
- [ ] **Scroll anchor**: Uses `overflow-anchor: auto` or manual anchoring to prevent content jumps when images/embeds load
- [ ] **overscroll-behavior**: Container has `overscroll-behavior: contain` to prevent pull-to-refresh interference

---

### 6. LOADING & STREAMING

- [ ] **Typing indicator**: Animated indicator (dots, shimmer, or text) appears immediately after user sends, before first token
- [ ] **Token-by-token streaming**: Tokens render as they arrive via SSE; DOM updates throttled to ~16ms
- [ ] **Partial content preservation**: If stream disconnects mid-response, received content is preserved with incomplete indicator
- [ ] **Retry on failure**: Failed messages show a retry button; clicking resends the last user message
- [ ] **Error states**: Clear, non-technical error messages for network errors, rate limits, server errors
- [ ] **Optimistic UI**: User message appears in chat immediately on send (before server acknowledgment)
- [ ] **Loading skeleton**: On initial conversation load, skeleton/shimmer placeholders shown while fetching

---

### 7. ACCESSIBILITY

- [ ] **Message log role**: Message container has `role="log"` (implies `aria-live="polite"`)
- [ ] **Status announcements**: Visually hidden `role="status"` element announces: "Sending...", "Response complete", "Error"
- [ ] **ARIA labels**: Input ("Type your message"), send button ("Send message"), stop button ("Stop generating"), scroll-to-bottom ("Scroll to latest messages")
- [ ] **Focus management**: Focus stays on textarea after send; does not jump to new message
- [ ] **Keyboard navigation**: Tab moves between header, messages, input; Escape closes modals/drawers
- [ ] **Focus indicators**: All interactive elements have visible focus outlines (2px+, contrasting color)
- [ ] **Reduced motion**: All animations wrapped in `prefers-reduced-motion` check with static fallbacks
- [ ] **Contrast compliance**: Text meets WCAG AA (4.5:1 normal, 3:1 large text) in both light and dark mode
- [ ] **Code block accessibility**: Code blocks have `aria-label` and keyboard-accessible copy button

---

### 8. VISUAL POLISH

- [ ] **Consistent spacing scale**: Uses 4px-based scale (4, 8, 12, 16, 24, 32px) — no arbitrary values
- [ ] **Message bubble padding**: Consistent internal padding (12-16px horizontal, 8-12px vertical)
- [ ] **Inter-message spacing**: 4-8px within same-sender groups; 16-24px between different-sender groups
- [ ] **Typography hierarchy**: Body 15-16px, metadata 14px, code 13-14px mono, timestamps 11-12px muted
- [ ] **Message entrance animation**: Subtle fade-in + slide-up (150-200ms, ease-out) respecting `prefers-reduced-motion`
- [ ] **Border radius consistency**: Message bubbles use consistent radius (12-16px); consider speech-bubble effect (reduced radius on sender's corner)
- [ ] **Whitespace breathing room**: 16px+ padding on left/right of message area
- [ ] **Consistent iconography**: Single icon library (Lucide); 16-20px in messages, 20-24px for buttons
- [ ] **Empty state design**: Welcoming empty state with greeting, suggested prompts, or quick-action cards
- [ ] **Max-width for readability**: Message text capped at 65-75ch on desktop

---

### 9. DARK/LIGHT MODE

- [ ] **Semantic tokens only**: Zero hardcoded hex/rgb/hsl values in chat components
- [ ] **Both modes tested**: Chat looks correct in both light and dark modes
- [ ] **Code block theme switching**: Syntax highlighting adapts to current theme
- [ ] **Scrollbar theming**: Scrollbars match the current theme
- [ ] **No flash of wrong theme**: Theme applied before first paint (server-side or blocking script)
- [ ] **Smooth theme transition**: `transition: background-color 0.2s, color 0.2s` on containers

---

### 10. MOBILE-SPECIFIC

- [ ] **Bottom-anchored input**: Input always visible, anchored above virtual keyboard
- [ ] **Virtual keyboard handling**: Uses `visualViewport` API or `interactive-widget=resizes-content` to handle keyboard appearance
- [ ] **Pull-to-refresh prevention**: `overscroll-behavior-y: contain` on chat container
- [ ] **Prevent iOS zoom on focus**: Textarea font-size >= 16px
- [ ] **Touch scroll performance**: `touch-action: pan-y` on message area; momentum scrolling enabled
- [ ] **Viewport height stability**: Uses `svh` or `dvh` appropriately; no layout jumps when browser chrome shows/hides

---

## Audit Process

1. **Read** all target files and their CSS
2. **Score** each dimension: PASS / PARTIAL / FAIL with specific line references
3. **Prioritize** fixes: HIGH (broken UX / accessibility) > MEDIUM (polish / best practice) > LOW (nice-to-have)
4. **Fix iteratively**: Address HIGH issues first, then MEDIUM, then LOW
5. **Verify** each fix doesn't break other dimensions

## Output Format

```
## Chat UI Audit: [target]

### Overall: X/10 dimensions passing

### Dimension Scores
| # | Dimension | Score | Issues |
|---|-----------|-------|--------|
| 1 | Layout & Container | PASS/PARTIAL/FAIL | count |
| ... | ... | ... | ... |

### Issues Found (by priority)

#### HIGH
1. [DIMENSION] — description — file:line
   Evidence: what's wrong
   Fix: specific code change

#### MEDIUM
...

#### LOW
...

### Passing Dimensions
- [DIMENSION] — what's working well
```

## Fix Protocol

When fixing issues:
1. Read the file before editing
2. Use semantic tokens, never hardcoded values
3. Use shadcn/ui components where applicable
4. Respect the project's CSS custom property system (`--chat-viewport-offset`, `--measure-wide`, etc.)
5. Test that fixes work across the three-zone layout (header/messages/input)
6. Preserve existing behavior while improving quality
7. Keep changes minimal and focused — fix the issue, don't refactor surroundings
