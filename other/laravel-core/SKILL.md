---
name: laravel-core
description: >
  Activate when creating or modifying SaaS/e-commerce features using the coderstm/laravel-core
  package. Triggers on: Subscription, Plan, Feature, Coupon, Shop, Cart, Checkout, Order,
  Payment, Refund, WalletBalance, Blog, Admin, Currency, AppSetting, PaymentMethod,
  ManagesSubscriptions, Billable, HasWallet, HasFeature, HasPermission, Coderstm facade,
  Blog facade, Shop facade, Currency facade, auth guards, artisan commands (check:canceled-subscriptions,
  subscriptions:renew, reset:subscriptions-usages), config keys (coderstm.*), or any route
  prefixed with /auth/, /subscriptions/, /admin/, /user/, /shop/, or /webhooks/.
---

# Laravel Core Development

`coderstm/laravel-core` is an enterprise-grade Laravel package for building SaaS and e-commerce
applications. It provides multi-guard authentication, subscription billing (via Laravel Cashier),
shopping cart and checkout, 20+ payment gateway integrations, advanced reporting (60+ report types),
role-based access control, multi-currency support, blog/content management, and a wallet/balance
system — all wired together through service providers, facades, traits, and an event-driven
architecture.

## Documentation

Use `search-docs` for detailed laravel-core patterns, model usage, payment processor integration,
and subscription management documentation.

## Architecture

- **Entry point**: `Coderstm\Coderstm` — static facade for model binding, feature toggles, and
  payment/gateway client access (`Coderstm::stripe()`, `Coderstm::paypal()`, etc.)
- **Service Providers**: `CoderstmServiceProvider`, `CoderstmPermissionsServiceProvider`,
  `CoderstmEventServiceProvider`, `ShortcodeServiceProvider`
- **Facades**: `Blog`, `Shop`, `Currency` — request-scoped service accessors
- **Services** (`src/Services/`): `BlogService`, `ShopService`, `Currency`, `ApplicationState`,
  `ConfigLoader`, `ReportService`, `MetricsCalculator`, `NotificationTemplateRenderer`
- **Payment** (`src/Payment/`): `AbstractPaymentProcessor` + 11 concrete processors behind
  `PaymentProcessorInterface`; mapper classes normalise provider responses
- **Traits**: 39 model traits (`Billable`, `ManagesSubscriptions`, `HasWallet`, `HasPermission`,
  `Paymentable`, `Addressable`, `Fileable`, `Avatarable`, etc.)
- **Models**: 61 Eloquent models under `Coderstm\Models`
- **Guards**: `users` (default) and `admins` — both backed by Laravel Sanctum
- **Config**: single file `config/coderstm.php`; many values are overridable from DB via `ConfigLoader`

Use `search-docs` for layer boundaries, DI patterns, and observer/event integration details.

## Usage

- **Main facade**: `Coderstm::useUserModel(User::class)` — bind custom models; `Coderstm::ignoreRoutes()`,
  `Coderstm::withoutCart()`, `Coderstm::ignoreMigrations()` — opt-out toggles
- **Blog facade**: `Blog::current()`, `Blog::find($id)`, `Blog::findBySlug($slug)`,
  `Blog::recent($limit)`, `Blog::categories()`, `Blog::clearCaches()`
- **Shop facade**: `Shop::cart()`, `Shop::checkout()`, `Shop::addToCart(array $data)`,
  `Shop::updateCartItem($id, $qty)`, `Shop::removeCartItem($id)`, `Shop::clearCart()`
- **Currency facade**: `Currency::convert($amount)`, `Currency::format($amount)`,
  `Currency::set($code, $rate)`, `Currency::resolve(array $address)`, `Currency::isBase()`
- **Helpers**: `guard()`, `user($key)`, `is_user()`, `is_admin()`, `app_url($path)`,
  `base_currency()`, `display_currency()`, `format_currency($amount)`, `convert_currency($amount)`
- **Config**: `config/coderstm.php` — sections: `application`, `currency`, `subscription`,
  `shop`, `wallet`, `license`, `theme`
- **Artisan**:
  - `php artisan install` — initial setup
  - `php artisan check:canceled-subscriptions` / `check:grace-period-subscriptions` / `check:expired-subscriptions`
  - `php artisan subscriptions:renew` / `resume:subscriptions`
  - `php artisan reset:subscriptions-usages`
  - `php artisan update:exchange-rates`
  - `php artisan process:abandoned-checkouts`
  - `php artisan cleanup:expired-reports`
  - `php artisan lang:parse`
- **Routes**: `/auth/{guard?}/*` (auth), `/subscriptions/*` (billing), `/admin/*` (admin API),
  `/user/*` (user SPA), `/shop/*` (e-commerce), `/webhooks/*` (payment provider callbacks)
- **Middleware**: `GuardMiddleware`, `CheckSubscribed`, `CartTokenMiddleware`, `ResolveCurrency`,
  `ResolveIpAddress`, `ApplicationState`, `ResponseOptimizer`, `PreserveJsonWhitespace`

## Workflows

### Add a New Subscription Plan

```
- [ ] Create plan via `Plan::create([...])` or via admin API POST `/plans`
- [ ] Define features using `Feature` model and attach to plan via `$plan->features()->attach()`
- [ ] Set `plan_id` on a `Subscription` or use `$user->newSubscription('default', $plan->slug)->create($paymentMethod)`
- [ ] Verify `ManagesSubscriptions` trait is on the User model
- [ ] Schedule `subscriptions:renew` and `reset:subscriptions-usages` in `routes/console.php`
```

> Use `search-docs` for detailed subscription lifecycle patterns.

### Integrate a New Payment Gateway

```
- [ ] Create a processor class extending `AbstractPaymentProcessor` and implementing `PaymentProcessorInterface`
- [ ] Implement `charge()`, `refund()`, `createSubscription()`, `cancelSubscription()` methods
- [ ] Return `PaymentResult` / `RefundResult` value objects
- [ ] Register the processor in `Coderstm::$processors` or via `PaymentMethod` configuration
- [ ] Add a mapper class in `Payment/Mappers/` to normalise provider webhook payloads
- [ ] Register a webhook route in `routes/api.php` pointing to a dedicated webhook controller
- [ ] Add the payment method seed to `PaymentMethod` table or config
```

> Use `search-docs` for detailed payment processor patterns.

### Add a Custom Report

```
- [ ] Create a report class in `src/Services/Reports/` extending the appropriate base
- [ ] Implement `getData()` returning a collection of rows
- [ ] Register the report in `ReportService::$reports` map
- [ ] Add corresponding export class if CSV export is required
- [ ] Expose via admin route if user-facing
```

> Use `search-docs` for detailed report and metrics patterns.

### Implement Feature-Gated Functionality

```
- [ ] Define the feature in `Feature` model with a unique slug
- [ ] Attach feature to the relevant `Plan` records
- [ ] Use `$user->hasFeature('slug')` (via `HasFeature` trait) to gate access
- [ ] Increment usage with `$user->useFeature('slug')` and check limits with `$user->featureUsage('slug')`
- [ ] Reset usage counters via `reset:subscriptions-usages` artisan command on schedule
```

> Use `search-docs` for detailed feature usage patterns.

### Set Up Multi-Currency Support

```
- [ ] Set base currency in `.env` (`CASHIER_CURRENCY` / `coderstm.currency`)
- [ ] Enable auto-detection via `CURRENCY_AUTO_DETECT=true` if needed
- [ ] Use `Currency::resolve($address)` in middleware or controller to set the request currency
- [ ] Format amounts with `format_currency($amount)` helper or `Currency::format($amount)`
- [ ] Schedule `update:exchange-rates` artisan command to keep rates fresh
```

> Use `search-docs` for detailed currency resolution patterns.

### Add Admin RBAC Permissions

```
- [ ] Define a `Module` entry for the feature area
- [ ] Create `Permission` records (e.g., `view`, `create`, `update`, `delete`) linked to the module
- [ ] Assign permissions to `Group` records
- [ ] Assign admins to groups via `$admin->groups()->attach()`
- [ ] Gate routes with `HasPermission::checkPermission('module', 'action')` or the `GuardMiddleware`
```

> Use `search-docs` for detailed RBAC configuration patterns.

## Best Practices

**Strict typing and contracts.** Always declare `strict_types=1` and type-hint against interfaces
(`PaymentProcessorInterface`, `PayableInterface`, `ManagesSubscriptions`) rather than concrete
classes. The DI container resolves the correct implementation at runtime.

**Model binding over hard-coding.** Use `Coderstm::useUserModel()`, `useAdminModel()`,
`useSubscriptionModel()`, etc. in the host application's service provider instead of referencing
concrete model classes directly. This keeps the package decoupled from application-level model
customisations.

**Service facade over `new Service()`.** Resolve `BlogService`, `ShopService`, and `Currency`
through their facades (`Blog::`, `Shop::`, `Currency::`) or via the service container — never
instantiate them with `new`. The currency service is request-scoped; the blog service is
singleton-cached.

**Config override via database.** Use the `ConfigLoader` / `AppSetting` mechanism for runtime
configuration changes (mail drivers, currency rates, payment keys). Avoid reading `env()` directly
in package code; use `config('coderstm.*')` instead so overrides propagate correctly.

**Event-driven side effects.** Hook into subscription and payment lifecycle changes via the
existing event classes (`SubscriptionCreated`, `SubscriptionCancelled`, `RefundProcessed`, etc.)
rather than overriding model methods. This preserves the observer chain and integrates cleanly
with queue workers.

**Guard-aware helpers.** Always use the `user()`, `is_user()`, `is_admin()`, and `guard()` helpers
instead of `auth()->user()` directly — they handle the multi-guard context correctly and return
the right model type for the active guard.

## Key API Endpoints

| Purpose | Method | Endpoint |
|---|---|---|
| User/Admin signup | POST | `/auth/{guard?}/signup` |
| User/Admin login | POST | `/auth/{guard?}/login` |
| Get current user | POST | `/auth/{guard?}/me` |
| Request password reset | POST | `/auth/{guard?}/password/request` |
| Validate promo code | POST | `/subscriptions/check-promo-code` |
| Admin application stats | GET | `/admin/application/stats` |
| Admin settings | GET/POST | `/admin/application/settings` |
| List plans | GET | `/admin/plans` |
| Manage coupons | GET/POST | `/admin/coupons` |
| Customer management | GET | `/admin/customers` |
| Order management | GET | `/admin/orders` |
| Subscription management | GET | `/admin/subscriptions` |
| Payment methods config | GET/POST | `/admin/payment-methods` |
| Report export | GET | `/admin/reports/{type}` |
| Blog management | GET/POST | `/admin/blogs` |
| Payment webhooks | POST | `/webhooks/{provider}` |
| User wallet | GET | `/user/wallet` |
