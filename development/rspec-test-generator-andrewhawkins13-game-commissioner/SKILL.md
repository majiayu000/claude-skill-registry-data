---
name: "RSpec Test Generator"
description: "Generates complete, runnable RSpec tests for Rails models, services, controllers, and background jobs following project conventions. Use when new code is created without corresponding tests, when refactoring existing code, or when explicitly asked to add test coverage."
---

# RSpec Test Generator Skill

This skill generates comprehensive, project-specific RSpec tests that follow the Game Commissioner Rails application's testing conventions.

## When to Use This Skill

**Automatically invoke when:**
- A new model, service, controller, or job is created without a corresponding spec file
- Existing code is modified and tests need updating
- User explicitly requests test generation or improved test coverage
- Code review reveals missing test coverage

**Key Triggers:**
- "Write tests for..."
- "Add test coverage for..."
- "Generate specs for..."
- Creating new `.rb` files in `app/models/`, `app/services/`, `app/controllers/`, or `app/jobs/`

## Project Testing Conventions

### Core Principles
1. **No Factory Bot**: Despite gem being installed, this project does NOT use Factory Bot
   - Models: Use real ActiveRecord objects with `.create!`
   - Services: Use RSpec doubles extensively
2. **Comprehensive Coverage**: Test validations, associations, enums, happy paths, error paths, and edge cases
3. **WebMock for HTTP**: All external API calls (Ollama) use WebMock stubs
4. **Geocoder Stubbing**: Address-based models require Geocoder test stubs

### Test Structure
```ruby
RSpec.describe ClassName, type: :model do
  describe "#method_name" do
    context "when specific condition" do
      it "does something specific" do
        # test implementation
      end
    end
  end
end
```

## Test Generation Workflow

### Step 1: Analyze the Code

**Determine code type:**
- **Model**: `app/models/*.rb`
- **Service (Class Methods)**: Stateless service with class methods (`.method_name`)
- **Service (Instance Methods)**: Stateful service with `initialize` and instance methods
- **Controller**: `app/controllers/*_controller.rb`
- **Job**: `app/jobs/*_job.rb`

**Extract key information:**
- Class name and module namespace
- Public methods to test
- Dependencies (other classes, services, APIs)
- ActiveRecord associations and validations (for models)
- Whether it uses geocoding (Game, Official models)

### Step 2: Select Appropriate Template

**Model Tests** (`templates/model_spec.rb.erb`):
- Validations (presence, uniqueness, format, custom)
- Associations (belongs_to, has_many, has_many :through)
- Enums (if using RoleEnumerable or similar)
- Scopes
- Instance methods
- Class methods
- Geocoder setup/teardown if model has `address` field

**Service Tests - Class Methods** (`templates/service_class_method_spec.rb.erb`):
- Used for stateless services
- Examples: `EligibilityFilterService`, `CandidateFinder`, `AssignmentBuilder`
- Test class methods directly with doubles for dependencies

**Service Tests - Instance Methods** (`templates/service_instance_method_spec.rb.erb`):
- Used for stateful services with configuration
- Examples: `OrchestratorService`, `Ollama::ClientService`, `ResponseParserService`
- Test `#initialize` and instance methods
- Use `described_class.new` pattern

**Controller Tests** (`templates/controller_spec.rb.erb`):
- RESTful actions (index, show, new, create, edit, update, destroy)
- Response status codes
- Variable assignments
- Redirects and renders

**Job Tests** (`templates/job_spec.rb.erb`):
- `#perform` method
- Service delegation
- Error handling

### Step 3: Generate Complete Test

**DO NOT generate stubs.** Generate complete, runnable tests with:
- Proper `let` blocks for test data
- Appropriate mocking/stubbing
- Multiple contexts (happy path, error cases, edge cases)
- Clear, descriptive test names
- Actual expectations and assertions

### Step 4: Apply Project-Specific Patterns

#### For Models:
```ruby
# Use real ActiveRecord objects
let(:model) { Model.create!(name: "Test", attribute: value) }

# Geocoder setup if model has addresses
before do
  Geocoder.configure(lookup: :test)
  Geocoder::Lookup::Test.add_stub("123 Test St", [{ "latitude" => 40.7, "longitude" => -74 }])
end

after do
  Geocoder::Lookup::Test.reset
end

# Test validations
it "is valid with valid attributes" do
  expect(model).to be_valid
end

it "is invalid without required_field" do
  model.required_field = nil
  expect(model).not_to be_valid
  expect(model.errors[:required_field]).to include("can't be blank")
end

# Test associations
it "belongs to parent" do
  expect(Model.reflect_on_association(:parent).macro).to eq(:belongs_to)
end

# Test enums
it "defines status enum" do
  expect(Model.defined_enums["status"]).to eq({ "pending" => 0, "active" => 1 })
end
```

#### For Services with Class Methods:
```ruby
# Use doubles for dependencies
let(:dependency) { double("DependencyClass", id: 1, method: "value") }
let(:relation) { double("ActiveRecord::Relation") }

# Stub dependency behavior
before do
  allow(DependencyClass).to receive(:method).and_return(relation)
  allow(relation).to receive(:where).and_return([dependency])
end

# Test class methods
describe ".class_method" do
  context "when input is valid" do
    it "returns expected result" do
      result = described_class.class_method(dependency)
      expect(result).to eq(expected_value)
    end
  end

  context "when input is invalid" do
    it "handles gracefully" do
      result = described_class.class_method(nil)
      expect(result).to be_empty
    end
  end
end
```

#### For Services with Instance Methods:
```ruby
# Initialize service with config
let(:config_param) { "default_value" }
let(:service) { described_class.new(config_param: config_param) }

# Test initialization
describe "#initialize" do
  it "initializes with default config" do
    expect { described_class.new }.not_to raise_error
  end

  it "initializes with custom config" do
    custom = described_class.new(config_param: "custom")
    expect(custom.instance_variable_get(:@config_param)).to eq("custom")
  end
end

# Test instance methods
describe "#instance_method" do
  let(:input) { "test input" }

  context "when successful" do
    before do
      # Stub dependencies or HTTP requests
    end

    it "returns expected result" do
      result = service.instance_method(input)
      expect(result[:key]).to eq(expected)
    end
  end

  context "when error occurs" do
    before do
      allow(dependency).to receive(:method).and_raise(StandardError)
    end

    it "raises appropriate error" do
      expect { service.instance_method(input) }.to raise_error(StandardError)
    end
  end
end
```

#### For Ollama/External API Services:
```ruby
# Use WebMock for HTTP requests
before do
  stub_request(:post, "http://localhost:11434/api/generate")
    .with(body: hash_including(model: "llama3.2"))
    .to_return(
      status: 200,
      body: { response: "test response" }.to_json,
      headers: { "Content-Type" => "application/json" }
    )
end

# Test both success and failure
context "when API call succeeds" do
  it "parses response correctly" do
    result = service.call
    expect(result[:response]).to eq("test response")
  end
end

context "when API call fails" do
  before do
    stub_request(:post, url).to_return(status: 500)
  end

  it "raises an error" do
    expect { service.call }.to raise_error(/API error/)
  end
end
```

#### For Controllers:
```ruby
describe "GET #index" do
  it "returns a successful response" do
    get :index
    expect(response).to be_successful
  end

  it "assigns @resources" do
    resources = Resource.all
    get :index
    expect(assigns(:resources)).to eq(resources)
  end
end

describe "POST #create" do
  context "with valid parameters" do
    let(:valid_attributes) { { name: "Test" } }

    it "creates a new resource" do
      expect {
        post :create, params: { resource: valid_attributes }
      }.to change(Resource, :count).by(1)
    end

    it "redirects to the created resource" do
      post :create, params: { resource: valid_attributes }
      expect(response).to redirect_to(Resource.last)
    end
  end

  context "with invalid parameters" do
    it "does not create a resource" do
      expect {
        post :create, params: { resource: { name: nil } }
      }.not_to change(Resource, :count)
    end
  end
end
```

#### For Background Jobs:
```ruby
describe "#perform" do
  let(:param) { double("Model", id: 1) }
  let(:service) { instance_double(ServiceClass) }

  before do
    allow(ServiceClass).to receive(:new).and_return(service)
    allow(service).to receive(:perform_action)
  end

  it "calls the service with correct parameters" do
    expect(service).to receive(:perform_action).with(param)
    described_class.perform_now(param)
  end

  context "when service raises an error" do
    before do
      allow(service).to receive(:perform_action).and_raise(StandardError)
    end

    it "handles the error" do
      expect { described_class.perform_now(param) }.to raise_error(StandardError)
    end
  end
end
```

## Test File Location and Naming

- **Models**: `spec/models/model_name_spec.rb`
- **Services**: `spec/services/module_name/service_name_spec.rb` (mirror app/ structure)
- **Controllers**: `spec/controllers/controller_name_spec.rb`
- **Jobs**: `spec/jobs/job_name_spec.rb`

**Examples:**
- `app/models/game.rb` → `spec/models/game_spec.rb`
- `app/services/ai_assignment/orchestrator.rb` → `spec/services/ai_assignment/orchestrator_spec.rb`
- `app/controllers/games_controller.rb` → `spec/controllers/games_controller_spec.rb`
- `app/jobs/assign_open_games_job.rb` → `spec/jobs/assign_open_games_job_spec.rb`

## Common Patterns Reference

### Doubles and Mocking
```ruby
# Doubles with type hints
let(:game) { double("Game", id: 1, name: "Test Game", status: "open") }
let(:official) { double("Official", id: 10, name: "John Doe") }

# ActiveRecord relation doubles
let(:relation) { double("ActiveRecord::Relation") }
allow(Game).to receive(:upcoming).and_return(relation)
allow(relation).to receive(:includes).and_return([game])

# Method stubbing
allow(object).to receive(:method).and_return(value)
allow(object).to receive(:method).with(args).and_return(value)
allow(object).to receive(:method).and_raise(StandardError)
```

### Expectations
```ruby
# Value expectations
expect(result).to eq(expected)
expect(result).to be_truthy / be_falsy
expect(result).to be_nil
expect(result[:key]).to include(value)
expect(result).to match(/regex/)

# Behavior expectations
expect(service).to receive(:method).with(args)
expect { action }.to change(Model, :count).by(1)
expect { action }.to raise_error(ErrorClass)
expect { action }.not_to raise_error

# Model validation expectations
expect(model).to be_valid
expect(model).not_to be_valid
expect(model.errors[:field]).to include("error message")
```

### WebMock Patterns
```ruby
# Basic stub
stub_request(:post, "http://example.com/api")
  .to_return(status: 200, body: json, headers: {})

# With request matching
stub_request(:post, url)
  .with(
    body: hash_including(key: "value"),
    headers: { "Content-Type" => "application/json" }
  )
  .to_return(status: 200, body: response.to_json)

# Error responses
stub_request(:post, url).to_return(status: 500)
stub_request(:post, url).to_raise(StandardError)
```

## Output Format

When generating tests, provide:

1. **Complete test file path**: `spec/[type]/[name]_spec.rb`
2. **Full test code**: Not stubs, but complete, runnable tests
3. **Brief explanation**: What the test covers and any special considerations
4. **Next steps**: Suggest running `bundle exec rspec spec/path/to/file_spec.rb`

## Example Generation

**User creates:**
```ruby
# app/models/league.rb
class League < ApplicationRecord
  has_many :games
  validates :name, presence: true, uniqueness: true
  validates :season, presence: true

  enum status: { active: 0, inactive: 1 }

  scope :active, -> { where(status: :active) }
end
```

**You generate:**
```ruby
# spec/models/league_spec.rb
require "rails_helper"

RSpec.describe League, type: :model do
  describe "validations" do
    let(:league) { League.new(name: "Test League", season: "2024", status: :active) }

    it "is valid with valid attributes" do
      expect(league).to be_valid
    end

    context "name" do
      it "is invalid without a name" do
        league.name = nil
        expect(league).not_to be_valid
        expect(league.errors[:name]).to include("can't be blank")
      end

      it "is invalid with duplicate name" do
        League.create!(name: "Test League", season: "2024")
        duplicate = League.new(name: "Test League", season: "2025")
        expect(duplicate).not_to be_valid
        expect(duplicate.errors[:name]).to include("has already been taken")
      end
    end

    context "season" do
      it "is invalid without a season" do
        league.season = nil
        expect(league).not_to be_valid
        expect(league.errors[:season]).to include("can't be blank")
      end
    end
  end

  describe "associations" do
    it "has many games" do
      expect(League.reflect_on_association(:games).macro).to eq(:has_many)
    end
  end

  describe "enums" do
    it "defines status enum" do
      expect(League.defined_enums["status"]).to eq({
        "active" => 0,
        "inactive" => 1
      })
    end
  end

  describe "scopes" do
    describe ".active" do
      it "returns only active leagues" do
        active = League.create!(name: "Active League", season: "2024", status: :active)
        inactive = League.create!(name: "Inactive League", season: "2024", status: :inactive)

        expect(League.active).to include(active)
        expect(League.active).not_to include(inactive)
      end
    end
  end
end
```

**Explanation:**
Created comprehensive model spec testing all validations (presence, uniqueness), associations, enums, and scopes. Uses real ActiveRecord objects per project conventions.

**Next steps:**
Run: `bundle exec rspec spec/models/league_spec.rb`

## Tips for Success

1. **Read the actual code**: Don't guess at method signatures or behavior
2. **Use project doubles pattern**: Type-hinted doubles like `double("Game", attributes)`
3. **Test all paths**: Happy path, error conditions, edge cases, nil handling
4. **Match existing style**: Review similar spec files for consistency
5. **Include setup/teardown**: Especially for Geocoder and WebMock
6. **Use descriptive contexts**: "when user is authenticated", "with invalid parameters"
7. **Write clear expectations**: Use specific matchers and error messages

## References

For more detailed patterns, see:
- `references/testing_patterns.md` - Comprehensive pattern guide
- `../claude_project_rules.md` - Project-wide conventions
- Existing specs in `spec/` - Real examples from this project
