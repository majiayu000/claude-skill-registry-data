---
name: doc-formatter
description: Format documentation with emojis, status bars, and versioning matrix. Use when creating or updating README files, documentation, specs, or any markdown files.
---

# Documentation Formatter

Ensures all documentation has consistent formatting with emojis, status indicators, and version tracking.

## Required Elements

### 1. Emojis for Section Headers

Use these emojis consistently:

| Section | Emoji |
|---------|-------|
| Overview/About | 📋 |
| Features | ✨ |
| Installation | 📦 |
| Quick Start | 🚀 |
| Usage | 💡 |
| Configuration | ⚙️ |
| API/Reference | 📚 |
| Examples | 📝 |
| Testing | 🧪 |
| Deployment | 🌐 |
| Contributing | 🤝 |
| Changelog | 📜 |
| License | 📄 |
| Warning/Caution | ⚠️ |
| Important | ❗ |
| Tip/Note | 💡 |
| Success | ✅ |
| Error/Fail | ❌ |
| In Progress | 🔄 |
| Deprecated | ⛔ |

### 2. Status Bars (Shields.io Badges)

Include at the top of every README:

```markdown
![Status](https://img.shields.io/badge/Status-Active-success)
![Version](https://img.shields.io/badge/Version-1.0.0-blue)
![Last Updated](https://img.shields.io/badge/Last%20Updated-Dec%202025-orange)
```

#### Status Options
- `Active` (green/success)
- `Maintenance` (yellow/warning)
- `Deprecated` (red/critical)
- `Beta` (blue/informational)
- `Alpha` (purple)

### 3. Versioning Matrix

Include a compatibility/version matrix table:

```markdown
## 📊 Version Matrix

| Version | Status | Release Date | Node | Python | Notes |
|---------|--------|--------------|------|--------|-------|
| 3.0.0 | ✅ Current | Dec 2025 | 18+ | 3.9+ | Major refactor |
| 2.1.0 | 🔄 Maintained | Nov 2025 | 16+ | 3.8+ | Security fixes only |
| 1.x.x | ⛔ Deprecated | Oct 2024 | 14+ | 3.7+ | No longer supported |
```

Adapt columns based on project type (languages, frameworks, APIs, etc.)

## Template

```markdown
<div align="center">

# 📋 Project Name

Brief description here.

![Status](https://img.shields.io/badge/Status-Active-success)
![Version](https://img.shields.io/badge/Version-1.0.0-blue)
![Last Updated](https://img.shields.io/badge/Last%20Updated-Dec%202025-orange)

</div>

---

## ✨ Features

- Feature 1
- Feature 2

## 🚀 Quick Start

1. Step one
2. Step two

## 📊 Version Matrix

| Version | Status | Release Date | Notes |
|---------|--------|--------------|-------|
| 1.0.0 | ✅ Current | Dec 2025 | Initial release |

## ⚙️ Configuration

Configuration details...

## 📚 API Reference

API documentation...

## 🧪 Testing

How to run tests...

## 🤝 Contributing

Contribution guidelines...

## 📜 Changelog

See [CHANGELOG.md](CHANGELOG.md)

## 📄 License

License information...

---

*Last Updated: December 2025*
```

## Formatting Rules

1. **Every major section** gets an emoji prefix
2. **Status badges** go at the top, centered
3. **Version matrix** required for any project with releases
4. **Tables** should use emoji status indicators (✅ ❌ 🔄 ⛔)
5. **Code blocks** should specify language for syntax highlighting
6. **Links** should be descriptive, not "click here"

## When to Apply

Apply this formatting when:
- Creating new README.md files
- Updating existing documentation
- Writing spec documents
- Creating CHANGELOG files
- Any markdown file in the project
