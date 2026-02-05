---
name: codebase-analyzer
description: Analyze codebases to find patterns and anti-patterns, identify code duplication, suggest optimizations, analyze dependencies, and perform automated code reviews
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - Task
---

# Codebase Analyzer

Expert skill for comprehensive codebase analysis and quality assessment. Specializes in pattern detection, code duplication analysis, performance optimization, dependency auditing, and automated code review.

## Core Capabilities

### 1. Pattern Detection
- Design patterns (Singleton, Factory, Observer, etc.)
- React patterns (HOC, Render Props, Hooks, Compound Components)
- Anti-patterns (God components, Prop drilling, Premature optimization)
- Architectural patterns (MVC, MVVM, Flux, Clean Architecture)
- Code smells (Long methods, large classes, duplicated code)

### 2. Code Duplication Analysis
- Exact code duplication
- Similar code blocks (clone detection)
- Copy-paste programming detection
- Opportunities for abstraction
- Refactoring suggestions
- DRY (Don't Repeat Yourself) violations

### 3. Optimization Opportunities
- Performance bottlenecks
- Unnecessary re-renders (React)
- Bundle size optimization
- Memory leaks
- Inefficient algorithms
- Database query optimization
- Network request optimization

### 4. Dependency Analysis
- Unused dependencies
- Outdated packages
- Security vulnerabilities
- Circular dependencies
- Dependency graph visualization
- Import/export analysis
- Package size impact

### 5. Code Quality Metrics
- Cyclomatic complexity
- Code coverage
- Maintainability index
- Technical debt assessment
- Lines of code (LOC)
- Comment ratio
- Test-to-code ratio

### 6. Automated Code Review
- Style consistency
- Best practices adherence
- Accessibility issues
- Type safety problems
- Security vulnerabilities
- Performance concerns
- Documentation quality

## Workflow

### Phase 1: Initial Analysis
1. **Codebase Discovery**
   - Scan directory structure
   - Identify project type (React, Vue, Node.js, etc.)
   - Detect frameworks and libraries
   - Map file organization

2. **Metric Collection**
   - Count files, lines, components
   - Measure code complexity
   - Check test coverage
   - Analyze bundle size

3. **Quick Health Check**
   - TypeScript errors
   - Linting issues
   - Test failures
   - Build warnings

### Phase 2: Deep Analysis
1. **Pattern Detection**
   - Identify common patterns
   - Detect anti-patterns
   - Find inconsistencies
   - Note architectural issues

2. **Duplication Analysis**
   - Find duplicate code
   - Identify similar structures
   - Suggest abstractions
   - Calculate duplication percentage

3. **Dependency Audit**
   - Check for vulnerabilities
   - Find unused dependencies
   - Identify outdated packages
   - Analyze bundle impact

4. **Performance Analysis**
   - Identify bottlenecks
   - Find unnecessary renders
   - Check bundle sizes
   - Analyze load times

### Phase 3: Reporting & Recommendations
1. **Generate Report**
   - Executive summary
   - Detailed findings
   - Metrics and charts
   - Priority rankings

2. **Provide Recommendations**
   - Quick wins
   - High-impact improvements
   - Long-term refactoring
   - Best practices

3. **Create Action Plan**
   - Prioritized tasks
   - Effort estimates
   - Implementation guides
   - Success metrics

## Analysis Techniques

### Pattern Detection Scripts

#### Find Large Components
```typescript
// analyze-components.ts
import { readFileSync, readdirSync, statSync } from 'fs'
import { join } from 'path'

interface ComponentMetrics {
  file: string
  lines: number
  complexity: number
  hooks: number
  props: number
}

function analyzeComponent(filePath: string): ComponentMetrics {
  const content = readFileSync(filePath, 'utf-8')
  const lines = content.split('\n').length

  // Count hooks
  const hookMatches = content.match(/use[A-Z]\w+/g) || []
  const hooks = new Set(hookMatches).size

  // Estimate complexity (simplified)
  const complexity =
    (content.match(/if|else|switch|case|for|while|&&|\|\|/g) || []).length

  // Count props
  const propsMatch = content.match(/interface \w+Props \{([^}]+)\}/)
  const props = propsMatch
    ? propsMatch[1].split('\n').filter(l => l.trim()).length
    : 0

  return { file: filePath, lines, complexity, hooks, props }
}

function findLargeComponents(dir: string): ComponentMetrics[] {
  const results: ComponentMetrics[] = []

  function walk(currentDir: string) {
    const files = readdirSync(currentDir)

    for (const file of files) {
      const filePath = join(currentDir, file)
      const stat = statSync(filePath)

      if (stat.isDirectory()) {
        if (!file.includes('node_modules') && !file.includes('dist')) {
          walk(filePath)
        }
      } else if (file.match(/\.(tsx|jsx)$/)) {
        const metrics = analyzeComponent(filePath)
        if (metrics.lines > 200 || metrics.complexity > 20) {
          results.push(metrics)
        }
      }
    }
  }

  walk(dir)
  return results.sort((a, b) => b.lines - a.lines)
}

// Usage
const largeComponents = findLargeComponents('./src')
console.table(largeComponents)
```

#### Detect Code Duplication
```bash
# Using jscpd (JavaScript Copy/Paste Detector)
npx jscpd src/ --min-lines 5 --min-tokens 50 --format markdown -o duplication-report.md
```

```json
// .jscpd.json
{
  "threshold": 3,
  "reporters": ["html", "markdown", "console"],
  "ignore": [
    "**/node_modules/**",
    "**/dist/**",
    "**/*.test.ts",
    "**/*.test.tsx"
  ],
  "format": ["typescript", "javascript", "jsx", "tsx"],
  "minLines": 5,
  "minTokens": 50
}
```

#### Find Unused Exports
```bash
# Using ts-prune
npx ts-prune --error

# Using depcheck for unused dependencies
npx depcheck
```

#### Analyze Bundle Size
```bash
# Using webpack-bundle-analyzer
npm run build -- --analyze

# Using source-map-explorer
npx source-map-explorer 'dist/**/*.js'
```

### Complexity Analysis

#### Cyclomatic Complexity
```bash
# Using complexity-report
npx complexity-report src/ --format json -o complexity.json
```

```typescript
// analyze-complexity.ts
import { ESLint } from 'eslint'

async function analyzeComplexity() {
  const eslint = new ESLint({
    overrideConfig: {
      rules: {
        'complexity': ['error', { max: 10 }],
        'max-lines-per-function': ['error', { max: 50 }],
        'max-depth': ['error', { max: 4 }],
        'max-params': ['error', { max: 4 }],
      },
    },
  })

  const results = await eslint.lintFiles(['src/**/*.{ts,tsx}'])
  const highComplexity = results
    .filter(r => r.messages.some(m => m.ruleId === 'complexity'))

  return highComplexity
}
```

### Dependency Analysis

#### Security Audit
```bash
# npm audit
npm audit --json > audit-report.json

# Fix automatically
npm audit fix

# Snyk security scan
npx snyk test

# Check for vulnerabilities with detailed report
npm audit --audit-level=moderate
```

#### Unused Dependencies
```bash
# depcheck
npx depcheck --json > unused-deps.json

# unimported - find unused files
npx unimported

# List globally installed but unused
npm list -g --depth=0
```

#### Outdated Packages
```bash
# Check outdated packages
npm outdated

# Interactive update
npx npm-check-updates -i

# Update all to latest
npx npm-check-updates -u && npm install
```

#### Analyze Import Costs
```typescript
// Using import-cost analysis
// Shows package sizes in IDE

// Check bundle impact
import { visualizer } from 'rollup-plugin-visualizer'

// In rollup/vite config
plugins: [
  visualizer({
    filename: './dist/stats.html',
    open: true,
    gzipSize: true,
    brotliSize: true,
  }),
]
```

### Performance Analysis

#### React Performance
```typescript
// find-render-issues.ts
import { readFileSync } from 'fs'
import { glob } from 'glob'

interface RenderIssue {
  file: string
  issue: string
  line: number
}

function findRenderIssues(): RenderIssue[] {
  const issues: RenderIssue[] = []
  const files = glob.sync('src/**/*.{tsx,jsx}')

  for (const file of files) {
    const content = readFileSync(file, 'utf-8')
    const lines = content.split('\n')

    lines.forEach((line, idx) => {
      // Find inline function declarations in JSX
      if (/={.*=>/.test(line)) {
        issues.push({
          file,
          issue: 'Inline function in JSX (causes re-render)',
          line: idx + 1,
        })
      }

      // Find missing dependencies in useEffect
      if (line.includes('useEffect')) {
        const nextLines = lines.slice(idx, idx + 10).join('\n')
        if (!/\[.*\]/.test(nextLines)) {
          issues.push({
            file,
            issue: 'useEffect without dependency array',
            line: idx + 1,
          })
        }
      }

      // Find missing React.memo
      if (/export (const|function) [A-Z]/.test(line)) {
        const hasProps = content.includes('Props')
        const hasMemo = content.includes('React.memo') || content.includes('memo(')

        if (hasProps && !hasMemo && content.split('\n').length > 50) {
          issues.push({
            file,
            issue: 'Large component without React.memo',
            line: idx + 1,
          })
        }
      }
    })
  }

  return issues
}
```

#### Bundle Analysis Report
```typescript
// generate-bundle-report.ts
import { exec } from 'child_process'
import { promisify } from 'util'

const execAsync = promisify(exec)

async function analyzeBundleSize() {
  // Build project
  await execAsync('npm run build')

  // Analyze with source-map-explorer
  const { stdout } = await execAsync(
    'npx source-map-explorer dist/**/*.js --json'
  )

  const analysis = JSON.parse(stdout)

  // Find largest dependencies
  const dependencies = Object.entries(analysis.files)
    .map(([name, size]) => ({ name, size: size as number }))
    .sort((a, b) => b.size - a.size)
    .slice(0, 20)

  console.table(dependencies)

  // Generate recommendations
  const recommendations = []
  for (const dep of dependencies) {
    if (dep.size > 100000) {
      recommendations.push({
        dependency: dep.name,
        size: (dep.size / 1024).toFixed(2) + ' KB',
        suggestion: 'Consider code splitting or finding lighter alternative',
      })
    }
  }

  return { dependencies, recommendations }
}
```

## Analysis Reports

### Comprehensive Health Report
```typescript
// health-report.ts
import { exec } from 'child_process'
import { promisify } from 'util'
import { readFileSync } from 'fs'
import { glob } from 'glob'

const execAsync = promisify(exec)

interface HealthReport {
  overview: {
    totalFiles: number
    totalLines: number
    components: number
    tests: number
    coverage: number
  }
  quality: {
    typeErrors: number
    lintErrors: number
    complexity: number
    duplication: number
  }
  dependencies: {
    total: number
    outdated: number
    vulnerable: number
    unused: number
  }
  performance: {
    bundleSize: number
    renderIssues: number
    memoryLeaks: number
  }
  recommendations: Array<{
    category: string
    priority: 'high' | 'medium' | 'low'
    issue: string
    solution: string
  }>
}

async function generateHealthReport(): Promise<HealthReport> {
  // Count files and lines
  const files = glob.sync('src/**/*.{ts,tsx,js,jsx}')
  const totalFiles = files.length
  const totalLines = files.reduce((acc, file) => {
    return acc + readFileSync(file, 'utf-8').split('\n').length
  }, 0)

  // Count components and tests
  const components = glob.sync('src/**/*.{tsx,jsx}').filter(
    f => !f.includes('.test.') && !f.includes('.spec.')
  ).length
  const tests = glob.sync('src/**/*.{test,spec}.{ts,tsx,js,jsx}').length

  // Get test coverage
  const { stdout: coverageOutput } = await execAsync('npm test -- --coverage --silent')
  const coverageMatch = coverageOutput.match(/All files\s+\|\s+(\d+\.?\d*)/)
  const coverage = coverageMatch ? parseFloat(coverageMatch[1]) : 0

  // Type check
  const { stdout: tscOutput } = await execAsync('npx tsc --noEmit || true')
  const typeErrors = (tscOutput.match(/error TS\d+:/g) || []).length

  // Lint check
  const { stdout: eslintOutput } = await execAsync('npx eslint src/ --format json || true')
  const eslintResults = JSON.parse(eslintOutput || '[]')
  const lintErrors = eslintResults.reduce(
    (acc: number, r: any) => acc + r.errorCount,
    0
  )

  // Dependency audit
  const { stdout: auditOutput } = await execAsync('npm audit --json || true')
  const audit = JSON.parse(auditOutput || '{}')
  const vulnerable = audit.metadata?.vulnerabilities?.total || 0

  // Outdated packages
  const { stdout: outdatedOutput } = await execAsync('npm outdated --json || true')
  const outdated = Object.keys(JSON.parse(outdatedOutput || '{}')).length

  // Unused dependencies
  const { stdout: depcheckOutput } = await execAsync('npx depcheck --json')
  const depcheck = JSON.parse(depcheckOutput || '{}')
  const unused = depcheck.dependencies?.length || 0

  // Bundle size
  await execAsync('npm run build')
  const { stdout: sizeOutput } = await execAsync('du -sk dist')
  const bundleSize = parseInt(sizeOutput.split('\t')[0])

  // Generate recommendations
  const recommendations = []

  if (coverage < 80) {
    recommendations.push({
      category: 'Testing',
      priority: 'high' as const,
      issue: `Test coverage is ${coverage}% (target: 80%+)`,
      solution: 'Add unit tests for untested components and utilities',
    })
  }

  if (typeErrors > 0) {
    recommendations.push({
      category: 'Type Safety',
      priority: 'high' as const,
      issue: `${typeErrors} TypeScript errors found`,
      solution: 'Fix TypeScript errors to ensure type safety',
    })
  }

  if (vulnerable > 0) {
    recommendations.push({
      category: 'Security',
      priority: 'high' as const,
      issue: `${vulnerable} security vulnerabilities found`,
      solution: 'Run npm audit fix and update vulnerable dependencies',
    })
  }

  if (unused > 0) {
    recommendations.push({
      category: 'Dependencies',
      priority: 'medium' as const,
      issue: `${unused} unused dependencies`,
      solution: 'Remove unused dependencies to reduce bundle size',
    })
  }

  if (bundleSize > 500) {
    recommendations.push({
      category: 'Performance',
      priority: 'medium' as const,
      issue: `Bundle size is ${bundleSize}KB (target: <500KB)`,
      solution: 'Implement code splitting and tree-shaking optimizations',
    })
  }

  return {
    overview: {
      totalFiles,
      totalLines,
      components,
      tests,
      coverage,
    },
    quality: {
      typeErrors,
      lintErrors,
      complexity: 0, // Would need complexity analysis
      duplication: 0, // Would need duplication analysis
    },
    dependencies: {
      total: Object.keys(
        JSON.parse(readFileSync('package.json', 'utf-8')).dependencies || {}
      ).length,
      outdated,
      vulnerable,
      unused,
    },
    performance: {
      bundleSize,
      renderIssues: 0, // Would need render analysis
      memoryLeaks: 0, // Would need profiling
    },
    recommendations,
  }
}

// Generate and display report
generateHealthReport().then(report => {
  console.log('\n📊 CODEBASE HEALTH REPORT\n')
  console.log('Overview:')
  console.table(report.overview)
  console.log('\nQuality:')
  console.table(report.quality)
  console.log('\nDependencies:')
  console.table(report.dependencies)
  console.log('\nPerformance:')
  console.table(report.performance)
  console.log('\n💡 Recommendations:')
  console.table(report.recommendations)
})
```

## Best Practices for Analysis

### 1. Regular Analysis
- Run analysis weekly or per sprint
- Integrate into CI/CD pipeline
- Track metrics over time
- Set quality gates

### 2. Prioritize Findings
- **High**: Security, critical bugs, major performance issues
- **Medium**: Code quality, maintainability, moderate optimizations
- **Low**: Style issues, minor refactoring, nice-to-haves

### 3. Actionable Recommendations
- Provide specific solutions
- Include code examples
- Estimate effort required
- Link to documentation

### 4. Continuous Improvement
- Track progress on metrics
- Celebrate improvements
- Learn from regressions
- Update standards

## Tools & Commands

### Static Analysis
```bash
# TypeScript type checking
npx tsc --noEmit

# ESLint
npx eslint src/ --ext .ts,.tsx

# Complexity analysis
npx complexity-report src/

# Code duplication
npx jscpd src/
```

### Dependency Analysis
```bash
# Security audit
npm audit
npx snyk test

# Unused dependencies
npx depcheck

# Outdated packages
npm outdated
npx npm-check-updates

# License check
npx license-checker
```

### Performance Analysis
```bash
# Bundle analysis
npx webpack-bundle-analyzer dist/stats.json

# Source map explorer
npx source-map-explorer dist/**/*.js

# Performance profiling
npm run build -- --profile
```

### Code Quality
```bash
# Coverage
npm test -- --coverage

# Mutation testing
npx stryker run

# Code quality metrics
npx plato -r -d report src/
```

## Anti-Patterns to Detect

### React Anti-Patterns
1. **Prop Drilling**: Passing props through many levels
2. **God Components**: Components doing too much
3. **Inline Functions**: Creating new functions on every render
4. **Missing Keys**: Lists without proper key props
5. **Index as Key**: Using array index as key
6. **Direct State Mutation**: Mutating state directly
7. **Missing Dependencies**: useEffect without proper deps
8. **Unnecessary Re-renders**: Components re-rendering too often

### General Anti-Patterns
1. **Magic Numbers**: Hard-coded values without explanation
2. **Copy-Paste Code**: Duplicated code blocks
3. **Long Functions**: Functions over 50 lines
4. **Deep Nesting**: More than 4 levels of nesting
5. **Too Many Parameters**: Functions with 5+ parameters
6. **God Objects**: Classes/objects doing everything
7. **Tight Coupling**: High dependencies between modules
8. **Missing Error Handling**: No try-catch or error boundaries

## When to Use This Skill

Activate this skill when you need to:
- Analyze codebase quality
- Find performance bottlenecks
- Detect code duplication
- Audit dependencies
- Review architectural patterns
- Identify technical debt
- Assess code complexity
- Find security vulnerabilities
- Optimize bundle size
- Review code before release
- Onboard to new codebase
- Prepare for refactoring

## Output Format

When analyzing codebases, provide:
1. **Executive Summary**: Key findings and metrics
2. **Detailed Analysis**: In-depth findings by category
3. **Metrics Dashboard**: Visual representation of health
4. **Recommendations**: Prioritized action items
5. **Code Examples**: Before/after refactoring suggestions
6. **Implementation Plan**: Steps to address issues

Always provide actionable, specific recommendations with clear priorities and estimated effort.
