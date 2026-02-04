---
name: cote-teacher
description: This skill should be used when the user requests learning materials for algorithm or data structure patterns (e.g., "Create learning material for sliding window pattern"). It automatically generates structured markdown documents in the _learning/ folder and updates the main README.md with links to the new materials.
---

# CoTe Teacher

## Overview

This skill automates the creation of structured learning materials for coding test (CoTe) algorithm and data structure patterns. When a user requests learning materials for a specific pattern or concept, this skill generates a comprehensive markdown document following a standardized template and automatically updates the project's README.md with a link to the new material.

## When to Use This Skill

Use this skill when the user requests:
- Learning materials for algorithm patterns (e.g., "Create learning material for sliding window pattern")
- Concept explanations for data structures (e.g., "Explain hash table concept with examples")
- Study guides for specific problem-solving techniques (e.g., "Make a two-pointer technique guide")

**Trigger keywords**: 학습 자료, 패턴 정리, 개념 정리, 학습, 정리, learning material, pattern guide

## Workflow

### Step 1: Understand the Request

Identify the algorithm/pattern/concept from the user's request:
- Sliding window (슬라이딩 윈도우)
- Two pointers (투 포인터)
- Hash table (해시 테이블)
- Dynamic programming (동적 계획법)
- DFS/BFS
- Greedy algorithm (그리디)
- Binary search (이진 탐색)
- etc.

### Step 2: Prepare the Environment

1. **Check/create _learning/ folder**:
   ```bash
   mkdir -p _learning
   ```

2. **Determine the filename**:
   - Format: Korean pattern name with underscores
   - Example: `슬라이딩_윈도우.md`, `투_포인터.md`

### Step 3: Select Appropriate Template

**Template Selection Logic**: Automatically choose the best template based on the content type:

1. **visualization.md** - Use when the topic involves:
   - Graphs, trees, or complex data structures
   - Step-by-step visual progression
   - Keywords: "그래프", "트리", "탐색", "DFS", "BFS", "최단경로"

2. **mathematical.md** - Use when the topic requires:
   - Mathematical proofs or recurrence relations
   - Dynamic programming formulations
   - Complexity analysis with formal proofs
   - Keywords: "DP", "동적계획법", "조합", "증명", "점화식", "복잡도 분석"

3. **implementation.md** - Use when the topic focuses on:
   - Data structure implementation details
   - Class design and methods
   - Internal mechanics
   - Keywords: "구현", "자료구조", "힙", "세그먼트 트리", "Union-Find", "클래스"

4. **basic_pattern.md** - Use as default for:
   - Simple algorithmic patterns
   - Text-heavy concept explanations
   - Techniques without heavy visualization or math
   - Keywords: "슬라이딩 윈도우", "투 포인터", "그리디", "패턴"

**Decision Process**:
```
IF keywords match visualization criteria:
    → Use visualization.md

ELSE IF keywords match mathematical criteria:
    → Use mathematical.md

ELSE IF keywords match implementation criteria:
    → Use implementation.md

ELSE:
    → Use basic_pattern.md (default)
```

### Step 4: Generate Learning Material

1. **Read the selected template**: Load the appropriate template from `assets/`

2. **Create the learning document** at `_learning/[패턴명].md`

3. **Fill in the content** based on the template structure:
   - Use clear, educational Korean explanations
   - Include practical Python code examples
   - Reference real coding test problems
   - Add complexity analysis
   - Follow the template's specific sections

### Step 5: Update README.md

1. **Locate the section**: Find "## 고민 없이 풀는 방법은 없을까?" in the main README.md

2. **Add the link** following existing pattern:
   ```markdown
   ## 고민 없이 풀는 방법은 없을까?

   - [변수 및 함수 작명법](NAMING.md)
   - [문제 풀이 방법](SOLVING.md)
   - [슬라이딩 윈도우 패턴](_learning/슬라이딩_윈도우.md)
   ```

3. **Maintain alphabetical or logical ordering** if preferred

### Step 6: Confirm Completion

Inform the user:
- Location of the created file
- What was added to README.md
- Suggest reviewing and customizing the content as needed

## Resources

This skill provides **4 specialized templates** for different types of learning content. Choose the appropriate template based on the topic's characteristics.

### assets/basic_pattern.md

**Purpose**: Default template for simple algorithmic patterns and techniques

**Best for**:
- Sliding window, two pointers, greedy algorithms
- Text-focused concept explanations
- Simple problem-solving patterns

**Structure**:
- Concept explanation
- Step-by-step approach
- Python code examples
- Complexity analysis
- Related problems
- Learning tips

### assets/visualization.md

**Purpose**: Template emphasizing visual learning with diagrams and step-by-step illustrations

**Best for**:
- Graph algorithms (DFS, BFS, shortest paths)
- Tree structures and traversals
- Complex data structures requiring visualization
- Algorithms with clear state changes

**Special features**:
- Mermaid diagrams
- ASCII art visualizations
- Step-by-step execution tables
- Flowcharts
- Hand-drawing practice checklists

### assets/mathematical.md

**Purpose**: Template focused on mathematical formulations and proofs

**Best for**:
- Dynamic programming with recurrence relations
- Combinatorics and number theory
- Algorithms requiring mathematical proof
- Complexity analysis with formal proofs

**Special features**:
- Recurrence relation derivation
- Mathematical induction proofs
- Optimal substructure proofs
- Asymptotic notation analysis
- Formula-heavy explanations

### assets/implementation.md

**Purpose**: Template for detailed data structure implementation guides

**Best for**:
- Heap, segment tree, Union-Find
- Custom data structure implementations
- Class design and method explanations
- Internal mechanics and invariants

**Special features**:
- Complete class implementation
- Method-by-method breakdown
- Invariant conditions
- Helper method patterns
- Test code examples
- Optimization techniques

## Example Usage

### Example 1: Basic Pattern

**User request**: "슬라이딩 윈도우 패턴 학습 자료 만들어줘"

**Template selected**: `basic_pattern.md` (simple algorithmic pattern)

**Actions**:
1. Create `_learning/슬라이딩_윈도우.md` using basic_pattern.md
2. Fill in text-focused content:
   - Concept: Definition of sliding window pattern
   - Principle: How it works with examples
   - Code: Python implementation with comments
   - Complexity: O(N) time, O(1) space
   - Problems: Programmers/Baekjoon recommendations
3. Update README.md with link
4. Confirm: "✅ Created at `_learning/슬라이딩_윈도우.md` using basic pattern template"

### Example 2: Visualization Template

**User request**: "그래프 DFS 알고리즘 학습 자료"

**Template selected**: `visualization.md` (requires visual diagrams)

**Actions**:
1. Create `_learning/그래프_DFS.md` using visualization.md
2. Fill in visualization-rich content:
   - Mermaid graph diagrams
   - Step-by-step execution tables
   - ASCII art for graph states
   - Hand-drawing practice checklist
3. Update README.md
4. Confirm: "✅ Created with Mermaid diagrams at `_learning/그래프_DFS.md`"

### Example 3: Mathematical Template

**User request**: "동적 계획법 원리 정리해줘"

**Template selected**: `mathematical.md` (DP recurrence relations)

**Actions**:
1. Create `_learning/동적_계획법.md` using mathematical.md
2. Fill in math-heavy content:
   - Recurrence relation derivation
   - Mathematical induction proof
   - Optimal substructure proof
   - Complexity analysis with proofs
3. Update README.md
4. Confirm: "✅ Created with mathematical proofs at `_learning/동적_계획법.md`"

### Example 4: Implementation Template

**User request**: "힙 자료구조 구현 방법 설명"

**Template selected**: `implementation.md` (data structure implementation)

**Actions**:
1. Create `_learning/힙_구현.md` using implementation.md
2. Fill in implementation-focused content:
   - Complete class implementation
   - Method-by-method breakdown
   - Invariant conditions
   - Test code examples
3. Update README.md
4. Confirm: "✅ Created with complete implementation at `_learning/힙_구현.md`"

## Notes

- All learning materials use Korean for explanations to match the project's documentation language
- Code examples should always be in Python as per project standards
- Maintain consistency with existing project structure and naming conventions
- Learning materials are separate from problem solutions - they focus on teaching concepts, not solving specific problems
