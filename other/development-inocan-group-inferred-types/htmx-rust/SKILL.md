---
name: htmx-rust
description: Build interactive hypermedia-driven applications with Axum and HTMX. Use when creating dynamic UIs, real-time updates, AJAX interactions, mentions 'HTMX', 'dynamic content', or 'interactive web app'.
---

# HTMX + Axum Integration (Rust)

## Overview

HTMX enables modern, interactive web applications with minimal JavaScript. Combined with Rust's type safety and Axum's powerful routing, you get fast, reliable hypermedia-driven UIs with compile-time guarantees.

**Key Benefits:**
- No JavaScript framework needed
- Server-side rendering with Askama templates
- Type-safe request/response handling with Axum extractors
- Minimal client-side code
- Progressive enhancement
- Memory safety and zero-cost abstractions

## When to Use This Skill

Use when:
- Building interactive UIs with server-side rendering
- Creating dynamic content updates
- User mentions "HTMX", "dynamic updates", "real-time"
- Implementing AJAX-like behavior without JS
- Building interactive web apps without SPAs

## Quick Start

### 1. Add Dependencies

```toml
[dependencies]
axum = "0.7"
tokio = { version = "1", features = ["full"] }
askama = "0.12"
serde = { version = "1.0", features = ["derive"] }
```

### 2. Create Base Template (Askama)

```html
<!DOCTYPE html>
<html>
    <head>
        <title>{{ title }}</title>
        <script src="https://unpkg.com/htmx.org@1.9.10"></script>
    </head>
    <body>
        {{ content }}
    </body>
</html>
```

### 3. Create Interactive Component

```html
{# counter.html #}
<div id="counter">
    <p>Count: {{ count }}</p>
    <button
        hx-post="/counter/increment"
        hx-target="#counter"
        hx-swap="outerHTML"
    >
        Increment
    </button>
</div>
```

Define the template struct:
```rust
use askama::Template;

#[derive(Template)]
#[template(path = "counter.html")]
struct CounterTemplate {
    count: i32,
}
```

### 4. Create Handler

```rust
use axum::{
    extract::{State},
    response::IntoResponse,
    Json,
};

async fn increment_counter(
    State(state): State<AppState>,
) -> impl IntoResponse {
    let mut count = state.counter.lock().unwrap();
    *count += 1;

    CounterTemplate { count: *count }
}
```

### 5. Setup Router

```rust
use axum::{routing::post, Router};

#[tokio::main]
async fn main() {
    let app = Router::new()
        .route("/counter/increment", post(increment_counter))
        .with_state(AppState::default());

    let listener = tokio::net::TcpListener::bind("127.0.0.1:3000")
        .await
        .unwrap();

    axum::serve(listener, app).await.unwrap();
}
```

---

## Core HTMX Attributes

### hx-get / hx-post

Trigger HTTP requests with Axum extractors:

```html
{# search.html #}
<input
    type="text"
    name="q"
    hx-get="/search"
    hx-trigger="keyup changed delay:500ms"
    hx-target="#results"
/>
<div id="results"></div>
```

Handler with type-safe query parameters:
```rust
use axum::extract::Query;
use serde::Deserialize;

#[derive(Deserialize)]
struct SearchQuery {
    q: String,
}

#[derive(Template)]
#[template(path = "search_results.html")]
struct SearchResults {
    results: Vec<String>,
}

async fn search(Query(params): Query<SearchQuery>) -> impl IntoResponse {
    let results = perform_search(&params.q);
    SearchResults { results }
}
```

### hx-target

Specify where to insert response:

```html
{# load_more.html #}
<button
    hx-get="/posts?page=2"
    hx-target="#posts"
    hx-swap="beforeend"
>
    Load More
</button>
```

### hx-swap

Control how content is swapped:

```html
{# swap options #}
<!-- innerHTML (default) -->
hx-swap="innerHTML"

<!-- outerHTML - replace element itself -->
hx-swap="outerHTML"

<!-- beforeend - append inside -->
hx-swap="beforeend"

<!-- afterend - insert after -->
hx-swap="afterend"
```

### hx-trigger

Control when requests fire:

```html
<!-- On click (default for buttons) -->
<button hx-get="/data">Click me</button>

<!-- On change -->
<select hx-get="/filter" hx-trigger="change">

<!-- On keyup with delay -->
<input hx-get="/search" hx-trigger="keyup changed delay:300ms">

<!-- On page load -->
<div hx-get="/data" hx-trigger="load">

<!-- Every 5 seconds -->
<div hx-get="/updates" hx-trigger="every 5s">
```

---

## Common Patterns

### Pattern 1: Live Search

Component template (`search_box.html`):
```html
<div>
    <input
        type="text"
        name="q"
        placeholder="Search..."
        hx-get="/search"
        hx-trigger="keyup changed delay:500ms"
        hx-target="#search-results"
        hx-indicator="#spinner"
    />
    <span id="spinner" class="htmx-indicator">
        Searching...
    </span>
</div>
<div id="search-results"></div>
```

Results template (`search_results.html`):
```html
<ul>
    {% for result in results %}
        <li>{{ result }}</li>
    {% endfor %}
</ul>
```

Handler:
```rust
use axum::extract::Query;
use askama::Template;
use serde::Deserialize;

#[derive(Deserialize)]
struct SearchParams {
    q: String,
}

#[derive(Template)]
#[template(path = "search_results.html")]
struct SearchResults {
    results: Vec<String>,
}

async fn search(Query(params): Query<SearchParams>) -> impl IntoResponse {
    let results = perform_search(&params.q);
    SearchResults { results }
}
```

### Pattern 2: Infinite Scroll

Template (`post_list.html`):
```html
<div id="posts">
    {% for post in posts %}
        <div class="post-card">{{ post.title }}</div>
    {% endfor %}
</div>

{% if !posts.is_empty() %}
    <div
        hx-get="/posts?page={{ page + 1 }}"
        hx-trigger="revealed"
        hx-swap="outerHTML"
    >
        Loading more...
    </div>
{% endif %}
```

Handler:
```rust
use axum::extract::Query;
use serde::Deserialize;

#[derive(Deserialize)]
struct PageParams {
    page: u32,
}

#[derive(Template)]
#[template(path = "post_list.html")]
struct PostList {
    posts: Vec<Post>,
    page: u32,
}

async fn list_posts(Query(params): Query<PageParams>) -> impl IntoResponse {
    let posts = fetch_posts(params.page);
    PostList {
        posts,
        page: params.page,
    }
}
```

### Pattern 3: Delete with Confirmation

Template (`delete_button.html`):
```html
<button
    hx-delete="/items/{{ item_id }}"
    hx-confirm="Are you sure?"
    hx-target="closest tr"
    hx-swap="outerHTML swap:1s"
>
    Delete
</button>
```

Handler:
```rust
use axum::extract::Path;
use axum::http::StatusCode;

async fn delete_item(Path(item_id): Path<String>) -> StatusCode {
    delete_from_database(&item_id);
    StatusCode::OK  // Empty response removes element
}
```

### Pattern 4: Inline Edit

Display template (`editable_field.html`):
```html
<div id="field-{{ id }}">
    <span>{{ value }}</span>
    <button
        hx-get="/edit/{{ id }}"
        hx-target="#field-{{ id }}"
        hx-swap="outerHTML"
    >
        Edit
    </button>
</div>
```

Edit form template (`edit_form.html`):
```html
<form
    hx-post="/save/{{ id }}"
    hx-target="#field-{{ id }}"
    hx-swap="outerHTML"
>
    <input type="text" name="value" value="{{ value }}" />
    <button type="submit">Save</button>
    <button
        hx-get="/cancel/{{ id }}"
        hx-target="#field-{{ id }}"
    >
        Cancel
    </button>
</form>
```

Handlers:
```rust
use axum::extract::Path;
use axum::Form;
use serde::Deserialize;

#[derive(Deserialize)]
struct SaveData {
    value: String,
}

#[derive(Template)]
#[template(path = "editable_field.html")]
struct EditableField {
    id: String,
    value: String,
}

#[derive(Template)]
#[template(path = "edit_form.html")]
struct EditForm {
    id: String,
    value: String,
}

async fn show_edit_form(Path(id): Path<String>) -> impl IntoResponse {
    let value = fetch_field(&id);
    EditForm { id, value }
}

async fn save_field(
    Path(id): Path<String>,
    Form(data): Form<SaveData>,
) -> impl IntoResponse {
    update_field(&id, &data.value);
    EditableField {
        id,
        value: data.value,
    }
}

async fn cancel_edit(Path(id): Path<String>) -> impl IntoResponse {
    let value = fetch_field(&id);
    EditableField { id, value }
}
```

### Pattern 5: Form Validation

Template (`signup_form.html`):
```html
<form hx-post="/signup" hx-target="#form-errors">
    <div id="form-errors"></div>

    <input
        type="email"
        name="email"
        hx-post="/validate/email"
        hx-trigger="blur"
        hx-target="#email-error"
    />
    <div id="email-error"></div>

    <input type="password" name="password" />

    <button type="submit">Sign Up</button>
</form>
```

Validation template (`validation_error.html`):
```html
<span class="error">{{ message }}</span>
```

Handlers:
```rust
use axum::Form;
use serde::Deserialize;

#[derive(Deserialize)]
struct EmailValidation {
    email: String,
}

#[derive(Template)]
#[template(path = "validation_error.html")]
struct ValidationError {
    message: String,
}

async fn validate_email(Form(data): Form<EmailValidation>) -> impl IntoResponse {
    if is_email_valid(&data.email) {
        (StatusCode::OK, "").into_response()
    } else {
        ValidationError {
            message: "Invalid email format".to_string(),
        }
        .into_response()
    }
}
```

### Pattern 6: Polling / Real-time Updates

Template (`live_stats.html`):
```html
<div
    hx-get="/stats"
    hx-trigger="load, every 5s"
    hx-swap="innerHTML"
>
    Loading stats...
</div>
```

Stats template (`stats_display.html`):
```html
<div>
    <p>Users online: {{ stats.users_online }}</p>
    <p>Active sessions: {{ stats.sessions }}</p>
</div>
```

Handler:
```rust
use askama::Template;

#[derive(Template)]
#[template(path = "stats_display.html")]
struct StatsDisplay {
    stats: Stats,
}

#[derive(Clone)]
struct Stats {
    users_online: usize,
    sessions: usize,
}

async fn get_stats() -> impl IntoResponse {
    let stats = fetch_current_stats();
    StatsDisplay { stats }
}
```

---

## Advanced Patterns

### Out-of-Band Updates (OOB)

Update multiple parts of page in a single request:

Cart button template (`cart_button.html`):
```html
<button id="cart-btn">
    Cart ({{ count }})
</button>
```

Add to cart response template (`add_to_cart_response.html`):
```html
<!-- Main response -->
<div class="notification">
    Added {{ item.name }} to cart!
</div>

<!-- Update cart button (different part of page) -->
<div id="cart-btn" hx-swap-oob="true">
    <button id="cart-btn">
        Cart ({{ new_count }})
    </button>
</div>
```

Handler:
```rust
use axum::Form;
use serde::Deserialize;

#[derive(Deserialize)]
struct AddToCart {
    item_id: String,
}

#[derive(Template)]
#[template(path = "add_to_cart_response.html")]
struct AddToCartResponse {
    item: Item,
    new_count: usize,
}

async fn add_to_cart(Form(data): Form<AddToCart>) -> impl IntoResponse {
    let item = fetch_item(&data.item_id);
    let new_count = add_to_cart_db(&data.item_id);

    AddToCartResponse { item, new_count }
}
```

### Progressive Enhancement

Template that works with and without HTMX:
```html
<form
    action="/submit"
    method="POST"
    hx-post="/submit"
    hx-target="#result"
>
    <input type="text" name="data" />
    <button type="submit">Submit</button>
</form>
<div id="result"></div>
```

Works without JavaScript (form submission), enhanced with HTMX (no page reload).

### Loading States

Template:
```html
<div
    hx-get="/data"
    hx-trigger="load"
    hx-indicator="#loading"
>
    <div id="loading" class="htmx-indicator">
        Loading data...
    </div>
</div>
```

CSS:
```css
.htmx-indicator {
    display: none;
}

.htmx-request .htmx-indicator {
    display: inline;
}

.htmx-request.htmx-indicator {
    display: inline;
}
```

---

## Response Headers

### HX-Trigger

Trigger client-side custom events:

```rust
use axum::http::HeaderMap;

async fn create_item(Form(data): Form<ItemForm>) -> impl IntoResponse {
    let item = create_in_db(data);

    let mut headers = HeaderMap::new();
    headers.insert("HX-Trigger", "itemCreated".parse().unwrap());

    (headers, ItemTemplate { item })
}
```

Client side:
```javascript
document.body.addEventListener("itemCreated", function(evt) {
    console.log("Item created!");
});
```

### HX-Redirect

Redirect to new page after form submission:

```rust
async fn login(Form(credentials): Form<LoginForm>) -> impl IntoResponse {
    if authenticate(&credentials) {
        let mut headers = HeaderMap::new();
        headers.insert("HX-Redirect", "/dashboard".parse().unwrap());
        (headers, StatusCode::OK)
    } else {
        (StatusCode::UNAUTHORIZED, "Invalid credentials")
    }
}
```

### HX-Refresh

Trigger a full page refresh:

```rust
async fn update_config(Form(config): Form<Config>) -> impl IntoResponse {
    save_config(config);

    let mut headers = HeaderMap::new();
    headers.insert("HX-Refresh", "true".parse().unwrap());

    (headers, StatusCode::OK)
}
```

---

## Best Practices

1. **Keep handlers focused** - Return only the HTML fragment needed
2. **Use semantic HTML** - Works without JS, enhanced with HTMX
3. **Type-safe extractors** - Leverage Axum's built-in form/query validation
4. **Handle errors gracefully** - Return error components with appropriate status codes
5. **Optimize responses** - Send minimal HTML, only what changed
6. **Use OOB for multi-updates** - Update multiple page sections efficiently
7. **Progressive enhancement** - Always provide fallback (form action attribute)
8. **Leverage Rust's type system** - Encode validation rules in types, not handlers

---

## Testing HTMX Handlers

Use the fluent Given-When-Then DSL pattern for acceptance testing HTMX interactions:

### Pattern 1: Simple Live Search

**Template Setup:**
```html
{# search.html #}
<input
    type="text"
    name="q"
    hx-get="/search"
    hx-trigger="keyup changed delay:500ms"
    hx-target="#search-results"
/>
<div id="search-results"></div>
```

**Handler:**
```rust
#[derive(Deserialize)]
struct SearchParams {
    q: String,
}

#[derive(Template)]
#[template(path = "search_results.html")]
struct SearchResults {
    results: Vec<String>,
}

async fn search(Query(params): Query<SearchParams>) -> impl IntoResponse {
    let results = perform_search(&params.q);
    SearchResults { results }
}
```

**Acceptance Test:**
```rust
#[tokio::test]
async fn live_search_should_return_matching_results() {
    WebApp::given()
        .a_file_with_content(
            "## TT 2025-01-15\n\
             - #frontend 2h Building search UI\n\
             - #backend 1h Search API\n\
             - #docs 30m Search documentation\n",
        )
        .when_get("/search")
        .with_query("q=search")
        .should_succeed()
        .await
        .expect_status(200)
        .expect_contains("Search API")
        .expect_contains("Search documentation");
}

#[tokio::test]
async fn live_search_should_handle_empty_query() {
    WebApp::given()
        .when_get("/search")
        .with_query("q=")
        .should_succeed()
        .await
        .expect_status(200)
        .expect_not_contains("Search API");
}
```

`★ Insight ─────────────────────────────────────`
The test names describe the HTMX behavior users experience: "should return matching results" communicates the interaction pattern. By testing through the `/search` endpoint with query parameters, you're verifying the handler correctly processes HTMX requests without testing JavaScript—pure server-side hypermedia.
`─────────────────────────────────────────────────`

### Pattern 2: Form Submission with Validation

**Template:**
```html
<form hx-post="/items" hx-target="#items">
    <input type="text" name="title" required />
    <button type="submit">Add Item</button>
</form>
<div id="items"></div>
```

**Handler:**
```rust
#[derive(Deserialize)]
struct CreateItem {
    title: String,
}

#[derive(Template)]
#[template(path = "item.html")]
struct ItemTemplate {
    item: Item,
}

async fn create_item(Form(data): Form<CreateItem>) -> impl IntoResponse {
    if data.title.is_empty() {
        return (StatusCode::BAD_REQUEST, "Title required").into_response();
    }

    let item = Item::create(data.title);
    ItemTemplate { item }.into_response()
}
```

**Acceptance Tests:**
```rust
#[tokio::test]
async fn form_submission_should_create_item() {
    WebApp::given()
        .when_post("/items")
        .with_form_data(&[("title", "New Task")])
        .should_succeed()
        .await
        .expect_status(200)
        .expect_contains("New Task");
}

#[tokio::test]
async fn form_submission_should_reject_empty_title() {
    WebApp::given()
        .when_post("/items")
        .with_form_data(&[("title", "")])
        .should_fail()
        .await
        .expect_status(400)
        .expect_contains("Title required");
}
```

### Pattern 3: Delete with Confirmation

**Handler:**
```rust
async fn delete_item(Path(item_id): Path<String>) -> StatusCode {
    delete_from_database(&item_id);
    StatusCode::OK
}
```

**Acceptance Test:**
```rust
#[tokio::test]
async fn delete_button_should_remove_item() {
    WebApp::given()
        .a_file_with_content(
            "## TT 2025-01-15\n\
             - #project-alpha 2h Work\n",
        )
        .when_delete("/items/project-alpha")
        .should_succeed()
        .await
        .expect_status(200);
}
```

### Pattern 4: Out-of-Band Updates

**Handler returning OOB response:**
```rust
#[derive(Template)]
#[template(path = "add_to_cart_response.html")]
struct AddToCartResponse {
    notification: String,
    cart_count: usize,
}

async fn add_to_cart(Form(data): Form<AddToCart>) -> impl IntoResponse {
    add_to_cart_db(&data.item_id);
    let count = get_cart_count();

    AddToCartResponse {
        notification: format!("Added {} to cart", data.item_id),
        cart_count: count,
    }
}
```

**Template with OOB:**
```html
{# add_to_cart_response.html #}
<!-- Main response -->
<div class="notification">{{ notification }}</div>

<!-- Out-of-band update: cart button elsewhere on page -->
<button id="cart-btn" hx-swap-oob="true">
    Cart ({{ cart_count }})
</button>
```

**Acceptance Test:**
```rust
#[tokio::test]
async fn add_to_cart_should_update_cart_button() {
    WebApp::given()
        .when_post("/add-to-cart")
        .with_form_data(&[("item_id", "widget-123")])
        .should_succeed()
        .await
        .expect_status(200)
        .expect_contains("Added widget-123 to cart")
        .expect_contains("Cart (1)");  // OOB update verified
}
```

`★ Insight ─────────────────────────────────────`
Testing OOB updates verifies that a single response fragment updates multiple page sections—a powerful HTMX pattern. The test reads naturally: "should update cart button" communicates the user-visible effect without mentioning implementation details. This acceptance-test style ensures the actual rendered HTML behaves correctly.
`─────────────────────────────────────────────────`

### Pattern 5: Real-time Polling

**Handler:**
```rust
async fn get_stats() -> impl IntoResponse {
    let stats = fetch_current_stats();
    StatsDisplay { stats }
}
```

**Acceptance Test:**
```rust
#[tokio::test]
async fn stats_endpoint_should_return_current_data() {
    WebApp::given()
        .when_get("/stats")
        .should_succeed()
        .await
        .expect_status(200)
        .expect_contains("Users online")
        .expect_contains("Active sessions");
}
```

---

## Testing Best Practices

1. **Test the handler, not the JavaScript** - HTMX is client-side; your Rust handler only needs to return correct HTML
2. **Use descriptive test names** - Name tests after the user-visible behavior ("should update cart button")
3. **Verify HTML response content** - Assert the returned template renders with correct data
4. **Test error paths** - Verify handlers return appropriate status codes for invalid requests
5. **Test OOB updates** - When using out-of-band updates, verify all parts appear in response
6. **Keep tests focused** - Each test should verify one interaction pattern

---

## Full Example: Todo App

Templates:

**todo_app.html:**
```html
<!DOCTYPE html>
<html>
<head>
    <title>Todo App</title>
    <script src="https://unpkg.com/htmx.org@1.9.10"></script>
</head>
<body>
    <div>
        <h1>My Todos</h1>
        <form
            hx-post="/todos"
            hx-target="#todo-list"
            hx-swap="beforeend"
            hx-on::after-request="this.reset()"
        >
            <input
                type="text"
                name="text"
                placeholder="New todo..."
                required
            />
            <button type="submit">Add</button>
        </form>

        <ul id="todo-list">
            {% for todo in todos %}
                <li id="todo-{{ todo.id }}">
                    <input
                        type="checkbox"
                        {% if todo.completed %}checked{% endif %}
                        hx-post="/todos/{{ todo.id }}/toggle"
                        hx-target="#todo-{{ todo.id }}"
                        hx-swap="outerHTML"
                    />
                    <span class="{% if todo.completed %}completed{% endif %}">
                        {{ todo.text }}
                    </span>
                    <button
                        hx-delete="/todos/{{ todo.id }}"
                        hx-target="#todo-{{ todo.id }}"
                        hx-swap="outerHTML swap:500ms"
                    >
                        Delete
                    </button>
                </li>
            {% endfor %}
        </ul>
    </div>
</body>
</html>
```

Rust implementation:

```rust
use axum::{
    extract::{Path, State},
    Form, Router,
    routing::{get, post, delete},
    http::StatusCode,
    response::IntoResponse,
};
use askama::Template;
use serde::Deserialize;
use std::sync::Mutex;

#[derive(Clone)]
struct Todo {
    id: String,
    text: String,
    completed: bool,
}

#[derive(Clone)]
struct AppState {
    todos: std::sync::Arc<Mutex<Vec<Todo>>>,
}

#[derive(Template)]
#[template(path = "todo_app.html")]
struct TodoApp {
    todos: Vec<Todo>,
}

#[derive(Template)]
#[template(path = "todo_item.html")]
struct TodoItem {
    todo: Todo,
}

#[derive(Deserialize)]
struct CreateTodo {
    text: String,
}

async fn list_todos(State(state): State<AppState>) -> impl IntoResponse {
    let todos = state.todos.lock().unwrap().clone();
    TodoApp { todos }
}

async fn create_todo(
    State(state): State<AppState>,
    Form(form): Form<CreateTodo>,
) -> impl IntoResponse {
    let todo = Todo {
        id: uuid::Uuid::new_v4().to_string(),
        text: form.text,
        completed: false,
    };

    state.todos.lock().unwrap().push(todo.clone());
    TodoItem { todo }
}

async fn toggle_todo(
    State(state): State<AppState>,
    Path(id): Path<String>,
) -> impl IntoResponse {
    let mut todos = state.todos.lock().unwrap();
    if let Some(todo) = todos.iter_mut().find(|t| t.id == id) {
        todo.completed = !todo.completed;
        TodoItem { todo: todo.clone() }
    } else {
        StatusCode::NOT_FOUND.into_response()
    }
}

async fn delete_todo(
    State(state): State<AppState>,
    Path(id): Path<String>,
) -> StatusCode {
    let mut todos = state.todos.lock().unwrap();
    todos.retain(|t| t.id != id);
    StatusCode::OK
}

#[tokio::main]
async fn main() {
    let state = AppState {
        todos: std::sync::Arc::new(Mutex::new(vec![])),
    };

    let app = Router::new()
        .route("/todos", get(list_todos).post(create_todo))
        .route("/todos/:id/toggle", post(toggle_todo))
        .route("/todos/:id", delete(delete_todo))
        .with_state(state);

    let listener = tokio::net::TcpListener::bind("127.0.0.1:3000")
        .await
        .unwrap();

    axum::serve(listener, app).await.unwrap();
}
```

---

## Resources

- [HTMX Documentation](https://htmx.org/docs/)
- [HTMX Examples](https://htmx.org/examples/)
- [Hypermedia Systems Book](https://hypermedia.systems/)
- [Axum Documentation](https://docs.rs/axum/)
- [Askama Template Guide](https://docs.rs/askama/)

## Next Steps

- **Style components** → Use CSS frameworks (Tailwind, Bootstrap)
- **Add state management** → Consider database integration
- **Deploy** → Use Docker, Railway, or cloud platforms
- **Test** → Use the WebApp DSL for comprehensive acceptance tests

