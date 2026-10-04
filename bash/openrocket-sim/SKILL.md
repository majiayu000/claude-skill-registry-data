---
name: openrocket-sim
category: aerospace
description: "Headless rocket design, simulation, and optimization using OpenRocket's Java core engine. Includes rocket-sim CLI tool for batch simulations and parameter sweeps, plus an AI-driven optimization loop using Claude. Use when: (1) designing model rockets programmatically, (2) running headless flight simulations, (3) optimizing rocket designs for altitude/stability/velocity, (4) batch-processing .ork files, (5) parameter sweeps over launch conditions, (6) AI-driven design optimization, (7) building a simulation pipeline or API wrapper, (8) exporting designs for 3D printing or laser cutting, (9) user mentions 'openrocket', 'rocket simulation', 'flight sim', 'rocket design', 'model rocket', 'rocketry', 'apogee optimization', 'thrust curve', 'rocket-sim'."
---

# OpenRocket Headless Simulation

## Quick Start — rocket-sim CLI

The `rocket-sim` CLI at `~/broomva/experiments/rocket-tools/` wraps OpenRocket's headless core. All output is structured JSON.

```bash
# Prerequisites: Java 17
export JAVA_HOME=/opt/homebrew/opt/openjdk@17/libexec/openjdk.jdk/Contents/Home

ROCKET="~/broomva/experiments/openrocket/core/src/main/resources/datafiles/examples/A simple model rocket.ork"

# Inspect rocket design
rocket-sim info "$ROCKET"

# Run simulation → JSON with altitude, velocity, mach, events
rocket-sim run "$ROCKET"

# Parameter sweep (rod_angle, rod_length, launch_altitude, wind_speed, time_step)
rocket-sim sweep "$ROCKET" wind_speed 0,2,5,8,10

# Flight event timeline
rocket-sim events "$ROCKET"
```

**Validated results** (A simple model rocket, A8-3 motor):
- Max altitude: 50.7m | Max velocity: 29.3 m/s | Mach: 0.086 | Flight time: 15.9s
- Events: Launch→Ignition→Liftoff→Burnout→Apogee→Ejection→Parachute→Ground

**Two stage high power rocket** (multi-branch):
- Max altitude: 677.6m | Max velocity: 159.1 m/s | Mach: 0.469 | Flight time: 64.0s

## AI Optimizer

At `~/broomva/experiments/rocket-ai/optimizer.py`. Iterative loop: Claude analyzes simulation results, proposes parameter sweeps, evaluates trade-offs, converges.

```bash
export ANTHROPIC_API_KEY=sk-...
cd ~/broomva/experiments/rocket-ai
python3 optimizer.py "path/to/rocket.ork" \
    --goal "Maximize altitude while keeping ground hit velocity under 10 m/s" \
    --iterations 5
```

Loop: baseline sim → Claude analysis → sweep proposal → run sweep → feed results back → refine → converge.

## Repository Layout

```
~/broomva/experiments/
├── openrocket/          # OpenRocket source (github.com/openrocket/openrocket)
│   ├── core/            # Headless simulation engine (Java 17, Gradle)
│   └── swing/           # GUI (optional)
├── rocket-tools/        # rocket-sim CLI (Gradle project, depends on core shadow JAR)
│   ├── rocket-sim       # Shell wrapper
│   └── src/main/java/rocket/cli/RocketCLI.java
└── rocket-ai/           # AI optimizer (Python + Anthropic SDK)
    └── optimizer.py
```

## Build from Scratch

```bash
export JAVA_HOME=/opt/homebrew/opt/openjdk@17/libexec/openjdk.jdk/Contents/Home
export PATH="$JAVA_HOME/bin:$PATH"

# 1. Build OpenRocket core + shadow JAR
cd ~/broomva/experiments/openrocket
./gradlew build -x test && ./gradlew shadowJar

# 2. Build rocket-sim CLI
cd ~/broomva/experiments/rocket-tools
./gradlew jar

# 3. Install AI optimizer deps
cd ~/broomva/experiments/rocket-ai
pip install -r requirements.txt
```

## Headless Java API

For programmatic use without the CLI, use `OpenRocketCore.initialize()`:

```java
import info.openrocket.core.startup.OpenRocketCore;

// One-line bootstrap (headless, no GUI)
OpenRocketCore.initialize();

// Load and simulate
var loader = new GeneralRocketLoader(new File("rocket.ork"));
var doc = loader.load();
var sim = doc.getSimulation(0);
sim.simulate();

FlightData data = sim.getSimulatedData();
data.getMaxAltitude();   // meters
data.getMaxVelocity();   // m/s
data.getFlightTime();    // seconds
```

System properties for faster startup:
```java
System.setProperty("openrocket.bypass.presets", "true");   // skip component DB
System.setProperty("openrocket.bypass.motors", "true");    // skip motor DB
```

## References

- [API Reference](references/api-reference.md) — Components, SimulationOptions, FlightData, optimization framework, scripting
- [Compounding Strategies](references/compounding.md) — CLI, web API, AI optimization, design language, manufacturing pipeline, SaaS

## Example .ork Files

At `openrocket/core/src/main/resources/datafiles/examples/`:
- `A simple model rocket.ork` — single stage, 5 motor configs
- `Two stage high power rocket.ork` — multi-stage, multi-branch sim
- `Clustered motors.ork` — parallel motor clusters
- `Simulation extensions.ork` — GraalVM JS scripting demo
- `Dual parachute deployment.ork` — recovery system demo
- `Parallel booster staging.ork` — side booster staging
