---
name: implement-builtin
description: Implements new TCL builtin commands or subcommands in feather. Use when adding new TCL commands like lrepeat, or new subcommands to existing commands like namespace.
---

# Implement Builtin Skill

Step-by-step process for implementing new TCL builtin commands or subcommands in feather.

## Working Process

### 1. Review Last Commit

Before starting any work:

```bash
git show HEAD
```

Understand the current state and any handoff notes from your colleague.

### 2. Understand Command Behavior

Use the view-manual skill to get the TCL specification:

```bash
man -P cat n <command>
```

### 3. Verify Oracle Behavior

Test expected behavior against the reference TCL interpreter:

```bash
echo '<tcl code>' | bin/oracle
```

Build the oracle if needed: `mise build:oracle`

Test all cases:
- Basic usage with various inputs
- Edge cases (empty strings, special characters)
- Error cases (wrong # args, invalid inputs)

### 4. Create Test Suite

Create `testcases/<command>.html` with test cases verified against oracle.

Use the correct test case structure:

```html
<test-case name="descriptive name">
  <script>tcl code here</script>
  <return>TCL_OK</return>
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

### 5. Verify Test Suite Against Oracle

```bash
bin/harness run --host bin/oracle testcases/<command>.html
```

All tests must pass against the oracle before implementation.

### 6. Implement the Command

#### For New Commands

1. Create `src/builtin_<command>.c` with the implementation
2. Add declaration to `src/internal.h`
3. Register command in `src/interp.c` command table
4. Add include to `interp/feather_amalgamation.c`

#### For New Subcommands

1. Add static function in existing `src/builtin_<command>.c`
2. Add dispatch case in the main command handler
3. Update error message listing valid subcommands

### 7. Build and Test

```bash
# Force rebuild to pick up C changes
go build -a -o bin/feather-tester ./cmd/feather-tester

# Run new tests
bin/harness run --host bin/feather-tester testcases/<command>.html

# Run full regression (Go host)
mise test

# Run JS/WASM host tests
mise test:js
```

### 8. Update Existing Tests If Needed

If you changed error messages (e.g., added subcommands to the "must be..." list), update affected test files.

### 9. Commit

Use the commit skill to create a comprehensive handoff message documenting:
- What was implemented
- Architecture decisions
- Current state
- Next steps for colleague

## Key Files

| File | Purpose |
|------|---------|
| `src/builtin_*.c` | Builtin command implementations |
| `src/internal.h` | Internal declarations |
| `src/interp.c` | Command registration table |
| `interp/feather_amalgamation.c` | Amalgamated C source for CGO |
| `testcases/*.html` | Test definitions |
| `bin/oracle` | Reference TCL interpreter |

## Common Patterns

### Argument Count Check

```c
if (ops->list.length(interp, args) != 1) {
  FeatherObj msg = ops->string.intern(interp, 
    "wrong # args: should be \"command arg\"", 37);
  ops->interp.set_result(interp, msg);
  return TCL_ERROR;
}
```

### String Operations

```c
FeatherObj str = ops->list.at(interp, args, 0);
size_t len;
const char *s = ops->string.get(interp, str, &len);
```

### Return Result

```c
ops->interp.set_result(interp, result);
return TCL_OK;
```

### Subcommand Dispatch

```c
if (feather_str_eq(subcmd_str, subcmd_len, "subcommand")) {
  return ns_subcommand(ops, interp, args);
}
```
