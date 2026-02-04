---
name: Nova Resource Builder
description: Create and modify Laravel Nova 5.x resources with PCR Card patterns (tab panels, Badge fields with closures, Select fields with constants). Triggers include "nova resource", "nova badge", "nova tabs", "nova field".
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - Bash
---

# Nova Resource Builder

Build Nova 5.x resources following PCR Card's established patterns.

## When to Use

- Creating new Nova resources
- Adding fields to existing resources
- Implementing tab-based layouts
- Configuring Badge/Select fields with constants
- Setting up Nova search

## Quick Commands

```bash
# Create resource
php artisan nova:resource ResourceName

# Validate Nova search configs
./scripts/dev.sh validate:nova-search

# Clear Nova cache
./scripts/dev.sh nova:publish
```

## PCR Card Nova Patterns

### 1. Badge Fields (Closure Pattern)

**CRITICAL**: Badge fields use closures + hardcoded string maps, NOT constants.

```php
use Laravel\Nova\Fields\Badge;

Badge::make('Status', function () {
    // Closure returns calculated value
    return $this->is_active ? 'active' : 'inactive';
})
->map([
    'active' => 'success',      // Hardcoded strings
    'inactive' => 'danger',
    'pending' => 'warning',
])
->label(function ($value) {
    return match ($value) {
        'active' => 'Active',
        'inactive' => 'Inactive',
        'pending' => 'Pending',
    };
});
```

### 2. Select Fields (Constants Pattern)

Use constant class `options()` method:

```php
use App\Constants\PromoCodeType;
use Laravel\Nova\Fields\Select;

Select::make('Type')
    ->options(PromoCodeType::options())  // Returns ['fixed' => 'Fixed Amount', ...]
    ->displayUsingLabels()
    ->sortable()
    ->rules('required');
```

### 3. Tab-Based Layouts

Use `Tab::group()` with `Heading::make()` for sections:

```php
use Laravel\Nova\Tabs\Tab;
use Laravel\Nova\Fields\Heading;

public function fields(NovaRequest $request): array
{
    return [
        ID::make()->sortable(),

        Tab::group('Resource Information', [
            Tab::make('Overview', [
                Heading::make('Basic Details'),
                Text::make('Name')->required(),

                Heading::make('Settings'),
                Boolean::make('Is Active'),
            ]),

            Tab::make('Details', [
                Heading::make('Additional Information'),
                Textarea::make('Description'),
            ]),
        ]),
    ];
}
```

**Rules**:
- Use `Tab::group('Title', [...])` for panel with heading
- Use `Heading::make('Name')` for section dividers
- NO `Panel::make()` inside tabs
- HasMany relationships work in tabs

### 4. Search Configuration

```php
public static $search = [
    'id',
    'name',
    'user.email',           // Relationship search
    'submission.submission_number',
];

// REQUIRED: Eager load relationships
public static $with = ['user', 'submission'];
```

**Validate before commit**:
```bash
./scripts/dev.sh validate:nova-search
```

## Constants Reference

All constants follow this pattern:

```php
class ConstantName
{
    public const PREFIX_VALUE = 'value';

    public static function all(): array;        // All values
    public static function label(string $value): string;  // Human label
    public static function options(): array;    // For Select fields
    public static function isValid(string $value): bool;  // Validation
}
```

**Available Constants** (18 total):
- `App\Constants\PromoCodeType` - TYPE_FIXED, TYPE_PERCENTAGE
- `App\Constants\ManualPaymentMethod` - METHOD_CASH, METHOD_CHECK, etc.
- `App\Constants\ManualPaymentStatus` - STATUS_PENDING, STATUS_VERIFIED, etc.
- `App\Constants\SubmissionState` - DRAFT, SUBMITTED, RECEIVED, etc. (stores `::class` refs)
- `App\Constants\CardState` - RECEIVED, ASSESSMENT, IN_PROGRESS, etc.
- See `app/Constants/` for all 18 classes

## Common Pitfalls

**❌ WRONG**: Using NovaBadgeType constants in Badge fields
```php
Badge::make('Status')
    ->map(fn($value) => NovaBadgeType::SUCCESS);  // ❌ Don't do this
```

**✅ CORRECT**: Use hardcoded strings
```php
Badge::make('Status', function () {
    return $this->state;
})
->map([
    'active' => 'success',    // ✅ Hardcoded strings
    'inactive' => 'danger',
]);
```

**❌ WRONG**: Manual options array for Select
```php
Select::make('Type')
    ->options([
        'fixed' => 'Fixed Amount',
        'percentage' => 'Percentage',
    ]);
```

**✅ CORRECT**: Use constant `options()` method
```php
Select::make('Type')
    ->options(PromoCodeType::options());  // ✅ Centralized
```

## Documentation Links

- Nova Admin Guide: `docs/development/NOVA-ADMIN-GUIDE.md`
- Nova Search Guide: `docs/development/NOVA-SEARCH-GUIDE.md`
- Constants Pattern: CLAUDE.md "Constants Pattern & Nova Best Practices"
- Laravel Nova Docs: https://nova.laravel.com/docs/5.0
