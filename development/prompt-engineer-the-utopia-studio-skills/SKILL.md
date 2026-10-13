---
name: prompt-engineer
description: Makes a repository AI-native by creating AGENTS.md, .cursorrules, and documentation that helps any AI agent understand the codebase. Follows the WHAT/WHY/HOW framework from best practices. Use when the user asks to "make repo AI-ready", "add cursor rules", "create AGENTS.md", "set up for AI coding", or "make agents work better". Don't use for deployment (use deployment-engineer), monitoring (use monitoring-setup), or code organization (use repo-structurer).
---

# Prompt Engineer

Makes your repository "AI-native" so any coding agent (Claude Code, Cursor, Copilot, Gemini CLI, Codex) can understand and work with your codebase effectively.

## How It Works

1. Analyze codebase patterns and conventions
2. Create AGENTS.md following the WHAT/WHY/HOW framework
3. Create .cursorrules with code style and framework patterns
4. Add directory-level READMEs for agent navigation

## Key Principle

**Source:** [HumanLayer - "Writing a good CLAUDE.md"](https://www.humanlayer.dev/blog/writing-a-good-claude-md)

Claude Code injects CLAUDE.md with a system note: "this context may or may not be relevant to your tasks." This means agents WILL IGNORE instructions that aren't universally applicable. Only include information that's relevant to EVERY task.

## Step-by-Step Procedure

### Step 1: Analyze Codebase Patterns
```bash
# Identify tech stack
cat package.json 2>/dev/null | head -30
cat requirements.txt pyproject.toml 2>/dev/null | head -20

# Identify naming conventions
find . -name "*.ts" -not -path "*/node_modules/*" | head -5 | xargs head -20

# Identify file structure pattern
find . -type f -not -path "./.git/*" -not -path "*/node_modules/*" -not -path "*/.next/*" -maxdepth 3 | head -40

# Identify available scripts/commands
cat package.json 2>/dev/null | python3 -c "import sys,json; [print(f'  {k}: {v}') for k,v in json.load(sys.stdin).get('scripts',{}).items()]" 2>/dev/null

# Check for existing agent config
ls AGENTS.md CLAUDE.md .cursorrules .cursor/rules/ .github/copilot/ 2>/dev/null
```

### Step 2: Create AGENTS.md

**Framework:** WHAT (tech & structure) → WHY (purpose) → HOW (commands & verification)

Generate this template filled with detected values:

```markdown
# AGENTS.md

## Project Overview
{One sentence: what this project does and who it's for.}

## Tech Stack
- **Runtime:** {Node.js 20 / Python 3.11 / etc.}
- **Framework:** {Next.js 14 / FastAPI / etc.}
- **Database:** {PostgreSQL + Prisma / MongoDB + Mongoose / etc.}
- **Styling:** {Tailwind CSS / styled-components / etc.}
- **Auth:** {NextAuth / Clerk / Supabase Auth / etc.}
- **Hosting:** {Vercel / AWS / Railway / etc.}

## Commands
```bash
{package_manager} run dev     # Start development server
{package_manager} run build   # Production build
{package_manager} run test    # Run tests
{package_manager} run lint    # Run linter
```

## Project Structure
```
{root}/
├── app/          # {description}
├── components/   # {description}
├── lib/          # {description}
├── prisma/       # {description}
└── public/       # {description}
```

## Conventions
- {Naming convention: e.g., "camelCase for variables, PascalCase for components"}
- {Import convention: e.g., "Use @/ alias for project imports"}
- {Error handling: e.g., "Use try/catch with structured logging via pino"}
- {State management: e.g., "Server components by default, client only when needed"}

## Boundaries
- DO NOT modify `prisma/schema.prisma` without running `npx prisma generate`
- DO NOT commit `.env` files — use `.env.example` for documentation
- DO NOT use `any` type in TypeScript — use proper types or `unknown`
- ALWAYS run `{package_manager} run build` before committing to verify no errors
```

### Step 3: Create .cursorrules

```markdown
# {Project Name} — Cursor Rules

## Code Style
- Use {detected naming convention}
- Prefer {detected import style}
- {Framework-specific: e.g., "Use Server Components by default in Next.js App Router"}
- {Error handling: e.g., "Always use try/catch, never silently swallow errors"}

## File Organization
- New pages go in `app/{route}/page.tsx`
- Shared components go in `components/`
- Utility functions go in `lib/`
- API routes go in `app/api/{route}/route.ts`

## Do NOT
- Use `var` — use `const` or `let`
- Use `any` type — use proper types
- Put business logic in components — extract to `lib/`
- Commit without building first
```

### Step 4: Verify Agent Config Works

Test by asking the agent: "What tech stack does this project use?"
- If agent answers correctly from AGENTS.md: ✅ working
- If agent reads source files instead: ⚠️ AGENTS.md may need more specificity

## Output Format

```markdown
## 🤖 AI-Readiness Report

### Files Created
| File | Purpose | Size |
|------|---------|------|
| `AGENTS.md` | Onboards any AI agent to the codebase (WHAT/WHY/HOW) | {N} lines |
| `.cursorrules` | Code style + framework rules for Cursor IDE | {N} lines |
| `.cursor/rules/{name}.mdc` | Scoped rules for specific directories | {N} lines |

### What Each File Teaches the Agent
- **AGENTS.md:** Tech stack ({stack}), commands ({N} scripts), structure ({N} directories), conventions ({N} rules), boundaries ({N} guardrails)
- **.cursorrules:** Code style ({N} rules), file organization ({N} patterns), anti-patterns ({N} "Do NOTs")

### Verification
- [x] AGENTS.md covers WHAT/WHY/HOW
- [x] Only universally-applicable instructions included (per HumanLayer best practice)
- [x] Commands listed early (per GitHub AGENTS.md analysis)
- [x] Boundaries set (what NOT to do)
- [ ] Test: Ask agent "What tech stack does this project use?" → should answer from AGENTS.md
```
