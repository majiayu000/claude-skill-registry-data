---
name: nockapp-api-design
description: Design new API endpoints following the Hoon-Rust-HTTP pattern used in this NockApp. Use when adding endpoints, modifying SNARK structure, extending the API, or implementing new features.
---

# NockApp API Design Pattern

This skill guides you through adding new API endpoints to the prover NockApp following the established architectural pattern.

## The 4-Step Pattern

Every new API endpoint requires changes in 4 places, in this order:

### Step 1: Update Hoon Kernel Types

**File**: `prover/hoon/prover.hoon`

Add your new operation to the `$cause` type:

```hoon
+$  cause
  $%  [%init ~]
      [%submit-snark proof=tape verification-key=tape public-inputs=tape proof-system=tape submitter=tape]
      [%get-snark id=@ud]
      [%list-snarks ~]
      [%delete-snark id=@ud]
      [%update-status id=@ud new-status=tape]
      ::  Add your new operation here
      [%your-new-operation field1=@ud field2=tape]
  ==
```

**Type Guidelines**:
- `@ud`: Unsigned decimal (numbers, IDs)
- `tape`: String/text data
- `~`: Null/unit (no data)
- `(list ...)`: List of items
- `(map ...)`: Key-value pairs

### Step 2: Implement Handler in `++poke` Arm

Add your handler logic inside the `++poke` arm:

```hoon
++  poke
  |=  [=cause =bowl:cask]
  ^-  [(list effect:cask) _this]
  ?-  -.cause
    %init
      ...
    %submit-snark
      ...
    ::  Add your handler here
    %your-new-operation
      =/  field1  field1.cause
      =/  field2  field2.cause
      ::  Validate inputs
      ?:  =(field1 0)
        :_  this
        [%http-response (error-response "Field1 cannot be zero")]~
      ::  Update state
      =/  new-state  ...
      ::  Return response
      :_  this(state new-state)
      [%http-response (success-response "Operation completed")]~
  ==
```

**Common Patterns**:
- Access input: `field.cause`
- Update state: `this(state new-state)`
- Return with HTTP response: `:_  this  [%http-response ...]~`
- Error handling: Check conditions with `?:` and return error responses

### Step 3: Add Rust HTTP Handler

**File**: `prover/src/main.rs`

#### 3a. Define Request/Response Structs

```rust
#[derive(Deserialize)]
struct YourNewOperationRequest {
    field1: u64,
    field2: String,
}

#[derive(Serialize)]
struct YourNewOperationResponse {
    success: bool,
    message: String,
    data: Option<YourData>,
}
```

#### 3b. Implement Handler Function

```rust
async fn handle_your_new_operation(
    State(kernel): State<Arc<RwLock<Kernel>>>,
    Json(payload): Json<YourNewOperationRequest>,
) -> Result<Json<YourNewOperationResponse>, StatusCode> {
    // Validate input
    if payload.field1 == 0 {
        return Err(StatusCode::BAD_REQUEST);
    }

    // Build noun message for Hoon kernel
    let message = format!(
        "[%your-new-operation {} '{}']",
        payload.field1,
        payload.field2
    );

    // Send to kernel
    let mut kernel_guard = kernel.write().await;
    let response_noun = kernel_guard.poke(&message)?;

    // Parse response (simplified)
    let response = YourNewOperationResponse {
        success: true,
        message: "Operation completed".to_string(),
        data: Some(parse_response(&response_noun)),
    };

    Ok(Json(response))
}
```

#### 3c. Add Route to Router

In the `main()` function, add your route:

```rust
let app = Router::new()
    .route("/api/v1/snark", post(submit_snark))
    .route("/api/v1/snark/:id", get(get_snark))
    .route("/api/v1/snarks", get(list_snarks))
    .route("/api/v1/snark/:id", delete(delete_snark))
    // Add your new route
    .route("/api/v1/your-endpoint", post(handle_your_new_operation))
    .with_state(kernel)
    .layer(cors);
```

### Step 4: Update Frontend (if needed)

**File**: `prover/web/prover.js`

Add JavaScript to call your new endpoint:

```javascript
async function callYourNewOperation(field1, field2) {
    try {
        const response = await fetch('/api/v1/your-endpoint', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                field1: field1,
                field2: field2
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        console.log('Success:', data);
        return data;
    } catch (error) {
        console.error('Error:', error);
        showError(error.message);
    }
}
```

## Detailed Examples

For complete working examples, see [PATTERNS.md](PATTERNS.md).

## Rebuilding After Changes

After modifying the code:

```bash
# 1. Recompile Hoon kernel to Nock
hoonc prover/hoon/prover.hoon -o prover/out.jam

# 2. Rebuild Rust binary
cargo build --release

# 3. Restart server
RUST_LOG=debug cargo run
```

## Common Pitfalls

1. **Type Mismatches**: Ensure Hoon types match Rust deserialization
2. **Noun Formatting**: Check noun message format carefully (brackets, spaces)
3. **State Updates**: Remember to return updated state in Hoon with `this(state ...)`
4. **Error Handling**: Always validate inputs in both Rust and Hoon
5. **Base64 Data**: For binary data, validate base64 encoding in Rust before sending to Hoon

## Testing Your New Endpoint

```bash
# Test with curl
curl -X POST http://localhost:8080/api/v1/your-endpoint \
  -H "Content-Type: application/json" \
  -d '{
    "field1": 42,
    "field2": "test data"
  }'

# Check server logs
RUST_LOG=debug cargo run
```

## State Management Best Practices

- **Immutable Updates**: Always create new state, don't mutate
- **Validation First**: Validate all inputs before updating state
- **Atomic Operations**: Keep state updates atomic within a single poke
- **ID Generation**: Use `next-id` pattern for generating unique IDs
- **Timestamps**: Use `now.bowl` from the bowl for consistent timestamps

## Response Format Guidelines

**Success Response**:
```json
{
  "success": true,
  "data": {...}
}
```

**Error Response**:
```json
{
  "error": "Descriptive error message"
}
```

## Performance Considerations

- **Async Handlers**: All Rust handlers should be async
- **Lock Duration**: Minimize time holding kernel write lock
- **Validation Early**: Validate in Rust before sending to Hoon kernel
- **Serialization Cost**: Be mindful of large noun serialization overhead

## Security Checklist

- [ ] Input validation in Rust handler
- [ ] Input validation in Hoon handler
- [ ] No SQL injection risks (using nouns, not SQL)
- [ ] Base64 validation for binary data
- [ ] Authentication/authorization (if required)
- [ ] Rate limiting considerations
- [ ] Error messages don't leak sensitive info
