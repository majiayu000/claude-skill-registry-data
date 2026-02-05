---
name: gitattributes-config
description: Git attributes configuration for cross-platform line ending normalization and file handling. Includes 8 required pattern categories (global auto-detection, source code, shell scripts, Windows files, Docker files, binary files, lock files, generated files). Critical for Windows WSL compatibility. Use when creating or auditing .gitattributes files to prevent line ending issues and binary corruption.
---

# Gitattributes Configuration Skill

This skill provides the canonical .gitattributes patterns for MetaSaver monorepos.

## Core Principle

Use `* text=auto eol=lf` as the foundation - Git auto-detects text vs binary and normalizes to LF line endings.

## Required Patterns

### 1. Global Auto-Detection (REQUIRED)

```gitattributes
# Auto detect text files and perform LF normalization
* text=auto eol=lf
```

### 2. Source Code Files

```gitattributes
# JavaScript/TypeScript
*.js text eol=lf
*.jsx text eol=lf
*.ts text eol=lf
*.tsx text eol=lf
*.mjs text eol=lf
*.cjs text eol=lf

# JSON and YAML
*.json text eol=lf
*.yml text eol=lf
*.yaml text eol=lf

# Markdown
*.md text eol=lf
*.mdx text eol=lf

# CSS
*.css text eol=lf
*.scss text eol=lf
*.less text eol=lf

# HTML
*.html text eol=lf
*.htm text eol=lf
```

### 3. Shell Scripts (CRITICAL for WSL)

```gitattributes
# Shell scripts - CRITICAL: must be LF for Unix/WSL
*.sh text eol=lf
.husky/* text eol=lf
```

### 4. Windows Batch Files

```gitattributes
# Windows batch files - must be CRLF
*.bat text eol=crlf
*.cmd text eol=crlf
*.ps1 text eol=crlf
```

### 5. Docker Files

```gitattributes
# Docker files
Dockerfile text eol=lf
*.dockerfile text eol=lf
docker-compose.yml text eol=lf
docker-compose.yaml text eol=lf
.dockerignore text eol=lf
```

### 6. Binary Files

```gitattributes
# Images
*.png binary
*.jpg binary
*.jpeg binary
*.gif binary
*.ico binary
*.webp binary
*.svg text eol=lf
*.bmp binary
*.tiff binary

# Fonts
*.woff binary
*.woff2 binary
*.ttf binary
*.eot binary
*.otf binary

# Documents
*.pdf binary

# Archives
*.zip binary
*.gz binary
*.tar binary
*.7z binary

# Media
*.mp3 binary
*.mp4 binary
*.webm binary
*.ogg binary
```

### 7. Lock Files (Merge Strategy)

```gitattributes
# Lock files - prevent merge conflicts
pnpm-lock.yaml merge=ours linguist-generated
package-lock.json merge=ours linguist-generated
yarn.lock merge=ours linguist-generated
```

### 8. Generated Files

```gitattributes
# Generated files - mark as generated for GitHub
*.min.js linguist-generated
*.min.css linguist-generated
dist/** linguist-generated
build/** linguist-generated
coverage/** linguist-generated
```

## Complete Template

```gitattributes
# ========================================
# Git Attributes Configuration
# ========================================
# Ensures consistent line endings and file handling across platforms
# Critical for Windows WSL compatibility

# ========================================
# Auto-detection (REQUIRED)
# ========================================
* text=auto eol=lf

# ========================================
# Source Code - Explicit LF
# ========================================
*.js text eol=lf
*.jsx text eol=lf
*.ts text eol=lf
*.tsx text eol=lf
*.mjs text eol=lf
*.cjs text eol=lf
*.json text eol=lf
*.yml text eol=lf
*.yaml text eol=lf
*.md text eol=lf
*.mdx text eol=lf
*.css text eol=lf
*.scss text eol=lf
*.less text eol=lf
*.html text eol=lf
*.htm text eol=lf
*.xml text eol=lf
*.graphql text eol=lf
*.gql text eol=lf

# ========================================
# Shell Scripts - CRITICAL for Unix/WSL
# ========================================
*.sh text eol=lf
.husky/* text eol=lf

# ========================================
# Windows Scripts - CRLF required
# ========================================
*.bat text eol=crlf
*.cmd text eol=crlf
*.ps1 text eol=crlf

# ========================================
# Docker Files
# ========================================
Dockerfile text eol=lf
*.dockerfile text eol=lf
docker-compose.yml text eol=lf
docker-compose.yaml text eol=lf
.dockerignore text eol=lf

# ========================================
# Configuration Files
# ========================================
.gitignore text eol=lf
.gitattributes text eol=lf
.editorconfig text eol=lf
.prettierrc text eol=lf
.prettierignore text eol=lf
.eslintrc text eol=lf
.nvmrc text eol=lf

# ========================================
# Binary Files - No transformation
# ========================================
# Images
*.png binary
*.jpg binary
*.jpeg binary
*.gif binary
*.ico binary
*.webp binary
*.bmp binary
*.tiff binary
*.svg text eol=lf

# Fonts
*.woff binary
*.woff2 binary
*.ttf binary
*.eot binary
*.otf binary

# Documents
*.pdf binary

# Archives
*.zip binary
*.gz binary
*.tar binary
*.7z binary
*.rar binary

# Media
*.mp3 binary
*.mp4 binary
*.webm binary
*.ogg binary
*.wav binary
*.flac binary

# ========================================
# Lock Files - Merge Strategy
# ========================================
pnpm-lock.yaml merge=ours linguist-generated
package-lock.json merge=ours linguist-generated
yarn.lock merge=ours linguist-generated

# ========================================
# Generated Files
# ========================================
*.min.js linguist-generated
*.min.css linguist-generated
*.bundle.js linguist-generated
dist/** linguist-generated
build/** linguist-generated
coverage/** linguist-generated
```

## Validation Logic

```typescript
const REQUIRED_PATTERNS = {
  critical: [
    "* text=auto eol=lf", // Global auto-detection
    "*.sh text eol=lf", // Shell scripts
  ],
  high: [
    "*.js text eol=lf",
    "*.ts text eol=lf",
    "*.json text eol=lf",
    "*.md text eol=lf",
    "*.yml text eol=lf",
  ],
  medium: [
    "*.png binary",
    "*.jpg binary",
    "*.woff binary",
    "*.ttf binary",
    "pnpm-lock.yaml merge=ours",
  ],
  low: ["*.svg text eol=lf", "*.bat text eol=crlf", "Dockerfile text eol=lf"],
};

function validateGitattributes(content: string): ValidationResult {
  const lines = content
    .split("\n")
    .map((l) => l.trim())
    .filter((l) => !l.startsWith("#") && l);
  const violations = [];

  for (const [priority, patterns] of Object.entries(REQUIRED_PATTERNS)) {
    for (const pattern of patterns) {
      // Check if pattern exists (allowing for variations)
      const found = lines.some((line) => line.includes(pattern.split(" ")[0]));
      if (!found) {
        violations.push({
          pattern,
          priority,
          message: `Missing ${priority} pattern: ${pattern}`,
        });
      }
    }
  }

  return {
    valid: violations.filter((v) => v.priority === "critical").length === 0,
    violations,
  };
}
```

## Cross-Platform Compatibility

### Windows WSL Issues

- Shell scripts with CRLF endings fail: "bad interpreter"
- Fix: `*.sh text eol=lf` ensures LF on checkout

### Git Line Ending Flip-Flop

- Files changing between CRLF and LF in every commit
- Fix: `* text=auto eol=lf` normalizes to LF

### Binary File Corruption

- Images display incorrectly after checkout
- Fix: Mark as `binary` to prevent any transformation

## Common Mistakes

1. **Missing `* text=auto eol=lf`**: No global normalization
2. **No shell script LF**: Scripts fail on Unix/WSL
3. **Missing binary markers**: Images get corrupted
4. **No lock file strategy**: Constant merge conflicts
5. **Wrong Windows endings**: Batch files fail with LF

## Best Practices

1. **Start with auto-detection**: `* text=auto eol=lf`
2. **Be explicit**: Declare each file type explicitly
3. **Binary protection**: Mark ALL binary files
4. **Test cross-platform**: Verify on Windows, macOS, Linux
5. **Lock file strategy**: Use `merge=ours` for package locks
6. **Document patterns**: Use clear section comments
