---
name: fuzz-testing
description: "Fuzz testing protocols, randomized input generation, crash reproduction, and memory sanitizers."
---

# Fuzz Testing Protocol

1. Supply unexpected, malformed, and boundary inputs to public parsers.
2. Run continuously in CI using tools like go-fuzz, cargo-fuzz, or libFuzzer.
3. Archive crash-producing inputs as permanent regression test cases.
