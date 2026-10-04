---
name: rust
description: Rust systems programming language for safe, concurrent, practical software
license: MIT
compatibility: opencode
metadata:
  audience: developers
  category: programming-languages
---
## What I do
- Write memory-safe systems code
- Implement error handling with Result and Option
- Use lifetimes and generics
- Create concurrent programs with async/await
- Build CLI tools with Clap
- Write web services with Axum
- Use cargo for project management

## When to use me
When building high-performance, memory-safe applications or systems software.

## Ownership & Borrowing
```rust
fn main() {
    let s1 = String::from("hello");
    let s2 = s1;  // s1 moved to s2
    
    // Clone to avoid move
    let s3 = s2.clone();
    
    // Borrowing
    let len = calculate_length(&s3);
    
    // Mutable reference
    let mut s = String::from("hello");
    change(&mut s);
}

fn calculate_length(s: &String) -> usize {
    s.len()
}

fn change(s: &mut String) {
    s.push_str(", world");
}
```

## Error Handling
```rust
use std::fs::File;
use std::io::{self, Read};

fn read_file(path: &str) -> Result<String, io::Error> {
    let mut file = File::open(path)?;
    let mut contents = String::new();
    file.read_to_string(&mut contents)?;
    Ok(contents)
}

// Using match
fn main() {
    match read_file("example.txt") {
        Ok(contents) => println!("{}", contents),
        Err(e) => eprintln!("Error: {}", e),
    }
}

// Using if let
fn main() {
    if let Ok(contents) = read_file("example.txt") {
        println!("{}", contents);
    }
}

// Custom error type
#[derive(Debug)]
enum AppError {
    Io(std::io::Error),
    Parse(std::num::ParseIntError),
}

impl From<std::io::Error> for AppError {
    fn from(err: std::io::Error) -> Self {
        AppError::Io(err)
    }
}
```

## Structs & Impl
```rust
struct Rectangle {
    width: u32,
    height: u32,
}

impl Rectangle {
    fn new(width: u32, height: u32) -> Self {
        Rectangle { width, height }
    }
    
    fn area(&self) -> u32 {
        self.width * self.height
    }
    
    fn can_hold(&self, other: &Rectangle) -> bool {
        self.width > other.width && self.height > other.height
    }
}

// Associated function (no self)
impl Rectangle {
    fn square(size: u32) -> Self {
        Rectangle { width: size, height: size }
    }
}
```

## Traits & Generics
```rust
trait Summary {
    fn summarize(&self) -> String;
    
    // Default implementation
    fn summarize_author(&self) -> String {
        format!("(Read more from {}...)", self.summarize())
    }
}

struct Article {
    title: String,
    author: String,
}

impl Summary for Article {
    fn summarize(&self) -> String {
        format!("{}, by {}", self.title, self.author)
    }
}

// Generic function
fn largest<T: PartialOrd>(list: &[T]) -> &T {
    let mut largest = &list[0];
    for item in list {
        if item > largest {
            largest = item;
        }
    }
    largest
}
```

## Concurrency
```rust
use std::thread;
use std::sync::Mutex;

fn main() {
    let handle = thread::spawn(|| {
        for i in 1..10 {
            println!("thread: {}", i);
        }
    });
    
    handle.join().unwrap();
}

// Shared state
fn main() {
    let counter = Mutex::new(0);
    
    let mut handles = vec![];
    for _ in 0..10 {
        let handle = thread::spawn(|| {
            let mut num = counter.lock().unwrap();
            *num += 1;
        });
        handles.push(handle);
    }
    
    for handle in handles {
        handle.join().unwrap();
    }
    
    println!("Result: {}", *counter.lock().unwrap());
}
```

## Async/Await
```rust
use async_std;

async fn fetch_url(url: &str) -> Result<String, reqwest::Error> {
    let resp = reqwest::get(url).await?;
    let body = resp.text().await?;
    Ok(body)
}

#[tokio::main]
async fn main() {
    let result = fetch_url("https://example.com").await;
    match result {
        Ok(body) => println!("{}", body),
        Err(e) => eprintln!("Error: {}", e),
    }
}
```

## CLI with Clap
```rust
use clap::{Parser, Subcommand};

#[derive(Parser)]
#[command(name = "myapp")]
#[command(about = "A CLI app", long_about = None)]
struct Cli {
    #[command(subcommand)]
    command: Commands,
    
    #[arg(short, long, global = true)]
    verbose: bool,
}

#[derive(Subcommand)]
enum Commands {
    Add { name: String },
    Remove { id: u32 },
    List,
}

fn main() {
    let cli = Cli::parse();
    
    match &cli.command {
        Commands::Add { name } => println!("Adding: {}", name),
        Commands::Remove { id } => println!("Removing: {}", id),
        Commands::List => println!("Listing all"),
    }
}
```
