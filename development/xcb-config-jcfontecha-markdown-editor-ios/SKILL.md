---
name: xcb-config
description: Configure xcb.json to map Xcode schemes to workspaces/projects for building with xcb
---

# xcb Configuration Guide

xcb is a CLI wrapper around xcodebuild. The `xcb.json` file maps scheme names to their containers (workspace, project, or Swift package).

## Config Structure

```json
{
  "version": 1,
  "open": {
    "defaultTarget": "app",
    "aliases": {
      "demo": "demo-app",
      "kit": "packages"
    }
  },
  "builds": [
    {
      "id": "optional-identifier",
      "scheme": "SchemeName",
      "workspace": "Path/To/App.xcworkspace",
      "destination": "platform=iOS Simulator,name=iPhone 15",
      "configuration": "Debug"
    }
  ]
}
```

## Build Entry Fields

| Field | Required | Description |
|-------|----------|-------------|
| `scheme` | Yes | Xcode scheme name (must match exactly) |
| `workspace` | One of these | Path to `.xcworkspace` file |
| `project` | required | Path to `.xcodeproj` file |
| `packageDir` | | Path to Swift package directory |
| `id` | No | Identifier for the build entry |
| `destination` | No | xcodebuild destination string |
| `configuration` | No | Build configuration (Debug/Release) |
| `sdk` | No | SDK name (iphonesimulator, iphoneos, macosx) |

## Open Shortcuts

If your repo has multiple Xcode containers, configure which one `xcb open` should use:

```json
{
  "open": {
    "defaultTarget": "app",
    "aliases": {
      "demo": "demo-app",
      "kit": "packages"
    }
  }
}
```

- `open.defaultTarget` points to a build entry by `id` (preferred) or by `scheme`.
- `open.aliases` maps short names to build entry `id` (or scheme).

Then:

```bash
xcb open           # opens defaultTarget
xcb open demo      # opens aliases.demo
```

## Common Destinations

- iOS Simulator: `"platform=iOS Simulator,name=iPhone 15"`
- Generic iOS: `"generic/platform=iOS"`
- macOS: `"platform=macOS"`
- watchOS Simulator: `"platform=watchOS Simulator,name=Apple Watch Series 9 (45mm)"`

## How to Configure

1. Run `xcb schemes` to list available schemes from the workspace/project
2. For each scheme you want to build, add a build entry with:
   - The exact `scheme` name
   - The `workspace` or `project` path containing that scheme
   - Optional `destination` and `configuration`

## Example: App with SPM Dependencies

```json
{
  "version": 1,
  "builds": [
    {
      "id": "app",
      "scheme": "MyApp",
      "workspace": "MyApp.xcworkspace",
      "destination": "platform=iOS Simulator,name=iPhone 15",
      "configuration": "Debug"
    },
    {
      "id": "tests",
      "scheme": "MyAppTests",
      "workspace": "MyApp.xcworkspace",
      "destination": "platform=iOS Simulator,name=iPhone 15",
      "configuration": "Debug"
    }
  ]
}
```

## Example: Swift Package

```json
{
  "version": 1,
  "builds": [
    {
      "scheme": "MyLibrary",
      "packageDir": ".",
      "destination": "generic/platform=iOS"
    }
  ]
}
```

## Example: Swift Package that Uses UIKit (macOS `swift build` will fail)

If any package targets import UIKit, do **not** rely on `swift build` on macOS. Use an iOS Simulator destination in `xcb.json`:

```json
{
  "version": 1,
  "builds": [
    {
      "id": "uikit-package",
      "scheme": "MyUIKitPackage",
      "packageDir": ".",
      "destination": "platform=iOS Simulator,name=iPhone 15",
      "configuration": "Debug"
    }
  ]
}
```

Notes:
- `xcb` will auto-generate a `.xcodeproj` for the package if needed.
- If you **explicitly** pass `--destination` or `--sdk`, those override defaults.

## Usage After Configuration

```bash
xcb MyApp          # Build the MyApp scheme
xcb MyAppTests     # Build the test scheme
xcb schemes        # List all available schemes
```