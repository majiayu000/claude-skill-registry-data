---
name: begin-session
version: 1.0.0
description: Start development session with diagnostics, context loading, and intelligent task menu
tags: [workflow, session, diagnostics, planning]
inputs: ./input.schema.json
outputs: ./output.schema.json
allowedPaths:
  read:
    - "./**"
    - "docs/**"
    - ".git/**"
  write:
    - "logs/**"
    - ".skillkit/**"
allowedCommands:
  - git
steps:
  - Load session context from tracking docs and git
  - Run diagnostics using framework adapter
  - Analyze codebase state
  - Present intelligent task menu
  - Return recommendations based on diagnostic data
retries: 0
dryRunSupported: true
dependencies: []
---

# BEGIN SESSION - Development Session Entry Point

**Purpose:** Single command to start any development session with full context and intelligent recommendations.

## What This Workflow Does

1. **Loads Context** (60s)
   - Read today's AI tracking documents
   - Check sprint status
   - Review recent git commits
   - Find unfinished work

2. **Runs Diagnostics** (2min)
   - Lint errors (via framework adapter)
   - Type errors (via framework adapter)
   - TODO/FIXME/HACK count (via framework adapter)
   - Circular dependencies (via framework adapter)
   - Build status (via framework adapter)

3. **Analyzes State** (30s)
   - Identify problem areas
   - Find incomplete features
   - Check for security issues

4. **Presents Task Menu**
   - Data-driven task recommendations
   - Clear options with priorities
   - Contextual suggestions

5. **Routes to Workflow**
   - Based on user choice
   - Passes diagnostic context to next workflow

---

## Input Schema

```json
{
  "projectRoot": "path/to/project",
  "trackingDocs": ["docs/AITracking/**", "docs/SprintStatus/**"],
  "userPreferences": {
    "showGitLog": true,
    "showDiagnostics": true,
    "autoRecommend": true
  }
}
```

---

## Output Schema

```json
{
  "diagnostics": {
    "lintErrors": 0,
    "typeErrors": 0,
    "todoCount": 0,
    "circularDeps": 0,
    "buildStatus": "pass|fail"
  },
  "context": {
    "todaysWork": ["list of files"],
    "recentCommits": ["commit messages"],
    "unfinishedWork": ["incomplete items"]
  },
  "recommendations": [
    {
      "task": "implement-feature",
      "priority": "high",
      "reason": "Low error count, ready for development"
    }
  ],
  "menu": {
    "development": [...],
    "fixing": [...],
    "quality": [...],
    "planning": [...]
  }
}
```

---

## Execution Steps (Framework-Agnostic)

### Step 1: Load Context

**Read tracking documents:**
```typescript
// Get today's date
const today = new Date().toLocaleDateString('en-GB').replace(/\//g, '-'); // DD-MM-YYYY

// Read AI tracking
const trackingFiles = await glob(`docs/AITracking/AIAction_${today}_*.md`);
const todaysWork = await Promise.all(trackingFiles.map(f => readFile(f)));

// Read sprint status
const sprintStatus = await readFile(`docs/SprintStatus/Sprint Status-${today}.md`);

// Get recent git commits
const recentCommits = await git.log({ since: '8 hours ago', maxCount: 10 });

// Find unfinished work
const auditFiles = await glob(`docs/audit/**/*${today}*`);
```

### Step 2: Run Diagnostics (Using Framework Adapter)

**Detect project type and run appropriate commands:**
```typescript
// Detect framework adapter
const adapter = await adapterRegistry.detect(projectRoot);
if (!adapter) {
  throw new Error('No framework adapter detected');
}

// Run diagnostics via adapter
const lintResult = await adapter.lint();
const typeCheckResult = await adapter.typeCheck();
const buildResult = await adapter.build();

// Find TODOs via adapter
const todos = await adapter.findTodos();

// Find circular dependencies (if supported)
const circularDeps = adapter.findCircularDeps 
  ? await adapter.findCircularDeps()
  : [];

// Compile diagnostics
const diagnostics = {
  lintErrors: countErrors(lintResult.stderr),
  typeErrors: countErrors(typeCheckResult.stderr),
  todoCount: todos.length,
  circularDeps: circularDeps.length,
  buildStatus: buildResult.success ? 'pass' : 'fail'
};
```

### Step 3: Analyze State

**Identify problem areas:**
```typescript
// Parse errors to find problem files
const problemAreas = analyzeDiagnostics(diagnostics);

// Find incomplete features (files with TODO/INCOMPLETE)
const incompleteFeatures = todos.filter(t => 
  t.includes('TODO') || t.includes('INCOMPLETE') || t.includes('FIXME')
);

// Check for high-priority security issues (if auditing available)
const securityIssues = await checkSecurityIssues();
```

### Step 4: Present Task Menu

**Generate menu based on diagnostics:**
```typescript
const menu = {
  development: [
    {
      id: 1,
      name: 'Implement Feature',
      workflow: 'implement-feature',
      condition: diagnostics.lintErrors < 50,
      description: 'Start new feature or resume incomplete feature'
    },
    {
      id: 2,
      name: 'Resume Work',
      workflow: 'continue',
      condition: unfinishedWork.length > 0,
      description: 'Continue from where you left off'
    }
  ],
  fixing: [
    {
      id: 3,
      name: 'Fix Errors',
      workflow: 'fix-all',
      condition: diagnostics.lintErrors > 0 || diagnostics.typeErrors > 0,
      priority: diagnostics.lintErrors > 50 ? 'critical' : 'medium',
      description: `Fix ${diagnostics.lintErrors} lint + ${diagnostics.typeErrors} type errors`
    },
    {
      id: 4,
      name: 'Complete Features',
      workflow: 'feature-fix-strategy',
      condition: diagnostics.todoCount > 50,
      description: `Complete ${diagnostics.todoCount} incomplete items`
    },
    {
      id: 5,
      name: 'Process TODOs',
      workflow: 'todo-execution',
      condition: diagnostics.todoCount > 0,
      description: `Systematic resolution of ${diagnostics.todoCount} TODOs`
    }
  ],
  quality: [
    {
      id: 6,
      name: 'Final Check',
      workflow: 'final-check',
      condition: true,
      description: 'Pre-deployment quality gate'
    },
    {
      id: 7,
      name: 'System Audit',
      workflow: 'system-audit',
      condition: true,
      description: 'Full codebase architecture review'
    },
    {
      id: 8,
      name: 'Documentation Review',
      workflow: 'documentation-audit',
      condition: true,
      description: 'Check docs are up-to-date'
    },
    {
      id: 9,
      name: 'Security Review',
      workflow: 'security-audit',
      condition: true,
      description: 'Pre-deployment security check'
    }
  ],
  planning: [
    {
      id: 10,
      name: 'Sprint Planning',
      workflow: 'sprint-planning',
      condition: true,
      description: 'Analyze features, velocity, blockers'
    },
    {
      id: 11,
      name: 'Tech Debt Report',
      workflow: 'tech-debt-analysis',
      condition: true,
      description: 'Quarterly complexity and duplication analysis'
    }
  ]
};
```

### Step 5: Make Recommendations

**Data-driven suggestions:**
```typescript
const recommendations = [];

if (diagnostics.lintErrors > 100) {
  recommendations.push({
    task: 'fix-all',
    priority: 'critical',
    reason: `${diagnostics.lintErrors} lint errors - Must fix before continuing`
  });
} else if (diagnostics.lintErrors > 50) {
  recommendations.push({
    task: 'fix-all',
    priority: 'high',
    reason: `${diagnostics.lintErrors} lint errors - Should fix soon`
  });
} else if (diagnostics.typeErrors > 50) {
  recommendations.push({
    task: 'fix-all',
    priority: 'medium',
    reason: `${diagnostics.typeErrors} type errors need attention`
  });
} else if (diagnostics.todoCount > 100) {
  recommendations.push({
    task: 'todo-execution',
    priority: 'medium',
    reason: `${diagnostics.todoCount} TODOs need resolution`
  });
} else if (diagnostics.buildStatus === 'fail') {
  recommendations.push({
    task: 'fix-all',
    priority: 'critical',
    reason: 'Build is broken - Must fix immediately'
  });
} else {
  recommendations.push({
    task: 'implement-feature',
    priority: 'normal',
    reason: 'Low error count - Ready for new development'
  });
}

return {
  diagnostics,
  context,
  menu,
  recommendations
};
```

---

## Usage

### From CLI:
```bash
# Run begin-session workflow
tsk run begin-session

# With specific project root
tsk run begin-session --input '{"projectRoot": "./my-project"}'

# Dry run (see what it would check)
tsk run begin-session --dry-run
```

### From Code:
```typescript
import { adapterRegistry, TypeScriptAdapter } from '@trinity-os/skillkit';

// Register adapter
const adapter = new TypeScriptAdapter(process.cwd());
adapterRegistry.register(adapter);

// Run workflow
const result = await runner.run('begin-session', {
  projectRoot: process.cwd(),
  trackingDocs: ['docs/AITracking/**', 'docs/SprintStatus/**'],
  userPreferences: {
    showGitLog: true,
    showDiagnostics: true,
    autoRecommend: true
  }
});

console.log(result.output.recommendations);
```

---

## Success Criteria

**Performance:**
- ✅ Context loading: < 60 seconds
- ✅ Diagnostics: < 2 minutes
- ✅ Total execution: < 5 minutes

**Output Quality:**
- ✅ Clear diagnostic summary
- ✅ Data-driven recommendations
- ✅ Actionable task menu
- ✅ Contextual priority suggestions

**User Experience:**
- ✅ Understand codebase state immediately
- ✅ Know what needs attention
- ✅ Choose task based on data
- ✅ Start work within 5 minutes

---

## Framework Compatibility

This workflow uses the **framework adapter system** and works with:

- ✅ **TypeScript/JavaScript** (npm, pnpm, yarn)
- ✅ **Python** (pip, poetry, pipenv)
- ✅ **Java** (maven, gradle)
- ✅ **Go** (go modules)
- ✅ **PHP** (composer)
- ✅ **Ruby** (bundler)
- ✅ **C#** (dotnet)

**Adapter auto-detection** ensures the right commands run for your project!

---

## Related Workflows

- `implement-feature` - Start new feature development
- `continue` - Resume previous work
- `fix-all` - Systematic error fixing
- `final-check` - Pre-deployment quality gate
- `system-audit` - Full codebase review

---

**Status:** ✅ Production Ready  
**Type:** Workflow (Orchestrator)  
**Execution Mode:** Hybrid (Native diagnostics + Instructional menu)  
**Last Updated:** November 5, 2025

