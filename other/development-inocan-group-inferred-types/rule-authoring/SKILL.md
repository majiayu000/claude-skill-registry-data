---
name: rule-authoring
description: Create or update inspequte analysis rules and harness-based tests. Use when adding new rules, modifying rule metadata, or writing JVM harness tests for rules in src/rules/*.rs.
---

# Rule authoring (inspequte)

## Workflow
1) Define rule metadata: unique `id`, clear `name`, and short `description`.
2) Implement `Rule::run` using `AnalysisContext` and helpers from `crate::rules` (ex: `result_message`, `method_location_with_line`, `class_location`).
3) Add harness tests in the same rule file (`#[cfg(test)]`): compile Java sources with `JvmTestHarness`, analyze, then assert on `rule_id` and message text.
4) Register the rule in `src/rules/mod.rs` and `src/engine.rs` if it is new.
5) Keep output deterministic (results are sorted by `rule_id`/message; avoid non-deterministic ordering in rule code).

See `references/rule-checklist.md` for a compact checklist.

## Harness testing
- Use `JvmTestHarness::new()`; it requires `JAVA_HOME` (Java 21).
- Prefer local stub sources over downloading jars.
- Filter SARIF results by `rule_id` for assertions.
- Cover both happy-path and edge cases: include cases that should report, cases that should not report (false positives), and cases that should not miss reports (false negatives).

### Harness test template
```rust
let harness = JvmTestHarness::new().expect("JAVA_HOME must be set for harness tests");
let sources = vec![SourceFile {
    path: "com/example/Sample.java".to_string(),
    contents: r#"
package com.example;
public class Sample {
    public void run() {
        // code under test
    }
}
"#.to_string(),
}];
let output = harness
    .compile_and_analyze(Language::Java, &sources, &[])
    .expect("run harness analysis");
let messages: Vec<String> = output
    .results
    .iter()
    .filter(|result| result.rule_id.as_deref() == Some("RULE_ID"))
    .filter_map(|result| result.message.text.clone())
    .collect();
assert!(messages.iter().any(|msg| msg.contains("expected")));
```

## Guardrails
- Keep tests in the rule file to avoid a massive shared test module.
- Use ASCII-only edits unless the file already uses Unicode.
- Add doc comments to any new structs.
