---
name: go-modules
description: Go modules and dependency management
sasmp_version: "1.3.0"
bonded_agent: 01-go-fundamentals
bond_type: SECONDARY_BOND
---

# Go Modules Skill

Master Go module system and dependency management.

## Overview

Complete guide for Go modules including versioning, private modules, vendoring, and dependency updates.

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| action | string | yes | - | Action: "init", "tidy", "vendor", "update" |
| private | bool | no | false | Handle private modules |

## Core Topics

### Module Initialization
```bash
# Initialize new module
go mod init github.com/myorg/myapp

# Download dependencies
go mod download

# Cleanup unused dependencies
go mod tidy

# Verify dependencies
go mod verify
```

### go.mod Structure
```go
module github.com/myorg/myapp

go 1.22

require (
    github.com/gin-gonic/gin v1.9.1
    github.com/jmoiron/sqlx v1.3.5
    go.uber.org/zap v1.26.0
)

require (
    // indirect dependencies auto-managed
    github.com/lib/pq v1.10.9 // indirect
)
```

### Private Modules
```bash
# Configure private module pattern
go env -w GOPRIVATE=github.com/myorg/*

# Use SSH for private repos
git config --global url."git@github.com:".insteadOf "https://github.com/"

# Or use access token
git config --global url."https://${GITHUB_TOKEN}@github.com/".insteadOf "https://github.com/"
```

### Vendoring
```bash
# Create vendor directory
go mod vendor

# Build with vendor
go build -mod=vendor ./...

# Verify vendor is in sync
go mod verify
```

### Dependency Updates
```bash
# List available updates
go list -m -u all

# Update specific dependency
go get github.com/gin-gonic/gin@latest

# Update all dependencies
go get -u ./...

# Update to specific version
go get github.com/gin-gonic/gin@v1.9.1

# Downgrade
go get github.com/gin-gonic/gin@v1.8.0
```

### Replace Directives
```go
// go.mod

// Local development
replace github.com/myorg/shared => ../shared

// Fork with fixes
replace github.com/original/pkg => github.com/myorg/pkg-fork v1.2.3

// Exclude vulnerable version
exclude github.com/vulnerable/pkg v1.0.0
```

### Workspace (Go 1.18+)
```go
// go.work
go 1.22

use (
    ./api
    ./shared
    ./worker
)
```

```bash
# Initialize workspace
go work init ./api ./shared

# Add module to workspace
go work use ./worker

# Sync workspace
go work sync
```

## Troubleshooting

### Failure Modes
| Symptom | Cause | Fix |
|---------|-------|-----|
| Module not found | Private repo | Set GOPRIVATE |
| Checksum mismatch | Proxy cache | GOPROXY=direct |
| Version conflict | Diamond dependency | Use `go mod graph` |

### Debug Commands
```bash
go mod graph                    # Show dependency graph
go mod why github.com/pkg/errors # Why is this needed?
go list -m -versions github.com/gin-gonic/gin # Available versions
```

## Usage

```
Skill("go-modules")
```
