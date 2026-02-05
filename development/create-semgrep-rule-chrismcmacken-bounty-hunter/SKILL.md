---
name: create-semgrep-rule
description: Create custom Semgrep rules for vulnerability detection. Use when writing new rules for specific vulnerability patterns, creating org-specific detections, or building rules for novel attack vectors discovered during bug bounty hunting.
---

# Create Custom Semgrep Rules

Expert workflow for creating high-quality, low-false-positive Semgrep rules for security vulnerability detection.

## When to Create Custom Rules

Create custom rules when:
- Novel vulnerability patterns not covered by `p/default` or existing custom rules
- Org-specific code patterns (custom frameworks, internal APIs, coding conventions)
- Chained vulnerabilities requiring multi-step detection
- Language/framework-specific bugs (e.g., PHP `parse_url` bypass, Go unsafe patterns)
- High-value targets warranting deeper, targeted analysis
- **CVE variant hunting** - Finding the same vulnerable pattern in other codebases

## CVE-to-Rule Workflow

When creating rules from CVEs, the goal is to find the **underlying vulnerable code pattern** in OTHER codebases - NOT to detect the vulnerable library (SCA tools like Dependabot/Snyk do that better).

### Anti-Pattern: SCA-Style Detection (DON'T DO THIS)

```yaml
# WRONG - This is SCA work, not pattern detection
# Dependabot/Snyk already do this, and do it better
patterns:
  - pattern: require("loader-utils").parseQuery(...)
  - pattern: import { parseQuery } from "loader-utils"
  - pattern: require("vulnerable-package")
```

This approach:
- Duplicates what SCA tools already do
- Only finds the specific library, not the pattern
- Misses the same vulnerability in custom code
- Provides no value for bug bounty hunting

### Correct Approach: Pattern Detection

**Step 1: Fetch and analyze the fix commit**

```bash
# Get the patch diff
curl -s https://github.com/org/repo/commit/abc123.patch
```

Ask yourself:
- What was the **root cause** of the vulnerability?
- What **code pattern** made it exploitable?
- How did the fix **address** the root cause?
- What would this pattern look like in **custom code**?

**Step 2: Abstract the pattern**

The key question: "If a developer wrote similar functionality from scratch, what would the vulnerable version look like?"

Don't think about the library. Think about the **category of code** that has this problem.

**Step 3: Create a library-agnostic rule**

The rule should find the SAME MISTAKE anywhere, not just in the specific library.

### Example: CVE-2022-37601 (loader-utils Prototype Pollution)

**Fix commit analysis:**
```javascript
// BEFORE (vulnerable)
const result = {};           // Has prototype chain
result[key] = value;         // key could be "__proto__"

// AFTER (fixed)
const result = Object.create(null);  // No prototype chain
result[key] = value;                 // "__proto__" is just a regular key
```

**Root cause:** Query string parsing into `{}` with unsanitized dynamic keys.

**Abstracted pattern:** Any code that:
1. Creates an object with `{}` (not `Object.create(null)`)
2. Assigns properties using dynamic/user-controlled keys
3. Doesn't validate against `__proto__`, `constructor`, `prototype`

**Rule focus:** Find custom query parsers, config loaders, merge utilities, or any key-value processing with this antipattern.

**What to detect:**
```javascript
// DETECT: Custom query parser with same vulnerability
function parseConfig(input) {
  const config = {};                    // Vulnerable: has prototype
  for (const [key, val] of entries) {
    config[key] = val;                  // Unsanitized key assignment
  }
  return config;
}

// DETECT: Custom merge/extend function
function merge(target, source) {
  for (const key in source) {
    target[key] = source[key];          // Prototype pollution sink
  }
}
```

**What NOT to detect:**
```javascript
// SKIP: Using the library (SCA handles this)
const { parseQuery } = require("loader-utils");

// SKIP: Already using safe pattern
const result = Object.create(null);
result[key] = value;

// SKIP: Has prototype pollution guard
if (key === "__proto__" || key === "constructor") continue;
```

### CVE-to-Rule Checklist

Before writing the rule, verify:

| Check | Question |
|-------|----------|
| Root cause identified | What code pattern caused the vulnerability? |
| Pattern abstracted | Would I find this in custom code, not just the library? |
| Not SCA | Am I detecting a pattern, not a library import? |
| Realistic matches | Will this find bugs in real-world code? |
| Low FP rate | Are there clear safe patterns to exclude? |

### Common CVE Pattern Categories

| CVE Type | Root Cause Pattern | Rule Focus |
|----------|-------------------|------------|
| Prototype Pollution | `obj[userKey] = val` on `{}` | Custom parsers, merge functions |
| Template Injection | User input in template options | Custom template rendering |
| Command Injection | String concat to shell exec | Custom exec wrappers |
| Path Traversal | User input in file paths | Custom file handlers |
| SSRF | User input in URL construction | Custom HTTP clients |
| Deserialization | Untrusted data to deserializer | Custom data loaders |

## Rule Broadness: When Patterns Are Too Generic

Some vulnerability patterns are too common to detect without drowning in false positives. Before writing a rule, assess whether it will produce signal or noise.

### Pattern Frequency Spectrum

| Signal Level | Pattern Type | Example | Approach |
|--------------|--------------|---------|----------|
| **HIGH** | Rare sink + user input | `res.render(tpl, req.query)` | Direct detection, HIGH confidence |
| **MEDIUM** | Common pattern + specific context | `obj[key] = val` in loops | Audit rule, MEDIUM confidence |
| **LOW** | Ubiquitous pattern | `obj[key] = val` anywhere | Skip or sink-focused only |

### Example: Prototype Pollution

**Too broad (produces noise):**
```yaml
# This matches almost every JS file
pattern: $OBJ[$KEY] = $VALUE
```

**Specific enough (produces signal):**
```yaml
# Recursive descent pattern - characteristic of vulnerable merge functions
patterns:
  - pattern: $SMTH = $SMTH[$A]
  - pattern-inside: |
      for (...) { ... }
```

**Sink-focused (best signal):**
```yaml
# Detect where pollution becomes exploitable
pattern-sinks:
  - pattern: res.render($T, $OPTS)  # Template options = RCE
  - pattern: spawn($CMD, $ARGS, $OPTS)  # child_process options
```

### When to Use Audit vs Vuln Rules

| Rule Type | Confidence | Use Case |
|-----------|------------|----------|
| `subcategory: vuln` | HIGH | Rare pattern, clear exploit, few FPs |
| `subcategory: audit` | LOW-MEDIUM | Common pattern, needs manual review |

If you can't achieve HIGH confidence, mark the rule as `audit` with LOW confidence.
The official Semgrep registry does this for prototype pollution:

```yaml
metadata:
  subcategory: audit
  confidence: LOW
  likelihood: LOW
```

### Sink-Focused vs Pattern-Focused Rules

When a vulnerability pattern is too common to detect directly, focus on the **sinks** where it becomes exploitable:

| Vulnerability | Pattern-Focused (noisy) | Sink-Focused (high signal) |
|---------------|------------------------|---------------------------|
| Prototype Pollution | `obj[key] = val` | Template options, child_process options |
| XSS | String concatenation | `innerHTML`, `document.write` |
| SQLi | String + variable | `cursor.execute`, ORM raw queries |

**Rule of thumb:** If the source pattern is ubiquitous, detect at the sink instead.

## Project Structure

```
custom-rules/
├── 0xdea-semgrep-rules/     # Third-party: Memory safety, C/C++ vulns
├── open-semgrep-rules/      # Third-party: Multi-language security rules
├── web-vulns/               # Web-specific injection rules
└── custom/                  # YOUR custom rules
    ├── org-specific/        # Rules targeting specific organizations
    │   └── <org-name>/      # Per-org rule directories
    └── novel-vulns/         # Novel vulnerability patterns
```

## CRITICAL: Rule Quality Standards

Custom rules must meet these standards before use:
- **LOW false positive rate** - Every FP wastes time; add exclusions aggressively
- **Clear security impact** - Rule must detect exploitable vulnerabilities, not code smells
- **Tested against real code** - Validate on target repos before adding to pipeline
- **Complete metadata** - CWE, severity, confidence, references
- **Path exclusions for performance** - Exclude bundled/minified files to prevent timeouts

## CRITICAL: Path Exclusions for Performance

Taint mode rules are computationally expensive and will **timeout on large bundled/minified files**. Always add path exclusions to your rules.

### Required Path Exclusions

Add this `paths` block to EVERY rule (especially taint mode):

```yaml
rules:
  - id: my-taint-rule
    mode: taint
    paths:
      exclude:
        # Package managers
        - "**/node_modules/**"
        - "**/vendor/**"
        # Build output
        - "**/dist/**"
        - "**/build/**"
        # Minified/bundled files (specific patterns only)
        - "**/*.min.js"
        - "**/*.min.mjs"
        - "**/*.bundle.js"
        - "**/*.chunk.js"
        - "**/*.chunk.mjs"
        - "**/*-init.mjs"
        # NOTE: Do NOT use broad patterns like "**/js/*.js" or "**/assets/**"
        # as they exclude legitimate source files in some repos
    # ... rest of rule
```

### Why This Matters

| File Type | Typical Size | Taint Mode Behavior |
|-----------|-------------|---------------------|
| Source file | 1-50 KB | Fast analysis |
| Bundled JS | 100KB-2MB | **TIMEOUT** (30s default) |
| Minified JS | 50KB-500KB | **TIMEOUT** or very slow |

**Real example:** A 588KB Vite bundle (`viewer-init.mjs`) caused 3 timeout errors and blocked rule execution until path exclusions were added.

### Signs You Need More Exclusions

When running your rule, watch for:
```
Warning: 3 timeout error(s) in path/to/file.mjs when running rules...
Semgrep stopped running rules on path/to/file.mjs after 3 timeout error(s).
```

Add the problematic file pattern to your `paths.exclude` list.

## Workflow

### Step 1: Define the Vulnerability

Before writing any YAML, answer these questions:

```
Vulnerability Type: [e.g., Command Injection, SSRF, SQLi]
CWE ID: [e.g., CWE-78]
Security Impact: [e.g., Remote code execution as web server user]
Vulnerable Pattern: [e.g., os.system() with user-controlled input]
Exploit Scenario: [e.g., Attacker controls filename parameter, injects shell commands]
```

Find 2-3 real examples from target codebase to guide pattern creation.

### Step 2: Choose Rule Mode

| Mode | Use When | Example |
|------|----------|---------|
| **Pattern-based** | Single function calls, hardcoded values, dangerous API usage | `eval()`, hardcoded secrets, weak crypto |
| **Taint mode** | Data flows from user input to dangerous sink | SQLi, XSS, command injection, SSRF |

**Decision guide:**
- "Is user input involved?" → Taint mode
- "Is it a dangerous function regardless of input?" → Pattern mode
- "Do I need to track data across variables/functions?" → Taint mode

### Step 3: Write the Rule

#### Pattern-Based Rule Template

```yaml
rules:
  - id: <org>-<vuln-type>-<specific-pattern>
    languages:
      - python
    message: |
      <Clear description of what was detected and why it's dangerous>

      Remediation: <Specific fix recommendation>
    severity: ERROR  # ERROR, WARNING, or INFO
    metadata:
      cwe: "CWE-XX"
      owasp:
        - "A03:2021-Injection"
      category: security
      confidence: HIGH  # HIGH, MEDIUM, LOW
      author: "Your Name"
      references:
        - https://cwe.mitre.org/data/definitions/XX.html
    patterns:
      - pattern-either:
          - pattern: dangerous_function($ARG)
          - pattern: other_dangerous_function($ARG)
      - pattern-not: safe_wrapper(...)
      - pattern-not-inside: |
          if $X is None:
              ...
```

#### Taint Mode Rule Template

```yaml
rules:
  - id: <org>-<vuln-type>-taint
    mode: taint
    languages:
      - python  # or javascript, typescript, etc.
    # CRITICAL: Always include path exclusions for taint mode
    paths:
      exclude:
        - "**/node_modules/**"
        - "**/vendor/**"
        - "**/dist/**"
        - "**/build/**"
        - "**/*.min.js"
        - "**/*.min.mjs"
        - "**/*.bundle.js"
        - "**/*.chunk.js"
        - "**/*.chunk.mjs"
        - "**/*-init.mjs"
    message: |
      User input flows to <dangerous sink> without proper sanitization.
      This could allow <attack type>.

      Remediation: <Specific fix>
    severity: ERROR
    metadata:
      cwe: "CWE-XX"
      owasp:
        - "A03:2021-Injection"
      category: security
      confidence: HIGH
      author: "Your Name"
    pattern-sources:
      - pattern: request.args.get(...)
      - pattern: request.form[...]
      - pattern: request.json[...]
    pattern-sinks:
      - pattern: cursor.execute($QUERY, ...)
        focus-metavariable: $QUERY
    pattern-sanitizers:
      - pattern: escape(...)
      - pattern: int(...)
      - pattern: parameterized_query(...)
```

### Step 4: Reduce False Positives

This is the most critical step. For every rule, consider:

**Exclusion patterns to add:**
```yaml
# Exclude hardcoded/literal strings (not user input)
- pattern-not: $FUNC("...", ...)

# Exclude safe wrappers
- pattern-not: safe_execute(...)

# Exclude already-validated contexts
- pattern-not-inside: |
    if validate($INPUT):
        ...

# Exclude test files (if not already in .semgrepignore)
- pattern-not-inside: |
    def test_...:
        ...
```

**Common FP sources:**
- Hardcoded strings (not user-controlled)
- Test/example code
- Already-sanitized inputs
- Framework auto-escaping
- Admin-only code paths

### Step 5: Test the Rule

**Create test file alongside rule:**
```
custom-rules/custom/novel-vulns/
├── command-injection-eval.yml
└── command-injection-eval.py    # Test cases
```

**Test file format:**
```python
# ruleid: command-injection-eval
eval(user_input)

# ruleid: command-injection-eval
exec(request.args.get('code'))

# ok: command-injection-eval
eval("2 + 2")  # Hardcoded, safe

# ok: command-injection-eval
safe_eval(user_input)  # Uses sanitizer
```

**Run validation:**
```bash
# Test rule syntax and test cases
semgrep --config custom-rules/custom/novel-vulns/command-injection-eval.yml \
        --test custom-rules/custom/novel-vulns/

# Test against real target repo
semgrep --config custom-rules/custom/novel-vulns/command-injection-eval.yml \
        repos/<org>/<repo>/

# Count findings
semgrep --config custom-rules/custom/novel-vulns/command-injection-eval.yml \
        repos/<org>/ --json | jq '.results | length'
```

### Step 5b: Test Performance (CRITICAL for Taint Mode)

Taint mode rules can timeout on large files. Always test on repos with bundled JS:

```bash
# Test against a repo known to have bundled files
time semgrep --config my-rule.yaml repos/<org>/<repo-with-bundles>/ 2>&1 | grep -E "(timeout|Error|Ran)"
```

**Watch for these warning signs:**
```
Warning: 3 timeout error(s) in path/to/file.mjs when running rules...
```

**If you see timeouts:**

1. Check which files are causing issues:
   ```bash
   ls -la path/to/problematic/file.mjs  # Check file size
   head -c 200 path/to/problematic/file.mjs  # Check if minified
   ```

2. Add path exclusions to your rule:
   ```yaml
   paths:
     exclude:
       - "**/path/pattern/*.mjs"
   ```

3. Re-test until no timeouts:
   ```bash
   # Should complete in seconds, not timeout
   time semgrep --config my-rule.yaml repos/<org>/<repo>/
   ```

**Performance targets:**
| Repo Size | Expected Time | Action if Slower |
|-----------|--------------|------------------|
| Small (<100 files) | < 5 seconds | Check for bundled files |
| Medium (100-1000 files) | < 30 seconds | Add path exclusions |
| Large (1000+ files) | < 2 minutes | Verify exclusions working |

**Verify findings still work after exclusions:**
```bash
# Run on source directory only (where real vulns are)
semgrep --config my-rule.yaml repos/<org>/<repo>/src/
```

### Step 6: Integrate with Pipeline

Rules in `custom-rules/` are automatically included when running:
```bash
./scripts/scan-semgrep.sh <org-name>
```

To use only your custom rule:
```bash
semgrep --config custom-rules/custom/novel-vulns/my-rule.yml repos/<org>/
```

## Pattern Operators Reference

### Basic Matching

| Operator | Purpose | Example |
|----------|---------|---------|
| `pattern` | Match exact code | `os.system($CMD)` |
| `pattern-either` | Match any (OR) | Multiple dangerous functions |
| `patterns` | Match all (AND) | Function + constraint |

### Metavariables

| Syntax | Meaning |
|--------|---------|
| `$VAR` | Capture any expression |
| `$_` | Match anything (no capture) |
| `$...ARGS` | Match multiple arguments |
| `<... $X ...>` | Match $X nested at any depth |
| `...` | Match any statements between |

### Exclusions (Critical for FP reduction)

```yaml
pattern-not: safe_function(...)           # Exclude specific pattern
pattern-not-inside: |                     # Exclude if inside context
  if validated($X):
      ...
```

### Metavariable Constraints

```yaml
# Regex match on captured variable
metavariable-regex:
  metavariable: $FUNC
  regex: "(system|exec|popen)"

# Pattern match on captured variable
metavariable-pattern:
  metavariable: $ARG
  pattern-either:
    - pattern: request.args[...]
    - pattern: request.form[...]

# Entropy analysis (detect secrets)
metavariable-analysis:
  analyzer: entropy
  metavariable: $VALUE

# Highlight specific variable in output
focus-metavariable: $DANGEROUS_ARG
```

### Taint Mode Operators

```yaml
mode: taint                    # Enable taint tracking

pattern-sources:               # Where tainted data enters
  - pattern: request.args[...]

pattern-sinks:                 # Where tainted data causes harm
  - pattern: cursor.execute($Q)
    focus-metavariable: $Q

pattern-sanitizers:            # Functions that clean data
  - pattern: escape(...)
  - pattern: int(...)

pattern-propagators:           # Custom taint spread (Pro only)
  - pattern: $TO = transform($FROM)
    from: $FROM
    to: $TO
```

## Common Rule Patterns

### Command Injection
```yaml
patterns:
  - pattern-either:
      - pattern: os.system($CMD)
      - pattern: os.popen($CMD)
      - pattern: subprocess.call($CMD, shell=True, ...)
      - pattern: subprocess.Popen($CMD, shell=True, ...)
  - pattern-not: $FUNC("...", ...)  # Exclude hardcoded strings
```

### SQL Injection (Taint)
```yaml
mode: taint
pattern-sources:
  - pattern: request.$METHOD[...]
  - pattern: request.$METHOD.get(...)
pattern-sinks:
  - pattern: $CURSOR.execute($QUERY, ...)
  - pattern: $CURSOR.executemany($QUERY, ...)
pattern-sanitizers:
  - pattern: $CURSOR.execute("...", ($PARAM,))  # Parameterized
```

### Hardcoded Secrets
```yaml
patterns:
  - pattern: $VAR = "..."
  - metavariable-regex:
      metavariable: $VAR
      regex: "(?i)(password|secret|api_key|token|private_key)"
  - metavariable-analysis:
      analyzer: entropy
      metavariable: $VAR
  - pattern-not-inside: |
      # Example: ...
```

### Insecure Cryptography
```yaml
pattern-either:
  - pattern: hashlib.md5(...)
  - pattern: hashlib.sha1(...)
  - pattern: DES.new(...)
  - pattern: Blowfish.new(...)
  - pattern: ARC4.new(...)
```

### Path Traversal
```yaml
mode: taint
pattern-sources:
  - pattern: request.args.get("...")
  - pattern: request.form["..."]
pattern-sinks:
  - pattern: open($PATH, ...)
  - pattern: os.path.join(..., $PATH, ...)
pattern-sanitizers:
  - pattern: os.path.basename(...)
  - pattern: secure_filename(...)
```

## Metadata Standards

Every rule MUST include:

```yaml
metadata:
  # Required
  cwe: "CWE-78"                      # Primary CWE ID
  category: security                  # Always "security" for vulns
  confidence: HIGH                    # HIGH, MEDIUM, LOW

  # Recommended
  owasp:
    - "A03:2021-Injection"           # OWASP Top 10 2021
  likelihood: HIGH                    # Exploitation probability
  impact: HIGH                        # Damage if exploited
  subcategory:
    - vuln                           # vuln, audit, guardrail

  # For custom rules
  author: "Your Name"
  created: "2025-01-15"
  tested_against: "org-name"         # Where you validated it
  references:
    - https://cwe.mitre.org/...
    - https://blog.example.com/...   # Writeups explaining the vuln
```

## Severity Guidelines

| Severity | Use For | Examples |
|----------|---------|----------|
| `ERROR` | Exploitable vulns with high impact | RCE, SQLi, auth bypass |
| `WARNING` | Likely vulns needing verification | Potential XSS, weak crypto |
| `INFO` | Code smells, audit points | Missing headers, debug code |

## Pro Engine Features

When running with `--pro` (our default), you get:
- **Cross-file taint tracking** - Follow data across imports
- **Interprocedural analysis** - Track through function calls
- **Field sensitivity** - Track object properties

These are automatic; no rule changes needed.

## Debugging Rules

**Rule not matching expected code?**
```bash
# Verbose output shows matching attempts
semgrep --config rule.yml target/ --debug

# Test specific pattern interactively
semgrep --pattern 'os.system($X)' target/
```

**Too many false positives?**
- Add `pattern-not` for safe patterns
- Add `pattern-not-inside` for safe contexts
- Use `metavariable-regex` to constrain variable names
- Lower `confidence` in metadata if FPs are expected

## Output

Save completed rules to:
```
custom-rules/custom/
├── org-specific/<org-name>/    # Org-targeted rules
└── novel-vulns/                # General novel patterns
```

Rules are automatically picked up by `./scripts/scan-semgrep.sh`.

## References

- [Semgrep Rule Syntax](https://semgrep.dev/docs/writing-rules/rule-syntax/)
- [Taint Mode Overview](https://semgrep.dev/docs/writing-rules/data-flow/taint-mode/overview)
- [Advanced Taint Techniques](https://semgrep.dev/docs/writing-rules/data-flow/taint-mode/advanced)
- [Semgrep Playground](https://semgrep.dev/playground/) - Interactive rule testing
