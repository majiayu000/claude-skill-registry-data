---
name: mojolicious
description: Assist with Mojolicious web framework development using documentation search, browsing, and testing requests without starting a server.
---

# Mojolicious Development

Use the Mojolicious app script for efficient development and testing.

## Core Capabilities

- **Search documentation** - Search Mojolicious docs using Google Custom Search
- **Browse documentation** - View official docs at https://docs.mojolicious.org/
- **Test requests** - Test app endpoints using the built-in commands
- **View routes** - List all application routes

## Documentation Access

### Searching Documentation

Use WebSearch with site restriction to search Mojolicious documentation:

```
WebSearch: "routing guide site:docs.mojolicious.org"
WebSearch: "websocket site:docs.mojolicious.org"
```

Or use WebFetch with Google Custom Search:

```
https://www.google.com/cse?cx=014527573091551588235:pwfplkjpgbi&q=<query>
```

### Browsing Documentation

Documentation URLs follow these patterns:

- **Mojolicious modules**: `https://docs.mojolicious.org/Mojolicious/Guides/Routing`
  - Use `/` separators for Mojolicious namespace
  - Example: `Mojolicious::Guides::Routing` → `/Mojolicious/Guides/Routing`

- **CPAN modules**: `https://docs.mojolicious.org/Path::To::Module`
  - Use `::` separators for other modules
  - Example: `Mojo::UserAgent` → `/Mojo::UserAgent`

## Testing Your Application

### Quick Testing

Quick testing is useful for rapid manual verification during development.

#### Testing Requests

Use the app script for GET requests only. For other HTTP methods (POST, PUT, DELETE), use curl with a running server:

```bash
# GET request (use app.pl)
./app.pl get /api/users

# GET request with query parameters (use app.pl)
./app.pl get /api/users?page=1

# GET request with custom headers (use app.pl)
./app.pl get /api/users -H 'Authorization: Bearer token123'

# For POST, PUT, DELETE: Start server first
./app.pl daemon -l http://127.0.0.1:3000

# POST request with JSON data (use curl)
curl -X POST http://127.0.0.1:3000/api/users \
  -H 'Content-Type: application/json' \
  -d '{"name":"Alice","email":"alice@example.com"}'

# PUT request (use curl)
curl -X PUT http://127.0.0.1:3000/api/users/1 \
  -H 'Content-Type: application/json' \
  -d '{"name":"Alice Updated"}'

# DELETE request (use curl)
curl -X DELETE http://127.0.0.1:3000/api/users/1

# curl with custom headers
curl http://127.0.0.1:3000/api/users \
  -H 'Authorization: Bearer token123'
```

#### Viewing Routes

List all application routes:

```bash
./app.pl routes
```

This shows the routing table with HTTP methods, paths, and route names.

### Unit Testing with Test::Mojo

For proper automated testing, use Test::Mojo. It provides a comprehensive testing framework with chainable assertions.

#### Creating Test Files

Create test files in the `t/` directory:

```perl
# t/api.t
use Test2::V0;
use Test::Mojo;

# Create test instance
my $t = Test::Mojo->new('path/to/app.pl');

# Test GET request
$t->get_ok('/api/todos')
  ->status_is(200)
  ->json_is([]);

# Test POST request
$t->post_ok('/api/todos' => json => {title => 'Buy milk', completed => 0})
  ->status_is(201)
  ->json_has('/id')
  ->json_is('/title' => 'Buy milk')
  ->json_is('/completed' => 0);

# Test GET specific todo
$t->get_ok('/api/todos/1')
  ->status_is(200)
  ->json_is('/title' => 'Buy milk');

# Test PUT request
$t->put_ok('/api/todos/1' => json => {completed => 1})
  ->status_is(200)
  ->json_is('/completed' => 1);

# Test DELETE request
$t->delete_ok('/api/todos/1')
  ->status_is(200)
  ->json_has('/message');

# Test error cases
$t->get_ok('/api/todos/999')
  ->status_is(404)
  ->json_has('/error');

$t->post_ok('/api/todos' => json => {})
  ->status_is(400)
  ->json_is('/error' => 'Title is required');

done_testing();
```

#### Running Tests

```bash
# Run all tests
prove -lv t/

# Run specific test file
prove -lv t/api.t

# Run with verbose output
perl t/api.t
```

#### Key Test::Mojo Features

- **Chainable assertions**: Chain multiple assertions for concise tests
- **HTTP methods**: `get_ok`, `post_ok`, `put_ok`, `delete_ok`, etc.
- **Status assertions**: `status_is()`, `status_isnt()`
- **JSON assertions**: `json_is()`, `json_has()`, `json_like()`
- **Content assertions**: `content_like()`, `content_type_is()`
- **Header assertions**: `header_is()`, `header_like()`
- **Automatic session management**: Cookies are handled automatically
- **No server needed**: Tests run without starting a real server

## Quick Examples

```bash
# View all routes in your application
./app.pl routes

# Test a GET endpoint (use app.pl)
./app.pl get /api/users

# Test with authentication header (use app.pl)
./app.pl get /api/protected -H 'Authorization: Bearer mytoken'

# Start server for testing POST/PUT/DELETE
./app.pl daemon -l http://127.0.0.1:3000

# Test a POST endpoint with JSON (use curl)
curl -X POST http://127.0.0.1:3000/api/users \
  -H 'Content-Type: application/json' \
  -d '{"name":"Bob","role":"admin"}'
```

## Workflow

1. **Plan**: Check routes with `./app.pl routes`
2. **Search**: Find relevant documentation for the feature
3. **Read docs**: Browse official docs at https://docs.mojolicious.org/
4. **Implement**: Write your code
5. **Test**:
   - **Recommended**: Write unit tests with Test::Mojo in `t/` directory
   - **Quick testing**: Use `./app.pl get` for GET requests, or curl with daemon for other methods
6. **Run tests**: Execute with `prove -lv t/` to verify all functionality

## Guidelines

- Always check `./app.pl routes` to understand the current routing structure
- **Prefer unit testing over quick testing:**
  - Write automated tests with Test::Mojo in `t/` directory for reliable, repeatable testing
  - Use quick testing (app.pl/curl) only for rapid manual verification during development
- For quick testing endpoints:
  - GET requests: Use `./app.pl get <path>` (no server needed)
  - POST/PUT/DELETE: Start server with `./app.pl daemon` and use curl
- Search documentation using site-restricted WebSearch: `site:docs.mojolicious.org <query>`
- For module documentation, use WebFetch with proper URL patterns:
  - Mojolicious namespace: `https://docs.mojolicious.org/Mojolicious/Path`
  - Other modules: `https://docs.mojolicious.org/Module::Name`
- Follow the workflow: plan → search → read docs → implement → unit test → (optional: quick test)
- Test::Mojo provides better test coverage and automation than manual curl commands
