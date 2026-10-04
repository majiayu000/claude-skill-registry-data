---
name: test-design
description: "(Optional, high-risk flow) Design test cases and write the test-design artifact that /sdd:test-impl consumes. Runs inside an active pipeline after /sdd:implement."
allowed-tools: Bash(find src:*), Bash(cat src/*), Bash(git rev-parse:*), Bash(git diff:*), Bash(cat .specwork/_state/*), Bash(mkdir:*), Bash(python3:*), Read, Write
---

# Test Design — Optional

Optional step in the **high-risk** flow. Runs inside an active pipeline, after `/sdd:implement` has produced changes. It analyzes the diff and writes a design artifact that `/sdd:test-impl` reads.

Being optional, it can be skipped: from here you may go straight to `/sdd:commit`. But if you intend to run `/sdd:test-impl`, you must run this first — `/sdd:test-impl` refuses without the artifact.

---

## When to Use

- After `/sdd:implement`, within an active pipeline
- To identify test gaps (integration, E2E, edge cases)
- Before `/sdd:test-impl` (which depends on the artifact this writes)

## Usage

```bash
/sdd:test-design              # analyze the pipeline branch for test gaps
/sdd:test-design PROJ-1234   # explicit ticket ID
```

**Requires**: an active pipeline (`.specwork/`) with implementation changes.
**Writes**: `.specwork/_test/<slug>-test-design.md` — the designed cases go under its "Designed test cases" heading; `/sdd:test-impl` reads this file.

---

## Hard Rules — Required Coverage

Every design output **must** include at least one integration-level scenario for each primary unit of behavior in the diff:

- **Java**: one `@SpringBootTest` / `@WebMvcTest` / `@DataJpaTest` scenario per REST endpoint, SQS listener, or scheduled job touched by the diff. If the diff only changes internal service logic with no endpoint, design one integration test that exercises the service through its public collaborators (controller, listener, or a real `@DataJpaTest` against the repository).
- **Frontend**: one component-level scenario (RTL + MSW, full component tree) per modified page, route, or top-level component. If only hooks/utilities changed, design at least one component test that drives the hook/utility through a real component.

If the diff has no plausible integration entry point (pure library code, isolated helper), state this explicitly under *Missing Coverage* with the reason — do not silently omit the integration section.

The integration scenario is non-negotiable. A design output that lists only unit tests for a touched endpoint or listener is a defect — re-run the analysis after explicitly looking for the integration entry point.

---

**Next step**: `/sdd:test-impl` to implement the test files, or skip straight to `/sdd:commit` (`/sdd:test-impl` is optional).
