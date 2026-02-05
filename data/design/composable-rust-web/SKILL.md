---
name: composable-rust-web
description: Expert knowledge for building web APIs and real-time applications with Composable Rust. Use when building HTTP REST APIs with Axum, implementing WebSocket for real-time updates, working with authentication (magic link, OAuth, passkeys), setting up email providers (SMTP, Console), designing API routes or request handlers, or questions about web integration and real-time communication.
---

# Composable Rust Web Integration Expert

Expert knowledge for building web APIs and real-time applications with Composable Rust - HTTP/WebSocket patterns, authentication framework, action broadcasting, email providers, and client integration.

## When to Use This Skill

Automatically apply when:
- Building HTTP REST APIs with Axum
- Implementing WebSocket for real-time updates
- Working with authentication (magic link, OAuth, passkeys)
- Setting up email providers (SMTP, Console)
- Designing API routes or request handlers
- Questions about web integration, real-time communication, or auth

## HTTP API Pattern with Axum

### Basic Router Setup

```rust
use axum::{
    Router,
    routing::{get, post},
    extract::State,
    Json,
};

pub fn create_router(store: AppStore) -> Router {
    Router::new()
        .route("/health", get(health_check))
        .route("/api/v1/orders", post(create_order))
        .route("/api/v1/orders/:id", get(get_order))
        .with_state(store)
}

async fn health_check() -> &'static str {
    "OK"
}
```

**Pattern**: Share store via `State`. Use versioned routes (`/api/v1/`). Include health check.

### Request Handler Pattern

```rust
#[derive(Debug, Deserialize)]
pub struct CreateOrderRequest {
    pub customer_id: String,
    pub items: Vec<Item>,
}

#[derive(Debug, Serialize)]
pub struct CreateOrderResponse {
    pub order_id: String,
    pub status: String,
}

async fn create_order(
    State(store): State<Arc<Store<OrderState, OrderAction, OrderEnvironment, OrderReducer>>>,
    Json(request): Json<CreateOrderRequest>,
) -> Result<Json<CreateOrderResponse>, ApiError> {
    // Convert request to action
    let action = OrderAction::PlaceOrder {
        customer_id: request.customer_id,
        items: request.items,
    };

    // Send action to store and wait for result
    let result = store
        .send_and_wait_for(
            action,
            |action| matches!(action, OrderAction::OrderPlaced { .. }),
            Duration::from_secs(5),
        )
        .await?;

    // Extract result
    let order_id = match result {
        OrderAction::OrderPlaced { order_id, .. } => order_id,
        _ => return Err(ApiError::UnexpectedResponse),
    };

    Ok(Json(CreateOrderResponse {
        order_id,
        status: "placed".to_string(),
    }))
}
```

**Pattern**:
1. Deserialize request to DTO
2. Convert DTO to Action
3. Use `send_and_wait_for` for request-response
4. Extract result from action
5. Serialize response DTO

### Error Handling Pattern

```rust
#[derive(Debug)]
pub enum ApiError {
    NotFound,
    BadRequest(String),
    InternalServerError(String),
    Timeout,
}

impl IntoResponse for ApiError {
    fn into_response(self) -> Response {
        let (status, message) = match self {
            ApiError::NotFound => (StatusCode::NOT_FOUND, "Not found"),
            ApiError::BadRequest(msg) => (StatusCode::BAD_REQUEST, msg.leak()),
            ApiError::InternalServerError(msg) => {
                tracing::error!("Internal server error: {}", msg);
                (StatusCode::INTERNAL_SERVER_ERROR, "Internal server error")
            }
            ApiError::Timeout => (StatusCode::REQUEST_TIMEOUT, "Request timeout"),
        };

        (status, message).into_response()
    }
}

// Conversion from domain errors
impl From<DomainError> for ApiError {
    fn from(err: DomainError) -> Self {
        match err {
            DomainError::NotFound => ApiError::NotFound,
            DomainError::ValidationError(msg) => ApiError::BadRequest(msg),
            _ => ApiError::InternalServerError(err.to_string()),
        }
    }
}
```

**Pattern**: Define API-specific error type. Implement `IntoResponse`. Convert domain errors. Log internal errors.

## WebSocket Pattern (Real-Time Updates)

### WebSocket Handler Setup

```rust
use axum::extract::ws::{WebSocket, WebSocketUpgrade};
use tokio::sync::broadcast;

pub fn create_router_with_websocket(
    store: AppStore,
    action_tx: broadcast::Sender<Action>,
) -> Router {
    Router::new()
        .route("/ws", get(websocket_handler))
        .with_state((store, action_tx))
}

async fn websocket_handler(
    ws: WebSocketUpgrade,
    State((store, action_tx)): State<(AppStore, broadcast::Sender<Action>)>,
) -> impl IntoResponse {
    ws.on_upgrade(|socket| handle_socket(socket, store, action_tx))
}
```

**Pattern**: Use `broadcast` channel for action broadcasting. Share both store and channel.

### Message Protocol (JSON Envelope)

WebSocket messages use a tagged envelope format with a `type` field:

**Message Types:**

| Type      | Direction       | Purpose                |
|-----------|-----------------|------------------------|
| `command` | Client → Server | Execute an action      |
| `event`   | Server → Client | Broadcast an action    |
| `error`   | Server → Client | Error occurred         |
| `ping`    | Bidirectional   | Keep connection alive  |
| `pong`    | Bidirectional   | Respond to ping        |

**Command (Client → Server):**

```json
{
  "type": "command",
  "action": {
    "PlaceOrder": {
      "customer_id": "cust-123",
      "items": [{"product_id": "prod-1", "quantity": 2}]
    }
  }
}
```

**Event (Server → Client):**

```json
{
  "type": "event",
  "action": {
    "OrderPlaced": {
      "order_id": "ord-456",
      "customer_id": "cust-123",
      "status": "pending"
    }
  }
}
```

**Error (Server → Client):**

```json
{
  "type": "error",
  "message": "Invalid action format: missing customer_id"
}
```

**Keep-Alive (Bidirectional):**

```json
{"type": "ping"}
{"type": "pong"}
```

**Important**: Clients receive events for ALL actions from effects, not just their own commands.

### Socket Handler Pattern

```rust
async fn handle_socket(
    mut socket: WebSocket,
    store: AppStore,
    action_tx: broadcast::Sender<Action>,
) {
    let mut action_rx = action_tx.subscribe();

    // Spawn task to broadcast actions to this client
    let mut send_task = tokio::spawn(async move {
        while let Ok(action) = action_rx.recv().await {
            // Filter actions to send (optional)
            if should_broadcast(&action) {
                let message = serde_json::to_string(&action).unwrap();
                if socket.send(Message::Text(message)).await.is_err() {
                    break;
                }
            }
        }
    });

    // Spawn task to receive messages from client
    let mut recv_task = tokio::spawn(async move {
        while let Some(Ok(Message::Text(text))) = socket.recv().await {
            if let Ok(action) = serde_json::from_str::<Action>(&text) {
                // Client sent action, send to store
                let _ = store.send(action).await;
            }
        }
    });

    // Wait for either task to finish
    tokio::select! {
        _ = (&mut send_task) => recv_task.abort(),
        _ = (&mut recv_task) => send_task.abort(),
    }
}
```

**Pattern**:
1. Subscribe to action broadcast
2. Spawn send task (broadcasts actions to client)
3. Spawn receive task (receives actions from client)
4. Use `tokio::select!` to handle disconnection

### Action Broadcasting Pattern

In your Store, broadcast actions after executing effects:

```rust
pub async fn send(&self, action: Action) {
    // Reduce
    let effects = self.reducer.reduce(&mut state, action.clone(), &self.env);

    // Broadcast action to WebSocket clients
    let _ = self.action_tx.send(action);

    // Execute effects
    for effect in effects {
        self.execute_effect(effect).await;
    }
}
```

**Pattern**: Broadcast action before or after reducing (depending on needs). Ignore send errors (no subscribers OK).

### Streaming Actions via WebSocket (Phase 8)

`Effect::Stream` automatically broadcasts each streamed action to WebSocket clients:

```rust
// In your reducer
fn reduce(...) -> SmallVec<[Effect<Action>; 4]> {
    match action {
        Action::StartLlmGeneration { prompt } => {
            // Stream LLM tokens as they arrive
            let effect = Effect::Stream(Box::pin(async_stream::stream! {
                let mut response_stream = env.llm_client.messages_stream(prompt).await?;

                while let Some(chunk) = response_stream.next().await {
                    // Each yield is automatically broadcast to WebSocket clients
                    yield Action::LlmChunk {
                        content: chunk?.delta.text
                    };
                }

                yield Action::LlmComplete;
            }));

            smallvec![effect]
        }
        // ...
    }
}
```

**Result**: WebSocket clients receive `LlmChunk` actions in real-time as tokens arrive.

**Use cases**:
- LLM token streaming (ChatGPT-style UX)
- Progress updates from long-running operations
- Multi-step workflow status broadcasts
- Real-time data feed processing

### Client Integration (React Example)

```typescript
// useWebSocket hook
function useWebSocket(url: string) {
  const [actions, setActions] = useState<Action[]>([]);
  const ws = useRef<WebSocket | null>(null);

  useEffect(() => {
    ws.current = new WebSocket(url);

    ws.current.onmessage = (event) => {
      const action = JSON.parse(event.data);
      setActions((prev) => [...prev, action]);
    };

    return () => ws.current?.close();
  }, [url]);

  const sendAction = (action: Action) => {
    ws.current?.send(JSON.stringify(action));
  };

  return { actions, sendAction };
}

// Usage in component
function OrderList() {
  const { actions, sendAction } = useWebSocket('ws://localhost:3000/ws');

  // Filter order actions
  const orderActions = actions.filter(
    (a) => a.type === 'OrderPlaced' || a.type === 'OrderUpdated'
  );

  return (
    <div>
      {orderActions.map((action) => (
        <div key={action.order_id}>{/* Render order */}</div>
      ))}
    </div>
  );
}
```

**Pattern**: Single WebSocket connection. Filter actions client-side. Update local state on action received.

### Filtering Actions for Broadcast

```rust
fn should_broadcast(action: &OrderAction) -> bool {
    match action {
        // Broadcast external-facing events
        OrderAction::OrderPlaced { .. } => true,
        OrderAction::OrderCancelled { .. } => true,

        // Don't broadcast internal actions
        OrderAction::InternalStateUpdate { .. } => false,

        _ => true,
    }
}
```

**Pattern**: Only broadcast actions that clients care about. Reduces bandwidth and client processing.

## Authentication Framework

### Auth Crate Integration

```rust
use composable_rust_auth::{
    AuthConfig, AuthStore, MagicLinkProvider, SmtpEmailProvider,
};

// Setup auth store
let email_provider = SmtpEmailProvider::new(smtp_config)?;
let auth_config = AuthConfig::builder()
    .magic_link_enabled(true)
    .oauth_providers(vec!["google", "github"])
    .build();

let auth_store = AuthStore::new(
    AuthState::default(),
    AuthReducer::new(auth_config),
    AuthEnvironment {
        database: postgres_db,
        email_provider,
        clock: SystemClock,
    },
);

// Add auth routes
let app = Router::new()
    .merge(auth_routes(auth_store.clone()))
    .route("/api/v1/protected", get(protected_handler))
    .layer(AuthLayer::new(auth_store.clone()));
```

### Auth Routes Pattern

```rust
pub fn auth_routes(auth_store: AuthStore) -> Router {
    Router::new()
        .route("/auth/magic-link/request", post(request_magic_link))
        .route("/auth/magic-link/verify", post(verify_magic_link))
        .route("/auth/oauth/:provider", get(oauth_redirect))
        .route("/auth/oauth/:provider/callback", get(oauth_callback))
        .route("/auth/logout", post(logout))
        .with_state(auth_store)
}

#[derive(Deserialize)]
struct MagicLinkRequest {
    email: String,
}

async fn request_magic_link(
    State(auth_store): State<AuthStore>,
    Json(req): Json<MagicLinkRequest>,
) -> Result<StatusCode, ApiError> {
    auth_store
        .send(AuthAction::RequestMagicLink { email: req.email })
        .await?;

    Ok(StatusCode::OK)
}
```

### Protected Route Pattern

```rust
use axum::middleware::from_fn_with_state;

async fn auth_middleware(
    State(auth_store): State<AuthStore>,
    mut request: Request<Body>,
    next: Next,
) -> Result<Response, ApiError> {
    // Extract token from Authorization header
    let token = request
        .headers()
        .get(AUTHORIZATION)
        .and_then(|h| h.to_str().ok())
        .and_then(|s| s.strip_prefix("Bearer "))
        .ok_or(ApiError::Unauthorized)?;

    // Verify token
    let user_id = auth_store
        .send_and_wait_for(
            AuthAction::VerifyToken { token: token.to_string() },
            |action| matches!(action, AuthAction::TokenVerified { .. }),
            Duration::from_secs(2),
        )
        .await?;

    // Add user_id to request extensions
    request.extensions_mut().insert(user_id);

    Ok(next.run(request).await)
}

// Protected handler
async fn protected_handler(
    Extension(user_id): Extension<UserId>,
) -> Result<String, ApiError> {
    Ok(format!("Hello, user {}", user_id))
}
```

**Pattern**: Middleware extracts token. Verifies via auth store. Adds user ID to extensions. Handler extracts user ID.

### Magic Link Flow

```
1. Client → POST /auth/magic-link/request { email }
2. Server → Send email with link containing token
3. Client → GET /auth/magic-link/verify?token=xxx
4. Server → Verify token, return session
5. Client → Store session, use for authenticated requests
```

### OAuth Flow

```
1. Client → GET /auth/oauth/google
2. Server → Redirect to Google OAuth
3. User → Authorizes on Google
4. Google → Redirect to /auth/oauth/google/callback?code=xxx
5. Server → Exchange code for tokens, create session, redirect to app
6. Client → Extract session, use for authenticated requests
```

## Email Providers

### SMTP Provider Pattern

```rust
use composable_rust_email::{EmailProvider, SmtpEmailProvider, Email};

let smtp_provider = SmtpEmailProvider::builder()
    .host("smtp.gmail.com")
    .port(587)
    .username(env::var("SMTP_USERNAME")?)
    .password(env::var("SMTP_PASSWORD")?)
    .from_email("noreply@example.com")
    .from_name("Example App")
    .build()?;

// Send email via effect
vec![Effect::SendEmail {
    provider: smtp_provider,
    email: Email {
        to: "user@example.com".to_string(),
        subject: "Magic link".to_string(),
        body: format!("Click here: {}", magic_link_url),
    },
}]
```

### Console Provider Pattern (Development)

```rust
use composable_rust_email::ConsoleEmailProvider;

let console_provider = ConsoleEmailProvider::new();

// Prints email to console instead of sending
// Useful for local development
```

### Email in Reducer Pattern

```rust
fn reduce(&self, state: &mut State, action: Action, env: &Env) -> Vec<Effect> {
    match action {
        AuthAction::RequestMagicLink { email } => {
            // Generate token
            let token = generate_token();
            let magic_link = format!("https://app.com/auth/verify?token={}", token);

            // Store token
            state.pending_tokens.insert(token.clone(), email.clone());

            // Send email
            vec![Effect::SendEmail {
                email: Email {
                    to: email,
                    subject: "Your magic link".to_string(),
                    body: format!("Click here to sign in: {}", magic_link),
                },
            }]
        }
        _ => vec![Effect::None],
    }
}
```

**Pattern**: Generate token in reducer (deterministic). Store in state. Return `Effect::SendEmail`.

## CORS and Middleware

### CORS Setup

```rust
use tower_http::cors::{CorsLayer, Any};

let cors = CorsLayer::new()
    .allow_origin(Any)  // For development
    .allow_methods([Method::GET, Method::POST, Method::PUT, Method::DELETE])
    .allow_headers([CONTENT_TYPE, AUTHORIZATION]);

let app = Router::new()
    .route("/api/v1/orders", post(create_order))
    .layer(cors);
```

**Production**: Use `.allow_origin(Origin::exact("https://app.com"))` instead of `Any`.

### Logging Middleware

```rust
use tower_http::trace::TraceLayer;

let app = Router::new()
    .route("/api/v1/orders", post(create_order))
    .layer(TraceLayer::new_for_http());
```

## Request-Response Pattern

### send_and_wait_for

Most common pattern for HTTP handlers:

```rust
async fn handler(
    State(store): State<AppStore>,
    Json(req): Json<CreateRequest>,
) -> Result<Json<Response>, ApiError> {
    let action = Action::from_request(req);

    // Wait for specific response action
    let result = store
        .send_and_wait_for(
            action,
            |action| matches!(action, Action::Success { .. }),
            Duration::from_secs(5),
        )
        .await?;

    Ok(Json(Response::from_action(result)))
}
```

**Pattern**: Send action. Wait for result action matching predicate. Timeout after duration.

### Async Effect with Callback

Alternative: Use effect that returns result action:

```rust
use composable_rust_core::async_effect;

fn reduce(...) -> Vec<Effect> {
    vec![async_effect! {
        let result = database.save(&data).await?;

        // Return action with result
        Some(Action::SaveComplete {
            success: true,
            id: result.id,
        })
    }]
}
```

**Pattern**: Effect returns `Option<Action>`. Store feeds it back into reducer.

## Security Patterns

### Input Validation

```rust
#[derive(Deserialize)]
struct CreateOrderRequest {
    #[serde(deserialize_with = "validate_email")]
    customer_email: String,

    #[serde(deserialize_with = "validate_items")]
    items: Vec<Item>,
}

fn validate_email<'de, D>(deserializer: D) -> Result<String, D::Error>
where
    D: Deserializer<'de>,
{
    let email = String::deserialize(deserializer)?;
    if email.contains('@') && email.len() > 3 {
        Ok(email)
    } else {
        Err(serde::de::Error::custom("Invalid email"))
    }
}
```

**Pattern**: Validate during deserialization. Reject invalid data early.

### Rate Limiting

```rust
use tower_governor::{governor::GovernorConfigBuilder, GovernorLayer};

let governor_conf = GovernorConfigBuilder::default()
    .per_second(10)  // 10 requests per second
    .burst_size(20)  // Allow burst of 20
    .finish()
    .unwrap();

let app = Router::new()
    .route("/api/v1/orders", post(create_order))
    .layer(GovernorLayer { config: governor_conf });
```

### SQL Injection Prevention

Always use parameterized queries via sqlx:

```rust
// ✅ SAFE - Parameterized query
sqlx::query("SELECT * FROM orders WHERE customer_id = $1")
    .bind(&customer_id)
    .fetch_all(&pool)
    .await?;

// ❌ UNSAFE - String interpolation
sqlx::query(&format!("SELECT * FROM orders WHERE customer_id = '{}'", customer_id))
    .fetch_all(&pool)
    .await?;
```

## Common Anti-Patterns to Avoid

### ❌ Anti-Pattern 1: Blocking Operations in Handlers

```rust
// ❌ Synchronous blocking call
async fn handler(State(store): State<AppStore>) -> Result<Response, Error> {
    std::thread::sleep(Duration::from_secs(5));  // ❌ Blocks executor
}
```

**Solution**: Use async operations. If sync needed, use `spawn_blocking`.

### ❌ Anti-Pattern 2: Not Using send_and_wait_for

```rust
// ❌ Fire-and-forget, no result
async fn create_order(State(store): State<AppStore>, Json(req): Json<Request>) -> Response {
    store.send(Action::Create { ... }).await;
    // ❌ No way to know if it succeeded
    Response::new("OK".into())
}
```

**Solution**: Use `send_and_wait_for` to get result.

### ❌ Anti-Pattern 3: Broadcasting All Actions

```rust
// ❌ Broadcasting internal state updates
self.action_tx.send(Action::InternalDebugLog { ... });
```

**Solution**: Filter actions before broadcasting.

### ❌ Anti-Pattern 4: Mixing Business Logic in Handlers

```rust
// ❌ Business logic in handler
async fn create_order(State(store): State<AppStore>, Json(req): Json<Request>) -> Response {
    // ❌ Validation, calculation in handler
    if req.items.is_empty() {
        return Response::error("No items");
    }
    let total = req.items.iter().map(|i| i.price).sum();

    // Then send to store
}
```

**Solution**: Put all business logic in reducer. Handler only translates HTTP ↔ Actions.

### ❌ Anti-Pattern 5: Not Handling WebSocket Disconnects

```rust
// ❌ No error handling
while let Some(Ok(msg)) = socket.recv().await {
    // Process message
}  // ❌ Loop exits silently on error
```

**Solution**: Log disconnects, clean up resources.

## Testing Patterns

### Unit Test: Request Handler Logic

```rust
#[tokio::test]
async fn test_create_order_success() {
    let store = test_store();

    let request = CreateOrderRequest {
        customer_id: "cust-123".to_string(),
        items: vec![test_item()],
    };

    let response = create_order(State(store), Json(request)).await.unwrap();

    assert_eq!(response.status, "placed");
    assert!(response.order_id.starts_with("order-"));
}
```

### Integration Test: HTTP API

```rust
#[tokio::test]
async fn test_http_api() {
    let app = create_router(test_store());
    let server = TestServer::new(app).unwrap();

    let response = server
        .post("/api/v1/orders")
        .json(&json!({
            "customer_id": "cust-123",
            "items": [{"id": "item-1", "quantity": 2}]
        }))
        .await;

    assert_eq!(response.status(), StatusCode::OK);

    let body: CreateOrderResponse = response.json().await;
    assert!(!body.order_id.is_empty());
}
```

### Integration Test: WebSocket

```rust
#[tokio::test]
async fn test_websocket_broadcast() {
    let (action_tx, _) = broadcast::channel(100);
    let app = create_router_with_websocket(test_store(), action_tx.clone());

    let mut client = test_websocket_client(app).await;

    // Send action via broadcast
    action_tx.send(OrderAction::OrderPlaced { order_id: "123".to_string() }).unwrap();

    // Receive action on client
    let message = client.recv().await.unwrap();
    let action: OrderAction = serde_json::from_str(&message).unwrap();

    assert!(matches!(action, OrderAction::OrderPlaced { .. }));
}
```

## Performance Considerations

- **WebSocket connections**: ~1MB RAM per connection, scale to 10k+ per instance
- **HTTP throughput**: Axum handles 100k+ req/sec on modern hardware
- **Action broadcasting**: `broadcast` channel is efficient, low overhead
- **send_and_wait_for latency**: Adds ~1-10ms depending on reducer complexity

## Quick Reference Checklist

When building web APIs:

- [ ] **Versioned routes**: Use `/api/v1/` prefix
- [ ] **Health check**: Include `/health` endpoint
- [ ] **Error handling**: Convert domain errors to HTTP errors
- [ ] **CORS**: Configure for production
- [ ] **Authentication**: Use middleware for protected routes
- [ ] **Rate limiting**: Protect against abuse
- [ ] **Input validation**: Validate in deserialization or reducer
- [ ] **WebSocket filtering**: Only broadcast relevant actions
- [ ] **Logging**: Use TraceLayer for request logging
- [ ] **Timeouts**: Use `send_and_wait_for` with reasonable timeout

## See Also

- **Architecture**: `composable-rust-architecture.skill` - Core patterns
- **Authentication**: `docs/authentication.md` - Complete auth guide
- **WebSocket**: `docs/websocket.md` - WebSocket patterns
- **Email**: `docs/email-providers.md` - Email setup

---

**Remember**: HTTP handlers translate between HTTP and Actions. Business logic stays in reducers. WebSocket broadcasts actions to connected clients. Authentication via middleware.
