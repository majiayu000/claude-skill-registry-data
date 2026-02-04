---
name: form-validator-generator
description: Generate comprehensive form validation logic for React forms with TypeScript. Use when creating signup/login forms, input validation, or user data collection. Includes email regex, password strength, required fields, and error handling.
allowed-tools: write_to_file, view_file, replace_file_content
---

# Form Validator Generator

Generate TypeScript validation logic for React forms with comprehensive error handling.

## When to Use

Use this skill when:

- Creating signup or signin forms
- Building forms with multiple fields
- Need client-side validation before submission
- Implementing user input validation
- Creating questionnaires or surveys

## Instructions

### Step 1: Identify Form Fields

Determine which fields need validation:

- Email addresses
- Passwords (with strength requirements)
- Names (trim whitespace)
- Phone numbers
- Dropdowns/selects (required selections)
- Text areas
- Custom fields

### Step 2: Generate Validation Function

Create a TypeScript validation function:

```typescript
const validateForm = (): boolean => {
  const errors: Record<string, string> = {};

  // Add validation logic for each field

  setValidationErrors(errors);
  return Object.keys(errors).length === 0;
};
```

### Step 3: Implement Field-Specific Validation

Add rules for each field type:

**Email Validation**:

```typescript
if (!formData.email.trim()) {
  errors.email = "Email is required";
} else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
  errors.email = "Please enter a valid email address";
}
```

**Password Validation**:

```typescript
if (!formData.password) {
  errors.password = "Password is required";
} else if (formData.password.length < 8) {
  errors.password = "Password must be at least 8 characters";
}
```

**Password Confirmation**:

```typescript
if (formData.password !== formData.confirmPassword) {
  errors.confirmPassword = "Passwords do not match";
}
```

**Required Field**:

```typescript
if (!formData.name.trim()) {
  errors.name = "Name is required";
}
```

**Required Select**:

```typescript
if (!formData.softwareExperience) {
  errors.softwareExperience = "Please select your experience level";
}
```

### Step 4: Add Real-time Validation

Clear errors as user types:

```typescript
const handleChange = (field: string, value: string) => {
  setFormData((prev) => ({ ...prev, [field]: value }));

  // Clear validation error for this field
  if (validationErrors[field]) {
    setValidationErrors((prev) => {
      const newErrors = { ...prev };
      delete newErrors[field];
      return newErrors;
    });
  }
};
```

### Step 5: Display Validation Errors

Show errors in UI:

```typescript
<input
  type="email"
  value={formData.email}
  onChange={(e) => handleChange("email", e.target.value)}
  className={validationErrors.email ? styles.error : ""}
/>;
{
  validationErrors.email && (
    <span className={styles.errorMessage}>{validationErrors.email}</span>
  );
}
```

## Complete Example: Signup Form Validation

```typescript
import { useState } from "react";

interface SignupFormData {
  name: string;
  email: string;
  password: string;
  confirmPassword: string;
  softwareExperience: string;
  aiMlFamiliarity: string;
}

export default function SignupForm() {
  const [formData, setFormData] = useState<SignupFormData>({
    name: "",
    email: "",
    password: "",
    confirmPassword: "",
    softwareExperience: "",
    aiMlFamiliarity: "",
  });

  const [validationErrors, setValidationErrors] = useState<
    Record<string, string>
  >({});

  const validateForm = (): boolean => {
    const errors: Record<string, string> = {};

    // Name validation
    if (!formData.name.trim()) {
      errors.name = "Name is required";
    }

    // Email validation
    if (!formData.email.trim()) {
      errors.email = "Email is required";
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
      errors.email = "Please enter a valid email address";
    }

    // Password validation
    if (!formData.password) {
      errors.password = "Password is required";
    } else if (formData.password.length < 8) {
      errors.password = "Password must be at least 8 characters";
    }

    // Password confirmation
    if (formData.password !== formData.confirmPassword) {
      errors.confirmPassword = "Passwords do not match";
    }

    // Required select fields
    if (!formData.softwareExperience) {
      errors.softwareExperience = "Please select your experience level";
    }

    if (!formData.aiMlFamiliarity) {
      errors.aiMlFamiliarity = "Please select your AI/ML familiarity";
    }

    setValidationErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!validateForm()) {
      return;
    }

    // Proceed with form submission
  };

  return <form onSubmit={handleSubmit}>{/* Form fields */}</form>;
}
```

## Validation Rules Library

### Email Patterns

```typescript
// Basic email
/^[^\s@]+@[^\s@]+\.[^\s@]+$/

// Strict email (RFC 5322)
/^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/
```

### Password Strength

```typescript
// At least 8 characters
password.length >= 8

// Contains uppercase
/[A-Z]/.test(password)

// Contains number
/\d/.test(password)

// Contains special character
/[!@#$%^&*(),.?":{}|<>]/.test(password)
```

### Phone Numbers

```typescript
// US phone number
/^\(?([0-9]{3})\)?[-. ]?([0-9]{3})[-. ]?([0-9]{4})$/

// International format
/^\+?[1-9]\d{1,14}$/
```

### URLs

```typescript
// Basic URL
/^https?:\/\/.+/

// Strict URL
/^https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)$/
```

## Error Message Best Practices

1. **Be Specific**: "Email is required" not "Invalid input"
2. **Be Helpful**: "Password must be at least 8 characters" not "Bad password"
3. **Be Consistent**: Use same tone/style across all messages
4. **Be Positive**: "Please enter your email" not "You forgot email"

## TypeScript Types

```typescript
// Validation errors
type ValidationErrors = Record<string, string>;

// Form data
interface FormData {
  [key: string]: string | number | boolean;
}

// Validation rules
type ValidationRule = (value: any) => string | null;

// Field config
interface FieldConfig {
  required?: boolean;
  pattern?: RegExp;
  minLength?: number;
  maxLength?: number;
  custom?: ValidationRule;
}
```

## Accessibility Considerations

- Link error messages to inputs with `aria-describedby`
- Use `aria-invalid` on fields with errors
- Ensure error messages are screen-reader friendly
- Don't rely solely on color to indicate errors

```tsx
<input
  type="email"
  id="email"
  aria-invalid={!!validationErrors.email}
  aria-describedby={validationErrors.email ? "email-error" : undefined}
/>;
{
  validationErrors.email && (
    <span id="email-error" role="alert">
      {validationErrors.email}
    </span>
  );
}
```
