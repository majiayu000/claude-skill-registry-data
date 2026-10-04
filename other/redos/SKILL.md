---
name: redos
description: "Detect Regular Expression Denial of Service (ReDoS) where crafted input causes catastrophic backtracking in regex patterns applied to user-controlled strings."
metadata:
  filePattern:
    - "**/*.js"
    - "**/*.ts"
    - "**/*.py"
    - "**/*.rb"
    - "**/*.php"
    - "**/*.java"
  bashPattern:
    - "grep.*(RegExp|regex|pattern|match)"
    - "semgrep.*redos"
  priority: 70
---

# ReDoS Detection

## When to Use

Audit input validation libraries, URL/email/date parsers, sanitization utilities, template engines, and any package that applies regular expressions to user-controlled strings.

## Critical Rule

**MUST measure actual backtracking growth rate.** Do not report based on pattern structure alone. The validator.js lesson: assumed ReDoS from pattern complexity but could not confirm exponential growth. Always TIME IT.

## Vulnerable Regex Patterns

### Nested Quantifiers (Most Common)
```
(a+)+$          # Nested plus -- classic ReDoS
(a*)*$          # Nested star
(a+)*$          # Star of plus
(a*)+$          # Plus of star
(a{1,}){1,}$   # Nested bounded quantifiers
```

### Overlapping Alternation
```
(a|a)+$         # Identical alternatives
(a|ab)+$        # Prefix overlap
(a|b|ab)+$      # Partial overlap
(\w|\d)+$       # \d is subset of \w -- overlap
```

### Quantified Groups with Optional Elements
```
(a+b?)+$        # Optional between repeated groups
(\s*,\s*)+$     # Common in CSV/list parsing
([^"]*"[^"]*")*[^"]*$  # Quote matching
```

### Dangerous Real-World Patterns
```
^([a-zA-Z0-9])(([\-.]|[_]+)?([a-zA-Z0-9]+))*$    # Email local part
^((https?|ftp):\/\/)?([\w.-]+)\.([a-z.]{2,6}).*$  # URL validation
^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$              # IP (safe but often combined)
```

## Evil String Construction

| Pattern | Evil String | Growth |
|---------|-------------|--------|
| `(a+)+$` | `"a" * N + "!"` | O(2^N) |
| `(a+b?)+$` | `"a" * N + "!"` | O(2^N) |
| `(a\|aa)+$` | `"a" * N + "!"` | O(2^N) |
| `([a-zA-Z]+)*$` | `"a" * N + "1"` | O(2^N) |
| `(\s+$)` | `" " * N + "x"` | O(N^2) quadratic |
| `(.*a){10}$` | `"a" * N + "!"` | O(N^10) polynomial |

**Key insight:** The evil string is N copies of a character the pattern CAN match, followed by one character it CANNOT. This forces the engine to try every possible split of the N characters across the quantifiers.

## Process

### Step 1: Find Regex Usage

```
# JavaScript/TypeScript
grep -rn "new RegExp\|RegExp(" . --include="*.js" --include="*.ts"
grep -rn "\.match(\|\.test(\|\.replace(\|\.search(\|\.split(" . --include="*.js" --include="*.ts"
grep -rn "/[^/]*[+*][^/]*[+*][^/]*/" . --include="*.js" --include="*.ts"

# Python
grep -rn "re\.compile\|re\.match\|re\.search\|re\.findall\|re\.sub" . --include="*.py"
grep -rn "re\.DOTALL\|re\.MULTILINE\|re\.VERBOSE" . --include="*.py"

# Ruby
grep -rn "Regexp\.new\|=~\|\.match\|\.scan\|\.gsub" . --include="*.rb"

# PHP
grep -rn "preg_match\|preg_replace\|preg_split" . --include="*.php"

# Java
grep -rn "Pattern\.compile\|\.matches(\|\.replaceAll(" . --include="*.java"
```

### Step 2: Identify Potentially Vulnerable Patterns

Look for these red flags:
1. **Nested quantifiers:** `(X+)+`, `(X*)*`, `(X+)*`, `(X*)+`
2. **Overlapping alternation:** `(a|a)+`, `(a|ab)+`
3. **Quantified group with internal repetition:** `(\s*,\s*)+`
4. **Unbounded repetition with anchor failure:** Pattern ends with `$` and input doesn't match
5. **User-controlled regex:** `new RegExp(userInput)` -- always exploitable

### Step 3: Mandatory Timing Measurement

```js
// Node.js timing test -- REQUIRED before reporting
const regex = /VULNERABLE_PATTERN/;

console.log('Length | Time (ms) | Ratio');
let prevTime = 0;
for (let len = 15; len <= 35; len++) {
  const evil = 'a'.repeat(len) + '!';
  const start = performance.now();
  regex.test(evil);
  const elapsed = performance.now() - start;
  const ratio = prevTime > 0 ? (elapsed / prevTime).toFixed(1) : '-';
  console.log(`${String(len).padStart(6)} | ${elapsed.toFixed(2).padStart(9)} | ${ratio}`);
  prevTime = elapsed;
}
```

**Interpretation:**
- Ratio ~2.0 per character = exponential (O(2^N)) = CONFIRMED ReDoS
- Ratio ~1.0 but time grows = likely polynomial = needs larger input test
- Ratio ~1.0 and time flat = linear = NOT ReDoS

### Step 4: Classify Severity

| Growth Rate | Ratio Pattern | Input for 1s Hang | Severity |
|-------------|---------------|-------------------|----------|
| O(2^N) exponential | ~2x per char | 25-30 chars | HIGH 7.5 |
| O(N^3+) polynomial | grows with input | 10K-100K chars | MEDIUM 5.3-6.5 |
| O(N^2) quadratic | grows slowly | 100K+ chars | LOW-MEDIUM |
| O(N) linear | constant ratio | never | NOT ReDoS |

### Step 5: Verify User Input Reaches Regex

The regex MUST be applied to user-controlled input. Check the full call chain:
1. Where does input enter? (HTTP param, form field, file content)
2. Is input truncated before regex? (length limit < 100 chars = likely safe)
3. Is there a regex timeout? (some libraries implement circuit breakers)
4. Is the regex applied in a worker/child process? (reduces impact to DoS of worker only)

## Language-Specific Notes

### JavaScript (V8 Engine)
- **No built-in regex timeout.** Catastrophic backtracking freezes the entire event loop.
- Single-threaded: one ReDoS hangs ALL request processing.
- `String.prototype.matchAll()` is lazy but still backtracks.
- V8 does NOT use RE2 for regex. All JS regex uses backtracking.

### Python
- **GIL blocks all threads.** ReDoS in one thread freezes the entire process.
- `re` module uses backtracking. No built-in timeout.
- `re2` package (Google RE2 bindings) is safe but rarely used.
- Python 3.11+ has some regex optimizations but is still vulnerable.

### Go
- **Uses RE2 engine.** Guarantees linear-time matching. NOT vulnerable to ReDoS.
- Exception: CGo bindings to PCRE (rare) ARE vulnerable.
- Skip Go targets unless they use PCRE bindings.

### Ruby
- Uses Oniguruma engine (backtracking). Vulnerable to ReDoS.
- Ruby 3.2+ added `Regexp.timeout=` global setting -- check if configured.
- `Regexp.timeout` defaults to nil (no timeout) unless explicitly set.

### PHP
- Uses PCRE (backtracking). Vulnerable to ReDoS.
- `pcre.backtrack_limit` defaults to 1,000,000 -- provides some protection.
- Check `ini_get('pcre.backtrack_limit')` -- if lowered, may limit impact.

### Java
- Uses backtracking engine. Vulnerable to ReDoS.
- No built-in timeout in `Pattern.compile()`.
- Can be mitigated with `Thread.interrupt()` but rarely done.

## CVSS Guidance

- Exponential backtracking, user input, event loop blocking: HIGH 7.5
- Exponential backtracking, authenticated only: MEDIUM 6.5
- Quadratic on user input requiring large payload (>10KB): MEDIUM 5.3
- Regex on bounded input (< 100 chars): usually not exploitable
- Regex with timeout/circuit breaker configured: reduced severity
- User-controlled regex pattern (`new RegExp(input)`): HIGH 7.5 (always exploitable)

## References

- [Sinks](references/sinks.md) -- Regex-heavy libraries and known vulnerable patterns
- [False Positive Indicators](references/false-positive-indicators.md)
- [PoC Skeleton](references/poc-skeleton.md)
