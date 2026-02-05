---
name: rails-grpc-implementation
description: Implement gRPC services in Rails for high-performance microservices. Use when building inter-service communication, streaming APIs, or efficient binary protocol endpoints.
---

# Rails gRPC Implementation Specialist

Specialized in creating gRPC services and clients for Rails applications.

## When to Use This Skill

- Implementing microservices with inter-service communication
- Building high-performance API endpoints with binary protocol
- Creating real-time streaming APIs (server, client, bidirectional)
- Implementing polyglot service ecosystems
- Replacing REST APIs for performance-critical operations

## Core Principles

- **Protocol Buffers**: Define service contracts in .proto files
- **Service Interface**: Implement clear RPC methods
- **Error Handling**: Use gRPC status codes appropriately
- **Streaming Support**: Handle unary and streaming patterns
- **Interceptors**: Apply cross-cutting concerns (auth, logging)

## Implementation Guidelines

### Setup

```ruby
# Gemfile
gem 'grpc'
gem 'grpc-tools'
```

### Proto File Definition

```protobuf
// app/protos/user_service.proto
syntax = "proto3";

service UserService {
    rpc GetUser (GetUserRequest) returns (GetUserResponse);
    rpc CreateUser (CreateUserRequest) returns (CreateUserResponse);
    rpc ListUsers (ListUsersRequest) returns (stream UserResponse);
}

message GetUserRequest {
    int64 id = 1;
}

message GetUserResponse {
    int64 id = 1;
    string email = 2;
    string name = 3;
}

message CreateUserRequest {
    string email = 1;
    string name = 2;
}

message CreateUserResponse {
    int64 id = 1;
}
```

### Unary RPC Implementation

```ruby
# app/grpc/services/user_service.rb
module GrpcServices
    class UserService < UserService::Service
        def get_user(request, _call)
            user = User.find(request.id)

            UserService::GetUserResponse.new(
                id: user.id,
                email: user.email,
                name: user.name
            )
        rescue ActiveRecord::RecordNotFound
            raise GRPC::NotFound.new('User not found')
        rescue StandardError => e
            Rails.logger.error("gRPC get_user error: #{e.message}")
            raise GRPC::Internal.new('Internal server error')
        end

        def create_user(request, _call)
            user = User.create!(
                email: request.email,
                name: request.name
            )

            UserService::CreateUserResponse.new(id: user.id)
        rescue ActiveRecord::RecordInvalid => e
            raise GRPC::InvalidArgument.new(e.message)
        end
    end
end
```

### Server Streaming

```ruby
# WHY: Yield results one by one for large datasets
def list_users(request, _call)
    User.find_each do |user|
        yield UserService::UserResponse.new(
            id: user.id,
            email: user.email,
            name: user.name
        )
    end
end
```

### gRPC Client

```ruby
# app/grpc/clients/user_client.rb
module GrpcClients
    class UserClient
        def initialize(host: 'localhost:50051')
            @stub = UserService::Stub.new(host, :this_channel_is_insecure)
        end

        def get_user(user_id)
            request = UserService::GetUserRequest.new(id: user_id)
            @stub.get_user(request, deadline: Time.now + 5)
        rescue GRPC::NotFound
            nil
        rescue GRPC::BadStatus => e
            Rails.logger.error("gRPC error: #{e.message}")
            raise
        end

        def list_users(&block)
            request = UserService::ListUsersRequest.new
            @stub.list_users(request).each(&block)
        end
    end
end
```

### Interceptors

```ruby
# app/grpc/interceptors/authentication_interceptor.rb
module GrpcInterceptors
    class AuthenticationInterceptor < GRPC::ServerInterceptor
        def request_response(request:, call:, method:)
            authenticate!(call)
            yield
        end

        private

        # WHY: Verify JWT token from metadata
        def authenticate!(call)
            token = call.metadata['authorization']&.sub('Bearer ', '')
            raise GRPC::Unauthenticated.new('Missing token') unless token

            decoded = JWT.decode(token, Rails.application.secrets.secret_key_base)[0]
            call.metadata['user_id'] = decoded['user_id']
        rescue JWT::DecodeError
            raise GRPC::Unauthenticated.new('Invalid token')
        end
    end
end
```

```ruby
# app/grpc/interceptors/logging_interceptor.rb
module GrpcInterceptors
    class LoggingInterceptor < GRPC::ServerInterceptor
        def request_response(request:, call:, method:)
            start_time = Time.now
            result = yield
            duration = ((Time.now - start_time) * 1000).round(2)
            Rails.logger.info("gRPC #{method} completed in #{duration}ms")
            result
        rescue StandardError => e
            Rails.logger.error("gRPC #{method} failed: #{e.class}")
            raise
        end
    end
end
```

### Server Setup

```ruby
# config/initializers/grpc.rb
Thread.new do
    server = GRPC::RpcServer.new(
        interceptors: [
            GrpcInterceptors::LoggingInterceptor.new,
            GrpcInterceptors::AuthenticationInterceptor.new
        ]
    )
    server.add_http2_port('0.0.0.0:50051', :this_port_is_insecure)
    server.handle(GrpcServices::UserService)
    server.run_till_terminated_or_interrupted([1, 'int', 'SIGTERM'])
end
```

## gRPC Status Codes

```ruby
# Common status codes
GRPC::NotFound.new('Resource not found')
GRPC::InvalidArgument.new('Invalid parameters')
GRPC::Unauthenticated.new('Authentication required')
GRPC::PermissionDenied.new('Access denied')
GRPC::Internal.new('Internal server error')
```

## Tools to Use

- `Read`: Read proto files and gRPC services
- `Write`: Create proto files and services
- `Edit`: Modify gRPC services
- `Bash`: Generate code and run tests
- `mcp__serena__find_symbol`: Find models and services

### Bash Commands

```bash
# Generate Ruby code from proto
grpc_tools_ruby_protoc -I app/protos --ruby_out=lib/grpc --grpc_out=lib/grpc app/protos/*.proto

# Run gRPC service tests
bundle exec rspec spec/grpc/services/user_service_spec.rb
```

## Workflow

1. **Define Contract**: Create .proto files
2. **Generate Code**: Run protoc compiler
3. **Write Tests**: Use `rspec-grpc-testing` skill
4. **Verify Failure**: Confirm tests fail
5. **Implement Service**: Create gRPC service class
6. **Handle Errors**: Use appropriate status codes
7. **Add Interceptors**: Implement auth/logging
8. **Run Tests**: Ensure all pass
9. **Run Rubocop**: Validate style

## Related Skills

- `rspec-grpc-testing`: For gRPC tests
- `rails-service-objects`: For business logic
- `rails-error-handling`: For error patterns
- `rails-security`: For authentication

## Coding Standards

See [Rails Coding Standards](../_shared/rails-coding-standards.md)

## TDD Workflow

Follow [TDD Workflow](../_shared/rails-tdd-workflow.md)

## Key Reminders

- Define clear contracts in .proto files
- Use appropriate gRPC status codes
- Implement interceptors for cross-cutting concerns
- Handle streaming patterns correctly
- Set timeouts and deadlines
- Write tests before implementation (TDD)
- Use English comments explaining WHY
- Log errors appropriately
