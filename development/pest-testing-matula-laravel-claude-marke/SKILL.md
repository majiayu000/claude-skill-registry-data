---
name: pest-testing
description: Comprehensive guidance for writing Pest v4 tests in Laravel applications, including feature tests, unit tests, and browser tests. Use this skill when writing tests, implementing test-driven development, testing APIs, creating browser automation tests, or ensuring code quality through testing.
---

# Pest Testing Skill

This skill provides expert guidance for writing high-quality tests with Pest v4 in Laravel applications, covering feature tests, unit tests, browser tests, and testing best practices.

## Purpose

Provide comprehensive Pest v4 testing guidance covering:
- Core Pest syntax and expectations API
- Feature and unit testing in Laravel
- Browser testing with Pest v4 (new feature)
- HTTP testing, authentication, and authorization
- Database testing and factories
- Mocking and faking Laravel services
- Testing best practices and patterns
- Datasets for efficient test organization

## When to Use

Use this skill when:
- Writing or updating tests
- Implementing test-driven development (TDD)
- Testing APIs and HTTP endpoints
- Testing authentication and authorization
- Creating browser automation tests
- Testing with model factories
- Using datasets to avoid duplicate tests
- Mocking services or external dependencies
- Verifying features work correctly
- Ensuring code quality and preventing regressions

## Core Principles

### 1. Most Tests Should Be Feature Tests

Focus on feature tests that verify complete workflows:

```php
// ✅ GOOD - Feature test testing full workflow
it('creates a post', function () {
    $user = User::factory()->create();
    
    $response = $this->actingAs($user)->post('/posts', [
        'title' => 'My Post',
        'body' => 'Content',
    ]);
    
    $response->assertCreated();
    
    $this->assertDatabaseHas('posts', [
        'title' => 'My Post',
        'user_id' => $user->id,
    ]);
});

// Unit tests are for isolated logic
it('calculates total correctly', function () {
    $calculator = new Calculator();
    
    expect($calculator->add(2, 2))->toBe(4);
});
```

### 2. Always Use Model Factories

Never manually create models - use factories:

```php
// ✅ CORRECT - Use factories
$user = User::factory()->create();
$posts = Post::factory()->count(3)->create();

// Check for factory states
$admin = User::factory()->admin()->create();
$publishedPost = Post::factory()->published()->create();

// ❌ WRONG - Manual creation
$user = User::create([
    'name' => 'Test',
    'email' => 'test@example.com',
    // ... many fields
]);
```

### 3. Use Datasets to Avoid Duplication

When testing similar scenarios with different data, use datasets:

```php
// ✅ GOOD - Using dataset
it('validates email format', function (string $email, bool $valid) {
    $validator = validator(['email' => $email], ['email' => 'email']);
    
    expect($validator->passes())->toBe($valid);
})->with([
    ['valid@example.com', true],
    ['invalid', false],
    ['test@test.co', true],
    ['@example.com', false],
]);

// ❌ WRONG - Duplicate tests
it('accepts valid email', function () {
    $validator = validator(['email' => 'valid@example.com'], ['email' => 'email']);
    expect($validator->passes())->toBeTrue();
});

it('rejects invalid email', function () {
    $validator = validator(['email' => 'invalid'], ['email' => 'email']);
    expect($validator->passes())->toBeFalse();
});
```

### 4. Use Specific Assertions

Prefer specific assertions over generic ones:

```php
// ✅ GOOD - Specific assertions
$response->assertOk();           // 200
$response->assertCreated();      // 201
$response->assertNoContent();    // 204
$response->assertNotFound();     // 404
$response->assertForbidden();    // 403
$response->assertUnprocessable();// 422

// ❌ AVOID - Generic assertions
$response->assertStatus(200);
$response->assertStatus(404);
```

### 5. Import Mock Function When Needed

Always import the mock function before using it:

```php
use function Pest\Laravel\mock;

it('mocks a service', function () {
    $mock = mock(PaymentService::class);
    
    $mock->shouldReceive('charge')
        ->once()
        ->andReturn(true);
    
    // Test code
});
```

Read `references/core.md` for complete Pest syntax and expectations API.

## Running Tests

### Run All Tests

```bash
php artisan test
```

### Run Specific File

```bash
php artisan test tests/Feature/PostTest.php
```

### Run with Filter

```bash
php artisan test --filter=login
php artisan test --filter="can create posts"
```

### Run Specific Group

```bash
php artisan test --group=integration
```

**Best Practice**: Run the minimal number of tests using an appropriate filter when developing, then run the full suite before committing.

## Feature Testing Patterns

### Basic HTTP Testing

```php
it('displays homepage', function () {
    $response = $this->get('/');
    
    $response->assertOk()
        ->assertSee('Welcome');
});

it('creates resource', function () {
    $user = User::factory()->create();
    
    $response = $this->actingAs($user)->post('/posts', [
        'title' => 'My Post',
        'body' => 'Content',
    ]);
    
    $response->assertCreated()
        ->assertJson(['title' => 'My Post']);
});
```

### Authentication Testing

```php
it('requires authentication', function () {
    $response = $this->get('/dashboard');
    
    $response->assertRedirect('/login');
});

it('allows authenticated users', function () {
    $user = User::factory()->create();
    
    $response = $this->actingAs($user)->get('/dashboard');
    
    $response->assertOk();
});
```

### Validation Testing

```php
it('validates required fields', function () {
    $user = User::factory()->create();
    
    $response = $this->actingAs($user)->post('/posts', []);
    
    $response->assertUnprocessable()
        ->assertJsonValidationErrors(['title', 'body']);
});
```

Read `references/laravel.md` for comprehensive Laravel testing patterns.

## Pest v4 Browser Testing

Pest v4 introduces powerful browser testing capabilities:

```php
use function Pest\Laravel\visit;

it('can login', function () {
    $user = User::factory()->create([
        'password' => bcrypt('password'),
    ]);
    
    $page = visit('/login');
    
    $page->fill('email', $user->email)
        ->fill('password', 'password')
        ->click('Login')
        ->assertPath('/dashboard')
        ->assertSee("Welcome, {$user->name}");
});
```

### Browser Testing Features

- **Real browser testing** - Chrome, Firefox, Safari
- **JavaScript support** - Full JS execution
- **Multiple devices** - Test on different viewports/devices
- **Dark mode testing** - Test light and dark color schemes
- **Screenshots** - Capture on failure or manually
- **Touch gestures** - Test mobile interactions
- **Wait utilities** - Wait for dynamic content

### Browser Test Best Practices

```php
it('has no JavaScript errors', function () {
    $pages = visit(['/', '/about', '/contact']);
    
    $pages->assertNoJavascriptErrors()
        ->assertNoConsoleLogs();
});

it('works in dark mode', function () {
    $page = visit('/', colorScheme: 'dark');
    
    $page->assertSee('Welcome')
        ->assertNoJavascriptErrors();
});

it('works on mobile', function () {
    $page = visit('/', device: 'iPhone 14 Pro');
    
    $page->assertSee('Welcome')
        ->assertVisible('.mobile-menu');
});
```

Read `references/browser.md` for comprehensive browser testing guide.

## Using Model Factories

### Basic Factory Usage

```php
// Single model
$user = User::factory()->create();

// Multiple models
$users = User::factory()->count(5)->create();

// With specific attributes
$user = User::factory()->create([
    'name' => 'John Doe',
    'email' => 'john@example.com',
]);

// With relationships
$user = User::factory()
    ->has(Post::factory()->count(3))
    ->create();
```

### Using Factory States

Check if factories have custom states before manually setting attributes:

```php
// Check factory for states like:
$admin = User::factory()->admin()->create();
$publishedPost = Post::factory()->published()->create();
$verifiedUser = User::factory()->verified()->create();
```

## Testing with RefreshDatabase

Clean database state between tests:

```php
use Illuminate\Foundation\Testing\RefreshDatabase;

uses(RefreshDatabase::class);

it('creates user', function () {
    $user = User::factory()->create();
    
    expect(User::count())->toBe(1);
});
```

## Mocking and Faking

### Faking Laravel Services

```php
use Illuminate\Support\Facades\Mail;
use Illuminate\Support\Facades\Queue;
use Illuminate\Support\Facades\Event;
use Illuminate\Support\Facades\Notification;
use Illuminate\Support\Facades\Storage;

it('sends email', function () {
    Mail::fake();
    
    // Trigger email
    
    Mail::assertSent(WelcomeEmail::class);
});

it('dispatches job', function () {
    Queue::fake();
    
    // Trigger job
    
    Queue::assertPushed(ProcessPodcast::class);
});

it('dispatches event', function () {
    Event::fake();
    
    // Trigger event
    
    Event::assertDispatched(UserCreated::class);
});
```

### Mocking Classes

```php
use function Pest\Laravel\mock;

it('mocks external service', function () {
    $mock = mock(PaymentGateway::class);
    
    $mock->shouldReceive('charge')
        ->once()
        ->with(100)
        ->andReturn(['status' => 'success']);
    
    // Test code that uses PaymentGateway
});
```

## Test Organization

### Grouping Related Tests

```php
describe('User Management', function () {
    it('creates users', function () {
        //
    });
    
    it('updates users', function () {
        //
    });
    
    it('deletes users', function () {
        //
    });
});
```

### Using Tags/Groups

```php
it('is an integration test', function () {
    //
})->group('integration');

it('is slow', function () {
    //
})->group('slow', 'integration');

// Run: php artisan test --group=integration
```

## Reference Files

This skill includes detailed reference files:

- **`references/core.md`** - Pest syntax, expectations API, assertions, datasets, mocking, lifecycle hooks
- **`references/browser.md`** - Browser testing, interactions, waiting, device testing, screenshots, smoke testing
- **`references/laravel.md`** - HTTP testing, authentication, validation, database testing, faking services

Read the appropriate reference file(s) when working on specific testing tasks.

## Testing Workflow

### Test-Driven Development (TDD)

1. **Write failing test** - Define expected behavior
2. **Write minimal code** - Make test pass
3. **Refactor** - Improve code while keeping tests green
4. **Repeat** - For next feature or behavior

### Testing Existing Features

1. **Write test for happy path** - Normal, successful flow
2. **Write test for failure paths** - Error cases, validation failures
3. **Write test for edge cases** - Empty data, null values, boundaries
4. **Run tests** - Verify all pass
5. **Refactor if needed** - Improve while keeping tests green

## Best Practices Summary

1. ✅ **Write feature tests** - Most tests should test complete workflows
2. ✅ **Use factories** - Always use model factories for test data
3. ✅ **Use datasets** - Avoid duplicate tests with different data
4. ✅ **Use specific assertions** - `assertOk()` not `assertStatus(200)`
5. ✅ **Import mock function** - `use function Pest\Laravel\mock;`
6. ✅ **Use RefreshDatabase** - Clean database between tests
7. ✅ **Check factory states** - Use existing states before manual setup
8. ✅ **Test all paths** - Happy, failure, and edge cases
9. ✅ **Run minimal tests** - Use filters when developing
10. ✅ **Run full suite** - Before committing changes
11. ✅ **Use browser tests** - For JavaScript-heavy features
12. ✅ **Check for JS errors** - Use `assertNoJavascriptErrors()`
13. ✅ **Test both themes** - Verify light and dark modes
14. ✅ **Keep tests isolated** - Each test should be independent
15. ✅ **Use descriptive names** - Tests should read like specifications

## Common Testing Tasks

### Testing a New Feature

1. Create test file: `php artisan make:test FeatureTest --pest`
2. Write test for expected behavior
3. Run test: `php artisan test --filter=FeatureName`
4. Implement feature
5. Verify test passes
6. Add tests for edge cases
7. Run full suite: `php artisan test`

### Testing API Endpoints

1. Test successful requests (2xx status)
2. Test validation errors (422 status)
3. Test authentication (401/403 status)
4. Test not found (404 status)
5. Verify JSON structure and data
6. Test with different user permissions

### Testing Browser Interactions

1. Create browser test in `tests/Browser/`
2. Visit the page
3. Interact with elements (click, type, select)
4. Assert expected results
5. Check for JavaScript errors
6. Test on different devices/viewports
7. Test both color schemes

This skill ensures tests are comprehensive, maintainable, and follow Pest v4 best practices for Laravel applications.
