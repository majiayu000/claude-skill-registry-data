---
name: speckit-task-grounding
description: Task grounding validation framework for ensuring development tasks are properly specified in planning artifacts before implementation. Use when validating feature specifications, checking task grounding against artifacts like spec.md, plan.md, data-model.md, api-contracts.md, research.md, and quickstart.md, or when performing parallel task validation for feature readiness assessment.
---

# SpecKit Task Grounding Validator

A framework for validating that development tasks are properly grounded in planning artifacts before implementation, enabling parallel task validation and reducing implementation risks.

## Integration with Speckit SDD

This skill integrates with the **Spec-Driven Development (SDD)** methodology implemented by Speckit:

- **SDD Workflow**: specify → plan → tasks
- **Artifact Scope**: Works within `specs/[branch-name]/` specification folders
- **Validation Timing**: Use after `/speckit.tasks` generates the task list
- **Quality Gate**: Ensures tasks are properly grounded before implementation begins

## Core Concept

**Parallel Task Validation**: Each task grounding check is independent, allowing multiple reviewers to validate tasks simultaneously (2-3 minutes per task).

## Quick Start

1. **Verify artifacts exist**: Check for spec.md, plan.md, tasks.md, and supporting artifacts
2. **Process each task in parallel**:
   - Extract task details from tasks.md
   - Search artifacts for evidence
   - Score grounding level (0-100%)
   - Assess risk and identify gaps
   - Document findings
3. **Generate report**: Use the complete report template for decision gates

## Grounding Score Calculator

| Score    | Meaning    | Evidence Required                    | Action           |
| -------- | ---------- | ------------------------------------ | ---------------- |
| **100%** | Explicit   | Direct quote with exact location     | ✅ Execute        |
| **90%**  | Detailed   | Code example or schema provided      | ✅ Execute        |
| **80%**  | Referenced | Clear spec with implementation notes | ✅ Execute        |
| **70%**  | Pattern    | Documented pattern to follow         | ⚠️ Verify pattern |
| **60%**  | Inferred   | Multiple weak references             | ⚠️ Clarify        |
| **50%**  | Assumed    | Single weak reference                | 🔴 High risk      |
| **<50%** | Missing    | No evidence found                    | 🔴 Block          |

## Decision Matrix

### Phase Thresholds
- **Phase 1 (Setup)**: ≥90% tasks at ≥80% grounding
- **Phase 2 (Foundation)**: ≥80% tasks at ≥70% grounding
- **Phase 3+ (Features)**: ≥70% tasks at ≥60% grounding

### Risk Levels
- **🟢 Low**: ≥90% grounding, no gaps
- **🟡 Medium**: 70-89% grounding, resolvable gaps
- **🔴 High**: <70% grounding, critical gaps

## 📚 Grounding Status Glossary

### Task Grounding Status Values
| Status                                  | Meaning | Description                                                                                                                                    | Action                         |
| --------------------------------------- | ------- | ---------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------ |
| 🟢 **Documented**<br/>(Fully Grounded)   | 80-100% | Clear specification with implementation details from planning phase artifacts (plan.md, research.md, data-model.md, contracts/, quickstart.md) | ✅ Ready to implement           |
| 🟡 **Inferred**<br/>(Partially Grounded) | 50-79%  | Evidence exists but requires clarification                                                                                                     | ⚠️ Verify before implementation |
| 🔴 **Missing**<br/>(Ungrounded)          | <50%    | No evidence found in artifacts                                                                                                                 | 🔴 Block until specified        |

### Phase-Level Grounding Status Values
| Status                   | Meaning                     | Description                                  |
| ------------------------ | --------------------------- | -------------------------------------------- |
| 🟢 **Fully Documented**   | ≥80% tasks fully grounded   | All critical tasks have clear specifications |
| 🟢 **Mostly Documented**  | 70-79% tasks fully grounded | Most tasks grounded, minor gaps              |
| 🟡 **Partially Inferred** | 50-69% tasks fully grounded | Significant gaps requiring clarification     |
| 🟡 **Mostly Inferred**    | 30-49% tasks fully grounded | Major gaps, high risk                        |
| 🔴 **Poorly Grounded**    | <30% tasks fully grounded   | Critical gaps, block implementation          |

### Risk Level Values
| Level        | Meaning                           | Description                            |
| ------------ | --------------------------------- | -------------------------------------- |
| 🟢 **Low**    | ≥90% grounding, no gaps           | Straightforward implementation         |
| 🟡 **Medium** | 70-89% grounding, resolvable gaps | Needs verification but implementable   |
| 🔴 **High**   | <70% grounding, critical gaps     | High risk, may require planning rework |

### Overall Assessment Values
| Assessment                | Meaning                                 | Description                    |
| ------------------------- | --------------------------------------- | ------------------------------ |
| ✅ **APPROVE**             | Meets phase thresholds                  | Proceed with implementation    |
| ⚠️ **NEEDS CLARIFICATION** | Resolvable gaps identified              | Address gaps before proceeding |
| 🔴 **BLOCK**               | Critical gaps or insufficient grounding | Return to planning phase       |

### Grounding Score Scale (0-100%)
| Score    | Qualitative Term | Evidence Required                                                                                                           |
| -------- | ---------------- | --------------------------------------------------------------------------------------------------------------------------- |
| **100%** | Explicit         | Direct quote with exact location from planning phase artifacts                                                              |
| **90%**  | Detailed         | Code example or schema provided from planning phase artifacts                                                               |
| **80%**  | Referenced       | Clear implementation details from planning phase artifacts (plan.md, research.md, data-model.md, contracts/, quickstart.md) |
| **70%**  | Pattern          | Documented pattern to follow from any artifact                                                                              |
| **60%**  | Inferred         | Multiple weak references from any artifacts                                                                                 |
| **50%**  | Assumed          | Single weak reference from any artifact                                                                                     |
| **<50%** | Missing          | No evidence found in any artifacts (spec.md alone does not qualify for ≥80% scores)                                         |

**Important**: Tasks must be grounded in planning phase artifacts to achieve "Documented" (≥80%) status. Evidence from spec.md alone caps scoring at 70% maximum, as spec.md represents requirements specification rather than implementation planning.

## Key Features

- **Parallel Processing**: Independent task validation enables team distribution
- **Evidence-Based Scoring**: Systematic 0-100% grounding assessment
- **Gap Analysis**: Identifies missing specifications with resolution steps
- **Decision Gates**: Clear approve/clarify/block recommendations
- **Report Templates**: Complete documentation framework

## Usage Workflow

For each task in tasks.md:
1. **Extract** task details and requirements
2. **Exhaustively search ALL artifacts** in order: spec.md → plan.md → research.md → data-model.md → contracts/ → quickstart.md (do not stop at first evidence found - scan all artifacts for complete grounding assessment)
3. **Score** grounding level based on evidence strength
4. **Assess** risk and document gaps
5. **Aggregate** results for feature-level decision

## Parallel Processing Workflow

### Step 1: Assign Tasks to Reviewers
- **Reviewer A**: Tasks T001-T003 (Phase 1)
- **Reviewer B**: Tasks T004-T005 (Phase 2)
- **Reviewer C**: Tasks T006+ (Phase 3+)

### Step 2: Individual Validation
```powershell
# Reviewer A validates their assigned tasks
.\scripts\Validate-TaskGrounding.ps1 -FeaturePath "specs/my-feature" -TaskFilter "T001,T002,T003" -JsonOutput -OutputPath "specs/my-feature/assessments/reviewerA-assessment.json"

# Reviewer B validates their assigned tasks
.\scripts\Validate-TaskGrounding.ps1 -FeaturePath "specs/my-feature" -TaskFilter "T004,T005" -JsonOutput -OutputPath "specs/my-feature/assessments/reviewerB-assessment.json"
```

### Step 3: Aggregate Results
```powershell
# Combine all individual assessments into final report
.\scripts\Aggregate-TaskGrounding.ps1 -FeatureName "my-feature" -AssessmentFiles @("specs/my-feature/assessments/reviewerA-assessment.json", "specs/my-feature/assessments/reviewerB-assessment.json", "specs/my-feature/assessments/reviewerC-assessment.json") -OutputPath "specs/my-feature/tasks.grounding.md"
```

**Post-Aggregation Cleanup:**
```powershell
# Optional: Remove intermediate assessment files after successful aggregation
Remove-Item "specs/my-feature/assessments/*.json"
```

**Benefits:**
- **Parallel Execution**: 2-3 minutes per reviewer instead of 15-25 minutes total
- **Independent Validation**: Each task assessed by one person, avoiding conflicts
- **Efficient Aggregation**: Automated combination maintains consistency
- **Scalable**: Works with 2 reviewers or 10 reviewers equally well

## Resulting File Structure

After complete validation, your specification folder will contain:

```
specs/[branch-name]/
├── spec.md                    # Original artifacts
├── plan.md
├── research.md
├── data-model.md
├── contracts/
├── quickstart.md
├── tasks.md
├── assessments/                # Intermediate files (can be removed after aggregation)
│   ├── reviewerA-assessment.json
│   ├── reviewerB-assessment.json
│   └── reviewerC-assessment.json
└── tasks.grounding.md         # Final validation report (VS Code nested under tasks.md)
```

## References

- [Complete Framework](references/framework.md) - Full validation methodology and templates
- [Scoring Examples](references/examples.md) - Real-world validation cases
- [Report Template](references/report-template.md) - Reusable template for validation reports
- [Report Example](references/report-example.md) - Complete filled-out validation report
- [Automation Scripts](scripts/) - PowerShell validation and aggregation scripts

## Prerequisites

- `spec.md` - Feature specification with user stories and requirements (highest authority)
- `plan.md` - Implementation plan with technical decisions
- `research.md` - Technical research and context gathering
- `data-model.md` - Data models and entity definitions
- `contracts/` - Directory containing API contracts and interface specifications
- `quickstart.md` - Key validation scenarios and quickstart guide
- `tasks.md` - Executable task list derived from plan (input for validation)
- `assessments/` - Directory for intermediate assessment files (created automatically)

## Common Use Cases

- **Feature Readiness**: Validate all tasks before implementation begins
- **Specification Review**: Ensure planning artifacts are complete
- **Risk Assessment**: Identify implementation uncertainties early
- **Team Coordination**: Parallel validation by multiple reviewers
- **Quality Gates**: Automated checking in CI/CD pipelines
- **SDD Compliance**: Validate Speckit-generated artifacts meet grounding standards

## Output

**File Locations (relative to specification root):**

- `assessments/reviewer*-assessment.json` - Individual reviewer assessments (intermediate files)
- `tasks.grounding.md` - Final comprehensive validation report

**Report Contents:**
- Executive Summary table with phase status
- Task Grounding Matrix with status indicators
- Gap analysis with impact and resolution steps
- Action plan with phase-specific execution steps
- Risk assessment and mitigation strategies
- Decision gate recommendation (Approve/Clarify/Block)

## Decision Rules

- **✅ APPROVE**: Meets phase thresholds, no critical gaps
- **⚠️ CLARIFY**: Resolvable gaps identified, needs verification
- **🔴 BLOCK**: Critical gaps or insufficient grounding

## Training Levels

- **Level 1 (30 min)**: Basic scoring and validation process
- **Level 2 (60 min)**: Complex cases and customization
- **Level 3 (2 hours)**: Administration and team training

## Version History

- **v3 (Current)**: Single-page parallel validation framework
- **v2 (Experimental)**: Four-file compressed structure
- **v1 (Experimental)**: Original 13-file comprehensive documentation