---
name: rust-borrow-checker
description: Debug Rust ownership, borrowing, and lifetime errors. Use when encountering borrow checker errors (E0382, E0502, E0597, etc.) or when code won't compile due to ownership issues.
---

<essential_principles>
The Rust borrow checker enforces memory safety at compile time through three rules:

1. **Each value has exactly one owner** - When the owner goes out of scope, the value is dropped
2. **You can have either one mutable reference OR any number of immutable references** - Never both simultaneously
3. **References must always be valid** - No dangling references, lifetimes must be sufficient

Understanding these rules is the key to fixing borrow checker errors.
</essential_principles>

<intake>
What would you like help with?

1. Diagnose a borrow checker error (paste the error)
2. Fix a lifetime annotation issue
3. Fix an ownership transfer problem
4. Fix a mutable/immutable borrow conflict
5. Understand a specific error code

**Paste the compiler error or describe the issue, then I'll route to the appropriate workflow.**
</intake>

<routing>
| Response | Workflow |
|----------|----------|
| Error message pasted, "diagnose", "error", "E0XXX" | `workflows/diagnose-error.md` |
| "lifetime", "'a", "outlives", "E0597", "E0621" | `workflows/fix-lifetime.md` |
| "move", "moved", "ownership", "E0382", "E0507" | `workflows/fix-ownership.md` |
| "borrow", "mutable", "immutable", "E0502", "E0499" | `workflows/fix-borrowing.md` |
| Other | Clarify, then select appropriate workflow |
</routing>

<quick_fixes>
Common solutions for frequent errors:

**E0382 (use of moved value)**: Clone, use references, or restructure to avoid the move
**E0502 (cannot borrow as mutable, already borrowed as immutable)**: Separate the borrows into different scopes, or use interior mutability (RefCell, Mutex)
**E0499 (cannot borrow as mutable more than once)**: Split into separate scopes or use indices instead of references
**E0597 (borrowed value does not live long enough)**: Extend the lifetime of the owner, or use owned types instead
**E0506 (cannot assign, already borrowed)**: Complete borrow before assignment, or use Cell/RefCell
</quick_fixes>

<reference_index>
Domain knowledge in `references/`:

**Core Rules:**
- ownership-rules.md - The three ownership rules with examples
- borrowing-rules.md - Borrowing and reference rules
- lifetime-syntax.md - Lifetime annotation patterns and elision

**Problem Solving:**
- common-errors.md - Detailed breakdown of E0XXX errors
- patterns.md - Clone, Rc, Arc, RefCell, Cow patterns
</reference_index>

<workflows_index>
| Workflow | Purpose |
|----------|---------|
| diagnose-error.md | Systematically diagnose any borrow checker error |
| fix-lifetime.md | Resolve lifetime annotation issues |
| fix-ownership.md | Fix ownership transfer problems |
| fix-borrowing.md | Handle borrow conflicts |
</workflows_index>

<success_criteria>
A fix is complete when:
- `cargo check` passes without borrow checker errors
- The solution doesn't introduce unnecessary cloning
- The fix maintains the original intent of the code
- Lifetimes are as simple as possible (rely on elision when possible)
</success_criteria>
