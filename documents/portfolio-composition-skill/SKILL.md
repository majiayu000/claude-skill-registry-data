---
name: Portfolio Composition Skill
description: Generate structured, narrative-style portfolio case studies from project data. Use when creating portfolio entries, project case studies, or professional work documentation. Focuses on reasoning, decision-making, and measurable outcomes with a factual, reflective tone instead of promotional language.
---

# Portfolio Composition Skill

## Purpose

Transform raw project data into professional case study narratives that demonstrate reasoning, technical decisions, and measurable results.

**Output characteristics:**

- Reads as professional portfolio entry, not marketing content
- Factual, reflective, confident tone
- Emphasizes process and decision-making over promotional claims
- Uses past tense verbs (designed, validated, implemented)

**Avoid:**

- Sales language, exclamation marks, generic adjectives
- First-person pronouns unless style requires it
- CTAs, slogans, marketing claims

## Required Input

**Core fields:**

- project_name: Project title
- role: Your role in the project
- timeline: Project duration
- objective: Primary goal
- challenge: Main problem addressed
- methods: Approaches and techniques used
- impact: Results achieved

**Optional fields:**

- tools: Technologies and tools used
- metrics: Quantified results
- feedback: User or stakeholder quotes
- reflection: Lessons learned
- related_projects: Connected work

## Output Structure

Generate JSON with six sections. Each section maximum 120 words.

### 1. Overview

Summarize what the project is and why it mattered.

**Uses:** project_name, timeline, role, objective

**Format:**

```json
{
  "overview": {
    "headline": "string (project title, max 10 words)",
    "summary": "string (2-3 sentences on goal and scope)",
    "meta": { "role": "string", "timeline": "string" }
  }
}
```

**Requirements:**

- Neutral tone
- Must mention purpose and scale
- Headline under 10 words

### 2. Context

Explain environment, target users, and constraints.

**Uses:** objective, tools, constraints

**Format:**

```json
{
  "context": {
    "background": "string (setting and target users)",
    "constraints": ["string (technical or business limits, max 10 words each)"],
    "tools_used": ["string"]
  }
}
```

**Requirements:**

- Factual descriptions, avoid adjectives like "innovative"
- Each constraint under 10 words

### 3. Challenge

State the main problem and insights that guided direction.

**Uses:** challenge, insights

**Format:**

```json
{
  "challenge": {
    "problem_statement": "string (1-2 sentences)",
    "insights": ["string (3-5 insights or pain points)"]
  }
}
```

**Requirements:**

- Mention both what was wrong and why it mattered
- Use active phrasing: "Users struggled to...", "The system lacked..."

### 4. Process

Detail reasoning, iterations, and methods used.

**Uses:** methods, decisions, iterations

**Format:**

```json
{
  "process": [
    {
      "step_title": "string (phase or milestone, max 5 words)",
      "approach": "string (what was done and why, max 40 words)",
      "visual_hint": "string (suggested image or diagram)"
    }
  ]
}
```

**Requirements:**

- Use 3-5 steps only
- Focus on how challenges were solved, not listing tools
- Each step_title under 5 words, approach under 40 words

### 5. Outcome

Show tangible results and evidence of success.

**Uses:** impact, metrics, feedback

**Format:**

```json
{
  "outcome": {
    "results": ["string (quantified or descriptive outcomes)"],
    "metrics": ["string (e.g., '+25% retention')"],
    "feedback": ["string (user or stakeholder quotes)"],
    "visual_hint": "string (suggested before/after or result visual)"
  }
}
```

**Requirements:**

- Include at least one quantifiable impact or quote
- Avoid adjectives like "amazing" or "great"

### 6. Reflection

Demonstrate learning and professional growth.

**Uses:** reflection, next_steps, related_projects

**Format:**

```json
{
  "reflection": {
    "lessons": ["string (what was learned)"],
    "future_focus": "string (what could be improved or extended)",
    "related_projects": ["string (other works)"]
  }
}
```

**Requirements:**

- Authentic and forward-looking tone
- Mention at least one personal or team insight

## Validation Checklist

Before finalizing, verify:

- [ ] All six sections present (overview through reflection)
- [ ] Challenge clearly links to process decisions
- [ ] Outcome includes measurable or testimonial proof
- [ ] Reflection mentions learning or next iteration
- [ ] No sales or CTA language detected
- [ ] Each section under 120 words
- [ ] Consistent past tense verbs throughout

## Example Usage

**Input:**

```json
{
  "project_name": "Vibe Coding Agent",
  "role": "Product Manager",
  "timeline": "Q3-Q4 2025",
  "objective": "Enable low-code users to build functional web apps with an AI assistant",
  "challenge": "Non-technical creators struggled to debug and publish complex UIs.",
  "methods": ["multi-model orchestration", "skill composition framework", "user co-design workshops"],
  "impact": "Reduced build-to-publish time by 60%, improved satisfaction scores by 2.3x.",
  "metrics": ["60% faster delivery", "2.3x higher usability rating"],
  "feedback": ["'It feels like the AI reads my mind.' - Beta user"],
  "reflection": "Future focus: expanding Skill marketplace and contextual learning."
}
```

**Output:**

```json
{
  "overview": {
    "headline": "Vibe Coding Agent",
    "summary": "An AI-assisted builder that lets non-coders design, debug, and deploy web apps end-to-end.",
    "meta": { "role": "Product Manager", "timeline": "Q3-Q4 2025" }
  },
  "context": {
    "background": "Built within YouWare's creation platform for SMB users aiming to build sites visually.",
    "constraints": ["Low-code user base", "Browser-only runtime"],
    "tools_used": ["Figma", "TypeScript", "OpenAI APIs"]
  },
  "challenge": {
    "problem_statement": "Non-technical creators struggled to debug logic and deploy stable UIs.",
    "insights": [
      "Users lost context across design and code steps",
      "Debug process was opaque",
      "Model suggestions were not reusable"
    ]
  },
  "process": [
    {
      "step_title": "Skill Design",
      "approach": "Defined modular Skill units bridging model reasoning and UI actions.",
      "visual_hint": "System diagram showing Skill orchestration"
    },
    {
      "step_title": "Prototype & Test",
      "approach": "Ran co-design sessions to validate flow and refine UI feedback loops.",
      "visual_hint": "User testing screenshots"
    },
    {
      "step_title": "Integration",
      "approach": "Implemented orchestration and validation logic for agent Skill calls.",
      "visual_hint": "Workflow chart of multi-model routing"
    }
  ],
  "outcome": {
    "results": ["Launch-to-publish time reduced by 60%"],
    "metrics": ["2.3x higher usability rating"],
    "feedback": ["'It feels like the AI reads my mind.' - Beta user"],
    "visual_hint": "Before/after interface comparison"
  },
  "reflection": {
    "lessons": ["Clearer Skill definitions improved reasoning consistency"],
    "future_focus": "Extend Skill sharing and adaptive learning features.",
    "related_projects": ["AI Integration Skill"]
  }
}
```
