---
name: pangea-refactoring
description: Refactors Pangea Ruby code following SOLID principles, dry-rb patterns, and file size guidelines. Use when splitting large files, extracting modules, reducing duplication, or improving type definitions.
---

# Pangea Refactoring

Refactors Ruby code following best practices for dry-rb, SOLID principles, and Pangea's 200-line file limit.

## When to Use This Skill

- Splitting files exceeding 200 lines
- Extracting classes or modules from large components
- Reducing type duplication across resources
- Improving dry-struct composition
- Applying SOLID principles
- Creating shared validators

## File Size Guidelines

**Hard limit: 200 lines per file** (per CLAUDE.md)

When a file exceeds this limit, apply one of these refactoring patterns:

### 1. Extract Module Pattern

For components with multiple concerns:

```ruby
# BEFORE: lib/pangea/components/siem_security_platform/component.rb (2,876 lines)

# AFTER: Split into focused modules
# lib/pangea/components/siem_security_platform/
#   component.rb          # Main entry point, orchestrates modules (<100 lines)
#   log_ingestion.rb      # Log collection and Firehose streams
#   threat_detection.rb   # Detection rules and Lambda functions
#   alerting.rb           # SNS topics, SQS queues, notifications
#   opensearch.rb         # OpenSearch domain configuration
#   compliance.rb         # Compliance reporting and auditing
#   types.rb              # Attribute definitions
```

### 2. Extract Class Pattern

When a module has multiple responsibilities:

```ruby
# BEFORE: Single class doing parsing AND sending
class ReportGenerator
  def parse_logs; end
  def generate_report; end
  def send_email; end
  def format_output; end
end

# AFTER: Separate classes with single responsibility
class LogParser
  def parse(logs); end
end

class ReportFormatter
  def format(data); end
end

class ReportNotifier
  def send(report, recipients); end
end

class ReportGenerator
  def initialize(parser: LogParser.new, formatter: ReportFormatter.new, notifier: ReportNotifier.new)
    @parser = parser
    @formatter = formatter
    @notifier = notifier
  end

  def generate_and_send(logs, recipients)
    data = @parser.parse(logs)
    report = @formatter.format(data)
    @notifier.send(report, recipients)
  end
end
```

## SOLID Principles for Pangea

### Single Responsibility Principle (SRP)

Each file should have one reason to change:

| File Type | Single Responsibility |
|-----------|----------------------|
| `resource.rb` | Terraform synthesis for one resource |
| `types.rb` | Attribute validation for that resource |
| `component.rb` | Orchestration of related resources |
| Module file | One functional concern (e.g., networking, security) |

### Open/Closed Principle (OCP)

Extend through composition, not modification:

```ruby
# Use attributes_from for extension
class BaseSecurityConfig < Dry::Struct
  attribute :encryption_enabled, Types::Bool.default(true)
  attribute :audit_logging, Types::Bool.default(true)
end

class EnhancedSecurityConfig < Dry::Struct
  attributes_from BaseSecurityConfig
  attribute :threat_detection, Types::Bool.default(false)
  attribute :compliance_mode, Types::String.optional
end
```

### Dependency Inversion

Depend on abstractions (modules), not concrete implementations:

```ruby
# Good: Component depends on resource module interface
module Pangea::Components::WebApp
  include Pangea::Resources::AWS  # Interface

  def create_web_app(name, attrs)
    aws_vpc(...)      # Uses interface methods
    aws_subnet(...)
  end
end
```

## dry-struct Composition Patterns

### Use `attributes_from` for Shared Attributes

```ruby
# lib/pangea/types/shared/taggable.rb
module Pangea::Types::Shared
  class Taggable < Dry::Struct
    attribute :tags?, Types::Hash.default({}.freeze)
  end
end

# lib/pangea/types/shared/nameable.rb
module Pangea::Types::Shared
  class Nameable < Dry::Struct
    attribute :name, Types::String.constrained(min_size: 1, max_size: 255)
  end
end

# lib/pangea/resources/aws_s3_bucket/types.rb
class BucketAttributes < Dry::Struct
  attributes_from Pangea::Types::Shared::Nameable
  attributes_from Pangea::Types::Shared::Taggable

  attribute :acl?, Types::String.default('private')
  attribute :versioning?, Types::Bool.default(false)
end
```

### Nested Struct Definitions

```ruby
class OpenSearchConfig < Dry::Struct
  transform_keys(&:to_sym)

  # Inline nested struct (auto-creates OpenSearchConfig::ClusterConfig)
  attribute :cluster do
    attribute :instance_type, Types::String.default('r6g.large.search')
    attribute :instance_count, Types::Integer.default(3)
    attribute :zone_awareness, Types::Bool.default(true)
  end

  attribute :ebs do
    attribute :enabled, Types::Bool.default(true)
    attribute :volume_size, Types::Integer.default(100)
    attribute :volume_type, Types::String.default('gp3')
  end
end
```

### Shared Type Constraints

Define reusable type constraints in `lib/pangea/types/`:

```ruby
# lib/pangea/types/aws.rb
module Pangea::Types::AWS
  include Dry.Types()

  # ARN format
  Arn = String.constrained(format: /\Aarn:aws:[a-z0-9-]+:[a-z0-9-]*:\d{12}:.+\z/)

  # Resource ID patterns
  VpcId = String.constrained(format: /\Avpc-[a-f0-9]{8,17}\z/)
  SubnetId = String.constrained(format: /\Asubnet-[a-f0-9]{8,17}\z/)
  SecurityGroupId = String.constrained(format: /\Asg-[a-f0-9]{8,17}\z/)

  # Common constraints
  InstanceType = String.constrained(format: /\A[a-z][a-z0-9]*\.[a-z0-9]+\z/)
  Region = String.constrained(format: /\A[a-z]{2}-[a-z]+-\d\z/)

  # Reusable in any resource types.rb
  CidrBlock = String.constrained(
    format: /\A\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\/\d{1,2}\z/
  )
end

# Usage in resource types
class VpcAttributes < Dry::Struct
  attribute :cidr_block, Pangea::Types::AWS::CidrBlock
  attribute :vpc_id?, Pangea::Types::AWS::VpcId.optional
end
```

## Component Refactoring Template

When splitting a large component (>200 lines):

### Step 1: Identify Concerns

Analyze the component for distinct functional areas:

```
siem_security_platform (2,876 lines) →
  ├── Log Ingestion (Firehose, CloudWatch)
  ├── Threat Detection (Lambda, Step Functions)
  ├── Data Storage (OpenSearch, S3)
  ├── Alerting (SNS, SQS, EventBridge)
  ├── Security (IAM, KMS, Security Groups)
  └── Compliance (Config rules, auditing)
```

### Step 2: Create Module Structure

```ruby
# lib/pangea/components/siem_security_platform/component.rb
module Pangea::Components::SiemSecurityPlatform
  extend self

  def siem_security_platform(name, attributes = {})
    attrs = Types::Attributes.new(attributes)

    resources = {}
    resources.merge!(create_security_resources(name, attrs))
    resources.merge!(create_storage_resources(name, attrs))
    resources.merge!(create_ingestion_resources(name, attrs))
    resources.merge!(create_detection_resources(name, attrs))
    resources.merge!(create_alerting_resources(name, attrs))

    ComponentReference.new(type: :siem_security_platform, name: name, resources: resources)
  end

  private

  def create_security_resources(name, attrs)
    Security.create(name, attrs)
  end

  # ... other delegations
end
```

### Step 3: Extract Each Concern

```ruby
# lib/pangea/components/siem_security_platform/security.rb
module Pangea::Components::SiemSecurityPlatform
  module Security
    extend self
    include Pangea::Resources::AWS

    def create(name, attrs)
      {
        kms_keys: create_kms_keys(name, attrs),
        iam_roles: create_iam_roles(name, attrs),
        security_groups: create_security_groups(name, attrs)
      }
    end

    private

    def create_kms_keys(name, attrs)
      # KMS key creation logic
    end

    # ... focused methods
  end
end
```

## Type File Refactoring

When `types.rb` exceeds 200 lines:

### Strategy: Split by Attribute Groups

```ruby
# BEFORE: aws_media_live_channel/types.rb (1,001 lines)

# AFTER: Split into logical groups
# aws_media_live_channel/
#   types.rb                    # Main Attributes class, imports sub-types
#   types/
#     input_settings.rb         # Input configuration types
#     output_groups.rb          # Output group types
#     encoding_settings.rb      # Video/audio encoding types
#     network_settings.rb       # Network configuration types
```

```ruby
# lib/pangea/resources/aws_media_live_channel/types.rb
require_relative 'types/input_settings'
require_relative 'types/output_groups'
require_relative 'types/encoding_settings'

module Pangea::Resources::AWS
  module MediaLiveChannel
    class Attributes < Dry::Struct
      transform_keys(&:to_sym)

      attribute :name, Types::String
      attribute :input_settings, Types::InputSettings
      attribute :output_groups, Types::Array.of(Types::OutputGroup)
      attribute :encoding_settings?, Types::EncodingSettings.optional
    end
  end
end
```

## CLI Command Refactoring

When CLI commands exceed 200 lines:

```ruby
# BEFORE: cli/commands/agent.rb (608 lines)

# AFTER: Extract operation classes
# cli/commands/agent/
#   command.rb              # Main command definition
#   list_operation.rb       # List resources operation
#   inspect_operation.rb    # Inspect templates operation
#   analyze_operation.rb    # Analysis operations
```

```ruby
# lib/pangea/cli/commands/agent/command.rb
module Pangea::CLI::Commands
  class Agent < BaseCommand
    def run
      case subcommand
      when 'list' then ListOperation.new(options).execute
      when 'inspect' then InspectOperation.new(options).execute
      when 'analyze' then AnalyzeOperation.new(options).execute
      end
    end
  end
end
```

## RBS Type Annotations

For critical modules, add RBS signatures:

```rbs
# sig/pangea/types/aws.rbs
module Pangea
  module Types
    module AWS
      Arn: Dry::Types::Type[String]
      VpcId: Dry::Types::Type[String]
      SubnetId: Dry::Types::Type[String]
      CidrBlock: Dry::Types::Type[String]
    end
  end
end
```

Run type checking with:
```bash
bundle exec steep check
```

## Refactoring Checklist

Before refactoring:
- [ ] Read the entire file to understand all dependencies
- [ ] Identify the distinct responsibilities (look for "and" in descriptions)
- [ ] Check which methods/attributes are used together
- [ ] Verify tests exist (create if needed before refactoring)

During refactoring:
- [ ] Extract one concern at a time
- [ ] Keep tests passing after each extraction
- [ ] Use `require_relative` for local modules
- [ ] Maintain the public API

After refactoring:
- [ ] Each file under 200 lines
- [ ] Each module has single responsibility
- [ ] All tests still pass
- [ ] No functionality changes (refactoring only)

## Common Duplication to Eliminate

### 1. Tag Handling

```ruby
# Create shared concern
module Pangea::Components::Concerns::Taggable
  def component_tags(component_type, name, custom_tags = {})
    {
      'Component' => component_type,
      'Name' => name,
      'ManagedBy' => 'Pangea'
    }.merge(custom_tags)
  end
end
```

### 2. Resource Naming

```ruby
# Create shared naming convention
module Pangea::Components::Concerns::Nameable
  def component_resource_name(component_name, resource_type)
    :"#{component_name}_#{resource_type}"
  end
end
```

### 3. VPC/Subnet Pattern

```ruby
# Create reusable networking module
module Pangea::Components::Networking
  def create_vpc_with_subnets(name, attrs)
    # Reusable VPC + subnet creation
  end
end
```

## Running Refactoring Verification

```bash
# Check file sizes
find lib -name "*.rb" -exec wc -l {} \; | sort -rn | head -20

# Run tests after refactoring
bundle exec rspec

# Check for unused methods (optional)
bundle exec rubocop --only Lint/UnusedMethodArgument

# Type check (if RBS configured)
bundle exec steep check
```

## Priority Files for Refactoring

Based on current codebase analysis:

| File | Lines | Priority |
|------|-------|----------|
| `components/siem_security_platform/component.rb` | 2,876 | Critical |
| `components/sustainable_ml_training/component.rb` | 1,753 | Critical |
| `components/spot_instance_carbon_optimizer/component.rb` | 1,637 | Critical |
| `resources/aws_media_live_channel/types.rb` | 1,001 | Critical |
| `cli/commands/agent.rb` | 608 | High |
| `cli/commands/plan.rb` | 512 | High |
| `architectures/patterns/data_processing.rb` | 668 | High |

## References

- [dry-struct Composition](https://dry-rb.org/gems/dry-struct/)
- [SOLID Principles in Ruby](https://www.honeybadger.io/blog/ruby-solid-design-principles/)
- [Extract Class Pattern](https://thoughtbot.com/ruby-science/extract-class.html)
- [RBS Best Practices](https://github.com/ruby/rbs/wiki/Writing-Signatures-Best-Practices)
- [RuboCop Metrics](https://docs.rubocop.org/rubocop/cops_metrics.html)
