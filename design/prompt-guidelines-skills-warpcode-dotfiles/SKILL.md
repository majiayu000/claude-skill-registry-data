---
name: prompt-guidelines-skills
description: >-
  Skill creation guidelines and protocols for high-fidelity, token-efficient specialized capabilities.
  Provides routing patterns, component selection criteria, and skill structure templates.
  Includes progressive disclosure patterns for routing vs reference separation.
  Scope: skill creation, skill structure, routing logic, template patterns.
  Excludes: agent creation, command creation (handled by component-specific skills).
  Triggers: skill, create a skill, edit skill, validate skill, new skill.
---

# PROMPT GUIDELINES FOR SKILLS

## CORE PHILOSOPHY
- **Goal**: High-fidelity, token-efficient specialized capabilities.
- **Principle**: Core protocols in SKILL.md. Reference files ONLY for routing scenarios (e.g., multiple distinct workflows).
- **No Artificial Limits**: SKILL.md length determined by content needs, not arbitrary constraints.

## STRUCTURE

### Directory Layout (Recommended)

#### Minimal Structure
```text
skill-name/
 ├── SKILL.md (Required - main skill file)
 └── references/ (Optional - routing scenarios only)
```

#### Recommended Structure
```text
skill-name/
 ├── SKILL.md (Required - routing logic only)
 ├── references/ (Optional - progressive disclosure)
 │   ├── modes/        # Mode-specific behavioral extensions
 │   ├── intents/      # Intent-specific workflows
 │   ├── contexts/     # Context/environment-specific patterns
 │   ├── domains/      # Domain expertise (security, database, api, etc.)
 │   └── schemas/     # Data schemas, API specs, configuration formats
 ├── templates/       # Optional - Output templates, prompt templates
 ├── scripts/         # Optional - Python/Bash scripts for deterministic tasks
 └── assets/          # Optional - Logos, icons, file templates, example files
```

### SKILL.md Constraints
- **Purpose**: Core protocols + Routing logic (if external references exist)
- **Content**: Frontmatter + Core Protocols + Routing Logic (if needed) + Glossary
- **References**: Use ONLY for distinct routing scenarios (e.g., separate workflows)
- **Prohibited**: Unnecessary content splitting - keep core information in SKILL.md

## ROUTING LOGIC PATTERN

```markdown
## ROUTING_PROTOCOL

### Mode Detection
IF "analyze" OR "explain" OR "show" detected THEN
  READ FILE: @references/modes/analyse.md
END

IF "create" OR "write" OR "edit" detected THEN
  READ FILE: @references/modes/write.md
  READ FILE: @references/output/common.md
END

IF "review" OR "check" OR "audit" detected THEN
  READ FILE: @references/modes/review.md
END

### Component-Specific Loading
IF domain-specific keywords detected THEN
  READ FILE: @references/domains/[domain].md
END

### Context-Aware Loading
IF framework/language detected THEN
  READ FILE: @references/contexts/[framework].md
END
```

## TRIGGERS FIELD BEST PRACTICES

**Purpose**: Enable reliable LLM detection via explicit keywords.

### Triggers Field Rules

**Explicit Keywords**: List specific verbs/nouns
**Action-Oriented**: "create", "edit", "validate" vs "help with"
**Domain-Specific**: Include domain terms (database, api, security, testing)
**Avoid Ambiguity**: "help" is too broad; "validate yaml schema" is specific

### Examples

❌ **Too Vague**:
```yaml
description: >-
  Helps with various coding tasks.
  Triggers: help, assist, support
```

✅ **Specific & Actionable**:
```yaml
description: >-
  Database schema design and query optimization for PostgreSQL.
  Scope: table structure, indexes, migrations, performance tuning.
  Excludes: application logic, frontend work.
  Triggers: database, schema, query optimization, migration, postgres, sql
```

### Keyword Expansion Patterns

**Basic (insufficient)**:
```bash
skill: "skill"
```

**Expanded (flexible + deterministic)**:
```bash
skill: "skill|create.*skill|new.*skill|add.*skill|edit.*skill|build.*skill"
```

### Routing Implementation

- Expand keyword lists with regex patterns for flexibility
- Log which keywords matched for debugging
- Provide fallback for unrecognized: "Clarify: what do you need help with?"
- Avoid over-matching: generic = false positives

## RESOURCE MANAGEMENT

- **Scripts**: Deterministic tasks (PDF rotate, Data processing). Path: `@scripts/`.
- **References**: Heavy context (API Docs, Schemas). Path: `@references/`.
- **Rule**: You MUST load resources IMMEDIATELY when task requires specialized knowledge. Use directive: `ACTION -> READ FILE: @references/filename.md`.
- **Constraint**: ALL `@` paths (references, scripts, assets) MUST be relative to skill's main `SKILL.md` file.
- **Assets**: Output artifacts (Logos, Templates). Path: `@assets/`.

## SECURITY CONSIDERATIONS (MANDATORY)

- **Input Handling**: Always sanitize user inputs in scripts.
- **Path Safety**: Validate file paths, prevent directory traversal.
- **Command Execution**: Never use `eval()`, `subprocess` with unsanitized input.
- **Secrets**: Never log or output credentials/tokens.
- **Permissions**: Scripts run with minimal required privileges.
- **Error Messages**: Sanitized, no sensitive data exposure.

## BEST PRACTICES

- **Tone**: Imperative. "Do X. Check Y."
- **Routing**: Explicitly instruct LLM to read reference files based on intent (e.g., "IF [Condition] -> READ FILE: @references/[file].md").
- **Context**: Assume LLM intelligence. Don't explain *why*, just *what*.
- **Triggers**: Description must contain specific keywords/filetypes.
- **Validation**:
  - YAML valid?
  - Paths relative (using `@` syntax)?
  - Dependencies listed?
  - Routing logic explicit?

## REFERENCE FILE GUIDELINES

### Reference Headers
- **Mandatory**: # PURPOSE
- **Recommended**: # TRIGGER_CONDITIONS (when to load)
- **Content**: STM-formatted rules and patterns

### No Circular Dependencies
- Reference A references B
- B references C
- C must NOT reference A

## SKILL TEMPLATE

```markdown
---
name: skill-name
description: >-
  [One-line purpose]
  Scope: [key capabilities]
  Excludes: [exclusions - domain skills only]
  Triggers: [keywords for routing]
---

# SKILL_NAME

## ROUTING_PROTOCOL

### Mode Detection
IF "analyze" OR "explain" OR "show" detected THEN
  READ FILE: @references/modes/analyse.md
END

IF "create" OR "write" OR "edit" OR "update" detected THEN
  READ FILE: @references/modes/write.md
  READ FILE: @references/output/common.md
END

IF "review" OR "check" OR "audit" OR "validate" OR "compliance" detected THEN
  READ FILE: @references/modes/review.md
  READ FILE: @references/output/severity-classification.md
END

IF "plan" OR "design" OR "breakdown" OR "estimate" detected THEN
  READ FILE: @references/modes/plan.md
  READ FILE: @references/output/jira-structure.md
END

IF "teach" OR "explain" OR "guide" OR "tutorial" detected THEN
  READ FILE: @references/modes/teach.md
END

### Domain-Specific Routing
IF [domain keyword 1] detected THEN
  READ FILE: @references/domains/[domain1].md
END

IF [domain keyword 2] detected THEN
  READ FILE: @references/domains/[domain2].md
END

### Context-Aware Routing
IF framework/language detected THEN
  READ FILE: @references/contexts/[framework].md
END

### Security Context
IF destructive OR "sudo" OR "rm" OR "security" OR "validation" detected THEN
  READ FILE: @references/core/security.md
  READ FILE: @references/core/validation.md
END

## GLOSSARY [RECOMMENDED when abbreviations exist]

**TERM1**: [Definition]
**TERM2**: [Definition]
```

## COMPONENT CREATION ADVISOR

### Role
Implementation_Advisor

### Goal
Analyze Req -> Score -> Recommend(Skill|Agent|Command|Hybrid|Tool)

### ENTITY DEFINITIONS

#### 1. SKILL
- **Atomic**: Single, well-defined operation
- **Reusable**: High reuse, auto-invoke, natural flow
- **Constraints**: Prompt engineering required, single purpose
- **Best_For**: Atomic ops, high frequency, utilities, data transform

#### 2. AGENT
- **Autonomous**: Multi-step workflow, adaptive
- **Context_Synth**: High context synthesis capability
- **Constraints**: Design complexity high, latency high, predictability low
- **Best_For**: Research, debugging, refactoring, system analysis

#### 3. COMMAND
- **Static**: CLI instruction, predictable
- **Speed**: Fast, scriptable
- **Constraints**: Flexibility low, discovery hard, inputs rigid
- **Best_For**: Deployment, migrations, boilerplate, test execution

#### 4. HYBRID
- **Composite**: Command → Agent → Skill
- **Flexibility**: Maximum, separation of concerns high
- **Constraints**: Maintenance overhead high, learning curve steep
- **Best_For**: Large workflows, mixed requirements (simple + complex)

#### 5. CUSTOM TOOL
- **External**: API/service integration
- **Control**: Full control, persistent state, max performance
- **Constraints**: Hosting required, auth complexity high, portability low
- **Best_For**: DB operations, Jira/Linear, heavy compute, security ops

### SCORING MATRICES

#### SKILL (Threshold: 8/12)
- **Atomic**: Single, well-defined operation? (Weight: 3)
- **Reusable**: Repeated use across projects? (Weight: 2)
- **One_Shot**: Complete in one invocation? (Weight: 3)
- **I/O**: Inputs/outputs clear? (Weight: 2)
- **Concise**: Explainable in simple prompt? (Weight: 2)

#### AGENT (Threshold: 8/12)
- **Multi_Step**: Requires multiple sequential steps? (Weight: 3)
- **Decisions**: Requires decision-making/judgment? (Weight: 3)
- **Branching**: Workflow conditional/branching? (Weight: 2)
- **Tools**: Needs multiple tools/sources? (Weight: 2)
- **Dynamic**: Path NOT predictable upfront? (Weight: 2)

#### COMMAND (Threshold: 7/11)
- **Static**: Operation always identical? (Weight: 3)
- **Params**: Parameters defined upfront? (Weight: 3)
- **Speed**: Execution speed critical? (Weight: 2)
- **No_AI**: Should bypass AI interpretation? (Weight: 2)
- **Script**: Intended for automation/scripting? (Weight: 1)

#### HYBRID (Threshold: 7/10)
- **Mixed_Ops**: Involves BOTH simple & complex ops? (Weight: 3)
- **Optimization**: Parts benefit from different approaches? (Weight: 3)
- **System**: Part of larger ecosystem? (Weight: 2)
- **Flexibility**: Needs automation AND adaptability? (Weight: 2)

#### CUSTOM TOOL (Threshold: 7/11)
- **External**: Requires external APIs/Services? (Weight: 3)
- **Deps**: Specific libraries/dependencies needed? (Weight: 3)
- **State**: Persistent state/DB required? (Weight: 2)
- **Security**: Compliance/Auth requirements? (Weight: 2)
- **Compute**: Computationally intensive? (Weight: 1)

### HEURISTICS

#### DECISION FRAMEWORK
1. **Simplicity_First**: Simple > Complex. Command/Skill > Agent.
2. **Frequency_Gradient**:
   - One_time -> Manual/Script
   - Occasional -> Skill/Command
   - Frequent -> Command(Speed) || Skill(Flex)
   - Continuous -> Agent/Tool
3. **Complexity_Gradient**:
   - 1 Op -> Command/Skill
   - 2-3 Ops -> Skill
   - 4-10 Ops -> Agent/Hybrid
   - 10+ Ops -> Hybrid/Tool
4. **User_Expertise**:
   - Beginner -> Skill (Discoverable)
   - Intermediate -> Command/Skill
   - Advanced -> Agent/Hybrid
5. **Scope**:
   - Individual -> Personal_Workflow
   - Team -> Documentation/Consistency
   - Org -> Custom_Tool (Standardization)

### RED FLAGS (Anti-Patterns)
- **Skill**: Steps > 3 || State_Persistence == True || Logic_Branching(Complex)
- **Agent**: Workflow == Linear/Predictable || Speed > Flexibility || Output_Deterministic(Strict)
- **Command**: Logic == Fuzzy || Context_Sensitive(High) || Params(Wildly_Variable)
- **Tool**: Task_Covered_By_Existing || Maint_Resources(None) || Reqs(Volatile)

### EXECUTION

#### PHASE 1: CLARIFY
- IF Input.Ambiguous -> Ask("Frequency? Complexity? User_Base?").
- IF Input.Vague -> Ask("Describe workflow step-by-step.").

#### PHASE 2: EVALUATE
- **Action**: Score User_Case against criteria section.
- **Apply**: Heuristics to refine selection.

#### PHASE 3: RECOMMEND
- **Selection**: `Winner == Max(Score) && Score >= Threshold`.
- **Tie_Breaker**: Prefer Simplicity (Command > Skill > Agent).

#### PHASE 4: REPORT
- **Output_Structure**:
   1. **Analysis**: Restate Req + Breakdown
   2. **Evaluation**: Show Scores/Matches for top methods
   3. **Verdict**: `RECOMMENDATION: [TYPE]` + Confidence(%)
   4. **Why**: Justify using Attributes & Heuristics
   5. **Implementation**:
      - Step 1..N
      - **Challenges**: List risks + mitigations
   6. **Alternative**: Next best option + Trade-off
   7. **Next_Steps**: Actionable items

## OPTIONAL CONTENT

For additional implementation guidance beyond skill creation patterns above, see:
@references/routing/implementation-advisor.md
