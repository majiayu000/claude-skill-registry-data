---
name: ddd
description: Domain-Driven Design (DDD) skill for the ikigai project
---

# Domain-Driven Design (DDD)

## Ubiquitous Language

Use these domain terms consistently in code, docs, and conversation.

### Core Domain: Terminal-based AI Coding Agent

**REPL** - Read-Eval-Print Loop. The main interactive loop that reads user input, processes it, and displays results. The top-level orchestrator (`ik_repl_ctx_t`).

**Scrollback** - Immutable conversation history displayed above the separator. CRITICAL: Scrollback IS the context window - what you see is what the LLM sees (WYSIWYG). NOT just a display buffer.

**Input Buffer** - Editable multi-line user input area below the separator. Supports readline-style shortcuts and UTF-8.

**Viewport** - The visible portion of scrollback within terminal dimensions. Scrollable via Page Up/Down.

**Layer** - Independent rendering component in the layer cake architecture (scrollback layer, separator layer, input layer, spinner layer).

**Session** - A conversation instance. Created on startup or after /clear. Maps to database session record. Contains the active message array.

**Message** - Structured conversation unit with role (user/assistant/system/mark/rewind), content, timestamp, tokens, model. The fundamental unit of conversation history.

**Context Window** - The messages sent to the LLM. ALWAYS equals messages in scrollback. User controls this explicitly via /clear and message visibility.

**Mark** - Checkpoint in conversation history created by /mark command. Enables /rewind to restore context to earlier state.

**Streaming** - Progressive delivery of LLM response chunks. Displayed in real-time as they arrive via HTTP streaming.

**Provider** - LLM service (OpenAI, Anthropic, Google, X.AI). Abstracted behind unified interface using superset API approach.

**Archive** - Database storage of all messages. Permanent record, never auto-loaded into context. User searches and selectively loads.

### Memory Management Domain

**talloc Context** - Hierarchical memory arena. Parent owns children. Free parent, free entire subtree. Root context owns everything.

**Ownership** - Clear parent-child relationships. Each allocation has exactly one owner responsible for cleanup.

**Result Type** - Return value carrying OK/ERR status with optional error context. Use `CHECK()` and `TRY()` macros for propagation.

**PANIC** - Unrecoverable error (OOM, data corruption). Immediately terminates process. NOT for recoverable errors.

### Architectural Concepts

**Three-Layer Separation**:
1. **Display Layer** (scrollback) - Decorated, formatted, ephemeral. ANSI codes, colors, syntax highlighting applied at render time.
2. **Active Context** (session messages) - Structured `ik_message_t[]` array sent to LLM API.
3. **Permanent Archive** (database) - All messages ever, searchable, never auto-injected.

**Scrollback-as-Context-Window Principle** - The revolutionary insight: scrollback visibility = LLM context. User has explicit control. /clear = fresh context without data loss.

**Single-threaded Event Loop** - Sequential processing. No concurrency complexity. Terminal input → parse → mutate → render.

**Direct Terminal Control** - Raw mode ANSI escape sequences. No curses library. Single framebuffer write per frame.

**Graceful Degradation** - Never crash REPL for recoverable errors. Display errors inline. Continue accepting input.

## Core Entities

**`ik_repl_ctx_t`** - Root aggregate. Owns all subsystems (terminal, scrollback, input, session messages, marks, LLM client, database).

**`ik_message_t`** - Value object. Immutable once created. Primary entity in conversation domain.

**`ik_scrollback_t`** - Entity managing display lines. Append-only buffer with O(1) arithmetic reflow.

**`ik_input_buffer_t`** - Entity managing user input. Mutable, supports multi-line editing.

**`ik_term_ctx_t`** - Entity for terminal state (raw mode, dimensions, capabilities).

## Core Services

**Rendering Service** (`render.c`) - Builds framebuffer from layers, writes to terminal atomically.

**LLM Client Service** (`openai.c`, future: `anthropic.c`) - HTTP streaming to LLM providers. Abstracts API differences.

**Database Service** (`db.c` - future) - PostgreSQL persistence. Synchronous writes. Session and message management.

**Config Service** (`config.c`) - Loads `~/.config/ikigai/config.json`. Provides API keys, model settings.

**Command Service** (`commands.c`) - Slash command dispatch (/clear, /mark, /rewind, /help, /model, /system).

## Bounded Contexts

**Terminal UI Context** - REPL, scrollback, input, rendering, viewport, layers. Concerned with user interaction and display.

**Conversation Context** - Sessions, messages, marks, context window. Concerned with conversation structure and history.

**LLM Integration Context** - Providers, streaming, API requests, token management. Concerned with external AI services.

**Persistence Context** - Database, sessions table, messages table, full-text search. Concerned with permanent storage.

**Memory Management Context** - talloc contexts, ownership, Result types, error propagation. Cross-cutting concern.

## Key Invariants

- Scrollback messages MUST match session_messages array (same content, same order)
- Session messages array MUST equal what gets sent to LLM
- Database writes MUST succeed before updating in-memory state
- Exactly one owner per allocation (talloc parent-child)
- 90% test coverage MUST be maintained
- Never run multiple make commands simultaneously

## Anti-Patterns to Avoid

- Auto-loading messages from database into context (breaks explicit control)
- Hidden context injection (violates WYSIWYG principle)
- Using malloc/free instead of talloc (breaks hierarchical ownership)
- Recoverable errors that PANIC (PANIC is only for unrecoverable)
- Creating new files when editing existing ones works
- Over-engineering (KISS/YAGNI - build what's needed now)
