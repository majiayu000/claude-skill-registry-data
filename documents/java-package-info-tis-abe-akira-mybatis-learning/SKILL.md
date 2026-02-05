---
name: java-package-info
description: Generate package-info.java files for Java packages. Use when the user requests to add package documentation files to Java packages, create package-info.java files, or document Java package structures. Automatically scans directories for Java packages and creates Javadoc package documentation files where they don't exist.
---

# Java Package Info Generator

Generate `package-info.java` files for Java packages with Javadoc comments.

## Quick Start

Generate package-info.java files for a Java project:

```bash
python3 scripts/generate_package_info.py <project-directory>
```

## Usage

### Basic Usage

Generate package-info.java for all Java packages:

```bash
python3 scripts/generate_package_info.py /path/to/project
```

### Filter by Base Package

Generate only for packages under a specific base package:

```bash
python3 scripts/generate_package_info.py /path/to/project --base-package com.example.myapp
```

### Preview Changes (Dry Run)

See what would be created without actually creating files:

```bash
python3 scripts/generate_package_info.py /path/to/project --dry-run
```

### Overwrite Existing Files

Force overwrite existing package-info.java files:

```bash
python3 scripts/generate_package_info.py /path/to/project --force
```

### Custom Source Root

Specify a different source root directory:

```bash
python3 scripts/generate_package_info.py /path/to/project --src-root src/java
```

## Generated Content

Each package-info.java file contains:

- **Package declaration**: Proper package statement
- **Javadoc comment**: Automatically generated description based on package name
- **UTF-8 encoding**: Standard Java file encoding

Example generated file for package `com.example.myapp.service`:

```java
/**
 * Serviceパッケージ
 *
 * <p>このパッケージはServiceに関連する機能を提供します。</p>
 */
package com.example.myapp.service;
```

## Behavior

- **Scans recursively**: Finds all directories containing .java files
- **Skips existing files**: By default, does not overwrite existing package-info.java
- **Ignores build directories**: Automatically skips `target/`, `build/`, `out/`
- **Handles nested packages**: Creates files for all package levels

## Common Use Cases

1. **New project setup**: Add package documentation to a new Java project
2. **Javadoc compliance**: Ensure all packages have documentation
3. **Code quality**: Improve project documentation coverage
4. **Batch processing**: Document multiple packages at once
