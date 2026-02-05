---
name: go-linting
description: Go static analysis. Routes to specific tools.
---

# Linting

## Route by Tool
- go vet warnings → see [vet/](vet/)
- staticcheck issues → see [staticcheck/](staticcheck/)
- golangci-lint setup → see [golangci/](golangci/)

## Quick Check
- [ ] go vet ./... passes
- [ ] go fmt applied
- [ ] No unchecked errors

## Common Workflow
```bash
go fmt ./...
go vet ./...
staticcheck ./...
```

## Install Tools
```bash
go install honnef.co/go/tools/cmd/staticcheck@latest
go install github.com/golangci/golangci-lint/cmd/golangci-lint@latest
```
