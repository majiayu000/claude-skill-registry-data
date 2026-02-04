---
name: Global Validation
description: Implement comprehensive input validation on server-side with complementary client-side validation for user experience, using allowlists, type checking, and sanitization to prevent injection attacks. Use this skill when validating user inputs, form data, API requests, file uploads, query parameters, or any external data entering the application. Apply this skill when implementing server-side validation as the primary security layer, adding client-side validation for immediate user feedback, validating data types and formats, checking ranges and required fields, sanitizing inputs to prevent SQL injection and XSS attacks, using allowlists over blocklists, providing field-specific error messages, or enforcing business rules at appropriate application layers. This skill ensures validation happens at all entry points consistently, security is never dependent on client-side checks alone, users receive helpful immediate feedback, and data integrity is maintained through multiple layers of validation.
---

# Global Validation

This Skill provides Claude Code with specific guidance on how to adhere to coding standards as they relate to how it should handle global validation.

## When to use this skill

- When implementing server-side validation for API endpoints, forms, or data processing
- When adding client-side validation for immediate user feedback (but always duplicating server-side)
- When validating user inputs in forms, search fields, or text inputs
- When processing API request payloads, query parameters, or file uploads
- When sanitizing inputs to prevent SQL injection, XSS, or command injection attacks
- When validating data types, formats (email, phone, date), required fields, and ranges
- When providing specific, helpful error messages for each validation failure
- When using allowlists (defining what's allowed) rather than blocklists (blocking bad patterns)
- When implementing business rule validation (sufficient balance, valid dates, inventory checks)
- When ensuring validation is applied consistently across all entry points (web, API, background jobs)
- When failing early by rejecting invalid data before processing or storing it
- When working with form validation libraries or schema validation tools (Yup, Zod, Joi, Pydantic)
- When adding validation error handling in UI components or API error responses
- When testing validation logic to ensure security and data integrity

## Instructions

For details, refer to the information provided in this file:
[global validation](../../../agent-os/standards/global/validation.md)
