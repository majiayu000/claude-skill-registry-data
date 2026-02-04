---
name: superwhisper-custom-mode
description: Guide for creating effective Custom Mode prompts and examples for Superwhisper, an AI dictation app. Use when users want to create, improve, or understand Superwhisper custom mode instructions for processing dictated speech with context-awareness, and when users want to generate examples.
---

# Superwhisper Prompt Generator

This skill helps create effective Custom Mode prompts for Superwhisper, an AI dictation app that processes speech with context-awareness.

## Overview

Superwhisper Custom Modes use AI instructions to transform dictated speech. The AI receives:
- **User Message**: The transcribed dictation
- **Application Context**: Active app info, system details (date, time, user name, computer name)
- **Clipboard Context**: Recently copied text (within 3 seconds of dictation)
- **Text Selection Context**: Selected text (requires JSON config edit)

## Working with Existing Prompts

When users want to modify an existing Custom Mode prompt, they may provide either:

### Option 1: Just the Custom Instructions
The raw prompt text they wrote in Superwhisper's Advanced Settings.

### Option 2: The History Tab Output
The complete prompt that Superwhisper sent to the AI, which includes:

```
INSTRUCTIONS:
[Their custom prompt instructions]

EXAMPLES OF CORRECT BEHAVIOR:
User: [Example input 1]
Assistant: [Example output 1]
User: [Example input 2]
Assistant: [Example output 2]

SYSTEM CONTEXT:
[Auto-generated: current time, timezone, locale, computer name]

USER INFORMATION:
[Auto-generated: user's full name]

APPLICATION CONTEXT:
[Auto-generated: active app, focused elements, detected names]

USER MESSAGE:
[The actual dictated speech that was transcribed]
```

**Key understanding**: 
- The **INSTRUCTIONS** section contains the custom prompt to modify
- The **EXAMPLES OF CORRECT BEHAVIOR** section shows their examples in User/Assistant format (automatically converted from the Input/Output fields they entered in the UI)
  - **IMPORTANT**: These examples are ALREADY properly configured in the UI. This is just the output format for viewing in history. Do NOT suggest moving them to the UI - they're already there!
- Everything else (SYSTEM CONTEXT, USER INFORMATION, APPLICATION CONTEXT, USER MESSAGE) is automatically added by Superwhisper and is NOT part of the custom instructions

**When modifying a prompt from history output:**
- Focus on improving the INSTRUCTIONS section
- If examples need improvement, suggest BETTER examples to REPLACE the existing ones
- Do NOT suggest "separating examples into the UI" - if they're in the history output, they're already in the UI

## Prompt Structure

### Basic Structure

```
[Role/Purpose Statement]

[Main Instructions]

[Context References]

[Requirements/Constraints]

[Examples (optional but recommended)]
```

### Using XML Tags (Optional)

For complex, multi-step instructions, structuring your prompt with XML tags can help communicate clearly with the AI.

**Important**: XML tags are optional in Superwhisper prompts. In many cases, using XML tags improves clarity and output quality, especially with advanced models. However, some less capable or local AI models may misinterpret or be confused by XML tags. Use them thoughtfully and test your results for best compatibility.

**Basic Tag Structure**

Set a role and instructions:
```xml
<role>You are a text editor</role>
<instructions>Format the content of User Message into clear paragraphs</instructions>
```

Define specific requirements:
```xml
<requirements>
- Use simple, clear language
- Keep the casual tone
- Break into short paragraphs
</requirements>
```

**Extended Tag Examples**

Provide context and style for richer outputs:
```xml
<context>
- This content is for a cooking blog post
- Target audience is home cooks
- Should use casual, approachable language
- Include cooking-specific terminology where relevant
</context>

<style>
- Write in a warm, encouraging tone
- Use descriptive but simple language
- Include helpful cooking tips
- Make instructions easy to follow
</style>

<output-format>
- Title and introduction
- Ingredient list
- Step-by-step instructions
- Cook's notes and tips
</output-format>
```

**Tip**: Adjust and expand your XML tags based on your specific needs. Generally speaking, the more detailed your instructions, the better the results.

## Referencing Context

Use these exact naming conventions to reference context in your custom instructions:

**Note**: When viewing the history output, you'll see SYSTEM CONTEXT, USER INFORMATION, and APPLICATION CONTEXT automatically included by Superwhisper. You don't write these sections - you just reference them in your custom instructions using the conventions below.

### User Message
The dictated/transcribed text. Always the primary input.

**Example**: "The User Message contains dictated speech. Format it into clear paragraphs."

### Application Context
Active application and system information.

**Example**: "If Application Context shows a code editor, format the User Message as code comments."

### Clipboard Context
Text copied within 3 seconds of starting dictation.

**Example**: "Use the code style from Clipboard Context as a reference when formatting."

### Text Selection Context
Text selected before dictation (requires JSON config: `"context_from_selection": true`).

**Example**: "Transform the Text Selection Context based on the command in User Message."

### Combined Context

**Example**:
```
If Application Context shows a messaging app:
- Keep the User Message casual and brief
- If Clipboard Context contains a URL, format as a link

If Application Context shows an email client:
- Format the User Message professionally
- Sign with the user's name from Application Context
```

## Best Practices

### Be Explicit About Dictation
Tell the AI that input is spoken, not written:
- ✅ "The User Message contains dictated speech that may have informal phrasing."
- ❌ Assuming the AI knows it's dictated

### Focus Instructions
Direct the AI to specific content and actions:
- ✅ "Transform the User Message into bullet points. Use simple language."
- ❌ "Help me with my text."

### Add Detail for Better Results
More specific instructions yield better outputs:
- ✅ "Format the User Message as a professional email with a greeting, 2-3 concise paragraphs, and a polite closing."
- ❌ "Make this an email."

### Include 2-3 Examples

Examples significantly improve accuracy by showing expected input/output patterns. Examples are added separately in Superwhisper's Advanced Settings sidebar (not in the prompt itself).

**How examples work in Superwhisper:**
- Each example has two parts: **Input field** (how you'll phrase requests) and **Output field** (expected AI response)
- Click "Add Example" in the Advanced Settings sidebar to create example pairs
- Add 2-3 examples for best results

**Format when providing examples to users:**

Input: "I need to finish the quarterly report and send it to Sarah by Friday"
Output: "[TASK] Finish quarterly report
Due: Friday
Priority: Normal
Assignee: Sarah
Details: Complete and send the quarterly report to Sarah by end of week"

**How they appear in the history tab:**

When you view the history output, your examples are automatically formatted as:
```
EXAMPLES OF CORRECT BEHAVIOR:
User: I need to finish the quarterly report and send it to Sarah by Friday
Assistant: [TASK] Finish quarterly report
Due: Friday
Priority: Normal
Assignee: Sarah
Details: Complete and send the quarterly report to Sarah by end of week
```

This transformation is automatic - you just provide Input/Output pairs in the UI.

**When evaluating existing examples from history output:**
- If examples are present in "EXAMPLES OF CORRECT BEHAVIOR" → they're already properly configured
- Evaluate them for quality: Do they demonstrate the desired behavior? Are they diverse enough?
- Suggest BETTER or ADDITIONAL examples if needed, but never suggest "moving them to the UI"

### Keep It Simple for Basic Tasks
Not every prompt needs complexity:

**Simple**: "Format the User Message into clear, short paragraphs."

**Complex**: Only when handling multiple contexts, conditional logic, or specialized formatting.

## Detailed Use Case Examples

For complete prompt examples with Input/Output pairs for various scenarios, see [references/EXAMPLES.md](references/EXAMPLES.md).

The examples file includes ready-to-use prompts for:
- Email Writing
- Code Comments
- Meeting Notes
- Text Transformation Commands
- Translation with Context
- Quick Task Creation
- Slack Message Formatting
- Professional Document Writing
- Social Media Post Creation

Read EXAMPLES.md when you need specific prompt templates or want to see complete examples with suggested Input/Output pairs.

## Troubleshooting Tips

### Unexpected Results
- Check if context was captured: View History tab → right sidebar "prompt" field
- Simplify instructions if using a less capable model
- Verify context toggles are enabled in Advanced Settings

### Context Not Working
- Clipboard Context: Must copy within 3 seconds of starting dictation
- Text Selection Context: Requires JSON config edit (`"context_from_selection": true`)
- Application Context: Should work automatically when enabled

### Model Compatibility
- Complex prompts with XML and multiple contexts work best with Claude or GPT models
- Simpler prompts work better with less capable or local models
- Test and adjust based on results

### Common Misconceptions When Reviewing History Output
- **Examples in "EXAMPLES OF CORRECT BEHAVIOR"**: These ARE already properly configured in the UI. This is just how they appear in the history view. Focus on improving their quality, not their location.
- **System/User/Application Context sections**: These are auto-generated and cannot be edited. You can only reference them in your custom instructions.
- **User Message section**: This is the actual dictation being processed. It's not part of the configuration.

## Prompt Generation Process

When creating a custom prompt:

1. **Identify the task**: What should the output be?
2. **Determine context needs**: Which contexts are relevant?
3. **Write clear instructions**: Be specific about what to do
4. **Add constraints**: Define format, tone, requirements
5. **Create 2-3 examples**: Format as Input/Output pairs to add in Superwhisper's Advanced Settings sidebar
6. **Test and iterate**: Try it out and refine based on results

**Important**: When providing examples to users, always format them clearly with "Input:" and "Output:" labels. These get added separately in Superwhisper's UI, not embedded in the prompt instructions.

## Template Starter

```
[What the AI should do with User Message]

[How to use Application Context, if relevant]

[How to use Clipboard Context or Text Selection Context, if relevant]

Requirements:
- [Requirement 1]
- [Requirement 2]
- [Requirement 3]

[Any special conditions or edge cases]
```

Fill in the brackets based on your specific use case, then test and refine.
