---
name: xcode-file-manager
description: Add Swift files to the AIQ Xcode project. Use when creating new Swift files (views, view models, services, models, tests) that need to be added to the Xcode project and build targets.
allowed-tools: Bash, Read, Write, Glob
---

# Xcode File Manager Skill

This skill handles adding Swift files to the AIQ Xcode project using the `xcodeproj` Ruby gem.

## When to Use This Skill

Use this skill whenever you:
- Create a new Swift file in the `ios/AIQ/` directory
- Create a new test file in the `ios/AIQTests/` directory
- Need to add existing Swift files to the Xcode project

## How to Add Files

### Using the Existing Script

There is a reusable Ruby script at `ios/scripts/add_files_to_xcode.rb`. Use it like this:

```bash
cd ios && ruby scripts/add_files_to_xcode.rb <relative_path_to_file>
```

**Examples:**

```bash
# Add a single file
cd ios && ruby scripts/add_files_to_xcode.rb AIQ/ViewModels/NewViewModel.swift

# Add multiple files
cd ios && ruby scripts/add_files_to_xcode.rb AIQ/Views/NewView.swift AIQ/ViewModels/NewViewModel.swift

# Add a test file (automatically added to AIQTests target)
cd ios && ruby scripts/add_files_to_xcode.rb AIQTests/NewTests.swift
```

### File Path Convention

- Paths must be relative to the `ios/` directory
- The script uses the directory structure to find the correct Xcode group
- Files in `AIQ/` are added to the main `AIQ` target
- Files in `AIQTests/` are added to the `AIQTests` target

### Common Directories

| Directory | Purpose | Target |
|-----------|---------|--------|
| `AIQ/Views/` | SwiftUI views | AIQ |
| `AIQ/ViewModels/` | View models | AIQ |
| `AIQ/Models/` | Data models | AIQ |
| `AIQ/Services/` | API and business services | AIQ |
| `AIQ/Utilities/` | Helper utilities | AIQ |
| `AIQTests/` | Unit tests | AIQTests |

### Creating New Groups

If you need to add a file to a group that doesn't exist in the Xcode project, you must first create the group in Xcode or modify the script to create groups dynamically.

## Prerequisites

The `xcodeproj` gem must be installed:

```bash
gem install xcodeproj
```

## Troubleshooting

- **"Group not found"**: The directory structure in the file path must match the group structure in the Xcode project
- **"File already in project"**: The file reference already exists; the script will skip it unless the path is incorrect
- **"File not found"**: The Swift file must exist on disk before running the script
