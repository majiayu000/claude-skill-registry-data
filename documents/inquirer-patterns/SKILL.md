---
name: inquirer-patterns
description: Interactive prompt patterns for CLI tools with text, list, checkbox, password, autocomplete, and conditional questions. Use when building CLIs with user input, creating interactive prompts, implementing questionnaires, or when user mentions inquirer, prompts, interactive input, CLI questions, user prompts.
allowed-tools: Read, Write, Bash
---

# Inquirer Patterns

Comprehensive interactive prompt patterns for building CLI tools with rich user input capabilities. Provides templates for text, list, checkbox, password, autocomplete, and conditional questions in both Node.js and Python.

## Instructions

### When Building Interactive CLI Prompts

1. **Identify prompt type needed:**
   - Text input: Simple string input
   - List selection: Single choice from options
   - Checkbox: Multiple selections
   - Password: Secure input (hidden)
   - Autocomplete: Type-ahead suggestions
   - Conditional: Questions based on previous answers

2. **Choose language:**
   - **Node.js**: Use templates in `templates/nodejs/`
   - **Python**: Use templates in `templates/python/`

3. **Select appropriate template:**
   - `text-prompt.js/py` - Basic text input
   - `list-prompt.js/py` - Single selection list
   - `checkbox-prompt.js/py` - Multiple selections
   - `password-prompt.js/py` - Secure password input
   - `autocomplete-prompt.js/py` - Type-ahead suggestions
   - `conditional-prompt.js/py` - Dynamic questions based on answers
   - `comprehensive-example.js/py` - All patterns combined

4. **Install required dependencies:**
   - **Node.js**: Run `scripts/install-nodejs-deps.sh`
   - **Python**: Run `scripts/install-python-deps.sh`

5. **Test prompts:**
   - Use examples in `examples/nodejs/` or `examples/python/`
   - Run validation script: `scripts/validate-prompts.sh`

6. **Customize for your CLI:**
   - Copy relevant template sections
   - Modify questions, choices, validation
   - Add custom conditional logic

### Node.js Implementation

**Library**: `inquirer` (v9.x)

**Installation**:
```bash
npm install inquirer
```

**Basic Usage**:
```javascript
import inquirer from 'inquirer';

const answers = await inquirer.prompt([
  {
    type: 'input',
    name: 'username',
    message: 'Enter your username:',
    validate: (input) => input.length > 0 || 'Username required'
  }
]);

console.log(`Hello, ${answers.username}!`);
```

### Python Implementation

**Library**: `questionary` (v2.x)

**Installation**:
```bash
pip install questionary
```

**Basic Usage**:
```python
import questionary

username = questionary.text(
    "Enter your username:",
    validate=lambda text: len(text) > 0 or "Username required"
).ask()

print(f"Hello, {username}!")
```

## Available Templates

### Node.js Templates (`templates/nodejs/`)

1. **text-prompt.js** - Text input with validation
2. **list-prompt.js** - Single selection from list
3. **checkbox-prompt.js** - Multiple selections
4. **password-prompt.js** - Secure password input with confirmation
5. **autocomplete-prompt.js** - Type-ahead with fuzzy search
6. **conditional-prompt.js** - Dynamic questions based on answers
7. **comprehensive-example.js** - Complete CLI questionnaire

### Python Templates (`templates/python/`)

1. **text_prompt.py** - Text input with validation
2. **list_prompt.py** - Single selection from list
3. **checkbox_prompt.py** - Multiple selections
4. **password_prompt.py** - Secure password input with confirmation
5. **autocomplete_prompt.py** - Type-ahead with fuzzy search
6. **conditional_prompt.py** - Dynamic questions based on answers
7. **comprehensive_example.py** - Complete CLI questionnaire

## Prompt Types Reference

### Text Input
- **Use for**: Names, emails, URLs, paths, free-form text
- **Features**: Validation, default values, transform
- **Node.js**: `{ type: 'input' }`
- **Python**: `questionary.text()`

### List Selection
- **Use for**: Single choice from predefined options
- **Features**: Arrow key navigation, search filtering
- **Node.js**: `{ type: 'list' }`
- **Python**: `questionary.select()`

### Checkbox
- **Use for**: Multiple selections from options
- **Features**: Space to toggle, Enter to confirm
- **Node.js**: `{ type: 'checkbox' }`
- **Python**: `questionary.checkbox()`

### Password
- **Use for**: Sensitive input (credentials, tokens)
- **Features**: Hidden input, confirmation, validation
- **Node.js**: `{ type: 'password' }`
- **Python**: `questionary.password()`

### Autocomplete
- **Use for**: Large option lists with search
- **Features**: Type-ahead, fuzzy matching, suggestions
- **Node.js**: `inquirer-autocomplete-prompt` plugin
- **Python**: `questionary.autocomplete()`

### Conditional Questions
- **Use for**: Dynamic forms based on previous answers
- **Features**: Skip logic, dependent questions, branching
- **Node.js**: `when` property in question config
- **Python**: Conditional logic with if statements

## Validation Patterns

### Email Validation
```javascript
// Node.js
validate: (input) => {
  const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return regex.test(input) || 'Invalid email address';
}
```

```python
# Python
def validate_email(text):
    import re
    regex = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
    return bool(re.match(regex, text)) or "Invalid email address"

questionary.text("Email:", validate=validate_email).ask()
```

### Non-Empty Validation
```javascript
// Node.js
validate: (input) => input.length > 0 || 'This field is required'
```

```python
# Python
questionary.text("Name:", validate=lambda t: len(t) > 0 or "Required").ask()
```

### Numeric Range Validation
```javascript
// Node.js
validate: (input) => {
  const num = parseInt(input);
  return (num >= 1 && num <= 100) || 'Enter number between 1-100';
}
```

```python
# Python
def validate_range(text):
    try:
        num = int(text)
        return 1 <= num <= 100 or "Enter number between 1-100"
    except ValueError:
        return "Invalid number"

questionary.text("Number:", validate=validate_range).ask()
```

## Examples

### Example 1: Project Initialization Wizard

**Use case**: Interactive CLI for scaffolding new projects

```javascript
// Node.js - See examples/nodejs/project-init.js
const answers = await inquirer.prompt([
  {
    type: 'input',
    name: 'projectName',
    message: 'Project name:',
    validate: (input) => /^[a-z0-9-]+$/.test(input) || 'Invalid project name'
  },
  {
    type: 'list',
    name: 'framework',
    message: 'Choose framework:',
    choices: ['React', 'Vue', 'Angular', 'Svelte']
  },
  {
    type: 'checkbox',
    name: 'features',
    message: 'Select features:',
    choices: ['TypeScript', 'ESLint', 'Prettier', 'Testing']
  }
]);
```

```python
# Python - See examples/python/project_init.py
import questionary

project_name = questionary.text(
    "Project name:",
    validate=lambda t: bool(re.match(r'^[a-z0-9-]+$', t)) or "Invalid name"
).ask()

framework = questionary.select(
    "Choose framework:",
    choices=['React', 'Vue', 'Angular', 'Svelte']
).ask()

features = questionary.checkbox(
    "Select features:",
    choices=['TypeScript', 'ESLint', 'Prettier', 'Testing']
).ask()
```

### Example 2: Conditional Question Flow

**Use case**: Dynamic questions based on previous answers

```javascript
// Node.js - See examples/nodejs/conditional-flow.js
const questions = [
  {
    type: 'confirm',
    name: 'useDatabase',
    message: 'Use database?',
    default: true
  },
  {
    type: 'list',
    name: 'dbType',
    message: 'Database type:',
    choices: ['PostgreSQL', 'MySQL', 'MongoDB', 'SQLite'],
    when: (answers) => answers.useDatabase
  },
  {
    type: 'input',
    name: 'dbHost',
    message: 'Database host:',
    default: 'localhost',
    when: (answers) => answers.useDatabase && answers.dbType !== 'SQLite'
  }
];
```

```python
# Python - See examples/python/conditional_flow.py
use_database = questionary.confirm("Use database?", default=True).ask()

if use_database:
    db_type = questionary.select(
        "Database type:",
        choices=['PostgreSQL', 'MySQL', 'MongoDB', 'SQLite']
    ).ask()

    if db_type != 'SQLite':
        db_host = questionary.text(
            "Database host:",
            default="localhost"
        ).ask()
```

### Example 3: Password with Confirmation

**Use case**: Secure password input with validation and confirmation

```javascript
// Node.js - See examples/nodejs/password-confirm.js
const answers = await inquirer.prompt([
  {
    type: 'password',
    name: 'password',
    message: 'Enter password:',
    validate: (input) => input.length >= 8 || 'Password must be 8+ characters'
  },
  {
    type: 'password',
    name: 'confirmPassword',
    message: 'Confirm password:',
    validate: (input, answers) => {
      return input === answers.password || 'Passwords do not match';
    }
  }
]);
```

```python
# Python - See examples/python/password_confirm.py
password = questionary.password(
    "Enter password:",
    validate=lambda t: len(t) >= 8 or "Password must be 8+ characters"
).ask()

confirm = questionary.password(
    "Confirm password:",
    validate=lambda t: t == password or "Passwords do not match"
).ask()
```

## Scripts

### Install Dependencies

**Node.js**:
```bash
./scripts/install-nodejs-deps.sh
# Installs: inquirer, inquirer-autocomplete-prompt
```

**Python**:
```bash
./scripts/install-python-deps.sh
# Installs: questionary, prompt_toolkit
```

### Validate Prompts

```bash
./scripts/validate-prompts.sh [nodejs|python]
# Tests all templates and examples
```

### Generate Prompt Code

```bash
./scripts/generate-prompt.sh --type [text|list|checkbox|password] --lang [js|py]
# Generates boilerplate prompt code
```

## Best Practices

1. **Always validate user input** - Prevent invalid data early
2. **Provide clear messages** - Use descriptive prompt text
3. **Set sensible defaults** - Reduce friction for common cases
4. **Use conditional logic** - Skip irrelevant questions
5. **Group related questions** - Keep context together
6. **Handle Ctrl+C gracefully** - Catch interrupts and exit cleanly
7. **Test interactively** - Run examples to verify UX
8. **Provide help text** - Add descriptions for complex prompts

## Common Patterns

### CLI Configuration Generator
```javascript
const config = await inquirer.prompt([
  { type: 'input', name: 'appName', message: 'App name:' },
  { type: 'input', name: 'version', message: 'Version:', default: '1.0.0' },
  { type: 'list', name: 'env', message: 'Environment:', choices: ['dev', 'prod'] },
  { type: 'confirm', name: 'debug', message: 'Enable debug?', default: false }
]);
```

### Multi-Step Installation Wizard
```python
# Step 1: Choose components
components = questionary.checkbox(
    "Select components:",
    choices=['Core', 'CLI', 'Web UI', 'API']
).ask()

# Step 2: Configure each component
for component in components:
    print(f"\nConfiguring {component}...")
    # Component-specific questions
```

### Error Recovery
```javascript
try {
  const answers = await inquirer.prompt(questions);
  // Process answers
} catch (error) {
  if (error.isTtyError) {
    console.error('Prompt could not be rendered in this environment');
  } else {
    console.error('User interrupted prompt');
  }
  process.exit(1);
}
```

## Requirements

- **Node.js**: v14+ with ESM support
- **Python**: 3.7+ with pip
- **Dependencies**:
  - Node.js: `inquirer@^9.0.0`, `inquirer-autocomplete-prompt@^3.0.0`
  - Python: `questionary@^2.0.0`, `prompt_toolkit@^3.0.0`

## Troubleshooting

### Node.js Issues

**Problem**: `Error [ERR_REQUIRE_ESM]`
**Solution**: Use `import` instead of `require`, or add `"type": "module"` to package.json

**Problem**: Autocomplete not working
**Solution**: Install `inquirer-autocomplete-prompt` plugin

### Python Issues

**Problem**: No module named 'questionary'
**Solution**: Run `pip install questionary`

**Problem**: Prompt rendering issues
**Solution**: Ensure terminal supports ANSI escape codes

---

**Purpose**: Provide reusable interactive prompt patterns for CLI development
**Load when**: Building CLIs with user input, creating interactive questionnaires, implementing wizards
