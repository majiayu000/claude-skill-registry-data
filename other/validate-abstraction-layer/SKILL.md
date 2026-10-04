---
name: validate-abstraction-layer
description: Scan product-stage artifacts (research/, specification/, scope/) for abstraction-layer deny-list tokens — specific database engines, SDK method names, framework identifiers, programming-language type signatures, wire-level protocol identifiers, cryptographic constructions, and model version strings. Deterministic grep-based linter. Called by any producer skill (configure-capabilities, enrich-capabilities, generate-intent-epics, recommend-mvp) after writing an artifact, and as a close-phase check by the specify play.
user-invocable: false
model: haiku
allowed-tools: Read, Write, Grep, Glob
deprecated: true
deprecated_note: '#434 ProductOS realignment — superseded by the command model; retained for Phase E reference, not installed'
---

# validate-abstraction-layer

Deterministic linter that enforces Rule 14 (Abstraction-Layer Boundary, Defect 7) across product-stage artifacts. Implements the "cite the pattern, not the tool" discipline by scanning written files for a deny-list of tech-binding tokens and returning a structured violation list.

## Purpose

Product-stage artifacts under `.garura/product/research/`, `.garura/product/specification/`, and `.garura/product/scope/` are implementation-agnostic. They describe domain shape, market opportunity, scope decisions, and epic outcomes — not how the work is built. Implementation choices (runtime, framework, database, library, schema design, API wire format, cryptographic construction, model version) need cross-domain tradeoff analysis and user approval at Stage 6 architecture. Leaking them into earlier artifacts prejudges architecture and breaks the stage contract.

This skill is a post-write check. Producer skills invoke it after writing an artifact; if it returns violations, the producer deletes the file and halts with a structured failure. The specify play invokes it at close as a final sanity check across all product/ files. The skill is deterministic — no LLM reasoning, just a regex scan against a maintained deny-list — so it can run in CI pipelines without cost or latency concerns.

## Input

Receive from the calling agent or skill via the JSON contract. All paths resolve against `{product_base}` supplied by the caller — do not hard-code `.garura/product/` or assume a working directory.

- `scan_paths` (list, required) — list of file paths OR directory paths to scan. Each entry is either a specific file (scan just that file) or a directory (recursively scan every `.md` and `.yaml` file in that directory). Typical usage patterns:
  - Single file: `["{product_base}scope/scope.yaml"]` (post-write check from a producer skill)
  - Directory: `["{product_base}research/", "{product_base}specification/", "{product_base}scope/"]` (close-phase sweep from specify)
- `deny_list_path` (path, optional) — path to a YAML file with the deny-list tokens. When null, the skill uses the baked-in default deny-list documented in the Constants section below. Custom deny-lists let product teams extend or customize the rule for their specific pipeline — the baked-in default is the canonical framework rule.
- `output_path` (string, required) — where to write the structured violation report. Typically `{stm_base}/{issue}/evidence/validate-abstraction-layer/{YYYYMMDD-HHMMSS}.yaml` or for specify close-phase, `{product_base}_evidence/specify/abstraction-layer-audit.yaml`.
- `fail_on_violation` (boolean, optional, default true) — when true, any violation flips the output status to `failed` and the calling skill should halt. When false, violations are reported but status remains `passed` (useful for advisory runs or pre-commit checks where the author wants to see the violations before deciding whether to rewrite).

## Constants — Default Deny-List

The baked-in default deny-list is organized by category. Each entry is a regex pattern, a violation category, and a severity. Match is case-insensitive unless explicitly noted.

### Category: Database Engines

Pattern → Violation: specific database product name in a product-stage artifact.

- `\b(PostgreSQL|Postgres|MySQL|MariaDB|SQLite|DynamoDB|MongoDB|Cassandra|Redis|Memcached|Elasticsearch|OpenSearch|ClickHouse|CockroachDB|Neo4j|Snowflake|BigQuery|Redshift|Athena|RDS|Aurora|Fauna|Supabase|PlanetScale|PocketBase|Firestore|Firebase)\b`
- Exception: match inside a fenced code block tagged `text` (ASCII wireframe) or `markdown` is NOT a violation — those are illustrative, not committing. Match outside fenced blocks IS a violation.

### Category: SDK Method Names and Parameters

Pattern → Violation: specific method signatures from framework SDKs.

- `\b(query\(\)|fetch\(\)|useState\(|useEffect\(|createClient\(|createStore\(|createRouter\(|ref\(|reactive\(|defineComponent\(|withRouter\()\b`
- `\b(temperature\s*=\s*\d|output_format\s*=|resume\s*=|max_tokens\s*=|top_p\s*=|top_k\s*=|seed\s*=)\b`
- `\b(axios\.get|fetch\(|XMLHttpRequest|\$\.ajax|Http\.get)\b`
- Exception: same as above — fenced code blocks tagged `text` or `markdown` are exempt.

### Category: Framework Identifiers

Pattern → Violation: specific framework or library name.

- `\b(React|Vue\.js|Vue 3|Angular|Svelte|SolidJS|Qwik|Ember|Backbone|Astro|Next\.js|Nuxt\.js|Remix|SvelteKit|Gatsby|Eleventy|Hugo|Jekyll)\b`
- `\b(AntDesign|Ant Design|MaterialUI|Material UI|Tailwind|TailwindCSS|Bootstrap|shadcn|Chakra|ChakraUI|Radix|Headless UI|DaisyUI|PrimeReact|Mantine)\b`
- `\b(Express|Koa|Fastify|Hapi|NestJS|FastAPI|Flask|Django|Rails|Sinatra|Laravel|Symfony|Spring|Spring Boot|Quarkus|Micronaut|Gin|Echo|Fiber|Actix)\b`
- `\b(LangChain|LangGraph|LlamaIndex|CrewAI|AutoGen|Haystack|Semantic Kernel|Guidance|DSPy|Instructor|Marvin)\b`
- Exception: market-brief.md is exempt from the competitor-mention deny-list — it MUST name competitors. Specifically, `market-brief.md` skips this category. The skill detects market-brief.md by filename and applies the exemption.

### Category: Programming Language Type Signatures

Pattern → Violation: code snippets with language-specific type syntax.

- `\b(class|interface|struct|enum|type|def|func|fn|sub|proc)\s+[A-Z]\w+` (class/interface/type declarations)
- `(public|private|protected|internal|abstract|static|async)\s+(class|interface|function|def|fn)\b`
- `\bextends\s+\w+\s*\{` / `\bimplements\s+\w+\s*\{`
- `::\s*\w+` (C++/Rust scope resolution)
- `->\s*\w+\s*$` (Python/PHP type hints)
- `<\s*T\s*>` / `<\s*\w+\s*>` (generic type parameters outside text)
- Exception: fenced code blocks tagged `text`, `markdown`, or a language NOT in the above list are exempt — they're illustrative.

### Category: Wire-Level Protocol Identifiers

Pattern → Violation: specific wire-level protocol, endpoint path, or method signature.

- `\b(GET|POST|PUT|PATCH|DELETE|HEAD|OPTIONS)\s+/\w+` (REST endpoint declarations)
- `\b(gRPC|GraphQL|WebSocket|SSE|RPC)\b` (wire protocol names when used as tech choices — not when used descriptively)
- `\/api\/v\d+\/` (versioned API paths)
- `\b(protobuf|Protocol Buffers|Avro|Thrift|MessagePack|CBOR|FlatBuffers)\b` (serialization formats as tech choices)
- Exception: fenced blocks, and paths that are clearly example URLs in prose (e.g., "the scoring source returns its data over a standard web interface").

### Category: Cryptographic Constructions

Pattern → Violation: specific hash/encryption construction.

- `\b(sha256\(|sha512\(|md5\(|bcrypt\(|scrypt\(|argon2\(|pbkdf2\()\b`
- `\b(AES-\d+|ChaCha20|RSA-\d+|ECDSA|Ed25519|HMAC-SHA\d+)\b`
- `\b(prev_hash\s*\|\||this_hash\s*=)` (hash chain construction details)
- Exception: generic references to "argon2id" or "bcrypt" as a standard in constraint language (e.g., "password hashing uses argon2id") are a BORDERLINE case. The rule: if it specifies a named standard that the product MUST comply with (like "WCAG 2.1 AA"), it's allowed. If it specifies the specific CONSTRUCTION the implementation uses (like "sha256(prev_hash || ...)"), it's forbidden. The skill uses a heuristic: if the token appears in an epic's `constraints.security.value` field with a `source_for_quantification`, it's allowed; if it appears in a schema example, prose description, or wireframe block, it's forbidden.

### Category: Model Version Strings

Pattern → Violation: specific model identifiers.

- `\bclaude-[a-z0-9\-]+\b` (all claude model IDs)
- `\bgpt-[0-9a-z\-]+\b` (all GPT model IDs)
- `\b(opus|sonnet|haiku|turbo|mini|flash|pro|ultra)-\d+[-.]\d+\b` (model tier + version)
- `\b(gemini|llama|mistral|mixtral|qwen|deepseek|grok|phi)-[0-9a-z\-]+\b`
- Exception: the skill's own frontmatter `model:` field is allowed; that's the skill-to-runtime binding for the skill itself.

## Process

Resolve each input path by substituting `{product_base}` from the incoming JSON contract; do not re-prefix with `.garura/product/` or assume a working directory.

### 1. Load the deny-list

- If `deny_list_path` is provided, parse the YAML file into a list of `{category, pattern, severity, exception_rule}` entries.
- Otherwise, use the baked-in default deny-list from the Constants section above.
- Validate that every pattern compiles as a valid regex. If any pattern is malformed, halt with `what_failed: invalid_deny_list` and the failing pattern.

### 2. Expand scan paths

For each entry in `scan_paths`:

- If it's a file path, add it to the scan queue.
- If it's a directory path, recursively glob for `*.md` and `*.yaml` files under it and add each to the scan queue.
- Exclude `.garura/product/_checkpoints/`, `.garura/product/_evidence/`, `.garura/product/_status/` by default — those are lifecycle files, not product-stage artifacts, and may legitimately contain tech references in evidence reports.
- Exclude `.garura/product/user-provided/` — user inputs are whatever the user wrote, not pipeline output.
- Build the final scan queue as an explicit list of file paths.

### 3. Scan each file

For each file in the queue:

1. Read the file contents.
2. Split the contents into sections: `prose` (normal markdown text), `fenced_text` (fenced code blocks tagged `text` or `markdown` or untagged), `fenced_code` (fenced code blocks tagged with a programming language), `yaml_front_matter` (frontmatter).
3. For each deny-list entry, scan the `prose` section(s) for the regex pattern. Apply the exception rules documented per category (e.g., market-brief.md exempt from framework-name category; epic `constraints.security.value` fields exempt from crypto-construction category).
4. For `fenced_code` sections (tagged with a specific language), scan with ALL categories applied — these are almost always violations because they contain code that commits to a language and framework.
5. For `fenced_text` sections (tagged `text` or `markdown` or untagged), apply a RELAXED rule: only the Model Version Strings category fires in fenced_text (because even an ASCII wireframe should not name `claude-sonnet-4-6`). Database engines, framework identifiers, etc. in `fenced_text` are exempt — they may appear in illustrative diagrams.
6. Record every match as a violation with: `file_path`, `line_number`, `column`, `category`, `matched_token`, `context_line` (the line containing the match), `severity`.

### 4. Apply file-specific exemptions

The skill has a hard-coded list of file-specific exemptions based on filename heuristics:

- `market-brief.md` — exempt from Framework Identifiers and Database Engines categories because it names competitors and industry tools as part of the competitive landscape.
- `research/{domain}.md` — exempt from Framework Identifiers when the match is in a "Primary Sources" or "Industry Framing" section AND the match is a framework name cited as an industry reference (e.g., "LangChain" as a reference in an agentic research file is allowed because it's citing industry precedent, not committing to use).

For each matched violation, check if the file + match context matches an exemption. Exempted matches are still recorded in the output but tagged with `exempted: true` and a `exemption_reason`. The `failed` status is computed from non-exempted violations only.

### 5. Write the violation report

Write a YAML file to `output_path` with this shape:

```yaml
validation:
  skill: validate-abstraction-layer
  run_at: <ISO-8601 timestamp>
  scan_paths: <echoed input>
  files_scanned: <int>
  files_with_violations: <int>
  total_violations: <int>
  exempted_violations: <int>
  blocking_violations: <int>  # total - exempted
  status: passed | failed

  deny_list:
    source: "baked-in default" | "{deny_list_path}"
    categories: [<list of category names>]

  violations:
    - file_path: <string>
      line_number: <int>
      column: <int>
      category: <string>
      matched_token: <string>
      context_line: <string>
      severity: blocker | warning
      exempted: <bool>
      exemption_reason: <string or null>

by_category:
  database_engines: <int>
  sdk_method_names: <int>
  framework_identifiers: <int>
  programming_language_type_signatures: <int>
  wire_level_protocols: <int>
  cryptographic_constructions: <int>
  model_version_strings: <int>

by_severity:
  blocker: <int>
  warning: <int>
```

### 6. Return the output contract

```yaml
validate_abstraction_layer:
  status: passed | failed
  files_scanned: <int>
  blocking_violations: <int>
  report_path: <output_path>
  exit_code: 0 | 1  # 0 = passed, 1 = failed (for pre-commit hook wiring)
```

If `fail_on_violation: true` AND `blocking_violations > 0`, the status is `failed` and the caller should halt its own process. The caller's typical pattern after receiving a `failed` response:

1. DELETE the file it just wrote (so it doesn't commit a violating artifact)
2. Re-enter its narrative-generation step with the violation list as additional context (e.g., "avoid naming specific databases — use 'append-only ledger' instead")
3. Retry up to 2 times before halting with `what_failed: abstraction_layer_violation_unresolved`

## Constraints

- NEVER modify the scanned files. This skill is read-only on the scan paths and write-only on the `output_path`.
- NEVER invent deny-list categories not documented here or in a provided `deny_list_path`. Every category must be documented so that authors writing to these files can predict what will fail.
- NEVER silently expand exemptions. If a match is exempted, the output MUST record `exempted: true` with a human-readable `exemption_reason`. An auditor reading the report must be able to verify every exemption.
- NEVER fire a false positive without a way to mark it as an exemption. If a legitimate match is getting flagged (e.g., an epic constraint that cites "OWASP ASVS Level 2" for a security standard), the skill must recognize it via the exemption rules. If it doesn't, the fix is to extend the exemption rules, not suppress the category.
- NEVER scan files outside the declared `scan_paths`. Directory-level entries in `scan_paths` recurse, but the skill does not walk into sibling directories.
- ALWAYS produce the full violation report even when status is `passed`. Callers may want to see exempted matches for auditing.
- ALWAYS be deterministic. The same input (same files, same deny-list) produces the same output. No LLM-based reasoning; this is a regex linter.
- ALWAYS honor the `fail_on_violation: false` mode. In advisory mode, the report is written but the caller does not halt.
- ALWAYS handle non-existent files in `scan_paths` gracefully. Record them as `files_not_found` in the report rather than halting — the calling skill may be passing paths that haven't been written yet.

## Version

| Field | Value |
|-------|-------|
| Version | 0.1.0 |
| Category | validation |
| Created | 2026-04-15 |
| Related | `core/components/memory/standards/rules/product.md` (Rule 14 Abstraction-Layer Boundary), `core/components/plays/specify/reference/intent.yaml` (C16 / F13), `core/components/skills/configure-capabilities/SKILL.md` (caller), `core/components/skills/enrich-capabilities/SKILL.md` (caller), `core/components/skills/generate-intent-epics/SKILL.md` (caller), `core/components/skills/recommend-mvp/SKILL.md` (caller) |
