---
name: "Requirements Elicitation"
description: "Extract complete, unambiguous requirements from specifications by identifying functional/non-functional requirements and clarifying ambiguities"
category: "analysis"
required_tools: ["Read", "Write", "Grep"]
---

# Requirements Elicitation

## Purpose
Extract complete, unambiguous requirements from user specifications, identifying what needs to be built while clarifying unclear or missing information.

## When to Use
- Analyzing new feature requests
- Processing enhancement specifications
- Breaking down large features into components
- Identifying missing information in requirements

## Key Capabilities
1. **Extract Requirements** - Identify functional and non-functional requirements
2. **Clarify Ambiguities** - Flag unclear specifications and ask targeted questions
3. **Identify Constraints** - Find technical, business, and resource limitations

## Approach
1. Read entire specification thoroughly
2. Extract explicit requirements (stated clearly)
3. Identify implicit requirements (assumed but not stated)
4. Flag ambiguities and inconsistencies
5. Document acceptance criteria for each requirement

## Example
**Context**: Feature request to "add export functionality"

**Approach**:
- What formats? (CSV, JSON, PDF?)
- What data to export? (All fields or subset?)
- Who can export? (All users or admins only?)
- Size limits? (Max rows, file size?)
- Output: Clear requirements with acceptance criteria

## Best Practices
- ✅ Ask "what" questions, not "how"
- ✅ Document assumptions explicitly
- ✅ Create testable acceptance criteria
- ❌ Avoid: Making technical implementation decisions