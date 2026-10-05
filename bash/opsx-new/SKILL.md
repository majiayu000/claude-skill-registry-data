---
name: opsx-new
description: Create a new OpenSpec change directory. Use when user wants to start a new change by creating just the directory scaffold.
license: MIT
compatibility: Requires openspec CLI.
metadata:
  author: openspec
  version: "1.0"
  generatedBy: "1.3.1"
---

Create a new OpenSpec change directory.

**Input**: The change name (kebab-case) after `/opsx:new` (e.g., `/opsx:new add-user-auth`).

**Steps**

1. **If no name provided, ask what they want to create**

   Use the **AskUserQuestion tool** to ask:
   > "What change do you want to create? Provide a name in kebab-case (e.g., add-user-auth)."

2. **Create the change directory**
   ```bash
   openspec new change "<name>"
   ```

3. **Show result**
   ```bash
   openspec status --change "<name>"
   ```

**Output**

```
## Change Created

**Name:** <name>
**Location:** openspec/changes/<name>/

Ready to add artifacts. Use `/opsx:propose <name>` to create proposal, design, and tasks artifacts.
```