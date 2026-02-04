---
name: episodic-memory-testing
description: Domain-specific testing patterns for episodic memory operations. Use when testing episode lifecycle, pattern extraction, reward scoring, or memory retrieval.
---

# Episodic Memory Testing Patterns

This skill provides specialized testing patterns for the episodic memory system.

## Episode Lifecycle Testing

### Complete Episode Flow

```rust
#[tokio::test]
async fn test_complete_episode_lifecycle() {
    let memory = setup_memory().await;

    // 1. Start episode
    let episode_id = memory.start_episode(
        "Test code generation".to_string(),
        TaskContext::default(),
        TaskType::CodeGeneration,
    ).await;
    assert!(!episode_id.is_empty());

    // 2. Log execution steps
    let step1 = memory.log_execution_step(
        episode_id.clone(),
        ToolCall {
            tool_name: "bash".to_string(),
            input: "ls -la".to_string(),
            output: Some("total 4\ndrwxr-xr-x  2 user user  4096 Jan 16 10:00 .\n".to_string()),
            duration_ms: 12,
        },
    ).await;

    let step2 = memory.log_execution_step(
        episode_id.clone(),
        ToolCall {
            tool_name: "read".to_string(),
            input: "file.rs".to_string(),
            output Some("fn main() { println!(\"Hello\"); }".to_string()),
            duration_ms: 5,
        },
    ).await;

    // 3. Complete episode
    memory.complete_episode(
        episode_id.clone(),
        TaskOutcome::Success,
        Some(vec!["Use more descriptive variable names".to_string()]),
    ).await?;

    // 4. Verify episode was stored
    let episode = memory.get_episode(&episode_id).await?;
    assert_eq!(episode.outcome, TaskOutcome::Success);
    assert_eq!(episode.steps.len(), 2);
}
```

### Episode ID Uniqueness

```rust
#[tokio::test]
async fn test_episode_ids_are_unique() {
    let memory = setup_memory().await;
    let ids: HashSet<String> = (0..100)
        .map(|i| {
            memory.start_episode(
                format!("Task {}", i),
                TaskContext::default(),
                TaskType::CodeGeneration,
            ).await
        })
        .collect();

    assert_eq!(ids.len(), 100, "All episode IDs should be unique");
}
```

## Pattern Extraction Testing

### Basic Pattern Extraction

```rust
#[tokio::test]
async fn test_pattern_extraction() {
    let memory = setup_memory().await;
    let episode_id = create_test_episode_with_patterns(&memory).await;

    // Extract patterns
    let patterns = memory.extract_patterns(episode_id).await?;

    // Verify patterns were extracted
    assert!(!patterns.is_empty());

    // Verify pattern structure
    for pattern in &patterns {
        assert!(!pattern.name.is_empty());
        assert!(pattern.frequency > 0.0);
        assert!(!pattern.description.is_empty());
    }
}
```

### Pattern Frequency Calculation

```rust
#[tokio::test]
async fn test_pattern_frequency_calculation() {
    let memory = setup_memory().await;

    // Create multiple episodes with similar patterns
    for _ in 0..5 {
        let episode_id = memory.start_episode(
            "Similar task".to_string(),
            TaskContext::default(),
            TaskType::CodeGeneration,
        ).await;

        memory.log_execution_step(
            episode_id.clone(),
            ToolCall {
                tool_name: "bash".to_string(),
                input: "cargo build".to_string(),
                output: Some("Finished dev [optimized] target(s)".to_string()),
                duration_ms: 100,
            },
        ).await;

        memory.complete_episode(
            episode_id,
            TaskOutcome::Success,
            None,
        ).await?;
    }

    // Extract patterns and verify frequency
    let patterns = memory.extract_patterns_for_task_type(TaskType::CodeGeneration).await?;

    let build_pattern = patterns.iter()
        .find(|p| p.name.contains("cargo build"))
        .expect("Should find cargo build pattern");

    assert!(build_pattern.frequency >= 0.8);
}
```

## Reward Scoring Testing

### Score Calculation

```rust
#[tokio::test]
async fn test_reward_score_calculation() {
    let memory = setup_memory().await;

    let episode_id = memory.start_episode(
        "High quality task".to_string(),
        TaskContext::default(),
        TaskType::CodeGeneration,
    ).await;

    // Log high-quality steps
    for i in 0..10 {
        memory.log_execution_step(
            episode_id.clone(),
            ToolCall {
                tool_name: "write".to_string(),
                input: format!("Step {}", i),
                output: Some("Success".to_string()),
                duration_ms: 10,
            },
        ).await;
    }

    memory.complete_episode(
        episode_id.clone(),
        TaskOutcome::Success,
        Some(vec!["Good refactoring".to_string()]),
    ).await?;

    let score = memory.get_episode_score(&episode_id).await?;
    assert!(score >= 0.7, "High quality episode should have high score");
}
```

### Score Bounds

```rust
#[test]
fn test_reward_score_bounds() {
    // Perfect efficiency and quality
    let perfect_score = calculate_reward_score(1.0, 1.0);
    assert!(perfect_score >= 0.9);

    // Zero efficiency
    let zero_score = calculate_reward_score(0.0, 1.0);
    assert!(zero_score < perfect_score);

    // Zero quality
    let zero_quality = calculate_reward_score(1.0, 0.0);
    assert!(zero_quality < perfect_score);
}
```

## Memory Retrieval Testing

### Context-Based Retrieval

```rust
#[tokio::test]
async fn test_memory_retrieval_by_context() {
    let memory = setup_memory().await;

    // Create episodes with different contexts
    let rust_episode = memory.start_episode(
        "Rust implementation".to_string(),
        TaskContext { language: "rust".to_string(), ..Default::default() },
        TaskType::CodeGeneration,
    ).await;

    let python_episode = memory.start_episode(
        "Python implementation".to_string(),
        TaskContext { language: "python".to_string(), ..Default::default() },
        TaskType::CodeGeneration,
    ).await;

    // Retrieve by context
    let rust_memories = memory.retrieve_context(
        "rust".to_string(),
        Some(10),
    ).await?;

    assert!(rust_memories.len() >= 1);
    assert!(rust_memories.iter().all(|m| m.context.language == "rust"));
}
```

### Similar Episode Retrieval

```rust
#[tokio::test]
async fn test_similar_episode_retrieval() {
    let memory = setup_memory().await;

    // Create base episode
    let base_id = memory.start_episode(
        "Database migration".to_string(),
        TaskContext::default(),
        TaskType::Database,
    ).await;

    memory.complete_episode(base_id.clone(), TaskOutcome::Success, None).await?;

    // Create similar episodes
    for i in 0..5 {
        let similar_id = memory.start_episode(
            format!("Database migration {}", i),
            TaskContext::default(),
            TaskType::Database,
        ).await;
        memory.complete_episode(similar_id, TaskOutcome::Success, None).await?;
    }

    // Retrieve similar episodes
    let similar = memory.retrieve_similar(&base_id, 5).await?;
    assert_eq!(similar.len(), 5);
}
```

## Best Practices

1. **Use setup functions** - Centralize test memory initialization
2. **Clean up after tests** - Use `#[teardown]` or manual cleanup
3. **Test edge cases** - Empty episodes, failed operations
4. **Verify state transitions** - Ensure all lifecycle states work
5. **Mock embedding providers** - Faster, deterministic tests

## Common Patterns

- **Creating test episodes**: `create_test_episode()` helper
- **Mock storage**: `MockTursoStorage`, `MockRedbCache`
- **Embedding mocks**: `MockEmbeddingProvider`
- **Test fixtures**: `test-fixtures/` directory
