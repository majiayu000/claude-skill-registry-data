---
name: chapter-translation
description: Translate textbook chapter content into Urdu on demand while preserving technical accuracy and formatting.
---

# Chapter Translation

## Instructions

1. Receive chapter content (Markdown or plain text) as input.
2. Translate all content into Urdu, preserving:
   - Technical terms (robotics, AI, programming terms)
   - Diagrams/figure references (keep placeholders)
   - Headings, lists, code blocks formatting
3. Return the translated chapter ready for rendering in Docusaurus.
4. Optionally, allow integration with content-personalization to apply user-specific adaptations before translation.

## Example

Input:
```json
{
  "chapter_content": "Chapter 3: Kinematics of Humanoid Robots..."
}
