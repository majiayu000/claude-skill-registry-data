---
name: Global Error Handling
description: Implement proper error handling patterns for n8n nodes using NodeApiError and NodeOperationError classes. Use this skill when writing try-catch blocks in execute methods, handling HTTP errors, validating parameters, parsing API error responses, implementing continueOnFail logic, writing actionable error messages, or handling errors in trigger nodes. Apply when working with external API calls, authentication errors, rate limiting, or any error scenarios in n8n node development.
---

## When to use this skill:

- When writing try-catch blocks in n8n node execute methods
- When handling HTTP request errors (401, 404, 429, etc.)
- When choosing between NodeApiError and NodeOperationError
- When validating required parameters and input formats
- When parsing error responses from external APIs
- When implementing continueOnFail() logic for batch processing
- When writing actionable, user-friendly error messages
- When redacting sensitive information from error output
- When handling errors in trigger node setup
- When adding error descriptions that help users fix issues
- When dealing with authentication, rate limiting, or external service failures

# Global Error Handling

This Skill provides Claude Code with specific guidance on how to adhere to coding standards as they relate to how it should handle global error handling.

## Instructions

For details, refer to the information provided in this file:
[global error handling](../../../agent-os/standards/global/error-handling.md)
