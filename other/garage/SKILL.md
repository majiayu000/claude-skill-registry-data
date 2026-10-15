---
name: garage
description: Generate agent performance visuals — watch faces, API gauges, failure states, livery presets. SVG and Unicode renderers for fleet status displays.
version: 0.1.0
execution-mode: advisory
argument-hint: "[watch \"agent_name\" --state executing | gauge \"agent_name\" --score 750 | livery \"agent_name\" --preset gulf | failure \"agent_name\" --state degraded]"
category: dev-tools
status: candidate
---
# HUMMBL Garage

Agent Performance Index (API), livery presets, watch faces, and failure aesthetics. Implements automotive + horology + kintsugi metaphors for agent status visualization.

## When to Use

- Rendering agent status as a watch face (analog clock metaphor)
- Generating API (Agent Performance Index) gauges (100-999 score)
- Applying racing livery presets (Martini, Gulf, JPS, Rothmans, Marlboro, Castrol)
- Visualizing failure states (degraded=wabi-sabi, broken=kintsugi, dead=death screen)
- Generating sparklines for activity history

## Usage

```bash
[garage] watch "devin" --state executing
[garage] gauge "devin" --score 750 --class B
[garage] livery "devin" --preset gulf
[garage] failure "devin" --state degraded
[garage] sparkline "devin" --data "1,3,2,5,4,6,5,7"
```

## Python API

```python
from hummbl_garage import (
    AgentPerformanceIndex,
    LiveryPresets,
    WatchFace,
    FailureState,
)

# API score (100-999, 6 sub-ratings)
api = AgentPerformanceIndex(
    agent_name="devin",
    score=750,
    sub_ratings={"speed": 80, "accuracy": 85, "coordination": 75, ...}
)

# Watch face (4-layer: analog hands, complications, dial finish, cockpit)
watch = WatchFace(agent_name="devin", state="executing")

# SVG rendering
from hummbl_garage.svg import render_watch_svg, render_api_gauge_svg
watch_svg = render_watch_svg(watch)
gauge_svg = render_api_gauge_svg(api)

# Unicode terminal rendering
from hummbl_garage.text import (
    render_watch_unicode,
    render_api_gauge_unicode,
    render_failure_state_unicode,
    render_sparkline,
)
watch_str = render_watch_unicode(watch)
gauge_str = render_api_gauge_unicode(api)
sparkline = render_sparkline([1, 3, 2, 5, 4, 6, 5, 7])
```

## Key Concepts

- **API (Agent Performance Index)**: 100-999 composite score with 6 sub-ratings (speed, accuracy, coordination, autonomy, reliability, trust)
- **Watch face states**: idle, planning, executing, verifying, blocked, offline
- **Livery presets**: Racing-inspired color schemes — Martini (red/blue/silver), Gulf (blue/orange), JPS (black/gold), etc.
- **Failure aesthetics**: degraded (wabi-sabi patina), broken (kintsugi gold seams), dead (death screen blue)
- **Goodhart mitigation**: Built-in gaming detection and held-out evaluation

## Install

```bash
cd /work/active/oss/packages/python/hummbl-garage
pip install -e ".[test]"
```

## Package

- **Repo**: `hummbl-io/oss`
- **Path**: `packages/python/hummbl-garage/`
- **License**: Apache 2.0
- **Dependencies**: stdlib only
