---
name: ring:using-finops-team
description: |
  2 FinOps agents for Brazilian financial regulatory compliance (BACEN, RFB,
  Open Banking). Dispatch for compliance analysis or template generation.

trigger: |
  - Brazilian regulatory reporting (BACEN, RFB)
  - Financial compliance requirements
  - Open Banking specifications
  - Template generation for Reporter platform

skip_when: |
  - Non-Brazilian regulations → use appropriate resources
  - General financial analysis → use other tools
---

# Using Ring FinOps & Regulatory Agents

The ring-finops-team plugin provides 2 specialized FinOps agents for Brazilian financial compliance. Use them via `Task tool with subagent_type:`.

**Remember:** Follow the **ORCHESTRATOR principle** from `ring:using-ring`. Dispatch agents to handle regulatory complexity; don't implement compliance manually.

---

## 2 FinOps Specialists

### 1. FinOps Analyzer (Compliance Analysis)
**`ring:finops-analyzer`**

**Specializations:**
- Brazilian regulatory compliance analysis
- BACEN (Central Bank) requirements:
  - COSIF (accounting chart of accounts)
  - CADOCs (financial instruments catalog)
- RFB (Federal Revenue) requirements:
  - e-Financeira (financial reporting)
  - SPED (electronic data exchange)
- Open Banking specifications
- Field mapping & validation

**Use When:**
- Analyzing regulatory requirements (Gate 1-2)
- Validating field mappings for compliance
- Understanding BACEN/RFB specifications
- Planning compliance architecture
- Determining required data structures

**Output:** Compliance analysis, field mappings, validation rules

**Example dispatch:**
```
Task tool:
  subagent_type: "ring:finops-analyzer"
  model: "opus"
  prompt: "Analyze BACEN COSIF requirements for corporate account reporting"
```

---

### 2. FinOps Automation (Template Generation)
**`ring:finops-automation`**

**Specializations:**
- Template generation from specifications
- .tpl file creation for Reporter platform
- XML template generation
- HTML template generation
- TXT template generation
- Reporter platform integration

**Use When:**
- Generating regulatory report templates (Gate 3)
- Creating BACEN/RFB compliant templates
- Building Reporter platform files
- Converting specifications to executable templates
- Finalizing compliance implementation

**Output:** Complete .tpl template files, ready for Reporter platform

**Example dispatch:**
```
Task tool:
  subagent_type: "ring:finops-automation"
  model: "opus"
  prompt: "Generate BACEN COSIF template from analyzed requirements"
```

---

## Regulatory Workflow: 3-Gate Process

Brazilian regulatory compliance follows a 3-gate workflow:

### Gate 1: Compliance Analysis
**Agent:** ring:finops-analyzer
**Purpose:** Understand requirements, identify fields, validate mappings
**Output:** compliance analysis document

**Dispatch when:**
- Starting regulatory feature
- Need to understand BACEN/RFB specs
- Planning field mappings

---

### Gate 2: Validation & Confirmation
**Agent:** ring:finops-analyzer (again)
**Purpose:** Confirm mappings are correct, validate against specs
**Output:** validated specification document

**Dispatch when:**
- Ready to confirm compliance understanding
- Need secondary validation
- Before moving to template generation

---

### Gate 3: Template Generation
**Agent:** ring:finops-automation
**Purpose:** Generate executable .tpl templates from validated specifications
**Output:** complete .tpl files for Reporter platform

**Dispatch when:**
- Specifications are finalized & validated
- Ready to create Reporter templates
- Need production-ready compliance files

---

## Supported Regulatory Standards

### BACEN (Central Bank of Brazil)
- **COSIF** – Chart of accounts and accounting rules
- **CADOCs** – Financial instruments and derivatives catalog
- **Manual de Normas** – Regulatory requirements

### RFB (Brazilian Federal Revenue)
- **e-Financeira** – Electronic financial reporting
- **SPED** – Electronic data exchange system
- **ECF** – Financial institutions data

### Open Banking
- **API specifications** – Data sharing standards
- **Security requirements** – Auth and encryption
- **Integration patterns** – System interoperability

---

## Decision: Which Agent?

| Phase | Agent | Use Case |
|-------|-------|----------|
| Understanding requirements | ring:finops-analyzer | Analyze specs, identify fields |
| Validating mappings | ring:finops-analyzer | Confirm correctness, validate |
| Generating templates | ring:finops-automation | Create .tpl files, finalize |

---

## When to Use FinOps Agents

### Use ring:finops-analyzer for:
- ✅ **Understanding regulations** – What does BACEN require?
- ✅ **Compliance research** – How do we map our data?
- ✅ **Requirement analysis** – Which fields are required?
- ✅ **Validation** – Does our mapping match the spec?

### Use ring:finops-automation for:
- ✅ **Template creation** – Build .tpl files
- ✅ **Specification execution** – Convert analysis to templates
- ✅ **Reporter platform prep** – Generate deployment files
- ✅ **Production readiness** – Finalize compliance implementation

---

## Dispatching Multiple FinOps Agents

If you need both analysis and template generation, **dispatch sequentially** (analyze first, then automate):

```
Workflow:
Step 1: Dispatch ring:finops-analyzer
  └─ Returns: compliance analysis
Step 2: Dispatch ring:finops-automation
  └─ Returns: .tpl templates

Note: These must run sequentially because automation depends on analysis.
```

---

## ORCHESTRATOR Principle

Remember:
- **You're the orchestrator** – Dispatch agents, don't implement compliance manually
- **Don't write BACEN specs yourself** – Dispatch analyzer to understand
- **Don't generate templates by hand** – Dispatch automation agent
- **Combine with ring:using-ring principle** – Skills + Agents = complete workflow

### Good Example (ORCHESTRATOR):
> "I need BACEN compliance. Let me dispatch ring:finops-analyzer to understand requirements, then ring:finops-automation to generate templates."

### Bad Example (OPERATOR):
> "I'll manually read BACEN documentation and write templates myself."

---

## Reporter Platform Integration

Generated .tpl files integrate directly with Reporter platform:
- **Input:** Validated specifications from ring:finops-analyzer
- **Output:** .tpl files (XML, HTML, TXT formats)
- **Deployment:** Direct integration with Reporter
- **Validation:** Compliance verified by template structure

---

## Available in This Plugin

**Agents:**
- ring:finops-analyzer (Gate 1-2)
- ring:finops-automation (Gate 3)

**Skills:**
- using-finops-team (this skill - plugin introduction)
- regulatory-templates (overview/index skill)
- regulatory-templates-setup (Gate 0: Setup & initialization)
- regulatory-templates-gate1 (Gate 1: Compliance analysis)
- regulatory-templates-gate2 (Gate 2: Field mapping & validation)
- regulatory-templates-gate3 (Gate 3: Template generation)

**Note:** If agents are unavailable, check if ring-finops-team is enabled in `.claude-plugin/marketplace.json`.

---

## Integration with Other Plugins

- **ring:using-ring** (default) – ORCHESTRATOR principle for ALL agents
- **ring:using-dev-team** – Developer specialists
- **ring:using-pm-team** – Pre-dev workflow agents

Dispatch based on your need:
- General code review → default plugin agents
- Regulatory compliance → ring-finops-team agents
- Developer expertise → ring-dev-team agents
- Feature planning → ring-pm-team agents
