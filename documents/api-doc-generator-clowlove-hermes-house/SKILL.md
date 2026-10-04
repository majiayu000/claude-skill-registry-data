---
name: api-doc-generator
description: "Generate API documentation from code, OpenAPI specs, or raw endpoints. Supports Markdown, HTML, and interactive documentation."
triggers:
  - "generate api docs"
  - "API 文档生成"
  - "openapi documentation"
  - "swagger docs"
---

# API Doc Generator

Generate beautiful API documentation from code or specs.

## Features

- 📝 **Multi-format** — Markdown, HTML, PDF
- 🎨 **Interactive** — Try-it-out functionality
- 📊 **OpenAPI** — Generate from OpenAPI/Swagger
- 🔄 **Auto-sync** — Keep docs updated
- 🌐 **Hosting** — Deploy to GitHub Pages

## Usage

### From Code

```bash
# Python FastAPI
hermes api-docs generate --framework fastapi --file main.py

# Node.js Express
hermes api-docs generate --framework express --dir ./src

# Go Gin
hermes api-docs generate --framework gin --file main.go
```

### From OpenAPI

```bash
# Generate from spec
hermes api-docs generate --spec openapi.yaml

# Update existing
hermes api-docs update --spec openapi.yaml --output ./docs
```

### Generate Output

```bash
# Markdown
hermes api-docs generate --format markdown --output README.md

# HTML (Redoc)
hermes api-docs generate --format html --output docs/

# Stoplight
hermes api-docs generate --format stoplight --output docs/
```

## Examples

### FastAPI Project
```bash
hermes api-docs generate \
  --framework fastapi \
  --file app/main.py \
  --title "My API" \
  --version 1.0.0 \
  --output docs/
```

### From OpenAPI 3.0
```bash
hermes api-docs generate \
  --spec api.yaml \
  --theme redoc \
  --output docs/
```

## Output Formats

| Format | Use Case | Interactive |
|--------|----------|-------------|
| Markdown | GitHub README | ❌ |
| HTML/Redoc | Self-hosted docs | ✅ |
| HTML/Swagger | Swagger UI | ✅ |
| Slate | Stripe-style docs | ✅ |
| PDF | Offline viewing | ❌ |

## Configuration

```yaml
# api-docs-config.yml
output:
  format: redoc
  theme: dark
  
metadata:
  title: My API
  version: 1.0.0
  description: API documentation
  
hosting:
  provider: github-pages
  branch: gh-pages
```

## Pitfalls

1. **Spec Quality** — Good docs need good OpenAPI spec
2. **Keep Updated** — Docs can become stale
3. **Security** — Don't expose internal endpoints