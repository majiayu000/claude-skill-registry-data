---
name: language-conventions
description: Defines language usage conventions separating user communication from technical artifacts. Use when writing code, documentation, commits, or communicating with users in multilingual projects.
---

# Language Conventions

<!-- CUSTOMIZE: Set project language preferences -->
<!-- Common patterns:
  - User Language: Korean, Japanese, Chinese, Spanish, etc.
  - Code Language: Always English (international standard)
  - Replace {{USER_LANG}} with your project's user communication language
-->

## Instructions

### Core rule

**{{USER_LANG}}:** User communication, documentation, commits
**English:** Code, comments, technical identifiers

### Quick reference

| Artifact | Language | Why |
|----------|----------|-----|
| User messages | {{USER_LANG}} | User's language |
| Code | English | International standard |
| Comments | English | Matches code |
| Variables/Functions | English | Part of code |
| Commits | {{USER_LANG}} | Team communication |
| Documentation | {{USER_LANG}} | User's language |
| Tags | English | Technical ID |

<!-- CUSTOMIZE: If your project uses English for all communication, simplify to single-language policy -->

## Example

<!-- Example uses Korean as {{USER_LANG}} - replace with your language -->

```{{LANG}}
# User: {{USER_LANG}}
"{{User message in local language}}"

# Code: English
# @FEAT:{{feature-name}} @COMP:service @TYPE:core
class {{EntityName}}ValidationService:
    '''Validates {{entities}} before submission'''

    def validate(self, {{entity}}: dict) -> bool:
        # Validate {{field}} is positive
        if {{entity}}.get('{{field}}', 0) <= 0:
            return False
        return True

# User: {{USER_LANG}}
"{{Completion message in local language}}"
```

## Common mistakes

```{{LANG}}
# ❌ {{USER_LANG}} in code
def {{local_language_function_name}}({{local_language_param}}): pass

# ❌ English to user
"Implementation complete."

# ✅ Correct
"{{Completion message in user language}}"
def {{english_function_name}}({{english_param}}): pass
```

## Multi-Language Examples

### Python
```python
# User communication: {{USER_LANG}}
# Code: English

# @FEAT:user-auth @COMP:service @TYPE:core
class AuthenticationService:
    '''Handles user authentication'''

    def authenticate(self, username: str, password: str) -> bool:
        # Validate credentials
        if not username or not password:
            return False
        return True
```

### JavaScript/TypeScript
```javascript
// User communication: {{USER_LANG}}
// Code: English

// @FEAT:user-auth @COMP:service @TYPE:core
class AuthenticationService {
    /**
     * Handles user authentication
     */
    authenticate(username, password) {
        // Validate credentials
        if (!username || !password) {
            return false;
        }
        return true;
    }
}
```

### Go
```go
// User communication: {{USER_LANG}}
// Code: English

// @FEAT:user-auth @COMP:service @TYPE:core
// AuthenticationService handles user authentication
type AuthenticationService struct{}

// Authenticate validates user credentials
func (s *AuthenticationService) Authenticate(username, password string) bool {
    // Validate credentials
    if username == "" || password == "" {
        return false
    }
    return true
}
```

## Language-Agnostic Alternative

**If your project uses English for all communication:**

```markdown
### Simplified Single-Language Policy

**English everywhere:** User communication, code, documentation, commits

| Artifact | Language |
|----------|----------|
| User messages | English |
| Code | English |
| Comments | English |
| Variables/Functions | English |
| Commits | English |
| Documentation | English |
| Tags | English |

**Consistency:** Use clear, professional English throughout all artifacts.
```

---

**For detailed guidelines, see [reference.md](reference.md)**
**For more examples, see [examples.md](examples.md)**
