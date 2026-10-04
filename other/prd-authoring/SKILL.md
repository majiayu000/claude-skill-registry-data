---
name: prd-authoring
description: Use this skill for early-stage project planning. It leverages the Gemini CLI to generate high-quality first drafts of Product Briefs, Research Documents, and full PRDs, guiding users from idea to validated requirements. Triggers include "create PRD", "product brief", or "validate requirements".
---

# PRD Authoring Skill

## Purpose

To accelerate and enhance early-stage project planning by using a powerful generative AI to create high-quality first drafts of key strategic documents. This skill integrates the Gemini CLI into the PRD authoring workflow, transforming it from a manual template-filling exercise into a dynamic, AI-assisted process.

The skill guides users from a vague project idea to a well-defined Product Requirements Document (PRD) by:
- **Generating a Product Brief:** Creates a comprehensive brief from a simple project name.
- **Generating a Research Plan:** Uses the product brief to generate a targeted research document.
- **Generating a full PRD:** Synthesizes the brief and research into a detailed PRD with objectives, requirements, and success criteria.

This approach bridges the gap between "we have an idea" and "we're ready to write specs" with unprecedented speed and quality.

## When to Use

Use this skill in the following situations:

- Starting a new project from an initial concept.
- Generating a first draft of a product brief, research plan, or PRD.
- Validating an existing PRD against quality standards.
- Breaking down a PRD into epics for sprint planning.

Do NOT use this skill for:
- Implementation-level specifications (use spec-authoring instead).
- Sprint planning from approved specs (use sprint-planner instead).

## Prerequisites

- Project initialized with SynthesisFlow structure (`docs/` directory exists).
- `gemini` CLI tool installed and authenticated.

## PRD Philosophy

**Strategy Before Tactics**: PRDs define WHAT we're building and WHY before specs define HOW we'll build it. This skill uses AI to rapidly generate the "WHAT" and "WHY" so that teams can focus on review, refinement, and strategic alignment.

---

## Workflow Commands

### The `status` Command

#### Purpose

Assess project readiness and provide guidance on next workflow steps. This is the recommended starting point.

#### Workflow

Run the status check to understand the current state of your PRD documents.
```bash
bash scripts/prd-authoring.sh status [project-name]
```
The script will report which documents exist (`product-brief.md`, `research.md`, `prd.md`, etc.) and recommend the next logical command to run.

---

### The `brief` Command

#### Purpose

Generate a comprehensive, high-quality first draft of a Product Brief from a simple project name.

#### Workflow

##### Step 1: Run Brief Generation Script

Execute the script with your project name.
```bash
bash scripts/prd-authoring.sh brief "Your Awesome Project Name"
```

##### Step 2: Understand What the Script Does

Instead of creating an empty template, the script calls the **Gemini CLI** with a detailed prompt, asking it to generate a full product brief. This includes plausible, well-structured content for:
- Problem Statement
- Target Users
- Proposed Solution
- Value Proposition
- Success Metrics

The output from Gemini is saved as the first draft in `docs/prds/your-awesome-project-name/product-brief.md`.

##### Step 3: Review and Refine

Open the generated file. Review the AI-generated content with your team and stakeholders, refining the details to match your specific vision. The draft provides a strong foundation, saving hours of initial writing.

---

### The `research` Command

#### Purpose

Generate a targeted, context-aware market research plan based on the contents of your product brief.

#### Workflow

##### Step 1: Run Research Generation Script

Once your product brief is reviewed and saved, run the research command:
```bash
bash scripts/prd-authoring.sh research your-awesome-project-name
```

##### Step 2: Understand What the Script Does

The script sends the entire content of your `product-brief.md` to the **Gemini CLI**. It prompts the AI to act as a business analyst and generate a research plan that logically follows from the brief. The generated draft will include sections for:
- Competitive Analysis
- Market Insights
- User Feedback Analysis
- Technical Considerations
- Actionable Recommendations

This draft is saved to `docs/prds/your-awesome-project-name/research.md`.

##### Step 3: Execute Research and Refine Document

Use the AI-generated document as a guide for your research activities. Fill in the details and refine the analysis based on your actual findings.

---

### The `create-prd` Command

#### Purpose

Generate a comprehensive, detailed first draft of a Product Requirements Document (PRD) by synthesizing the product brief and the research document.

#### Workflow

##### Step 1: Run PRD Creation Script

After completing your brief and research documents, run the `create-prd` command:
```bash
bash scripts/prd-authoring.sh create-prd your-awesome-project-name
```

##### Step 2: Understand What the Script Does

This is the most powerful feature. The script sends the **full content of both your product brief and your research document** to the **Gemini CLI**. It prompts the AI to generate a detailed PRD that includes:
- SMART Objectives
- Measurable Success Criteria
- Specific Functional and Non-Functional Requirements
- Constraints, Assumptions, and Out-of-Scope items

The resulting draft, saved in `docs/prds/your-awesome-project-name/prd.md`, is a deeply contextualized document that connects business goals from the brief with insights from the research.

##### Step 3: Review, Validate, and Refine

The generated PRD provides an excellent starting point. Review it with your team to ensure all requirements are accurate, testable, and aligned with project goals. Use the `validate-prd` command to check for quality.

---

### The `validate-prd` Command

#### Purpose

Validate an existing PRD against quality standards, checking for missing sections, vague requirements, and unmeasurable success criteria. This command does **not** use the Gemini CLI; it uses pattern matching to enforce quality.

#### Workflow

Run the validation check on your PRD:
```bash
bash scripts/prd-authoring.sh validate-prd your-awesome-project-name
```
Review the report and address any issues found.

---

### The `decompose` Command

#### Purpose

Break down a validated PRD into epics for sprint planning. This helps transition from strategic planning to tactical execution.

#### Workflow

Once your PRD is validated, run the decompose command:
```bash
bash scripts/prd-authoring.sh decompose your-awesome-project-name
```
This creates an `epics.md` file with a template structure for you to define your epics.

---

## Error Handling and Troubleshooting

### Gemini CLI Issues

**Symptom**: The script fails during the `brief`, `research`, or `create-prd` commands with an error related to the `gemini` command.

**Solution**:
- Ensure the `gemini` CLI is installed and in your system's PATH.
- Verify you are authenticated. Run `gemini auth` if needed.
- Check for any Gemini API-related issues or outages.
- Examine the prompt being constructed in the `prd-authoring.sh` script for any potential issues.

### Other Issues

For issues related to file existence, permissions, or validation errors, the script provides detailed error messages and recommendations. Always check the script's output for guidance.

---

## Best Practices

- **Review and Refine**: The AI-generated drafts are a starting point, not a final product. Always review and tailor the content to your specific project needs.
- **Garbage In, Garbage Out**: The quality of the generated `research` and `prd` documents depends on the quality of the `product-brief` you provide. Take time to refine the initial brief.
- **Iterate**: Use the `status` command to guide you through the workflow. Don't be afraid to go back and refine a previous document if new insights emerge.