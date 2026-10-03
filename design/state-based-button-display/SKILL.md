---
memory_layer: durable_knowledge
para_section: pages/skills/state-based-button-display
gigabrain_tags: ui, button, state-based, navigation, modal, layout
openstinger_context: ui-design, button-layout, page-structure
last_updated: 2026-03-30
related_docs:
  - https://github.com/Construct-AI-primary/construct_ai/blob/main/docs/codebase/procedures/ui-frontend/0000_STATE_BASED_BUTTON_DISPLAY_PROCEDURE.md
  - https://github.com/Construct-AI-primary/construct_ai/blob/main/docs/codebase/procedures/ui-frontend/0000_MODAL_DESIGN_PROCEDURE.md
  - https://github.com/Construct-AI-primary/construct_ai/blob/main/docs/pages-design/0000_PAGE_ARCHITECTURE_GUIDE.md
related_skills:
  - modal-design
  - page-architecture
  - ui-configuration-validation
frequency_percent: 85.0
success_rate_percent: 94.2
---

# State-Based Button Display Skill

## Overview

Systematic implementation of state-based button displays with navigation structures, modal triggering, and responsive layouts. This skill covers the complete Construct AI page architecture pattern for organizing UI elements by state, ensuring consistent user experience across all pages.

## When to Use This Skill

**Trigger Conditions:**
- Creating new pages with multiple functional states
- Adding state-based navigation to existing pages
- Implementing modal trigger buttons organized by state
- Setting up page navigation with state transitions
- Creating responsive button layouts for different screen sizes
- Organizing page functionality into logical state groups

## Step-by-Step Procedure

### Step 1: Analyze Page State Requirements
```javascript
// Define the states your page needs
const PAGE_STATES = {
  agents: {
    label: 'Agents',
    emoji: '🤖',
    description: 'AI agent interactions',
    buttonCount: 4
  },
  upserts: {
    label: 'Upserts',
    emoji: '📤',
    description: 'Data modification operations',
    buttonCount: 3
  },
  workspace: {
    label: 'Workspace',
    emoji: '🗂️',
    description: 'Workspace management',
    buttonCount: 4
  }
};
```

**Key Considerations:**
- What functional areas does the page serve?
- How many buttons per state (typically 2-4)?
- Are there discipline-specific state names needed?
- What's the primary user workflow?

### Step 2: Implement State Management
```javascript
import React, { useState, useEffect } from 'react';

const PageComponent = () => {
  // Core state management
  const [currentState, setCurrentState] = useState('agents');
  const [isButtonContainerVisible, setIsButtonContainerVisible] = useState(false);

  // State-specific state variables
  const [activeAgent, setActiveAgent] = useState(null);
  const [showWorkspaceComponent, setShowWorkspaceComponent] = useState(false);

  // State change handler with cleanup
  const handleStateChange = (newState) => {
    setCurrentState(newState);

    // State-specific cleanup
    if (newState !== 'agents') {
      setActiveAgent(null);
    }

    if (newState !== 'workspace') {
      setShowWorkspaceComponent(false);
    }
  };

  // Button container animation
  useEffect(() => {
    const timer = setTimeout(() => {
      setIsButtonContainerVisible(true);
    }, 100);
    return () => clearTimeout(timer);
  }, []);

  return (
    <PageStructure
      currentState={currentState}
      onStateChange={handleStateChange}
      isButtonContainerVisible={isButtonContainerVisible}
    />
  );
};
```

### Step 3: Create Navigation Structure
```html
<!-- Fixed bottom navigation -->
<div className="page-navigation-container">
  <div className="page-nav-row">
    {Object.entries(STATE_CONFIG).map(([key, config]) => (
      <button
        key={key}
        className={`state-button ${currentState === key ? 'active' : ''}`}
        onClick={() => handleStateChange(key)}
      >
        {config.emoji} {config.label}
      </button>
    ))}
  </div>
  <button className="nav-button primary">
    {pageTitle}
  </button>
</div>
```

**Navigation CSS:**
```css
.page-navigation-container {
  position: fixed;
  left: 50%;
  bottom: 10px;
  transform: translateX(-50%);
  z-index: 200;
  pointer-events: none;
}

.page-nav-row {
  display: flex;
  gap: 10px;
  margin-bottom: 10px;
  pointer-events: auto !important;
}

.state-button {
  pointer-events: auto !important;
  background: white;
  border: 2px solid #FF8C00;
  border-radius: 20px;
  padding: 8px 16px;
  cursor: pointer;
  transition: all 0.2s;
  font-weight: 600;
  color: #333;
}

.state-button:hover {
  background: #FFF8F0;
  transform: translateY(-2px);
}

.state-button.active {
  background: #FF8C00;
  color: white;
  border-color: #FF8C00;
}
```

### Step 4: Design Button Layout Grid
```css
/* 2x2 Grid (Most Common) */
.button-container {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10px;
  max-width: 600px;
  padding: 30px;
  justify-items: center;
  align-items: center;
  z-index: 10;
  background: rgba(255, 255, 255, 0.95);
  border-radius: 12px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.button-container.visible {
  opacity: 1;
}

/* Alternative layouts */
.button-container-1x4 {
  grid-template-columns: 1fr;
  gap: 15px;
}

.button-container-3x2 {
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
}
```

### Step 5: Implement Modal Trigger Buttons
```javascript
const ButtonContainer = ({ currentState, buttons, onOpenModal, pageId, isVisible }) => {
  const renderStateButtons = (stateButtons) => {
    return stateButtons.map((button, index) => (
      <button
        key={index}
        className="modal-trigger-button"
        onClick={() => onOpenModal(button.modalId, {
          modalTitle: button.modalTitle,
          triggerPage: pageId,
        })}
        disabled={button.disabled}
      >
        {button.emoji && <span>{button.emoji}</span>}
        {button.label}
      </button>
    ));
  };

  return (
    <div className={`button-container ${isVisible ? 'visible' : ''}`}>
      {currentState === 'agents' && renderStateButtons(buttons.agents)}
      {currentState === 'upserts' && renderStateButtons(buttons.upserts)}
      {currentState === 'workspace' && renderStateButtons(buttons.workspace)}
    </div>
  );
};
```

**Button Styling:**
```css
.modal-trigger-button {
  background: white;
  border: 2px solid #FF8C00;
  border-radius: 8px;
  padding: 12px 20px;
  cursor: pointer;
  font-size: 16px;
  font-weight: 500;
  min-width: 200px;
  text-align: center;
  color: #333;
  transition: all 0.2s ease;
}

.modal-trigger-button:hover {
  background: #FFF8F0;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.modal-trigger-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
}
```

### Step 6: Configure Button Arrays by State
```javascript
// Button configuration by state
const BUTTONS_BY_STATE = {
  agents: [
    {
      label: '🤖 AI Analysis',
      modalId: 'AnalysisModal',
      modalTitle: 'AI Analysis',
    },
    {
      label: '📊 Generate Report',
      modalId: 'ReportModal',
      modalTitle: 'Generate Report',
    },
    {
      label: '⚙️ Settings',
      modalId: 'SettingsModal',
      modalTitle: 'Settings',
    },
    {
      label: '📧 Correspondence',
      modalId: 'CorrespondenceModal',
      modalTitle: 'Correspondence',
    },
  ],

  upserts: [
    {
      label: '☁️ Cloud Import',
      modalId: 'CloudImportModal',
      modalTitle: 'Cloud Import',
    },
    {
      label: '🌐 URL Import',
      modalId: 'UrlImportModal',
      modalTitle: 'Import from URL',
    },
    {
      label: '📄 File Upload',
      modalId: 'FileUploadModal',
      modalTitle: 'Upload Files',
    },
  ],

  workspace: [
    {
      label: '🗂️ Manage Files',
      modalId: 'FileManagerModal',
      modalTitle: 'Manage Files',
    },
    {
      label: '📈 Dashboard',
      modalId: 'DashboardModal',
      modalTitle: 'Dashboard',
    },
    {
      label: '👥 User Management',
      modalId: 'UserManagerModal',
      modalTitle: 'User Management',
    },
    {
      label: '🔧 Configuration',
      modalId: 'ConfigModal',
      modalTitle: 'Configuration',
    },
  ],
};
```

### Step 7: Implement Modal Trigger Handler
```javascript
const handleOpenModal = (modalId, modalProps = {}) => {
  // Track which page opened the modal
  window.currentModalTriggerPage = modalProps.triggerPage;

  // Set active agent for agent state
  if (currentState === 'agents') {
    const agentMap = {
      CorrespondenceModal: 'correspondence',
      AnalysisModal: 'analysis',
      ReportModal: 'report-generation',
    };
    setActiveAgent(agentMap[modalId]);
  }

  // Open the modal
  openModal(modalId, modalProps);
};
```

### Step 8: Add Responsive Design
```css
/* Mobile adjustments */
@media (max-width: 768px) {
  .button-container {
    grid-template-columns: 1fr;
    padding: 20px;
    gap: 15px;
  }

  .modal-trigger-button {
    min-width: 250px;
    padding: 15px 25px;
  }

  .page-navigation-container {
    bottom: 5px;
  }
}

/* Tablet adjustments */
@media (min-width: 769px) and (max-width: 1024px) {
  .button-container {
    max-width: 500px;
    padding: 25px;
  }
}
```

### Step 9: Add Page Background and Chatbot
```javascript
// Get themed background image
const backgroundImagePath = getThemedImagePath(`${pageId}.png`);

// Page structure
return (
  <div
    className="page-container"
    style={{ backgroundImage: `url(${backgroundImagePath})` }}
  >
    <NavigationComponent
      currentState={currentState}
      onStateChange={handleStateChange}
      pageTitle={pageTitle}
    />

    <ButtonContainerComponent
      currentState={currentState}
      buttons={BUTTONS_BY_STATE}
      onOpenModal={handleOpenModal}
      pageId={pageId}
      isVisible={isButtonContainerVisible}
    />

    <ChatbotBase
      pageId={pageId}
      disciplineCode={DISCIPLINE_CODE}
      userId={window.currentUser?.id || 'demo-user'}
      chatType="document"
      title={`${pageTitle} Assistant`}
      welcomeTitle={`${pageTitle} Command Center`}
      welcomeMessage={`I can help with ${pageTitle.toLowerCase()} operations.`}
    />
  </div>
);
```

### Step 10: Test State Transitions
```javascript
// Test all state transitions
const testStateTransitions = () => {
  const states = Object.keys(STATE_CONFIG);

  states.forEach(state => {
    // Simulate state change
    handleStateChange(state);

    // Verify button container updates
    const expectedButtons = BUTTONS_BY_STATE[state];
    const actualButtons = getCurrentButtons();

    console.assert(
      actualButtons.length === expectedButtons.length,
      `State ${state}: Expected ${expectedButtons.length} buttons, got ${actualButtons.length}`
    );
  });
};
```

## Success Criteria

- [ ] Navigation buttons positioned correctly (bottom center)
- [ ] State transitions work smoothly
- [ ] Button container displays correct buttons for each state
- [ ] Modal triggering works for all buttons
- [ ] Layout is responsive on mobile/tablet
- [ ] Hover effects and animations work
- [ ] No layout conflicts with other page elements
- [ ] Chatbot integration works correctly

## Common Pitfalls

1. **Pointer Events Issues** - Container blocks clicks unless properly configured
2. **Z-Index Conflicts** - Navigation hidden behind other elements
3. **State Cleanup Missing** - State-specific variables not reset on transition
4. **Modal ID Mismatches** - Modal IDs don't match component names
5. **Responsive Layout Breaks** - Grid doesn't adapt to small screens

## State Configuration Patterns

### Generic Pattern (Most Common)
```javascript
const STATE_CONFIG = {
  agents: { label: 'Agents', emoji: '🤖' },
  upserts: { label: 'Upserts', emoji: '📤' },
  workspace: { label: 'Workspace', emoji: '🗂️' }
};
```

### Discipline-Specific Pattern
```javascript
const STATE_CONFIG = {
  agents: { label: 'Agents', emoji: '🤖' },
  suppliers: { label: 'Suppliers', emoji: '📤' }, // Instead of upserts
  vetting: { label: 'Vetting', emoji: '🗂️' }, // Instead of workspace
  simulator: { label: 'Simulator', emoji: '🔄' } // Additional state
};
```

## Cross-References

### Related Procedures
- [State-Based Button Display Procedure](https://github.com/Construct-AI-primary/construct_ai/blob/main/docs/codebase/procedures/ui-frontend/0000_STATE_BASED_BUTTON_DISPLAY_PROCEDURE.md) - Complete implementation guide
- [Modal Design Procedure](https://github.com/Construct-AI-primary/construct_ai/blob/main/docs/codebase/procedures/ui-frontend/0000_MODAL_DESIGN_PROCEDURE.md) - Modal design patterns
- [Page Architecture Guide](https://github.com/Construct-AI-primary/construct_ai/blob/main/docs/pages-design/0000_PAGE_ARCHITECTURE_GUIDE.md) - Page structure guidelines

### Related Skills
- `modal-design` - Designing modal components
- `page-architecture` - Overall page structure
- `ui-configuration-validation` - Validating UI configurations

### Related Agents
- `DevForge_AI_Team` - Implementation assistance
- `QualityForge_AI_Team` - Layout validation

## Example Implementation

```javascript
// Complete page implementation
const ProcurementPage = () => {
  const [currentState, setCurrentState] = useState('agents');
  const [isVisible, setIsVisible] = useState(false);

  const handleStateChange = (newState) => {
    setCurrentState(newState);
    // State-specific cleanup
    if (newState !== 'agents') setActiveAgent(null);
  };

  const handleOpenModal = (modalId, modalProps) => {
    window.currentModalTriggerPage = '01900-procurement';
    if (currentState === 'agents') {
      const agentMap = {
        CorrespondenceModal: 'correspondence',
        OrderProcessModal: 'order-process'
      };
      setActiveAgent(agentMap[modalId]);
    }
    openModal(modalId, modalProps);
  };

  return (
    <div className="page-container">
      <NavigationComponent
        currentState={currentState}
        onStateChange={handleStateChange}
        states={STATE_CONFIG}
      />

      <ButtonContainerComponent
        currentState={currentState}
        buttons={BUTTONS_BY_STATE}
        onOpenModal={handleOpenModal}
        pageId="01900"
        isVisible={isVisible}
      />

      <ChatbotBase
        pageId="01900"
        disciplineCode="PROCUREMENT"
        title="Procurement Assistant"
      />
    </div>
  );
};
```

## Performance Metrics

- **Average Implementation Time:** 60-90 minutes
- **Success Rate:** 94.2%
- **Frequency:** Used in 85% of page implementations
- **Layout Consistency:** 96% match design specifications

## Grid Layout Templates

```css
/* Standard 2x2 grid */
.grid-2x2 { grid-template-columns: repeat(2, 1fr); }

/* Single column for mobile */
.grid-1x4 { grid-template-columns: 1fr; }

/* Three columns for wide layouts */
.grid-3x2 { grid-template-columns: repeat(3, 1fr); }

/* Four columns for complex layouts */
.grid-4x1 { grid-template-columns: repeat(4, 1fr); }
```

This skill ensures consistent, professional state-based button displays across all Construct AI pages, following established design patterns and responsive principles.