---
name: create-questions
description: Build interactive CLI questionnaires with validation, conditional logic, parameter mapping, and review capabilities using the question-and-answer library
---

# Question and Answer Library Integration

You are helping developers integrate the `question-and-answer` library into their Node.js projects. This library provides command-line question and answer functionality for building interactive CLI interrogations.

## When to Use This Skill

Use this skill when the user wants to:
- Create interactive CLI questionnaires or wizards
- Build user onboarding flows
- Generate configuration files interactively
- Collect user input with validation
- Create surveys or forms in CLI applications
- Implement conditional question flows

## Installation

```bash
npm install question-and-answer
```

## Core Architecture

The library centers on the `Questioner` class, which processes an **interrogation bundle** - an array of actions that execute sequentially. Each action is one of four types:

1. **Question** - Prompts user for input and stores in a parameter
2. **Statement** - Displays text to the user
3. **Map** - Derives new parameters from existing ones using expressions
4. **Review** - Allows user to review and modify previous answers

## Basic Implementation Pattern

```javascript
import { Questioner } from 'question-and-answer'

const interactions = [
  // Array of action objects
]

const questioner = new Questioner({ interactions })
await questioner.question()

// Access results
const value = questioner.get('PARAMETER_NAME')
```

## Action Types

### Question Actions

Questions MUST have:
- `prompt` - The question text
- `parameter` - Variable name to store the answer

Questions MAY have:
- `type` - "boolean", "integer", "numeric", or "string" (default)
- `default` - Default value
- `options` - Array of choices (creates selection menu)
- `multiValue` - Boolean, allows multiple comma-separated answers
- `separator` - Custom separator for multiValue (default: comma)
- `condition` - Expression; skip if falsy
- `validations` - Object with validation rules
- `noSkipDefined` - Boolean, ask even if parameter already defined

```javascript
{
  prompt: "What is your name?",
  parameter: "USER_NAME"
}

{
  prompt: "Choose a color",
  options: ["red", "blue", "green"],
  parameter: "COLOR"
}

{
  prompt: "Enable debug mode?",
  type: "boolean",
  parameter: "DEBUG",
  default: false
}
```

### Statement Actions

Statements display text without user input:

```javascript
{
  statement: "Welcome to the configuration wizard!"
}

{
  statement: "<warn>Warning:<rst> This will overwrite existing files",
  condition: "FILES_EXIST === true"
}
```

### Map Actions

Maps derive new parameters from existing ones:

```javascript
{
  maps: [
    {
      source: "AGE >= 18",
      parameter: "IS_ADULT",
      type: "boolean"
    },
    {
      source: "PRICE * QUANTITY",
      parameter: "TOTAL",
      type: "numeric"
    },
    {
      value: "literal-value",
      parameter: "CONSTANT"
    }
  ]
}
```

Maps use [condition-eval](https://github.com/liquid-labs/condition-eval) syntax for `source` expressions.

### Review Actions

Reviews let users verify and modify answers:

```javascript
{
  review: "questions"  // Only review questions
}

{
  review: "maps"  // Only review maps
}

{
  review: "all"  // Review both
}
```

During review:
- Press ENTER to accept current value
- Enter new value to change
- Enter `-` to clear value
- If rejected, interrogation restarts

## Validation

Use the `validations` object with [specify-string](https://github.com/liquid-labs/specify-string) format:

```javascript
{
  prompt: "Enter email",
  parameter: "EMAIL",
  validations: {
    "match-regexp": "^[^@]+@[^@]+\\.[^@]+$"
  }
}

{
  prompt: "Rate 1-10",
  type: "integer",
  parameter: "RATING",
  validations: {
    "min-value": 1,
    "max-value": 10
  }
}

{
  prompt: "Select 2-3 options",
  multiValue: true,
  options: ["A", "B", "C", "D"],
  parameter: "CHOICES",
  validations: {
    "min-count": 2,
    "max-count": 3
  }
}
```

Common validation keys:
- `min-length`, `max-length` - String length
- `min-value`, `max-value` - Numeric range
- `min-count`, `max-count` - Multi-value count
- `require-exact` - Exact match required
- `require-truthy`, `require-falsy` - Boolean validation
- `match-regexp` - Regular expression pattern

## Conditional Logic

Any action can have a `condition` field with an expression:

```javascript
{
  prompt: "Enter API key",
  parameter: "API_KEY",
  condition: "ENVIRONMENT === 'production'"
}

{
  statement: "Debug mode is enabled",
  condition: "DEBUG === true"
}
```

Conditions use [condition-eval](https://github.com/liquid-labs/condition-eval) syntax and can reference any previously set parameter.

## Type System

The `type` field coerces answers:

- `"boolean"` or `"bool"` - Accepts: y/yes/true/n/no/false (case-insensitive)
- `"integer"` or `"int"` - Whole numbers only
- `"numeric"` or `"float"` - Decimal numbers
- `"string"` - Default, no coercion

## Accessing Results

```javascript
// Single value
const name = questioner.get('USER_NAME')

// Full result object (includes metadata)
const result = questioner.getResult('USER_NAME')

// Check existence
if (questioner.has('EMAIL')) { ... }

// All values as object
const values = questioner.values

// All results (with metadata)
const results = questioner.results

// Interrogation with dispositions
const interactions = questioner.interactions
```

## Constructor Options

```javascript
const questioner = new Questioner({
  interactions,              // Required: array of actions
  initialParameters: {},     // Optional: pre-populated values
  noSkipDefined: false,      // Optional: ask defined questions
  input: process.stdin,      // Optional: custom input stream
  output: customOutput,      // Optional: custom output handler
  printOptions: {}          // Optional: magic-print options
})
```

## Implementation Guidelines

### 1. Start Simple

Begin with basic questions, add complexity incrementally:

```javascript
const interactions = [
  { prompt: "Project name", parameter: "NAME" },
  { prompt: "Version", parameter: "VERSION", default: "1.0.0" }
]
```

### 2. Add Validation

Layer in validation for data quality:

```javascript
{
  prompt: "Project name",
  parameter: "NAME",
  validations: {
    "min-length": 1,
    "max-length": 50,
    "match-regexp": "^[a-z0-9-]+$"
  }
}
```

### 3. Use Options for Fixed Choices

When answers are constrained, use `options`:

```javascript
{
  prompt: "License",
  options: ["MIT", "Apache-2.0", "GPL-3.0", "ISC"],
  parameter: "LICENSE"
}
```

### 4. Add Conditional Logic

Build dynamic flows with conditions:

```javascript
{
  prompt: "Use TypeScript?",
  type: "boolean",
  parameter: "USE_TS"
},
{
  prompt: "TypeScript version",
  parameter: "TS_VERSION",
  default: "latest",
  condition: "USE_TS === true"
}
```

### 5. Derive Computed Values

Use maps for calculated parameters:

```javascript
{
  maps: [
    {
      source: "USE_TS === true",
      parameter: "FILE_EXTENSION",
      value: "ts"
    },
    {
      source: "USE_TS === false",
      parameter: "FILE_EXTENSION",
      value: "js"
    }
  ]
}
```

### 6. End with Review

Let users verify their answers:

```javascript
{ review: "questions" }
```

## Common Patterns

See `patterns.md` for detailed examples of:
- User onboarding flows
- Configuration wizards
- Surveys with validation
- Conditional branching
- Multi-value inputs

## Testing Interrogations

Test bundles using the CLI:

```bash
npx qna path/to/interrogation.json
```

## Important Notes

1. **Action Order Matters** - Actions execute sequentially; parameters must be defined before use in conditions/maps
2. **Parameter Skipping** - Questions/maps skip if parameter already defined (unless `noSkipDefined: true`)
3. **Condition Evaluation** - Uses condition-eval library; supports comparisons, arithmetic, logical operators
4. **Type Safety** - Always specify `type` for non-string data to ensure proper coercion
5. **Review Behavior** - Reviews collect all non-skipped questions/maps since last review
6. **Validation Timing** - Validations run immediately; invalid answers re-prompt

## Reference Materials

When you need detailed information, refer to:
- `reference.md` - Complete API reference
- `patterns.md` - Common implementation patterns
- `examples/` - Working interrogation bundles

## Code Generation

When generating interrogation bundles:
1. Wrap in proper structure: `{ "actions": [...] }`
2. Use consistent parameter naming (UPPER_SNAKE_CASE recommended)
3. Add validations for data quality
4. Include review step for important flows
5. Test with `npx qna bundle.json` before integration

## Error Handling

The library throws standard errors:
- `ArgumentInvalidError` - Validation failed
- `ArgumentMissingError` - Required field missing
- `ArgumentTypeError` - Type mismatch

Always wrap `questioner.question()` in try-catch for production use.
