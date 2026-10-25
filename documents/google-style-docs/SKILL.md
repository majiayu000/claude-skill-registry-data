---
name: google-style-docs
description: Guide for writing documentation following Google's Developer Documentation Style Guide. Use this when creating or reviewing technical documentation, API docs, tutorials, or any product documentation that should follow Google's standards for clarity, consistency, and accessibility.
license: MIT
---

# Google Style Documentation Writer

This skill helps you write clear, consistent technical documentation following Google's Developer Documentation Style Guide principles and best practices.

## When to Use This Skill

Use this skill when:
- Writing new technical documentation, tutorials, or guides
- Reviewing or editing existing documentation for style consistency
- Creating API documentation or reference material
- Writing user-facing product documentation
- Ensuring documentation is accessible and inclusive
- Converting documentation from other styles to Google's standards

## Prerequisites

- Access to files being documented (code, APIs, features)
- Understanding of the target audience and their technical level
- Familiarity with the product or feature being documented

## Core Principles

Google's style guide is built on these foundations:

1. **Clarity**: Write in clear, simple, and direct language
2. **Consistency**: Use uniform terminology and structure
3. **Accessibility**: Make content accessible to all users, including those with disabilities
4. **Inclusivity**: Use inclusive, bias-free language
5. **Global audience**: Write for international readers (avoid idioms, region-specific terms)

## Instructions

### 1. Plan Your Document Structure

Before writing, determine:

- **Purpose**: What problem does this document solve?
- **Audience**: Who will read this? What's their technical level?
- **Scope**: What topics will you cover and what's out of scope?
- **Document type**: Tutorial, concept, reference, how-to guide?

Create an outline with:
```markdown
# Document Title (clear, specific, task-oriented)

## Overview (1-2 paragraphs)

## Prerequisites (if applicable)

## Main Content Sections
- Step-by-step instructions (for how-to guides)
- Conceptual explanation (for concept docs)
- Reference tables (for API docs)

## What's next (optional)

## Additional resources (optional)
```

### 2. Write the Title and Introduction

**Titles:**
- Use sentence case (capitalize only first word and proper nouns)
- Be specific and task-oriented: "Set up authentication" not "Authentication setup"
- Avoid gerunds when possible: "Configure" not "Configuring"
- Keep titles concise (under 80 characters)

**Introduction:**
- Write 1-2 paragraphs explaining what the document covers
- State the goal or outcome clearly in the first sentence
- Include what the reader will learn or accomplish
- Don't use phrases like "This document..." or "In this guide..."

Example:
```markdown
# Set up OAuth 2.0 authentication

Learn how to configure OAuth 2.0 authentication for your application. 
After completing these steps, your app will be able to securely authenticate 
users and access protected resources.
```

### 3. Apply Voice and Tone Guidelines

**Use second person ("you") to address the reader:**
- ✅ "You can configure the settings..."
- ❌ "One can configure..." or "The user can configure..."

**Use active voice:**
- ✅ "The system sends a confirmation email"
- ❌ "A confirmation email is sent by the system"

**Write in present tense:**
- ✅ "The function returns a string"
- ❌ "The function will return a string"

**Be direct and conversational:**
- ✅ "To delete a file, click **Delete**"
- ❌ "In order to accomplish the deletion of a file, one must click on the Delete button"

**Use contractions when natural:**
- ✅ "don't", "you're", "it's"
- But avoid in formal reference docs or when clarity might suffer

### 4. Format Text Elements

**Code elements:**
- Use backticks for inline code: `variable_name`, `function()`, `--flag`
- Use code blocks with language specification:
  ```python
  def example_function():
      return "Hello, world!"
  ```

**UI elements:**
- Bold for clickable UI elements: Click **Save**
- Use exact text from the interface
- Don't use italics for UI elements

**Placeholders:**
- Use ALL_CAPS with underscores: `PROJECT_ID`, `YOUR_API_KEY`
- Or use angle brackets: `<project-id>`, `<api-key>`
- Be consistent within a document
- Always explain what the placeholder represents

**Command-line examples:**
```bash
gcloud projects create PROJECT_ID --name="My Project"
```

**File paths:**
- Use forward slashes: `/path/to/file`
- Use backticks: `config/settings.json`

### 5. Write Clear Instructions

**Number steps sequentially:**
1. First, do this action.
2. Next, do this action.
3. Finally, verify the result.

**One action per step:**
- ✅ "1. Click **File** > **New** > **Project**."
- ❌ "1. Click File, then click New, and then create a new project."

**Use imperative mood (commands):**
- ✅ "Open the configuration file"
- ❌ "You should open the configuration file"

**Include expected results:**
```markdown
1. Run the following command:
   ```bash
   npm install package-name
   ```
   The output shows the installation progress and confirms success:
   ```
   added 1 package in 2s
   ```
```

### 6. Apply Inclusive and Accessible Writing

**Use inclusive language:**
- ✅ "They", "their" for singular gender-neutral pronouns
- ❌ "He/she", "his or her"
- ✅ "Allowlist", "blocklist"
- ❌ "Whitelist", "blacklist"
- ✅ "Primary/secondary" or "main/subordinate"
- ❌ "Master/slave"

**Write accessible content:**
```markdown
- Use descriptive link text: "See the authentication guide" not "Click here"
```
- Add alt text for images: `![Diagram showing data flow between client and server](image.png)`
- Don't rely solely on color to convey information
- Use proper heading hierarchy (H1 → H2 → H3, don't skip levels)

**Avoid ableist language:**
- ✅ "Run the script"
- ❌ "Sanity check the script"
- ✅ "Simple", "straightforward"
- ❌ "Crazy simple", "insanely easy"

### 7. Use Lists Effectively

**Bulleted lists** (unordered):
- Use for items without sequence
- Start each item with a capital letter
- Use parallel structure (all sentences or all fragments)
- Use periods if items are complete sentences

**Numbered lists** (ordered):
1. Use for sequential steps or ranked items
2. Start each item with a capital letter
3. Use periods for all items in a numbered list

**Example of parallel structure:**
✅ Good:
- Configure authentication
- Set up permissions
- Enable API access

❌ Bad:
- Configure authentication
- Setting up permissions
- The API access should be enabled

### 8. Write Effective Notes and Warnings

Use callouts sparingly and appropriately:

**Note**: Provides additional helpful information
```markdown
**Note:** The API has rate limits of 1000 requests per hour.
```

**Caution**: Warns about potential issues or unexpected behavior
```markdown
**Caution:** Deleting a project also deletes all associated resources.
```

**Warning**: Alerts about critical issues that could cause data loss or security problems
```markdown
**Warning:** This action cannot be undone. All data will be permanently deleted.
```

### 9. Format Code Examples

**Make examples self-contained and runnable:**
```python
# Import required libraries
import requests

# Set up authentication
api_key = "YOUR_API_KEY"
headers = {"Authorization": f"Bearer {api_key}"}

# Make the API request
response = requests.get("https://api.example.com/data", headers=headers)

# Handle the response
if response.status_code == 200:
    print("Success:", response.json())
else:
    print("Error:", response.status_code)
```

**Add explanatory comments:**
- Explain non-obvious code
- Don't state the obvious: ❌ `# Loop through items`
- Do explain intent: ✅ `# Retry up to 3 times for transient failures`

**Show error handling:**
Include realistic error handling in examples, not just the happy path.

### 10. Review and Edit

Before finalizing documentation:

1. **Check for clarity:**
   - Can a reader follow the instructions without external help?
   - Are all terms defined or linked to definitions?
   - Is the purpose clear from the first paragraph?

2. **Verify consistency:**
   - Is terminology consistent throughout?
   - Are formatting conventions uniform?
   - Do code examples use the same style?

3. **Test accuracy:**
   - Run all code examples and commands
   - Verify all links work
   - Check that UI instructions match current interface

4. **Review for style compliance:**
   - Use the checklist in the "Quality Checklist" section below
   - Search for common anti-patterns (passive voice, "please", future tense)
   - Ensure accessibility (heading hierarchy, link text, alt text)

## Examples

### Example 1: API Reference Entry

```markdown
## authenticate()

Authenticates a user with the provided credentials and returns an access token.

### Syntax

```javascript
authenticate(username, password)
```

### Parameters

- `username` (string, required): The user's email address or username.
- `password` (string, required): The user's password.

### Returns

A Promise that resolves to an object containing:
- `token` (string): The JWT access token for authenticated requests.
- `expiresIn` (number): Token expiration time in seconds.

### Example

```javascript
const auth = await authenticate("user@example.com", "securePass123");
console.log("Token:", auth.token);
console.log("Expires in:", auth.expiresIn, "seconds");
```

### Exceptions

- Throws `AuthenticationError` if credentials are invalid.
- Throws `NetworkError` if the authentication service is unreachable.
```

### Example 2: How-to Guide

```markdown
# Deploy your application to production

Deploy your application to a production environment using the deployment CLI tool.
After completing these steps, your application will be live and accessible to users.

## Before you begin

- Install the deployment CLI (version 2.0 or later)
- Set up your production credentials
- Ensure your application passes all tests

## Deploy the application

1. Build your application for production:
   ```bash
   npm run build
   ```
   The build process creates optimized files in the `dist/` directory.

2. Authenticate with the deployment service:
   ```bash
   deploy-cli login
   ```
   A browser window opens for authentication. Complete the sign-in process.

3. Deploy your application:
   ```bash
   deploy-cli deploy --project=PROJECT_ID --environment=production
   ```
   Replace `PROJECT_ID` with your project identifier.
   
   The deployment process takes 2-5 minutes. Monitor the progress in the terminal.

4. Verify the deployment:
   ```bash
   deploy-cli status --project=PROJECT_ID
   ```
   The status should show "Running" for all services.

## What's next

- [Monitor application performance](monitoring-guide.md)
- [Set up automated deployments](ci-cd-setup.md)
- [Configure custom domains](domain-setup.md)
```

### Example 3: Conceptual Overview

```markdown
# Authentication and authorization

Authentication verifies user identity, while authorization determines what actions an authenticated user can perform.

## How authentication works

When a user signs in to your application:

1. The application sends credentials (username and password) to the authentication service.
2. The service verifies the credentials against stored user records.
3. If valid, the service generates an access token and returns it to the application.
4. The application includes this token in subsequent API requests.

The token proves the user's identity without requiring repeated credential transmission.

## How authorization works

After authentication, the authorization system controls access:

- **Role-based access control (RBAC)**: Users are assigned roles (admin, editor, viewer), and each role has specific permissions.
- **Permission checks**: Before performing an action, the system verifies the user's role has the required permission.
- **Resource-level control**: Permissions can be scoped to specific resources (for example, edit access to only certain projects).

## Best practices

- Implement both authentication and authorization—they serve different purposes.
- Use industry-standard protocols (OAuth 2.0, OpenID Connect) for authentication.
- Apply the principle of least privilege: grant users only the permissions they need.
- Regularly audit and update user permissions.
```

## Best Practices

- **Start with the user's goal**: Frame documentation around what users want to accomplish, not feature lists
- **Use concrete examples**: Show real, runnable code rather than abstract syntax
- **Keep it scannable**: Use headings, lists, and formatting to help readers find information quickly
- **Link generously**: Connect to related docs, but ensure link text is descriptive
- **Update regularly**: Keep documentation current with product changes
- **Test your docs**: Have someone follow your instructions to find gaps or unclear steps
- **Use templates**: Create document templates for consistency across similar content types
- **Consider internationalization**: Avoid idioms, slang, and culturally specific references

## Word Choice and Terminology

**Preferred terms:**
- "Click" (not "click on")
- "Select" for choosing from dropdown menus or lists
- "Enter" for typing text (not "type in" or "input")
- "Filename" (one word)
- "Email" (not "e-mail")
- "Sign in" and "sign out" (not "log in" or "login")
- "On" for devices and platforms: "on macOS", "on your phone"
- "In" for applications: "in the app", "in Chrome"

**Avoid:**
- "Please" (just give the instruction)
- "Simply", "just", "easy" (they're subjective and can be condescending)
- "Obviously", "clearly" (if it were obvious, you wouldn't need to document it)
- Exclamation points (except in UI text quotes or very rare celebratory contexts)
- Latin abbreviations: Use "for example" not "e.g.", "that is" not "i.e."

## Common Issues

**Issue**: Documentation reads like a feature announcement  
**Solution**: Focus on user tasks and goals, not feature descriptions. Start with "You can..." or action verbs.

**Issue**: Steps are too broad or combine multiple actions  
**Solution**: Break down into atomic steps, each with one action. Number them clearly.

**Issue**: Code examples don't run  
**Solution**: Test all examples in a clean environment. Include all necessary imports, setup, and error handling.

**Issue**: Passive voice makes instructions unclear  
**Solution**: Convert to active voice and use imperative mood. "The configuration file should be edited" → "Edit the configuration file"

**Issue**: Technical jargon without explanation  
**Solution**: Define terms on first use, link to glossary, or use simpler alternatives when possible.

**Issue**: Inconsistent terminology  
**Solution**: Create a project-specific term list and use consistent terms throughout. Don't alternate between synonyms.

**Issue**: Documentation becomes outdated  
**Solution**: Set up a review schedule, use doc tests that run against actual code, and link docs to specific version numbers.

## Quality Checklist

Use this checklist when reviewing documentation:

**Structure and Organization:**
- [ ] Title uses sentence case and is task-oriented
- [ ] Introduction clearly states purpose and outcome
- [ ] Proper heading hierarchy (H1 → H2 → H3, no skipped levels)
- [ ] Logical flow from prerequisites to conclusion

**Voice and Style:**
- [ ] Uses second person ("you")
- [ ] Uses active voice
- [ ] Uses present tense
- [ ] Direct and conversational tone

**Instructions and Code:**
- [ ] Steps are numbered and sequential
- [ ] One action per step
- [ ] Code examples are complete and runnable
- [ ] Placeholders are clearly marked and explained
- [ ] Expected outputs are shown

**Formatting:**
- [ ] Code elements use backticks
- [ ] UI elements are bolded
- [ ] Links use descriptive text
- [ ] Lists use parallel structure
- [ ] Callouts (Note, Caution, Warning) are used appropriately

**Accessibility and Inclusion:**
- [ ] Inclusive language (no ableist or biased terms)
- [ ] Gender-neutral pronouns
- [ ] Descriptive link text
- [ ] Alt text for images
- [ ] No reliance on color alone

**Accuracy and Clarity:**
- [ ] All technical information is accurate
- [ ] Code examples have been tested
- [ ] Links work and point to current content
- [ ] Terminology is consistent
- [ ] All terms are defined or linked

## Additional Resources

### Primary References
- [Google Developer Documentation Style Guide](https://developers.google.com/style) - Official comprehensive guide
- [Google Style Guide Highlights](https://developers.google.com/style/highlights) - Quick reference for key guidelines
- [Word List](https://developers.google.com/style/word-list) - Preferred terms and usage

### Related Skills
- API documentation skills
- Tutorial writing skills
- Technical editing skills

### Tools
- Linters and validators for Markdown and documentation
- Vale (style checker that can enforce Google's style rules)
- Write Good linter for basic grammar and style checks

## Supporting Files in This Skill

This skill includes several helpful resources:

- **QUICKREF.md**: Quick reference guide with checklists, common patterns, and style rules. Use this for fast lookups while writing or reviewing documentation.

- **example-deployment-guide.md**: A complete example of a how-to guide that demonstrates all Google style principles in practice. Reference this to see how the guidelines apply to real documentation.

- **README.md**: Human-readable overview of the skill for developers and contributors. Explains what the skill does and how to use it.

## Notes

This skill is based on the [Google Developer Documentation Style Guide](https://developers.google.com/style) and incorporates best practices from Google's technical writing team. The guidelines provided are recommendations; always prioritize clarity and user needs over strict adherence to any single rule.

When style guidelines conflict with established project conventions, discuss with your team before making changes. Consistency within a project is often more important than perfect compliance with an external style guide.
