---
name: simulator-workflows
description: iOS Simulator device and app management with simctl. Use when managing simulator devices (boot, create, delete), installing/launching apps, or troubleshooting simulator issues. Covers device lifecycle, app lifecycle, and diagnostics.
---

# Simulator Workflows

**Use the `execute_simulator_command` MCP tool for all simulator management**

The xclaude-plugin provides the `execute_simulator_command` MCP tool which consolidates all simctl operations into a single, token-efficient dispatcher.

## ⚠️ CRITICAL: Always Use MCP Tools First

**This is the most important rule:** When working with iOS simulators, you MUST use the `execute_simulator_command` MCP tool.

- ✅ **DO**: Invoke `execute_simulator_command` for all device/app lifecycle operations
- ✅ **DO**: If the MCP tool fails, adjust parameters and retry
- ✅ **DO**: Read error messages and debug the parameters
- ❌ **NEVER**: Fall back to bash `xcrun simctl` commands
- ❌ **NEVER**: Use `simctl` directly in bash
- ❌ **NEVER**: Run `xcrun simctl` commands in a terminal

**Why?** The MCP tool provides:
- Structured error handling
- Token efficiency (consolidated into 1 tool vs. verbose bash output)
- Proper integration with the xclaude-plugin architecture
- Consistent response formatting

If `execute_simulator_command` fails, the issue is with parameters or device state - not that you should use bash.

## When to Use Bash (And When NOT to)

### ❌ NEVER Use Bash For These (Use MCP Tools Instead)

| Task | ❌ WRONG (Bash) | ✅ RIGHT (MCP Tool) |
|------|---------------|-------------------|
| List devices | `xcrun simctl list` | `execute_simulator_command` op: "list" |
| Boot simulator | `xcrun simctl boot <UDID>` | `execute_simulator_command` op: "device-lifecycle" sub: "boot" |
| Install app | `xcrun simctl install <UDID> <app.app>` | `execute_simulator_command` op: "app-lifecycle" sub: "install" |
| Launch app | `xcrun simctl launch <UDID> <bundle-id>` | `execute_simulator_command` op: "app-lifecycle" sub: "launch" |
| Screenshot | `xcrun simctl io <UDID> screenshot` | `execute_simulator_command` op: "io" sub: "screenshot" |

### ✅ Bash is Acceptable For (Non-Simulator Tasks)

- File operations: `mkdir`, `cp`, `rm`, `ls`, etc.
- Text inspection: `grep`, `find`, `cat`, etc.
- Git operations: `git status`, `git log`, etc.
- Environment checks: `which`, `simctl --version`, etc.
- Project exploration: `find . -name "*.app"`, etc.

### The Rule: If it's about simulator management → Use MCP tool, not bash

## Quick Reference

| Task | MCP Tool | Operation | Sub-Operation |
|------|----------|-----------|---------------|
| List devices | `execute_simulator_command` | `list` | - |
| Boot device | `execute_simulator_command` | `device-lifecycle` | `boot` |
| Shutdown device | `execute_simulator_command` | `device-lifecycle` | `shutdown` |
| Create device | `execute_simulator_command` | `device-lifecycle` | `create` |
| Delete device | `execute_simulator_command` | `device-lifecycle` | `delete` |
| Install app | `execute_simulator_command` | `app-lifecycle` | `install` |
| Launch app | `execute_simulator_command` | `app-lifecycle` | `launch` |
| Screenshot | `execute_simulator_command` | `io` | `screenshot` |
| Health check | `execute_simulator_command` | `health-check` | - |

## Device Management

### 1. Listing Devices - Use `execute_simulator_command` with operation: "list"

Invoke the `execute_simulator_command` MCP tool:

```json
{
  "operation": "list"
}
```

**Returns (Progressive Disclosure):**
```json
{
  "summary": {
    "total_devices": 47,
    "available_devices": 31,
    "booted_devices": 1
  },
  "booted": [
    {
      "name": "iPhone 15",
      "udid": "ABC123...",
      "state": "Booted",
      "runtime": "iOS 17.0"
    }
  ],
  "cache_id": "sim-list-xyz789",
  "next_steps": [
    "Use device name or UDID for operations",
    "Query cache_id for full device list if needed"
  ]
}
```

**Note:** Large device lists use progressive disclosure to save tokens.

### 2. Booting a Simulator - Use `execute_simulator_command` with device-lifecycle

Invoke the `execute_simulator_command` MCP tool:

**By Name:**
```json
{
  "operation": "device-lifecycle",
  "sub_operation": "boot",
  "device_id": "iPhone 15"
}
```

**By UDID:**
```json
{
  "operation": "device-lifecycle",
  "sub_operation": "boot",
  "device_id": "ABC123-DEF456-...",
  "parameters": {
    "wait_for_boot": true
  }
}
```

**wait_for_boot:** Blocks until device fully booted (recommended)

### 3. Shutting Down

```json
{
  "operation": "device-lifecycle",
  "sub_operation": "shutdown",
  "device_id": "iPhone 15"
}
```

### 4. Creating a New Simulator

```json
{
  "operation": "device-lifecycle",
  "sub_operation": "create",
  "device_id": "My iPhone 15 Test",
  "parameters": {
    "device_type": "iPhone 15",
    "runtime": "iOS 17.0"
  }
}
```

**Returns:** New device UDID

**Available Device Types:**
- iPhone SE (3rd generation)
- iPhone 14, 14 Plus, 14 Pro, 14 Pro Max
- iPhone 15, 15 Plus, 15 Pro, 15 Pro Max
- iPad (10th generation), iPad Air, iPad Pro

**Check available runtimes:** Use `list` to see installed iOS versions

### 5. Deleting a Simulator

```json
{
  "operation": "device-lifecycle",
  "sub_operation": "delete",
  "device_id": "My iPhone 15 Test"
}
```

**Warning:** This is permanent and cannot be undone.

### 6. Erasing a Simulator

**Remove all data but keep device:**

```json
{
  "operation": "device-lifecycle",
  "sub_operation": "erase",
  "device_id": "iPhone 15"
}
```

**When to erase:**
- Reset app state completely
- Clear test data
- Reproduce fresh install behavior

### 7. Cloning a Simulator

**Duplicate a device with all its data:**

```json
{
  "operation": "device-lifecycle",
  "sub_operation": "clone",
  "device_id": "iPhone 15",
  "parameters": {
    "new_name": "iPhone 15 Clone"
  }
}
```

**Use case:** Preserve a specific test state

## App Management

### 1. Installing an App

```json
{
  "operation": "app-lifecycle",
  "sub_operation": "install",
  "device_id": "iPhone 15",
  "app_identifier": "/path/to/MyApp.app"
}
```

**Note:** `app_identifier` is the path to `.app` bundle for install operation.

**Build + Install Pattern:**

```
1. execute_xcode_command (operation: build) → Get .app path
2. execute_simulator_command (operation: app-lifecycle, sub_operation: install)
```

### 2. Launching an App

```json
{
  "operation": "app-lifecycle",
  "sub_operation": "launch",
  "device_id": "iPhone 15",
  "app_identifier": "com.example.MyApp"
}
```

**With Arguments:**
```json
{
  "operation": "app-lifecycle",
  "sub_operation": "launch",
  "device_id": "iPhone 15",
  "app_identifier": "com.example.MyApp",
  "parameters": {
    "arguments": ["--test-mode", "--mock-data"],
    "environment": {
      "API_URL": "https://staging.example.com"
    }
  }
}
```

### 3. Terminating an App

```json
{
  "operation": "app-lifecycle",
  "sub_operation": "terminate",
  "device_id": "iPhone 15",
  "app_identifier": "com.example.MyApp"
}
```

### 4. Uninstalling an App

```json
{
  "operation": "app-lifecycle",
  "sub_operation": "uninstall",
  "device_id": "iPhone 15",
  "app_identifier": "com.example.MyApp"
}
```

### 5. Getting App Container Paths

**For accessing app data:**

```json
{
  "operation": "get-app-container",
  "device_id": "iPhone 15",
  "app_identifier": "com.example.MyApp",
  "parameters": {
    "container_type": "data"
  }
}
```

**Container Types:**
- **data**: App's Documents, Library, tmp directories
- **bundle**: App's .app bundle
- **group**: Shared group containers

**Returns:** File system path to container

**Use case:** Inspect database files, logs, or user defaults

## Capture & Media

### 1. Taking Screenshots

```json
{
  "operation": "io",
  "sub_operation": "screenshot",
  "device_id": "iPhone 15",
  "parameters": {
    "output_path": "/path/to/screenshot.png"
  }
}
```

**Auto-generated path:** If `output_path` omitted, creates temp file

### 2. Recording Video

```json
{
  "operation": "io",
  "sub_operation": "video",
  "device_id": "iPhone 15",
  "parameters": {
    "output_path": "/path/to/video.mp4",
    "duration": 30
  }
}
```

**Note:** Duration in seconds. Press Ctrl+C to stop recording manually.

## Advanced Operations

### 1. Opening URLs

```json
{
  "operation": "openurl",
  "device_id": "iPhone 15",
  "parameters": {
    "url": "myapp://deep-link/path"
  }
}
```

**Use cases:**
- Test universal links
- Test deep linking
- Open Safari to specific URL

### 2. Push Notifications

```json
{
  "operation": "push",
  "device_id": "iPhone 15",
  "app_identifier": "com.example.MyApp",
  "parameters": {
    "payload": {
      "aps": {
        "alert": "Test notification",
        "badge": 1,
        "sound": "default"
      }
    }
  }
}
```

**Payload:** Standard APNs JSON payload

## Environment Validation

### Health Check

**Verify iOS development environment:**

```json
{
  "operation": "health-check"
}
```

**Checks:**
- Xcode installation
- Command line tools
- simctl availability
- CoreSimulator framework

**Returns:**
```json
{
  "xcode_installed": true,
  "xcode_version": "15.0",
  "simctl_available": true,
  "issues": []
}
```

## Device Selection Strategies

### By Name (Easiest)

```json
{
  "device_id": "iPhone 15"
}
```

**Pro:** Readable, easy to remember
**Con:** May match multiple devices

### By UDID (Most Reliable)

```json
{
  "device_id": "ABC123-DEF456-GHI789..."
}
```

**Pro:** Unique, guaranteed single match
**Con:** Long, hard to remember

### Using "booted" (Convenience)

Some tools (like IDB) accept `"booted"` to target the currently booted simulator:

```json
{
  "target": "booted"
}
```

**Note:** Only works with IDB operations, not simctl

## Common Workflows

### Workflow: Fresh Install Test

```
1. boot → Start simulator
2. uninstall → Remove existing app
3. install → Install fresh build
4. launch → Start app
5. (UI automation) → Test flow
6. terminate → Stop app
7. shutdown → Stop simulator
```

### Workflow: Rapid Iteration

```
1. build → Compile latest code
2. install → Update app on simulator (already booted)
3. terminate → Stop running app
4. launch → Start updated app
```

**Note:** No need to boot/shutdown between iterations

### Workflow: Multi-Device Testing

```
1. list → Get available devices
2. For each device:
   - boot → Start device
   - install → Install app
   - launch → Start app
   - (run tests) → Execute test suite
   - terminate → Stop app
   - shutdown → Stop device
```

## Troubleshooting

### Device Not Found

**Problem:** "Unable to find device: iPhone 15"

**Solutions:**
1. Run `list` to see exact device names
2. Use UDID instead of name
3. Check device hasn't been deleted

### Unable to Boot

**Problem:** Boot fails or times out

**Solutions:**
1. Check disk space (simulators need space)
2. Shutdown other running simulators
3. Restart CoreSimulator: `killall -9 com.apple.CoreSimulator.CoreSimulatorService`
4. Run `health-check` to validate environment

### App Install Fails

**Problem:** Install operation fails

**Solutions:**
1. Verify .app path is correct
2. Check device is booted
3. Ensure .app is built for simulator (not device)
4. Try erasing simulator first

### App Won't Launch

**Problem:** Launch succeeds but app crashes immediately

**Solutions:**
1. Check app logs in Console.app
2. Verify app is signed correctly
3. Check for missing frameworks/resources
4. Try clean build + reinstall

## Performance Tips

### 1. Keep Simulators Booted

Booting is slow (~5-10 seconds). Keep simulator running during development.

### 2. Use Progressive Disclosure

Device lists can be large. Summary provides what you need 95% of the time.

### 3. Reuse Simulators

Creating/deleting is slower than erasing. Reuse devices when possible.

### 4. Parallel Operations

Boot multiple simulators in parallel for multi-device testing:

```
Launch 3 boot operations concurrently
Wait for all to complete
Proceed with testing
```

## Integration with Other Tools

### With Xcodebuild

```
1. execute_xcode_command (build) → Get .app bundle
2. execute_simulator_command (install) → Install to simulator
3. execute_simulator_command (launch) → Start app
```

### With IDB

```
1. execute_simulator_command (boot) → Start device
2. execute_idb_command (describe) → Query UI
3. execute_idb_command (tap) → Interact
```

### With Testing

```
1. execute_simulator_command (boot) → Start device
2. execute_xcode_command (test) → Run tests on device
3. execute_simulator_command (shutdown) → Stop device
```

## Integration with MCP Tools

This Skill works with `execute_simulator_command` tool:

- All operations use the `execute_simulator_command` tool
- Tool handles simctl execution
- Tool provides progressive disclosure for large outputs
- This Skill teaches WHEN and HOW to use operations

## Related Skills

- **xcode-workflows**: Building apps for simulators
- **ui-automation-workflows**: Automating simulator interactions
- **ios-testing-patterns**: Test execution strategies

## Related Resources

- `xc://operations/simulator`: Complete simctl operations reference
- `xc://reference/device-specs`: Available device types and runtimes
- `xc://reference/error-codes`: Common simulator errors

---

**Tip: Use `list` to discover, boot by name for convenience, use UDID for reliability.**
