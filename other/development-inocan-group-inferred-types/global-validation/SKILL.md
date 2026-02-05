---
name: Global Validation
description: Implement comprehensive validation using Zod schemas for type-safe validation on both client and server, with server-side validation as the security boundary (never trust client input). Use this skill when validating user inputs, creating API endpoints that accept data, implementing forms, defining data schemas, validating file uploads, creating validation middleware, implementing Firestore security rules or Supabase RLS, or writing validation rules for any user-provided data. Apply when working on API route handlers, form components with React Hook Form, validation middleware, Zod schema definitions (schemas/*.ts, validation/*.ts), Firestore security rules (firestore.rules), Supabase RLS policies, or any code that accepts external input. This skill ensures server-side validation always (client-side is for UX only), Zod for schema validation with TypeScript type inference (z.infer<typeof schema>), validation middleware factory for Express/Bun APIs, React Hook Form + zodResolver for forms, user-friendly error messages (not technical jargon), input sanitization with DOMPurify for HTML content, file upload validation (type whitelist, size limits with multer), Firestore security rules with data type and length validation, FluentValidation for .NET APIs, database-level constraints enforcement, fail-early validation principles, and environment variable validation with Zod on application startup.
---

# Global Validation

## When to use this skill:

- When creating API endpoints that accept request bodies
- When implementing validation middleware factory for Express/Bun/Hono
- When defining Zod schemas for data validation with type inference
- When creating forms with React Hook Form and zodResolver
- When validating file uploads (MIME type whitelist, size limits with multer)
- When writing Firestore security rules (firestore.rules) for database validation
- When writing Supabase Row Level Security (RLS) policies
- When implementing input sanitization with DOMPurify to prevent XSS
- When adding validation to service layer methods (fail-early)
- When creating custom Zod refinements (e.g., password complexity) or transforms (e.g., string to Date)
- When writing user-friendly validation error messages (not technical jargon)
- When validating environment variables with Zod on application startup
- When working on any code that accepts user input or external data
- When implementing FluentValidation for .NET API validation
- When creating complex nested schemas with arrays and optional fields

This Skill provides Claude Code with specific guidance on how to adhere to coding standards as they relate to how it should handle global validation.

## Instructions

For details, refer to the information provided in this file:
[global validation](../../../agent-os/standards/global/validation.md)
