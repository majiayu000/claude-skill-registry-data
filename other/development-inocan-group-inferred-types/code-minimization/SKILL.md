---
name: code-minimization
description: Write minimum necessary code following YAGNI principle to prevent bloat and over-engineering. Use when implementing features to keep the codebase lean and avoid premature optimization or speculative features.
---

# Code Minimization

## Instructions

### Write minimum code

Implement what's needed NOW, not what MIGHT be needed.

**Avoid:**
- Premature optimization
- Speculative features
- Over-abstraction
- Unnecessary complexity

### YAGNI principle

**You Aren't Gonna Need It**

## Example

<!-- CUSTOMIZE: Replace with {{MAIN_TECH_STACK}}-appropriate examples -->

### Python Example
```python
# ❌ Over-engineered
class ValidatorFactory:
    def create(self, type):
        if type == 'basic': return BasicValidator()
        elif type == 'advanced': return AdvancedValidator()
        # 10 more types... (only use BasicValidator!)

# ✅ Minimal
class EntityValidator:
    def validate(self, entity):
        return entity.required_field is not None
```

### JavaScript/Node.js Example
```javascript
// ❌ Over-engineered
class ValidatorFactory {
    create(type) {
        if (type === 'basic') return new BasicValidator();
        else if (type === 'advanced') return new AdvancedValidator();
        // 10 more types... (only use BasicValidator!)
    }
}

// ✅ Minimal
class EntityValidator {
    validate(entity) {
        return entity.requiredField !== null && entity.requiredField !== undefined;
    }
}
```

### Go Example
```go
// ❌ Over-engineered
type ValidatorFactory struct{}

func (f *ValidatorFactory) Create(validatorType string) Validator {
    switch validatorType {
    case "basic":
        return &BasicValidator{}
    case "advanced":
        return &AdvancedValidator{}
    // 10 more types... (only use BasicValidator!)
    }
    return nil
}

// ✅ Minimal
type EntityValidator struct{}

func (v *EntityValidator) Validate(entity *Entity) bool {
    return entity.RequiredField != ""
}
```

## Guidelines

**Do:** Solve current requirements simply
**Don't:** Add "maybe later" features

---

**For detailed patterns, see [reference.md](reference.md)**
**For more examples, see [examples.md](examples.md)**
