---
name: State Comparison Patterns
description: Model helper methods for clean state checking instead of verbose Spatie Model States comparisons (63% code reduction)
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
---

# State Comparison Patterns

Use clean helper methods instead of verbose Spatie Model States comparisons.

## When to Use

- Checking submission or card states in application code
- Writing conditional logic based on states
- Querying database for specific states
- Refactoring verbose state comparisons

## The Problem

### ❌ Verbose Spatie Pattern (Don't Use)

```php
// 63% more code than necessary!
(new ($card->card_state)($card))->equals(CardState::QUALITY_CHECK)
(new ($submission->state)($submission))->equals(SubmissionState::COMPLETED)
```

**Issues**:
- Verbose and hard to read
- Repeated boilerplate
- Error-prone (easy to make typos)
- Difficult to maintain

### ✅ Clean Helper Methods (Always Use)

```php
// DRY, SOLID, KISS principles
$card->isCardQualityCheck()
$submission->isCompleted()
```

**Benefits**:
- 63% code reduction
- Improved readability
- Type safety
- Single source of truth
- Zero duplication

## Model Helper Methods

### SubmissionTradingCard Model

**Location**: `app/Models/SubmissionTradingCard.php`

#### State Check Methods

```php
// Check specific state
$card->isCardState(CardState::ASSESSMENT)      // true/false
$card->hasCardStateIn([CardState::ASSESSMENT, CardState::IN_PROGRESS])  // true/false

// Convenience methods for each state
$card->isCardReceived()         // CardState::RECEIVED
$card->isCardAssessment()       // CardState::ASSESSMENT
$card->isCardInProgress()       // CardState::IN_PROGRESS
$card->isCardQualityCheck()     // CardState::QUALITY_CHECK
$card->isCardLabelSlab()        // CardState::LABEL_SLAB
$card->isCardCompleted()        // CardState::COMPLETED
$card->isCardCancelled()        // CardState::CANCELLED
```

#### Query Scopes

```php
// Filter by single state
SubmissionTradingCard::whereCardState(CardState::ASSESSMENT)->get();

// Filter by multiple states
SubmissionTradingCard::whereCardStateIn([
    CardState::ASSESSMENT,
    CardState::IN_PROGRESS,
])->get();
```

### Submission Model

**Location**: `app/Models/Submission.php`

#### State Check Methods

```php
// Check specific state
$submission->isSubmissionState(SubmissionState::COMPLETED)  // true/false
$submission->hasSubmissionStateIn([SubmissionState::COMPLETED, SubmissionState::SHIPPED])  // true/false

// Convenience methods for each state
$submission->isDraft()          // SubmissionState::DRAFT
$submission->isSubmitted()      // SubmissionState::SUBMITTED
$submission->isReceived()       // SubmissionState::RECEIVED
$submission->isAssessment()     // SubmissionState::ASSESSMENT
$submission->isCompleted()      // SubmissionState::COMPLETED
$submission->isShipped()        // SubmissionState::SHIPPED
$submission->isCancelled()      // SubmissionState::CANCELLED

// Terminal state check (completed, shipped, or cancelled)
$submission->isTerminalState()
```

#### Query Scopes

```php
// Filter by single state
Submission::whereSubmissionState(SubmissionState::COMPLETED)->get();

// Filter by multiple states
Submission::whereSubmissionStateIn([
    SubmissionState::COMPLETED,
    SubmissionState::SHIPPED,
    SubmissionState::CANCELLED,
])->get();
```

## Common Usage Patterns

### Single State Check

```php
// ❌ WRONG: Verbose pattern
if ((new ($card->card_state)($card))->equals(CardState::QUALITY_CHECK)) {
    // ...
}

// ✅ CORRECT: Clean helper
if ($card->isCardQualityCheck()) {
    // ...
}
```

### Multiple States Check

```php
// ❌ WRONG: Repeated verbose checks
if ((new ($submission->state)($submission))->equals(SubmissionState::COMPLETED) ||
    (new ($submission->state)($submission))->equals(SubmissionState::SHIPPED) ||
    (new ($submission->state)($submission))->equals(SubmissionState::CANCELLED)) {
    // ...
}

// ✅ CORRECT: Array syntax
if ($submission->hasSubmissionStateIn([
    SubmissionState::COMPLETED,
    SubmissionState::SHIPPED,
    SubmissionState::CANCELLED,
])) {
    // ...
}

// ✅ EVEN BETTER: Terminal state helper
if ($submission->isTerminalState()) {
    // ...
}
```

### Database Queries

```php
// ❌ WRONG: Manual state filtering
$cards = SubmissionTradingCard::all()->filter(function ($card) {
    return (new ($card->card_state)($card))->equals(CardState::ASSESSMENT);
});

// ✅ CORRECT: Query scope
$cards = SubmissionTradingCard::whereCardState(CardState::ASSESSMENT)->get();

// ✅ CORRECT: Multiple states
$cards = SubmissionTradingCard::whereCardStateIn([
    CardState::ASSESSMENT,
    CardState::IN_PROGRESS,
])->get();
```

### Conditional Logic

```php
// ❌ WRONG: Nested ternaries with verbose checks
$status = (new ($card->card_state)($card))->equals(CardState::COMPLETED)
    ? 'done'
    : ((new ($card->card_state)($card))->equals(CardState::QUALITY_CHECK) ? 'reviewing' : 'processing');

// ✅ CORRECT: Match expression with helpers
$status = match (true) {
    $card->isCardCompleted() => 'done',
    $card->isCardQualityCheck() => 'reviewing',
    default => 'processing',
};
```

### View Logic

```php
<!-- ❌ WRONG: Verbose Blade syntax -->
@if((new ($submission->state)($submission))->equals(SubmissionState::COMPLETED))
    <span class="badge-success">Completed</span>
@endif

<!-- ✅ CORRECT: Clean helper -->
@if($submission->isCompleted())
    <span class="badge-success">Completed</span>
@endif
```

## Implementation

### Helper Method Pattern

**Generic Check**:

```php
public function isCardState(string $state): bool
{
    return $this->card_state === $state;
}

public function hasCardStateIn(array $states): bool
{
    return in_array($this->card_state, $states, true);
}
```

**Convenience Methods**:

```php
public function isCardQualityCheck(): bool
{
    return $this->isCardState(CardState::QUALITY_CHECK);
}
```

**Query Scopes**:

```php
public function scopeWhereCardState($query, string $state)
{
    return $query->where('card_state', $state);
}

public function scopeWhereCardStateIn($query, array $states)
{
    return $query->whereIn('card_state', $states);
}
```

## Refactoring Guide

### Step 1: Find Verbose Patterns

```bash
# Search for verbose Spatie comparisons
./vendor/bin/sail grep -r "new (\$.*->.*state)" app/
./vendor/bin/sail grep -r "->equals(.*State::" app/
```

### Step 2: Replace with Helpers

**Before**:

```php
if ((new ($card->card_state)($card))->equals(CardState::QUALITY_CHECK)) {
    // Process quality check
}
```

**After**:

```php
if ($card->isCardQualityCheck()) {
    // Process quality check
}
```

### Step 3: Test

```bash
# Run tests to verify behavior unchanged
./scripts/dev.sh test
```

## Benefits

### Code Reduction

**Before** (100 lines):

```php
if ((new ($card->card_state)($card))->equals(CardState::QUALITY_CHECK)) {
    // Line 1
}

if ((new ($submission->state)($submission))->equals(SubmissionState::COMPLETED)) {
    // Line 2
}

// ... 98 more lines with verbose patterns
```

**After** (37 lines):

```php
if ($card->isCardQualityCheck()) {
    // Line 1
}

if ($submission->isCompleted()) {
    // Line 2
}

// ... 35 more lines with clean helpers
```

**Savings**: 63% code reduction

### Readability

**Verbose**: `(new ($card->card_state)($card))->equals(CardState::QUALITY_CHECK)`

**Clean**: `$card->isCardQualityCheck()`

**Developer Experience**: 10x more readable, self-documenting

### Type Safety

Helper methods provide IDE autocomplete:

```php
$card->is  // ← IDE suggests:
           // isCardReceived()
           // isCardAssessment()
           // isCardInProgress()
           // isCardQualityCheck()
           // ... etc.
```

### Single Source of Truth

Change state comparison logic in ONE place:

```php
// If state comparison logic changes, update helper only
public function isCardQualityCheck(): bool
{
    // Could add additional conditions here
    return $this->isCardState(CardState::QUALITY_CHECK)
        && $this->quality_check_passed === null;
}
```

All usages automatically updated!

## Common Pitfalls

### ❌ WRONG: Still using verbose pattern

```php
if ((new ($card->card_state)($card))->equals(CardState::QUALITY_CHECK)) {
    // This defeats the purpose of helper methods!
}
```

### ❌ WRONG: Manual state string comparison

```php
if ($submission->state === 'completed') {
    // Don't use magic strings!
}
```

### ❌ WRONG: Inconsistent naming

```php
// Don't create your own naming convention
if ($card->isQC()) {  // Abbreviation unclear
    // Use isCardQualityCheck() instead
}
```

## Documentation Links

- **Model Helpers Guide**: `docs/features/state-machine/MODEL-HELPERS.md`
- **State Machine Guide**: `docs/features/state-machine/`
- **Spatie Model States**: https://github.com/spatie/laravel-model-states
- **Service Architecture**: `docs/SERVICE-ARCHITECTURE.md`
