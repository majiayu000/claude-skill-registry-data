---
name: laravel-conventions
description: >-
  Laravel development conventions for this project. Covers controller patterns, middleware,
  service layer, Form Requests, route organization, Blade components, and queue jobs.
  Use when creating or modifying any Laravel application code.
---

# Laravel Conventions

## Controller Patterns

### Web Controllers (blade-ssr mode)
```php
class ProductController extends Controller
{
    public function index()
    {
        $products = Product::query()
            ->with('category')
            ->latest()
            ->paginate(15);

        return view('products.index', compact('products'));
    }

    public function store(Request $request)
    {
        $validated = $request->validate([
            'name' => 'required|string|max:255',
            'price' => 'required|numeric|min:0',
            'category_id' => 'required|exists:categories,id',
        ]);

        $product = Product::create($validated);

        return redirect()->route('products.show', $product)
            ->with('success', 'Product created successfully.');
    }
}
```

### API Controllers (react-spa mode)
```php
class ProductController extends Controller
{
    public function index(): JsonResponse
    {
        $products = Product::query()
            ->with('category')
            ->latest()
            ->paginate(15);

        return response()->json($products);
    }

    public function store(Request $request): JsonResponse
    {
        $validated = $request->validate([
            'name' => 'required|string|max:255',
            'price' => 'required|numeric|min:0',
            'category_id' => 'required|exists:categories,id',
        ]);

        $product = Product::create($validated);

        return response()->json($product, 201);
    }
}
```

### Key Differences
- Web: returns `view()` or `redirect()`
- API: returns `response()->json()` with HTTP status codes
- API: always declare `: JsonResponse` return type

## Form Requests (When to Use)

Use Form Requests when:
- Validation rules are complex (5+ rules)
- Same validation is used in multiple places
- Authorization logic is needed

```php
// Create with: php artisan make:request StoreProductRequest

class StoreProductRequest extends FormRequest
{
    public function authorize(): bool
    {
        return true; // or: return $this->user()->isAdmin();
    }

    public function rules(): array
    {
        return [
            'name' => 'required|string|max:255',
            'price' => 'required|numeric|min:0',
        ];
    }
}
```

For simple cases (2-3 rules), inline `$request->validate([])` is fine.

## Route Organization

```php
// routes/web.php — Group by feature
Route::middleware('auth')->group(function () {
    // Products
    Route::resource('products', ProductController::class);
    
    // Orders
    Route::resource('orders', OrderController::class)->only(['index', 'show', 'store']);
});

// Admin routes
Route::middleware(['auth', EnsureIsAdmin::class])
    ->prefix('admin')
    ->name('admin.')
    ->group(function () {
        Route::get('/', [AdminDashboardController::class, 'index'])->name('dashboard');
        Route::resource('users', AdminUserController::class);
    });
```

## Eloquent Best Practices

```php
// ✅ Use query() for clarity
Product::query()->where('active', true)->get();

// ✅ Eager load to avoid N+1
Product::query()->with(['category', 'tags'])->get();

// ✅ Use scopes for reusable queries
// In Model:
public function scopeActive(Builder $query): Builder
{
    return $query->where('active', true);
}
// Usage:
Product::active()->get();

// ✅ Use casts() method (not $casts property)
protected function casts(): array
{
    return [
        'price' => 'integer',
        'metadata' => 'array',
        'published_at' => 'datetime',
    ];
}

// ✅ Explicit relationship return types
public function category(): BelongsTo
{
    return $this->belongsTo(Category::class);
}

// ❌ Avoid raw DB queries
DB::table('products')->where(...); // NO
Product::query()->where(...);       // YES
```

## Middleware

```php
// Custom middleware pattern
class EnsureIsVerified
{
    public function handle(Request $request, Closure $next): Response
    {
        if (! $request->user()?->hasVerifiedEmail()) {
            if ($request->expectsJson()) {
                return response()->json(['message' => 'Email not verified.'], 403);
            }
            return redirect()->route('verification.notice');
        }

        return $next($request);
    }
}
```

Always handle both JSON and HTML responses using `$request->expectsJson()`.

## Queue Jobs

```php
// Create with: php artisan make:job ProcessImage

class ProcessImage implements ShouldQueue
{
    use Queueable;

    public function __construct(
        public readonly Product $product,
    ) {}

    public function handle(): void
    {
        // Process the image...
    }

    public function failed(\Throwable $exception): void
    {
        // Handle failure (notify admin, log, etc.)
    }
}

// Dispatch:
ProcessImage::dispatch($product);
```

## Blade Components (blade-ssr mode)

```php
// Anonymous component: resources/views/components/button.blade.php
@props(['type' => 'button', 'variant' => 'primary'])

<button type="{{ $type }}" {{ $attributes->merge(['class' => "btn btn-{$variant}"]) }}>
    {{ $slot }}
</button>

// Usage:
<x-button type="submit" variant="danger">Delete</x-button>
```

## Error Handling

```php
// In bootstrap/app.php
->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->shouldRenderJsonWhen(
        fn (Request $request) => $request->is('api/*'),
    );
})
```

## Artisan Commands Reference

```bash
# Models
php artisan make:model Product -mfc    # Model + Migration + Factory + Controller
php artisan make:model Product -mfcr   # + Resource controller

# Other
php artisan make:controller Api/ProductController --api
php artisan make:middleware EnsureIsVerified
php artisan make:request StoreProductRequest
php artisan make:job ProcessImage
php artisan make:mail OrderConfirmation
php artisan make:event OrderPlaced
php artisan make:listener SendOrderNotification
```
