---
name: laravel-api
description: "Build production-ready RESTful APIs with Laravel. Covers authentication (Sanctum/Passport), versioning, resources, rate limiting, and API testing."
category: php-frameworks
tags: ['laravel', 'api', 'rest', 'sanctum', 'passport']
complexity: advanced
risk: low
compatibility: [claude-code, antigravity, gemini-cli, cursor, copilot, codex-cli, autohand, kiro]
source: antigravity-official
version: "1.0.0"
date_added: "2026-07-10"
last_updated: "2026-07-10"
---

# Laravel API Builder

## Purpose
Build secure, versioned, well-documented RESTful APIs using Laravel with proper authentication, rate limiting, and response standards.

## Operating Mode
You are a **Laravel API specialist**. Focus on API architecture, authentication, and consistent response formatting.

## The Process

### 1️⃣ API Architecture Setup
```bash
# Install Laravel Sanctum for SPA/mobile token auth
composer require laravel/sanctum
php artisan vendor:publish --provider="Laravel\Sanctum\SanctumServiceProvider"
php artisan migrate

# For OAuth2 (third-party clients), use Passport
composer require laravel/passport
php artisan passport:install
```

### 2️⃣ API Versioning Structure
```
routes/
├── api.php           # v1 routes
├── api_v2.php        # v2 routes (or use prefix groups)

# In RouteServiceProvider:
Route::prefix('api/v1')->middleware('api')->group(base_path('routes/api.php'));
Route::prefix('api/v2')->middleware('api')->group(base_path('routes/api_v2.php'));
```

### 3️⃣ API Resource Transformation
```php
// App/Http/Resources/PostResource.php
class PostResource extends JsonResource
{
    public function toArray(Request $request): array
    {
        return [
            'id'         => $this->id,
            'type'       => 'posts',
            'title'      => $this->title,
            'excerpt'    => Str::limit($this->body, 150),
            'author'     => new UserResource($this->whenLoaded('author')),
            'tags'       => TagResource::collection($this->whenLoaded('tags')),
            'meta' => [
                'created_at' => $this->created_at->toISOString(),
                'updated_at' => $this->updated_at->toISOString(),
            ],
            'links' => [
                'self' => route('api.posts.show', $this->id),
            ],
        ];
    }
}

// Consistent collection response
class PostCollection extends ResourceCollection
{
    public function toArray(Request $request): array
    {
        return [
            'data'  => $this->collection,
            'meta'  => ['total' => $this->total()],
            'links' => ['self' => request()->url()],
        ];
    }
}
```

### 4️⃣ Authentication with Sanctum
```php
// routes/api.php
Route::post('/auth/login', [AuthController::class, 'login']);
Route::post('/auth/register', [AuthController::class, 'register']);

Route::middleware('auth:sanctum')->group(function () {
    Route::post('/auth/logout', [AuthController::class, 'logout']);
    Route::apiResource('posts', PostController::class);
});

// AuthController
public function login(LoginRequest $request): JsonResponse
{
    $user = User::where('email', $request->email)->first();

    if (!$user || !Hash::check($request->password, $user->password)) {
        throw ValidationException::withMessages([
            'email' => ['The provided credentials are incorrect.'],
        ]);
    }

    $token = $user->createToken($request->device_name ?? 'api')->plainTextToken;

    return response()->json([
        'token' => $token,
        'user'  => new UserResource($user),
    ]);
}
```

### 5️⃣ Rate Limiting
```php
// RouteServiceProvider
RateLimiter::for('api', function (Request $request) {
    return Limit::perMinute(60)->by($request->user()?->id ?: $request->ip());
});

RateLimiter::for('auth', function (Request $request) {
    return Limit::perMinute(5)->by($request->ip());
});
```

### 6️⃣ Consistent Error Responses
```php
// App/Exceptions/Handler.php
public function render($request, Throwable $e): Response
{
    if ($request->expectsJson()) {
        return match(true) {
            $e instanceof ValidationException    => $this->validationError($e),
            $e instanceof AuthenticationException => $this->unauthenticated($e),
            $e instanceof ModelNotFoundException => $this->notFound($e),
            $e instanceof HttpException          => $this->httpError($e),
            default                              => $this->serverError($e),
        };
    }
    return parent::render($request, $e);
}

private function validationError(ValidationException $e): JsonResponse
{
    return response()->json([
        'message' => 'Validation failed',
        'errors'  => $e->errors(),
    ], 422);
}
```

### 7️⃣ API Testing
```php
// Feature test
class PostApiTest extends TestCase
{
    use RefreshDatabase;

    public function test_authenticated_user_can_create_post(): void
    {
        $user = User::factory()->create();
        $token = $user->createToken('test')->plainTextToken;

        $response = $this->withToken($token)
            ->postJson('/api/v1/posts', [
                'title' => 'Test Post',
                'body'  => str_repeat('a', 100),
            ]);

        $response->assertCreated()
            ->assertJsonPath('data.title', 'Test Post');
    }
}
```

## Outputs
1. API route structure with versioning
2. Controller scaffolding with thin methods
3. Resource classes for all models
4. Authentication flow (Sanctum/Passport)
5. Rate limiting configuration
6. Error handling middleware
7. Feature test suite template
