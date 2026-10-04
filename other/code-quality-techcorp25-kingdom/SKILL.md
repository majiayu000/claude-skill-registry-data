---
name: production-code-quality
description: "Ensures consistent production-grade code quality with autonomous self-assessment for Python, JavaScript/TypeScript, and React Native projects. Use when writing, modifying, or reviewing ANY code to guarantee (1) Best-in-class implementation patterns, (2) Zero breaking changes without explicit user permission, (3) Full preservation of existing functionality and features, (4) Automatic compatibility verification with project files, (5) Self-assessment before delivering code, (6) React Native component quality, navigation, native module, and performance analysis. Triggers on all code generation, modification, refactoring, or review tasks — including React Native, Expo, NativeWind, and mobile development work."
---

# Production Code Quality Skill

This skill ensures every piece of code produced meets production-grade standards with zero tolerance for:
- Breaking changes without explicit permission
- Loss of existing functionality
- Compatibility issues with project files
- Substandard code quality

## Core Guarantees

1. **Best-in-Class Code**: Every output follows industry best practices
2. **Zero Surprise Breaking Changes**: All breaking changes require explicit approval
3. **Full Feature Preservation**: Original functionality is never lost
4. **Project Compatibility**: New code integrates seamlessly

## Self-Assessment Protocol

Before delivering ANY code, execute this mandatory workflow:

### Step 1: Pre-Modification Inventory

Before making changes:
- Catalog all existing functions, classes, and exports in target file
- Document current behavior and integration points
- Identify dependencies and dependents within the project

### Step 2: Compatibility Analysis

Run: `python scripts/compatibility_checker.py <file> <project_root>`

Requirements:
- MUST achieve compatibility score ≥ 95 to proceed
- Any CRITICAL compatibility issues block delivery
- Document all compatibility concerns in assessment report

### Step 3: Breaking Change Detection

Run: `python scripts/breaking_change_detector.py <original> <modified>`

Requirements:
- ANY breaking change requires explicit user permission
- HALT delivery and request permission before proceeding
- Never assume permission is granted

### Step 4: Functionality Preservation

Run: `python scripts/functionality_preserver.py <original> <modified>`

Requirements:
- 100% feature preservation required by default
- Any feature loss blocks delivery
- Document preservation verification in report

### Step 5: React Native Analysis (for RN projects)

Run: `python scripts/rn_analyzer.py <file_or_directory> [--project-root <path>]`

Requirements:
- MUST achieve RN quality score ≥ 90 to proceed
- Any CRITICAL or HIGH issues block delivery
- Covers component quality, navigation patterns, native module safety, and performance
- Uses Node.js AST parsing when available, falls back to regex pattern matching

### Step 6: Quality Assessment

Run: `python scripts/self_assessment.py <file> [--compare <original>] [--project-root <path>]`

Requirements:
- Generate comprehensive assessment report
- All quality criteria must pass
- Include report summary with delivery
- For RN projects, the orchestrator automatically invokes `rn_analyzer.py`

## Permission Protocol for Breaking Changes

When breaking changes are detected, follow this exact workflow:

1. **STOP** code delivery immediately

2. **PRESENT** detailed change impact analysis:
```
⚠️ BREAKING CHANGE DETECTED

The following changes will break existing functionality:
- [Change 1]: [Impact description]
- [Change 2]: [Impact description]

Affected components:
- [Component 1]: [How it's affected]
- [Component 2]: [How it's affected]

Risk Level: [CRITICAL/HIGH/MEDIUM]
```

3. **REQUEST** explicit confirmation:
```
Do you explicitly approve these breaking changes? 
Please respond with "yes" to approve or "no" to cancel.
```

4. **WAIT** for user response - do not proceed without explicit "yes"

5. **DOCUMENT** approval in code comments if approved:
```python
# BREAKING CHANGE APPROVED: [date]
# Change: [description]
# Approved by user for reason: [reason if provided]
```

6. **PROCEED** only after documented approval

## Reference Documentation

Load these references as needed:

- **Code Standards**: `references/code-standards.md` - Language-specific best practices (Python, JS/TS)
- **React Native Standards**: `references/react-native-standards.md` - Component quality, navigation, native modules, performance, Expo, NativeWind, and TypeScript patterns
- **Assessment Criteria**: `references/assessment-criteria.md` - Quality thresholds and metrics
- **Breaking Change Protocols**: `references/breaking-change-protocols.md` - Detailed approval workflow
- **Preservation Checklist**: `references/preservation-checklist.md` - Feature verification steps

## Script Reference

| Script | Purpose | When to Use |
|--------|---------|-------------|
| `compatibility_checker.py` | Verify project compatibility | Before any code modification |
| `breaking_change_detector.py` | Detect breaking changes | When modifying existing code |
| `functionality_preserver.py` | Verify feature preservation | After any modification |
| `rn_analyzer.py` | React Native quality analysis | When working with RN/Expo/NativeWind files |
| `self_assessment.py` | Complete quality assessment | Before delivering any code |

## Quality Standards by Language

### Python
- Type hints on all function signatures
- Docstrings for public functions and classes
- Error handling with specific exceptions
- Logging for significant operations
- PEP 8 compliance

### JavaScript/TypeScript
- TypeScript strict mode when applicable
- JSDoc comments for public APIs
- Proper error boundaries
- Async/await over callbacks
- ESLint compliance

### React Native

#### Component Quality
- Rules of Hooks compliance (no hooks in conditionals, loops, or callbacks)
- Explicit TypeScript interfaces for all component props
- `useState` for local UI state; `useReducer` for complex transitions
- Derived values computed via `useMemo`, never stored in state
- Custom hooks with single responsibility and typed returns

#### Navigation Patterns
- Typed navigators and screens (React Navigation `ParamList` types or Expo Router typed params)
- `_layout.tsx` files for every Expo Router route group
- Deep link parameters validated before use
- Prefer declarative `<Link>` over imperative `router.push()` for static navigation

#### Native Module Compatibility
- All native module access guarded by `Platform.OS` or `Platform.select`
- Expo module permissions checked before hardware access
- TurboModule lookups verified non-null before invocation
- JavaScript fallbacks provided for web/unsupported platforms

#### Performance Patterns
- `React.memo()` on presentational components receiving non-primitive props
- `useCallback()` on handlers passed to memoized children or FlatList
- FlatList: `keyExtractor`, `getItemLayout` (fixed height), stable `renderItem` reference
- No nested FlatList inside ScrollView (breaks virtualisation)
- `StyleSheet.create()` over inline style objects
- Explicit image dimensions to prevent layout thrash

### General
- Single Responsibility Principle
- DRY (Don't Repeat Yourself)
- KISS (Keep It Simple, Stupid)
- Meaningful variable and function names
- Appropriate code comments for complex logic

## Troubleshooting

### Assessment Fails

1. Review the detailed assessment report
2. Identify specific failures by category
3. Address each flagged issue
4. Re-run assessment until all checks pass
5. If unable to resolve, explain the blocker to user

### Cannot Preserve All Functionality

1. Document which features cannot be preserved
2. Explain technical reason for limitation
3. Present alternatives if available
4. Request explicit permission to proceed with reduced functionality
5. Never silently drop functionality

### Compatibility Score Below Threshold

1. Identify incompatible imports/dependencies
2. Check for conflicting function signatures
3. Verify integration points are maintained
4. Resolve conflicts or request guidance
5. Re-run compatibility check after fixes

### React Native Analysis Issues

1. If AST mode fails, the analyzer falls back to regex — results may be less precise
2. Install `@babel/parser` globally (`npm i -g @babel/parser`) for full AST coverage
3. For false positives on conditional hooks, verify the flagged line and suppress if valid
4. Navigation typing issues only flag in `.ts`/`.tsx` files — rename `.js` files if appropriate

## Assessment Report Format

Every code delivery includes an assessment summary:

```
## Assessment Summary
- Compatibility Score: XX/100
- Breaking Changes: None / X (all approved)
- Features Preserved: X/X (100%)
- RN Quality Score: XX/100 (if applicable)
- Quality Checks: PASS/FAIL

[Details if any issues]
```
