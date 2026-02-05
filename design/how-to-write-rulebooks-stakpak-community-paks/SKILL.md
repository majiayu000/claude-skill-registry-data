---
name: how-to-write-rulebooks
description: |
  A practical, step-by-step guide that standardizes how to author, structure and publish rulebooks in Stakpak. It covers metadata creation, goal articulation, workflow design, reference inclusion and best-practice guidelines.
license: MIT
tags:
  - rulebook-creation
  - knowledge-management
  - devops-automation
  - best-practice
  - stakpak-cli
metadata:
  author: Stakpak <team@stakpak.dev>
  version: "1.0.2"
---

## Goals

* Make it easy for anyone to write and share Rulebooks

* Standardize how operational knowledge is captured and reused

* Enable Stakpak to help users create high quality Rulebooks

## Workflow

When generating a new Rule Book, always follow this process:

### Step 1: Start with Metadata

**URI:** <category>/<name>\
**Description:** The description will help Stakpak know what this Rulebook is about, its scope, and when to use it, keep this short and to the point\
**Tags:** create at least three tags to help Stakpak find this Rulebook in the future with keyword search

### Step 2: Write the Goals

Explain the outcome the user will achieve by following this Rule Book. The goal should be written as a clear, outcome oriented sentence:

**Bad:** "This Rule Book is about Kubernetes."

**Good:** "This Rule Book helps you deploy and scale applications on Kubernetes with production grade configuration."

### Step 3: Write the Workflow

Provide a numbered, step by step guide that explains how to accomplish the goal, maximize re-usability by avoiding hard coded values.

Each step should include:

**Action:** Imperative instruction (e.g., "Install the CLI tool").

**Reasoning:** Why this step is required (optional but recommended).

**Examples:** Code samples, commands, or configuration snippets where applicable.

Guidelines:

* Use short, direct sentences

* Keep steps atomic (one action per step)

* Include necessary context but avoid unnecessary details and hard-coded literals

### Step 4: Add References

Conclude the Rule Book with a "References" section.\
This section should contain:

* Links to official documentation or standards

* Related Rulebooks

* External resources for deeper learning

### Best Practices for Writing a Rule Book

* Use a clear structure, and concise text

* Only include new information and insights learned throughout the session, for example good patterns you see, and information you learn by doing web research. This information should complement LLM agents, so repeating knowledge the agent already processes is redundant and reduces the quality of this Rulebook

* You can add a prerequisites with conditions and initial requirements in the description (e.g. only run if there is Terraform code)

* You can ask the agent in the Rulebook to follow certain standards and guidelines

  * Principle of least privilege

  * OWASP Guidelines (with reference to which guidelines exactly)

  * AWS Well Architected Framework

  * Or even your internal company guidelines found in other Rulebooks (with reference)

### Using the stakpak CLI to manage Rulebook

```
# Get rulebook(s) (URI is optional - if not provided, lists all rulebooks)
stakpak rb get [URI]

# Apply/create a rulebook from a markdown file
stakpak rb apply <FILE_PATH>

# Delete a rulebook
stakpak rb delete <URI>
```
