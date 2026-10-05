---
name: v0-mastery
description: Design generation using V0 (v0.dev) via the official MCP server. Generates production React/Tailwind/Shadcn components with live preview URLs. Use for all design generation — original designs and clone workflows. Replaces Stitch for primary generation.
---

# V0 Design Generation Pipeline

## Why V0
- Generates real React/TypeScript + Tailwind + Shadcn UI components
- Returns live demo URLs (shareable previews)
- Supports iterative refinement via `sendChatMessage` on same chatId
- Output is 70-80% production-ready code for Maks
- Models: v0-1.5-sm, v0-1.5-md, v0-1.5-lg, v0-gpt-5

## MCP Tools (via mcporter)

### createChat — New design
```bash
MCPORTER_CALL_TIMEOUT=300000 mcporter call v0.createChat \
  message="YOUR PROMPT" \
  chatPrivacy="private" \
  --output json
```
Returns: chatId, files (with path + source code), demo URL, webUrl.

### sendChatMessage — Iterate on existing design
```bash
MCPORTER_CALL_TIMEOUT=300000 mcporter call v0.sendChatMessage \
  chatId="CHAT_ID" \
  message="Fix: change background to #080C18, increase card padding to 24px" \
  --output json
```

### getChat — Pull files from a chat
```bash
mcporter call v0.getChat chatId="CHAT_ID" --output json
```

### findChats — List all chats
```bash
mcporter call v0.findChats --output json
```

### getUser — Check account info
```bash
mcporter call v0.getUser --output json
```

## Generation Pipeline

### Phase 1: Craft the prompt
Include exact brand tokens, layout spec, component names, content.

Template:
```
Create a [screen type] for [product name].

Tech: React, Next.js App Router, TypeScript, Tailwind CSS, Shadcn UI, Lucide icons.

Design specs:
- Background: [hex]
- Card surface: [hex]
- Primary text: [hex]
- Accent: [hex]
- Font: [name]
- Border radius: [value]

Layout: [detailed section-by-section]
Components: [exact Shadcn components]
Content: [realistic data, not placeholder]

Requirements:
- Mobile-first responsive
- WCAG AA contrast
- 44px touch targets
- Loading + empty states
```

### Phase 2: Generate
Call `createChat` with the prompt. Save:
- chatId (for iterations)
- demo URL (for visual review)
- files (the React code)

### Phase 3: Review
- Screenshot the demo URL with Playwright
- Run the 10-point design review
- Check brand token compliance in Tailwind classes
- Check TypeScript/component quality

### Phase 4: Iterate (max 3x)
Call `sendChatMessage` with specific fixes on the same chatId.

### Phase 5: Approve + Hand Off
- Save .tsx files to `stitch-pulls/[project]/`
- Share demo URL with Nick
- Write developer handoff spec for Maks
- V0 code is 70-80% production-ready

## Key Differences from Stitch
| | Stitch | V0 |
|---|---|---|
| Output | Raw HTML/CSS | React/TypeScript + Tailwind |
| Preview | Must render locally | Live demo URL |
| Iteration | edit_screens (limited) | sendChatMessage (full chat) |
| Quality | Good structure, basic styling | Production components |
| Timeout | 180s | 300s (longer but better) |
| Components | Generic HTML | Shadcn UI + Lucide |

## Important
- Always set `MCPORTER_CALL_TIMEOUT=300000` — V0 generation takes 60-120s
- Use `chatPrivacy="private"` for client work
- V0 output uses Geist font by default — override in prompt if needed
- Stitch remains available for quick HTML prototypes via `stitch.*` tools
