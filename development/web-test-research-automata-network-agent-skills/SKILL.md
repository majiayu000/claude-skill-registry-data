---
name: web-test-research
description: Analyze ANY web project - detect if Web3 DApp, research dependencies via WebSearch, understand business functions from code AND UI screenshots, generate test requirements.
license: MIT
compatibility: Node.js 18+
metadata:
  author: AI Agent
  version: 6.0.0
allowed-tools: Bash Read Glob Grep WebSearch WebFetch Skill
---

# Project Research

Analyze any web project to understand what it does and what needs to be tested.

## Core Principle: Full Code Tree Traversal + Visual Analysis

```
╔════════════════════════════════════════════════════════════════╗
║  ⚠️  CRITICAL: FULL CODE TREE TRAVERSAL                        ║
╠════════════════════════════════════════════════════════════════╣
║                                                                ║
║  You MUST read the ENTIRE codebase systematically:             ║
║                                                                ║
║  1. Start from entry files (index.ts, main.ts, App.tsx)        ║
║  2. Follow ALL imports/references like a tree                  ║
║  3. Read EVERY file that is referenced                         ║
║  4. Build a complete module & function map                     ║
║                                                                ║
║  DO NOT:                                                       ║
║  ✗ Only search for specific keywords                           ║
║  ✗ Only read files you think are important                     ║
║  ✗ Skip files because they "look simple"                       ║
║  ✗ Miss functionality hidden in utility files                  ║
║                                                                ║
║  The goal is 100% code coverage understanding!                 ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
```

**You must dynamically:**

1. **Detect** - Is this a Web3 DApp? What dependencies does it use?
2. **Find Docs** - Read README.md, design docs, architecture docs for requirements
3. **Tree Traverse** - Start from entry files, read EVERY imported file
4. **Map Modules** - Build complete module map with entry files
5. **Research** - WebSearch any unknown dependency/protocol
6. **See** - Launch the app and take UI screenshots to discover visual features
7. **Analyze Business** - Deep dive into business logic, user flows, roles, and permissions
8. **Generate** - Create comprehensive feature analysis for test case generation

## Workflow Overview

```
┌─────────────────────────────────────────────────────────────────┐
│  web-test-research - FULL CODE ANALYSIS                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Phase 1: Project Documentation Analysis                        │
│          ↓                                                      │
│          - Read README.md for project overview                  │
│          - Find design docs, architecture docs, API docs        │
│          - Understand business requirements                     │
│          ↓                                                      │
│  Phase 2: Entry Point Discovery                                 │
│          ↓                                                      │
│          - Find all entry files (index, main, App)              │
│          - Map project structure                                │
│          - Identify framework (React/Vue/Next/etc)              │
│          ↓                                                      │
│  Phase 3: Full Code Tree Traversal ← CRITICAL!                  │
│          ↓                                                      │
│          - Start from entry files                               │
│          - Follow ALL imports recursively                       │
│          - Read EVERY referenced file                           │
│          - Build complete dependency graph                      │
│          ↓                                                      │
│  Phase 4: Module & Function Mapping                             │
│          ↓                                                      │
│          - Group files into logical modules                     │
│          - Identify each module's functions                     │
│          - Document entry files per module                      │
│          ↓                                                      │
│  Phase 5: Dependency Research                                   │
│          ↓                                                      │
│          - Research unknown packages via WebSearch              │
│          - Understand third-party functionality                 │
│          ↓                                                      │
│  Phase 6: Visual UI Analysis                                    │
│          ↓                                                      │
│          - Launch browser, take screenshots                     │
│          - Discover features not obvious from code              │
│          - Analyze third-party UI components                    │
│          ↓                                                      │
│  Phase 7: Role & Permission Analysis                            │
│          ↓                                                      │
│          - Identify user roles (guest, user, admin, owner)      │
│          - Map permissions per role                             │
│          - Find protected routes/features                       │
│          ↓                                                      │
│  Phase 8: Generate Comprehensive Analysis                       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Phase 1: Project Documentation Analysis

**Find and read ALL project documentation:**

```bash
# Find README and documentation files
find . -maxdepth 3 -name "README*" -o -name "DESIGN*" -o -name "ARCHITECTURE*" -o -name "API*" -o -name "*.md" | grep -v node_modules

# Read the main README
cat README.md

# Look for docs folder
ls -la docs/ documentation/ doc/
```

**Extract from documentation:**

| Document Type | What to Extract |
|--------------|-----------------|
| README.md | Project purpose, features list, tech stack |
| DESIGN.md | Business requirements, user flows |
| ARCHITECTURE.md | System structure, module relationships |
| API.md | Endpoints, data formats |
| CONTRIBUTING.md | Code organization hints |

**Ask user for missing docs:**
If design documents are not found in the codebase, use AskUserQuestion to request:
- Design specifications
- Figma/design file links
- Product requirements document
- API documentation

## Phase 2: Entry Point Discovery

**Find all entry files:**

```bash
# React/Next.js entry points
ls -la src/index.* src/main.* src/App.* app/layout.* app/page.* pages/_app.* pages/index.*

# Vue entry points
ls -la src/main.* src/App.vue

# Package.json main field
cat package.json | grep -A2 '"main"'

# Build configuration
cat vite.config.* webpack.config.* next.config.*
```

**Map project structure:**

```bash
# Get full directory structure (excluding node_modules)
find . -type f \( -name "*.ts" -o -name "*.tsx" -o -name "*.js" -o -name "*.jsx" -o -name "*.vue" \) | grep -v node_modules | sort
```

## Phase 3: Full Code Tree Traversal (CRITICAL!)

```
╔════════════════════════════════════════════════════════════════╗
║  TREE TRAVERSAL ALGORITHM                                      ║
╠════════════════════════════════════════════════════════════════╣
║                                                                ║
║  1. Create a queue with entry files                            ║
║  2. Create a "visited" set (initially empty)                   ║
║  3. While queue is not empty:                                  ║
║     a. Dequeue a file                                          ║
║     b. If already visited, skip                                ║
║     c. Read the file content                                   ║
║     d. Extract all imports/requires                            ║
║     e. Add imported files to queue                             ║
║     f. Mark current file as visited                            ║
║     g. Document file's purpose and exports                     ║
║  4. Result: Complete map of all code and dependencies          ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
```

**Step-by-step execution:**

### 3.1 Start from Entry File

```bash
# Read the main entry file
cat src/index.tsx
# or
cat src/main.ts
# or
cat src/App.tsx
```

### 3.2 Extract Imports

For each file read, extract ALL imports:

```
// Example: src/App.tsx
import { Header } from './components/Header'        → Read src/components/Header.tsx
import { useAuth } from './hooks/useAuth'          → Read src/hooks/useAuth.ts
import { SwapPage } from './pages/Swap'            → Read src/pages/Swap.tsx
import { StakingService } from './services/staking' → Read src/services/staking.ts
import { config } from './config'                  → Read src/config.ts
```

### 3.3 Follow Each Import

```bash
# For each import found, read the file
cat src/components/Header.tsx
cat src/hooks/useAuth.ts
cat src/pages/Swap.tsx
cat src/services/staking.ts
cat src/config.ts
```

### 3.4 Continue Recursively

Each file may have its own imports - follow them all:

```
src/pages/Swap.tsx imports:
├── ./components/TokenSelector → Read
├── ./hooks/useSwap            → Read
├── ../utils/formatAmount      → Read
└── @/store/swapStore          → Read

Continue until ALL files are read!
```

### 3.5 Document Each File

As you read each file, document:

| File Path | Purpose | Exports | Dependencies |
|-----------|---------|---------|--------------|
| src/components/Header.tsx | Navigation header | Header component | useAuth, useWallet |
| src/hooks/useSwap.ts | Swap logic hook | useSwap | swapService, tokenStore |
| src/services/staking.ts | Staking API calls | stake, unstake, getRewards | api, config |

## Phase 4: Module & Function Mapping

**After reading all files, create module map:**

```markdown
# Module Map

## Module: Authentication (src/auth/)
Entry file: src/auth/index.ts
Files:
- src/auth/AuthProvider.tsx - Auth context provider
- src/auth/useAuth.ts - Auth hook
- src/auth/LoginForm.tsx - Login form component
- src/auth/guards.ts - Route guards

Functions:
- login(credentials) - User login
- logout() - User logout
- register(data) - New user registration
- resetPassword(email) - Password reset

## Module: Swap (src/features/swap/)
Entry file: src/features/swap/index.ts
Files:
- src/features/swap/SwapPage.tsx - Main swap page
- src/features/swap/SwapForm.tsx - Swap input form
- src/features/swap/TokenSelector.tsx - Token dropdown
- src/features/swap/useSwap.ts - Swap logic
- src/features/swap/swapService.ts - API calls

Functions:
- getQuote(from, to, amount) - Get swap quote
- executeSwap(params) - Execute token swap
- getTokenList() - Fetch available tokens
- approveToken(token, amount) - ERC20 approval

## Module: Staking (src/features/staking/)
...
```

## Phase 5: Dependency Research

**Check package.json for all dependencies:**

```bash
cat package.json
```

**For EVERY unfamiliar package, WebSearch:**

```
Found: @uniswap/sdk
→ WebSearch: "uniswap sdk documentation"
→ Learn: DEX swap functionality

Found: @rainbow-me/rainbowkit
→ WebSearch: "rainbowkit wallet connection"
→ Learn: Wallet connection UI

Found: recharts
→ WebSearch: "recharts react library"
→ Learn: Chart/graph components
```

**Document what each dependency provides:**

| Package | Purpose | UI Components | Functions |
|---------|---------|---------------|-----------|
| @uniswap/sdk | Token swaps | - | getQuote, swap |
| rainbowkit | Wallet UI | ConnectButton, Modal | connect, disconnect |
| recharts | Charts | LineChart, BarChart | - |

## Phase 6: Visual UI Analysis

**Code analysis alone misses visual features. You MUST see the actual UI.**

### 6.1 Start Dev Server

```bash
npm run dev
# Wait for server ready message
```

### 6.2 Take Screenshots of ALL Pages

```bash
SKILL_DIR="/Users/duxiaofeng/code/agent-skills/web-test"

# Homepage
node $SKILL_DIR/scripts/test-helper.js navigate "http://localhost:3000" --headed --keep-open
node $SKILL_DIR/scripts/test-helper.js screenshot research-home.jpg --headed --keep-open

# Navigate to each route found in code
node $SKILL_DIR/scripts/test-helper.js navigate "http://localhost:3000/swap" --headed --keep-open
node $SKILL_DIR/scripts/test-helper.js screenshot research-swap.jpg --headed --keep-open

# Scroll to see more content
node $SKILL_DIR/scripts/test-helper.js scroll down 500 --headed --keep-open
node $SKILL_DIR/scripts/test-helper.js screenshot research-scroll.jpg --headed --keep-open
```

### 6.3 Analyze Screenshots for Missing Features

Compare code analysis with UI screenshots:

| Found in Code | Found in UI | Action |
|---------------|-------------|--------|
| SwapForm component | Swap interface | ✓ Covered |
| - | TradingView chart | Add to features! |
| - | Token logo images | Add to features! |
| - | Social links footer | Add to features! |

### 6.4 Check Different Screen Sizes

```bash
# Desktop (1920x1080)
node $SKILL_DIR/scripts/test-helper.js set-viewport 1920 1080 --headed --keep-open
node $SKILL_DIR/scripts/test-helper.js screenshot research-desktop.jpg --headed --keep-open

# Tablet (768x1024)
node $SKILL_DIR/scripts/test-helper.js set-viewport 768 1024 --headed --keep-open
node $SKILL_DIR/scripts/test-helper.js screenshot research-tablet.jpg --headed --keep-open

# Mobile (375x667)
node $SKILL_DIR/scripts/test-helper.js set-viewport 375 667 --mobile --headed --keep-open
node $SKILL_DIR/scripts/test-helper.js screenshot research-mobile.jpg --headed --keep-open
```

**Document layout differences:**

| Element | Desktop | Tablet | Mobile |
|---------|---------|--------|--------|
| Navigation | Horizontal menu | Horizontal menu | Hamburger menu |
| Swap form | Side panel | Centered | Full width |
| Token list | Grid (4 cols) | Grid (3 cols) | List view |

## Phase 7: Role & Permission Analysis

```
╔════════════════════════════════════════════════════════════════╗
║  ⚠️  CRITICAL: ANALYZE ALL USER ROLES & PERMISSIONS            ║
╠════════════════════════════════════════════════════════════════╣
║                                                                ║
║  Search for role/permission patterns in code:                  ║
║                                                                ║
║  1. Role definitions (admin, user, guest, owner)               ║
║  2. Permission checks (canAccess, isAllowed, hasPermission)    ║
║  3. Protected routes (RequireAuth, ProtectedRoute)             ║
║  4. Role-based UI (show/hide based on role)                    ║
║                                                                ║
║  Test that each role:                                          ║
║  ✓ CAN access features they should have                        ║
║  ✓ CANNOT access features they shouldn't have                  ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
```

**Search for role patterns:**

```bash
# Find role definitions
grep -rn "role\|permission\|admin\|owner\|guest" --include="*.ts" --include="*.tsx" src/

# Find route guards
grep -rn "ProtectedRoute\|RequireAuth\|isAuthenticated\|canAccess" --include="*.ts" --include="*.tsx" src/

# Find conditional rendering based on role
grep -rn "isAdmin\|isOwner\|hasRole\|userRole" --include="*.ts" --include="*.tsx" src/
```

**Document roles and permissions:**

```markdown
# Role & Permission Matrix

## Roles Identified
1. **Guest** - Unauthenticated visitor
2. **User** - Logged in regular user
3. **Admin** - Administrator with elevated privileges
4. **Owner** - System owner with full access

## Permission Matrix

| Feature | Guest | User | Admin | Owner |
|---------|-------|------|-------|-------|
| View public pages | ✓ | ✓ | ✓ | ✓ |
| Connect wallet | ✓ | ✓ | ✓ | ✓ |
| Execute swap | ✗ | ✓ | ✓ | ✓ |
| View own transactions | ✗ | ✓ | ✓ | ✓ |
| View all transactions | ✗ | ✗ | ✓ | ✓ |
| Modify settings | ✗ | ✗ | ✓ | ✓ |
| Delete users | ✗ | ✗ | ✗ | ✓ |
| System configuration | ✗ | ✗ | ✗ | ✓ |

## Protected Routes

| Route | Required Role | Redirect if Unauthorized |
|-------|--------------|-------------------------|
| /dashboard | User+ | /login |
| /admin | Admin+ | /403 |
| /settings | Owner | /403 |
```

## Phase 8: Generate Comprehensive Analysis

**Output format for web-test-case-gen:**

```markdown
# Project Analysis Report

## Project Overview

- **Name:** [from package.json]
- **Type:** Web3 DApp / Traditional Web App
- **Framework:** React / Vue / Next.js / etc
- **Dev Server:** npm run dev → http://localhost:3000

## Documentation Found

| Document | Location | Key Requirements |
|----------|----------|------------------|
| README.md | ./README.md | [summary] |
| Design Spec | ./docs/design.md | [summary] |
| API Docs | ./docs/api.md | [summary] |

## Dependencies Researched

| Package | Purpose | Features Provided |
|---------|---------|-------------------|
| wagmi | Wallet connection | connect, disconnect, sign |
| @uniswap/sdk | Token swaps | getQuote, executeSwap |

## Module Map (from Code Tree Traversal)

### Module: [Name]
- **Entry File:** src/[module]/index.ts
- **Files Read:**
  - src/[module]/Component.tsx - [purpose]
  - src/[module]/hook.ts - [purpose]
  - src/[module]/service.ts - [purpose]
- **Functions:**
  - function1(params) - [description]
  - function2(params) - [description]
- **UI Components:**
  - Component1 - [description]
  - Component2 - [description]

### Module: [Next Module]
...

## Features Summary

| Feature | Module | Entry File | Key Functions | UI Components |
|---------|--------|------------|---------------|---------------|
| Token Swap | swap | src/swap/index.ts | executeSwap, getQuote | SwapForm, TokenSelector |
| Staking | staking | src/staking/index.ts | stake, unstake | StakingForm |
| Wallet Connect | wallet | src/wallet/index.ts | connect, disconnect | ConnectButton |

## Visual-Only Discoveries (from Screenshots)

| Feature | Screenshot | Description | Not in Code Because |
|---------|------------|-------------|---------------------|
| TradingView Chart | research-home.jpg | Price chart widget | Third-party embed |
| Token Logos | research-swap.jpg | Token icon images | CDN/external source |

## Layout Analysis

| Viewport | Width | Screenshot | Key Differences |
|----------|-------|------------|-----------------|
| Desktop | 1920px | research-desktop.jpg | Full navigation, side panels |
| Tablet | 768px | research-tablet.jpg | Stacked layout |
| Mobile | 375px | research-mobile.jpg | Hamburger menu, single column |

## Role & Permission Analysis

### Roles
1. Guest - [description]
2. User - [description]
3. Admin - [description]

### Permission Matrix
[table as shown above]

### Protected Routes
[table as shown above]

## Test Coverage Requirements

Based on analysis, the following test types are needed:

### 1. Flow Tests (per module)
For each module, test complete user flows:
- Happy path: Complete flow from start to finish
- Alternative paths: Different routes through the flow
- Error recovery: What happens when errors occur

### 2. UI Layout Tests
- Desktop layout verification
- Tablet layout verification
- Mobile layout verification
- Responsive transitions

### 3. Functionality Tests
For each function identified:
- Does it work correctly with valid input?
- Does it handle invalid input properly?
- Are error messages clear and helpful?
- Does form validation work?
- Does network error handling work?

### 4. Network Tests
- High latency behavior
- Request timeout handling
- Packet loss recovery
- Retry logic verification

### 5. Role & Permission Tests
For each role identified:
- Can access permitted features
- Cannot access restricted features
- Proper error messages when denied
- Role switching behavior

## Files Read (Complete List)

[List every file that was read during tree traversal]

1. src/index.tsx
2. src/App.tsx
3. src/components/Header.tsx
4. src/hooks/useAuth.ts
5. src/pages/Swap.tsx
...
[Continue until all files listed]

## Execution Order Recommendation

Based on dependencies between modules:

1. WALLET tests (no dependencies)
2. AUTH tests (may depend on wallet)
3. SWAP tests (depends on wallet + auth)
4. STAKING tests (depends on wallet + auth)
5. ADMIN tests (depends on admin role)
```

## Key Rules

1. **Read EVERY file** - Don't skip any file in the codebase
2. **Follow ALL imports** - Tree traversal must be complete
3. **Find documentation** - README, design docs, architecture docs
4. **Research unknowns** - WebSearch any unfamiliar package
5. **See the UI** - Screenshots reveal hidden features
6. **Map all roles** - Identify every user role and permission
7. **Document everything** - Complete map for test case generation

## Usage

This skill can be used in two ways:

1. **Automatically** - Called by `web-test-case-gen` as its first step
2. **Standalone** - Run directly to analyze a project without generating test cases

## Related Skills

| Skill | Relationship |
|-------|--------------|
| web-test-case-gen | Calls this skill first, then generates test cases |
| web-test | Provides test-helper.js for screenshots |
| web-test-wallet-setup | Sets up wallet (if Web3 DApp detected) |
| web-test-wallet-connect | Connects wallet (if Web3 DApp detected) |
