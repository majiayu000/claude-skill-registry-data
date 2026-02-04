---
name: filament-form-debugger
description: Diagnose and fix common Filament 4.x form errors - namespace issues (Tabs/Grid/Get), type mismatch, trait errors. USE WHEN encountering 'Class not found', 'Argument must be of type', namespace errors, or Filament compilation/runtime errors.
---
---
## When to Use This Skill

- Error: "Class ... not found"
- Error: "Argument must be of type ..."
- Error: "Trait not found"
- Namespace-related Filament errors
- Form not displaying correctly


---
---
## Quick Namespace Map

| Type | Namespace | Examples |
|------|-----------|----------|
| **Layout** | `Schemas\Components\` | Tabs, Grid, Section |
| **Fields** | `Forms\Components\` | TextInput, Select, Toggle |
| **Get** | `Schemas\...Utilities\Get` | fn (Get $get) => |
| **Schema** | `Schemas\Schema` | form(Schema $schema) |
| **Actions** | `Actions\` | EditAction, DeleteAction |
| **Enums** | `Support\Enums\` | GridDirection |


---
## Quick Debug Process

1. **Read error** → Identify type (namespace/type/trait)
2. **Check imports** → Verify `use` statements
3. **Check signature** → `form(Schema $schema): Schema`
4. **Apply fix** → Use correct namespace
5. **Clear cache** → `php artisan optimize:clear`
6. **Test** → Reload page


---
## Complete Import Template

```php
<?php

// Layout (Schemas)
use Filament\Schemas\Components\Tabs;
use Filament\Schemas\Components\Grid;
use Filament\Schemas\Components\Section;

// Fields (Forms)
use Filament\Forms\Components\TextInput;
use Filament\Forms\Components\Select;
use Filament\Forms\Components\Toggle;

// Utilities
use Filament\Schemas\Components\Utilities\Get;
use Filament\Schemas\Schema;

// Actions
use Filament\Actions\EditAction;
use Filament\Actions\DeleteAction;

// Enums
use Filament\Support\Enums\GridDirection;
```


---
## Prevention Checklist

Before saving:
- [ ] Tabs/Grid/Section from `Schemas\Components`
- [ ] TextInput/Select from `Forms\Components`
- [ ] Get from `Utilities\Get`
- [ ] Method signature: `form(Schema $schema)`
- [ ] Only `InteractsWithForms` trait
- [ ] Actions from `Filament\Actions`


---
## Quick Commands

```bash
# Clear caches after fixing
php artisan optimize:clear
php artisan filament:clear-cache

# Rebuild autoload
composer dump-autoload
```


## Complete Error Catalog

For full error list, detailed troubleshooting, and advanced fixes:

`read .claude/skills/filament/filament-form-debugger/CLAUDE.md`

**Related skills:**
- Filament standards: `read .claude/skills/filament/filament-rules/SKILL.md`
- Resource generation: `read .claude/skills/filament/filament-resource-generator/SKILL.md`


---

## References

**Top 5 Common Errors & Fixes:** `read .claude/skills/filament/filament-form-debugger/references/top-5-common-errors--fixes.md`
