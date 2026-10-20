---
name: ui-gen
description: "Generate User Interfaces (Web, CLI, Mobile) using GenUI, HTMX, or TUI patterns. Use when: ui gen."
license: CC-BY-SA-4.0
metadata:
  source: "agents/skills/coding/ui-gen.skill.md"
  tags: "coding"
  core: "false"
  context_cost: "medium"
---
# UI Generation Skill

## Goal
Use this skill when the user asks for a User Interface, Dashboard, CLI tool, or Frontend.

## Steps
## 1. Paradigm Selection
First, determine the best paradigm based on the User's Stack and needs:

| Scenario | Recommended Paradigm |
|---|---|
| "Modern SaaS", "React", "Dashboard" | **Generative UI** (React/ShadCN/Tailwind) |
| "Internal Tool", "Go/PHP/Node Backend" | **HTMX** (Hypermedia-driven) |
| "Dev Tool", "Script", "Server Utils" | **TUI** (Bubble Tea / Ink) |
| "Quick Prototype", "Data App" | **Streamlit / Gradio** (Python) |

## 2. Generative UI Workflow (React/ShadCN)
1.  **Dependencies:** Ensure `lucide-react`, `clsx`, `tailwind-merge` are installed.
2.  **Component:** Create a single-file component if possible, or modularize if complex.
3.  **Style:** Use Tailwind CSS. Focus on "Vibe Coding" (Dark mode, gradients, glassmorphism).
4.  **Mocking:** If backend is missing, mock data inside the component.

## 3. HTMX Workflow
1.  **Route:** Create a backend route (e.g., `GET /partials/dashboard`).
2.  **Template:** Return *only* the HTML fragment (no `<html>` or `<body>` unless it's the full page).
3.  **Interactivity:** Use `hx-get`, `hx-post`, `hx-trigger`.
    *   Example: `<button hx-post="/update" hx-swap="outerHTML">Save</button>`

## 4. TUI Workflow
1.  **Library:** Use Bubble Tea (Go) or Ink (Node).
2.  **Model:** Define the State (Cursor position, Input value).
3.  **Update:** Define the Keypress handlers.
4.  **View:** Return the String representation of the UI.

## 5. Security Checklist
- [ ] **XSS Prevention:** Ensure all user input is escaped (React/Templ do this automatically).
- [ ] **Validation:** Client-side validation is UX, Server-side is Security. Do both.
- [ ] **Access Control:** UI elements should simply *not exist* if the user lacks permission.

## 6. Artifact Generation
When generating the UI, create a `UI_SPEC.md` first if the complexity is high ( > 5 components).
Otherwise, write the code directly.

## Security & Guardrails

### 1. Skill Security (UI Gen)
- **DOM-Based XSS via Props**: In "Generative UI" (Step 2), the LLM might correctly escape standard HTML bodies but incorrectly bind raw, unsanitized user input directly to sensitive DOM properties (e.g., `dangerouslySetInnerHTML`, `href`, `src`, or inline `style` objects). The agent must strictly mandate the use of framework-level safe bindings (e.g., standard React curly braces `{}`) and strictly forbid raw HTML insertion unless passed through a verified HTML sanitizer like DOMPurify.
- **Client-Side Validation Illusion**: The Security Checklist (Step 5) notes that "Client-side validation is UX, Server-side is Security." However, an LLM might generate a UI that *appears* highly secure (e.g., disabling the "Submit" button if a field is invalid) while neglecting to implement or verify the corresponding backend API constraints. The agent must explicitly tag all UI-level validation code with a warning comment stating it is strictly cosmetic and not a security perimeter.

### 2. System Integration Security
- **HTMX Route Exposure**: In the "HTMX Workflow" (Step 3), the agent creates backend routes returning HTML fragments (e.g., `GET /partials/dashboard`). If the agent fails to secure these partial routes with the exact same authentication/authorization middleware as the main application routes, an attacker can bypass the UI and directly fetch sensitive HTML fragments. The agent must mandate that all HTMX endpoints inherit the project's global security context.
- **TUI Command Injection (Terminal Escape Sequences)**: In the "TUI Workflow" (Step 4), returning the String representation of the UI can be dangerous if it includes untrusted data. An attacker might supply input containing malicious ANSI escape sequences designed to spoof terminal history, hide malicious commands, or exploit terminal emulator vulnerabilities. The agent must rigorously strip or securely escape all raw ANSI control characters from dynamic user input before rendering it in the TUI view.

### 3. LLM & Agent Guardrails
- **The "Admin Dashboard" Hallucination**: When asked to build an "Internal Tool" (Step 1), the LLM might hallucinate standard administrative features (like a "Delete All Users" button or "View Raw Passwords" table) that were never explicitly requested, simply because "Internal Tool" is heavily associated with those features in its training data. The agent must rigidly constrain UI generation to the exact components specified in the user's prompt or the `UI_SPEC.md`.
- **Third-Party CDN Hijacking**: To quickly style a prototype, the LLM might hallucinate `unpkg` or `cdnjs` script tags for libraries (like Tailwind or Alpine.js) instead of using local `npm` module imports. Pulling executable code from unpinned, external CDNs introduces a severe supply-chain risk (Subresource Integrity issues). The agent must categorically reject UI code that relies on external CDN `<script>` tags, forcing local dependency resolution.
