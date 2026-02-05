---
name: rust-patterns
description: Rust design patterns and advanced language patterns. Use when designing APIs, implementing complex abstractions, applying type-level programming, or looking for idiomatic solutions to common problems.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Rust Design Patterns and Advanced Patterns

Comprehensive guide to idiomatic Rust patterns and advanced techniques.

## Creational Patterns

### Builder Pattern

```rust
use std::time::Duration;
use thiserror::Error;

#[derive(Debug, Error)]
pub enum BuildError {
    #[error("missing required field: {0}")]
    MissingField(&'static str),
}

#[derive(Debug)]
pub struct Server {
    host: String,
    port: u16,
    timeout: Duration,
    max_connections: usize,
}

#[derive(Default)]
pub struct ServerBuilder {
    host: Option<String>,
    port: Option<u16>,
    timeout: Option<Duration>,
    max_connections: Option<usize>,
}

impl ServerBuilder {
    pub fn new() -> Self {
        Self::default()
    }
    
    pub fn host(mut self, host: impl Into<String>) -> Self {
        self.host = Some(host.into());
        self
    }
    
    pub fn port(mut self, port: u16) -> Self {
        self.port = Some(port);
        self
    }
    
    pub fn timeout(mut self, timeout: Duration) -> Self {
        self.timeout = Some(timeout);
        self
    }
    
    pub fn max_connections(mut self, max: usize) -> Self {
        self.max_connections = Some(max);
        self
    }
    
    pub fn build(self) -> Result<Server, BuildError> {
        Ok(Server {
            host: self.host.ok_or(BuildError::MissingField("host"))?,
            port: self.port.unwrap_or(8080),
            timeout: self.timeout.unwrap_or(Duration::from_secs(30)),
            max_connections: self.max_connections.unwrap_or(100),
        })
    }
}

impl Server {
    pub fn builder() -> ServerBuilder {
        ServerBuilder::new()
    }
}

// Usage
let server = Server::builder()
    .host("localhost")
    .port(3000)
    .timeout(Duration::from_secs(60))
    .build()?;
```

### Typestate Builder (Compile-Time Validation)

```rust
use std::marker::PhantomData;

// States
pub struct NoHost;
pub struct HasHost;
pub struct NoPort;
pub struct HasPort;

pub struct ServerBuilder<H, P> {
    host: Option<String>,
    port: Option<u16>,
    _state: PhantomData<(H, P)>,
}

impl ServerBuilder<NoHost, NoPort> {
    pub fn new() -> Self {
        Self {
            host: None,
            port: None,
            _state: PhantomData,
        }
    }
}

impl<P> ServerBuilder<NoHost, P> {
    pub fn host(self, host: impl Into<String>) -> ServerBuilder<HasHost, P> {
        ServerBuilder {
            host: Some(host.into()),
            port: self.port,
            _state: PhantomData,
        }
    }
}

impl<H> ServerBuilder<H, NoPort> {
    pub fn port(self, port: u16) -> ServerBuilder<H, HasPort> {
        ServerBuilder {
            host: self.host,
            port: Some(port),
            _state: PhantomData,
        }
    }
}

// Only available when both are set
impl ServerBuilder<HasHost, HasPort> {
    pub fn build(self) -> Server {
        Server {
            host: self.host.unwrap(),
            port: self.port.unwrap(),
        }
    }
}

// Compile-time error if host or port not set
let server = ServerBuilder::new()
    .host("localhost")
    .port(8080)
    .build();  // OK

// let server = ServerBuilder::new()
//     .host("localhost")
//     .build();  // Compile error: no method `build` for HasHost, NoPort
```

### Factory Pattern

```rust
pub trait Transport: Send + Sync {
    fn send(&self, data: &[u8]) -> Result<(), Error>;
}

pub struct TcpTransport { /* ... */ }
pub struct UdpTransport { /* ... */ }
pub struct UnixTransport { /* ... */ }

impl Transport for TcpTransport { /* ... */ }
impl Transport for UdpTransport { /* ... */ }
impl Transport for UnixTransport { /* ... */ }

pub fn create_transport(uri: &str) -> Result<Box<dyn Transport>, Error> {
    let scheme = uri.split("://").next().ok_or(Error::InvalidUri)?;
    
    match scheme {
        "tcp" => Ok(Box::new(TcpTransport::connect(uri)?)),
        "udp" => Ok(Box::new(UdpTransport::bind(uri)?)),
        "unix" => Ok(Box::new(UnixTransport::connect(uri)?)),
        _ => Err(Error::UnsupportedScheme(scheme.into())),
    }
}
```

## Structural Patterns

### Newtype Pattern

```rust
// Wrap primitives for type safety
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct UserId(u64);

impl UserId {
    pub fn new(id: u64) -> Self {
        Self(id)
    }
    
    pub fn as_u64(&self) -> u64 {
        self.0
    }
}

// Validated newtype
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Email(String);

impl Email {
    pub fn new(email: impl Into<String>) -> Result<Self, ValidationError> {
        let email = email.into();
        if email.contains('@') && email.len() <= 254 {
            Ok(Self(email))
        } else {
            Err(ValidationError::InvalidEmail)
        }
    }
    
    pub fn as_str(&self) -> &str {
        &self.0
    }
}

// Can't create invalid Email
// let email = Email("invalid".into());  // No direct construction
let email = Email::new("user@example.com")?;  // Must validate
```

### Type Aliases for Clarity

```rust
// Simple alias
pub type Result<T> = std::result::Result<T, Error>;

// Generic alias with constraints
pub type BoxFuture<'a, T> = Pin<Box<dyn Future<Output = T> + Send + 'a>>;

// Associated type pattern
pub trait Container {
    type Item;
    type Error;
    
    fn get(&self, key: &str) -> Result<Self::Item, Self::Error>;
}
```

### Extension Traits

```rust
// Extend types you don't own
pub trait StringExt {
    fn truncate_ellipsis(&self, max_len: usize) -> String;
}

impl StringExt for str {
    fn truncate_ellipsis(&self, max_len: usize) -> String {
        if self.len() <= max_len {
            self.to_string()
        } else {
            format!("{}...", &self[..max_len.saturating_sub(3)])
        }
    }
}

// Extend external types with your traits
pub trait ResultExt<T, E> {
    fn log_err(self) -> Self;
}

impl<T, E: std::fmt::Display> ResultExt<T, E> for Result<T, E> {
    fn log_err(self) -> Self {
        if let Err(ref e) = self {
            tracing::error!(error = %e, "Operation failed");
        }
        self
    }
}

// Usage
let result = fallible_operation().log_err()?;
```

### Deref for Smart Pointers

```rust
use std::ops::{Deref, DerefMut};

pub struct Wrapper<T> {
    inner: T,
    metadata: Metadata,
}

impl<T> Deref for Wrapper<T> {
    type Target = T;
    
    fn deref(&self) -> &Self::Target {
        &self.inner
    }
}

impl<T> DerefMut for Wrapper<T> {
    fn deref_mut(&mut self) -> &mut Self::Target {
        &mut self.inner
    }
}

// Methods on T are available on Wrapper<T>
let wrapper = Wrapper { inner: String::from("hello"), metadata: Metadata::new() };
println!("{}", wrapper.len());  // String::len() via Deref
```

## Behavioral Patterns

### Strategy Pattern with Traits

```rust
pub trait CompressionStrategy: Send + Sync {
    fn compress(&self, data: &[u8]) -> Result<Vec<u8>, Error>;
    fn decompress(&self, data: &[u8]) -> Result<Vec<u8>, Error>;
}

pub struct GzipStrategy;
pub struct ZstdStrategy { level: i32 }
pub struct NoCompression;

impl CompressionStrategy for GzipStrategy {
    fn compress(&self, data: &[u8]) -> Result<Vec<u8>, Error> { /* ... */ }
    fn decompress(&self, data: &[u8]) -> Result<Vec<u8>, Error> { /* ... */ }
}

impl CompressionStrategy for ZstdStrategy {
    fn compress(&self, data: &[u8]) -> Result<Vec<u8>, Error> { /* ... */ }
    fn decompress(&self, data: &[u8]) -> Result<Vec<u8>, Error> { /* ... */ }
}

pub struct Storage<C: CompressionStrategy> {
    compression: C,
}

impl<C: CompressionStrategy> Storage<C> {
    pub fn new(compression: C) -> Self {
        Self { compression }
    }
    
    pub fn store(&self, data: &[u8]) -> Result<(), Error> {
        let compressed = self.compression.compress(data)?;
        // Store compressed data
        Ok(())
    }
}
```

### Command Pattern

```rust
pub trait Command: Send {
    fn execute(&self) -> Result<(), Error>;
    fn undo(&self) -> Result<(), Error>;
}

pub struct CreateFileCommand {
    path: PathBuf,
}

impl Command for CreateFileCommand {
    fn execute(&self) -> Result<(), Error> {
        std::fs::File::create(&self.path)?;
        Ok(())
    }
    
    fn undo(&self) -> Result<(), Error> {
        std::fs::remove_file(&self.path)?;
        Ok(())
    }
}

pub struct CommandHistory {
    executed: Vec<Box<dyn Command>>,
}

impl CommandHistory {
    pub fn execute(&mut self, cmd: Box<dyn Command>) -> Result<(), Error> {
        cmd.execute()?;
        self.executed.push(cmd);
        Ok(())
    }
    
    pub fn undo_last(&mut self) -> Result<(), Error> {
        if let Some(cmd) = self.executed.pop() {
            cmd.undo()?;
        }
        Ok(())
    }
}
```

### Visitor Pattern

```rust
pub trait Visitor {
    fn visit_file(&mut self, file: &File);
    fn visit_directory(&mut self, dir: &Directory);
}

pub trait Visitable {
    fn accept(&self, visitor: &mut dyn Visitor);
}

pub struct File {
    pub name: String,
    pub size: u64,
}

pub struct Directory {
    pub name: String,
    pub children: Vec<Box<dyn Visitable>>,
}

impl Visitable for File {
    fn accept(&self, visitor: &mut dyn Visitor) {
        visitor.visit_file(self);
    }
}

impl Visitable for Directory {
    fn accept(&self, visitor: &mut dyn Visitor) {
        visitor.visit_directory(self);
        for child in &self.children {
            child.accept(visitor);
        }
    }
}

// Size calculator visitor
pub struct SizeCalculator {
    pub total_size: u64,
}

impl Visitor for SizeCalculator {
    fn visit_file(&mut self, file: &File) {
        self.total_size += file.size;
    }
    
    fn visit_directory(&mut self, _dir: &Directory) {
        // Directories don't have size themselves
    }
}
```

## Advanced Type Patterns

### Phantom Types

```rust
use std::marker::PhantomData;

// Marker types for state
pub struct Locked;
pub struct Unlocked;

pub struct Door<State> {
    _state: PhantomData<State>,
}

impl Door<Locked> {
    pub fn unlock(self) -> Door<Unlocked> {
        Door { _state: PhantomData }
    }
}

impl Door<Unlocked> {
    pub fn lock(self) -> Door<Locked> {
        Door { _state: PhantomData }
    }
    
    pub fn open(&self) {
        println!("Opening door");
    }
}

// Can only open unlocked doors
let door: Door<Locked> = Door { _state: PhantomData };
// door.open();  // Compile error: no method `open` for Door<Locked>
let door = door.unlock();
door.open();  // OK
```

### Type-Level State Machines

```rust
use std::marker::PhantomData;

// HTTP request states
pub struct Created;
pub struct HeadersSet;
pub struct BodySet;
pub struct Sent;

pub struct Request<State> {
    url: String,
    headers: Vec<(String, String)>,
    body: Option<Vec<u8>>,
    _state: PhantomData<State>,
}

impl Request<Created> {
    pub fn new(url: impl Into<String>) -> Self {
        Self {
            url: url.into(),
            headers: Vec::new(),
            body: None,
            _state: PhantomData,
        }
    }
    
    pub fn header(mut self, name: &str, value: &str) -> Request<HeadersSet> {
        self.headers.push((name.into(), value.into()));
        Request {
            url: self.url,
            headers: self.headers,
            body: self.body,
            _state: PhantomData,
        }
    }
}

impl Request<HeadersSet> {
    pub fn header(mut self, name: &str, value: &str) -> Self {
        self.headers.push((name.into(), value.into()));
        self
    }
    
    pub fn body(self, body: Vec<u8>) -> Request<BodySet> {
        Request {
            url: self.url,
            headers: self.headers,
            body: Some(body),
            _state: PhantomData,
        }
    }
    
    pub fn send(self) -> Result<Response, Error> {
        // Send request without body
        todo!()
    }
}

impl Request<BodySet> {
    pub fn send(self) -> Result<Response, Error> {
        // Send request with body
        todo!()
    }
}
```

### Sealed Traits

```rust
mod private {
    pub trait Sealed {}
}

/// A trait that cannot be implemented outside this crate.
pub trait DatabaseDriver: private::Sealed {
    fn connect(&self, url: &str) -> Result<Connection, Error>;
}

pub struct PostgresDriver;
pub struct SqliteDriver;

impl private::Sealed for PostgresDriver {}
impl private::Sealed for SqliteDriver {}

impl DatabaseDriver for PostgresDriver {
    fn connect(&self, url: &str) -> Result<Connection, Error> { /* ... */ }
}

impl DatabaseDriver for SqliteDriver {
    fn connect(&self, url: &str) -> Result<Connection, Error> { /* ... */ }
}

// External crates cannot implement DatabaseDriver
```

### GATs (Generic Associated Types)

```rust
pub trait StreamingIterator {
    type Item<'a> where Self: 'a;
    
    fn next(&mut self) -> Option<Self::Item<'_>>;
}

pub struct WindowedSlice<'data, T> {
    data: &'data [T],
    pos: usize,
    window_size: usize,
}

impl<'data, T> StreamingIterator for WindowedSlice<'data, T> {
    type Item<'a> = &'a [T] where Self: 'a;
    
    fn next(&mut self) -> Option<Self::Item<'_>> {
        if self.pos + self.window_size <= self.data.len() {
            let window = &self.data[self.pos..self.pos + self.window_size];
            self.pos += 1;
            Some(window)
        } else {
            None
        }
    }
}
```

### HRTB (Higher-Rank Trait Bounds)

```rust
// Function that accepts a closure working with any lifetime
fn apply_to_ref<F>(f: F)
where
    F: for<'a> Fn(&'a str) -> &'a str,
{
    let s = String::from("hello");
    println!("{}", f(&s));
}

// Useful for callbacks that work with borrowed data
fn process_with_callback<F>(data: Vec<String>, callback: F)
where
    F: for<'a> Fn(&'a str) -> bool,
{
    for item in &data {
        if callback(item) {
            println!("Match: {}", item);
        }
    }
}

// Usage
apply_to_ref(|s| s);
process_with_callback(data, |s| s.starts_with("prefix"));
```

### Variance and Lifetime Bounds

```rust
use std::marker::PhantomData;

// Covariant over 'a - can shorten lifetime
struct Covariant<'a, T> {
    value: &'a T,
}

// Invariant over 'a - lifetime must match exactly
struct Invariant<'a, T> {
    value: &'a mut T,
}

// Contravariant (rare) - can lengthen lifetime
struct Contravariant<'a, T> {
    func: fn(&'a T),
    _marker: PhantomData<T>,
}

// Lifetime bounds on generic types
struct Cache<'a, T: 'a> {
    data: &'a T,
}

fn store_reference<'a, T: 'a>(cache: &mut Cache<'a, T>, value: &'a T) {
    cache.data = value;
}
```

### Never Type and Diverging Functions

```rust
// The never type (!) indicates a function never returns
fn diverges() -> ! {
    panic!("This never returns!");
}

// Useful in match arms
fn example(condition: bool) -> i32 {
    if condition {
        42
    } else {
        diverges() // ! coerces to any type
    }
}

// Common in infinite loops
fn run_server() -> ! {
    loop {
        accept_connection();
    }
}

// In Result handling
fn must_succeed() -> Value {
    match fallible_op() {
        Ok(v) => v,
        Err(_) => std::process::exit(1), // returns !
    }
}
```

### DST and ?Sized

```rust
// [T] and str are Dynamically Sized Types (DST)
fn print_slice<T: std::fmt::Debug>(slice: &[T]) {
    println!("{:?}", slice);
}

// By default, generics require T: Sized
// Use ?Sized to accept unsized types
fn generic_unsized<T: ?Sized + std::fmt::Debug>(value: &T) {
    println!("{:?}", value);
}

// Works with both sized and unsized types
generic_unsized(&42i32);      // &i32 - sized
generic_unsized("hello");     // &str - unsized
generic_unsized(&[1, 2, 3]);  // &[i32] - can work too

// Trait objects are also DST
fn call_draw(drawable: &dyn Draw) {
    drawable.draw();
}
```

### Zero-Sized Types (ZST)

```rust
struct MyZst;

// Size = 0, no memory allocation needed
assert_eq!(std::mem::size_of::<MyZst>(), 0);

// Useful for type-level markers
struct Collection<T, Strategy = DefaultStrategy> {
    items: Vec<T>,
    _strategy: PhantomData<Strategy>,
}

struct DefaultStrategy;
struct SortedStrategy;

// The strategy marker has no runtime cost
impl<T> Collection<T, DefaultStrategy> {
    fn add(&mut self, item: T) {
        self.items.push(item);
    }
}

impl<T: Ord> Collection<T, SortedStrategy> {
    fn add(&mut self, item: T) {
        let pos = self.items.binary_search(&item).unwrap_or_else(|p| p);
        self.items.insert(pos, item);
    }
}
```

## Error Handling Patterns

### Error Enums with Context

```rust
use thiserror::Error;

#[derive(Debug, Error)]
pub enum ServiceError {
    #[error("user not found: {user_id}")]
    UserNotFound { user_id: u64 },
    
    #[error("permission denied for {action} on {resource}")]
    PermissionDenied { action: String, resource: String },
    
    #[error("rate limit exceeded: {limit} requests per {window:?}")]
    RateLimited { limit: u32, window: Duration },
    
    #[error("database error")]
    Database(#[from] sqlx::Error),
    
    #[error("external service error: {service}")]
    ExternalService {
        service: String,
        #[source]
        source: reqwest::Error,
    },
}

impl ServiceError {
    pub fn is_retryable(&self) -> bool {
        matches!(self, 
            ServiceError::RateLimited { .. } |
            ServiceError::Database(_) |
            ServiceError::ExternalService { .. }
        )
    }
    
    pub fn status_code(&self) -> u16 {
        match self {
            ServiceError::UserNotFound { .. } => 404,
            ServiceError::PermissionDenied { .. } => 403,
            ServiceError::RateLimited { .. } => 429,
            ServiceError::Database(_) => 500,
            ServiceError::ExternalService { .. } => 502,
        }
    }
}
```

### Result Extensions

```rust
pub trait ResultExt<T, E> {
    fn inspect_ok<F: FnOnce(&T)>(self, f: F) -> Self;
    fn inspect_err_ref<F: FnOnce(&E)>(self, f: F) -> Self;
    fn with_context<C, F>(self, f: F) -> Result<T, ContextError<E, C>>
    where
        F: FnOnce() -> C;
}

impl<T, E> ResultExt<T, E> for Result<T, E> {
    fn inspect_ok<F: FnOnce(&T)>(self, f: F) -> Self {
        if let Ok(ref value) = self {
            f(value);
        }
        self
    }
    
    fn inspect_err_ref<F: FnOnce(&E)>(self, f: F) -> Self {
        if let Err(ref e) = self {
            f(e);
        }
        self
    }
    
    fn with_context<C, F>(self, f: F) -> Result<T, ContextError<E, C>>
    where
        F: FnOnce() -> C,
    {
        self.map_err(|e| ContextError {
            context: f(),
            source: e,
        })
    }
}
```

## Async Patterns

### Async Trait Methods

```rust
use async_trait::async_trait;

#[async_trait]
pub trait Repository: Send + Sync {
    type Entity;
    type Error;
    
    async fn find(&self, id: &str) -> Result<Option<Self::Entity>, Self::Error>;
    async fn save(&self, entity: &Self::Entity) -> Result<(), Self::Error>;
    async fn delete(&self, id: &str) -> Result<bool, Self::Error>;
}

#[async_trait]
impl Repository for UserRepository {
    type Entity = User;
    type Error = DbError;
    
    async fn find(&self, id: &str) -> Result<Option<User>, DbError> {
        // ...
    }
    
    async fn save(&self, entity: &User) -> Result<(), DbError> {
        // ...
    }
    
    async fn delete(&self, id: &str) -> Result<bool, DbError> {
        // ...
    }
}
```

### Cancellation Token Pattern

```rust
use tokio_util::sync::CancellationToken;

pub struct Worker {
    cancel: CancellationToken,
}

impl Worker {
    pub fn new() -> Self {
        Self {
            cancel: CancellationToken::new(),
        }
    }
    
    pub async fn run(&self) {
        loop {
            tokio::select! {
                _ = self.cancel.cancelled() => {
                    tracing::info!("Worker cancelled");
                    break;
                }
                _ = self.do_work() => {
                    // Work completed, continue
                }
            }
        }
    }
    
    pub fn stop(&self) {
        self.cancel.cancel();
    }
    
    async fn do_work(&self) {
        // ...
    }
}
```

### Retry with Backoff

```rust
use std::time::Duration;
use tokio::time::sleep;

pub struct RetryConfig {
    pub max_attempts: u32,
    pub initial_delay: Duration,
    pub max_delay: Duration,
    pub multiplier: f64,
}

impl Default for RetryConfig {
    fn default() -> Self {
        Self {
            max_attempts: 3,
            initial_delay: Duration::from_millis(100),
            max_delay: Duration::from_secs(10),
            multiplier: 2.0,
        }
    }
}

pub async fn retry<T, E, F, Fut>(
    config: &RetryConfig,
    mut operation: F,
) -> Result<T, E>
where
    F: FnMut() -> Fut,
    Fut: std::future::Future<Output = Result<T, E>>,
    E: std::fmt::Display,
{
    let mut delay = config.initial_delay;
    let mut attempts = 0;
    
    loop {
        attempts += 1;
        
        match operation().await {
            Ok(result) => return Ok(result),
            Err(e) if attempts >= config.max_attempts => {
                tracing::error!(attempts, error = %e, "All retry attempts failed");
                return Err(e);
            }
            Err(e) => {
                tracing::warn!(attempts, error = %e, "Attempt failed, retrying");
                sleep(delay).await;
                delay = Duration::from_secs_f64(
                    (delay.as_secs_f64() * config.multiplier).min(config.max_delay.as_secs_f64())
                );
            }
        }
    }
}
```

## Resource Management

### RAII Guards

```rust
pub struct FileGuard {
    path: PathBuf,
}

impl FileGuard {
    pub fn create(path: impl Into<PathBuf>) -> std::io::Result<Self> {
        let path = path.into();
        std::fs::File::create(&path)?;
        Ok(Self { path })
    }
}

impl Drop for FileGuard {
    fn drop(&mut self) {
        let _ = std::fs::remove_file(&self.path);
    }
}

// File is automatically deleted when guard goes out of scope
fn use_temp_file() -> Result<(), Error> {
    let guard = FileGuard::create("/tmp/temp_file")?;
    
    // Do work with file
    
    // File deleted here when guard drops
    Ok(())
}
```

### Scoped Resources

```rust
pub fn with_connection<F, R>(url: &str, f: F) -> Result<R, Error>
where
    F: FnOnce(&mut Connection) -> Result<R, Error>,
{
    let mut conn = Connection::connect(url)?;
    let result = f(&mut conn);
    conn.close()?;
    result
}

// Usage
let result = with_connection("postgres://...", |conn| {
    conn.execute("SELECT * FROM users")?;
    Ok(())
})?;
```

### Object Pool

```rust
use std::sync::{Arc, Mutex};
use std::collections::VecDeque;

pub struct Pool<T> {
    available: Mutex<VecDeque<T>>,
    create: Box<dyn Fn() -> T + Send + Sync>,
    max_size: usize,
}

pub struct PoolGuard<'a, T> {
    pool: &'a Pool<T>,
    item: Option<T>,
}

impl<T> Pool<T> {
    pub fn new<F>(max_size: usize, create: F) -> Self
    where
        F: Fn() -> T + Send + Sync + 'static,
    {
        Self {
            available: Mutex::new(VecDeque::new()),
            create: Box::new(create),
            max_size,
        }
    }
    
    pub fn get(&self) -> PoolGuard<'_, T> {
        let item = self.available.lock().unwrap().pop_front()
            .unwrap_or_else(|| (self.create)());
        
        PoolGuard {
            pool: self,
            item: Some(item),
        }
    }
    
    fn return_item(&self, item: T) {
        let mut available = self.available.lock().unwrap();
        if available.len() < self.max_size {
            available.push_back(item);
        }
    }
}

impl<'a, T> std::ops::Deref for PoolGuard<'a, T> {
    type Target = T;
    
    fn deref(&self) -> &T {
        self.item.as_ref().unwrap()
    }
}

impl<'a, T> Drop for PoolGuard<'a, T> {
    fn drop(&mut self) {
        if let Some(item) = self.item.take() {
            self.pool.return_item(item);
        }
    }
}
```

## Functional Patterns

### Railway-Oriented Programming

```rust
pub fn process_user(id: &str) -> Result<User, Error> {
    fetch_user(id)
        .and_then(validate_user)
        .and_then(enrich_user)
        .and_then(save_user)
}

// With early returns for clarity
pub fn process_user_explicit(id: &str) -> Result<User, Error> {
    let user = fetch_user(id)?;
    let user = validate_user(user)?;
    let user = enrich_user(user)?;
    save_user(user)
}
```

### Monad-like Chaining

```rust
pub struct Pipeline<T> {
    value: T,
}

impl<T> Pipeline<T> {
    pub fn new(value: T) -> Self {
        Self { value }
    }
    
    pub fn map<U, F: FnOnce(T) -> U>(self, f: F) -> Pipeline<U> {
        Pipeline { value: f(self.value) }
    }
    
    pub fn and_then<U, F: FnOnce(T) -> Pipeline<U>>(self, f: F) -> Pipeline<U> {
        f(self.value)
    }
    
    pub fn tap<F: FnOnce(&T)>(self, f: F) -> Self {
        f(&self.value);
        self
    }
    
    pub fn finish(self) -> T {
        self.value
    }
}

// Usage
let result = Pipeline::new(input)
    .map(parse)
    .tap(|x| tracing::debug!("Parsed: {:?}", x))
    .map(validate)
    .map(transform)
    .finish();
```

### Compose Functions

```rust
pub fn compose<A, B, C, F, G>(f: F, g: G) -> impl Fn(A) -> C
where
    F: Fn(A) -> B,
    G: Fn(B) -> C,
{
    move |x| g(f(x))
}

// Usage
let parse_and_validate = compose(parse, validate);
let result = parse_and_validate(input);
```

## Pattern Matching Patterns

### Match Guards with Let Chains (Rust 2024)

```rust
fn process(opt: Option<Value>) -> Result<(), Error> {
    match opt {
        Some(v) if v.is_valid() && let Ok(data) = v.parse() => {
            handle_valid(data)
        }
        Some(v) if v.is_recoverable() => {
            handle_recovery(v)
        }
        Some(_) => Err(Error::Invalid),
        None => Err(Error::Missing),
    }
}
```

### Destructuring Patterns

```rust
struct Point { x: i32, y: i32, z: i32 }

fn process_point(p: Point) {
    match p {
        // Exact match
        Point { x: 0, y: 0, z: 0 } => println!("Origin"),
        
        // Partial match with binding
        Point { x, y: 0, .. } => println!("On X axis at {}", x),
        
        // Range patterns
        Point { x: 0..=10, y, z } => println!("Near origin: y={}, z={}", y, z),
        
        // Or patterns
        Point { x: 0, .. } | Point { y: 0, .. } => println!("On an axis"),
        
        // Binding with @
        Point { x: x @ 100.., y, z } => println!("Far point x={}", x),
        
        // Catch-all
        p => println!("Point at ({}, {}, {})", p.x, p.y, p.z),
    }
}
```

### Slice Patterns

```rust
fn analyze_slice(slice: &[i32]) {
    match slice {
        [] => println!("Empty"),
        [single] => println!("Single element: {}", single),
        [first, second] => println!("Pair: {}, {}", first, second),
        [first, .., last] => println!("First: {}, Last: {}", first, last),
        [first, middle @ .., last] => {
            println!("First: {}, Middle: {:?}, Last: {}", first, middle, last)
        }
    }
}

fn starts_with(slice: &[u8], prefix: &[u8]) -> bool {
    match (slice, prefix) {
        (_, []) => true,
        ([x, xs @ ..], [y, ys @ ..]) if x == y => starts_with(xs, ys),
        _ => false,
    }
}
```
