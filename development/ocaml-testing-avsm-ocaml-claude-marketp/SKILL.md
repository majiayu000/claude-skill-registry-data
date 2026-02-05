---
name: ocaml-testing
description: Testing strategies for OCaml libraries. Use when discussing tests, alcotest, eio mocks, test structure, or test-driven development in OCaml projects.
license: ISC
---

# OCaml Testing Strategies

## When to Use This Skill

Invoke this skill when:
- Setting up tests for an OCaml project
- Writing unit tests with Alcotest
- Using Eio mock infrastructure
- Discussing testing patterns and strategies

## General Testing Setup

### Basic Test Structure

Tests use Alcotest. See `templates/test_template.ml` for the basic structure.

```ocaml
let test_basic () =
  Alcotest.(check int) "same ints" 42 (21 + 21)

let suite = [
  "basic", `Quick, test_basic;
]

let () = Alcotest.run "MyLibrary" [
  "suite1", suite;
]
```

### Test Dependencies

Add to `dune-project` package stanza:

```lisp
(depends
  ; ... other deps ...
  (alcotest (and :with-test (>= 1.7.0)))
  (eio_main :with-test)  ; if using Eio
)
```

### Test dune file

```lisp
(test
 (name test_mylib)
 (libraries mylib alcotest))
```

For Eio-based libraries:

```lisp
(test
 (name test_mylib)
 (libraries mylib alcotest eio_main eio.mock))
```

## Testing Eio-Based Libraries

### Using Eio Mock Infrastructure

If your library uses Eio, **prefer using Eio's mock infrastructure** for testing. This provides:
- Deterministic tests
- No actual filesystem/network operations
- Better error injection and edge case testing
- Faster test execution

### Fetching Eio Sources for Reference

To understand mock APIs, fetch Eio sources:

```bash
mkdir -p third_party
cd third_party && opam source eio && cd ..
```

Key files to study:
- `lib_eio/mock/` - Mock implementations
- `tests/` - Example test patterns

### Mock Modules

Common mock modules:
- `Eio_mock.Backend` - Mock backend for testing
- `Eio_mock.Clock` - Deterministic clock
- `Eio_mock.Flow` - Mock flows/streams
- `Eio_mock.Net` - Mock network
- `Eio_mock.Fs` - Mock filesystem

### Example: Testing with Mocks

See `templates/test_eio_mock.ml` for a complete example.

```ocaml
let test_with_mock_clock () =
  Eio_mock.Backend.run @@ fun () ->
  let clock = Eio_mock.Clock.make () in
  (* Your test using the mock clock *)
  Eio_mock.Clock.advance clock 1.0;
  Alcotest.(check bool) "time advanced" true true

let () = Alcotest.run "MyLibrary" [
  "eio-mocks", [
    "mock clock", `Quick, test_with_mock_clock;
  ];
]
```

### Integration Tests

For tests that need real I/O (use sparingly):

```ocaml
let test_real_io () =
  Eio_main.run @@ fun env ->
  (* Use env#fs, env#clock, etc. *)
  ()
```

## Testing Strategies by Library Type

### Pure Libraries (No I/O)
- Use simple Alcotest cases
- Focus on property-based testing if appropriate
- No special infrastructure needed

### Libraries with Filesystem I/O
- Use `Eio_mock.Fs` for mocked filesystem
- Study Eio test patterns in third_party

### Libraries with Network I/O
- Use `Eio_mock.Net` for mocked networking
- Test connection failures, timeouts
- No actual network calls in unit tests

### Libraries with Time/Concurrency
- Use `Eio_mock.Clock` for deterministic time
- Advance time explicitly in tests
- Test races and timeouts reliably

## Test Organization

```
project/
├── lib/
│   └── mylib.ml
├── test/
│   ├── dune
│   ├── test_mylib.ml          # Unit tests (with mocks)
│   └── test_integration.ml    # Integration tests (if needed)
└── third_party/               # Fetched sources for reference
    └── eio.*/
```

## Best Practices

1. **Prefer mocks over real I/O** - Tests should be fast and deterministic
2. **Fetch dependency sources** - Understand mock APIs by reading source
3. **Keep integration tests minimal** - Most tests should use mocks
4. **Test edge cases** - Use mocks to inject errors and edge conditions
5. **Clean up resources** - Even in tests, clean up temp files/state

## Running Tests

```bash
# Run all tests
dune runtest

# Run tests verbosely
dune runtest --verbose

# Run specific test
dune exec -- test/test_mylib.exe
```
