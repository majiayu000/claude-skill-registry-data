---
name: rust-backend-api
description: Provides API design patterns for Rust backends including request validation with validator, OpenAPI documentation with utoipa, and SwaggerUI integration. Use when building REST APIs with Axum, adding request validation, generating OpenAPI specs, or setting up API documentation.
---

<objective>
Enable production-quality REST API development with type-safe request validation, automatic OpenAPI documentation, and interactive API exploration.
</objective>

<essential_principles>
1. **Validation at the Edge** - Validate all external input immediately.
2. **Code-First OpenAPI** - Documentation lives in the code via derive macros.
3. **Schema as Contract** - ToSchema-derived types define the API contract.
</essential_principles>

<patterns>
<pattern name="validation">
**Request Validation**

```rust
use validator::Validate;

#[derive(Debug, Deserialize, Validate, ToSchema)]
pub struct CreateUserRequest {
    #[validate(email)]
    #[schema(example = "user@example.com")]
    pub email: String,

    #[validate(length(min = 8, max = 64))]
    pub password: String,

    #[validate(length(min = 1, max = 100))]
    #[schema(example = "Jane Doe")]
    pub name: String,
}

pub async fn create_user(
    State(state): State<AppState>,
    Json(req): Json<CreateUserRequest>,
) -> Result<Json<UserResponse>, AppError> {
    req.validate()?;
    // ...
}
```
</pattern>

<pattern name="openapi">
**OpenAPI with utoipa**

```rust
#[utoipa::path(
    post,
    path = "/users",
    tag = "users",
    request_body = CreateUserRequest,
    responses(
        (status = 201, description = "User created", body = UserResponse),
        (status = 400, description = "Validation error")
    )
)]
pub async fn create_user(/* ... */) { }

#[derive(OpenApi)]
#[openapi(
    info(title = "My API", version = "1.0.0"),
    tags((name = "users", description = "User management"))
)]
struct ApiDoc;

pub fn create_router(state: AppState) -> Router {
    let (router, api) = OpenApiRouter::with_openapi(ApiDoc::openapi())
        .routes(routes!(create_user))
        .split_for_parts();

    router
        .merge(SwaggerUi::new("/swagger-ui").url("/api-docs/openapi.json", api))
        .with_state(state)
}
```
</pattern>
</patterns>

<success_criteria>
- [ ] All request types derive Validate with constraints
- [ ] Validation errors return 400 with field-specific messages
- [ ] All endpoints have #[utoipa::path] documentation
- [ ] SwaggerUI accessible and shows all endpoints
- [ ] OpenAPI spec includes security schemes if using auth
</success_criteria>
