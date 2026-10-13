---
name: integration-testing
description: >
  Expert guidance on Integration Testing in software engineering. Use this skill whenever the user
  asks about integration testing strategies, approaches (Big-Bang, Top-Down, Bottom-Up, Mixed/Sandwich),
  writing integration test cases, setting up test environments, identifying integration defects, or
  comparing integration testing with unit/system testing. Trigger this skill for questions like
  "how do I do integration testing", "what's the difference between top-down and bottom-up testing",
  "how to write integration tests for my modules", "what testing approach should I use", or any
  mention of module interaction testing, stub/driver usage, or interface verification. Also trigger
  when users discuss CI/CD pipelines and want to know where integration tests fit in.
metadata:
  author: Ronnasayd Machado - github.com/Ronnasayd
  version: "1.0.0"
---

# Integration Testing Skill

## What is Integration Testing?

Integration Testing verifies interactions and data exchange between different components or modules
of a software application. It occurs **after unit testing** and **before system testing**, focusing on:

- Correctness of interfaces between modules
- Data flow between integrated units
- Detecting defects that arise only when components are combined

## The 4 Integration Testing Approaches

### 1. Big-Bang Integration Testing

All modules are combined and tested at once after individual unit testing.

**When to use:** Very small systems with low module interdependence.

| ✅ Advantages                              | ❌ Disadvantages                                      |
| ------------------------------------------ | ----------------------------------------------------- |
| Simple, quick, minimal planning            | Hard to localize bugs (any module could be the cause) |
| Good for small/low-interdependence systems | High-risk modules not isolated                        |
|                                            | Long delays waiting for all modules                   |
|                                            | Expensive to debug                                    |

---

### 2. Bottom-Up Integration Testing

Lower-level modules are tested first, then progressively integrated with higher-level modules.
Uses **test drivers** to pass data to lower-level modules.

**When to use:** Applications built with a bottom-up design. No stubs required.

| ✅ Advantages                                      | ❌ Disadvantages                            |
| -------------------------------------------------- | ------------------------------------------- |
| No stubs needed                                    | Driver modules must be created              |
| Multiple subsystems can be tested simultaneously   | No working model until late stages          |
| Easy to create test conditions and observe results | Complexity grows with many small subsystems |

---

### 3. Top-Down Integration Testing

Testing starts from the top (high-level modules), simulating lower-level modules not yet integrated
using **stubs**. Proceeds top → bottom.

**When to use:** When early design validation and interface error detection is priority.

| ✅ Advantages                    | ❌ Disadvantages                        |
| -------------------------------- | --------------------------------------- |
| Design defects found early       | Requires many stubs                     |
| Few or no drivers needed         | Lower-level modules tested inadequately |
| Easier interface error isolation | Stub design can be complex              |
| More stable at aggregate level   | Difficult to observe test output        |

---

### 4. Mixed (Sandwich/Hybrid) Integration Testing

Combines Top-Down and Bottom-Up approaches. Tests top and bottom layers in parallel, meeting
in the middle. Uses both stubs and drivers.

**When to use:** Very large projects with several sub-projects.

| ✅ Advantages                                      | ❌ Disadvantages                                  |
| -------------------------------------------------- | ------------------------------------------------- |
| Overcomes limitations of pure top-down / bottom-up | High cost (two approaches running simultaneously) |
| Parallel testing of top and bottom layers          | Not suitable for small systems                    |
| Best for large, complex projects                   |                                                   |

---

## How to Write Integration Tests — Step-by-Step

1. **Identify components to test** — Which modules interact or depend on each other?
2. **Define test objectives** — What are you validating? (data flow, error handling, behavior on interaction?)
3. **Define test data** — Use real-world representative data scenarios
4. **Design test cases** — Specific steps and expected outcomes for each integration point
5. **Develop test scripts** — Automate where possible; document manual steps clearly
6. **Set up the test environment** — Mirror production as closely as possible
7. **Execute tests** — Focus on component interactions and interface behavior
8. **Evaluate results** — Check for errors, unexpected behaviors, and data integrity issues

---

## Choosing the Right Approach

| Scenario                                          | Recommended Approach |
| ------------------------------------------------- | -------------------- |
| Small system, fast delivery needed                | Big-Bang             |
| Bottom-up design, reusable low-level modules      | Bottom-Up            |
| Early design validation matters, risk at top      | Top-Down             |
| Large project, parallel teams, complex subsystems | Mixed/Sandwich       |

---

## Integration Testing vs Unit Testing

| Aspect             | Unit Testing                | Integration Testing                       |
| ------------------ | --------------------------- | ----------------------------------------- |
| Scope              | Single module in isolation  | Multiple combined modules                 |
| Knowledge required | Internal design (white-box) | Interface behavior (black-box)            |
| Performed by       | Developer                   | Tester                                    |
| When               | First                       | After unit testing, before system testing |
| Focus              | Module correctness          | Interaction correctness                   |

---

## Key Concepts: Stubs vs Drivers

- **Stub** — A dummy module that simulates a _lower-level_ module not yet implemented (used in Top-Down testing)
- **Driver** — A dummy module that simulates a _higher-level_ module calling the unit under test (used in Bottom-Up testing)

---

## Integration Testing in CI/CD

Integration tests typically run:

- After unit tests pass in the CI pipeline
- Before system/end-to-end tests
- On every PR or merge to main branches

**Tip:** Keep integration tests focused on interface contracts. Leave full workflow validation to system/E2E tests.

---

## Common Integration Defects to Look For

- Incorrect data formats passed between modules
- Mismatched API contracts (wrong field names, types, or missing fields)
- Error handling not propagating correctly across module boundaries
- Race conditions when modules communicate asynchronously
- Authentication/authorization tokens not forwarded correctly
- Database connection or transaction scoping issues across services
