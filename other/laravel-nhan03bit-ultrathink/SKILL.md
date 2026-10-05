---
name: laravel
description: "Laravel PHP framework — Eloquent ORM, Blade templates, middleware, queues, and Sanctum auth."
layer: domain
category: backend
triggers:
  - "laravel"
  - "eloquent"
  - "blade template"
  - "laravel sanctum"
  - "artisan"
inputs:
  - "API endpoint or feature requirements"
  - "Eloquent relationship design questions"
  - "Queue job and event handling needs"
  - "Authentication and authorization configuration"
outputs:
  - "Laravel controllers, models, and migrations"
  - "Eloquent queries with proper eager loading"
  - "Queue jobs and event listeners"
  - "Middleware and policy configurations"
linksTo:
  - postgresql
  - redis
  - docker
linkedFrom: []
riskLevel: low
memoryReadPolicy: selective
memoryWritePolicy: none
sideEffects: []
---

# Laravel Patterns & Best Practices

## Purpose

Provide expert guidance on Laravel application architecture, Eloquent ORM patterns, queue management, API development, and production-grade configuration. Covers Laravel 11+ with its streamlined application structure.

## Key Patterns

### Project Structure (Laravel 11+)

Laravel 11 simplifies the directory structure:

```
app/
├── Http/
│   ├── Controllers/
│   ├── Middleware/
│   └── Requests/          # Form request validation
├── Models/
├── Services/              # Business logic (custom)
├── Actions/               # Single-purpose action classes (custom)
├── Events/
├── Listeners/
├── Jobs/
├── Policies/
├── Enums/
└── Providers/
database/
├── migrations/
├── seeders/
└── factories/
routes/
├── api.php
└── web.php
```

### Eloquent Models

**Model with relationships, scopes, and casts:**

```php
class Order extends Model
{
    use HasFactory, SoftDeletes;

    protected $fillable = [
        'user_id',
        'status',
        'notes',
        'total_cents',
    ];

    protected function casts(): array
    {
        return [
            'status' => OrderStatus::class,      // Backed enum
            'total_cents' => 'integer',
            'shipped_at' => 'immutable_datetime',
        ];
    }

    // Relationships
    public function user(): BelongsTo
    {
        return $this->belongsTo(User::class);
    }

    public function items(): HasMany
    {
        return $this->hasMany(OrderItem::class);
    }

    public function tags(): BelongsToMany
    {
        return $this->belongsToMany(Tag::class)->withTimestamps();
    }

    // Scopes
    public function scopeCompleted(Builder $query): Builder
    {
        return $query->where('status', OrderStatus::Completed);
    }

    public function scopeRecent(Builder $query, int $days = 30): Builder
    {
        return $query->where('created_at', '>=', now()->subDays($days));
    }

    // Accessors
    protected function totalFormatted(): Attribute
    {
        return Attribute::make(
            get: fn () => number_format($this->total_cents / 100, 2),
        );
    }
}
```

**Backed enum for status fields:**

```php
enum OrderStatus: string
{
    case Draft = 'draft';
    case Pending = 'pending';
    case Processing = 'processing';
    case Completed = 'completed';
    case Cancelled = 'cancelled';

    public function label(): string
    {
        return match ($this) {
            self::Draft => 'Draft',
            self::Pending => 'Pending Payment',
            self::Processing => 'Processing',
            self::Completed => 'Completed',
            self::Cancelled => 'Cancelled',
        };
    }

    public function canTransitionTo(self $next): bool
    {
        return match ($this) {
            self::Draft => in_array($next, [self::Pending, self::Cancelled]),
            self::Pending => in_array($next, [self::Processing, self::Cancelled]),
            self::Processing => in_array($next, [self::Completed, self::Cancelled]),
            default => false,
        };
    }
}
```

### Controllers

**API Resource Controller with Form Requests:**

```php
class OrderController extends Controller
{
    public function __construct(
        private readonly OrderService $orderService,
    ) {}

    public function index(Request $request): AnonymousResourceCollection
    {
        $orders = Order::query()
            ->with(['user:id,name', 'items.product:id,name,price_cents'])
            ->when($request->status, fn ($q, $status) => $q->where('status', $status))
            ->when($request->search, fn ($q, $search) => $q->whereHas('user', fn ($q) =>
                $q->where('name', 'ilike', "%{$search}%")
            ))
            ->latest()
            ->paginate($request->integer('per_page', 20));

        return OrderResource::collection($orders);
    }

    public function store(StoreOrderRequest $request): JsonResponse
    {
        $order = $this->orderService->create($request->validated());

        return OrderResource::make($order)
            ->response()
            ->setStatusCode(201);
    }

    public function show(Order $order): OrderResource
    {
        $order->load(['items.product', 'user']);
        return OrderResource::make($order);
    }

    public function update(UpdateOrderRequest $request, Order $order): OrderResource
    {
        $order = $this->orderService->update($order, $request->validated());
        return OrderResource::make($order);
    }

    public function destroy(Order $order): Response
    {
        $this->authorize('delete', $order);
        $order->delete();
        return response()->noContent();
    }
}
```

**Form Request Validation:**

```php
class StoreOrderRequest extends FormRequest
{
    public function authorize(): bool
    {
        return true;
    }

    public function rules(): array
    {
        return [
            'items' => ['required', 'array', 'min:1'],
            'items.*.product_id' => ['required', 'exists:products,id'],
            'items.*.quantity' => ['required', 'integer', 'min:1', 'max:100'],
            'notes' => ['nullable', 'string', 'max:1000'],
            'shipping_address_id' => ['required', 'exists:addresses,id'],
        ];
    }

    public function messages(): array
    {
        return [
            'items.required' => 'At least one item is required.',
            'items.*.product_id.exists' => 'Product not found.',
        ];
    }
}
```

### API Resources

```php
class OrderResource extends JsonResource
{
    public function toArray(Request $request): array
    {
        return [
            'id' => $this->id,
            'status' => $this->status->value,
            'status_label' => $this->status->label(),
            'total_formatted' => $this->total_formatted,
            'notes' => $this->notes,
            'items' => OrderItemResource::collection($this->whenLoaded('items')),
            'user' => UserResource::make($this->whenLoaded('user')),
            'created_at' => $this->created_at->toISOString(),
            'updated_at' => $this->updated_at->toISOString(),
        ];
    }
}
```

### Queue Jobs

```php
class ProcessOrderJob implements ShouldQueue
{
    use Queueable;

    public int $tries = 3;
    public int $backoff = 60; // seconds
    public int $timeout = 120;

    public function __construct(
        public readonly Order $order,
    ) {}

    public function handle(PaymentGateway $gateway, InventoryService $inventory): void
    {
        DB::transaction(function () use ($gateway, $inventory) {
            $gateway->charge($this->order);
            $inventory->reserve($this->order->items);
            $this->order->update(['status' => OrderStatus::Processing]);
        });

        OrderProcessed::dispatch($this->order);
    }

    public function failed(\Throwable $exception): void
    {
        Log::error('Order processing failed', [
            'order_id' => $this->order->id,
            'error' => $exception->getMessage(),
        ]);

        $this->order->update(['status' => OrderStatus::Draft]);
        Notification::send($this->order->user, new OrderFailedNotification($this->order));
    }

    public function retryUntil(): DateTime
    {
        return now()->addHours(1);
    }
}
```

### Middleware

```php
// Custom rate limiter in AppServiceProvider
RateLimiter::for('api', function (Request $request) {
    return Limit::perMinute(60)->by($request->user()?->id ?: $request->ip());
});

// Custom middleware
class EnsureJsonResponse
{
    public function handle(Request $request, Closure $next): Response
    {
        $request->headers->set('Accept', 'application/json');
        return $next($request);
    }
}
```

### Migrations

```php
return new class extends Migration
{
    public function up(): void
    {
        Schema::create('orders', function (Blueprint $table) {
            $table->id();
            $table->foreignId('user_id')->constrained()->cascadeOnDelete();
            $table->string('status', 20)->default('draft')->index();
            $table->integer('total_cents')->default(0);
            $table->text('notes')->nullable();
            $table->timestamp('shipped_at')->nullable();
            $table->timestamps();
            $table->softDeletes();

            $table->index(['user_id', 'status']);
            $table->index('created_at');
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('orders');
    }
};
```

### Action Classes

Single-responsibility action classes for complex operations:

```php
class CreateOrderAction
{
    public function __construct(
        private readonly InventoryService $inventory,
    ) {}

    public function execute(User $user, array $data): Order
    {
        return DB::transaction(function () use ($user, $data) {
            $order = $user->orders()->create([
                'status' => OrderStatus::Draft,
                'notes' => $data['notes'] ?? null,
            ]);

            foreach ($data['items'] as $item) {
                $product = Product::findOrFail($item['product_id']);
                $this->inventory->checkAvailability($product, $item['quantity']);

                $order->items()->create([
                    'product_id' => $product->id,
                    'quantity' => $item['quantity'],
                    'price_cents' => $product->price_cents,
                ]);
            }

            $order->update(['total_cents' => $order->items->sum(fn ($i) =>
                $i->price_cents * $i->quantity
            )]);

            return $order->load('items.product');
        });
    }
}
```

## Best Practices

1. **Always eager load relationships** — Use `with()` to prevent N+1 queries. Run `DB::enableQueryLog()` in development to catch them.
2. **Use Form Requests for validation** — Keep controllers thin by extracting validation to dedicated request classes.
3. **Use API Resources for responses** — Never return Eloquent models directly. Resources give you a stable API contract.
4. **Use backed enums for status fields** — Type-safe, castable, and self-documenting.
5. **Use action classes for complex operations** — Single-purpose, testable, reusable business logic.
6. **Queue heavy operations** — Email, PDF generation, payment processing, and third-party API calls belong in jobs.
7. **Use database transactions** — Wrap multi-step writes in `DB::transaction()`.
8. **Index foreign keys and frequently filtered columns** — Laravel does not auto-index `foreignId` columns in all cases.
9. **Use `chunk()` or `lazy()` for large datasets** — Never load thousands of models into memory at once.
10. **Cache configuration in production** — Run `php artisan config:cache`, `route:cache`, and `view:cache` on deploy.

## Common Pitfalls

| Pitfall | Problem | Fix |
|---------|---------|-----|
| N+1 queries | Accessing relationships in loops without eager loading | Use `with()` or `load()` |
| Mass assignment vulnerability | Filling unguarded attributes | Define `$fillable` or `$guarded` |
| Missing queue worker restart | Workers cache old code after deploy | Use `php artisan queue:restart` in deploy script |
| Fat controllers | Business logic in controllers | Extract to service/action classes |
| No transaction wrapping | Partial writes on failure | Wrap in `DB::transaction()` |
| Returning models from API | Exposing internal structure, passwords | Use API Resources |
| Synchronous heavy tasks | Slow response times | Dispatch to queues |
| Missing database indexes | Slow queries at scale | Add composite indexes for common query patterns |
