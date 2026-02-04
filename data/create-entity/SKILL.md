---
name: create-entity
description: Automate creation of complete CRUD entities (backend Laravel + frontend Vue) following Budget Manager project conventions. Use when the user asks to create a new entity, model, resource, or CRUD feature. Triggers on requests like "create a new category entity", "add a product model with CRUD", "generate an entity for transactions", or any request to scaffold a complete feature with database, API, and UI components.
---

# Create Entity

Automatically generate a complete CRUD entity following Budget Manager's architectural conventions: Laravel backend (migration, model, controller, routes) + Vue frontend (TypeScript interface, API client, Pinia store, page component, route).

## Quick Start

Generate an entity by running the Python script with entity name and fields:

```bash
python3 scripts/generate_entity.py <entity-name> --fields="field1:type1,field2:type2,..." [--soft-deletes]
```

**Example:**
```bash
python3 scripts/generate_entity.py category --fields="name:string,description:text,isActive:boolean"
```

## Workflow

When a user requests entity creation:

1. **Parse the request** - Identify entity name and required fields
2. **Determine field types** - Map user requirements to supported types (see [field-types.md](references/field-types.md))
3. **Run the generator script** with appropriate options
4. **Review generated files** and inform user of manual steps
5. **Execute manual integration steps** (add routes, update imports)

## Generator Script Usage

### Basic Syntax

```bash
python3 scripts/generate_entity.py <entity-name> --fields="<field-definitions>" [options]
```

### Parameters

- `<entity-name>`: Entity name (singular, any case - will be normalized)
- `--fields`: Comma-separated field definitions in format `fieldName:fieldType`
- `--soft-deletes`: Optional flag to add soft delete support
- `--output`: Optional output directory (default: current directory)

### Field Definition Format

Fields are defined as `name:type` pairs separated by commas:

```
--fields="name:string,amount:integer,isActive:boolean,userId:foreignId"
```

**Naming conventions:**
- Use camelCase for field names (e.g., `userId`, `createdBy`)
- Generator automatically converts to snake_case for backend
- For foreign keys, end with `Id` (e.g., `categoryId` → `category_id`)

### Supported Field Types

Common types (see [field-types.md](references/field-types.md) for complete list):

- `string` - Variable-length text (VARCHAR 255)
- `text` - Long text content
- `integer` - Integer numbers (use for money in cents)
- `boolean` - True/false values
- `date` - Date only
- `datetime` - Date and time
- `foreignId` - Foreign key reference
- `decimal`, `float`, `json`, `bigInteger`, `timestamp`

## Generated Files

### Backend (Laravel)

1. **Migration** - `backend/database/migrations/YYYY_MM_DD_HHMMSS_create_<entities>_table.php`
   - Creates table with specified fields
   - Includes timestamps (created_at, updated_at)
   - Optional soft deletes (deleted_at)
   - Foreign key constraints with cascade delete

2. **Model** - `backend/app/Models/<Entity>.php`
   - Eloquent model with fillable fields
   - Optional SoftDeletes trait
   - Follows Laravel conventions

3. **Controller** - `backend/app/Http/Controllers/<Entity>Controller.php`
   - RESTful API controller with CRUD methods
   - Validation rules based on field types
   - JSON responses

4. **Routes snippet** - `backend/routes/<entity>_routes.txt`
   - Route definition to manually add to `api.php`

### Frontend (Vue + TypeScript)

5. **TypeScript interface** - `frontend/src/types/<entity>_interface.ts`
   - Interface definition in camelCase
   - To manually add to `types/index.ts`

6. **API client** - `frontend/src/api/<entities>.ts`
   - Axios-based API methods (list, get, create, update, delete)
   - Typed responses

7. **Pinia store** - `frontend/src/stores/<entity>.ts`
   - State management with loading/error states
   - CRUD action methods
   - Reactive state

8. **Vue page** - `frontend/src/pages/<Entities>Page.vue`
   - Basic list view component
   - Table with actions
   - Ready to customize

9. **Route snippet** - `frontend/src/router/<entity>_route.txt`
   - Route definition to manually add to router

## Manual Integration Steps

After running the generator, integrate the generated code:

### 1. Add Backend Route

Edit `backend/routes/api.php`:

```php
// Add inside the auth:sanctum middleware group
Route::apiResource('<entities>', <Entity>Controller::class);
```

Copy from the generated `backend/routes/<entity>_routes.txt` file.

### 2. Add TypeScript Interface

Edit `frontend/src/types/index.ts`:

```typescript
export interface <Entity> {
  id: number;
  // ... fields from generated file
  createdAt: string;
  updatedAt: string;
}
```

Copy from the generated `frontend/src/types/<entity>_interface.ts` file.

### 3. Add Frontend Route

Edit `frontend/src/router/index.ts`:

```typescript
{
  path: '/<entities>',
  name: '<entities>',
  component: () => import('@/pages/<Entities>Page.vue'),
  meta: { requiresAuth: true },
}
```

Copy from the generated `frontend/src/router/<entity>_route.txt` file.

### 4. Run Migration

Execute the migration to create the database table:

```bash
make artisan CMD="migrate"
```

### 5. Customize Vue Component

Edit the generated page component to:
- Display actual entity fields in the table
- Add create/edit forms
- Implement proper styling
- Add validation

## Examples

### Simple Entity with Basic Fields

**User request:** "Create a category entity with name, description, and active status"

**Command:**
```bash
python3 scripts/generate_entity.py category --fields="name:string,description:text,isActive:boolean"
```

**Generated:**
- Backend: Migration, Category model, CategoryController, routes
- Frontend: Category interface, categoriesApi, category store, CategoriesPage, route

### Entity with Relationships

**User request:** "Create an expense entity with amount, description, date, and links to category and user"

**Command:**
```bash
python3 scripts/generate_entity.py expense --fields="amountCents:integer,description:text,expenseDate:date,categoryId:foreignId,userId:foreignId"
```

**Foreign keys:** Automatically creates constraints to `categories` and `users` tables with cascade delete.

### Entity with Soft Deletes

**User request:** "Create a product entity that shouldn't be permanently deleted"

**Command:**
```bash
python3 scripts/generate_entity.py product --fields="name:string,priceCents:integer,stock:integer,sku:string" --soft-deletes
```

**Result:** Adds `deleted_at` column and `SoftDeletes` trait to model.

## Important Conventions

### Case Conversion
- **Backend:** Always snake_case (database, models, controllers)
- **Frontend:** Always camelCase (TypeScript, Vue)
- **Automatic:** Middleware handles conversion between API requests/responses

### Money Handling
Always use `integer` type for monetary amounts and store in cents:
```bash
--fields="priceCents:integer,totalAmount:integer"
```

Display conversion: `cents / 100` = euros
Input conversion: `euros * 100` = cents

### Foreign Keys
Name foreign key fields with `Id` suffix (camelCase):
- `userId` → references `users` table
- `categoryId` → references `categories` table
- `budgetTemplateId` → references `budget_templates` table

The generator automatically:
- Extracts the table name from the field name
- Creates `foreignId` column with `constrained()` and `onDelete('cascade')`
- Adds proper validation (`exists:table,id`)

### Timestamps
All entities automatically include:
- `created_at`
- `updated_at`

Don't specify these in `--fields`.

## Troubleshooting

### Permission Issues
If you encounter permission errors when creating files, ensure you're running the script from the project root and have write permissions.

### Field Type Not Recognized
Check [field-types.md](references/field-types.md) for supported types. If using a custom type, you may need to manually edit the generated migration.

### Foreign Key Constraint Fails
Ensure the referenced table exists before running the migration. Create parent entities first.

### Route Conflicts
If routes already exist, Laravel will throw an error. Check `api.php` for duplicate route names.

## Resources

### scripts/generate_entity.py
Main Python script that generates all backend and frontend files based on provided entity name and field definitions.

### references/field-types.md
Complete reference of supported field types with Laravel migration and TypeScript mappings, validation rules, and usage examples.