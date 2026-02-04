---
name: using-xcode
description: Use this before running `xcodebuild` or working with Xcode - tells you the specifics of how we use Xcode and its tools
---

## Building Xcode projects

When running Xcode builds, use the `xcodebuild-wrapper` script to automatically capture build data [`xcsift`](https://github.com/ldomaradzki/xcsift). Wrapper accepts the same arguments as `xcodebuild` itself.

```bash
./xcodebuild-wrapper build -scheme "Actions For Obsidian (macOS)"
```

The wrapper returns structured data for the build, so do not abbreviate or `tail` its output!

**Location**: `~/.claude/skills/using-xcode/xcodebuild-wrapper`

## Derived Data

**DO NOT** attempt to delete or remove the derived data folder unless explicitly told so.
