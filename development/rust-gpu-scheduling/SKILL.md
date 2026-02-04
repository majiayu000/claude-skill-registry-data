---
name: rust-gpu-scheduling
description: Implement GPU scheduling with VRAM budgets, work queues, and model lifecycle management. Use when building ML pipeline orchestrators.
---

# GPU Scheduling

VRAM-aware GPU scheduling for ML model orchestration.

## Model Types and VRAM Configuration

```rust
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub enum ModelType {
    Whisper = 0,    // 4.5 GB
    VideoMAE = 1,   // 5.0 GB
    CLAP = 2,       // 2.0 GB
    Qwen3 = 3,      // 1.5 GB
    DINOv3 = 4,     // 1.0 GB
}

#[derive(Debug, Clone)]
pub struct VramConfig {
    pub total_vram_gb: f64,      // e.g., 16.0
    pub safety_factor: f64,       // e.g., 0.9 (use 90%)
    pub whisper_vram_gb: f64,
    pub videomae_vram_gb: f64,
    pub clap_vram_gb: f64,
    pub qwen3_vram_gb: f64,
    pub dinov3_vram_gb: f64,
}

impl VramConfig {
    pub fn usable_vram_gb(&self) -> f64 {
        self.total_vram_gb * self.safety_factor
    }

    pub fn model_vram(&self, model: ModelType) -> f64 {
        match model {
            ModelType::Whisper => self.whisper_vram_gb,
            ModelType::VideoMAE => self.videomae_vram_gb,
            ModelType::CLAP => self.clap_vram_gb,
            ModelType::Qwen3 => self.qwen3_vram_gb,
            ModelType::DINOv3 => self.dinov3_vram_gb,
        }
    }

    pub fn can_fit(&self, model: ModelType) -> bool {
        self.model_vram(model) <= self.usable_vram_gb()
    }
}

impl Default for VramConfig {
    fn default() -> Self {
        Self {
            total_vram_gb: 16.0,
            safety_factor: 0.9,
            whisper_vram_gb: 4.5,
            videomae_vram_gb: 5.0,
            clap_vram_gb: 2.0,
            qwen3_vram_gb: 1.5,
            dinov3_vram_gb: 1.0,
        }
    }
}
```

## Work Item with Dependencies

```rust
use std::collections::HashSet;
use std::time::{SystemTime, UNIX_EPOCH};

#[derive(Debug, Clone)]
pub struct WorkItem {
    pub id: String,
    pub video_id: String,
    pub model_type: ModelType,
    pub input_data: String,
    pub priority: u32,
    pub dependencies: Vec<String>,
    pub submitted_at: f64,
    pub resolved_deps: HashSet<String>,
}

impl WorkItem {
    pub fn new(
        video_id: String,
        model_type: ModelType,
        input_data: String,
        dependencies: Option<Vec<String>>,
        priority: Option<u32>,
    ) -> Self {
        let id = format!("{}_{:?}_{}", video_id, model_type, uuid::Uuid::new_v4());

        Self {
            id,
            video_id,
            model_type,
            input_data,
            priority: priority.unwrap_or(0),
            dependencies: dependencies.unwrap_or_default(),
            submitted_at: SystemTime::now()
                .duration_since(UNIX_EPOCH)
                .map(|d| d.as_secs_f64())
                .unwrap_or(0.0),
            resolved_deps: HashSet::new(),
        }
    }

    pub fn is_ready(&self) -> bool {
        self.dependencies.iter()
            .all(|dep| self.resolved_deps.contains(dep))
    }

    pub fn resolve_dependency(&mut self, dep_id: &str) {
        self.resolved_deps.insert(dep_id.to_string());
    }

    pub fn waiting_time(&self) -> f64 {
        let now = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .map(|d| d.as_secs_f64())
            .unwrap_or(0.0);
        now - self.submitted_at
    }
}
```

## Work Queue with Priority

```rust
use std::collections::{HashMap, VecDeque};

pub struct WorkQueue {
    model_type: ModelType,
    ready_items: VecDeque<WorkItem>,
    waiting_items: Vec<WorkItem>,
}

impl WorkQueue {
    pub fn new(model_type: ModelType) -> Self {
        Self {
            model_type,
            ready_items: VecDeque::new(),
            waiting_items: Vec::new(),
        }
    }

    pub fn push(&mut self, item: WorkItem) {
        if item.is_ready() {
            // Insert by priority (higher priority first)
            let pos = self.ready_items
                .iter()
                .position(|i| i.priority < item.priority)
                .unwrap_or(self.ready_items.len());
            self.ready_items.insert(pos, item);
        } else {
            self.waiting_items.push(item);
        }
    }

    pub fn pop(&mut self) -> Option<WorkItem> {
        self.ready_items.pop_front()
    }

    pub fn resolve_dependency(&mut self, dep_id: &str) {
        let mut newly_ready = Vec::new();
        let mut i = 0;

        while i < self.waiting_items.len() {
            self.waiting_items[i].resolve_dependency(dep_id);

            if self.waiting_items[i].is_ready() {
                let item = self.waiting_items.swap_remove(i);
                newly_ready.push(item);
            } else {
                i += 1;
            }
        }

        for item in newly_ready {
            self.push(item);
        }
    }

    pub fn ready_count(&self) -> usize {
        self.ready_items.len()
    }

    pub fn waiting_count(&self) -> usize {
        self.waiting_items.len()
    }
}
```

## Model State Manager

```rust
use std::time::{Duration, Instant};

pub struct ModelStateManager {
    current_model: Option<ModelType>,
    loaded_at: Option<Instant>,
    load_counts: [u32; 5],
    last_load_times: [Option<Duration>; 5],
}

impl ModelStateManager {
    pub fn new() -> Self {
        Self {
            current_model: None,
            loaded_at: None,
            load_counts: [0; 5],
            last_load_times: [None; 5],
        }
    }

    pub fn mark_loaded(&mut self, model: ModelType, load_time: Duration) {
        self.current_model = Some(model);
        self.loaded_at = Some(Instant::now());
        self.load_counts[model as usize] += 1;
        self.last_load_times[model as usize] = Some(load_time);
    }

    pub fn mark_unloaded(&mut self) {
        self.current_model = None;
        self.loaded_at = None;
    }

    pub fn current_model(&self) -> Option<ModelType> {
        self.current_model
    }

    pub fn estimated_load_time(&self, model: ModelType) -> Duration {
        self.last_load_times[model as usize].unwrap_or_else(|| {
            // Default estimates
            match model {
                ModelType::Whisper => Duration::from_secs(5),
                ModelType::VideoMAE => Duration::from_secs(8),
                ModelType::CLAP => Duration::from_secs(4),
                ModelType::Qwen3 => Duration::from_secs(10),
                ModelType::DINOv3 => Duration::from_secs(6),
            }
        })
    }

    pub fn needs_switch(&self, target: ModelType) -> bool {
        self.current_model != Some(target)
    }
}
```

## GPU Scheduler

```rust
use parking_lot::RwLock;
use std::sync::Arc;

pub struct GPUScheduler {
    queues: Arc<RwLock<HashMap<ModelType, WorkQueue>>>,
    state: Arc<RwLock<ModelStateManager>>,
    vram_config: VramConfig,
}

impl GPUScheduler {
    pub fn new(vram_config: VramConfig) -> Self {
        let mut queues = HashMap::new();
        for model in [
            ModelType::Whisper,
            ModelType::VideoMAE,
            ModelType::CLAP,
            ModelType::Qwen3,
            ModelType::DINOv3,
        ] {
            queues.insert(model, WorkQueue::new(model));
        }

        Self {
            queues: Arc::new(RwLock::new(queues)),
            state: Arc::new(RwLock::new(ModelStateManager::new())),
            vram_config,
        }
    }

    pub fn submit(&self, item: WorkItem) -> String {
        let id = item.id.clone();
        let model = item.model_type;

        let mut queues = self.queues.write();
        if let Some(queue) = queues.get_mut(&model) {
            queue.push(item);
        }

        id
    }

    pub fn resolve_dependency(&self, dep_id: &str) {
        let mut queues = self.queues.write();
        for queue in queues.values_mut() {
            queue.resolve_dependency(dep_id);
        }
    }

    pub fn get_next_batch(&self, max_batch_size: usize) -> Option<(ModelType, Vec<WorkItem>)> {
        let state = self.state.read();
        let mut queues = self.queues.write();

        // Prefer current model to minimize switches
        if let Some(current) = state.current_model() {
            if let Some(queue) = queues.get_mut(&current) {
                if queue.ready_count() > 0 {
                    let mut batch = Vec::new();
                    while batch.len() < max_batch_size {
                        if let Some(item) = queue.pop() {
                            batch.push(item);
                        } else {
                            break;
                        }
                    }
                    if !batch.is_empty() {
                        return Some((current, batch));
                    }
                }
            }
        }

        // Find queue with most ready items
        let best_model = queues
            .iter()
            .filter(|(_, q)| q.ready_count() > 0)
            .max_by_key(|(_, q)| q.ready_count())
            .map(|(m, _)| *m);

        if let Some(model) = best_model {
            let queue = queues.get_mut(&model).unwrap();
            let mut batch = Vec::new();
            while batch.len() < max_batch_size {
                if let Some(item) = queue.pop() {
                    batch.push(item);
                } else {
                    break;
                }
            }
            if !batch.is_empty() {
                return Some((model, batch));
            }
        }

        None
    }

    pub fn total_pending(&self) -> usize {
        self.queues.read()
            .values()
            .map(|q| q.ready_count() + q.waiting_count())
            .sum()
    }
}
```

## Semaphore-Based VRAM Limiting

```rust
use tokio::sync::Semaphore;

// Alternative: Use semaphore for simpler VRAM tracking
pub struct VramSemaphore {
    semaphore: Semaphore,
    units_per_gb: u32,
}

impl VramSemaphore {
    pub fn new(total_gb: f64, units_per_gb: u32) -> Self {
        let total_units = (total_gb * units_per_gb as f64) as usize;
        Self {
            semaphore: Semaphore::new(total_units),
            units_per_gb,
        }
    }

    pub async fn acquire(&self, vram_gb: f64) -> Result<SemaphorePermit<'_>> {
        let units = (vram_gb * self.units_per_gb as f64) as u32;
        self.semaphore.acquire_many(units).await
            .map_err(|_| Error::VramAcquisition)
    }
}

// Usage
let vram = VramSemaphore::new(16.0, 10);  // 160 units total

async fn run_whisper(vram: &VramSemaphore) -> Result<()> {
    let _permit = vram.acquire(4.5).await?;  // 45 units
    // Run model - permit released on drop
    Ok(())
}
```

## Guidelines

- Track VRAM usage per model type
- Use safety factor (90%) to avoid OOM
- Minimize model switches (prefer current model)
- Support work item dependencies
- Use priority queues for important work
- Track model load times for scheduling decisions
- Use semaphores for simpler VRAM limiting

## Examples

See `hercules-local-algo/src/scheduler/` for complete implementation.
