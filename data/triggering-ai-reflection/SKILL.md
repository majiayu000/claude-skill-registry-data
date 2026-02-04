---
name: triggering-ai-reflection
description: Triggering and managing AI reflection cycles in StickerNest. Use when the user wants to run AI evaluation, trigger reflection, check AI quality, improve AI prompts, analyze AI performance, or audit AI generations. Covers reflection triggers, evaluation analysis, and improvement actions.
---

# Triggering AI Reflection in StickerNest

This skill covers how to trigger and manage AI reflection cycles - the process where AI evaluates its own outputs and suggests improvements.

## When to Use This Skill

This skill helps when you need to:
- Run an immediate reflection on recent AI generations
- Analyze why certain generations failed
- Force a prompt update based on evaluations
- Review and act on improvement suggestions
- Audit the AI's performance over time

## Quick Reference

### Trigger Reflection Immediately

```typescript
import { reflectOnWidgetGeneration, reflectOnImageGeneration } from '../ai/AIReflectionService';

// Reflect on widget generations
const result = await reflectOnWidgetGeneration({ forceRun: true });

// Reflect on image generations
const imageResult = await reflectOnImageGeneration({ forceRun: true });

// Check results
if (result.evaluation) {
  console.log(`Score: ${result.evaluation.overallScore}/5`);
  console.log(`Passed: ${result.evaluation.passed}`);
  console.log(`Suggestions: ${result.suggestions.length}`);
}
```

### Check Current Status

```typescript
import { useAIReflectionStore } from '../state/useAIReflectionStore';

const store = useAIReflectionStore.getState();

// Get statistics
const stats = store.getStats();
console.log(`Total evaluations: ${stats.totalEvaluations}`);
console.log(`Pass rate: ${stats.passRate}%`);
console.log(`Average score: ${stats.averageScore}`);

// Check if currently reflecting
const isReflecting = store.currentRunId !== null;

// Check cooldown
const inCooldown = store.isInCooldown();
```

## Step-by-Step Guide

### Step 1: Prepare for Reflection

Before triggering, ensure there's data to evaluate:

```typescript
import { useGenerationMetricsStore } from '../state/useGenerationMetricsStore';

const metricsStore = useGenerationMetricsStore.getState();

// Check unevaluated records
const unevaluated = metricsStore.getUnevaluatedRecords('widget');
console.log(`${unevaluated.length} widget generations to evaluate`);

// If no unevaluated, you can still force evaluation of recent records
// by using evaluateUnevaluatedOnly: false in config
```

### Step 2: Configure Evaluation Settings

Adjust settings before reflection if needed:

```typescript
import { useAIReflectionStore } from '../state/useAIReflectionStore';

const reflectionStore = useAIReflectionStore.getState();

// For a thorough analysis
reflectionStore.updateConfig({
  messagesToEvaluate: 50,      // Evaluate more records
  scoreThreshold: 3.0,         // Lower threshold (more likely to suggest changes)
  evaluateUnevaluatedOnly: false, // Include previously evaluated
});

// For quick check
reflectionStore.updateConfig({
  messagesToEvaluate: 10,
  evaluateUnevaluatedOnly: true,
});
```

### Step 3: Run Reflection

```typescript
import { getAIReflectionService } from '../ai/AIReflectionService';

const service = getAIReflectionService();

const result = await service.runReflection({
  targetType: 'widget_generation',
  forceRun: true,  // Bypass cooldown
  recordsToEvaluate: 30,  // Override config
});

// Handle result
if (result.skipped) {
  console.log(`Skipped: ${result.skipReason}`);
} else {
  console.log(`Run ID: ${result.runId}`);
  console.log(`Evaluation:`, result.evaluation);
  console.log(`Prompt changed: ${result.promptChanged}`);

  if (result.newVersionId) {
    console.log(`New prompt version: ${result.newVersionId}`);
  }
}
```

### Step 4: Review Results

Examine evaluation details:

```typescript
const reflectionStore = useAIReflectionStore.getState();

// Get latest evaluation
const latestEval = reflectionStore.getLatestEvaluation('widget_generation');

if (latestEval) {
  console.log('\n=== Evaluation Results ===');
  console.log(`Overall: ${latestEval.overallScore}/${latestEval.maxPossibleScore}`);
  console.log(`Threshold: ${latestEval.threshold}`);
  console.log(`Status: ${latestEval.passed ? 'PASSED' : 'FAILED'}`);

  console.log('\nScore Breakdown:');
  latestEval.scores.forEach(score => {
    console.log(`  ${score.criterionName}: ${score.score}/${score.maxScore}`);
    console.log(`    ${score.reasoning}`);
  });

  console.log('\nAnalysis:', latestEval.analysis);

  console.log('\nSuggested Changes:');
  latestEval.suggestedChanges.forEach(change => {
    console.log(`  - ${change}`);
  });
}
```

### Step 5: Act on Suggestions

Review and address improvement suggestions:

```typescript
const reflectionStore = useAIReflectionStore.getState();

// Get active suggestions
const suggestions = reflectionStore.getActiveSuggestions();

suggestions.forEach(suggestion => {
  console.log(`[${suggestion.severity.toUpperCase()}] ${suggestion.title}`);
  console.log(`  ${suggestion.description}`);
  console.log(`  Action: ${suggestion.proposedAction}`);

  // Mark as addressed after taking action
  if (actionTaken) {
    reflectionStore.markSuggestionAddressed(suggestion.id);
  }

  // Or hide if not relevant
  if (notRelevant) {
    reflectionStore.hideSuggestion(suggestion.id);
  }
});
```

### Step 6: Handle Prompt Proposals

Review pending prompt changes:

```typescript
import { usePromptVersionStore } from '../state/usePromptVersionStore';

const promptStore = usePromptVersionStore.getState();

// Get pending proposals
const proposals = promptStore.getPendingProposals('widget_generation');

proposals.forEach(proposal => {
  console.log(`Proposal: ${proposal.reason}`);
  console.log(`Evidence: ${proposal.evidence.join(', ')}`);
  console.log(`Proposed content preview:`, proposal.proposedContent.substring(0, 200));

  // Approve to create new version
  const newVersionId = promptStore.approveProposal(proposal.id);

  // Or reject
  // promptStore.rejectProposal(proposal.id);
});
```

## Code Examples

### Example: Full Reflection Cycle

```typescript
async function runFullReflectionCycle() {
  const reflectionStore = useAIReflectionStore.getState();
  const promptStore = usePromptVersionStore.getState();
  const metricsStore = useGenerationMetricsStore.getState();

  // 1. Check what we have to evaluate
  const widgetRecords = metricsStore.getUnevaluatedRecords('widget');
  const imageRecords = metricsStore.getUnevaluatedRecords('image');

  console.log(`Widget records: ${widgetRecords.length}`);
  console.log(`Image records: ${imageRecords.length}`);

  // 2. Run widget reflection if we have data
  if (widgetRecords.length >= 5) {
    const result = await reflectOnWidgetGeneration({ forceRun: true });

    if (result.evaluation && !result.evaluation.passed) {
      console.log('Widget generation needs improvement');

      // Check for pending proposals
      const proposals = promptStore.getPendingProposals('widget_generation');
      if (proposals.length > 0) {
        console.log(`${proposals.length} prompt proposals pending review`);
      }
    }
  }

  // 3. Run image reflection
  if (imageRecords.length >= 5) {
    await reflectOnImageGeneration({ forceRun: true });
  }

  // 4. Report findings
  const stats = reflectionStore.getStats();
  console.log('\n=== Reflection Complete ===');
  console.log(`Pass rate: ${stats.passRate.toFixed(1)}%`);
  console.log(`Active suggestions: ${stats.activeSuggestions}`);

  return stats;
}
```

### Example: Diagnostic Check

```typescript
function diagnoseAIPerformance() {
  const reflectionStore = useAIReflectionStore.getState();
  const metricsStore = useGenerationMetricsStore.getState();

  // Get recent evaluations
  const evaluations = reflectionStore.evaluations.slice(0, 10);

  // Calculate trends
  const recentPassRate = evaluations.filter(e => e.passed).length / evaluations.length;

  // Find common issues
  const allIssues: string[] = [];
  evaluations.forEach(e => {
    e.scores.filter(s => s.score <= 2).forEach(s => {
      allIssues.push(s.criterionName);
    });
  });

  const issueFrequency = allIssues.reduce((acc, issue) => {
    acc[issue] = (acc[issue] || 0) + 1;
    return acc;
  }, {} as Record<string, number>);

  console.log('=== AI Diagnostics ===');
  console.log(`Recent pass rate: ${(recentPassRate * 100).toFixed(0)}%`);
  console.log('\nProblem areas:');
  Object.entries(issueFrequency)
    .sort(([,a], [,b]) => b - a)
    .forEach(([issue, count]) => {
      console.log(`  ${issue}: ${count} occurrences`);
    });

  // Check generation success rates
  const widgetRate = metricsStore.getSuccessRate('widget', 50);
  const imageRate = metricsStore.getSuccessRate('image', 50);

  console.log('\nGeneration success rates:');
  console.log(`  Widgets: ${widgetRate.toFixed(0)}%`);
  console.log(`  Images: ${imageRate.toFixed(0)}%`);
}
```

### Example: Custom Evaluation

```typescript
import { getAIReflectionService, type RubricCriteria } from '../ai/AIReflectionService';

async function customEvaluation() {
  const service = getAIReflectionService();

  // Define custom rubric for special evaluation
  const strictRubric: RubricCriteria[] = [
    {
      name: 'Accuracy',
      description: 'Output exactly matches requirements',
      weight: 0.5,
      minScore: 1,
      maxScore: 5,
    },
    {
      name: 'Performance',
      description: 'Executes within acceptable time limits',
      weight: 0.3,
      minScore: 1,
      maxScore: 5,
    },
    {
      name: 'Standards',
      description: 'Follows all coding standards',
      weight: 0.2,
      minScore: 1,
      maxScore: 5,
    },
  ];

  const result = await service.runReflection({
    targetType: 'widget_generation',
    forceRun: true,
    customRubric: strictRubric,
  });

  return result;
}
```

## Common Patterns

### Pattern: Scheduled Reflection

Set up periodic reflection (typically done in app initialization):

```typescript
let reflectionInterval: NodeJS.Timeout;

function startReflectionSchedule() {
  const config = useAIReflectionStore.getState().config;

  if (!config.enabled) return;

  reflectionInterval = setInterval(async () => {
    await reflectOnWidgetGeneration();
    await reflectOnImageGeneration();
  }, config.intervalMinutes * 60 * 1000);
}

function stopReflectionSchedule() {
  clearInterval(reflectionInterval);
}
```

### Pattern: Reflection on Failure Spike

Trigger reflection when failures increase:

```typescript
function checkForFailureSpike() {
  const metricsStore = useGenerationMetricsStore.getState();

  const recent = metricsStore.getRecordsByType('widget', 10);
  const failures = recent.filter(r => r.result === 'failure').length;

  if (failures >= 3) {
    console.log('Failure spike detected, triggering reflection');
    reflectOnWidgetGeneration({ forceRun: true });
  }
}
```

### Pattern: Pre-deployment Check

Run reflection before deploying changes:

```typescript
async function preDeploymentCheck(): Promise<boolean> {
  const result = await reflectOnWidgetGeneration({
    forceRun: true,
    recordsToEvaluate: 100
  });

  if (!result.evaluation || !result.evaluation.passed) {
    console.error('Pre-deployment check failed');
    console.error('Score:', result.evaluation?.overallScore);
    return false;
  }

  console.log('Pre-deployment check passed');
  return true;
}
```

## Reference Files

| File | Purpose |
|------|---------|
| `src/ai/AIReflectionService.ts` | Core reflection logic |
| `src/state/useAIReflectionStore.ts` | Evaluation storage |
| `src/state/useGenerationMetricsStore.ts` | Generation tracking |
| `src/state/usePromptVersionStore.ts` | Prompt versioning |
| `src/components/ai-reflection/ReflectionDashboard.tsx` | UI controls |

## Troubleshooting

### Issue: "In cooldown period" when running reflection
**Fix**: Use `forceRun: true` or call `clearCooldown()`
```typescript
useAIReflectionStore.getState().clearCooldown();
```

### Issue: Reflection skipped with "No records to evaluate"
**Fix**: Ensure generations are being recorded, or disable `evaluateUnevaluatedOnly`

### Issue: Evaluation scores seem wrong
**Fix**: Check the rubric weights add up to 1.0 and criteria descriptions are clear

### Issue: Too many prompt changes
**Fix**: Increase `cooldownMinutes`, lower `scoreThreshold`, or disable `autoApplyChanges`
