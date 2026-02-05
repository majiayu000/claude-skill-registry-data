---
name: bubbletea-designer
description: Automates Bubble Tea TUI design by analyzing requirements, mapping to appropriate components from the Charmbracelet ecosystem, generating component architecture, and creating implementation workflows. Use when designing terminal UIs, planning Bubble Tea applications, selecting components, or needing design guidance for TUI development.
---

# Bubble Tea TUI Designer

Automate the design process for Bubble Tea terminal user interfaces with intelligent component mapping, architecture generation, and implementation planning.

## When to Use This Skill

This skill automatically activates when you need help designing, planning, or structuring Bubble Tea TUI applications:

### Design & Planning

Use this skill when you:
- **Design a new TUI application** from requirements
- **Plan component architecture** for terminal interfaces
- **Select appropriate Bubble Tea components** for your use case
- **Generate implementation workflows** with step-by-step guides
- **Map user requirements to Charmbracelet ecosystem** components

### Typical Activation Phrases

The skill responds to questions like:
- "Design a TUI for [use case]"
- "Create a file manager interface"
- "Build an installation progress tracker"
- "Which Bubble Tea components should I use for [feature]?"
- "Plan a multi-view dashboard TUI"
- "Generate architecture for a configuration wizard"
- "Automate TUI design for [application]"

### TUI Types Supported

- **File Managers**: Navigation, selection, preview
- **Installers/Package Managers**: Progress tracking, step indication
- **Dashboards**: Multi-view, tabs, real-time updates
- **Forms & Wizards**: Multi-step input, validation
- **Data Viewers**: Tables, lists, pagination
- **Log/Text Viewers**: Scrolling, searching, highlighting
- **Chat Interfaces**: Input + message display
- **Configuration Tools**: Interactive settings
- **Monitoring Tools**: Real-time data, charts
- **Menu Systems**: Selection, navigation

## How It Works

The Bubble Tea Designer follows a systematic 6-step design process:

### 1. Requirement Analysis

**Purpose**: Extract structured requirements from natural language descriptions

**Process**:
- Parse user description
- Identify core features
- Extract interaction patterns
- Determine data types
- Classify TUI archetype

**Output**: Structured requirements dictionary with:
- Features list
- Interaction types (keyboard, mouse, both)
- Data types (files, text, tabular, streaming)
- View requirements (single, multi-view, tabs)
- Special requirements (validation, progress, real-time)

### 2. Component Mapping

**Purpose**: Map requirements to appropriate Bubble Tea components

**Process**:
- Match features to component capabilities
- Consider component combinations
- Evaluate alternatives
- Justify selections based on requirements

**Output**: Component recommendations with:
- Primary components (core functionality)
- Supporting components (enhancements)
- Styling components (Lipgloss)
- Justification for each selection
- Alternative options considered

### 3. Pattern Selection

**Purpose**: Identify relevant example files from charm-examples-inventory

**Process**:
- Search CONTEXTUAL-INVENTORY.md for matching patterns
- Filter by capability category
- Rank by relevance to requirements
- Select 3-5 most relevant examples

**Output**: List of example files to reference:
- File path in charm-examples-inventory
- Capability category
- Key patterns to extract
- Specific lines or functions to study

### 4. Architecture Design

**Purpose**: Create component hierarchy and interaction model

**Process**:
- Design model structure (what state to track)
- Plan Init() function (initialization commands)
- Design Update() function (message handling)
- Plan View() function (rendering strategy)
- Create component composition diagram

**Output**: Architecture specification with:
- Model struct definition
- Component hierarchy (ASCII diagram)
- Message flow diagram
- State management plan
- Rendering strategy

### 5. Workflow Generation

**Purpose**: Create ordered implementation steps

**Process**:
- Determine dependency order
- Break into logical phases
- Reference specific example files
- Include testing checkpoints

**Output**: Step-by-step implementation plan:
- Phase breakdown (setup, components, integration, polish)
- Ordered tasks with dependencies
- File references for each step
- Testing milestones
- Estimated time per phase

### 6. Comprehensive Design Report

**Purpose**: Generate complete design document combining all analyses

**Process**:
- Execute all 5 previous analyses
- Combine into unified document
- Add implementation guidance
- Include code scaffolding templates
- Generate README outline

**Output**: Complete TUI design specification with:
- Executive summary
- All analysis results (requirements, components, patterns, architecture, workflow)
- Code scaffolding (model struct, basic Init/Update/View)
- File structure recommendation
- Next steps and resources

## Data Source: Charm Examples Inventory

This skill references a curated inventory of 46 Bubble Tea examples from the Charmbracelet ecosystem.

### Inventory Structure

**Location**: `charm-examples-inventory/bubbletea/examples/`

**Index File**: `CONTEXTUAL-INVENTORY.md`

**Categories** (11 capability groups):
1. Installation & Progress Tracking
2. Form Input & Validation
3. Data Display & Selection
4. Content Viewing
5. View Management & Navigation
6. Loading & Status Indicators
7. Time-Based Operations
8. Network & External Operations
9. Real-Time & Event Handling
10. Screen & Terminal Management
11. Input & Interaction

### Component Coverage

**Input Components**:
- `textinput` - Single-line text input
- `textarea` - Multi-line text editing
- `textinputs` - Multiple inputs with focus management
- `filepicker` - File system navigation and selection
- `autocomplete` - Text input with suggestions

**Display Components**:
- `table` - Tabular data with row selection
- `list` - Filterable, paginated lists
- `viewport` - Scrollable content area
- `pager` - Document viewer
- `paginator` - Page-based navigation

**Feedback Components**:
- `spinner` - Loading indicator
- `progress` - Progress bar (animated & static)
- `timer` - Countdown timer
- `stopwatch` - Elapsed time tracker

**Layout Components**:
- `views` - Multiple screen states
- `composable-views` - Composed bubble models
- `tabs` - Tab-based navigation
- `help` - Help menu system

**Utility Patterns**:
- HTTP requests (`http`)
- External commands (`exec`)
- Real-time events (`realtime`)
- Alt screen buffer (`altscreen-toggle`)
- Mouse support (`mouse`)
- Window resize (`window-size`)

### Pattern Recognition

The skill uses pattern matching to identify:

**By Feature**:
- "progress tracking" → `progress`, `spinner`, `package-manager`
- "form with validation" → `credit-card-form`, `textinputs`
- "table display" → `table`, `table-resize`
- "file selection" → `file-picker`, `list-default`
- "multi-step process" → `views`, `package-manager`

**By Interaction**:
- "keyboard navigation" → Most examples, especially `help`
- "mouse support" → `mouse`, `table`
- "scrolling" → `viewport`, `pager`
- "filtering" → `list-default`, `autocomplete`

**By Architecture**:
- "single view" → `simple`, `spinner`, `textinput`
- "multi-view state machine" → `views`
- "composed models" → `composable-views`
- "tab navigation" → `tabs`

## Workflow Details

### Workflow 1: Quick Component Lookup

**User Query**: "Which component should I use for [feature]?"

**Process**:
1. Parse feature description
2. Search component taxonomy
3. Return top 3 matches with justification

**Example**:
```
User: "Which component for file selection?"

Response:
Top recommendations:
1. filepicker.Model - Dedicated file system navigation
   - Built-in directory traversal
   - File type filtering
   - Selection callbacks
   Reference: examples/file-picker/main.go

2. list.Model - Custom file list
   - More control over display
   - Custom item rendering
   - Can add file metadata
   Reference: examples/list-fancy/main.go

3. table.Model - Tabular file display
   - Show multiple file attributes
   - Sortable columns
   - Good for detailed views
   Reference: examples/table/main.go
```

### Workflow 2: Design from Description

**User Query**: "Design a TUI for [application]"

**Process**:
1. Run `requirement_analysis(description)`
2. Run `component_mapping(requirements)`
3. Run `pattern_selection(components)`
4. Run `architecture_design(components, patterns)`
5. Run `workflow_generation(architecture)`
6. Combine into design report

**Example**:
```
User: "Design a TUI for a log file viewer with search and highlighting"

Response: [Comprehensive design report including]:

REQUIREMENTS:
- View: Scrollable text display
- Interaction: Search, highlight matches, navigate results
- Data: Log file lines (streaming or loaded)

COMPONENTS:
- viewport.Model (scrollable display)
- textinput.Model (search query)
- Custom highlighter (Lipgloss styles)

ARCHITECTURE:
model struct {
    viewport viewport.Model
    searchInput textinput.Model
    logLines []string
    searchMode bool
    matches []int
    currentMatch int
}

WORKFLOW:
Phase 1: Basic viewer (viewport + file loading)
Phase 2: Add search input
Phase 3: Implement highlighting
Phase 4: Add navigation between matches
Phase 5: Polish (status bar, help text)

[Full implementation steps with file references...]
```

### Workflow 3: Architecture Planning

**User Query**: "Plan architecture for [complex TUI]"

**Process**:
1. Identify sub-components
2. Design model composition
3. Create message flow diagram
4. Plan state management
5. Generate ASCII architecture diagram

**Example**:
```
User: "Plan architecture for a package manager TUI with installation queue and progress"

Response:

ARCHITECTURE DIAGRAM:
┌─────────────────────────────────────┐
│         Main Model                  │
├─────────────────────────────────────┤
│  view: currentView                  │
│  packages: []PackageItem            │
│  queue: InstallQueue                │
│  progress: ProgressState            │
└────────────┬───────────────┬────────┘
             │               │
        ┌────▼────┐     ┌───▼─────┐
        │ List    │     │Progress │
        │ Model   │     │ Model   │
        └─────────┘     └─────────┘

STATE MANAGEMENT:
- currentView: enum (selectView, installView, completeView)
- packages: list of selectable items
- queue: ordered installation queue
- progress: current package progress (0-100)

MESSAGE FLOW:
User Input → Update() → Route to current view handler
Install Start → Switch view + Init progress
Package Complete → Update progress + Next package
All Complete → Switch to complete view

[Detailed implementation guidance...]
```

### Workflow 4: Pattern Selection

**User Query**: "Show me examples for [capability]"

**Process**:
1. Search CONTEXTUAL-INVENTORY.md
2. Filter by capability
3. Return sorted by relevance
4. Include key patterns to study

**Example**:
```
User: "Show me examples for progress tracking"

Response:

PROGRESS TRACKING EXAMPLES:

1. package-manager (examples/package-manager/main.go)
   Category: Installation & Progress Tracking
   Key Patterns:
   - Combined spinner + progress bar
   - Sequential task execution
   - Tea.Println for persistent output above TUI
   - Custom completion messages

2. progress-animated (examples/progress-animated/main.go)
   Category: Loading & Status Indicators
   Key Patterns:
   - Gradient progress styling
   - Smooth animation with FrameMsg
   - Indeterminate/determinate modes

3. progress-download (examples/progress-download/main.go)
   Category: Loading & Status Indicators
   Key Patterns:
   - Network operation tracking
   - Real-time percentage updates
   - HTTP integration

Study these in order:
1. progress-animated (learn basics)
2. package-manager (see real-world usage)
3. progress-download (network-specific)
```

## Available Scripts

All scripts are in `scripts/` directory and can be run independently or through the main orchestrator.

### Main Orchestrator

**`design_tui.py`**

Comprehensive design report generator - combines all analyses.

**Usage**:
```python
from scripts.design_tui import comprehensive_tui_design_report

report = comprehensive_tui_design_report(
    description="Log viewer with search and highlighting",
    inventory_path="/path/to/charm-examples-inventory"
)

print(report['summary'])
print(report['architecture'])
print(report['workflow'])
```

**Parameters**:
- `description` (str): Natural language TUI description
- `inventory_path` (str): Path to charm-examples-inventory directory
- `include_sections` (List[str], optional): Which sections to include
- `detail_level` (str): "summary" | "detailed" | "complete"

**Returns**:
```python
{
    'description': str,
    'generated_at': str (ISO timestamp),
    'sections': {
        'requirements': {...},
        'components': {...},
        'patterns': {...},
        'architecture': {...},
        'workflow': {...}
    },
    'summary': str,
    'scaffolding': str (code template),
    'next_steps': List[str]
}
```

### Analysis Scripts

**`analyze_requirements.py`**

Extract structured requirements from natural language.

**Functions**:
- `extract_requirements(description)` - Parse description
- `classify_tui_type(requirements)` - Determine archetype
- `identify_interactions(requirements)` - Find interaction patterns

**`map_components.py`**

Map requirements to Bubble Tea components.

**Functions**:
- `map_to_components(requirements, inventory)` - Main mapping
- `find_alternatives(component)` - Alternative suggestions
- `justify_selection(component, requirement)` - Explain choice

**`select_patterns.py`**

Select relevant example files from inventory.

**Functions**:
- `search_inventory(capability, inventory)` - Search by capability
- `rank_by_relevance(examples, requirements)` - Relevance scoring
- `extract_key_patterns(example_file)` - Identify key code patterns

**`design_architecture.py`**

Generate component architecture and structure.

**Functions**:
- `design_model_struct(components)` - Create model definition
- `plan_message_handlers(interactions)` - Design Update() logic
- `generate_architecture_diagram(structure)` - ASCII diagram

**`generate_workflow.py`**

Create ordered implementation steps.

**Functions**:
- `break_into_phases(architecture)` - Phase planning
- `order_tasks_by_dependency(tasks)` - Dependency sorting
- `estimate_time(task)` - Time estimation
- `generate_workflow_document(phases)` - Formatted output

### Utility Scripts

**`utils/inventory_loader.py`**

Load and parse the examples inventory.

**Functions**:
- `load_inventory(path)` - Load CONTEXTUAL-INVENTORY.md
- `parse_inventory_markdown(content)` - Parse structure
- `build_capability_index(inventory)` - Index by capability
- `search_by_keyword(keyword, inventory)` - Keyword search

**`utils/component_matcher.py`**

Component matching and scoring logic.

**Functions**:
- `match_score(requirement, component)` - Relevance score
- `find_best_match(requirements, components)` - Top match
- `suggest_combinations(requirements)` - Component combos

**`utils/template_generator.py`**

Generate code templates and scaffolding.

**Functions**:
- `generate_model_struct(components)` - Model struct code
- `generate_init_function(components)` - Init() implementation
- `generate_update_skeleton(messages)` - Update() skeleton
- `generate_view_skeleton(layout)` - View() skeleton

**`utils/ascii_diagram.py`**

Create ASCII architecture diagrams.

**Functions**:
- `draw_component_tree(structure)` - Tree diagram
- `draw_message_flow(flow)` - Flow diagram
- `draw_state_machine(states)` - State diagram

### Validator Scripts

**`utils/validators/requirement_validator.py`**

Validate requirement extraction quality.

**Functions**:
- `validate_description_clarity(description)` - Check clarity
- `validate_requirements_completeness(requirements)` - Completeness
- `suggest_clarifications(requirements)` - Ask for missing info

**`utils/validators/design_validator.py`**

Validate design outputs.

**Functions**:
- `validate_component_selection(components, requirements)` - Check fit
- `validate_architecture(architecture)` - Structural validation
- `validate_workflow_completeness(workflow)` - Ensure all steps

## Available Analyses

### 1. Requirement Analysis

**Function**: `extract_requirements(description)`

**Purpose**: Convert natural language to structured requirements

**Methodology**:
1. Tokenize description
2. Extract nouns (features, data types)
3. Extract verbs (interactions, actions)
4. Identify patterns (multi-view, progress, etc.)
5. Classify TUI archetype

**Output Structure**:
```python
{
    'archetype': str,  # file-manager, installer, dashboard, etc.
    'features': List[str],  # [navigation, selection, preview, ...]
    'interactions': {
        'keyboard': List[str],  # [arrow keys, enter, search, ...]
        'mouse': List[str]  # [click, drag, ...]
    },
    'data_types': List[str],  # [files, text, tabular, streaming, ...]
    'views': str,  # single, multi, tabbed
    'special_requirements': List[str]  # [validation, progress, real-time, ...]
}
```

**Interpretation**:
- Archetype determines recommended starting template
- Features map directly to component selection
- Interactions affect component configuration
- Data types influence model structure

**Validations**:
- Description not empty
- At least 1 feature identified
- Archetype successfully classified

### 2. Component Mapping

**Function**: `map_to_components(requirements, inventory)`

**Purpose**: Map requirements to specific Bubble Tea components

**Methodology**:
1. Match features to component capabilities
2. Score each component by relevance (0-100)
3. Select top matches (score > 70)
4. Identify component combinations
5. Provide alternatives for each selection

**Output Structure**:
```python
{
    'primary_components': [
        {
            'component': 'viewport.Model',
            'score': 95,
            'justification': 'Scrollable display for log content',
            'example_file': 'examples/pager/main.go',
            'key_patterns': ['viewport scrolling', 'content loading']
        }
    ],
    'supporting_components': [...],
    'styling': ['lipgloss for highlighting'],
    'alternatives': {
        'viewport.Model': ['pager package', 'custom viewport']
    }
}
```

**Scoring Criteria**:
- Feature coverage: Does component provide required features?
- Complexity match: Is component appropriate for requirement complexity?
- Common usage: Is this the typical choice for this use case?
- Ecosystem fit: Does it work well with other selected components?

**Validations**:
- At least 1 component selected
- All requirements covered by components
- No conflicting components

### 3. Pattern Selection

**Function**: `select_relevant_patterns(components, inventory)`

**Purpose**: Find most relevant example files to study

**Methodology**:
1. Search inventory by component usage
2. Filter by capability category
3. Rank by pattern complexity (simple → complex)
4. Select 3-5 most relevant
5. Extract specific code patterns to study

**Output Structure**:
```python
{
    'examples': [
        {
            'file': 'examples/pager/main.go',
            'capability': 'Content Viewing',
            'relevance_score': 90,
            'key_patterns': [
                'viewport.Model initialization',
                'content scrolling (lines 45-67)',
                'keyboard navigation (lines 80-95)'
            ],
            'study_order': 1,
            'estimated_study_time': '15 minutes'
        }
    ],
    'recommended_study_order': [1, 2, 3],
    'total_study_time': '45 minutes'
}
```

**Ranking Factors**:
- Component usage match
- Complexity appropriate to skill level
- Code quality and clarity
- Completeness of example

**Validations**:
- At least 2 examples selected
- Examples cover all selected components
- Study order is logical (simple → complex)

### 4. Architecture Design

**Function**: `design_architecture(components, patterns, requirements)`

**Purpose**: Create complete component architecture

**Methodology**:
1. Design model struct (state to track)
2. Plan Init() (initialization)
3. Design Update() message handling
4. Plan View() rendering
5. Create component hierarchy diagram
6. Design message flow

**Output Structure**:
```python
{
    'model_struct': str,  # Go code
    'init_logic': str,  # Initialization steps
    'message_handlers': {
        'tea.KeyMsg': str,  # Keyboard handling
        'tea.WindowSizeMsg': str,  # Resize handling
        # Custom messages...
    },
    'view_logic': str,  # Rendering strategy
    'diagrams': {
        'component_hierarchy': str,  # ASCII tree
        'message_flow': str,  # Flow diagram
        'state_machine': str  # State transitions (if multi-view)
    }
}
```

**Design Patterns Applied**:
- **Single Responsibility**: Each component handles one concern
- **Composition**: Complex UIs built from simple components
- **Message Passing**: All communication via tea.Msg
- **Elm Architecture**: Model-Update-View separation

**Validations**:
- Model struct includes all component instances
- All user interactions have message handlers
- View logic renders all components
- No circular dependencies

### 5. Workflow Generation

**Function**: `generate_implementation_workflow(architecture, patterns)`

**Purpose**: Create step-by-step implementation plan

**Methodology**:
1. Break into phases (Setup, Core, Polish, Test)
2. Identify tasks per phase
3. Order by dependency
4. Reference specific example files per task
5. Add testing checkpoints
6. Estimate time per phase

**Output Structure**:
```python
{
    'phases': [
        {
            'name': 'Phase 1: Setup',
            'tasks': [
                {
                    'task': 'Initialize Go module',
                    'reference': None,
                    'dependencies': [],
                    'estimated_time': '2 minutes'
                },
                {
                    'task': 'Install dependencies (bubbletea, lipgloss)',
                    'reference': 'See README in any example',
                    'dependencies': ['Initialize Go module'],
                    'estimated_time': '3 minutes'
                }
            ],
            'total_time': '5 minutes'
        },
        # More phases...
    ],
    'total_estimated_time': '2-3 hours',
    'testing_checkpoints': [
        'After Phase 1: go build succeeds',
        'After Phase 2: Basic display working',
        # ...
    ]
}
```

**Phase Breakdown**:
1. **Setup**: Project initialization, dependencies
2. **Core Components**: Implement main functionality
3. **Integration**: Connect components, message passing
4. **Polish**: Styling, help text, error handling
5. **Testing**: Comprehensive testing, edge cases

**Validations**:
- All tasks have clear descriptions
- Dependencies are acyclic
- Time estimates are realistic
- Testing checkpoints at each phase

### 6. Comprehensive Design Report

**Function**: `comprehensive_tui_design_report(description, inventory_path)`

**Purpose**: Generate complete TUI design combining all analyses

**Process**:
1. Execute requirement_analysis(description)
2. Execute component_mapping(requirements)
3. Execute pattern_selection(components)
4. Execute architecture_design(components, patterns)
5. Execute workflow_generation(architecture)
6. Generate code scaffolding
7. Create README outline
8. Compile comprehensive report

**Output Structure**:
```python
{
    'description': str,
    'generated_at': str,
    'tui_type': str,
    'summary': str,  # Executive summary
    'sections': {
        'requirements': {...},
        'components': {...},
        'patterns': {...},
        'architecture': {...},
        'workflow': {...}
    },
    'scaffolding': {
        'main_go': str,  # Basic main.go template
        'model_go': str,  # Model struct + Init/Update/View
        'readme_md': str  # README outline
    },
    'file_structure': {
        'recommended': [
            'main.go',
            'model.go',
            'view.go',
            'messages.go',
            'go.mod'
        ]
    },
    'next_steps': [
        '1. Review architecture diagram',
        '2. Study recommended examples',
        '3. Implement Phase 1 tasks',
        # ...
    ],
    'resources': {
        'documentation': [...],
        'tutorials': [...],
        'community': [...]
    }
}
```

**Report Sections**:

**Executive Summary** (auto-generated):
- TUI type and purpose
- Key components selected
- Estimated implementation time
- Complexity assessment

**Requirements Analysis**:
- Parsed requirements
- TUI archetype
- Feature list

**Component Selection**:
- Primary components with justification
- Alternatives considered
- Component interaction diagram

**Pattern References**:
- Example files to study
- Key patterns highlighted
- Recommended study order

**Architecture**:
- Model struct design
- Init/Update/View logic
- Message flow
- ASCII diagrams

**Implementation Workflow**:
- Phase-by-phase breakdown
- Detailed tasks with references
- Testing checkpoints
- Time estimates

**Code Scaffolding**:
- Basic `main.go` template
- Model struct skeleton
- Init/Update/View stubs

**Next Steps**:
- Immediate actions
- Learning resources
- Community links

**Validation Report**:
- Design completeness check
- Potential issues identified
- Recommendations

## Error Handling

### Missing Inventory

**Error**: Cannot locate charm-examples-inventory

**Cause**: Inventory path not provided or incorrect

**Resolution**:
1. Verify inventory path: `~/charmtuitemplate/vinw/charm-examples-inventory`
2. If missing, clone examples: `git clone https://github.com/charmbracelet/bubbletea examples`
3. Generate CONTEXTUAL-INVENTORY.md if missing

**Fallback**: Use minimal built-in component knowledge (less detailed)

### Unclear Requirements

**Error**: Cannot extract clear requirements from description

**Cause**: Description too vague or ambiguous

**Resolution**:
1. Validator identifies missing information
2. Generate clarifying questions
3. User provides additional details

**Clarification Questions**:
- "What type of data will the TUI display?"
- "Should it be single-view or multi-view?"
- "What are the main user interactions?"
- "Any specific visual requirements?"

**Fallback**: Make reasonable assumptions, note them in report

### No Matching Components

**Error**: No components found for requirements

**Cause**: Requirements very specific or unusual

**Resolution**:
1. Relax matching criteria
2. Suggest custom component development
3. Recommend closest alternatives

**Alternative Suggestions**:
- Break down into smaller requirements
- Use generic components (viewport, textinput)
- Suggest combining multiple components

### Invalid Architecture

**Error**: Generated architecture has structural issues

**Cause**: Conflicting component requirements or circular dependencies

**Resolution**:
1. Validator detects issue
2. Suggest architectural modifications
3. Provide alternative structures

**Common Issues**:
- **Circular dependencies**: Suggest message passing
- **Too many components**: Recommend simplification
- **Missing state**: Add required fields to model

## Mandatory Validations

All analyses include automatic validation. Reports include validation sections.

### Requirement Validation

**Checks**:
- ✅ Description is not empty
- ✅ At least 1 feature identified
- ✅ TUI archetype classified
- ✅ Interaction patterns detected

**Output**:
```python
{
    'validation': {
        'passed': True/False,
        'checks': [
            {'name': 'description_not_empty', 'passed': True},
            {'name': 'features_found', 'passed': True, 'count': 5},
            # ...
        ],
        'warnings': [
            'No mouse interactions specified - assuming keyboard only'
        ]
    }
}
```

### Component Validation

**Checks**:
- ✅ At least 1 component selected
- ✅ All requirements covered
- ✅ No conflicting components
- ✅ Reasonable complexity

**Warnings**:
- "Multiple similar components selected - may be redundant"
- "High complexity - consider breaking into smaller UIs"

### Architecture Validation

**Checks**:
- ✅ Model struct includes all components
- ✅ No circular dependencies
- ✅ All interactions have handlers
- ✅ View renders all components

**Errors**:
- "Missing message handler for [interaction]"
- "Circular dependency detected: A → B → A"
- "Unused component: [component] not rendered in View()"

### Workflow Validation

**Checks**:
- ✅ All phases have tasks
- ✅ Dependencies are acyclic
- ✅ Testing checkpoints present
- ✅ Time estimates reasonable

**Warnings**:
- "No testing checkpoint after Phase [N]"
- "Task [X] has no dependencies but should come after [Y]"

## Performance & Caching

### Inventory Loading

**Strategy**: Load once, cache in memory

- Load CONTEXTUAL-INVENTORY.md on first use
- Build search indices (by capability, component, keyword)
- Cache for session duration

**Performance**: O(1) lookup after initial O(n) indexing

### Component Matching

**Strategy**: Pre-computed similarity scores

- Build component-feature mapping at initialization
- Score calculations cached
- Incremental updates only

**Performance**: O(log n) search with indexing

### Diagram Generation

**Strategy**: Template-based with caching

- Use pre-built ASCII templates
- Cache generated diagrams
- Regenerate only on structure changes

**Performance**: O(n) where n = number of components

## Automatic Detection Keywords

This skill activates when you mention:

**Technologies**:
- Bubble Tea, bubbletea, charm, charmbracelet
- TUI, terminal UI, terminal interface
- Lipgloss, Tea Program

**Components**:
- spinner, progress, table, list, viewport, textarea, textinput
- pager, paginator, timer, stopwatch, filepicker, help
- tabs, views, autocomplete

**Design Actions**:
- design TUI, create TUI, build TUI, architect TUI, plan TUI
- automate TUI design, generate TUI, scaffold TUI
- design interface, create interface, build interface
- map components, select components

**TUI Types**:
- file manager, installer, package manager, dashboard
- form, wizard, configuration tool
- chat interface, log viewer, data viewer, text viewer
- monitoring tool, menu system, selector

**Patterns**:
- multi-view, composable views, tabbed interface
- progress tracking, form validation, data display
- keyboard navigation, mouse support
- real-time updates, streaming data

**Questions**:
- "how to design", "how to build", "how to structure"
- "which components", "what patterns", "best practices"
- "design a TUI for", "create interface for"
- "automate design process"

## Usage Examples

### Example 1: Simple Log Viewer

**User**: "Design a TUI for viewing log files with search"

**Response**:

```
TUI DESIGN: Log File Viewer

ARCHETYPE: Text Viewer

REQUIREMENTS ANALYSIS:
- View: Scrollable text display
- Interaction: Search, navigate matches
- Data: Text file (log lines)

COMPONENT SELECTION:

Primary Components:
1. viewport.Model - Scrollable text display
   Justification: Built for viewing large text content
   Example: examples/pager/main.go

2. textinput.Model - Search query input
   Justification: Standard text input for search
   Example: examples/textinput/main.go

Supporting:
- Lipgloss styles for match highlighting

ARCHITECTURE:

Model Struct:
```go
type model struct {
    viewport viewport.Model
    searchInput textinput.Model
    content []string
    searchMode bool
    matches []int
    currentMatch int
    ready bool
}
```

WORKFLOW:

Phase 1: Basic Viewer (30min)
- Load file into string array
- Initialize viewport
- Implement basic scrolling

Phase 2: Search (45min)
- Add textinput for search
- Toggle search mode with '/'
- Highlight matches

Phase 3: Navigation (20min)
- Navigate matches with n/N
- Show match counter

Total: ~2 hours

NEXT STEPS:
1. Study examples/pager/main.go for viewport usage
2. Study examples/textinput/main.go for input handling
3. Implement Phase 1
4. Test scrolling with large files
5. Add search in Phase 2
```

### Example 2: Installation Progress Tracker

**User**: "Create a package installer UI with progress bars"

**Response**:

```
TUI DESIGN: Package Installer

ARCHETYPE: Installer/Progress Tracker

REQUIREMENTS ANALYSIS:
- View: Progress indication for multiple packages
- Interaction: Minimal (automated process)
- Data: Package list, progress per package
- Special: Sequential installation, visual feedback

COMPONENT SELECTION:

Primary Components:
1. progress.Model - Individual package progress
   Justification: Animated progress visualization
   Example: examples/progress-animated/main.go

2. spinner.Model - Loading indicator
   Justification: Feedback during package download
   Example: examples/spinner/main.go

Reference Pattern:
- examples/package-manager/main.go - Complete implementation

ARCHITECTURE:

Model Struct:
```go
type model struct {
    packages []Package
    currentIdx int
    progress progress.Model
    spinner spinner.Model
    installed []string
    err error
}

type Package struct {
    name string
    status string // pending, installing, done
}
```

Message Flow:
Install Start → Download Package → Update Progress → Package Done → Next Package

WORKFLOW:

Phase 1: Package List (20min)
- Define Package struct
- Initialize list of packages
- Display package names

Phase 2: Add Progress (30min)
- Initialize progress.Model per package
- Update on install progress messages
- Handle completion

Phase 3: Add Spinner (15min)
- Add spinner during download
- Stop when installation starts

Phase 4: Sequential Logic (30min)
- Implement install queue
- Sequential execution
- Completion handling

Total: ~2 hours

REFERENCE STUDY:
1. examples/package-manager/main.go (main reference)
   - Lines 50-80: Progress + spinner combo
   - Lines 120-145: Sequential installation
   - Lines 200-230: Completion handling

NEXT STEPS:
1. Clone package-manager example structure
2. Customize for your package list
3. Add package-specific install logic
4. Test with mock installations
```

### Example 3: Configuration Wizard

**User**: "Build a multi-step configuration wizard with validation"

**Response**:

```
TUI DESIGN: Configuration Wizard

ARCHETYPE: Multi-Step Form

REQUIREMENTS ANALYSIS:
- View: Multi-step (multiple screens)
- Interaction: Form input, validation, navigation
- Data: Configuration fields (text, selections)
- Special: Validation per field, step navigation

COMPONENT SELECTION:

Primary Components:
1. textinput.Model (array) - Multiple input fields
   Justification: Standard form inputs
   Example: examples/textinputs/main.go

2. State machine for steps
   Justification: Multi-step workflow
   Example: examples/views/main.go

Reference Pattern:
- examples/credit-card-form/main.go - Form validation

ARCHITECTURE:

Model Struct:
```go
type model struct {
    currentStep int
    steps []Step
    inputs []textinput.Model
    focusIdx int
    err error
}

type Step struct {
    name string
    fields []Field
    valid bool
}
```

State Machine:
Step 1 (Basic Info) → Step 2 (Advanced) → Step 3 (Confirm) → Done

WORKFLOW:

Phase 1: Basic Form (45min)
- Create input array
- Implement focus management
- Basic key handling (tab, enter)

Phase 2: Add Steps (30min)
- Define Step struct
- Implement step navigation
- Show current step indicator

Phase 3: Validation (45min)
- Add validators to each input
- Show validation errors
- Prevent next step if invalid

Phase 4: Polish (30min)
- Add progress indicator
- Help text per step
- Confirmation screen

Total: ~2.5 hours

REFERENCE STUDY ORDER:
1. examples/textinputs/main.go (focus management)
2. examples/credit-card-form/main.go (validation pattern)
3. examples/views/main.go (multi-view state machine)

NEXT STEPS:
1. Start with textinputs example
2. Add step state management
3. Implement validators
4. Build confirmation view
```

### Example 4: File Manager

**User**: "Design a file manager TUI like ranger"

**Response**:

```
TUI DESIGN: File Manager

ARCHETYPE: File Manager

REQUIREMENTS ANALYSIS:
- View: Three-column (parent, current, preview)
- Interaction: Keyboard navigation, selection
- Data: File system hierarchy
- Special: File preview, directory traversal

COMPONENT SELECTION:

Primary Components:
1. filepicker.Model - File navigation
   Justification: Built-in file system navigation
   Example: examples/file-picker/main.go
   Alternative: Custom with list.Model for more control

2. viewport.Model - File preview
   Justification: Preview pane for selected file
   Example: examples/pager/main.go

3. Lipgloss layout - Three-column layout
   Justification: Side-by-side panels
   Example: examples/split-editors/main.go (two-pane reference)

ARCHITECTURE:

Model Struct:
```go
type model struct {
    parentList list.Model    // Parent directory
    currentList list.Model   // Current directory
    preview viewport.Model   // File preview
    currentDir string
    selectedFile string
    width int
    height int
}
```

Layout:
┌────────────┬─────────────┬──────────────┐
│  Parent    │   Current   │   Preview    │
│  Dir       │   Dir       │   Pane       │
│            │             │              │
│  ../       │ > file1.txt │ File content │
│  docs/     │   file2.go  │ ...          │
│  src/      │   dir/      │              │
└────────────┴─────────────┴──────────────┘

WORKFLOW:

Phase 1: Single Dir Nav (1h)
- Implement current directory listing
- Arrow key navigation
- Directory entry/exit

Phase 2: Three-Pane Layout (1h)
- Add parent directory pane
- Add preview pane
- Lipgloss layout

Phase 3: File Preview (45min)
- Load file content on selection
- Show in preview pane
- Handle large files

Phase 4: Polish (45min)
- File type icons/colors
- Status bar
- Help overlay

Total: ~3.5 hours

REFERENCE STUDY:
1. examples/file-picker/main.go - File system navigation
2. examples/list-fancy/main.go - Custom list styling
3. examples/pager/main.go - Content preview
4. examples/split-editors/main.go - Multi-pane layout

NEXT STEPS:
1. Start with file-picker for navigation logic
2. Build three-pane layout
3. Add preview functionality
4. Style with Lipgloss
```

### Example 5: Quick Component Lookup

**User**: "Which component for a dropdown menu?"

**Response**:

```
COMPONENT RECOMMENDATIONS: Dropdown Menu

Since Bubble Tea doesn't have a built-in dropdown component, here are the best approaches:

1. list.Model (Recommended)
   - Display as temporary list overlay
   - Filter on keypress
   - Select with Enter
   - Example: examples/list-simple/main.go
   - Customization: Use ItemDelegate for dropdown styling

2. autocomplete
   - Text input with suggestions below
   - Good for searchable dropdowns
   - Example: examples/autocomplete/main.go
   - Use case: Large option lists

3. Custom with viewport
   - Full control over appearance
   - Scrollable for many options
   - Example: examples/viewport/main.go (for scrolling)
   - Build: Overlay viewport on trigger

IMPLEMENTATION PATTERN:

```go
type model struct {
    dropdownOpen bool
    dropdownList list.Model
    selectedValue string
}

func (m model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    switch msg := msg.(type) {
    case tea.KeyMsg:
        if msg.String() == "enter" && !m.dropdownOpen {
            // Open dropdown
            m.dropdownOpen = true
            return m, nil
        }
        if m.dropdownOpen {
            // Delegate to list
            var cmd tea.Cmd
            m.dropdownList, cmd = m.dropdownList.Update(msg)
            return m, cmd
        }
    }
    return m, nil
}
```

RECOMMENDED APPROACH:
Use list.Model in "dropdown mode" - render as overlay when open, hide when closed.

Study: examples/list-simple/main.go
```

---

**Total Word Count**: ~7,200 words

This comprehensive skill documentation provides:
- Clear activation criteria
- Complete workflow explanations
- Detailed function documentation
- Architecture patterns
- Error handling guidance
- Extensive usage examples
- Integration with charm-examples-inventory
