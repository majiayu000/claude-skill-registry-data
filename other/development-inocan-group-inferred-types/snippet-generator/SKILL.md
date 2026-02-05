---
name: Snippet Generator
description: Generate reusable, customizable code snippets for common programming patterns and boilerplate code across multiple languages
---

# Snippet Generator

## Purpose

Create production-ready code snippets that:
- Follow language best practices
- Are properly documented
- Include error handling
- Are customizable with parameters
- Save development time

## When to Use

Invoke this skill when:
- User needs boilerplate code quickly
- Creating common patterns (loops, classes, functions)
- Scaffolding new components or modules
- Teaching programming patterns
- Standardizing code across a team

## Instructions

### Step 1: Identify the Snippet Type

Determine what kind of snippet is needed:
1. **Language construct**: Class, function, loop, conditional
2. **Design pattern**: Singleton, factory, observer, etc.
3. **Framework-specific**: React component, Express route, etc.
4. **Utility**: Common algorithm, data structure, helper
5. **Test pattern**: Test suite, test case, mock

### Step 2: Determine the Language/Framework

Identify the target environment:
- **Language**: JavaScript, TypeScript, Python, Go, Rust, Java, etc.
- **Framework**: React, Vue, Express, Django, Spring, etc.
- **Version**: ES6+, TypeScript 5+, Python 3.10+, etc.

### Step 3: Apply Best Practices

Ensure the snippet includes:
1. **Type safety**: Types/interfaces where applicable
2. **Error handling**: Try/catch, error checking
3. **Documentation**: JSDoc, docstrings, comments
4. **Naming**: Clear, descriptive names
5. **Modern syntax**: Latest language features
6. **Testing**: Testable structure

### Step 4: Add Customization Placeholders

Include placeholders for:
- Names: `${ComponentName}`, `${functionName}`
- Parameters: `${param1}`, `${options}`
- Types: `${Type}`, `${ReturnType}`
- Values: `${defaultValue}`, `${initialState}`

### Step 5: Include Usage Examples

Provide:
- Basic usage example
- Advanced usage (if applicable)
- Common variations
- Integration examples

## Snippet Templates

### JavaScript/TypeScript

#### Async Function with Error Handling

```typescript
/**
 * ${description}
 * @param ${param} - ${paramDescription}
 * @returns ${returnDescription}
 * @throws ${errorDescription}
 */
async function ${functionName}(${param}: ${ParamType}): Promise<${ReturnType}> {
  try {
    // Validate input
    if (!${param}) {
      throw new Error('${param} is required');
    }

    // Main logic
    const result = await ${operation}(${param});

    return result;
  } catch (error) {
    console.error(`Error in ${functionName}:`, error);
    throw new Error(`Failed to ${operation}: ${error.message}`);
  }
}

// Usage example
try {
  const result = await ${functionName}(${exampleParam});
  console.log('Success:', result);
} catch (error) {
  console.error('Error:', error);
}
```

#### React Component (Functional)

```typescript
import { useState, useEffect } from 'react';

interface ${ComponentName}Props {
  ${prop1}: ${Prop1Type};
  ${prop2}?: ${Prop2Type};
  on${Event}?: (${eventParam}: ${EventType}) => void;
}

/**
 * ${componentDescription}
 */
export const ${ComponentName}: React.FC<${ComponentName}Props> = ({
  ${prop1},
  ${prop2} = ${defaultValue},
  on${Event}
}) => {
  const [${state}, set${State}] = useState<${StateType}>(${initialState});

  useEffect(() => {
    // Setup
    ${setupCode}

    // Cleanup
    return () => {
      ${cleanupCode}
    };
  }, [${dependencies}]);

  const handle${Action} = (${param}: ${ParamType}) => {
    set${State}(${newState});
    on${Event}?.(${eventData});
  };

  return (
    <div className="${component-name}">
      {${state} && (
        <div>
          {/* Component content */}
          {${prop1}}
        </div>
      )}
    </div>
  );
};

// Usage example
<${ComponentName}
  ${prop1}={${value1}}
  on${Event}={(data) => console.log(data)}
/>
```

#### Express Route Handler

```typescript
import { Request, Response, NextFunction } from 'express';
import { ${Service} } from '../services/${service}';
import { validate${Schema} } from '../validators';
import { ${ErrorType} } from '../errors';

/**
 * ${routeDescription}
 * @route ${METHOD} ${path}
 * @access ${public|private}
 */
export const ${handlerName} = async (
  req: Request,
  res: Response,
  next: NextFunction
): Promise<void> => {
  try {
    // Validate request
    const validated = validate${Schema}(req.body);

    // Service call
    const result = await ${Service}.${method}(validated);

    // Success response
    res.status(${statusCode}).json({
      success: true,
      data: result,
      message: '${successMessage}'
    });
  } catch (error) {
    // Error handling
    if (error instanceof ${ErrorType}) {
      res.status(${errorStatus}).json({
        success: false,
        error: error.message
      });
    } else {
      next(error);
    }
  }
};

// Route registration
router.${method}('${path}', ${authMiddleware}, ${handlerName});
```

---

### Python

#### Class with Dataclass

```python
from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime

@dataclass
class ${ClassName}:
    """
    ${classDescription}

    Attributes:
        ${attr1}: ${attr1Description}
        ${attr2}: ${attr2Description}
    """
    ${attr1}: ${Type1}
    ${attr2}: ${Type2} = ${defaultValue}
    ${attr3}: Optional[${Type3}] = None
    created_at: datetime = field(default_factory=datetime.now)

    def ${method_name}(self, ${param}: ${ParamType}) -> ${ReturnType}:
        """
        ${methodDescription}

        Args:
            ${param}: ${paramDescription}

        Returns:
            ${returnDescription}

        Raises:
            ${Exception}: ${exceptionDescription}
        """
        if not ${param}:
            raise ValueError(f"${param} cannot be empty")

        # Method logic
        result = ${operation}
        return result

    def __str__(self) -> str:
        return f"${ClassName}(${attr1}={self.${attr1}})"

# Usage example
obj = ${ClassName}(
    ${attr1}=${value1},
    ${attr2}=${value2}
)
result = obj.${method_name}(${argument})
```

#### Async Function with Context Manager

```python
import asyncio
from contextlib import asynccontextmanager
from typing import AsyncGenerator

@asynccontextmanager
async def ${context_manager_name}(${param}: ${ParamType}) -> AsyncGenerator[${YieldType}, None]:
    """
    ${description}

    Args:
        ${param}: ${paramDescription}

    Yields:
        ${yieldDescription}

    Example:
        async with ${context_manager_name}(${exampleParam}) as ${resource}:
            await ${resource}.${operation}()
    """
    # Setup
    ${resource} = await ${setup_operation}(${param})

    try:
        yield ${resource}
    finally:
        # Cleanup
        await ${resource}.${cleanup_method}()

# Usage
async def main():
    async with ${context_manager_name}(${param}) as ${resource}:
        result = await ${resource}.${operation}()
        return result
```

---

### Go

#### Struct with Methods

```go
package ${packageName}

import (
    "context"
    "fmt"
    "time"
)

// ${StructName} represents ${description}
type ${StructName} struct {
    ${field1} ${Type1}
    ${field2} ${Type2}
    ${field3} *${Type3}
}

// New${StructName} creates a new ${StructName} instance
func New${StructName}(${param1} ${Type1}, ${param2} ${Type2}) *${StructName} {
    return &${StructName}{
        ${field1}: ${param1},
        ${field2}: ${param2},
        ${field3}: ${defaultValue},
    }
}

// ${MethodName} ${methodDescription}
func (s *${StructName}) ${MethodName}(ctx context.Context, ${param} ${ParamType}) (${ReturnType}, error) {
    // Validation
    if ${param} == ${zeroValue} {
        return ${zeroReturn}, fmt.Errorf("${param} cannot be ${zeroValue}")
    }

    // Main logic
    result, err := s.${operation}(ctx, ${param})
    if err != nil {
        return ${zeroReturn}, fmt.Errorf("failed to ${operation}: %w", err)
    }

    return result, nil
}

// Usage example
func main() {
    obj := New${StructName}(${value1}, ${value2})

    ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
    defer cancel()

    result, err := obj.${MethodName}(ctx, ${argument})
    if err != nil {
        log.Fatalf("Error: %v", err)
    }

    fmt.Printf("Result: %v\n", result)
}
```

---

### Rust

#### Struct with Trait Implementation

```rust
use std::fmt;
use std::error::Error;

/// ${structDescription}
#[derive(Debug, Clone)]
pub struct ${StructName} {
    ${field1}: ${Type1},
    ${field2}: ${Type2},
    ${field3}: Option<${Type3}>,
}

impl ${StructName} {
    /// Creates a new ${StructName}
    pub fn new(${param1}: ${Type1}, ${param2}: ${Type2}) -> Self {
        Self {
            ${field1}: ${param1},
            ${field2}: ${param2},
            ${field3}: None,
        }
    }

    /// ${methodDescription}
    pub fn ${method_name}(&self, ${param}: ${ParamType}) -> Result<${ReturnType}, Box<dyn Error>> {
        // Validation
        if ${param}.is_empty() {
            return Err("${param} cannot be empty".into());
        }

        // Main logic
        let result = ${operation}(${param})?;

        Ok(result)
    }
}

impl fmt::Display for ${StructName} {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "${StructName} {{ ${field1}: {}, ${field2}: {} }}",
               self.${field1}, self.${field2})
    }
}

// Usage example
fn main() -> Result<(), Box<dyn Error>> {
    let obj = ${StructName}::new(${value1}, ${value2});
    let result = obj.${method_name}(${argument})?;
    println!("Result: {:?}", result);
    Ok(())
}
```

## Common Patterns

### Factory Pattern

```typescript
interface ${Product} {
  ${method}(): void;
}

class ${ConcreteProductA} implements ${Product} {
  ${method}(): void {
    console.log('${ConcreteProductA}.${method}');
  }
}

class ${ConcreteProductB} implements ${Product} {
  ${method}(): void {
    console.log('${ConcreteProductB}.${method}');
  }
}

class ${Factory} {
  static create(type: '${typeA}' | '${typeB}'): ${Product} {
    switch (type) {
      case '${typeA}':
        return new ${ConcreteProductA}();
      case '${typeB}':
        return new ${ConcreteProductB}();
      default:
        throw new Error(`Unknown type: ${type}`);
    }
  }
}

// Usage
const product = ${Factory}.create('${typeA}');
product.${method}();
```

### Observer Pattern

```typescript
interface ${Observer} {
  update(data: ${DataType}): void;
}

class ${Subject} {
  private observers: ${Observer}[] = [];

  subscribe(observer: ${Observer}): void {
    this.observers.push(observer);
  }

  unsubscribe(observer: ${Observer}): void {
    this.observers = this.observers.filter(obs => obs !== observer);
  }

  notify(data: ${DataType}): void {
    this.observers.forEach(observer => observer.update(data));
  }
}

class ${ConcreteObserver} implements ${Observer} {
  update(data: ${DataType}): void {
    console.log('Received update:', data);
  }
}

// Usage
const subject = new ${Subject}();
const observer = new ${ConcreteObserver}();
subject.subscribe(observer);
subject.notify(${data});
```

## Best Practices

1. **Documentation**: Always include docstrings/JSDoc
2. **Error Handling**: Never ignore errors
3. **Type Safety**: Use types where available
4. **Validation**: Validate inputs
5. **Naming**: Use clear, descriptive names
6. **Modularity**: Keep functions small and focused
7. **Testing**: Make code testable
8. **Consistency**: Follow language conventions

## Output Format

When generating a snippet:

```
## ${SnippetName}

**Purpose**: ${purpose}

**Language**: ${language}

**Code**:
```${language}
${snippetCode}
```

**Usage**:
```${language}
${usageExample}
```

**Parameters**:
- `${param1}`: ${description}
- `${param2}`: ${description}

**Notes**:
- ${note1}
- ${note2}
```

## Related Skills

- `code-template-library`: For managing snippet collections
- `boilerplate-generator`: For project scaffolding
- `refactoring-patterns`: For improving existing code
- `test-generator`: For creating test snippets
