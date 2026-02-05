---
name: phoenix-generator
description: Generate Phoenix resources (contexts, schemas, LiveViews, controllers) using mix phx.gen.* commands with best practices. Use when creating new Phoenix resources, contexts, or LiveView components.
allowed-tools: Bash, Read, Edit, Write
---

# Phoenix Generator

This skill helps generate Phoenix resources using built-in generators with proper patterns and best practices.

## When to Use

- Creating new Phoenix contexts
- Adding schemas to existing contexts
- Generating LiveView CRUD interfaces
- Creating JSON/HTML resources
- Scaffolding authentication

## Available Generators

### Context and Schema Generation

**mix phx.gen.context** - Generate a context with schema and migration
```bash
mix phx.gen.context Accounts User users name:string email:string:unique age:integer
```

Generates:
- Context module: `lib/my_app/accounts.ex`
- Schema: `lib/my_app/accounts/user.ex`
- Migration: `priv/repo/migrations/*_create_users.exs`
- Test files

**mix phx.gen.schema** - Schema and migration only (no context)
```bash
mix phx.gen.schema Accounts.User users name:string email:string:unique
```

### LiveView Generators

**mix phx.gen.live** - Full LiveView CRUD with context
```bash
mix phx.gen.live Catalog Product products \
  name:string \
  description:text \
  price:decimal \
  sku:string:unique \
  in_stock:boolean
```

Generates:
- Context and schema
- LiveView modules (Index, Show, Form Component)
- Routes
- Tests

**mix phx.gen.live.component** - Standalone LiveView component
```bash
mix phx.gen.live.component Components.Modal
```

### Traditional Web Generators

**mix phx.gen.html** - HTML resource with controllers
```bash
mix phx.gen.html Blog Post posts title:string body:text published:boolean
```

**mix phx.gen.json** - JSON API resource
```bash
mix phx.gen.json Shop Product products name:string price:decimal
```

## Field Types and Modifiers

### Common Field Types
- `string` - varchar(255)
- `text` - unlimited text
- `integer` - whole numbers
- `decimal` - precise decimals (for money)
- `float` - floating point
- `boolean` - true/false
- `date` - date only
- `time` - time only
- `datetime` - timestamp
- `uuid` - UUID
- `binary` - binary data

### Field Modifiers
- `:unique` - adds unique index
- `:redact` - marks for redaction in logs
- `name:string:unique:redact` - chain modifiers

### References (Associations)
```bash
# belongs_to
mix phx.gen.context Blog Post posts \
  title:string \
  body:text \
  user_id:references:users

# Specify custom reference
mix phx.gen.context Comments Comment comments \
  body:text \
  post_id:references:posts \
  author_id:references:users
```

## Best Practices

### 1. Context Naming
- Use plural for context: `Accounts`, `Catalog`, `Blog`
- Use singular for schema: `User`, `Product`, `Post`
- Table name matches schema plural: `users`, `products`, `posts`

### 2. Field Selection
```bash
# Good: Specific types
price:decimal         # For money
published_at:datetime # For timestamps
active:boolean        # For flags

# Avoid: Wrong types
price:float          # Loses precision for money
published:string     # Use datetime or boolean
```

### 3. Associations
```bash
# Always specify references explicitly
user_id:references:users

# Don't use bare integer for foreign keys
user_id:integer  # Missing association metadata
```

### 4. Decimal Precision
For money fields, update migration:
```elixir
# Generated
add :price, :decimal

# Best Practice - specify precision
add :price, :decimal, precision: 10, scale: 2
```

### 5. String Length Limits
Update schema for validation:
```elixir
# Add to changeset
|> validate_length(:name, max: 100)
|> validate_length(:email, max: 160)
```

## Generator Workflow

### Step 1: Plan Schema
```bash
# List fields with types
name:string
email:string:unique
age:integer
bio:text
admin:boolean
inserted_at:datetime
updated_at:datetime  # automatic with timestamps()
```

### Step 2: Generate Resource
```bash
# Choose appropriate generator
mix phx.gen.live Accounts User users \
  name:string \
  email:string:unique \
  age:integer \
  bio:text \
  admin:boolean
```

### Step 3: Review Generated Files
- Check migration for proper indexes and constraints
- Review schema for additional validations needed
- Update context functions as needed
- Review tests and add edge cases

### Step 4: Customize Migration
```bash
# Before running migration, edit it
vim priv/repo/migrations/*_create_users.exs
```

Add:
- Check constraints
- Default values
- Additional indexes
- Precision for decimals

### Step 5: Add Routes (if needed)
```elixir
# lib/my_app_web/router.ex
scope "/", MyAppWeb do
  pipe_through :browser

  live "/users", UserLive.Index, :index
  live "/users/new", UserLive.Index, :new
  live "/users/:id/edit", UserLive.Index, :edit
  live "/users/:id", UserLive.Show, :show
  live "/users/:id/show/edit", UserLive.Show, :edit
end
```

### Step 6: Run Migration
```bash
mix ecto.migrate
```

### Step 7: Update Tests
- Add validation tests
- Add association tests
- Test edge cases

## Common Patterns

### Money Fields
```bash
mix phx.gen.live Shop Product products \
  name:string \
  price:decimal \
  sale_price:decimal
```

Then update migration:
```elixir
add :price, :decimal, precision: 10, scale: 2, null: false
add :sale_price, :decimal, precision: 10, scale: 2
```

### Soft Deletes
Add to schema:
```bash
deleted_at:datetime
```

Update migration:
```elixir
add :deleted_at, :utc_datetime
create index(:products, [:deleted_at])
```

### Polymorphic Associations
```bash
mix phx.gen.schema Comments.Comment comments \
  body:text \
  commentable_type:string \
  commentable_id:integer
```

### Multi-tenant (Tenant ID)
```bash
mix phx.gen.live Accounts User users \
  organization_id:references:organizations \
  name:string \
  email:string
```

Add unique constraint on tenant + field:
```elixir
create unique_index(:users, [:organization_id, :email])
```

## Undoing Generators

If you need to rollback:
```bash
# Rollback migration
mix ecto.rollback

# Delete generated files manually or use:
mix phx.gen.context --undo Accounts User users
```

## Troubleshooting

**Module already exists:**
- Generator won't overwrite existing files
- Use `--merge-with-existing-context` to add to existing context
- Or manually integrate generated code

**Routes not working:**
- Check router.ex was updated
- Verify pipe_through matches (:browser or :api)
- Restart server after adding routes

**Migration fails:**
- Check for duplicate table names
- Verify referenced tables exist
- Ensure field types are valid

## Generator Flags

```bash
# Skip migration
mix phx.gen.context Accounts User users name:string --no-migration

# Binary ID (UUID)
mix phx.gen.schema Accounts User users name:string --binary-id

# Merge with existing context
mix phx.gen.context Accounts Profile profiles bio:text --merge-with-existing-context

# Specify table name
mix phx.gen.schema Accounts User my_users name:string --table my_users
```
