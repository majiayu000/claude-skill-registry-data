---
name: e2e-tests
description: This skill should be used every time you create, update, or review end-to-end tests in this repository.
compatibility: opencode
---

# E2E Test Standards

## Purpose

This project uses **exclusively E2E (end-to-end) tests**. We do not write unit tests or integration tests. E2E tests verify complete user-facing workflows using real services, real data, and real API calls.

## Core Principles

1. **E2E tests only** - No unit tests, no integration tests. Every test validates a complete scenario from start to finish.
2. **No mocks** - Tests must use real services, real databases, and real API calls. Mocking defeats the purpose of E2E testing.
3. **Real-world data** - Prefer production-like data over synthetic test fixtures. Tests should reflect actual usage patterns.
4. **Context-driven** - Every test originates from Next Actions defined in a context file (see `skills/nexus/context-driven-development/SKILL.md`).

## Test Source: Context Files

5. **Tests derive from context files** - The `## E2E Test Scenarios` table in each context file defines what tests to write.
6. **One test file per scenario** - Each scenario becomes its own test file.
7. **Scenario table format** - Each scenario has a Name (snake_case, **no `test_` prefix**) and Description column. The `test_` prefix is automatically added when generating filenames and test functions. Never use `test_` in the Name column.
8. **Test folder inside crate's tests/ directory** - In a Rust workspace, tests live inside each crate:
   - `.context/nexus-tui/TUI_001-sidebar-navigation.md` → `crates/nexus-tui/tests/tui_001_sidebar_navigation/`
   - `.context/nexus-llm/RIG_001-oauth-authentication.md` → `crates/nexus-llm/tests/rig_001_oauth_authentication/`
   - Context ID uses **lowercase with underscores** in folder name (e.g., `TUI_001` → `tui_001`)
9. **Test file naming** - Each scenario file is named `test_<name>.rs` where `<name>` is from the Name column.
10. **mod.rs required** - Each context folder must have a `mod.rs` that declares all test modules.

Example context scenario table:
```markdown
## Next Actions

| Description | Test |
|-------------|------|
| User creates session and knowledge is extracted | `session_creates_knowledge` |
| Malformed session is skipped with warning logged | `malformed_session_skipped` |
| Rate-limited API request retries with backoff | `rate_limit_retry` |
```

This produces the following test structure:
```
crates/nexus-rag/tests/              # Inside the crate directory
└── rag_002_session_watcher/         # Context ID (lowercase, underscores)
    ├── mod.rs                       # Declares: mod test_session_creates_knowledge;
    ├── test_session_creates_knowledge.rs
    ├── test_malformed_session_skipped.rs
    └── test_rate_limit_retry.rs
```

Run tests with: `cargo test -p nexus-rag --test rag_002_session_watcher`

Each file contains a test function with the `test_` prefix added:
```rust
#[test]
fn test_session_creates_knowledge() {
    // Test implementation
}
```

## Naming Validation

**CRITICAL: Never use `test_` prefix in the Name column**

The `test_` prefix is automatically added to:
- Filenames: `session_creates_knowledge` → `test_session_creates_knowledge.rs`
- Test function names: `test_session_creates_knowledge()`

Using `test_` in the Name column causes double-prefix errors:
- Wrong: `test_menu_opens_view` → `test_test_menu_opens_view.rs` ❌
- Correct: `menu_opens_view` → `test_menu_opens_view.rs` ✓

The test-sync tool validates this and will report mismatches if found.

## No Mocks Policy

8. **Real services required** - Tests connect to actual services (databases, APIs, message queues).
9. **Real network calls** - HTTP requests hit real endpoints, not mock servers.
10. **Real file system** - Tests write to and read from actual files, not in-memory fakes.
11. **Real data stores** - Use actual databases with test data, not in-memory substitutes.

## User Input Exception

12. **Skip or prompt for user-required input** - When a test requires explicit user action (e.g., OAuth authentication with a third party, manual approval flows, CAPTCHA):
    - **Option A: Skip** - Mark the test as skipped with clear documentation explaining why
    - **Option B: Prompt** - Request the required input from the user at test runtime

Example skip annotation (Rust):
```rust
#[test]
#[ignore = "Requires manual OAuth login - run with --ignored when credentials available"]
fn test_third_party_oauth_flow() {
    // Test implementation
}
```

Example prompt pattern:
```rust
fn get_oauth_token() -> String {
    if let Ok(token) = std::env::var("OAUTH_TOKEN") {
        token
    } else {
        eprintln!("OAUTH_TOKEN not set. Please authenticate and provide token:");
        // Read from stdin or fail gracefully
    }
}
```

## Test Implementation Guidelines

13. **Functional program testing** - Each test validates that a functional program/scenario works correctly end-to-end.
14. **Setup real environment** - Tests may need to provision real resources (start services, create test databases, seed data).
15. **Clean up after tests** - Remove test artifacts, reset state, but preserve real service availability.
16. **Accept latency** - E2E tests are slower than unit tests. This is expected and acceptable.
17. **Retry for flakiness** - Network-dependent tests may use retries with backoff for transient failures.

## What Tests Must Verify

18. **User-observable outcomes** - Test what users see and experience, not internal implementation.
19. **Complete workflows** - From initial input to final output, including all intermediate steps.
20. **Error conditions** - Verify graceful handling of real failures (network errors, invalid data, service unavailability).
21. **Edge cases in production context** - Test edge cases using real services, not mocked edge responses.

## Public API Only

22. **No private member access** - E2E tests must only use the public API (`pub` items exported from `lib.rs`). Never access private modules, internal constants, or unexported functions.
23. **Test rendered output, not internal state** - Instead of checking internal constants like `BULLET_MARKERS`, verify the rendered output contains the expected characters (`●`, `○`, `◆`, `◇`).
24. **If a test needs private access, it's testing implementation** - Rewrite to test observable behavior, or move to unit tests inside `src/` if truly testing internal logic.

Example - Wrong (accesses private constant):
```rust
use nexus_tui::markdown::styled_line::BULLET_MARKERS; // ❌ Private module

#[test]
fn test_bullet_markers() {
    assert_eq!(BULLET_MARKERS[0], "● "); // ❌ Testing implementation
}
```

Example - Correct (tests observable output):
```rust
use nexus_tui::markdown::render_markdown_to_styled_lines;

#[test]
fn test_bullet_markers() {
    let lines = render_markdown_to_styled_lines("- Item\n");
    let rendered = lines[0].render(80);
    let text: String = rendered[0].spans.iter()
        .map(|s| s.content.to_string()).collect();
    
    assert!(text.contains("●"), "Should render with bullet marker"); // ✓ Observable
}
```

## Anti-Patterns

25. **No mocking libraries** - Do not use mockall, mockito, wiremock, or similar.
26. **No test doubles** - No fakes, stubs, spies, or dummies.
27. **No in-memory databases** - Use the same database technology as production.
28. **No HTTP record/replay** - Tests hit live endpoints every run.
29. **No isolated unit tests** - Every test must exercise the full stack.
30. **No private API access** - Tests importing private modules (e.g., `mod::internal::*`) are testing implementation, not behavior.

## Test Environment Isolation

31. **Isolate from user data** - Tests must NEVER read from or write to real user directories (`~/.config/`, `~/.local/`, etc.).
32. **Use environment variables** - Override default paths via environment variables to redirect all I/O to `/tmp/` or similar.
33. **Shared test utilities** - Use `tests/test_utils.rs` to set up isolated test environments consistently.
34. **Guard pattern** - The `setup_test_env()` function returns a guard that automatically cleans up environment variables when dropped.

### Required Environment Variables

Tests should override these paths to prevent touching real user data:

| Variable | Purpose | Test Value |
|----------|---------|------------|
| `NEXUS_CONTEXT_DIR` | Context file storage | `/tmp/nexus_test_context/` |
| `NEXUS_STATE_FILE` | TUI state persistence | `/tmp/nexus_test/state.json` |
| `NEXUS_SETTINGS_FILE` | User settings | `/tmp/nexus_test/settings.json` |
| `NEXUS_RIG_TOKEN_PATH` | OAuth tokens | `/tmp/nexus_test/tokens.json` |
| `NEXUS_RIG_SESSION_PATH` | Chat session storage | `/tmp/nexus_test/sessions` |

### Test Setup Pattern

Every E2E test that interacts with persisted state must use the shared isolation:

```rust
mod test_utils;

#[test]
fn test_something() {
    let _guard = test_utils::setup_test_env();
    
    // Test code here - all paths automatically redirected to /tmp/
    // Guard cleanup happens automatically when test ends
}
```

### What This Prevents

- Tests resetting user's OAuth tokens (requiring re-authentication)
- Tests corrupting user's TUI settings
- Tests polluting user's session history
- Tests launching browser for OAuth flow during CI

## Validation

All E2E tests run via justfile recipes:

```bash
just test-e2e           # Run all E2E tests
just test-e2e-verbose   # Run with detailed output
```
