---
name: clink-codex-delegate
description: Activate when user mentions "clink codex" to provide guidance on delegating implementation tasks to clink codex as a junior developer. Use when assigning coding tasks, discussing task delegation, or working with clink codex for code implementation.
---

# Clink Codex Task Delegation Guide

When delegating tasks to clink codex, treat it like a junior developer. This skill provides a standardized approach to task assignment.

## 🎯 Core Principles

### What to Delegate to Clink Codex
Clink Codex can handle **all types of coding tasks**:

- ✅ **Implementation tasks**: Writing code logic, functions, components
- ✅ **Code generation**: Creating new files, modules, classes
- ✅ **Logic implementation**: Business logic, algorithms, data processing
- ✅ **Research & Analysis**: Investigating architecture, analyzing codebases
- ✅ **Design**: System design, architecture decisions
- ✅ **Testing**: Writing tests, running tests, debugging
- ✅ **Code Review**: Reviewing code quality, best practices
- ✅ **Documentation**: Writing docs, comments, READMEs
- ✅ **Refactoring**: Code optimization, restructuring
- ✅ **Bug fixing**: Debugging and resolving issues

### Important: Provide Full Context
When delegating any task, always provide:
- **Project context**: What the project does, tech stack, conventions
- **Relevant files**: Paths to files that need to be read/modified
- **Dependencies**: Related modules, APIs, or external services
- **Constraints**: Any limitations or requirements to follow

## 📝 Your Responsibilities (After Clink Codex Completes Task)
1. **Verify** the output meets requirements
2. **Validate** the code works as expected
3. **Integrate** the changes into the project
4. **Iterate** if needed - provide specific feedback and re-delegate

## ⚠️ Important Notes
- **Provide full context** - Codex works best with comprehensive information
- **Be specific** - Clear requirements lead to better results
- **If codex fails** - Switch to **clink gemini** as fallback (see Fallback section below)
- **If code doesn't meet requirements** - Provide specific feedback and re-delegate

---

## 📋 Standard Task Brief Template

Use this template when delegating tasks to clink codex:

```markdown
## 🎯 Task Title

Implement [specific feature or logic]

---

### 🧩 Context

[Brief summary about the project, module, and task context]

Example: "This module handles swap logic for LP Copilot, currently building the impermanent loss calculation feature"

---

### 📋 Requirements/User Stories

- [List each specific requirement as bullet points, the more detailed the better]
- Input: [data type, structure, parameters]
- Output: [return type, format]
- Constraints: [any limitations or conditions]

---

### 💡 Known Workarounds / Assumptions

- [List any workarounds or assumptions, e.g., "assume balance is always > 0", "skip cache", "mock API response with temporary JSON file"]
- [Any temporary solutions or shortcuts]
- [Dependencies that might not be available yet]

---

### 🧱 Technical Hints

- **File to edit**: `/path/to/file.ts`
- **Function name**: `functionName`
- **Framework/Libs**: [specify if needed, e.g., ethers.js, uniswap-sdk, lodash]
- **Code Style**: [ESM, async/await, TypeScript strict mode, etc.]
- **Related files**: [list files that provide context or dependencies]
- **Test command**: [if testing is needed, e.g., `npm test`, `pytest`]

---

### ✅ Acceptance Criteria

- [ ] Code compiles successfully
- [ ] Logic matches requirements
- [ ] No dead code or unnecessary comments
- [ ] Clean and readable code

---
```

## 🔄 Workflow Process

### 1. **Before Delegating**
Ensure you have:
- ✅ Clear understanding of the **goal** (what needs to be accomplished)
- ✅ Identified **assumptions and known workarounds**
- ✅ Defined **scope** (what tasks codex should complete)
- ✅ Specified **entry point** (specific file, function, module, or repo)
- ✅ Gathered **full context** (related files, dependencies, project conventions)

### 🔀 Fallback: Switch to Clink Gemini

If **clink codex** encounters errors or fails to complete the task:

1. **Identify the error** - Note what went wrong (timeout, API error, incomplete output, etc.)
2. **Switch to clink gemini** - Use the same task brief template
3. **Adjust if needed** - Gemini may have different capabilities, adjust requirements if necessary

**When to switch to clink gemini:**
- ❌ Codex returns errors or timeouts
- ❌ Codex output is incomplete or corrupted
- ❌ Codex cannot handle the specific task type
- ❌ Multiple failed attempts with codex

**Example fallback command:**
```
Use clink gemini instead of codex for this task
```

**Note:** Both clink codex and clink gemini follow the same task brief template and workflow. The switch should be seamless.

### 2. **During Delegation**
- Use the standard template above
- Be specific and detailed in requirements
- Provide context about the project/module
- List all assumptions and workarounds
- Specify technical constraints

### 3. **After Completion**
- Review the implementation
- Run tests yourself
- Debug any issues
- Either:
  - ✅ Accept and integrate the code
  - 🔄 Provide specific feedback and re-delegate with corrections

## 💡 Best Practices

1. **Be Specific**: The more detailed your requirements, the better the implementation
2. **Provide Context**: Help clink codex understand the bigger picture
3. **List Assumptions**: Make implicit knowledge explicit
4. **Specify Entry Points**: Don't make clink codex guess where to start
5. **Use Real Data**: Follow project guidelines - no mock data unless specified
6. **Iterate if Needed**: If first attempt doesn't meet requirements, refine and re-delegate

## 🚨 Quality Control

Always verify:
- Code compiles and builds successfully
- Logic is implemented correctly
- No placeholder code or TODOs
- Follows project conventions
- Ready for real-world use (no mocks unless explicitly requested)

---

## Example Task Delegation

```markdown
## 🎯 Task: Implement Order Processing Logic

---

### 🧩 Context

Building the order processing module for Shopfia e-commerce platform. This handles customer orders from cart to payment processing.

---

### 📋 Requirements

- Create `processOrder` function in `/src/services/orderService.ts`
- Input: `{ userId: string, cartItems: CartItem[], paymentMethod: string }`
- Output: `{ orderId: string, status: string, total: number }`
- Validate cart items exist and are in stock
- Calculate total including tax and shipping
- Create order record in database
- Return order confirmation

---

### 💡 Known Workarounds / Assumptions

- Payment gateway integration will be added later - for now just validate payment method is provided
- Tax calculation is flat 10% rate (will use real tax API later)
- Shipping is calculated as $10 flat rate for now

---

### 🧱 Technical Hints

- File to edit: `/src/services/orderService.ts`
- Function name: `processOrder`
- Framework/Libs: TypeScript, Prisma for DB
- Code Style: async/await, TypeScript strict mode
- Related files: `/src/types/order.ts`, `/src/services/cartService.ts`
- Test command: `npm test -- orderService`

---

### ✅ Acceptance Criteria

- [ ] Function signature matches requirements
- [ ] All validation logic implemented
- [ ] Order creation works with Prisma
- [ ] Returns correct response format
- [ ] Clean, readable code with proper error handling
```

---

Remember: Clink codex can handle all coding tasks when given proper context. Provide comprehensive information for best results. If codex fails, switch to clink gemini as fallback.
