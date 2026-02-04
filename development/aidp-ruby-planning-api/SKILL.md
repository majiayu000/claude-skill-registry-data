---
id: ruby_aidp_planning
name: AIDP Ruby Planning API
description: Expert in using AIDP's Ruby planning utilities (parsers, generators, mappers, builders)
version: 1.0.0
expertise:
  - AIDP Planning module Ruby API
  - DocumentParser for parsing existing docs
  - WBSGenerator for work breakdown structures
  - GanttGenerator for Mermaid charts
  - PersonaMapper for ZFC-based task assignment
  - ProjectPlanBuilder for plan orchestration
keywords:
  - aidp
  - ruby
  - planning
  - wbs
  - gantt
  - personas
when_to_use:
  - Implementing AIDP planning workflows in Ruby
  - Using AIDP's Planning module classes
  - Generating WBS, Gantt charts, or persona assignments
  - Parsing documentation with AIDP utilities
when_not_to_use:
  - Non-Ruby implementations
  - Non-AIDP projects
  - Language-agnostic planning (use generic templates)
compatible_providers:
  - anthropic
  - openai
  - cursor
  - codex
---

# AIDP Ruby Planning API

You are an expert in **AIDP's Ruby Planning API**. Your role is to implement planning workflows using AIDP's built-in Ruby utilities for parsing documents, generating work breakdowns, creating Gantt charts, and mapping tasks to personas.

## AIDP Planning Module Structure

```text
lib/aidp/planning/
├── parsers/
│   └── document_parser.rb      # Parse existing documentation
├── generators/
│   ├── wbs_generator.rb        # Generate work breakdown structure
│   └── gantt_generator.rb      # Generate Gantt charts
├── mappers/
│   └── persona_mapper.rb       # Map tasks to personas (ZFC)
└── builders/
    └── project_plan_builder.rb # Orchestrate plan generation
```

## Module Namespaces

All planning utilities are under the `Aidp::Planning` namespace:

- `Aidp::Planning::Parsers::DocumentParser`
- `Aidp::Planning::Generators::WBSGenerator`
- `Aidp::Planning::Generators::GanttGenerator`
- `Aidp::Planning::Mappers::PersonaMapper`
- `Aidp::Planning::Builders::ProjectPlanBuilder`

## 1. DocumentParser

### Purpose

Parse existing markdown documentation to extract structured information.

### Usage

```ruby
require_relative 'lib/aidp/planning/parsers/document_parser'

# Create parser (optionally with AI decision engine for ZFC)
parser = Aidp::Planning::Parsers::DocumentParser.new
# OR with AI engine:
# parser = Aidp::Planning::Parsers::DocumentParser.new(ai_decision_engine: ai_engine)

# Parse a single file
parsed = parser.parse_file('.aidp/docs/PRD.md')
# Returns: {
#   path: "...",
#   type: :prd/:design/:adr/:task_list/:unknown,
#   sections: { "section_name" => "content", ... },
#   raw_content: "..."
# }

# Parse entire directory
docs = parser.parse_directory('.aidp/docs')
# Returns array of parsed documents
```

### Document Type Detection

Uses Zero Framework Cognition (ZFC) when AI engine is available, falls back to heuristics:

- `:prd` - Product requirements document
- `:design` - Technical design document
- `:adr` - Architecture decision record
- `:task_list` - Task list
- `:unknown` - Unrecognized type

### Section Extraction

Automatically extracts markdown sections based on `#` and `##` headers:

```ruby
parsed[:sections]
# => {
#   "problem_statement" => "content...",
#   "goals" => "content...",
#   "success_criteria" => "content..."
# }
```

## 2. WBSGenerator

### Purpose

Generate hierarchical Work Breakdown Structure with phases and tasks.

### Usage

```ruby
require_relative 'lib/aidp/planning/generators/wbs_generator'

# Create generator
generator = Aidp::Planning::Generators::WBSGenerator.new

# Optional: Custom phases
generator = Aidp::Planning::Generators::WBSGenerator.new(
  phases: ["Planning", "Development", "Testing", "Launch"]
)

# Generate WBS from PRD and design
wbs = generator.generate(prd: parsed_prd, tech_design: parsed_design)
# Returns: {
#   phases: [
#     { name: "Requirements", description: "...", tasks: [...] },
#     { name: "Design", description: "...", tasks: [...] },
#     ...
#   ],
#   metadata: {
#     generated_at: "...",
#     phase_count: 5,
#     total_tasks: 23
#   }
# }

# Format as markdown
markdown = generator.format_as_markdown(wbs)
File.write('.aidp/docs/WBS.md', markdown)
```

### Default Phases

1. **Requirements** - Gather and document all requirements
2. **Design** - Design system architecture and components
3. **Implementation** - Implement features and functionality
4. **Testing** - Test all features and fix bugs
5. **Deployment** - Deploy to production and monitor

### Task Structure

Each task includes:

```ruby
{
  name: "Design system architecture",
  description: "Create high-level architecture diagram...",
  effort: "5 story points",
  dependencies: ["Document functional requirements"],
  subtasks: [
    { name: "Subtask 1" },
    { name: "Subtask 2" }
  ]
}
```

## 3. GanttGenerator

### Purpose

Generate Mermaid Gantt charts with critical path analysis.

### Usage

```ruby
require_relative 'lib/aidp/planning/generators/gantt_generator'

# Create generator
generator = Aidp::Planning::Generators::GanttGenerator.new

# Generate Gantt chart from WBS
gantt = generator.generate(wbs: wbs)
# Returns: {
#   tasks: [
#     { id: "task1", name: "...", phase: "...", duration: 3, dependencies: [] },
#     ...
#   ],
#   critical_path: ["task1", "task3", "task7"],
#   mermaid: "gantt\n    title Project Timeline\n    ...",
#   metadata: {
#     generated_at: "...",
#     total_tasks: 23,
#     critical_path_length: 8
#   }
# }

# Format as Mermaid syntax
mermaid_chart = gantt[:mermaid]
# => "gantt
#         title Project Timeline
#         dateFormat YYYY-MM-DD
#         section Requirements
#         Task 1 :crit, task1, 2d
#         Task 2 :task2, after task1, 1d
#         ..."

# Write output with critical path
output = ["# Project Gantt Chart", ""]
output << "```mermaid"
output << gantt[:mermaid]
output << "```"
output << ""
output << "## Critical Path"
output << ""
gantt[:critical_path].each_with_index do |task_id, idx|
  output << "#{idx + 1}. #{task_id}"
end

File.write('.aidp/docs/GANTT.md', output.join("\n"))
```

### Duration Calculation

Converts story points to days:

- 1 story point = 0.5 days
- Minimum duration = 1 day

### Critical Path

The critical path is the longest sequence of dependent tasks. Any delay in critical path tasks delays the entire project.

## 4. PersonaMapper

### Purpose

Map tasks to personas using Zero Framework Cognition (NO heuristics!).

### Usage

```ruby
require_relative 'lib/aidp/planning/mappers/persona_mapper'

# Create mapper with AI decision engine (REQUIRED for ZFC)
mapper = Aidp::Planning::Mappers::PersonaMapper.new(
  ai_decision_engine: ai_engine
)

# Assign personas to tasks
assignments = mapper.assign_personas(
  gantt[:tasks],
  available_personas: [
    "product_strategist",
    "architect",
    "senior_developer",
    "qa_engineer",
    "devops_engineer",
    "tech_writer"
  ]
)
# Returns: {
#   assignments: {
#     "task1" => {
#       persona: "architect",
#       task: "Design system architecture",
#       phase: "Design",
#       rationale: "AI-determined based on task characteristics"
#     },
#     ...
#   },
#   metadata: {
#     generated_at: "...",
#     total_assignments: 23,
#     personas_used: ["architect", "senior_developer", "qa_engineer"]
#   }
# }

# Generate YAML configuration
yaml_config = mapper.generate_persona_map(assignments)
File.write('.aidp/docs/persona_map.yml', yaml_config)
```

### Zero Framework Cognition (ZFC)

**CRITICAL**: PersonaMapper uses `AIDecisionEngine.decide()` for ALL assignments.

**NEVER use**:

- Regex pattern matching
- Keyword matching
- Heuristic rules
- Scoring formulas

The AI makes semantic decisions based on:

- Task type and complexity
- Required skills and expertise
- Project phase
- Technical vs. product focus

### Default Personas

- `product_strategist` - Product requirements, user research, stakeholder management
- `architect` - System design, architecture decisions, technology choices
- `senior_developer` - Implementation, code quality, technical problem solving
- `qa_engineer` - Testing strategy, test implementation, quality assurance
- `devops_engineer` - Infrastructure, CI/CD, deployment, monitoring
- `tech_writer` - Documentation, user guides, API documentation

## 5. ProjectPlanBuilder

### Purpose

Orchestrate all generators and assemble complete project plan.

### Usage

```ruby
require_relative 'lib/aidp/planning/builders/project_plan_builder'

# Create builder with AI engine and optional component injection
builder = Aidp::Planning::Builders::ProjectPlanBuilder.new(
  ai_decision_engine: ai_engine
)

# Build from existing documentation (ingestion path)
plan_components = builder.build_from_ingestion('.aidp/docs')
# Parses directory, generates WBS, Gantt, personas, assembles plan

# Build from scratch (generation path)
plan_components = builder.build_from_scratch(
  problem: "Problem to solve",
  goals: "Project goals",
  success_criteria: "Success metrics"
)

# Assemble complete project plan document
project_plan_md = builder.assemble_project_plan(plan_components)
File.write('.aidp/docs/PROJECT_PLAN.md', project_plan_md)
```

### Plan Components

```ruby
{
  prd: parsed_prd,
  tech_design: parsed_design,
  wbs: wbs_structure,
  wbs_markdown: wbs_formatted,
  gantt: gantt_data,
  gantt_mermaid: mermaid_chart,
  critical_path: ["task1", "task5", "task9"],
  persona_assignments: assignments
}
```

### Assembled Plan Structure

The assembled PROJECT_PLAN.md includes:

1. **Executive Summary**
2. **Work Breakdown Structure** (full WBS)
3. **Timeline and Gantt Chart** (Mermaid visualization)
4. **Critical Path** (task list)
5. **Persona Assignments** (grouped by persona)
6. **Metadata** (phase count, task count, personas used)

## Complete Example Workflow

### Scenario: Generate Complete Project Plan

```ruby
require_relative 'lib/aidp/planning/parsers/document_parser'
require_relative 'lib/aidp/planning/generators/wbs_generator'
require_relative 'lib/aidp/planning/generators/gantt_generator'
require_relative 'lib/aidp/planning/mappers/persona_mapper'
require_relative 'lib/aidp/planning/builders/project_plan_builder'

# Get AI decision engine (from AIDP configuration)
ai_engine = get_ai_decision_engine  # Implementation-specific

# 1. Parse existing documentation
parser = Aidp::Planning::Parsers::DocumentParser.new(ai_decision_engine: ai_engine)
prd = parser.parse_file('.aidp/docs/PRD.md')
tech_design = parser.parse_file('.aidp/docs/TECH_DESIGN.md')

# 2. Generate WBS
wbs_generator = Aidp::Planning::Generators::WBSGenerator.new
wbs = wbs_generator.generate(prd: prd, tech_design: tech_design)
wbs_markdown = wbs_generator.format_as_markdown(wbs)
File.write('.aidp/docs/WBS.md', wbs_markdown)

# 3. Generate Gantt chart
gantt_generator = Aidp::Planning::Generators::GanttGenerator.new
gantt = gantt_generator.generate(wbs: wbs)
File.write('.aidp/docs/GANTT.md', gantt[:mermaid])

# 4. Assign personas
persona_mapper = Aidp::Planning::Mappers::PersonaMapper.new(ai_decision_engine: ai_engine)
assignments = persona_mapper.assign_personas(gantt[:tasks])
persona_yaml = persona_mapper.generate_persona_map(assignments)
File.write('.aidp/docs/persona_map.yml', persona_yaml)

# 5. Assemble complete plan
builder = Aidp::Planning::Builders::ProjectPlanBuilder.new(ai_decision_engine: ai_engine)
components = {
  prd: prd,
  tech_design: tech_design,
  wbs: wbs,
  wbs_markdown: wbs_markdown,
  gantt: gantt,
  gantt_mermaid: gantt[:mermaid],
  critical_path: gantt[:critical_path],
  persona_assignments: assignments
}
project_plan = builder.assemble_project_plan(components)
File.write('.aidp/docs/PROJECT_PLAN.md', project_plan)
```

## Dependency Injection for Testing

All classes support dependency injection for testing:

```ruby
# Custom parser for testing
mock_parser = double("DocumentParser")
wbs_gen = WBSGenerator.new
gantt_gen = GanttGenerator.new
persona_mapper = PersonaMapper.new(ai_decision_engine: mock_ai)

builder = ProjectPlanBuilder.new(
  ai_decision_engine: mock_ai,
  document_parser: mock_parser,
  wbs_generator: wbs_gen,
  gantt_generator: gantt_gen,
  persona_mapper: persona_mapper
)
```

## Error Handling

All classes follow AIDP error handling patterns:

```ruby
begin
  parsed = parser.parse_file(file_path)
rescue ArgumentError => e
  # File not found or invalid path
  Aidp.log_error("document_parser", "parse_failed", error: e.message, path: file_path)
  raise
end
```

## Logging

All classes use `Aidp.log_debug()` extensively:

```ruby
Aidp.log_debug("wbs_generator", "generate", has_prd: true, has_design: true)
Aidp.log_debug("gantt_generator", "critical_path_found", length: 8, duration: 42)
Aidp.log_debug("persona_mapper", "assigned", task: "Design API", persona: "architect")
```

## Configuration

Access waterfall configuration:

```ruby
config = Aidp::Config.waterfall_config
# Returns configuration hash with effort estimation and persona settings
```

## Best Practices

1. **Always provide AI decision engine** to PersonaMapper for ZFC
2. **Use dependency injection** for testing
3. **Log extensively** with Aidp.log_debug()
4. **Handle errors gracefully** and let them bubble up
5. **Write output files** in `.aidp/docs/` directory
6. **Follow Ruby style** (snake_case, keyword args, etc.)

**Remember: These are generic planning utilities usable by ANY workflow, not just waterfall!**
