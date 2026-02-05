---
name: build-automation
description: Build coordination wrapper for VCV Rack modules using Makefile
allowed-tools:
  - Bash
  - Read
  - Task # For troubleshooter agent on failures
preconditions:
  - Module must exist
  - RACK_DIR must be set
---

# build-automation Skill

**Purpose:** Orchestrates VCV Rack module builds using Makefile-based build system with comprehensive failure handling.

## Integration Points

This skill is invoked by:

- **module-workflow**: After each stage completion (Stages 2-6) to build and verify changes
- **module-improve**: After implementation changes to rebuild with modifications
- **module-lifecycle**: During installation verification to ensure modules are buildable

This skill invokes:

- **Makefile**: VCV Rack's standard Makefile-based build system
- **troubleshooter agent**: Deep research agent (via Task tool) when user chooses "Investigate" option

## Build Workflow

When invoked, the build-automation skill follows this workflow:

### 1. Input Validation

- Verify module name provided
- Check module directory exists: `test -d "modules/$MODULE_NAME"`
- Validate Makefile present: `test -f "modules/$MODULE_NAME/Makefile"`
- Validate RACK_DIR environment variable is set

### 2. Determine Build Target

Context-aware target selection:

- **Stage 2 (Foundation)**: Always use clean build to verify compilation (`make clean && make`)
- **Stages 3-6 (Implementation Stages)**: Full build with dist target (`make dist`)
- **module-improve**: Full build with dist target (`make dist`)
- **User manual invocation**: Ask if they want specific target (clean, all, dist, install)

### 3. Validate RACK_DIR

```bash
# Check RACK_DIR is set
if [[ -z "$RACK_DIR" ]]; then
  echo "⚠️ RACK_DIR environment variable not set"
  echo ""
  echo "RACK_DIR must point to your VCV Rack SDK directory."
  echo ""
  echo "What would you like to do?"
  echo "1. Run /setup to configure environment"
  echo "2. Set RACK_DIR manually"
  echo "3. Exit"
  echo ""
  read -p "Choose (1-3): " choice

  case "$choice" in
    1)
      # Invoke system-setup skill
      exit 2  # Signal to orchestrator to run /setup
      ;;
    2)
      echo "Enter RACK_DIR path:"
      read -p "> " RACK_DIR_PATH
      export RACK_DIR="$RACK_DIR_PATH"
      ;;
    3)
      exit 1
      ;;
  esac
fi

# Verify RACK_DIR exists and contains SDK
if [[ ! -f "$RACK_DIR/include/rack.hpp" ]]; then
  echo "⚠️ RACK_DIR doesn't contain VCV Rack SDK"
  echo "Expected: $RACK_DIR/include/rack.hpp"
  echo ""
  echo "Run /setup to configure environment"
  exit 1
fi
```

### 4. Platform Detection

```bash
# Determine platform for build target
PLATFORM=$(uname -s)
ARCH=$(uname -m)

case "$PLATFORM" in
  Darwin)
    if [[ "$ARCH" == "arm64" ]]; then
      RACK_PLATFORM="mac-arm64"
    else
      RACK_PLATFORM="mac-x64"
    fi
    ;;
  Linux)
    RACK_PLATFORM="linux-x64"
    ;;
  MINGW*|MSYS*|CYGWIN*)
    RACK_PLATFORM="win-x64"
    ;;
  *)
    echo "Unknown platform: $PLATFORM"
    exit 1
    ;;
esac

echo "Building for platform: $RACK_PLATFORM"
```

### 5. Invoke Make

Execute build with appropriate target:

```bash
cd "modules/$MODULE_NAME"

# Create logs directory
mkdir -p "../../logs/$MODULE_NAME"
LOG_FILE="../../logs/$MODULE_NAME/build_$(date +%Y%m%d_%H%M%S).log"

# Run make with logging
make $BUILD_TARGET 2>&1 | tee "$LOG_FILE"
BUILD_EXIT_CODE=${PIPESTATUS[0]}

# Return to root directory
cd ../..

# Check exit code
if [[ $BUILD_EXIT_CODE -eq 0 ]]; then
  echo "✓ Build successful"
else
  echo "✗ Build failed (exit code: $BUILD_EXIT_CODE)"
fi
```

**Build targets:**

- `make clean` - Clean build artifacts
- `make` or `make all` - Compile module (creates plugin.so/.dylib/.dll)
- `make dist` - Create distributable plugin archive (.vcvplugin)
- `make install` - Copy plugin to VCV Rack plugins directory
- `make clean all` - Clean build from scratch

### 6. Monitor Build Output

- Capture stdout and stderr
- Display progress messages to user
- Watch for error indicators
- Track build duration

### 7. Capture Exit Code

Check build exit code:

- **Exit 0**: Build succeeded → proceed to Success Protocol
- **Exit non-zero**: Build failed → proceed to Failure Protocol

### 8. Log File Location

Always show log file path after build attempt:

```
Build log: logs/[ModuleName]/build_TIMESTAMP.log
```

User can review full build output from log file if needed.

## Failure Protocol

When build fails (non-zero exit code), present this structured decision menu:

```
⚠️ Build failed

What would you like to do?
1. Investigate - Run troubleshooter agent to research the error (recommended)
2. Show me the build log - Display full build output for manual review
3. Show me the code - Open relevant source files where error occurred
4. Wait - I'll fix it manually and tell you to resume
5. Other

Choose (1-5): _
```

### Option 1: Investigate (Recommended)

**Purpose**: Automated diagnosis using troubleshooter agent

**Implementation**:

1. Extract error from build log (last 50 lines or first error indicator)
2. Parse error for key information:
   - Error message (exact text)
   - File/line reference (if available)
   - Error type (Make error, compilation, linker, etc.)
3. Invoke troubleshooter agent via Task tool:

   ```markdown
   Invoke troubleshooter agent to research this build error:

   Error: [extracted error message]
   Context: Building VCV Rack module "[ModuleName]" with Make
   VCV Rack SDK: [RACK_DIR path]
   Platform: [mac-arm64 | mac-x64 | linux-x64 | win-x64]
   File: [file path:line number if available]

   Please investigate using the graduated depth protocol and provide a structured report.
   ```

4. Wait for troubleshooter report (structured markdown)
5. Display report to user with findings and recommended solution
6. Ask: "Should I apply this solution?" (Yes/No/Modify)
   - **Yes**: Apply solution, then ask "Retry build now?"
   - **No**: Return to failure menu
   - **Modify**: Accept user modifications, then ask "Retry build now?"

**IMPORTANT**: NEVER auto-retry without explicit user confirmation.

### Option 2: Show Build Log

**Purpose**: Display full build output for manual analysis

**Implementation**:

1. Read log file: `logs/[ModuleName]/build_TIMESTAMP.log`
2. Display last 100 lines (or full log if < 100 lines)
3. Format for readability (preserve colors if possible)
4. After display, re-present decision menu (iterative debugging)

### Option 3: Show Code

**Purpose**: Display source files where error occurred

**Implementation**:

1. Parse build error for file/line reference
   - Make errors: Extract from Makefile references
   - Compilation errors: Extract from compiler output (e.g., "src/ModuleName.cpp:42")
   - Linker errors: Show relevant Makefile and header files
2. Read relevant source file using Read tool
3. Display file with context (±10 lines around error line if line number available)
4. If no file reference parseable: "Error location not found in build output. Try Option 2 (Show build log)."
5. After display, re-present decision menu (iterative debugging)

### Option 4: Wait (Manual Fix)

**Purpose**: User will fix issue manually outside workflow

**Implementation**:

1. Display exit message:

   ```
   Pausing workflow. Please fix the issue manually.

   When ready to retry the build, say:
   - "resume build" or "retry build" - Retry build with same target
   - "continue workflow" - Skip build and continue to next stage (not recommended)

   Build log: logs/[ModuleName]/build_TIMESTAMP.log
   Module directory: modules/[ModuleName]/
   ```

2. Exit skill, return control to invoking skill/workflow
3. Await user continuation command

### Option 5: Other

**Purpose**: Accept free-form user input for custom actions

**Implementation**:

1. Prompt: "What would you like to do?"
2. Accept free-text response
3. Interpret request and act accordingly:
   - Build-related: Execute custom build command
   - Code-related: Read/display requested files
   - Investigation: Perform custom research
   - Continue: Proceed as requested

## Success Protocol

When build succeeds (exit code 0), follow this workflow:

### 1. Verify Success

- Confirm build exit code 0
- Check that expected artifacts were created
- Extract output locations from build log

**Expected artifacts by target:**

- `make all`: `build/plugin.so` (macOS), `build/plugin.dll` (Windows), `build/plugin.so` (Linux)
- `make dist`: `dist/[ModuleName]-[version]-[platform].vcvplugin`

### 2. Display Success Message

Use this template:

**For Stage 2 (compilation verification):**

```
✓ Build successful (compilation verified)

Module: [ModuleName]
Platform: [mac-arm64 | mac-x64 | linux-x64 | win-x64]
Output: build/plugin.[so|dylib|dll]

Build time: [duration]
Log: logs/[ModuleName]/build_TIMESTAMP.log
```

**For full dist build (Stages 3-6, module-improve):**

```
✓ Build successful

Module: [ModuleName]
Platform: [mac-arm64 | mac-x64 | linux-x64 | win-x64]
Plugin: dist/[ModuleName]-[version]-[platform].vcvplugin

Build time: [duration]
Log: logs/[ModuleName]/build_TIMESTAMP.log

Ready to install to VCV Rack.
```

### 3. Context-Aware Decision Menu

Present menu based on invoking context:

#### From Stage 2 (Foundation)

```
Foundation verified. What's next?
1. Continue to Stage 3 (Shell/Parameters)
2. Review generated code
3. Pause workflow
```

#### From Stage 3 (Shell)

```
Shell built successfully. What's next?
1. Continue to Stage 4 (DSP)
2. Test in VCV Rack now
3. Review parameter code
4. Pause workflow
```

#### From Stage 4 (DSP)

```
DSP built successfully. What's next?
1. Run manual tests (recommended)
2. Continue to Stage 5 (GUI)
3. Test in VCV Rack now
4. Pause workflow
```

#### From Stage 5 (GUI)

```
GUI built successfully. What's next?
1. Run manual tests (recommended)
2. Continue to Stage 6 (Validation)
3. Test in VCV Rack now
4. Pause workflow
```

#### From Stage 6 (Validation)

```
Module complete! What's next?
1. Test in VCV Rack (recommended)
2. Install to VCV Rack (/install-module)
3. Make improvements (/improve)
```

#### From module-improve

```
Update built successfully. What's next?
1. Test changes in VCV Rack
2. Continue improving
3. Done (commit changes)
```

### 4. Return to Invoking Skill

After user makes decision, return control to the skill that invoked build-automation:

- **module-workflow**: Returns to stage dispatcher to continue or pause
- **module-improve**: Returns to improvement workflow to continue or finalize
- **Manual invocation**: Exits skill, displays final status

**IMPORTANT**: Always return control to invoking skill after success. Don't continue workflow autonomously.

## Integration Examples

### Example 1: module-workflow Stage 2 (Foundation)

**Scenario**: foundation-agent completes, module-workflow needs to verify compilation

**Invocation**:

- Skill: module-workflow
- Stage: 2 (Foundation)
- Action: Invoke build-automation with clean build

**Success Path**:

1. build-automation invokes: `make clean && make` in `modules/[ModuleName]/`
2. Build succeeds (compilation verified)
3. Displays success message with artifact location
4. Presents Stage 2 completion menu
5. Returns to module-workflow with status: SUCCESS

**Failure Path**:

1. Build fails (likely missing includes or API misuse)
2. build-automation presents 4-option failure menu
3. User chooses "Investigate"
4. troubleshooter diagnoses: "Missing rack.hpp include"
5. User confirms: "Apply solution"
6. Source file updated to include rack.hpp
7. User confirms: "Retry build"
8. Build succeeds
9. Returns to module-workflow with status: SUCCESS

### Example 2: module-workflow Stages 3-6 (Implementation Stages)

**Scenario**: dsp-agent completes Phase 4.2, module-workflow needs full dist build

**Invocation**:

- Skill: module-workflow
- Stage: 4 (DSP), Phase: 2
- Action: Invoke build-automation with dist target

**Success Path**:

1. build-automation invokes: `make dist` in `modules/[ModuleName]/`
2. Build succeeds, creates distributable plugin
3. Displays success message with .vcvplugin location
4. Presents Stage 4 completion menu: "Run manual tests / Continue to Stage 5 / Test in VCV Rack / Pause"
5. Returns to module-workflow with status: SUCCESS
6. module-workflow auto-invokes module-testing skill (if user chose "Run tests")

**Failure Path**:

1. Build fails (compilation error in DSP code)
2. Error: "modules/TestModule/src/TestModule.cpp:87: error: 'params' was not declared in this scope"
3. build-automation presents 4-option failure menu
4. User chooses "Show me the code"
5. Displays TestModule.cpp lines 77-97 with error highlighted
6. User sees issue: used 'params' instead of 'params[PARAM_ID]'
7. User says: "Wait" (will fix manually)
8. build-automation exits with: "When ready, say 'retry build'"
9. User fixes code manually
10. User says: "retry build"
11. module-workflow re-invokes build-automation
12. Build succeeds
13. Returns to module-workflow with status: SUCCESS

### Example 3: module-improve (Bug Fix or Feature Addition)

**Scenario**: module-improve applies bug fix to existing module, needs to rebuild

**Invocation**:

- Skill: module-improve
- Phase: 5 (Build & Test)
- Action: Invoke build-automation with dist target

**Success Path**:

1. build-automation invokes: `make dist` in `modules/[ModuleName]/`
2. Build succeeds
3. Displays success message
4. Presents improvement completion menu: "Test changes / Continue improving / Done"
5. Returns to module-improve with status: SUCCESS
6. module-improve continues to Phase 6 (CHANGELOG update)

**Failure Path**:

1. Build fails (regression from bug fix)
2. Error: "modules/MyModule/src/MyModule.cpp:142: error: cannot convert 'int' to 'float' in assignment"
3. build-automation presents 4-option failure menu
4. User chooses "Investigate"
5. troubleshooter agent invoked:
   ```
   Error: cannot convert 'int' to 'float' in assignment
   Context: Building VCV Rack module "MyModule" after bug fix
   File: src/MyModule.cpp:142
   ```
6. troubleshooter returns report:

   ```
   ## Research Report: Type Conversion Error

   ### Problem Identified
   - **Error:** cannot convert 'int' to 'float' in assignment
   - **Context:** Line 142 attempts to assign integer result to float voltage output
   - **Root Cause:** Changed return type of helper function but didn't update assignment

   ### Research Path
   Level 0 (Quick Assessment)

   ### Confidence Assessment
   - **Confidence Level:** HIGH
   - **Reasoning:** Error message is explicit, solution straightforward

   ### Recommended Solution
   Cast result to float: `outputs[OUTPUT_ID].setVoltage(static_cast<float>(calculateValue()));`
   Or change calculateValue() return type to float.

   **Why This Works:** Explicit type conversion satisfies compiler type checker.
   ```

7. User reviews report: "Apply solution"
8. Code updated with cast
9. User confirms: "Retry build"
10. Build succeeds
11. Returns to module-improve with status: SUCCESS

## Error Handling Rules

### Never Auto-Retry

**CRITICAL**: build-automation must NEVER automatically retry a failed build without explicit user decision. Always present failure menu and await user choice.

Bad (DON'T DO):

```
Build failed. Retrying with different flags...
```

Good (DO THIS):

```
⚠️ Build failed

What would you like to do?
1. Investigate...
```

### Preserve Context Between Retries

When user says "retry build" after manual fixes:

1. Use same build target as original build attempt
2. Preserve same invoking context (Stage 2, module-improve, etc.)
3. Return to same decision point after success/failure

### Handle Missing Dependencies

If build fails with dependency errors (RACK_DIR not set, SDK not found):

1. Display specific missing dependency
2. Provide configuration command (e.g., "Run /setup to configure environment")
3. After user configures, offer: "Retry build now?"

### Parse Errors Intelligently

Extract meaningful error information for troubleshooter:

- **Make errors**: Configuration issues, missing files, path problems
- **Compilation errors**: Syntax, type mismatches, missing declarations, API misuse
- **Linker errors**: Missing symbols, library issues
- **RACK_DIR errors**: SDK not found, wrong version

Pass full context to troubleshooter, not just error message.

## Performance Considerations

### Build Duration Tracking

Always display build duration in success/failure messages:

- Start timer before invoking make
- Stop timer after exit
- Format as "Build time: 2m 34s" or "Build time: 45s"

### Log File Management

- Build logs accumulate in `logs/[ModuleName]/`
- Each build creates timestamped log: `build_20251112_143022.log`
- No automatic cleanup (user can manually delete old logs)
- Always reference most recent log file

### Parallel Builds

Makefile can use parallel compilation:

```bash
# Use all available cores
make -j$(nproc)

# Or specify core count
make -j4
```

build-automation can pass `-j` flag to make for faster builds.

## Common Build Issues

### Issue: "RACK_DIR not set"

**Cause**: Environment variable missing

**Solution**: Run `/setup` to configure environment

### Issue: "rack.hpp not found"

**Cause**: RACK_DIR points to wrong location or SDK not installed

**Solution**: Verify RACK_DIR points to VCV Rack SDK directory containing `include/rack.hpp`

### Issue: "plugin.json not found"

**Cause**: Module directory structure incorrect

**Solution**: Verify plugin.json exists in module root

### Issue: "Undefined symbols during linking"

**Cause**: Missing VCV Rack API symbols

**Solution**: Verify Makefile includes proper LDFLAGS from RACK_DIR

### Issue: "Make command not found"

**Cause**: Make not installed

**Solution**: Install build tools (macOS: Xcode CLI tools, Linux: build-essential, Windows: MinGW)

## VCV Rack-Specific Build Notes

### Makefile Structure

VCV Rack modules use standardized Makefile:

```makefile
# Standard Rack plugin Makefile

RACK_DIR ?= ../..  # Path to VCV Rack SDK
FLAGS +=
SOURCES += src/plugin.cpp
SOURCES += src/ModuleName.cpp
DISTRIBUTABLES += res

include $(RACK_DIR)/plugin.mk
```

### Build Targets

- `make clean` - Remove build artifacts
- `make dep` - Build dependencies
- `make` - Compile module (default target)
- `make dist` - Create distributable .vcvplugin archive
- `make install` - Copy to VCV Rack plugins directory

### Platform-Specific Output

- **macOS**: `build/plugin.dylib`
- **Linux**: `build/plugin.so`
- **Windows**: `build/plugin.dll`

### Distributable Plugin

`make dist` creates platform-specific archive:

- **Format**: `dist/[ModuleName]-[version]-[platform].vcvplugin`
- **Contents**: ZIP archive containing plugin.json, plugin binary, and res/ folder
- **Platform string**: `mac-arm64`, `mac-x64`, `linux-x64`, `win-x64`

## Testing & Debugging

### Manual Invocation

Skill can be invoked manually for testing:

```
Please invoke the build-automation skill to build TestModule.

Context: Manual test of build system.
Expected: Full dist build.
```

### Simulated Failures

To test failure protocol:

1. Introduce intentional syntax error in module source
2. Invoke build-automation
3. Verify 4-option menu appears
4. Test each option (Investigate, Show log, Show code, Wait)
5. Verify troubleshooter integration works
6. Fix error and retry
7. Verify success path works

### Integration Testing

To test workflow integration:

1. Start new module workflow: `/implement TestModule`
2. Progress to Stage 2 (Foundation)
3. Verify build-automation invoked with clean build
4. Verify success returns to workflow
5. Progress to Stage 3+ and verify dist build invoked
6. Introduce failure and verify handling
7. Verify workflow resumes after fix

---

**Skill Status**: Ready for integration
**Last Updated**: 2025-11-12
**Dependencies**: Makefile (per module), RACK_DIR environment, .claude/agents/troubleshooter.md
