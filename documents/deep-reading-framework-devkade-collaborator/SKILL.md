---
name: deep-reading-framework
description: Three-pass critical reading framework for systematic document analysis. Supports tech blogs, retrospectives, technical documentation, personal writing, and academic papers. Primary focus on Third Pass critical analysis, context validation, and actionable reconstruction. Use when analyzing complex documents, performing critical reading, extracting actionable insights, or conducting deep analysis. Triggers include Third Pass, 비판적 분석, critique, 깊이 읽기, 심층 분석.
---

# Deep Reading Framework

A systematic approach to deep document analysis based on the three-pass reading methodology. This skill guides critical analysis with emphasis on Third Pass: assumption validation, context dependencies, and actionable reconstruction.

## Overview

This skill provides structured guidance for Third Pass critical analysis of documents. Users complete First and Second Pass independently (reading, understanding, note-taking), then use this skill for deep critical analysis that challenges assumptions, identifies context dependencies, and extracts actionable insights.

## Quick Start

**Typical workflow:**

1. User reads document and completes First/Second Pass independently
2. User triggers skill: "Third Pass 시작" or "이 글 비판적으로 분석해줘"
3. Skill detects document type automatically
4. Guides systematic critical analysis
5. Outputs structured analysis compatible with user's template

## Document Type Detection

Automatically detect and adapt analysis to document type based on content, structure, vocabulary, and writing style.

**Supported types:**
- **tech-blog**: Technical articles, tutorials, engineering posts (problem-solution structure, code examples)
- **retrospective**: Project retrospectives, experience sharing, lessons learned (temporal narrative, reflective tone)
- **technical-doc**: API documentation, architecture docs, specifications (reference structure, technical precision)
- **personal-writing**: User's own drafts, essays, thought pieces (exploratory tone, argument structure)
- **academic-paper**: Research papers, scholarly articles (abstract, methods, citations)

**Detection approach:**
1. Analyze content markers (abstract, code blocks, section headings)
2. Identify vocabulary patterns (academic vs conversational, technical depth)
3. Assess structure (sequential vs reference vs argumentative)
4. If ambiguous, ask: "이 문서는 [TYPE1] 또는 [TYPE2] 중 어느 것에 가까운가요?"

## Third Pass Workflow

Follow these steps systematically:

### Step 1: Document Type Confirmation

State the detected type and confirm with user:
"이 문서를 [TYPE]로 판단했습니다. Third Pass 비판적 분석을 시작할까요?"

### Step 2: Critical Analysis

Challenge core claims and validate reasoning.

**Universal questions (all types):**
- What are the central claims or messages?
- What evidence or reasoning supports them?
- What are potential weaknesses or limitations?
- What counterexamples or failure cases exist?
- Is this generalizable or context-specific?

**Load type-specific questions:** Read `references/critical-questions.md` for detailed questions per document type.

Output format:
```markdown
#### Critical Analysis
- **주장의 약점 / 적용 한계**
  - [Specific issues with claims, evidence, or reasoning]
  - [Scenarios where this approach fails]
  - [Generalization limits]
```

### Step 3: Context Dependencies

Identify implicit assumptions that constrain validity.

**Key dimensions:**
- **Technical environment**: Stack, tools, scale, constraints
- **Prerequisites**: Assumed knowledge or experience level
- **Temporal context**: When written, evolving technologies
- **Cultural/organizational**: Team structure, company culture, regional factors

Output format:
```markdown
- **컨텍스트 의존성 (환경, 스택, 시기)**
  - Environment: [Tech stack, scale, constraints that this assumes]
  - Prerequisites: [What reader needs to know/have]
  - Temporal: [Time-dependent assumptions]
  - Cultural: [Organizational or regional assumptions]
```

### Step 4: Missing Perspectives

Find gaps, alternatives, and unexplored angles.

**Look for:**
- Alternative approaches not mentioned
- Trade-offs or costs not discussed
- Contrary viewpoints or debates
- Edge cases or exceptions
- Relevant references or prior work not cited

Output format:
```markdown
- **누락된 관점 / 대안**
  - Alternatives: [Other approaches not considered]
  - Trade-offs: [Costs or sacrifices not discussed]
  - Contrary views: [Opposing perspectives]
  - Edge cases: [Scenarios not addressed]
```

### Step 5: Reconstruction

Demonstrate deep understanding by restating core ideas without reference to source.

**Tasks:**
- Summarize key concepts in own words
- Explain the approach as if teaching someone
- Identify what applies to your context
- Consider how you would approach differently

Output format:
```markdown
#### Reconstruction
- **핵심을 나만의 언어로**
  - [Restate the central thesis and key supporting ideas without looking at source]

- **내 상황에 적용한다면**
  - 직접 적용: [What can be adopted as-is]
  - 변형 필요: [What needs modification and how]
  - 적용 불가: [What doesn't fit my situation and why]
```

### Step 6: Actionable Insights

Extract practical value and next steps.

**Focus on:**
- Immediate takeaways
- Limitations to remember
- Follow-up questions or experiments
- Related areas to explore
- Actions to take

Output format:
```markdown
#### Discussion
- **가져갈 것**
  - [Most valuable insights - what to remember and apply]

- **한계**
  - [Boundaries of applicability, remaining uncertainties]

#### Action Items
- [ ] [Specific action item or research question]
- [ ] [Related concept to explore]

#### Future Ideas
- [ ] [Experiment to validate understanding]
```

## Interactive Guidance

Guide user through analysis with checkpoints:

**After type detection:**
"[TYPE]로 분석을 시작합니다. 이 유형에 맞는 비판적 질문을 적용하겠습니다."

**After each major step:**
"[STEP] 완료했습니다. 다음 단계([NEXT_STEP])로 진행할까요, 아니면 이 부분을 더 깊이 탐구할까요?"

**When user seems uncertain:**
"특정 섹션이나 주장에 대해 더 자세히 분석하고 싶으신 부분이 있나요?"

## On-Demand Support

Provide targeted assistance beyond Third Pass:

**Second Pass support:**
- "이 그림/표가 정확히 무엇을 의미하는지 도와줘"
- "핵심 주장과 증거를 정리해줘"

**Contextual research:**
- "관련 논문/글 찾아줘"
- "이 접근법을 사용한 다른 사례는?"

**Concept clarification:**
- "이 용어/개념이 정확히 무엇을 의미하는지 설명해줘"
- "이 가정이 타당한지 검증해줘"

**Comparison:**
- "이 글과 [[다른글]] 비교 분석해줘"
- "이 두 접근법의 차이는 무엇인가?"

## Best Practices

**For optimal results:**

1. **Complete First/Second Pass independently** - Have basic understanding before critical analysis
2. **Provide context** - Share your background, goals, or specific concerns
3. **Be specific** - Point to particular sections or claims for focused analysis
4. **Iterate** - Refine sections that need deeper exploration
5. **Connect to practice** - Always consider real-world applicability

**When to use this skill:**

✅ After reading complex technical content
✅ When evaluating whether to adopt an approach
✅ Before citing or building upon an article
✅ When reviewing your own writing for gaps
✅ During literature review or research

**When NOT to use:**

❌ For quick skimming or surface reading
❌ When basic comprehension is sufficient
❌ For simple reference lookups

## Progressive Disclosure

For complex analysis needs:

1. **Start with SKILL.md** - Core workflow and guidance
2. **Load references as needed**:
   - `references/critical-questions.md` - Type-specific analytical questions
   - `references/reconstruction-guide.md` - Detailed reconstruction techniques
   - `references/common-patterns.md` - Frequently encountered patterns and pitfalls
3. **Use assets for output** - Standard templates for consistent formatting

## Notes on Output

- Match user's existing template structure when provided
- Use bullet points with bold headings for clear structure
- Keep analysis concise but thorough
- Focus on actionable insights over abstract critique
- Prioritize practical applicability
