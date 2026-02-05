---
name: build-swift-project
description: Build and test the LocalizeAR Swift project using build.sh scripts. Use this skill whenever building, testing, or cleaning the project. NEVER use xcodebuild or swift build directly - always use build.sh.
allowed-tools: Bash(./build.sh:*), Bash(./Examples/LARExplorer/build.sh:*), Bash(./Examples/LARScan/build.sh:*)
---

# Build LocalizeAR Project

This skill manages building and testing the LocalizeAR Swift project using build scripts that properly configure compilers.

## CRITICAL: Always Use build.sh

**NEVER use these commands directly:**
- `xcodebuild`
- `swift build`
- `swift test`

**ALWAYS use build.sh scripts instead** - they configure Apple Clang to prevent gcc-12 conflicts from Homebrew.

## Main Library (LocalizeAR)

Located at project root. Use `./build.sh`:

| Command | Description |
|---------|-------------|
| `./build.sh` | Debug build |
| `./build.sh test` | Build and run tests |
| `./build.sh release` | Optimized release build |
| `./build.sh clean` | Remove build artifacts |

## Example Apps

### LARExplorer (macOS)

Located at `Examples/LARExplorer/`. Use `./Examples/LARExplorer/build.sh`:

| Command | Description |
|---------|-------------|
| `./Examples/LARExplorer/build.sh` | Debug build |
| `./Examples/LARExplorer/build.sh test` | Run unit tests |
| `./Examples/LARExplorer/build.sh release` | Release build |
| `./Examples/LARExplorer/build.sh clean` | Clean artifacts |

### LARScan (iOS)

Located at `Examples/LARScan/`. Use `./Examples/LARScan/build.sh` if available.

## Example Requests

- "Build the project" → `./build.sh`
- "Run the tests" → `./build.sh test`
- "Build LARExplorer" → `./Examples/LARExplorer/build.sh`
- "Test LARExplorer" → `./Examples/LARExplorer/build.sh test`
- "Clean everything" → `./build.sh clean`

## Why build.sh?

The build scripts:
1. Set `CC` and `CXX` to Apple Clang (not Homebrew's gcc-12)
2. Prevent "unrecognized command-line option" errors
3. Match CI/CD configuration exactly
4. Display compiler versions for verification
