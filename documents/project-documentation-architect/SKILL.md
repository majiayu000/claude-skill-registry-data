---
name: Project Documentation Architect
description: Expert instructions for structuring and maintaining README and other documentation files.
---

# Project Documentation Architect

This skill provides the blueprint for high-quality, professional project documentation.

## README.md Structure

A standard `README.md` must contain the following sections:

### 1. Header
- **Project Title**: H1 Header.
- **Badges**: CI/CD status, License, Version (using `shields.io`).
- **Short Description**: A one-paragraph summary of what the project does.

### 2. Features (功能特色)
- Bulleted list of key features.
- Screen recordings (GIF/MP4) or Screenshots if UI-heavy.

### 3. Installation & Getting Started (安裝與快速開始)
- **Prerequisites**: JDK version, Android Studio version.
- **Build Steps**:
  ```bash
  git clone ...
  ./gradlew assembleDebug
  ```

### 4. Contributing (貢獻指南)
- Link to `CONTRIBUTING.md` if it exists, or brief rules (PR process, coding style).

### 5. License (授權)
- Copyright and License type.

## Bilingual Documentation (雙語文件)
**Rule**: Documentation must be accessible to both English and Traditional Chinese (Taiwan) readers.

**Strategy A: Side-by-Side**
Good for short documents.
> **Installation** / **安裝**
> Run the setup script.
> 請執行安裝腳本。

**Strategy B: Separate Files/Sections**
Good for long documents.
- `README.md` (English)
- `README_zh-TW.md` (Traditional Chinese)
- Add a visible link at the top: `[中文版](README_zh-TW.md) | [English](README.md)`

## Markdown Best Practices
- **Images**: Use relative paths `./docs/images/screenshot.png`.
- **Code Blocks**: Always specify language: ` ```java `, ` ```bash `.
- **Tables**: Use for feature comparison or configuration options.
