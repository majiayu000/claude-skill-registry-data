---
name: egpu <<<<<<< HEAD
description: External GPU technology fundamentals, Thunderbolt bandwidth math, hotplug detection, workload migration, and Basin's eGPU infrastructure (basin-display, basin-gpu). Use when working with eGPU detection, GPU failover, Thunderbolt networking, or multi-GPU workload routing. >>>>>>> origin/main
---

# eGPU Skill

<<<<<<< HEAD
External GPU knowledge for hardware detection, bandwidth analysis, hotplug recovery, and Project's GPU infrastructure.
=======
External GPU knowledge for hardware detection, bandwidth analysis, hotplug recovery, and Basin's GPU infrastructure.
>>>>>>> origin/main

## Trigger Conditions

- User asks about eGPU, external GPU, or Thunderbolt GPU
- Working on GPU hotplug, device lifecycle, or workload migration
- Questions about Thunderbolt bandwidth, PCIe tunneling, or GPU enclosures
- Multi-GPU routing, failover, or compute offloading
- Apple Silicon eGPU limitations
<<<<<<< HEAD
- Project's `gpu-display/src/egpu.rs` or `gpu-runtime/src/workload_migrator.rs`
=======
- Basin's `basin-display/src/egpu.rs` or `basin-gpu/src/workload_migrator.rs`
>>>>>>> origin/main

## What Is an eGPU?

An **external GPU** (eGPU) is a desktop-class GPU housed in an external enclosure, connected to a computer via Thunderbolt. It tunnels PCIe over the Thunderbolt cable, giving laptops and compact machines access to high-end GPU compute.

### Physical Stack

```
┌────────────────────┐     Thunderbolt Cable     ┌──────────────────────┐
│  Host Computer     │  ◄═══════════════════════► │  eGPU Enclosure      │
│  (TB Controller)   │   PCIe tunneled over TB    │  (TB Controller)     │
│                    │                            │  ┌────────────────┐  │
│  CPU ◄── PCIe ──►  │                            │  │ Desktop GPU    │  │
│  iGPU              │                            │  │ (RTX 4090,     │  │
│                    │                            │  │  RX 7900 XTX,  │  │
│                    │                            │  │  etc.)         │  │
└────────────────────┘                            │  └────────────────┘  │
                                                  │  PSU (500-700W)     │
                                                  └──────────────────────┘
```

### Thunderbolt Bandwidth

| Version | Total BW | PCIe Tunneled | Effective GPU BW | PCIe Equivalent |
|---------|----------|---------------|------------------|-----------------|
| TB1     | 10 Gbps  | ~8 Gbps       | ~1.0 GB/s        | ~PCIe 2.0 x1    |
| TB2     | 20 Gbps  | ~16 Gbps      | ~2.0 GB/s        | ~PCIe 2.0 x2    |
| TB3     | 40 Gbps  | ~22 Gbps      | ~2.8 GB/s        | ~PCIe 3.0 x2    |
| TB4     | 40 Gbps  | ~22 Gbps      | ~2.8 GB/s        | ~PCIe 3.0 x2    |
| TB5     | 80 Gbps  | ~48 Gbps      | ~6.0 GB/s        | ~PCIe 4.0 x4    |

**Internal PCIe 4.0 x16 = ~32 GB/s** -- so even TB5 is ~5x less bandwidth than a slot.

### Performance Implications

**Compute-bound workloads** (shader-heavy, large VRAM working sets):
- eGPU performs at 85-95% of internal GPU
- Hash joins, e-graph saturation, matrix multiply, neural net inference

**Bandwidth-bound workloads** (constant CPU↔GPU data transfer):
- eGPU performs at 15-40% of internal GPU
- Small batch sizes, frequent readback, streaming data

**Rule of thumb**: If the GPU kernel runs >1ms per dispatch, the TB overhead is negligible.

## OS-Level Detection

### macOS (IOKit)

```
IORegistry hierarchy:
  AppleThunderboltNHIType4 (or Type3/Type5)
    └── IOThunderboltPort
        └── IOPCIDevice (GPU)
            └── AGXAccelerator or IOGPUDevice
```

- `is_egpu()` checks for `Thunderbolt` parent service in IORegistry
- TB version detected via `AppleThunderboltNHIType{1..5}` class name
- Metal API: `MTLDevice.isRemovable` (Intel Macs only)

**Apple Silicon note**: macOS officially dropped eGPU support on Apple Silicon. The TB hardware can still tunnel PCIe, but macOS won't render graphics to an external AMD/NVIDIA GPU. Compute-only use requires custom drivers.

### Linux (udev/DRM)

```bash
# Detect Thunderbolt devices
cat /sys/bus/thunderbolt/devices/*/device_name

# Check if GPU is on Thunderbolt bus
udevadm info /sys/class/drm/card1 | grep THUNDERBOLT

# DRM hotplug events
inotifywait /sys/class/drm/
```

- udev rules trigger on TB device add/remove
- DRM subsystem emits hotplug events
- sysfs: `/sys/bus/thunderbolt/devices/*/authorized`

### wgpu (Cross-Platform)

```rust
// wgpu device-lost callback
device.on_uncaptured_error(|error| {
    if matches!(error, wgpu::Error::DeviceLost { .. }) {
        // GPU disconnected - trigger migration
    }
});
```

<<<<<<< HEAD
## Project eGPU Infrastructure
=======
## Basin eGPU Infrastructure
>>>>>>> origin/main

### Key Files

| File | Purpose |
|------|---------|
<<<<<<< HEAD
| `crates/gpu-display/src/egpu.rs` | `EGpuManager`, `EGpuDevice`, `ThunderboltMesh`, `AppleSiliconEGpuInfo` |
| `crates/gpu-runtime/src/device_lifecycle.rs` | `GpuDeviceRegistry`, `GpuDeviceState`, health scoring, simulated GPU |
| `crates/gpu-runtime/src/workload_migrator.rs` | `WorkloadMigrator`, `MigrationConfig`, `MigrationStrategy` (Eager/Lazy/Preemptive/LoadBalanced) |
| `crates/gpu-runtime/src/workload_checkpoint.rs` | `CheckpointManager`, `Checkpointable` trait for GPU state snapshots |
| `foundation/hardware-layer/src/iokit.rs` | IOKit FFI for TB speed detection, `is_egpu()` |
=======
| `crates/basin-display/src/egpu.rs` | `EGpuManager`, `EGpuDevice`, `ThunderboltMesh`, `AppleSiliconEGpuInfo` |
| `crates/basin-gpu/src/device_lifecycle.rs` | `GpuDeviceRegistry`, `GpuDeviceState`, health scoring, simulated GPU |
| `crates/basin-gpu/src/workload_migrator.rs` | `WorkloadMigrator`, `MigrationConfig`, `MigrationStrategy` (Eager/Lazy/Preemptive/LoadBalanced) |
| `crates/basin-gpu/src/workload_checkpoint.rs` | `CheckpointManager`, `Checkpointable` trait for GPU state snapshots |
| `foundation/basin-hardware/src/iokit.rs` | IOKit FFI for TB speed detection, `is_egpu()` |
>>>>>>> origin/main
| `docs/design/EGPU_HOTPLUG_ROADMAP.md` | 5-phase implementation plan |

### Core Types

```rust
// EGpuDevice - full device info
pub struct EGpuDevice {
    pub gpu: GpuDevice,
    pub enclosure_name: Option<String>,
    pub thunderbolt_port: u8,
    pub thunderbolt_speed: ThunderboltSpeed,  // TB1..TB5
    pub power_delivery_watts: Option<u32>,
    pub power_state: EGpuPowerState,          // Active/Idle/Suspended/Disconnected
    pub has_displays: bool,
    pub display_ids: Vec<DisplayId>,
}

// EGpuEvent - hotplug lifecycle
pub enum EGpuEvent {
    Connected { device, thunderbolt_port },
    Disconnected { device_id, thunderbolt_port, graceful },
    LinkSpeedChanged { device_id, old_speed, new_speed },
    PowerStateChanged { device_id, state },
    MigrationStarted { device_id, target_gpu },
    MigrationCompleted { device_id, target_gpu, duration_ms },
}

// ThunderboltSpeed - link speed enum
pub enum ThunderboltSpeed { TB1, TB2, TB3, TB4, TB5 }
```

### EGpuManager Usage

```rust
<<<<<<< HEAD
use gpu_display::egpu::EGpuManager;
=======
use basin_display::egpu::EGpuManager;
>>>>>>> origin/main

let manager = EGpuManager::new();  // Auto-enumerates
manager.start_monitoring()?;       // Hotplug events

// Register callback
manager.on_event(Box::new(|event| match event {
    EGpuEvent::Disconnected { device_id, graceful, .. } => {
        if !graceful {
            // Surprise disconnect - trigger migration
        }
    }
    _ => {}
}));

// Safe disconnect (migrates workloads first)
manager.safe_disconnect(gpu_id)?;
```

### Workload Migration

```rust
<<<<<<< HEAD
use gpu_runtime::workload_migrator::{WorkloadMigrator, MigrationConfig, MigrationStrategy};
=======
use basin_gpu::workload_migrator::{WorkloadMigrator, MigrationConfig, MigrationStrategy};
>>>>>>> origin/main

let config = MigrationConfig {
    strategy: MigrationStrategy::Eager,
    max_concurrent_migrations: 4,
    migration_timeout: Duration::from_secs(30),
    prefer_cpu_fallback: true,
    ..Default::default()
};

// Migration flow:
// 1. GPU disconnect detected (device_lifecycle callback)
// 2. WorkloadMigrator::on_device_failure called
// 3. Checkpoint GPU state (buffers, compute state)
// 4. Select target device (integrated GPU, another eGPU, or CPU)
// 5. Restore state on target
// 6. Resume execution from checkpoint
```

### Migration Strategies

| Strategy | When | Tradeoff |
|----------|------|----------|
| **Eager** | Migrate on first warning (high temp, low memory) | More migrations, faster recovery |
| **Lazy** | Only migrate on device failure | Fewer migrations, risk of data loss |
| **Preemptive** | Predict failures, migrate in advance | Best UX, complex implementation |
| **LoadBalanced** | Distribute across all available devices | Best throughput, more complexity |

### Thunderbolt Mesh Networking

<<<<<<< HEAD
Project supports TB mesh networking for GPU cluster communication (IP over Thunderbolt):

```rust
use gpu_display::egpu::ThunderboltMesh;
=======
Basin supports TB mesh networking for GPU cluster communication (IP over Thunderbolt):

```rust
use basin_display::egpu::ThunderboltMesh;
>>>>>>> origin/main

let mesh = ThunderboltMesh::discover()?;
println!("Active peers: {}", mesh.active_peer_count());
println!("Aggregate bandwidth: {} Gbps", mesh.total_bandwidth_gbps);

if let Some(best) = mesh.best_peer() {
    // Lowest latency peer for frame streaming
    println!("{} @ {}us latency", best.hostname, best.latency_us);
}
```

<<<<<<< HEAD
## Implementation Status (Project)
=======
## Implementation Status (Basin)
>>>>>>> origin/main

| Component | Status |
|-----------|--------|
| Hardware detection (IOKit/udev) | **Complete** |
| TB speed detection (TB1-TB5) | **Complete** |
| eGPU detection (`is_egpu()`) | **Complete** |
| GPU vendor routing (Metal/wgpu/CUDA) | **Complete** |
| EGpuManager + events | **Complete** |
| Device lifecycle registry | **Skeleton** |
| Workload migration | **Missing** (types exist, execution not wired) |
| State checkpointing | **Missing** |
| GPU passthrough for VMs | **Missing** |

See `docs/design/EGPU_HOTPLUG_ROADMAP.md` for the 5-phase plan.

## Common eGPU Enclosures

| Enclosure | GPU Support | TB Version | Power | Notes |
|-----------|------------|------------|-------|-------|
| Razer Core X | Full-length, 3-slot | TB3 | 650W PSU | Most popular |
| Sonnet Breakaway | Full-length, 2-slot | TB3 | 550W PSU | Mac-optimized |
| Mantiz Saturn Pro | Full-length, 2-slot | TB3 | 550W PSU | Built-in hub |
| ASUS XG Station Pro | Full-length, 2.5-slot | TB3 | 330W PSU | Compact |

## When to Use eGPU vs Cloud GPU

| Factor | eGPU | Cloud GPU (A100/H100) |
|--------|------|----------------------|
| Latency | <1ms (local TB) | 1-50ms (network) |
| Bandwidth | 2.8-6.0 GB/s | Network-limited |
| Cost | One-time ($300-2000) | Per-hour ($1-30/hr) |
| Availability | Always on | Capacity-dependent |
| VRAM | Consumer (8-24GB) | Enterprise (40-80GB) |
| Best for | Dev/test, small models | Training, large models |
