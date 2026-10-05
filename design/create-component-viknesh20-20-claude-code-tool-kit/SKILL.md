---
name: create-component
description: "Scaffolds a new component, module, or package following the project's existing structure, naming conventions, and patterns. Auto-detects framework and generates all necessary files including tests."
argument-hint: "[component/module name]"
allowed-tools: Read, Glob, Grep, Bash, Write
---

# Create Component / Module

## Detect Project Structure
!`ls -d src/ app/ lib/ pkg/ cmd/ internal/ components/ pages/ modules/ features/ 2>/dev/null`
!`ls package.json go.mod Cargo.toml pyproject.toml *.csproj Gemfile mix.exs 2>/dev/null`

## Existing Components (for pattern matching)
!`find . -type d -maxdepth 4 \( -path "*/components/*" -o -path "*/modules/*" -o -path "*/features/*" -o -path "*/pkg/*" -o -path "*/internal/*" \) -not -path "*/node_modules/*" -not -path "*/.git/*" 2>/dev/null | head -20`

---

## Scaffolding Process

### Step 1: Analyze Existing Patterns
1. Find the most similar existing component/module
2. Note its file structure:
   - Main implementation file
   - Test file
   - Types/interfaces file
   - Index/barrel file
   - Styles file (if frontend)
   - Storybook/docs file (if applicable)
3. Note naming conventions:
   - PascalCase, camelCase, kebab-case, or snake_case?
   - File extensions (.tsx, .ts, .py, .go, etc.)
   - Test file suffix (.test.ts, _test.go, test_.py, _spec.rb, etc.)

### Step 2: Determine What to Generate

Based on the detected framework:

**React/Next.js/Vue:**
```
ComponentName/
├── ComponentName.tsx       # Main component
├── ComponentName.test.tsx  # Tests
├── ComponentName.types.ts  # TypeScript interfaces
├── ComponentName.module.css # Styles (if CSS modules used)
└── index.ts               # Barrel export
```

**Python:**
```
module_name/
├── __init__.py            # Public exports
├── module_name.py         # Main implementation
├── models.py              # Data models (if applicable)
└── test_module_name.py    # Tests
```

**Go:**
```
packagename/
├── packagename.go         # Main implementation
├── packagename_test.go    # Tests
└── types.go               # Type definitions (if needed)
```

**Rust:**
```
module_name/
├── mod.rs                 # Module entry point
├── types.rs               # Types and structs
└── tests.rs               # Tests
```

**C#/.NET:**
```
ModuleName/
├── ModuleName.cs          # Main class
├── IModuleName.cs         # Interface
└── ModuleNameTests.cs     # Tests
```

### Step 3: Generate Files
For each file:
1. Use the patterns found in Step 1
2. Include proper imports/using statements
3. Add standard boilerplate (constructor, basic methods)
4. Follow the project's export pattern
5. Include a skeleton test file with at least one test

### Step 4: Register the Component
- Add to barrel exports if the project uses them
- Register routes if it's a page/endpoint
- Add to module system if applicable (Angular modules, Python packages, etc.)

---

## Rules
- **Mirror existing patterns exactly** — don't introduce new conventions
- **Minimal boilerplate** — generate just enough to be useful, not bloated
- **Include tests** — always create the test file
- **Don't guess** — if you can't determine the convention, ask the user
