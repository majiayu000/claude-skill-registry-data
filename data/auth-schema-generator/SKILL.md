---
name: auth-schema-generator
description: Generate Better Auth user schema configuration with custom additional fields for user profiles. Use when implementing authentication, user profiles, or extending user data models with Better Auth. Automatically generates TypeScript types and database schema.
allowed-tools: write_to_file, view_file, replace_file_content
---

# Auth Schema Generator

Generate Better Auth user schema configurations with custom additional fields for authentication systems.

## When to Use

Use this skill when:

- Implementing Better Auth in a new project
- Adding custom user profile fields (background info, preferences, settings)
- Extending user data model with questionnaire responses
- Setting up authentication with personalized user data

## Instructions

### Step 1: Identify Required Fields

Determine what additional user data you need:

- User preferences (theme, language, notifications)
- Profile information (job title, department, bio)
- Background data (experience levels, skills, interests)
- System metadata (onboarding status, last login)

### Step 2: Generate Schema Configuration

Create Better Auth configuration in `src/lib/auth.ts`:

```typescript
export const auth = betterAuth({
  database: pool,
  emailAndPassword: {
    enabled: true,
  },
  user: {
    additionalFields: {
      // Generated fields based on requirements
      fieldName: {
        type: "string",
        required: true,
        defaultValue: "default",
      },
    },
  },
});
```

### Step 3: Generate TypeScript Types

Export inferred types for type safety:

```typescript
export type Session = typeof auth.$Infer.Session;
export type User = typeof auth.$Infer.User;
```

### Step 4: Create Interface Definitions

Generate TypeScript interfaces for use in components:

```typescript
interface UserProfile {
  [fieldName]: string;
  // Additional fields...
}
```

## Example: Background Questionnaire

For a learning platform with user background profiling:

**Input**: Need to track software experience, AI/ML familiarity, hardware knowledge, learning goals

**Generated Schema**:

```typescript
user: {
  additionalFields: {
    softwareExperience: {
      type: "string",
      required: true,
      defaultValue: "beginner"
    },
    aiMlFamiliarity: {
      type: "string",
      required: true,
      defaultValue: "none"
    },
    hardwareExperience: {
      type: "string",
      required: true,
      defaultValue: "none"
    },
    learningGoals: {
      type: "string",
      required: true,
      defaultValue: "hobby"
    },
    programmingLanguages: {
      type: "string",
      required: false,
      defaultValue: ""
    }
  }
}
```

**Generated Interface**:

```typescript
interface BackgroundProfile {
  softwareExperience: string;
  aiMlFamiliarity: string;
  hardwareExperience: string;
  learningGoals: string;
  programmingLanguages?: string;
}
```

## Field Types Supported

- `string`: Text fields
- `number`: Numeric values
- `boolean`: True/false flags
- `date`: Timestamps

## Best Practices

1. **Use Descriptive Names**: `softwareExperience` not `exp`
2. **Set Sensible Defaults**: Provide default values for required fields
3. **Mark Optional Fields**: Use `required: false` for optional data
4. **Type Safety**: Always export TypeScript types
5. **Validation**: Validate field values in your forms before submission

## Files Modified

This skill typically modifies:

- `src/lib/auth.ts` - Better Auth configuration
- `src/types/auth.ts` - TypeScript type definitions (if separate file)
- `src/hooks/useAuth.ts` - Custom auth hook to use typed data

## Security Considerations

- Never store sensitive data in additional fields (use separate encrypted storage)
- Validate all user input before saving to database
- Use appropriate field types for the data being stored
- Consider GDPR/privacy implications for profile data
