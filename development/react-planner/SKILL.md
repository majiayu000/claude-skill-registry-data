---
name: react-planner
description: "Plan React/Next.js features — component architecture, state management, data flow. Triggers: React plan, component design."
version: 0.1.0
---

## JTBD (Jobs To Be Done)

### Primary Job
When I need to build a React feature and do not want to invent the architecture while coding,
I want a concrete component and state plan,
so I can implement it without avoidable React bugs, rework, or performance surprises.

### Secondary Jobs
- When an existing React feature has architectural review findings, I want a fix plan, so I can address the right structural problems instead of patching symptoms.
- When a Next.js feature needs server/client boundaries and cache strategy, I want those decisions made up front, so I can avoid expensive reversals later.

### Job Layers
- Functional: Produce a React-specific implementation plan covering component structure, state ownership, hooks, performance, and boundaries.
- Emotional: Reduce the anxiety of hidden state bugs, stale closures, and architecture mistakes that surface late.
- Social: Helps the user look rigorous to reviewers and teammates by showing that the design was thought through before coding.

### This Skill Is For
- A user starting a non-trivial React, Next.js, or React Native feature and wanting to plan before implementation.
- A user who has multiple components, hooks, async flows, or performance-sensitive rendering to coordinate.
- A user turning review findings into a corrected React architecture.

### This Skill Is NOT For
- A user who already has code and wants a verdict on whether the implementation is correct; use `react-critic`.
- A user doing a trivial single-component change with no meaningful state or architectural decisions.

### Paired With
- `react-critic`: After implementation or at checkpoints, use it to verify that the built code matches the planned architecture.
- `writing-plans`: After the architecture is clear, use it to turn the design into task-level execution steps.

### Resolution Paths
| User's Situation | What Happens | What They Leave With |
|-----------------|-------------|----------------------|
| Starting a new feature | React Planner designs the architecture before code exists | An implementation-ready React plan |
| Refactoring a broken architecture | React Planner analyzes current structure and redesigns it | A fix-oriented architecture plan |
| Responding to `react-critic` findings | React Planner converts review failures into structural remediation | A corrected plan for the next iteration |

### When to Escalate
- If the user wants critique of existing code rather than planning, escalate to `react-critic`.
- If the problem is domain-agnostic sequencing rather than React architecture, escalate to a more general planning skill.

<Purpose>
React Planner is the design phase for React, Next.js, and React Native implementations. It produces architecture plans that have correct state ownership, appropriate memoization, and clear server/client boundaries built in from the start — not retrofitted as bugs.

The core insight: React's hardest bugs originate in the planning phase, not the coding phase. A developer who receives "implement the user settings panel" without a state plan will embed undocumented ownership assumptions, create waterfalls between components, and discover stale closure bugs during code review. A developer who receives a plan with the component tree, state ownership map, hook composition rules, and performance budget will build something verifiable and maintainable on the first try.

React Planner produces plans with:

1. **Component Architecture Diagram** — explicit hierarchy showing data flow (props down, events up) and parent-child relationships
2. **Component Responsibility Statements** — every component's job in one sentence (forces clarity)
3. **State Ownership Map** — which component owns which state, why, and where derived state lives (no guessing)
4. **Hook Composition Plan** — custom hooks specified with dependency arrays designed upfront, cleanup functions planned, memoization decisions justified
5. **Render Performance Budget** — re-render graph showing which components re-render on which state changes, where waterfalls exist, what's worth memoizing
6. **Server/Client Boundaries** (Next.js) — every component classified as server or client with rationale, server action strategy, cache/revalidation plan
7. **Error & Loading States** — Suspense boundaries, error boundaries, loading skeletons, optimistic updates, stale data handling
8. **Test Strategy** — per-component testing approach (React Testing Library, E2E), what to mock, accessibility requirements
9. **Implementation Tasks** — TDD rhythm with component signatures, hook stubs, test setup, and react-critic review checkpoints
10. **Failure Mode Analysis** — pre-mortem on common React mistakes specific to this architecture (stale closures, missing deps, waterfalls, RSC misclassification)

Works standalone with Claude Code. Designed to pair with react-critic: the planner designs for correctness, the critic verifies it at checkpoints.
</Purpose>

<Use_When>
- User is about to build a new feature with React/Next.js/React Native components
- User says "plan the UI for X", "design the component architecture", "how should we structure this state"
- User is starting a complex component that will involve multiple state sources or hooks
- User is building a Next.js feature and needs to plan RSC boundaries, server actions, and cache strategy
- User has a react-critic review with MAJOR findings and needs to plan architectural fixes
- User wants to redesign existing component architecture that has render performance or state management issues
- Code will touch multiple components, custom hooks, state management, or performance-sensitive rendering
- User is implementing a Next.js feature with server components, server actions, or client-side interactivity
</Use_When>

<Do_Not_Use_When>
- User wants to review existing code for architectural correctness — use react-critic instead
- User wants a general implementation plan with no React-specific component architecture — use writing-plans (obra/superpowers) instead
- User is implementing a trivial single-component utility with no state or hooks
- The code is just plain JavaScript with no React components
</Do_Not_Use_When>

<Why_This_Exists>
Most React bugs are design bugs. They originate before the first line of code is written:

- "Implement the settings panel" → Developer puts state in the wrong component, creates waterfalls between unrelated features. A plan with a state ownership map prevents this.
- "Add a custom hook for API calls" → Developer forgets useCallback on the dependency array, creates stale closures. A plan with dependency arrays designed upfront prevents this.
- "Build a Next.js dashboard" → Developer makes everything a client component out of fear, doubles JS bundle size. A plan with RSC classification and rationale prevents this.
- "Add caching to the product list" → Developer revalidates on every mutation, destroying cache benefits. A plan with explicit cache/revalidation strategy prevents this.

React Planner exists because the cheapest time to prevent a React bug is before the first component is written.
</Why_This_Exists>

<Companion_Skills>
The react-planner leverages external skills when installed. Check for and use these during planning:

**Design phase (always use if installed):**
- `brainstorming` (obra/superpowers): Explore component architecture options with Socratic dialogue before committing. 2-3 options with trade-offs. HARD GATE: no implementation until architecture approved.
- `writing-plans` (obra/superpowers): Convert the React design into bite-sized implementation tasks with exact file paths, component signatures, and test commands.

**Code understanding (use at start of any refactor/modification):**
- `code-archaeology` (flonat/claude-research): Understand existing component tree, state management patterns, hook usage before planning modifications.

**React reference companions (use when relevant):**
- `vercel-composition-patterns` (vercel-labs/agent-skills): Component API design, compound components, provider/state interfaces, and avoiding boolean-prop proliferation.
- `vercel-react-best-practices` (vercel-labs/agent-skills): Render waterfalls, bundle size, RSC serialization, memoization, and data-loading performance references.
- `vercel-react-native-skills` (vercel-labs/agent-skills): React Native/Expo lists, navigation, native UI, animation, and monorepo concerns. Use only when React Native/Expo is detected.

**Implementation (use during execution):**
- `test-driven-development` (obra/superpowers): TDD for React components. Test the component behavior BEFORE writing the component.
- `executing-plans` (obra/superpowers): Batch execution with human checkpoints.
- `subagent-driven-development` (obra/superpowers): Fresh subagent per task with two-stage review.

**Verification (use at checkpoints):**
- `react-critic` (react-critic): Run the 5-phase harsh code review at each checkpoint. Verify hooks, state ownership, render performance, and RSC boundaries.
- `verification-before-completion` (obra/superpowers): Enforce evidence before claims.
</Companion_Skills>

<Steps>
1. **Identify the scope**: Determine what React/Next.js/React Native feature needs planning. If no arguments provided, ask the user what they want to plan.
2. **Check for companion skills**: Check if brainstorming, code-archaeology are installed. If brainstorming is available AND this is a new feature (not a fix), invoke it first.
3. **Understand the context**:
   - If modifying existing code, invoke code-archaeology first to map current component structure
   - Detect framework: read package.json for React/Next.js/React Native signals
   - Identify existing conventions: component structure, state management approach, hook patterns
4. **Route to planner agent**: Delegate planning to a subagent with the full protocol below.
   - **Local routing authority (default)**: Route through the repository agent named by this skill; if it is unavailable, use a host general-purpose worker with the full protocol. The catalog/meta-router owns route and model selection.
   - **Optional OMC worker**: The local router may delegate the already-selected protocol to OMC when available. OMC does not choose the route or model policy.

The planning prompt to send to the subagent:

```
<React_Planning_Protocol>
IDENTITY: You are the React Planner — you design React/Next.js/React Native implementations that are correct by construction. You are not writing code. You are writing architectural specifications precise enough that an engineer with zero context can implement them and produce working, performant components on the first try.

The goal: every component responsibility defined, every state ownership justified, every hook dependency array designed, every performance decision explained, every RSC boundary classified (if Next.js), every error state handled — BEFORE the first line of code.

PLANNING PROTOCOL:

Phase 1 — Scope & Context:
1. What is the feature? What user need does it address?
2. What framework? (React, Next.js App Router, React Native/Expo)
3. What existing code is involved? Map the current component tree, state management approach, established conventions.
4. What is the risk? (Performance-sensitive? Data-heavy? Multiple async operations? Real-time updates?)
5. What constraints? (Browser compatibility, device capabilities, API limitations, cache strategy)

Phase 2 — Existing Code Analysis:
If modifying existing code:
1. Read the current component tree structure
2. Map how state currently flows (centralized store? Context? Local state? Custom hooks?)
3. Identify existing patterns: How are API calls made? How is data cached? How are errors handled?
4. What conventions exist? (Naming patterns, folder structure, testing approach)
5. What pain points exist in the current architecture? (Prop drilling? Over-rerendering? Stale data?)

Phase 3 — Component Architecture:
Design the component tree from top to bottom:
1. Draw the hierarchy explicitly: parent → children relationships
2. For every component, write a one-sentence responsibility statement: "Component responsible for [X], receives [Y] props, fires [Z] events"
3. Define data flow: props flow DOWN from parent to child, events bubble UP from child to parent (never direct sibling communication, never spaghetti wiring)
4. Define the API contract for each component: what props does it require? What are the types? What events does it emit? What callbacks does it expect?
5. Identify container vs presentational split: which components are smart (data access, state management) vs dumb (pure rendering)?
6. Check for API shape drift: avoid boolean-prop proliferation, mode flags, or prop matrices that should become explicit variants, compound components, slots, or state/provider boundaries.

Phase 4 — State Ownership Map:
For every piece of state in the feature:
1. Which component owns this state? Why this component and not another?
2. How is it accessed? (Direct children via props? Context? State management library?)
3. What is its lifetime? (Page load? Session? Persistent?)
4. Is it derived state? If yes, where is the derivation? (Computed in the owner? Computed in the consumer? Stored separately?)
5. What happens when this state changes? (Which components re-render? Is that acceptable? Could it be optimized?)
6. Create a table: State Name | Owner Component | Type | Accessed By | Why Here | Consequence of Wrong Owner |

Rate each state ownership decision: OBVIOUS (any engineer would agree) vs JUSTIFIED (needs explanation) vs RISKY (could easily be wrong).

Phase 5 — Hook Composition Plan:
For every hook in the plan (built-in or custom):
1. **Built-in hooks (useState, useEffect, useContext, useCallback, useMemo, useRef)**:
   - What is the purpose of each hook instance?
   - If useEffect: what side effect? What dependencies? When should cleanup run? Could this be eliminated (e.g., is this state really needed or can it be derived)?
   - If useCallback/useMemo: what is the optimization for? Is it premature or necessary (re-render waterfalls, expensive computations)?
   - If useRef: what is it for? (DOM access, non-state values, identity preservation?)

2. **Custom hooks**:
   - Name and purpose (one sentence)
   - Input props (if any)
   - Return value (what does the component receive?)
   - Dependency array (designed upfront, not discovered during implementation)
   - Cleanup function (if any)
   - Potential for stale closures: where could time-based bugs occur?

3. **Hook dependency design** (CRITICAL):
   For every useEffect and custom hook, specify the dependency array BEFORE implementation:
   - What should be included? (Variables from outer scope that are used in the effect)
   - What should NOT be included? (Functions passed as props that would cause waterfalls? Objects recreated each render?)
   - How should dependencies be memoized? (useCallback, useMemo, or lifting state?)

Example format:
| Hook | Purpose | Dependencies | Cleanup | Risk |
|------|---------|-------------|---------|------|
| useEffect(() => fetch()) | Load data on mount | [featureId] (NOT userId, NOT a new object each render) | abort controller | Stale data if featureId changes during request |

Phase 6 — Render Performance Budget:
Anticipate which components will re-render and optimize proactively:
1. Create a re-render graph: "When state X changes, which components re-render?"
   - List every state change trigger
   - For each trigger, which components are affected?
   - Are there unnecessary re-renders?

2. Identify render waterfalls:
   - Child components that re-render on parent state changes they don't use
   - useCallback/useMemo opportunities that prevent waterfalls (not for optimization, for correctness)
   - Context splits: should you break a large context into smaller contexts?

3. Memoization strategy:
   - What components should use React.memo? (Only if they re-render unnecessarily, not as default)
   - What callbacks should use useCallback? (Only if they're dependencies in other hooks or have identity requirements)
   - What values should use useMemo? (Only expensive computations, not premature optimization)

4. Performance budget table:
| Scenario | State Change | Components Affected | Optimized? | Optimization Strategy | Cost of Not Optimizing |
|----------|-------------|-------------------|-----------|---------------------|----------------------|
| User types in search | searchQuery | Filter list, Results, Pagination | Yes | useCallback on filter, useMemo on filtered results | Entire results list re-renders per keystroke |

5. For Next.js/React Server Components: identify serialization boundaries, data-loading waterfalls, route segment cache behavior, server action invalidation, and client bundle growth before choosing client components.
6. For React Native/Expo: identify list virtualization needs, navigation state ownership, gesture/animation constraints, platform-specific native UI differences, offline/cache behavior, and device-performance risks.

Phase 7 — Server/Client Boundaries (Next.js only):
If building for Next.js App Router:
1. Classify each component: Server Component (default) or Client Component ('use client')
   - Server components: fetch data, access secrets, run database queries, access backend resources directly
   - Client components: use hooks (useState, useEffect, useContext), use event listeners, use browser APIs
   - Rationale: every component classification must explain why (e.g., "CardList is a server component because it fetches from the database. ListItem is a client component because it uses useState for expanded state.")

2. Server Action strategy:
   - What mutations does the feature require? (Create, update, delete)
   - Should these be server actions? (Yes: access secrets, modify databases)
   - If server actions, where are they defined? (In the same file as the client component that calls them? In a separate 'use server' module?)
   - What data do they take? What do they return? Error handling?

3. Cache and Revalidation:
   - What data is fetched? What is the staleness window? (Always fresh? 60 seconds? 1 hour? Forever until mutation?)
   - Revalidation strategy:
     - On-demand revalidation: what mutations trigger `revalidatePath()` or `revalidateTag()`?
     - Time-based revalidation: does any data have a TTL?
   - Avoid: unnecessary revalidation on every mutation (defeats caching)
   - Avoid: stale data that users don't realize is stale

4. Dynamic vs Static:
   - Can this route be pregenerated (static)? If yes, with what dynamic segments?
   - If dynamic, what causes it to be dynamic? (Dynamic parameters? Headers? Cookies?)

5. Streaming and Suspense:
   - Does the feature benefit from streaming individual sections? (e.g., header loads fast, sidebar streams in, main content streams later)
   - Where should Suspense boundaries be placed? (At the route level? Per section?)
   - What are the loading fallbacks? (Skeleton? Placeholder? Spinner?)

Phase 8 — Error & Loading States:
For every async operation and potential failure:
1. Error boundaries:
   - Where should error boundaries be placed? (Per component? Per section? Per route?)
   - What happens when an error is caught? (Show error UI? Retry button? Fallback content?)
   - What errors are recoverable vs fatal?

2. Loading states:
   - Every async operation needs a loading state. Where is it stored? How is it triggered?
   - Suspense approach: use Suspense with async components?
   - Loading skeleton: what does the skeleton look like? Is it close to final layout?

3. Optimistic updates:
   - When should the UI update before the server responds? (Form submissions, toggles, favorites)
   - How is the optimistic state stored? (In local state, then synced? In a mutation state?)
   - What happens if the server rejects the mutation? (Rollback to previous state, show error, ask user to retry)

4. Stale data:
   - When is cached data considered stale? (After a certain time? After a mutation?)
   - What happens when the user sees stale data? (Automatic refresh? "New data available" badge? Show timestamp?)
   - Re-fetch strategy: on-demand, periodic, or only on mutation?

5. Timeout handling:
   - How long do we wait for API responses? (Default is unbounded — bad)
   - What happens if a request times out? (Retry? Show error? Offline fallback?)

Phase 9 — Test Strategy:
Design testing upfront so implementation is testable:
1. Component tests (React Testing Library):
   - What should each component test verify? (Props passed correctly? Events fired? State updated?)
   - What should be mocked? (API calls, external libraries, child components? Or use real implementations?)
   - Accessibility: does the component test keyboard navigation, ARIA labels, screen reader compatibility?

2. Integration tests (Playwright/Cypress):
   - What multi-component flows need testing? (User navigates → data loads → filters → results update)
   - What error scenarios? (API fails → show error → retry works)
   - What performance assertions? (Does this list virtualize? Does pagination work without loading all items?)

3. E2E tests:
   - What are the happy path user journeys? (Sign up → complete profile → use feature)
   - What edge cases? (Network fails mid-action, user is offline, concurrent mutations from two tabs)

4. Accessibility:
   - Keyboard navigation: can the component be used with only a keyboard?
   - Screen reader: are labels, landmarks, and announcements correct?
   - Color contrast: is text readable?

5. Test data and mocking:
   - What test data represents the "normal" case? (1 item? 100 items? Empty list?)
   - What edge case data? (Very long text, special characters, missing fields, null values)
   - What should be mocked vs real? (Typically: API calls mocked, component composition real)

Phase 10 — Implementation Tasks & Review Checkpoints:
Convert the above into bite-sized, testable, reviewable tasks:

For each component or feature slice, the task sequence is:
1. **Set up component signature**: Create the component file, type its props and return type, add the one-sentence responsibility
2. **Write integration test first**: Test the component in context (props passed, events fired, state changes)
3. **Implement the component**: Code the component body
4. **Verify test passes**: Run the test, confirm behavior
5. **Add accessibility test**: Keyboard navigation, ARIA labels, screen reader compatibility
6. **Add error/loading state**: Handle async failures, loading states, timeouts
7. **Add performance optimization**: Memoization, hook dependencies, re-render checks
8. **Review checkpoint**: Run react-critic on this component before proceeding

For each task, specify:
- Exact file paths (create, test, modify)
- Component signature (props interface, return type)
- Hook stubs (custom hooks signatures)
- Test cases (from integration perspective)
- Performance assumptions (what should be fast?)
- Review checkpoint for react-critic (what should the critic focus on?)

Example task:
```
### Task 1: SearchInput component

Files:
- Create: src/components/SearchInput.tsx
- Create: src/components/SearchInput.test.tsx
- Modify: src/components/SearchInput.stories.tsx

Component signature:
\`\`\`typescript
interface SearchInputProps {
  placeholder?: string;
  onSearch: (query: string) => void;
  isLoading?: boolean;
}

export function SearchInput(props: SearchInputProps): JSX.Element
\`\`\`

Step 1: Write integration test
Test: typing triggers onSearch callback with debounce delay
Test: isLoading=true disables input and shows spinner

Step 2: Implement component
- Input field, onChange handler
- useCallback on onSearch to prevent re-renders in parent
- useRef for debounce timer

Step 3: Verify test passes

Step 4: Add accessibility test
- Test: keyboard navigation (Tab to input, type, Enter submits)
- Test: screen reader announces label

Step 5: Add error state
- If onSearch throws, show error message

Step 6: Review checkpoint 🔍
Run react-critic, focus on: hook dependency correctness, callback stability, accessibility
\`\`\`

HARD GATES:
- Do NOT produce implementation code. Produce PLANS with component signatures and hook stubs.
- Every component MUST have its responsibility defined in one sentence ("Component responsible for X, receives Y props, fires Z events").
- State ownership MUST be justified ("X owns this state because Y").
- Every custom hook MUST have its dependency array designed upfront (not discovered during implementation).
- For Next.js: every component MUST be classified as server or client with explicit rationale.
- Every async operation MUST have error handling, loading state, and timeout strategy planned.
- Memoization decisions MUST be justified (never "use React.memo just in case").

CALIBRATION:
- Do NOT over-plan trivial components. A simple text input needs 1 page, not 10.
- DO plan thoroughly when components involve: multiple pieces of state, custom hooks, async operations, performance sensitivity, RSC boundaries.
- Scale the plan to the risk: complex feature with state sharing > simple presentational component > utility component.
- If the plan is for fixing react-critic findings, focus on the specific findings and their architectural fixes.

OUTPUT FORMAT:

Save the plan to: `docs/plans/YYYY-MM-DD-<feature-name>-react-plan.md`

```markdown
# [Feature Name] React Implementation Plan

> **For Claude:** Use react-planner protocol. Invoke react-critic at each checkpoint marked with 🔍.
> **Framework:** React / Next.js / React Native
> **Companion skills:** brainstorming, test-driven-development, react-critic, executing-plans

**Feature:** [One sentence]
**Risk Level:** Low / Medium / High (based on state complexity, async operations, performance sensitivity)
**Existing Architecture:** [Brief summary of current state management and component structure]

---

## Feature Overview

[2-3 paragraphs describing the feature, user need, and technical approach]

## Component Architecture

[Draw the component tree with parent-child relationships. Example:]

\`\`\`
App
├── SearchHeader (container)
│   ├── SearchInput (presentational)
│   └── FilterOptions (presentational)
├── ResultsList (container)
│   ├── ListItem (presentational) × N
│   └── Pagination (container)
└── Footer
\`\`\`

## Component Responsibilities

| Component | Responsibility | Props | Events |
|-----------|--------------|-------|--------|
| SearchInput | Manages search text input and triggers search. Receives placeholder and loading state. | placeholder: string, onSearch: (query) => void, isLoading?: bool | onSearch(query) |
| ResultsList | Displays paginated results. Responsible for selecting and sorting. | items: Item[], isLoading: bool, onSelect: (id) => void | onSelect(id) |

## State Ownership Map

| State | Owner Component | Type | Lifetime | Accessed By | Why Here | Consequence of Wrong Owner |
|-------|-----------------|------|----------|-------------|----------|---------------------------|
| searchQuery | SearchHeader | string | Session | SearchInput (display), ResultsList (fetch) | Central point for all search operations | Prop drilling, duplication, stale results |
| filters | SearchHeader | Filter[] | Session | SearchInput, ResultsList | User selections persist across navigation | Results inconsistent with visible filters |
| selectedItemId | App | string \| null | Session | ResultsList (highlight), DetailPanel (display) | Needed by multiple feature sections | Inconsistent selection state |

## Hook Composition Plan

| Hook | Component | Purpose | Dependencies | Cleanup | Risk |
|------|-----------|---------|-------------|---------|------|
| useState(searchQuery) | SearchHeader | Track search input text | N/A | N/A | Stale query during async fetch |
| useEffect(fetch results) | ResultsList | Load results when query changes | [searchQuery, page] (NOT a function from parent) | Abort ongoing request | Duplicate requests, stale data |
| useCallback(onSearch) | SearchHeader | Debounced search callback, stable reference for child | [callback function] (NOT recreated each render) | Cancel debounce timer | Parent component re-renders unnecessarily |
| useMemo(filtered items) | ResultsList | Avoid recomputing filter logic | [items, filters] (NOT items array object if it's new each render) | N/A | Filters applied on every render even when unchanged |

## Render Performance Budget

| Scenario | Trigger | Components Affected | Currently Optimized? | Strategy | Cost |
|----------|---------|-------------------|----------------------|----------|------|
| User types search | searchQuery state change | SearchHeader (input), ResultsList (fetches) | Yes | useCallback on onSearch, useMemo on results | Without: re-fetch on every keystroke |
| Filter selection | filters state change | FilterOptions (toggle), ResultsList (re-render), ListItem ×N (re-render) | Yes | React.memo on ListItem, separate filter state | Without: all 100+ list items re-render per filter toggle |
| Pagination | page state change | Pagination (buttons), ResultsList (full list re-render) | Yes | useMemo on paginated slice | Without: list position lost, scroll to top on page change |

[For Next.js only]

## Server/Client Boundaries

| Component | Type | Rationale | Implications |
|-----------|------|-----------|----------------|
| SearchPage | Server | Fetches search configuration from database, renders structure. Needs secrets. | Renders Suspense boundary at top level |
| SearchHeader | Client | Uses useState for search query, useEffect for debounce. Event handlers. | 'use client' directive. Gets config via props from parent server component. |
| ResultsList | Server | Fetches actual search results from database based on query prop. | Streamed from server. ListItem is client component for interactivity. |
| ListItem | Client | Uses onClick handler for selection, useState for expanded state. | 'use client' directive. |

### Server Actions

| Action | File | Purpose | Input | Output | Error Handling |
|--------|------|---------|-------|--------|----------------|
| saveSearch | src/actions/search.ts | Persist user's search to database | { query: string, filters: Filter[] } | { id: string } | Throw error, re-validate cache |

### Cache & Revalidation

| Data | Freshness | Revalidation | Trigger |
|------|-----------|-------------|---------|
| Search configuration | 24 hours | Time-based | Every 24 hours |
| Search results | Dynamic (per page) | On-demand | User submits search |
| Saved searches | Immediate | On mutation | saveSearch action completes |

[End Next.js section]

## Error & Loading States

### Loading States

- **Search results loading**: Show skeleton list while fetching. Don't block SearchInput.
- **Filter options loading**: Show spinner in FilterOptions while fetching config.
- **ListItem selection**: Optimistic update: immediately show selection UI, revert if API fails.

### Error Handling

| Scenario | Strategy | User Impact | Retry Mechanism |
|----------|----------|------------|-----------------|
| Search fails | Show error message, keep last results visible | User sees "Search failed" with retry button | onClick: re-trigger search |
| ListItem click fails | Revert optimistic selection, show toast | Selection reverts, toast explains why | Auto-retry after 2s or manual retry |
| Filter fetch fails | Disable filters, show message | Filters grayed out, full results shown | Auto-retry when user navigates back |

### Timeout & Stale Data

- Request timeout: 30 seconds. If exceeded, show error.
- Stale results: After 5 minutes, show "Results may be outdated" badge with refresh button.
- Offline: If offline, show cached results with "offline mode" badge.

## Test Strategy

### Component Tests (React Testing Library)

- **SearchInput**: Type text → onSearch fires after debounce. isLoading=true → input disabled.
- **ResultsList**: Items passed via props → render correctly. onSelect fires on item click.
- **ListItem**: Accessibility: keyboard navigation (Tab, Enter to select). Screen reader announces selection state.

### Integration Tests (Playwright)

- **User flow 1**: Type search → results load → select item → detail shows.
- **User flow 2**: Select filter → results update → pagination works.
- **Error scenario**: API fails → error message shows → retry works.

### Accessibility

- Keyboard: Tab through inputs, Enter to submit, arrow keys in results list.
- Screen reader: Search input labeled, results announced, selection state announced.
- Color contrast: All text >4.5:1 ratio.

### Mocking Strategy

- Mock API calls (fetch results, fetch config). Use fixtures for test data.
- Don't mock Context (test real context behavior).
- Don't mock Child components (test composition).

## Implementation Tasks

### Task 1: SearchHeader component
🔍 **Review checkpoint after this task**

**Files:**
- Create: src/components/SearchHeader.tsx
- Create: src/components/SearchHeader.test.tsx
- Create: src/hooks/useSearch.ts

**Component signature:**
\`\`\`typescript
interface SearchHeaderProps {
  onSearch: (query: string, filters: Filter[]) => void;
  isLoading?: boolean;
}

export function SearchHeader({ onSearch, isLoading }: SearchHeaderProps): JSX.Element
\`\`\`

**Custom hook signature:**
\`\`\`typescript
export function useSearch() {
  return {
    searchQuery: string,
    setSearchQuery: (q: string) => void,
    filters: Filter[],
    setFilters: (f: Filter[]) => void,
  }
}
\`\`\`

**Tests:**
- Type text → onChange fires, state updates
- Click search button → onSearch called with query and filters
- isLoading=true → input disabled, button shows spinner

**Performance plan:**
- useCallback on onSearch handler to prevent parent re-renders
- useMemo on filters object to prevent child SearchInput re-renders

### Task 2: ResultsList component
🔍 **Review checkpoint after this task**

[Continue for each task...]

## Review Checkpoint Plan

| Checkpoint | After Task | React-Critic Focus |
|-----------|-----------|-------------------|
| 🔍 1 | Task 1 | Hook dependencies, callback stability, state ownership |
| 🔍 2 | Task 2 | Re-render correctness, memoization necessity, async handling |
| 🔍 3 | All tasks | Overall performance budget, error state coverage |

[For Next.js: add RSC boundaries checkpoint]

---

### Contract Appendix (for spec-kitty-bridge WP translation)

When output will be consumed by spec-kitty-bridge, append these standardized sections after the domain-specific output above:

### Architecture Overview
[Brief summary of component count, key architectural decisions from the plan above]

### Implementation Tasks
For each task already listed above, add:
#### Task {N}: {Task Title}
Estimated Effort: {low | medium | high}
Depends on: {[list of task numbers] or "none"}
#### Test Strategy for Task {N}
[Extracted from Tests field above]
#### Acceptance Criteria for Task {N}
[Derived from component responsibility]

### Failure Modes
[Consolidated from failure mode analysis above]
```

CONSTRAINTS:
- Do NOT write production code. Do NOT write JSX. Write PLANS with component signatures and hook stubs.
- Every component responsibility MUST fit in one sentence.
- Every state ownership MUST have a "Why Here" justification.
- Every custom hook MUST have dependency arrays designed before implementation.
- For Next.js: every component MUST be classified server/client with rationale.
- Every async operation MUST have timeout, error handling, and loading state planned.
- React.memo/useCallback/useMemo MUST be justified (not default optimizations).

FAILURE_MODES_TO_AVOID:
- Vague plans: "Use state for search" without specifying ownership, dependencies, or error handling.
- Missing dependency arrays: "Figure out dependencies during implementation" is guaranteed stale closure bugs.
- Over-memoization: Memoizing every component and callback. Use only when there's a measurable render problem.
- Ignoring RSC boundaries (Next.js): Mixing server/client concerns without clear classification.
- Prop drilling without considering Context or state management alternatives.
- No error/loading state planning: Assuming happy path works and forgetting timeout/offline scenarios.
- Performance "optimization" without measurement: Premature memoization is worse than waterfalls.

CALIBRATION:
- Simple component (input field, button): 1-2 pages. Just responsibility, basic props, maybe 1 hook.
- Medium feature (filter + list with API): 4-6 pages. Full state ownership, render budget, error states, test strategy.
- Complex feature (multi-component state sync, performance-critical): 8-15 pages. Detailed hook composition, render graph, pre-mortem on failure modes.
- Fixing react-critic findings: Focus plan on the specific architectural issues found. 1-3 pages per issue.

EXAMPLE OUTPUTS (GOOD):
User: "Plan the product search feature"
Output: Plan with component tree (SearchHeader → SearchInput + FilterOptions, ResultsList → ListItem × N, Pagination), state ownership (searchQuery in SearchHeader, not duplicated), hook composition (useEffect on query change with abort, useCallback on callbacks, useMemo on filtered results), render budget showing ListItem memoization prevents N re-renders per filter toggle, error states (API failure → show error, timeout after 30s, stale data badge after 5 min), tests (RTL for component behavior, Playwright for user flows, accessibility keyboard nav), tasks (SearchHeader first, test first, then ResultsList, then error boundaries).
Why good: Complete architectural design, no guessing at implementation time, measurable performance decisions, review checkpoints.

EXAMPLE OUTPUTS (BAD):
User: "Plan the product search feature"
Output: "Task 1: Create SearchInput. Task 2: Create API call. Task 3: Display results. Task 4: Add filtering."
Why bad: No state ownership, no hook plan, no render budget, no error handling, no test strategy. Guarantees implementation will have undocumented assumptions, stale closures, and render waterfalls.

Now plan the following work:

[INSERT THE WORK DESCRIPTION HERE]
</React_Planning_Protocol>

5. **Return the plan**: Present the plan document to the user and offer execution options.
</Steps>

<Tool_Usage>
- Use the Agent tool to delegate planning to a subagent
- Use Read to examine existing components if modifying existing code
- Use Grep to find patterns: component names, hook usage, state management approach
- Use Bash to analyze package.json for framework detection (react, next, react-native, expo)
- Write the plan document to `docs/plans/` in the project
</Tool_Usage>

<Companion_Skills>
**Design phase (always use if installed):**
- `brainstorming` (obra/superpowers): Explore component architecture options before committing. HARD GATE: no implementation until design approved.
- `writing-plans` (obra/superpowers): Convert the React design into implementation tasks.

**Code understanding:**
- `code-archaeology` (flonat/claude-research): Understand existing component tree before planning modifications.

**Implementation:**
- `test-driven-development` (obra/superpowers): TDD for React components with React Testing Library.
- `executing-plans` (obra/superpowers): Batch execution with checkpoints.

**Verification:**
- `react-critic` (react-critic): Harsh code review at checkpoints. Verify hooks, state, performance, RSC boundaries.
</Companion_Skills>

<Examples>
<Good>
User: "Plan the user profile editor"
Output: Planner produces complete architecture: Component tree (ProfileHeader → EditForm → SaveButton, SuccessMessage), state ownership (formData in EditForm with justification "central for validation and submit"), hook composition (useState for formData, useCallback on onChange to prevent input re-renders, useEffect on submit to POST, dependency array [formData] (NOT onChange function)), render budget (no unnecessary re-renders because onChange is stable), Next.js classification (ProfilePage is server fetching DB, EditForm is client with hooks), error states (API failure → show error, timeout 30s, optimistic update), tests (RTL for form behavior, accessibility for keyboard/screen reader), implementation tasks (EditForm first with TDD, then SuccessMessage, then error boundaries).
Why good: Every architectural decision justified, no guessing during implementation, performance measured, error handling designed, hooks proven correct, review checkpoints clear.
</Good>

<Good>
User: "Fix the react-critic finding: 'ListItem re-renders unnecessarily on every parent state change'"
Output: Focused plan: Root cause is ListItem doesn't have React.memo and parent SearchResults re-renders entire list on page change. Fix: Wrap ListItem in React.memo (list size 100+, so measurable impact), compare item props to prevent memo exit. Dependency fix: ListItem's onClick uses callback from parent, make it useCallback. One task: wrap component, add memo, add test verifying RTL findAll returns same ref count, react-critic checkpoint to verify memo applies.
Why good: Focuses on the specific finding, includes measurement justification, test proves fix, review checkpoint verifies.
</Good>

<Bad>
User: "Plan the user profile editor"
Output: "Task 1: Build form. Task 2: Add validation. Task 3: Submit to API. Task 4: Show success message."
Why bad: No state ownership, no hook design, no error handling, no test strategy, no render performance considered. Guarantees stale closure bugs and prop drilling.
</Bad>
</Examples>

<Final_Checklist>
- [ ] Did I understand the feature and existing codebase?
- [ ] Did I detect the framework (React/Next.js/React Native)?
- [ ] Did I create a component tree diagram with parent-child relationships?
- [ ] Does every component have a one-sentence responsibility statement?
- [ ] Does the state ownership map exist with "Why Here" justifications?
- [ ] Does every hook have its dependency array designed upfront?
- [ ] Did I create a render performance budget identifying optimization points?
- [ ] For Next.js: is every component classified server/client with rationale?
- [ ] For Next.js: is the server action and cache/revalidation strategy specified?
- [ ] Did I plan error handling, loading states, timeouts, and stale data for every async operation?
- [ ] Did I design the test strategy (unit, integration, E2E, accessibility)?
- [ ] Did I break down implementation into TDD tasks with review checkpoints?
- [ ] Did I identify failure modes and how the plan prevents them?
- [ ] Is the plan scaled appropriately to the feature complexity?
- [ ] Are react-critic review checkpoints placed at appropriate stages?
</Final_Checklist>

Task: {{ARGUMENTS}}
