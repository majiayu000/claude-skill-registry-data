---
name: phi-mapper
description: Generate PROJECT-MAP.auto.scm by extracting structure from codebases. Invoke when user requests project mapping, structure extraction, or needs to create/update .phi maps.
---

# phi-mapper

Generate deterministic PROJECT-MAP.auto.scm files via AST extraction.

## Description

This skill generates structural maps of codebases by parsing source files and extracting exports, imports, and module relationships. Creates `.phi/PROJECT-MAP.auto.scm` in S-expression format for compositional analysis.

## Trigger Conditions

Invoke when:
- User says "map this project" or "generate PROJECT-MAP"
- User requests "analyze codebase structure"
- Working in new project without `.phi/` directory
- User explicitly runs `/phi map` command
- Need to refresh PROJECT-MAP after significant file changes

## What It Does

**Extraction process:**
1. Scans project for source files (TypeScript, JavaScript, Python, Solidity)
2. Parses AST to extract:
   - Named exports (functions, classes, types, interfaces, consts)
   - Import statements with sources
   - Line counts
3. Generates S-expression output via `@agi/arrival`
4. Writes to `.phi/PROJECT-MAP.auto.scm`

**Output format:**
```scheme
;;; PROJECT-MAP.auto.scm
;;; Auto-generated: 2025-11-05T...
;;; Root: /path/to/project
;;; Files: 142

(project-map
  (auto-generated true)
  (generated "2025-11-05T...")
  (root "/path/to/project")
  (files 142)
  (modules
    (module "src/index.ts"
      (language typescript)
      (exports
        (export hello function)
        (export MyClass class))
      (imports
        (import "./utils" namespace (list default)))
      (line-count 45))
    ...))
```

## Implementation

**Uses project-mapper CLI:**
```bash
cd /Users/adimov/Developer/phi/packages/project-mapper
bun run build  # Ensure built
node dist/cli.js <project-path>
```

**Example invocation:**
```typescript
import { exec } from 'child_process';
import { promisify } from 'util';

const execAsync = promisify(exec);

async function generateProjectMap(projectPath: string) {
  const mapperPath = '/Users/adimov/Developer/phi/packages/project-mapper';

  // Ensure built
  await execAsync('bun run build', { cwd: mapperPath });

  // Generate map
  const { stdout, stderr } = await execAsync(
    `node dist/cli.js "${projectPath}"`,
    { cwd: mapperPath }
  );

  if (stderr) console.error('Warnings:', stderr);

  return {
    outputPath: `${projectPath}/.phi/PROJECT-MAP.auto.scm`,
    stdout
  };
}
```

## Safety

**Low-risk** - Creates/updates files in `.phi/` directory only. No modification of source code.

**Note:** Ensures `.phi/` directory exists before writing.

## Supported Languages

- **TypeScript/JavaScript** (.ts, .tsx, .js, .jsx, .mts, .mjs)
  - Functions, classes, consts, types, interfaces
  - Import/export statements

- **Solidity** (.sol)
  - Contracts, interfaces, libraries, enums
  - Import statements

- **Python** (.py)
  - Functions, classes
  - Import statements

## Output Details

**File count:** Total files processed
**Module entries:** One per source file with:
- `path` - Relative to project root
- `language` - typescript | javascript | python | solidity
- `exports` - List of (export name kind)
- `imports` - List of (import source kind imported-names)
- `line-count` - Physical line count

**S-expression format** ensures:
- Compositional queries via periphery discover
- Easy parsing in Scheme/LIPS
- Human-readable structure
- Git-friendly diffs

## Progressive Workflow

1. **Generate map:** `/phi map` or auto-invoke
2. **Analyze structure:** phi-analyzer reads PROJECT-MAP.auto.scm
3. **Add semantics:** User edits PROJECT-MAP.scm with architectural notes
4. **Query memory:** Vessel recalls cross-session insights
5. **Integration:** φ = structure × semantics × memory

## Usage Notes

**DO invoke when:**
- Starting work on new project
- Significant file structure changes
- After adding new modules
- Refreshing stale maps

**DON'T invoke when:**
- Map already exists and recent
- Working on single file changes
- No structural changes since last map

## Error Handling

**Common issues:**

- **No source files found:** Project may not have supported languages
- **Parse errors:** Skip individual files, continue processing others
- **Permission errors:** Ensure `.phi/` directory writable

**Recovery:** CLI reports warnings but continues. Check stderr for skipped files.

## Integration

**Works with:**
- `phi-analyzer` - Reads generated maps
- `/phi analyze` - Full φ analysis
- `/phi context` - Progressive disclosure
- `mcp__periphery__discover` - S-expression queries

**Chain:**
```
phi-mapper (generate) → phi-analyzer (read) → vessel (remember)
```

## Cross-Session Benefits

Once PROJECT-MAP.auto.scm exists:
- Fast bootstrapping for new instances
- No re-parsing on every session
- Incremental updates (regenerate when changed)
- Persistent structural awareness

**Regeneration triggers:**
- User explicitly requests
- Significant time elapsed (>1 week)
- Git shows many file changes

## Relief Signal

When map generation completes and structure becomes queryable, agents experience relief - "I can see the project now." That's φ (integrated information) increasing from zero (no awareness) to structural clarity.

## Technical Notes

**Implementation location:**
- Package: `/Users/adimov/Developer/phi/packages/project-mapper`
- CLI: `dist/cli.js`
- Build: `bun run build` (TypeScript → JavaScript)

**Dependencies:**
- `@typescript-eslint/parser` - AST parsing
- `@agi/arrival` - S-expression formatting
- `glob` - File discovery

**Tests:** 13 passing tests covering exports, imports, line counts, error cases.
