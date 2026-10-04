---
name: php-symfony
description: >-
  Patterns for PHP/Symfony with service layer architecture. Includes Doctrine
  ORM, PHPUnit, Messenger, Voters. Use when: Symfony development, composer.json
  with symfony detected. Not for: Laravel, plain PHP, WordPress, Drupal.
---

# PHP/Symfony Development Patterns

## Overview

Modern Symfony (7.x/8.x) patterns emphasizing thin controllers, final services,
Doctrine ORM, and Messenger for async operations. Service layer architecture
with clear separation of concerns.

## Auto-detection

Automatically loaded when detecting:
- `composer.json` containing `symfony/framework-bundle`
- Directory structure: `config/packages/`, `src/Controller/`, `src/Entity/`
- Files: `symfony.lock`, `bin/console`

## Architecture → @references/architecture.md

### Project Structure

```
project/
├── config/
│   ├── packages/              # Bundle configuration
│   ├── routes/                # Route definitions
│   └── services.yaml          # DI configuration
├── src/
│   ├── Controller/            # Thin HTTP controllers
│   ├── Command/               # Console commands
│   ├── Entity/                # Doctrine entities
│   ├── Repository/            # Doctrine repositories
│   ├── Service/               # Business logic (final classes)
│   ├── Dto/                   # Data Transfer Objects
│   ├── Handler/               # Use-case handlers (CQRS)
│   ├── Message/               # Messenger messages
│   ├── MessageHandler/        # Async handlers
│   ├── Event/                 # Domain events
│   ├── EventListener/         # Event listeners
│   ├── Security/Voter/        # Authorization voters
│   └── Validator/Constraint/  # Custom validation
├── templates/                 # Twig templates
├── tests/
│   ├── Unit/
│   └── Functional/
└── public/index.php
```

### Thin Controller Pattern

```php
<?php
declare(strict_types=1);

#[Route('/api/users', name: 'api_users_')]
final class UserController extends AbstractController
{
    public function __construct(
        private readonly UserService $userService,
    ) {}

    #[Route('', name: 'create', methods: ['POST'])]
    public function create(#[MapRequestPayload] CreateUserDto $dto): JsonResponse
    {
        $user = $this->userService->createUser($dto->email, $dto->name);
        return $this->json($user, Response::HTTP_CREATED, [], ['groups' => ['user:read']]);
    }
}
```

### Service Layer

```php
<?php
declare(strict_types=1);

final class UserService
{
    public function __construct(
        private readonly UserRepository $userRepository,
        private readonly EntityManagerInterface $entityManager,
        private readonly EventDispatcherInterface $eventDispatcher,
    ) {}

    public function createUser(string $email, string $name): User
    {
        $user = new User($email, $name);
        $this->entityManager->persist($user);
        $this->entityManager->flush();
        $this->eventDispatcher->dispatch(new UserCreatedEvent($user));
        return $user;
    }
}
```

## Doctrine ORM → @references/doctrine.md

### Entity with Business Methods

```php
<?php
declare(strict_types=1);

#[ORM\Entity(repositoryClass: UserRepository::class)]
#[ORM\Table(name: 'users')]
#[ORM\Index(columns: ['status', 'created_at'], name: 'idx_user_status_created')]
final class User
{
    public const STATUS_PENDING = 'pending';
    public const STATUS_ACTIVE = 'active';

    #[ORM\Id, ORM\GeneratedValue, ORM\Column]
    private ?int $id = null;

    #[ORM\Column(length: 255, unique: true)]
    private string $email;

    #[ORM\Column(length: 20)]
    private string $status = self::STATUS_PENDING;

    public function __construct(string $email, string $name) { /* ... */ }

    public function activate(): void
    {
        if ($this->status !== self::STATUS_PENDING) {
            throw new \DomainException('Only pending users can be activated');
        }
        $this->status = self::STATUS_ACTIVE;
    }
}
```

### N+1 Prevention

```php
// BAD - N+1 queries
foreach ($orders as $order) {
    echo $order->getCustomer()->getName(); // 1 query per order
}

// GOOD - Eager loading with JOIN
public function findAllWithCustomer(): array
{
    return $this->createQueryBuilder('o')
        ->select('o', 'c')
        ->join('o.customer', 'c')
        ->getQuery()
        ->getResult();
}
```

## Security → @references/security.md

### Voters for Authorization

```php
<?php
declare(strict_types=1);

final class PostVoter extends Voter
{
    public const EDIT = 'POST_EDIT';

    protected function voteOnAttribute(string $attribute, mixed $subject, TokenInterface $token): bool
    {
        $user = $token->getUser();
        if (!$user instanceof User) return false;

        return match ($attribute) {
            self::EDIT => $subject->getAuthor() === $user,
            default => false,
        };
    }
}

// In controller
#[IsGranted('POST_EDIT', subject: 'post')]
public function edit(Post $post): Response { /* ... */ }
```

### CSRF Protection

```php
// In form - enabled by default
// For non-form actions
#[IsCsrfTokenValid('delete-post', tokenKey: '_token')]
public function delete(Post $post): Response { /* ... */ }
```

## Messenger → @references/messenger.md

### Async Message Pattern

```php
<?php
// Message (simple data object)
final readonly class SendWelcomeEmailMessage
{
    public function __construct(
        public int $userId,
        public string $email,
    ) {}
}

// Handler
#[AsMessageHandler]
final class SendWelcomeEmailHandler
{
    public function __invoke(SendWelcomeEmailMessage $message): void
    {
        $this->emailService->sendWelcomeEmail($message->email);
    }
}

// Dispatch
$this->bus->dispatch(new SendWelcomeEmailMessage($user->getId(), $user->getEmail()));
```

## Testing → @references/testing.md

### PHPUnit WebTestCase

```php
<?php
declare(strict_types=1);

final class UserControllerTest extends WebTestCase
{
    public function testCreateUser(): void
    {
        $client = static::createClient();
        $client->request('POST', '/api/users', [], [],
            ['CONTENT_TYPE' => 'application/json'],
            json_encode(['email' => 'new@example.com', 'name' => 'Test'])
        );

        $this->assertResponseStatusCodeSame(Response::HTTP_CREATED);
    }

    public function testAdminAccessRequiresAuthentication(): void
    {
        $client = static::createClient();
        $client->loginUser($admin);
        $client->request('GET', '/admin/users');
        $this->assertResponseIsSuccessful();
    }
}
```

## Commands

```bash
# Entity & Migration
php bin/console make:entity
php bin/console make:migration
php bin/console doctrine:migrations:migrate

# Debug
php bin/console debug:router
php bin/console debug:container UserService
php bin/console debug:autowiring

# Messenger
php bin/console messenger:consume async --limit=100 --memory-limit=128M

# Tests
php bin/phpunit
php bin/phpunit --testsuite Unit
php bin/phpunit --coverage-html coverage/
```

---

## Quick Reference

| Element | Convention | Example |
|---------|------------|---------|
| Controller | `*Controller`, final | `UserController` |
| Entity | Singular, PascalCase, final | `User`, `OrderItem` |
| Repository | `*Repository`, final | `UserRepository` |
| Service | Descriptive, final | `EmailNotifier` |
| DTO | `*Dto`, readonly | `CreateUserDto` |
| Message | `*Message`, readonly | `SendWelcomeEmailMessage` |
| Voter | `*Voter`, final | `PostVoter` |
| Command | `app:domain:action` | `app:user:cleanup` |

---

## Common Patterns

| Pattern | Implementation |
|---------|----------------|
| Thin Controller | Delegate to service, return response only |
| Final Services | All services `final class`, constructor injection |
| DTO Validation | `#[MapRequestPayload]` with `#[Assert\*]` constraints |
| Repository Methods | Custom finders, no business logic |
| Domain Events | Dispatch via `EventDispatcherInterface` |
| Async Processing | Messenger with `#[AsMessageHandler]` |
| Authorization | Voters with `#[IsGranted]` attribute |
| CSRF | `#[IsCsrfTokenValid]` for non-form actions |

---

## Anti-patterns

| Anti-pattern | Problem | Solution |
|--------------|---------|----------|
| Fat controller | Business logic in controller | Extract to service |
| `$container->get()` | Service locator, untestable | Constructor injection |
| Public setters | Mutable state, no validation | Business methods |
| N+1 queries | Performance degradation | `select()` + `join()` |
| Hardcoded config | Environment-specific values | `%env(VAR)%` |
| Manual validation | Inconsistent, verbose | Validator constraints |
| Role checks in code | Scattered authorization | Voters |
| Sync heavy tasks | Blocking requests | Messenger async |
