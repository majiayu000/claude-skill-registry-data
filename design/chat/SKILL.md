---
name: chat
description: "Skill for the Chat area of paddock. 62 symbols across 10 files."
---

# Chat

62 symbols | 10 files | Cohesion: 76%

## When to Use

- Working with code in `src/`
- Understanding how ChatInput, autoResize, addFiles work
- Modifying chat-related functionality

## Key Files

| File | Symbols |
|------|---------|
| `src/components/chat/conversation-list.tsx` | asRecord, readString, readNumber, readSessionPrefs, readSessions (+10) |
| `src/components/chat/chat-input.tsx` | ChatInput, autoResize, addFiles, removeAttachment, handleDrop (+5) |
| `src/components/chat/session-message.tsx` | SessionMessage, PartRenderer, ThinkingPart, ToolUsePart, ToolResultPart (+5) |
| `src/components/chat/chat-workspace.tsx` | ChatWorkspace, check, ChatIndicators, AgentAvatar, getConversationStatus (+2) |
| `src/components/chat/message-list.tsx` | formatDateGroup, groupMessagesByDate, isGroupedWithPrevious, MessageList, isNearBottom (+2) |
| `src/components/chat/message-bubble.tsx` | getAgentTheme, formatTime, asRecord, renderContent, ToolCallBubble (+1) |
| `src/components/chat/session-kind-brand.tsx` | getMeta, getSessionKindLabel, SessionKindAvatar, SessionKindPill |
| `src/lib/chat-utils.ts` | detectTextDirection |
| `src/components/panels/chat-page-panel.tsx` | ChatPagePanel |
| `src/components/chat/chat-panel.tsx` | ChatPanel |

## Entry Points

Start here when exploring this area:

- **`ChatInput`** (Function) — `src/components/chat/chat-input.tsx:15`
- **`autoResize`** (Function) — `src/components/chat/chat-input.tsx:29`
- **`addFiles`** (Function) — `src/components/chat/chat-input.tsx:48`
- **`removeAttachment`** (Function) — `src/components/chat/chat-input.tsx:66`
- **`handleDrop`** (Function) — `src/components/chat/chat-input.tsx:80`

## Key Symbols

| Symbol | Type | File | Line |
|--------|------|------|------|
| `ChatInput` | Function | `src/components/chat/chat-input.tsx` | 15 |
| `autoResize` | Function | `src/components/chat/chat-input.tsx` | 29 |
| `addFiles` | Function | `src/components/chat/chat-input.tsx` | 48 |
| `removeAttachment` | Function | `src/components/chat/chat-input.tsx` | 66 |
| `handleDrop` | Function | `src/components/chat/chat-input.tsx` | 80 |
| `handlePaste` | Function | `src/components/chat/chat-input.tsx` | 88 |
| `handleKeyDown` | Function | `src/components/chat/chat-input.tsx` | 106 |
| `insertMention` | Function | `src/components/chat/chat-input.tsx` | 154 |
| `handleSend` | Function | `src/components/chat/chat-input.tsx` | 174 |
| `formatFileSize` | Function | `src/components/chat/chat-input.tsx` | 185 |
| `detectTextDirection` | Function | `src/lib/chat-utils.ts` | 3 |
| `MessageBubble` | Function | `src/components/chat/message-bubble.tsx` | 161 |
| `ChatPagePanel` | Function | `src/components/panels/chat-page-panel.tsx` | 4 |
| `ChatWorkspace` | Function | `src/components/chat/chat-workspace.tsx` | 29 |
| `check` | Function | `src/components/chat/chat-workspace.tsx` | 66 |
| `ChatPanel` | Function | `src/components/chat/chat-panel.tsx` | 5 |
| `MessageList` | Function | `src/components/chat/message-list.tsx` | 49 |
| `isNearBottom` | Function | `src/components/chat/message-list.tsx` | 56 |
| `handleScroll` | Function | `src/components/chat/message-list.tsx` | 85 |
| `handleRetry` | Function | `src/components/chat/message-list.tsx` | 97 |

## Connected Areas

| Area | Connections |
|------|-------------|
| Panels | 13 calls |
| Terminal | 2 calls |
| Ui | 1 calls |

## How to Explore

1. `gitnexus_context({name: "ChatInput"})` — see callers and callees
2. `gitnexus_query({query: "chat"})` — find related execution flows
3. Read key files listed above for implementation details
