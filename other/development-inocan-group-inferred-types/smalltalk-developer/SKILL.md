---
name: smalltalk-developer
description: Comprehensive Pharo Smalltalk development workflow guide with AI-driven Tonel editing. Provides expertise in Tonel file format syntax (class definitions with name, superclass, instVars, category, method categories, class comment placement), package structure (package.st placement, directory organization, BaselineOf dependencies), development workflow (Edit → Import → Test cycle with absolute paths, re-import timing, test execution), and Pharo best practices (CRC format documentation, method categorization conventions). Use when working with Pharo Smalltalk projects, creating or editing Tonel .st files, organizing packages and dependencies, resolving import order issues, writing class comments, implementing standard Pharo development patterns, or troubleshooting Tonel syntax.
---

# Smalltalk Developer Workflow

Implement the standard workflow for Pharo Smalltalk development using AI editors and the Tonel file format.

## Core Development Cycle

The fundamental workflow for Smalltalk development consists of three steps that repeat:

### 1. Edit Tonel Files

Edit Tonel files directly in the AI editor. The AI editor is the **single source of truth** for code.

**Key principle**: All code changes happen in `.st` files, not in the Pharo image.

**Tonel basics:**
- One class per `.st` file
- File name matches class name
- Each package directory contains `package.st`

For detailed Tonel syntax and examples, see [Tonel Format Reference](references/tonel-format.md).

### 2. Import to Pharo

**Before importing**, run lint to check code quality:

```
/st:lint src/MyPackage   # Check Smalltalk best practices
```

Then import the package into the running Pharo image using absolute paths:

```
mcp__smalltalk-interop__import_package: 'MyPackage' path: '/home/user/project/src'
```

**Critical rules:**
- ✅ **Lint before import** - Check code quality first
- ✅ Always use **absolute paths** (never relative)
- ✅ Re-import after **every change**
- ✅ Import packages in **dependency order**
- ✅ Import test packages **after main packages**

### 3. Run Tests

After import, run tests to verify changes:

```
mcp__smalltalk-interop__run_class_test: 'MyClassTest'
mcp__smalltalk-interop__run_package_test: 'MyPackage-Tests'
```

If tests fail, return to step 1, fix the Tonel file, and repeat.

## Essential Best Practices

### Path Management

**Always use absolute paths for imports:**
```
✅ /home/user/myproject/src
❌ ./src
❌ ../myproject/src
```

**Finding the source directory:**
1. Check `.project` file for `srcDirectory` field
2. Common locations: `src/`, `repositories/`
3. Construct full path: `<project_root>/<srcDirectory>`

See [Best Practices Reference](references/best-practices.md#path-management) for details.

### Package Dependencies

Check `BaselineOf<ProjectName>` to determine correct import order:

```smalltalk
baseline: spec
    <baseline>
    spec for: #common do: [
        spec
            package: 'MyPackage-Core';
            package: 'MyPackage-Json' with: [
                spec requires: #('MyPackage-Core')
            ]
    ]
```

**Import order**: Dependencies first → `MyPackage-Core` → `MyPackage-Json`

See [Best Practices: Dependencies](references/best-practices.md#package-dependencies-and-import-order) for complete guide.

### Import Timing

**Re-import after every change** - Pharo doesn't automatically reload files.

**Standard sequence:**
1. Edit `MyPackage/MyClass.st`
2. Import `MyPackage`
3. Edit `MyPackage-Tests/MyClassTest.st`
4. Import `MyPackage-Tests`
5. Run tests

### File Editing Philosophy

The AI editor is the source of truth:

- ✅ Edit `.st` files → Import to Pharo
- ❌ Edit in Pharo → Export to `.st` files

Use `export_package` only for:
- Initial project setup
- Emergency recovery
- Exploring existing code

See [Best Practices: File Editing](references/best-practices.md#file-editing-philosophy) for rationale.

## Common Patterns

### Pattern 1: Creating New Class

```
1. Create src/MyPackage/MyClass.st with class definition
2. import_package: 'MyPackage' path: '/absolute/path/src'
3. run_class_test: 'MyClassTest'
```

### Pattern 2: Adding Methods

```
1. Read existing src/MyPackage/MyClass.st
2. Add new method to file
3. import_package: 'MyPackage' path: '/absolute/path/src'
4. run_class_test: 'MyClassTest'
```

### Pattern 3: Multi-Package Development

```
1. Check BaselineOf for dependency order
2. Import packages in correct sequence
3. Import test packages last
4. Run comprehensive tests
```

For complete examples, see [Development Session Examples](examples/development-sessions.md).

## Automation

When this skill is active, automatically suggest:

1. **Import commands** after editing Tonel files
2. **Test commands** after successful import
3. **Debugging procedures** when tests fail

## Quick Reference

### MCP Tools

**Import:**
```
mcp__smalltalk-interop__import_package: 'PackageName' path: '/absolute/path'
```

**Test:**
```
mcp__smalltalk-interop__run_class_test: 'TestClassName'
mcp__smalltalk-interop__run_package_test: 'PackageName-Tests'
```

**Debug:**
```
mcp__smalltalk-interop__eval: 'Smalltalk code here'
```

**Validate (optional):**
```
mcp__smalltalk-validator__validate_tonel_smalltalk_from_file: '/path/to/file.st'
```

### Common Commands

- `/st:import PackageName /path` - Import package
- `/st:test TestClass` - Run tests
- `/st:eval code` - Execute Smalltalk snippet
- `/st:validate file.st` - Validate syntax

## Troubleshooting

### Import Fails

**"Package not found":**
- Verify absolute path is correct
- Check `package.st` exists
- Ensure package name matches directory

**"Syntax error":**
- Run `validate_tonel_smalltalk_from_file` first
- Check Tonel syntax (brackets, quotes, periods)

**"Dependency not found":**
- Check Baseline for required packages
- Import dependencies first

### Tests Fail

1. Read error message carefully
2. Use `/st:eval` to debug incrementally
3. Fix in Tonel file (not Pharo)
4. Re-import and re-test

See [Best Practices: Error Handling](references/best-practices.md#error-handling-and-debugging) for complete guide.

## Complete Documentation

This skill provides focused guidance for the core workflow. For comprehensive information:

- **[Tonel Format Reference](references/tonel-format.md)** - Complete Tonel syntax guide
- **[Style Guide](references/style-guide.md)** - Idiomatic Smalltalk patterns and concise coding practices
- **[Best Practices](references/best-practices.md)** - Detailed practices and patterns
- **[Development Examples](examples/development-sessions.md)** - Real-world session workflows

## Summary Workflow

```
Edit .st file
    ↓
Lint code (/st:lint)
    ↓
Import package (absolute path)
    ↓
Run tests
    ↓
Tests pass? → Done
    ↓
Tests fail? → Debug with /st:eval → Fix .st file → Re-import
```

**Remember**: The cycle is Edit → Lint → Import → Test. Never skip lint, import, or tests.
