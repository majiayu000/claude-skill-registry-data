---
name: filament-rules
description: Filament 4.x coding standards for Laravel 12. Custom Schema namespace (NOT Form), Vietnamese UI, Observer patterns, Image management. USE WHEN creating resources, fixing namespace errors, implementing forms, RelationManagers, Settings pages, or any Filament development.
---

# Filament 4.x Standards

Quick reference for Filament 4.x in this Laravel 12 project.

## When to Use

- Creating/editing Filament resources
- Namespace errors ("Class not found")
- Forms, tables, RelationManagers
- Settings pages
- Image management

---

## Critical Namespaces

**⚠️ This project uses `Schema` NOT `Form`!**

```php
// Layout → Schemas
use Filament\Schemas\Components\Tabs;
use Filament\Schemas\Components\Grid;
use Filament\Schemas\Components\Section;

// Fields → Forms
use Filament\Forms\Components\TextInput;
use Filament\Forms\Components\Select;
use Filament\Forms\Components\Toggle;

// Utilities
use Filament\Schemas\Components\Utilities\Get;
use Filament\Schemas\Schema;

// Actions
use Filament\Actions\EditAction;
use Filament\Actions\DeleteAction;

```

---

## Resource Structure

```php
// Form: Schema with Tabs
public static function form(Schema $schema): Schema
{
    return $schema->schema([
        Tabs::make()->tabs([
            Tabs\Tab::make('Thông tin')->schema([
                TextInput::make('name')->label('Tên')->required(),
            ]),
        ])->columnSpanFull(),
    ]);
}

// Table: modifyQueryUsing for eager loading
public static function table(Table $table): Table
{
    return $table
        ->modifyQueryUsing(fn($q) => $q->with(['category']))
        ->columns([
            TextColumn::make('name')->label('Tên')->searchable(),
        ])
        ->recordActions([
            EditAction::make()->iconButton(),
        ]);
}

```

---

## Quick Patterns

**Observer for SEO:**
```php
class ProductObserver {
    public function creating(Product $p): void {
        if (empty($p->slug)) $p->slug = Str::slug($p->name);
    }
}
// Register: Product::observe(ProductObserver::class);

```

**Vietnamese labels:**
```php
TextInput::make('name')->label('Tên')->required();
->dateTime('d/m/Y H:i')

```

**Images:**
```php
public function images(): MorphMany {
    return $this->morphMany(Image::class, 'model');
}
// Resource: ImagesRelationManager::class

```

**Settings page:**
```php
class SettingsPage extends Page implements HasForms {
    use InteractsWithForms;
    public function form(Schema $schema): Schema { /* ... */ }
}

```

**⚠️ allowHtml() - Use inline styles NOT Tailwind:**
```php
->options([1 => '<div style="display: flex;">...</div>'])->allowHtml();

```

---

## References

**Advanced patterns:** `read .claude/skills/filament/filament-rules/references/advanced-patterns.md`
**Complete guide:** `read .claude/skills/filament/filament-rules/CLAUDE.md`

**Related skills:**
- `read .claude/skills/filament/filament-resource-generator/SKILL.md`
- `read .claude/skills/filament/filament-form-debugger/SKILL.md`
- `read .claude/skills/filament/image-management/SKILL.md`
