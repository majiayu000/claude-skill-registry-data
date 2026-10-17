---
name: rust-testing
category: testing
description: Use when writing tests for Rust service code - unit tests beside the code, integration tests in tests/, tokio::test, Router::oneshot for HTTP, sqlx::test for a fresh database per test, trait fakes or mockall at ports, test-first
tech_stack: Rust
---
# Rust Testing

## Overview

Test-first, same discipline as everywhere (see tdd-workflow): write the failing test, watch it fail, minimal code to pass. This skill is the Rust mechanics for a service.

**Core principle:** the type system already rules out a lot; tests cover behaviour, invariants and the boundaries the compiler cannot see — HTTP wiring, serialization and SQL.

## Test levels

| Level | What it covers | Tools |
|-------|-----------------|-------|
| Unit | Domain types and pure functions | `#[cfg(test)] mod tests` in the same file, `#[test]` |
| Unit with fakes | Service, its port traits faked | a hand-written fake struct, or `mockall` where the repository uses it |
| HTTP | Routing, extractors, status codes, error body | the `Router` called with `tower::ServiceExt::oneshot` — no port |
| Persistence | sqlx queries and migrations | `#[sqlx::test]`: a fresh database per test with migrations applied |

Integration tests that use the crate's public API go in `tests/`.

## Unit and service tests

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn title_rejects_blank_and_overlong() {
        for bad in ["", "   ", &"x".repeat(201)] {
            assert!(TaskTitle::try_from(bad.to_string()).is_err(), "{bad:?} should be rejected");
        }
        assert!(TaskTitle::try_from("x".repeat(200)).is_ok());
    }

    #[tokio::test]
    async fn create_stores_the_task() {
        let repo = FakeTaskRepo::default();
        let service = TaskService::new(repo.clone());
        let task = service.create(UserId::new(1), TaskTitle::try_from("Report".into()).unwrap()).await.unwrap();
        assert_eq!(repo.stored(), vec![task]);
    }
}
```

`unwrap()` is fine in tests: a panic is a failure with a line number.

## HTTP without a port

```rust
#[tokio::test]
async fn blank_title_is_400_in_the_problem_shape() {
    let app = router(test_state());
    let res = app
        .oneshot(Request::post("/tasks").header("content-type", "application/json")
            .header("authorization", test_token(1)).body(Body::from(r#"{"title":""}"#)).unwrap())
        .await
        .unwrap();
    assert_eq!(res.status(), StatusCode::BAD_REQUEST);
    let body: serde_json::Value = serde_json::from_slice(&res.into_body().collect().await.unwrap().to_bytes()).unwrap();
    assert!(body["errors"]["title"].is_string());
}
```

## Rules

- **Fakes at trait boundaries.** A hand-written fake (a struct with an `Arc<Mutex<Vec<_>>>`) is often clearer than a mock; `mockall`'s `#[automock]` where the repository already uses it. Never fake the type under test.
- Boundary tables as a loop over cases with a message per case, or `rstest`'s `#[case]` where the repository uses it.
- **`#[sqlx::test]`** for anything that runs SQL: each test gets its own database with the migrations applied, so tests run in parallel without sharing rows. It needs `DATABASE_URL` pointing at a server it may create databases on (a container in CI and locally).
- **Time:** inject a clock trait, or use `tokio::time::pause()` + `advance()` in `#[tokio::test(start_paused = true)]` for timers; never a real sleep.
- Property tests (`proptest`) for parsers and invariants with large input spaces, where the repository has them.
- Focused run while iterating: `cargo test title_rejects` or `cargo test -p <crate> --test <file>`; the full `cargo test` (all features the CI uses) plus `cargo clippy --all-targets -- -D warnings` before you stop. Coverage with `cargo llvm-cov`; mutation testing, where the repository runs it, is `cargo mutants`.

## Common Mistakes

- Testing only the happy path because the types "already guarantee" the rest.
- A test that shares a database between cases and depends on run order.
- `#[ignore]` on a failing test instead of fixing it.
- Asserting on `Debug` output strings rather than values.

## Red Flags

- The test compiles and passes before the production code exists.
- A unit test that needs a running database or network.
- `std::thread::sleep` in a test to wait for a task.
