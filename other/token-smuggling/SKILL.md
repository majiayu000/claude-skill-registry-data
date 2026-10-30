---
name: token-smuggling
description: Detects user input passed to LLMs without Unicode normalization, allowing RTL
  overrides, zero-width joiners, and homoglyph attacks. Use when writing code
  that passes user-supplied strings to an LLM, constructs prompts from
  external data, or processes text that may contain Unicode control
  characters, homoglyphs, or invisible formatting characters.
---

# Token Smuggling / Unicode Injection (LLM01:2025)

## What this checks

Detects user input passed to LLMs without Unicode normalization. Attackers embed RTL
override characters, zero-width joiners, or homoglyphs to manipulate prompt structure,
bypass keyword filters, or make malicious instructions appear legitimate.

## Vulnerable patterns

- User input interpolated into a prompt with no normalization step at the trust boundary
- Blocklists or keyword filters that compare against pre-normalized text, letting homoglyph variants pass
- Retrieved RAG content or tool outputs concatenated into a prompt on a path the sanitizer does not cover
- Comparisons on raw bytes where bidirectional overrides or zero-width characters can split or hide tokens

## Fix immediately

Flag the vulnerable code, explain the risk, and suggest a fix establishing these
properties. Translate to the Unicode library or runtime APIs of the audited file — use
that stack's documented NFKC normalization and character-class predicates; do not
import a recipe from a different stack.

1. **User input is NFKC-normalized before it reaches any prompt or blocklist comparison.** NFKC collapses compatibility forms and canonical equivalents, so homoglyphs, fullwidth digits, and ligatures fold to their ASCII counterparts. Normalization runs once, at the trust boundary — not scattered per call site.
2. **Unicode control and invisible formatting characters are stripped after normalization.** Bidirectional overrides (`U+202A`–`U+202E`), zero-width space/joiner (`U+200B`–`U+200D`), word joiner (`U+2060`), and BOM (`U+FEFF`) do not survive into the prompt. These are the characters attackers use to hide instructions or split keywords.
3. **Security-sensitive comparisons (blocklists, keyword filters, domain allowlists) run on normalized input**, not on the raw bytes. A filter that checks for a string but runs on pre-normalized text lets the homoglyph variant pass.
4. **The same helper runs on every ingress path** — direct user input, retrieved RAG content, tool outputs. Attackers move the payload wherever the sanitizer does not run.

## Verification

- [ ] User input is normalized with NFKC before inclusion in any LLM prompt
- [ ] Unicode control and invisible formatting characters are stripped before prompt construction
- [ ] Security-sensitive string comparisons (blocklists, keyword filters) run on normalized input
- [ ] All ingress paths — direct input, retrieved content, tool outputs — pass through the same sanitization helper

## References

- CWE-116 ([Improper Encoding or Escaping of Output](https://cwe.mitre.org/data/definitions/116.html))
- CWE-20 ([Improper Input Validation](https://cwe.mitre.org/data/definitions/20.html))
- [OWASP LLM01:2025 Prompt Injection](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
