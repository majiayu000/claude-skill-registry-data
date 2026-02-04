---
name: prepare-docs
description: |
  Use when user requests automated documentation preparation. Triggers include:
  - Korean: "문서 준비해줘", "문서화 준비", "문서 요구사항 작성", "자동 문서화 준비"
  - English: "prepare documentation", "setup doc requirements", "prepare for automated docs"
  - Context: User wants to prepare all requirements for automated documentation generation

  This skill discovers sources, defines structure, and saves complete requirements to file
  for use with write-docs skill (automated generation).
---

# Documentation Preparation Skill (Automated Workflow - Step 1)

## Overview

This skill prepares complete documentation requirements for automated generation. It:

1. **Discovers all sources** - Core sources + related files (tests, types, examples)
2. **Defines document structure** - Based on doc type and project templates
3. **Builds content map** - What to document from where
4. **Saves requirements file** - Complete specification for write-docs skill

**When to use this skill:**
- User says "문서 준비해줘" or "prepare documentation"
- Starting automated documentation workflow
- User wants hands-off doc generation after initial setup

**⚠️ IMPORTANT - Automated Workflow:**
- **Interactive setup** - Steps 1-3 ask user questions to define scope
- **Automated discovery** - Step 4 automatically finds related sources and builds content map
- **Saves requirements to file** - Always outputs `docs/doc-requirements.md`

---

## Workflow: 5-Step Preparation Process

### Step 1: Collect Source Links

**Questions to ask:**

1. "어떤 소스를 분석할까요?" (What sources should I analyze?)
   - GitHub repositories (URLs or local paths)
   - Web pages (documentation sites, blog posts)
   - Local files (code files, markdown docs, PDFs)
   - Google Drive documents (check for MCP server)
   - Notion pages (check for MCP server)

2. "중점적으로 분석할 키워드나 토픽이 있나요?" (Any specific keywords or topics to focus on?)

---

### Step 2: Select Document Type

Ask: "어떤 문서를 만들까요?" (What type of documentation should I create?)

**Options:**

1. **API Reference**
   - Audience: Developers integrating with the code
   - Focus: Functions, classes, parameters, return values, examples
   - Structure: Organized by module/class/function

2. **System Overview**
   - Audience: Engineers understanding architecture
   - Focus: Components, data flow, design principles, communication patterns
   - Structure: Top-down from high-level to implementation details

3. **Tutorial**
   - Audience: Users learning how to use the system
   - Focus: Step-by-step instructions, practical examples, common pitfalls
   - Structure: Sequential steps with verification checkpoints

4. **Custom**
   - User specifies their own document type and purpose

---

### Step 3: Define Document Structure

Based on document type selected in Step 2, **present default sections and ask user to customize**.

**Workflow:**

1. **Show default sections** for selected document type (see below)

2. **Ask user**: "기본 구조에서 제외할 항목이 있나요?" (Any sections to remove from default structure?)
   - User can specify sections to exclude
   - Example: "Performance Characteristics 제외"

3. **Ask user**: "추가로 포함할 항목이 있나요?" (Any additional sections to include?)
   - User can add custom sections
   - Examples: Migration Guide, Troubleshooting, FAQ, Benchmarks, Comparison with Alternatives

4. **Confirm final structure** - Show final section list before proceeding to Step 4

**Note**: If user mentions a project template, use that instead of default structure.

---

**Default sections by document type:**

**For API Reference:**
- [ ] Overview (purpose of this module/API)
- [ ] Core Concepts (key abstractions)
- [ ] Functions (organized by category)
- [ ] Types (data structures)
- [ ] Constants
- [ ] Usage Patterns
- [ ] Limitations
- [ ] Related APIs

**For System Overview:**
- [ ] Introduction (purpose, use cases)
- [ ] Architecture (high-level design)
- [ ] Components (individual parts + responsibilities)
- [ ] Data Flow (how information moves)
- [ ] State Management
- [ ] Communication Patterns
- [ ] Configuration
- [ ] Error Handling
- [ ] Performance Characteristics

**For Tutorial:**
- [ ] Introduction (what you'll learn, time estimate)
- [ ] Prerequisites (required knowledge, tools)
- [ ] Step 1, 2, 3... (sequential instructions)
- [ ] Testing Your Implementation
- [ ] Common Pitfalls
- [ ] Next Steps

**Note**: Order sections logically (general → specific) in final structure.

---

### Step 4: Content Discovery and Source Expansion

**Purpose:** Start from core sources and actively discover all related sources needed for comprehensive documentation.

**Workflow:**

1. **Analyze core sources** (from Step 1)
   - Identify documentable items: functions, types, classes, concepts
   - Note primary information available

2. **For each item, discover related sources**:

   **For Functions/Methods:**
   - ✅ Test files (usage examples, edge cases)
   - ✅ Type definitions (parameter types, return types)
   - ✅ Related functions (callers, callees)
   - ✅ Documentation comments (inline docs)
   - ✅ Error handling (related error types)

   **For Types/Classes:**
   - ✅ Constructors and factory functions
   - ✅ Methods and properties
   - ✅ Usage examples in tests
   - ✅ Related types (inheritance, composition)
   - ✅ Serialization/deserialization code

   **For Concepts/Modules:**
   - ✅ Design documents (docs/, wiki, ADRs)
   - ✅ README files
   - ✅ Example code (examples/, demos/)
   - ✅ Related modules (imports, dependencies)

3. **Build content map**:

   ```
   ## Content Map

   ### Function: parse()
   **Primary source:** src/parser.rs:45-60
   **Related sources found:**
   - tests/parser_test.rs:100-150 (usage examples, edge cases)
   - src/types.rs:10-25 (Token type definition)
   - docs/design.md:30-45 (recursive descent explanation)
   - examples/basic_usage.rs:20-35 (real-world example)

   **Coverage:** ✅ Complete (signature, behavior, examples, design rationale)

   ### Type: Token
   **Primary source:** src/types.rs:10-25
   **Related sources found:**
   - src/lexer.rs:80-120 (Token creation)
   - tests/token_test.rs:50-80 (all variants tested)

   **Coverage:** ✅ Complete (definition, creation, usage)

   ### Concept: Error Recovery
   **Primary source:** src/parser.rs:300-350
   **Related sources found:**
   - (none found in tests/)
   - (no design docs found)

   **Coverage:** ⚠️ Partial (implementation exists, no design rationale or examples)
   ```

**Example Workflow:**

```
User provides: src/parser.rs

Claude discovers:
1. Functions: parse(), tokenize(), validate()
2. For parse():
   → Search tests/ for "parse" → Found tests/parser_test.rs
   → Check imports in test file → Found src/types.rs (Token definition)
   → Search docs/ for "parse" → Found docs/design.md
   → Check examples/ → Found examples/basic_usage.rs
3. For Token type:
   → Search for "Token" in codebase → Found src/lexer.rs (creation)
   → Found tests/token_test.rs (all variants)
4. For validate():
   → Search tests/ for "validate" → Found tests/validator_test.rs
   ...

Result: Comprehensive source list discovered automatically
```

**⚠️ Trust all sources** - Don't judge quality or note contradictions. If contradictions exist, write-docs will handle them during generation.

---

### Step 5: Save Requirements File

**Always save to:** `docs/doc-requirements.md`

**File contains:**
- Document type and target audience
- All discovered sources (core + related)
- Document structure with sections
- Content map (what to document from where)

**File format:**
```markdown
# Documentation Requirements

**Created**: 2025-10-22
**Document Type**: API Reference
**Target Audience**: Developers integrating the parser

## Discovered Sources

### Core Sources (user-provided):
- src/parser.rs

### Related Sources (discovered):
- tests/parser_test.rs (usage examples)
- src/types.rs (type definitions)
- docs/design.md (design rationale)
- examples/basic_usage.rs (real-world usage)
- src/lexer.rs (related functionality)
- tests/token_test.rs (type examples)

Total: 7 sources

## Document Structure

- [ ] Introduction
- [ ] Core Concepts
- [ ] Functions (parse, tokenize, validate)
- [ ] Types (Token, AST, ParseError)
- [ ] Usage Patterns
- [ ] Limitations

## Content Map

### Function: parse()
**Primary source:** src/parser.rs:45-60
**Related sources:**
- tests/parser_test.rs:100-150 (usage examples)
- src/types.rs:10-25 (Token type)
- docs/design.md:30-45 (design rationale)

### Type: Token
**Primary source:** src/types.rs:10-25
**Related sources:**
- src/lexer.rs:80-120 (construction)
- tests/token_test.rs:50-80 (examples)

```

After saving, confirm to user:
> "문서 요구사항을 docs/doc-requirements.md에 저장했습니다. 'write-docs 실행해줘'를 입력하면 자동으로 문서를 생성합니다."

---

## Tips for Effective Preparation

1. **Ask before assuming** - If user's intent is unclear during initial setup, ask clarifying questions
2. **Suggest recommendations** - "parser 모듈이니까 API Reference가 적합해 보입니다"
3. **Document discovery thoroughly** - Build comprehensive content map showing all discovered sources for each documentable item

---

## Conclusion

After completing this preparation workflow, you should have:

✅ All sources discovered (core + related)
✅ Document type and structure defined
✅ Content map showing what to document from where
✅ Requirements file saved to `docs/doc-requirements.md`

