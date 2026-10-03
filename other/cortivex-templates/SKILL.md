---
name: cortivex-templates
version: 1.0.0
description: Reference for all built-in pipeline templates with usage guidance and customization
category: reference
tags: [templates, pipelines, reference, best-practices]
author: Cortivex
requires: [cortivex MCP server]
capabilities: [template-listing, template-usage, template-customization, template-sharing]
slash_commands:
  - name: cortivex templates
    description: List and manage pipeline templates
    usage: /cortivex templates [list|info|copy|share]
---

# Cortivex Pipeline Templates

Templates are pre-built, tested pipeline configurations for common development workflows. They are ready to run immediately and serve as starting points for customization.

## Built-in Template Directory

| # | Template | Description | Nodes | Est. Cost | Est. Duration |
|---|----------|-------------|-------|-----------|---------------|
| 1 | pr-review | Review PRs for security, quality, and auto-fix issues | 5 | $0.05 | 3m |
| 2 | full-test-suite | Generate comprehensive unit, integration, and E2E tests | 4 | $0.08 | 5m |
| 3 | js-to-typescript | Migrate JavaScript source files to TypeScript | 4 | $0.12 | 8m |
| 4 | dependency-update | Update dependencies safely with testing | 3 | $0.03 | 3m |
| 5 | security-audit | Deep security analysis with written report | 3 | $0.06 | 4m |
| 6 | documentation-refresh | Analyze codebase and regenerate all documentation | 4 | $0.07 | 5m |
| 7 | bug-hunt | Find bugs, fix them, generate tests, and validate | 4 | $0.06 | 5m |
| 8 | performance-audit | Profile performance, fix bottlenecks, and verify | 3 | $0.05 | 4m |
| 9 | onboarding-guide | Generate onboarding documentation for new developers | 3 | $0.05 | 4m |
| 10 | nightly-review | Comprehensive nightly security and quality scan | 4 | $0.05 | 5m |
| 11 | pre-release-check | Full pre-release validation: security, tests, perf, changelog | 4 | $0.06 | 6m |
| 12 | api-design | Design API from codebase analysis with tests and docs | 4 | $0.08 | 6m |
| 13 | refactor-module | Analyze, refactor, test, and review a module | 4 | $0.08 | 6m |
| 14 | coverage-boost | Analyze gaps and generate tests to boost coverage | 4 | $0.08 | 7m |
| 15 | changelog-release | Generate changelog, update docs, and create release PR | 3 | $0.03 | 2m |

## Using Templates

### Running a Template

```
/cortivex run <template-name>
```

Examples:
```
/cortivex run pr-review
/cortivex run security-audit --verbose
/cortivex run full-test-suite --dry-run
/cortivex run pr-review --param pr_number=42 --param branch=feature/auth
```

### Getting Template Info

```
/cortivex templates info <template-name>
```

Shows the full template YAML with node definitions, configurations, and dependency graph.

### Dry Run

Always available with any template:

```
/cortivex run <template-name> --dry-run
```

Output:
```
Dry Run: pr-review
===================
Nodes: 5
Estimated Cost: $0.05
Estimated Duration: 3m

Execution Plan:
  1. SecurityScanner     (parallel: none)         ~15s  ~$0.004
  2. CodeReviewer        (after: SecurityScanner)  ~45s  ~$0.018
  3. AutoFixer           (after: CodeReviewer)     ~30s  ~$0.012
  4. TestRunner          (after: AutoFixer)        ~60s  ~$0.008
  5. PRCreator           (after: TestRunner)       ~8s   ~$0.003

No issues found. Ready to run.
```

## Customizing Templates

### Copy and Modify

To customize a template:

```
/cortivex templates copy pr-review --as my-pr-review
```

This creates a copy in your custom pipelines directory. Edit the copy freely.

### Common Customizations

**Change a model for a specific node:**
```yaml
nodes:
  - id: code_review
    type: CodeReviewer
    config:
      model: claude-sonnet-4-20250514    # override default
```

**Add a node to an existing template:**
Insert the node definition and update `depends_on` references to maintain the DAG.

**Remove a node:**
Delete the node definition and update any `depends_on` references that pointed to it.

**Change scope or parameters:**
```yaml
nodes:
  - id: security_scan
    type: SecurityScanner
    config:
      scan_depth: deep            # override default "standard"
      severity_threshold: low     # override default "medium"
```

**Add conditions:**
```yaml
nodes:
  - id: security_scan
    type: SecurityScanner
    condition:
      if: "changed_files.any(f => f.path.startsWith('src/auth/'))"
      skip_message: "No auth files changed, skipping security scan"
```

**Add retry logic:**
```yaml
nodes:
  - id: test_run
    type: TestRunner
    retry:
      max_attempts: 3
      backoff: exponential
      base_delay_seconds: 5
```

## Sharing Templates

### Export a Template

```
/cortivex templates share my-pr-review --output my-pr-review.yaml
```

Produces a standalone YAML file that can be shared with teammates.

### Import a Template

```
/cortivex templates import ./shared/team-review.yaml --as team-review
```

Imports a YAML template file into your local template registry.

### Team Template Repository

For teams, store shared templates in a git repository:

```
my-org/cortivex-templates/
  pr-review-strict.yaml
  nightly-security.yaml
  release-process.yaml
```

Configure the remote repository:

```
cortivex_config({
  action: "set",
  key: "template_repos",
  value: ["https://github.com/my-org/cortivex-templates"]
})
```

Templates from remote repos are available with their prefix:
```
/cortivex run my-org/pr-review-strict
```

## Best Practices for Pipeline Design

### 1. Start with Analysis

Always begin pipelines with an analysis node (ArchitectAnalyzer, SecurityScanner, CodeReviewer) before modification nodes. Analysis output provides context that makes modifications more accurate.

### 2. Validate After Modification

Every modification node (AutoFixer, RefactorAgent, TypeMigrator) should be followed by a validation node (TestRunner, LintFixer). Never end a pipeline on a modification without verification.

### 3. Keep Pipelines Focused

A pipeline should do one thing well. Instead of a 15-node mega-pipeline, compose smaller pipelines:

```
/cortivex run security-audit
/cortivex run pr-review
/cortivex run documentation-refresh
```

### 4. Use Conditions to Save Cost

Add conditions to skip nodes when they are not relevant:

```yaml
condition:
  if: "changed_files.length > 0 && changed_files.any(f => f.endsWith('.ts'))"
```

### 5. Set Appropriate Timeouts

Set `timeout_seconds` based on expected duration, not on worst case:
- LintFixer: 30s
- TestRunner: 300s (5m) for most projects, up to 900s (15m) for large suites
- TypeMigrator: 600s (10m) for large codebases

### 6. Use Haiku for Lightweight Nodes

Nodes that do not require deep reasoning (LintFixer, TestRunner, ChangelogWriter, PRCreator) can use `claude-haiku-4-20250414` at a fraction of the cost with equivalent results.

### 7. Leverage the Learning System

After several runs, check `cortivex_insights` to see if the system has learned optimizations for your specific repository. Apply high-confidence insights to your custom templates.

### 8. Name Pipelines Descriptively

Use names that describe the workflow, not the trigger:
- Good: `security-audit`, `pr-review-strict`, `nightly-quality-check`
- Bad: `pipeline1`, `my-pipeline`, `test`

## Template File Format

All templates follow this YAML structure:

```yaml
name: template-name
version: "1.0"
description: What this pipeline does
tags: [tag1, tag2]
estimated_cost: "$0.05"
estimated_duration: "3m"

# Optional: parameters that can be overridden at runtime
params:
  branch:
    type: string
    default: main
    description: Target branch
  coverage_threshold:
    type: number
    default: 80
    description: Minimum test coverage percentage

# Node definitions
nodes:
  - id: unique_node_id
    type: NodeType
    depends_on: []                # list of node IDs this depends on
    config:
      key: value
    condition:                    # optional
      if: "expression"
      skip_message: "reason"
    retry:                        # optional
      max_attempts: 3
      backoff: exponential
    fallback_for: other_node_id   # optional
```

Refer to the individual template YAML files in the `templates/` directory for complete, runnable examples.

## Reasoning Protocol

Before selecting or customizing a template, reason through:

1. **Does a built-in template cover this use case?** Check the template directory table above. If a template covers 80%+ of the need, customize it rather than building from scratch.
2. **What customizations are needed?** List the specific changes: different models, additional nodes, removed nodes, adjusted scopes, added conditions.
3. **Will the customizations break the pipeline's logic?** When removing a node, check if other nodes depend on it. When adding a node, ensure it has correct `depends_on` references.
4. **Is the estimated cost acceptable?** Check the template's `estimated_cost`. If customizations add expensive nodes (CodeReviewer, RefactorAgent), recalculate the estimate.
5. **Should this be a saved custom template?** If you will use this customization more than once, save it with `--save-as`. One-off modifications do not need to be saved.

## Anti-Patterns

| Anti-Pattern | Consequence | Correct Approach |
|-------------|------------|-----------------|
| Building from scratch when a template exists | Wasted effort; templates are tested and optimized | Always check built-in templates first |
| Customizing a template without dry-running | Modification may break the DAG or exceed budget | Always `--dry-run` after any customization |
| Saving every one-off customization | Template registry fills with unused variations | Only save templates you will reuse |
| Using `pr-review` for non-PR work | Template assumes PR context (branch, changed files) | Use `security-audit` or `bug-hunt` for general codebase analysis |
| Running `full-test-suite` on a repo without tests | TestRunner will fail because there are no tests to run | Use `coverage-boost` to generate tests first, then validate |
| Ignoring template parameters | Running with defaults when the repo needs specific values | Review and set `params` (branch, coverage_threshold, etc.) for each run |
| Mega-pipeline by combining all templates | Enormous cost and runtime for marginal benefit | Run focused templates sequentially |

## Grounding Rules

- **No template matches the request:** Use cortivex-pipeline to build a custom pipeline from natural language. Save it as a template if you will reuse it.
- **Template runs successfully but output quality is low:** Check if the right models are configured. Analysis nodes benefit from Sonnet. Consider adding an ArchitectAnalyzer as the first node to provide codebase context.
- **Template fails on a specific repo:** Check the repo's tech stack. Templates assume standard project structures. For non-standard repos, customize the template with appropriate paths and tool configurations.
- **Unsure whether to use `pr-review` or `security-audit`:** If the work involves a specific PR with changed files, use `pr-review`. If you want to analyze the full codebase regardless of recent changes, use `security-audit`.
- **Template cost seems high for a small repo:** Small repos process faster but the per-node startup cost is fixed. For repos under 20 files, consider running individual nodes instead of full templates.

## Advanced Capabilities

### Template Inheritance & Composition

Templates can extend a base template via the `extends` field, inheriting all nodes and configuration while selectively overriding, removing, or appending nodes without rewriting the entire pipeline.

```yaml
name: pr-review-strict
extends: pr-review
overrides:
  nodes:
    - id: security_scan
      config:
        scan_depth: deep
        severity_threshold: "{{ params.severity_threshold }}"
    - id: code_review
      config:
        model: claude-sonnet-4-20250514
        strictness: high
remove_nodes: [auto_fixer]
append_nodes:
  - id: compliance_check
    type: ComplianceValidator
    depends_on: [code_review]
    config:
      standards: [SOC2, OWASP]
```

### Parameterized Template Variables

Parameters use JSON Schema for validation and defaults. Reference them in node configs via `{{ params.name }}`.

```json
{
  "type": "object",
  "properties": {
    "target_branch": { "type": "string", "default": "main" },
    "coverage_threshold": { "type": "number", "minimum": 0, "maximum": 100, "default": 80 },
    "scan_mode": { "type": "string", "enum": ["quick", "standard", "deep"], "default": "standard" }
  },
  "required": ["target_branch"]
}
```

### Template Validation & Linting

The `cortivex_template_validate` tool checks DAG integrity, parameter schemas, node compatibility, and cost bounds before execution.

```json
{
  "tool": "cortivex_template_validate",
  "params": { "template": "my-custom-review", "strict": true, "check_cost_bounds": true }
}
```

Success response:

```json
{
  "valid": true,
  "warnings": ["Node 'lint_fix' uses haiku which may underperform on complex refactors"],
  "dag_check": "passed",
  "estimated_cost": "$0.07"
}
```

Failure response:

```json
{
  "valid": false,
  "errors": [
    "Node 'test_runner' depends on 'auto_fixer' which does not exist",
    "Parameter 'coverage_threshold' type mismatch: string vs number"
  ],
  "dag_check": "cycle_detected"
}
```

### Version-Controlled Template Management

Templates support semantic versioning with changelogs, allowing teams to pin versions, roll back, and review changes before upgrading.

```yaml
name: nightly-security
version: "2.3.0"
min_cortivex_version: "1.4.0"
changelog:
  - version: "2.3.0"
    date: "2026-03-20"
    changes:
      - "Added OWASP dependency check node"
      - "Upgraded default model to claude-sonnet-4-20250514"
  - version: "2.2.0"
    date: "2026-02-10"
    changes:
      - "Added monorepo scanning support"
version_policy:
  auto_upgrade: minor
  pin_major: true
  notify_on_deprecation: true
```

Pin a specific version at runtime with `/cortivex run nightly-security@2.2.0`.

### Dynamic Template Generation from Specs

Generate templates from natural language specifications when no existing template fits. The `cortivex_template_generate` tool selects node types, wires dependencies, and produces valid YAML.

```json
{
  "tool": "cortivex_template_generate",
  "params": {
    "spec": "Analyze TypeScript files for accessibility violations, fix issues, run tests, generate report",
    "constraints": { "max_nodes": 5, "max_cost": "$0.10" },
    "output_format": "yaml"
  }
}
```

Response with generated template:

```json
{
  "generated_template": "a11y-fix-and-verify",
  "node_count": 4,
  "estimated_cost": "$0.07",
  "confidence": 0.92,
  "suggestions": ["Consider adding a LintFixer node after a11y_fix"]
}
```

Save the generated template programmatically:

```typescript
const result = await cortivex_template_generate({
  spec: "Scan for accessibility issues, fix, test, and report",
  constraints: { max_nodes: 5, max_cost: "$0.10" },
  output_format: "yaml",
  save_as: "a11y-fix-and-verify"
});
// result.saved === true
// Available via: /cortivex run a11y-fix-and-verify
```

## Security Hardening (OWASP AST10 Aligned)

### AST01/AST02: Template Signature Verification

External templates must be Ed25519-signed and verified before use (AST01 -- Prompt Injection, AST02 -- Improper Tool Access Control).

```yaml
template_signing:
  algorithm: ed25519
  key_management: { public_keys_dir: .cortivex/keys/trusted/, key_rotation_days: 90 }
  verification_policy: { require_signature: true, require_trusted_key: true, fail_open: false }
```

```json
{
  "title": "TemplateSignatureEnvelope", "type": "object",
  "required": ["template_hash", "signature", "signer_key_id", "signed_at"],
  "properties": {
    "template_hash": { "type": "string", "pattern": "^sha256:[a-f0-9]{64}$" },
    "signature": { "type": "string" }, "signer_key_id": { "type": "string" },
    "signed_at": { "type": "string", "format": "date-time" } }
}
```

```json
{ "method": "cortivex_template_verify", "params": { "template_file": "team-review.yaml", "signature_file": "team-review.yaml.sig", "trusted_keys_dir": ".cortivex/keys/trusted/" } }
```

### Remote Template Repository Validation

Remote repos are validated against an allowlist with hash pinning (AST01, AST02) to prevent supply-chain attacks.

```yaml
remote_template_policy:
  enforcement: strict
  allowed_repositories:
    - { url: "https://github.com/my-org/cortivex-templates", require_signature: true, branch_allowlist: ["main"] }
  blocked_repositories: [{ url_pattern: "http://*" }, { url_pattern: "*gist.github.com*" }]
  hash_pinning: { enabled: true, pin_file: .cortivex/security/template-pins.yaml, auto_update_pins: false }
```

```json
{ "method": "cortivex_remote_template_validate", "params": { "repository": "https://github.com/my-org/cortivex-templates", "template": "pr-review-strict", "version": "2.3.1" } }
```

### Template Parameter Sanitization

Runtime parameters flow into node configs; without sanitization they enable injection (AST01).

```yaml
parameter_sanitization:
  global_rules: { max_string_length: 1024, strip_null_bytes: true, strip_control_characters: true }
  type_enforcement:
    string:
      block_patterns: ["\\$\\{.*\\}", "\\{\\{.*\\}\\}", "`.*`", "\\$\\(.*\\)", ";.*", "\\|.*"]
      max_length: 512
    number: { min: -1000000, max: 1000000, reject_nan: true }
    enum: { validate_against_schema: true }
  per_parameter_overrides:
    target_path: { block_path_traversal: true, allowed_prefixes: ["src/", "lib/", "tests/"] }
    test_command: { allowlist_only: true, reference_policy: ".cortivex/security/shell-allowlists.yaml" }
```

```json
{ "method": "cortivex_parameter_sanitize", "params": { "template": "pr-review", "parameters": { "branch": "feature/auth", "coverage_threshold": 80 } } }
```

```json
{ "valid": false, "violations": [{ "parameter": "branch", "value": "main; rm -rf /", "matched_pattern": ";.*", "ast_risk": "AST01" }] }
```

### Risk Tier Classification (L0-L3 per OWASP AST)

Every template is assigned a risk tier determining runtime security controls.

```yaml
risk_tier_classification:
  L0_minimal:
    criteria: { no_modification_nodes: true, no_shell_execution: true }
    controls: { require_approval: false, sandbox_level: none }
  L1_standard:
    criteria: { has_modification_nodes: true, no_shell_execution: true }
    controls: { require_signature: true, sandbox_level: filesystem }
  L2_elevated:
    criteria: { has_shell_execution: true }
    controls: { require_approval: true, sandbox_level: container, cost_gate_required: true }
  L3_critical:
    criteria: { has_deployment_nodes: true }
    controls: { require_multi_party_approval: true, sandbox_level: firecracker, dry_run_mandatory: true }
```

```json
{ "method": "cortivex_template_classify", "params": { "template": "pr-review" } }
```

```json
{ "risk_tier": "L2_elevated", "ast_risks_addressed": ["AST01", "AST02", "AST03", "AST06"], "required_controls": { "require_approval": true, "sandbox_level": "container" } }
```

### Template Import Sandboxing

External templates are parsed in an isolated context (AST01) to prevent malicious YAML from affecting the host engine.

```yaml
import_sandbox:
  isolation_level: process
  parser_config:
    yaml_safe_load: true
    max_document_size_bytes: 102400
    disallow_anchors: true            # billion laughs prevention
    disallow_custom_tags: true        # block !!python/object, !!js/function
  post_parse_validation: { schema_check: true, prompt_injection_scan: true, tool_access_audit: true }
  quarantine: { quarantine_dir: .cortivex/quarantine/, quarantine_on_failure: true }
```

```json
{ "method": "cortivex_template_import", "params": { "source": "./shared/team-review.yaml", "save_as": "team-review", "sandbox": true, "verify_signature": true } }
```

```json
{ "imported": false, "quarantined": true, "validation_errors": [{ "check": "prompt_injection_scan", "ast_risk": "AST01" }, { "check": "tool_access_audit", "ast_risk": "AST02" }] }
