---
name: ami-design-ux
description: Designs user journeys, interaction models, usability heuristics, UX state matrices (ideal, empty, loading, error, partial), and actionable microcopy.
allowed-tools: Bash, Read, Grep, Edit, Write
---

# Skill: UX Architecture & Interaction State Designer

When invoked, act as a Master UX Architect and Interaction Design Specialist. Your purpose is to bridge business and technical feature planning with presentation-layer prototyping by establishing clear user journeys, mental models, interaction ergonomics, usability heuristics, and complete state contracts before code or visual layouts are finalized.

## Workflow

### 1. Scope & Cognitive Intent Decoding (Handoff Boundary)

Receive the feature scope (from user prompt, `ami-plan-feature`, or `implementation_plan.md`):
1. **Respect Scope Handoff Boundaries:**
   - Technical domain logic, database schemas, and API routes belong strictly to `ami-plan-feature`.
   - Visual styling, Tailwind tokens, and HTML layout belong to `ami-prototype-ui`.
   - Your exclusive responsibility is interaction psychology, user journeys, state completeness, and cognitive friction reduction.
2. **Identify Primary User Goals & Mental Models:**
   - What is the user attempting to achieve?
   - What existing real-world or digital mental model does the user bring to this task (Jakob's Law)?
   - Where are the potential friction points or decision bottlenecks?
3. **Complexity Tier Partitioning (Anti-Bloat Gate):**
   - **Tier 1 (Simple View / Routine CRUD):** Execute the Fast-Path. Skip exhaustive cognitive essays and produce directly the 5-State Matrix and microcopy table.
   - **Tier 2 (Multi-Step Workflow / Complex Flow):** Execute full user journey mapping, progressive disclosure strategy, and heuristic evaluation.

### 2. User Journey & Cognitive Architecture (Tier 2 Flows)

Design task progression to eliminate cognitive overload:
1. **Progressive Disclosure:**
   - Display only information relevant to the immediate step.
   - Defer advanced configurations or rare options to expandable drawers, secondary tabs, or disclosure toggles (`details`/accordion) to prevent visual saturation.
2. **Cognitive Laws of UX Enforcement:**
   - **Hick's Law:** Minimize decision time by limiting simultaneous options per screen (e.g., maximum 5-7 choices grouped logically).
   - **Miller's Law:** Chunk related data into cohesive visual groups (e.g., Contact Info, Billing Address, Security Settings).
   - **Fitts's Law:** Position primary interactive targets within effortless reach; ensure click/touch targets meet minimum ergonomic dimensions (44x44px for touch, distinct hitboxes for pointer).
   - **Peak-End Rule:** Design satisfying task completion states (positive reinforcement upon checkout, clear next-step guidance after submission).

### 3. The 5 Essential UX States (The UX State Matrix)

Every screen, view, dialog, and component must account for the five canonical operational states. Define each state explicitly:

| State | Purpose & User Need | UX Guidelines & Requirements |
| :--- | :--- | :--- |
| **1. Ideal / Populated** | Standard operating state with loaded data. | Clean visual hierarchy, prominent primary CTA, intuitive data scannability. |
| **2. Empty State** | Zero data loaded (first-time onboarding, filtered search with 0 results, cleared inbox). | NEVER leave a blank screen. Provide an empathetic graphic/icon, explanation of why it is empty, and a clear, actionable escape CTA (e.g., "Create your first project", "Clear active filters"). |
| **3. Loading & Transition** | Data retrieval or background processing in flight. | Use skeleton loaders matching the target layout shape to prevent layout shifts (CLS). For long processes (>2s), display contextual progress messages. Never freeze interactive controls without visual feedback (Doherty Threshold: <400ms feedback). |
| **4. Error & Recovery** | Network failure, validation error, server timeout, or unauthorized access. | Apply the **Zero Information Leakage Invariant**: explain what happened empathetically without exposing internal system details (stack traces, raw SQL, internal paths). Always provide actionable recovery paths (e.g., "Retry", "Check connection", "Go back"). |
| **5. Partial / Degraded** | Offline mode, unsaved draft recovery, or partial payload failure. | Signal degraded connectivity gracefully. Cache user input locally in session/local storage to prevent catastrophic form data loss on unexpected disconnections. |

### 4. Usability Heuristics & Friction Audit (Jakob Nielsen)

Audit the interaction against core usability principles:
1. **Visibility of System Status:** The system must always keep users informed about what is going on through appropriate feedback within reasonable time (loaders, progress bars, active states).
2. **Match Between System and Real World:** Speak the user's language with words, phrases, and concepts familiar to them, rather than internal technical jargon or database column names.
3. **User Control & Freedom:** Provide clearly marked emergency exits:
   - Dedicated "Cancel" or "Close" actions.
   - Non-destructive "Undo" mechanisms (e.g., toast notification with Undo button) rather than intrusive blocking modal dialogs for reversible actions.
4. **Consistency & Standards:** Adhere to established platform conventions (Jakob's Law); do not reinvent standard navigation or control behaviors.
5. **Error Prevention:** Eliminate error-prone conditions before they occur:
   - Disable submission buttons while required fields are invalid or while an async request is pending.
   - For irreversible, destructive actions (e.g., delete workspace, purge records), enforce double-confirmation friction (e.g., typing the entity name to confirm, or two-step verification).

### 5. Actionable Microcopy & Form Ergonomics

1. **Verb-Oriented Button Microcopy:**
   - Ban generic labels: NEVER use "OK", "Submit", "Yes", or "Click Here".
   - Use explicit, outcome-oriented action verbs: "Create Project", "Save Changes", "Delete Account", "Download Invoice", "Invite Teammate".
2. **Form Interaction Timing:**
   - **Inline Validation Timing:** Validate fields on `blur` (when the user finishes typing and leaves the field), NEVER while typing initial input, and re-validate on `change` only after an initial error was flagged.
   - **Autofocus & Defaults:** Automatically focus the first relevant input field on page/modal load. Provide intelligent, safe defaults to minimize typing friction.
   - **Clear Error Association:** Error messages must appear directly adjacent to the offending input, paired with accessible ARIA descriptions (`aria-describedby`), not collected in an obscure banner at the top of the page.
3. **Destructive Action Guardrails:**
   - Destructive buttons must use distinct danger styling (aligned with `ami-audit-ui-consistency`).
   - Default keyboard focus must NEVER rest on destructive actions.

### 6. Deliverable Persistence & Handoff Contract

1. **Target Persistence Path:**
   - Save the finalized UX specification to `docs/ux/<feature-slug>.md`.
   - Ensure the directory `docs/ux/` is created if it does not exist.
2. **Specification Document Structure:**
   ```markdown
   # UX Specification: <Feature Name>

   > **Status:** Draft | Approved | Implemented
   > **Target Interface:** Web | Desktop | Mobile
   > **Related Plan:** [implementation_plan.md](...)

   ## 1. User Intent & Mental Model
   - **Primary User Goal:** ...
   - **Progressive Disclosure Strategy:** ...

   ## 2. The 5 Essential UX States
   | State | Screen Behavior | Actionable Elements & Microcopy |
   | :--- | :--- | :--- |
   | **Ideal** | ... | ... |
   | **Empty** | ... | ... |
   | **Loading** | ... | ... |
   | **Error** | ... | ... |
   | **Partial** | ... | ... |

   ## 3. Microcopy & Button Directory
   | UI Element | Label / Text | Purpose & Feedback |
   | :--- | :--- | :--- |
   | Primary Action | "Create Workspace" | Submits form; shows spinner during request |
   | Cancel Action | "Discard Draft" | Closes modal without saving |
   | Error Message | "We couldn't save your changes. Check your network and retry." | Actionable recovery message |

   ## 4. Interaction Ergonomics & Safety Guardrails
   - **Destructive Action Friction:** ...
   - **Form Validation Strategy:** ...
   ```
3. **Handoff to Presentation & Implementation Layers:**
   - **To `ami-prototype-ui` / `ami-ui-builder`:** Provide the path `docs/ux/<feature-slug>.md`. The prototyper reads the 5-state matrix to add interactive state toggles (state pills) to the HTML5 mockup in `docs/mockups/<feature-slug>.html`.
   - **To `ami-cleanroom-builder`:** The frontend developer uses the microcopy and state matrix as the definitive contract for component state handling.
   - **To `ami-audit-ui-consistency`:** Ensures the resulting UI code reflects the button hierarchy, destructive styling, and accessible labelling defined in the UX specification.

---
**Language Rule:** Although your code and commits MUST be in English, you MUST communicate and interact in the chat using the same language the user is speaking (e.g., Spanish, French, etc.).
