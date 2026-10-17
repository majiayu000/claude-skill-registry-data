---
name: rails-generators
description: Use when using Rails generators or scaffolding to create conventional models, controllers, views, migrations, tests, or related application structure.
license: MIT
---

# Rails Generators and Scaffolding

## Purpose

Use Rails generators to accelerate conventional work while treating generated output as code that still requires design review.

## Activate when

- creating a new Rails resource
- generating model/controller/view/test structure
- using `rails generate` or scaffolding
- reviewing generated migrations/routes

## Repository inspection

Before generating:

- resolve Rails version
- inspect existing resource conventions
- inspect test stack
- inspect naming/namespace conventions
- inspect whether project uses scaffolding at all

## Decision rules

Use a generator when the generated structure matches the desired architecture.

Typical generator output may include some combination of:

- model
- migration
- controller
- views
- routes
- tests

The exact output is version/project dependent. Verify rather than assuming.

## Scaffolding

Scaffolding is appropriate when a conventional CRUD resource is actually desired.

Do not use scaffolding simply because it is faster than designing the resource.

## Post-generation review

Treat generation as a draft.

Review:

1. migration
2. schema impact
3. model
4. associations/validations
5. controller
6. routes
7. views/forms
8. tests
9. generated comments/placeholder behavior

Delete artifacts not required by the feature.

## Safety

For destructive generators or generators that replace files, inspect the generated diff before accepting it.

Do not let a generator silently overwrite custom code.

## Reference example

A generator that declares its arguments, respects the force flag, and emits one reviewed template instead of scaffolding sprawl.

```ruby
# lib/generators/value_object/value_object_generator.rb
class ValueObjectGenerator < Rails::Generators::NamedBase
  source_root File.expand_path("templates", __dir__)

  argument :fields, type: :array, default: [], banner: "field field"

  def create_value_object
    template "value_object.rb", File.join("app/values", class_path, "#{file_name}.rb")
  end

  def create_test
    template "value_object_test.rb", File.join("test/values", class_path, "#{file_name}_test.rb")
  end
end

# Usage: bin/rails g value_object Money cents currency
# Generated code lands untracked; review the diff, then commit intentionally.
```

## Agent review checklist

- [ ] Rails version checked
- [ ] project conventions checked
- [ ] generated files reviewed
- [ ] migration reviewed
- [ ] routes reviewed
- [ ] unnecessary artifacts removed
- [ ] tests run

## Verification

Run the relevant generator command, inspect the exact diff, run migration/schema checks, then run affected tests.

## Source foundation

Derived from the Rails scaffolding/generator material in *The Ruby Workshop*, including the use of `rails generate scaffold` to create conventional resource structure. The final-design and review requirements are added for agent safety.

## Book integration: scaffold lifecycle

Treat scaffold output as a first draft. After generation, review the migration, model, controller, routes, views/forms, tests, and authorization boundaries.

Remove generated actions, files, placeholders, or routes that the actual feature does not need. The goal is a coherent resource, not maximum generated surface area.
