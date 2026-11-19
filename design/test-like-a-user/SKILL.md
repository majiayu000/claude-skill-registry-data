---
name: test-like-a-user
description: Hold every test to one bar, real integration tests that walk the whole user journey and prove the intended end state, with fakes only at boundaries you can't control. Use when writing, fixing, reviewing or auditing tests, or when the user says "write a test", "add tests for this", "are these tests any good", "test this properly", "audit the tests" or "review this test".
---

# Test like a user: no mocks of your own code

This standard works for web apps, services, mobile apps and desktop apps. "The project's own code" means everything in the repo you are testing: its source folders, services, stores, hooks, components, screens, navigators, parsers and registries. Find those folders first (for example `src/`, `app/`, `lib/`, `packages/*`).

## The contract

- Aim for the strongest faithful proof of product behaviour, not the fastest green test or the shortest path to an answer. Exercise the broadest user journey needed to expose real failures. Never trade coverage quality, maintainability or UI/UX confidence for speed.
- Do not bless a half-done migration, duplicated navigation, leftover compatibility clutter, or a journey that technically works but confuses people. Test the intended end state.
- Do not mock the project's own code. Keep its services, stores, hooks, components, screens, navigators, parsers and registries real.
- Prove product behaviour with an integration test: use the real router or navigation stack, reach the state through real user actions, and run the real production path. On web, assert the URL, history and deep links. On mobile, mount the real screen and navigation stack and use real gestures.
- Assert what the user can observe. Internal calls, mock calls and implementation details are not product outcomes.
- For a replacement or a change to how things are organised, assert both sides: every needed item and action can still be found through the new structure, and the old or duplicate surface is gone. Redirects and source-text assertions alone do not prove a clear user experience.
- Check changed UI by eye at the relevant wide and narrow sizes, including expanded and collapsed, loading, empty and error, keyboard and focus, and the absence of duplicate navigation. Screenshot checks add to behaviour assertions; they do not replace them. Capture only after loading and every animation have settled, then look at the actual pixels for blank or see-through content, clipping, overflow, cut-off text, unclear hierarchy and confusing layout. A saved screenshot, a DOM visibility assertion or a green test is not by itself a visual pass.
- Fake only a boundary the test environment cannot control or reproduce faithfully, such as a native device API, a model runtime, a remote server, a full disk or running out of memory. Put the fake at that boundary and keep all of the project's logic above it real.
- Do not use direct store `setState` to set up a precondition for an integration test.
- Use unit tests for pure functions and narrow contracts. They do not replace the integration test for changed product behaviour.
- When native code (for example Swift or Kotlin) owns behaviour that can be tested natively, add native tests (XCTest, JUnit or the platform's equivalent). Use a shared contract test when more than one platform builds the same capability.

## Workflow

1. State the behaviour the user can see and the failure being guarded against.
2. Define the intended end state and name the old paths or surfaces that must disappear.
3. Find the real screen, navigation path, production stack and outside boundary.
4. Reuse an existing boundary fake, or add the smallest faithful fake at that boundary.
5. Write the integration test through real actions, URLs and history where they apply, and visible assertions.
6. For a bug, run the test against the broken code and confirm it fails for the reason you expect.
7. Fix the production seam and remove the old path. Do not patch the test around a poor abstraction.
8. Run the visual check, the focused test, related suites, and the project's lint, format and type checks. Run native tests when the change crosses a native boundary.
9. Remove leaked timers, subscriptions, processes and pending promises. A suite that needs a force-exit flag to hide unfinished work is not clean.

## Review verdict

Fail the review when a test mocks the project's own code, makes up state instead of using the product, asserts only calls or source text, skips a known bug, keeps a duplicate or replaced journey, leaves out visual or navigation proof for changed UI, or passes while async work outlives teardown. Name the exact file and the real integration test that should replace it.

For the deeper method (fakes vs stubs vs mocks, observing the transition, debugging a test), see `reference/test-doctrine.md` in this skill. The companion skill `bug-trap` is the short checklist.
