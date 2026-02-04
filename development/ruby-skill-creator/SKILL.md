---
name: ruby-skill-creator
description: Create new Claude Code Skills using Ruby as the control flow language. Use this skill when users want to author Skills with programmatic logic, conditionals, loops, and dynamic behavior using Ruby code. Ideal for Skills requiring IF/THEN conditionals, variable-driven control flow, dynamic file references, or complex multi-step workflows that benefit from a programming language over static markdown.
---

# Ruby Skill Creator

Create Claude Code Skills where Ruby serves as the orchestration and control flow language.

## Overview

This skill enables authoring new Skills using Ruby code to implement:

- **Conditional logic** - IF/THEN branching based on user input or context
- **Control flow** - Loops, switches, and dynamic routing
- **Variable management** - Constants and state that influence behavior
- **File orchestration** - Programmatic reference to cookbook/prompt/tool files
- **Dynamic output** - Generate instructions based on runtime evaluation

## Skill Structure

```
.claude/skills/skill-name/
├── SKILL.md              # Entry point - loads and executes skill.rb
├── skill.rb              # Main Ruby skill definition (required)
├── cookbook/             # Instruction modules loaded conditionally
│   ├── variant_a.md
│   └── variant_b.md
├── prompts/              # User-facing prompt templates
│   └── example_prompt.md
├── tools/                # Ruby helper scripts and utilities
│   ├── helpers.rb
│   └── validators.rb
└── references/           # Domain knowledge loaded as needed
    └── api_docs.md
```

## Ruby Skill Definition API

The `skill.rb` file defines skill behavior using a Ruby DSL. Claude reads and interprets this file to determine how to proceed.

### Core DSL Methods

```ruby
# skill.rb - Main skill definition

# Constants influencing control flow
CONSTANTS = {
  output_format: "markdown",      # markdown | json | html
  strict_mode: true,              # Enable validation
  max_iterations: 5,              # Loop limits
  default_variant: "standard"     # Default cookbook variant
}

# Entry point - Claude calls this to begin
def execute(context)
  # context.user_input   - The user's request
  # context.files        - Uploaded files
  # context.conversation - Conversation history
  
  variant = determine_variant(context.user_input)
  load_cookbook(variant)
  
  if context.files.any?
    process_files(context.files)
  end
  
  generate_output(context)
end

# Conditional cookbook loading
def determine_variant(input)
  case input
  when /fast|quick|simple/i
    "lightweight"
  when /detailed|comprehensive|thorough/i
    "comprehensive"
  when /api|integration|connect/i
    "api_integration"
  else
    CONSTANTS[:default_variant]
  end
end

# Load cookbook instructions
def load_cookbook(variant)
  cookbook_path = "cookbook/#{variant}.md"
  read_file(cookbook_path)
end

# Conditional file processing
def process_files(files)
  files.each do |file|
    case file.extension
    when ".pdf"
      load_tool("tools/pdf_processor.rb")
    when ".csv", ".xlsx"
      load_tool("tools/data_processor.rb")
    when ".rb", ".py", ".js"
      load_tool("tools/code_analyzer.rb")
    end
  end
end

# Dynamic output generation
def generate_output(context)
  template = read_file("prompts/output_template.md")
  
  if CONSTANTS[:strict_mode]
    validate_output(template)
  end
  
  render(template, context)
end
```

### Available DSL Methods

| Method | Description |
|--------|-------------|
| `read_file(path)` | Load file contents into context |
| `load_cookbook(name)` | Load cookbook/`name`.md instructions |
| `load_tool(path)` | Load and prepare Ruby tool for execution |
| `load_prompt(name)` | Load prompts/`name`.md template |
| `load_reference(name)` | Load references/`name`.md documentation |
| `render(template, vars)` | Interpolate variables into template |
| `validate(data, schema)` | Validate data against schema |
| `emit(instruction)` | Output instruction to Claude |
| `ask_user(question)` | Request clarification from user |
| `execute_tool(tool, args)` | Run a tool script with arguments |

### Control Flow Patterns

#### Pattern 1: Conditional Cookbook Selection

```ruby
def execute(context)
  cookbook = case
    when context.user_input.match?(/create|new|generate/)
      "creation"
    when context.user_input.match?(/edit|modify|update/)
      "modification"
    when context.user_input.match?(/analyze|review|check/)
      "analysis"
    else
      "general"
  end
  
  load_cookbook(cookbook)
  emit "Follow the #{cookbook} workflow above."
end
```

#### Pattern 2: Multi-Step Workflow

```ruby
WORKFLOW_STEPS = [:gather, :validate, :process, :output]

def execute(context)
  state = { current_step: 0, data: {} }
  
  WORKFLOW_STEPS.each_with_index do |step, index|
    state[:current_step] = index
    
    case step
    when :gather
      load_cookbook("gather_requirements")
      state[:data][:requirements] = gather_from_user(context)
    when :validate
      load_tool("tools/validator.rb")
      unless validate(state[:data][:requirements])
        emit "Validation failed. Please review requirements."
        return
      end
    when :process
      load_cookbook("processing")
      state[:data][:result] = process(state[:data][:requirements])
    when :output
      load_prompt("final_output")
      render_final(state[:data])
    end
  end
end
```

#### Pattern 3: Feature Flags

```ruby
FEATURES = {
  enhanced_validation: true,
  experimental_output: false,
  strict_formatting: true,
  verbose_logging: false
}

def execute(context)
  load_cookbook("base")
  
  if FEATURES[:enhanced_validation]
    load_cookbook("validation_enhanced")
  end
  
  if FEATURES[:experimental_output]
    load_cookbook("output_experimental")
  else
    load_cookbook("output_standard")
  end
  
  if FEATURES[:strict_formatting]
    emit "Apply strict formatting rules from cookbook."
  end
end
```

#### Pattern 4: Input-Driven Routing

```ruby
ROUTES = {
  /\b(pdf|document)\b/i => "document_processing",
  /\b(image|photo|picture)\b/i => "image_handling",
  /\b(data|csv|excel)\b/i => "data_analysis",
  /\b(code|script|program)\b/i => "code_review"
}

def execute(context)
  route = ROUTES.find { |pattern, _| context.user_input.match?(pattern) }
  
  if route
    cookbook_name = route[1]
    load_cookbook(cookbook_name)
    emit "Proceeding with #{cookbook_name} workflow."
  else
    load_cookbook("general")
    emit "Using general workflow. Clarify if specific handling needed."
  end
end
```

## Creating a New Ruby-Based Skill

### Step 1: Initialize Structure

Create the skill directory:

```bash
mkdir -p .claude/skills/my-skill/{cookbook,prompts,tools,references}
touch .claude/skills/my-skill/{SKILL.md,skill.rb}
```

### Step 2: Write SKILL.md

The SKILL.md serves as the entry point and instructs Claude to load skill.rb:

```markdown
---
name: my-skill-name
description: Clear description of what this skill does and when to trigger it.
---

# My Skill Name

This skill uses Ruby for control flow. Execute the skill definition:

1. Read `skill.rb` to understand the skill's logic
2. Evaluate the Ruby code conceptually to determine workflow
3. Follow the control flow to load appropriate cookbook/prompt/tool files
4. Execute instructions from loaded files

## Entry Point

\`\`\`ruby
# See skill.rb for full implementation
load "skill.rb"
execute(context)
\`\`\`
```

### Step 3: Implement skill.rb

Define the skill logic in Ruby:

```ruby
# skill.rb

CONSTANTS = {
  version: "1.0.0",
  default_mode: "standard"
}

def execute(context)
  mode = detect_mode(context.user_input)
  load_cookbook(mode)
  
  if requires_tools?(context)
    load_required_tools(context)
  end
  
  generate_response(context, mode)
end

def detect_mode(input)
  # Mode detection logic
end

def requires_tools?(context)
  # Tool requirement check
end

def load_required_tools(context)
  # Dynamic tool loading
end

def generate_response(context, mode)
  # Response generation
end
```

### Step 4: Create Cookbook Files

Add markdown instruction files in `cookbook/`:

```markdown
<!-- cookbook/standard.md -->
# Standard Mode Instructions

When operating in standard mode:

1. Analyze the user's request
2. Apply default formatting rules
3. Generate output following standard template

## Guidelines

- Keep responses concise
- Use consistent formatting
- Validate output before presenting
```

### Step 5: Add Prompts and Tools

Create prompt templates and Ruby helper tools as needed:

```markdown
<!-- prompts/output_template.md -->
# Output Template

## Summary
{{summary}}

## Details
{{details}}

## Next Steps
{{next_steps}}
```

```ruby
# tools/validator.rb

def validate_output(content)
  errors = []
  
  errors << "Missing summary" unless content.include?("## Summary")
  errors << "Too short" if content.length < 100
  
  { valid: errors.empty?, errors: errors }
end
```

## Example: Complete Ruby-Based Skill

See `references/complete_example.md` for a fully implemented example skill demonstrating all patterns.

## Best Practices

1. **Keep skill.rb focused** - Logic only, not content. Content lives in cookbook/prompts.
2. **Use meaningful CONSTANTS** - Document what each constant controls.
3. **Prefer pattern matching** - Ruby's case/when and regex matching for routing.
4. **Load files lazily** - Only load cookbook/tools when the branch is taken.
5. **Provide fallbacks** - Always have a default/else branch.
6. **Comment control flow** - Explain why branches exist, not what they do.

## Interpreting Ruby Skills

When Claude encounters a Ruby-based skill:

1. **Parse skill.rb** - Understand the defined methods and control flow
2. **Identify entry point** - Find the `execute(context)` method
3. **Trace execution** - Follow the logic path based on current context
4. **Load referenced files** - When `load_cookbook`, `load_tool`, etc. are called
5. **Execute instructions** - Follow the loaded markdown instructions
6. **Apply CONSTANTS** - Respect configuration values in decision-making

Claude interprets the Ruby conceptually - it does not run a Ruby interpreter, but understands the logic to determine which files to load and what instructions to follow.
