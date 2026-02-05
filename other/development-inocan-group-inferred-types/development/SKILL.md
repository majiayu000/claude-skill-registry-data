---
name: development
description: Guidance and code snippets for software development using common languages and frameworks. Use this skill to setup projects, write clean and maintainable code, manage dependencies, and debug effectively.
license: MIT
allowed-tools:
  - python
  - bash
metadata:
  category: engineering
---
# Software Development Guide

## Overview

This skill provides best practices, code snippets, and workflows for modern software development. Use it whenever you need help writing or organizing code, setting up environments, or debugging.

### Key Principles

- **Modular design**: Break functionality into small, reusable modules. Use descriptive function and variable names.
- **Version control**: Use Git to track changes. Commit early and often with meaningful messages.
- **Documentation**: Write docstrings and comments. Include a README.md in your projects.

## Python Development

### Setting up a project

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Format code with black and check style
pip install black isort flake8
black src/
isort src/
flake8 src/
```

### Creating a CLI application

```python
import argparse


def main():
    parser = argparse.ArgumentParser(description="Example CLI")
    parser.add_argument("input_file", help="Path to input file")
    args = parser.parse_args()

    with open(args.input_file) as f:
        content = f.read()
    print(content)


if __name__ == "__main__":
    main()
```

### Debugging with pdb

```python
import pdb


def divide(a, b):
    pdb.set_trace()
    return a / b
```

Run your script with `python -m pdb script.py` to step through execution.

## JavaScript/Node.js Development

### Initializing a project

```bash
npm init -y
npm install express
```

### Creating an Express server

```javascript
const express = require('express');
const app = express();
const port = 3000;

app.get('/', (req, res) => {
  res.send('Hello World!');
});

app.listen(port, () => {
  console.log(`Server listening on port ${port}`);
});
```

### Debugging

Use `node --inspect-brk` to debug your code with Chrome DevTools. Add breakpoints or use `debugger;` statements in your script.

## Best Practices

- Write unit tests before implementing features (see the `testing` skill).
- Structure code into packages and modules.
- Use continuous integration (CI) to automatically run tests and linters.
- Document important APIs in a docs folder or inline with docstrings.

## Additional Resources

- Python Packaging Authority’s packaging guide.
- Node.js documentation.
- Atlassian Git tutorials.
