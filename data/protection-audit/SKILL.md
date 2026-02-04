---
name: protection-audit
description: Audit protected files, generate protection reports, and verify protection consistency. Use for protection system maintenance and compliance.
---

# Protection Audit Skill

## What This Skill Does

Comprehensive auditing of code protection system:
- Scans codebase for @protected/@immutable/@maintainable annotations
- Generates protection reports (by level, by file, by date)
- Verifies consistency (annotations match CODE_PROTECTION_POLICY.md)
- Identifies unprotected passing features
- Tracks protection coverage over time
- Validates audit trail in git log

## When Claude Should Use This

Use this skill when the user:
- Says "audit protection" or "check protected files"
- Wants protection status report
- Mentions "protection coverage" or "what's protected"
- Needs to verify CODE_PROTECTION_POLICY.md accuracy
- References protection compliance or maintenance
- Asks "which files are protected?"

## Workflow Process

### 1. Scan Codebase for Protection Annotations

**Create audit script: `scripts/audit-protection.js`**

```javascript
#!/usr/bin/env node

/**
 * Protection Audit Script
 *
 * Scans codebase for protection annotations and generates reports.
 *
 * Usage:
 *   node scripts/audit-protection.js [--report=summary|detailed|json]
 *   node scripts/audit-protection.js --verify  # Verify consistency
 *   node scripts/audit-protection.js --coverage  # Show coverage metrics
 *
 * Reports:
 *   - summary: Count by protection level
 *   - detailed: Full list with details
 *   - json: Machine-readable output
 *   - verify: Check CODE_PROTECTION_POLICY.md consistency
 *   - coverage: Protection coverage over time
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// Protection annotation patterns
const PROTECTION_REGEX = {
  immutable: /@immutable\s+Locked:\s*(\d{4}-\d{2}-\d{2})[^\n]*\n.*?Test:\s*([^\n]+)/s,
  protected: /@protected\s+Locked:\s*(\d{4}-\d{2}-\d{2})[^\n]*\n.*?Test:\s*([^\n]+)/s,
  maintainable: /@maintainable\s+Locked:\s*(\d{4}-\d{2}-\d{2})[^\n]*\n.*?Test:\s*([^\n]+)/s
};

// Files/directories to exclude from scan
const EXCLUDE_PATTERNS = [
  'node_modules/',
  '.git/',
  'out/',
  'dist/',
  'build/',
  'coverage/',
  '.vscode-test/',
  '.vscode-test-user-data/',
  '*.test.ts',
  '*.spec.ts'
];

/**
 * Check if file should be excluded
 */
function shouldExclude(filePath) {
  return EXCLUDE_PATTERNS.some(pattern => filePath.includes(pattern));
}

/**
 * Recursively find all TypeScript/JavaScript files
 */
function findSourceFiles(dir, fileList = []) {
  const files = fs.readdirSync(dir);

  files.forEach(file => {
    const filePath = path.join(dir, file);

    if (shouldExclude(filePath)) {
      return;
    }

    const stat = fs.statSync(filePath);

    if (stat.isDirectory()) {
      findSourceFiles(filePath, fileList);
    } else if (file.match(/\.(ts|js|tsx|jsx)$/)) {
      fileList.push(filePath);
    }
  });

  return fileList;
}

/**
 * Extract protection annotations from file
 */
function extractProtectionAnnotations(filePath) {
  try {
    const content = fs.readFileSync(filePath, 'utf-8');
    const annotations = [];

    // Check each protection level
    for (const [level, regex] of Object.entries(PROTECTION_REGEX)) {
      const matches = content.matchAll(new RegExp(regex, 'gs'));

      for (const match of matches) {
        const lockDate = match[1];
        const testRef = match[2].trim();

        // Extract function/class name (simplified - looks for export/function/class before annotation)
        const lines = content.substring(0, match.index).split('\n');
        const contextLines = lines.slice(-10).join('\n');
        const nameMatch = contextLines.match(/(?:export\s+)?(?:async\s+)?(?:function|class)\s+(\w+)/);
        const name = nameMatch ? nameMatch[1] : 'Unknown';

        annotations.push({
          file: filePath.replace(/\\/g, '/'),
          level,
          name,
          lockDate,
          testRef,
          lineNumber: content.substring(0, match.index).split('\n').length
        });
      }
    }

    return annotations;
  } catch (error) {
    console.error(`Error reading ${filePath}:`, error.message);
    return [];
  }
}

/**
 * Generate summary report
 */
function generateSummaryReport(annotations) {
  const summary = {
    immutable: 0,
    protected: 0,
    maintainable: 0,
    total: 0
  };

  annotations.forEach(ann => {
    summary[ann.level]++;
    summary.total++;
  });

  console.log('╔═══════════════════════════════════════╗');
  console.log('║   Code Protection Audit - Summary    ║');
  console.log('╚═══════════════════════════════════════╝\n');

  console.log(`📊 Protection Levels:`);
  console.log(`   @immutable   : ${summary.immutable.toString().padStart(3)} files (never change)`);
  console.log(`   @protected   : ${summary.protected.toString().padStart(3)} files (refactor only)`);
  console.log(`   @maintainable: ${summary.maintainable.toString().padStart(3)} files (bug fixes allowed)`);
  console.log(`   ─────────────────────────────────────`);
  console.log(`   Total        : ${summary.total.toString().padStart(3)} protected items\n`);

  // Group by lock date
  const byDate = {};
  annotations.forEach(ann => {
    byDate[ann.lockDate] = (byDate[ann.lockDate] || 0) + 1;
  });

  console.log(`📅 Protection by Date:`);
  Object.entries(byDate)
    .sort()
    .forEach(([date, count]) => {
      console.log(`   ${date}: ${count} items`);
    });
  console.log('');

  // Most protected files
  const fileCount = {};
  annotations.forEach(ann => {
    const shortPath = ann.file.replace(/^.*\/vscode-lumina\/src\//, '');
    fileCount[shortPath] = (fileCount[shortPath] || 0) + 1;
  });

  console.log(`📁 Most Protected Files:`);
  Object.entries(fileCount)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 5)
    .forEach(([file, count]) => {
      console.log(`   ${count}x ${file}`);
    });
  console.log('');
}

/**
 * Generate detailed report
 */
function generateDetailedReport(annotations) {
  console.log('╔═══════════════════════════════════════╗');
  console.log('║   Code Protection Audit - Detailed   ║');
  console.log('╚═══════════════════════════════════════╝\n');

  const grouped = {
    immutable: [],
    protected: [],
    maintainable: []
  };

  annotations.forEach(ann => grouped[ann.level].push(ann));

  // Print each protection level
  for (const [level, items] of Object.entries(grouped)) {
    if (items.length === 0) continue;

    console.log(`\n${'='.repeat(60)}`);
    console.log(`@${level.toUpperCase()} (${items.length} items)`);
    console.log('='.repeat(60));

    items.forEach(ann => {
      const shortPath = ann.file.replace(/^.*\/vscode-lumina\/src\//, '');
      console.log(`\n📄 ${shortPath}:${ann.lineNumber}`);
      console.log(`   Function/Class: ${ann.name}`);
      console.log(`   Lock Date: ${ann.lockDate}`);
      console.log(`   Test: ${ann.testRef}`);
    });
  }

  console.log('\n');
}

/**
 * Generate JSON report (machine-readable)
 */
function generateJsonReport(annotations) {
  const report = {
    timestamp: new Date().toISOString(),
    summary: {
      immutable: annotations.filter(a => a.level === 'immutable').length,
      protected: annotations.filter(a => a.level === 'protected').length,
      maintainable: annotations.filter(a => a.level === 'maintainable').length,
      total: annotations.length
    },
    annotations: annotations
  };

  console.log(JSON.stringify(report, null, 2));
}

/**
 * Verify consistency with CODE_PROTECTION_POLICY.md
 */
function verifyConsistency(annotations) {
  console.log('╔═══════════════════════════════════════╗');
  console.log('║  Protection Consistency Verification ║');
  console.log('╚═══════════════════════════════════════╝\n');

  const policyFile = 'docs/CODE_PROTECTION_POLICY.md';

  if (!fs.existsSync(policyFile)) {
    console.log('❌ CODE_PROTECTION_POLICY.md not found');
    console.log('   Run PROTECT-003 to create protection policy document\n');
    return;
  }

  const policyContent = fs.readFileSync(policyFile, 'utf-8');

  // Extract file paths from policy document
  const policyFiles = new Set();
  const fileMatches = policyContent.matchAll(/\|\s*([^\|]+\.ts)\s*\|/g);
  for (const match of fileMatches) {
    policyFiles.add(match[1].trim());
  }

  console.log(`📋 Policy Document: ${policyFiles.size} files listed`);
  console.log(`🔍 Codebase Scan: ${annotations.length} annotations found\n`);

  // Files in policy but not in code
  const inPolicyNotCode = [...policyFiles].filter(policyFile => {
    return !annotations.some(ann => ann.file.includes(policyFile));
  });

  // Files in code but not in policy
  const inCodeNotPolicy = annotations.filter(ann => {
    const shortPath = ann.file.replace(/^.*\/vscode-lumina\/src\//, '');
    return ![...policyFiles].some(policyFile => policyFile.includes(shortPath));
  });

  // Report discrepancies
  if (inPolicyNotCode.length > 0) {
    console.log('⚠️  Files in policy but not in code:');
    inPolicyNotCode.forEach(file => {
      console.log(`   - ${file}`);
    });
    console.log('');
  }

  if (inCodeNotPolicy.length > 0) {
    console.log('⚠️  Files in code but not in policy:');
    inCodeNotPolicy.forEach(ann => {
      const shortPath = ann.file.replace(/^.*\/vscode-lumina\/src\//, '');
      console.log(`   - ${shortPath} (@${ann.level})`);
    });
    console.log('');
  }

  if (inPolicyNotCode.length === 0 && inCodeNotPolicy.length === 0) {
    console.log('✅ Policy and codebase are consistent\n');
  } else {
    console.log('❌ Inconsistencies found - update CODE_PROTECTION_POLICY.md\n');
  }
}

/**
 * Show protection coverage metrics
 */
function showCoverageMetrics(annotations) {
  console.log('╔═══════════════════════════════════════╗');
  console.log('║     Protection Coverage Metrics      ║');
  console.log('╚═══════════════════════════════════════╝\n');

  // Count total source files
  const allFiles = findSourceFiles('vscode-lumina/src');
  const protectedFileSet = new Set(annotations.map(a => a.file));

  const coverage = {
    totalFiles: allFiles.length,
    protectedFiles: protectedFileSet.size,
    percentage: ((protectedFileSet.size / allFiles.length) * 100).toFixed(1)
  };

  console.log(`📊 Coverage Statistics:`);
  console.log(`   Total source files  : ${coverage.totalFiles}`);
  console.log(`   Protected files     : ${coverage.protectedFiles}`);
  console.log(`   Coverage percentage : ${coverage.percentage}%\n`);

  // Protection over time (via git log)
  console.log(`📈 Protection Growth Over Time:`);
  try {
    const gitLog = execSync('git log --all --grep="@protected\\|@immutable\\|@maintainable" --pretty=format:"%as" --reverse', {
      encoding: 'utf-8'
    });

    const dates = gitLog.trim().split('\n');
    const byMonth = {};

    dates.forEach(date => {
      const month = date.substring(0, 7); // YYYY-MM
      byMonth[month] = (byMonth[month] || 0) + 1;
    });

    Object.entries(byMonth).forEach(([month, count]) => {
      console.log(`   ${month}: ${count} annotations`);
    });
  } catch (error) {
    console.log('   (git log data not available)');
  }

  console.log('');
}

/**
 * Main audit function
 */
function runAudit() {
  const args = process.argv.slice(2);
  const reportType = args.find(a => a.startsWith('--report='))?.split('=')[1] || 'summary';
  const verify = args.includes('--verify');
  const coverage = args.includes('--coverage');

  console.log('🔍 Scanning codebase for protection annotations...\n');

  // Find all source files
  const sourceFiles = findSourceFiles('vscode-lumina/src');
  console.log(`📁 Scanning ${sourceFiles.length} source files...\n`);

  // Extract annotations
  const annotations = [];
  sourceFiles.forEach(file => {
    const fileAnnotations = extractProtectionAnnotations(file);
    annotations.push(...fileAnnotations);
  });

  // Generate requested report
  if (verify) {
    verifyConsistency(annotations);
  } else if (coverage) {
    showCoverageMetrics(annotations);
  } else if (reportType === 'json') {
    generateJsonReport(annotations);
  } else if (reportType === 'detailed') {
    generateDetailedReport(annotations);
  } else {
    generateSummaryReport(annotations);
  }

  return 0;
}

// Run audit
const exitCode = runAudit();
process.exit(exitCode);
```

**Make script executable:**
```bash
chmod +x scripts/audit-protection.js
```

### 2. Generate Protection Reports

**Summary report (default):**
```bash
node scripts/audit-protection.js

# Output:
# ╔═══════════════════════════════════════╗
# ║   Code Protection Audit - Summary    ║
# ╚═══════════════════════════════════════╝
#
# 📊 Protection Levels:
#    @immutable   :   5 files (never change)
#    @protected   :  18 files (refactor only)
#    @maintainable:   3 files (bug fixes allowed)
#    ─────────────────────────────────────
#    Total        :  26 protected items
#
# 📅 Protection by Date:
#    2025-11-06: 20 items
#    2025-11-07: 6 items
#
# 📁 Most Protected Files:
#    3x extension.ts
#    2x SprintLoader.ts
#    2x voicePanel.ts
#    1x whisperClient.ts
#    1x AutoTerminalSelector.ts
```

**Detailed report:**
```bash
node scripts/audit-protection.js --report=detailed

# Output:
# ╔═══════════════════════════════════════╗
# ║   Code Protection Audit - Detailed   ║
# ╚═══════════════════════════════════════╝
#
# ============================================================
# @IMMUTABLE (5 items)
# ============================================================
#
# 📄 services/whisperClient.ts:23
#    Function/Class: WhisperClient
#    Lock Date: 2025-11-06
#    Test: MANUAL_TEST_v0.16.7.md - Test 1.4
#
# [... more items ...]
```

**JSON report (machine-readable):**
```bash
node scripts/audit-protection.js --report=json > protection-report.json

# Output: JSON file with full annotation details
```

### 3. Verify Consistency

**Check annotations match CODE_PROTECTION_POLICY.md:**
```bash
node scripts/audit-protection.js --verify

# Output:
# ╔═══════════════════════════════════════╗
# ║  Protection Consistency Verification ║
# ╚═══════════════════════════════════════╝
#
# 📋 Policy Document: 26 files listed
# 🔍 Codebase Scan: 26 annotations found
#
# ✅ Policy and codebase are consistent
```

**If inconsistencies found:**
```bash
node scripts/audit-protection.js --verify

# Output:
# ⚠️  Files in policy but not in code:
#    - vscode-lumina/src/services/deletedFile.ts
#
# ⚠️  Files in code but not in policy:
#    - commands/newFeature.ts (@protected)
#
# ❌ Inconsistencies found - update CODE_PROTECTION_POLICY.md
```

### 4. Track Protection Coverage

**Show coverage metrics over time:**
```bash
node scripts/audit-protection.js --coverage

# Output:
# ╔═══════════════════════════════════════╗
# ║     Protection Coverage Metrics      ║
# ╚═══════════════════════════════════════╝
#
# 📊 Coverage Statistics:
#    Total source files  : 85
#    Protected files     : 26
#    Coverage percentage : 30.6%
#
# 📈 Protection Growth Over Time:
#    2025-11: 20 annotations
#    2025-12: 6 annotations
```

### 5. Identify Unprotected Passing Features

**Find passing features without protection:**

```bash
# Create helper script: scripts/find-unprotected-features.js
node scripts/find-unprotected-features.js
```

**Script logic:**
1. Read MANUAL_TEST results (find all ✅ PASS tests)
2. Extract file paths from passing tests
3. Check if files have @protected annotations
4. Report unprotected passing features

**Example output:**
```
⚠️  Unprotected Passing Features:

1. Test 5.1: Sprint dropdown (PASS)
   File: vscode-lumina/src/webview/SprintDropdown.tsx
   Status: Passing but not protected
   Recommendation: Add @protected annotation

2. Test 5.2: Settings UI (PASS)
   File: vscode-lumina/src/webview/SettingsPanel.tsx
   Status: Passing but not protected
   Recommendation: Add @protected annotation

Action: Run 'protect' skill to annotate these features
```

### 6. Create Protection Dashboard

**Aggregate reports into dashboard:**

File: `docs/PROTECTION_DASHBOARD.md`

```markdown
# Code Protection Dashboard

**Last Updated:** 2025-11-06
**Report Generated:** node scripts/audit-protection.js

---

## Protection Summary

| Metric | Value |
|--------|-------|
| Total Source Files | 85 |
| Protected Files | 26 |
| Coverage | 30.6% |
| @immutable | 5 |
| @protected | 18 |
| @maintainable | 3 |

## Protection by Module

| Module | Protected | Total | Coverage |
|--------|-----------|-------|----------|
| Services | 8 | 15 | 53.3% |
| Commands | 6 | 12 | 50.0% |
| WebView | 4 | 20 | 20.0% |
| Utils | 2 | 18 | 11.1% |

## Recent Protection Activity

| Date | Files Protected | Protection Level |
|------|-----------------|------------------|
| 2025-11-06 | 20 | @protected, @immutable |
| 2025-11-07 | 6 | @protected |

## Unprotected Passing Features

⚠️ 4 passing features without protection:
- Sprint dropdown (Test 5.1)
- Settings UI (Test 5.2)
- Terminal selection (Test 3.4)
- Voice recording (Test 1.2)

**Action Required:** Run `protect` skill to annotate

## Consistency Status

✅ CODE_PROTECTION_POLICY.md matches codebase (0 discrepancies)

---

**Regenerate:** `node scripts/audit-protection.js > docs/PROTECTION_DASHBOARD.md`
```

### 7. Scheduled Audit Workflow

**Create weekly audit routine:**

```bash
#!/bin/bash
# File: scripts/weekly-protection-audit.sh

echo "📅 Weekly Protection Audit - $(date)"
echo ""

# 1. Generate summary report
echo "📊 Summary Report:"
node scripts/audit-protection.js
echo ""

# 2. Verify consistency
echo "🔍 Consistency Check:"
node scripts/audit-protection.js --verify
echo ""

# 3. Show coverage trends
echo "📈 Coverage Metrics:"
node scripts/audit-protection.js --coverage
echo ""

# 4. Generate JSON for tracking
node scripts/audit-protection.js --report=json > "protection-reports/audit-$(date +%Y-%m-%d).json"

echo "✅ Audit complete - report saved to protection-reports/"
```

**Run weekly:**
```bash
chmod +x scripts/weekly-protection-audit.sh
./scripts/weekly-protection-audit.sh
```

## Integration with Protection Tasks

**PROTECT-001 → PROTECT-002 → PROTECT-003 → Audit (This Skill)**

1. **PROTECT-001:** Annotate code with protection levels
2. **PROTECT-002:** Build pre-commit enforcement
3. **PROTECT-003:** Document CODE_PROTECTION_POLICY.md
4. **Audit (This Skill):** Verify, report, maintain protection system

**Use audit skill for:**
- Post-implementation verification (after PROTECT-001-003)
- Weekly maintenance checks
- Pre-release protection review
- Compliance reporting
- Identifying protection gaps

## Related Files

- `scripts/audit-protection.js` - Main audit script (created by this skill)
- `scripts/find-unprotected-features.js` - Find passing features without protection
- `scripts/weekly-protection-audit.sh` - Automated weekly audit
- `docs/PROTECTION_DASHBOARD.md` - Protection dashboard (generated)
- `docs/CODE_PROTECTION_POLICY.md` - Protection policy reference
- `protection-reports/` - Historical audit reports (JSON)

## Performance Target

**Audit must complete in < 5 seconds:**

```bash
time node scripts/audit-protection.js

# Expected:
# real    0m2.341s  (well under 5s target)
# user    0m2.156s
# sys     0m0.185s
```

**Optimization strategies:**
- Cache file list (don't re-scan directories)
- Use streaming for large files
- Parallel file scanning (if needed)
- Exit early if report type doesn't need full scan

## Error Handling

**Common issues and solutions:**

### Audit script finds no annotations
```bash
# Verify annotations exist in code
grep -r "@protected" vscode-lumina/src/
# Expected: Should find protected code

# Check audit script regex patterns
node scripts/audit-protection.js --report=detailed
# Review output for pattern matching issues
```

### Consistency check shows false positives
```bash
# Verify CODE_PROTECTION_POLICY.md format
cat docs/CODE_PROTECTION_POLICY.md
# Expected: Table format with file paths

# Check file path normalization
node scripts/audit-protection.js --verify --debug
```

### Coverage metrics incorrect
```bash
# Verify source file count
find vscode-lumina/src -name "*.ts" | wc -l
# Compare to audit report total

# Check exclusion patterns
node scripts/audit-protection.js --report=json | grep "node_modules"
# Expected: Should NOT find excluded files
```

## Historical Context

**Why protection auditing is critical:**

### Without auditing (before this skill):
- No visibility into protection coverage
- Inconsistencies between policy and code undetected
- Protected code could "drift" over time
- No tracking of protection growth

### With auditing (after this skill):
- Weekly reports show protection status
- Consistency automatically verified
- Coverage trends visible (↑ 30.6% protection)
- Unprotected passing features identified
- Compliance reporting automated

**Pattern:** Regular auditing maintains protection system health. What gets measured gets managed.

## Tips

**Start with summary report:**
1. Run: `node scripts/audit-protection.js`
2. Review protection counts
3. Check most protected files
4. Verify numbers match expectations

**Verify consistency weekly:**
- Run: `node scripts/audit-protection.js --verify`
- Fix any discrepancies immediately
- Update CODE_PROTECTION_POLICY.md as needed

**Track coverage trends:**
- Generate JSON reports weekly
- Store in `protection-reports/` directory
- Plot coverage over time (30.6% → 40% → 50%)
- Celebrate protection milestones

**Identify gaps proactively:**
- Run unprotected features check
- Cross-reference with test results
- Annotate newly passing features
- Keep protection current (not stale)

**Automate reporting:**
- Set up weekly cron job
- Generate dashboard automatically
- Share with team in standup
- Make protection visible
