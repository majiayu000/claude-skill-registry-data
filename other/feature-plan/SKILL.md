---
name: feature-plan
description: >
  Planning and requirements definition for large-scale feature additions, generating step-by-step
  structured markdown files. Use for feature development spanning multiple domains (frontend, backend,
  infra) or when planning multiple features simultaneously. Triggered explicitly by the user with
  /feature-plan.
---

# Feature Plan

Planning skill for large-scale feature additions in the AI Reception project.
Outputs structured markdown files covering development plans that span multiple domains and features.

## Interaction Style

This skill uses an interactive selection-based approach throughout all steps. Every decision point uses `AskUserQuestion` to present choices to the user, making the planning process guided and efficient.

### Selection Rules

These rules apply to every question asked throughout the entire process:

1. **Always present 8+ choices per topic** — Split into multiple questions (up to 4 questions per call, up to 4 options each) to cover the topic comprehensively. Each question should explore a different facet of the same topic.
2. **Always use `multiSelect: true`** — Users often need to select multiple applicable options. Every question must allow multiple selections.
3. **Free-text is always available** — The `AskUserQuestion` tool automatically provides an "Other" option for free input. Remind users of this in the first question of each step.
4. **Navigation option** — The last question in each step must include a "Back: Redo previous step" option so the user can return and revise earlier answers. When the user selects this, re-present the previous step's questions with their prior answers noted.

### Comparison & Recommendation Rules

When presenting choices that involve trade-offs (technical approaches, libraries, architectural patterns, etc.), each option must include comparison context so the user can make informed decisions without needing to research independently.

1. **Attach comparison axes to each option** — Include concise pros and cons directly in the option description. Format: `Option Name — ✅ merit1, merit2 / ⚠️ demerit1, demerit2`. Keep each axis to a few words; the goal is quick scanning, not exhaustive analysis.
2. **Mark the recommended option** — Prepend `⭐推薦:` to the option you recommend based on your research findings and the project's context. There should be exactly one recommendation per question (when trade-offs exist). If multiple options are equally viable, pick the one with the lowest risk for the project.
3. **State the recommendation rationale** — After the options, add a one-line note explaining why the recommendation fits this project. Reference specific codebase findings or research results (e.g., "既存のWebSocket実装との整合性が高いため" or "メンテナンスコストと学習曲線のバランスから").
4. **When comparison doesn't apply** — For factual/preference questions without trade-offs (e.g., "Who are the target users?"), skip the pros/cons format. Use your judgment — the rule applies when the user is choosing between competing approaches, not when listing requirements.

Example of a well-formed option:
```
⭐推薦: WebSocket拡張 — ✅ 既存接続を再利用、リアルタイム対応 / ⚠️ プロトコル複雑化、デバッグ困難
REST API新設 — ✅ シンプル、テスト容易 / ⚠️ ポーリング必要、リアルタイム性低い
GraphQL導入 — ✅ 柔軟なクエリ、型安全 / ⚠️ 学習コスト高、既存と異なるパラダイム
Server-Sent Events — ✅ 軽量、HTTP互換 / ⚠️ 双方向通信不可、ブラウザ制限あり

💡 推薦理由: 既存のWebSocketインフラを活かせるため、追加の運用コストを最小化できる
```

### Answer Tracking

Maintain an internal record of all user selections across steps. When the user goes back to revise a previous step:
- Re-present that step's questions, noting which options were previously selected
- After the user revises, re-evaluate all subsequent steps that depend on the changed answers
- If a completed document (e.g., 00-requirements.md) is affected by the revision, update it before proceeding

## Process

Follow these 7 steps in order. The key design principle: research the codebase and external sources first, then use those findings to drive informed questions during the hearing step. This produces higher-quality choices because options are grounded in what actually exists in the code and what's technically feasible.

### Step 1: Codebase Research

Based on the user's feature overview, immediately dive into the existing codebase to understand the current state. This step runs without user interaction — just analyze and document.

#### 1a. Deep Codebase Analysis

Go beyond surface-level file listing. For each area relevant to the user's feature description:

- **Read the actual source code** — not just file names, but the implementation details. Trace the data flow from endpoint to database and back.
- **Identify patterns and conventions** — How are similar concerns handled? What base classes, utilities, or abstractions exist that should be reused?
- **Map function signatures and interfaces** — Document the exact method signatures, parameter types, and return types that the new feature will interact with.
- **Note coupling and side effects** — What will break or need adjustment when this code changes? Are there implicit dependencies?
- **Check test coverage** — What tests exist for the affected areas? What test patterns are used?

Example depth: instead of "SummaryManager handles summaries", write "SummaryManager.list_user_summaries() queries DynamoDB via GSI `user_id-created_at-index`, returns list[SummaryItem], paginated with LastEvaluatedKey. Currently no bulk export method exists. DynamoDBClient.query() at line 45 lacks pagination support — this is a gap for large result sets."

#### 1b. Technical Constraint Discovery

- Performance limits, rate limits, compatibility issues
- Infrastructure constraints (memory, storage, network)
- Existing functionality that partially covers the requested feature

After analysis, present a brief summary of key findings to the user, then ask for confirmation before proceeding:

**Codebase Findings Questions:**

| Question | Header | Example Options |
|----------|--------|----------------|
| Which of these existing components should we build on? | Reuse | [Present 4 relevant existing components found in codebase] |
| Which technical constraints are most important to address? | Constraints | [Present 4 constraints discovered during analysis] |
| Are there additional codebase areas I should investigate? | More Areas | [Present 4 potentially related areas + "No, this is sufficient"] |
| Should we proceed to external research? | Next Step | Proceed to Web research / Investigate more code areas / Back: Provide more context about the feature |

Output as `docs/plans/<feature-name>/00-codebase-research.md`:

```markdown
# <Feature Name> — Codebase Research

## Deep Codebase Analysis

### <Area 1>
- **Files analyzed**: (list with line numbers for key sections)
- **Current implementation**: (detailed description of how it works)
- **Key interfaces**: (method signatures, types, data flow)
- **Patterns used**: (design patterns, conventions)
- **Coupling & side effects**: (what depends on this, what breaks if changed)
- **Test coverage**: (existing tests, patterns used)
- **Gaps identified**: (missing functionality, limitations)

### <Area 2>
...

## Technical Constraints
- ...

## Key Findings Summary
- Findings that directly impact the feature design
- Existing functionality that can be reused
- Gaps that need to be filled
```

Research quality standards:
- Codebase analysis must be based on actually reading source files. Cite specific files, line numbers, and function names — not speculation.

### Step 2: Web Technical Research

Conduct external research to complement the codebase findings. This step also runs proactively, then validates findings with the user.

#### 2a. Official Documentation & External Research

Use WebSearch and WebFetch to research:

- **Official documentation** of libraries, APIs, and services that the feature will use or integrate with
- **Best practices and recommended patterns** from framework/library maintainers
- **Known limitations, gotchas, and migration guides** that could affect implementation
- **Changelog and version compatibility** — ensure the approach works with the project's dependency versions

#### 2b. Similar OSS Project Analysis

Search GitHub and the web for open-source projects that have implemented similar features. This provides battle-tested patterns and helps avoid known pitfalls.

- **Find 2-3 relevant repositories** — Look for projects with similar tech stack or problem domain
- **Analyze their approach** — How did they structure the feature? What design decisions did they make and why?
- **Extract reusable patterns** — Identify architectural patterns, data models, or UX flows that could be adapted
- **Note their mistakes** — Check their issue trackers for post-launch bugs or regrets related to this feature

#### 2c. Library/Service Selection

When new dependencies are needed:
- Research candidates with pros, cons, and project compatibility
- Check maintenance status, download counts, bundle size, license

#### 2d. API/Protocol Verification

For external integrations:
- Verify API specs, rate limits, authentication requirements
- Check data formats, WebSocket protocols, webhook schemas

**After research, present key findings as choices for the user to validate:**

| Question | Header | Example Options |
|----------|--------|----------------|
| Which architectural approach looks most promising? | Approach | [Present 4 approaches with ✅/⚠️ comparison axes + ⭐推薦 mark on recommended one, followed by 💡 推薦理由] |
| Which libraries should we consider? | Libraries | [Present 4 candidates with ✅/⚠️ comparison axes + ⭐推薦 mark, followed by 💡 推薦理由] |
| Which OSS patterns are worth referencing? | Patterns | [Present 4 patterns from analyzed projects with applicability notes] |
| Should we proceed to the hearing step? | Next Step | Proceed to hearing / Research more topics / Back: Redo Step 1 |

Output as `docs/plans/<feature-name>/01-web-research.md`:

```markdown
# <Feature Name> — Web Technical Research

## Official Documentation
- (Key findings from official docs with source links)

## Similar OSS Projects
#### <Project 1> — [repository URL]
- **Relevance**: (why this project is comparable)
- **Approach**: (how they implemented the similar feature)
- **Reusable patterns**: (what we can learn/adapt)
- **Pitfalls found**: (issues from their tracker, lessons learned)

#### <Project 2> — [repository URL]
...

### Pattern Comparison
| Aspect | Our Project | OSS Project 1 | OSS Project 2 | Recommendation |
|--------|-------------|----------------|----------------|----------------|
| ...    | ...         | ...            | ...            | ...            |

## Library/Service Selection
### <Selection Target>
| Candidate | Pros | Cons | Maintenance | Recommendation |
|-----------|------|------|-------------|----------------|
| A         | ...  | ...  | ...         | ...            |

## API/Protocol Research
- ...

## Research Summary
- Key findings that impact design
- Patterns adopted from external research (with rationale)
- Recommended approach and rationale
```

Research quality standards:
- External research should include source URLs. Use WebSearch and WebFetch to verify claims.
- OSS project analysis should reference specific repositories and explain why their approach is or isn't suitable for this project.

### Step 3: Hearing — Feature Details

Now that both codebase and web research are complete, conduct the hearing step. The research findings allow presenting much more informed and specific choices to the user — options are grounded in what actually exists in the code and what external research suggests.

Present questions organized by the following perspectives. Ask one round of `AskUserQuestion` (up to 4 questions), then follow up with additional rounds as needed based on answers. The first question should mention: "各質問で「Other」を選ぶと自由記述も可能です。"

**Round 1: Purpose & Scope (informed by research)**

| Question | Header | Example Options |
|----------|--------|----------------|
| What is the primary purpose of this feature? | Purpose | [Present 4 options informed by what's feasible given codebase state] |
| Who are the target users? | Users | End users / Administrators / Internal team / External partners |
| What is the scope for this iteration? | Scope | [Present 4 scope options informed by research — e.g., "MVP using existing X component" / "Full feature requiring new Y"] |
| What are the main constraints? | Constraints | [Present 4 constraints, including ones discovered during research] |

**Round 2: Technical Decisions (informed by research)**

| Question | Header | Example Options |
|----------|--------|----------------|
| Which technical approach should we take? | Approach | [Present 4 approaches with ✅/⚠️ comparison axes + ⭐推薦 mark, followed by 💡 推薦理由] |
| What non-functional requirements are important? | NFR | Performance / Security / Availability / Scalability |
| Which existing components should we extend vs. build new? | Build/Extend | [Present 4 options based on codebase findings] |
| Are you ready to proceed to requirements? | Navigation | Proceed to requirements / Ask more questions / Back: Redo Step 2 |

### Step 4: Requirements Definition

Present the drafted requirements as selection choices for the user to validate and refine. Requirements should reflect insights from the research steps.

**Validation Questions:**

| Question | Header | Example Options |
|----------|--------|----------------|
| Which user stories are highest priority? | Priority | [Present 4 drafted user stories for ranking] |
| Which functional requirements should we include? | Features | [Present 4 key functional requirements] |
| Which non-functional aspects need explicit targets? | NFR Targets | Response time SLA / Concurrent user limit / Data retention policy / Uptime target |
| Are these out-of-scope items correct? | Out of Scope | [Present 4 items identified as out of scope + "Back: Redo Step 3"] |

After confirmation, output `docs/plans/<feature-name>/02-requirements.md`:

```markdown
# <Feature Name> — Requirements Definition

## Background and Purpose
(Why are we building this)

## User Stories
- As a [who], I want [what], so that [why]
(List main stories)

## Functional Requirements
1. ...
2. ...

## Non-Functional Requirements
- Performance: ...
- Security: ...
- Availability: ...

## Out of Scope
- Items excluded from this iteration

## Glossary
(Project-specific terms if any)
```

### Step 5: Architecture Design

Present architecture decisions as selections before writing the document.

**Architecture Decision Questions:**

| Question | Header | Example Options |
|----------|--------|----------------|
| Frontend: Which UI approach fits best? | Frontend | [Present 4 UI approaches with ✅/⚠️ comparison axes + ⭐推薦 mark, followed by 💡 推薦理由. e.g., `⭐推薦: 新規ページ — ✅ 独立性高い、ルーティング明確 / ⚠️ 実装コスト大`] |
| Backend: How should we structure the API? | Backend | [Present 4 API approaches with ✅/⚠️ comparison axes + ⭐推薦 mark, followed by 💡 推薦理由] |
| Data: What data model changes are needed? | Data Model | [Present 4 data approaches with ✅/⚠️ comparison axes + ⭐推薦 mark, followed by 💡 推薦理由] |
| Infrastructure: What AWS resources are needed? | Infra | [Present 4 infra options with ✅/⚠️ comparison axes + ⭐推薦 mark, followed by 💡 推薦理由 + Back: Redo Step 4] |

Output as `docs/plans/<feature-name>/03-architecture.md`:

Build on the existing project architecture (see CLAUDE.md) and include:

- **Overall diagram**: Text-based diagram showing component relationships
- **Frontend design**: New pages, components, hooks, state management
- **Backend design**: Endpoints, domain models, use cases
- **Data model**: Table/schema changes, data flow
- **Infrastructure changes**: AWS resources, Terraform changes (if applicable)
- **External integrations**: Newly required APIs or services

Follow the existing folder structure and explicitly state which files go in which directories.

### Step 6: Implementation Step Breakdown

Present task organization choices before detailing the breakdown.

**Implementation Planning Questions:**

| Question | Header | Example Options |
|----------|--------|----------------|
| What should be the implementation order priority? | Priority | [Present 4 ordering strategies with ✅/⚠️ comparison axes + ⭐推薦 mark, followed by 💡 推薦理由. e.g., `⭐推薦: Backend-first — ✅ API契約が先に確定、フロントが安定 / ⚠️ UI確認が後回し`] |
| How granular should the steps be? | Granularity | [Present 4 granularity levels with ✅/⚠️ comparison axes + ⭐推薦 mark, followed by 💡 推薦理由] |
| Which tasks can be parallelized? | Parallel | [Present 4 candidate parallel workstreams from architecture] |
| How should we handle cross-cutting concerns? | Cross-cut | [Present 4 strategies with ✅/⚠️ comparison axes + ⭐推薦 mark, followed by 💡 推薦理由 + Back: Redo Step 5] |

Output as `docs/plans/<feature-name>/04-steps.md`:

Each task should include:

```markdown
## Step N: <Task Name>

**Target**: backend / frontend / infra / cross-cutting
**Dependencies**: Step X, Step Y (or "None")

### Overview
(What this task achieves, 1-2 sentences)

### Work Items
- [ ] Specific work item 1
- [ ] Specific work item 2
- ...

### Target Files (Expected)
- `backend/src/domain/...`
- `frontend/src/components/...`

### Acceptance Criteria
- ... (Conditions for this task to be considered "done")
```

Breakdown guidelines:
- 1 task = 1 technical concern (endpoint addition, component creation, DB schema change, etc.)
- Clearly identify dependencies and tasks that can be parallelized
- When spanning multiple domains, split tasks by domain

### Step 7: Risk, Dependencies, and Test Strategy

Combine risk analysis and test strategy into a final validation step.

**Risk Assessment Questions:**

| Question | Header | Example Options |
|----------|--------|----------------|
| Which risks concern you most? | Top Risks | [Present 4 identified risks with impact/probability assessment] |
| What mitigation strategies do you prefer? | Mitigation | [Present 4 strategies with ✅/⚠️ comparison axes + ⭐推薦 mark, followed by 💡 推薦理由. e.g., `⭐推薦: Feature flag rollout — ✅ 段階的リリース、即時ロールバック可能 / ⚠️ フラグ管理の複雑化`] |
| Which test types should we emphasize? | Test Types | [Present 4 testing strategies with ✅/⚠️ comparison axes + ⭐推薦 mark, followed by 💡 推薦理由] |
| What coverage target is appropriate? | Coverage | [Present 4 coverage strategies with ✅/⚠️ comparison axes + ⭐推薦 mark, followed by 💡 推薦理由 + Back: Redo Step 6] |

Output as `docs/plans/<feature-name>/05-risks.md`:

```markdown
# Risks and Dependencies

## Risk List

| # | Risk | Impact | Probability | Mitigation |
|---|------|--------|-------------|------------|
| 1 | ...  | High/Med/Low | High/Med/Low | ... |

## External Dependencies
- (External services, libraries, other team work, etc.)

## Technical Debt
- (Potential debt introduced by this implementation)

## Open Items
- (Decisions needed but not yet made)
```

Output as `docs/plans/<feature-name>/06-testing.md`:

```markdown
# Test Strategy

## Testing Approach
(Overall approach)

## Unit Tests
- Backend: pytest (list of target modules)
- Frontend: Jest + Testing Library (list of target components)

## Integration Tests
- API tests (list of target endpoints)

## E2E Tests
- Playwright (list of target scenarios)

## Test Data
- (Required mock data, fixtures)

## Coverage Targets
- Unit: XX%
- E2E: XX main flow scenarios
```

## Output Structure

The following files are generated:

```
docs/plans/<feature-name>/
├── 00-codebase-research.md  # Codebase analysis
├── 01-web-research.md       # External technical research
├── 02-requirements.md       # Requirements definition
├── 03-architecture.md       # Architecture design
├── 04-steps.md              # Implementation steps
├── 05-risks.md              # Risks and dependencies
└── 06-testing.md            # Test strategy
```

`<feature-name>` should be a kebab-case name that concisely represents the feature (e.g., `realtime-notification`, `multi-agent-handoff`).

## Important Notes

- Every decision point uses `AskUserQuestion` with `multiSelect: true`. Always present 8+ choices per topic by splitting into multiple questions.
- The first question in Step 3 (Hearing) should mention: "各質問で「Other」を選ぶと自由記述も可能です。"
- Each step's final question includes a "Back" option to return to the previous step. When the user selects "Back", re-present the previous step's questions.
- When the user revises a previous step, update any already-generated documents that depend on the changed answers before moving forward.
- Read the existing codebase and ensure the design is consistent with the current implementation.
- Follow the folder structure, technology stack, and glossary in CLAUDE.md.
- Implementation steps should be granular enough for Claude to execute one at a time later.
- When multiple features are involved, explicitly state cross-feature dependencies in 04-steps.md.

## Output Language

All documents must be written in Japanese.
