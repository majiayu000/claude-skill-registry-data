---
name: ui-surface-inventory
description: Identify the product's UI scopes (inspectable areas), classify them by type (App Shell, Journey, Route, Sub-surface), note component candidates within each scope, and recommend a prioritized recovery or specification order. Use this as the first step for large-scale projects or when performing Retrospective Specification Recovery on an existing app.
status: stable
---

# UI Surface Inventory

A skill for mapping the landscape of a product's interface before diving into deep specification work. It helps prevent "scope bloat" by breaking the app down into coherent, manageable units called **UI Scopes**.

## When to use this skill

Use this skill when:
- **Spec Recovery:** An implementation already exists and you need to decide what to specify first.
- **Large-scale projects:** You are starting a new feature or product that is too complex for a single `ui-brief`.
- **Scope Confusion:** The user is struggling to define the boundaries of a feature or is trying to specify too much at once.

Do **not** use this skill when:
- The task is a small, well-defined feature (e.g., "Add a 'forgot password' link").
- The UI scope is already clearly defined and agreed upon.

## Core principle

**Identify coherent scopes first.** Do not run one giant Retrospective Specification Recovery on the whole app. A giant recovery mixes navigation, screens, journey logic, and visual styling into one fuzzy document. Instead, identify the product's UI scopes and recommend a prioritized order for recovery.

## The "Smallest Coherent Scope" Test

A **smallest coherent scope** should meet these criteria:
- **User Job:** It has a specific job the user is trying to accomplish.
- **Boundary:** It has a clear visual or logical boundary.
- **States:** It has its own internal states (loading, empty, error, active).
- **Acceptance Criteria:** It can have its own independent success criteria.

## Scope Classification

| Layer                   | Example                                | What it owns                   |
| ----------------------- | -------------------------------------- | ------------------------------ |
| **App Shell**           | Left sidebar, header, project switcher | Navigation frame               |
| **Journey**             | Content journey                        | Cross-route flow               |
| **Route**               | `/create` page                         | One page’s layout and behavior |
| **Sub-surface**         | AI review panel, wizard, modal         | Meaningful area inside a route |
| **Component candidate** | Nav item, post card, approve button    | Reusable UI piece; candidate for `ui-component-spec` |

## Workflow

### Step 1 — Scan the product

If performing **Spec Recovery**, browse the existing app or review provided screenshots/DOM trees. If starting a **New Project**, discuss the high-level goals with the user.

Identify:
- Persistent navigation and framing (App Shell).
- Major user journeys and flows (Journeys).
- Individual pages and URLs (Routes).
- Complex, reusable interactive units (Component candidates; record them inside sub-surfaces).

### Step 2 — Filter and Classify

Apply the "Smallest Coherent Scope" test. Group related items into their respective layers.

### Step 3 — Prioritize

Recommend a recovery or specification order. Generally, the order should be:
1. **App Shell:** Establishes the frame and global navigation.
2. **Journey maps:** Establishes the "connective tissue" between routes.
3. **Primary Routes:** The core screens where the most important actions happen.
4. **Sub-surfaces:** Modals, wizards, or complex cards within routes.

### Step 4 — Produce the surface-inventory.md

Use the template below. The canonical filename is strictly `surface-inventory.md`. Save as `surface-inventory.md` in the root of the spec package directory (or the project root if mapping a whole app).

## Output template

```markdown
---
spec_type: inventory
spec_id: <project-slug>-surface-inventory
created: <YYYY-MM-DD>
status: draft
surface_type: multi-surface-map
---

# UI Surface Inventory: <Project Name>

## 1. Purpose
<One-sentence description of the goal of this inventory.>

## 2. Source evidence
<List of files, URLs, or screenshots used to derive this inventory.>
- `path/to/source/files`
- `https://app.example.com/route`

## 3. App Shell Scopes
- [ ] **<Scope Name>**: <One sentence description of role and what it owns>
- [ ] **Example**: Left sidebar navigation (owns nav order, labels, active states)

## 4. Journey Scopes
- [ ] **<Scope Name>**: <Describes the cross-route flow or logic it owns>
- [ ] **Example**: Content Journey (owns movement from planning to scheduling)

## 5. Route-level Scopes
- [ ] **<Scope Name>**: <The specific page or URL>

## 6. Sub-surface Scopes
| Sub-surface | Parent route | User job | States | Component candidates |
|---|---|---|---|---|
| **<Name>** | `/create` | <Describe the user job this surface supports> | loading, edited, approved, error | PostPreviewCard, CaptionEditor, ApproveButton |

## 7. Surface Status Table
| Surface | Type | Status | Existing spec? | Recommended next skill |
|---|---|---|---|---|
| `/example` | route | pending | no | ui-inspector |

## 8. Recommended Specification Order
1. **<Scope Name>**: <Reason for prioritizing this>
2. **<Scope Name>**: ...

## 9. Next-skill routing
<Instructions on which skill to run next for the primary target surface.>

## 10. Open Questions / Ambiguities
- <Numbered list of areas where the boundary is unclear or classification is difficult>

## 11. Deprecated or duplicate inventory files
- `inventory.md` → deprecated; use this file.
```

## Acceptance criteria for this skill's output

- [ ] The output file is strictly named `surface-inventory.md`.
- [ ] All four layers (App Shell, Journey, Route, Sub-surface) are evaluated, and each sub-surface includes a `Component candidates` field where applicable.
- [ ] Every listed scope passes the "Smallest Coherent Scope" test.
- [ ] A prioritized specification order is provided with reasoning.
- [ ] Output follows the template structure exactly.
- [ ] Uses the term "UI Scope" consistently.

## Output template

```markdown
---
spec_type: inventory
spec_id: [slugified-project-name]-surface-inventory
created: [YYYY-MM-DD]
status: approved
surface_type: multi-surface-map
---

# UI Surface Inventory: [Project Name]

## 1. Purpose
[Brief summary of the discovery mission]

## 2. Source evidence
[Links to brief, screenshots, or source files used]

## 3. App Shell Scopes
[List of global UI elements like navigation, global headers, or toolbars]

## 4. Journey Scopes
[List of multi-page flows like Onboarding, Checkout, or Search-to-Detail]

## 5. Route-level Scopes
[List of specific URLs or routes that own multiple sub-surfaces]

## 6. Sub-surface Scopes
| Sub-surface | Parent route | User job | States | Component candidates |
|---|---|---|---|---|
| **[Name]** | [Parent] | [Job] | [States] | [Candidates] |

## 7. Surface Status Table
| Surface | Type | Status | Existing spec? | Recommended next skill |
|---|---|---|---|---|
| [Name] | [type] | pending | no | ui-inspector |

## 8. Recommended Specification Order
[Prioritized list of surfaces to spec next, with reasoning]

## 9. Next-skill routing
[Routing logic for next agent steps]
```

---

## Promotion checklist

Complete every item before changing `status: draft` to `status: stable`.

### Evidence on the spec-recovery-create fixture

- [ ] Running this skill against the Pulse app description produces output consistent with `examples/spec-recovery-create/surface-inventory.md`.
- [ ] The four-layer structure (App Shell, Journey, Route, Sub-surface) is fully populated — no layer is blank or marked TBD.
- [ ] The recovery order matches the one in `surface-inventory.md` (`/create` → AI Draft Panel → Channel Selector).

### Evidence on the settings-page fixture

- [ ] Running this skill against `examples/settings-page/brief.md` produces a scope map that identifies the settings page as a Route-level scope.
- [ ] The profile-form is identified as a Sub-surface with `Component candidates` including the profile-form component.

### Regression: smallest coherent scope

- [ ] Given a vague description like "the whole dashboard", the output breaks it into multiple named scopes rather than treating the whole dashboard as one scope.
- [ ] Each resulting scope passes the "Could someone spec and build this independently?" test — the skill is not complete until it does.

### Skill integration

- [ ] `validate-skill.py` passes for this skill with `status: stable` (no missing sections).
- [ ] `skills.json` entry for `ui-surface-inventory` has been updated to `"status": "stable"`.
- [ ] README core workflow starts with `ui-surface-inventory` (already true — verify).
- [ ] README Skill Map table has been updated to show `stable`.
