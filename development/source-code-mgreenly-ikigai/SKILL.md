---
name: source-code
description: Source Code skill for the ikigai project
---

# Source Code

## Description

Comprehensive reference for all C source files in the Ikigai REPL project organized by functional area.

## Core Infrastructure

- `src/client.c` - Main entry point for the REPL application, loads configuration and initializes the event loop.
- `src/shared.c` - Shared context initialization for terminal, rendering, database, and history.
- `src/panic.c` - Panic handler for unrecoverable errors with safe async-signal-safe cleanup.
- `src/error.c` - Error handling wrapper using talloc-based allocator for consistent memory management.
- `src/config.c` - Configuration file loading and parsing with tilde expansion and default config creation.
- `src/credentials.c` - API key management with environment variable and JSON file (~/.ikigai/credentials.json) support.
- `src/logger.c` - Thread-safe logging system with ISO 8601 timestamps and local timezone support.
- `src/uuid.c` - UUID generation using base64url encoding for compact agent identifiers.

## Memory Management

- `src/array.c` - Generic expandable array implementation with configurable element size and growth strategy.
- `src/byte_array.c` - Typed wrapper for byte (uint8_t) arrays built on top of the generic array.
- `src/line_array.c` - Typed wrapper for line (char*) arrays built on top of the generic array.
- `src/json_allocator.c` - Talloc-based allocator for yyjson providing consistent memory management.

## Terminal Management

- `src/terminal.c` - Raw mode and alternate screen buffer management with CSI u support detection.
- `src/signal_handler.c` - Signal handling infrastructure for SIGWINCH (terminal resize) events.
- `src/ansi.c` - ANSI escape sequence parsing and color code generation utilities.

## Rendering System

- `src/render.c` - Direct ANSI terminal rendering with text and cursor positioning.
- `src/render_cursor.c` - Cursor screen position calculation accounting for UTF-8 widths and line wrapping.
- `src/layer.c` - Output buffer management for composable rendering layers.
- `src/layer_scrollback.c` - Scrollback layer wrapper that renders conversation history.
- `src/layer_input.c` - Input buffer layer wrapper that renders the current user input.
- `src/layer_separator.c` - Separator layer wrapper that renders horizontal separators with debug info and navigation context.
- `src/layer_spinner.c` - Spinner layer wrapper for animated loading indicators with frame cycling.
- `src/layer_completion.c` - Completion layer wrapper that renders tab completion suggestions.
- `src/event_render.c` - Universal event renderer that converts database events to styled scrollback content.

## Scrollback Buffer

- `src/scrollback.c` - Scrollback buffer implementation with line wrapping and layout caching.
- `src/scrollback_layout.c` - Layout calculation for scrollback lines with segment width tracking and newline handling.
- `src/scrollback_render.c` - Scrollback rendering helper functions for calculating display positions and byte offsets.
- `src/scrollback_utils.c` - Utility functions for scrollback text analysis including display width calculation with ANSI escape handling.
- `src/scroll_detector.c` - Distinguishes mouse wheel scrolling from keyboard arrow key presses using timing-based burst detection.

## Input System

- `src/input.c` - Input parser that converts raw bytes to semantic actions with UTF-8 and escape sequence handling.
- `src/input_escape.c` - Escape sequence parsing for terminal control codes with CSI sequence handling.
- `src/input_xkb.c` - XKB keyboard layout support for translating shifted keys to their base characters using reverse mapping.

## Input Buffer

- `src/input_buffer/core.c` - Input buffer text storage implementation with UTF-8 support and layout caching.
- `src/input_buffer/cursor.c` - Cursor position tracking with byte and grapheme offset management using utf8proc.
- `src/input_buffer/cursor_pp.c` - Cursor pretty-print implementation for debugging with structured output.
- `src/input_buffer/layout.c` - Input buffer layout caching for efficient display width calculation with ANSI handling.
- `src/input_buffer/multiline.c` - Multi-line navigation implementation for up/down arrow keys with line start/end detection.
- `src/input_buffer/pp.c` - Input buffer pretty-print implementation for debugging with nested structure visualization.

## REPL Core

- `src/repl.c` - REPL main event loop with select()-based multiplexing for input, HTTP, and tool execution.
- `src/repl_init.c` - REPL initialization and cleanup with session restoration support and agent tree reconstruction.
- `src/repl_viewport.c` - Viewport calculation logic for determining what's visible on screen with scroll offset tracking.
- `src/repl_callbacks.c` - HTTP callback handlers for streaming OpenAI responses with line buffering.
- `src/repl_event_handlers.c` - Event handlers for stdin, HTTP completion, tool completion, and timeouts with timeout calculation.
- `src/repl_tool.c` - Tool execution helper that runs tools in background threads with mutex-protected result passing.
- `src/repl_tool_completion.c` - Tool completion handling with tool loop continuation and provider request submission.

## REPL Actions

- `src/repl_actions.c` - Core action processing including arrow key handling through scroll detector with multiline scrollback append.
- `src/repl_actions_llm.c` - LLM and slash command handling with conversation management and command dispatching.
- `src/repl_actions_viewport.c` - Viewport and scrolling actions (page up/down, scroll up/down) with max offset calculation.
- `src/repl_actions_history.c` - History navigation actions (Ctrl+P/N for previous/next) with pending entry preservation.
- `src/repl_actions_completion.c` - Tab completion functionality for slash commands with auto-update after character insertion.

## Agent Management

- `src/agent.c` - Agent context creation and lifecycle management with layer system, conversation state, and mutex initialization.
- `src/agent_messages.c` - Agent message handling for adding messages to conversation arrays with capacity growth.
- `src/agent_provider.c` - Agent provider interface for lazy-initializing LLM providers with caching.
- `src/agent_state.c` - Agent state machine transitions between idle, waiting, and tool-executing states.
- `src/repl_agent_mgmt.c` - REPL agent array management for adding/removing agents with capacity growth.
- `src/repl_navigation.c` - Agent navigation helpers for switching between agents and finding by UUID.
- `src/repl/agent_restore.c` - Agent restoration on startup with conversation replay, mark stack reconstruction, and sorted agent tree building.
- `src/repl/agent_restore_replay.c` - Agent restoration replay helpers for populating conversation and scrollback from database.

## Commands

- `src/commands.c` - REPL command registry and dispatcher for slash commands (/clear, /help, /model, /system, /debug, etc).
- `src/commands_basic.c` - Basic command implementations (/clear, /help, /system, /debug).
- `src/commands_mark.c` - Mark and rewind command implementations for conversation checkpoints with database truncation.
- `src/commands_model.c` - Model command implementation for switching AI models with provider validation.
- `src/commands_fork.c` - Fork command handler for creating child agents with quoted prompt parsing and conversation cloning.
- `src/commands_fork_args.c` - Fork command argument parsing with quoted prompt extraction and message ID detection.
- `src/commands_fork_helpers.c` - Fork command helper functions for agent creation and conversation cloning.
- `src/commands_kill.c` - Kill command handler for terminating agents and descendants with depth-first collection and database updates.
- `src/commands_mail.c` - Mail command handlers (/send, /inbox) for inter-agent messaging with unread count tracking.
- `src/commands_mail_helpers.c` - Mail command helper functions for message formatting and delivery.
- `src/commands_agent_list.c` - /agents command implementation for displaying agent hierarchy tree with indentation and status.
- `src/marks.c` - Mark creation and management with ISO 8601 timestamps and scrollback rendering.
- `src/completion.c` - Tab completion data structures and fuzzy matching logic with model/agent argument providers.

## History

- `src/history.c` - Command history management with capacity limits and duplicate detection.
- `src/history_io.c` - History persistence to JSON file with load/save operations.

## Database Layer

- `src/db/connection.c` - PostgreSQL connection management with connection string validation and automatic migrations.
- `src/db/migration.c` - Database schema migration system with version tracking and directory scanning.
- `src/db/session.c` - Session management for creating and querying conversation sessions.
- `src/db/message.c` - Message persistence with event kind validation, parameterized queries, and conversation/metadata filtering.
- `src/db/agent.c` - Agent persistence with insert/update/list operations and status tracking.
- `src/db/agent_row.c` - Agent row parsing from PostgreSQL results with field extraction.
- `src/db/agent_zero.c` - Root agent (Agent 0) creation and lookup for ensuring root agent exists.
- `src/db/agent_replay.c` - Agent replay helpers for finding clear events and loading conversation history with mark boundaries.
- `src/db/mail.c` - Mail message persistence with insert/query/update operations for inter-agent messaging.
- `src/db/replay.c` - Replay context for loading and replaying conversation history with mark stack, message array, and rewind support.
- `src/db/pg_result.c` - PGresult wrapper with automatic cleanup using talloc destructors for RAII-style resource management.

## AI Provider System

### Provider Interface

- `src/providers/factory.c` - Provider factory for creating provider instances by name with API key lookup.
- `src/providers/provider.c` - Model capability lookup with thinking support detection and provider inference from model name.
- `src/providers/request.c` - Request builder implementation for constructing LLM requests with messages, tools, and thinking config.
- `src/providers/request_tools.c` - Standard tool definitions (glob, file_read, grep, bash, file_write) and schema generation.
- `src/providers/response.c` - Response builder for constructing LLM responses with content blocks and usage statistics.
- `src/providers/stubs.c` - Stub implementations placeholder (actual implementations in provider-specific directories).

### Common Provider Utilities

- `src/providers/common/error_utils.c` - Error category utilities for mapping HTTP status codes and determining retryability.
- `src/providers/common/http_multi.c` - Shared HTTP multi-handle client for async requests with curl integration.
- `src/providers/common/http_multi_info.c` - HTTP multi-handle info reading and completion callback dispatching.
- `src/providers/common/sse_parser.c` - Server-Sent Events parser for streaming HTTP responses with event extraction.

### Anthropic Provider

- `src/providers/anthropic/anthropic.c` - Anthropic provider implementation with vtable for async HTTP operations.
- `src/providers/anthropic/error.c` - Anthropic error handling with HTTP status mapping and error response parsing.
- `src/providers/anthropic/request.c` - Anthropic request serialization to Messages API format with thinking config.
- `src/providers/anthropic/request_serialize.c` - Anthropic request serialization helpers for content blocks and tool_use format.
- `src/providers/anthropic/response.c` - Anthropic response parsing with finish reason mapping.
- `src/providers/anthropic/response_helpers.c` - Anthropic response parsing helper functions.
- `src/providers/anthropic/streaming.c` - Anthropic streaming implementation with SSE parsing and context management.
- `src/providers/anthropic/streaming_events.c` - Anthropic SSE event processors for message_start, content_block, and message_delta.
- `src/providers/anthropic/thinking.c` - Anthropic thinking budget implementation with model-specific limits.

### OpenAI Provider

- `src/providers/openai/openai.c` - OpenAI provider implementation with vtable for async HTTP operations.
- `src/providers/openai/error.c` - OpenAI error handling with HTTP status mapping and content filter detection.
- `src/providers/openai/openai_handlers.c` - OpenAI HTTP completion handlers for non-streaming and streaming requests.
- `src/providers/openai/reasoning.c` - OpenAI reasoning effort implementation for o-series models.
- `src/providers/openai/request_chat.c` - OpenAI Chat Completions request serialization with strict mode and reasoning_effort.
- `src/providers/openai/request_responses.c` - OpenAI Responses API request serialization.
- `src/providers/openai/response_chat.c` - OpenAI Chat Completions response parsing with tool call extraction.
- `src/providers/openai/response_responses.c` - OpenAI Responses API response parsing with reasoning tokens.
- `src/providers/openai/serialize.c` - OpenAI JSON serialization for messages with role and content handling.
- `src/providers/openai/streaming_chat.c` - OpenAI Chat Completions streaming implementation with context creation.
- `src/providers/openai/streaming_chat_delta.c` - OpenAI Chat Completions delta processing for streaming events.
- `src/providers/openai/streaming_responses.c` - OpenAI Responses API streaming implementation.
- `src/providers/openai/streaming_responses_events.c` - OpenAI Responses API event processing.

### Google Provider

- `src/providers/google/google.c` - Google Gemini provider implementation with vtable for async HTTP operations.
- `src/providers/google/error.c` - Google error handling with HTTP status mapping and error response parsing.
- `src/providers/google/request.c` - Google request serialization to Gemini contents/parts format.
- `src/providers/google/request_helpers.c` - Google request serialization helpers for content blocks and role mapping.
- `src/providers/google/response.c` - Google response parsing with content parts extraction.
- `src/providers/google/response_error.c` - Google error response parsing with category mapping.
- `src/providers/google/response_utils.c` - Google response utilities including tool ID generation and finish reason mapping.
- `src/providers/google/streaming.c` - Google streaming implementation with response builder.
- `src/providers/google/streaming_helpers.c` - Google streaming helper functions for tool call handling and error mapping.
- `src/providers/google/thinking.c` - Google thinking implementation with model series detection and budget/level handling.

## Tool System

- `src/tool.c` - Tool call data structures and JSON schema generation for OpenAI function definitions with parameter helpers.
- `src/tool_dispatcher.c` - Tool dispatcher that routes tool calls to appropriate handlers with JSON validation and error envelope building.
- `src/tool_arg_parser.c` - Tool argument parsing utilities for extracting string/boolean/integer parameters from JSON.
- `src/tool_response.c` - Tool response building helpers for success/error envelopes with custom data callbacks.
- `src/tool_bash.c` - Bash command execution tool using popen with output capture and exit code extraction.
- `src/tool_file_read.c` - File reading tool with error handling for missing/inaccessible files and size limits.
- `src/tool_file_write.c` - File writing tool with error handling for permission/space issues and byte counting.
- `src/tool_glob.c` - File pattern matching tool using glob() with JSON result formatting and count tracking.
- `src/tool_grep.c` - Pattern search tool using regex with file filtering, line matching, and result formatting.

## Utilities

- `src/format.c` - Format buffer implementation for building strings with printf-style formatting and JSON appending.
- `src/pp_helpers.c` - Pretty-print helpers for debugging data structures with indentation and type formatting.
- `src/fzy_wrapper.c` - Wrapper for fzy fuzzy matching library used in tab completion with scoring and prefix matching.
- `src/debug_pipe.c` - Debug output pipe system for capturing tool output in separate channels with non-blocking reads.
- `src/msg.c` - Canonical message format utilities for distinguishing conversation kinds from metadata events.
- `src/message.c` - Message creation utilities for building ik_message_t structures with text, tool calls, and tool results.
- `src/file_utils.c` - File I/O utilities for reading entire files with error handling and size limits.

## Mail System

- `src/mail/msg.c` - Mail message structure creation with timestamp generation and field initialization.

## Wrapper Functions

- `src/wrapper_curl.c` - libcurl function wrappers with mockable link seams for testing.
- `src/wrapper_internal.c` - Internal ikigai function wrappers for database, scrollback, and provider operations.
- `src/wrapper_json.c` - yyjson wrapper implementations for JSON parsing and generation.
- `src/wrapper_posix.c` - POSIX system call wrappers for file operations and terminal control.
- `src/wrapper_postgres.c` - PostgreSQL function wrappers for database queries and result handling.
- `src/wrapper_pthread.c` - pthread wrapper implementations for mutex and thread operations.
- `src/wrapper_stdlib.c` - C standard library wrappers for formatting and time functions.
- `src/wrapper_talloc.c` - talloc wrapper implementations for memory allocation and string operations.

## Vendor Libraries

- `src/vendor/yyjson/yyjson.c` - High-performance JSON library for parsing and generation (vendored).
- `src/vendor/fzy/match.c` - Fuzzy string matching algorithm from the fzy project with bonus scoring (vendored).
