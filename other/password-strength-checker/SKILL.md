---
name: password-strength-checker
description: Check password strength and complexity
activation_keywords: [password, strength, complexity, security, secure password]
execution_mode: server
---

# Password Strength Checker

Checks password strength and provides security recommendations:
- Password length check (minimum 8 characters)
- Uppercase and lowercase letter check
- Number check
- Special character check
- Common password detection
- Entropy calculation

Use `builtin_password_strength_checker` tool with fields:
- `password`: the password to check (required)
- `min_length`: (optional) minimum length requirement (default: 8)

Returns strength score (0-100) and improvement recommendations.
