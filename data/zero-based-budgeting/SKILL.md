---
name: zero-based-budgeting
description: Expert knowledge in zero-based budgeting principles and implementation
triggers: [budget, allocation, zero-based, ready to assign, available, rollover, spending]
---

# Zero-Based Budgeting Skill

## Core Principle

**Give every dollar a job.** In zero-based budgeting, you allocate all of your income to specific categories until you have zero dollars left unassigned.

```
Income - Allocations = $0
```

## Key Concept: Ready to Assign

**Formula:**
```
Ready to Assign = Total Account Balance - Total Allocated Amount
```

**Goal:** Ready to Assign should be $0.00

**Example:**
```
Account Balances:
  Checking:     $5,000
  Savings:      $2,000
  Credit Card:   -$500
  Total:        $6,500

Allocated to Categories:
  Rent:         $1,200
  Groceries:      $500
  Gas:            $200
  Savings Goal: $1,000
  Total:        $2,900

Ready to Assign: $6,500 - $2,900 = $3,600

❌ Not zero-based yet! Allocate the remaining $3,600
```

## Implementation Formula

### 1. Calculate Ready to Assign

```go
func CalculateReadyToAssign(accounts []Account, allocations []Allocation) int {
    totalBalance := 0
    for _, account := range accounts {
        totalBalance += account.Balance  // Includes negative credit card balances
    }

    totalAllocated := 0
    for _, allocation := range allocations {
        totalAllocated += allocation.Amount  // All allocations, all periods
    }

    return totalBalance - totalAllocated
}
```

**Key Points:**
- Include ALL accounts (checking, savings, credit cards)
- Credit card balances are negative (reduce total balance)
- Include ALL allocations (not just current period)
- Updates in real-time as accounts or allocations change

### 2. Calculate Category Available (with Rollover)

**Formula:**
```
Available = Sum(All Allocations for Category) - Sum(All Spending for Category)
```

**Example:**
```go
func CalculateCategoryAvailable(categoryID string, allocations []Allocation, transactions []Transaction) int {
    totalAllocated := 0
    for _, alloc := range allocations {
        if alloc.CategoryID == categoryID {
            totalAllocated += alloc.Amount
        }
    }

    totalSpent := 0
    for _, txn := range transactions {
        if txn.CategoryID == categoryID && txn.Amount < 0 {
            totalSpent += -txn.Amount  // Negative amounts are expenses
        }
    }

    return totalAllocated - totalSpent
}
```

**Key Points:**
- Include ALL history (automatic rollover)
- Don't filter by period for available calculation
- Unspent money automatically carries forward
- Negative available = overspending (allowed)

### 3. Period Summary

For a specific period (e.g., "2024-01"):

```go
type CategorySummary struct {
    CategoryID string
    Name       string
    Allocated  int  // Amount allocated THIS period
    Spent      int  // Amount spent THIS period
    Available  int  // Total available (includes ALL history)
}
```

**Example:**
```
January Budget:
  Groceries:
    Allocated: $500 (January allocation)
    Spent: $450 (January spending)
    Available: $50 (rolled over to February)

February Budget:
  Groceries:
    Allocated: $500 (February allocation)
    Spent: $550 (February spending)
    Available: $0 (used February allocation + January rollover)
```

## Rollover Behavior

### How Rollover Works

Unspent money automatically carries forward to future periods.

**Month 1:**
```
Groceries allocated: $500
Groceries spent: $400
Remaining: $100 (rolls over)
```

**Month 2:**
```
Groceries allocated: $500
Available before spending: $600 ($500 new + $100 rollover)
Groceries spent: $550
Remaining: $50
```

### Implementation

```go
// Rollover is automatic because available includes ALL history
func GetAllocationSummary(period string, categoryID string) *CategorySummary {
    // Get allocation for THIS period
    allocation := getAllocationForPeriod(categoryID, period)

    // Get spending for THIS period only
    spent := getSpendingForPeriod(categoryID, period)

    // Get available including ALL history (automatic rollover)
    available := getAllTimeAllocated(categoryID) - getAllTimeSpent(categoryID)

    return &CategorySummary{
        Allocated: allocation.Amount,  // This period only
        Spent:     spent,               // This period only
        Available: available,           // All time (includes rollover)
    }
}
```

## Credit Card Budgeting

Credit cards are budgeted differently to track debt and payments.

### Credit Card Rules

1. **Balance is Negative**: Credit card balance represents debt owed
2. **Payment Category**: Each credit card gets a payment category
3. **Spending Behavior**: Spending on credit card moves budget from expense category to payment category

### Credit Card Flow

```
Initial State:
  Credit Card Balance: -$500 (owe $500)
  Payment Category Available: $0

Step 1: Buy groceries on credit card ($100)
  Credit Card Balance: -$600 (owe $600 now)
  Groceries Available: $300 → $200 (used $100 of grocery budget)
  Payment Category Available: $0 → $100 (auto-allocated for payment)

Step 2: Pay credit card from checking ($600)
  Checking Balance: $5,000 → $4,400
  Credit Card Balance: -$600 → $0 (debt paid off)
  Payment Category Available: $100 → -$500 (overspent by $500)
```

### Implementation

```go
// When credit card transaction is created
func OnCreditCardTransaction(txn *Transaction) {
    // 1. Update credit card balance
    creditCard.Balance += txn.Amount  // Negative amount increases debt

    // 2. If spending (negative amount), move budget
    if txn.Amount < 0 {
        expenseCategory := getCategoryByID(txn.CategoryID)
        paymentCategory := getCreditCardPaymentCategory(txn.AccountID)

        // Spending decreases expense category available
        // and increases payment category available
        // (This happens automatically through available calculation)
    }
}
```

## Validation Rules

### Allocation Validation

```go
func ValidateAllocation(allocation *Allocation) error {
    // Only expense categories can be allocated
    category := getCategoryByID(allocation.CategoryID)
    if category.Type == "income" {
        return errors.New("cannot allocate to income category")
    }

    // Amount must be positive
    if allocation.Amount <= 0 {
        return errors.New("allocation amount must be positive")
    }

    // Period format must be YYYY-MM
    if !isValidPeriod(allocation.Period) {
        return errors.New("period must be in YYYY-MM format")
    }

    return nil
}
```

### One Allocation Per Category Per Period

```go
// Database constraint
CREATE UNIQUE INDEX idx_unique_allocation
ON allocations(category_id, period);

// Upsert behavior
func CreateOrUpdateAllocation(allocation *Allocation) error {
    existing := findAllocation(allocation.CategoryID, allocation.Period)
    if existing != nil {
        return updateAllocation(existing.ID, allocation)
    }
    return createAllocation(allocation)
}
```

## Common Scenarios

### Scenario 1: Starting Fresh

```
1. Create accounts and add balances
   → Ready to Assign: $6,500

2. Create categories (Rent, Groceries, Gas, etc.)

3. Allocate money to categories
   Rent: $1,200
   Groceries: $500
   Gas: $200
   ...
   → Ready to Assign: $4,600 (still have money to allocate)

4. Continue allocating until Ready to Assign = $0
```

### Scenario 2: Monthly Budgeting

```
New month starts:
1. Check Ready to Assign (income from last month + unspent)
2. Create allocations for new month
3. Allocate money to categories
4. Track spending throughout month
5. Rollover happens automatically
```

### Scenario 3: Overspending

```
Budget: $500
Spent: $600
Available: -$100 (overspent)

Options:
1. Accept it (overspending is allowed)
2. Move money from another category
3. Allocate more money to cover overspending
```

### Scenario 4: Moving Money

```
Groceries Available: $50
Gas Available: $200

Reduce Gas allocation: -$100
Increase Groceries allocation: +$100

Result:
Groceries Available: $150
Gas Available: $100
```

## Testing Zero-Based Budgeting Logic

### Test Case 1: Ready to Assign Calculation

```go
func TestReadyToAssign(t *testing.T) {
    accounts := []Account{
        {Balance: 500000},  // $5,000 checking
        {Balance: 200000},  // $2,000 savings
        {Balance: -50000},  // -$500 credit card
    }
    // Total: $6,500

    allocations := []Allocation{
        {Amount: 120000},  // $1,200 rent
        {Amount: 50000},   // $500 groceries
    }
    // Total: $1,700

    readyToAssign := CalculateReadyToAssign(accounts, allocations)
    expected := 480000  // $4,800

    if readyToAssign != expected {
        t.Errorf("Expected %d, got %d", expected, readyToAssign)
    }
}
```

### Test Case 2: Rollover Behavior

```go
func TestRollover(t *testing.T) {
    categoryID := "groceries"

    // January: Allocate $500, Spend $400
    allocations := []Allocation{
        {CategoryID: categoryID, Amount: 50000, Period: "2024-01"},
    }
    transactions := []Transaction{
        {CategoryID: categoryID, Amount: -40000, Date: "2024-01-15"},
    }

    available := CalculateCategoryAvailable(categoryID, allocations, transactions)
    expected := 10000  // $100 rolled over

    if available != expected {
        t.Errorf("Expected rollover of %d, got %d", expected, available)
    }

    // February: Allocate $500, Spend $550
    allocations = append(allocations,
        Allocation{CategoryID: categoryID, Amount: 50000, Period: "2024-02"},
    )
    transactions = append(transactions,
        Transaction{CategoryID: categoryID, Amount: -55000, Date: "2024-02-15"},
    )

    available = CalculateCategoryAvailable(categoryID, allocations, transactions)
    expected = 5000  // $50 left ($100 rollover + $500 Feb - $550 spent)

    if available != expected {
        t.Errorf("Expected %d, got %d", expected, available)
    }
}
```

## Common Mistakes

### ❌ Filtering Available by Period

```go
// WRONG: Don't filter available by period
available := getAllocationsForPeriod(period) - getSpendingForPeriod(period)

// CORRECT: Include all history
available := getAllAllocations() - getAllSpending()
```

### ❌ Not Including Credit Cards in Ready to Assign

```go
// WRONG: Only checking/savings
totalBalance := checkingBalance + savingsBalance

// CORRECT: Include credit card debt
totalBalance := checkingBalance + savingsBalance + creditCardBalance  // negative
```

### ❌ Preventing Overspending

```go
// WRONG: Don't prevent overspending
if spending > available {
    return errors.New("insufficient funds")
}

// CORRECT: Allow overspending (user's choice)
// Just show negative available
```

## Quick Reference

**Ready to Assign:**
```
Total Balance - Total Allocated = Ready to Assign
Goal: $0
```

**Category Available:**
```
All Allocations - All Spending = Available
Includes automatic rollover
```

**Period Summary:**
```
Allocated: This period only
Spent: This period only
Available: All history
```

**Credit Cards:**
```
Negative balance = debt
Payment category auto-created
Spending moves budget automatically
```
