---
name: odin-install
description: |
  Install and configure the Odin programming language. Use when:
  - Setting up Odin on a new machine
  - Updating Odin to latest version
  - Configuring Odin language server (ols)
---

# Odin Installation

## Quick Install (Linux)

**Step 1**: Get the download URL for the latest release:
```bash
curl -sL https://api.github.com/repos/odin-lang/Odin/releases/latest | grep -o '"browser_download_url": "[^"]*linux[^"]*amd64[^"]*"' | head -1 | cut -d'"' -f4
```

**Step 2**: Download using the URL from Step 1 (replace URL as needed):
```bash
curl -L "https://github.com/odin-lang/Odin/releases/download/dev-2025-12a/odin-linux-amd64-dev-2025-12a.tar.gz" -o /tmp/odin.tar.gz
```

**Step 3**: Extract and install:
```bash
sudo tar -xzf /tmp/odin.tar.gz -C /opt/
```

**Step 4**: Find the extracted directory and create symlink:
```bash
ls /opt/ | grep odin
# Then create symlink (adjust directory name as needed):
sudo ln -sf /opt/odin-linux-amd64-nightly+2025-12-04/odin /usr/local/bin/odin
```

**Step 5**: Verify installation:
```bash
odin version
```

## Prerequisites

### Linux (Debian/Ubuntu)

```bash
# Odin uses libatomic from GCC
clang++ -v  # Check "Selected GCC installation" version
sudo apt install libstdc++-12-dev  # or version 14

# For SDL2 (vendor library)
sudo apt install libsdl2-dev
```

### macOS

```bash
# Using Homebrew
brew install odin
brew install sdl2  # For SDL2 projects
```

## From Source

```bash
# Install LLVM (14, 17, 18, 19, 20, or 21)
sudo apt install llvm-17 clang-17 lld-17

# Clone and build
git clone https://github.com/odin-lang/Odin
cd Odin
make release-native

# Add to PATH
export PATH="$PWD:$PATH"
```

## Language Server (OLS) and Formatter

### Install OLS from Source

```bash
# Clone OLS repository
cd /tmp && git clone --depth 1 https://github.com/DanielGavin/ols.git

# Build OLS (uses build script)
cd /tmp/ols && ./build.sh

# Build odinfmt formatter
./odinfmt.sh

# Install to system
sudo cp /tmp/ols/ols /usr/local/bin/
sudo cp /tmp/ols/odinfmt /usr/local/bin/

# Verify installation
which ols odinfmt
```

### Check if OLS is installed

```bash
# Check for OLS and odinfmt
which ols odinfmt

# If missing, follow the install steps above
```

### Configure OLS (ols.json in project root)

After installing, create `ols.json` in your project root:

```json
{
    "$schema": "https://raw.githubusercontent.com/DanielGavin/ols/master/misc/ols.schema.json",
    "collections": [
        { "name": "core", "path": "/opt/odin-linux-amd64-nightly+2025-12-04/core" },
        { "name": "vendor", "path": "/opt/odin-linux-amd64-nightly+2025-12-04/vendor" }
    ],
    "enable_semantic_tokens": true,
    "enable_snippets": true,
    "enable_inlay_hints": true,
    "enable_hover": true,
    "enable_document_symbols": true,
    "enable_format": true,
    "enable_procedure_snippet": true,
    "enable_references": true,
    "odin_command": "/usr/local/bin/odin"
}
```

**Note**: Adjust the collection paths to match your actual Odin install directory (use `ls /opt/ | grep odin`).

### Using odinfmt

```bash
# Format a file (output to stdout)
odinfmt /path/to/file.odin

# Format and overwrite file in place
odinfmt -w /path/to/file.odin

# Format from stdin
echo 'package main; main :: proc() { x:=1 }' | odinfmt -stdin
```

## Project Setup

```bash
# Create new project
mkdir my-project && cd my-project
mkdir -p src build

# Create main file
cat > src/main.odin << 'EOF'
package main

import "core:fmt"

main :: proc() {
    fmt.println("Hello, Odin!")
}
EOF

# Create ols.json for language server
cat > ols.json << 'EOF'
{
    "$schema": "https://raw.githubusercontent.com/DanielGaworski/ols/master/misc/ols.schema.json",
    "collections": [
        { "name": "core", "path": "ODIN_ROOT/core" },
        { "name": "vendor", "path": "ODIN_ROOT/vendor" }
    ]
}
EOF

# Create Makefile
cat > Makefile << 'EOF'
.PHONY: build run clean debug test

build:
	odin build src -out:build/app

run: build
	./build/app

debug:
	odin build src -out:build/app -debug

clean:
	rm -rf build/

test:
	odin test src -out:build/test
EOF

# Create .gitignore
cat >> .gitignore << 'EOF'
build/
*.o
*.obj
EOF

# Build and run
make run
```

## Verify Installation

```bash
# Check version
odin version

# Check LLVM backend
odin report

# Run hello world
odin run -file:src/main.odin
```

## Update Odin

**Step 1**: Remove old version:
```bash
sudo rm -rf /opt/odin-*
```

**Step 2**: Follow the Quick Install steps above to download and install the latest version.

**Step 3**: Verify the update:
```bash
odin version
```

## Troubleshooting

### "atomic.h not found"
```bash
sudo apt install libstdc++-12-dev
# or libstdc++-14-dev depending on clang version
```

### LLVM version mismatch
```bash
# Check supported versions
odin report

# Set explicit LLVM
LLVM_CONFIG=/usr/bin/llvm-config-17 make release-native
```

### SDL2 not found
```bash
sudo apt install libsdl2-dev
# Or on macOS: brew install sdl2
```
