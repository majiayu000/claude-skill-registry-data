---
name: spec-based-web-dev
description: Systematic web development workflow from PRD to implementation plan. Generates database schemas, detailed use cases with sequence diagrams, page requirements with state management design (Context + useReducer), and modular implementation plans. Use when building web applications following spec-driven development methodology with PostgreSQL and React.
---

# Spec-Based Web Development

Structured workflow for translating specifications into implementation-ready plans.

## Workflow Overview

The development process follows a sequential workflow with built-in review cycles:

1. **Database Schema** - Design minimal database structure from PRD and user flow
   - → **Review & Approval** - User validates schema before proceeding
2. **Use Cases** - Document detailed specifications for each feature with sequence diagrams
   - → **Review & Approval** - User validates use case before proceeding
   - → **Page Complexity Analysis** - Analyze pages and suggest state management needs
3. **State Management** - Design page-level state using Flux pattern with Context + useReducer
   - → **Review & Approval** - User validates state design before proceeding
4. **Implementation Plan** - Create modular implementation plans (feature-based or page-based)
   - → **Final Review** - User approves plan before implementation

Each phase builds upon previous outputs, creating a complete specification chain from requirements to code-ready plans. **User approval is required after each phase to ensure alignment before proceeding.**

## Phase 1: Database Schema

Generate minimal database schema and migration files.

**🤖 Recommended Agent: `database_writer`**

Use the Task tool to launch the database_writer agent for this phase:
```
Task(
  subagent_type="database_writer",
  description="Generate database schema",
  prompt="/docs/prd.md, /docs/userflow.md, 그리고 /docs/external/ 디렉토리의 모든 파일을 참조하여 데이터베이스 스키마를 설계하고 /docs/database.md와 migration SQL을 생성해주세요. 외부 서비스 연동이 필요한 경우 해당 데이터 요구사항도 스키마에 반영해주세요."
)
```

**Inputs:**
- `/docs/prd.md` - Product requirements document
- `/docs/userflow.md` - User flow documentation
- `/docs/external/[service].md` - External service integration specs (if exists)

**Process:**
1. Read all files in `/docs/external/` directory to identify external service requirements
2. Identify data entities explicitly mentioned in user flow
3. Create high-level data flow diagram (including external service data flows)
4. Design PostgreSQL schema with minimal fields
5. Consider external service data requirements when designing schema
6. Generate migration SQL

**Outputs:**
- `/docs/database.md` - Data flow + schema documentation
- `/supabase/migrations/*.sql` - Migration files

**Key Guidelines:**
- **MUST read all files in `/docs/external/` directory before designing schema**
- Include ONLY data explicitly in user flow or required by external services
- Consider external service data requirements (API responses, webhook payloads, etc.)
- Use PostgreSQL-specific features appropriately
- Present data flow before detailed schema (including external service interactions)
- Keep schema minimal for MVP

**Agent Benefits:**
- Specialized in database design from userflow
- Follows PostgreSQL best practices
- Generates idempotent migration files automatically

**Review & Approval:**

After completing this phase, present the generated files to the user with:

1. **Summary**: Brief overview of what was created
   - Number of tables designed
   - Key relationships identified
   - Migration files generated

2. **Review Questions**:
   - "Does the data flow diagram accurately represent your requirements?"
   - "Are there any missing entities or relationships?"
   - "Is the schema minimal enough for MVP, or should we simplify further?"

3. **Request Feedback**:
   - Ask: "Please review `/docs/database.md` and `/supabase/migrations/*.sql`. Any changes needed before proceeding to Use Cases?"
   - Wait for user approval or modification requests
   - If modifications needed, update files and repeat review

4. **Git Commit Proposal** (after user approval):
   - Suggest creating a commit with the following message:
     ```
     docs(database): add database schema and migration

     - Create database schema documentation
     - Add PostgreSQL migration file
     - Define N tables with relationships
     ```
   - Ask: "이 커밋을 생성할까요?"
   - If user approves, use Bash tool to create the commit
   - If user declines, skip and proceed to Phase 2

**Do not proceed to Phase 2 until user explicitly approves the review.**

## Phase 2: Use Cases

Create detailed use case specifications for individual features.

**🤖 Recommended Agent: `usecase-writer`**

Use the Task tool to launch the usecase-writer agent for each feature:
```
Task(
  subagent_type="usecase-writer",
  description="Write use case for feature N",
  prompt="/docs/userflow.md의 {N}번 기능에 대한 상세 유스케이스를 작성하고 /docs/00N/spec.md에 저장해주세요. Hono Backend Guide를 참고하여 API 명세도 포함해주세요."
)
```

**Inputs:**
- `/docs/userflow.md` - Identifies features to document
- Feature number N from user flow
- `/docs/database.md` - Database schema (for data references)
- `/docs/external/[service].md` - External service integration specs (if exists)

**Process:**
1. Extract feature N from user flow
2. Check if external service integration is required (`/docs/external/[service].md`)
3. Document use case with standard structure
4. Create sequence diagram showing User → FE → BE → Database (and External Service if applicable) interactions
5. **[IMPORTANT]** Include Backend API specifications (see [Hono Backend Guide](references/hono-backend-guide.md))
6. **[IMPORTANT]** Include External Service integration details if `/docs/external/[service].md` exists

**Output:**
- `/docs/00N/spec.md` - Use case specification

**Required Sections:**
- Primary Actor
- Precondition (user perspective only)
- Trigger
- Main Scenario (numbered steps)
- Edge Cases (error handling)
- Business Rules
  - **API Specification**: Endpoint, Request/Response schemas, Error codes
  - **Database Operations**: Tables, operations (INSERT/SELECT/UPDATE/DELETE)
  - **External Service Integration**: Service name, purpose, API calls (if `/docs/external/[service].md` exists)
- Sequence Diagram (PlantUML format, no separators)

**Diagram Guidelines:**
- Use standard PlantUML syntax
- **Subdivide BE layer**: Hono Router (route.ts) and Service (service.ts)
- **Include External Service participant**: If external service is used, add as a separate participant (e.g., "Payment Gateway", "Email Service")
- Show validation, transformation, and error handling flows
- No custom separators or non-standard markup
- Show complete interaction flow including external service calls

**For Hono + Supabase projects**: See detailed guidance in [Hono Backend Guide](references/hono-backend-guide.md#phase-2-use-cases)

**Agent Benefits:**
- Automatically reads PRD, userflow, and database schema
- Creates PlantUML sequence diagrams with correct syntax
- Includes API specifications (endpoints, schemas, error codes)
- Follows use case writing best practices
- Numbers use cases appropriately (001, 002, etc.)

**Review & Approval:**

After completing this phase, present the use case document to the user with:

1. **Summary**: Quick overview of the use case
   - Feature being documented
   - Number of main scenario steps
   - Number of edge cases covered
   - API endpoints defined (if applicable)

2. **Key Highlights**:
   - Primary actor and trigger
   - Critical business rules
   - Important edge cases

3. **Visual Check**:
   - Share the PlantUML sequence diagram (suggest rendering at plantuml.com)
   - Ask: "Does this flow match your expectations?"

4. **Review Questions**:
   - "Is the main scenario complete and accurate?"
   - "Are there any missing edge cases or error scenarios?"
   - "Do the business rules align with your requirements?"
   - "Is the API specification clear?" (for Hono projects)

5. **Request Feedback**:
   - Ask: "Please review `/docs/00N/spec.md`. Any changes needed before proceeding to the next use case or State Management?"
   - Wait for user approval or modification requests
   - If modifications needed, update the document and repeat review

6. **Git Commit Proposal** (after user approval):
   - Suggest creating a commit with the following message:
     ```
     docs(usecase): add use case specification for feature N

     - Document main scenario with X steps
     - Add Y edge cases for error handling
     - Include API specification (endpoints, schemas, error codes)
     - Create sequence diagram for user flow
     ```
   - Ask: "이 커밋을 생성할까요?"
   - If user approves, use Bash tool to create the commit
   - If user declines, skip and proceed to next use case or Phase 2.5

**Do not proceed to the next use case or Phase 2.5 until user explicitly approves the review.**

---

## Phase 2.5: Page Complexity Analysis

**Trigger**: After all Use Cases are completed and approved

Analyze all use cases to identify pages requiring state management and suggest appropriate complexity levels.

**Purpose:**
- Identify which pages need state management
- Determine complexity level for each page
- Suggest state management depth (Level 1-3)
- Prioritize pages for Phase 3 work

**Process:**

1. **Extract Pages from Use Cases**
   - Read all `/docs/00N/spec.md` files
   - Identify all unique pages mentioned
   - List pages with their associated use cases

2. **Calculate Complexity Score**

   For each page, score across four dimensions (see [page-complexity-analysis.md](references/page-complexity-analysis.md)):

   - **State Complexity** (1-5+ points)
     - Number of data types to manage
     - Server data, form state, UI state, filters, etc.

   - **Interaction Complexity** (1-5+ points)
     - Number of user actions
     - CRUD operations, filtering, sorting, pagination

   - **Component Hierarchy** (1-4+ points)
     - Component depth
     - Number of siblings sharing state

   - **Data Flow Complexity** (1-5+ points)
     - Data sources (API, localStorage, URL params)
     - Data transformations (filter, sort, aggregate)

3. **Determine Management Level**

   Based on total score:

   | Total Score | Level | Recommendation |
   |-------------|-------|----------------|
   | 0-5 | Low | No state management needed |
   | 6-10 | Medium | **Level 1**: Basic state definition only |
   | 11-15 | High | **Level 2**: Flux pattern (Action/Reducer/View) |
   | 16+ | Very High | **Level 3**: Full Context + useReducer |

4. **Suggest Priority Order**
   - Rank pages by complexity (highest first)
   - Consider business criticality
   - Recommend which pages to work on in Phase 3

**Output Format:**

Present analysis to user with:

```markdown
📊 **페이지 복잡도 분석 완료**

모든 Use Case를 분석한 결과:

## 분석 결과 테이블

| 페이지 | 점수 | 레벨 | 작업 범위 |
|--------|------|------|-----------|
| 결제 페이지 | 18 | Very High | ⭐⭐⭐ Level 3 (Context + useReducer) |
| 장바구니 | 15 | High | ⭐⭐ Level 2 (Flux 패턴) |
| 상품 목록 | 12 | High | ⭐⭐ Level 2 (Flux 패턴) |
| 상품 상세 | 6 | Medium | ⭐ Level 1 (기본 상태만) |
| 회사 소개 | 2 | Low | ❌ 작업 불필요 |

## 각 페이지 상세 분석

### 1. 결제 페이지 (18점, Very High)
**복잡도 구성:**
- 상태: 6점 (결제 정보, 배송 정보, 쿠폰, UI 상태)
- 상호작용: 5점 (여러 폼, 검증, API 호출)
- 계층: 4점 (5단계 이상 깊이)
- 데이터 흐름: 3점 (API + localStorage + 복잡한 계산)

**제안 수준: Level 3**
- ✅ Requirement.md
- ✅ State Management.md (전체)
  - 상태 정의
  - Flux 패턴
  - Context 설계

**이유:**
여러 하위 컴포넌트가 결제 상태를 공유해야 하므로 Context 필수

[... 다른 페이지들 ...]

## 권장 작업 순서

1. **결제 페이지** (18점) → Level 3
2. **장바구니** (15점) → Level 2
3. **상품 목록** (12점) → Level 2
4. **(선택) 상품 상세** (6점) → Level 1

## 다음 단계 선택

어떻게 진행하시겠습니까?

1. "결제 페이지부터 시작" → 해당 페이지 Level 3 작업
2. "순서대로 모두 진행" → 1번부터 순차 작업
3. "[페이지명] 먼저" → 지정 페이지 작업
4. "분석만 확인" → Phase 3 건너뛰고 Phase 4로
```

**Level별 작업 범위:**

- **Level 1** (Medium, 6-10점):
  - `/docs/pages/[pagename]/requirement.md` 작성
  - 상태 정의 + 상태 전환 테이블만
  - Flux/Context 없음

- **Level 2** (High, 11-15점):
  - `/docs/pages/[pagename]/requirement.md` 작성
  - `/docs/pages/[pagename]/state_management.md` 작성 (부분)
  - 상태 정의 + Flux 패턴 (Action/Reducer/View)
  - Context 설계 없음 (useReducer만)

- **Level 3** (Very High, 16+점):
  - `/docs/pages/[pagename]/requirement.md` 작성
  - `/docs/pages/[pagename]/state_management.md` 작성 (전체)
  - 상태 정의 + Flux 패턴 + Context 설계

**User Decision:**

Wait for user to select:
- Which page(s) to work on
- Whether to proceed with all suggestions
- Whether to skip Phase 3 entirely

**Important:**
- Do not proceed to Phase 3 without user's decision
- If user skips Phase 3, go directly to Phase 4
- If user selects specific pages, only work on those

For detailed scoring criteria, see [Page Complexity Analysis Guide](references/page-complexity-analysis.md).

---

## Phase 3: State Management

Design page-level state management with Flux pattern.

**🤖 Recommended Agent: `status_management_writer`**

Use the Task tool to launch the status_management_writer agent for selected pages:
```
Task(
  subagent_type="status_management_writer",
  description="Design state management for [pagename]",
  prompt="[pagename] 페이지에 대한 상태 관리 문서를 작성해주세요. Level {N} 수준으로 작성하며, requirement.md와 state_management.md를 생성해주세요."
)
```

**Note**: Based on Phase 2.5 analysis, only work on pages that require state management (Level 1-3).

**Inputs:**
- `/docs/prd.md`
- `/docs/userflow.md`
- `/docs/usecases/**` - Related use cases
- Page name
- Complexity Level (from Phase 2.5 analysis)

**Process:**
1. Create page requirements document
2. Define state data vs derived/display data
3. Apply Flux pattern (Action → Store → View)
4. Design Context + useReducer implementation
5. Document exposed interface for child components

**Outputs:**
- `/docs/pages/[pagename]/requirement.md` - Requirements and data flow
- `/docs/pages/[pagename]/state_management.md` - State design

**State Management Structure:**
1. **State Data Identification**
   - List managed state
   - List derived/display-only data

2. **State Transition Table**
   - Change conditions
   - UI updates per state change

3. **Flux Pattern Design**
   - Actions (user-triggered events)
   - Store (state updates via useReducer)
   - View (component rendering)

4. **Context Design**
   - Data loading flow visualization
   - Exposed variables and functions
   - Focus on interface design, not implementation details

**Implementation Standards:**
- Use useReducer for state management
- Follow industry best practices for Context API
- Include database interactions in requirements

**Agent Benefits:**
- Follows structured workflow (requirement → state definition → Flux → Context)
- Adheres to complexity level guidelines (Level 1/2/3)
- Creates both requirement.md and state_management.md automatically
- Ensures Flux pattern consistency (Action → Reducer → View)
- Designs Context interface with proper TypeScript types

**Review & Approval:**

After completing this phase, present the state management documents to the user with:

1. **Summary**: Overview of state design
   - Number of managed state variables
   - Number of derived/display-only data
   - Number of actions defined
   - Data loading sources (API, local storage, etc.)

2. **Key Design Decisions**:
   - State vs. Derived data separation rationale
   - Critical state transitions
   - Context interface highlights

3. **Validation Check**:
   - Confirm state is minimal (not over-engineered)
   - Verify action names are clear and consistent
   - Check reducer logic is understandable

4. **Review Questions**:
   - "Does the state structure match your mental model of the page?"
   - "Are the actions comprehensive enough to handle all user interactions?"
   - "Is the Context interface clear for other developers to use?"
   - "Should we simplify or expand any state management logic?"

5. **Request Feedback**:
   - Ask: "Please review `/docs/pages/[pagename]/requirement.md` and `/docs/pages/[pagename]/state_management.md`. Any changes needed before proceeding to Implementation Plan?"
   - Wait for user approval or modification requests
   - If modifications needed, update documents and repeat review

6. **Git Commit Proposal** (after user approval):
   - Suggest creating a commit with the following message:
     ```
     docs(state): add state management design for [pagename] page

     - Create page requirements documentation
     - Define N state variables and M derived data
     - Design Flux pattern with X actions
     - Implement Context API interface (Level N)
     ```
   - Ask: "이 커밋을 생성할까요?"
   - If user approves, use Bash tool to create the commit
   - If user declines, skip and proceed to next page or Phase 4

**Do not proceed to Phase 4 until user explicitly approves the review.**

## Phase 4: Implementation Plan

Create modular, implementation-ready plans.

### Feature-Based Plan

For implementing individual features from use cases.

**🤖 Recommended Agent: `caseplan-writer`**

Use the Task tool to launch the caseplan-writer agent:
```
Task(
  subagent_type="caseplan-writer",
  description="Create implementation plan for use case N",
  prompt="/docs/usecases/00N/spec.md의 유스케이스를 구현하기 위한 상세한 계획을 작성하고 /docs/usecases/00N/plan.md에 저장해주세요. Hono Backend Guide를 참고하여 backend 모듈도 포함해주세요."
)
```

**Inputs:**
- `/docs/usecases/00N/spec.md`
- `/docs/external/[service].md` - External service integration specs (if referenced in spec.md)
- Existing codebase (conventions, implemented features)
- `CLAUDE.md` - Codebase structure guidelines

**Process:**
1. Parse use case requirements
2. Check if external service integration is required (read `/docs/external/[service].md` if referenced)
3. Explore codebase for existing patterns and conventions
4. Design modular structure following AGENTS.md
5. Identify shared/generic modules
6. **[IMPORTANT]** Design backend modules (see [Hono Backend Guide](references/hono-backend-guide.md))
7. **[IMPORTANT]** Design external service integration layer if required

**Output:**
- `/docs/usecases/00N/plan.md`

**Plan Structure:**
- **Overview** - Module list with names, locations, descriptions
  - Include backend modules: schema.ts, error.ts, service.ts, route.ts
  - Include external service integration modules if needed (e.g., `lib/external/[service]-client.ts`)
- **Diagram** - Mermaid diagram showing module relationships
  - Show data flow from Route → Service → Supabase
  - Show external service integration flow if applicable
- **Implementation Plan** - Per-module details with:
  - Presentation layer: QA sheets
  - Business logic: Unit tests
  - **Backend layer**: Schema definitions, Service unit tests, Route QA sheets
  - **External Service layer**: Integration module, error handling, unit tests (if applicable)

**For Hono + Supabase projects**: See detailed module templates in [Hono Backend Guide](references/hono-backend-guide.md#backend-모듈-구현-템플릿)

**Agent Benefits:**
- Explores codebase to find existing patterns and conventions
- Identifies shared/generic modules automatically
- Follows CLAUDE.md structure guidelines strictly
- Includes backend modules (schema, error, service, route) for Hono projects
- **Integrates external service specs from `/docs/external/[service].md`**
- Generates Mermaid diagrams showing module relationships including external services
- Creates QA sheets for UI and unit test scenarios for logic

### Page-Based Plan

For implementing complete pages with all features.

**🤖 Recommended Agent: `pageplan-writer`**

Use the Task tool to launch the pageplan-writer agent:
```
Task(
  subagent_type="pageplan-writer",
  description="Create implementation plan for [pagename]",
  prompt="[pagename] 페이지의 구현 계획을 작성해주세요. 관련된 모든 use case와 state management 문서를 참고하여 /docs/pages/[pagename]/plan.md에 저장해주세요."
)
```

**Inputs:**
- All `/docs/*.md` files (direct children only)
- Related `/docs/usecases/*/spec.md` files
- `/docs/external/[service].md` - External service integration specs (if referenced in related use cases)
- `/docs/pages/[pagename]/state_management.md` (if exists)
- Existing codebase
- `CLAUDE.md`

**Process:**
1. Read all relevant documentation
2. Extract page requirements from related use cases
3. Check if external service integration is required (read `/docs/external/[service].md` if referenced)
4. Reference state management design if available
5. Explore codebase patterns
6. Design modular structure with shared components
7. Design external service integration layer if required

**Output:**
- `/docs/pages/[pagename]/plan.md`

**Plan Structure:** (Same as feature-based)

**Planning Guidelines:**
- Follow CLAUDE.md structure strictly
- Identify reusable shared modules
- Consider generic implementations
- Include QA sheets for UI components
- Include unit tests for business logic

**Agent Benefits:**
- Same as caseplan-writer, but optimized for page-level planning
- Reads all related use cases and state management documents
- Consolidates multiple features into cohesive page implementation
- Ensures consistency across related features

**Review & Approval:**

After completing this phase, present the implementation plan to the user with:

1. **Summary**: High-level overview
   - Total number of modules to implement
   - Module breakdown by category (Frontend, Backend, Shared)
   - Estimated implementation order
   - Key dependencies identified

2. **Key Architectural Decisions**:
   - Why certain modules were separated
   - Shared/generic modules identified for reuse
   - Critical dependencies and their rationale

3. **Visual Check**:
   - Share the Mermaid diagram (suggest rendering at mermaid.live)
   - Ask: "Does the module structure make sense?"

4. **Implementation Readiness**:
   - Confirm all modules have clear responsibilities
   - Verify QA sheets are comprehensive
   - Check unit test scenarios are actionable

5. **Review Questions**:
   - "Is the modular structure clear and logical?"
   - "Are there any modules that should be split or merged?"
   - "Do the QA sheets and unit tests provide enough guidance?"
   - "Are backend modules properly designed?" (for Hono projects)
   - "Can a developer start coding immediately with this plan?"

6. **Request Feedback**:
   - Ask: "Please review `/docs/usecases/00N/plan.md` or `/docs/pages/[pagename]/plan.md`. Any changes needed before starting implementation?"
   - Wait for user approval or modification requests
   - If modifications needed, update the plan and repeat review

7. **Final Checklist Reminder**:
   - Suggest: "You can use the validation checklist in [references/validation-checklist.md](references/validation-checklist.md) to ensure all items are covered."

8. **Git Commit Proposal** (after user approval):
   - Suggest creating a commit with the following message:
     ```
     docs(plan): add implementation plan for [feature/page]

     - Define N modules with clear responsibilities
     - Create module dependency diagram
     - Add QA sheets for UI components
     - Include unit test scenarios for business logic
     - Design backend modules (route, service, schema, error)
     ```
   - Ask: "이 커밋을 생성할까요?"
   - If user approves, use Bash tool to create the commit
   - If user declines, skip and proceed to implementation

**Do not proceed to implementation until user explicitly approves the plan.**

---

## Review Cycle Best Practices

### For Users:
- **Be specific**: Instead of "looks good", provide concrete feedback
- **Check completeness**: Use validation checklists as a guide
- **Think ahead**: Consider edge cases and future extensibility
- **Ask questions**: If anything is unclear, ask for clarification

### For AI Assistant:
- **Wait for approval**: Never proceed to next phase without explicit user confirmation
- **Accept iterations**: Be prepared to revise documents multiple times
- **Summarize changes**: When updating, clearly state what changed
- **Proactive suggestions**: If you notice potential issues, point them out during review

---

## Agent Usage Guidelines

### When to Use Agents

**✅ DO use agents for:**
- Phase 1: Database schema generation (database_writer)
- Phase 2: Use case documentation (usecase-writer)
- Phase 3: State management design (status_management_writer)
- Phase 4: Implementation planning (caseplan-writer / pageplan-writer)
- Implementation: Actual coding (implementer)

**❌ DON'T use agents for:**
- Phase 2.5: Page complexity analysis (manual analysis required)
- Review & Approval steps (user interaction required)
- Simple file edits or updates

### How to Launch Agents

Use the Task tool with the appropriate subagent_type:

```typescript
Task(
  subagent_type="<agent-name>",  // e.g., "database_writer"
  description="<short description>",  // e.g., "Generate database schema"
  prompt="<detailed task instructions>"  // What you want the agent to do
)
```

### Agent Handoff Pattern

Agents work sequentially, with each agent's output becoming input for the next:

```
database_writer → /docs/database.md
                  /supabase/migrations/*.sql
                       ↓
usecase-writer → /docs/usecases/00N/spec.md
                       ↓
[Page Analysis] → Complexity scores
                       ↓
status_management_writer → /docs/pages/[page]/requirement.md
                           /docs/pages/[page]/state_management.md
                       ↓
caseplan-writer/pageplan-writer → /docs/usecases/00N/plan.md
                                   /docs/pages/[page]/plan.md
                       ↓
implementer → Actual code implementation
```

### Agent Supervision

**Monitor agent progress:**
- Agents may take several minutes for complex tasks
- Check intermediate outputs if available
- Intervene if agent goes off-track

**After agent completes:**
- Review the generated files
- Use the Review & Approval prompts
- Request modifications if needed
- Only proceed to next phase after approval

### Troubleshooting Agents

**If agent fails:**
1. Check the prompt clarity
2. Ensure all required input files exist
3. Verify file paths are correct
4. Re-launch with more specific instructions

**If agent output is incomplete:**
1. Use the validation checklist
2. Point out missing items
3. Request agent to complete missing parts

**If agent deviates from guidelines:**
1. Reference the relevant guide (Hono Backend Guide, etc.)
2. Ask agent to revise following the guidelines

---

## Best Practices

**Documentation:**
- Write concisely for easy review
- Use consistent formatting across phases
- Include visual diagrams where helpful
- Keep specifications implementation-agnostic until plan phase

**Database:**
- Start minimal, expand as needed
- Document relationships clearly
- Use appropriate PostgreSQL types and constraints

**State Management:**
- Separate state from derived data
- Design clear action boundaries
- Keep reducer logic simple and testable
- Document data flow explicitly

**Implementation Plans:**
- Break into small, testable modules
- Consider reusability from the start
- Include acceptance criteria
- Reference architectural guidelines

## Reference Documentation

- **[workflow-examples.md](references/workflow-examples.md)** - Complete examples of each phase with real-world scenarios
- **[hono-backend-guide.md](references/hono-backend-guide.md)** - Hono + Supabase architecture guide for backend implementation
- **[page-complexity-analysis.md](references/page-complexity-analysis.md)** - Page complexity scoring criteria and state management level recommendations
- **[prompt-templates.md](references/prompt-templates.md)** - Copy-paste ready prompts for each phase, including review prompts
- **[review-guide.md](references/review-guide.md)** - Comprehensive guide for the review and approval process
