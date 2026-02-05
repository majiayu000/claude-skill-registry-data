---
name: acx.ux.evaluator
description: Expert UX evaluation and usability guidance for Carbon ACX interfaces using heuristic evaluation, cognitive walkthroughs, user journey mapping, and flow analysis.
---

# acx.ux.evaluator

## Purpose

This skill provides expert UX evaluation capabilities to identify usability issues, optimize information architecture, reduce cognitive load, and improve user experience across Carbon ACX interfaces (Dash app, React web app, static site).

**Problem Context:**
Carbon ACX interfaces are parameter-rich and data-dense. Without careful UX design, users face:
- Parameter overwhelm (too many options visible at once)
- Unclear information hierarchy
- Confusing navigation paths
- Cognitive overload from complex carbon accounting concepts
- Poor progressive disclosure

**Solution Approach:**
Guide users through complexity using established UX methodologies to create intuitive, learnable interfaces that reveal complexity progressively.

**Capabilities:**
- Heuristic Evaluation (Nielsen's 10 Usability Heuristics + domain-specific)
- Cognitive Walkthroughs (task-based mental model analysis)
- User Journey Mapping (end-to-end experience flows)
- Experience Mapping (emotional states and pain points)
- Task-Based Usability Analysis
- UX Flow Audits (interaction sequences, state transitions)
- Information Architecture Analysis
- Progressive Disclosure Assessment

## When to Use

**Trigger Patterns:**
- "Evaluate the UX of the activity browser"
- "Perform a cognitive walkthrough for new user onboarding"
- "Audit the emission calculation flow"
- "This interface feels cluttered, help me simplify it"
- "Map the user journey for creating a carbon report"
- "How can I reduce parameter overwhelm on this screen?"
- "Review the information architecture of the layer navigation"
- "Evaluate the dashboard against Nielsen heuristics"

**Use During:**
- Initial UI design (proactive evaluation)
- Feature development (before implementation)
- UI refactoring (identifying issues)
- Post-implementation review (validation)
- User feedback analysis (structured diagnosis)

**Do NOT Use When:**
- Pure visual design (color, typography) - not UX methodology
- Performance optimization (technical, not experiential)
- Code quality review (different domain)
- Writing documentation (use acx.code.assistant)

## Allowed Tools

- `read_file` - Examine UI code, components, and flows
- `grep` - Search for patterns across UI files
- `glob` - Find related component files
- `bash` - Run the app to experience flows (make app, pnpm dev)

**Access Level:** 1 (Read-Only Analysis - no code modification, pure evaluation)

**Tool Rationale:**
- `read_file`: Required to analyze component structure, props, state management
- `grep`: Needed to find interaction patterns and UI elements
- `glob`: Helps discover related components and flows
- `bash`: Allows experiencing the UI directly for evaluation

**Explicitly Denied:**
- No file writes or edits (this skill ONLY evaluates, does not implement fixes)
- No deployments or production access
- No data collection or user tracking

## Expected I/O

**Input:**
- Type: UX evaluation request
- Format: Natural language description of:
  - Interface/flow to evaluate (e.g., "activity browser", "report builder")
  - Specific concerns (e.g., "too cluttered", "confusing navigation")
  - Methodology preference (optional - will auto-select if not specified)
  - User persona/context (e.g., "first-time analyst", "expert user")

**Examples:**
```
"Evaluate the emission calculation workflow using cognitive walkthrough"
"Perform heuristic evaluation on the dashboard layout"
"Map the user journey for a new analyst creating their first report"
"Audit the UX flow for switching between layers"
```

**Output:**
- Type: Structured UX evaluation report
- Format: Markdown document with:
  - Executive summary (3-5 key findings)
  - Methodology used
  - Detailed findings with severity ratings
  - Specific recommendations with file:line references
  - Prioritized action items
- Severity Levels:
  - **Critical** - Blocks task completion or causes errors
  - **High** - Causes significant friction or confusion
  - **Medium** - Noticeable usability issue
  - **Low** - Minor enhancement opportunity
- Each finding includes:
  - Issue description
  - User impact
  - Component/file reference
  - Specific recommendation
  - Estimated effort (S/M/L)

## Dependencies

**Required:**
- Access to Carbon ACX UI code:
  - `apps/carbon-acx-web/src/` (modern web app)
  - `site/src/` (static React site)
  - `app/` (Dash analytics interface)
- Understanding of target users:
  - Carbon analysts (primary)
  - Investors/stakeholders (secondary)
  - Auditors/compliance officers (tertiary)
- Reference files:
  - `reference/ux_heuristics.md` - Nielsen + domain-specific heuristics
  - `reference/ux_methodologies.md` - Evaluation frameworks
  - `reference/user_personas.md` - Target user profiles

**UX Frameworks:**
- Nielsen's 10 Usability Heuristics
- Cognitive Dimensions of Notation
- Information Foraging Theory
- Progressive Disclosure Principles
- Fitts's Law (interaction targets)
- Miller's Law (cognitive load - 7±2 items)

## Core Methodologies

### 1. Heuristic Evaluation

**Nielsen's 10 Heuristics (+ Carbon ACX adaptations):**

1. **Visibility of system status**
   - Show calculation progress, data loading states
   - Indicate which layer/scenario is active
   - Display data freshness (last updated timestamps)

2. **Match between system and real world**
   - Use carbon accounting terminology correctly
   - Present units clearly (kgCO2e, tCO2e)
   - Match analyst mental models (not developer abstractions)

3. **User control and freedom**
   - Allow undo for parameter changes
   - Enable scenario comparison without losing work
   - Provide clear exit paths from flows

4. **Consistency and standards**
   - Consistent navigation across Dash/React/Static interfaces
   - Standard patterns for filters, exports, visualizations
   - Unified design language

5. **Error prevention**
   - Validate inputs before submission
   - Warn before destructive actions
   - Provide sensible defaults

6. **Recognition rather than recall**
   - Show recently used activities/layers
   - Display current filter state visibly
   - Use tooltips for complex terms

7. **Flexibility and efficiency of use**
   - Keyboard shortcuts for power users
   - Batch operations for analysts
   - Customizable dashboards

8. **Aesthetic and minimalist design**
   - Hide advanced parameters by default
   - Progressive disclosure for complexity
   - Remove decorative elements that don't aid understanding

9. **Help users recognize, diagnose, and recover from errors**
   - Clear error messages with actionable guidance
   - Validation feedback inline
   - Context-aware help

10. **Help and documentation**
    - Contextual tooltips for emission factors
    - Onboarding for first-time users
    - Searchable documentation

**Domain-Specific Heuristics:**

11. **Data transparency and provenance**
    - Show emission factor sources
    - Display calculation methodology
    - Link to reference documentation

12. **Progressive disclosure of complexity**
    - Start simple, reveal advanced options on demand
    - Layer complexity (basic → intermediate → expert)
    - Collapsible sections for optional parameters

**Process:**
1. Read UI components systematically
2. Evaluate each heuristic against the interface
3. Document violations with severity
4. Provide specific, actionable recommendations

### 2. Cognitive Walkthrough

**Purpose:** Evaluate learnability for new users attempting specific tasks

**Process:**
1. Define user persona (e.g., "new carbon analyst")
2. Define task (e.g., "calculate emissions for coffee shop")
3. Walk through each step asking:
   - Will user know what to do?
   - Will user see the control/action?
   - Will user understand the control does what they want?
   - Will user understand progress toward goal?
4. Document friction points
5. Recommend improvements

**Example Tasks for Carbon ACX:**
- First-time setup: Add organization and activities
- Calculate emissions for a new activity
- Compare scenarios (baseline vs. mitigation)
- Export a compliance report
- Understand why emissions increased month-over-month

### 3. User Journey Mapping

**Purpose:** Visualize end-to-end experience across touchpoints

**Components:**
- Stages (e.g., Discovery → Onboarding → Daily Use → Reporting)
- User actions at each stage
- Touchpoints (web app, Dash, static site, exports)
- User thoughts and emotions
- Pain points and opportunities

**Output Format:**
```
Stage: Onboarding
Actions:
  - Create account
  - Add first activity
  - Run first calculation
Thoughts:
  - "Is my data secure?"
  - "What emission factors are being used?"
Emotions:
  - Curious but cautious
Pain Points:
  - Unclear where to start
  - Too many options on first screen
Opportunities:
  - Guided wizard for first calculation
  - Sample data to explore
```

### 4. Experience Mapping

**Purpose:** Map emotional journey and identify moments that matter

**Focus Areas:**
- High-stakes moments (compliance deadlines, audit preparation)
- Frustration points (slow calculations, unclear errors)
- Delight moments (insight discovery, easy exports)
- Uncertainty moments (which emission factor to use?)

### 5. Task-Based Usability Analysis

**Process:**
1. Identify critical tasks
2. Measure task success criteria:
   - Completion rate (can user finish?)
   - Time on task (efficiency)
   - Error rate (mistakes made)
   - Satisfaction (subjective rating)
3. Analyze failure points
4. Recommend optimizations

**Critical Tasks for Carbon ACX:**
- Add new activity with emission factor
- Filter activities by layer
- Toggle between scenarios
- Export calculation results
- Trace emission factor provenance
- Compare time periods

### 6. UX Flow Audit

**Purpose:** Analyze interaction sequences and state transitions

**Analysis:**
- Entry points (how users arrive at flow)
- Decision points (branching logic)
- Dead ends (no clear next action)
- Loops (repeated actions)
- Exit points (how users complete or abandon)
- State management (what persists across steps?)

**Flow Types:**
- Linear (onboarding wizard)
- Hub-and-spoke (dashboard with tools)
- Stepped (multi-stage forms)
- Freeform (exploratory analysis)

## Evaluation Framework

### Severity Rating

**Critical (P0):**
- Blocks task completion entirely
- Causes data loss or corruption
- Creates security/compliance risk
- Violates accessibility requirements (WCAG A)

**High (P1):**
- Causes significant user frustration
- Requires workaround to complete task
- Affects >50% of users
- Violates accessibility recommendations (WCAG AA)

**Medium (P2):**
- Noticeable usability issue
- Has acceptable workaround
- Affects 20-50% of users
- Reduces efficiency

**Low (P3):**
- Minor enhancement
- Aesthetic inconsistency
- Affects <20% of users
- Polish opportunity

### Effort Estimation

**Small (S):**
- 1-4 hours (simple prop change, copy update, visibility toggle)

**Medium (M):**
- 1-3 days (component restructure, new state management, flow reorganization)

**Large (L):**
- 1-2 weeks (major architectural change, new interaction paradigm, multi-component refactor)

### Impact vs. Effort Matrix

Prioritize fixes using 2x2 matrix:
```
High Impact, Low Effort → Quick Wins (do first)
High Impact, High Effort → Strategic Projects (plan carefully)
Low Impact, Low Effort → Fill-ins (do when bandwidth available)
Low Impact, High Effort → Time Sinks (avoid unless user-requested)
```

## Example Evaluation

### Example 1: Activity Browser Heuristic Evaluation

**User Request:** "Evaluate the activity browser - it feels overwhelming"

**Claude Process:**
1. Read `apps/carbon-acx-web/src/components/ActivityBrowser.tsx`
2. Analyze against Nielsen heuristics
3. Identify progressive disclosure issues
4. Document findings with severity

**Output:**
```markdown
# Activity Browser UX Evaluation

**Date:** 2025-10-22
**Methodology:** Heuristic Evaluation (Nielsen + Domain Heuristics)
**Evaluator:** Claude (acx.ux.evaluator)

## Executive Summary

The activity browser violates progressive disclosure principles by showing all 50+ parameters simultaneously. Users report feeling overwhelmed and unable to find basic actions.

**Key Findings:**
1. **Critical:** No search/filter on initial load (blocks task for >500 activities)
2. **High:** All metadata columns visible by default (cognitive overload)
3. **Medium:** No recently-used section (requires recall vs recognition)

## Detailed Findings

### Finding 1: Parameter Overload [Critical, Small]

**Heuristic Violated:** #8 Aesthetic and minimalist design, #12 Progressive disclosure

**Issue:**
File: `apps/carbon-acx-web/src/components/ActivityBrowser.tsx:45-120`

All activity metadata is displayed in table columns:
- activity_id
- name
- layer_id
- scope
- emission_factor
- unit
- source
- last_updated
- notes

**User Impact:**
- Horizontal scrolling required
- Can't scan quickly
- Experts need detail, but beginners need simplicity

**Recommendation:**
Implement column visibility controls with smart defaults:

```typescript
// Default visible columns (beginners)
const defaultColumns = ['name', 'emission_factor', 'unit'];

// Advanced columns (show on toggle)
const advancedColumns = ['activity_id', 'scope', 'source', 'last_updated', 'notes'];
```

Add column picker UI:
```tsx
<ColumnVisibilityControl
  defaultVisible={defaultColumns}
  available={advancedColumns}
  onToggle={(cols) => setVisibleColumns(cols)}
/>
```

**Effort:** Small (2-3 hours)
**Impact:** High (reduces cognitive load for 80% of users)
**Priority:** Quick Win

---

### Finding 2: No Search on Load [Critical, Small]

**Heuristic Violated:** #6 Recognition rather than recall, #7 Flexibility and efficiency

**Issue:**
File: `apps/carbon-acx-web/src/components/ActivityBrowser.tsx:25`

Search input exists but is not auto-focused. With 500+ activities, users must scroll/scan unnecessarily.

**User Impact:**
- Expert users know activity ID (e.g., "COFFEE.12OZ") but can't type immediately
- New users don't know what activities exist

**Recommendation:**
Auto-focus search input on mount:

```tsx
const searchInputRef = useRef<HTMLInputElement>(null);

useEffect(() => {
  searchInputRef.current?.focus();
}, []);

<Input
  ref={searchInputRef}
  placeholder="Search activities (e.g., 'coffee', 'transport', 'COFFEE.12OZ')"
  // ... other props
/>
```

**Effort:** Small (30 minutes)
**Impact:** High (supports both novice and expert users)
**Priority:** Quick Win

---

### Finding 3: No Recently Used [Medium, Medium]

**Heuristic Violated:** #6 Recognition rather than recall, #7 Efficiency for frequent users

**Issue:**
File: `apps/carbon-acx-web/src/components/ActivityBrowser.tsx:1-200`

No "recently used" or "favorites" section. Analysts repeatedly working with same activities must search each time.

**User Impact:**
- Repetitive work (search "coffee" 10x/day)
- Lost context between sessions

**Recommendation:**
Add recent activities section above main table:

```tsx
<Section title="Recently Used">
  <ActivityChips
    activities={recentActivities}
    onSelect={handleQuickSelect}
  />
</Section>

// Store in localStorage or user preferences
const addToRecent = (activity: Activity) => {
  const recent = JSON.parse(localStorage.getItem('recent_activities') || '[]');
  const updated = [activity, ...recent.filter(a => a.id !== activity.id)].slice(0, 10);
  localStorage.setItem('recent_activities', JSON.stringify(updated));
};
```

**Effort:** Medium (4-6 hours including persistence)
**Impact:** Medium (helps frequent users, not critical for occasional users)
**Priority:** Strategic Project (plan for next sprint)

## Recommendations Summary

| Finding | Severity | Effort | Impact | Priority |
|---------|----------|--------|--------|----------|
| Parameter Overload | Critical | S | High | Quick Win |
| No Search Focus | Critical | S | High | Quick Win |
| No Recently Used | Medium | M | Medium | Strategic |

## Next Steps

1. **Immediate (this sprint):**
   - Implement column visibility controls
   - Auto-focus search input

2. **Short-term (next sprint):**
   - Add recently-used activities
   - Consider favorites/bookmarks

3. **Long-term (backlog):**
   - User preferences persistence (backend)
   - Activity recommendations based on usage
```

---

### Example 2: Cognitive Walkthrough for First Report

**User Request:** "Walk through a new analyst creating their first carbon report"

**Claude Process:**
1. Define persona: "Sarah, new sustainability analyst, familiar with Excel, unfamiliar with carbon accounting"
2. Define task: "Calculate Q3 2024 emissions for her coffee shop chain"
3. Walk through steps in `app/app.py` (Dash interface)
4. Document friction points at each step

**Output:**
```markdown
# Cognitive Walkthrough: First Carbon Report

**Persona:** Sarah - New Sustainability Analyst
- Background: 2 years in operations, familiar with Excel, new to carbon accounting
- Goal: Calculate Q3 2024 emissions for 5-location coffee shop chain
- Context: First week on job, manager asked for "quick emissions estimate"

**Task:** Generate first carbon report
**Interface:** Dash analytics app (`app/app.py`)

## Step-by-Step Analysis

### Step 1: Landing Page

**Action Required:** Navigate to report builder

**Questions:**
- *Will Sarah know what to do?*
  - ❌ No - Landing shows 6 tiles with technical terms ("Layers", "Intensity Matrices", "Scenarios")
  - She doesn't know carbon accounting terminology yet

- *Will Sarah see the control?*
  - ⚠️ Maybe - "Reports" tile exists but buried among technical options

- *Will Sarah understand it does what she wants?*
  - ❌ No - "Reports" is vague. Does it show existing reports or create new ones?

- *Will Sarah understand progress?*
  - ❌ No - No onboarding wizard, no "Start here" guidance

**Friction Points:**
- **High severity:** Assumes user knows carbon accounting workflow
- No progressive onboarding for first-time users
- Technical jargon without explanations

**Recommendation:**
Add first-time user flow:
```python
# app/app.py:150
if is_first_visit():
    return dbc.Modal([
        dbc.ModalHeader("Welcome to Carbon ACX"),
        dbc.ModalBody([
            html.P("Let's calculate emissions in 3 steps:"),
            html.Ol([
                html.Li("Add your activities (what your business does)"),
                html.Li("Select time period"),
                html.Li("View emissions breakdown"),
            ]),
            dbc.Button("Start Guided Setup", id="start-wizard"),
        ])
    ], is_open=True)
```

---

### Step 2: Adding Activities

**Action Required:** Input coffee shop activities

**Questions:**
- *Will Sarah know what to do?*
  - ⚠️ Partially - "Add Activity" button is visible
  - But she doesn't know what qualifies as an "activity"
  - Does "coffee shop" mean one activity or many?

- *Will Sarah see the control?*
  - ✅ Yes - Button is prominent

- *Will Sarah understand it?*
  - ❌ No - Clicking reveals form with fields:
    - activity_id (what format? is this auto-generated?)
    - layer_id (dropdown with "professional", "online", "civic" - unclear which applies to coffee)
    - scope (1/2/3 - no explanation what these mean)

**Friction Points:**
- **Critical severity:** Scope 1/2/3 is compliance jargon, not explained
- **High severity:** layer_id categories don't match mental model of "coffee shop"
- **Medium severity:** activity_id format unclear (free text? must match pattern?)

**Recommendation:**
Add contextual help and better labels:
```python
# app/components/activity_form.py
dbc.FormGroup([
    dbc.Label([
        "Activity Type",
        dbc.Badge("?", id="activity-type-help", className="ml-2"),
    ]),
    dbc.Tooltip(
        "An activity is anything that produces emissions. "
        "For a coffee shop: brewing coffee, heating water, refrigeration, deliveries.",
        target="activity-type-help",
    ),
    dcc.Dropdown(id="activity-type", options=[
        {"label": "Coffee brewing (12oz cup)", "value": "COFFEE.12OZ"},
        {"label": "Electricity consumption (kWh)", "value": "ELECTRICITY.GRID"},
        {"label": "Natural gas heating (m³)", "value": "GAS.HEATING"},
        # ... common activities
    ])
])
```

Replace jargon:
- "Scope 1/2/3" → "Direct emissions / Purchased energy / Value chain"
- "layer_id" → "Business category" with examples in dropdown

---

### Step 3: Selecting Emission Factors

**Action Required:** Choose appropriate emission factors

**Questions:**
- *Will Sarah know what to do?*
  - ❌ No - Form shows "Emission Factor" field expecting numeric input
  - Sarah doesn't know emission factors, expects system to provide them

- *Will Sarah see the control?*
  - ✅ Yes - Field is visible

- *Will Sarah understand it?*
  - ❌ No - No guidance on where emission factors come from
  - No suggestion of defaults
  - No units explanation (kgCO2e/unit means what?)

**Friction Points:**
- **Critical severity:** User expected defaults, not manual entry
- **High severity:** No link to emission factor database
- **High severity:** Units not explained (kgCO2e per WHAT?)

**Recommendation:**
Auto-populate emission factors with transparency:
```python
# When activity selected, auto-fill emission factor
@app.callback(
    Output("emission-factor", "value"),
    Output("ef-source", "children"),
    Input("activity-type", "value")
)
def populate_emission_factor(activity_id):
    ef_data = get_emission_factor(activity_id)
    return ef_data.value, dbc.Alert([
        f"Using default: {ef_data.value} kgCO2e/{ef_data.unit}",
        html.Br(),
        html.Small([
            "Source: ", html.A(ef_data.source, href=ef_data.url, target="_blank")
        ])
    ], color="info")
```

Allow override but make defaults obvious.

---

### Step 4: Viewing Results

**Action Required:** Understand emissions output

**Questions:**
- *Will Sarah know what to do?*
  - ⚠️ Partially - "Calculate" button is clear
  - But after clicking, results show as JSON-like structure

- *Will Sarah see the results?*
  - ⚠️ Maybe - Results appear below fold, no scroll indication

- *Will Sarah understand the results?*
  - ❌ No - Output format:
    ```
    {
      "total_kgCO2e": 1247.3,
      "by_layer": {"professional": 1247.3},
      "by_scope": {"scope1": 450.2, "scope2": 797.1}
    }
    ```
  - Technical structure, not human-readable

- *Will Sarah understand if this is good/bad?*
  - ❌ No - No context (Is 1247 kg a lot? How does this compare?)

**Friction Points:**
- **Critical severity:** Results not human-readable
- **High severity:** No context or benchmarking
- **Medium severity:** No export option visible

**Recommendation:**
Human-friendly results display:
```python
# app/components/results.py
dbc.Card([
    dbc.CardHeader("Your Emissions Summary"),
    dbc.CardBody([
        html.H2(f"{total_kgCO2e:,.1f} kg CO2e", className="text-center"),
        html.P(f"≈ {total_kgCO2e / 1000:.1f} tonnes", className="text-muted text-center"),

        html.Hr(),

        html.H5("What does this mean?"),
        dbc.Row([
            dbc.Col([
                dbc.Badge("Equivalent to:", className="mr-2"),
                html.Span(f"{total_kgCO2e / 411:.0f} flights (NYC to London)"),
            ]),
        ]),

        html.Hr(),

        html.H5("Breakdown"),
        dcc.Graph(figure=create_emissions_chart(breakdown)),

        dbc.Button("Export Report", id="export-btn", color="primary"),
    ])
])
```

## Overall Learnability Assessment

**Task Completion Likelihood:** 40%
- Sarah will likely get stuck at Step 2 (activity definition)
- May abandon if no help available

**Learning Curve Issues:**
1. **Assumes domain knowledge** - expects user to know Scope 1/2/3, emission factors
2. **No scaffolding** - jumps straight to advanced interface
3. **Poor error prevention** - allows nonsensical inputs
4. **Lack of examples** - no sample data to explore

**Recommendations Priority:**

**Immediate (Blocking first-time use):**
1. Add onboarding wizard with sample data
2. Auto-populate emission factors
3. Replace jargon with plain language
4. Add contextual help throughout

**Short-term (Reduces friction):**
1. Human-readable results format
2. Contextual tooltips on all fields
3. Example-driven activity library

**Long-term (Improves mastery):**
1. Progressive disclosure (basic → advanced mode)
2. Guided templates for common use cases
3. In-app tutorials and videos
```

## Limitations

**Scope Limitations:**
- Cannot conduct actual user testing (no real users available)
- Cannot measure quantitative metrics (time on task, completion rate) without instrumentation
- Evaluations are expert-based, not user-validated
- Cannot assess brand perception or marketing effectiveness

**Methodology Constraints:**
- Heuristic evaluation finds ~75% of usability issues (remaining 25% require user testing)
- Cognitive walkthroughs are hypothesis-driven, not empirically validated
- Journey maps require user research to validate assumptions
- Flow audits are static analysis, not behavioral observation

**Knowledge Boundaries:**
- Evaluates based on established UX principles, may not account for novel interaction paradigms
- Carbon accounting domain knowledge is important context
- Accessibility evaluation is basic (full WCAG audit requires specialized tools)

## Validation Criteria

**Success Metrics:**
- ✅ Evaluation covers all requested methodologies
- ✅ Findings include severity, effort, and impact ratings
- ✅ Recommendations are specific with file:line references
- ✅ Output is actionable (not just "improve UX")
- ✅ Prioritization is clear (Quick Wins vs Strategic Projects)

**Quality Checks:**
- Each finding maps to specific heuristic or UX principle
- Recommendations include code examples where applicable
- User impact is articulated clearly
- Severity ratings are consistent and justified

**Failure Modes:**
- ❌ Vague recommendations ("improve layout") → Fix: Be specific
- ❌ No prioritization → Fix: Use Impact/Effort matrix
- ❌ Missing file references → Fix: Include component paths
- ❌ Contradictory recommendations → Fix: Consider tradeoffs explicitly

## Related Skills

**Composes With:**
- `acx.code.assistant` - Implement UX recommendations as code
- `carbon.data.qa` - Understand data structure for UX design

**Precedes:**
- After UX evaluation, use `acx.code.assistant` to implement fixes

**Not a Replacement For:**
- Actual user testing with real users
- Quantitative analytics (GA, heatmaps, session recordings)
- Visual design expertise (color theory, typography)
- Accessibility auditing tools (axe, WAVE)

## Maintenance

**Owner:** ACX UX Team
**Review Cycle:** Monthly (interfaces evolve frequently)
**Last Updated:** 2025-10-22
**Version:** 1.0.0

**Maintenance Notes:**
- Update heuristics as new UI patterns emerge
- Refresh user personas when target audience shifts
- Review findings monthly to track progress
- Update methodologies as Carbon ACX UI matures
