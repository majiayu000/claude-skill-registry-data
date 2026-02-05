---
name: nnt-compiler
description: Work with the NNT (Nakul Notation Tool) compiler - parse music notation shorthand, query musical structures, and export to MusicXML, ABC, and other formats for PhD research and educational content
---

# nnt-compiler Skill

Teaches how to develop and extend the NNT compiler - a TypeScript-based music notation compiler that transforms shorthand notation into rich musical data structures.

## When to Use This Skill

Use this skill when the user mentions:
- nnt, nakul notation, music notation compiler
- parser, lexer, tokenization, musical primitives
- note, chord, measure, part, musical structures
- musicxml, abc notation, lilypond export
- transformers, query dsl, musical analysis
- nnt-docs integration, abcjs rendering
- tscribe, timecode payload, audio sync
- phd research, dissertation, musical data

## Core Concepts

### What is NNT?

**NNT (Nakul Notation Tool)** is a domain-specific compiler for music notation that:
- Parses shorthand text notation into rich data structures
- Enables querying musical content (find all C notes in measure 1)
- Exports to multiple formats (MusicXML, ABC, JSON, NML)
- Powers educational content in nnt-docs
- Generates data for PhD research analysis

**Location:** `~/Code/github.com/theslyprofessor/nnt/`

**Status:** Core dependency for entire NNT ecosystem (nnt-docs, midimaze vault, tscribe component)

### The Compilation Pipeline

```
1. Input: Shorthand notation
   "do re mi fa"
        ↓
2. Lexer: Tokenization
   Breaks into Token[] objects
        ↓
3. Parser: toMus() conversion
   Creates Part/Measure/Note hierarchy
        ↓
4. MusCollection: Query & Transform
   Part[] → query/filter → export
        ↓
5. Output: Multiple formats
   MusicXML, ABC, JSON, NML
```

### Architecture: Musical Primitives ARE the Transformers

**Key insight:** Export methods live ON the musical classes themselves!

**Hierarchy:**
```
MusCollection
  └─ Part[] (voices/instruments)
      └─ Measure[] (time containers)
          └─ Note[] / Chord[] (harmonic events)
```

**Each class has export methods:**
```typescript
Note.toXML()          // Individual note as MusicXML
Part.toXML()          // Part with all measures
MusCollection.toXML() // Full score document
```

## Musical Primitives

### Aggregate (Containers)

**Part** (`src/mus/timeline/aggregate/part.ts`)
- Represents a musical voice/instrument
- Contains measures
- Has metadata: partName, keySignature, timeSignature

**Measure** (`src/mus/timeline/aggregate/measure.ts`)
- Time container for notes/chords
- Has beat boundaries
- Can auto-close or use explicit measure bars

### Harmonic (Musical Events)

**Note** (`src/mus/timeline/harmonic/note/index.ts`)
- Single pitch with duration, octave, decorators
- 17KB file - complex class with many methods
- Exports: `toXML()`, `transpose()`, rendering methods

**Chord** (`src/mus/timeline/harmonic/chord/`)
- Multiple simultaneous pitches
- Similar API to Note

### Other Structures

- **Slur** - Groups notes under single articulation
- **Tuplet** - Irregular divisions (triplets, quintuplets)
- **Polyrhythm** - Multiple rhythms simultaneously

## NNT Syntax Reference

### Duration Notation

| Syntax | Duration | Example |
|--------|----------|---------|
| `"do` | Sixteenth note | `"a "b "c` |
| `'do` | Eighth note | `'do 're 'mi` |
| `do` | Quarter note (default) | `do re mi fa` |
| `do'` | Half note | `do' re' mi'` |
| `do"` | Whole note | `do" re" mi"` |

### Rests

| Syntax | Rest Duration |
|--------|---------------|
| `;` | Quarter rest |
| `';` | Eighth rest |
| `;'` | Half rest |
| `;"` or `;''` | Whole rest |

### Octave Notation

```
c4        # Middle C (octave 4)
do6       # Do in octave 6
^6        # Octave modifier prefix
```

### Decorators

```
do:trill  # or c:tr - Trill
c:lm      # Lower mordent
c:um      # Upper mordent
```

### Slurs

```
~{do re mi fa}   # Quarter note slur
~8{do re mi}     # Eighth note slur
```

### Measure Bars

```
do re | mi fa    # Explicit measure separation
```

**Auto-close:** If no `|` bars, measures auto-close based on time signature

## Public API

### Main Entry Point

```typescript
import NNT from 'nnt'

// Parse notation
const result = NNT.parse('do re mi fa')

// Result is a MusCollection with Part[] data
```

### Transform Methods (.to() - returns string)

```typescript
// Export to MusicXML 4.0
const xml = result.to('xml')

// Export to ABC notation (for abcjs)
const abc = result.to('abc')

// Export to JSON
const json = result.to('json')

// Export to NML (Native Markup Language)
const nml = result.to('nml')
```

### Adapter Methods (.as() - returns MusCollection)

Convert notation system while staying in MusCollection:

```typescript
// Letter notation (a b c d)
result.as('alpha')

// Solfege (do re mi fa)
result.as('solfege')

// Sargam (sa re ga ma)
result.as('sargam')

// Numeric (1 2 3 4)
result.as('numeric')
```

### Query DSL

```typescript
// Find all C notes in measure 1
result
  .where({ measure: 1, pitch: 'c' })
  .all()

// Get first match
result
  .where({ measure: 1, pitch: 'c' })
  .first()

// Chaining methods
result
  .measure(1)
  .pitch('do')
  .first()
```

### Exported Classes

```typescript
import { Part, Measure, Note, Chord } from 'nnt'

// Use for manual score construction
const score = NNT.score()
```

## Project Structure

```
nnt/
├── src/
│   ├── index.ts              # Public API (NNT.parse, exports)
│   ├── lexer/                # Tokenization & parsing
│   │   ├── index.ts          # Lexer class
│   │   └── helpers/          # BeatClock, token extraction
│   ├── mus/                  # Musical primitives
│   │   ├── timeline/
│   │   │   ├── aggregate/    # Part, Measure, Slur, Tuplet
│   │   │   └── harmonic/     # Note, Chord
│   │   ├── modifiers/        # Clefs, dynamics, key/time signatures
│   │   └── helpers/          # XML headers, pitch conversions
│   ├── transform/            # Query & export subsystems
│   │   ├── collection/       # MusCollection (has .to()/.as())
│   │   ├── query/            # Query DSL filters
│   │   └── composer/         # Composition helpers
│   ├── score/                # Manual score building
│   ├── config/               # Configuration
│   └── import/               # Import functionality
│       └── music-xml/        # MusicXML import (stub)
├── spec/                     # Jest tests
├── dist/                     # Compiled output (auto-generated)
├── package.json              # Dependencies, scripts
└── tsconfig.json             # TypeScript config (CommonJS)
```

## Development Workflows

### Build the Compiler

```bash
cd ~/Code/github.com/theslyprofessor/nnt

# Build TypeScript → JavaScript
bun run build

# What happens:
# 1. Clears dist/
# 2. Compiles TS → JS (CommonJS modules)
# 3. Runs tsc-alias for path resolution
# 4. Generates type definitions (dist/index.d.ts)
```

**Auto-build:** `postinstall` script runs build automatically when installed

### Run Tests

```bash
# All tests
bun test

# Watch mode (auto-rerun on changes)
bun test --watch

# Specific test file
bun test spec/lexer.spec.ts

# Verbose output
bun test --verbose

# Coverage report
bun test --coverage
```

### Local Development with nnt-docs

**nnt-docs dependency:** `"nnt": "file:../nnt"` in package.json

**After making changes to nnt:**

```bash
# 1. Build compiler
cd ~/Code/github.com/theslyprofessor/nnt
bun run build

# 2. Reinstall in nnt-docs (picks up changes)
cd ~/Code/github.com/theslyprofessor/nnt-docs
yarn install

# 3. Restart dev server
bun start
```

**Why manual reinstall needed:**
- Local file dependencies don't auto-update
- Changes to compiler API may break nnt-docs components
- Type definitions regenerated on build

## Common Tasks

### Task 1: Fix Parsing Bug

**Scenario:** NNT notation not parsing correctly

**Steps:**
1. Write failing test in `spec/`
   ```typescript
   it('should parse eighth note slurs', () => {
     const result = NNT.parse("~8{do re mi}")
     expect(result.unwrapped[0].isSlur).toBe(true)
   })
   ```

2. Debug lexer tokenization
   ```typescript
   // In src/lexer/index.ts
   console.log('Tokens:', this.tokenize())
   ```

3. Fix parser logic in `src/lexer/` or `src/mus/`

4. Verify test passes: `bun test`

5. Build & propagate to nnt-docs
   ```bash
   bun run build
   cd ../nnt-docs && yarn install && bun start
   ```

### Task 2: Add New Syntax Feature

**Example:** Add grace note support

**Steps:**

1. **Update lexer** (`src/lexer/`)
   - Add grace note token pattern
   - Update parser to recognize syntax

2. **Create GraceNote class** (`src/mus/timeline/harmonic/grace-note.ts`)
   - Extend Note or create standalone
   - Implement `toXML()`, `toNML()`, rendering methods

3. **Export from index.ts**
   ```typescript
   export { default as GraceNote } from 'mus/timeline/harmonic/grace-note'
   ```

4. **Update transformers**
   - Ensure MusicXML output handles grace notes
   - Update ABC transformer if needed

5. **Add tests** (`spec/`)
   - Test parsing
   - Test transformations

6. **Document in README.md**
   - Add syntax examples
   - Show usage

### Task 3: Add New Export Format

**Example:** Add Lilypond export

**Steps:**

1. **Add to MusCollection** (`src/transform/collection/index.ts`)
   ```typescript
   public to(adapter: string): string {
     switch(getAdapterType(adapter)) {
       // ... existing cases
       case AdapterTypes.LILYPOND:
         return this.toLilypond()
     }
   }
   
   private toLilypond(): string {
     return this.data.map(part => part.toLilypond()).join("\n")
   }
   ```

2. **Add to Part class** (`src/mus/timeline/aggregate/part.ts`)
   ```typescript
   public toLilypond(): string {
     return this.measures.map(m => m.toLilypond()).join(" ")
   }
   ```

3. **Add to Note/Chord**
   - Implement Lilypond syntax for each primitive

4. **Add to AdapterTypes** (`src/config/mus/index.ts`)
   ```typescript
   export enum AdapterTypes {
     // ... existing
     LILYPOND = 'lilypond'
   }
   ```

5. **Test thoroughly**
   - Verify output is valid Lilypond
   - Test edge cases (decorators, slurs, etc.)

### Task 4: Optimize Performance

**Scenario:** Transformation slow for large scores

**Steps:**

1. **Profile the code**
   ```typescript
   console.time('parse')
   const result = NNT.parse(largeScore)
   console.timeEnd('parse')
   
   console.time('toXML')
   const xml = result.to('xml')
   console.timeEnd('toXML')
   ```

2. **Identify bottlenecks**
   - Is parsing slow? → Optimize lexer
   - Is export slow? → Add memoization/caching

3. **Optimize without changing output**
   ```typescript
   // Example: Cache XML headers
   private _xmlHeadersCache?: string
   
   private get xmlHeaders() {
     if (!this._xmlHeadersCache) {
       this._xmlHeadersCache = generateHeaders()
     }
     return this._xmlHeadersCache
   }
   ```

4. **Regression tests**
   - Verify output unchanged
   - Benchmark improvement

## Integration with nnt-docs

### How nnt-docs Uses the Compiler

**nnt-docs is a Next.js documentation site** that uses NNT for:
- Live notation rendering (via abcjs)
- Interactive API examples
- Educational content

**Key component usage:**
```typescript
// In nnt-docs React component
import nnt from 'nnt'
import ABCJS from 'abcjs'

const NotationDisplay = ({ notation }) => {
  const abcContent = nnt
    .parse(notation)
    .to('abc')
  
  useEffect(() => {
    ABCJS.renderAbc(containerRef.current, abcContent, options)
  }, [abcContent])
  
  return <div ref={containerRef} />
}
```

**Integration points:**
- `<NNT>` component - Renders notation via ABC → abcjs
- `<NNTInput>` component - Live preview as user types
- API documentation pages - Interactive examples
- Future `<TScribe>` component - Audio sync with timecode

**Why ABC for rendering:**
- abcjs is mature, well-supported library
- Standard format, widely compatible
- Easy visual debugging

**Future:** MusicXML/Lilypond will be primary exports for production

## TypeScript Configuration

**Module system:** CommonJS (not ESM)

```json
// tsconfig.json
{
  "compilerOptions": {
    "module": "commonjs",    // Node.js compatibility
    "target": "es2016",
    "declaration": true,     // Generate .d.ts for consumers
    "outDir": "./dist",
    "strict": true
  }
}
```

**Why CommonJS:**
- Node.js compatibility
- Easier integration with build tools
- nnt-docs expects CommonJS modules

## Future Extensions

### Timecode Payload (tscribe Component)

**Goal:** Add timing data for audio/video synchronization

**Planned addition to musical primitives:**

```typescript
interface NNTEvent {
  uuid: string
  nntCode: string
  timecode?: {
    type: 'absolute' | 'relative' | 'transient-linked'
    value: number  // seconds since start
    transientUUID?: string  // Link to reference event
    metadata?: {
      audioFile?: string
      videoFile?: string
      confidence?: number
    }
  }
}
```

**Where to add:**
- Note and Chord classes (optional field)
- Preserved through transformations
- Exported in MusicXML as custom attributes
- Used by tscribe component in nnt-docs

**Use case:**
```typescript
// Sync notation display with audio playback
const score = NNT.parse(notation)
const noteAt2Seconds = score.where({ 
  timecode: { type: 'absolute', value: 2.0 }
}).first()

// Highlight note when audio reaches 2 seconds
```

## Export Formats

### MusicXML (Primary Production Format)

**Generated output:**
- Full MusicXML 4.0 document
- `<score-partwise>` structure
- Part lists with headers
- Measures with notes, chords, decorators
- Clefs, key signatures, time signatures

**Usage:**
```typescript
const xml = NNT.parse('do re mi fa').to('xml')
// Imports into: MuseScore, Sibelius, Finale, Dorico
```

### ABC Notation (Rendering in nnt-docs)

**Generated output:**
- ABC headers (key, meter, length)
- Voice definitions if multi-part
- Note sequences in ABC syntax

**Usage:**
```typescript
const abc = NNT.parse('do re mi fa').to('abc')
// Renders with: abcjs library
```

**Status:** Implemented but may be incomplete (README shows `<TODO>`)

### NML (Native Markup Language)

**Internal format** - likely used for:
- Round-trip parsing (NNT → NML → NNT)
- Canonical representation
- Debugging

### JSON (Analysis & Querying)

**Structured data export:**
```typescript
const json = NNT.parse('do re mi fa').to('json')
// Use for: PhD research data, statistical analysis, ML training
```

### Lilypond (Planned)

**Not yet implemented** - will generate Lilypond syntax for high-quality engraving

## Common Issues

### Parsing Errors

**Problem:** "Invalid token" error on valid notation

**Debug:**
```typescript
// Add logging to lexer
const lexer = new Lexer(notation)
console.log('Tokens:', lexer.tokenize())
```

**Common causes:**
- Unsupported syntax
- Incorrect duration markers
- Malformed measure bars

### Transform Output Invalid

**Problem:** MusicXML doesn't open in MuseScore

**Debug:**
```bash
# Validate XML
xmllint --schema musicxml.xsd output.xml

# Check structure
cat output.xml | grep -E "<score-partwise|<part|<measure"
```

**Solutions:**
- Check Note.toXML() generates valid elements
- Verify headers match MusicXML spec
- Test with minimal example first

### nnt-docs Not Picking Up Changes

**Problem:** Changes to compiler don't appear in nnt-docs

**Solution:**
```bash
# Force rebuild + reinstall
cd ~/Code/github.com/theslyprofessor/nnt
rm -rf dist && bun run build

cd ~/Code/github.com/theslyprofessor/nnt-docs
rm -rf node_modules/nnt
yarn install --force
bun start
```

### Test Failures

**Problem:** Tests pass locally but fail in CI

**Causes:**
- Snapshot mismatches
- Timing-dependent tests
- Platform-specific behavior (line endings)

**Solutions:**
- Update snapshots: `bun test -u`
- Use deterministic test data
- Normalize line endings in assertions

## Git Workflow

### Commit Message Style

**Format:** `<type>: <description>`

**Types:**
- `feat:` New syntax or feature
- `fix:` Bug fix (parsing, transformation)
- `perf:` Performance improvement
- `refactor:` Code restructuring
- `test:` Adding/updating tests
- `docs:` README or comment updates

**Examples:**
```
feat: add grace note support
fix: correct eighth note slur parsing
perf: optimize MusicXML transformation caching
refactor: extract common toXML logic
test: add measure boundary edge cases
docs: update README with slur syntax
```

## Dependencies

**Runtime:**
- `fast-xml-parser` - MusicXML generation
- `typescript` - Type system
- `ts-alias` - Path resolution in builds

**Dev:**
- `jest` / `ts-jest` - Testing framework
- `@types/jest` - TypeScript definitions

**No external music libraries** - all parsing/transformation is custom

## Best Practices

### Code Organization

1. **Musical primitives are self-contained**
   - Each class has its own export methods
   - Don't add global transformer functions

2. **Keep lexer focused on tokenization**
   - Parser logic → `toMus()` helper
   - Musical logic → primitive classes

3. **Test each layer independently**
   - Lexer tests → Token[] correctness
   - Parser tests → Musical structure
   - Transform tests → Output format validity

### Performance

1. **Lazy evaluation where possible**
   - Don't compute unless `.to()` called
   - Cache expensive transformations

2. **Avoid deep cloning**
   - Musical structures are immutable
   - Return references, not copies

### API Design

1. **Fluent interfaces**
   - Chain query methods: `.where().measure().first()`
   - Return MusCollection for continued chaining

2. **Consistent naming**
   - `.to()` for string outputs
   - `.as()` for MusCollection outputs

## Testing Strategy

### Unit Tests (spec/)

**Test structure:**
```typescript
describe('Lexer', () => {
  describe('#parse', () => {
    it('should parse quarter notes', () => {
      const result = NNT.parse('do re mi fa')
      expect(result.unwrapped.length).toBe(4)
    })
    
    it('should handle measure bars', () => {
      const result = NNT.parse('do re | mi fa')
      expect(result.data[0].measures.length).toBe(2)
    })
  })
})
```

**Coverage targets:**
- Lexer: Token extraction, edge cases
- Musical primitives: Construction, export methods
- Transformers: Format validity
- Query DSL: Filter correctness

### Integration Tests

**Test full pipeline:**
```typescript
it('should export valid MusicXML', () => {
  const notation = 'part: violin\nmeter: 4/4\ndo re mi fa'
  const xml = NNT.parse(notation).to('xml')
  
  // Verify structure
  expect(xml).toContain('<score-partwise')
  expect(xml).toContain('version="4.0"')
  
  // Verify validity (would need XML validator)
  // validateMusicXML(xml)
})
```

## Related Documentation

**Parent ecosystem:**
- `~/Code/github.com/theslyprofessor/midimaze/_Nakul/5. Coding Actions/NNT Ecosystem/AGENTS.md`

**Dependent projects:**
- `~/Code/github.com/theslyprofessor/nnt-docs/AGENTS.md` - Documentation site

**Planning documents:**
- tscribe component planning (timecode integration)
- NNT ecosystem tech stack

**User-facing:**
- `README.md` in nnt repo - Syntax reference

## See Also

- **Related Skills:**
  - `nnt-docs` - Documentation site (once created)
  - `obsidian-workflows` - Vault management (planning docs)
  
- **External Resources:**
  - [MusicXML Specification](https://www.musicxml.com/for-developers/)
  - [ABC Notation Standard](https://abcnotation.com/)
  - [abcjs Library](https://www.abcjs.net/)

## Quick Reference

### Essential Commands

```bash
# Build compiler
cd ~/Code/github.com/theslyprofessor/nnt
bun run build

# Run tests
bun test
bun test --watch

# Propagate to nnt-docs
cd ~/Code/github.com/theslyprofessor/nnt-docs
yarn install && bun start
```

### Key Concepts

- **MusCollection** = Results from `NNT.parse()`
- **Part → Measure → Note/Chord** = Musical hierarchy
- **`.to(format)`** = Export as string
- **`.as(system)`** = Convert notation system
- **Musical primitives have export methods** (not separate transformers)
- **CommonJS modules** (not ESM)
- **MusicXML = primary production format** (not ABC)
- **Local file dependency** = requires manual reinstall in nnt-docs
