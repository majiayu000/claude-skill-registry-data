---
name: coding-error-messages
description: Best practices for writing clear, actionable error messages in code.
---

# Coding Error Messages

You are an expert at writing clear, actionable error messages. Review the following error message and improve it according to these criteria:

## Core Principles

1. Clarity: What went wrong?

- State the problem in plain language
- Avoid jargon unless it's domain-specific and necessary
- Be specific about what failed, not just that something failed

2. Context: Where and why?

- Include relevant values, parameters, or state
- Explain what the system expected vs. what it received
- Provide enough context to locate the issue quickly

3. Actionability: What can the user do?

- Suggest concrete next steps
- Point to the likely cause if known
- Include documentation links or examples when helpful

4. Tone: Be helpful, not accusatory

- Avoid "invalid", "illegal", "bad" without explanation
- Don't blame the user
- Stay professional and supportive

## Quality Checklist

- [] Does it explain WHAT failed?
- [] Does it explain WHY it failed?
- [] Does it suggest HOW to fix it?
- [] Are actual values included (when safe/relevant)?
- [] Is it understandable to the target audience?
- [] Does it avoid technical debt phrases like "Error: undefined"?
- [] Is it appropriately brief but complete?

## Example Transformations

❌ Before:

```
typescriptthrow new Error("Invalid input");
```

✅ After:

```
typescriptthrow new Error(
  `Invalid email format: "${email}". Expected format: user@domain.com`
);
```

❌ Before:

```
typescriptthrow new Error("Failed to connect");
```

✅ After:

```
typescriptthrow new Error(
  `Failed to connect to database at ${host}:${port}. ` +
  `Check that the database is running and credentials are correct. ` +
  `Connection timeout: ${timeout}ms`
);
```

---

**Now review this error message:**

[Paste error message here]

Provide:

A score (1-10) for each core principle
The improved error message
Brief explanation of changes made
