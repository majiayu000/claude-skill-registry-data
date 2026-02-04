---
name: dependency-analysis
description: Enhanced dependency analyzer with comprehensive markdown reporting and actionable recommendations. Use when you need to optimize frontend project dependencies, detect security vulnerabilities, identify unused packages, find duplicate functionality, analyze dependency impact, generate cleanup scripts, or produce detailed Markdown reports. Supports JavaScript, TypeScript, Vue, React, Angular, and modern build tools with parallel processing and incremental analysis capabilities.
---

# Enhanced Dependency Analyzer

Comprehensive dependency analysis tool with visual reports, categorization, and actionable recommendations for optimizing frontend project dependencies.

## Quick Start

### Installation
```bash
npm install
```

### Basic Analysis
```bash
# Run enhanced analyzer with markdown report
node scripts/enhanced-analyzer.js /path/to/project

# Full analysis with all features
node scripts/enhanced-analyzer.js /path/to/project \
  --generateFixScript \
  --generateGraph \
  --checkPeerDependencies \
  --checkOutdated \
  --checkSecurity
```

### Advanced Options
```bash
# Parallel processing for large projects
node scripts/enhanced-analyzer.js /path/to/project --parallel

# Incremental analysis with cache
node scripts/enhanced-analyzer.js /path/to/project --incremental

# Analyze specific dependency scopes
node scripts/enhanced-analyzer.js /path/to/project --scope=dependencies

# Production-only analysis
node scripts/enhanced-analyzer.js /path/to/project --scope=dependencies --includeDev=false
```

## Enhanced Features

### 🔍 Advanced Detection
- **Unused Dependencies**: Smart detection with confidence scoring
- **Missing Dependencies**: Runtime error prevention
- **Phantom Dependencies**: Hidden dependency identification
- **Duplicate Functionality**: Redundant package detection
- **Version Conflicts**: Peer dependency resolution issues
- **Circular Dependencies**: Import cycle detection with impact analysis

### 📊 Analysis Reports
- **Markdown Reports**: Comprehensive, readable analysis reports
- **Dependency Graphs**: Visual dependency relationship mapping
- **Category Breakdowns**: Frontend, backend, devtools, testing, build tools
- **Health Scoring**: Overall dependency quality metrics
- **Trend Analysis**: Historical dependency changes

### 🚀 Performance Features
- **Parallel Processing**: Faster analysis for large projects
- **Incremental Analysis**: Cache-based repeat analysis
- **Smart Exclusions**: Intelligent file/directory filtering
- **Batch Operations**: Efficient batch dependency checks

### 🛠️ Automation Tools
- **Auto-fix Scripts**: Generated shell scripts for cleanup
- **CI/CD Integration**: TeamCity, GitHub Actions reports
- **Multiple Formats**: JSON, CSV, Markdown outputs
- **Priority Recommendations**: Actionable improvement suggestions

## Output Formats

### Enhanced JSON Output
```json
{
  "success": true,
  "timestamp": "2024-01-15T10:30:00Z",
  "project": {
    "name": "my-project",
    "version": "1.0.0",
    "path": "/path/to/project"
  },
  "summary": {
    "total": 150,
    "unused": 5,
    "missing": 2,
    "phantom": 3,
    "outdated": 10,
    "vulnerable": 1,
    "peerConflicts": 2,
    "circular": 1,
    "duplicate": 3,
    "versionConflicts": 2
  },
  "categories": {
    "frontend": { "count": 45, "size": "2.3MB", "packages": [] },
    "backend": { "count": 12, "size": "1.1MB", "packages": [] },
    "devtools": { "count": 28, "size": "890KB", "packages": [] },
    "testing": { "count": 15, "size": "450KB", "packages": [] },
    "build": { "count": 20, "size": "670KB", "packages": [] },
    "other": { "count": 30, "size": "1.2MB", "packages": [] }
  },
  "recommendations": {
    "high": [],
    "medium": [],
    "low": []
  },
  "healthScore": 78,
  "markdownReport": "/path/to/DEPENDENCY_ANALYSIS_REPORT.md",
  "fixScript": "/path/to/FIX_DEPENDENCIES.sh"
}
```

### Markdown Report Features
- Comprehensive analysis summary
- Dependency category breakdowns
- Priority-based recommendations
- Quick fix commands
- Security vulnerability details
- Easy integration with documentation tools

## Command Line Interface

```bash
# Enhanced analyzer options
node scripts/enhanced-analyzer.js <project-path> [options]

Options:
  --generateFixScript Generate auto-fix shell script
  --generateGraph     Generate dependency graph data
  --parallel          Use parallel processing for speed
  --incremental       Use cache for faster repeat analysis
  --checkPeerDependencies  Analyze peer dependency conflicts
  --checkOutdated     Check for outdated packages
  --checkSecurity     Scan for security vulnerabilities
  --scope=<type>      Dependency scope: all|dependencies|devDependencies|peerDependencies
  --includeDev        Include devDependencies in analysis
  --cacheDir=<path>   Cache directory for incremental analysis
  --pretty            Pretty-print JSON output
```

## Report Generation

### Generate Multiple Report Formats
```bash
# Generate all report formats from analysis results
node scripts/generate-report.js analysis-result.json ./reports

# Available formats:
# - Markdown report (DEPENDENCY_ANALYSIS_REPORT.md)
# - JSON summary (DEPENDENCY_ANALYSIS_SUMMARY.json)
# - CSV issues (DEPENDENCY_ANALYSIS_ISSUES.csv)
# - TeamCity report (TEAMCITY_REPORT.txt)
# - GitHub Actions report (GITHUB_ACTIONS_REPORT.json)
```

## Integration Examples

### GitHub Actions Workflow
```yaml
- name: Analyze Dependencies
  run: |
    node scripts/enhanced-analyzer.js . \
      --generateFixScript \
      --checkSecurity \
      --checkOutdated

- name: Upload Analysis Report
  uses: actions/upload-artifact@v3
  with:
    name: dependency-analysis
    path: DEPENDENCY_ANALYSIS_REPORT.md
```

### TeamCity Integration
```bash
# Generate TeamCity-compatible report
node scripts/enhanced-analyzer.js . --checkSecurity
# TeamCity report automatically includes build statistics and problems
```

## Advanced Usage Patterns

### Custom Configuration
```javascript
const analyzer = new EnhancedDependencyAnalyzer('/path/to/project', {
  parallel: true,
  incremental: true,
  generateFixScript: true,
  checkSecurity: true,
  maxDepth: 10,
  cacheDir: '.dependency-cache',
  excludePatterns: ['docs/**', 'examples/**']
});

const result = await analyzer.analyze();
```

### Batch Project Analysis
```bash
# Analyze multiple projects
for project in project1 project2 project3; do
  node scripts/enhanced-analyzer.js $project \
    --generateFixScript
done
```

## Framework Support

The enhanced analyzer provides deep support for:
- **React**: Hooks, components, lazy loading
- **Vue**: SFC, script setup, async components
- **Angular**: Modules, services, lazy routes
- **Next.js**: Dynamic imports, API routes
- **Nuxt.js**: Auto-imports, composables
- **Svelte**: Components, stores
- **Build Tools**: Webpack, Vite, Rollup, esbuild

## Performance Optimization

- **Parallel Analysis**: Processes files concurrently for large projects
- **Smart Caching**: Incremental analysis avoids re-scanning unchanged files
- **Batch Operations**: Groups npm commands for efficiency
- **Memory Efficient**: Streaming analysis for large codebases
- **Progress Tracking**: Real-time analysis progress

## Reference Documentation

- **Implementation**: See [enhanced-analyzer.js](scripts/enhanced-analyzer.js)
- **Report Generation**: See [generate-report.js](scripts/generate-report.js)
- **Import Patterns**: See [references/import-patterns.md](references/import-patterns.md)
- **Peer Dependencies**: See [references/peer-dependency-analysis.md](references/peer-dependency-analysis.md)
- **Deep Analysis**: See [references/deep-dependency-patterns.md](references/deep-dependency-patterns.md)
- **Output Formats**: See [references/output-formats.md](references/output-formats.md)
