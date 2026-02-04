---
name: inbox-processing-expert
description: Expert guidance for building and maintaining the Para Obsidian inbox processing system - a security-hardened automation framework for processing PDFs and attachments with AI-powered metadata extraction. Use when building inbox processors, implementing security patterns (TOCTOU, command injection prevention, atomic writes), designing interactive CLIs with suggestion workflows, integrating LLM detection, implementing idempotency with SHA256 registries, or working with the para-obsidian inbox codebase. Covers engine/interface separation, suggestion-based architecture, confidence scoring, error taxonomy, structured logging, and testing patterns. Useful when user mentions inbox automation, PDF processing, document classification, security-hardened file processing, or interactive CLI design.
allowed-tools: Read, Grep, Glob
---

# Inbox Processing Expert

Build security-hardened inbox automation with AI-powered metadata extraction following the Para Obsidian inbox processing framework.

## Quick Navigation

- **[Architecture Overview](#architecture-overview)** - Engine/interface separation, suggestion-based design
- **[Security Patterns](#security-patterns)** - P0 critical protections (TOCTOU, command injection, atomic writes)
- **[Core Concepts](#core-concepts)** - Suggestions, confidence scoring, idempotency
- **[Performance Characteristics](#performance-characteristics)** - Timing, concurrency limits, optimization
- **[Interactive CLI](#interactive-cli)** - Terminal UI, command parsing, user feedback
- **[Error Handling](#error-handling)** - 23-error taxonomy across 7 categories
- **[Testing Strategy](#testing-strategy)** - 246 tests, coverage patterns
- **[Common Questions](#common-questions)** - FAQ and troubleshooting
- **[Related Skills](#related-skills)** - Bun CLI, Bun FS Helpers

---

## Architecture Overview

### Engine/Interface Separation

**Core principle:** Engine logic is UI-agnostic. Same core powers CLI, web app, or API.

```typescript
// Engine returns suggestions - never mutates state directly
const engine = createInboxEngine({ vaultPath: "/path/to/vault" });

// 1. Scan inbox → generate suggestions
const suggestions = await engine.scan();

// 2. Edit suggestion with custom prompt
const updated = await engine.editWithPrompt("abc123", "put in Health area instead");

// 3. Execute approved suggestions
const results = await engine.execute(["abc123", "def456"]);

// 4. Generate markdown report
const report = engine.generateReport(suggestions);
```

**Benefits:**
- UI can be replaced without touching core logic
- Easy to test (engine is pure logic, no console.log or process.exit)
- Multiple interfaces (CLI, web, CI/CD) share same engine

### Suggestion-Based Architecture

**Never mutate state directly.** All operations return suggestions that require human approval.

```typescript
interface InboxSuggestion {
  id: string;                    // UUID for tracking
  source: string;                // Original file path
  processor: "attachments" | "notes" | "images";
  confidence: "high" | "medium" | "low";
  action: "create-note" | "move" | "rename" | "link" | "skip";

  // Optional based on action
  suggestedNoteType?: string;    // invoice, booking, session
  suggestedTitle?: string;
  suggestedDestination?: string; // PARA folder
  suggestedArea?: string;        // [[Area]] wikilink
  suggestedProject?: string;     // [[Project]] wikilink
  extractedFields?: Record<string, unknown>;
  suggestedAttachmentName?: string;
  attachmentLink?: string;
  reason: string;                // Human-readable explanation
}
```

**Key insight:** Suggestions are immutable. `editWithPrompt()` returns a NEW suggestion.

---

## Security Patterns

### P0 Critical Protections

#### 1. Command Injection Prevention

**Always use array args, never string interpolation.**

```typescript
// ❌ WRONG - vulnerable to injection
await $`pdftotext ${filePath} -`;

// ✅ CORRECT - array args prevent shell interpretation
const proc = Bun.spawn(["pdftotext", filePath, "-"]);
```

**Related:** See [Bun FS Helpers skill](../bun-fs-helpers/SKILL.md) for command-injection-safe filesystem operations.

#### 2. TOCTOU (Time-of-Check-Time-of-Use) Mitigation

**Check file before AND after operations to detect tampering.**

```typescript
import { stat } from "@sidequest/core/fs";

// Pre-check
const preStats = await stat(filePath);

// Extract text
const text = await extractPdfText(filePath, cid);

// Post-verify
const postStats = await stat(filePath);
if (postStats.mtimeMs !== preStats.mtimeMs) {
  throw createInboxError("EXT_PDF_TOCTOU", { cid, source: filePath });
}
```

**Use case:** Prevent file swapping during multi-step operations.

#### 3. Atomic Registry Writes

**Write to temp file, then atomically rename.**

```typescript
import { rename } from "@sidequest/core/fs";

// Write to temp file
await Bun.write(tempPath, JSON.stringify(registry));

// Atomic rename (POSIX guarantees atomicity)
await rename(tempPath, registryPath);
```

**Why:** Prevents corrupt registry if process crashes mid-write.

#### 4. File Locking

**Acquire lock before concurrent operations.**

```typescript
// Acquire lock → do work → release lock (finally block)
await acquireLock(lockPath);
try {
  // ... registry operations
} finally {
  releaseLock(lockPath);
}
```

**Use case:** Multiple processes accessing same registry.

#### 5. Process Lifecycle Management

**Kill child processes on timeout to prevent zombies.**

```typescript
const timeout = setTimeout(() => {
  proc.kill(); // Prevent zombie process
  reject(new Error("Timeout"));
}, 30000);

try {
  // Wait for process
  await proc.exited;
  clearTimeout(timeout);
} catch (error) {
  clearTimeout(timeout);
  throw error;
}
```

#### 6. Prompt Injection Sanitization

**Strip control characters from user input.**

```typescript
function sanitizePrompt(input: string): string {
  return input.replace(/[\x00-\x1F\x7F]/g, ""); // Strip control chars
}

const userPrompt = sanitizePrompt(rawInput);
```

#### 7. Rollback on Failure

**Delete orphaned resources if operation fails.**

```typescript
try {
  // Create note
  await createNote(notePath, content);

  // Move attachment
  await moveFile(source, dest);
} catch (error) {
  // Rollback: delete orphaned note
  if (pathExistsSync(notePath)) {
    unlinkSync(notePath);
  }
  throw error;
}
```

---

## Core Concepts

### Confidence Scoring

| Level | Criteria |
|-------|----------|
| **HIGH** | Heuristics AND AI agree + target location exists + template available |
| **MEDIUM** | AI detects type but filename/content ambiguous |
| **LOW** | AI uncertain, content unclear, extraction failed |

**Implementation:**

```typescript
// Start with base confidence from LLM
let confidence: "high" | "medium" | "low" = llmResult.confidence > 0.8 ? "high" : "medium";

// Downgrade if heuristics disagree
if (filenameHint !== llmType) {
  confidence = confidence === "high" ? "medium" : "low";
}

// Downgrade if target doesn't exist
if (!pathExistsSync(targetFolder)) {
  confidence = "low";
}

// Downgrade if template missing
if (!templateExists(suggestedNoteType)) {
  confidence = confidence === "high" ? "medium" : "low";
}
```

### Idempotency with SHA256 Registry

**Use content hashing to prevent duplicate processing.**

```typescript
import { hashFile, createRegistry } from "./registry";

const registry = createRegistry(vaultPath);
await registry.load();

const hash = await hashFile(filePath);
if (registry.isProcessed(hash)) {
  console.log("Already processed - skipping");
  return;
}

// Process file...
registry.markProcessed({
  sourceHash: hash,
  sourcePath: filePath,
  processedAt: new Date().toISOString(),
  createdNote: notePath,
});

await registry.save();
```

**Benefits:**
- Filename changes don't break idempotency
- Safe to re-run on same files
- Registry tracks what was created from each source

### Converters Architecture

**Extensible document type detection via converter configuration.**

The converters module provides a pluggable architecture for detecting document types:

```typescript
import type { InboxConverter } from "./converters/types";

const invoiceConverter: InboxConverter = {
  id: "invoice",
  displayName: "Invoice",
  enabled: true,
  priority: 90,  // Higher = checked first

  heuristics: {
    filenamePatterns: [
      { pattern: "invoice|rechnung|factura", weight: 0.9 },
      { pattern: "receipt|bill", weight: 0.7 },
    ],
    contentMarkers: [
      { pattern: "total|amount due|subtotal", weight: 0.8 },
      { pattern: "invoice number|inv[.#]", weight: 0.9 },
    ],
    threshold: 0.3,
  },

  fields: [
    { name: "provider", type: "string", description: "Company name", required: true },
    { name: "amount", type: "currency", description: "Total amount", required: true },
    { name: "date", type: "date", description: "Invoice date", required: true },
    { name: "invoiceNumber", type: "string", description: "Invoice #", required: false },
  ],

  extraction: {
    promptHint: "Extract invoice details including provider, amount, and date.",
    keyFields: ["provider", "amount"],
  },

  template: {
    name: "Invoice",
    fieldMappings: {
      provider: "Provider",
      amount: "Amount",
      date: "Date",
      invoiceNumber: "Invoice Number",
    },
  },

  scoring: {
    heuristicWeight: 0.3,
    llmWeight: 0.7,
    highThreshold: 0.85,
    mediumThreshold: 0.6,
  },
};
```

**Key patterns:**
- **Heuristics first:** Quick filename/content pattern matching (0ms)
- **LLM second:** AI-powered extraction only for matched files (~1-3s)
- **Field-driven:** Each converter defines extraction fields and template mappings
- **Priority-based:** Higher priority converters are checked first
- **Extensible:** Add new document types by creating converters

---

## Performance Characteristics

| Operation | Typical Time | Notes |
|-----------|--------------|-------|
| Scan (10 PDFs) | ~15-30s | Depends on LLM latency (3 concurrent) |
| PDF extraction | ~500-2000ms | Per file, depends on size |
| LLM detection | ~1-3s | Per file (haiku model) |
| Execute (10 items) | ~2-5s | File I/O bound (10 concurrent) |
| Registry load | ~10-50ms | Depends on size (1000 items = ~50ms) |

### Concurrency Limits

```typescript
import pLimit from "p-limit";

// PDF extraction: CPU-bound
const pdfLimit = pLimit(5);

// LLM calls: API rate limits
const llmLimit = pLimit(3);

// File I/O: Disk is fast
const ioLimit = pLimit(10);
```

**Why limit concurrency:**
- Prevent API rate limit errors
- Avoid OOM from too many parallel operations
- Balance throughput vs. resource usage

---

## Interactive CLI

### Command Loop Pattern

**Display → Parse → Execute → Update display**

```typescript
while (true) {
  // Display suggestions table
  console.log(formatSuggestionsTable(suggestions));

  // Show commands
  console.log("\nCommands:");
  console.log("  a         - Approve all HIGH confidence");
  console.log("  e<N>      - Edit suggestion with prompt");
  console.log("  <N>,<M>   - Execute specific suggestions");
  console.log("  q         - Quit");

  // Get user input
  const cmd = await getUserInput();

  if (cmd === 'a') {
    // Approve all high-confidence suggestions
    const highIds = suggestions
      .filter(s => s.confidence === "high")
      .map(s => s.id);
    const results = await engine.execute(highIds);

    // Update display
    suggestions = suggestions.filter(s => !highIds.includes(s.id));
  }
  else if (cmd.match(/^e(\d+)/)) {
    // Edit with prompt
    const index = parseInt(cmd.slice(1));
    const suggestion = suggestions[index];

    const prompt = await getUserInput("Custom instructions: ");
    const updated = await engine.editWithPrompt(suggestion.id, sanitizePrompt(prompt));

    // Update suggestions array
    suggestions[index] = updated;
  }
  else if (cmd === 'q') {
    break;
  }
}
```

**Key points:**
- Stable ID-based lookups (not array indices)
- Sanitize all user input
- Update display after each operation
- Clear command structure

**Related:** See [Bun CLI skill](../bun-cli/SKILL.md) for argument parsing and output formatting patterns.

### Formatted Output

**Use tables for suggestion display:**

```typescript
function formatSuggestionsTable(suggestions: InboxSuggestion[]): string {
  const rows = suggestions.map((s, i) => [
    i.toString(),
    s.confidence,
    s.action,
    s.suggestedTitle || s.source,
    s.reason.slice(0, 50) + "...",
  ]);

  return table([
    ["#", "Confidence", "Action", "Title", "Reason"],
    ...rows,
  ]);
}
```

**Benefits:**
- Scannable at a glance
- Clear column alignment
- Truncated text for readability

---

## Error Handling

### Error Taxonomy (23 Codes)

| Category | Example Codes | Recoverable? |
|----------|---------------|--------------|
| **dependency** | `DEP_PDFTOTEXT_MISSING`, `DEP_LLM_UNAVAILABLE` | No |
| **extraction** | `EXT_PDF_CORRUPT`, `EXT_PDF_EMPTY`, `EXT_PDF_TOO_LARGE` | No |
| **detection** | `DET_TYPE_UNKNOWN`, `DET_FIELDS_INCOMPLETE` | No |
| **validation** | `VAL_AREA_NOT_FOUND`, `VAL_TEMPLATE_MISSING` | No |
| **execution** | `EXE_NOTE_CREATE_FAILED`, `EXE_ATTACHMENT_MOVE_FAILED` | No |
| **registry** | `REG_READ_FAILED`, `REG_WRITE_FAILED`, `REG_CORRUPT` | Yes |
| **user** | `USR_INVALID_COMMAND`, `USR_EDIT_PROMPT_EMPTY` | Yes |

### Error Factory Pattern

```typescript
interface InboxError extends Error {
  code: string;
  category: string;
  recoverable: boolean;
  context: Record<string, unknown>;
}

function createInboxError(
  code: string,
  context: Record<string, unknown>,
): InboxError {
  const error = new Error(ERROR_MESSAGES[code]) as InboxError;
  error.code = code;
  error.category = code.split("_")[0].toLowerCase();
  error.recoverable = RECOVERABLE_ERRORS.includes(code);
  error.context = context;
  return error;
}
```

**Usage:**

```typescript
if (!pathExistsSync(pdfPath)) {
  throw createInboxError("EXT_PDF_NOT_FOUND", {
    cid,
    source: pdfPath
  });
}
```

**Benefits:**
- Structured error handling
- Correlation IDs for debugging
- User-facing messages separate from codes
- Recoverable vs. fatal distinction

---

## Logging & Observability

### Structured Logging

**Every log includes correlation ID.**

```typescript
import { inboxLogger, pdfLogger, llmLogger, executeLogger } from "./logger";

const cid = crypto.randomUUID().slice(0, 8);

inboxLogger.info`Scan started items=${count} ${cid}`;
pdfLogger.debug`Extracting ${filePath} ${cid}`;
llmLogger.info`Detection complete type=${type} confidence=${conf} ${cid}`;
executeLogger.info`Note created path=${notePath} ${cid}`;
```

**Log location:** `~/.claude/logs/para-obsidian.jsonl`

### Key Metrics

| Metric | Purpose |
|--------|---------|
| `scan.duration_ms` | Overall scan performance |
| `pdf.extraction_duration_ms` | pdftotext latency |
| `llm.call_duration_ms` | LLM API latency |
| `llm.calls_per_scan` | Cost tracking |
| `execute.success_rate` | Reliability |

**Usage for debugging:**

```bash
# Find logs for correlation ID
grep "abc12345" ~/.claude/logs/para-obsidian.jsonl

# Analyze LLM latency
jq 'select(.llm.call_duration_ms) | .llm.call_duration_ms' \
  ~/.claude/logs/para-obsidian.jsonl | \
  awk '{sum+=$1; count++} END {print sum/count}'
```

---

## Testing Strategy

### Coverage (246 Tests)

- **Registry** (28 tests) - Atomic writes, locking, validation, idempotency
- **PDF Processor** - Extraction, heuristics, TOCTOU, timeout handling
- **Engine** - Scan, execute, edit, rollback on failure
- **CLI Adapter** - Command parsing, display, prompt sanitization
- **Errors** - All 23 error codes, recovery strategies
- **Logging** - Correlation IDs, subsystem loggers

### Testing Patterns

#### Security Testing

```typescript
test("prevents command injection in PDF extraction", async () => {
  const maliciousPath = "/tmp/file.pdf; rm -rf /";

  await expect(extractPdfText(maliciousPath, "cid"))
    .rejects.toThrow("EXT_PDF_NOT_FOUND");

  // Verify no shell command was executed
  // (file doesn't exist, so extraction should fail safely)
});
```

#### TOCTOU Testing

```typescript
test("detects file tampering during extraction", async () => {
  const filePath = await createTempFile("test.pdf");

  // Mock stat to simulate file change
  const originalStat = stat;
  vi.spyOn(fs, "stat").mockImplementation(async (path) => {
    const result = await originalStat(path);
    // Increment mtime on second call
    result.mtimeMs += 1000;
    return result;
  });

  await expect(extractPdfText(filePath, "cid"))
    .rejects.toThrow("EXT_PDF_TOCTOU");
});
```

#### Idempotency Testing

```typescript
test("doesn't reprocess same file twice", async () => {
  const engine = createInboxEngine({ vaultPath });

  // First scan
  const suggestions1 = await engine.scan();
  expect(suggestions1).toHaveLength(1);

  // Execute
  await engine.execute([suggestions1[0].id]);

  // Second scan - should skip processed file
  const suggestions2 = await engine.scan();
  expect(suggestions2).toHaveLength(0);
});
```

---

## Common Questions

### When should I use HIGH vs MEDIUM vs LOW confidence?

**HIGH confidence** requires all of:
- LLM detection confidence > 0.8
- Filename heuristics match LLM type
- Target destination folder exists
- Required template is available

**MEDIUM confidence** when:
- LLM is confident but heuristics disagree
- Target location exists but some ambiguity
- Most fields extracted successfully

**LOW confidence** when:
- LLM confidence < 0.5
- Target location doesn't exist
- Template missing
- Extraction failed or incomplete

### How do I handle files that fail processing?

Use the error taxonomy to determine if recoverable:

```typescript
try {
  await processPDF(file);
} catch (error) {
  if (error.recoverable) {
    // Registry errors, user input errors - retry or skip
    logger.warn`Recoverable error: ${error.code} ${cid}`;
  } else {
    // Dependency, extraction, validation errors - fatal
    logger.error`Fatal error: ${error.code} ${cid}`;
    throw error;
  }
}
```

### Should I process files in CI/CD or interactively?

**Interactive mode** (CLI):
- Review suggestions before executing
- Edit with custom prompts
- Handle MEDIUM/LOW confidence items

**CI/CD mode** (future):
- Auto-execute HIGH confidence only
- Queue MEDIUM/LOW for manual review
- Generate report for human oversight

### How do I debug slow LLM calls?

Check logs for correlation ID:

```bash
# Find all LLM calls for a scan
grep "abc12345" ~/.claude/logs/para-obsidian.jsonl | grep "llm.call_duration_ms"

# Average LLM latency
jq 'select(.llm.call_duration_ms) | .llm.call_duration_ms' \
  ~/.claude/logs/para-obsidian.jsonl | \
  awk '{sum+=$1; count++} END {print sum/count " ms"}'
```

Optimization strategies:
- Use faster model (haiku vs sonnet)
- Reduce concurrency limit (less rate limiting)
- Cache common vault context (areas, projects)

### How do I prevent duplicate processing after renaming files?

The registry uses SHA256 content hashing, not filenames:

```typescript
// File renamed from invoice-old.pdf → invoice-new.pdf
const hash = await sha256File("invoice-new.pdf");

// Registry still recognizes it by content
if (registry.isProcessed(hash)) {
  console.log("Already processed (content match)");
}
```

Filename changes don't affect idempotency.

### What happens if a file changes during processing (TOCTOU)?

Pre- and post-checks detect tampering:

```typescript
// Before extraction
const preStats = await stat(filePath);

// Extract (could take 1-2 seconds)
const text = await extractPdfText(filePath);

// After extraction - verify unchanged
const postStats = await stat(filePath);
if (postStats.mtimeMs !== preStats.mtimeMs) {
  throw createInboxError("EXT_PDF_TOCTOU", { cid, source: filePath });
}
```

If file modified during processing, operation fails safely.

---

## Related Skills

### Bun CLI Development

**Reference:** [Bun CLI skill](../bun-cli/SKILL.md)

Use for:
- Argument parsing patterns (--flag value, --flag=value, --flag)
- Dual output formatting (markdown + JSON)
- Error handling with exit codes
- Subcommand dispatch
- Usage text structure

**Example from inbox CLI:**

```typescript
const { command, flags, positional } = parseArgs(process.argv.slice(2));

if (command === "process") {
  const format = parseOutputFormat(flags.format);
  const dryRun = flags["dry-run"] === true;

  // ... processing logic

  console.log(formatOutput(result, format));
}
```

### Bun FS Helpers

**Reference:** [Bun FS Helpers skill](../bun-fs-helpers/SKILL.md)

Use for:
- Command-injection-safe file operations
- TOCTOU protection with stat()
- Atomic file updates (temp + rename)
- SHA256 hashing for idempotency
- Pure Bun-native APIs (no node:fs)

**Example from inbox engine:**

```typescript
import {
  pathExistsSync,
  readTextFileSync,
  writeTextFileSync,
  rename,
  sha256File,
  stat,
} from "@sidequest/core/fs";

// Atomic update
const tempPath = `${targetPath}.tmp`;
writeTextFileSync(tempPath, newContent);
await rename(tempPath, targetPath);

// Idempotency
const hash = await sha256File(sourceFile);
if (registry.isProcessed(hash)) return;

// TOCTOU protection
const preStat = await stat(filePath);
// ... do work ...
const postStat = await stat(filePath);
if (postStat.mtimeMs !== preStat.mtimeMs) throw error;
```

---

## Common Patterns

### Engine Factory

```typescript
function createInboxEngine(options: { vaultPath: string }): InboxEngine {
  let cachedSuggestions: InboxSuggestion[] = [];

  return {
    async scan() {
      // Scan inbox, generate suggestions
      cachedSuggestions = await scanInbox(options.vaultPath);
      return cachedSuggestions;
    },

    async editWithPrompt(id: string, prompt: string) {
      const suggestion = cachedSuggestions.find(s => s.id === id);
      if (!suggestion) throw error;

      // Call LLM with user prompt
      const updated = await llmEditSuggestion(suggestion, prompt);

      // Replace in cache
      cachedSuggestions = cachedSuggestions.map(s =>
        s.id === id ? updated : s
      );

      return updated;
    },

    async execute(ids: string[]) {
      const toExecute = cachedSuggestions.filter(s => ids.includes(s.id));

      const results = await Promise.all(
        toExecute.map(s => executeSuggestion(s))
      );

      // Remove executed from cache
      cachedSuggestions = cachedSuggestions.filter(
        s => !ids.includes(s.id)
      );

      return results;
    },

    generateReport(suggestions: InboxSuggestion[]) {
      return formatMarkdownReport(suggestions);
    },
  };
}
```

### LLM Integration

```typescript
import { buildInboxPrompt, parseDetectionResponse } from "./llm-detection";
import { callLLM } from "@sidequest/core/llm";

async function detectDocumentType(
  content: string,
  filename: string,
  vaultContext: { areas: string[]; projects: string[] },
): Promise<DocumentTypeResult> {
  const prompt = buildInboxPrompt({
    content,
    filename,
    vaultContext,
  });

  const response = await callLLM(prompt, {
    model: "haiku",
    temperature: 0.3,
  });

  return parseDetectionResponse(response);
}
```

---

## Quick Reference

### File Structure

```
src/inbox/
├── types.ts              # Core types (InboxSuggestion, InboxEngine)
├── engine.ts             # Engine factory (scan/execute/edit/report)
├── registry.ts           # Idempotency tracking (SHA256, locking)
├── pdf-processor.ts      # PDF extraction + heuristics
├── llm-detection.ts      # AI type detection + field extraction
├── cli-adapter.ts        # Interactive terminal UI
├── cli.ts                # Interactive CLI entry point
├── errors.ts             # Error taxonomy (23 codes)
├── logger.ts             # Structured logging with correlation IDs
├── unique-path.ts        # Path collision detection and resolution
├── converters/           # Document type detection configuration
│   ├── types.ts          # InboxConverter interface definitions
│   ├── defaults.ts       # Default converters (invoice, booking)
│   ├── loader.ts         # Converter loading and merging
│   └── index.ts          # Module exports
└── [*.test.ts]           # 246 comprehensive tests (10 files)
```

### Key Dependencies

- `p-limit` - Controlled concurrency
- `nanospinner` - Progress indicators for CLI
- `@sidequest/core/fs` - Atomic write utilities (ensureDirSync, moveFile, readTextFileSync)
- `@sidequest/core/glob` - File globbing utilities (globFilesSync)
- `pdftotext` - External CLI (brew install poppler)
- `crypto.subtle` - SHA256 hashing (Bun native)

### Checklist: Building an Inbox Processor

- [ ] Engine/interface separation (engine is UI-agnostic)
- [ ] Suggestion-based architecture (never mutate directly)
- [ ] Command injection prevention (array args only)
- [ ] TOCTOU protection (stat before AND after)
- [ ] Atomic writes (temp file + rename)
- [ ] File locking for concurrent access
- [ ] Process timeout handling (kill zombies)
- [ ] Prompt sanitization (strip control chars)
- [ ] Rollback on failure (delete orphans)
- [ ] Confidence scoring (high/medium/low)
- [ ] SHA256 idempotency (content-based, not filename)
- [ ] Error taxonomy (structured, recoverable flag)
- [ ] Correlation ID logging (debugging)
- [ ] Interactive CLI (display → parse → execute → update)
- [ ] Converter-based detection (extensible document types)
- [ ] Unique path handling (collision detection with .1, .2 suffixes)
- [ ] Test coverage (security, TOCTOU, idempotency)

---

**Last Updated:** 2025-12-12
**Status:** Production Reference Implementation
**Related:** [Bun CLI](../bun-cli/SKILL.md), [Bun FS Helpers](../bun-fs-helpers/SKILL.md)
