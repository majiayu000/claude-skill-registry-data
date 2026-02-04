---
name: laravel-patterns
description: Laravel 12 best practices, design patterns, and coding standards. Use when creating controllers, models, services, middleware, or any PHP backend code in Laravel projects.
allowed-tools: Read, Grep, Glob, Edit, Write
---

# Laravel Best Practices Skill

This skill provides guidance for writing clean, maintainable Laravel 12 code following modern PHP and Laravel conventions.

## Project Structure

### Service Layer Pattern
```
app/
├── Http/
│   ├── Controllers/        # Thin controllers, delegate to services
│   ├── Requests/           # Form request validation
│   ├── Resources/          # API resources
│   └── Middleware/         # Request/response middleware
├── Models/                 # Eloquent models
├── Services/               # Business logic
├── Repositories/           # Data access (optional)
├── Actions/                # Single-purpose action classes
├── DTOs/                   # Data transfer objects
├── Enums/                  # PHP 8.1+ enums
└── Exceptions/             # Custom exceptions
```

## Controllers

### Thin Controllers
Controllers should only handle HTTP concerns. Delegate business logic to services.

```php
<?php

namespace App\Http\Controllers;

use App\Http\Requests\StoreEmployeeRequest;
use App\Http\Resources\EmployeeResource;
use App\Services\EmployeeService;
use Illuminate\Http\JsonResponse;

class EmployeeController extends Controller
{
    public function __construct(
        private readonly EmployeeService $employeeService
    ) {}

    public function store(StoreEmployeeRequest $request): JsonResponse
    {
        $employee = $this->employeeService->create($request->validated());

        return EmployeeResource::make($employee)
            ->response()
            ->setStatusCode(201);
    }

    public function index(): JsonResponse
    {
        $employees = $this->employeeService->paginate();

        return EmployeeResource::collection($employees)->response();
    }
}
```

### Resource Controllers
Use resource controllers for CRUD operations:
```php
Route::resource('employees', EmployeeController::class);
Route::apiResource('api/employees', Api\EmployeeController::class);
```

## Form Requests

### Validation Logic
```php
<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;
use Illuminate\Validation\Rule;

class StoreEmployeeRequest extends FormRequest
{
    public function authorize(): bool
    {
        return $this->user()->can('create', Employee::class);
    }

    public function rules(): array
    {
        return [
            'name' => ['required', 'string', 'max:255'],
            'email' => ['required', 'email', 'unique:employees,email'],
            'employee_id' => ['required', 'string', 'unique:employees'],
            'department' => ['required', Rule::in(['IT', 'HR', 'Finance'])],
            'salary' => ['required', 'numeric', 'min:0'],
            'hire_date' => ['required', 'date', 'before_or_equal:today'],
        ];
    }

    public function messages(): array
    {
        return [
            'email.unique' => 'Email sudah terdaftar.',
            'hire_date.before_or_equal' => 'Tanggal tidak boleh di masa depan.',
        ];
    }
}
```

## Services

### Service Class Pattern
```php
<?php

namespace App\Services;

use App\Models\Employee;
use App\DTOs\EmployeeData;
use Illuminate\Pagination\LengthAwarePaginator;
use Illuminate\Support\Facades\DB;

class EmployeeService
{
    public function __construct(
        private readonly AttendanceService $attendanceService
    ) {}

    public function create(array $data): Employee
    {
        return DB::transaction(function () use ($data) {
            $employee = Employee::create($data);

            // Related operations
            $this->attendanceService->initializeForEmployee($employee);

            return $employee->fresh(['department', 'schedules']);
        });
    }

    public function paginate(int $perPage = 15): LengthAwarePaginator
    {
        return Employee::query()
            ->with(['department', 'latestAttendance'])
            ->withCount('attendances')
            ->latest()
            ->paginate($perPage);
    }

    public function findOrFail(string $id): Employee
    {
        return Employee::with(['department', 'schedules', 'attendances'])
            ->findOrFail($id);
    }
}
```

## Models

### Model Best Practices
```php
<?php

namespace App\Models;

use App\Enums\EmployeeStatus;
use App\Enums\EmployeeType;
use Illuminate\Database\Eloquent\Concerns\HasUuids;
use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Database\Eloquent\Relations\HasMany;
use Illuminate\Database\Eloquent\SoftDeletes;

class Employee extends Model
{
    use HasFactory, HasUuids, SoftDeletes;

    protected $fillable = [
        'name',
        'email',
        'employee_id',
        'department_id',
        'position',
        'salary',
        'hire_date',
        'status',
        'type',
    ];

    protected function casts(): array
    {
        return [
            'hire_date' => 'date',
            'salary' => 'decimal:2',
            'status' => EmployeeStatus::class,
            'type' => EmployeeType::class,
            'metadata' => 'array',
        ];
    }

    // Relationships
    public function department(): BelongsTo
    {
        return $this->belongsTo(Department::class);
    }

    public function attendances(): HasMany
    {
        return $this->hasMany(Attendance::class);
    }

    public function latestAttendance(): HasOne
    {
        return $this->hasOne(Attendance::class)->latestOfMany();
    }

    // Scopes
    public function scopeActive(Builder $query): Builder
    {
        return $query->where('status', EmployeeStatus::Active);
    }

    public function scopeByDepartment(Builder $query, string $departmentId): Builder
    {
        return $query->where('department_id', $departmentId);
    }

    // Accessors
    protected function fullName(): Attribute
    {
        return Attribute::get(fn () => "{$this->first_name} {$this->last_name}");
    }
}
```

## Enums (PHP 8.1+)

```php
<?php

namespace App\Enums;

enum EmployeeStatus: string
{
    case Active = 'active';
    case Inactive = 'inactive';
    case OnLeave = 'on_leave';
    case Terminated = 'terminated';

    public function label(): string
    {
        return match($this) {
            self::Active => 'Aktif',
            self::Inactive => 'Tidak Aktif',
            self::OnLeave => 'Cuti',
            self::Terminated => 'Diberhentikan',
        };
    }

    public function color(): string
    {
        return match($this) {
            self::Active => 'green',
            self::Inactive => 'gray',
            self::OnLeave => 'yellow',
            self::Terminated => 'red',
        };
    }
}
```

## Query Optimization

### Eager Loading
```php
// BAD - N+1 problem
$employees = Employee::all();
foreach ($employees as $employee) {
    echo $employee->department->name; // N queries
}

// GOOD - Eager load
$employees = Employee::with(['department', 'schedules'])->get();
```

### Chunking Large Datasets
```php
Employee::query()
    ->where('status', 'active')
    ->chunk(100, function ($employees) {
        foreach ($employees as $employee) {
            // Process each employee
        }
    });

// Or with lazy loading for memory efficiency
Employee::query()
    ->where('status', 'active')
    ->lazy()
    ->each(function ($employee) {
        // Process
    });
```

### Query Scopes
```php
// In Model
public function scopeAttendedToday(Builder $query): Builder
{
    return $query->whereHas('attendances', function ($q) {
        $q->whereDate('date', today());
    });
}

// Usage
$presentEmployees = Employee::active()->attendedToday()->get();
```

## API Resources

```php
<?php

namespace App\Http\Resources;

use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;

class EmployeeResource extends JsonResource
{
    public function toArray(Request $request): array
    {
        return [
            'id' => $this->id,
            'name' => $this->name,
            'email' => $this->email,
            'employee_id' => $this->employee_id,
            'position' => $this->position,
            'status' => [
                'value' => $this->status->value,
                'label' => $this->status->label(),
                'color' => $this->status->color(),
            ],
            'department' => DepartmentResource::make($this->whenLoaded('department')),
            'attendances_count' => $this->whenCounted('attendances'),
            'latest_attendance' => AttendanceResource::make($this->whenLoaded('latestAttendance')),
            'created_at' => $this->created_at->toISOString(),
            'updated_at' => $this->updated_at->toISOString(),
        ];
    }
}
```

## Exception Handling

### Custom Exceptions
```php
<?php

namespace App\Exceptions;

use Exception;
use Illuminate\Http\JsonResponse;

class EmployeeNotFoundException extends Exception
{
    public function __construct(string $employeeId)
    {
        parent::__construct("Employee with ID {$employeeId} not found.");
    }

    public function render(): JsonResponse
    {
        return response()->json([
            'error' => 'employee_not_found',
            'message' => $this->getMessage(),
        ], 404);
    }
}
```

## Middleware

```php
<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\Response;

class EnsureEmployeeIsActive
{
    public function handle(Request $request, Closure $next): Response
    {
        $employee = $request->user()->employee;

        if (!$employee || !$employee->status->isActive()) {
            abort(403, 'Employee account is not active.');
        }

        return $next($request);
    }
}
```

## Testing

### Feature Tests
```php
<?php

namespace Tests\Feature;

use App\Models\Employee;
use App\Models\User;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class EmployeeControllerTest extends TestCase
{
    use RefreshDatabase;

    public function test_can_list_employees(): void
    {
        $user = User::factory()->admin()->create();
        Employee::factory()->count(5)->create();

        $response = $this->actingAs($user)
            ->getJson('/api/employees');

        $response->assertOk()
            ->assertJsonCount(5, 'data')
            ->assertJsonStructure([
                'data' => [
                    '*' => ['id', 'name', 'email', 'status']
                ],
                'meta' => ['current_page', 'total']
            ]);
    }

    public function test_can_create_employee(): void
    {
        $user = User::factory()->admin()->create();

        $response = $this->actingAs($user)
            ->postJson('/api/employees', [
                'name' => 'John Doe',
                'email' => 'john@example.com',
                'employee_id' => 'EMP001',
            ]);

        $response->assertCreated()
            ->assertJsonPath('data.name', 'John Doe');

        $this->assertDatabaseHas('employees', [
            'email' => 'john@example.com'
        ]);
    }
}
```

## Security Best Practices

### Mass Assignment Protection
```php
// Always use $fillable, never use $guarded = []
protected $fillable = ['name', 'email', 'position'];
```

### Authorization with Policies
```php
// Policy
public function update(User $user, Employee $employee): bool
{
    return $user->hasRole('admin') || $user->employee_id === $employee->id;
}

// Controller
$this->authorize('update', $employee);
```

### Sensitive Data
```php
// Hide sensitive attributes
protected $hidden = ['password', 'salary', 'remember_token'];

// Or explicitly select
Employee::select(['id', 'name', 'email'])->get();
```

## Performance Tips

1. **Cache expensive queries**
   ```php
   Cache::remember('dashboard.stats', 3600, fn() => $this->calculateStats());
   ```

2. **Use database transactions**
   ```php
   DB::transaction(function () {
       // Multiple related operations
   });
   ```

3. **Index frequently queried columns**
   ```php
   $table->index(['department_id', 'status']);
   ```

4. **Use queue for heavy operations**
   ```php
   ProcessPayroll::dispatch($employee)->onQueue('payroll');
   ```
