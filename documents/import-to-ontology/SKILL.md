---
name: import-to-ontology
description: Intelligently parse and move content from source markdown files to appropriate ontology locations with validation, enrichment, and web content integration
---

# Import to Ontology Skill

Intelligently processes ~200 source markdown files and moves content blocks to the most suitable locations in the canonical ontology structure. Features semantic targeting, assertion validation, stub enrichment, and async web content integration.

## Overview

This skill:

1. **Parses** large source markdown files into content blocks (batch mode)
2. **Targets** optimal ontology file locations using semantic index
3. **Validates** OWL2 compliance before and after content moves (ontology-core integration)
4. **Handles** image asset references (preserves paths to shared assets/ folder)
5. **Updates** assertions/claims in content
6. **Enriches** WikiLink stubs and isolated URLs with web summaries
7. **Moves** content **destructively** (removes from source)
8. **Rolls back** on validation failures
9. **Cleans up** empty source files automatically
10. **Tracks** progress across batches with resume capability

⚠️ **DESTRUCTIVE OPERATION**: Content is moved from source files, not copied. Source files are deleted when empty. **NO BACKUPS ARE CREATED** - ensure external backups exist before running.

## Quick Start

```bash
# From project root
cd /home/devuser/workspace/project/Metaverse-Ontology

# ⚠️ IMPORTANT: Set up shared assets folder first
# Both source and target directories should reference the same assets/
mkdir -p assets/
mkdir -p /path/to/sources/assets/  # If not already present

# Dry run (analyze without moving)
claude-code "Use import-to-ontology skill with dry-run on source-file.md"

# Import single file (DESTRUCTIVE - moves content)
claude-code "Use import-to-ontology skill to process source-file.md"

# Import small batch (5 files at a time)
claude-code "Use import-to-ontology skill to process batch of 5 files from /sources/"

# Import all files (one at a time with progress tracking)
claude-code "Use import-to-ontology skill to process all files in /path/to/sources/"
```

⚠️ **WARNING**: This is a DESTRUCTIVE operation. Content is MOVED from source files and source files are DELETED when empty. **NO BACKUPS ARE CREATED**.

## Ontology-Core Integration

This skill integrates with the ontology-core library for OWL2 validation:

### Validation Bridge (Node.js ↔ Python)

```javascript
// src/validation_bridge.js
const { validateOntologyFile } = require("./src/validation_bridge");

// Validates OWL2 compliance for target files
const result = await validateOntologyFile(targetFile);

if (!result.is_valid) {
  console.error(`Validation failed: ${result.errors.length} errors`);
  // Rollback content move
}
```

### Validation Workflow

1. **Pre-Move Validation**: Check target file OWL2 compliance before modification
2. **Content Migration**: Insert content block into target file
3. **Post-Move Validation**: Re-validate target file with new content
4. **Rollback on Failure**: Restore source file if validation fails

### OWL2 Checks (via ontology-core)

- Class declarations and SubClassOf axioms
- Property declarations (ObjectProperty, DataProperty)
- Restrictions (ObjectSomeValuesFrom, etc.)
- Namespace consistency (ai:, bc:, mv:, rb:, dt:)
- Parentheses balance
- Annotation format
- Naming conventions

### Rollback Strategy

```javascript
// If post-move validation fails:
// 1. Restore source file from backup
// 2. Remove added content from target (if possible)
// 3. Log failure reason
// 4. Continue with next block
```

## Skill Architecture

### Phase 1: Analysis & Planning

**Input**: Source markdown file path(s)
**Output**: Import plan with semantic targeting

```typescript
interface ImportPlan {
  sourceFile: string;
  blocks: ContentBlock[];
  targets: TargetMapping[];
  enrichments: EnrichmentTask[];
  validations: ValidationTask[];
  estimatedTime: number;
}

interface ContentBlock {
  id: string;
  type: "heading" | "paragraph" | "list" | "code" | "quote";
  content: string;
  metadata: {
    keywords: string[];
    wikiLinks: string[];
    urls: string[];
    assertions: Assertion[];
  };
  startLine: number;
  endLine: number;
}

interface TargetMapping {
  blockId: string;
  targetFile: string;
  targetConcept: string;
  insertionPoint: "about" | "description" | "use-cases" | "examples" | "references";
  confidence: number;
  reasoning: string;
}
```

### Phase 2: Content Processing

**Actions**:

1. Extract content blocks from source
2. Identify keywords, WikiLinks, URLs, assertions
3. Query semantic index for target concepts
4. Generate insertion plan with confidence scores

### Phase 3: Enrichment (Async)

**Web Content Integration**:

```typescript
interface EnrichmentTask {
  blockId: string;
  url: string;
  type: "stub-expansion" | "citation-enrichment" | "context-addition";
  priority: "high" | "medium" | "low";
  status: "pending" | "processing" | "completed" | "failed";
}

// Uses web-summary skill (async, ~3-10s per URL)
async function enrichUrl(url: string): Promise<EnrichedContent> {
  // Call web-summary skill
  const summary = await executeSkill("web-summary", { url });

  return {
    url,
    title: summary.title,
    summary: summary.summary,
    keyPoints: summary.keyPoints,
    relevantLogseqLinks: summary.semanticLinks, // Auto-generated [[WikiLinks]]
    citations: summary.citations,
  };
}
```

### Phase 4: Validation & Updates

**Assertion Validation**:

```typescript
interface Assertion {
  text: string;
  type: "claim" | "definition" | "statistic" | "example";
  needsValidation: boolean;
  updatedText?: string;
  confidence: number;
}

function validateAssertions(block: ContentBlock): ValidationResult {
  const assertions = extractAssertions(block.content);

  return assertions.map((assertion) => {
    // Check against current ontology knowledge
    const validation = checkAgainstOntology(assertion);

    // Suggest updates if outdated
    if (validation.outdated) {
      return {
        original: assertion.text,
        updated: validation.suggestedUpdate,
        reason: validation.reason,
        confidence: validation.confidence,
      };
    }

    return { valid: true, assertion };
  });
}
```

### Phase 5: Content Migration with Validation

**Safe Move Strategy with OWL2 Compliance**:

```typescript
interface MigrationResult {
  sourceFile: string;
  targetFile: string;
  blocksMoved: number;
  blocksEnriched: number;
  assertionsUpdated: number;
  backupPath: string;
  success: boolean;
  errors: Error[];
}

async function migrateContent(plan: ImportPlan): Promise<MigrationResult> {
  // 1. Create backups
  const backup = await createBackup(plan.sourceFile);

  // 2. Process each block with validation
  for (const block of plan.blocks) {
    const target = plan.targets.find((t) => t.blockId === block.id);

    // 3. Pre-move OWL2 validation
    const preValidation = await validateOntologyFile(target.targetFile);
    if (!preValidation.is_valid && !preValidation.new_file) {
      console.error(`Pre-move validation failed: ${target.targetFile}`);
      continue; // Skip this block
    }

    // 4. Enrich content (async web summaries)
    const enriched = await enrichBlock(block, plan.enrichments);

    // 5. Validate and update assertions
    const validated = await validateBlock(enriched);

    // 6. Insert into target file
    await insertContent(target.targetFile, target.insertionPoint, validated);

    // 7. Post-move OWL2 validation
    const postValidation = await validateOntologyFile(target.targetFile);
    if (!postValidation.is_valid) {
      console.error(`Post-move validation failed: ${target.targetFile}`);

      // Rollback: restore source file
      await restoreFromBackup(backup, plan.sourceFile);

      // Log validation errors
      postValidation.errors.forEach((err) => {
        console.error(`  Line ${err.line_number}: ${err.message}`);
      });

      continue; // Skip this block
    }

    // 8. Remove from source (only if validation passed)
    await removeBlockFromSource(plan.sourceFile, block);

    // 9. Log progress
    logProgress(block, target);
  }

  // 10. Remove source file if empty
  await archiveSourceFile(plan.sourceFile);

  return {
    sourceFile: plan.sourceFile,
    targetFile: target.targetFile,
    blocksMoved: plan.blocks.length,
    success: true,
  };
}
```

## Semantic Targeting System

Uses the in-memory ontology index for intelligent placement:

```typescript
// Load index once
const INDEX = JSON.parse(fs.readFileSync(".cache/ontology-index.json", "utf-8"));

function findTargetConcept(block: ContentBlock): TargetMapping {
  // 1. Extract semantic features
  const keywords = extractKeywords(block.content);
  const wikiLinks = extractWikiLinks(block.content);

  // 2. Score all concepts by relevance
  const scored = Object.values(INDEX.concepts.concepts)
    .map((concept) => {
      let score = 0;

      // Keyword overlap
      const keywordMatch = keywords.filter((k) =>
        concept.keywords.some((ck) => ck.includes(k) || k.includes(ck))
      ).length;
      score += keywordMatch * 0.4;

      // WikiLink overlap
      const linkMatch = wikiLinks.filter(
        (link) => concept.linksTo.includes(link) || concept.linkedFrom.includes(link)
      ).length;
      score += linkMatch * 0.6;

      return { concept, score };
    })
    .filter((s) => s.score > 0)
    .sort((a, b) => b.score - a.score);

  if (scored.length === 0) {
    // Fallback: use domain detection
    return detectDomainAndSuggest(block);
  }

  const best = scored[0];

  return {
    blockId: block.id,
    targetFile: best.concept.file,
    targetConcept: best.concept.preferredTerm,
    insertionPoint: selectInsertionPoint(block),
    confidence: Math.min(best.score, 0.95),
    reasoning: `Matched ${keywordMatch} keywords and ${linkMatch} links`,
  };
}

function selectInsertionPoint(block: ContentBlock): InsertionPoint {
  // Heuristics for where to insert content
  if (block.type === "heading" && block.content.includes("Definition")) {
    return "description";
  }
  if (block.type === "heading" && block.content.includes("Example")) {
    return "examples";
  }
  if (block.type === "heading" && block.content.includes("Use Case")) {
    return "use-cases";
  }
  if (block.content.includes("http") || block.content.includes("[[")) {
    return "references";
  }

  // Default: append to About section
  return "about";
}
```

## WikiLink & URL Detection

```typescript
interface DetectedStub {
  type: "wikilink" | "url";
  value: string;
  context: string; // Surrounding text
  line: number;
  enrichmentNeeded: boolean;
}

function detectStubs(content: string): DetectedStub[] {
  const stubs: DetectedStub[] = [];

  // 1. Find WikiLinks
  const wikilinkRegex = /\[\[([^\]]+)\]\]/g;
  let match;

  while ((match = wikilinkRegex.exec(content)) !== null) {
    const wikilink = match[1];

    // Check if it's a stub (broken link or minimal context)
    const isStub = !INDEX.wikilinks.valid[`[[${wikilink}]]`] || !hasContext(content, match.index);

    if (isStub) {
      stubs.push({
        type: "wikilink",
        value: wikilink,
        context: extractContext(content, match.index, 100),
        line: getLineNumber(content, match.index),
        enrichmentNeeded: true,
      });
    }
  }

  // 2. Find isolated URLs
  const urlRegex = /(https?:\/\/[^\s\)]+)/g;

  while ((match = urlRegex.exec(content)) !== null) {
    const url = match[1];

    // Check if URL has description nearby
    const hasDescription = hasContext(content, match.index, 50);

    if (!hasDescription) {
      stubs.push({
        type: "url",
        value: url,
        context: extractContext(content, match.index, 100),
        line: getLineNumber(content, match.index),
        enrichmentNeeded: true,
      });
    }
  }

  return stubs;
}

function hasContext(content: string, index: number, minLength = 30): boolean {
  // Check if there's meaningful text around the link/URL
  const before = content.substring(Math.max(0, index - 50), index);
  const after = content.substring(index, Math.min(content.length, index + 50));

  const contextText = before + after;
  const words = contextText.split(/\s+/).filter((w) => w.length > 3);

  return words.length >= 5 && contextText.length >= minLength;
}
```

## Web Summary Integration

```typescript
interface WebSummarySkillCall {
  url: string;
  options: {
    maxLength: number;
    includeSemanticLinks: boolean;
    format: "logseq" | "markdown";
  };
}

async function enrichStubsWithWebContent(stubs: DetectedStub[]): Promise<EnrichedStub[]> {
  const enriched: EnrichedStub[] = [];

  // Process in parallel with concurrency limit (5 at a time)
  const CONCURRENCY = 5;

  for (let i = 0; i < stubs.length; i += CONCURRENCY) {
    const batch = stubs.slice(i, i + CONCURRENCY);

    const results = await Promise.all(
      batch.map(async (stub) => {
        if (stub.type === "url") {
          try {
            // Call web-summary skill (async, 3-10s)
            console.log(`Enriching URL: ${stub.value}`);

            const summary = await executeSkill("web-summary", {
              url: stub.value,
              options: {
                maxLength: 300,
                includeSemanticLinks: true,
                format: "logseq",
              },
            });

            return {
              ...stub,
              enrichedContent: formatEnrichedContent(summary, stub),
              status: "completed",
            };
          } catch (error) {
            console.warn(`Failed to enrich ${stub.value}: ${error.message}`);
            return {
              ...stub,
              enrichedContent: null,
              status: "failed",
              error: error.message,
            };
          }
        } else if (stub.type === "wikilink") {
          // Check if we can create the concept
          const suggestion = suggestConceptCreation(stub.value);

          return {
            ...stub,
            enrichedContent: suggestion,
            status: "suggest-creation",
          };
        }

        return stub;
      })
    );

    enriched.push(...results);

    // Progress update
    console.log(`Enriched ${i + results.length}/${stubs.length} stubs`);
  }

  return enriched;
}

function formatEnrichedContent(summary: WebSummarySummary, stub: DetectedStub): string {
  // Format as Logseq-compatible content
  return `
- **Source**:
  - ${summary.summary}
  - **Key Points**:
${summary.keyPoints.map((pt) => `    - ${pt}`).join("\n")}
  - **Related Concepts**: ${summary.semanticLinks.join(", ")}
  - **Retrieved**: ${new Date().toISOString().split("T")[0]}
`.trim();
}

// Execute skill helper (calls Claude Code skill system)
async function executeSkill(skillName: string, params: any): Promise<any> {
  // This calls the web-summary skill from your skill database
  // Implementation depends on Claude Code skill execution API

  // For now, placeholder that would be replaced with actual skill call
  const result = await fetch(`/skill/${skillName}`, {
    method: "POST",
    body: JSON.stringify(params),
  });

  return result.json();
}
```

## Content Block Parser

````typescript
interface ParsedContent {
  blocks: ContentBlock[];
  metadata: {
    totalBlocks: number;
    totalLines: number;
    hasWikiLinks: boolean;
    hasUrls: boolean;
    estimatedAssertions: number;
  };
}

function parseSourceFile(filePath: string): ParsedContent {
  const content = fs.readFileSync(filePath, "utf-8");
  const lines = content.split("\n");

  const blocks: ContentBlock[] = [];
  let currentBlock: Partial<ContentBlock> | null = null;
  let blockId = 1;

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];

    // Detect block boundaries
    if (line.startsWith("#")) {
      // New heading - start new block
      if (currentBlock) {
        blocks.push(completeBlock(currentBlock));
      }

      currentBlock = {
        id: `block-${blockId++}`,
        type: "heading",
        content: line,
        startLine: i,
        metadata: {
          keywords: [],
          wikiLinks: [],
          urls: [],
          assertions: [],
        },
      };
    } else if (line.startsWith("```")) {
      // Code block
      if (currentBlock) {
        blocks.push(completeBlock(currentBlock));
      }

      // Find end of code block
      let endLine = i + 1;
      while (endLine < lines.length && !lines[endLine].startsWith("```")) {
        endLine++;
      }

      currentBlock = {
        id: `block-${blockId++}`,
        type: "code",
        content: lines.slice(i, endLine + 1).join("\n"),
        startLine: i,
        endLine: endLine,
      };

      i = endLine; // Skip to end
    } else if (currentBlock) {
      // Continuation of current block
      currentBlock.content += "\n" + line;
    } else if (line.trim()) {
      // Start new paragraph block
      currentBlock = {
        id: `block-${blockId++}`,
        type: "paragraph",
        content: line,
        startLine: i,
      };
    }
  }

  // Complete final block
  if (currentBlock) {
    blocks.push(completeBlock(currentBlock));
  }

  // Extract metadata for each block
  blocks.forEach((block) => {
    block.metadata = {
      keywords: extractKeywords(block.content),
      wikiLinks: extractWikiLinks(block.content),
      urls: extractUrls(block.content),
      assertions: extractAssertions(block.content),
    };
  });

  return {
    blocks,
    metadata: {
      totalBlocks: blocks.length,
      totalLines: lines.length,
      hasWikiLinks: blocks.some((b) => b.metadata.wikiLinks.length > 0),
      hasUrls: blocks.some((b) => b.metadata.urls.length > 0),
      estimatedAssertions: blocks.reduce((sum, b) => sum + b.metadata.assertions.length, 0),
    },
  };
}

function extractUrls(content: string): string[] {
  const urlRegex = /(https?:\/\/[^\s\)]+)/g;
  const matches = content.match(urlRegex);
  return matches ? [...new Set(matches)] : [];
}

function extractAssertions(content: string): Assertion[] {
  const assertions: Assertion[] = [];

  // Patterns that indicate assertions
  const patterns = [
    /is defined as (.+?)\./gi,
    /refers to (.+?)\./gi,
    /(\d+%|\d+ percent)/gi,
    /according to (.+?),/gi,
    /enables (.+?)\./gi,
    /provides (.+?)\./gi,
  ];

  for (const pattern of patterns) {
    let match;
    while ((match = pattern.exec(content)) !== null) {
      assertions.push({
        text: match[0],
        type: determineAssertionType(match[0]),
        needsValidation: true,
        confidence: 0.7,
      });
    }
  }

  return assertions;
}

function determineAssertionType(text: string): Assertion["type"] {
  if (text.includes("%") || text.includes("percent")) return "statistic";
  if (text.includes("defined as") || text.includes("refers to")) return "definition";
  if (text.includes("for example") || text.includes("such as")) return "example";
  return "claim";
}
````

## Dry Run Mode

```typescript
interface DryRunReport {
  sourceFile: string;
  analysisDate: string;
  summary: {
    totalBlocks: number;
    targetedFiles: string[];
    urlsToEnrich: number;
    assertionsToValidate: number;
    estimatedTimeSeconds: number;
  };
  plan: ImportPlan;
  warnings: string[];
  recommendations: string[];
}

function dryRun(sourceFile: string): DryRunReport {
  const parsed = parseSourceFile(sourceFile);
  const plan = createImportPlan(parsed);

  const urlCount = parsed.blocks.reduce((sum, b) => sum + b.metadata.urls.length, 0);

  const estimatedTime =
    parsed.blocks.length * 2 + // 2s per block
    urlCount * 5; // 5s per URL (web-summary avg)

  return {
    sourceFile,
    analysisDate: new Date().toISOString(),
    summary: {
      totalBlocks: parsed.blocks.length,
      targetedFiles: [...new Set(plan.targets.map((t) => t.targetFile))],
      urlsToEnrich: urlCount,
      assertionsToValidate: parsed.metadata.estimatedAssertions,
      estimatedTimeSeconds: estimatedTime,
    },
    plan,
    warnings: generateWarnings(plan),
    recommendations: generateRecommendations(plan),
  };
}

function generateWarnings(plan: ImportPlan): string[] {
  const warnings: string[] = [];

  // Low confidence targets
  const lowConfidence = plan.targets.filter((t) => t.confidence < 0.5);
  if (lowConfidence.length > 0) {
    warnings.push(`${lowConfidence.length} blocks have low confidence targeting (<50%)`);
  }

  // Many URLs to enrich
  if (plan.enrichments.length > 20) {
    warnings.push(`${plan.enrichments.length} URLs to enrich - this will be slow (~${plan.enrichments.length * 5}s)`);
  }

  return warnings;
}

function generateRecommendations(plan: ImportPlan): string[] {
  const recs: string[] = [];

  // Suggest manual review for low confidence
  const veryLowConf = plan.targets.filter((t) => t.confidence < 0.3);
  if (veryLowConf.length > 0) {
    recs.push(`Recommend manual review for ${veryLowConf.length} low-confidence blocks`);
  }

  // Suggest creating missing concepts
  const missingConcepts = new Set(
    plan.blocks.flatMap((b) => b.metadata.wikiLinks).filter((link) => !INDEX.wikilinks.valid[`[[${link}]]`])
  );

  if (missingConcepts.size > 0) {
    recs.push(
      `Consider creating ${missingConcepts.size} missing concepts: ${Array.from(missingConcepts).slice(0, 5).join(", ")}...`
    );
  }

  return recs;
}
```

## Progress Tracking

```typescript
interface ImportProgress {
  sessionId: string;
  startTime: string;
  currentFile: string;
  filesProcessed: number;
  totalFiles: number;
  blocksProcessed: number;
  totalBlocks: number;
  urlsEnriched: number;
  totalUrls: number;
  assertionsValidated: number;
  errors: ImportError[];
  estimatedTimeRemaining: number;
}

class ImportTracker {
  private progress: ImportProgress;
  private logFile: string;

  constructor(totalFiles: number) {
    this.progress = {
      sessionId: generateSessionId(),
      startTime: new Date().toISOString(),
      currentFile: "",
      filesProcessed: 0,
      totalFiles,
      blocksProcessed: 0,
      totalBlocks: 0,
      urlsEnriched: 0,
      totalUrls: 0,
      assertionsValidated: 0,
      errors: [],
      estimatedTimeRemaining: 0,
    };

    this.logFile = `/tmp/import-ontology-${this.progress.sessionId}.log`;
  }

  updateProgress(update: Partial<ImportProgress>) {
    Object.assign(this.progress, update);

    // Calculate estimated time remaining
    const elapsed = Date.now() - new Date(this.progress.startTime).getTime();
    const rate = this.progress.blocksProcessed / (elapsed / 1000);
    const remaining = this.progress.totalBlocks - this.progress.blocksProcessed;
    this.progress.estimatedTimeRemaining = remaining / rate;

    // Log to file
    this.log(JSON.stringify(this.progress, null, 2));

    // Console update
    this.printProgress();
  }

  log(message: string) {
    fs.appendFileSync(this.logFile, `${new Date().toISOString()} - ${message}\n`);
  }

  printProgress() {
    const pct = ((this.progress.blocksProcessed / this.progress.totalBlocks) * 100).toFixed(1);
    const eta = Math.ceil(this.progress.estimatedTimeRemaining / 60);

    console.log(
      `
📊 Import Progress: ${pct}%
   Files: ${this.progress.filesProcessed}/${this.progress.totalFiles}
   Blocks: ${this.progress.blocksProcessed}/${this.progress.totalBlocks}
   URLs Enriched: ${this.progress.urlsEnriched}/${this.progress.totalUrls}
   ETA: ${eta} minutes
   Errors: ${this.progress.errors.length}
    `.trim()
    );
  }

  addError(error: ImportError) {
    this.progress.errors.push(error);
    this.log(`ERROR: ${JSON.stringify(error)}`);
  }

  getReport(): ImportProgress {
    return { ...this.progress };
  }
}
```

## Validation Bridge Usage

### Standalone Validation

```bash
# Validate single file
node src/validation_bridge.js /path/to/ontology-file.md

# Batch validate multiple files
node src/validation_bridge.js file1.md file2.md file3.md

# From import-engine
const { validateOntologyFile } = require('./src/validation_bridge');

async function checkFile(filePath) {
  try {
    const result = await validateOntologyFile(filePath);

    if (result.is_valid) {
      console.log(`✅ Valid: ${result.total_axioms} axioms`);
    } else {
      console.log(`❌ Invalid: ${result.errors.length} errors`);
      result.errors.forEach(err => {
        console.log(`  Line ${err.line_number}: ${err.message}`);
        if (err.fix_suggestion) {
          console.log(`    Fix: ${err.fix_suggestion}`);
        }
      });
    }
  } catch (error) {
    console.error(`Validation failed: ${error.message}`);
  }
}
```

### Integration Pattern

```javascript
// Before destructive move
const preValidation = await validateOntologyFile(targetFile);
if (!preValidation.is_valid) {
  console.error(`Target has errors - aborting move`);
  return { success: false, reason: "pre-validation-failed" };
}

// Perform move
moveContentBlock(source, target);

// After move - re-validate
const postValidation = await validateOntologyFile(targetFile);
if (!postValidation.is_valid) {
  // Rollback
  restoreFromBackup(source, target);
  return { success: false, reason: "post-validation-failed" };
}
```

## Usage Examples

### Example 1: Import Single File with Dry Run and Validation

```bash
# Analyze before importing
claude-code "Use import-to-ontology skill to dry-run source-notes.md"

# Review report, then import
claude-code "Use import-to-ontology skill to import source-notes.md"
```

### Example 2: Batch Import Directory

```bash
claude-code "Use import-to-ontology skill to import all files from /sources/research-notes/"
```

### Example 3: Import with Manual Target Override

```bash
claude-code "Use import-to-ontology skill to import blockchain-notes.md targeting BC-0001-blockchain.md"
```

## Configuration

Create `.import-ontology.config.json` in project root:

```json
{
  "sourceDirectory": "/home/devuser/workspace/project/sources",
  "ontologyDirectory": "/home/devuser/workspace/project/Metaverse-Ontology/logseq/pages",
  "backupDirectory": "/home/devuser/workspace/project/.backups",
  "indexPath": ".cache/ontology-index.json",

  "webSummary": {
    "enabled": true,
    "concurrency": 5,
    "timeout": 10000,
    "maxLength": 300
  },

  "validation": {
    "enabled": true,
    "autoFix": false,
    "requireManualReview": true,
    "owl2Compliance": true,
    "rollbackOnFailure": true
  },

  "targeting": {
    "minConfidence": 0.4,
    "requireManualReview": 0.7
  },

  "safety": {
    "createBackups": true,
    "dryRunFirst": true,
    "archiveSourceAfterImport": true
  }
}
```

## See Also

-
-
-
- [Web Summary Skill](/docker/lib/extensions/vf-web-summary/resources/SKILL.md)
