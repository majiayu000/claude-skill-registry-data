---
name: numeric-trust-boundary
description: Detects untrusted numeric input that flows through a conversion, cast, or parser into a length, size, index, or authorization comparison without bounds-checking the post-conversion value. Use when writing or modifying code that calls atoi/strtol/parseInt/strconv.Atoi on user-supplied or network-supplied input, casts between signed and unsigned integer types, narrows an integer width before a bounds check, or uses an untrusted integer as an allocation size, array index, file offset, length argument to memcpy, or comparison gate for authorization or permission decisions.
---

# Numeric Trust Boundary (CWE-190, CWE-194, CWE-704, CWE-20)

## What this checks

Plain numeric-conversion bugs (parser returns zero on garbage, divide-by-zero,
float equality) are correctness issues that standard linters catch. This skill
targets the security subset: an untrusted integer (from a string parser, a
wire-protocol length field, a JSON number) that flows into a length, size,
index, or permission sink without a bounds check on the post-conversion value.
Local pattern only — conversion within a function or two of the sink.

## Vulnerable patterns

- Sign-extension when a narrow signed value is cast into a width-or-size type — a byte of `0xFF` becomes a huge unsigned length.
- A string-to-integer parser whose error indicator is the same value as legitimate zero, used as an authorization or identity key without checking the parse-failure flag.
- Width truncation inside a bounds check — the narrowed value passes the check, but the full-width value is used at the sink.
- Signed/unsigned comparison where a negative value compares as smaller-than the bound, then gets re-promoted to a giant unsigned at the sink.
- Attacker-controlled divisor with no zero check.
- Length arithmetic (`count * sizeof(...)`) on attacker-controlled values that wraps around to a small total while the unwrapped value is later used at the sink.
- Array or buffer indexing where the parsed value is never bounded against the actual length.

## Fix immediately

Flag the vulnerable code and explain the risk. Then suggest a fix that establishes
these properties. Translate each property into the audited file's language and
standard library — do not import an example from a different stack.

1. **Use a parser that signals failure out-of-band**, distinct from a valid zero. Check the failure indicator (errno, exception, error return, optional) before consuming the value.
2. **Bound the parsed value against the sink's required range *after* conversion to the sink's type.** A check performed on the original narrow type does not protect a wider sink.
3. **Reject negatives explicitly when the sink is an unsigned length, size, or index.** Do not rely on the comparison operator to do this — signed-to-unsigned promotion flips the meaning.
4. **Guard multiplications used to compute lengths against wraparound** before the multiplication is performed. Compare the operands against the type's maximum divided by the other operand.
5. **Treat any attacker-controlled divisor or modulus as potentially zero** and reject before the divide.

## Verification

After rewriting, confirm:

- [ ] Every conversion of untrusted input checks for parser failure via an out-of-band signal (errno, exception, error return) — a zero return is not treated as a valid integer
- [ ] Every value used as an allocation size, array index, or length argument is checked against a bound *after* conversion to the type the sink expects
- [ ] No bounds check uses a narrower type than the value being checked at the sink
- [ ] Signed/unsigned comparisons are avoided, or both sides are explicitly converted to the same type before comparison
- [ ] Length arithmetic on attacker-controlled values is guarded against wraparound before the multiplication
- [ ] Attacker-controlled divisors and modulus operands are checked against zero

## References

- CWE-190 ([Integer Overflow or Wraparound](https://cwe.mitre.org/data/definitions/190.html))
- CWE-194 ([Unexpected Sign Extension](https://cwe.mitre.org/data/definitions/194.html))
- CWE-704 ([Incorrect Type Conversion or Cast](https://cwe.mitre.org/data/definitions/704.html))
- CWE-20 ([Improper Input Validation](https://cwe.mitre.org/data/definitions/20.html))
