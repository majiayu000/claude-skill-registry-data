---
name: add-project
description: Automatically add a GitHub project to the Current Projects section. Fetches repo info, generates an emoji and one-line description, then updates README. Use when the user provides a GitHub URL.
allowed-tools: Read, Edit, Bash, WebFetch
---

# Add Project to README (Auto)

## Instructions

When user provides a GitHub URL, automatically handle the entire process:

1. **Parse the URL** to extract the repository name and owner from the GitHub URL
2. **Fetch repository metadata**:
   - Use WebFetch to get the repository's GitHub page and extract the description/about section
   - Look for a README.md in the repo to understand the project purpose
3. **Generate an appropriate emoji**:
   - Analyze keywords in the description/README (e.g., "AI" → 🤖, "home" → 🏠, "search" → 🔍, "data" → 📊, "tool" → 🛠️, "web" → 🌐, "api" → 🔌, "automation" → ⚙️, "learning" → 📚, "security" → 🔐, "ml" → 🧠, "database" → 🗄️)
   - Pick the most relevant emoji based on the project type
4. **Generate a one-liner description** (max 80 characters):
   - Extract key information from the repo description or README
   - Create a concise, meaningful description that captures the project's purpose
   - If no description exists, infer from the repo name and content
5. **Read the current README.md** to locate the "### Current Projects" section
6. **Add the new project** in this exact format:
   ```
   - [EMOJI] [project-name](URL) - [one-line description]
   ```
7. **Update the README** by appending the new project entry to the Current Projects list, maintaining proper formatting
8. **Confirm** by showing the user the updated Current Projects section with the new entry highlighted
9. **Push the changes** to GitHub:
   - Run: `git add README.md`
   - Run: `git commit -m "Add claude-usage-widget to Current Projects"`
   - Run: `git push origin master`

## Format Requirements

- Emoji should be a single relevant character
- Project name extracted from URL
- Full GitHub URL must be preserved
- Description must be single line, under 80 characters
- Maintain consistent spacing with existing entries

## Example

**Input:** `/add-project https://github.com/user/ml-pipeline`

**Process:**
1. Fetch repo → finds "Machine learning pipeline orchestration framework"
2. Keywords suggest 🧠 (ML) or ⚙️ (automation) → select 🧠
3. Generate 1-liner: "ML pipeline orchestration framework"
4. Update README with: `- 🧠 [ml-pipeline](https://github.com/user/ml-pipeline) - ML pipeline orchestration framework`
5. Show confirmed update
