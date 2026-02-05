---
name: Code Archaeology
description: Systematic techniques for reading and understanding unfamiliar legacy code without documentation
when_to_use: when encountering unfamiliar legacy code and need to understand what it does, why it exists, and how it works
version: 1.0.0
languages: all
---

# Code Archaeology

## Overview

Legacy code is code without context. Code archaeology is the systematic process of excavating that context from the code itself, its history, and its runtime behavior.

**Core principle:** Read code like a detective, not a compiler. Look for clues about intent, not just mechanics.

## When to Use

Use code archaeology when:
- Encountering unfamiliar codebase without documentation
- Need to modify code you didn't write
- Investigating why code was written this way
- Before refactoring or adding features
- Understanding legacy system architecture

## The Archaeology Process

### Phase 1: Survey the Landscape

**Before diving into details, get the big picture:**

1. **Identify Entry Points**
   - Main functions, API endpoints
   - Event handlers, controllers
   - What triggers this code to run?

2. **Map the Territory**
   - Directory structure
   - Module organization
   - Key abstractions and their relationships

3. **Find the Documentation**
   - README files (even outdated ones have clues)
   - Code comments (especially "why" comments)
   - Tests (they show intended usage)
   - Commit messages in git history

**Quick mapping command:**
```bash
# Find all entry points
find . -name "main.*" -o -name "*Controller*" -o -name "*Handler*" -o -name "Program.cs" -o -name "Startup.cs"

# See directory structure
tree -L 3 -I 'node_modules|vendor|__pycache__|bin|obj'

# Find tests (they document behavior)
find . -name "*test*" -o -name "*spec*" -o -name "*.Tests" -o -name "*.Test"
```

### Phase 2: Follow the Data

**Understanding flow is key to understanding purpose:**

1. **Pick a Concrete Example**
   - Don't start with abstractions
   - Choose specific input/output case
   - "What happens when user logs in?"

2. **Trace Forward (from input)**
   ```
   Input → Where does it enter?
         → How is it transformed?
         → Where does it go?
         → What's the output?
   ```

3. **Trace Backward (from output)**
   ```
   Output → Where is it produced?
          → What data creates it?
          → Where does that data come from?
          → Keep going to the source
   ```

**Example: Understanding authentication:**
```
Forward: POST /login → router → authController.login() → UserService.authenticate() → Database
Backward: JWT token ← TokenService ← User object ← Database query ← Credentials validation
```

### Phase 3: Identify Core Abstractions

**What are the domain concepts?**

1. **Look for Nouns**
   - Classes, types, tables: User, Order, Payment
   - These are domain entities

2. **Look for Verbs**
   - Functions, methods: authenticate(), processPayment()
   - These are domain operations

3. **Find the Boundaries**
   - What talks to what?
   - What's isolated from what?
   - Where are the layers?

**Visualization helps:**
```
Presentation Layer (HTTP, UI)
    ↓
Business Logic Layer (Services, Use Cases)
    ↓
Data Layer (Database, External APIs)
```

### Phase 4: Understand Intent vs Implementation

**Code shows HOW. History shows WHY.**

1. **Git Archaeology**
   ```bash
   # When was this added?
   git log --follow --diff-filter=A -- path/to/file.py

   # Why was it changed?
   git log -p -- path/to/file.py

   # Who knows about it?
   git blame path/to/file.py

   # Find related changes
   git log --all --grep="auth"
   ```

2. **Look for Patterns**
   - Repeated code → probably important concept
   - Complex conditionals → business rules
   - Try/catch blocks → known failure modes
   - Comments saying "HACK" or "TODO" → technical debt

3. **Run the Code**
   - Set breakpoints, observe values
   - Add debug logging
   - See what actually happens vs what code says

## Reading Strategies

### Top-Down Reading

**Start from entry points, drill down:**

Good for:
- Understanding overall flow
- Finding where to start modifying
- Grasping system architecture

**Process:**
1. Find entry point (main, handler, controller)
2. Read function signature → what goes in, what comes out?
3. Scan function body → what are the major steps?
4. Drill into interesting steps
5. Recurse

### Bottom-Up Reading

**Start from utilities, build up:**

Good for:
- Understanding specific components
- Learning domain abstractions
- When top-down is overwhelming

**Process:**
1. Find leaf functions (no dependencies)
2. Understand what they do
3. Find what calls them
4. Build mental model upward
5. Eventually reach entry points

### Breadth-First Reading

**Survey everything shallowly first:**

Good for:
- Very large codebases
- Finding what matters
- Avoiding rabbit holes

**Process:**
1. List all files
2. Read first 20 lines of each
3. Note interesting/critical files
4. Deep dive only into those

## Tools and Techniques

### Static Analysis

```bash
# Find all uses of a function
grep -r "authenticate" --include="*.py" --include="*.js" --include="*.cs"

# Find all classes/types
grep -r "^class " --include="*.py" --include="*.js" --include="*.ts"
grep -r "^\s*public class " --include="*.cs"

# Find configuration
find . -name "*.config" -o -name ".env*" -o -name "settings*" -o -name "appsettings*.json" -o -name "web.config"

# Count lines by directory (complexity proxy)
find . \( -name "*.py" -o -name "*.js" -o -name "*.cs" \) -exec wc -l {} + | sort -n
```

### Dynamic Analysis

**Run code with instrumentation:**

```python
# Python: Add logging to understand flow
import logging
logging.basicConfig(level=logging.DEBUG)

def mystery_function(data):
    logging.debug(f"mystery_function called with: {data}")
    result = complex_operation(data)
    logging.debug(f"mystery_function returning: {result}")
    return result
```

```csharp
// C#: Add logging to understand flow
using Microsoft.Extensions.Logging;

public class MyService
{
    private readonly ILogger<MyService> _logger;

    public string MysteryFunction(string data)
    {
        _logger.LogDebug("MysteryFunction called with: {Data}", data);
        var result = ComplexOperation(data);
        _logger.LogDebug("MysteryFunction returning: {Result}", result);
        return result;
    }
}
```

**Use debugger:**
- Set breakpoint at entry
- Step through execution
- Inspect variables at each step
- Note: "Ah, that's where X comes from!"

### Pattern Recognition

**Common legacy patterns:**

| Pattern | What it means |
|---------|---------------|
| Singleton | Global state (often problematic) |
| Factory | Multiple implementations of same interface |
| Strategy | Pluggable behavior |
| Template Method | Framework with customization points |
| Null checks everywhere | Missing contracts, defensive programming |
| Try/catch around everything | Unstable dependencies or unknown errors |

## Checklist

- [ ] Identified entry points (where does execution start?)
- [ ] Mapped directory structure and module organization
- [ ] Found any existing documentation (README, comments, tests)
- [ ] Traced data flow for concrete example (input → processing → output)
- [ ] Identified core domain concepts (entities, operations)
- [ ] Understood system layers and boundaries
- [ ] Researched git history (when added, why changed, who knows)
- [ ] Recognized patterns and their purposes
- [ ] Ran code with debugging/logging to verify understanding

## Red Flags - You're Doing It Wrong

- "I'll just start changing things" - You don't understand yet. Archaeology first.
- "There's too much code to read" - You don't read all of it. Use strategies.
- "The code is self-explanatory" - Code shows HOW, not WHY. History matters.
- "I'll figure it out as I go" - Plan and map first, modify second.
- Diving into details before understanding big picture - Breadth before depth.

## Common Mistakes

| Mistake | Reality |
|---------|---------|
| "Reading code is slow, I'll just fix it" | Understanding saves hours of debugging. Read first. |
| "I understand what this function does" (after 30 seconds) | Functions exist in context. Understand their role in the system. |
| "This is bad code, I'll rewrite it" | It's solving a problem you don't understand yet. Archaeology first. |
| "I'll read it all linearly" | 100k LOC linearly = weeks. Use strategies. |
| "Comments and docs are outdated, I'll ignore them" | Even outdated docs have clues. They show original intent. |

## Examples

### Example 1: Understanding Authentication (Node.js)

**Goal:** Understand how login works

**Archaeology process:**
```
1. Entry point: POST /api/login endpoint
2. Trace: router.js → authController.login() → AuthService.authenticate()
3. Data flow: {email, password} → validate → query DB → generate JWT
4. Git history: Added in commit abc123 "Implement JWT authentication"
5. Why: Comments mention "replaced session-based auth for API scalability"
6. Pattern: Token-based stateless authentication
7. Tests: test/auth.test.js shows expected behavior
```

**Mental model:** Stateless auth using JWT, validates credentials, returns token for subsequent requests.

### Example 1b: Understanding Authentication (.NET)

**Goal:** Understand how authentication middleware works

**Archaeology process:**
```
1. Entry point: Program.cs or Startup.cs → app.UseAuthentication()
2. Trace: Middleware pipeline → [Authorize] attribute → AuthenticationHandler
3. Data flow: HTTP request → Extract token → Validate → Create ClaimsPrincipal → Controller
4. Git history: Added in commit def456 "Switch to JWT bearer authentication"
5. Why: Comments mention "migrated from cookie auth to support mobile clients"
6. Pattern: ASP.NET Core authentication middleware with JWT bearer
7. Tests: AuthenticationTests.cs shows token validation scenarios
```

**Mental model:** Middleware-based authentication, token validation happens early in pipeline, user identity flows through HttpContext.User to controllers.

### Example 2: Mystery Business Logic

**Code:**
```python
def calculate_price(item, user):
    base = item.price
    if user.is_premium:
        base *= 0.9
    if user.referral_count > 5:
        base *= 0.95
    if item.category == "seasonal":
        base *= 1.2
    return round(base, 2)
```

**Archaeology:**
```
Git log:
- Line 1-2: Original implementation
- Line 3-4: "Add premium discount per marketing request"
- Line 5-6: "Incentivize referrals" (commit by PM)
- Line 7-8: "Seasonal markup for inventory management"

Pattern: Accumulation of business rules over time
Why complex: Different stakeholders, different times
```

**Mental model:** Pricing is business-driven, not technical. Don't "simplify" without understanding business constraints.

## Integration with Other Skills

- **skills/research/tracing-knowledge-lineages** - Why does this code exist?
- **skills/refactoring/characterization-testing** - After understanding, add safety net
- **skills/understanding/questioning-techniques** - Systematic questions to ask
- **skills/debugging/root-cause-tracing** - When code breaks, trace back to source

## Remember

- Read code like a detective: look for clues about intent
- Use multiple strategies: top-down, bottom-up, breadth-first
- Git history is treasure: when/why/who
- Run code to verify understanding
- Pattern recognition speeds comprehension
- Understand before changing
