---
name: chappie-frontend
description: CHAPPiE's React frontend. Use when modifying UI pages, components, Tailwind styling, or the chat streaming experience.
---

# CHAPPiE Frontend Development

## Stack
- **Framework**: React 18 + TypeScript
- **Build**: Vite
- **Styling**: Tailwind CSS (utility classes only, no CSS files)
- **Routing**: React Router (page-based)
- **Data**: TanStack React Query (`useQuery`, `useMutation`)
- **API**: Fetch-based SSE streaming client

## Pages (`frontend/src/pages/`)

| Page | File | Key Features |
|---|---|---|
| Chat | `chat-page.tsx` | Token streaming, message queue, thinking animation, CoT/Answer boxes |
| Settings | `settings-page.tsx` | All 40+ settings, emotion sliders, neural mapping, auto-save |
| Memories | `memories-page.tsx` | LTM search, STM buffer, session history, cleanup/wipe |
| Life | `life-page.tsx` | Homeostasis, needs, world model (refetchInterval: 3s) |
| Growth | `growth-page.tsx` | Planning, forecast, social arcs (refetchInterval: 3s) |
| Training | `training-page.tsx` | Daemon control, logs, config (refetchInterval: 5s) |
| Debug | `debug-page.tsx` | Metadata, debug entries (refetchInterval: 2s) |

## Key Patterns

### Streaming Flow
1. User sends message → `processMessage()` → SSE stream via `api.sendMessageStream()`
2. Tokens arrive as `event: token` events with `token_type: "answer"|"reasoning"`
3. First answer token → transition from "thinking" to "streaming"
4. `turn_finished` → final message with metadata (formatted_cot, formatted_answer)

### Auto-Scroll
- `autoScrollRef` tracks user position
- Scroll event listener updates it (threshold: 60px from bottom)
- New message → `autoScrollRef.current = true`
- Reasoning truncation: 3000 chars in stream, 4000 chars in final box

### Two-Box UI (CoT + Answer)
- CoT: pine-border box above answer, shows `formatted_cot` from metadata
- Answer: main message bubble, shows `formatted_answer` (preferred) or raw content
- Uses `whitespace-pre-line` for formatted text with line breaks

## Styling Conventions
- No separate CSS files — all Tailwind utilities inline
- `rounded-none` (square corners) everywhere
- Colors: `ember` (primary), `pine` (success), `night` (bg), `ink` (darkest), `mist` (text)
- `shadow-glass` for card-like elements
- `text-[10px] uppercase tracking-widest` for labels
- Missing module: `../lib/format` → `parseEmotionalText()` in `frontend/src/lib/format.ts`
