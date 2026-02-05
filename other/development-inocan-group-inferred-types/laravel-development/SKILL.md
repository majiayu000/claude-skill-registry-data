---
name: laravel-development
description: Master Laravel 11 with Eloquent ORM, routing, middleware, queues, testing, and modern PHP development patterns.
---

# Laravel Development

Build modern PHP applications with Laravel's elegant syntax, Eloquent ORM, and production-ready features.

## Core Patterns

### Controller
```php
<?php

namespace App\Http\Controllers;

use App\Models\User;
use App\Http\Requests\StoreUserRequest;
use Illuminate\Http\JsonResponse;

class UserController extends Controller
{
    public function index(): JsonResponse
    {
        $users = User::all();
        return response()->json($users);
    }

    public function store(StoreUserRequest $request): JsonResponse
    {
        $user = User::create($request->validated());
        return response()->json($user, 201);
    }

    public function show(User $user): JsonResponse
    {
        return response()->json($user);
    }
}
```

### Model
```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

class User extends Model
{
    protected $fillable = ['name', 'email'];

    protected $casts = [
        'email_verified_at' => 'datetime',
    ];

    public function posts(): HasMany
    {
        return $this->hasMany(Post::class);
    }

    public function scopeActive($query)
    {
        return $query->where('active', true);
    }
}
```

### Service
```php
<?php

namespace App\Services;

use App\Models\User;
use Illuminate\Support\Facades\Hash;

class UserService
{
    public function createUser(array $data): User
    {
        return User::create([
            'name' => $data['name'],
            'email' => $data['email'],
            'password' => Hash::make($data['password']),
        ]);
    }
}
```

### Routes
```php
Route::middleware('auth:sanctum')->group(function () {
    Route::apiResource('users', UserController::class);
});
```

## Best Practices

1. Use Eloquent relationships
2. Implement form requests for validation
3. Use service classes for business logic
4. Leverage Laravel queues
5. Implement proper authentication
6. Use middleware for cross-cutting concerns
7. Write feature and unit tests
8. Use Laravel best practices

## Resources
- https://laravel.com/docs
