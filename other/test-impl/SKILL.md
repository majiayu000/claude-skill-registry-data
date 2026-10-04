---
name: test-impl
description: "(Optional, high-risk flow) Implement test files from the test-design artifact. Depends on /sdd:test-design and runs inside an active pipeline."
allowed-tools: Bash(find src:*), Bash(find test:*), Bash(cat src/*), Bash(git rev-parse:*), Bash(git diff:*), Bash(cat .specwork/_state/*), Bash(cat .specwork/_test/*), Bash(mkdir:*), Bash(python3:*), Read, Write
---

# Test Implementation — Optional

Optional step in the **high-risk** flow. Implements the test files designed by `/sdd:test-design`, following its artifact. Runs inside an active pipeline.

**Depends on `/sdd:test-design`**: this step reads `.specwork/_test/<slug>-test-design.md` and refuses to run if it is missing. Run `/sdd:test-design` first. Being optional, you may also skip this step and go straight to `/sdd:commit`.

---

## When to Use

- After `/sdd:test-design` has written its artifact, within an active pipeline
- To implement the designed unit / integration / E2E tests

## Usage

```bash
/sdd:test-impl              # implement test files for the pipeline branch
/sdd:test-impl PROJ-1234   # explicit ticket ID
```

**Requires**: an active pipeline (`.specwork/`) with implementation changes, and a completed `/sdd:test-design` (its artifact at `.specwork/_test/<slug>-test-design.md`).

---

## Hard Rules — Behavior-Based Assertions

Generated tests **must verify behavior**, not just that code doesn't explode. Before writing any test method, read the implementation file you are testing and extract concrete facts:

| Facet | What to extract | Asserted with |
|---|---|---|
| Return value | Type, fields populated, derived computations (e.g. `status = OPEN` when `count >= threshold`) | `assertThat(result.getStatus()).isEqualTo(OPEN);` — concrete value |
| Persistence | `repository.save(...)` / `entityManager.persist(...)` calls — what entity, which fields are set | `verify(repository).save(argThat(c -> c.getName().equals("X")));` |
| Events / messages | `applicationEventPublisher.publishEvent(...)`, `sqsTemplate.send(...)`, `kafkaTemplate.send(...)` | `verify(publisher).publishEvent(any(ConsentCreatedEvent.class));` |
| Outbound calls | Feign client / `RestTemplate` invocations — endpoint, payload shape | `verify(feignClient).fetchUser(eq(userId));` |
| Exceptions | Specific exception class thrown for which input | `assertThatThrownBy(...).isInstanceOf(NotFoundException.class).hasMessageContaining("...");` |

### Forbidden patterns

These assertions are **defects** — they pass even when the behavior is wrong:

```java
assertThat(result).isNotNull();              // says nothing about behavior
verify(repository).save(any());              // doesn't validate WHAT was saved
assertThat(result.getItems()).isNotEmpty();  // doesn't check content
```

A non-null check is acceptable **only** as a precondition before a content assertion on the same value:

```java
assertThat(result).isNotNull();
assertThat(result.getStatus()).isEqualTo(OPEN);   // ← the real assertion
```

### Pre-authoring read

For each class whose test you are about to write:

1. Read the public methods being tested
2. Note the return type and any computed/derived values
3. List every collaborator invocation that mutates state (`save`, `publishEvent`, `send`, etc.)
4. Note the exception types thrown and the conditions

Write the test methods only after this extraction. If you cannot determine the concrete value an implementation produces (truly dynamic — e.g. depends on a UUID or `Instant.now()`), assert against the **shape** (regex match, field present, type correct), not nullity.

For frontend tests, the equivalent extraction: which props the component renders into the DOM, which callbacks it fires with what arguments, which network requests it triggers (MSW handler). Assertions target visible text, accessible roles, or recorded callback arguments — never just "the component rendered".

---

**Requires**: `/sdd:test-design` first (reads its artifact). **Next step**: `/sdd:commit`.
