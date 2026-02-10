---
name: ln-640-pattern-evolution-auditor
description: "Audits architectural patterns against best practices (MCP Ref, Context7, WebSearch). Maintains patterns catalog, calculates 4 scores. Output: docs/project/patterns_catalog.md. Use when user asks to: (1) Check architecture health, (2) Audit patterns before refactoring, (3) Find undocumented patterns in codebase."
---

# Pattern Evolution Auditor

L2 Coordinator that analyzes implemented architectural patterns against current best practices and tracks evolution over time.

## Purpose & Scope

- Maintain `docs/project/patterns_catalog.md` with implemented patterns
- Research best practices via MCP Ref, Context7, WebSearch
- Audit layer boundaries via ln-642 (detect violations, check coverage)
- Calculate 4 scores per pattern via ln-641
- Track quality trends over time (improving/stable/declining)
- Output: `docs/project/patterns_catalog.md` (file-based, no task creation)

## 4-Score Model

| Score | What it measures | Threshold |
|-------|------------------|-----------|
| **Compliance** | Industry standards, naming, tech stack conventions, layer boundaries | 70% |
| **Completeness** | All components, error handling, observability, tests | 70% |
| **Quality** | Readability, maintainability, no smells, SOLID, no duplication | 70% |
| **Implementation** | Code exists, production use, integrated, monitored | 70% |

## Worker Invocation

> **CRITICAL:** All delegations use Task tool with `subagent_type: "general-purpose"` for context isolation.

| Worker | Purpose | Phase |
|--------|---------|-------|
| ln-641-pattern-analyzer | Calculate 4 scores per pattern | Phase 5 |
| ln-642-layer-boundary-auditor | Detect layer violations | Phase 4 |
| ln-643-api-contract-auditor | Audit API contracts, DTOs, layer leakage | Phase 4 |

**Prompt template:**
```
Task(description: "[Audit/Create] via ln-6XX",
     prompt: "Execute {skill-name}. Read skill from {skill-name}/SKILL.md. Pattern: {pattern}",
     subagent_type: "general-purpose")
```

**Anti-Patterns:**
- ❌ Direct Skill tool invocation without Task wrapper
- ❌ Any execution bypassing subagent context isolation

## Workflow

### Phase 1a: Baseline Detection

```
1. Load docs/project/patterns_catalog.md
   IF missing → create from shared/templates/patterns_template.md

2. Load docs/reference/adrs/*.md → link patterns to ADRs
   Load docs/reference/guides/*.md → link patterns to Guides

3. Auto-detect baseline patterns
   FOR EACH pattern IN pattern_library.md "Pattern Detection" table:
     Grep(detection_keywords) on codebase
     IF found but not in catalog → add as "Undocumented (Baseline)"
```

### Phase 1b: Adaptive Discovery

**MANDATORY READ:** Load `references/pattern_library.md` — use "Discovery Heuristics" section.

Predefined patterns are a **seed, not a ceiling**. Discover project-specific patterns beyond the baseline.

```
# Structural heuristics (from pattern_library.md)
1. Class naming: Grep GoF suffixes (Factory|Builder|Strategy|Adapter|Observer|...)
2. Abstract hierarchy: ABC/Protocol with 2+ implementations → Template Method/Strategy
3. Fluent interface: return self chains → Builder
4. Registration dict: _registry + register() → Registry
5. Middleware chain: app.use/add_middleware → Chain of Responsibility
6. Event listeners: @on_event/@receiver/signal → Observer
7. Decorator wrappers: @wraps/functools.wraps → Decorator

# Document-based heuristics
8. ADR/Guide filenames + H1 headers → extract pattern names not in library
9. Architecture.md → grep pattern terminology
10. Code comments → "pattern:|@pattern|design pattern"

# Output per discovered pattern:
  {name, evidence: [files], confidence: HIGH|MEDIUM|LOW, status: "Discovered"}
  → Add to catalog "Discovered Patterns (Adaptive)" section
```

### Phase 1c: Pattern Recommendations

Suggest patterns that COULD improve architecture (advisory, NOT scored).

```
# Check conditions from pattern_library.md "Pattern Recommendations" table
# E.g., external API calls without retry → recommend Resilience
# E.g., 5+ constructor params → recommend Builder/Parameter Object
# E.g., direct DB access from API layer → recommend Repository

→ Add to catalog "Pattern Recommendations" section
```

### Phase 1d: Applicability Verification

Verify each detected pattern is actually implemented, not just a keyword false positive.

**MANDATORY READ:** Load `references/scoring_rules.md` — use "Required components by pattern" table.

```
FOR EACH detected_pattern IN (baseline_detected + adaptive_discovered):
  IF pattern.source == "adaptive":
    # Adaptive patterns: check confidence + evidence volume
    IF pattern.confidence == "LOW" AND len(pattern.evidence.files) < 3:
      pattern.status = "EXCLUDED"
      pattern.exclusion_reason = "Low confidence, insufficient evidence"
      → Add to catalog "Excluded Patterns" section
      CONTINUE
  ELSE:
    # Baseline patterns: check minimum 2 structural components
    components = get_required_components(pattern, scoring_rules.md)
    found_count = 0
    FOR EACH component IN components:
      IF Grep(component.detection_grep, codebase) has matches:
        found_count += 1
    IF found_count < 2:
      pattern.status = "EXCLUDED"
      pattern.exclusion_reason = "Found {found_count}/{len(components)} components"
      → Add to catalog "Excluded Patterns" section
      CONTINUE

  pattern.status = "VERIFIED"

# Step 2: Semantic applicability via MCP Ref (after structural check passes)
FOR EACH pattern WHERE pattern.status == "VERIFIED":
  ref_search_documentation("{pattern.name} {tech_stack.language} idiom vs architectural pattern")
  WebSearch("{pattern.name} {tech_stack.language} — language feature or design pattern?")

  IF evidence shows pattern is language idiom / stdlib feature / framework built-in:
    pattern.status = "EXCLUDED"
    pattern.exclusion_reason = "Language idiom / built-in feature, not architectural pattern"
    → Add to catalog "Excluded Patterns" section

# Cleanup: remove stale patterns from previous audits
FOR EACH pattern IN existing_catalog WHERE NOT detected in current scan:
  → REMOVE from Pattern Inventory
  → Add to "Excluded Patterns" with reason "No longer detected in codebase"
```

### Phase 2: Best Practices Research

```
FOR EACH pattern WHERE last_audit > 30 days OR never:

  # MCP Ref + Context7 + WebSearch
  ref_search_documentation("{pattern} best practices {tech_stack}")
  IF pattern.library: query-docs(library_id, "{pattern}")
  WebSearch("{pattern} implementation best practices 2026")

  → Store: contextStore.bestPractices[pattern]
```

### Phase 3: Domain Discovery

```
# Detect project structure for domain-aware scanning
domains = detect_domains(src_root)
# e.g., [{name: "users", path: "src/users/"}, {name: "billing", path: "src/billing/"}]

IF len(domains) > 1:
  domain_mode = "domain-aware"
ELSE:
  domain_mode = "global"
```

### Phase 4: Layer Boundary + API Contract Audit

```
IF domain_mode == "domain-aware":
  # Per-domain invocation of ln-642 and ln-643
  FOR EACH domain IN domains (parallel):
    Task(ln-642-layer-boundary-auditor)
      Input: architecture_path, codebase_root, skip_violations,
             domain_mode="domain-aware", current_domain=domain.name, scan_path=domain.path
    Task(ln-643-api-contract-auditor)
      Input: pattern="API Contracts", locations=[domain.path], bestPractices,
             domain_mode="domain-aware", current_domain=domain.name, scan_path=domain.path
ELSE:
  Task(ln-642-layer-boundary-auditor)
    Input: architecture_path, codebase_root, skip_violations
  Task(ln-643-api-contract-auditor)
    Input: pattern="API Contracts", locations=[service_dirs, api_dirs], bestPractices

# Apply layer deductions to affected patterns (per scoring_rules.md)
FOR EACH violation IN ln642_violations:
  affected_pattern = match_violation_to_pattern(violation)
  affected_pattern.issues.append(violation)
  affected_pattern.compliance_deduction += get_deduction(violation)
```

### Phase 5: Pattern Analysis Loop

```
# ln-641 stays GLOBAL (patterns are cross-cutting, not per-domain)
# Only VERIFIED patterns from Phase 1d (skip EXCLUDED)
FOR EACH pattern IN catalog WHERE pattern.status == "VERIFIED":
  Task(ln-641-pattern-analyzer)
    Input: pattern, locations, bestPractices
    Output: scores{}, issues[], gaps{}

  **Worker Output Contract:**
  - ln-641 returns: `{overall_score, scores: {compliance, completeness, quality, implementation}, issues: [], gaps: {}}`
  - ln-642 returns: `{category, score, total_issues, critical, high, medium, low, findings: [], domain, scan_path}`
  - ln-643 returns: `{overall_score, scores: {compliance, completeness, quality, implementation}, issues: [], domain, scan_path}`

  # Merge layer violations from Phase 4
  pattern.issues += layer_violations.filter(v => v.pattern == pattern)
  pattern.scores.compliance -= compliance_deduction
  pattern.scores.quality -= quality_deduction
```

### Phase 5.5: Cross-Domain Aggregation

```
IF domain_mode == "domain-aware":
  # Group ln-642 findings by issue type across domains
  FOR EACH issue_type IN unique(ln642_findings.issue):
    domains_with_issue = ln642_findings.filter(f => f.issue == issue_type).map(f => f.domain)
    IF len(domains_with_issue) >= 2:
      systemic_findings.append({
        severity: "CRITICAL",
        issue: f"Systemic layer violation: {issue_type} in {len(domains_with_issue)} domains",
        domains: domains_with_issue,
        recommendation: "Address at architecture level, not per-domain"
      })

  # Group ln-643 findings by rule across domains
  FOR EACH rule IN unique(ln643_issues.principle):
    domains_with_issue = ln643_issues.filter(i => i.principle == rule).map(i => i.domain)
    IF len(domains_with_issue) >= 2:
      systemic_findings.append({
        severity: "HIGH",
        issue: f"Systemic API contract issue: {rule} in {len(domains_with_issue)} domains",
        domains: domains_with_issue,
        recommendation: "Create cross-cutting architectural fix"
      })
```

### Phase 6: Gap Analysis

```
gaps = {
  undocumentedPatterns: found in code but not in catalog,
  missingComponents: required components not found per scoring_rules.md,
  layerViolations: code in wrong architectural layers,
  consistencyIssues: conflicting patterns,
  systemicIssues: systemic_findings from Phase 5.5
}
```

### Aggregation Algorithm

```
# Step 1: Get all worker scores (0-10 scale)
pattern_scores = [p.overall_score for p in ln641_results]  # Each 0-10
layer_score = ln642_result.score                            # 0-10
api_score = ln643_result.overall_score                      # 0-10

# Step 2: Calculate architecture_health_score
all_scores = pattern_scores + [layer_score, api_score]
architecture_health_score = round(average(all_scores) * 10)  # 0-100 scale

# Status mapping:
# >= 80: "healthy"
# 70-79: "warning"
# < 70: "critical"
```

### Phase 7: Report + Trend Analysis

```
1. Update patterns_catalog.md:
   - Pattern scores, dates
   - Layer Boundary Status section
   - Quick Wins section
   - Patterns Requiring Attention section

2. Calculate trend: compare current vs previous scores

3. Output summary (see Return Result below)
```

### Phase 8: Return Result

```json
{
  "audit_date": "2026-02-04",
  "architecture_health_score": 78,
  "trend": "improving",
  "patterns_analyzed": 5,
  "layer_audit": {
    "architecture_type": "Layered",
    "violations_total": 5,
    "violations_by_severity": {"high": 2, "medium": 3, "low": 0},
    "coverage": {"http_abstraction": 85, "error_centralization": true}
  },
  "patterns": [
    {
      "name": "Job Processing",
      "scores": {"compliance": 72, "completeness": 85, "quality": 68, "implementation": 90},
      "avg_score": 79,
      "status": "warning",
      "issues_count": 3
    }
  ],
  "quick_wins": [
    {"pattern": "Caching", "issue": "Add TTL config", "effort": "2h", "impact": "+10 completeness"}
  ],
  "requires_attention": [
    {"pattern": "Event-Driven", "avg_score": 58, "critical_issues": ["No DLQ", "No schema versioning"]}
  ],
  "cross_domain_issues": [
    {
      "severity": "CRITICAL",
      "issue": "Systemic layer violation: HTTP client in domain layer in 3 domains",
      "domains": ["users", "billing", "orders"],
      "recommendation": "Address at architecture level"
    }
  ]
}
```

## Critical Rules

- **MCP Ref first:** Always research best practices before analysis
- **Layer audit first:** Run ln-642 before ln-641 pattern analysis
- **4 scores mandatory:** Never skip any score calculation
- **Layer deductions:** Apply scoring_rules.md deductions for violations
- **File output only:** Write results to patterns_catalog.md, no task/story creation

## Definition of Done

- Pattern catalog loaded or created
- Applicability verified for all detected patterns (Phase 1d); excluded patterns documented
- Best practices researched for all VERIFIED patterns needing audit
- Domain discovery completed (global or domain-aware mode selected)
- Layer boundaries audited via ln-642 (violations detected, coverage calculated)
- API contracts audited via ln-643
- All patterns analyzed via ln-641 (4 scores with layer deductions applied)
- If domain-aware: cross-domain aggregation completed (systemic issues identified)
- Gaps identified (undocumented, missing components, layer violations, inconsistent, systemic)
- Catalog updated with scores, dates, Layer Boundary Status
- Trend analysis completed
- Summary report output

## Reference Files

- **Task delegation pattern:** `shared/references/task_delegation_pattern.md`
- Pattern catalog template: `shared/templates/patterns_template.md`
- Pattern library (detection + best practices + discovery): `references/pattern_library.md`
- Layer boundary rules (for ln-642): `references/layer_rules.md`
- Scoring rules: `references/scoring_rules.md`
- Pattern analysis: `../ln-641-pattern-analyzer/SKILL.md`
- Layer boundary audit: `../ln-642-layer-boundary-auditor/SKILL.md`
- API contract audit: `../ln-643-api-contract-auditor/SKILL.md`

---
**Version:** 2.0.0
**Last Updated:** 2026-02-08
