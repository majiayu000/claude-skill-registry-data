---
name: go-bootstrap
description: Wire a new clean-arch feature into the app — DI and route registration under internal/bootstrap/, internal/bootstrap/registry/, and cmd/api/main.go. Use when adding a feature's Setup() wiring, adding a repository/gateway accessor to the registry, or deciding whether new routes need Firebase auth, an internal API key, or no auth. Enforces the conventions below.
---

# Go Bootstrap & Dependency Injection

Authoritative description of the wiring layer that ties handler + usecase + repository
together for a feature, and the three places new wiring can land. Read this before adding a
new clean-arch feature end-to-end, or before touching route registration order in
`cmd/api/main.go`.

## When to use

- Adding `internal/bootstrap/{feature}/setup.go` for a new feature.
- Adding a new repository accessor to `internal/bootstrap/registry/registry.go`.
- Deciding which of the three `bootstrap.Setup*` entrypoints a new route belongs to.
- Touching `cmd/api/main.go` (logger/gin/middleware setup, legacy wiring).

## The pieces and how they fit

```
cmd/api/main.go
  run()
    configureLogger()                -> log.Logger
    setupGin(logger, db)              -> *gin.Engine, authentication.Authenticator
      health.Register                  (unauthenticated: /healthz, /readyz)
      r.GET("/ping")                    (unauthenticated)
      bootstrap.SetupInternalJobs        (own auth: x-api-key, under /jobs)
      bootstrap.SetupPublicComponents     (unauthenticated: webhooks, etc.)
      r.Use(authenticator.Authenticate())  <-- everything registered AFTER this needs a Firebase user_token
      r.Use(authentication.LazyProvisionUser(...))
    <legacy v1 wiring, inline>          (registered after auth -> protected)
    bootstrap.SetupCleanArchComponents(r, db, authenticator)
      -> {feature}.Setup(r, reg) per clean-arch feature:
           reg.Get{X}Repository()  ->  usecase.New{Entity}(...)  ->  api.New{Entity}V2Handlers(r, &svc)
```

## Non-negotiable rules

**`cmd/api/main.go`**
- Keep `run()` as orchestration only: load env, configure logger, init metrics, open the
  DB, call `setupGin`, wire legacy v1 (the existing inline calls — don't add to this, it's
  migration debt), call `bootstrap.SetupCleanArchComponents`, start the server.
- Pull any standalone concern into its own top-level function (`configureLogger`,
  `setupGin`, `ping`) instead of growing `run()`. `setupGin` itself owns: engine creation,
  recovery/logging/metrics/CORS middleware, health checks, `/ping`, internal jobs, public
  components, then the auth middleware — in that order.
- **Route registration order inside `setupGin` decides auth.** Anything registered before
  `r.Use(authenticator.Authenticate())` is unauthenticated by default (health, `/ping`,
  jobs, public webhooks); anything after is Firebase-protected. Never reorder these calls
  without checking which routes you're exposing or locking down.

**The three `bootstrap.Setup*` entrypoints (`internal/bootstrap/setup.go`)**
- `SetupInternalJobs(r, db)` — routes under `/jobs`, protected by
  `authentication.InternalAPIKeyAuth()` (the `x-api-key` header), not Firebase. Add a new
  job by calling `{feature}.SetupJobs(jobsGroup, reg)` here; the group's middleware already
  covers it.
- `SetupPublicComponents(r, db, auth)` — genuinely unauthenticated routes (payment-provider
  webhooks, etc.), called *before* the global Firebase middleware exists. If one of its
  routes still needs auth (e.g. a subscription endpoint mixed into an otherwise-public
  group), apply it explicitly in that feature's own `Setup()` — e.g.
  `api.NewSubscriptionHandlers(r, uc, authenticator.Authenticate())` — don't rely on global
  middleware here, it isn't attached yet.
- `SetupCleanArchComponents(r, db, auth)` — every authenticated clean-arch feature. Add your
  new feature's `{feature}.Setup(r, reg)` call here.
- Each of the three entrypoints creates its **own** `registry.NewRegistry(db)` — they don't
  share one instance, so a repository built for jobs and the same repository built for
  clean-arch components are separate Go values (harmless: both just wrap the same
  `*gorm.DB`).
- The import list in `setup.go` is alphabetical (gofumpt/goimports-enforced); the call
  order inside each `Setup*` function body has no enforced order — append new calls at the
  end.

**`internal/bootstrap/registry/registry.go`**
- One unexported pointer field + one `Get{X}Repository()` method per repository, always
  following the lazy nil-check-then-construct pattern:
  ```go
  func (r *Registry) Get{X}Repository() *repository.{X}Repository {
      if r.{x}Repository == nil {
          r.{x}Repository = repository.New{X}Repository(r.db)
      }
      return r.{x}Repository
  }
  ```
- `Registry` is a **process-lifetime singleton**, built once per `Setup*` entrypoint call —
  not per-request. Never stash per-request state on it; request-scoped data (like
  `user_id`) flows through `ctx`, not the registry.
- When a dependency composes other repositories (see `GetPlanLimitsValidator`, which needs
  the wallet/credit-card/movement/recurrent repos), build it by calling the other `Get*`
  methods — never reach into another field directly — so those dependencies stay lazily
  initialized too.
- External gateways/HTTP clients (Stripe, MercadoPago, Firebase, Expo push) are **not**
  registry-backed — they're stateless clients constructed directly inside the feature's
  `Setup()` (`gateway.NewStripeGateway()`, `push.NewExpoClient()`), never memoized on the
  registry.

**`internal/bootstrap/{feature}/setup.go`**
- `package {feature}`, one exported `Setup(r *gin.Engine, registry *registry.Registry)` (or
  `SetupJobs(jobsGroup *gin.RouterGroup, registry *registry.Registry)` for a job-only
  feature). The parameter is named `registry`, shadowing the imported package — that's
  intentional; only the type is needed in the signature, and methods are called on the
  parameter throughout the body.
- Body shape: pull every dependency from the registry (or construct a gateway/client
  inline), build the usecase(s) — innermost dependency first when one usecase depends on
  another (see `invoiceService` built before `movementService` in
  `internal/bootstrap/movement/setup.go`) — then call the handler constructor.
- If the usecase's methods use pointer receivers, take the address when passing it on:
  `movementService := usecase.NewMovement(...); api.NewMovementV2Handlers(r,
  &movementService)`. Match whatever `usecase.New{Entity}` actually returns (value vs
  pointer use — see the `go-usecases` skill).
- Wire the new `{feature}.Setup` call into `internal/bootstrap/setup.go` — either
  `SetupCleanArchComponents` (normal case) or `SetupInternalJobs` (job-only feature, calling
  `SetupJobs` instead).

## Adding a brand-new feature, end to end

1. `internal/infrastructure/repository/{feature}_repository.go` + model + `FromDomain`/`ToDomain`.
2. `internal/usecase/{feature}_usecase.go` — see the `go-usecases` skill.
3. `internal/infrastructure/api/{feature}_api.go` — see the `go-api-handlers` skill.
4. Add a `{feature}Repository *repository.{Feature}Repository` field + `Get{Feature}Repository()` to `registry.go`.
5. `internal/bootstrap/{feature}/setup.go` with `Setup(r, reg)`, following the shape above.
6. Add the import + `{feature}.Setup(r, reg)` call to `SetupCleanArchComponents` in `internal/bootstrap/setup.go`.

## Anti-patterns (reject these)

| Don't | Do |
|---|---|
| Add a new feature's wiring inline in `cmd/api/main.go`'s `run()` | Create `internal/bootstrap/{feature}/setup.go` and call it from `SetupCleanArchComponents` |
| Register a new authenticated route before `r.Use(authenticator.Authenticate())` inside `setupGin` | Register it via `SetupCleanArchComponents`, which runs after the auth middleware is attached |
| Add a repository field to `Registry` without the matching nil-check lazy getter | Always pair the field with a `Get{X}Repository()` that checks-then-constructs |
| Reach into another field directly inside a composite `Get*` (e.g. `r.walletRepository` instead of `r.GetWalletRepository()`) | Call the other `Get*` method so that dependency also gets lazily initialized |
| Memoize an external gateway/HTTP client on the `Registry` | Construct it directly in the feature's `Setup()` — gateways aren't registry-backed |
| Store request-scoped data (user ID, request context) on the `Registry` | Keep the registry process-lifetime; pass request data through `ctx` |

## Run & verify

```bash
go build ./...
make linter
go run ./cmd/api/main.go   # confirm the app boots and the new route responds as expected
```
