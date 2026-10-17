---
name: sast
description: "Source code vulnerability hunting (SAST). Decomposes analysis into specialized passes: map entry points, map dangerous ops, trace flows, find gaps, adversarial validation, exploit. Usage: /sast <repo_path> [--lang c|cpp|rust|java|python|go|php] [--min-score 4] [--max-files 30] [--skip-static] [--best-of N]"
disable-model-invocation: false
---
Source code hunt on: $ARGUMENTS

ALL agents dispatched by this command MUST use `model: "inherit"` in the Agent tool call,
EXCEPT sast-flow-tracer and sast-gap-analyzer which MUST use `model: "opus"` (these
require cross-file reasoning that benefits from maximum reasoning depth regardless of
what the orchestrator inherits).

Read rules/hunting.md FIRST. Rules 0, 2, 9, 14 apply to SAST.
Read skills/sast-methodology/SKILL.md for reference.

## Why This Pipeline Exists

A single agent asked to "find vulnerabilities" will hallucinate plausible-looking bugs.
This pipeline decomposes the task into focused steps:

1. Reading code and listing entry points → comprehension task
2. Listing dangerous operations → pattern matching task
3. Connecting entry points to dangerous ops → cross-file reasoning (pinned opus)
4. Finding validation gaps in those connections → focused analysis (pinned opus)
5. Disproving each candidate → adversarial checking
6. Building PoC for survivors → targeted coding

The synthesis happens through the PIPELINE, not inside one agent's head.

## Phase 0: Setup

1. Parse args: `<repo_path>`, `--lang` (auto-detect), `--min-score` (default 4), `--max-files` (default 30), `--skip-static` (skip CodeQL/Semgrep), `--best-of N` (run N independent hunters on top files, default 1)
2. `ls <repo_path>/`
3. Auto-detect language:
   ```bash
   find <repo_path> \( -name '*.c' -o -name '*.cpp' -o -name '*.h' -o -name '*.rs' -o -name '*.java' -o -name '*.py' -o -name '*.go' -o -name '*.php' -o -name '*.phtml' -o -name '*.inc' \) | head -20
   ```
4. Check build: `ls <repo_path>/{Makefile,CMakeLists.txt,Cargo.toml,pom.xml,go.mod,composer.json} 2>/dev/null`
5. Brain: `uv run python3 $CLAUDE_PROJECT_DIR/tools/brain.py brief sast-<repo_name>`
6. Create output dirs: `mkdir -p findings/sast poc/sast/exploits sast-work/`

## Phase 1: Build + Static Analysis

### 1a: Build with sanitizers (best-effort, C/C++/Rust/Go only)
```bash
cd <repo_path>
export CC="gcc" CFLAGS="-fsanitize=address,undefined -g -O1 -fno-omit-frame-pointer"
export CXX="g++" CXXFLAGS="$CFLAGS"
```
If build fails → log and continue. Code review still works.

**Skip 1a for PHP/Python/Java** — no native sanitizers. For PHP, ensure `php --version` works and, if `composer.json` exists, run `composer install --no-dev` best-effort for autoload/deps.

### 1b: Static analysis (unless --skip-static)
Run available tools and collect warnings:
```bash
# C/C++
cppcheck --enable=all --xml <repo_path> 2> sast-work/cppcheck.xml
# Universal
semgrep --config auto <repo_path> -o sast-work/semgrep.json --json
# PHP (run these when --lang php or .php files detected)
semgrep --config p/php --config p/security-audit <repo_path> -o sast-work/semgrep-php.json --json
psalm --taint-analysis --output-format=json <repo_path> > sast-work/psalm.json 2>/dev/null || true
phpstan analyse --level=max --error-format=json <repo_path> > sast-work/phpstan.json 2>/dev/null || true
```
Parse into `sast-work/static-warnings.json`.
These feed into Phase 3d as additional candidates.

## Phase 2: File Ranking

Dispatch `sast-file-ranker` agent (model: inherit):
- Input: repo path, language, build info
- Output: `sast-rankings.json`

## Phase 3: Decomposed Analysis (per scored file)

For each file scoring >= `--min-score`, starting from highest:

### 3a: Entry Point Mapping
Dispatch `sast-entry-mapper` agent (model: inherit):
- Output: `sast-work/<file_hash>-entries.json`

### 3b: Dangerous Operation Mapping
Dispatch `sast-danger-mapper` agent (model: inherit):
- Output: `sast-work/<file_hash>-dangers.json`

### 3c: Data Flow Tracing
Dispatch `sast-flow-tracer` agent (model: **opus**):
- Input: entries + dangers + source + headers
- Output: `sast-work/<file_hash>-flows.json`

### 3d: Gap Analysis
Dispatch `sast-gap-analyzer` agent (model: **opus**):
- Input: flows + static-warnings (if relevant)
- Output: `sast-work/<file_hash>-candidates.json`

### 3e: Brain update
`uv run python3 $CLAUDE_PROJECT_DIR/tools/brain.py record sast-<repo_name> analyzed "<file>" "entries: N, dangers: N, flows: N, candidates: N"`

## Phase 4: Adversarial Validation

For each candidate:
Dispatch `sast-devils-advocate` agent (model: inherit):
- Verdict: SURVIVES / KILLED (with reason)

## Phase 5: PoC Confirmation

For each survivor:
Dispatch `sast-hunter` agent (model: inherit) in focused mode:
- Receives the specific candidate with full context
- Writes PoC, runs with ASan (C/C++/Rust/Go) OR PHP runtime/HTTP request (PHP) OR interpreter (Python/Java)
- Verdict: CONFIRMED / REJECTED

### Best-of-N (if --best-of > 1)
For score-5 files, run N independent instances. Finding in 2+ runs = real. Finding in 1 run = flag for review.

## Phase 6: Exploit Development (confirmed, severity >= medium)

Dispatch `sast-exploit-builder` agent (model: inherit):
- Tier 1-5 exploitation ladder
- Output: `poc/sast/exploits/`

## Phase 7: Document

Record to brain, write to `findings/sast/`, print summary.

## Output

```
SAST HUNT: <repo_name> (decomposed pipeline)
══════════════════════════════════════════════

Static warnings: N | Files ranked: N (huntable: N)
Entry points: N | Dangerous ops: N | Reachable flows: N | Candidates: N
Devil's advocate: N survived / N killed
ASan confirmed: N | Exploit tiers: ...

CONFIRMED:
1. [CRITICAL] <title> — <file>:<line>
   Flow: <entry> → <gap> → <dangerous op>

HALLUCINATIONS CAUGHT (saved by devil's advocate):
- <candidate> — killed: <reason>

Cost: $X.XX | Agents: N
```

## Cost Awareness

4-6 agents per file, two using Opus. Budget ~$0.50-2.00/file.
30 files ≈ $15-60. Adjust --min-score and --max-files accordingly.

## Top-Tier SAST Operator Addendum

Make source review adversarial and evidence-bound.

1. Rank by exploit reachability, not scary APIs. Entry point plus attacker control plus missing guard plus dangerous sink beats isolated `exec`, `eval`, or deserializer references.
2. For every candidate, require a concrete flow: source, transformations, authorization checks, validation gaps, sink, and trigger conditions.
3. Read tests and recent security patches. Regression tests often show the intended invariant; patch diffs show the bug shape.
4. Use static tools as lead generators only. A finding survives when the repo can be built or minimally exercised and the PoC hits the vulnerable path.
5. Maintain a killed-candidate list with reasons: unreachable, sanitized, auth required, type impossible, dead code, framework guard, version mismatch.
6. For memory-unsafe code, prefer sanitizer-confirmed crashes with minimized inputs. For web code, prefer request-level PoCs. For supply-chain or CI, prove the workflow trigger and trust boundary.
7. Stop when marginal files are low-value. Raise `--min-score` rather than spending Opus on glue code.
