---
name: reviewing-dependencies
description: Automated tooling and detection patterns for analyzing npm dependencies, unused packages, and dead code. Provides tool commands and what to look for—not how to structure output.
allowed-tools: Bash, Read, Grep, Glob
version: 1.0.0
---

# Dependencies Review Skill

## Purpose

This skill provides automated analysis commands and detection patterns for dependency issues. Use this as a reference for WHAT to check and HOW to detect issues—not for output formatting or workflow.

## Automated Analysis Tools

Run these scripts to gather metrics (if tools available):

### Unused Dependencies Detection

```bash
bash ~/.claude/plugins/marketplaces/claude-configs/review/scripts/review-unused-deps.sh
```

**Returns:** Unused dependencies, unused devDependencies, missing dependencies (imported but not in package.json)

### Unused Code Detection

```bash
bash ~/.claude/plugins/marketplaces/claude-configs/review/scripts/review-unused-code.sh
```

**Returns:** Unused exports, unused files, unused enum/class members, unused types/interfaces

### Security Audit

```bash
npm audit --json
npm audit --production --json
```

## Outdated Dependencies Detection

```bash
npm outdated
```

**Look for:**

- available patch/minor/major version upgrades
- Deprecated dependencies

### Bundle Analysis (if available)

```bash
npm run build -- --analyze
```

**Returns:** Bundle size breakdown, largest chunks

## Manual Detection Patterns

When automated tools unavailable or for deeper analysis, use Read/Grep/Glob to detect:

### Package.json Analysis

**Read package.json:**

```bash
cat package.json | jq '.dependencies, .devDependencies'
```

**Check for:**

- Version pinning strategy (^, ~, exact)
- Packages at latest/next tags
- Incorrect categorization (prod vs dev vs peer)
- Duplicate functionality patterns

### Usage Frequency Detection

**Count imports for specific package:**

```bash
grep -r "from ['\"]package-name['\"]" src/ | wc -l
grep -r "require(['\"]package-name['\"])" src/ | wc -l
```

**Find all import locations:**

```bash
grep -rn "from ['\"]package-name['\"]" src/
```

### Duplicate Functionality Detection

**Multiple date libraries:**

```bash
grep -E "moment|date-fns|dayjs|luxon" package.json
```

**Multiple HTTP clients:**

```bash
grep -E "axios|node-fetch|got|ky|superagent" package.json
```

**Multiple testing frameworks:**

```bash
grep -E "jest|mocha|jasmine|vitest" package.json
```

Uses skills tagged with `review: true` including reviewing-vitest-config from vitest-4 for detecting configuration deprecations and testing framework migration patterns.

**Multiple utility libraries:**

```bash
grep -E "lodash|underscore|ramda" package.json
```

### Tree-Shaking Opportunities

**Non-ES module imports:**

```bash
grep -r "import .* from 'lodash'" src/
grep -r "import _ from" src/
```

Look for: Default imports that could be named imports from ES module versions

**Large utility usage:**

```bash
grep -rn "from 'lodash'" src/ | head -20
```

Look for: Single function imports that could be inlined

### Dead Code Patterns

**Exported but never imported:**

```bash
# Find all exports
grep -rn "export (const|function|class|interface|type)" src/

# For each export, check if imported elsewhere
grep -r "import.*{ExportName}" src/
```

**Unused utility files:**

```bash
# Find utility/helper files
find src/ -name "*util*" -o -name "*helper*"

# Check if imported
grep -r "from.*utils" src/
```

**Deprecated code markers:**

```bash
grep -rn "@deprecated\|DEPRECATED\|DO NOT USE" src/
```

## Severity Mapping

Use these criteria when classifying findings:

| Pattern                               | Severity | Rationale                   |
| ------------------------------------- | -------- | --------------------------- |
| Vulnerable dependency (critical/high) | critical | Security risk in production |
| Unused dependency >100kb              | high     | Significant bundle bloat    |
| Multiple packages for same purpose    | high     | Maintenance overhead        |
| Vulnerable dependency (moderate)      | medium   | Security risk, lower impact |
| Unused dependency 10-100kb            | medium   | Moderate bundle bloat       |
| Unused devDependency                  | medium   | Maintenance overhead        |
| Single-use utility from large library | medium   | Tree-shaking opportunity    |
| Unused dependency <10kb               | nitpick  | Minimal impact              |
| Loose version ranges (^, ~)           | nitpick  | Potential instability       |
| Incorrect dependency category         | nitpick  | Organization issue          |

## Common Dependency Patterns

### Removal Candidates

**High Confidence (Unused):**

- Found by depcheck/Knip
- Zero imports in codebase
- Not in ignored files (scripts, config)
- Not peer dependency of other packages

**Medium Confidence (Low Usage):**

- 1-2 imports total
- Used only for simple operations
- Easy to inline or replace
- Alternative is smaller/native

**Consider Alternatives:**

- Large package (>50kb) with light usage
- Deprecated/unmaintained package
- Duplicate functionality exists
- Native alternative available

### Size Reference (Approximate)

| Category            | Examples                      | Typical Size |
| ------------------- | ----------------------------- | ------------ |
| Heavy date libs     | moment                        | 70kb         |
| Light date libs     | dayjs, date-fns (tree-shaken) | 2-10kb       |
| Heavy utilities     | lodash (full)                 | 70kb         |
| Light utilities     | lodash-es (per function)      | 1-5kb        |
| HTTP clients        | axios, node-fetch             | 10-15kb      |
| Native alternatives | fetch, Intl API               | 0kb          |

### Refactoring Patterns

**Replace large utility with inline:**

```typescript
// Before: lodash.debounce (71kb library)
import _ from 'lodash';
_.debounce(fn, 300);

// After: inline (0kb)
const debounce = (fn, ms) => {
  let timeout;
  return (...args) => {
    clearTimeout(timeout);
    timeout = setTimeout(() => fn(...args), ms);
  };
};
```

**Replace with tree-shakeable alternative:**

```typescript
// Before: full library
import moment from 'moment';
moment(date).format('YYYY-MM-DD');

// After: specific function
import { format } from 'date-fns/format';
format(date, 'yyyy-MM-dd');
```

**Replace with native alternative:**

```typescript
// Before: lodash
import { isEmpty } from 'lodash';
isEmpty(obj);

// After: native
Object.keys(obj).length === 0;
```

## Analysis Priority

1. **Run automated scripts first** (if tools available)

   - review-unused-deps.sh for unused packages
   - review-unused-code.sh for dead code
   - npm audit for security issues

2. **Parse script outputs** for package names and file locations

3. **Verify usage with grep** for each flagged package

   - Count imports
   - Check import patterns (default vs named)
   - Identify usage locations

4. **Read package.json** to check:

   - Version ranges
   - Dependency categorization
   - Duplicate functionality

5. **Cross-reference findings:**
   - Unused package + large size = high priority
   - Low usage + available alternative = medium priority
   - Vulnerable package + unused = critical priority

## Integration Notes

- This skill provides detection methods and patterns only
- Output formatting is handled by the calling agent
- Severity classification should align with agent's schema
- Do NOT include effort estimates, bundle size savings calculations, or success criteria
- Do NOT provide refactoring instructions beyond pattern examples
