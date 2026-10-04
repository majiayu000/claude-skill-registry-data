---
name: smells
description: Analyze a class or module for code smells and produce a prioritized refactoring plan. Use when the user asks for code smell analysis, says `/smells`, or runs `/refactor:smells`.
metadata:
  legacy-name: refactor:smells
---

Analyze the provided class for code smells and create a refactoring plan.

## Usage
```
/smells $ARGUMENTS
```

## Analysis Output

### 📊 Code Smell Analysis for: $ARGUMENTS

#### 🔍 Top 5 Code Smells Detected:

1. **Poor Naming Conventions**
   - Generic variable names (data, temp, obj, result)
   - Non-descriptive method names (process, handle, do)
   - Inconsistent naming patterns
   - **Fix**: Rename to domain-specific terms that describe purpose

2. **Long Method**
   - Methods exceeding 20-30 lines
   - Multiple responsibilities in single method
   - Difficult to test and understand
   - **Fix**: Extract smaller, focused methods with single responsibilities

3. **Large Class (God Object)**
   - Too many responsibilities in one class
   - High number of instance variables
   - Violates Single Responsibility Principle
   - **Fix**: Split into smaller, cohesive classes

4. **Duplicate Code**
   - Copy-pasted logic across methods
   - Similar patterns with slight variations
   - **Fix**: Extract common logic into reusable methods

5. **Feature Envy**
   - Methods that use data from other classes more than their own
   - Excessive getter/setter calls to another object
   - **Fix**: Move method to the class it's most interested in

### 📋 Refactoring Plan

#### Phase 1: Name Refactoring (No Behavior Changes)
- [ ] Identify all poorly named variables, methods, and fields
- [ ] Map current names to descriptive alternatives
- [ ] Ensure naming follows language conventions:
  - Java/JavaScript: camelCase for methods/variables, PascalCase for classes
  - Python: snake_case for functions/variables, PascalCase for classes
- [ ] Update all references throughout codebase
- [ ] Run tests to ensure no behavioral changes

#### Phase 2: Structure Improvements
- [ ] Address long methods by identifying extraction points
- [ ] Plan class decomposition for God Objects
- [ ] Identify duplicate code patterns for consolidation
- [ ] Map feature envy methods to their proper homes

#### Phase 3: Implementation Order
1. **Start with naming** - Low risk, high readability impact
2. **Extract methods** - Reduce complexity incrementally
3. **Remove duplication** - Create reusable components
4. **Reorganize classes** - Move methods to appropriate classes
5. **Split large classes** - Final structural improvements

### 🎯 Success Criteria
- All tests pass after each refactoring step
- Code coverage remains the same or improves
- Cyclomatic complexity reduced
- Improved readability scores
- No behavioral changes introduced

### ⚠️ Risk Mitigation
- Create comprehensive test suite before refactoring
- Use version control for easy rollback
- Refactor in small, reviewable commits
- Document all name mappings
- Review with team before major structural changes

## Example Name Refactorings
```
// Before
getData() → fetchCustomerPurchaseHistory()
processItems() → calculateMonthlyRevenue()
userObj → customerProfile
temp → filteredTransactions
data → invoiceRecords
doStuff() → validatePaymentCredentials()
```

## Next Steps
1. Review the identified code smells
2. Prioritize based on impact and risk
3. Begin with Phase 1 naming refactors
4. Proceed incrementally through the plan
5. Measure improvements after each phase
