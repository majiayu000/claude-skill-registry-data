---
name: generic-injection
description: Makes generic structs injectable by propagating type parameters through Provider and Injectable impls. Use when creating a generic repository, wrapper, or typed container that needs to be resolved from the DI container.
---

# Generic Injection

Generic structs and impl blocks are supported. Type params are propagated into
the generated `Provider` and `Injectable` impls.

## Generic struct (field injection)

```rust
use injectable::prelude::*;

// T must satisfy Injectable's bounds: Send + Sync + 'static
#[injectable]
struct Wrapper<T: Injectable + Send + Sync + 'static> {
    inner: Inject<T>,
}

// Resolve concrete specializations:
let w_db:    Wrapper<Database> = container.resolve().await?;
let w_cache: Wrapper<Cache>    = container.resolve().await?;
// Each is an independently managed singleton.
```

## Generic constructor injection

```rust
struct Repository<Entity: 'static + Send + Sync + Clone> {
    db: Arc<Database>,
    _phantom: std::marker::PhantomData<fn() -> Entity>,
}

#[injectable]
impl<Entity: 'static + Send + Sync + Clone> Repository<Entity> {
    #[injectable(ctor)]
    fn new(#[injectable(inject)] db: Arc<Database>) -> Self {
        Self { db, _phantom: std::marker::PhantomData }
    }
}

// Both specializations coexist and share the same Database singleton:
let user_repo:    Repository<UserEntity>    = container.resolve().await?;
let product_repo: Repository<ProductEntity> = container.resolve().await?;
```

## Consuming generic types as fields

Use `Arc<T>` (not `Inject<T>`) for generic injectable field types:

```rust
#[injectable]
struct App {
    #[injectable(inject)]
    user_repo: Arc<Repository<UserEntity>>,    // works via blanket Extract for Arc<T>
    #[injectable(inject)]
    order_repo: Arc<Repository<OrderEntity>>,
}
```

## Known limitation

`Inject<Wrapper<Database>>` as a field **does not work** — `InjectableArcFactory`
cannot be generated for generic types. Use `Arc<Wrapper<Database>>` instead.

## PhantomData pattern

```rust
struct TypedId<Marker: 'static + Send + Sync>(u64, std::marker::PhantomData<fn() -> Marker>);

#[injectable(factory)]
fn make_user_id(_db: Inject<Database>) -> TypedId<UserMarker> {
    TypedId(next_id(), std::marker::PhantomData)
}

#[injectable]
struct UserContext {
    #[injectable(inject(use_factory_async = self::make_user_id))]
    id: TypedId<UserMarker>,
}
```
