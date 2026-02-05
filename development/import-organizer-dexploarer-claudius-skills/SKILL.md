---
name: import-organizer
description: Organizes and sorts import statements in code files. Use when imports are messy or need organization.
allowed-tools: [Read, Edit, Grep]
---

# Import Organizer

Automatically organize and sort import statements in JavaScript, TypeScript, Python, and other languages.

## When to Activate

- "organize imports in this file"
- "sort the imports"
- "clean up import statements"
- "fix import order"

## Process

1. **Read the file** to see current imports
2. **Identify import groups**:
   - External/third-party imports
   - Internal/local imports
   - Type imports (TypeScript)
   - Side-effect imports
3. **Sort within groups** alphabetically
4. **Remove duplicates** if any
5. **Apply language-specific conventions**:
   - JavaScript/TypeScript: External, then internal
   - Python: Standard library, third-party, local
6. **Preserve comments** attached to imports
7. **Update the file** with organized imports

## Language-Specific Rules

### JavaScript/TypeScript
```javascript
// External packages first
import React from 'react'
import { useState } from 'react'
import axios from 'axios'

// Internal imports
import { Button } from './components/Button'
import { utils } from './utils'

// Type imports (TypeScript)
import type { User } from './types'

// Side-effect imports last
import './styles.css'
```

### Python
```python
# Standard library
import os
import sys
from datetime import datetime

# Third-party
import requests
from django.db import models

# Local
from .models import User
from .utils import helper
```

## Best Practices

- Group by source (external vs internal)
- Sort alphabetically within groups
- Separate groups with blank lines
- Remove unused imports (warn user)
- Preserve special comments
- Follow language conventions
