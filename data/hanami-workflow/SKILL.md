---
name: hanami-workflow
description: Hanami framework workflow guidelines. Activate when working with Hanami projects, Hanami CLI, or Hanami-specific patterns.
location: user
---

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in RFC 2119.

# Hanami Workflow

## Tool Grid

| Task | Tool | Command |
|------|------|---------|
| Lint | StandardRB | `bundle exec standardrb` |
| Test | RSpec | `bundle exec rspec` |
| Console | Hanami CLI | `bundle exec hanami console` |
| Server | Hanami CLI | `bundle exec hanami server` |
| Generate | Hanami CLI | `bundle exec hanami generate <type>` |
| DB Migrate | Hanami CLI | `bundle exec hanami db migrate` |
| Routes | Hanami CLI | `bundle exec hanami routes` |

## Slices Architecture

Hanami applications MUST be organized into isolated slices (`slices/admin/`, `slices/api/`, `slices/main/`).

- Each slice MUST have its own container and dependencies
- Slices SHOULD NOT directly depend on other slices
- Cross-slice communication SHOULD use explicit interfaces or events
- Shared code MUST live in `lib/` or `app/` (application layer)

```ruby
# slices/admin/config/slice.rb
module Admin
  class Slice < Hanami::Slice
    import keys: ["persistence.rom"], from: :main
  end
end
```

## Dependency Injection via Deps

Hanami uses dry-system for dependency injection. All dependencies MUST be injected, not hardcoded.

```ruby
module Main::Actions::Books
  class Show < Main::Action
    include Deps["repositories.book_repository"]

    def handle(request, response)
      book = book_repository.find(request.params[:id])
      response.body = book.to_json
    end
  end
end
```

- MUST use `include Deps[...]` for injecting dependencies
- SHOULD prefer constructor injection for testability
- MUST NOT use global state or singletons directly

## Entities, Relations, and Repositories (ROM)

Hanami uses ROM (Ruby Object Mapper) for persistence.

### Entities
Entities MUST be simple domain objects without persistence logic.
```ruby
module MyApp::Entities
  class Book < Hanami::Entity
    attribute :id, Types::Integer
    attribute :title, Types::String
  end
end
```

### Relations
Relations MUST define the database schema mapping.
```ruby
module MyApp::Relations
  class Books < Hanami::DB::Relation
    schema :books, infer: true do
      associations { belongs_to :author; has_many :reviews }
    end
  end
end
```

### Repositories
Repositories MUST encapsulate all persistence operations.
```ruby
module MyApp::Repositories
  class BookRepository < Hanami::DB::Repo
    def find(id) = books.by_pk(id).one
    def published = books.where { published_at <= Date.today }.to_a
    def create(attrs) = books.changeset(:create, attrs).commit
  end
end
```

- Repositories MUST NOT expose ROM internals to actions
- Relations SHOULD use `infer: true` when schema matches database
- Changesets SHOULD be used for create/update operations

## Validation with dry-validation

Input validation MUST use dry-validation contracts.

```ruby
module Main::Contracts::Books
  class Create < Hanami::Action::Contract
    params do
      required(:title).filled(:string, min_size?: 1)
      required(:author).filled(:string)
      optional(:published_at).maybe(:date)
    end

    rule(:title) do
      key.failure("must be unique") if BookRepository.new.exists?(title: value)
    end
  end
end
```

- Contracts MUST validate all external input
- Params SHOULD define type coercion
- Error messages MUST be user-friendly

## Actions

Actions MUST be single-purpose request handlers.

```ruby
module Main::Actions::Books
  class Create < Main::Action
    include Deps["repositories.book_repository"]
    contract Contracts::Books::Create

    def handle(request, response)
      result = request.params
      if result.valid?
        book = book_repository.create(result.to_h)
        response.status = 201
        response.body = book.to_json
      else
        response.status = 422
        response.body = { errors: result.errors.to_h }.to_json
      end
    end
  end
end
```

- Each action MUST handle exactly one request type
- Actions MUST use contracts for input validation
- Actions SHOULD delegate business logic to interactors/services

## Views and Templates

Views MUST separate presentation logic from templates.

```ruby
module Main::Views::Books
  class Show < Main::View
    expose :book do |book:|
      BookPresenter.new(book)
    end
  end
end
```

```erb
<%# slices/main/templates/books/show.html.erb %>
<article>
  <h1><%= book.title %></h1>
  <p>By <%= book.author %></p>
</article>
```

- Views MUST use `expose` for passing data to templates
- Templates SHOULD contain minimal logic
- Presenters SHOULD format data for display

## Configuration

```ruby
# config/app.rb
module MyApp
  class App < Hanami::App
    config.actions.content_security_policy[:script_src] = "'self'"
    config.logger.level = :info
  end
end

# slices/api/config/slice.rb
module Api
  class Slice < Hanami::Slice
    config.actions.format :json
    config.actions.default_response_format = :json
  end
end
```

- Sensitive config MUST use environment variables
- Per-slice config SHOULD override app defaults only when needed

## Testing Patterns

```ruby
# Action test - mock dependencies
RSpec.describe Main::Actions::Books::Show do
  subject(:action) { described_class.new(book_repository: repository) }
  let(:repository) { instance_double(BookRepository) }

  it "returns book" do
    allow(repository).to receive(:find).with(1).and_return(Book.new(id: 1))
    expect(action.call(id: 1).status).to eq(200)
  end
end

# Repository test - real database
RSpec.describe BookRepository, type: :database do
  it "finds published" do
    subject.create(title: "Old", published_at: Date.today - 30)
    expect(subject.published.map(&:title)).to eq(["Old"])
  end
end
```

- Actions MUST be tested with mocked dependencies
- Repositories SHOULD be tested against real database

## Interactor/Service Pattern

```ruby
module MyApp::Interactors::Books
  class Publish
    include Deps["repositories.book_repository", "events.publisher"]

    def call(book_id)
      book = book_repository.find(book_id) or return Failure(:not_found)
      updated = book_repository.update(book_id, published_at: Date.today)
      publisher.publish("book.published", book_id: book_id)
      Success(updated)
    end
  end
end
```

- Services SHOULD return Result objects (Success/Failure)
- Actions SHOULD use `halt` for error responses