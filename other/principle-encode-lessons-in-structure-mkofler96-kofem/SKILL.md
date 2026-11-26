---
name: principle-encode-lessons-in-structure
description: "Apply when you catch yourself writing the same instruction a second time, or notice a recurring correction. Encode the rule as a lint, metadata flag, runtime check, or script instead of more text."
---

# Encode Lessons in Structure

When the same instruction or correction comes up a second time, encode it as a lint, metadata flag, runtime check, or script instead of more text. In KoFEM that is usually a `web/eslint-rules/` rule, a Clippy lint, a type, or a test.

If the lesson needs judgment and cannot be encoded, make the instruction more prominent and add an example of the failure mode.

**Corollary:** If the fix is structural, only use the structural fix. The instruction is the symptom.
