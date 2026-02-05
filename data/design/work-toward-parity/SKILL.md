---
name: work-toward-parity
description: |
  Use this skill to make a the behavior of our builtins match that of TCL.
---

# Work Toward TCL Parity Skill

Step-by-step process for implementing missing TCL behaviors to achieve parity with standard TCL. Use this when a feature is partially implemented and needs additional behaviors to match TCL.

## When to Use

- A builtin exists but is missing specific behaviors
- Documentation lists features as "Not implemented"
- Tests pass but behavior differs from TCL oracle

## Working Process

### 1. Review Last Commit

Before starting any work:

```bash
git show HEAD
```

Understand the current state and any handoff notes from your colleague.

### 2. Identify Missing Behaviors

Review the documentation file for the feature:

```bash
cat docs/builtin-<feature>.md
```

Look for entries marked as "Not implemented" or features that differ from TCL.

### 3. Explore Oracle Behavior

Test expected behavior against the reference TCL interpreter interactively:

```bash
tclsh << 'EOF'
# Test code here
EOF
```

Or use the oracle wrapper:

```bash
echo '<tcl code>' | bin/oracle
```

Key areas to explore:

- Basic functionality
- Edge cases
- Error conditions and messages
- Interaction with other features (e.g., upvar, nested calls)

### 4. Create Test Cases First

Create or update `testcases/<feature>.html` with test cases for the missing behaviors.

Use the correct test case structure:

```html
<test-case name="descriptive name">
  <script>
    tcl code here
  </script>
  <return>TCL_OK</return>
  <error></error>
  <stdout>expected output</stdout>
  <stderr></stderr>
  <exit-code>0</exit-code>
</test-case>
```

For error cases:

- Set `<return>TCL_ERROR</return>`
- Set `<error>expected error message</error>`
- Set `<exit-code>1</exit-code>`
- **Omit `<stdout>` tag entirely** (do not include empty `<stdout></stdout>`)

### 5. Verify Tests Against Oracle

```bash
bin/harness run --host oracle testcases/<feature>.html
```

All tests must pass against the oracle before implementation. Fix any test expectation mismatches.

### 6. Commit Tests

Commit the tests separately before implementing:

```bash
git add testcases/<feature>.html
git commit -m "Add test cases for <feature> <specific behaviors>"
```

This ensures tests are preserved even if implementation is incomplete.

### 7. Implement the Feature

Now implement to make the tests pass. Common patterns:

#### Modifying Function Signatures

When adding return values or parameters:

1. Update `src/internal.h` declarations
2. Update implementation in `src/<file>.c`
3. Update all call sites

#### Adding Host Interface Functions

If new host operations are needed: you first MUST STOP and ASK THE USER whether the extension is appropriate.

Extending the host interface is a measure of last resort: we want to keep as much logic in the C core as possible.

First think again whether you could implement the feature _without_ extending the host interface.

If you have been granted permission to extend the host interface, follow these steps:

1. Add to `src/feather.h` in appropriate ops struct
2. Add declaration to `src/host.h`
3. Add C wrapper in `callbacks.c`
4. Add to ops initialization in `src/host.c`
5. Implement in Go (`interp_callbacks.go`)
6. Implement in JS (`js/feather.js`)

### 8. Build and Test Iteratively

```bash
# Build
mise build

# Run specific tests
bin/harness run --host bin/feather-tester testcases/<feature>.html

# When tests pass, run full regression
mise test

# Run JS/WASM tests
mise test:js
```

Fix failures one at a time. Common issues:

- Wrong argument counts in trace callbacks
- Missing cases in switch statements
- Error message format differences

### 9. Commit Implementation

```bash
git add -A
git commit -m "Implement <specific behaviors> for <feature>

<Detailed description of what was implemented>
<Key implementation decisions>

All N tests pass in both Go and JS/WASM hosts."
```

### 10. Update Documentation

Update `docs/builtin-<feature>.md`:

- Change "Not implemented" to "**Implemented**"
- Add implementation notes sections if needed
- Document any remaining limitations

Update `docs/index.md` if the feature status changed significantly.

### 11. Final Commit

```bash
git add docs/
git commit -m "Update <feature> documentation to reflect implementation"
```

## Key Files

| File                  | Purpose                                          |
| --------------------- | ------------------------------------------------ |
| `docs/builtin-*.md`   | Feature documentation with implementation status |
| `docs/index.md`       | Summary of all builtins and missing features     |
| `testcases/*.html`    | Test definitions                                 |
| `src/internal.h`      | Internal C declarations                          |
| `src/*.c`             | C implementations                                |
| `src/feather.h`       | Host interface definitions                       |
| `callbacks.c`         | C-to-Go callback wrappers                        |
| `interp_callbacks.go` | Go host implementations                          |
| `js/feather.js`       | JS/WASM host implementations                     |

## Common Patterns

### Error Propagation

Different trace types handle errors differently:

- Variable read/write: wrap as `can't read/set "varname": <error>`
- Variable unset: ignore errors
- Command traces: ignore errors, restore result
- Execution traces: propagate directly

### Nested Propagation

When behavior must propagate through nested calls:

1. Create a variable in the interpreter in the `::tcl` namespace
2. Save/restore the previous value when entering/exiting
3. Check the global in inner functions to continue the behavior

### Working Around Feather Limitations

If tests use TCL features Feather doesn't support (e.g., `lindex $list end`):

1. Verify the test passes against oracle first
2. Rewrite using supported constructs (e.g., `lindex $list [expr {$len - 1}]`)
3. Re-verify against oracle
4. Document the workaround in commit message

## Example Session Flow

1. User: "Implement enterstep/leavestep traces"
2. Explore: `tclsh` to understand behavior
3. Create: `testcases/trace-step.html` with 15 test cases
4. Verify: `bin/harness run --host oracle testcases/trace-step.html`
5. Commit: Tests only
6. Implement: Add stepped eval functions, modify proc invocation
7. Test: `bin/harness run --host bin/feather-tester testcases/trace-step.html`
8. Fix: Handle leavestep arguments, workaround `lindex end`
9. Verify: `mise test` and `mise test:js`
10. Commit: Implementation
11. Update: `docs/builtin-trace.md` and `docs/index.md`
12. Commit: Documentation
