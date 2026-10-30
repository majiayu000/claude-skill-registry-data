---
name: redos
description: Detects regex patterns vulnerable to catastrophic backtracking on crafted
  inputs. Use when writing regular expressions that will be applied to user-
  supplied input. Also invoke when compiling regexes from external
  configuration, building input validation patterns, or parsing untrusted
  strings with regex.
---

# ReDoS Security Check (CWE-1333)

## What this checks

Protects against Regular Expression Denial of Service where a crafted input causes
catastrophic backtracking in regex engines. A single malicious string can pin a CPU
core for minutes or hours, taking down the service.

## Vulnerable patterns

- Nested quantifiers applied to user input — a quantified group whose body is itself quantified produces exponential state
- Overlapping alternation inside repetition — alternatives that can match the same prefix multiply backtracking work
- Common "email" or "URL" regexes built from quantified character classes wrapped in further repetition
- Regexes compiled from external configuration or user input where the pattern shape itself is attacker-controlled

## Fix immediately

Flag the vulnerable regex, explain the risk, and suggest a fix establishing these
properties. Translate the principle to the language and engine of the audited file —
do not echo examples from another stack.

1. **No nested quantifiers on user input.** Collapse a quantified group whose body is also quantified into a single quantifier. Rewrite alternations so alternatives cannot match the same prefix.
2. **Prefer a linear-time regex engine when one is available** for the language under review. Engines that disallow backtracking guarantee linear matching regardless of pattern shape.
3. **Bound regex execution.** When the engine supports it, set a match timeout or run the match on a cancellable worker; when it does not, simplify the pattern until worst-case input completes in bounded time.
4. **Treat patterns sourced from configuration or user input as untrusted.** Either pre-compile a fixed allowlist of patterns, or run user-supplied patterns on a sandbox engine with a hard timeout.

## Verification

- [ ] No regex applied to user input contains nested quantifiers or alternation inside repetition where alternatives share a prefix
- [ ] If the language offers a linear-time engine, the audited code uses it for user-input regexes; otherwise patterns are simplified or execution is time-bounded
- [ ] Regex patterns loaded from external configuration or user input run against an allowlist or under an enforced timeout

## References

- CWE-1333 ([Inefficient Regular Expression Complexity](https://cwe.mitre.org/data/definitions/1333.html))
- CWE-400 ([Uncontrolled Resource Consumption](https://cwe.mitre.org/data/definitions/400.html))
