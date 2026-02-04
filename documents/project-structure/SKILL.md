---
name: project-structure
description: Generate comprehensive project structure documentation with intelligent tree representation, meaningful comments, and utility dependency analysis. Use when user asks to document project structure or create architecture overview.
allowed-tools: Bash, Read, Write, Glob, Grep
---

# Project Structure Documentation Generator

Generate `PROJECT-STRUCTURE.md` with comprehensive tree representation, meaningful comments, and utility dependency analysis.

## Core Workflow

**Important:** All file operations should be relative to the git repository root. Always determine the git root first:
```bash
GIT_ROOT=$(git rev-parse --show-toplevel 2>/dev/null)
```
Then reference files as `$GIT_ROOT/PROJECT-STRUCTURE.md`, `$GIT_ROOT/package.json`, etc.

### Generation Process

1. **Detect package manager and read production dependencies:**
   ```bash
   # Check for package managers (use $GIT_ROOT for all paths)
   test -f "$GIT_ROOT/package.json" && echo "node_found"
   test -f "$GIT_ROOT/pyproject.toml" && echo "python_toml_found"
   test -f "$GIT_ROOT/requirements.txt" && echo "python_requirements_found"
   test -f "$GIT_ROOT/Cargo.toml" && echo "rust_found"
   test -f "$GIT_ROOT/go.mod" && echo "go_found"
   ```
   - Read dependency files to identify production dependencies
   - Store list for later analysis in Step 6

2. **Gather all files (respecting .gitignore):**
   ```bash
   # Change to git root first, then gather files
   cd "$GIT_ROOT"

   # Get tracked files
   git ls-files

   # Get untracked files (respects .gitignore)
   git ls-files --others --exclude-standard
   ```
   - Combine both lists for complete file inventory
   - All paths will be relative to git root

3. **Build directory tree structure with root files:**
   - **CRITICAL: Show ALL directories at ALL nesting levels, but ONLY files in the repository root**
   - Build complete directory hierarchy recursively
   - Include all files at the repository root level
   - Do NOT show individual files within subdirectories
   - Use proper tree formatting:
     - `├──` for items with siblings below
     - `└──` for last item in directory
     - `│   ` for vertical continuation
     - Indent 4 spaces per level
   - Example structure:
     ```
     package.json            # Node.js dependencies and scripts
     README.md              # Project overview and setup instructions
     src/                   # Source: React components (45), utilities (12). Entry App.tsx
     ├── components/        # UI components: Button, Card, Form. Design system, accessibility. 15 modules
     │   ├── Button/       # Button component: primary/secondary variants. Tests, Storybook stories
     │   └── Form/         # Form inputs: Input, Select, Checkbox. Validation, error handling
     └── utils/             # Utilities: formatting, validation, data transformation. 12 helpers
     ```

4. **Generate telegraphic comments for directories and root files:**
   - Read [comment-guidelines.md](comment-guidelines.md)
   - **CRITICAL: Every directory at every nesting level must have a keyword-dense comment**
   - **For root-level files:** ~8-12 words describing functionality and purpose
   - **For directories:** ~14-23 words using telegraphic style:
     - Format: `Purpose: key items. Tech/patterns. Counts`
     - List key items by name (Button, Card, Form OR AuthService, UserService)
     - Mention tech/patterns concisely (JWT, React hooks, Sequelize ORM)
     - Include counts when relevant (15 modules, 8 files)
     - Omit articles (the, a, an) and unnecessary verbs
   - Describe WHAT content is about, not just restate names
   - Use Read/Glob/Grep to understand directory contents and structure
   - Examples:
     - `components/` → "UI components: Button, Card, Form, Modal. Design system, accessibility, tests, stories. 15 modules"
     - `components/Button/` → "Button component: primary/secondary/tertiary variants, loading states. ARIA accessibility, tests, Storybook stories"

5. **Analyze utility dependencies:**
   - Read [dependency-analysis.md](dependency-analysis.md)
   - Categorize production dependencies
   - Analyze actual usage patterns
   - Document commonly used functions
   - Only include meaningful utilities (3+ file usage)

6. **Write PROJECT-STRUCTURE.md:**

   **File Format:**
   ```markdown
   # Project Structure

   *Generated on [current date and time] with the project-structure skill*

   [FULL RECURSIVE tree showing ALL directories and files at ALL nesting levels with inline comments]

   ## Utility Dependencies

   **Note:** Before implementing custom utilities, check if functionality exists in these libraries.

   [Dependency analysis by category - ONLY if meaningful production dependencies exist]
   ```

   **File Location:**
   - File path: `$GIT_ROOT/PROJECT-STRUCTURE.md`
   - Always write to git repository root
   - File is standalone, dedicated to project structure documentation

   **Use Write tool:**
   - Use Write to create or replace the entire file
   - Since this is a dedicated file, simply write the complete content
   - The file will be overwritten if it already exists

   **CRITICAL Tree Requirements:**
   - **Show complete recursive directory structure** - expand ALL directories at ALL levels
   - **Show ONLY root-level files** - do NOT show files within subdirectories
   - **Every directory at every level gets a telegraphic comment** (e.g., `components/ # UI components: Button, Card. Design system. 15 modules`)
   - **Every root file gets a comment** (e.g., `package.json # Node.js dependencies and scripts`)
   - **All comments are INLINE in the tree** - NO separate sections
   - **Directory comments use telegraphic style** - Format: Purpose: items. Tech. Counts (~14-23 words)
   - **Omit articles and unnecessary verbs** - keyword-dense, information-rich
   - NO extra sections beyond tree and dependencies
   - Utility Dependencies section (##) only included if meaningful production dependencies found (3+ file usage or critical utilities)

## Output Format

See [examples.md](examples.md) for complete example outputs.

**File Structure (PROJECT-STRUCTURE.md):**
1. `# Project Structure` header (level 1, since it's the main document title)
2. Generation attribution line in italics: `*Generated on [date and time] with the project-structure skill*`
3. Complete directory tree with root files and inline comments:
   - All root-level files with comments
   - All directories at all nesting levels with detailed comments
   - NO files shown within subdirectories
4. `## Utility Dependencies` section (level 2, ONLY if meaningful production dependencies exist)

**File Notes:**
- The file is standalone and dedicated to project structure
- Located at repository root: `$GIT_ROOT/PROJECT-STRUCTURE.md`
- File is always generated fresh (simple and clean)
- Keep the file simple and focused - no extra sections beyond Utility Dependencies

## Performance Tips

- Use Glob for efficient directory scanning
- Use Grep to understand file purposes
- Read representative files, not every file
- Build tree incrementally
- Leverage progressive disclosure (read reference docs as needed)

## Key Principles

1. **Respect .gitignore** - Only document relevant project files
2. **Directory-focused structure** - Show all directories with telegraphic comments, only root-level files
3. **Telegraphic comments** - Use keyword-dense style: Purpose: items. Tech. Counts (~14-23 words)
4. **Production focus** - Only document production dependencies

## Reference Materials

- [comment-guidelines.md](comment-guidelines.md) - Telegraphic comment style guide with examples
- [dependency-analysis.md](dependency-analysis.md) - Dependency documentation
- [examples.md](examples.md) - Real-world examples with telegraphic comments

## Begin Execution

Read reference materials as needed using progressive disclosure and generate the project structure documentation.
